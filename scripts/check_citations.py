#!/usr/bin/env python3
"""原著引文硬验证（W503 第 20 门禁·W737 扩展三检）：规范引文行 + 归属对白 + 语料保真。

三项检查（--dir 门禁模式全跑；--file 单文件模式只跑前两项）：

1. **规范引文行**（W503 原始职能·文档规范 §4.8）：
       > 原文引文（第N回）：“……”
   - N ∈ 1-100；引号全角；引文单行，必须是 dataset/text-search.json chapters[N-1].text 的子串。
   - 归一规则：比较前双方去除全部空白（re.sub(r'\\s+','')，兼容原文换行）；除此之外逐字精确。
   - 禁止省略号节引——需节引时拆成多条引文行；每条引文独立命中。
   - 任何文档中任一引文行未命中 = FAIL（存量锚定引文行实测为 0，无历史豁免）。
   - 防静默跳过（2026-09-27 A 轨审查 ISSUE-001 加固）：凡以「原文引文」起始、却未匹配
     规范语法（`> 原文引文（第N回）：`）的行，一律 FAIL——堵死"格式漂移整行不进分母、
     报 100% 实为空真"的盲区（实证：匿名稿 3 条引文行因回目号带空格+半角引号曾长期被跳过）。
     疑似判定容忍常见漂移前缀：`>原文引文`、`> **原文引文` 等（2026-09-27 二档加固）。

2. **归属对白行**（W737 新增·对抗性审查 F-1 修复）：`X道：「……」` / `X道：“……”` 形态
   （说话人 ≤12 字 + 对白 ≥6 字）断言「角色说了这句原文」——必须在原著**全文**（任一回）中
   精确命中（去空白归一·与检查 1 同标准）。允许跨回引用（评论文 legitimately 引他回对白），
   失败消息标注所在文档回次供定位。
   - **豁免区**：① `## 原文全文` 照录区（原文照搬·非核验对象）；② 【文学演绎】标记区
     （文档规范 §4.12·标记行之后的节内内容——虚构叙事·其引号内容按规不构成原文引文）。
   - W737 实证背景：修复前「名句赏析」57 条归属引文 31 条（54%）两语料均不存在
     （虚构台词/静默删改/跨回误植）——原门禁语法族覆盖不到此形态，详见
     docs/11-报告复盘/对抗性审查报告-2026-10-14.md。

3. **语料保真检**（W737 新增·对抗性审查 F-2 修复）：text-search.json 各回 text 必须与
   source/原文/分回/第NNN回.md（剥离去头 `#` 标题行、截除「单字解释」附录、去空白归一）
   **逐回全等**——引文门禁的唯一事实源自身须有机器对账（BL-19/W691 裁决的权威源不变式）。
   W737 实证背景：修复前 100/100 回漂移（分回转换丢段 7 处 + 僻字降级 + 字级差异），
   已按「分回保内容完整 + 旧 json 清字基准」仲裁重建（7 丢段恢复/僻字还原/87 字级对齐）。

自检（--self-test）：内存正负样本覆盖三检的判定行为与豁免语义（含语料篡改负样本），防规则回归。

用法：
  python scripts/check_citations.py --file <md>   # 单文件（检查 1+2）
  python scripts/check_citations.py --dir docs/   # 目录全量（检查 1+2+3·门禁模式）
  python scripts/check_citations.py --check-corpus  # 只跑语料保真检
  python scripts/check_citations.py --self-test   # 自检（不依赖外部文档）
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_SEARCH = os.path.join(ROOT, "dataset", "text-search.json")
FENHUI_DIR = os.path.join(ROOT, "source", "原文", "分回")
CITE_RE = re.compile(r"^> 原文引文（第(\d+)回）：(.*)$")
SUSPECT_RE = re.compile(r"^>?\s*(?:\*\*)?\s*原文引文")
# 归属对白：说话人（≤12 字·不含逗句号冒号换行）+ 道： + 全角引号对白（≥6 字）
ATTRIB_RE = re.compile(r"[^，。：:\n]{0,12}道[：:]\s*[“「]([^”」]{6,})[”」]")
HEADING_RE = re.compile(r"^(#{1,6})\s+")
FICTION_MARK = "【文学演绎】"  # 文档规范 §4.12 演绎标记（节首 blockquote 行）
FULLTEXT_HEAD = "原文全文"     # 原文照录区标题前缀


def norm(s):
    return re.sub(r"\s+", "", s)


def load_chapters():
    d = json.load(open(TEXT_SEARCH, encoding="utf-8"))
    chs = {}
    for c in d["chapters"]:
        chs[int(c["num"])] = norm(c["text"])
    return chs


def load_doc_ignores():
    """从 .gitignore 提取 docs/ 下的字面忽略路径（目录前缀/文件全名）——门禁只治理入库内容，
    本地工作区（S2/S3/S4 等 gitignored 目录）不进门禁分母（W737：外购论文/本地稿不属仓内容）。"""
    prefixes, files = [], set()
    try:
        with open(os.path.join(ROOT, ".gitignore"), encoding="utf-8") as f:
            for ln in f:
                s = ln.strip()
                if not s or s.startswith("#") or not s.startswith("docs/"):
                    continue
                if any(ch in s for ch in "*?["):
                    continue  # 通配形态不猜解
                if s.endswith("/"):
                    prefixes.append(s)
                else:
                    files.add(s)
    except OSError:
        pass
    return prefixes, files


def is_ignored(rel, prefixes, files):
    rel = rel.replace(os.sep, "/")
    if rel in files:
        return True
    return any(rel.startswith(p) for p in prefixes)


def doc_chapter_num(path, text):
    """文档回次（chapter-meta num 优先·文件名 第NNN回 次之）——仅用于失败消息定位。"""
    m = re.search(r'chapter-meta:\s*\{\s*"num":\s*(\d+)', text)
    if m:
        return int(m.group(1))
    m = re.search(r"第(\d+)回", os.path.basename(path))
    return int(m.group(1)) if m else None


def _iter_checked_lines(text):
    """逐行产出 (行号, 行文本, 是否在核验区)。

    核验区 = 全文 − 「原文全文」照录区 − 【文学演绎】标记区（§4.12）。
    标记区范围：标记行所在标题节内（直到同级或更高级标题）。
    """
    head_level = 0
    in_fulltext = False
    fiction_until = 0  # >0 表示处于演绎豁免区（值=标记节标题级）
    for i, ln in enumerate(text.splitlines(), 1):
        st = ln.strip()
        hm = HEADING_RE.match(st)
        if hm:
            lv = len(hm.group(1))
            title = st[lv:].strip()
            head_level = lv
            if lv == 2:
                in_fulltext = title.startswith(FULLTEXT_HEAD)
            if in_fulltext or lv <= fiction_until:
                fiction_until = 0
            yield i, ln, False
            continue
        if FICTION_MARK in st and st.startswith(">"):
            fiction_until = head_level  # 豁免至同级/更高级标题
            yield i, ln, False
            continue
        if in_fulltext or fiction_until:
            yield i, ln, False
            continue
        yield i, ln, True


def check_text(text, chapters, path=""):
    """返回 (规范引文总数, 归属对白总数, 失败清单[(行号, 原因)])。"""
    total_c, total_a, fails = 0, 0, []
    whole = "".join(chapters[n] for n in sorted(chapters))
    doc_num = doc_chapter_num(path, text) if path else None
    for i, ln, checked in _iter_checked_lines(text):
        st = ln.strip()
        # --- 检查 1：规范引文行 ---
        m = CITE_RE.match(st)
        if not m:
            # 防静默跳过（2026-09-27 加固）：疑似引文行但语法漂移 → 直接判 FAIL
            if checked and SUSPECT_RE.match(st):
                fails.append((i, "疑似引文行未采用规范语法（`> 原文引文（第N回）：` 全角引号·回目号无空格），将不进核验分母"))
            continue
        total_c += 1
        num = int(m.group(1))
        quote = m.group(2).strip()
        if not (quote.startswith("“") and quote.endswith("”") and len(quote) >= 2):
            fails.append((i, "引文未用全角引号“…”包裹"))
            continue
        body = norm(quote[1:-1])
        if not body:
            fails.append((i, "引文为空"))
            continue
        if num not in chapters:
            fails.append((i, "回目 %d 超出 1-100" % num))
            continue
        if body not in chapters[num]:
            fails.append((i, "第%d回未命中（非原文精确子串）" % num))
        continue
    # --- 检查 2：归属对白（豁免区内不跑） ---
    for i, ln, checked in _iter_checked_lines(text):
        if not checked:
            continue
        st = ln.strip()
        for q in ATTRIB_RE.findall(st):
            total_a += 1
            nq = norm(q)
            if nq not in whole:
                where = "第%d回文档" % doc_num if doc_num else "文档"
                fails.append((i, "归属对白未命中（%s·%s）：%s" % (where, "全书原文无此精确子串", q[:30])))
    return total_c, total_a, fails


def iter_md(base):
    prefixes, files = load_doc_ignores()
    for r, _, fns in os.walk(base):
        for fn in sorted(fns):
            if fn.endswith(".md"):
                p = os.path.join(r, fn)
                rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
                if is_ignored(rel, prefixes, files):
                    continue
                yield p


QUOTE_LONG_RE = re.compile(r"[“「]([^”」]{15,})[”」]")


def scan_reverse(text, chapters):
    """S-35 反向扫描（W742·A-01 立项落地）：未标记节的漏标候选。

    判据 = 文档规范 §4.12 逆向（F-3 同源）：节内「未以规范语法标注的 ≥15 字引号内容
    与归属对白」对全书语料未命中率 ≥50%（样本 ≥2）→ 漏标候选。
    排除：原文照录区 / 延伸思考节 / 已含【文学演绎】标记的节；规范引文行不抽
    （已由检查 1 管控·必真原文）。报告型工具：不改变第 20 门禁判定。
    返回 [(节标题, 行号, n_total, n_miss, 示例)]。
    """
    whole = "".join(chapters[n] for n in sorted(chapters))
    cands = []
    state = {"lv": 0, "title": "", "line": 0, "fulltext": False, "marked": False, "samples": []}

    def flush():
        if (state["lv"] and state["samples"] and not state["marked"]
                and not state["fulltext"] and "延伸思考" not in state["title"]):
            n_total = len(state["samples"])
            n_miss = sum(1 for _ln, q in state["samples"] if norm(q) not in whole)
            if n_total >= 2 and n_miss / n_total >= 0.5:
                cands.append((state["title"], state["line"], n_total, n_miss, state["samples"][0][1][:24]))
        state["samples"] = []
        state["marked"] = False

    for i, ln in enumerate(text.splitlines(), 1):
        st = ln.strip()
        hm = HEADING_RE.match(st)
        if hm:
            flush()
            state["lv"] = len(hm.group(1))
            state["title"] = st[state["lv"]:].strip()
            state["line"] = i
            if state["lv"] == 2:
                state["fulltext"] = state["title"].startswith(FULLTEXT_HEAD)
            continue
        if state["fulltext"]:
            continue
        if FICTION_MARK in st:
            state["marked"] = True
            continue
        if CITE_RE.match(st):
            continue
        seen = set()
        for q in ATTRIB_RE.findall(st):
            seen.add(q)
        for q in QUOTE_LONG_RE.findall(st):
            seen.add(q)
        for q in seen:
            state["samples"].append((i, q))
    flush()
    return cands


def rel_or_abs(p):
    try:
        return os.path.relpath(p, ROOT).replace(os.sep, "/")
    except ValueError:
        return p.replace(os.sep, "/")


def fenhui_body(n):
    """分回 md 正文（剥离去头 # 标题行 + 截除「单字解释」附录）——与 json 重建口径一致。"""
    t = open(os.path.join(FENHUI_DIR, "第%03d回.md" % n), encoding="utf-8").read()
    lines = t.split("\n")
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    t = "\n".join(lines)
    i = t.rfind("单字解释")
    if i >= 0:
        t = t[:i]
    return t


def check_corpus(chapters, verbose=True):
    """检查 3：text-search.json vs source/原文/分回 逐回全等（去空白归一）。

    返回失败清单[(回次, 原因)]；空列表 = 通过。
    """
    fails = []
    for n in sorted(chapters):
        try:
            body = fenhui_body(n)
        except FileNotFoundError:
            fails.append((n, "分回文件缺失"))
            continue
        if norm(body) != chapters[n]:
            fails.append((n, "json 与分回 md 去空白归一后不一致"))
    if verbose:
        if fails:
            for n, why in fails[:5]:
                print("FAIL 语料保真：第%d回 %s" % (n, why))
            print("语料保真：%d/100 回不一致" % len(fails))
        else:
            print("语料保真通过：text-search.json 100 回与 source/原文/分回 逐回全等（去空白归一）")
    return fails


DQ = chr(34)
SELF_TEST_CASES = [
    (True, "> 原文引文（第1回）：“混沌未分天地乱”", "正样本·规范语法"),
    (False, "> 原文引文（第 1 回）：“混沌未分天地乱”", "负样本·回目号带空格（曾致静默跳过）"),
    (False, "> 原文引文（第1回）：" + DQ + "混沌未分天地乱" + DQ, "负样本·半角引号"),
    (False, "> **原文引文（第1回）：“混沌未分天地乱”", "负样本·粗体前缀漂移"),
]
# 归属对白自检样本（正样本须命中原著·负样本须未命中）
ATTRIB_SELF = [
    (True, "石猴问道：“里面怎么样？水有多深？”", "正样本·归属对白命中（第1回原文）"),
    (False, "八戒道：「娘啊，你物件有多少？都要我也用得着。」", "负样本·虚构对白（W737 实证案）"),
]


def self_test(chapters):
    bad = 0
    for expect_pass, line, label in SELF_TEST_CASES:
        total_c, total_a, fails = check_text(line + "\n", chapters)
        passed = (len(fails) == 0) and (total_c == 1)
        if passed != expect_pass:
            print("FAIL self-test：%s（期望 %s，实得 total=%d / fails=%d）"
                  % (label, "通过" if expect_pass else "失败", total_c, len(fails)))
            bad += 1
    for expect_pass, line, label in ATTRIB_SELF:
        _, _, fails = check_text(line + "\n", chapters)
        passed = len(fails) == 0
        if passed != expect_pass:
            print("FAIL self-test：%s（期望 %s，实得 fails=%d）"
                  % (label, "通过" if expect_pass else "失败", len(fails)))
            bad += 1
    # 演绎豁免语义：标记区内的虚构对白不得判 FAIL
    fiction_doc = "## 深度解读\n\n### SD001 · 测试\n\n> " + FICTION_MARK + "测试标记行\n\n八戒道：「娘啊，你物件有多少？都要我也用得着。」\n"
    _, _, fails = check_text(fiction_doc, chapters)
    if fails:
        print("FAIL self-test：演绎标记豁免失效（标记区内虚构对白被判 FAIL：%s）" % (fails[:1],))
        bad += 1
    # 原文全文照录区豁免
    fulltext_doc = "## 原文全文\n\n八戒道：「娘啊，你物件有多少？都要我也用得着。」\n"
    _, _, fails = check_text(fulltext_doc, chapters)
    if fails:
        print("FAIL self-test：原文全文区豁免失效（%s）" % (fails[:1],))
        bad += 1
    # 语料保真负样本：内存篡改一回 → 必须检出
    tampered = dict(chapters)
    tampered[1] = tampered[1] + "篡改"
    cf = check_corpus(tampered, verbose=False)
    if not cf:
        print("FAIL self-test：语料保真负样本未检出（篡改后仍判全等）")
        bad += 1
    # S-35 反向扫描自检（W742·A-01）：正向回归 + 对抗检出 + 真句零候选
    marked_sec = ("## 深度解读\n\n### SD001 · 测试\n\n> " + FICTION_MARK + "测试标记\n\n"
                  "八戒道：「娘啊，你物件有多少？都要我也用得着。」\n")
    if scan_reverse(marked_sec, chapters):
        print("FAIL self-test：反向扫描误报已标节（正向回归破坏）")
        bad += 1
    fake_sec = ("## 深度解读\n\n### SD002 · 测试\n\n"
                "八戒道：「娘啊，你物件有多少？都要我也用得着。」\n"
                "八戒又道：「这是第二条完全虚构的对白内容样本。」\n")
    if not scan_reverse(fake_sec, chapters):
        print("FAIL self-test：反向扫描未检出未标节虚构对白（对抗样本）")
        bad += 1
    real_sec = ("## 名句赏析\n\n石猴问道：“里面怎么样？水有多深？”\n"
                "他说道：「感盘古开辟，三皇治世，五帝定伦」\n")
    if scan_reverse(real_sec, chapters):
        print("FAIL self-test：反向扫描误报全真句节：%s" % (scan_reverse(real_sec, chapters)[:1],))
        bad += 1
    total = len(SELF_TEST_CASES) + len(ATTRIB_SELF) + 6
    print("self-test %s：%d/%d" % ("通过" if not bad else "失败", total - bad, total))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description="原著引文硬验证（W503·W737 三检扩展）")
    ap.add_argument("--file", help="单文件模式（检查 1+2）")
    ap.add_argument("--dir", help="目录模式（检查 1+2+3·门禁模式）")
    ap.add_argument("--check-corpus", action="store_true", help="只跑语料保真检（检查 3）")
    ap.add_argument("--self-test", action="store_true", help="自检（内存正负样本，不依赖外部文档）")
    ap.add_argument("--reverse", action="store_true",
                    help="S-35 反向扫描：未标记节漏标候选（配 --dir·默认 docs/01·报告不阻断）")
    ap.add_argument("--fail-on-candidates", action="store_true",
                    help="--reverse 发现候选时退出码 1（定标后收紧用）")
    args = ap.parse_args()

    chapters = load_chapters()

    if args.self_test:
        return self_test(chapters)

    if args.check_corpus:
        return 1 if check_corpus(chapters) else 0

    if args.reverse:
        base = args.dir or os.path.join(ROOT, "docs", "01-全书逐回解读")
        n_files = 0
        all_cands = []
        for p in iter_md(base):
            n_files += 1
            with open(p, encoding="utf-8") as fh:
                text = fh.read()
            for t, line_no, n_total, n_miss, ex in scan_reverse(text, chapters):
                all_cands.append((rel_or_abs(p), line_no, t, n_total, n_miss, ex))
        print("== S-35 漏标反向扫描（判据 §4.12 逆向·W742）==")
        print("扫描 %d 篇 · 候选节 %d 个" % (n_files, len(all_cands)))
        for rel, line_no, t, n_total, n_miss, ex in all_cands[:40]:
            print("候选 %s:%d 「%s」 样本%d 未命中%d（%.0f%%） 示例：「%s…」"
                  % (rel, line_no, t[:24], n_total, n_miss, 100.0 * n_miss / n_total, ex))
        if len(all_cands) > 40:
            print("…（其余 %d 条省略）" % (len(all_cands) - 40))
        if not all_cands:
            print("PASS 未发现漏标候选（已标区正向回归语义成立）")
        return 1 if (args.fail_on_candidates and all_cands) else 0

    if not args.file and not args.dir:
        ap.error("需要 --file 或 --dir（或 --self-test / --check-corpus）")
    files = [args.file] if args.file else list(iter_md(args.dir))

    g_total_c, g_total_a, g_fail_files = 0, 0, 0
    for p in files:
        try:
            text = open(p, encoding="utf-8").read()
        except Exception as e:
            print("FAIL %s: 读取失败 %s" % (p, e))
            g_fail_files += 1
            continue
        total_c, total_a, fails = check_text(text, chapters, path=p)
        g_total_c += total_c
        g_total_a += total_a
        if fails:
            g_fail_files += 1
            rel = rel_or_abs(p)
            for ln_no, why in fails[:5]:
                print("FAIL %s:%d %s" % (rel, ln_no, why))

    if args.dir:
        # 检查 3：语料保真（门禁模式随行）
        if check_corpus(chapters):
            g_fail_files += 1

    if g_fail_files:
        print("引文核验：共 %d 条规范引文 + %d 条归属对白 · %d 个文件存在未命中/格式错误"
              % (g_total_c, g_total_a, g_fail_files))
        return 1
    print("引文核验通过：共 %d 条规范引文 + %d 条归属对白 · 命中率 100%%（%d 个文件扫描）"
          % (g_total_c, g_total_a, len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
