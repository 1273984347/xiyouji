r"""W1332 专项测试：L-13 暗色对比度判据 + L-14 公共层补丁 + L-15 视觉零散

## 为什么测

本批三类改动都属「静默失效」高发面：
- 公共层 summary 屏蔽若被后续换肤覆盖 ⇒ reader 635 页双三角复发；
- --shadow-2 令牌若只在亮态补 ⇒ 暗色浮动钮回退到硬编码浅阴影；
- 页面私有「深底浅字」若回退到 var(--paper-warm) ⇒ 暗色下表头/tooltip 重新不可读；
- 暗色探针若失去 class/渐变过滤口径 ⇒ 误报重新淹没真缺陷。
本文件把「规则在位 + 令牌两态 + 批量修复幂等 + 探针判据负样本」钉成可回归判据。

## 覆盖判据

  G1 system.css 全局 summary 原生 marker 屏蔽在位
  G2 tokens.css --shadow-2 亮/暗两态各有定义
  G3 index.html aria-current + 非衬线按钮
  G4 两 viewer 已接 system.css
  G5 深底块不再使用 paper-warm/paper/surface-canvas 作文字色（抽样）
  G6 修复器纯函数幂等 + 跳过 INLINED CSS 副本
  G7 暗色探针 grade 负样本（th 不可读判 FAIL / 渐变背景降级 / 无 class 形状豁免）
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
# W1333：本批脚本按「脚本三档归位」迁入归档（第 42 槽 C4 要求历史批脚本不得滞留 scripts/ 根）
BATCH1332 = ROOT / "archive" / "scripts" / "batches" / "w1332"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(BATCH1332))

import _w1332_dark_contrast_probe as probe  # noqa: E402
import _w1332_dark_text_fix as fix  # noqa: E402


def test_system_css_summary_marker_masked():
    css = (ROOT / "site/system.css").read_text(encoding="utf-8")
    assert "summary::-webkit-details-marker" in css
    assert re.search(r"summary\s*\{\s*list-style:\s*none", css)


def test_tokens_shadow2_both_themes():
    css = (ROOT / "site/tokens.css").read_text(encoding="utf-8")
    assert css.count("--shadow-2:") >= 2, "亮/暗两态都应定义 --shadow-2"


def test_index_nav_and_button():
    html = (ROOT / "site/index.html").read_text(encoding="utf-8")
    assert 'class="nav-brand" href="index.html" aria-current="page"' in html
    m = re.search(r"\.ask-form button\s*\{[^}]*\}", html)
    assert m and "var(--font-serif)" not in m.group(0)
    assert "var(--font-sans)" in m.group(0)


def test_viewers_on_public_shell():
    for rel in ("site/rum-viewer.html", "site/visit-viewer.html"):
        html = (ROOT / rel).read_text(encoding="utf-8")
        assert 'href="system.css"' in html, rel


def test_dark_text_fix_samples():
    """抽样三类曾命中页：表头 / tooltip / 图表 tip。"""
    pages = ["site/data/cave-estate.html", "site/data/game-webnovel.html", "site/data/chart-design.html"]
    for rel in pages:
        html = (ROOT / rel).read_text(encoding="utf-8")
        new, n = fix.process(html)
        # 已修复态：再跑一次应零改动（幂等）
        assert n == 0, rel
        # 深底块内不应再有 paper-warm 作文字色
        for m in re.finditer(r"\{[^{}]*\}", html):
            blk = m.group(0)
            if "background: var(--dark)" in blk:
                assert "color: var(--paper-warm)" not in blk, rel


def test_fix_process_idempotent_and_skips_inlined():
    bad = "<style>.x{background:var(--dark);color:var(--paper-warm);}</style>"
    new, n = fix.process(bad)
    assert n == 1 and "--dark-text" in new
    again, n2 = fix.process(new)
    assert n2 == 0 and again == new
    inlined = "<!-- INLINED CSS x --><style>.x{background:var(--dark);color:var(--paper-warm);}</style>"
    _, n3 = fix.process(inlined)
    assert n3 == 0


def test_probe_grade_rules():
    def rec(html_text=None, shapes=None):
        return {"htmlText": html_text or [], "shapes": shapes or []}

    ok = rec()
    assert probe.grade(ok)[0] == "OK"
    th = rec(html_text=[{"cr": 1.11, "txt": "回目", "cls": "sortable", "tag": "th", "uncertain": False}])
    g, why = probe.grade(th)
    assert g == "FAIL" and any("HTML 文字" in w for w in why)
    unc = rec(html_text=[{"cr": 1.57, "txt": "Dashboard", "cls": "", "tag": "a", "uncertain": True}])
    assert probe.grade(unc)[0] == "OK"
    shape = rec(shapes=[{"cr": 1.02, "cls": "bar", "tag": "rect", "area": 500}])
    assert probe.grade(shape)[0] == "FAIL"


def test_cli_help_smoke():
    for name in ("_w1332_dark_contrast_probe.py", "_w1332_dark_text_fix.py"):
        r = subprocess.run([sys.executable, str(BATCH1332 / name), "--help"],
                           capture_output=True, text=True, timeout=60)
        assert r.returncode == 0, name
