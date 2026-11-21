"""W736 单元测试·preflight_check.py（S-33）·pytest 风格
W739 扩展：touches 列解析 / 在途判定 / 交集拒绝（多 Agent 干扰治理机制）。

覆盖：
  - parse_ledger        对账表取号解析（max W + 现势下一自由号 + rows 含 touches）
  - is_inflight         在途批次状态判定（已收官/已闭环 开头为 done）
  - touches_conflict    touches 交集纯函数
  - summarize_porcelain 工作树态统计（staged/未暂存/未跟踪三态计数）

运行：py -m pytest tests/unit/test_preflight_check.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import preflight_check  # noqa: E402

ROOT_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "scripts"

LEDGER_SAMPLE = "\n".join([
    "| W735 | 全仓归档大扫除批 | 1fd372b4 | W735 | 已收官 | 主会话 |",
    "| W739 | touches 机制批 | 认领占位 | W739 | 进行中 | 主会话 | AGENTS.md, pitfalls.md |",
    "- **W733**：现势下一自由号（756a7089 w732 收官级联后 checklist 例行）——预留登记豁免。",
    "- **W736**：现势下一自由号（1fd372b4 w735 收官级联后 checklist 例行）——预留登记豁免。",
    "> ## 现势：下一自由号 = **W721**（上一代机制遗留块·不参与解析）",
])


def test_parse_ledger_max_and_last_bullet():
    got = preflight_check.parse_ledger(LEDGER_SAMPLE)
    assert got["max_w"] == 739
    assert got["bullet_w"] == 736  # 取最末 bullet（轮换制），非首条、非遗留块


def test_parse_ledger_claimed_state():
    text = LEDGER_SAMPLE + "\n| W736 | 发布工具链批 | 待收官 | W736 | 进行中 | 主会话 |"
    got = preflight_check.parse_ledger(text)
    assert got["max_w"] == 739  # max 即已认领号（下一自由号=740）
    w736 = [r for r in got["rows"] if r["w"] == 736]
    assert len(w736) == 1 and w736[0]["status"] == "进行中"


def test_parse_ledger_tolerates_empty():
    got = preflight_check.parse_ledger("无表格")
    assert got == {"max_w": None, "bullet_w": None, "rows": []}


def test_parse_ledger_touches_column():
    got = preflight_check.parse_ledger(LEDGER_SAMPLE)
    w739 = [r for r in got["rows"] if r["w"] == 739][0]
    assert w739["touches"] == {"AGENTS.md", "pitfalls.md"}
    assert w739["status"] == "进行中"


def test_parse_ledger_touches_backcompat_old_format():
    # 6 列旧格式行（无 touches 列）→ touches 空集（向后兼容）
    got = preflight_check.parse_ledger("| W735 | 归档批 | 1fd372b4 | W735 | 已收官 | 主会话 |")
    assert got["rows"][0]["touches"] == set()


def test_is_inflight_states():
    assert preflight_check.is_inflight("进行中")
    assert preflight_check.is_inflight("进行中（剩余=真端点联调待用户三键）")
    assert preflight_check.is_inflight("待收官")
    assert not preflight_check.is_inflight("已收官")
    assert not preflight_check.is_inflight("已收官（830d3b39）")
    assert not preflight_check.is_inflight("已闭环")


def test_is_inflight_strips_markdown_bold():
    # W739 狗粮实证：状态列带 Markdown 强调符（**已收官**）不剥离会误判在途
    assert not preflight_check.is_inflight("**已收官**（5dca5834）")
    assert not preflight_check.is_inflight("**已闭环**")
    assert preflight_check.is_inflight("**进行中**")


def test_inflight_recognizes_merged_status():
    """W1160 根修锁：「已合并」是兄弟会话 PR 收官登记形态，必须判非在途。

    实证：W1137/W1147 状态列「**已合并（PR #142·8f724d1f）**」不被识别 ⇒
    preflight 每批误报「登记滞后」WARN ×19（触发器噪音淹没真信号）。
    同族形态「已让号/已撤销」（让号先例 W894/W1039）一并纳入。
    """
    assert not preflight_check.is_inflight("**已合并（PR #142·8f724d1f）**")
    assert not preflight_check.is_inflight("已合并")
    assert not preflight_check.is_inflight("**已让号（W895 先落地）**")
    assert not preflight_check.is_inflight("**已撤销（撞号停手）**")
    # 真在途形态仍判在途（判据强度不降）
    assert preflight_check.is_inflight("在途（认领·未收官）")
    assert preflight_check.is_inflight("进行中（剩余=联调）")

def test_inflight_with_bold_status_variants():
    # W741 加固回归：单星/多星/空白变体（replace("**") 防不住单星·re.sub 全量剥离）
    assert not preflight_check.is_inflight("*已收官*")
    assert not preflight_check.is_inflight("***已收官***")
    assert not preflight_check.is_inflight("  已收官  ")
    assert not preflight_check.is_inflight("*已收官*（4b1f007f）")
    assert not preflight_check.is_inflight("** 已闭环 **")
    assert preflight_check.is_inflight("*进行中*")
    assert preflight_check.is_inflight(" 已认领 ")


def test_summarize_porcelain_counts():
    text = ("M  scripts/verify_delivery.py\x00"
            " M CHANGELOG.md\x00"
            "?? docs/00-导读/新文档.md\x00"
            "A  tests/unit/test_release_prep.py\x00")
    got = preflight_check.summarize_porcelain(text)
    assert got["staged"] == 2
    assert got["unstaged"] == 1
    assert got["untracked"] == 1
    assert len(got["items"]) == 4
    assert ("??", "docs/00-导读/新文档.md") in got["items"]


def test_summarize_porcelain_untracked_counted():
    text = "?? tmpe/w736/x.py\x00 M docs/x.md\x00"
    got = preflight_check.summarize_porcelain(text)
    assert got["untracked"] == 1
    assert got["unstaged"] == 1


def test_touches_conflict_intersection():
    mine = {"AGENTS.md", "scripts/README.md"}
    assert preflight_check.touches_conflict({"AGENTS.md"}, mine) == ["AGENTS.md"]
    assert preflight_check.touches_conflict({"CHANGELOG.md"}, mine) == []
    assert preflight_check.touches_conflict(set(), mine) == []


def test_touches_conflict_multi_path():
    inflight = {"docs/00-导读/文档规范.md", "AGENTS.md", "pitfalls.md"}
    mine = {"AGENTS.md", "pitfalls.md", "scripts/README.md"}
    assert preflight_check.touches_conflict(inflight, mine) == ["AGENTS.md", "pitfalls.md"]


# ---------------------------------------------------------------------------
# W821：§8 干扰日志机器触发点（真触发才提示·用户裁决 2026-10-20）
# ---------------------------------------------------------------------------
# 背景：W741 立的两周干扰日志（路线图 §8）自 2026-10-16 断档 4 天 128 提交零登记，
# 而该期间实际发生 ≥2 次强制触发事件——根因是「该日志无任何机器防线·纯自觉动作」。
# W821 给 preflight / safe_commit 加提示行，把「靠人记得写」变成「机器喊一声」；
# **只加提示，不改任何判定与退出码**（用户裁决：只在真正触发时才提示·不输出常态提醒）。


def test_interference_log_hint_mentions_carrier_and_window():
    """W821 建提示含载体与窗口；W922 窗口收官（用户裁决）后改为锁定收官表述与载体。"""
    hint = preflight_check.interference_log_hint("preflight 交集拒绝")
    assert "interference-governance-roadmap.md" in hint, "提示须指向 §8 干扰日志载体"
    assert "§8" in hint, "提示须点明是 §8 干扰日志"
    assert "收官归档" in hint, "W922 起须点明窗口已收官（2026-10-24）"
    assert "命中：preflight 交集拒绝" in hint, "提示须带命中原因"


def test_interference_log_hint_is_not_emitted_unless_triggered():
    """W821：提示只在真触发时输出——不产生常态噪音（用户裁决核心）。"""
    import contextlib
    import io as _io
    # 正常态（无在途批次·无交集·工作树干净）→ 输出中不得含提示
    buf = _io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = preflight_check.main.__wrapped__() if hasattr(preflight_check.main, "__wrapped__") else None
    # main() 依赖 argv·此处不直接调用；改为断言「提示常量不被无条件打印」——
    # 即常量定义存在但调用点全在条件分支内（源码级断言）
    src = (ROOT_SCRIPTS / "preflight_check.py").read_text(encoding="utf-8")
    call_lines = [ln for ln in src.split("\n") if "interference_log_hint(" in ln and "def " not in ln]
    # 两处调用点都必须处于条件分支内（调用行本身或**上一行**含 if——
    # 块内调用写在 if 行的下一行是本仓通例，不能只看同行）
    # 注：触发①（开工已暂存变更）已按用户裁决删除·现役只剩 1 处调用点（touches 交集拒绝）
    assert len(call_lines) == 1, "预期 1 处调用点（touches 交集拒绝），实得 %d" % len(call_lines)
    src_lines = src.split("\n")
    for ln in call_lines:
        idx = src_lines.index(ln)
        indent = len(ln) - len(ln.lstrip())
        # 向上找同一缩进层（或更外层）的最近一条 if 语句——调用点须落在其块内
        guarded = False
        for back in range(idx - 1, -1, -1):
            prev = src_lines[back]
            if not prev.strip():
                continue
            prev_indent = len(prev) - len(prev.lstrip())
            if prev_indent < indent and prev.strip().startswith("if "):
                guarded = True
                break
            if prev_indent < indent and not prev.strip().startswith(("if ", "for ", "while ", "with ", "try", "else", "elif")):
                break
        assert guarded, "调用点必须处于条件分支内（禁常态输出）：%s" % ln.strip()
    assert rc is None or rc == 0, "本用例不改变 preflight 退出码"


def test_interference_log_hint_in_safe_commit():
    """W821：safe_commit 的 ref-lock 重试路径同样带提示（触发②）。"""
    src = (ROOT_SCRIPTS / "safe_commit.py").read_text(encoding="utf-8")
    assert "INTERFERENCE_LOG_HINT" in src, "safe_commit 须带提示常量"
    call_lines = [ln for ln in src.split("\n") if "interference_log_hint(" in ln and "def " not in ln]
    assert len(call_lines) == 1, "预期 1 处调用点（ref-lock 竞争重试路径），实得 %d" % len(call_lines)
    src_lines = src.split("\n")
    for ln in call_lines:
        idx = src_lines.index(ln)
        indent = len(ln) - len(ln.lstrip())
        # 向上找同一缩进层（或更外层）的最近一条 if 语句——调用点须落在其块内
        guarded = False
        for back in range(idx - 1, -1, -1):
            prev = src_lines[back]
            if not prev.strip():
                continue
            prev_indent = len(prev) - len(prev.lstrip())
            if prev_indent < indent and prev.strip().startswith("if "):
                guarded = True
                break
            if prev_indent < indent and not prev.strip().startswith(("if ", "for ", "while ", "with ", "try", "else", "elif")):
                break
        assert guarded, "调用点必须处于条件分支内（禁常态输出）：%s" % ln.strip()


# ---------------------------------------------------------------------------
# W825：解析层格式鲁棒性（状态列/touches 列按内容定位·禁按固定下标）
# ---------------------------------------------------------------------------
#
# 成因（实测 W764 行·8 格）：认领行摘要含裸竖线 → Markdown 按竖线分列 → 行被切成
# 8/9 格（标准 7 格）→ 固定下标 cells[4]/cells[6] 随即读错：状态读到摘要残段
# （「W764」被当状态）→ **已收官批次被永久判为在途**（在途列表幻影·误导后续批次）；
# touches 读到认领会话列（非路径垃圾串）。W750 行另以「—」占位 touches → 同样成幻影。


def test_parse_ledger_survives_extra_cell_from_pipe_in_summary():
    """W825 核心：摘要含裸竖线（行被切成 8 格）时，状态与 touches 仍须定位正确。"""
    line = (
        "| W900 | 修复 `a|b` 形态的批 | abc1234（级联） | W900 | **已收官**（abc1234） | 主会话 | AGENTS.md, pitfalls.md |"
    )
    got = preflight_check.parse_ledger(line)
    assert len(got["rows"]) == 1
    row = got["rows"][0]
    assert row["status"] == "**已收官**（abc1234）", "状态列读错：%r" % row["status"]
    assert not preflight_check.is_inflight(row["status"]), "已收官批次不得被误判为在途"
    assert row["touches"] == {"AGENTS.md", "pitfalls.md"}, "touches 列读错：%r" % row["touches"]


def test_parse_ledger_touches_placeholder_is_empty_set():
    """W825：占位符「—」不是路径条目（原实现把它当成一个路径·使该行永驻在途列表）。"""
    got = preflight_check.parse_ledger(
        "| W750 | 路由版改写批（**已作废**） | 作废·未提交 | — | **作废** | 主会话 2026-10-15 | — |")
    row = got["rows"][0]
    assert row["touches"] == set(), "占位符 touches 应归一为空集：%r" % row["touches"]


def test_parse_ledger_status_not_confused_by_summary_mentioning_done():
    """W825：主题里偶然出现「已收官」三字不得被误认作状态（紧匹配·右起扫描）。"""
    got = preflight_check.parse_ledger(
        "| W901 | 补齐已收官遗漏的判据批 | 待提交 | W901 | 进行中 | 主会话 | AGENTS.md |")
    row = got["rows"][0]
    assert row["status"] == "进行中", "状态被主题串扰：%r" % row["status"]
    assert preflight_check.is_inflight(row["status"])


def test_parse_ledger_normal_row_unchanged():
    """W825 回归锚：标准 7 格行的解析结果与修复前逐字一致（不因修法改变既有语义）。"""
    got = preflight_check.parse_ledger(LEDGER_SAMPLE)
    w739 = [r for r in got["rows"] if r["w"] == 739][0]
    assert w739["status"] == "进行中"
    assert w739["touches"] == {"AGENTS.md", "pitfalls.md"}
    w735 = [r for r in got["rows"] if r["w"] == 735][0]
    assert w735["status"] == "已收官"
    assert w735["touches"] == set()


# ---------------------------------------------------------------------------
# W956 / P-43-01：在途判定加 git 条件（登记滞后 = 告警不拒绝）
# ---------------------------------------------------------------------------


def test_wnum_commit_index_counts_tagged_subjects():
    """只认 type(w###): 批次标签形态；同一号多笔合并计数并记首笔短 hash。"""
    idx = preflight_check.wnum_commit_index([
        "d093bf64 docs(w955): GSAP 计划子批",
        "e5b262e7 docs(w884): 审计落盘",
        "92175003 chore(w884): 收官回填",
        "10dc5d75 docs(w954): 收官回填",
    ])
    assert idx[884] == [2, "e5b262e7"]
    assert idx[955] == [1, "d093bf64"]
    assert 954 in idx


def test_wnum_commit_index_ignores_prose_mentions():
    """负样本：散文提及别批号（承接/教训/引用）不得计入——防误降真在途批的 touches 防护。"""
    idx = preflight_check.wnum_commit_index([
        "chore(w950): 承接 W940 题材关修正后的打磨",
        "docs: 复盘引用 W954 报告实例",
        "feat(w951): 正常批次标签",
    ])
    assert 940 not in idx and 954 not in idx
    assert 951 in idx


def test_wnum_commit_index_empty_and_case():
    """空输入安全 + 大小写不敏感（历史提交存在大写 W 形态）。"""
    assert preflight_check.wnum_commit_index([]) == {}
    assert preflight_check.wnum_commit_index(["abc1234 FIX(W123): x"]) == {123: [1, "abc1234"]}



def test_wnum_commit_index_scope_comma_separated():
    """scope 段逗号分隔形态（fix(ci,w1191):）必须计入——原正则只认「括号内恰好是 w+数字」
    ⇒ P-43-01 反填对这类批次判「无批次标签提交」而拒绝回填（W1211 实测 W1191 命中）。"""
    idx = preflight_check.wnum_commit_index([
        "f5729d68f fix(ci,w1191): GitHub「Security and quality」全清",
    ])
    assert idx[1191] == [1, "f5729d68f"]


def test_wnum_commit_index_multi_tag_counts_each():
    """一笔提交含多个批次标签时各号各计——原实现只 search 一次（注释与实现不符）。"""
    idx = preflight_check.wnum_commit_index([
        "abcdef12 feat(w932,w933): 跨批提交",
    ])
    assert idx[932] == [1, "abcdef12"]
    assert idx[933] == [1, "abcdef12"]


def test_wnum_commit_index_ignores_later_bracket_prose():
    """首个括号组之后的散文括号引用不得计入（保持原语义·防误降在途批防护）。"""
    idx = preflight_check.wnum_commit_index([
        "12345678 feat(w932): 主体提交 (见 w933 讨论)",
    ])
    assert 932 in idx and 933 not in idx


def test_wnum_commit_index_still_ignores_prose_mentions():
    """回归锁：散文提及形态仍不计入（形态放宽不得削弱 touches 交集拒绝）。"""
    idx = preflight_check.wnum_commit_index([
        "chore(w950): 承接 W940 题材关修正后的打磨",
        "docs: 复盘引用 W954 报告实例",
    ])
    assert 940 not in idx and 954 not in idx


def test_wnum_commit_index_description_leading_wnum():
    """P-43-01（W1228 根修）：描述段开头 W 形态（type(scope)?: W#### 主题）必须计入——
    仓内批次提交既成惯例（W1209/W1210/W1226/W1227 实测形态），原判据只认 scope 段
    ⇒ ledger_backfill 对这类批次判「无批次标签提交」。用真实 subject 作正样本。"""
    idx = preflight_check.wnum_commit_index([
        "dfff13ecf chore(repo): W1209 仓库体积治理——历史改写 + LFS 迁移 + commit hash 回填",
        "a1212a228 chore(repo): W1226 T-1 远端 tag v2.3.0 清理落地（用户令批准）",
    ])
    assert idx[1209] == [1, "dfff13ecf"]
    assert idx[1226] == [1, "a1212a228"]


def test_wnum_commit_index_description_leading_no_scope():
    """无 scope 形态（type: W#### 主题）同属批次标签惯例（docs: W#### 台账回填）。"""
    idx = preflight_check.wnum_commit_index([
        "57fa19136 docs: W1227 台账收官回填（commit hash + 三问结论）",
    ])
    assert idx[1227] == [1, "57fa19136"]


def test_wnum_commit_index_description_prose_still_ignored():
    """负样本：描述段不以 W 开头的散文提及仍不计（「按 W### 计划」「承接 W###」）。"""
    idx = preflight_check.wnum_commit_index([
        "1234567 docs: 按 W1230 计划执行方案批",
        "2345678 fix: 承接 W1231 教训的回归锁",
        "3456789 chore: 提及 W940 教训但不带批次标签",
    ])
    assert idx == {}


def test_wnum_commit_index_double_form_counts_once():
    """同笔提交 scope 段与描述段都带同号 ⇒ 该号只计一次（防双形态重复计数）。"""
    idx = preflight_check.wnum_commit_index([
        "abcdef99 chore(w1209): W1209 仓库体积治理",
    ])
    assert idx[1209] == [1, "abcdef99"]


def test_wnum_commit_index_merge_subject_not_counted():
    """负样本：merge 提交 subject（无 conventional 头冒号形态）不计。"""
    idx = preflight_check.wnum_commit_index([
        "420f654d7 Merge pull request #178 from 1273984347/sync/w1223-w1224-main",
    ])
    assert idx == {}


def test_split_inflight_lagged_basic():
    """git 已有提交的登记面在途行 → lagged（退出拒绝集）；无提交的保留真在途。"""
    rows = [
        {"w": 931, "status": "在途（认领·未收官）", "touches": {"a.py"}},
        {"w": 936, "status": "在途（认领·未收官）", "touches": {"b.py"}},
    ]
    committed = {931: [3, "da1e3d6e"]}
    truly, lagged = preflight_check.split_inflight_lagged(rows, committed)
    assert [r["w"] for r in truly] == [936]
    assert [r["w"] for r in lagged] == [931]


def test_split_inflight_lagged_self_never_lagged():
    """本批自己的在途行（无提交）不得入 lagged——自己的行由交集检查按 self 排除。"""
    rows = [{"w": 956, "status": "在途（认领·未收官）", "touches": {"a.py"}}]
    truly, lagged = preflight_check.split_inflight_lagged(rows, {}, self_num=956)
    assert truly == rows and lagged == []


# ---------------------------------------------------------------------------
# W1289：台账 hash 列空缺告警（已收官 + hash 空/占位 + git 已有该 W 提交）
# ---------------------------------------------------------------------------
# 病根（实证）：台账状态列写「已收官」而 hash 列仍是空/占位的批次**静默累积**——
# 「登记滞后」判据只覆盖「状态在途 + git 已有提交」这一族 ⇒ 本族完全不告警
# ⇒ hash 列长期空缺 ⇒「W#↔commit 对照」失效（实测已累积 8 行）。
# 判据为 **WARN 级**：告警不拒绝·不改退出码·不参与 touches 交集拒绝。


def test_parse_ledger_extracts_hash_column():
    """W1289：hash 列（关联 commit）须被解析出来——按状态格锚点反推·不按固定下标。

    形态：标准 9 格行（主题 | hash | CHANGELOG 版段 | 状态 | 认领会话 | …）
    与「主题含裸竖线致行右移」形态（W825）两种都要定位正确。
    """
    row = preflight_check.parse_ledger(
        "| W1275 | 铺开批 | —（待回填） | —（待回填） | 已收官（对抗审查已派发） "
        "| 主会话 | — | 本会话（W1275） | site/en/ |")["rows"][0]
    assert row["hash"] == "—（待回填）", "hash 列读错：%r" % row["hash"]
    # 主题含裸竖线（W825 形态）→ 行右移一格 → hash 仍须定位正确
    row2 = preflight_check.parse_ledger(
        "| W900 | 修复 a|b 形态的批 | abc1234 | W900 | **已收官**（abc1234） "
        "| 主会话 | AGENTS.md |")["rows"][0]
    assert row2["hash"] == "abc1234", "hash 列读错：%r" % row2["hash"]


def test_hash_is_unfilled_placeholder_forms():
    """hash 空缺形态覆盖：空串 / 破折号开头 / 含「待回填」；合法 hash 不算空缺。"""
    for ph in ("", "   ", "—", "—（待回填）", "-（待回填）", "待回填", "—（末笔同首笔）"):
        assert preflight_check.hash_is_unfilled(ph), "占位形态须判未回填：%r" % ph
    for ok in ("df7f295cf", "`18eebbaca`", "fba21241b（本批首笔）", "653a366e9"):
        assert not preflight_check.hash_is_unfilled(ok), "合法 hash 不得判未回填：%r" % ok


def test_find_hash_unfilled_backfilled_hash_not_hit():
    """① 已回填 hash（合法形态）+ 状态已收官 + git 有提交 ⇒ **不命中**。"""
    rows = [{"w": 1263, "status": "**已收官**（commit 067adef8d）",
             "hash": "067adef8d", "touches": set()}]
    committed = {1263: [1, "067adef8d"]}
    assert preflight_check.find_hash_unfilled(rows, committed) == []


def test_find_hash_unfilled_hit_when_placeholder_and_committed():
    """② hash 列为空/占位 + 状态已收官 + git 有该 W 提交 ⇒ **命中**（W1289 判据本体）。"""
    rows = [{"w": 1275, "status": "已收官（对抗审查已派发·hash 待下批回填）",
             "hash": "—（待回填）", "touches": set()}]
    committed = {1275: [3, "aaa11111"]}
    hits = preflight_check.find_hash_unfilled(rows, committed)
    assert [r["w"] for r in hits] == [1275], "命中集应含 W1275：%r" % hits


def test_find_hash_unfilled_no_commit_not_hit():
    """③ hash 列空/占位 + 状态已收官 + git **无**该 W 提交 ⇒ **不命中**（防误报）。

    只读批次无提交是正常态（无从回填 ⇒ 不该喊）。
    """
    rows = [{"w": 1262, "status": "已收官（成果已并入 W1263 收官）",
             "hash": "—", "touches": set()}]
    assert preflight_check.find_hash_unfilled(rows, {}) == []
    assert preflight_check.find_hash_unfilled(rows, {1300: [1, "bbb22222"]}) == []


def test_find_hash_unfilled_self_row_excluded():
    """④ 自指行排除：传入 self_num 等于该行 W 号 ⇒ **不命中**（同 split_inflight_lagged 语义）。"""
    rows = [{"w": 1289, "status": "已收官（hash 待回填）",
             "hash": "—（待回填）", "touches": set()}]
    committed = {1289: [1, "ccc33333"]}
    assert preflight_check.find_hash_unfilled(rows, committed, self_num=1289) == []
    # 不传 self_num 时命中（对照组：排除逻辑真在起作用）
    assert [r["w"] for r in preflight_check.find_hash_unfilled(rows, committed)] == [1289]


def test_find_hash_unfilled_inflight_row_not_hit():
    """在途行（状态未收官）不命中——本判据只管「已收官却没回填 hash」这一族。"""
    rows = [{"w": 1290, "status": "在途（认领·未收官）",
             "hash": "—（待回填）", "touches": set()}]
    committed = {1290: [1, "ddd44444"]}
    assert preflight_check.find_hash_unfilled(rows, committed) == []
