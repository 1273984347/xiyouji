#!/usr/bin/env python3
"""
verify_delivery.py — 零依赖交付校验门禁（Senior Developer 设立）

解决两类工程顽疾：
  1) 「旧疾」：单文件连续多次 Edit 时描述段丢失 → 校验文档均含最新版本号 + W### 里程碑 token。
  2) 「范围漂移」：已评审/已记录 scope 之外又发生了改动（如 html 里出现 W334 标记但文档只记到 W333）
     → 校验 site/dukou-engine.html 中引用的所有 W### 是否都已在文档中记录。

降级六文档同步（W393）：
  - 核心 2 份（CHANGELOG.md / 交接文档.md）= 跨 session 连续性真载体，缺失 v/W 仍【阻断】。
  - 辅助 4 份（README.md / STRUCTURE.md / 项目说明.md / file-index.md）= 每次 W### 的纯手工税，
    缺失仅【WARN 不阻断】，里程碑时跑 scripts/bump_version.py 一键补齐。

动态期望版本（W518）：六文档同步的期望 v/W 不再锚定 dukou-engine.html 页脚（滞后型
  手工工件，辅助文档升版后必现"不含旧版"噪音 WARN），改为动态取 CHANGELOG 倒序首个
  版段（现役段）；页脚自身降级为新鲜度被检对象，落后现役段仅【WARN 不阻断】。

零依赖：仅标准库。可直接运行：
  python scripts/verify_delivery.py            # 静态校验（提交前门禁）
  python scripts/verify_delivery.py --health   # 额外探测 RAG /health（环境项，仅告警不阻断）

退出码：核心 FAIL 1；仅辅助 WARN 0。可直接挂到 .git/hooks/pre-commit（辅助 WARN 不再阻断提交）。
"""

import json
import os
import re
import subprocess
import sys
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, ".."))  # scripts/.. = 项目根 xiyouji

# 降级六文档同步（W393）：核心 2 份硬门禁，辅助 4 份仅 WARN 不阻断
# W413 修正（2026-08-09）：严格审查后交接文档恢复入库（无敏感内容），恢复为核心硬门禁
# 门禁段自洽锁声明（VERIFY_SECTIONS·W663/T3）：下方名单 == main() 内阻断门禁段标记，
# 每段段首 section(name) 上报、收尾断言缺段即红——防「段被删/注释后其余全绿」的假象。
EXPECTED_SECTION_NAMES = [
    "期望版本",
    "dukou页脚",
    "六文档同步",
    "旁文档同步",
    "范围漂移",
    "A4计数",
    "A1-A6计数",
    "学术引用",
    "A1导航",
    "docs链接",
    "sitemap覆盖",
    "内嵌回退",
    "双源漂移",
    "CSP漂移",
    "腐蚀插件",
    "内联语法",
    "CSS平衡",
    "token覆盖",
    "动效禁令",
    "a11y对比",
    "INLINED完整",
    "动态链接",
    "治理契约",
    "索引健康",
    "元信息块",
    "术语一致",
    "引文核验",
    "图表自洽",
    "数据一致",
    "W区间字面量",
    "SEOhead",
    "可引用性",
    "设计令牌对账",
    "色盲安全",
    "降级声明",
    "文档口径", "CLAUDE速查",
    "head内容", "CSS变量引用",
    "声明分隔", "孤立选择", "kpi基类", "内嵌残留", "时间线双源", "chapter双源",
]

# ---- scope 分级（W698·用户裁决「动工」，P2-2 落地）：pre-commit 按变更路径跑受影响门禁子集 ----
# 四态：full=全量（缺省·CI verify-delivery job·批收尾七步③恒为 full）；docs=文档轨子集；
# site=页面轨+级联相关文档段；auto=按变更路径白名单分类（任何越界文件保守回退 full）。
# 11 个内联廉价段（版本/计数/导航/sitemap walk）恒跑不跳；跳过只作用于 32 个 subprocess
# 委托段：_scoped_run 统一短路，_GATE_SUMMARY_MARKERS 兜住防静默跳过 wrapper 的汇总行
# 校验（fake stdout 含段标记，wrapper 不会误判「缺汇总行」）；段自洽锁按 scope 断言子集。
_DOC_FILES_RE = re.compile(
    r"^(docs/.+\.md|(CHANGELOG|交接文档|README|STRUCTURE|CLAUDE)\.md|"
    r"scripts/output/file-index(-archive)?\.md|CITATION\.cff|"
    r"\.github/workflows/README\.md|AGENTS\.md|dataset/glossary\.json)$")
_SITE_FILES_RE = re.compile(
    r"^(site/.+\.(html|css|js|xml)|dataset/.+\.json|scripts/output/data/.+\.json)$")
SCOPE_DOCS_SECTIONS = {
    "docs链接", "治理契约", "索引健康", "元信息块", "术语一致", "引文核验",
    "W区间字面量", "文档口径", "CLAUDE速查",
}
SCOPE_SITE_SECTIONS = {
    "双源漂移", "CSP漂移", "腐蚀插件", "内联语法", "CSS平衡", "token覆盖",
    "动效禁令", "a11y对比", "INLINED完整", "动态链接", "图表自洽", "数据一致",
    "SEOhead", "可引用性", "设计令牌对账", "色盲安全", "降级声明", "head内容",
    "CSS变量引用", "声明分隔", "孤立选择", "kpi基类", "内嵌残留", "时间线双源", "chapter双源",
    "文档口径", "W区间字面量", "索引健康", "治理契约",
}
_SCOPE_CORE = {"期望版本", "dukou页脚", "六文档同步", "范围漂移"}
_GATE_SUMMARY_MARKERS = {
    "可引用性": "---- 第 28 门禁：",
    "设计令牌对账": "---- 设计令牌对账：",
    "色盲安全": "---- 第 29 门禁 色盲安全：",
    "降级声明": "---- 第 30 门禁 降级声明：",
    "文档口径": "---- 第 31 门禁 文档口径体检：",
    "CLAUDE速查": "---- 第 32 门禁 CLAUDE.md 速查层：",
    "head内容": "---- 第 33 门禁 head 内容：",
    "CSS变量引用": "---- 第 34 门禁 CSS 变量引用：",
    "声明分隔": "---- 第 35 门禁 声明分隔：",
    "孤立选择": "---- 第 36 门禁 孤立选择器：",
    "kpi基类": "---- 第 37 门禁 kpi 基类：",
    "内嵌残留": "---- 第 38 门禁 页面内嵌残留标记：",
    "时间线双源": "---- 第 39 门禁 故事内时间线双源同步：",
    "chapter双源": "---- 第 40 门禁 chapter_stats 双源同步：",
}


def _parse_scope(argv):
    """解析 --scope full|auto|docs|site（缺省 full；非法值回退 full）。"""
    for i, a in enumerate(argv):
        if a == "--scope" and i + 1 < len(argv):
            return argv[i + 1]
        if a.startswith("--scope="):
            return a.split("=", 1)[1]
    return "full"


def _git_changed_files():
    """staged ∪ unstaged 变更文件集合；git 不可用/失败 → None（回退 full）。
    未跟踪的 docs/site 内容文件（.md/.html/.json）在场 → None（树态含未验证新文件，
    跳过任一门禁族都不安全；tmpe/ 临时区豁免）。"""
    files = set()
    for args in (["diff", "--cached", "--name-only"], ["diff", "--name-only"]):
        try:
            r = subprocess.run(["git", "-c", "core.quotePath=false"] + args,
                               cwd=ROOT, capture_output=True, text=True, timeout=30)
        except Exception:
            return None
        if r.returncode != 0:
            return None
        files |= {ln.strip().replace("\\", "/") for ln in r.stdout.splitlines() if ln.strip()}
    try:
        r = subprocess.run(["git", "-c", "core.quotePath=false",
                            "ls-files", "--others", "--exclude-standard"],
                           cwd=ROOT, capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            for ln in r.stdout.splitlines():
                ln = ln.strip().replace("\\", "/")
                if ln and not ln.startswith("tmpe/") and (
                        _DOC_FILES_RE.match(ln) or _SITE_FILES_RE.match(ln)):
                    return None
    except Exception:
        return None
    return files


def _classify_scope(files):
    """白名单分类：全部命中 doc-ish → docs；含 site-ish（含站点+级联混合批）→ site；
    任何越界文件（门禁脚本/workflow/tests/baseline/一次性脚本等）→ full（保守缺省）。"""
    norm = sorted(f.replace("\\", "/") for f in files)
    if any(not (_DOC_FILES_RE.match(f) or _SITE_FILES_RE.match(f)) for f in norm):
        return "full"
    if any(_SITE_FILES_RE.match(f) for f in norm):
        return "site"
    return "docs"

CORE_DOCS = [
    "CHANGELOG.md",
    "交接文档.md",
]
AUX_DOCS = [
    "README.md",
    "STRUCTURE.md",
    os.path.join("docs", "00-导读", "项目说明.md"),
    os.path.join("scripts", "output", "file-index.md"),
]
DOCS = CORE_DOCS + AUX_DOCS
HTML = os.path.join(ROOT, "site", "dukou-engine.html")

# 四份含 A4 计数语义的文档（W413 修正：交接文档恢复入库，恢复 4 份检查）
A4_DOCS = ["README.md", "STRUCTURE.md",
           os.path.join("docs", "00-导读", "项目说明.md"), "交接文档.md"]
EXPECT_A4 = "209 篇"  # 真实计数（W342 199→201 起步，W400 后实际 209）

# 归档文件（W417 新增）：归档后旧 W### 仍纳入范围漂移可追溯扫描，避免误报
# W513：CHANGELOG-ARCHIVE 二级归档层（W001-W399）同纳入扫描
ARCHIVE_DOCS = [
    os.path.join("docs", "archive", "CHANGELOG-ARCHIVE.md"),
    os.path.join("docs", "archive", "CHANGELOG-ARCHIVE-tier2.md"),
    os.path.join("scripts", "output", "file-index-archive.md"),
    os.path.join("docs", "archive", "交接文档-ARCHIVE.md"),
]

# A1-A6 内容板块真实文件计数 vs README 声明（W417 新增，防计数声明失真）
A_AREAS = [
    ("A1 逐回解读", os.path.join("docs", "01-全书逐回解读")),
    ("A2 个人随笔", os.path.join("docs", "06-个人随笔")),
    ("A3 人物分析", os.path.join("docs", "02-人物深度分析")),
    ("A4 主题专题", os.path.join("docs", "03-主题与情节专题")),
    ("A5 文化背景", os.path.join("docs", "04-文化与历史背景")),
    ("A6 诗词歌赋", os.path.join("docs", "05-诗词歌赋")),
]


def _count_content_md(area_dir):
    """统计板块 .md 文件数，排除 README.md/.gitkeep 等非正文文件（各板块恰好 1 个 README.md）"""
    p = os.path.join(ROOT, area_dir)
    if not os.path.isdir(p):
        return -1
    return sum(1 for fn in os.listdir(p)
               if fn.endswith(".md") and fn.lower() != "readme.md")


def _read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def latest_version_from_changelog(text):
    """从 CHANGELOG 文本解析现役（最新）版段 → (X.Y.Z, W##)；无版段返回 (None, None)。

    版段倒序排列（最新在最前），首个 `### vX.Y.Z（日期）：W###` 匹配即现役段。
    ver 不含 "v" 前缀，与既有 ("v" + ver) 用法一致。
    """
    m = re.search(r"^###\s+v(\d+\.\d+\.\d+)（[^）]*）：\s*W(\d+)", text, re.M)
    return (m.group(1), m.group(2)) if m else (None, None)


def parse_footer_version(text):
    """解析文本中首个 vX.Y.Z W### 版本标记 → (X.Y.Z, W##)；无匹配返回 (None, None)。"""
    m = re.search(r"v(\d+\.\d+\.\d+)\s+W(\d+)", text)
    return (m.group(1), m.group(2)) if m else (None, None)


def main():
    fails = 0
    warns = 0

    def fail(msg):
        nonlocal fails
        fails += 1
        print("FAIL  " + msg)

    def warn(msg):
        nonlocal warns
        warns += 1
        print("WARN  " + msg)

    def ok(msg):
        print("OK    " + msg)

    # ---- scope 分级（W698）：解析 --scope → 生效段集合 → subprocess 统一短路 ----
    scope = _parse_scope(sys.argv)
    if scope == "auto":
        changed = _git_changed_files()
        scope = "full" if changed is None else _classify_scope(changed)
    if scope not in ("full", "docs", "site"):
        scope = "full"
    if scope == "full":
        active_sections = set(EXPECTED_SECTION_NAMES)
    else:
        active_sections = _SCOPE_CORE | (SCOPE_DOCS_SECTIONS if scope == "docs"
                                         else SCOPE_SITE_SECTIONS)
    print("---- verify_delivery --scope %s（生效段 %d/%d）----"
          % (scope, len(active_sections), len(EXPECTED_SECTION_NAMES)))

    sections_ran = []

    def section(name):
        sections_ran.append(name)

    # subprocess 层统一短路（W698）：当前段不在生效集 → 返回伪造成功结果。
    # _GATE_SUMMARY_MARKERS 保证防静默跳过 wrapper 的「缺汇总行」校验不被误触发；
    # 真 subprocess 引用在打补丁前已完成（_git_changed_files 走原 run）。
    _subprocess_run_real = subprocess.run

    class _SkipResult:
        def __init__(self, name):
            marker = _GATE_SUMMARY_MARKERS.get(name, "")
            self.returncode = 0
            self.stdout = ((marker + "\n") if marker else "") + "（--scope %s 跳过）" % scope
            self.stderr = ""

    def _scoped_run(cmd, *args, **kwargs):
        cur = sections_ran[-1] if sections_ran else ""
        if scope != "full" and cur not in active_sections:
            ok("跳过 [%s]（--scope %s 未覆盖）" % (cur, scope))
            return _SkipResult(cur)
        return _subprocess_run_real(cmd, *args, **kwargs)

    subprocess.run = _scoped_run

    section("期望版本")
    # ---- 期望版本动态取自 CHANGELOG 现役版段（W518；页脚为滞后型手工工件，降级为新鲜度检查）----
    ver, wnum = latest_version_from_changelog(_read(os.path.join(ROOT, "CHANGELOG.md")))
    if not (ver and wnum):
        fail("CHANGELOG.md 未解析出现役版段（期望标题格式 ### vX.Y.Z（日期）：W###）")
    else:
        ok("期望版本动态取自 CHANGELOG 现役段 v%s W%s" % (ver, wnum))

    section("dukou页脚")
    # ---- 读取 dukou-engine.html：页脚新鲜度 + 扫描所有 W### ----
    html = _read(HTML)
    if not html:
        fail("找不到 %s（未生成或被忽略）" % HTML)
    html_w = [int(x) for x in re.findall(r"W(\d{3})", html)]
    max_w_html = max(html_w) if html_w else 0

    fver, fwnum = parse_footer_version(html)
    if fver and fwnum:
        if ver and wnum and int(fwnum) < int(wnum):
            warn("dukou-engine.html 页脚版本 v%s W%s 落后于现役段 W%s"
                 "（页脚为手工工件，建议随批升版，不阻断）" % (fver, fwnum, wnum))
        else:
            ok("dukou-engine.html footer 版本 v%s W%s" % (fver, fwnum))
    else:
        fail("dukou-engine.html footer 未解析出 vX.Y.Z W###")

    section("六文档同步")
    # ---- 降级六文档同步校验（W393）----
    # 核心 2 份（CHANGELOG/交接文档）缺失 v/W → 阻断；
    # 辅助 4 份（README/STRUCTURE/项目说明/file-index）缺失 → WARN 不阻断。
    doc_all = ""
    for d in DOCS:
        p = os.path.join(ROOT, d)
        c = _read(p)
        doc_all += c
        core = d in CORE_DOCS
        if not c:
            if core:
                fail("缺失核心文档: %s" % d)
            else:
                warn("缺失辅助文档（不阻断，可跑 scripts/bump_version.py）: %s" % d)
            continue
        if ver and ("v" + ver) not in c:
            if core:
                fail("%s 不含版本 v%s（旧疾风险·核心阻断）" % (d, ver))
            else:
                warn("%s 不含版本 v%s（辅助文档，跑 scripts/bump_version.py 同步，不阻断）" % (d, ver))
            continue
        if wnum and ("W" + wnum) not in c:
            if core:
                fail("%s 不含 W%s 里程碑 token（旧疾风险·核心阻断）" % (d, wnum))
            else:
                warn("%s 不含 W%s 里程碑 token（辅助文档，跑 scripts/bump_version.py 同步，不阻断）" % (d, wnum))
            continue
        ok("%s 含 v%s / W%s" % (d, ver, wnum))

    section("旁文档同步")
    # ---- 旁文档同步门禁（W526：workflows/README.md 头部版本行 + 里程碑行上限 == 现役 v/W，补 W525 实证盲区）----
    wf = _read(os.path.join(ROOT, ".github", "workflows", "README.md"))
    if not wf:
        fail(".github/workflows/README.md 缺失（旁文档，需人工补回）")
    else:
        wf_v, wf_w = parse_footer_version(wf)
        if wf_v and wf_w:
            if ver and wnum and (wf_v, wf_w) != (ver, wnum):
                fail(".github/workflows/README.md 头部版本 v%s W%s != 现役 v%s W%s"
                     "（旁文档滞后，W499/W525 两次实证复发）" % (wf_v, wf_w, ver, wnum))
            else:
                ok(".github/workflows/README.md 头部版本同步（v%s W%s）" % (wf_v, wf_w))
        else:
            fail(".github/workflows/README.md 未解析出头部版本标记（vX.Y.Z W###）")
        mw = re.search(r"W450-W(\d{3})", wf)
        if mw:
            if wnum and mw.group(1) != wnum:
                fail(".github/workflows/README.md 里程碑行上限 W%s != 现役 W%s（里程碑滞后）" % (mw.group(1), wnum))
            else:
                ok(".github/workflows/README.md 里程碑行上限 W%s == 现役 W%s" % (mw.group(1), wnum))
        else:
            fail(".github/workflows/README.md 未找到 W450-W### 里程碑行")

    section("范围漂移")
    # ---- 范围漂移检测 ----
    doc_w = [int(x) for x in re.findall(r"W(\d{3})", doc_all)]
    # W417：归档文件纳入扫描——归档后旧 W### 仍可追溯，不因归档误报范围漂移
    for a in ARCHIVE_DOCS:
        doc_w += [int(x) for x in re.findall(r"W(\d{3})", _read(os.path.join(ROOT, a)))]
    max_w_doc = max(doc_w) if doc_w else 0
    if max_w_html > max_w_doc:
        fail("范围漂移：%s 引用到 W%d，但六文档+归档最高仅记到 W%d（疑似未记录的改动，需补记或回退）"
             % (os.path.basename(HTML), max_w_html, max_w_doc))
    else:
        ok("无范围漂移（html 最高 W%d ≤ 文档+归档最高 W%d）" % (max_w_html, max_w_doc))

    section("A4计数")
    # ---- A4 计数一致性 ----
    miss = []
    for d in A4_DOCS:
        c = _read(os.path.join(ROOT, d))
        if EXPECT_A4 not in c:
            miss.append(d)
    if miss:
        fail("A4 计数不一致（缺 '%s'）：%s" % (EXPECT_A4, ", ".join(miss)))
    else:
        ok("A4 计数一致（四份文档均含 '%s'）" % EXPECT_A4)

    section("A1-A6计数")
    # ---- A1-A6 真实文件计数 vs README 声明（W417 新增，防计数声明失真）----
    readme_txt = _read(os.path.join(ROOT, "README.md"))
    m_cnt = re.search(r"共\s*(\d+)\s*篇", readme_txt)
    actual_total = 0
    for name, d in A_AREAS:
        n = _count_content_md(d)
        if n < 0:
            warn("%s 目录缺失: %s" % (name, d))
            continue
        actual_total += n
    if m_cnt:
        declared = int(m_cnt.group(1))
        if actual_total == declared:
            ok("A1-A6 真实文件计数 %d 篇 == README 声明 %d 篇（排除各板块 README.md）" % (actual_total, declared))
        else:
            fail("A1-A6 真实文件计数 %d 篇 != README 声明 %d 篇（计数漂移，需同步 README 声明）"
                 % (actual_total, declared))
    else:
        warn("README 未找到 '共 N 篇' 声明，跳过 A1-A6 计数校验")

    section("学术引用")
    # ---- 学术研究 轨显式引用门禁（W452 新增：可核查引用硬性化）----
    acad_total = 0
    acad_missing = []
    for r, _, fns in os.walk(os.path.join(ROOT, "docs")):
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            c = _read(os.path.join(r, fn))
            m = re.search(r"^> 轨标：([^\r\n]+)", c, re.M)
            if not m or m.group(1).strip() != "学术研究":
                continue
            acad_total += 1
            if not re.search(r"^> 引用：.*学术论文索引", c, re.M):
                acad_missing.append(os.path.join(r, fn))
    if acad_total == 0:
        warn("未发现 学术研究 轨文档，跳过显式引用门禁")
    elif acad_missing:
        fail("学术研究 轨文档 %d 篇缺显式引用（缺 '> 引用：' 学术论文索引 链接）：%s"
             % (len(acad_missing), ", ".join(acad_missing[:5])))
    else:
        ok("学术研究 轨文档 %d 篇均含显式引用（> 引用：学术论文索引 链接）" % acad_total)

    section("A1导航")
    # ---- A1 导航相邻性断言（W422 新增：W418 只保证"每回有导航行"不保证指向相邻回）----
    ch_dir = os.path.join(ROOT, "docs", "01-全书逐回解读")
    nav_fail = []
    if os.path.isdir(ch_dir):
        for fn in sorted(os.listdir(ch_dir)):
            m = re.match(r"^第(\d+)回-", fn)
            if not m or not fn.endswith(".md"):
                continue
            num = int(m.group(1))
            c = _read(os.path.join(ch_dir, fn))
            nm = re.search(r"(?m)^>\s*导航：.*$", c)
            if not nm:
                nav_fail.append("第%d回 无导航行" % num)
                continue
            line = nm.group(0)
            pm = re.search(r"\[上一回\]\(第(\d+)回", line)
            xm = re.search(r"\[下一回\]\(第(\d+)回", line)
            if num > 1:
                if not pm or int(pm.group(1)) != num - 1:
                    nav_fail.append("第%d回 上一回 -> %s（期望第%d回）" % (num, pm.group(1) if pm else "无", num - 1))
            elif pm:
                nav_fail.append("第1回 不应有上一回链接")
            if num < 100:
                if not xm or int(xm.group(1)) != num + 1:
                    nav_fail.append("第%d回 下一回 -> %s（期望第%d回）" % (num, xm.group(1) if xm else "无", num + 1))
            elif xm:
                nav_fail.append("第100回 不应有下一回链接")
    if nav_fail:
        fail("A1 导航相邻性异常 %d 处（示例：%s）" % (len(nav_fail), nav_fail[0]))
    else:
        ok("A1 导航相邻性 100/100（上一回=N-1·下一回=N+1·第1回无上/第100回全书完）")

    section("docs链接")
    # ---- docs 全量链接校验门禁（W422 建置 docs/01 · W699 扩为 docs 全量：
    # 挂载即绿 5191 链接 0 broken；lint_links 内建三豁免=docs/archive 冻结档/
    # gitignore 本地件（S4 双盲件）/fenced+inline code 去噪）----
    try:
        r = subprocess.run(
            [sys.executable, os.path.join(_HERE, "lint_links.py"),
             "--dir", os.path.join(ROOT, "docs")],
            capture_output=True, text=True, timeout=300)
        if r.returncode == 0:
            ok("docs 全量链接校验通过（lint_links 0 broken）")
        else:
            # W700 热修：tail 只捞 BROKEN/汇总行——原 stdout[-3:] 会混入 OK 行（CI 首跑实证）
            tail = ([x for x in r.stdout.splitlines()
                     if "[BROKEN]" in x or "校验完成" in x][-3:]
                    + r.stderr.splitlines()[-3:])
            fail("docs 存在 broken 链接（lint_links exit %d）：%s" % (r.returncode, " / ".join(tail)))
    except Exception as e:
        fail("docs 链接校验执行异常: %s" % e)

    section("sitemap覆盖")
    # ---- sitemap 覆盖校验（W422：防新增页面漏收录，W417 曾手工补 69→154）----
    sm_txt = _read(os.path.join(ROOT, "site", "sitemap.xml"))
    site_dir = os.path.join(ROOT, "site")
    EXCLUDED_SM = {
        "rum-viewer.html",
        "visit-viewer.html",
        "_template.html",
        "data/81-hardships-view.html",
        "data/character-relationship-3d-view.html",
        "data/_shell.html",
    }
    if sm_txt and os.path.isdir(site_dir):
        locs = set()
        for m in re.finditer(r"<loc>([^<]+)</loc>", sm_txt):
            u = m.group(1).strip().rstrip("/")
            u = re.sub(r"^https?://[^/]+/", "", u)
            u = u[len("xiyouji/"):] if u.startswith("xiyouji/") else u
            locs.add(u if u else "index.html")
        actual = set()
        for root, _dirs, fnames in os.walk(site_dir):
            for fn in fnames:
                if fn.endswith(".html"):
                    rel = os.path.relpath(os.path.join(root, fn), site_dir).replace("\\", "/")
                    actual.add(rel)
        expected = {x for x in actual if x not in EXCLUDED_SM}
        miss = sorted(expected - locs)
        extra = sorted(locs - expected)
        if miss or extra:
            fail("sitemap 与 site 不一致：缺 %d 页（%s）、多余 %d 页（%s）"
                 % (len(miss), miss[:3], len(extra), extra[:3]))
        else:
            ok("sitemap 覆盖一致（%d 页，排除统计/预览页 %d 个）" % (len(locs), len(EXCLUDED_SM)))
    else:
        warn("sitemap.xml 或 site/ 缺失，跳过 sitemap 覆盖校验")

    section("内嵌回退")
    # ---- site/data 内嵌回退模式静态检查（W422：file:// 铁律的自动验证）----
    data_dir = os.path.join(ROOT, "site", "data")
    EMB_RE = re.compile(r"EMBEDDED_DATA|const\s+EMBEDDED|FALLBACK|INLINE|MOCK_DATA|const\s+data\s*=|text-search-app")
    no_emb = []
    data_count = 0
    if os.path.isdir(data_dir):
        for fn in sorted(os.listdir(data_dir)):
            if fn.endswith(".html"):
                data_count += 1
                if not EMB_RE.search(_read(os.path.join(data_dir, fn))):
                    no_emb.append(fn)
    if no_emb:
        fail("site/data 有 %d/%d 页缺内嵌回退模式（file:// 直开风险）：%s"
             % (len(no_emb), data_count, ", ".join(no_emb[:5])))
    else:
        ok("site/data %d 页均含内嵌回退模式（EMBEDDED_DATA/EMBEDDED/FALLBACK/inline data）" % data_count)

    section("双源漂移")
    # ---- M2 双源漂移检查（W424：内嵌数据 vs scripts/output/data JSON 数组长度）----
    # 防"内嵌副本为空/过期、线上 fetch 404 后回退到错误数据"（81-hardships 先例）
    drift_js = os.path.join(ROOT, "scripts", "check_data_drift.js")
    try:
        r = subprocess.run(["node", drift_js], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("数据漂移检查通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("数据漂移检查失败（exit %d）：%s" % (r.returncode, " / ".join(tail)))
    except FileNotFoundError:
        warn("node 不可用，跳过数据漂移检查（W424 M2）")
    except Exception as e:
        warn("数据漂移检查执行异常（W424 M2）: %s" % e)

    section("CSP漂移")
    # ---- CSP 漂移检查（W424：全站 CSP meta 必须与内联脚本哈希一致）----
    # 改任何内联脚本后未重跑 generate_csp.py 会在此拦截（页面脚本会被 CSP 拦死）
    csp_py = os.path.join(_HERE, "generate_csp.py")
    try:
        r = subprocess.run(
            [sys.executable, csp_py, "--check"],
            capture_output=True, text=True, timeout=180,
        )
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("CSP 校验通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("CSP 漂移（exit %d）：%s（改内联脚本后须重跑 python scripts/generate_csp.py）"
                 % (r.returncode, " / ".join(tail)))
    except Exception as e:
        warn("CSP 校验执行异常（W424）: %s" % e)

    section("腐蚀插件")
    # ---- 腐蚀/插件引用门禁（W424 复盘沉淀：EN 腐蚀第二波 + sankey 漏引防复发）----
    corr_py = os.path.join(_HERE, "check_corruption.py")
    try:
        r = subprocess.run([sys.executable, corr_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("腐蚀/插件引用门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("腐蚀/插件引用门禁失败（exit %d）：%s" % (r.returncode, " / ".join(tail)))
    except Exception as e:
        warn("腐蚀/插件引用门禁执行异常（W424 复盘沉淀）: %s" % e)

    section("内联语法")
    # ---- 内联脚本语法门禁（W457：EN 引号/撇号/键名腐蚀致 SyntaxError 曾 7 页漏网）----
    js_syntax_js = os.path.join(_HERE, "check_js_syntax.js")
    try:
        r = subprocess.run(["node", js_syntax_js], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("内联脚本语法门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("内联脚本语法错误（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except FileNotFoundError:
        warn("node 不可用，跳过内联脚本语法门禁（W457）")
    except Exception as e:
        warn("内联脚本语法门禁执行异常（W457）: %s" % e)

    section("CSS平衡")
    # ---- CSS 结构平衡门禁（W457：url() 缺右括号致整页 CSS 裸奔白屏，222 页先例）----
    struct_py = os.path.join(_HERE, "check_structure.py")
    try:
        r = subprocess.run([sys.executable, struct_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("CSS 结构平衡通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("CSS 结构异常（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("CSS 结构平衡门禁执行异常（W457）: %s" % e)

    section("token覆盖")
    # ---- token 覆盖率门禁（W493 E6 转正：M2/M3 页面私有 <style> 裸色/裸阴影防回归）----
    tok_py = os.path.join(_HERE, "check_token_coverage.py")
    try:
        r = subprocess.run([sys.executable, tok_py], capture_output=True, text=True, timeout=180)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("token 覆盖率门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("token 覆盖率违规（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("token 覆盖率门禁执行异常（W493）: %s" % e)

    section("动效禁令")
    # ---- 动效禁止清单门禁（W493 E6 转正：D4 bounce/旋转/无限循环/parallax 防回归）----
    motion_py = os.path.join(_HERE, "check_motion_ban.py")
    try:
        r = subprocess.run([sys.executable, motion_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("动效禁止清单门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("动效禁止清单违规（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("动效禁止清单门禁执行异常（W493）: %s" % e)

    section("a11y对比")
    # ---- a11y 对比度门禁（W493 E6 转正：M1 WCAG AA，P0/P1 阻断）----
    a11y_py = os.path.join(_HERE, "a11y_audit.py")
    try:
        r = subprocess.run([sys.executable, a11y_py, "--dir", "site", "--format", "json", "--quiet"],
                           capture_output=True, text=True, timeout=300)
        if r.returncode == 0:
            try:
                import json as _json
                rep = _json.loads(r.stdout)
                s = rep.get("summary", {})
                e22 = s.get("E2-2", {})
                p01 = (e22.get("P0", 0) or 0) + (e22.get("P1", 0) or 0)
                if p01 == 0:
                    ok("a11y 对比度门禁通过（E2-2 P0/P1=0）")
                else:
                    fail("a11y 对比度 P0+P1=%d（M1 WCAG AA 阻断）" % p01)
            except Exception:
                ok("a11y 审计完成（summary 解析跳过）")
        else:
            fail("a11y_audit 失败（exit %d）：%s" % (r.returncode, (r.stderr or r.stdout).splitlines()[-1:]))
    except Exception as e:
        warn("a11y 对比度门禁执行异常（W493）: %s" % e)

    section("INLINED完整")
    # ---- INLINED CSS 完整性门禁（W495 转正：W493 事故曾清空 224 页内联块而 14 门禁全绿漏网）----
    inl_py = os.path.join(_HERE, "check_inlined_css.py")
    try:
        r = subprocess.run([sys.executable, inl_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("INLINED CSS 门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("INLINED CSS 块异常（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("INLINED CSS 门禁执行异常（W495）: %s" % e)

    section("动态链接")
    # ---- 动态链接门禁（W459：lint_links 只扫静态 href，JS 拼接链接曾致 D2 回目跳转全 404 漏网）----
    dyn_links_py = os.path.join(_HERE, "check_dynamic_links.py")
    try:
        r = subprocess.run([sys.executable, dyn_links_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("动态链接门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("动态链接死链（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("动态链接门禁执行异常（W459）: %s" % e)

    section("治理契约")
    # ---- 治理文档维护契约门禁（2026-08-18：防追加式乱写·WARN 起步，不阻断提交）----
    gov_py = os.path.join(_HERE, "check_governance_docs.py")
    try:
        r = subprocess.run([sys.executable, gov_py], capture_output=True, text=True, timeout=60)
        tail = (r.stdout.splitlines()[-4:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("治理文档维护契约通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            warn("治理文档维护契约告警（exit %d）：%s" % (r.returncode, " / ".join(tail[:4])))
    except Exception as e:
        warn("治理文档维护契约门禁执行异常: %s" % e)

        warn("Skills 索引一致性门禁执行异常（W498）: %s" % e)

    section("索引健康")
    # ---- 索引健康门禁（W500 转正：W499 全面审查——file-index 空壳/重复/残留 + 方法论 README 漏登记 + CHANGELOG 编号上限手工漏改）----
    idx_health_py = os.path.join(_HERE, "check_index_health.py")
    try:
        r = subprocess.run([sys.executable, idx_health_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("索引健康门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("索引健康异常（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("索引健康门禁执行异常（W500）: %s" % e)

    section("元信息块")
    # ---- 元信息块 v2 门禁（W501：内容可信度轨——新文件必须含血缘 + 核验状态 4 字段，基线豁免存量 611 篇）----
    fm_py = os.path.join(_HERE, "check_frontmatter.py")
    try:
        r = subprocess.run([sys.executable, fm_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("元信息块 v2 门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("元信息块 v2 缺字段/枚举非法（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("元信息块 v2 门禁执行异常（W501）: %s" % e)

    section("术语一致")
    # ---- 术语一致性门禁（W502：术语表↔glossary.json 双向同步 + 人物称谓规范词锚定·基线豁免 383 条）----
    gl_py = os.path.join(_HERE, "check_glossary.py")
    try:
        r = subprocess.run([sys.executable, gl_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("术语一致性门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("术语一致性异常（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("术语一致性门禁执行异常（W502）: %s" % e)

    section("引文核验")
    # ---- 原著引文硬验证门禁（W503：`> 原文引文（第N回）` 行必须对 text-search.json 精确命中，防 AI 幻觉引文）----
    cite_py = os.path.join(_HERE, "check_citations.py")
    try:
        r = subprocess.run([sys.executable, cite_py, "--dir", "docs"],
                           capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("原著引文核验通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("原著引文未命中/格式错误（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("原著引文核验门禁执行异常（W503）: %s" % e)
    section("图表自洽")
    # ---- 图表静态自洽门禁（W551：W550 全站截图审查实证三类批量图表缺陷——10 页桑基缺引用 /
    # 4 组饼图措辞×树图实现错配——均为门禁盲区积累数月后人工清账。本门禁文本层拦同类复发；
    # 需真实渲染的遮挡/空带/溢出/桑基运行时由 check_screenshot_gates.js（screenshot-review
    # workflow 动态步）覆盖）----
    cgd_py = os.path.join(_HERE, "check_chart_data.py")
    try:
        r = subprocess.run([sys.executable, cgd_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("图表静态自洽门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("图表静态自洽异常（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("图表静态自洽门禁执行异常（W551）: %s" % e)

    section("数据一致")
    # ---- 数据内容一致性门禁（W555：方案 C L1 站内自洽常驻化，经用户确认挂载为第 25 门禁。
    # 源自 W550 实证三类同页数字矛盾（relationships 89/88、narratology-13d 13/16/17、six-senses 5/4）。
    # --gate 模式：content-consistency-baseline.txt 冻结存量误报（W554 逐条人工裁决 4 条），
    # 新增矛盾 = FAIL 阻断。L2 对账 / L3 语义判读不在本门禁范围（报告型，见 W554 审计报告））----
    cct_py = os.path.join(_HERE, "check_content_consistency.py")
    try:
        r = subprocess.run([sys.executable, cct_py, "--gate"], capture_output=True, text=True, timeout=180)
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("数据内容一致性门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("数据内容一致性异常（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("数据内容一致性门禁执行异常（W555）: %s" % e)

    section("W区间字面量")
    # ---- W 号区间字面量门禁（W628 挂载·第 27 门禁·经用户指令防复发：现役叙述面
    # 「W001-Wxxx」覆盖上限字面量终点须等于现役 max W + CITATION.cff 版本同步）----
    wrl_py = os.path.join(_HERE, "check_w_range_literal.py")
    try:
        r = subprocess.run([sys.executable, wrl_py], capture_output=True, text=True, timeout=60)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("W 号区间字面量门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("W 号区间字面量漂移（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("W 号区间字面量门禁执行异常（W628）: %s" % e)

    section("SEOhead")
    # ---- SEO head 门禁（W630 挂载·第 26 门禁·slot 自 W591 预留：og/canonical/JSON-LD/
    # hreflang/sitemap 集合一致——SEO head 为静默腐烂面·经用户裁决挂载）----
    seo_py = os.path.join(_HERE, "check_seo_head.py")
    try:
        r = subprocess.run([sys.executable, seo_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("SEO head 门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("SEO head 异常（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("SEO head 门禁执行异常（W630）: %s" % e)


    section("可引用性")
    # ---- 可视化可引用性门禁（2026-10-02 用户裁决挂载·第 28 门禁·B-6 第一步：slot 自 W638 预留。
    # 来源=W636 缺口发现 / W637 门禁升级路径（WARN+基线只增·W555 先例）/ W638 出处四字段收编。
    # 经用户批准开工=反转 B-6 三次「登记不开工」裁决（registry 已记账）。
    # 基线 scripts/output/citability-baseline.txt 冻结存量 326 项缺口（86 页×4 项=344·D1 裁决仅 site/data）；
    # 基线外新增违规 = FAIL 阻断；存量 WARN 面转 FAIL 的时点=D4 裁决「missing 收敛至阈值以下」，不预设日期）----
    cit_py = os.path.join(_HERE, "check_citability.py")
    try:
        r = subprocess.run([sys.executable, cit_py, "--gate"], capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail("可视化可引用性门禁执行异常（第 28 门禁·crash 即拦不静默放过·W650 对齐 W631 防静默跳过）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("可引用性基线外违规（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 28 门禁：" not in r.stdout:
            fail("可引用性门禁输出缺汇总行（疑似未真正扫描·防静默跳过 W650）：%r" % r.stdout[-160:])
        else:
            ok("可视化可引用性门禁通过（%s）" % (r.stdout.splitlines()[-1] if r.stdout.splitlines() else "无输出"))


    section("设计令牌对账")
    # ---- 设计令牌文档对账门禁（PD-5·W652：design-tokens.json/design.md ↔ tokens.css 双向对账——
    # 防 DESIGN.md §2 手写表与单一事实源静默漂移（W652 首跑实证 6 处值漂移已同步+15 页面本地令牌白名单）·
    # wrapper 防静默跳过与第 28 门禁同款：crash 即拦+汇总行校验）----
    pd5_py = os.path.join(_HERE, "check_design_doc_drift.py")
    try:
        r = subprocess.run([sys.executable, pd5_py], capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail("设计令牌对账门禁执行异常（PD-5·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("设计令牌对账漂移（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 设计令牌对账：" not in r.stdout:
            fail("设计令牌对账输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("设计令牌文档对账通过（%s）" % (r.stdout.splitlines()[-1] if r.stdout.splitlines() else "无输出"))


    section("色盲安全")
    # ---- 色盲安全门禁（第 29 槽·PD-1a·W653：D-6 裁决 WARN+基线冻结——Machado 二型模拟+CIEDE2000
    # ΔE<10 成对检查·基线 17428 对冻结·基线外新增 FAIL·口径=light 静态（暗色 computed 态归 PD-4）·
    # wrapper 防静默跳过与第 28 门禁同款）----
    cb_py = os.path.join(_HERE, "check_chart_colorblind.py")
    try:
        r = subprocess.run([sys.executable, cb_py, "--gate"], capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail("色盲安全门禁执行异常（第 29 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("色盲安全基线外违规（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 29 门禁 色盲安全：" not in r.stdout:
            fail("色盲安全门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("色盲安全门禁通过（%s）" % (r.stdout.splitlines()[-1] if r.stdout.splitlines() else "无输出"))


    section("降级声明")
    # ---- 窄屏降级声明门禁（第 30 槽·PD-1b·W654：§4B 选型章配套——site/data 每页须声明
    # chart-degrade: stacked|scroll-x|simplified|n/a（静态解析不启浏览器）·wrapper 防静默跳过同前）----
    dg_py = os.path.join(_HERE, "check_chart_degrade.py")
    try:
        r = subprocess.run([sys.executable, dg_py], capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail("降级声明门禁执行异常（第 30 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("降级声明缺失/非法（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 30 门禁 降级声明：" not in r.stdout:
            fail("降级声明门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("降级声明门禁通过（%s）" % (r.stdout.splitlines()[-1] if r.stdout.splitlines() else "无输出"))


    section("文档口径")
    # ---- 文档口径体检门禁（第 31 槽·W663：doc-sync——代码/提交真值 vs 文档当前态声明反向对拍
    # 四类窄句式（README 抬头/交接头链/门禁清单上限/提交-版段对账·D2 对账表登记即豁免）·
    # wrapper 防静默跳过与第 29/30 槽同款）----
    ds_py = os.path.join(_HERE, "check_doc_sync.py")
    try:
        r = subprocess.run([sys.executable, ds_py], capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail("文档口径体检执行异常（第 31 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("文档口径体检失配（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 31 门禁 文档口径体检：" not in r.stdout:
            fail("文档口径体检输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("文档口径体检通过（%s）" % (r.stdout.splitlines()[-1] if r.stdout.splitlines() else "无输出"))


    section("CLAUDE速查")
    # ---- CLAUDE.md 速查层完整性门禁（第 32 槽·W667/S-02：指针存在性+章节锚点对拍+行数≤60+
    # 正文禁漂移字面量——防速查层断链与数字腐烂·wrapper 防静默跳过与第 29/30/31 槽同款）----
    cm_py = os.path.join(_HERE, "check_claude_md.py")
    try:
        r = subprocess.run([sys.executable, cm_py], capture_output=True, text=True, timeout=60)
    except Exception as e:
        fail("CLAUDE.md 速查层门禁执行异常（第 32 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("CLAUDE.md 速查层失配（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 32 门禁 CLAUDE.md 速查层：" not in r.stdout:
            fail("CLAUDE.md 速查层门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("CLAUDE.md 速查层门禁通过（%s）" % (r.stdout.splitlines()[-1] if r.stdout.splitlines() else "无输出"))


    section("head内容")
    # ---- head 内容合法性门禁（第 33 槽·W672/WP-1.3：head 区间剥 script/style/noscript/注释后
    # 只允许 head 合法开标签——防 W657 式注入器把 body 内容写进 </head> 之前（foster parenting
    # 视觉侥幸、源码畸形）。wrapper 防静默跳过与第 29/30/31/32 槽同款）----
    hc_py = os.path.join(_HERE, "check_html_head_content.py")
    try:
        r = subprocess.run([sys.executable, hc_py], capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail("head 内容门禁执行异常（第 33 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("head 内容违例（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 33 门禁 head 内容：" not in r.stdout:
            fail("head 内容门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("head 内容门禁通过（%s）" % (r.stdout.splitlines()[-1] if r.stdout.splitlines() else "无输出"))


    section("CSS变量引用")
    # ---- CSS 变量引用门禁（第 34 槽·W672/WP-1.4：style 块内每个无 fallback var(--x) 必须在
    # 已知定义集（tokens ∪ 页内 style 块 ∪ 内联属性 ∪ JS 文本·扫描器 3 宽口径，--chain-color
    # 运行时定义豁免）——防未定义变量 computed-value invalid 静默失效。wrapper 同款）----
    cv_py = os.path.join(_HERE, "check_css_var_refs.py")
    try:
        r = subprocess.run([sys.executable, cv_py], capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail("CSS 变量引用门禁执行异常（第 34 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("CSS 变量引用违例（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 34 门禁 CSS 变量引用：" not in r.stdout:
            fail("CSS 变量引用门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("CSS 变量引用门禁通过（%s）" % (r.stdout.splitlines()[-1] if r.stdout.splitlines() else "无输出"))


    section("声明分隔")
    # ---- 声明分隔门禁（第 35 槽·W673/WP-2.6：CSS 缺分号=整条声明静默丢弃（442 处实证 W558/W673
    # 修复）——换行形态+同行双通道判定，剥注释后扫描·规则末条豁免。wrapper 防静默跳过同款）----
    ds2_py = os.path.join(_HERE, "check_css_decl_separators.py")
    try:
        r = subprocess.run([sys.executable, ds2_py], capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail("声明分隔门禁执行异常（第 35 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("声明分隔违例（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 35 门禁 声明分隔：" not in r.stdout:
            fail("声明分隔门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("声明分隔门禁通过（%s）" % (r.stdout.splitlines()[-1] if r.stdout.splitlines() else "无输出"))


    section("孤立选择")
    # ---- 孤立选择器门禁（第 36 槽·W673/WP-2.6：残缀行与后继规则拼成错误后代选择器致规则静默
    # 死亡（84 命中+130 连带=214 行实证 W673 修复）——逗号结尾合法列表豁免。wrapper 同款）----
    os_py = os.path.join(_HERE, "check_css_orphan_selectors.py")
    try:
        r = subprocess.run([sys.executable, os_py], capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail("孤立选择器门禁执行异常（第 36 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("孤立选择器违例（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 36 门禁 孤立选择器：" not in r.stdout:
            fail("孤立选择器门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("孤立选择器门禁通过（%s）" % (r.stdout.splitlines()[-1] if r.stdout.splitlines() else "无输出"))


    section("kpi基类")
    # ---- kpi-card 基类门禁（第 37 槽·W673/WP-2.6：W557 基类被 W563 洗掉 122 页裸奔的复发防
    # 线——C1 system.css 含全局 .kpi-card 规则 + C2 使用页 INLINED 块含该规则（link 直引豁免）。
    # wrapper 同款）----
    kc_py = os.path.join(_HERE, "check_kpi_card_base.py")
    try:
        r = subprocess.run([sys.executable, kc_py], capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail("kpi 基类门禁执行异常（第 37 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("kpi 基类违例（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 37 门禁 kpi 基类：" not in r.stdout:
            fail("kpi 基类门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("kpi 基类门禁通过（%s）" % (r.stdout.splitlines()[-1] if r.stdout.splitlines() else "无输出"))

    section("内嵌残留")
    # ---- 页面内嵌残留标记门禁（第 38 槽·W693/W692 报告 A-01 用户裁决：json 副本修复批的
    # EMBEDDED 双路径回归防线——修复前旧值即标记（W691 review 6 页漏网样本即验收用例），
    # 新增标记随批在 MARKERS 登记。wrapper 同款）----
    em_py = os.path.join(_HERE, "check_embedded_stale_markers.py")
    try:
        r = subprocess.run([sys.executable, em_py], capture_output=True, text=True, timeout=180)
    except Exception as e:
        fail("内嵌残留门禁执行异常（第 38 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("内嵌残留标记命中（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 38 门禁 页面内嵌残留标记：" not in r.stdout:
            fail("内嵌残留门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("内嵌残留门禁通过（%s）" % (r.stdout.splitlines()[-2] if len(r.stdout.splitlines()) >= 2 else "无输出"))


    section("时间线双源")
    # ---- 故事内时间线双源同步门禁（第 39 槽·W695 用户裁决：六轮外审 P1-4——
    # timeline.py KEY_EVENTS 与 story-timeline.html EMBEDDED_DATA 为人工同步，
    # 本门禁即机器防线：逐条比对 chapter/event/characters/顺序 + phase 区间映射。wrapper 同款）----
    ts_py = os.path.join(_HERE, "check_story_timeline_sync.py")
    try:
        r = subprocess.run([sys.executable, ts_py], capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail("时间线双源门禁执行异常（第 39 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("时间线双源失配（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 39 门禁 故事内时间线双源同步：" not in r.stdout:
            fail("时间线双源门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("时间线双源门禁通过（%s）" % (r.stdout.splitlines()[-2] if len(r.stdout.splitlines()) >= 2 else "无输出"))


    section("chapter双源")
    # ---- chapter_stats 双源同步门禁（第 40 槽·W699 用户裁决「挂载为 verify 第 40 槽」：
    # chapter_stats.py 纯 regex 确定性分析——重跑生成器为真值与页面 EMBEDDED 全量比对；
    # 以重跑产物为基准使校验器 CI 可复现（gitignored 本地 json 不作基准）。wrapper 同款）----
    cs_py = os.path.join(_HERE, "check_chapter_stats_sync.py")
    try:
        r = subprocess.run([sys.executable, cs_py], capture_output=True, text=True, timeout=300)
    except Exception as e:
        fail("chapter双源门禁执行异常（第 40 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("chapter双源漂移（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 40 门禁 chapter_stats 双源同步：" not in r.stdout:
            fail("chapter双源门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("chapter双源门禁通过（%s）" % (r.stdout.splitlines()[-2] if len(r.stdout.splitlines()) >= 2 else "无输出"))


    # ---- 可选：RAG /health 探活（仅告警，不阻断）----
    if "--health" in sys.argv:
        try:
            r = urllib.request.urlopen("http://127.0.0.1:8777/health", timeout=5)
            body = json.loads(r.read().decode("utf-8"))
            ok("/health 存活：%s" % body)
        except Exception as e:
            print("WARN  /health 不可达（环境项，不阻断提交）：%s" % e)

    # ---- 门禁段自洽锁（VERIFY_SECTIONS·W663/T3：声明段集合 == 实跑段集合，缺段即红；
    # W698 scope 分级：非 full 档按生效子集断言，full 档仍断言全量 43 段）----
    expected_sections = list(EXPECTED_SECTION_NAMES) if scope == "full" else \
        [n for n in EXPECTED_SECTION_NAMES if n in active_sections]
    missing_sections = [n for n in expected_sections if n not in sections_ran]
    if missing_sections:
        fail("门禁段实跑 %d ≠ 声明 %d：缺 %s（VERIFY_SECTIONS 自洽锁·--scope %s）"
             % (len(set(sections_ran)), len(expected_sections),
                "、".join(missing_sections), scope))
    else:
        ok("门禁段自洽锁：实跑 %d 段 == 声明 %d 段（--scope %s）"
           % (len(expected_sections), len(expected_sections), scope))

    print("\n==== 交付校验汇总 ====")
    if fails == 0:
        print("核心全部通过 ✅" + ("（%d 项辅助 WARN，不阻断）" % warns if warns else ""))
        return 0
    print("%d 项核心 FAIL ❌（%d 项辅助 WARN）" % (fails, warns))
    return 1


if __name__ == "__main__":
    sys.exit(main())
