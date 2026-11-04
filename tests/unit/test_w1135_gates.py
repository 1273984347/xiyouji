"""W1135 三门禁槽的负样本自证单测（注入违规 ⇒ 退出码必须判红）。

被测门禁（W1135 批新增的三槽；判定口径/阈值/状态集合/输出文案不得改动）
--------------------------------------------------------------------
  M1 scripts/check_motion_guard.py            动效守卫覆盖率（d3 页 .duration/.delay 实参形态）
  M2 scripts/check_design_asset_manifest.py   assets/design 清单对拍（声明 vs 磁盘）
  M3 scripts/check_tooltip_spacing.py         tooltip 多行间距（运行层 · playwright · 亮/暗双主题）

三脚本共有约定：退出码 0 = 通过 / 1 = 判红 / 2 = 基础设施缺失（fail-closed）。

自证逻辑
--------
门禁脚本自身若失效（扫错目录 / 分类口径放宽 / 异常时静默放过），防护面会静默归零。
故每个槽都必须能证明「它真会拦」：
  · 负样本：注入**该判据本该拦住**的真实违规形态 ⇒ 退出码必须精确 == 1；
  · 并显式断言 != 2（2 = 基础设施缺失，不算判红成功）；
  · 再断言输出含该判据的专属 FAIL 文案（防「脚本崩了也 exit 1」的假绿）；
  · 正样本：同一夹具去掉注入 ⇒ 退出码必须 == 0（防「红得毫无道理」也算通过）。

隔离
----
临时件只落 pytest 的 tmp_path：门禁脚本**复制**到 tmp_path/scripts/（脚本的扫描根
ROOT 由 __file__ 推导 ⇒ 复制后 ROOT/SITE/BASE 自动指向 tmp_path），页面/清单夹具
也只写 tmp_path ⇒ 仓库内目录零写入、用例互不污染、可重复。

浏览器依赖
----------
M3 是运行层判据（playwright + chromium）。本机 chromium 可用 ⇒ 真跑用例实跑断言；
若运行环境无浏览器（脚本语义 = 退出码 2 基础设施缺失）⇒ 真跑用例 skip，
而**判红鉴别力由不依赖浏览器的 stubbed-probe 用例承担**：把假 CSSOM 读数注入
probe ⇒ 走真实 main() 判定路径 ⇒ 拿到真实进程退出码（精确断言 1 / 0，不 skip）。
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"

MOTION_GATE = SCRIPTS / "check_motion_guard.py"
MANIFEST_GATE = SCRIPTS / "check_design_asset_manifest.py"
TOOLTIP_GATE = SCRIPTS / "check_tooltip_spacing.py"

TOOLTIP_PAGES = (
    "data/heaven-power-network.html",
    "data/monster-hierarchy-network.html",
    "data/underworld-power-network.html",
)

BROWSER_SKIP_REASON = (
    "浏览器依赖不可用（脚本语义 = 退出码 2 基础设施缺失）——"
    "判红鉴别力由 test_tooltip_stubbed_probe_* 用例承担（退出码精确断言，不 skip）"
)


# ---------------------------------------------------------------------------
# 通用夹具/断言工具
# ---------------------------------------------------------------------------

def _stage_gate(tmp_path, src):
    """把门禁脚本复制到 tmp_path/scripts/ ⇒ 该副本的 ROOT == tmp_path（扫描根随之改道）。"""
    dst_dir = tmp_path / "scripts"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    shutil.copy2(src, dst)
    return dst


def _run(script, *args, cwd, timeout=300):
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(cwd),
    )


def _assert_red(result, must_contain, what):
    """负样本统一断言：退出码精确 == 1（判红）+ != 2（基础设施缺失）+ 专属 FAIL 文案命中。"""
    out = result.stdout + result.stderr
    assert "Traceback" not in out, "%s：脚本报异常（exit 1 会假绿）：\n%s" % (what, out[-800:])
    assert result.returncode == 1, "%s：期望判红退出码 1，实际 %d：\n%s" % (what, result.returncode, out[-800:])
    assert result.returncode != 2, "%s：退出码 2 = 基础设施缺失，不算判红成功" % what
    for token in must_contain:
        assert token in result.stdout, "%s：输出缺预期 FAIL 文案 %r：\n%s" % (what, token, result.stdout[-800:])


def _assert_green(result, what):
    """正样本统一断言：退出码 == 0 + 汇总行 0 FAIL（证明判据真跑过而不是静默空转）。"""
    out = result.stdout + result.stderr
    assert "Traceback" not in out, "%s：脚本报异常：\n%s" % (what, out[-800:])
    assert result.returncode == 0, "%s：期望通过退出码 0，实际 %d：\n%s" % (what, result.returncode, out[-800:])
    assert "0 FAIL" in result.stdout, "%s：缺 0 FAIL 汇总行（疑似未真正执行）：\n%s" % (what, result.stdout[-800:])


# ---------------------------------------------------------------------------
# M1 动效守卫覆盖率
# ---------------------------------------------------------------------------

MOTION_CLEAN_MOYUN = """<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>W1135 动效守卫夹具</title></head>
<body>
<script>
var MOYUN_RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
d3.selectAll('.bar').transition().duration(MOYUN_RM ? 0 : 600);
d3.selectAll('.bar').transition().delay(MOYUN_RM ? 0 : 1500 + i * 200);
</script>
</body>
</html>
"""

MOTION_CLEAN_REDUCE_MOTION = """<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>W1135 动效守卫夹具</title></head>
<body>
<script>
const REDUCE_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
d3.selectAll('.bar').transition().duration(REDUCE_MOTION ? 0 : 800);
</script>
</body>
</html>
"""

MOTION_BARE_DURATION = """<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>W1135 动效守卫负样本</title></head>
<body>
<script>
var MOYUN_RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
d3.selectAll('.bar').transition().duration(600);
</script>
</body>
</html>
"""

MOTION_EXPR_DELAY = """<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>W1135 动效守卫负样本</title></head>
<body>
<script>
var MOYUN_RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
d3.selectAll('.bar').transition().delay(1500 + i * 200);
</script>
</body>
</html>
"""

MOTION_NO_GUARD_DECL = """<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>W1135 动效守卫负样本</title></head>
<body>
<script>
d3.selectAll('.bar').transition().duration(MOYUN_RM ? 0 : 600);
</script>
</body>
</html>
"""


def _write_motion_page(tmp_path, html, name="fixture.html"):
    site = tmp_path / "site"
    site.mkdir(parents=True, exist_ok=True)
    (site / name).write_text(html, encoding="utf-8", newline="\n")


def test_motion_guard_positive_guarded_calls_exit_0(tmp_path):
    """M1 正样本：套守卫的实参（MOYUN_RM / REDUCE_MOTION 两命名都要被认）⇒ 退出码 0。"""
    gate = _stage_gate(tmp_path, MOTION_GATE)

    _write_motion_page(tmp_path, MOTION_CLEAN_MOYUN, "clean-moyun.html")
    _assert_green(_run(gate, cwd=tmp_path), "M1 正样本（MOYUN_RM 守卫）")

    _write_motion_page(tmp_path, MOTION_CLEAN_REDUCE_MOTION, "clean-reduce-motion.html")
    _assert_green(_run(gate, cwd=tmp_path), "M1 正样本（REDUCE_MOTION 守卫）")


def test_motion_guard_negative_bare_duration_exit_1(tmp_path):
    """M1 负样本：裸数字实参 .duration(600) ⇒ 判红（退出码 1）。"""
    gate = _stage_gate(tmp_path, MOTION_GATE)
    _write_motion_page(tmp_path, MOTION_BARE_DURATION)

    _assert_red(
        _run(gate, cwd=tmp_path),
        ["未套守卫的 BARE", ".duration(600)"],
        "M1 负样本（裸数字实参）",
    )


def test_motion_guard_negative_expr_delay_exit_1(tmp_path):
    """M1 负样本：未套守卫的表达式实参 .delay(1500 + i * 200) ⇒ 判红（退出码 1）。"""
    gate = _stage_gate(tmp_path, MOTION_GATE)
    _write_motion_page(tmp_path, MOTION_EXPR_DELAY)

    _assert_red(
        _run(gate, cwd=tmp_path),
        ["未套守卫的 EXPR", ".delay(1500 + i * 200)"],
        "M1 负样本（表达式实参）",
    )


def test_motion_guard_negative_missing_guard_declaration_exit_1(tmp_path):
    """M1 负样本：用了守卫变量却未声明 ⇒ 判红（退出码 1）。"""
    gate = _stage_gate(tmp_path, MOTION_GATE)
    _write_motion_page(tmp_path, MOTION_NO_GUARD_DECL)

    _assert_red(
        _run(gate, cwd=tmp_path),
        ["d3 页无守卫声明"],
        "M1 负样本（缺守卫声明）",
    )


# ---------------------------------------------------------------------------
# W1136（CodeQL bad-html-filtering-regexp 根修·E-194）：HTML 标签名/属性名大小写不敏感
# ⇒ 过滤型正则必须大小写不敏感。以下两例把该盲区钉死：
#   · 大写 <SCRIPT> 内联块必须被扫到（否则整页漏扫 ⇒ 动效守卫护栏静默归零）
#   · 大写 SRC= 外链脚本必须被排除（浏览器不执行其内容 ⇒ 不得当成内联块）

MOTION_UPPERCASE_SCRIPT_TAG = """<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>W1136 大写标签负样本</title></head>
<body>
<SCRIPT>
var MOYUN_RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
d3.selectAll('.bar').transition().duration(600);
</SCRIPT>
</body>
</html>
"""

MOTION_UPPERCASE_SRC_EXTERNAL = """<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>W1136 大写 SRC 外链正样本</title></head>
<body>
<SCRIPT SRC="external.js">d3.selectAll('.bar').transition().duration(600);</SCRIPT>
</body>
</html>
"""


def test_motion_guard_negative_uppercase_script_tag_exit_1(tmp_path):
    """M1 负样本：大写 <SCRIPT> 包裹的内联块必须被扫到 ⇒ 裸数字实参判红（防大小写盲区）。"""
    gate = _stage_gate(tmp_path, MOTION_GATE)
    _write_motion_page(tmp_path, MOTION_UPPERCASE_SCRIPT_TAG)

    _assert_red(
        _run(gate, cwd=tmp_path),
        ["未套守卫的 BARE", ".duration(600)"],
        "M1 负样本（大写 <SCRIPT> 内联块）",
    )


def test_motion_guard_uppercase_src_external_excluded_exit_0(tmp_path):
    """M1 正样本：大写 SRC= 外链脚本的内容不执行 ⇒ 不得当作内联块（否则误判红）。"""
    gate = _stage_gate(tmp_path, MOTION_GATE)
    _write_motion_page(tmp_path, MOTION_UPPERCASE_SRC_EXTERNAL)

    _assert_green(_run(gate, cwd=tmp_path), "M1 正样本（大写 SRC= 外链被排除）")


# ---------------------------------------------------------------------------
# M2 assets/design 清单对拍
# ---------------------------------------------------------------------------

MANIFEST_CLEAN_README = """# 设计资产清单（W1135 正样本夹具）

- 主入口：`index.html`
- 图标：`favicon-16.png`
"""

MANIFEST_BROKEN_README = """# 设计资产清单（W1135 负样本夹具）

- 主入口：`index.html`
- 磁盘上不存在的文件：`ghost-file.png`
"""


def _write_manifest_tree(tmp_path, readme):
    base = tmp_path / "assets" / "design"
    base.mkdir(parents=True, exist_ok=True)
    (base / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    (base / "index.html").write_text("<!DOCTYPE html>\n", encoding="utf-8", newline="\n")
    (base / "favicon-16.png").write_bytes(b"\x89PNG\r\n\x1a\n")


def test_design_manifest_positive_existing_files_exit_0(tmp_path):
    """M2 正样本：反引号声明的文件磁盘上都存在 ⇒ 退出码 0。"""
    gate = _stage_gate(tmp_path, MANIFEST_GATE)
    _write_manifest_tree(tmp_path, MANIFEST_CLEAN_README)

    _assert_green(_run(gate, cwd=tmp_path), "M2 正样本（声明均在磁盘）")


def test_design_manifest_negative_missing_file_exit_1(tmp_path):
    """M2 负样本：反引号声明磁盘上不存在的 ghost-file.png ⇒ 判红（退出码 1）。"""
    gate = _stage_gate(tmp_path, MANIFEST_GATE)
    _write_manifest_tree(tmp_path, MANIFEST_BROKEN_README)

    _assert_red(
        _run(gate, cwd=tmp_path),
        ["ghost-file.png", "磁盘不存在"],
        "M2 负样本（声明了磁盘不存在的文件）",
    )


# ---------------------------------------------------------------------------
# M3 tooltip 多行间距（运行层 · playwright）
# ---------------------------------------------------------------------------

CSS_CLEAN = (
    ":root { --space-2: 4px; }\n"
    ".chart-tooltip { position: absolute; }\n"
    ".chart-tooltip div + div { margin-top: var(--space-2); }"
)

CSS_MISSING_RULE = (
    ":root { --space-2: 4px; }\n"
    ".chart-tooltip { position: absolute; }"
)

CSS_LEGACY_RULE = (
    ":root { --space-2: 4px; }\n"
    ".tooltip div + div { margin-top: var(--space-2); }"
)


def _tooltip_page(css):
    return (
        "<!DOCTYPE html>\n"
        '<html lang="zh">\n'
        '<head><meta charset="utf-8"><title>W1135 tooltip 夹具</title>\n'
        "<style>\n%s\n</style>\n"
        "</head>\n"
        "<body></body>\n"
        "</html>\n"
    ) % css


def _write_tooltip_pages(tmp_path, overrides=None):
    """写 3 个被测页；overrides 里的页用指定 CSS，其余用干净 CSS。"""
    overrides = overrides or {}
    site = tmp_path / "site"
    for rel in TOOLTIP_PAGES:
        full = site / rel
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(_tooltip_page(overrides.get(rel, CSS_CLEAN)), encoding="utf-8", newline="\n")
    return site


@pytest.fixture(scope="module")
def chromium_ready():
    """chromium 是否可用（不可用 ⇒ 脚本语义 = 退出码 2 基础设施缺失）。"""
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return False
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            browser.close()
    except Exception:
        return False
    return True


def test_tooltip_positive_clean_pages_exit_0(tmp_path, chromium_ready):
    """M3 正样本：三页均有 .chart-tooltip div + div 且取自 --space-2 ⇒ 退出码 0（真跑浏览器）。"""
    if not chromium_ready:
        pytest.skip(BROWSER_SKIP_REASON)
    gate = _stage_gate(tmp_path, TOOLTIP_GATE)
    _write_tooltip_pages(tmp_path)

    _assert_green(_run(gate, cwd=tmp_path), "M3 正样本（规范规则齐备）")


def test_tooltip_negative_missing_rule_exit_1(tmp_path, chromium_ready):
    """M3 负样本：某页缺 .chart-tooltip div + div 规则 ⇒ 判红（退出码 1，真跑浏览器）。"""
    if not chromium_ready:
        pytest.skip(BROWSER_SKIP_REASON)
    gate = _stage_gate(tmp_path, TOOLTIP_GATE)
    _write_tooltip_pages(tmp_path, {TOOLTIP_PAGES[0]: CSS_MISSING_RULE})

    _assert_red(
        _run(gate, cwd=tmp_path),
        ["缺规范规则", ".chart-tooltip div + div"],
        "M3 负样本（缺规范规则）",
    )


def test_tooltip_negative_legacy_rule_exit_1(tmp_path, chromium_ready):
    """M3 负样本：残留旧死规则 .tooltip div + div ⇒ 判红（退出码 1，真跑浏览器）。"""
    if not chromium_ready:
        pytest.skip(BROWSER_SKIP_REASON)
    gate = _stage_gate(tmp_path, TOOLTIP_GATE)
    _write_tooltip_pages(tmp_path, {TOOLTIP_PAGES[1]: CSS_LEGACY_RULE})

    _assert_red(
        _run(gate, cwd=tmp_path),
        ["残留旧死规则", ".tooltip div + div"],
        "M3 负样本（残留旧死规则）",
    )


# ---------------------------------------------------------------------------
# M3 无浏览器自证（假 CSSOM 读数注入 probe ⇒ 真实 main() 判定路径 ⇒ 真实退出码）
# ---------------------------------------------------------------------------

DRIVER_SRC = """import json
import sys

_scripts_dir = sys.argv[1]
_rows_path = sys.argv[2]
sys.argv = [sys.argv[0]]

sys.path.insert(0, _scripts_dir)

import check_tooltip_spacing as gate


def _fake_probe():
    with open(_rows_path, encoding="utf-8") as fh:
        return json.load(fh)


gate.probe = _fake_probe
sys.exit(gate.main())
"""


def _fake_rows(margin_top, space2, rule_hits, legacy_rules):
    return [
        {
            "page": rel,
            "theme": theme,
            "marginTop": margin_top,
            "space2": space2,
            "ruleHits": rule_hits,
            "legacyRules": legacy_rules,
        }
        for rel in TOOLTIP_PAGES
        for theme in ("light", "dark")
    ]


def _run_stubbed(tmp_path, rows):
    """用假 CSSOM 读数驱动真实 main() 判定路径 ⇒ 拿到真实进程退出码（0 / 1）。"""
    gate = _stage_gate(tmp_path, TOOLTIP_GATE)
    (tmp_path / "site").mkdir(parents=True, exist_ok=True)
    rows_path = tmp_path / "fake-rows.json"
    rows_path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8", newline="\n")
    driver = tmp_path / "stub_driver.py"
    driver.write_text(DRIVER_SRC, encoding="utf-8", newline="\n")
    return _run(driver, str(gate.parent), str(rows_path), cwd=tmp_path)


def test_tooltip_stubbed_probe_negative_missing_rule_exit_1(tmp_path):
    """M3 无浏览器负样本：假 CSSOM 读数=缺规范规则 ⇒ 真实退出码 1（不 skip）。"""
    rows = _fake_rows(margin_top="0px", space2="4px", rule_hits=0, legacy_rules=0)

    _assert_red(
        _run_stubbed(tmp_path, rows),
        ["缺规范规则", ".chart-tooltip div + div"],
        "M3 无浏览器负样本（缺规范规则）",
    )


def test_tooltip_stubbed_probe_positive_clean_exit_0(tmp_path):
    """M3 无浏览器正样本：假 CSSOM 读数合规 ⇒ 真实退出码 0（不 skip）。"""
    rows = _fake_rows(margin_top="4px", space2="4px", rule_hits=1, legacy_rules=0)

    _assert_green(_run_stubbed(tmp_path, rows), "M3 无浏览器正样本（读数合规）")
