#!/usr/bin/env python3
"""
verify_delivery.py — 零依赖交付校验门禁（Senior Developer 设立）

解决两类工程顽疾：
  1) 「旧疾」：单文件连续多次 Edit 时描述段丢失 → 校验文档均含最新版本号 + W### 里程碑 token。
  2) 「范围漂移」：已评审/已记录 scope 之外又发生了改动（如 html 里出现 W334 标记但文档只记到 W333）
     → 校验 site/dukou-engine.html 中引用的所有 W### 是否都已在文档中记录。

降级六文档同步（W393）：
  - 核心 2 份（CHANGELOG.md / HANDOVER.md）= 跨 session 连续性真载体，缺失 v/W 仍【阻断】。
  - 辅助 4 份（README.md / STRUCTURE.md / 项目说明.md / file-index.md）= 每次 W### 的纯手工税，
    缺失仅【WARN 不阻断】，里程碑时跑 scripts/bump_version.py 一键补齐。

动态期望版本（W518）：六文档同步的期望 v/W 不再锚定 dukou-engine.html 页脚（滞后型
  手工工件，辅助文档升版后必现"不含旧版"噪音 WARN），改为动态取 CHANGELOG 倒序首个
  版段（现役段）；页脚自身降级为新鲜度被检对象，落后现役段仅【WARN 不阻断】。

fail-closed 委派语义（W831·用户批准修 B1/B2·CLAUDE.md 第 10 条授权）：门禁子进程崩溃/
  超时/输出不可解析/汇总结构缺失 = 判据不可执行 → 一律 FAIL。原 _run_simple_gate 异常记
  WARN、a11y 段 JSON 解析失败记 OK，使「从未通过的门禁」伪装「通过」、整轮仍报核心全部
  通过 + exit 0（T03 审查实证·本轮根除）；唯一例外为 Gate.missing_warn 登记的运行期缺失
  降级（W424 M2·仅 2 个 node 段·显式 opt-in）。

零依赖：仅标准库。可直接运行：
  python scripts/verify_delivery.py            # 静态校验（提交前门禁）
  python scripts/verify_delivery.py --health   # 额外探测 RAG /health（环境项，仅告警不阻断）

退出码：核心 FAIL 1；仅辅助 WARN 0。可直接挂到 .git/hooks/pre-commit（辅助 WARN 不再阻断提交）。

结构（W728 重构：原 905 行单体 main() 拆为五层·行为与输出逐字节不变）：
  模块级常量 → scope 分级工具 → 版本解析工具 → _Reporter/_GateContext（上报与执行态）
  → 门禁参数表（_SimpleGate×18 / _StrictGate×16）→ 通用 runner×2 → 13 个段函数
  → 收尾三函数 → main() 编排（52 段执行序 == EXPECTED_SECTION_NAMES 声明序·段自洽锁对账）。
"""

import json
import os
import re
import subprocess
import sys
import urllib.request
from typing import NamedTuple

from doc_areas import AREA_DIRS, count_content_md

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
    "文档口径",
    "CLAUDE速查",
    "head内容",
    "CSS变量引用",
    "声明分隔",
    "孤立选择",
    "kpi基类",
    "内嵌残留",
    "时间线双源",
    "chapter双源",
    "AGENTS分层",
    "脚本覆盖",
    "可视化数据",
    "英文站",
    "目录文档",
    "搜索索引",
    "性能影子",
    "计划方案合规",
    "朱砂实底",
]

# ---- scope 分级（W698·用户裁决「动工」，P2-2 落地）：pre-commit 按变更路径跑受影响门禁子集 ----
# 四态：full=全量（缺省·CI verify-delivery job·批收尾七步③恒为 full）；docs=文档轨子集；
# site=页面轨+级联相关文档段；auto=按变更路径白名单分类（任何越界文件保守回退 full）。
# 11 个内联廉价段（= _SCOPE_CORE 全集·W713 补齐原漏 7 段的自洽锁盲区）恒跑不跳；跳过只作用于
# 38 个 subprocess 委托段（50 段 - 12 内联/bespoke·W781 注册表派生与 EXPECTED 补齐第 45 槽段名后校数）：_scoped_run 统一短路，
# _GATE_SUMMARY_MARKERS 兜住防静默跳过 wrapper 的汇总行
# 校验（fake stdout 含段标记，wrapper 不会误判「缺汇总行」）；段自洽锁按 scope 断言子集。
_DOC_FILES_RE = re.compile(
    r"^(docs/.+\.md|(CHANGELOG|HANDOVER|README|STRUCTURE|CLAUDE)\.md|"
    r"scripts/output/file-index(-archive)?\.md|CITATION\.cff|"
    r"\.github/workflows/README\.md|AGENTS\.md|dataset/glossary\.json)$")
_SITE_FILES_RE = re.compile(
    r"^(site/.+\.(html|css|js|xml)|dataset/.+\.json|scripts/output/data/.+\.json)$")
SCOPE_DOCS_SECTIONS = {
    "docs链接", "治理契约", "索引健康", "元信息块", "术语一致", "引文核验",
    "W区间字面量", "文档口径", "CLAUDE速查", "搜索索引", "计划方案合规",
}
SCOPE_SITE_SECTIONS = {
    "双源漂移", "CSP漂移", "腐蚀插件", "内联语法", "CSS平衡", "token覆盖",
    "动效禁令", "a11y对比", "INLINED完整", "动态链接", "图表自洽", "数据一致",
    "SEOhead", "可引用性", "设计令牌对账", "色盲安全", "降级声明", "head内容",
    "朱砂实底",
    "CSS变量引用", "声明分隔", "孤立选择", "kpi基类", "内嵌残留", "时间线双源", "chapter双源", "可视化数据", "英文站",
    "文档口径", "W区间字面量", "索引健康", "治理契约", "AGENTS分层", "搜索索引", "性能影子",
}
_SCOPE_CORE = {  # W713：11 个内联廉价段全集入 core（原仅 4 段·旁文档/A4/A1-A6/学术/A1导航/sitemap/内嵌回退 7 段不在任何 scope 集=自洽锁盲区）
    "期望版本", "dukou页脚", "六文档同步", "旁文档同步", "范围漂移",
    "A4计数", "A1-A6计数", "学术引用", "A1导航", "sitemap覆盖", "内嵌回退",
}
# _GATE_SUMMARY_MARKERS 已由 _STRICT_GATES 元组派生（W781 R-1·见 _STRICT_GATES 定义后），
# 手工字典删除——挂槽漏登记即启动期断言红（W780 实证：漏登记会在 --scope 跳过路径爆「缺汇总行」假红）


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
    "HANDOVER.md",
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
           os.path.join("docs", "00-导读", "项目说明.md"), "HANDOVER.md"]
EXPECT_A4 = "209 篇"  # 真实计数（W342 199→201 起步，W400 后实际 209）

# 归档文件（W417 新增）：归档后旧 W### 仍纳入范围漂移可追溯扫描，避免误报
# W513：CHANGELOG-ARCHIVE 二级归档层（W001-W399）同纳入扫描
ARCHIVE_DOCS = [
    os.path.join("archive", "docs", "CHANGELOG-ARCHIVE.md"),
    os.path.join("archive", "docs", "CHANGELOG-ARCHIVE-tier2.md"),
    os.path.join("archive", "docs", "file-index-ARCHIVE.md"),
    os.path.join("archive", "docs", "HANDOVER-ARCHIVE.md"),
]

# A1-A6 内容板块真实文件计数 vs README 声明（W417 新增，防计数声明失真）
# 目录单一事实源在 doc_areas.AREA_DIRS（W728 与 sync_docs 共享·防双份手工表漂移）；
# 展示标签属呈现层留本文件。计数口径 = count_content_md（排除各板块 README.md）。
A_AREAS = list(zip(
    ("A1 逐回解读", "A2 个人随笔", "A3 人物分析", "A4 主题专题", "A5 文化背景", "A6 诗词歌赋"),
    AREA_DIRS,
    strict=True,  # 标签数与目录数必须一致（6=6·长度失配即口径装配错误）
))


def _read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def latest_version_from_changelog(text):
    """从 CHANGELOG 文本解析现役（最新）版段 → (X.Y.Z|None, W##)；无版段返回 (None, None)。

    W711 方案 D 双形态：历史段 `### vX.Y.Z（日期）：W###`（ver=X.Y.Z）/ 新段 `### W###（日期）：标题`（ver=None·批次键唯一）。
    """
    m = re.search(r"^###\s+(?:v(\d+\.\d+\.\d+)|W(\d+))（[^）]*）", text, re.M)
    if not m:
        return (None, None)
    ver = m.group(1)
    wnum = m.group(2)
    if wnum is None:
        m2 = re.search(r"^###\s+(?:v\d+\.\d+\.\d+|W\d+)（[^）]*）：\s*W(\d+)", text, re.M)
        wnum = m2.group(1) if m2 else None
    return (ver, wnum)


def parse_footer_version(text, anchor=None):
    """解析版本标记 → (X.Y.Z|None, W##)。

    W711 双形态：历史「vX.Y.Z W###」/ 新条目「W###」（ver=None）。
    anchor=可选定位正则（先锚定区段再取首个版本标记——页脚/头部正文混有其他 W### 时必给，
    W708 review 教训：宽匹配会咬正文 W 号）。
    """
    if anchor:
        m0 = re.search(anchor, text)
        if not m0:
            return (None, None)
        text = text[m0.start():]
    m = re.search(r"(?:v(\d+\.\d+\.\d+)\s+)?W(\d+)", text)
    return (m.group(1), m.group(2)) if m else (None, None)


# ---------------------------------------------------------------------------
# 上报与执行态（W728 重构：原 main() 内闭包/局部态提取为类）
# ---------------------------------------------------------------------------

class _Reporter:
    """门禁三级上报器：FAIL/WARN/OK 打印与计数。

    退出码语义由 _print_summary 消费：核心 FAIL>0 → exit 1；仅辅助 WARN → exit 0
    （W393 降级六文档同步：辅助文档缺失/滞后不阻断提交）。
    """

    def __init__(self):
        self.fails = 0
        self.warns = 0

    def fail(self, msg):
        self.fails += 1
        print("FAIL  " + msg)

    def warn(self, msg):
        self.warns += 1
        print("WARN  " + msg)

    @staticmethod
    def ok(msg):
        print("OK    " + msg)


class _SkipResult:
    """scope 跳过时返回的伪造成功结果（W698）。

    stdout 带 _GATE_SUMMARY_MARKERS 汇总行标记——防静默跳过 wrapper 的
    「缺汇总行」校验被误触发（严格门禁段照常能过 marker 检查）。
    """

    def __init__(self, name, scope):
        marker = _GATE_SUMMARY_MARKERS.get(name, "")
        self.returncode = 0
        self.stdout = ((marker + "\n") if marker else "") + "（--scope %s 跳过）" % scope
        self.stderr = ""


class _GateContext:
    """门禁执行上下文：scope 分级态 + 段登记 + subprocess 统一短路 + 跨段共享量。

    时序契约（W698 原注释明示）：subprocess 补丁必须在本类构造末尾安装——
    scope=="auto" 的 _git_changed_files() 要走真实 subprocess.run；提前打补丁会使其
    吃到伪造结果（彼时 sections_ran 为空 → cur="" → 不在任何生效集 → 全部伪造跳过），
    auto 档将永远退化为 docs 子集。
    """

    def __init__(self, reporter):
        self.rep = reporter
        self.scope = _parse_scope(sys.argv)
        if self.scope == "auto":
            changed = _git_changed_files()
            self.scope = "full" if changed is None else _classify_scope(changed)
        if self.scope not in ("full", "docs", "site"):
            self.scope = "full"
        if self.scope == "full":
            self.active_sections = set(EXPECTED_SECTION_NAMES)
        else:
            self.active_sections = _SCOPE_CORE | (
                SCOPE_DOCS_SECTIONS if self.scope == "docs" else SCOPE_SITE_SECTIONS)
        print("---- verify_delivery --scope %s（生效段 %d/%d）----"
              % (self.scope, len(self.active_sections), len(EXPECTED_SECTION_NAMES)))
        self.sections_ran = []
        # 跨段共享量（原 main() 局部变量·段间数据流经此传递）
        self.ver = None       # 现役版本 X.Y.Z|None（期望版本段解析·六文档/页脚/旁文档段消费）
        self.wnum = None      # 现役 W###（同上）
        self.max_w_html = 0   # dukou-engine.html 全文最高 W###（范围漂移段消费）
        self.doc_all = ""     # 六文档全文拼接（范围漂移段消费）
        self._real_run = subprocess.run
        subprocess.run = self._scoped_run

    def section(self, name):
        """登记段名（段自洽锁 + scope 短路的「当前段」判定均消费此列表）。"""
        self.sections_ran.append(name)

    def _scoped_run(self, cmd, *args, **kwargs):
        """subprocess 层统一短路（W698）：当前段不在生效集 → 打印跳过 + 伪造成功结果。"""
        cur = self.sections_ran[-1] if self.sections_ran else ""
        if self.scope != "full" and cur not in self.active_sections:
            self.rep.ok("跳过 [%s]（--scope %s 未覆盖）" % (cur, self.scope))
            return _SkipResult(cur, self.scope)
        return self._real_run(cmd, *args, **kwargs)


# ---------------------------------------------------------------------------
# subprocess 委托门禁参数表（W728 重构：35 个同构段的差异收编于表·同构收编于 runner）
# ---------------------------------------------------------------------------

class _SimpleGate(NamedTuple):
    """简单委托门禁参数行（18 段·crash→WARN 不阻断）。

    消息口径与重构前逐段内联版逐字节一致：
      ok_msg——成功消息（%s=尾行首行·空则「无输出」）；
      fail_msg/warn_msg——失败/异常消息前缀（fail 由 runner 统一拼「（exit %d）：%s」后缀）；
      fail_suffix——fail 消息尾缀（仅 CSP漂移 有：改内联脚本后须重跑的提示）；
      tail_out/tail_err——尾行切片（stdout/stderr 各末 N 行）；
      fail_tail——fail 消息中尾行上限（12 段 [:6]·治理契约 [:4]·6 段全量因 tail≤4 条等价）；
      runner——py=sys.executable / node=node；
      missing_warn——FileNotFoundError 专用 WARN（仅 2 个 node 段：运行时缺失语义·W424 M2
      受控降级；W831 起未登记 missing_warn 的段遇运行器缺失按 fail-closed 记 FAIL）；
      severity——fail=非零退出即 FAIL / warn=非零退出仅 WARN（治理契约·W499 起不阻断；
      注意：severity 只管「退出码口径」，子进程崩溃/超时任何段都 FAIL·W831 B1 根修）。
    """
    section: str
    script: str
    args: tuple = ()
    timeout: int = 120
    ok_msg: str = ""
    fail_msg: str = ""
    warn_msg: str = ""
    tail_out: int = 2
    tail_err: int = 2
    fail_tail: int = 6
    runner: str = "py"
    missing_warn: str = ""
    fail_suffix: str = ""
    severity: str = "fail"


class _StrictGate(NamedTuple):
    """严格委托门禁参数行（15 段·crash 即拦 + 汇总行防静默跳过·W650 同款四段式）。

    与简单段差异：① 执行异常直接 FAIL（不静默放过）；② 退出码 0 还须校验 stdout 含
    marker 汇总行（防 wrapper 假绿）；③ ok 详情取 stdout 指定行（ok_line=-1 末行/
    -2 次末行·4 个双源门禁取次末行）；④ AGENTS分层 fail 尾行口径特殊（stdout4）。
    """
    section: str
    script: str
    args: tuple = ()
    timeout: int = 120
    marker: str = ""
    crash_msg: str = ""
    fail_msg: str = ""
    marker_msg: str = ""
    ok_msg: str = ""
    ok_line: int = -1
    fail_tail: str = "tail6"
    runner: str = "py"  # W751：py=sys.executable（默认·既有 15 段行为不变）/ node=node（第 43 槽 check_chart_values.js）


# a11y对比（第 20 段·bespoke）之前的 7 个简单委托段（执行序=EXPECTED_SECTION_NAMES 声明序）
_SIMPLE_GATES_PRE_A11Y = [
    _SimpleGate(section="双源漂移", script="check_data_drift.js", runner="node",
                missing_warn="node 不可用，跳过数据漂移检查（W424 M2）",
                ok_msg="数据漂移检查通过（%s）", fail_msg="数据漂移检查失败",
                warn_msg="数据漂移检查执行异常（W424 M2）: %s"),
    _SimpleGate(section="CSP漂移", script="generate_csp.py", args=("--check",), timeout=180,
                ok_msg="CSP 校验通过（%s）", fail_msg="CSP 漂移",
                fail_suffix="（改内联脚本后须重跑 python scripts/generate_csp.py）",
                warn_msg="CSP 校验执行异常（W424）: %s"),
    _SimpleGate(section="腐蚀插件", script="check_corruption.py",
                ok_msg="腐蚀/插件引用门禁通过（%s）", fail_msg="腐蚀/插件引用门禁失败",
                warn_msg="腐蚀/插件引用门禁执行异常（W424 复盘沉淀）: %s"),
    _SimpleGate(section="内联语法", script="check_js_syntax.js", runner="node",
                missing_warn="node 不可用，跳过内联脚本语法门禁（W457）",
                ok_msg="内联脚本语法门禁通过（%s）", fail_msg="内联脚本语法错误",
                warn_msg="内联脚本语法门禁执行异常（W457）: %s"),
    _SimpleGate(section="CSS平衡", script="check_structure.py",
                ok_msg="CSS 结构平衡通过（%s）", fail_msg="CSS 结构异常",
                warn_msg="CSS 结构平衡门禁执行异常（W457）: %s"),
    _SimpleGate(section="token覆盖", script="check_token_coverage.py", timeout=180,
                ok_msg="token 覆盖率门禁通过（%s）", fail_msg="token 覆盖率违规",
                warn_msg="token 覆盖率门禁执行异常（W493）: %s"),
    _SimpleGate(section="动效禁令", script="check_motion_ban.py",
                ok_msg="动效禁止清单门禁通过（%s）", fail_msg="动效禁止清单违规",
                warn_msg="动效禁止清单门禁执行异常（W493）: %s"),
]

# a11y对比 之后的 11 个简单委托段
_SIMPLE_GATES_POST_A11Y = [
    _SimpleGate(section="INLINED完整", script="check_inlined_css.py",
                ok_msg="INLINED CSS 门禁通过（%s）", fail_msg="INLINED CSS 块异常",
                warn_msg="INLINED CSS 门禁执行异常（W495）: %s"),
    _SimpleGate(section="动态链接", script="check_dynamic_links.py",
                ok_msg="动态链接门禁通过（%s）", fail_msg="动态链接死链",
                warn_msg="动态链接门禁执行异常（W459）: %s"),
    # 治理契约：W781 转正 FAIL 阻断（2026-08-18 WARN 起步策略两月监测期满·当前 0 告警零成本转正；
    # 尾行口径 4+2·fail 取前 4）
    _SimpleGate(section="治理契约", script="check_governance_docs.py", timeout=60,
                tail_out=4, fail_tail=4,
                ok_msg="治理文档维护契约通过（%s）", fail_msg="治理文档维护契约违规",
                warn_msg="治理文档维护契约门禁执行异常: %s"),
    _SimpleGate(section="索引健康", script="check_index_health.py",
                ok_msg="索引健康门禁通过（%s）", fail_msg="索引健康异常",
                warn_msg="索引健康门禁执行异常（W500）: %s"),
    _SimpleGate(section="元信息块", script="check_frontmatter.py",
                ok_msg="元信息块 v2 门禁通过（%s）", fail_msg="元信息块 v2 缺字段/枚举非法",
                warn_msg="元信息块 v2 门禁执行异常（W501）: %s"),
    _SimpleGate(section="术语一致", script="check_glossary.py",
                ok_msg="术语一致性门禁通过（%s）", fail_msg="术语一致性异常",
                warn_msg="术语一致性门禁执行异常（W502）: %s"),
    _SimpleGate(section="引文核验", script="check_citations.py", args=("--dir", "docs"),
                ok_msg="原著引文核验通过（%s）", fail_msg="原著引文未命中/格式错误",
                warn_msg="原著引文核验门禁执行异常（W503）: %s"),
    # 图表自洽（W551：W550 全站截图审查实证三类批量图表缺陷——10 页桑基缺引用/4 组饼图措辞×树图
    # 实现错配——均为门禁盲区积累数月后人工清账，本门禁文本层拦同类复发；需真实渲染的遮挡/空带/
    # 溢出/桑基运行时由 check_screenshot_gates.js（screenshot-review workflow 动态步）覆盖）
    _SimpleGate(section="图表自洽", script="check_chart_data.py",
                ok_msg="图表静态自洽门禁通过（%s）", fail_msg="图表静态自洽异常",
                warn_msg="图表静态自洽门禁执行异常（W551）: %s"),
    _SimpleGate(section="数据一致", script="check_content_consistency.py", args=("--gate",),
                timeout=180, tail_out=1,
                ok_msg="数据内容一致性门禁通过（%s）", fail_msg="数据内容一致性异常",
                warn_msg="数据内容一致性门禁执行异常（W555）: %s"),
    _SimpleGate(section="W区间字面量", script="check_w_range_literal.py", timeout=60,
                ok_msg="W 号区间字面量门禁通过（%s）", fail_msg="W 号区间字面量漂移",
                warn_msg="W 号区间字面量门禁执行异常（W628）: %s"),
    _SimpleGate(section="SEOhead", script="check_seo_head.py", tail_out=1,
                ok_msg="SEO head 门禁通过（%s）", fail_msg="SEO head 异常",
                warn_msg="SEO head 门禁执行异常（W630）: %s"),
]

# 16 个严格委托段（第 28-47 门禁·「第 NN 门禁」字面量即第 41 门禁 C2 对账源·禁改写）
_STRICT_GATES = [
    _StrictGate(section="可引用性", script="check_citability.py", args=("--gate",),
                marker="---- 第 28 门禁：",
                crash_msg="可视化可引用性门禁执行异常（第 28 门禁·crash 即拦不静默放过·W650 对齐 W631 防静默跳过）: %s",
                fail_msg="可引用性基线外违规",
                marker_msg="可引用性门禁输出缺汇总行（疑似未真正扫描·防静默跳过 W650）：%r",
                ok_msg="可视化可引用性门禁通过（%s）"),
    _StrictGate(section="设计令牌对账", script="check_design_doc_drift.py",
                marker="---- 设计令牌对账：",
                crash_msg="设计令牌对账门禁执行异常（PD-5·crash 即拦）: %s",
                fail_msg="设计令牌对账漂移",
                marker_msg="设计令牌对账输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="设计令牌文档对账通过（%s）"),
    _StrictGate(section="色盲安全", script="check_chart_colorblind.py", args=("--gate",),
                marker="---- 第 29 门禁 色盲安全：",
                crash_msg="色盲安全门禁执行异常（第 29 槽·crash 即拦）: %s",
                fail_msg="色盲安全基线外违规",
                marker_msg="色盲安全门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="色盲安全门禁通过（%s）"),
    _StrictGate(section="降级声明", script="check_chart_degrade.py",
                marker="---- 第 30 门禁 降级声明：",
                crash_msg="降级声明门禁执行异常（第 30 槽·crash 即拦）: %s",
                fail_msg="降级声明缺失/非法",
                marker_msg="降级声明门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="降级声明门禁通过（%s）"),
    _StrictGate(section="文档口径", script="check_doc_sync.py",
                marker="---- 第 31 门禁 文档口径体检：",
                crash_msg="文档口径体检执行异常（第 31 槽·crash 即拦）: %s",
                fail_msg="文档口径体检失配",
                marker_msg="文档口径体检输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="文档口径体检通过（%s）"),
    _StrictGate(section="CLAUDE速查", script="check_claude_md.py", timeout=60,
                marker="---- 第 32 门禁 CLAUDE.md 速查层：",
                crash_msg="CLAUDE.md 速查层门禁执行异常（第 32 槽·crash 即拦）: %s",
                fail_msg="CLAUDE.md 速查层失配",
                marker_msg="CLAUDE.md 速查层门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="CLAUDE.md 速查层门禁通过（%s）"),
    _StrictGate(section="head内容", script="check_html_head_content.py",
                marker="---- 第 33 门禁 head 内容：",
                crash_msg="head 内容门禁执行异常（第 33 槽·crash 即拦）: %s",
                fail_msg="head 内容违例",
                marker_msg="head 内容门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="head 内容门禁通过（%s）"),
    _StrictGate(section="CSS变量引用", script="check_css_var_refs.py",
                marker="---- 第 34 门禁 CSS 变量引用：",
                crash_msg="CSS 变量引用门禁执行异常（第 34 槽·crash 即拦）: %s",
                fail_msg="CSS 变量引用违例",
                marker_msg="CSS 变量引用门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="CSS 变量引用门禁通过（%s）"),
    _StrictGate(section="声明分隔", script="check_css_decl_separators.py",
                marker="---- 第 35 门禁 声明分隔：",
                crash_msg="声明分隔门禁执行异常（第 35 槽·crash 即拦）: %s",
                fail_msg="声明分隔违例",
                marker_msg="声明分隔门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="声明分隔门禁通过（%s）"),
    _StrictGate(section="孤立选择", script="check_css_orphan_selectors.py",
                marker="---- 第 36 门禁 孤立选择器：",
                crash_msg="孤立选择器门禁执行异常（第 36 槽·crash 即拦）: %s",
                fail_msg="孤立选择器违例",
                marker_msg="孤立选择器门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="孤立选择器门禁通过（%s）"),
    _StrictGate(section="kpi基类", script="check_kpi_card_base.py",
                marker="---- 第 37 门禁 kpi 基类：",
                crash_msg="kpi 基类门禁执行异常（第 37 槽·crash 即拦）: %s",
                fail_msg="kpi 基类违例",
                marker_msg="kpi 基类门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="kpi 基类门禁通过（%s）"),
    _StrictGate(section="内嵌残留", script="check_embedded_stale_markers.py", timeout=180,
                marker="---- 第 38 门禁 页面内嵌残留标记：",
                crash_msg="内嵌残留门禁执行异常（第 38 槽·crash 即拦）: %s",
                fail_msg="内嵌残留标记命中",
                marker_msg="内嵌残留门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="内嵌残留门禁通过（%s）", ok_line=-2),
    _StrictGate(section="时间线双源", script="check_story_timeline_sync.py",
                marker="---- 第 39 门禁 故事内时间线双源同步：",
                crash_msg="时间线双源门禁执行异常（第 39 槽·crash 即拦）: %s",
                fail_msg="时间线双源失配",
                marker_msg="时间线双源门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="时间线双源门禁通过（%s）", ok_line=-2),
    _StrictGate(section="chapter双源", script="check_chapter_stats_sync.py", timeout=300,
                marker="---- 第 40 门禁 chapter_stats 双源同步：",
                crash_msg="chapter双源门禁执行异常（第 40 槽·crash 即拦）: %s",
                fail_msg="chapter双源漂移",
                marker_msg="chapter双源门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="chapter双源门禁通过（%s）", ok_line=-2),
    _StrictGate(section="AGENTS分层", script="check_agents_layers.py",
                marker="---- 第 41 门禁 AGENTS 分层完整性：",
                crash_msg="AGENTS 分层门禁执行异常（第 41 槽·crash 即拦）: %s",
                fail_msg="AGENTS 分层失配",
                marker_msg="AGENTS 分层门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="AGENTS 分层完整性通过（%s）", ok_line=-2, fail_tail="stdout4"),
    _StrictGate(section="脚本覆盖", script="check_script_coverage.py",
                marker="---- 第 42 门禁 根级脚本覆盖：",
                crash_msg="脚本覆盖门禁执行异常（第 42 槽·crash 即拦）: %s",
                fail_msg="根级脚本覆盖缺口",
                marker_msg="脚本覆盖门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="根级脚本覆盖通过（%s）", ok_line=-2),
    _StrictGate(section="可视化数据", script="check_chart_values.js", args=("--gate",), runner="node", timeout=300,
                marker="---- 第 43 门禁 可视化数据断言：",
                crash_msg="可视化数据断言门禁执行异常（第 43 槽·crash 即拦）: %s",
                fail_msg="可视化数据断言缺口",
                marker_msg="可视化数据断言门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="可视化数据断言通过（%s）", ok_line=-2),
    _StrictGate(section="英文站", script="validate_en.py", args=("--all",), timeout=180,
                marker="EN validate:",
                crash_msg="英文站校验执行异常（第 44 槽·crash 即拦）: %s",
                fail_msg="英文站 CJK 违规（script CJK=0 / chrome 白名单）",
                marker_msg="英文站校验输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="英文站校验通过（%s）", ok_line=-1),
    _StrictGate(section="目录文档", script="check_folder_docs.py", args=("--gate",), timeout=240,
                marker="---- 第 45 门禁 目录文档新鲜度：",
                crash_msg="目录文档新鲜度门禁执行异常（第 45 槽·crash 即拦）: %s",
                fail_msg="目录文档新鲜度违规（生成清单与磁盘漂移·重跑 python scripts/gen_folder_docs.py --refresh 刷新·人工维护件自动跳过）",
                marker_msg="目录文档门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="目录文档新鲜度通过（%s）", ok_line=-1),
    _StrictGate(section="搜索索引", script="check_search_index_fresh.py", args=("--gate",), timeout=300,
                marker="---- 第 46 门禁 搜索索引新鲜度：",
                crash_msg="搜索索引新鲜度门禁执行异常（第 46 槽·crash 即拦）: %s",
                fail_msg="站内搜索索引陈旧（页面内嵌索引 ≠ 生成器实算·重跑 python scripts/_gen_search_index.py 刷新并重算 CSP 哈希）",
                marker_msg="搜索索引门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="搜索索引新鲜度通过（%s）", ok_line=-1),
    _StrictGate(section="性能影子", script="check_perf_shadow.py", args=("--gate",), timeout=120,
                marker="---- 第 47 门禁 性能影子：",
                crash_msg="性能影子槽执行异常（第 47 槽·crash 即拦）: %s",
                fail_msg="性能影子槽采集面缺失（perf.yml collect.url 的页面不在了·先修断链再看数字）",
                marker_msg="性能影子槽输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="性能影子槽通过（%s）", ok_line=-1),
    _StrictGate(section="计划方案合规", script="check_plan_template.py", args=("--gate",), timeout=120,
                marker="---- 第 48 门禁 计划方案合规：",
                crash_msg="计划方案合规槽执行异常（第 48 槽·crash 即拦）: %s",
                fail_msg="计划方案模板符合性不达标（新增/修改的计划方案文件引入了缺失判据·补齐后重跑）",
                marker_msg="计划方案合规槽输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="计划方案合规槽通过（%s）", ok_line=-1),
    _StrictGate(section="朱砂实底", script="check_vermilion_solid.js", runner="node",
                args=("--gate",), timeout=600,
                marker="---- 第 49 门禁 朱砂实底：",
                crash_msg="朱砂实底槽执行异常（第 49 槽·crash 即拦）: %s",
                fail_msg="朱砂实底限额违规（有页面非豁免实底 >3 处·收敛或补登记豁免后重跑）",
                marker_msg="朱砂实底槽输出缺汇总行（疑似未真正执行·防静默跳过）：%r",
                ok_msg="朱砂实底限额门禁通过（%s）", ok_line=-1),
]

# ---- 注册表派生与一致性防线（W781 R-1·挂槽「五处同改」收敛）----
# 派生：section→marker 映射自 _STRICT_GATES 元组（W780 实证对拍逐项相等）——新挂槽只改
# 门禁元组与 EXPECTED_SECTION_NAMES 两处，漏改由 _assert_registry_consistent() 启动期
# fail-fast（防静默跳过/CI 红延迟暴露·K11 接线缺失型同族）。
_GATE_SUMMARY_MARKERS = {g.section: g.marker for g in _STRICT_GATES if getattr(g, "marker", "")}

# 仅 full 档生效的门禁段（刻意登记·不在任何 scope 子集）：仓库全域面，docs/site 变更子集
# 不触碰其判据分母——漏登记此集合的段会在 R-1 断言红（W713 内联段盲区同族的显式化）。
_FULL_ONLY_SECTIONS = {"脚本覆盖", "目录文档"}


def _assert_registry_consistent() -> None:
    """启动期注册表一致性断言（W781 R-1）：挂槽漏改任一手工面当场红，不等到 CI。

    四查：① 门禁段名互不重复；② 元组段名 ⊆ EXPECTED_SECTION_NAMES（W780 实证漏
    「目录文档」于顺序表·旧自洽锁单向查缺抓不到多段）；③ 元组相对序 == EXPECTED 相对序
    （执行序漂移即红）；④ 不在任何 scope 子集的段必须登记 _FULL_ONLY_SECTIONS。
    """
    gate_sections = [g.section for _l in (_SIMPLE_GATES_PRE_A11Y, _SIMPLE_GATES_POST_A11Y,
                                          _STRICT_GATES) for g in _l]
    dupes = sorted({s for s in gate_sections if gate_sections.count(s) > 1})
    assert not dupes, "门禁段名重复（挂槽漏改·R-1）： %r" % dupes
    expected_set = set(EXPECTED_SECTION_NAMES)
    missing = [s for s in gate_sections if s not in expected_set]
    assert not missing, ("门禁元组段名未入 EXPECTED_SECTION_NAMES（挂槽漏改·R-1·W780 第 45 槽同型）： %r"
                         % missing)
    order_in_expected = [n for n in EXPECTED_SECTION_NAMES if n in set(gate_sections)]
    assert order_in_expected == gate_sections, (
        "门禁执行序与 EXPECTED_SECTION_NAMES 相对序不一致（R-1）： %r vs %r"
        % (gate_sections, order_in_expected))
    unscoped = set(gate_sections) - _SCOPE_CORE - SCOPE_DOCS_SECTIONS - SCOPE_SITE_SECTIONS
    unregistered = sorted(unscoped - _FULL_ONLY_SECTIONS)
    assert not unregistered, ("门禁段不在任何 scope 子集且未登记 _FULL_ONLY_SECTIONS（R-1）： %r"
                              % unregistered)


def _run_simple_gate(ctx, gate):
    """简单委托门禁通用体（W728 重构）：替代原 18 个同构 try/run/tail 段。

    输出口径与逐段内联版逐字节一致；scope 跳过时经 ctx._scoped_run 拿伪造结果走 ok 路径。
    W831 B1 根修（用户批准·T03 D-01 遗留·CLAUDE.md 第 10 条）：异常路径由 WARN 改 FAIL——
    子进程崩溃/超时 = 判据不可执行，记 WARN 会使 18/33 委托段崩溃即降级、整轮仍「核心全部
    通过 ✅」+ exit 0（假绿面根除·对齐 _run_strict_gate 语义）；唯一保留的 WARN 是
    Gate.missing_warn 登记的运行期缺失降级（W424 M2·仅 2 个 node 段·显式 opt-in）。
    """
    ctx.section(gate.section)
    exe = "node" if gate.runner == "node" else sys.executable
    cmd = [exe, os.path.join(_HERE, gate.script)] + list(gate.args)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=gate.timeout)
    except FileNotFoundError as e:
        if gate.missing_warn:
            ctx.rep.warn(gate.missing_warn)  # W424 M2 登记式降级（node 运行期缺失·受控）
        else:
            ctx.rep.fail(gate.warn_msg % e)  # 未登记降级 → fail-closed（判据不可执行即红）
        return
    except Exception as e:
        ctx.rep.fail(gate.warn_msg % e)  # W831：crash/timeout → FAIL（原 WARN·假绿面根除）
        return
    tail = r.stdout.splitlines()[-gate.tail_out:] + r.stderr.splitlines()[-gate.tail_err:]
    first = tail[0] if tail else "无输出"
    if r.returncode == 0:
        ctx.rep.ok(gate.ok_msg % first)
    elif gate.severity == "warn":
        ctx.rep.warn("%s（exit %d）：%s%s" % (gate.fail_msg, r.returncode,
                                            " / ".join(tail[:gate.fail_tail]), gate.fail_suffix))
    else:
        ctx.rep.fail("%s（exit %d）：%s%s" % (gate.fail_msg, r.returncode,
                                            " / ".join(tail[:gate.fail_tail]), gate.fail_suffix))


def _run_strict_gate(ctx, gate):
    """严格委托门禁通用体（W728 重构）：crash 即拦 + 汇总行防静默跳过（W650 四段式）。

    与原 15 个逐段内联版输出逐字节一致；AGENTS分层 的 fail 尾行口径（stdout 末 4 行）
    经 fail_tail="stdout4" 参数化，其余段为标准 tail（stdout 末 1 行 + stderr 末 2 行）。
    """
    ctx.section(gate.section)
    exe = "node" if gate.runner == "node" else sys.executable
    try:
        r = subprocess.run([exe, os.path.join(_HERE, gate.script)] + list(gate.args),
                           capture_output=True, text=True, timeout=gate.timeout)
    except Exception as e:
        ctx.rep.fail(gate.crash_msg % e)
        return
    if r.returncode != 0:
        if gate.fail_tail == "stdout4":
            detail = " / ".join(r.stdout.splitlines()[-4:])
        else:
            tail = r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:]
            detail = " / ".join(tail[:6])
        ctx.rep.fail("%s（exit %d）：%s" % (gate.fail_msg, r.returncode, detail))
    elif gate.marker not in r.stdout:
        ctx.rep.fail(gate.marker_msg % r.stdout[-160:])
    else:
        lines = r.stdout.splitlines()
        if gate.ok_line == -1:
            detail = lines[-1] if lines else "无输出"
        else:
            detail = lines[-2] if len(lines) >= 2 else "无输出"
        ctx.rep.ok(gate.ok_msg % detail)


# ---------------------------------------------------------------------------
# 内联逻辑段函数（11 个非委托段 + 2 个 bespoke 委托段·W728 重构从 main() 提取）
# ---------------------------------------------------------------------------

def _gate_expected_version(ctx):
    """期望版本：动态取自 CHANGELOG 现役版段（W518；页脚为滞后型手工工件，降级为新鲜度检查）。"""
    ctx.section("期望版本")
    ctx.ver, ctx.wnum = latest_version_from_changelog(_read(os.path.join(ROOT, "CHANGELOG.md")))
    if ctx.wnum is None:
        ctx.rep.fail("CHANGELOG.md 未解析出现役版段（期望 ### W###（日期）：标题 或历史 ### vX.Y.Z（日期）：W###）")
    else:
        ctx.rep.ok("期望批次动态取自 CHANGELOG 现役段 %sW%s"
                   % (("v%s " % ctx.ver) if ctx.ver else "", ctx.wnum))


def _gate_dukou_footer(ctx):
    """dukou 页脚：新鲜度（落后现役仅 WARN）+ 全文 W### 扫描（max_w_html 供范围漂移段）。"""
    ctx.section("dukou页脚")
    html = _read(HTML)
    if not html:
        ctx.rep.fail("找不到 %s（未生成或被忽略）" % HTML)
    html_w = [int(x) for x in re.findall(r"W(\d{3})", html)]
    ctx.max_w_html = max(html_w) if html_w else 0

    # W711：footer 标签内联正则（页面正文含治理文档版本链引用·宽锚会误命中——锚定 <footer> 标签内首链目）
    m_f = re.search(r"<footer>.{0,200}?(?:v([\d.]+)\s+)?W(\d{3})", html, re.S)
    fver, fwnum = (m_f.group(1), m_f.group(2)) if m_f else (None, None)
    if fwnum:  # W711：fver 可 None（W-only 新条目）·批次键比对
        if ctx.wnum and int(fwnum) < int(ctx.wnum):
            ctx.rep.warn("dukou-engine.html 页脚版本 %sW%s 落后于现役 W%s"
                         "（页脚为手工工件，建议随批升版，不阻断）"
                         % (("v%s " % fver) if fver else "", fwnum, ctx.wnum))
        else:
            ctx.rep.ok("dukou-engine.html footer 版本 %sW%s"
                       % (("v%s " % fver) if fver else "", fwnum))
    else:
        ctx.rep.fail("dukou-engine.html footer 未解析出 vX.Y.Z W###")


def _gate_six_docs(ctx):
    """降级六文档同步校验（W393）：核心 2 份缺失 v/W 阻断，辅助 4 份仅 WARN。

    顺带累积 doc_all（六文档全文拼接）供范围漂移段消费。
    """
    ctx.section("六文档同步")
    for d in DOCS:
        p = os.path.join(ROOT, d)
        c = _read(p)
        ctx.doc_all += c
        core = d in CORE_DOCS
        if not c:
            if core:
                ctx.rep.fail("缺失核心文档: %s" % d)
            else:
                ctx.rep.warn("缺失辅助文档（不阻断，可跑 scripts/bump_version.py）: %s" % d)
            continue
        if ctx.ver and ("v" + ctx.ver) not in c:
            if core:
                ctx.rep.fail("%s 不含版本 v%s（旧疾风险·核心阻断）" % (d, ctx.ver))
            else:
                ctx.rep.warn("%s 不含版本 v%s（辅助文档，跑 scripts/bump_version.py 同步，不阻断）" % (d, ctx.ver))
            continue
        if ctx.wnum and ("W" + ctx.wnum) not in c:
            if core:
                ctx.rep.fail("%s 不含 W%s 里程碑 token（旧疾风险·核心阻断）" % (d, ctx.wnum))
            else:
                ctx.rep.warn("%s 不含 W%s 里程碑 token（辅助文档，跑 scripts/bump_version.py 同步，不阻断）" % (d, ctx.wnum))
            continue
        ctx.rep.ok("%s 含 %sW%s" % (d, ("v%s / " % ctx.ver) if ctx.ver else "", ctx.wnum))


def _gate_side_docs(ctx):
    """旁文档同步门禁（W526：workflows/README.md 头部版本行 + 里程碑行上限 == 现役 v/W）。"""
    ctx.section("旁文档同步")
    wf = _read(os.path.join(ROOT, ".github", "workflows", "README.md"))
    if not wf:
        ctx.rep.fail(".github/workflows/README.md 缺失（旁文档，需人工补回）")
    else:
        wf_v, wf_w = parse_footer_version(wf, anchor=r"，(?:v[\d.]+\s+)?W\d+）的 GitHub")
        if wf_w:
            if ctx.wnum and int(wf_w) != int(ctx.wnum):
                ctx.rep.fail(".github/workflows/README.md 头部版本 W%s != 现役 W%s"
                             "（旁文档滞后，W499/W525 两次实证复发）" % (wf_w, ctx.wnum))
            else:
                ctx.rep.ok(".github/workflows/README.md 头部版本同步（%sW%s）"
                           % (("v%s " % wf_v) if wf_v else "", wf_w))
        else:
            ctx.rep.fail(".github/workflows/README.md 未解析出头部版本标记（W### 或历史 vX.Y.Z W###）")
        mw = re.search(r"W450-W(\d{3})", wf)
        if mw:
            if ctx.wnum and mw.group(1) != ctx.wnum:
                ctx.rep.fail(".github/workflows/README.md 里程碑行上限 W%s != 现役 W%s（里程碑滞后）"
                             % (mw.group(1), ctx.wnum))
            else:
                ctx.rep.ok(".github/workflows/README.md 里程碑行上限 W%s == 现役 W%s"
                           % (mw.group(1), ctx.wnum))
        else:
            ctx.rep.fail(".github/workflows/README.md 未找到 W450-W### 里程碑行")


def _gate_scope_drift(ctx):
    """范围漂移检测：html 引用 W### 不得超出六文档+归档已记录范围（W417 归档纳入扫描）。"""
    ctx.section("范围漂移")
    doc_w = [int(x) for x in re.findall(r"W(\d{3})", ctx.doc_all)]
    for a in ARCHIVE_DOCS:
        doc_w += [int(x) for x in re.findall(r"W(\d{3})", _read(os.path.join(ROOT, a)))]
    max_w_doc = max(doc_w) if doc_w else 0
    if ctx.max_w_html > max_w_doc:
        ctx.rep.fail("范围漂移：%s 引用到 W%d，但六文档+归档最高仅记到 W%d（疑似未记录的改动，需补记或回退）"
                     % (os.path.basename(HTML), ctx.max_w_html, max_w_doc))
    else:
        ctx.rep.ok("无范围漂移（html 最高 W%d ≤ 文档+归档最高 W%d）" % (ctx.max_w_html, max_w_doc))


def _gate_a4_count(ctx):
    """A4 计数一致性（W722 双形态：裸字面量「209 篇」或实体标记「209<!--stats:a4_docs--> 篇」）。"""
    ctx.section("A4计数")
    _a4_re = re.compile(r"209(?:<!--stats:a4_docs-->)?\s*篇")
    miss = []
    for d in A4_DOCS:
        c = _read(os.path.join(ROOT, d))
        if not _a4_re.search(c):
            miss.append(d)
    if miss:
        ctx.rep.fail("A4 计数不一致（缺 '209 篇/209<!--stats:a4_docs--> 篇'）：%s" % ", ".join(miss))
    else:
        ctx.rep.ok("A4 计数一致（四份文档均含 '209 篇' 或实体标记形态）")


def _gate_a1_a6_count(ctx):
    """A1-A6 真实文件计数 vs README 声明（W417 新增，防计数声明失真；口径见 doc_areas）。"""
    ctx.section("A1-A6计数")
    readme_txt = _read(os.path.join(ROOT, "README.md"))
    m_cnt = re.search(r"共\s*(\d+)\s*篇", readme_txt)
    actual_total = 0
    for name, d in A_AREAS:
        n = count_content_md(d)
        if n < 0:
            ctx.rep.warn("%s 目录缺失: %s" % (name, d))
            continue
        actual_total += n
    if m_cnt:
        declared = int(m_cnt.group(1))
        if actual_total == declared:
            ctx.rep.ok("A1-A6 真实文件计数 %d 篇 == README 声明 %d 篇（排除各板块 README.md）"
                       % (actual_total, declared))
        else:
            ctx.rep.fail("A1-A6 真实文件计数 %d 篇 != README 声明 %d 篇（计数漂移，需同步 README 声明）"
                         % (actual_total, declared))
    else:
        ctx.rep.warn("README 未找到 '共 N 篇' 声明，跳过 A1-A6 计数校验")


def _gate_academic_citations(ctx):
    """学术研究轨显式引用门禁（W452 新增：可核查引用硬性化）。"""
    ctx.section("学术引用")
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
        ctx.rep.warn("未发现 学术研究 轨文档，跳过显式引用门禁")
    elif acad_missing:
        ctx.rep.fail("学术研究 轨文档 %d 篇缺显式引用（缺 '> 引用：' 学术论文索引 链接）：%s"
                     % (len(acad_missing), ", ".join(acad_missing[:5])))
    else:
        ctx.rep.ok("学术研究 轨文档 %d 篇均含显式引用（> 引用：学术论文索引 链接）" % acad_total)


def _gate_a1_navigation(ctx):
    """A1 导航相邻性断言（W422：每回导航行须指向相邻回·第1回无上/第100回无下）。"""
    ctx.section("A1导航")
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
                    nav_fail.append("第%d回 上一回 -> %s（期望第%d回）"
                                    % (num, pm.group(1) if pm else "无", num - 1))
            elif pm:
                nav_fail.append("第1回 不应有上一回链接")
            if num < 100:
                if not xm or int(xm.group(1)) != num + 1:
                    nav_fail.append("第%d回 下一回 -> %s（期望第%d回）"
                                    % (num, xm.group(1) if xm else "无", num + 1))
            elif xm:
                nav_fail.append("第100回 不应有下一回链接")
    if nav_fail:
        ctx.rep.fail("A1 导航相邻性异常 %d 处（示例：%s）" % (len(nav_fail), nav_fail[0]))
    else:
        ctx.rep.ok("A1 导航相邻性 100/100（上一回=N-1·下一回=N+1·第1回无上/第100回全书完）")


def _gate_docs_links(ctx):
    """docs 全量链接校验（W422 建置 docs/01·W699 扩为 docs 全量：挂载即绿 5191 链接 0 broken；
    lint_links 内建三豁免=archive 冻结档/gitignore 本地件/fenced+inline code 去噪）。"""
    ctx.section("docs链接")
    try:
        r = subprocess.run(
            [sys.executable, os.path.join(_HERE, "lint_links.py"),
             "--dir", os.path.join(ROOT, "docs")],
            capture_output=True, text=True, timeout=300)
        if r.returncode == 0:
            ctx.rep.ok("docs 全量链接校验通过（lint_links 0 broken）")
        else:
            # W700 热修：tail 只捞 BROKEN/汇总行——原 stdout[-3:] 会混入 OK 行（CI 首跑实证）
            tail = ([x for x in r.stdout.splitlines()
                     if "[BROKEN]" in x or "校验完成" in x][-3:]
                    + r.stderr.splitlines()[-3:])
            ctx.rep.fail("docs 存在 broken 链接（lint_links exit %d）：%s"
                         % (r.returncode, " / ".join(tail)))
    except Exception as e:
        ctx.rep.fail("docs 链接校验执行异常: %s" % e)


def _gate_sitemap(ctx):
    """sitemap 覆盖校验（W422：防新增页面漏收录，W417 曾手工补 69→154；统计/预览页按白名单排除）。"""
    ctx.section("sitemap覆盖")
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
            ctx.rep.fail("sitemap 与 site 不一致：缺 %d 页（%s）、多余 %d 页（%s）"
                         % (len(miss), miss[:3], len(extra), extra[:3]))
        else:
            ctx.rep.ok("sitemap 覆盖一致（%d 页，排除统计/预览页 %d 个）" % (len(locs), len(EXCLUDED_SM)))
    else:
        ctx.rep.warn("sitemap.xml 或 site/ 缺失，跳过 sitemap 覆盖校验")


def _gate_embedded_fallback(ctx):
    """site/data 内嵌回退模式静态检查（W422：file:// 铁律的自动验证）。"""
    ctx.section("内嵌回退")
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
        ctx.rep.fail("site/data 有 %d/%d 页缺内嵌回退模式（file:// 直开风险）：%s"
                     % (len(no_emb), data_count, ", ".join(no_emb[:5])))
    else:
        ctx.rep.ok("site/data %d 页均含内嵌回退模式（EMBEDDED_DATA/EMBEDDED/FALLBACK/inline data）"
                   % data_count)


def _gate_a11y(ctx):
    """a11y 对比度门禁（W493 E6 转正：M1 WCAG AA，P0/P1 阻断；bespoke=JSON 汇总解析）。

    W831 B2 根修（用户批准·T03 D-01 遗留）：原实现三处 fail-open——① JSON 解析异常 →
    rep.ok「summary 解析跳过」；② 缺 summary/E2-2 键 → p01=0 静默判绿（_count_by_rule 虽
    预置全规则 0 值，但任何输出形态漂移都走这条静默绿路）；③ 外层异常 → rep.warn。三者
    都使「判据不可执行」伪装成「通过」。现改 fail-closed：解析失败/结构不符/子进程异常
    一律 FAIL（对齐 _run_strict_gate 与 _run_simple_gate W831 语义）。
    """
    ctx.section("a11y对比")
    a11y_py = os.path.join(_HERE, "a11y_audit.py")
    try:
        r = subprocess.run(
            [sys.executable, a11y_py, "--dir", "site", "--format", "json", "--quiet"],
            capture_output=True, text=True, timeout=300)
    except Exception as e:
        ctx.rep.fail("a11y 对比度门禁执行异常（判据不可执行·fail-closed·W831）: %s" % e)
        return
    if isinstance(r, _SkipResult):
        # W839 回归修复：scope 跳过时 _scoped_run 返回伪造结果（stdout 为「（--scope X 跳过）」，
        # 跳过提示已由其打印）；W834 改 fail-closed 后误把该提示串送 json.loads → docs 档提交必红。
        # 跳过不是「判据不可执行」，直接返回，不重复上报。
        return
    if r.returncode != 0:
        ctx.rep.fail("a11y_audit 失败（exit %d）：%s"
                     % (r.returncode, (r.stderr or r.stdout).splitlines()[-1:]))
        return
    try:
        rep = json.loads(r.stdout)
    except Exception as e:
        ctx.rep.fail("a11y 审计输出不可解析（判据不可执行·fail-closed·W831）: %s" % str(e)[:120])
        return
    s = rep.get("summary") if isinstance(rep, dict) else None
    e22 = s.get("E2-2") if isinstance(s, dict) else None
    if not isinstance(e22, dict):
        ctx.rep.fail("a11y 汇总缺 summary.E2-2 结构（判据不可执行·fail-closed·W831）")
        return
    p01 = (e22.get("P0", 0) or 0) + (e22.get("P1", 0) or 0)
    if p01 == 0:
        ctx.rep.ok("a11y 对比度门禁通过（E2-2 P0/P1=0）")
    else:
        ctx.rep.fail("a11y 对比度 P0+P1=%d（M1 WCAG AA 阻断）" % p01)


# ---------------------------------------------------------------------------
# 收尾（health 探活 / 段自洽锁 / 汇总退出码）
# ---------------------------------------------------------------------------

def _probe_health(rep):
    """可选 RAG /health 探活（仅告警，不阻断；WARN 直印不计入 warns 计数）。"""
    if "--health" in sys.argv:
        try:
            r = urllib.request.urlopen("http://127.0.0.1:8777/health", timeout=5)
            body = json.loads(r.read().decode("utf-8"))
            rep.ok("/health 存活：%s" % body)
        except Exception as e:
            print("WARN  /health 不可达（环境项，不阻断提交）：%s" % e)


def _check_section_lock(ctx):
    """门禁段自洽锁（VERIFY_SECTIONS·W663/T3）：声明段集合 == 实跑段集合，缺段即红。

    W698 scope 分级：非 full 档按生效子集断言，full 档仍断言全量 46 段。
    """
    expected_sections = list(EXPECTED_SECTION_NAMES) if ctx.scope == "full" else \
        [n for n in EXPECTED_SECTION_NAMES if n in ctx.active_sections]
    ran_set = set(ctx.sections_ran)
    missing_sections = [n for n in expected_sections if n not in ran_set]
    # W781 R-1：补反向查（实跑多出声明外段=挂槽漏 EXPECTED·旧单向查放过了第 45 槽实证）
    extra_sections = [n for n in dict.fromkeys(ctx.sections_ran) if n not in set(EXPECTED_SECTION_NAMES)]
    if missing_sections or extra_sections:
        ctx.rep.fail("门禁段实跑 %d ≠ 声明 %d：缺 %s 多 %s（VERIFY_SECTIONS 自洽锁·--scope %s）"
                     % (len(ran_set), len(expected_sections),
                        "、".join(missing_sections) or "无", "、".join(extra_sections) or "无",
                        ctx.scope))
    else:
        ctx.rep.ok("门禁段自洽锁：实跑 %d 段 == 声明 %d 段（--scope %s）"
                   % (len(ran_set), len(expected_sections), ctx.scope))


def _print_summary(rep):
    """汇总与退出码：核心 FAIL>0 → 1；仅辅助 WARN → 0。"""
    print("\n==== 交付校验汇总 ====")
    if rep.fails == 0:
        print("核心全部通过 ✅" + ("（%d 项辅助 WARN，不阻断）" % rep.warns if rep.warns else ""))
        return 0
    print("%d 项核心 FAIL ❌（%d 项辅助 WARN）" % (rep.fails, rep.warns))
    return 1


def main():
    _assert_registry_consistent()  # W781 R-1：注册表一致性启动期防线
    """交付门禁编排（W728 重构：905 行单体 → 表驱动编排）。

    执行序 = 52 个段名在 EXPECTED_SECTION_NAMES 中的声明序（段自洽锁对账·不得重排）；
    新增/调整门禁段只改对应参数表项或段函数，main() 编排面保持稳定。
    """
    rep = _Reporter()
    ctx = _GateContext(rep)
    # —— 内联逻辑段（11）——
    _gate_expected_version(ctx)
    _gate_dukou_footer(ctx)
    _gate_six_docs(ctx)
    _gate_side_docs(ctx)
    _gate_scope_drift(ctx)
    _gate_a4_count(ctx)
    _gate_a1_a6_count(ctx)
    _gate_academic_citations(ctx)
    _gate_a1_navigation(ctx)
    _gate_docs_links(ctx)
    _gate_sitemap(ctx)
    _gate_embedded_fallback(ctx)
    # —— subprocess 委托段（33：a11y对比 夹在简单段中间·第 20 段）——
    for gate in _SIMPLE_GATES_PRE_A11Y:
        _run_simple_gate(ctx, gate)
    _gate_a11y(ctx)
    for gate in _SIMPLE_GATES_POST_A11Y:
        _run_simple_gate(ctx, gate)
    for gate in _STRICT_GATES:
        _run_strict_gate(ctx, gate)
    # —— 收尾 ----
    _probe_health(rep)
    _check_section_lock(ctx)
    return _print_summary(rep)


if __name__ == "__main__":
    sys.exit(main())
