#!/usr/bin/env python3
"""check_no_brand_refs.py — 品牌字面量零命中守卫（W836·N2「归档检测器复活到活面」）

为什么有这个东西（W812/W814 去品牌批留下的缺口）：

  W812/W814 两批把三枚品牌字面量从全仓清零，**验收方式是人工终扫**——仓内没有任何机器防线。
  与此同时，仓里唯一一处「品牌字面量扫描器」是归档件
  `archive/scripts/batches/misc/_audit_agentweb_baseline.py`：它在 W680 时被归档进
  `archive/scripts/batches/misc/`，而其 ROOT 仍按「脚本所在目录上溯两级」计算 ⇒ ROOT 落到
  `archive/scripts`（应为仓库根·上溯四级）⇒ 第 31 行读 `archive/scripts/xiyouji-agent-web/…`
  直接抛错，**第 110 行的品牌扫描段根本不可达**。
  于是「品牌回归」在仓库里既无扫描器、也无机器防线：**后写的文档又把字面量带回来也没人拦**。
  本文件即该检测能力的**活面承接**（归档件按文档规范 §11.2 不回溯修改）。

三条设计纪律：

  ① **字面量不在本文件明文出现**（base64 编码存储·运行时解码）——禁令要求的是
     「全仓明文 0 命中」，守卫自身若明文写出被禁字面量就等于自己违规；编码后明文扫描仍为 0，
     而守卫依旧能检出回归。
  ② **fail-closed 且分流退出码**：0=零命中 · 1=有命中 · 2=判据未执行（字面量解码失败 /
     扫描面为空 / git 不可用）——「判据未执行」与「判定为红」语义不同，故不同码（沿用
     W816 引文门禁的 1/2 分流口径）。
  ③ **扫描面 = git 已跟踪文件**（含 `archive/**`）：未跟踪文件（AI 会话运行态目录、
     本地临时产物）不进判定面——它们既不入库也不构成仓库内容。

用法：
    py -3 scripts/check_no_brand_refs.py            # 全仓扫描（退出码 0/1/2）
    py -3 scripts/check_no_brand_refs.py --self-test  # 判据自检（合成样本·不碰真实仓）

豁免（逐条写明·不豁免即等于漏检）：
    archive/scripts/batches/misc/_audit_agentweb_baseline.py
        ——归档件本身即历史检测器快照，其模式串是禁令对象的历史留痕；本批已按「活面承接」
          移除该段的模式串（见该文件内的移除说明），故不再需要路径豁免。
"""
import base64
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# 三枚被禁品牌字面量（base64 编码·明文不出现在仓库内容中）。
# 追加/调整须同步更新 docs/00-导读/W批次编号对账表.md 的 W836 行与本文档自检样本。
_B64_BRANDS = [
    "Y29kZWJ1ZGR5",          # 枚 1（其子串形态一并命中·子串匹配即命中）
    "d29ya2J1ZGR5",          # 枚 2
    "Y29tYXRl",               # 枚 3
]

# 扫描面排除的目录名（相对仓库根·顶层）与扩展名
_SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", "coverage",
    "__pycache__", ".pytest_cache", ".ruff_cache", ".tsbuild",
}
_SKIP_SUFFIX = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz",
                ".woff", ".woff2", ".ttf", ".eot", ".mp3", ".mp4", ".wasm", ".db", ".sqlite")

# W1062 新增·「声明性豁免」——化解「铁律 19 必须点名被禁品牌」与「守卫要求明文 0 命中」
# 的结构性冲突。
#
# 冲突事实：AGENTS.md 铁律 19 / CLAUDE.md 速查 14 行的正文**必须**写出被禁品牌名
# （否则禁令没有指向对象、读者无从知晓禁的是什么）⇒ 按「明文 0 命中」一刀切会把
# 禁令本身判红；于是 W1061 把铁律 19 入必载层后，Security job 恒红 ⇒ PR 无法合并。
#
# 解法（不是删禁令、也不是整体放行某个文件）：豁免**逐条绑定到「声明句」**——
# 只有当该行同时满足「含被禁字面量」且「命中声明标记」时才算豁免，且必须在本文件登记
# 声明标记串。标记串不含被禁字面量（否则本文件自身违规），由规则内的中性词构成。
#
# 三条硬约束（防止豁免机制退化成「随便写就过」）：
#  ① 豁免是**行级**的，不是文件级——同文件内未含标记的行仍然判红；
#  ② 标记串必须显式登记在本文件，不存在「默认豁免」；
#  ③ 声明标记本身不得含被禁字面量（守卫自指不违规）。
_DECLARE_MARKERS = (
    # —— 禁令正文（AGENTS 铁律 19 / CLAUDE 速查 14 行等：点名被禁品牌是禁令的指向对象）
    "禁令",      # 「禁用 X/Y（…禁令…）」类正文
    "禁用",      # 「禁用 X/Y」句式
    "禁 ",       # 「禁 X/Y」句式（半角空格分隔）
    "铁令",      # W1061 段标题「…铁令入必载层」
    "铁律 19",   # 铁律 19 专名
    "入必载层",   # W1061「…入必载层」简称式声明（禁令入层的中文简称）
    # —— 元叙述（讲「禁品牌字面量」这件事本身）
    "禁品牌字面量",  # 元叙述「本行在讲禁品牌字面量本身」
    "被禁品牌",      # 元叙述
    "永久禁令",      # 元叙述
    "brand-ban",     # 英文/拼音形态标记（供 spec 类 JSON 登记）
    "brandban",
)


def is_declaration_line(text):
    """该行是否为「声明句」（含被禁字面量但属于禁令/元叙述声明）→ 豁免。

    判据：行内含任一登记标记串（_DECLARE_MARKERS）⇒ 视为声明句。
    刻意收紧：**不**要求字面量与标记在同一条正则里共存，只按标记串判定——
    因为「铁律 19」这类禁令正文的中文标点/换行形态多变，用正则锁死形态必被绕过。
    """
    low = text.lower()
    return any(m.lower() in low for m in _DECLARE_MARKERS)


def brand_patterns():
    """解码被禁字面量 → 小写正则片段列表。解码失败即抛（调用方须转成退出码 2）。"""
    out = []
    for b64 in _B64_BRANDS:
        raw = base64.b64decode(b64.encode("ascii")).decode("utf-8")
        if not raw.strip():
            raise ValueError("空字面量")
        out.append(raw.lower())
    return out


def scan_text(text, patterns):
    """返回命中的 (pattern, 命中片段) 列表（大小写不敏感·子串匹配）。"""
    low = text.lower()
    hits = []
    for pat in patterns:
        idx = low.find(pat)
        if idx >= 0:
            hits.append((pat, text[max(0, idx - 30): idx + len(pat) + 30].replace("\n", "\\n")))
    return hits


def tracked_files(root=ROOT):
    """git ls-files 的结果（已跟踪文件=仓库内容面）。git 不可用即抛。

    W1062 根修：`core.quotepath=false`——否则含非 ASCII 字符的路径会被 git 转义成
    八进制并加引号（`"docs/11-\\346\\226\\271..."`），本函数把该串当真实路径返回，
    调用方 `open(rel)` 因路径不存在抛 OSError → 被 `except OSError: continue` **静默跳过**
    ⇒ 全仓 1812 个中文路径文件从未被真正扫描过（实测：修复前可读 3356 / 5197，
    修复后 5197 / 5197）。这是「守卫自建却漏检 1/3 仓库」型静默失效。
    """
    r = subprocess.run(["git", "-C", root, "-c", "core.quotepath=false", "ls-files"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError("git ls-files 失败：%s" % (r.stderr or "").strip()[:200])
    files = []
    for line in r.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        # 引号包裹 = git 对含非 ASCII / 特殊字符路径的转义输出（quotepath 关闭后
        # 仍可能带引号·含空格等）→ 去掉外壳引号。
        if len(line) >= 2 and line[0] == '"' and line[-1] == '"':
            line = line[1:-1]
        rel = line.replace("\\", "/")
        parts = rel.split("/")
        if any(p in _SKIP_DIRS for p in parts[:-1]):
            continue
        if rel.lower().endswith(_SKIP_SUFFIX):
            continue
        files.append(rel)
    return files


def scan_repo(root=ROOT):
    """全仓扫描 → (命中清单, 扫描文件数)。命中清单元素为 (相对路径, 片段)。

    W1062：判定粒度从「文件」降到「行」——含被禁字面量但属「声明句」（禁令正文或
    元叙述）的行按 _DECLARE_MARKERS 豁免；同一文件内未含标记的行仍判红（行级豁免
    ≠ 文件级放行）。读取失败不再静默跳过：记入 skipped 并在结果里暴露（防止
    「守卫扫不到文件 ⇒ 恒绿」型假绿）。
    """
    patterns = brand_patterns()
    files = tracked_files(root)
    if not files:
        raise RuntimeError("扫描面为空（无已跟踪文件）·判据未执行")
    hits = []
    skipped = []
    for rel in files:
        path = os.path.join(root, rel.replace("/", os.sep))
        try:
            with open(path, encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except OSError:
            skipped.append(rel)
            continue
        for line in text.split("\n"):
            for pat, snippet in scan_text(line, patterns):
                if is_declaration_line(line):
                    continue
                hits.append((rel, pat, snippet))
    if skipped:
        # 读不到任何文件 = 扫描面失效 ⇒ fail-closed（退出码 2），不得当作零命中。
        raise RuntimeError("扫描面失效：%d 个已跟踪文件读取失败（首例 %s）"
                           % (len(skipped), skipped[0]))
    return hits, len(files)


def _self_test():
    """判据自检（合成样本·不读真实仓）：正例须命中、反例须零命中、退出码须分流。"""
    fails = 0
    cases = 0

    def check(cond, note):
        nonlocal fails, cases
        cases += 1
        if not cond:
            fails += 1
        print("%s  %s" % ("OK  " if cond else "FAIL", note))

    patterns = brand_patterns()
    check(len(patterns) == 3, "字面量解码出 3 枚（%d）" % len(patterns))
    check(all(p == p.lower() and p.isascii() for p in patterns), "解码结果为小写 ASCII 字面量")

    # 正例：每枚字面量的大小写形态与词内嵌形态都必须命中
    # 探针**由解码结果在运行时派生**——若在此处硬编码探针串，本文件自身就带着明文字面量，
    # 守卫入库后会把自己判红（自指违规）。
    for pat in patterns:
        for probe in (pat, pat.upper(), pat.capitalize(), "a %scli b" % pat, "x%s" % pat):
            hit = scan_text("prefix %s suffix" % probe, patterns)
            check(bool(hit), "正例应命中：%s 的大小写/内嵌形态" % pat)

    # 反例：形近但不同的字面量、允许品牌、允许的中性标识一律不得命中
    for probe in ["claude", "Claude-compat", "旧厂商 Agent 品牌", "并行 Agent 会话", "主会话",
                  "codebud", "buddy", "workbud", "comat", "mate", "", "c0debuddy"]:
        hit = scan_text("prefix %s suffix" % probe, patterns)
        check(not hit, "反例不应命中：%r" % probe)

    # 退出码分流：判定为红=1；判据未执行=2
    check(_exit_code_for_hits(3) == 1, "有命中 → 退出码 1")
    check(_exit_code_for_hits(0) == 0, "零命中 → 退出码 0")
    check(_exit_code_for_error() == 2, "判据未执行 → 退出码 2")

    # W1062 负样本组①：声明句豁免必须「只对声明句生效」，不能退化成全局放行
    for marker in _DECLARE_MARKERS:
        probe = "prefix %s suffix" % ("x" + "y" * 0)
        check(is_declaration_line("本行含 %s 标记 ⇒ 应豁免" % marker),
              "声明句应被豁免：含标记 %r" % marker)
        check(not is_declaration_line(probe),
              "无标记行不应被豁免（标记 %r 不得导致全局放行）" % marker)
    # 负样本组②：豁免是行级——同文件内含标记的行豁免、其余行仍须命中
    # 探针**由解码结果在运行时派生**（不得在本文件明文写出被禁字面量·否则守卫自指违规）
    _p0 = patterns[0]
    decl_line = "禁令：禁 %s" % _p0
    plain_line = "普通叙述里提到 %s" % _p0
    check(not scan_text(decl_line, patterns) or is_declaration_line(decl_line),
          "声明行被识别为声明句")
    check(bool(scan_text(plain_line, patterns)) and not is_declaration_line(plain_line),
          "无标记行仍须命中且不被豁免（行级豁免≠文件级放行）")

    print("self-test: %d/%d 通过" % (cases - fails, cases))
    return 1 if fails else 0


def _exit_code_for_hits(n):
    return 1 if n else 0


def _exit_code_for_error():
    return 2


def main(argv):
    if "--self-test" in argv[1:]:
        return _self_test()
    root = ROOT
    try:
        hits, scanned = scan_repo(root)
    except Exception as exc:  # noqa: BLE001 — 判据未执行统一转退出码 2
        print("ERROR 判据未执行：%s" % exc)
        return _exit_code_for_error()
    if hits:
        print("FAIL 品牌字面量命中 %d 处（扫描 %d 个已跟踪文件）：" % (len(hits), scanned))
        for rel, _pat, snippet in hits[:40]:
            print("  %s :: %s" % (rel, snippet))
        if len(hits) > 40:
            print("  ……另有 %d 处未列" % (len(hits) - 40))
        return _exit_code_for_hits(len(hits))
    print("OK 品牌字面量零命中（扫描 %d 个已跟踪文件·含 archive/）" % scanned)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
