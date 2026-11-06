"""W1147 探针固化引用锁：四个新脚本（containment_block_scan / fixed_ancestor_probe /
interaction_components / interaction_state_probe）的冒烟与清单完整性（第 42 槽 C1 引用面）。"""
import importlib
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))


class TestContainmentBlockScan:
    """静态扫描探针：脚本级跑通 + 输出面断言。"""

    def test_script_runs_and_reports(self):
        import subprocess
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        r = subprocess.run(
            [sys.executable, os.path.join(root, "scripts", "containment_block_scan.py")],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert r.returncode == 0, r.stdout[-500:] + r.stderr[-300:]
        assert "包含块规则选择器" in r.stdout
        assert "fixed/sticky 规则选择器" in r.stdout

    def test_blocking_re_regex_covers_family(self):
        """特性族完备性：backdrop-filter/transform/filter/perspective/will-change/contain 全在判据。"""
        import containment_block_scan as cbs
        src = open(cbs.__file__, encoding="utf-8").read()
        for feat in ("backdrop-filter", "transform", "filter", "perspective",
                     "will-change", "contain"):
            assert feat in src, "判据缺特性：%s" % feat


class TestFixedAncestorProbe:
    """运行时退化探针：可导入 + 判据串在位（运行时全量跑由 test_w1142 抽屉锁覆盖）。"""

    def test_importable_with_judgement(self):
        import fixed_ancestor_probe as fap
        src = open(fap.__file__, encoding="utf-8").read()
        assert "offsetParent" in src
        assert "position === 'fixed'" in src or "position:fixed" in src


class TestInteractionComponents:
    """12 类开合组件清单：结构完整 + 代表页在盘。"""

    def test_components_shape(self):
        import interaction_components as ic
        assert len(ic.COMPONENTS) == 12, "清单须 12 类（现 %d）" % len(ic.COMPONENTS)
        for row in ic.COMPONENTS:
            assert len(row) == 5, "行须五元组：%r" % (row,)
            comp, page, entry, open_sel, wl = row
            assert comp and page
        kinds = {r[0] for r in ic.COMPONENTS}
        assert kinds == {
            "nav-drawer", "filter-tab", "search-clear", "chart-tooltip", "drill-layer",
            "ask-chip", "theme-toggle", "danmaku-hover", "cite-copy", "back-to-top",
            "table-sticky", "tag-cloud-hover"}, "组件类集合漂移须同步探针与文档"

    def test_representative_pages_exist(self):
        import interaction_components as ic
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        pages = {r[1] for r in ic.COMPONENTS}
        for pg in pages:
            assert os.path.isfile(os.path.join(root, "site", pg)), "代表页缺盘：%s" % pg


class TestInteractionStateProbe:
    """交互后态探针：基线报告（tmpe/w1147）主断言复核——退化 0 / 残留 0。"""

    def test_baseline_report_clean(self):
        rep = "tmpe/w1147/interaction_report.json"
        if not os.path.isfile(rep):
            import subprocess
            root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            probe = os.path.join(root, "scripts", "interaction_state_probe.py")
            subprocess.run([sys.executable, probe, "--out", rep], capture_output=True,
                           text=True, encoding="utf-8", timeout=300)
        r = json.load(open(rep, encoding="utf-8"))
        assert len(r) == 12, "报告须覆盖 12 组件（现 %d）" % len(r)
        for k, v in r.items():
            assert not v.get("degraded"), "%s 存在 fixed 退化：%r" % (k, v.get("degraded"))
            assert not v.get("leftover"), "%s 存在 .open 残留：%r" % (k, v.get("leftover"))
