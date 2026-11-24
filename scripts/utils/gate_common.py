"""gate_common.py — 门禁脚本公共骨架（W803 建 · 行为保持收敛）。

## 为什么有这个模块（W803 取证）

`scripts/check_*.py` 一族门禁脚本（第 32-37 槽等）在历史演进中各自内联了同一套骨架，
2026-10-19 实测重复形态：

  · `HERE = os.path.dirname(os.path.abspath(__file__))` + `ROOT = os.path.dirname(HERE)`
    —— 19 个根级脚本各写一遍；
  · 站点页面清单 `sorted(glob(site/data/*.html) + glob(site/*.html) + glob(site/en/*.html))`
    —— CSS/head 门禁各写一遍（其中 2 个是「data + en」二源变体）；
  · `open(f, encoding="utf-8", errors="replace").read()` —— 同上；
  · `<style>…</style>` 提取 + 「块起始行号 = `src[:m.start(1)].count("\\n") + 1`」
    —— CSS 门禁三件各写一遍；
  · 注入式自测的 fails 计数 + 逐例行 + `"---- 第 NN 门禁 self-test：%d/%d 通过 ----"`
    收尾行 + `return 1 if fails else 0` —— 多份逐字相同。

本模块即上述骨架的单一实现。设计红线（与 W761 `path_guard.py` 收敛 14 份内联守卫同款）：

  **只收敛重复，不改写任何既有语义** —— 所有输出的文案、字段、退出码属对外契约，
  收敛前后必须逐字节一致（对拍口径见 `docs/_templates/duipai/duipai.py`）。

## 公共 API

    ROOT / SCRIPTS_DIR / UTILS_DIR   仓库根、scripts/、scripts/utils/（绝对路径）
    read_text(path)                  UTF-8 容错读取（errors="replace"·扫描型门禁）
    read_text_strict(path)           UTF-8 严格读取（治理档门禁·编码异常即抛）
    relpath(path)                    仓库相对路径（历史 os.path.relpath(p, ROOT) 同义）
    site_pages(**sources)            站点页面清单（三源/二源可选·全局排序）
    iter_style_blocks(src)           [(style 块正文, 块起始行号)]（行号算法逐字保留）
    run_case_batch(...)              注入式自测跑批（统一逐例格式 + 收尾行 + 退出码）
    SelfTestTally                    逐例格式自定族复用的计数/收尾/退出码
    cli_main(check, selftest)        统一 CLI 分发（--self-test 走自测，否则只读校验）
    MAX_DOC_BYTES / LEDGER_WINDOW    治理文档体积窗 / 台账行窗（W1315 下沉）
    LEDGER_REL / ARCHIVE_LEDGER_REL  台账正本 / 滚动归档相对路径（W1315 下沉）
    parse_ledger(text)               台账取号与行解析（status/hash/touches·W1315 下沉）
    check_footnote_shape(line)       AGENTS 版本脚注定形判据（W1315 下沉）

## 使用形态

    from utils.gate_common import ROOT, read_text, relpath, site_pages

`python scripts/xxx.py` 直跑时 `sys.path[0]` 即 `scripts/`，故 `utils` 包可直接 import
（与 `scripts/utils/path_guard.py` 既有消费形态一致）。
"""
from __future__ import annotations

import glob
import os
import re
import sys
from collections.abc import Callable, Sequence
from typing import Any

# ---------------------------------------------------------------------------
# 路径常量
# ---------------------------------------------------------------------------
# 三级上溯：本文件 → scripts/utils/ → scripts/ → 仓库根。
# 用 abspath（不用 realpath）以与门禁历史内联写法逐字同义——含软链的机器上二者会分叉，
# 收敛不得夹带这层语义变化。

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(UTILS_DIR)
ROOT = os.path.dirname(SCRIPTS_DIR)

#: `<style …>…</style>` 提取口径（与各门禁历史内联正则逐字一致）
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
# INLINED 副本：由 inline_css.py 写入的标记注释与紧随其后的 <style> 配对。
# 这是识别「共享 CSS 副本」的**稳定契约**——判据不得依赖块内注释文本（如 "tokens.css —"）：
# 那类文本会被任何「剥离 CSS 注释」的动作静默抹掉（W1019 实证：剥注释后 228 页副本被
# 误判为页面私有块，token 覆盖率与动效门禁同时误报）。
INLINED_STYLE_RE = re.compile(
    r"<!--\s*INLINED CSS.*?-->\s*<style[^>]*>(.*?)</style>", re.S | re.I
)


# ---------------------------------------------------------------------------
# 治理文档共享常量与判据（W1315 下沉）
# ---------------------------------------------------------------------------
# 成因（W1315 取证）：这些「同一决策」原先分别住在 batch_closeout.py（体积窗/行窗）、
# check_doc_size_budget.py（脚注定形）、preflight_check.py（台账解析）三个 **CLI 入口**里，
# 消费方只能反向 import 入口模块 ⇒ 8 个入口脚本构成一个强连通分量（batch_cascade →
# check_doc_size_budget → batch_closeout → backfill_changelog → batch_cascade，
# 以及 preflight_check ↔ check_audit_trigger / check_backlog_review）。
# 下沉后入口模块重新成为依赖叶子：入口只向下引用本模块，本模块零 scripts 内部依赖。
# W1120 曾以「省一组 CI」为由拒绝新建中立模块——本次落在**既有** gate_common 内，
# 不新增模块、不新增 CI 组，该权衡不再成立。

#: 治理文档正本体积上限（默认 256KiB·W1119 立·W1315 自 batch_closeout 下沉）
MAX_DOC_BYTES = 262144
#: 台账正本数据行窗口（W1119 立·W1315 自 batch_closeout 下沉）
LEDGER_WINDOW = 60
#: 台账正本相对路径（W1315 自 preflight_check 下沉）
LEDGER_REL = os.path.join("docs", "00-导读", "W批次编号对账表.md")
#: 台账滚动归档相对路径（窗口迁出行的容器·W968 建·W1315 下沉）
ARCHIVE_LEDGER_REL = os.path.join("archive", "docs", "W批次编号对账表-ARCHIVE.md")

# touches 占位符（历史「作废」行以「—」占位·原实现被当成一个路径条目 ⇒ 该行永久出现在
# 在途列表·W825 修）
_TOUCHES_PLACEHOLDERS = {"—", "-", "－", "无", "n/a", "N/A", "(空)", "（空）"}
# W908 放宽：剥星去空后**前缀**匹配（允许嵌套括号证据长尾·如「已收官（hash·自测 33/33
# （T32/T33 双向锁）·…）」）——原单层括号紧匹配把长尾收官格拒识别 → 回退固定下标 cells[4]
# → 被含竖线碎行击穿（W908 认领拦截实测）；主题误认由「右起扫描」防。
_STATUS_CELL_RE = re.compile(r"^(?:已收官|已闭环)")


def _locate_status_idx(cells):
    """状态格**下标**：右起首个「已收官/已闭环」前缀格；无则回退固定下标 4（cells 不足则 -1）。

    W1289：抽出下标形态（值形态 _locate_status 由此派生·单一来源）——
    hash 列定位需要**相对状态格**的偏移（hash = status - 2），
    主题列含裸竖线致整行右移时相对偏移仍成立（禁按固定下标）。
    """
    for i in range(len(cells) - 1, -1, -1):
        norm = re.sub(r"[\s*]+", "", cells[i])
        if _STATUS_CELL_RE.match(norm):
            return i
    return 4 if len(cells) > 4 else -1


def _locate_status(cells):
    """状态列定位：右起首个「已收官/已闭环」前缀格；无则回退固定下标 cells[4]。

    右起扫描的原因：状态列在主题列之右·若主题里偶然出现「已收官」三字·
    右起扫描会优先命中真正的状态格。W908 起前缀匹配（允许证据长尾与嵌套括号）。
    """
    idx = _locate_status_idx(cells)
    return cells[idx] if idx >= 0 else ""


def _split_touches(text):
    """touches 串切分（多分隔符兼容·W897 修）+ 尾注归一（W903 修）+ 反引号包裹解析（W934 修）。

    病根（实测 W896）：本函数与命令行解析**都只按逗号切分**，而台账的 touches 列
    自 W739 起实际用「**·**」（中点）分隔 ⇒ 整串被当成**一个** touches ⇒
    **交集检查恒空假绿**⇒「PREFLIGHT PASS·无交集」是无效结论，撞面防护形同虚设。

    尾注归一（W903·机制审查报告 F1）：台账元素常带说明性尾注（如
    ``docs/11-方案报告/**（22 文件移动）``、``scripts/x.py（管控件·已批）``）——
    **全角括号内不切分且整段丢弃**（注记内常含中点·先切后剥必碎·W903 实现首版
    即踩此坑由负样本测试暴露）。安全性前提：仓内路径零全角括号（W903
    `git ls-files` 实证）；新文件名引入全角括号即破坏此前提。

    反引号包裹解析（W934·架构会话实测报出）：台账 touches 列的路径**常被反引号包裹**
    （`` `docs/00-导读/W批次编号对账表.md` ``），且反引号内可能用「/」并列多个文件
    （`` `a.py` / `b.py` ``）⇒ 旧实现把整段当成**一个** token（还带着反引号）⇒
    与命令行传入的**无反引号**路径字面不等 ⇒ `touches_conflict` 恒返空 ⇒
    「PREFLIGHT PASS·无交集」在**真实撞面时假绿**。
    本版：**反引号内内容整体取一个 token**（内部分隔符不切），反引号外按分隔符切。
    """
    out: set[str] = set()
    buf: list[str] = []
    depth = 0        # 全角括号注记深度
    in_code = False  # 是否在反引号内

    def flush() -> None:
        tok = "".join(buf).strip()
        buf.clear()
        if not tok:
            return
        # 反引号段之间的连接残渣（如 " / "）不是路径 ⇒ 丢弃
        if not tok.strip("/ "):
            return
        out.add(tok)

    for ch in text or "":
        if ch == "（":
            depth += 1
            continue
        if ch == "）":
            depth = max(0, depth - 1)
            continue
        if depth > 0:
            continue  # 注记内容整体丢弃
        if ch == "`":
            flush()              # 反引号段切换前先收尾外层内容
            in_code = not in_code
            continue
        if in_code:
            buf.append(ch)       # 反引号内：分隔符一律不切
            continue
        if ch in ",，、·•":
            flush()
            continue
        buf.append(ch)
    flush()
    return out


def _locate_touches(cells):
    """touches 列定位：末格（列序固定·末列恒为 touches）；占位符归一为空集。"""
    if len(cells) < 7:
        return set()
    last = cells[-1].strip()
    if last in _TOUCHES_PLACEHOLDERS:
        return set()
    return _split_touches(last)


def parse_ledger(text):
    """解析对账表：返回 {max_w, bullet_w, rows}。

    权威取号规则=表头「下一自由号 = 本表 max(W#)+1」（W663 规则）；
    bullet_w=最末一条「现势下一自由号」豁免 bullet（轮换制·供交叉核验；
    表顶部 L8 的「现势」块系上一代机制遗留（末次维护 W720），不参与解析）。
    rows=[{w, status, hash, touches}]——touches 列自 W739 起（历史行空·空集不参与交集判定）；
    hash 列（关联 commit·语义=该批**首笔**提交 hash）自 W1289 起解析（W1289：收官行 hash
    空缺告警判据需要它；列位由状态格内容锚点反推·不按固定下标）；
    兼容缺列旧格式（无第 7 列时 touches=空集）与历史不齐行（W687/W688 补空列后同为 7 列）。
    """
    rows_table = [int(x) for x in re.findall(r"^\|\s*W(\d{3,4})\s*\|", text, re.M)]
    bullets = re.findall(r"\*\*W(\d{3,4})\*\*：现势下一自由号", text)
    rows = []
    for line in text.splitlines():
        m = re.match(r"^\|\s*W(\d{3,4})\s*\|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        s_idx = _locate_status_idx(cells)
        status = cells[s_idx] if s_idx >= 0 else ""
        # W1289：hash 列（关联 commit）定位——**状态格内容锚点**·hash = status 前两格
        # （列序：主题 | hash | CHANGELOG 版段 | 状态）。与仓内列定位 doctrine 同源：
        # 状态格是唯一锚点 ⇒ 主题列含裸竖线致行右移时 hash 仍定位正确（禁按固定下标）。
        h_idx = s_idx - 2
        hash_cell = cells[h_idx] if 0 <= h_idx < len(cells) else ""
        touches = _locate_touches(cells)
        rows.append({"w": int(m.group(1)), "status": status,
                     "hash": hash_cell, "touches": touches})
    return {"max_w": max(rows_table) if rows_table else None,
            "bullet_w": int(bullets[-1]) if bullets else None,
            "rows": rows}


# W1014：AGENTS 脚注固定尾句家具（写入侧 batch_cascade.py 的 tail 逐字对齐）——C4 逐条
# 计量前剥它，使判据口径与写入侧「量 note 本体」一致；否则末条 = note + 家具被合并计数，
# 任何 97–120 字注记皆「级联绿 / 门禁红」（W1013 首踩）
_FOOTNOTE_TAIL_RE = re.compile(r"。?如与上述权威文档冲突，以权威文档为准。?\*+\s*$")
# W1272：形态合规判据（前导句号**必需**·与写入侧 compose_agents_entry 同源）——
# 剥离仍按可选（不误伤长度计量），但形态漂移**单独判红**：否则句号一丢即静默漂移、
# 写入侧每批收官卡死（W1266 同族复发·W1272 实证·两侧口径不一致 = 静默漂移）。
_FOOTNOTE_TAIL_STRICT_RE = re.compile(r"。如与上述权威文档冲突，以权威文档为准。?\*+\s*$")


def footnote_tail_shape_ok(footnote_line):
    """脚注尾句**形态**合规（前导句号必需·与写入侧同源）→ 违规描述列表（空 = 合规）。

    W1272：原实现只有「剥离用」的正则（前导句号可选）⇒ 句号丢失时长度计量照常、
    门禁全绿，而写入侧字面断言卡死**每批收官** ⇒ 两侧口径不一致 = 静默漂移。
    ⇒ 形态检查独立成判据（不改剥离口径·不误伤长度计量）。
    """
    if "如与上述权威文档冲突" not in footnote_line:
        return []
    if _FOOTNOTE_TAIL_STRICT_RE.search(footnote_line):
        return []
    return ["脚注尾句缺前导句号「。」（写入侧 compose_agents_entry 恒带句号·两侧口径须同源）"]


def check_footnote_shape(footnote_line, cap=120):
    r"""AGENTS 版本脚注逐条定形判据（W965 C4·W1014 口径对齐）→ 违规描述列表（空 = 合规）。

    计量对象 = **剥去固定尾句家具后的条目本体**，与写入侧 batch_cascade 的
    `spec.agents_note 长 > 120` 守卫同一口径。家具是文档级免责句（非任何一批的注记），
    原实现把它并进末条计数 ⇒ 97–120 字注记「级联绿 / 门禁红」（W1013 首踩：117 字被算 141）。
    剥离只影响末条的家具部分，条目本体超长照样抓（见 _self_test 负样本）。
    """
    bad = []
    bad.extend(footnote_tail_shape_ok(footnote_line))
    for e in re.split(r"；(?=20\d{2}-\d{2}-\d{2}（)", footnote_line)[1:]:
        if not re.match(r"^20\d{2}-\d{2}-\d{2}（W\d{3,4}）", e):
            bad.append("条目头非阿拉伯形态：" + e[:24])
            continue
        body = _FOOTNOTE_TAIL_RE.sub("", e)
        if len(body) > cap:
            bad.append("条目 %d 字 > %d：%s…" % (len(body), cap, body[:24]))
    return bad


# ---------------------------------------------------------------------------
# 读取与路径
# ---------------------------------------------------------------------------

def read_text(path: str) -> str:
    """按 UTF-8 容错读取文件（`errors="replace"`，与门禁历史内联写法一致）。

    容错而非抛错是刻意的：门禁要扫全站 800+ 页，单页编码异常不应中断整批扫描，
    而应以替换字符呈现、在判定阶段自然暴露。

    适用面：**扫描型**门禁（CSS/head 族——对象是站点产物，求「扫得完」）。
    治理档门禁（AGENTS/CLAUDE 族）读的是仓库自有 UTF-8 文件，编码异常应当立刻炸出来，
    请用 `read_text_strict()`——两种读取口径不可互替（W803 裁决）。
    """
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def read_text_strict(path: str) -> str:
    """按 UTF-8 严格读取文件（编码异常即抛 `UnicodeDecodeError`）。

    适用面：**治理档门禁**——读 `AGENTS.md` / `CLAUDE.md` / `verify_delivery.py` 这类
    仓库自有文件。这些文件若编码坏了，是必须立刻暴露的仓库事故，容错读取会把事故
    降级成「某个中文词没匹配上」的静默误判。
    """
    with open(path, encoding="utf-8") as f:
        return f.read()


def relpath(path: str) -> str:
    """返回相对仓库根的路径（历史 `os.path.relpath(p, ROOT)` 同义）。"""
    return os.path.relpath(path, ROOT)


# ---------------------------------------------------------------------------
# 站点页面清单
# ---------------------------------------------------------------------------

def site_pages(*, data: bool = True, root: bool = True, en: bool = True) -> list[str]:
    """收集站点页面清单，全局排序。

    与历史写法 `sorted(glob(A) + glob(B) + glob(C))` **同序**：`sorted()` 作用于拼接后的
    整体，故此处同样先拼接再整体排序。**不可**改成「逐源排序后拼接」——那会改变跨目录的
    相对顺序（如 `site/data/x.html` 与 `site/en/a.html` 的先后）。

    参数（按需取源；全 False 时返回空表）：
        data: 是否含 `site/data/*.html`（可视化页）
        root: 是否含 `site/*.html`（站点根页）
        en:   是否含 `site/en/*.html`（英文站）
    """
    parts: list[str] = []
    if data:
        parts += glob.glob(os.path.join(ROOT, "site", "data", "*.html"))
    if root:
        parts += glob.glob(os.path.join(ROOT, "site", "*.html"))
    if en:
        parts += glob.glob(os.path.join(ROOT, "site", "en", "*.html"))
    return sorted(parts)


def iter_style_blocks(src: str) -> list[tuple[str, int]]:
    """提取 `<style>` 块正文与块起始行号。

    行号算法与历史内联写法逐字一致：`src[:m.start(1)].count("\\n") + 1`，即块正文首行
    在全文件中的 1 基行号（各门禁据此打印 `文件:行号` 定位）。

    返回：
        [(块正文, 起始行号), …]，按出现顺序。
    """
    return [
        (m.group(1), src[: m.start(1)].count("\n") + 1)
        for m in STYLE_BLOCK_RE.finditer(src)
    ]


def iter_private_style_blocks(src: str) -> list[tuple[str, int]]:
    """页面**私有** `<style>` 块（跳过 INLINED tokens/system 副本），返回同 `iter_style_blocks`。

    判据取 `inline_css.py` 写入的 `<!-- INLINED CSS … -->` 标记与紧随 `<style>` 的配对，
    而非块内注释文本——后者会被「剥离 CSS 注释」静默破坏（见 INLINED_STYLE_RE 注释）。
    """
    inlined = {m.start(1) for m in INLINED_STYLE_RE.finditer(src)}
    return [
        (m.group(1), src[: m.start(1)].count("\n") + 1)
        for m in STYLE_BLOCK_RE.finditer(src)
        if m.start(1) not in inlined
    ]


# ---------------------------------------------------------------------------
# 注入式自测跑批
# ---------------------------------------------------------------------------

def run_case_batch(
    cases: Sequence[Any],
    evaluate: Callable[[Any], tuple[Any, Any]],
    label: str,
    *,
    got_text: Callable[[Any], str] = str,
    want_text: Callable[[Any], str] = str,
    line_format: str = "  %s %s（期望 %s）",
) -> int:
    """跑一批注入式自测用例，返回退出码（0 全过 / 1 有失败）。

    参数：
        cases:       用例序列，元素原样交给 `evaluate`（形态由各门禁自定）
        evaluate:    `(case) -> (got, want)`；`got == want` 即该例 PASS
        label:       收尾行标签，输出 `---- {label} self-test：{通过}/{总数} 通过 ----`
        got_text:    `got` 的渲染函数（默认 `str`；逐例行只打印期望值时用不到）
        want_text:   `want` 的渲染函数——各门禁期望值文案不同
                     （`"2 处"` / `"无违例"` / `"exit 0"` / `"missing=True"`），故由调用方提供
        line_format: 逐例输出格式，默认 `"  %s %s（期望 %s）"` = 状态、用例名、期望值

    说明：失败明细由各门禁自行追加打印——「明细行长什么样」属各门禁自有文案，
    不塞进公共层；本函数只负责计数、逐例状态行、收尾行与退出码。
    """
    fails = 0
    for case in cases:
        got, want = evaluate(case)
        ok = got == want
        if not ok:
            fails += 1
        print(line_format % ("PASS" if ok else "FAIL", case[0], want_text(want)))
    print("---- %s self-test：%d/%d 通过 ----" % (label, len(cases) - fails, len(cases)))
    return 1 if fails else 0


class SelfTestTally:
    """自测计数与收尾行（供逐例输出格式自定的门禁族复用）。

    适用形态：各门禁的判定函数签名与逐例输出差异较大（如需打印失败明细，或逐例只输出
    「状态 + 用例名」），无法套用 `run_case_batch` 的统一格式时，至少把「计数 → 收尾行 →
    退出码」这段逐字相同的逻辑收敛到此处。

        tally = SelfTestTally("第 41 门禁 AGENTS 分层完整性")
        for …:
            if not tally.add(ok):
                …  # 打印本门禁自有明细
        return tally.report()
    """

    def __init__(self, label: str) -> None:
        self.label = label
        self.total = 0
        self.fails = 0

    def add(self, ok: bool) -> bool:
        """登记一例结果，原样回传 `ok`。"""
        self.total += 1
        if not ok:
            self.fails += 1
        return ok

    @property
    def passed(self) -> int:
        return self.total - self.fails

    def report(self) -> int:
        """打印收尾行并返回退出码（0 全过 / 1 有失败）。"""
        print("---- %s self-test：%d/%d 通过 ----" % (self.label, self.passed, self.total))
        return 1 if self.fails else 0


# ---------------------------------------------------------------------------
# CLI 分发
# ---------------------------------------------------------------------------

def cli_main(run_check: Callable[[], int], run_self_test: Callable[[], int]) -> int:
    """门禁脚本统一的 CLI 分发：`--self-test` 走自测，否则走只读校验。

    这是门禁族用了最久、复制得最多的一段（`main()` 两分支 + `sys.exit(main())`），
    收敛在此以统一「CLI 形态」：**无参 = 只读校验，`--self-test` = 注入式自测**，
    其余参数一律忽略（与各门禁历史行为一致——它们只看 `sys.argv` 里有没有这个标记）。

    参数：
        run_check:      默认分支（无 `--self-test` 时调用）
        run_self_test:  `--self-test` 分支
    返回：
        两个分支各自的退出码，由调用方 `sys.exit(...)` 透传。
    """
    if "--self-test" in sys.argv:
        return run_self_test()
    return run_check()


__all__ = [
    "ARCHIVE_LEDGER_REL",
    "INLINED_STYLE_RE",
    "LEDGER_REL",
    "LEDGER_WINDOW",
    "MAX_DOC_BYTES",
    "ROOT",
    "SCRIPTS_DIR",
    "STYLE_BLOCK_RE",
    "UTILS_DIR",
    "SelfTestTally",
    "check_footnote_shape",
    "cli_main",
    "footnote_tail_shape_ok",
    "iter_private_style_blocks",
    "iter_style_blocks",
    "parse_ledger",
    "read_text",
    "read_text_strict",
    "relpath",
    "run_case_batch",
    "site_pages",
]
