"""W1124 单元测试 · 收官链接入幂等段重建 + 里程碑滚动幂等守卫 + 布局门禁 worktree 形态适配。

R-A（重建入口收进收官链）：rebuild_section.py 此前是**独立入口**（W1120 建）⇒ 段内容与
spec 不一致时只能人工想起单独跑它 ⇒ 「改完段内容后重建」这一步在流程里是断的 ⇒
段与 spec 长期漂移。W1124 把它接入收官链主链，并锁「rebuild 必须排在 precheck 之前」
（precheck 是 fail-closed 中止 ⇒ 修复步排其后即死路径·W1117 同族教训）。

R-C（滚动幂等守卫下沉到函数内）：守卫此前只在调用点（插入路径）生效 ⇒ 单独重跑滚动逻辑
仍会再淘汰一块 ⇒ 信息丢失且零红灯。

布局门禁适配：git worktree 形态下根目录 .git 是**文件**（指向主仓的指针）⇒ 第 52 门禁
原实现把它当「未声明文件」判红 ⇒ worktree 形态不可用 ⇒ 而隔离 worktree 是并行协作的
默认前提（AGENTS 铁律 24）⇒ scan 层排除 .git，judge 层判据强度不降。

运行：py -3 -m pytest tests/unit/test_w1124_closeout_rebuild.py -v
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import backfill_changelog as bf  # noqa: E402
import batch_cascade as bc  # noqa: E402
import batch_closeout as bcl  # noqa: E402
import check_repo_layout as layout  # noqa: E402
import rebuild_section as rs  # noqa: E402

SPEC = {
    "batch": "W1124",
    "date": "2026-11-04",
    "title": "W1124 测试批",
    "desc": "测试描述",
    "head_entry": "2026-11-04（W1124 测试批）",
    "head_sentence": "测试描述",
    "changelog_body": "\n\n**本批要点**：测试\n\n",
    "milestone_block": "- **W1124 测试批**：内容",
    "agents_note": "2026-11-04（W1124）测试条目",
    "file_index_rows": ["| a.py | W1124 | 本批工具/产物 |"],
}

CL_WITH_BATCH = (
    "# 更新日志\n\n"
    "### W1124（2026-11-04）：测试批\n\n**本批要点**：测试\n\n\n"
    "### W1123（2026-11-04）：旧标题\n\n旧段正文\n"
)


# ---------------- 收官链步骤顺序 ----------------


def test_closeout_steps_contain_rebuild():
    """正样本：收官链含 rebuild 步（R-A 的落点）。"""
    assert "rebuild" in bcl.step_order()


def test_closeout_rebuild_step_precedes_precheck():
    """顺序锁：rebuild 必须排在 precheck 之前。

    病根（W1117 同族）：precheck 是 fail-closed 中止 ⇒ 修复步排其后 ⇒ 在最需要它时不可达。
    """
    order = bcl.step_order()
    assert order.index("rebuild") < order.index("precheck")


def test_closeout_rebuild_step_precedes_archive_only_by_design():
    """顺序锁：archive 仍是首步（腾窗前置承诺不破）。"""
    assert bcl.step_order()[0] == "archive"


def test_closeout_steps_keep_csp_last_two():
    """W1112 既有承诺不破：csp/cspcheck 仍为末两步。"""
    assert bcl.step_order()[-2:] == ["csp", "cspcheck"]


# ---------------- 幂等段重建（纯函数层） ----------------


def test_rebuild_changelog_is_zero_change_when_identical():
    """正样本：段已立且内容一致 ⇒ 零变化（幂等·可重复执行）。"""
    block = bf.changelog_block(SPEC)
    out, changed, action = rs.rebuild_changelog(CL_WITH_BATCH, "W1124", block)
    assert changed is False
    assert "零变化" in action
    assert out == CL_WITH_BATCH


def test_rebuild_changelog_replaces_stale_segment():
    """正样本：段内容与 spec 不一致 ⇒ 就地重建该段（只动本批段）。"""
    stale = CL_WITH_BATCH.replace("**本批要点**：测试", "**本批要点**：旧内容")
    block = bf.changelog_block(SPEC)
    out, changed, action = rs.rebuild_changelog(stale, "W1124", block)
    assert changed is True
    assert "就地重建" in action
    assert "**本批要点**：测试" in out
    assert "**本批要点**：旧内容" not in out


def test_rebuild_keeps_history_segments_unchanged():
    """负样本：重建不得改写历史段（逐段比对断言·由 rebuild_section 自带）。"""
    stale = CL_WITH_BATCH.replace("**本批要点**：测试", "**本批要点**：旧内容")
    block = bf.changelog_block(SPEC)
    out, _changed, _action = rs.rebuild_changelog(stale, "W1124", block)
    ok, diff = rs.history_unchanged(stale, out, "W1124", "changelog")
    assert ok, "历史段被改写：%s" % diff


def test_rebuild_second_run_is_zero_change():
    """正样本：重建一次后再跑 ⇒ 零变化（幂等核心）。"""
    stale = CL_WITH_BATCH.replace("**本批要点**：测试", "**本批要点**：旧内容")
    block = bf.changelog_block(SPEC)
    once, _c1, _a1 = rs.rebuild_changelog(stale, "W1124", block)
    twice, changed2, _a2 = rs.rebuild_changelog(once, "W1124", block)
    assert changed2 is False
    assert twice == once


# ---------------- 里程碑滚动幂等守卫 ----------------

HANDOVER_ROLL = (
    "## 一、当前进度（W1123 新描述；更早批次详见 CHANGELOG.md）\n"
    "- **W1123 新批次**：新内容\n"
    "- **W1120 旧批次**：旧内容\n"
    "> 历史概要（W1120 及更早）的详细记录见 CHANGELOG.md\n\n"
    "## 二、下一步方向候选清单\n\n正文\n"
)


class _Ctx:
    def __init__(self, batch):
        self.batch = batch
        self.cl_src = "### W1120（2026-11-01）：旧标题\n\n旧段\n"


def test_rotate_oldest_is_skipped_when_batch_block_already_present():
    """正样本（R-C）：本批块已在链上 ⇒ 视为已滚动过 ⇒ 零变化。

    病根：守卫此前只在调用点生效 ⇒ 单独重跑滚动逻辑仍会再淘汰一块（信息丢失·零红灯）。
    """
    out = bc._handover_rotate_oldest(HANDOVER_ROLL, _Ctx("W1123"), "\n", 0)
    assert out == HANDOVER_ROLL, "本批块已存在却仍执行了滚动淘汰"


def test_rotate_oldest_still_rolls_when_batch_block_absent():
    """对照组：守卫不得变成「一律跳过」——本批块不在链上时滚动照常执行。"""
    out = bc._handover_rotate_oldest(HANDOVER_ROLL, _Ctx("W1124"), "\n", 0)
    assert out != HANDOVER_ROLL, "本批块不在链上时滚动被错误跳过"
    assert "旧内容" not in out, "最老块未被淘汰"
    assert "W1120 及更早" not in out, "历史概要指针未随淘汰同步"


# ---------------- 布局门禁：worktree 形态适配 ----------------


def test_layout_scan_excludes_git_pointer_file(tmp_path, monkeypatch):
    """正样本：worktree 形态（根目录 .git 是文件）⇒ 不计入根文件清单。"""
    (tmp_path / ".git").write_text("gitdir: D:/repo/.git/worktrees/x", encoding="utf-8")
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    monkeypatch.setattr(layout, "ROOT", str(tmp_path))
    monkeypatch.setattr(layout, "_ignored", lambda names: set())
    files, dirs = layout.scan()
    assert ".git" not in files
    assert "README.md" in files


def test_layout_judge_still_fails_on_other_undeclared_files():
    """负样本：judge 层判据强度不降——任意未声明文件仍判红（排除只发生在 scan 层）。"""
    ok, extra_files, _dirs, _missing = layout.judge([".git", "stray.txt"], [])
    assert ok is False
    assert "stray.txt" in extra_files
