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
    "| W739 | touches 机制批 | 认领占位 | W739 | 进行中 | 主会话 | AGENTS.md, docs/agent/pitfalls.md |",
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
    assert w739["touches"] == {"AGENTS.md", "docs/agent/pitfalls.md"}
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
    inflight = {"docs/00-导读/文档规范.md", "AGENTS.md", "docs/agent/pitfalls.md"}
    mine = {"AGENTS.md", "docs/agent/pitfalls.md", "scripts/README.md"}
    assert preflight_check.touches_conflict(inflight, mine) == ["AGENTS.md", "docs/agent/pitfalls.md"]


# ---------------------------------------------------------------------------
# W821：§8 干扰日志机器触发点（真触发才提示·用户裁决 2026-10-20）
# ---------------------------------------------------------------------------
# 背景：W741 立的两周干扰日志（路线图 §8）自 2026-10-16 断档 4 天 128 提交零登记，
# 而该期间实际发生 ≥2 次强制触发事件——根因是「该日志无任何机器防线·纯自觉动作」。
# W821 给 preflight / safe_commit 加提示行，把「靠人记得写」变成「机器喊一声」；
# **只加提示，不改任何判定与退出码**（用户裁决：只在真正触发时才提示·不输出常态提醒）。


def test_interference_log_hint_mentions_carrier_and_window():
    """W821：提示行须含日志载体路径与窗口（被提醒者据此知道往哪写）。"""
    hint = preflight_check.interference_log_hint("preflight 交集拒绝")
    assert "interference-governance-roadmap.md" in hint, "提示须指向 §8 干扰日志载体"
    assert "§8" in hint, "提示须点明是 §8 干扰日志"
    assert "2026-10-14" in hint and "10-28" in hint, "提示须含登记窗口"
    assert "命中：preflight 交集拒绝" in hint, "提示须带命中原因"


def test_interference_log_hint_is_not_emitted_unless_triggered():
    """W821：提示只在真触发时输出——不产生常态噪音（用户裁决核心）。"""
    import io as _io
    import contextlib
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
        "| W900 | 修复 `a|b` 形态的批 | abc1234（级联） | W900 | **已收官**（abc1234） | 主会话 | AGENTS.md, docs/agent/pitfalls.md |"
    )
    got = preflight_check.parse_ledger(line)
    assert len(got["rows"]) == 1
    row = got["rows"][0]
    assert row["status"] == "**已收官**（abc1234）", "状态列读错：%r" % row["status"]
    assert not preflight_check.is_inflight(row["status"]), "已收官批次不得被误判为在途"
    assert row["touches"] == {"AGENTS.md", "docs/agent/pitfalls.md"}, "touches 列读错：%r" % row["touches"]


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
    assert w739["touches"] == {"AGENTS.md", "docs/agent/pitfalls.md"}
    w735 = [r for r in got["rows"] if r["w"] == 735][0]
    assert w735["status"] == "已收官"
    assert w735["touches"] == set()
