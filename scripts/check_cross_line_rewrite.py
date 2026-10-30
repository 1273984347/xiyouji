r"""check_cross_line_rewrite.py — 同族扫描：改写面正则的「跨行静默删内容」风险清单

病根（W1005 实证）：Python 字符类 `[^X]` **匹配换行符**、`\s` 亦然 ⇒ 若某条正则的匹配段写成
`[^X]*` 且**无紧跟的尾锚点**，其匹配区间可跨行；`re.sub` 替换的是**整个匹配区间** ⇒ 跨行匹配
等于静默删掉中间行的内容，且往往仍报「自检全通过」。

本扫描器（**报告型**·不改任何文件）分三档输出：
  🔴 改写面高危：调用 re.sub / re.subn 且模式含 `[^…]*`/`[^…]+` 且**无尾锚点**
  🟡 改写面可疑：模式含 `[^…]*` 但有尾锚点（锚点是否紧跟需人工确认）
  ⚪ 只读面：仅 search/findall/match（跨行只致 fail-closed 误报，不产生破坏）

「尾锚点」判定：同一模式串中，`[^…]*` 之后**紧邻**出现非字符类的字面量（`·`/`—`/中文/标点）
⇒ 视为有锚点（仍可能跨行吃到别处，标 🟡 供人工确认）。

扫描范围：scripts/ 全树（含 archive/scripts/ 归档区——归档件若被恢复使用会带病）。
用法：py -3 scripts/check_cross_line_rewrite.py [--json]
"""
from __future__ import annotations

import ast
import hashlib
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIRS = [os.path.join(ROOT, "scripts"),
             os.path.join(ROOT, "archive", "scripts")]
SKIP_DIR_PARTS = {"__pycache__", "node_modules", ".git", "tmpe"}

# 匹配段形如 [^X]* 或 [^X]+（X 非换行）
RE_NEGCLASS_STAR = re.compile(r"\[\^([^\]]+)\][*+]")
# 字面量锚点候选（非 \w 非空白的中日韩/标点/间隔号等）
RE_LITERAL_ANCHOR = re.compile(r"[·—、：:;；,，。「」『』《》【】（）()\[\]{}!?！？\"'`|/\\=><^~@#$%&*+=]")


def _pattern_of(node):
    """取 re.sub/search 的第一个参数（模式）。支持字符串常量与拼接。"""
    if node is None:
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a = _pattern_of(node.left)
        b = _pattern_of(node.right)
        if a is not None and b is not None:
            return a + b
    if isinstance(node, ast.JoinedStr):
        return None      # f-string 模式 ⇒ 静态不可判 ⇒ 交人工
    return None


def _can_cross_line(pat):
    """模式里是否存在**可跨行**的 `[^X]*` 匹配段。

    关键判定：字符类的**排除符**里若含 `\\n` / `\\r`（转义形式），该类**不匹配换行** ⇒ 安全。
    ⇒ `[^\n]*` / `[^\r\n]*` **不会跨行**（首测把 `//[^\n]*` 误报为高危即源于此）。

    W1045 修（archive 域 129 处复核的判据盲区）：**`\\s` 也排除换行**（`\\s` = 空格 + 制表 +
    换行 + 回车 + 换页 + 垂直制表）⇒ 排除符含 `\\s` 的字符类同样**不跨行**。
    原实现未识别 ⇒ `_w616_zhuangshi_folder.py:92` 被误判为可跨行（实测不可跨行）。
    """
    for m in RE_NEGCLASS_STAR.finditer(pat):
        excl = m.group(1)
        if "\\n" in excl or "\\r" in excl or "\\s" in excl:
            continue          # 该字符类排除换行 ⇒ 整条模式不跨行（就此段而言）
        return True
    return False


def _has_tail_anchor(pat):
    """`[^…]*` 之后是否紧跟字面量锚点（**仅作提示·不可当安全依据**）。

    W1042 复核实证（43 处逐处人工复核·子代理 verifier）：**尾锚点只约束匹配的末端，
    不约束匹配内部** —— `[^X]` 只排除 X，**不排除换行**。实测 `build_reader.py:205`
    在 832 个 md 上确有 1 处真实跨行匹配（仅因替换回原内容才无害）。
    ⇒ 本函数仅用于**分级展示**，绝不参与「是否高危」的判定。
    """
    for m in RE_NEGCLASS_STAR.finditer(pat):
        excl = m.group(1)
        if "\\n" in excl or "\\r" in excl or "\\s" in excl:
            continue
        tail = pat[m.end():]
        if tail and RE_LITERAL_ANCHOR.search(tail[:2]):
            return True
    return False


def _replacement_of(node):
    """取 re.sub/subn 的**替换参数**（第 2 个位置参数 · `re.sub(pattern, repl, string)`）。

    W1042 自测盲区实证：首版误取第 3 个参数（那是 **string**）⇒ 全部调用被判
    `unknown` ⇒ 高危档恒为空（假绿）。⇒ 该位次由 AST 级自测钉死（⑨–⑪ 例）。
    """
    if len(node.args) >= 2:
        return _pattern_of(node.args[1])
    for kw in node.keywords:
        if kw.arg == "repl":
            return _pattern_of(kw.value)
    return None


RE_BACKREF = re.compile(r"\\\d|\\g<")

# 已人工复核确认「无害」的候选基线（键 = 文件:行）。
# W1042 引入：静态判据无法判定「替换结果是否真被消费」（写回磁盘 / 返回给调用者 /
# 仅用于检查）⇒ 危害性需人工确认 + 现场实测 ⇒ 确认结论落基线文件，
# 门禁只对**基线之外的新增候选**判红（防复发·不冻结既有面）。
BASELINE_PATH = os.path.join(ROOT, "scripts", "cross_line_baseline.json")


def _item_key(item):
    """基线键 = sha256(文件 + **完整模式** + **完整替换串** + 行号)，前 12 位。

    W1043 轮改过一次（行号 → 内容指纹）⇒ **堵死**了「原地改写/行号位移静默豁免」，
    但 W1045 轮对抗审查**实测出三类新残余豁免**（仓外沙箱 A/B 实证）：
      ① 同文件**新增同模式调用点** ⇒ 纯内容指纹碰撞 ⇒ 漏拦；
      ② 替换串**语义变更**（`""` → `"REPLACED"`）而 `repl` 三分类不变 ⇒ 键不变 ⇒ 漏拦；
      ③ 模式 >160 字符被**截断**后参与计算 ⇒ 不同模式可能撞键。

    ⇒ 本版把「键的四个输入」定为：文件 + 完整模式 + 完整替换串 + 行号：
      · 原地改写 ⇒ 模式/替换串变 ⇒ 换键 ✓
      · 替换串语义变更 ⇒ 换键 ✓
      · 模式超长 ⇒ **不截断**（截断只用于显示）⇒ 不撞键 ✓
      · 同文件新增同模式调用点 ⇒ 行号不同 ⇒ 换键 ✓
      · 行号漂移（上方增删行）⇒ 换键 ⇒ **报「基线外新增」**（宁可多报·安全侧：
        人来确认一次，比静默豁免真缺陷便宜得多）
    """
    sig = hashlib.sha256(
        ("%s|%s|%s|%d" % (item["file"], item["pattern_full"], item["repl_full"], item["line"]))
        .encode("utf-8")).hexdigest()[:12]
    return "%s#%s" % (item["file"], sig)


def _load_baseline():
    if not os.path.exists(BASELINE_PATH):
        return set()
    try:
        data = json.load(io.open(BASELINE_PATH, encoding="utf-8"))
        return set(data.get("confirmed", []))
    except Exception:  # noqa: BLE001
        return set()


def _write_baseline(keys):
    """写基线（**不写生成时间戳**——否则每次跑都变·门禁跑完须 add 还不收敛）。

    键口径（W1045 订正）：`文件#sha256(完整模式|完整替换串|行号)` 前 12 位 ⇒
    原地改写 / 替换串语义变更 / 同文件新增同模式调用点 / 模式超长截断 **四类漏拦
    路径全部换键**；行号漂移亦换键 ⇒ 报「基线外新增」（宁可多报·安全侧）。
    """
    payload = {
        "note": "已人工复核确认「跨行匹配但无害」的候选清单（键 = 文件#内容指纹）。"
                "危害性取决于替换结果是否真被消费（写回磁盘 / 返回给调用方并被后续使用 / "
                "仅用于检查），静态判据到不了这一轴 ⇒ 以复核结论为准。"
                "键口径：sha256(完整模式|完整替换串|行号) 前 12 位——"
                "原地改写、替换串语义变更、同文件新增同模式调用点、模式超长截断 四类漏拦路径均换键；"
                "行号漂移亦换键 ⇒ 报「基线外新增」（宁可多报·安全侧）。",
        "confirmed": sorted(keys),
    }
    txt = json.dumps(payload, ensure_ascii=False, indent=1) + "\n"
    tmp = BASELINE_PATH + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(txt.encode("utf-8"))
    os.replace(tmp, BASELINE_PATH)


def _repl_kind_of_literal(rep):
    """按**替换字面量**分类：None ⇒ unknown（静态不可判）· 含回引 ⇒ backref · 否则 fixed。"""
    if rep is None:
        return "unknown"
    if RE_BACKREF.search(rep):
        return "backref"
    return "fixed"


def _replacement_kind(node):
    r"""替换语义分类 —— **危害的真正来源**。

    W1042 复核实证：
      · 替换为**固定串/空串** ⇒ 跨行匹配会把匹配段（连同其间内容）**整段删掉** ⇒ 危险；
      · 替换**回原内容**（含 `\1` / `\g<1>` 回引）⇒ 即使跨行匹配，匹配内容被原样回写
        ⇒ 不删内容（但匹配范围可能过大，仍需人工确认）。
      · 替换为**函数**（第 2 参数不可静态求值）⇒ 静态不可判 ⇒ 按最坏处理并标注「待人工」。

    返回 'fixed' | 'backref' | 'unknown'
    """
    return _repl_kind_of_literal(_replacement_of(node))


def scan():
    high, mid, low, skipped = [], [], [], []
    for base in SCAN_DIRS:
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_DIR_PARTS]
            for fn in files:
                if not fn.endswith(".py"):
                    continue
                p = os.path.join(root, fn)
                rel = os.path.relpath(p, ROOT).replace("\\", "/")
                try:
                    src = open(p, encoding="utf-8").read()
                    tree = ast.parse(src)
                except Exception as e:  # noqa: BLE001
                    skipped.append((rel, "解析失败：%r" % (e,)))
                    continue
                for node in ast.walk(tree):
                    if not isinstance(node, ast.Call):
                        continue
                    fn_name = None
                    if isinstance(node.func, ast.Attribute):
                        fn_name = node.func.attr
                    elif isinstance(node.func, ast.Name):
                        fn_name = node.func.id
                    if fn_name not in ("sub", "subn", "search", "findall", "finditer", "match", "fullmatch"):
                        continue
                    if not node.args:
                        continue
                    pat = _pattern_of(node.args[0])
                    if pat is None:
                        continue
                    if not RE_NEGCLASS_STAR.search(pat):
                        continue
                    cross = _can_cross_line(pat)
                    _rep = _replacement_of(node)
                    item = {"file": rel, "line": node.lineno,
                            "func": fn_name, "pattern": pat[:160],
                            # 键计算用**未截断**的模式与替换串（W1045 对抗审查 P2-2：
                            # 显示截断参与计算 ⇒ 不同模式撞键 ⇒ 漏拦）
                            "pattern_full": pat,
                            "repl_full": _rep if _rep is not None else "<fstring-or-unknown>",
                            "cross": cross, "anchor": _has_tail_anchor(pat),
                            "repl": _replacement_kind(node)}
                    if fn_name in ("sub", "subn"):
                        if not cross:
                            continue          # 排除符含 \n ⇒ 不跨行 ⇒ 安全
                        # W1042 判据升级：尾锚点**不再**作为「非高危」依据
                        # （尾锚点只约束匹配末端，不约束匹配内部 ⇒ 仍可跨行）；
                        # 真正的分界是**替换语义**：替换为固定串/空串 ⇒ 跨行即真删。
                        if item["repl"] == "fixed":
                            high.append(item)          # 跨行 × 固定串 ⇒ 真删 ⇒ 高危
                        else:
                            mid.append(item)           # 回原内容/函数替换 ⇒ 需人工确认
                    else:
                        if not cross:
                            continue          # 只读面且不跨行 ⇒ 无需列
                        low.append(item)
    return high, mid, low, skipped


def _repl_kind_of_call(src):
    """AST 级：解析源码片段，取其中第一个 re.sub 调用的替换语义分类（自测用）。"""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
            if name in ("sub", "subn"):
                return _replacement_kind(node)
    return None


def _self_test():
    """8 例负样本自证（判据可证伪性）：高危必抓 · 安全形态必不报。

    W1042 判据升级：新增**替换语义**维度（fixed / backref / unknown），
    并废除「尾锚点 ⇒ 非高危」的旧依据（尾锚点只约束匹配末端·不约束匹配内部）。
    """
    cases = []

    def add(name, cond, detail=""):
        cases.append((name, bool(cond), detail))

    # ① 经典高危：`[^·]*` 无尾锚点 ⇒ 可跨行 ⇒ 必须判高危
    add("① 经典高危（`[^·]*` 无锚点）→ 判高危",
        _can_cross_line("[^·]*") and not _has_tail_anchor("[^·]*"),
        "cross=%s anchor=%s" % (_can_cross_line("[^·]*"), _has_tail_anchor("[^·]*")))
    # ② 排除符含 \n ⇒ 该字符类不跨行 ⇒ 必须不判高危（首测即把 `//[^\n]*` 误报为高危）
    add("② 排除符含 \\n（`[^\\n]*`）→ 不判高危",
        not _can_cross_line(r"//[^\n]*"),
        "cross=%s" % _can_cross_line(r"//[^\n]*"))
    # ③ 行锚定形态（W1005 修法）：`[^\n\r·]*·A1-A6` ⇒ 不跨行 ⇒ 必须不判高危
    add("③ 行锚定形态（`[^\\n\\r·]*·A1-A6`）→ 不判高危",
        not _can_cross_line(r"[^\n\r·]*·A1-A6"),
        "cross=%s" % _can_cross_line(r"[^\n\r·]*·A1-A6"))
    # ④ 有紧跟字面量锚点的可跨行形态 ⇒ 锚点存在（仅提示·不作安全依据）
    add("④ 可跨行但有紧跟锚点（`[^）]*）`）→ 锚点存在（仅提示）",
        _can_cross_line("（[^）]*）") and _has_tail_anchor("（[^）]*）"),
        "cross=%s anchor=%s" % (_can_cross_line("（[^）]*）"), _has_tail_anchor("（[^）]*）")))
    # ⑤ 替换语义分类：空串 ⇒ fixed（真删型）
    add("⑤ 替换为空串 ⇒ 判 fixed（跨行即真删）",
        _repl_kind_of_literal("") == "fixed")
    # ⑥ 替换语义分类：含 `\1` 回引 ⇒ backref（回原内容）
    add("⑥ 替换含 `\\1` 回引 ⇒ 判 backref（不删内容）",
        _repl_kind_of_literal(r"\g<1>标题") == "backref")
    # ⑦ 替换语义分类：f-string（静态不可求值）⇒ unknown
    add("⑦ 替换为 f-string ⇒ 判 unknown（按最坏处理并标注待人工）",
        _repl_kind_of_literal(None) == "unknown")
    # ⑧ 判据升级的**核心负样本**：带尾锚点但替换为固定串 ⇒ **必须判高危**
    #   （W1042 实证：`章节切分.py` 的 `!\[[^\]]*\]\([^)]*\)` 与 `<[^>]+>`
    #     旧版因「有尾锚点」被判可疑 ⇒ 全仓「高危 0 处」是假结论）
    add("⑧ 带尾锚点但替换为空串 ⇒ 判高危（尾锚点不再当安全依据）",
        _can_cross_line(r"!\[[^\]]*\]\([^)]*\)") and _has_tail_anchor(r"!\[[^\]]*\]\([^)]*\)")
        and _repl_kind_of_literal("") == "fixed")
    # ⑨⑩⑪ AST 级：替换参数的**位次**必须钉死（`re.sub(pattern, repl, string)` 的
    #      repl 是第 2 个）——首版误取第 3 个（= string）⇒ 全仓高危恒为空（假绿），
    #      而字面量级自测照绿 ⇒ 覆盖盲区在此补齐。
    add("⑨ AST 级：repl 取第 2 个参数（空串 ⇒ fixed）",
        _repl_kind_of_call('re.sub(r"<[^>]+>", "", text)') == "fixed")
    add("⑩ AST 级：repl 含回引 ⇒ backref",
        _repl_kind_of_call('re.sub(r"<[^>]+>", r"\\g<0>", text)') == "backref")
    add("⑪ AST 级：repl 为函数 ⇒ unknown（静态不可判）",
        _repl_kind_of_call('re.sub(r"<[^>]+>", lambda m: m.group(0), text)') == "unknown")

    # ⑫ 排除符含 `\s` ⇒ `\s` 亦排除换行 ⇒ **不跨行**（W1045 archive 域 129 处复核的判据盲区：
    #     原实现未识别 `\s` ⇒ `_w616_zhuangshi_folder.py:92` 被误判可跨行·实测不可跨行）
    add("⑫ 排除符含 `\\s` ⇒ 判不跨行（`\\s` 亦排除换行）",
        not _can_cross_line(r"[^\s]*"),
        "cross=%s" % _can_cross_line(r"[^\s]*"))

    ok = True
    for name, passed, detail in cases:
        print("  %s %s%s" % ("PASS" if passed else "FAIL", name, ("  [%s]" % detail) if detail else ""))
        ok = ok and passed
    print("SELF_TEST_%s（%d/%d 例通过）" % ("OK" if ok else "FAIL", sum(1 for _, p, _ in cases if p), len(cases)))
    return 0 if ok else 1


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()
    high, mid, low, skipped = scan()
    print("== 改写面高危（可跨行 `[^…]*` × 替换为固定串/空串 ⇒ 匹配段连同其间内容被整段删掉）==")
    for it in high:
        print("  [RED ] %s:%d  re.%s  repl=%s  pattern=%r"
              % (it["file"], it["line"], it["func"], it["repl"], it["pattern"]))
    print("   共 %d 处" % len(high))
    print("\n== 改写面可疑（可跨行 × 替换回原内容/函数替换 ⇒ 匹配段被原样回写·仍需人工确认匹配范围）==")
    for it in mid:
        print("  [YELL] %s:%d  re.%s  repl=%s  pattern=%r"
              % (it["file"], it["line"], it["func"], it["repl"], it["pattern"]))
    print("   共 %d 处" % len(mid))
    # W1043 对抗审查 P1-3：mid 桶里 **re.sub/subn 是改写面**（会改写原文），而 repl=unknown
    # （f-string / 变量替换）时**静态判不出是删还是留** ⇒ 危害面被静默放大。
    # ⇒ 本批不把它推成高危（112 处未逐处人工复核·推高危会把未复核面直接豁免进基线），
    #    但**必须可见**：单独计数并明示「人工复核队列」。
    mid_rw = [it for it in mid if it["func"] in ("sub", "subn")]
    if mid_rw:
        unk = [it for it in mid_rw if it["repl"] == "unknown"]
        print("   ⚠ 其中属**改写面**（re.sub/subn）的 %d 处（repl=unknown·静态判不出删留·"
              "**人工复核队列**）：%d 处" % (len(mid_rw), len(unk)))
    print("\n== 只读面（search/findall/match·跨行只致 fail-closed 误报·不产生破坏）==")
    for it in low:
        print("  [RO ] %s:%d  re.%s  pattern=%r" % (it["file"], it["line"], it["func"], it["pattern"]))
    print("   共 %d 处" % len(low))
    if skipped:
        print("\n== 跳过（解析失败）==")
        for rel, why in skipped:
            print("  [SKIP] %s · %s" % (rel, why))
    if "--json" in sys.argv:
        print(json.dumps({"high": high, "mid": mid, "low": low}, ensure_ascii=False, indent=1))

    # ---- 门禁模式：改写面高危必须为 0（W1005 修复后的常驻防线）----
    # ---- 门禁模式：基线之外的新增跨行删改候选必须为 0（W1042 判据升级）----
    if "--update-baseline" in sys.argv:
        _write_baseline({_item_key(it) for it in high})
        print("OK    基线已更新 · 确认清单 %d 项 → %s" % (len(high), BASELINE_PATH))
        return 0
    if "--gate" in sys.argv:
        base = _load_baseline()
        cur = {_item_key(it): it for it in high}
        new_keys = sorted(k for k in cur if k not in base)
        stale = sorted(k for k in base if k not in cur)
        if new_keys:
            print("FAIL  改写面高危候选 %d 处为基线之外的新增（可跨行 `[^…]*` × 替换为固定串/空串）"
                  % len(new_keys))
            for k in new_keys:
                it = cur[k]
                print("  extra: %s  re.%s  repl=%s  pattern=%r" % (k, it["func"], it["repl"], it["pattern"]))
            print("       处理：① 确认无害 ⇒ py -3 scripts/check_cross_line_rewrite.py --update-baseline"
                  "（须人工复核过）② 有害 ⇒ 把排除符补 \\n\\r")
            print("---- 跨行改写门禁：1 FAIL ----")
            return 1
        print("NOTE  改写面高危候选 %d 处（全部已在人工复核基线内·新增 0 处）·可跨行但替换回原内容"
              "的可疑 %d 处·只读面 %d 处" % (len(cur), len(mid), len(low)))
        if stale:
            print("NOTE  基线中已不存在的条目 %d 项（代码已改/已修）⇒ 可清理：%s"
                  % (len(stale), "、".join(stale[:5])))
        print("---- 跨行改写门禁：0 FAIL ----")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
