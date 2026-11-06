"""W1142 体积根修回归锁（对抗审查 P2-1·铁律 18-②「无判据的教训=未解决」闭环）。

覆盖三件新机制：
① batch_spec.fi_group_rows —— 阈值边界/无斜杠根级文件保留精确行（P1-3）/分组形态
② archive_segments 体积模式迁后剩余段 ≥20 断言 —— 合成树负样本拦截（P1-1 同族）
③ check_doc_size_budget._fileindex_row_density —— cap 内绿/超限红/边界段
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import archive_segments as arcs  # noqa: E402
import batch_spec  # noqa: E402
import check_doc_size_budget as dsb  # noqa: E402


class TestFiGroupRows:
    """① fi_group_rows 分组原语。"""

    def test_small_rows_passthrough(self):
        rows = ["| a.py | W1 | x |", "| b/c.md | W1 | y |"]
        assert batch_spec.fi_group_rows(rows, "W1") == rows

    def test_big_rows_grouped(self):
        rows = (["| site/data/p%d.html | W9 | 改 |" % i for i in range(150)]
                + ["| site/en/q%d.html | W9 | 改 |" % i for i in range(150)]
                + ["| scripts/tool.py | W9 | 改 |"])
        g = batch_spec.fi_group_rows(rows, "W9")
        assert len(g) == 3
        assert all("件）" in r.split("|")[1] for r in g)

    def test_root_files_keep_exact_rows(self):
        """P1-3 根修：无斜杠根级文件不伪装成目录分组行。"""
        rows = (["| site/data/p%d.html | W9 | 改 |" % i for i in range(200)]
                + ["| AGENTS.md | W9 | 治理 |", "| pytest.ini | W9 | 配置 |"])
        g = batch_spec.fi_group_rows(rows, "W9")
        flat = "\n".join(g)
        assert "AGENTS.md/（1 件）" not in flat, "根级文件不得伪装目录"
        assert "| AGENTS.md | W9 | 治理 |" in g, "根级文件保留精确行"
        assert "| pytest.ini | W9 | 配置 |" in g

    def test_grouped_rows_covers_compatible(self):
        rows = (["| site/data/p%d.html | W9 | 改 |" % i for i in range(200)]
                + ["| AGENTS.md | W9 | 治理 |"])
        g = batch_spec.fi_group_rows(rows, "W9")
        ok, extra = batch_spec.covers(g, ["site/data/p0.html", "AGENTS.md"])
        assert ok and extra == []
        ok2, extra2 = batch_spec.covers(g, ["site/reader/evil.html"])
        assert not ok2 and extra2 == ["site/reader/evil.html"]

    def test_threshold_boundary_201(self):
        """阈值边界：恰 200 行原样、201 行起分组。"""
        rows200 = ["| d/f%d.html | W9 | x |" % i for i in range(200)]
        assert batch_spec.fi_group_rows(rows200, "W9") == rows200
        rows201 = rows200 + ["| d/g.html | W9 | x |"]
        assert len(batch_spec.fi_group_rows(rows201, "W9")) == 1


class TestArchiveKeepFloor:
    """③ 体积模式迁后剩余段 ≥20 断言（monkeypatch 注入合成树·打 move() 真实断言）。"""

    SEG_RE = re.compile(r"^### (W\d+)", re.M)

    def _segments(self, n):
        # file-index 面段标题为 ## 形态（TARGETS 正则 ^## (W\d+)）
        return "".join("## W%d x（t）\n\n| 文件 | W | 说明 |\n|---|---|---|\n| d/f%d | W | x |\n\n"
                       % (1100 - i, i) for i in range(n))

    def _run_move(self, monkeypatch, chunk):
        src = self._segments(30)
        arc = "> 归档时间：2026-01-01\n\n## W900 old\n\n| a | W | x |\n\n"
        monkeypatch.setattr(
            arcs.bc, "load",
            lambda rel: ((src, "\n") if "file-index" in rel else (arc, "\n")))
        try:
            arcs.move("file-index", None, False, "WTEST", max_bytes=10, chunk=chunk)
            return None
        except AssertionError as e:
            return str(e)

    def test_full_migration_blocked(self, monkeypatch):
        """chunk=50 全迁 30 段 → 剩 1 < 20 ⇒ fail-closed 拦截。"""
        msg = self._run_move(monkeypatch, chunk=50)
        assert msg is not None and "保留底线 20" in msg, "负样本未被拦"

    def test_small_migration_passes(self, monkeypatch):
        """正常量级（迁 5 剩 25）不触发断言——上限设为 25 段体积。"""
        src = self._segments(30)
        cap = int(len(src) * 25 / 30) + 10  # 迁出约 5 段后正本即达标
        monkeypatch.setattr(
            arcs.bc, "load",
            lambda rel: ((src, "\n") if "file-index" in rel
                         else ("> 归档时间：2026-01-01\n\n## W900 old\n\n| a | W | x |\n\n", "\n")))
        try:
            arcs.move("file-index", None, False, "WTEST", max_bytes=cap, chunk=5)
            return None
        except AssertionError as e:
            return str(e)


class TestRowDensity:
    """④ file-index 单段行数密度判据。"""

    def test_within_cap_green(self):
        t = "## W1 x\n\n| 文件 | W | 说明 |\n|---|---|---|\n" + "\n".join(
            "| d/f%d.html | W1 | x |" % i for i in range(200)) + "\n"
        assert dsb._fileindex_row_density(t) == []

    def test_over_cap_red(self):
        t = "## W1 x\n\n| 文件 | W | 说明 |\n|---|---|---|\n" + "\n".join(
            "| d/f%d.html | W1 | x |" % i for i in range(201)) + "\n"
        fails = dsb._fileindex_row_density(t)
        assert len(fails) == 1 and "201 行 > 200" in fails[0]

    def test_last_segment_counted(self):
        """边界：末段无后继段标题也要计数。"""
        t = "## W1 x\n\n" + "\n".join("| d/f%d.html | W1 | x |" % i for i in range(201)) + "\n"
        assert dsb._fileindex_row_density(t), "末段超限须被抓"

    def test_grouped_rows_not_counted_as_files(self):
        """分组行本身计入行数——分组后段行数≈目录数，天然绿（语义自洽）。"""
        t = "## W1 x\n\n" + "\n".join(
            "| site/%s/（10 件） | W1 | 分组 |" % d for d in ("data", "en", "reader")) + "\n"
        assert dsb._fileindex_row_density(t) == []


class TestDrawerFixedAtNarrow:
    """⑤ 抽屉 fixed 塌陷回归锁（用户 2026-11-06 窄视口 745 实报·W335 backdrop-filter
    使祖先成为 fixed 包含块 ⇒ 抽屉被压进 144px 顶条）。运行时探针·Playwright 本地站。"""

    def test_drawer_full_height_at_745(self):
        import subprocess
        import time
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        srv = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8791", "--bind", "127.0.0.1"],
            cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.2)
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as pw:
                try:
                    b = pw.chromium.launch()
                except Exception as exc:  # noqa: BLE001
                    pytest.skip("Playwright 浏览器不可用（CI pytest-unit 未装浏览器）：%s" % exc)
                pg = b.new_context(viewport={"width": 745, "height": 957}).new_page()
                pg.goto("http://127.0.0.1:8791/site/index.html", wait_until="load")
                pg.wait_for_timeout(900)
                pg.click(".nav-toggle")
                pg.wait_for_timeout(600)
                r = pg.evaluate("""(() => {
                    const nav = document.querySelector('.topnav nav');
                    const rect = nav.getBoundingClientRect();
                    return {h: rect.height, links: nav.querySelectorAll('a').length};
                })()""")
                b.close()
            assert r["h"] == 957, "抽屉面板须全高（实测 %s）——fixed 被祖先 backdrop-filter 退化" % r["h"]
            assert r["links"] == 8
        finally:
            srv.terminate()
