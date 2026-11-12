"""W1210 新增守卫 check_placeholder_hash_carrier.py 的单测（第 71 槽）。

三个断言面：
  ① 判据行为——内联 <script> 正文 / <script src> 属性必红，meta 与外部 JS 必绿，
     扫描面失效（扫不到内联块）必须 fail-closed 判红；
  ② 口径同源——内联块提取与 generate_csp 逐字一致（哈希口径不分裂）；
  ③ 接线面——第 71 槽已登记进 verify_delivery 注册表三处，且槽号声明面同步。
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
GUARD_REL = "scripts/check_placeholder_hash_carrier.py"
PH = "__XIJ_SERVICE_BASE__"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def _load_guard():
    """按路径加载守卫模块（守卫自身会 import generate_csp·口径同源）。"""
    spec = importlib.util.spec_from_file_location(
        "phc_guard", SCRIPTS / "check_placeholder_hash_carrier.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


GUARD = _load_guard()


# ---------------------------------------------------------------- ① 判据行为

def test_guard_script_exists():
    assert (ROOT / GUARD_REL).exists()


def test_inline_script_placeholder_flagged(tmp_path):
    """C1：占位符落在内联 <script> 块内 ⇒ 判红（哈希载体）。"""
    p = tmp_path / "a.html"
    p.write_text(
        "<html><head><script>var B = '%s';</script></head></html>" % PH,
        encoding="utf-8")
    rep = GUARD.evaluate([str(tmp_path)])
    assert rep["violation_count"] == 1, rep["violations"]
    v = rep["violations"][0]
    assert v["role"] == "inline_script"
    assert v["token"] == PH
    assert v["block_index"] == 1
    assert v["block_hash12"], "须给出该块 sha256 前 12 位（定位到具体段）"


def test_script_src_placeholder_flagged(tmp_path):
    """C2：占位符落在 <script src> 属性值上 ⇒ 判红（替换后成外域）。

    目录内另有含内联块的页：C3 兜底是**扫描面级**判据（整次扫描内联块数为 0 才触发），
    故本页单独存在时兜底会一并触发——混排后只余 script_src 一条违规。
    """
    (tmp_path / "b0.html").write_text(
        "<html><head><script>var x=1;</script></head></html>", encoding="utf-8")
    p = tmp_path / "b.html"
    p.write_text(
        '<html><head><script src="%s/app.js"></script></head></html>' % PH,
        encoding="utf-8")
    rep = GUARD.evaluate([str(tmp_path)])
    assert rep["violation_count"] == 1, rep["violations"]
    assert rep["violations"][0]["role"] == "script_src"


def test_meta_and_external_js_allowed(tmp_path):
    """C4：CSP 声明面 / 旁挂 meta / 外部 JS 为合法载体 ⇒ 判红 0。"""
    (tmp_path / "c.html").write_text(
        '<html><head><meta http-equiv="Content-Security-Policy" content="connect-src %s">'
        '<meta name="xij-service-base" content="%s"></head>'
        "<body><script>var x=1;</script></body></html>" % (PH, PH),
        encoding="utf-8")
    (tmp_path / "d.js").write_text("var B = '%s';\n" % PH, encoding="utf-8")
    rep = GUARD.evaluate([str(tmp_path)])
    assert rep["violation_count"] == 0, rep["violations"]
    roles = {r["role"] for r in rep["registry"]}
    assert "csp_meta" in roles and "meta" in roles and "external_js" in roles, roles


def test_scan_surface_failure_closed(tmp_path):
    """C3 扫描面级兜底：整次扫描扫不到任何内联块 ⇒ 必须判红（防扫描器静默失效假绿）。"""
    (tmp_path / "e.html").write_text(
        '<html><head><script src="static/js/app.js"></script></head></html>',
        encoding="utf-8")
    rep = GUARD.evaluate([str(tmp_path)])
    assert rep["violation_count"] == 1, rep["violations"]
    assert rep["violations"][0]["role"] == "scan_surface"


# ---------------------------------------------------------------- ② 口径同源

def test_inline_extraction_matches_generate_csp():
    """内联块提取必须与 generate_csp 同源（块数一致 + 块正文逐字一致）。"""
    import generate_csp
    sample = "<html><body><script>\n  const a = 1;\n</script></body></html>"
    blocks = GUARD.inline_blocks(sample)
    hashes = generate_csp.inline_script_hashes(sample)
    assert len(blocks) == len(hashes) == 1
    assert generate_csp.inline_script_hashes("<script>%s</script>" % blocks[0][1]) == hashes


def test_guard_self_test_passes():
    """守卫自带负样本自证必须全过（rc 0）。"""
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_placeholder_hash_carrier.py"), "--self-test"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "全部通过" in r.stdout, r.stdout


# ---------------------------------------------------------------- ③ 接线面

def test_slot_registered_in_verify_delivery():
    """第 71 槽必须登记进 verify_delivery 注册表三处（W781 R-1）。"""
    src = (ROOT / "scripts" / "verify_delivery.py").read_text(encoding="utf-8")
    assert '"占位符哈希载体"' in src
    assert "---- 第 71 门禁 占位符哈希载体：" in src
    assert "第 71 槽" in src
    # 注册表三处：EXPECTED_SECTION_NAMES / _SCOPE_CORE / 门禁元组
    assert src.count('"占位符哈希载体"') >= 2


def test_declaration_surfaces_in_sync():
    """槽号声明面同步：AGENTS 第 71 条 / gates.md 第 71 条 / 文档规范 76 段。"""
    import re
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    gates = (ROOT / "docs" / "agent" / "gates.md").read_text(encoding="utf-8")
    doc_spec = (ROOT / "docs" / "00-导读" / "文档规范.md").read_text(encoding="utf-8")
    i = agents.find("### 4.2")
    j = agents.find("### 4.3", i)
    sec42 = agents[i:j]
    assert re.search(r"(?m)^71\. \*\*", sec42), "AGENTS §4.2 缺第 71 条"
    assert re.search(r"(?m)^71\. \*\*", gates), "gates.md 缺第 71 条"
    # 槽总数由 gates.md 编号条目派生（marker 化后 sweep 自动跟随，钉字面量会在挂新槽时假红）
    slots = len(re.findall(r"(?m)^\d+\. \*\*", gates))
    assert ("内含 %d 槽，五组" % slots) in re.sub(r"<!--stats:[a-z_0-9]+-->", "", sec42), \
        "AGENTS §4.2 槽数散文未与 gates.md 编号条目数（%d）一致" % slots
    m = re.search(r"verify full 全部执行段（随挂槽演进·现役 (\d+) 段", doc_spec)
    assert m and int(m.group(1)) == 76, "文档规范段数未随挂槽同步为 76"
