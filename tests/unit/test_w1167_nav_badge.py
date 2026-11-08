"""W1167 迁移批机制件单测：导航/徽标两个正本生成器 + 两个门禁判据。

覆盖：active_for 路由映射 / relpath 三深度 / build_nav 六项序与高亮 / classify 证据集 /
build_badge 三态文案 / 门禁 check_page 正负样本（与 --self-test 同源但走 pytest 计数钉）。
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
ROOT = Path(__file__).resolve().parents[2]


def _load(fname):
    spec = importlib.util.spec_from_file_location("m_" + fname.replace(".py", ""), SCRIPTS / fname)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


nav = _load("w1167_nav_inject.py")
badge = _load("w1167_badge_inject.py")
analytics = _load("w1167_analytics_inject.py")
gate_nav = _load("check_nav_parity.py")
gate_badge = _load("check_data_badge_coverage.py")


def test_analytics_block_shape():
    assert analytics.rel_static("index.html") == "static/js/goatcounter.js"
    assert analytics.rel_static("data/x.html") == "../static/js/goatcounter.js"
    blk = analytics.build_block("data/x.html", {"goatcounter_endpoint": "https://a.goatcounter.com/count", "ga4_measurement_id": "G-TEST123"})
    assert analytics.MARK in blk
    assert 'data-goatcounter="https://a.goatcounter.com/count"' in blk
    assert 'src="../static/js/goatcounter.js"' in blk
    assert 'src="../static/js/stats.js"' in blk  # 桥随块分发：全站唯一统计发射出口
    # W1168 G0-1-R GA4 轨退役：配置里即便还留着 ID 也不得再生成 gtag 块
    # （「待填位 + 已退役」共存就是死轨形态，正本是 generate_csp.py 的例外域全集）
    assert "G-TEST123" not in blk and "gtag" not in blk
    assert analytics.build_block("x.html", {}) == ""  # 无端点=不注入


# ---- 导航正本 ----

def test_active_for_mapping():
    assert nav.active_for("index.html") is None
    assert nav.active_for("404.html") is None
    assert nav.active_for("en/aesthetics.html") is None
    assert nav.active_for("guide.html") == "导读"
    assert nav.active_for("curated.html") == "导读"
    assert nav.active_for("reader/ch001.html") == "阅读"
    assert nav.active_for("dashboard.html") == "看板"
    assert nav.active_for("data/chapter-stats.html") == "看板"
    assert nav.active_for("data/text-search.html") == "检索"
    assert nav.active_for("about.html") == "关于"


def test_relpath_depth():
    assert nav.relpath("guide.html", "index.html") == "guide.html"
    assert nav.relpath("guide.html", "data/x.html") == "../guide.html"
    assert nav.relpath("index.html", "en/x.html") == "index.html"  # EN 同目录语义
    assert nav.relpath("../index.html", "en/x.html") == "../index.html"  # 中文回根


def test_build_nav_order_and_active():
    html = nav.build_nav("guide.html", "root")
    assert nav.MARK in html
    assert html.index("导读") < html.index("阅读") < html.index("看板") < html.index("检索") < html.index("关于") < html.index("EN")
    # 断言按「同一锚点上的属性集合」而非相邻文本——属性顺序不是契约（W1167 加埋点属性后，
    # 曾以 `aria-current="page">导读` 相邻形态断言的写法会误报，属判据脆弱而非实现缺陷）。
    guide = re.search(r'<a [^>]*>导读</a>', html).group(0)
    assert 'aria-current="page"' in guide and 'class="nav-item is-active"' in guide
    assert 'href="guide.html"' in guide  # active 项指向自身去向（当前页不可再跳转）
    en = nav.build_nav("en/aesthetics.html", "en")
    assert "Visualizations" in en and "中文" in en and "导读" not in en


def test_nav_event_slugs_are_declared_not_derived():
    """埋点事件名（must×8 之 nav_click）契约：正本内显式声明 + ASCII + 中英区不撞名。

    反例即本仓踩过的派生坑：index.html 在中/英/回根三处含义不同，
    "../index.html" 按文件名派生成空 slug——故事件名必须是声明面。
    """
    assert [it[2] for it in nav.ZH_ITEMS] == [
        "nav-guide", "nav-reader", "nav-dashboard", "nav-search", "nav-about", "nav-switch-en"]
    assert [it[2] for it in nav.EN_ITEMS] == [
        "nav-home", "nav-en-guide", "nav-en-dashboard", "nav-en-search",
        "nav-en-visualizations", "nav-switch-zh"]
    zh, en = [it[2] for it in nav.ZH_ITEMS], [it[2] for it in nav.EN_ITEMS]
    assert not (set(zh) & set(en)), "中英区事件名混流会让两侧计数不可拆"
    assert all(s.isascii() and " " not in s for s in zh + en)
    html = nav.build_nav("dashboard.html", "root")
    assert re.findall(r'data-goatcounter-click="([^"]+)"', html) == zh
    assert 'data-goatcounter-click="nav-switch-en"' in html  # 无空 slug 漏网


# ---- 徽标正本 ----

def test_classify_evidence_sets():
    assert badge.classify("data-explorer.html") == "live"
    assert badge.classify("chapter-stats.html") == "snapshot"
    assert badge.classify("anything.html") == "snapshot"  # 默认态，零虚构 sample


def test_build_badge_reader_language():
    html = badge.build_badge("snapshot")
    assert badge.MARK in html
    assert 'data-status="snapshot"' in html
    assert "内嵌快照" in html
    for jargon in ("EMBEDDED", "fallback", "mock"):
        assert jargon not in html  # story-2 AC3 读者语言


# ---- 门禁判据（与 --self-test 同源断言，pytest 计数钉） ----

def test_gate_nav_negative_samples():
    zh, en = gate_nav._load_truth()
    good = gate_nav.MARK + '<nav aria-label="主导航">' + "".join(f'<a class="nav-item">{t}</a>' for t in zh) + "</nav>"
    assert not gate_nav.check_page("a.html", good, zh, en)
    assert gate_nav.check_page("a.html", "<p>裸</p>", zh, en)  # 缺 MARK
    assert gate_nav.check_page("a.html", gate_nav.MARK + "<div>剥壳</div>", zh, en)
    swapped = gate_nav.MARK + '<nav aria-label="主导航"><a class="nav-item">阅读</a><a class="nav-item">导读</a>' + "".join(f'<a class="nav-item">{t}</a>' for t in zh[2:]) + "</nav>"
    assert gate_nav.check_page("a.html", swapped, zh, en)


def test_gate_badge_negative_samples():
    good = badge.build_badge("snapshot")
    assert not gate_badge.check_page(badge, "x.html", good)
    assert gate_badge.check_page(badge, "x.html", "<p>无徽标</p>")
    assert gate_badge.check_page(badge, "x.html", good.replace("内嵌快照", "EMBEDDED"))  # 行话回潮
    assert gate_badge.check_page(badge, "x.html", badge.build_badge("live"))  # 与 classify 不符


def test_gate_badge_tolerates_new_attribute_on_canonical():
    """正本给徽标**加属性**（W1168 的 `data-goatcounter-view` 曝光面）不得判成「破损」。

    第 66 槽原按「属性顺序 + 恰好 class/data-status 两个属性」的正则识别结构，加一个属性
    就让 88 页全红——与第 65 槽「正本元组加字段炸门禁」同族：判据必须抗正本的字段增扩。
    """
    good = badge.build_badge("snapshot")
    assert 'data-goatcounter-view="badge_view"' in good, "正本未带曝光属性（W1168 埋点面）"
    assert not gate_badge.check_page(badge, "x.html", good)
    # 属性换序同样放行（结构判据按属性集合而非顺序）
    swapped = good.replace('<div class="data-status-badge" data-status="snapshot"',
                           '<div data-status="snapshot" class="data-status-badge"')
    assert swapped != good and not gate_badge.check_page(badge, "x.html", swapped)
    # 但真破损仍要红：徽标 div 整个不在
    assert gate_badge.check_page(badge, "x.html", badge.MARK + "\n<p>手删了徽标</p>\n")


# ---- 实质执行面（第 42 槽 E3：subprocess 真跑 --dry-run/--self-test，import 冒烟不算覆盖） ----

def test_nav_inject_dry_run_executes():
    r = subprocess.run([sys.executable, "scripts/w1167_nav_inject.py", "--dry-run"],
                       capture_output=True, text=True, encoding="utf-8", timeout=300, cwd=str(ROOT))
    assert r.returncode == 0
    assert "mode=--dry-run" in r.stdout
    assert "实际改动=0" in r.stdout  # 已规范化幂等：dry-run 应零改动（apply 后）

def test_badge_dry_run_executes():
    r = subprocess.run([sys.executable, "scripts/w1167_badge_inject.py", "--dry-run"],
                       capture_output=True, text=True, encoding="utf-8", timeout=120, cwd=str(ROOT))
    assert r.returncode == 0
    assert "mode=--dry-run" in r.stdout


def test_analytics_inject_dry_run_executes():
    r = subprocess.run([sys.executable, "scripts/w1167_analytics_inject.py", "--dry-run"],
                       capture_output=True, text=True, encoding="utf-8", timeout=300, cwd=str(ROOT))
    assert r.returncode == 0
    assert "GoatCounter 单轨=开" in r.stdout and "GA4=已退役" in r.stdout  # W1168 起单轨形态如实打印


def test_spec_mangled_path_guard_blocks_git_octal_escapes():
    """W1167 实证坑回归锁：`git status --porcelain`（非 -z）把中文路径转成八进制转义，
    加 core.quotePath=false 也照转；乱码路径一旦进 spec，级联会写出磁盘不存在的「乱码目录」行
    ⇒ 第 51 槽应动全集与 file-index 登记面双双失真且全程零红灯。守卫须在写入口抛，
    不能静默少登记；同时不得误伤真数字目录（守卫误伤同样会卡死收官链）。
    """
    bspec = _load("batch_spec.py")
    ok_rows = [
        "| docs/00-导读/文档规范.md | W1167 | 改：计数刷新 |",
        "| site/data/81-hardships-view.html | W1167 | 改：导航正本分发 |",
        "| photos/200/301/x.png | W1167 | 真数字目录不得误判 |",
    ]
    bspec.assert_clean_rows(ok_rows)
    assert len(bspec.paths_from_rows(ok_rows)) == 3
    mangled = "| docs/00-/345/257/274/350/257/273//346/226/207.md | W1167 | 乱码 |"
    for call in (lambda: bspec.assert_clean_rows([mangled]),
                 lambda: bspec.paths_from_rows([mangled]),
                 lambda: bspec.fi_group_rows([mangled] * 201, "W1167")):
        try:
            call()
            raise AssertionError("乱码路径未被守卫拦下")
        except ValueError as exc:
            assert "八进制转义" in str(exc)
