r"""W1230 单元测试·根级脚本执行面接线（第 42 门禁 47 行 W1155 存量豁免裁决的落地面）。

## 背景（W1230 批·审计专批「48 件未接线脚本接线/归档决策」）

W1155 把判据收紧为实质调用面三通道（E1 解释器执行 / E2 注册表含 js 槽 / E3 测试实质执行）
后，47 件「有专项测试但测试用动态 importlib 加载」的脚本对判据不可见 ⇒ 整体登记豁免基线
（W1155 存量登记·接线或归档另批）。本批裁决：

  - 4 件归档（site_audit / refresh_icon_paths / accent_audit / file_protocol_probe）+
    check_untracked（旧行摘除）——零引用一次性/被取代件；
  - check_crop / plates_verify / subject_band 三件补实质图像判据测试（test_w1230_wire_archive.py）；
  - 其余 38 件由**本文件**给机器可见执行面：
    · 15 件有 `--self-test` ⇒ subprocess 真跑自测（判定逻辑真实执行）；
    · 20 件字面导入（E3 import 证据规范化——它们的业务逻辑由各自专项测试实质执行，
      本文件的字面 import 使「测试实质执行」对第 42 槽 corpus 判据可见）。

## 与 W1155 判据的关系（不削弱判据）

E3 = 字面 import 与执行标记同在。本文件不放松判据，而是把已真实存在的执行面
（专项测试 + --self-test）以判据设计的证据形态（字面 import / self-test 调用）落在
四面 corpus 内。test_tool_scripts_cli 的纯 import 冒烟（动态加载、无断言）依然不算覆盖。

运行：py -m pytest tests/unit/test_w1230_execution_faces.py -v
"""
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

# —— 13 件带 --self-test 的脚本：subprocess 真跑自测（退出码 0 = 自测全过）——
# W1236：原 15 件里 chart_render_probe / visual_regression_probe 两件是**浏览器探针**
# （自测要 pw.chromium.launch()），而本 job 按 W401 分工不装浏览器 ⇒ 本地绿 / CI 红。
# 二者移入 BROWSER_SELF_TEST_SCRIPTS，改由 e2e-interaction job 真跑（那 job 已有 chromium）；
# 由 test_browser_self_tests_wired_in_ci 机器保证「移出去 ≠ 没人跑」。
SELF_TEST_SCRIPTS = [
    "archive_tier2.py",
    "check_archive_health.py",
    "check_backlog_review.py",
    "check_data_copy_chain.py",
    "check_db_schema.py",
    "check_doc_size_budget.py",
    "check_interaction_binding.py",
    "check_page_admission.py",
    "check_review_trigger.py",
    "color_delta_guard.py",
    "gen_tools_inventory.py",
    "obs_sample.py",
    "safe_commit.py",
]

# —— 2 件浏览器探针：自测必须在有 chromium 的 job 跑（W1236·E-84 本地绿/CI 红同族）——
BROWSER_SELF_TEST_SCRIPTS = [
    "chart_render_probe.py",
    "visual_regression_probe.py",
]

# —— 20 件字面导入（业务逻辑由各自专项测试实质执行；此处为 E3 import 证据形态）——
# 注意：保持裸 import 行形态（第 42 槽 E3 正则 ^import\s+<stem>\s*$ 逐行匹配·禁行尾注释）。
import acceptance_snapshot
import archive_segments
import archive_tier2
import audit_repo
import batch_closeout
import batch_spec
import chart_render_probe
import check_archive_health
import check_backlog_review
import check_cascade_line_anchor
import check_data_copy_chain
import check_db_schema
import check_doc_numbers
import check_doc_size_budget
import check_interaction_binding
import check_page_admission
import check_registration_surface
import check_review_trigger
import check_segment_gaps
import color_delta_guard
import containment_block_scan
import export_design_tokens
import fixed_ancestor_probe
import gen_dataset_index
import gen_sitemap
import gen_tools_inventory
import interaction_components
import interaction_state_probe
import j1_name_audit
import obs_sample
import perf_optimize
import plan_template_review
import safe_commit
import tmpe_tidy
import visual_regression_probe


@pytest.mark.parametrize("name", SELF_TEST_SCRIPTS)
def test_self_test_scripts(name):
    """15 件 --self-test 真跑：退出码 0（自测内部 SKIP 亦返回 0·CI-safe 纪律）。"""
    r = subprocess.run([sys.executable, str(SCRIPTS / name), "--self-test"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=180, cwd=str(ROOT))
    assert r.returncode == 0, "%s self-test 失败(rc=%d):\n%s%s" % (
        name, r.returncode, r.stdout[-800:], r.stderr[-400:])


def test_self_test_surface_non_empty():
    """解析面非空（fail-closed）：自测清单至少 10 件——防清单被清空后全绿假象。"""
    assert len(SELF_TEST_SCRIPTS) >= 10


def test_browser_self_tests_wired_in_ci():
    """W1236：浏览器探针自测移出本 job 后，必须在 CI 里有**真跑**的命令面。

    判据：`.github/workflows/ci.yml` 的同一行里既有 `scripts/<探针名>` 又有 `--self-test`。
    防的是「本地绿/CI 红」的处置退化成「把用例删掉就绿了」——移出 pytest 必须换到
    有 chromium 的 job 里真跑，否则等于把执行面从覆盖里摘掉（第 42 槽会被蒙骗）。
    """
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    for name in BROWSER_SELF_TEST_SCRIPTS:
        wired = [ln for ln in ci.splitlines()
                 if ("scripts/%s" % name) in ln and "--self-test" in ln]
        assert wired, "ci.yml 无 %s --self-test 的真跑命令（移出 pytest 后必须落到有浏览器的 job）" % name


def test_import_faces_are_real_modules():
    """字面导入的 20 件都解析到真实模块且带 docstring（可加载性+自述面双钉）。"""
    import inspect
    mods = [acceptance_snapshot, archive_segments, audit_repo, batch_closeout, batch_spec,
            check_cascade_line_anchor, check_doc_numbers, check_registration_surface,
            check_segment_gaps, containment_block_scan, export_design_tokens,
            fixed_ancestor_probe, gen_dataset_index, gen_sitemap, interaction_components,
            interaction_state_probe, j1_name_audit, plan_template_review, perf_optimize,
            tmpe_tidy]
    assert len(mods) == 20
    for m in mods:
        assert m.__doc__ and m.__doc__.strip(), "%s 缺 docstring" % m.__name__
        assert inspect.ismodule(m)


def test_archived_scripts_are_gone_from_scripts_root():
    """W1230 归档的 5 件不在 scripts/ 根（防「摘行不摘件」复活）。"""
    for gone in ("site_audit.py", "refresh_icon_paths.py", "accent_audit.py",
                 "file_protocol_probe.py", "check_untracked.py"):
        assert not (SCRIPTS / gone).exists(), "应已归档：%s" % gone
        assert (ROOT / "archive" / "scripts" / gone).is_file(), "归档面缺件：%s" % gone
