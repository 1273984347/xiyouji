"""W1342 专项测试：scripts/check_chart_data.py 的 R4（族注册）与 R5（雷达规模）

## 为什么测这个脚本

W1341 图表选型审查实证：雷达族 27 页在用，却不在 DESIGN §4B 九族选型表内
⇒ 该族无数据形态约束、无禁用条件、无窄屏降级、**零机器判据**。R4/R5 就是把这
一发现转成的机器判据；判据本身的失效形态是「静默放行」（表外族不报 / 超限不报 /
基线被当成无底洞），因此必须自证。

## 覆盖判据

  P1 现网实跑：退出码 0 且汇总行「FAIL 0 页」（干净态不假红）
  P2 spec-check 与常量同源：DESIGN 实表单行数 == EXPECT_SPEC_ROWS，且缺行/空格必红
  P3 R4 表外族必检：未注册族 ⇒ 命中；已注册 ⇒ 放行；§4B 缺章 ⇒ fail-closed
  P4 R5 规模判据：缺声明 / 轴超限 / 系列超限 必检；合规声明放行；基线内豁免
  P5 self-test：脚本内置 10 例全过
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_chart_data as ccd  # noqa: E402

GATE = SCRIPTS / "check_chart_data.py"

RADAR_HTML = '<html><body><svg id="chart-radar"></svg></body></html>'
META_OK = '<!-- chart-radar-meta: axes=5 series=3 -->'
META_OVER = '<!-- chart-radar-meta: axes=12 series=9 -->'


def _run(*args, timeout=180):
    return subprocess.run(
        [sys.executable, str(GATE), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(ROOT),
    )


def _design(tmp_path, body):
    p = tmp_path / "design.md"
    p.write_text(body, encoding="utf-8")
    return str(p)


def test_p1_live_tree_passes():
    """P1：现网实跑 0 FAIL（R4/R5 不漏判也不假红）。"""
    r = _run()
    assert r.returncode == 0, "图表自洽门禁在现网树上 FAIL：\n%s" % r.stdout[-1500:]
    assert "FAIL 0 页" in r.stdout, "缺 0 FAIL 汇总行（疑似未真正执行）：\n%s" % r.stdout[-800:]
    expect = "基线豁免 %d 页" % len(ccd.load_baseline())
    assert expect in r.stdout, "基线豁免页数与基线文件不符（期望「%s」）：\n%s" % (expect, r.stdout[-800:])


def test_p2_spec_rows_match_constant():
    """P2：§4B 实表行数 == EXPECT_SPEC_ROWS（改表不改常量 ⇒ 这里红）。"""
    seg = ccd.design_segment(str(ROOT / "DESIGN.md"))
    assert seg is not None, "DESIGN.md 缺 §4B 章"
    rows = [row for row in seg.split("\n")
            if row.startswith("| ") and "数据形态约束" not in row and not row.startswith("|---")]
    assert len(rows) == ccd.EXPECT_SPEC_ROWS, (
        "§4B 实表 %d 行 ≠ EXPECT_SPEC_ROWS=%d" % (len(rows), ccd.EXPECT_SPEC_ROWS)
    )
    assert ccd.EXPECT_SPEC_ROWS == 10, "W1342 起雷达族已入表，预期 10 族"
    assert _run("--spec-check", str(ROOT / "DESIGN.md")).returncode == 0


def test_p2_spec_check_detects_row_count_and_empty_cell(tmp_path):
    """P2 负样本：行数不符 / 有空单元格 必红。"""
    nine = "## 4B. 图表选型与数据契约\n\n| a | b |\n|---|---|\n" + "| 1 | 2 |\n" * 8 + "\n## 4C. x\n"
    r = _run("--spec-check", _design(tmp_path, nine))
    assert r.returncode == 1, "行数不足未判红：\n%s" % r.stdout
    empty_cell = ("## 4B. 图表选型与数据契约\n\n| a | b |\n|---|---|\n"
                  + "| 1 | 2 |\n" * 8 + "|  | 3 |\n" + "\n## 4C. x\n")
    assert _run("--spec-check", _design(tmp_path, empty_cell)).returncode == 1, "空单元格未判红"


def test_p3_family_registry(tmp_path):
    """P3：表外族必检；已注册放行；§4B 缺章 fail-closed。"""
    no_radar = _design(tmp_path, "## 4B. 图表选型与数据契约\n\n| 桑基图 | 折线图 |\n\n## 4C. x\n")
    hits = ccd.family_registry_fails([RADAR_HTML], no_radar)
    assert [f for f, _n in hits] == ["雷达"], "表外族未检出：%r" % (hits,)

    with_radar = _design(tmp_path, "## 4B. 图表选型与数据契约\n\n| 雷达图 | 桑基图 |\n\n## 4C. x\n")
    assert ccd.family_registry_fails([RADAR_HTML], with_radar) == [], "已注册族被误报"

    missing = _design(tmp_path, "# 无选型章\n")
    assert ccd.family_registry_fails([RADAR_HTML], missing), "§4B 缺章应 fail-closed"


def test_p4_radar_scale():
    """P4：R5 四态——合规放行 / 缺声明检出 / 超限检出 / 基线豁免。"""
    rel = "site/data/x.html"
    assert ccd.radar_scale_fails(rel, RADAR_HTML + META_OK, set()) == [], "合规声明被误报"

    fails = ccd.radar_scale_fails(rel, RADAR_HTML, set())
    assert fails and fails[0].startswith("R5"), "缺规模声明未检出：%r" % (fails,)

    over = ccd.radar_scale_fails(rel, RADAR_HTML + META_OVER, set())
    assert len(over) == 2, "轴/系列双超应报两条：%r" % (over,)

    assert ccd.radar_scale_fails(rel, RADAR_HTML + META_OVER, {rel}) == [], "基线内页面应豁免"
    assert ccd.radar_scale_fails(rel, "<html><body><svg id='c'></svg></body></html>",
                                 set()) == [], "非雷达页不应受 R5 约束"


def test_p5_baseline_file_shape():
    """P5：基线可解析、路径合法、页面存在、无重复，且每行仍对应带雷达签名的页面（防陈旧豁免）。

    条数不写死：W1343-W1346 把存量逐页改造后基线已自然清零，任何固定条数都会变成
    「改页面就要改测试」的假红源；真正的判据是「基线与现网一致」。
    """
    lines = ccd.load_baseline()
    assert len(set(lines)) == len(lines), "基线含重复路径"
    assert all(x.startswith("site/data/") and x.endswith(".html") for x in lines), "基线含非法路径"
    assert os_path_exists(lines), "基线含磁盘上不存在的页面"
    stale = [p for p in lines
             if not ccd.RADAR_SIG.search((ROOT / p).read_text(encoding="utf-8"))]
    assert not stale, "基线含已无雷达签名的页面（应删行）：%r" % (stale,)


def os_path_exists(lines):
    return all((ROOT / p).exists() for p in lines)


def test_p6_self_test_passes():
    """P6：脚本内置 10 例自检全过。"""
    r = _run("--self-test")
    assert r.returncode == 0 and "self-test: PASS" in r.stdout, r.stdout[-800:]
