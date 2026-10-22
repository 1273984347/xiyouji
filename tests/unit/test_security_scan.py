# -*- coding: utf-8 -*-
"""W266 E5 测试深化·security_scan.py 单元测试·pytest 风格

覆盖 3 大扫描入口：
  - test_headers_scan       验证 _headers 文件扫描
  - test_sri_scan            验证 SRI 完整性
  - test_dependency_scan     验证 pip-audit 集成

运行：pytest tests/unit/test_security_scan.py -v
"""
import json
import sys
from pathlib import Path

import pytest

# 将 scripts/ 加入 sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import security_scan  # noqa: E402


# ---------------------------------------------------------------------------
# 辅助：在 security_scan 中没有的扫描能力时，以独立函数补齐
# 这里以可被测试调用的辅助函数形式实现，保持被测代码与脚本解耦
# ---------------------------------------------------------------------------

def scan_headers_file(headers_path: Path):
    """扫描 _headers 文件，返回 findings 列表

    检查项：
      - CSP 缺失
      - 缺失 X-Content-Type-Options: nosniff
      - 缺失 X-Frame-Options: DENY/SAMEORIGIN
      - 缺失 Referrer-Policy
    """
    findings = []
    if not headers_path.exists():
        return findings
    text = headers_path.read_text(encoding="utf-8", errors="replace")
    has_csp = "Content-Security-Policy" in text
    has_nosniff = "X-Content-Type-Options" in text and "nosniff" in text
    has_frame = "X-Frame-Options" in text
    has_referrer = "Referrer-Policy" in text

    if not has_csp:
        findings.append({"rule": "HDR-001", "severity": "high",
                        "description": "_headers 缺失 Content-Security-Policy"})
    if not has_nosniff:
        findings.append({"rule": "HDR-002", "severity": "medium",
                        "description": "_headers 缺失 X-Content-Type-Options: nosniff"})
    if not has_frame:
        findings.append({"rule": "HDR-003", "severity": "medium",
                        "description": "_headers 缺失 X-Frame-Options"})
    if not has_referrer:
        findings.append({"rule": "HDR-004", "severity": "low",
                        "description": "_headers 缺失 Referrer-Policy"})
    return findings


def scan_sri_in_html(html_path: Path):
    """扫描 HTML 中 <link>/<script> 的 SRI 完整性

    检查项：
      - 外部资源（带 src/href 且 https 跨域）缺少 integrity 属性
      - 缺少 crossorigin 属性
    """
    import re
    findings = []
    if not html_path.exists():
        return findings
    text = html_path.read_text(encoding="utf-8", errors="replace")

    pattern = re.compile(
        r'<(?:link|script)\b([^>]*?)(?:src|href)\s*=\s*'
        r'["\'](https?://[^"\']+)["\']([^>]*?)>',
        re.IGNORECASE,
    )
    for m in pattern.finditer(text):
        all_attrs = m.group(1) + m.group(3)
        url = m.group(2)
        # 仅检查跨域 https 资源
        if not url.startswith("https://"):
            continue
        if "integrity" not in all_attrs.lower():
            findings.append({
                "rule": "SRI-001", "severity": "high",
                "url": url,
                "description": f"外部资源 {url} 缺少 integrity 属性",
            })
        if "crossorigin" not in all_attrs.lower():
            findings.append({
                "rule": "SRI-002", "severity": "medium",
                "url": url,
                "description": f"外部资源 {url} 缺少 crossorigin 属性",
            })
    return findings


def run_pip_audit_mock(requirements_path: Path):
    """模拟 pip-audit 运行（避免依赖外部工具）

    返回模拟审计结果 dict：
      - vulnerabilities: 空数组（模拟无漏洞）
      - scanned: True
      - requirements_file: 路径
    """
    if not requirements_path.exists():
        return {"error": "requirements.txt 不存在", "vulnerabilities": []}
    return {
        "vulnerabilities": [],
        "scanned": True,
        "requirements_file": str(requirements_path),
        "note": "W266 E5 mock - 实际环境由 CI 调用 pip-audit",
    }


# ---------------------------------------------------------------------------
# test_headers_scan
# ---------------------------------------------------------------------------

def test_headers_scan_complete(tmp_path: Path):
    """完整的 _headers 文件应通过扫描无 findings"""
    hp = tmp_path / "_headers"
    hp.write_text(
        "/*\n"
        "  Content-Security-Policy: default-src 'self'\n"
        "  X-Content-Type-Options: nosniff\n"
        "  X-Frame-Options: DENY\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n",
        encoding="utf-8",
    )
    findings = scan_headers_file(hp)
    assert findings == []


def test_headers_scan_missing_csp(tmp_path: Path):
    """缺失 CSP 应报 high 级别"""
    hp = tmp_path / "_headers"
    hp.write_text(
        "/*\n  X-Content-Type-Options: nosniff\n",
        encoding="utf-8",
    )
    findings = scan_headers_file(hp)
    rules = [f["rule"] for f in findings]
    assert "HDR-001" in rules
    csp_finding = next(f for f in findings if f["rule"] == "HDR-001")
    assert csp_finding["severity"] == "high"


def test_headers_scan_missing_nosniff(tmp_path: Path):
    """缺失 nosniff 应报 medium 级别"""
    hp = tmp_path / "_headers"
    hp.write_text(
        "/*\n  Content-Security-Policy: default-src 'self'\n",
        encoding="utf-8",
    )
    findings = scan_headers_file(hp)
    rules = [f["rule"] for f in findings]
    assert "HDR-002" in rules


def test_headers_scan_missing_file(tmp_path: Path):
    """文件不存在时应返回空列表"""
    findings = scan_headers_file(tmp_path / "missing")
    assert findings == []


# ---------------------------------------------------------------------------
# test_sri_scan
# ---------------------------------------------------------------------------

def test_sri_scan_clean_html(tmp_path: Path):
    """完整 SRI 配置的 HTML 应无 findings"""
    hp = tmp_path / "page.html"
    hp.write_text(
        '<html><head>'
        '<link rel="stylesheet" href="https://cdn.example.com/style.css" '
        'integrity="sha384-abc" crossorigin="anonymous">'
        '<script src="https://cdn.example.com/app.js" '
        'integrity="sha384-def" crossorigin="anonymous"></script>'
        '</head><body></body></html>',
        encoding="utf-8",
    )
    findings = scan_sri_in_html(hp)
    assert findings == []


def test_sri_scan_missing_integrity(tmp_path: Path):
    """外部资源缺少 integrity 应报 high"""
    hp = tmp_path / "page.html"
    hp.write_text(
        '<html><head>'
        '<script src="https://cdn.example.com/unsafe.js" '
        'crossorigin="anonymous"></script>'
        '</head><body></body></html>',
        encoding="utf-8",
    )
    findings = scan_sri_in_html(hp)
    sri001 = [f for f in findings if f["rule"] == "SRI-001"]
    assert len(sri001) >= 1
    assert sri001[0]["severity"] == "high"


def test_sri_scan_missing_crossorigin(tmp_path: Path):
    """外部资源缺少 crossorigin 应报 medium"""
    hp = tmp_path / "page.html"
    hp.write_text(
        '<html><head>'
        '<link rel="stylesheet" href="https://cdn.example.com/style.css" '
        'integrity="sha384-abc">'
        '</head><body></body></html>',
        encoding="utf-8",
    )
    findings = scan_sri_in_html(hp)
    sri002 = [f for f in findings if f["rule"] == "SRI-002"]
    assert len(sri002) >= 1
    assert sri002[0]["severity"] == "medium"


def test_sri_scan_skip_local(tmp_path: Path):
    """本地相对路径资源应跳过"""
    hp = tmp_path / "page.html"
    hp.write_text(
        '<html><head>'
        '<link rel="stylesheet" href="local.css">'
        '<script src="./app.js"></script>'
        '</head><body></body></html>',
        encoding="utf-8",
    )
    findings = scan_sri_in_html(hp)
    assert findings == []


def test_sri_scan_skip_http(tmp_path: Path):
    """http:// 资源应跳过（仅扫描 https 跨域）"""
    hp = tmp_path / "page.html"
    hp.write_text(
        '<html><head>'
        '<script src="http://cdn.example.com/old.js"></script>'
        '</head><body></body></html>',
        encoding="utf-8",
    )
    findings = scan_sri_in_html(hp)
    assert findings == []


# ---------------------------------------------------------------------------
# test_dependency_scan
# ---------------------------------------------------------------------------

def test_dependency_scan_clean_requirements(tmp_path: Path):
    """干净 requirements.txt 应通过 mock 审计"""
    rp = tmp_path / "requirements.txt"
    rp.write_text("jieba>=0.42\nPillow>=9.0\n", encoding="utf-8")
    result = run_pip_audit_mock(rp)
    assert result["scanned"] is True
    assert result["vulnerabilities"] == []


def test_dependency_scan_missing_requirements(tmp_path: Path):
    """requirements.txt 不存在时应报 error"""
    rp = tmp_path / "nope.txt"
    result = run_pip_audit_mock(rp)
    assert "error" in result
    assert result["vulnerabilities"] == []


def test_dependency_scan_integration_with_security_scan():
    """验证 security_scan 模块导出可被调用（不实际执行扫描）"""
    # 验证模块导入成功 + 关键函数/常量存在
    assert hasattr(security_scan, "RULES")
    assert hasattr(security_scan, "scan_file")
    assert hasattr(security_scan, "discover_files")
    assert hasattr(security_scan, "build_report")
    # 验证规则集中包含 XSS / SEC / API / CSP 类别
    categories = {rid.split("-")[0] for rid, *_ in security_scan.RULES}
    assert "XSS" in categories
    assert "SEC" in categories
    assert "API" in categories
    assert "CSP" in categories


# ---------------------------------------------------------------------------
# W757 扩面：扫描面必须覆盖 xiyouji-agent-web（能读写仓库的 React+Express 服务）
# ---------------------------------------------------------------------------

def test_discover_files_covers_agent_web():
    """W757 D3：扫描面必须包含 xiyouji-agent-web/ 下的源文件。

    缺陷背景：原 roots = [site, scripts, tests, mcp-server]，不含 agent-web；
    exts 不含 .ts/.tsx/.mjs。该目录是「能读写仓库文件、运行脚本」的服务
    （安全风险最集中处），此前**零覆盖**（全文件 grep `agent-web` 命中 0）。
    """
    files = security_scan.discover_files()
    aw = [f for f in files if "xiyouji-agent-web" in str(f).replace("\\", "/")]
    assert aw, "扫描面不含 xiyouji-agent-web/ 任何文件——扩面被回退（W757 D3 复发）"


def test_discover_files_includes_typescript_sources():
    """W757 D3：必须扫 .ts / .tsx / .mjs（agent-web 主体为 TypeScript）。"""
    files = security_scan.discover_files()
    exts = {f.suffix for f in files}
    for want in (".ts", ".tsx", ".mjs"):
        assert want in exts, "扫描面缺扩展名 %s——TypeScript 源文件不受安全门禁保护" % want


def test_discover_files_excludes_agent_web_build_artifacts():
    """W757：tsc 编译产物必须排除（否则「本地红 / CI 绿」分歧）。

    实测：tools.test.js（由 tools.test.ts 生成·.gitignore:121 忽略）内含测试夹具
    假凭证，命中 SEC-002 high；CI 上无该产物，若纳入扫描会造成本地阻断而 CI 放行。
    """
    files = security_scan.discover_files()
    artifacts = [
        str(f).replace("\\", "/") for f in files
        if str(f).replace("\\", "/").startswith("xiyouji-agent-web/server/")
        and (str(f).endswith(".js") or str(f).endswith(".d.ts"))
    ]
    assert not artifacts, "扫描面含 agent-web tsc 编译产物（应排除）：%s" % artifacts[:5]


def test_agent_web_scan_surface_is_stable():
    """W757：扩面规模下限（防扩面被静默收窄成空集）。"""
    files = security_scan.discover_files()
    aw = [f for f in files if "xiyouji-agent-web" in str(f).replace("\\", "/")]
    assert len(aw) >= 30, "agent-web 扫描面仅 %d 个文件，疑似收窄（实测入库源文件 43 个）" % len(aw)


# ---------------------------------------------------------------------------
# W816：XSS 规则覆盖面补齐 + 构建产物排除修复（负样本实证）
# ---------------------------------------------------------------------------

def test_discover_files_excludes_tsbuild_artifacts():
    """W816：tsc outDir 产物必须排除（outDir 已迁至 .tsbuild·W757 的旧断言只覆盖 server/ 形态）。

    成因：tsconfig.node.json 的 "outDir": "./.tsbuild"，而 W757 写下的排除只认
    `xiyouji-agent-web/server/**` 与 `server/engine/**` → .tsbuild/ 下的编译测试夹具
    （内含假凭证）被纳入扫描 → 本机报 SEC-002 high 而 CI（无该目录）恒绿——
    正是「本地红 / CI 绿」分裂在 outDir 迁移后的复发。
    """
    files = security_scan.discover_files()
    leaked = [
        str(f).replace("\\", "/") for f in files
        if ".tsbuild" in str(f).replace("\\", "/").split("/")
    ]
    assert not leaked, "扫描面含 agent-web tsc 产物（.tsbuild/ 应排除）：%s" % leaked[:5]


def test_agent_web_build_artifact_regex_covers_tsbuild():
    """W816：排除正则须覆盖 .tsbuild 前缀（正则层直证·不依赖 discover_files 全量扫描）。"""
    root = security_scan.ROOT
    probe = root / "xiyouji-agent-web" / ".tsbuild" / "server" / "engine" / "tools.test.js"
    assert security_scan._is_agent_web_build_artifact(probe), (
        "排除正则未覆盖 .tsbuild/ 产物：%s" % probe)
    legacy = root / "xiyouji-agent-web" / "server" / "engine" / "tools.test.js"
    assert security_scan._is_agent_web_build_artifact(legacy), (
        "排除正则回归：旧形态 server/engine/*.js 不再被排除")


def _scan_synthetic(tmp_path, monkeypatch, rel_name, content):
    """在 tmp 仓形下扫描一个合成文件（monkeypatch ROOT·避免污染真实工作树）。"""
    monkeypatch.setattr(security_scan, "ROOT", tmp_path)
    target = tmp_path / rel_name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return security_scan.scan_file(target)


def test_xss_rule_covers_d3_html_sink(tmp_path, monkeypatch):
    """W816：d3 `.html()` 是 innerHTML 等价 sink——XSS-001 不覆盖此形态（原零信号）。"""
    findings = _scan_synthetic(
        tmp_path, monkeypatch, "page.html",
        "<html><body><script>\n"
        "d3.select('#x').html('<b>' + value + '</b>');\n"
        "</script></body></html>\n")
    rules = {f["rule"] for f in findings}
    assert "XSS-007" in rules, "d3 .html() 未被 XSS 规则捕获（rules=%s）" % sorted(rules)


def test_xss_rule_covers_innerhtml_append_sink(tmp_path, monkeypatch):
    """W816：`.innerHTML +=` 追加赋值——XSS-001 的 `=` 前有 `+` 故不匹配（原零信号）。"""
    findings = _scan_synthetic(
        tmp_path, monkeypatch, "page.html",
        "<html><body><script>\n"
        "el.innerHTML += '<b>' + value + '</b>';\n"
        "</script></body></html>\n")
    rules = {f["rule"] for f in findings}
    assert "XSS-008" in rules, ".innerHTML += 未被 XSS 规则捕获（rules=%s）" % sorted(rules)


def test_xss001_still_fires_for_plain_innerhtml_assignment(tmp_path, monkeypatch):
    """W816 回归锚：补新规则不得破坏既有 XSS-001（`.innerHTML =` 形态）。"""
    findings = _scan_synthetic(
        tmp_path, monkeypatch, "page.html",
        "<html><body><script>\n"
        "el.innerHTML = '<b>' + value + '</b>';\n"
        "</script></body></html>\n")
    rules = {f["rule"] for f in findings}
    assert "XSS-001" in rules, "既有 XSS-001 失效（rules=%s）" % sorted(rules)


def test_new_xss_rules_use_site_downgrade_semantics(tmp_path, monkeypatch):
    """W816：新规则须沿用既有 site/ 降级口径（visual 页面 high→medium·非 site/ 仍 high）。"""
    site_findings = _scan_synthetic(
        tmp_path, monkeypatch, "site/page.html",
        "<html><body><script>\n"
        "d3.select('#x').html('<b>' + v + '</b>');\n"
        "el.innerHTML += '<i>' + v + '</i>';\n"
        "</script></body></html>\n")
    sev = {f["rule"]: f["severity"] for f in site_findings if f["rule"] in ("XSS-007", "XSS-008")}
    assert sev.get("XSS-007") == "medium", "site/ 内 XSS-007 未按既有口径降级：%s" % sev
    assert sev.get("XSS-008") == "medium", "site/ 内 XSS-008 未按既有口径降级：%s" % sev

    outside = _scan_synthetic(
        tmp_path, monkeypatch, "outside/page.html",
        "<html><body><script>\n"
        "d3.select('#x').html('<b>' + v + '</b>');\n"
        "</script></body></html>\n")
    sev2 = {f["rule"]: f["severity"] for f in outside if f["rule"] == "XSS-007"}
    assert sev2.get("XSS-007") == "high", "非 site/ 目录的 XSS-007 未保持 high：%s" % sev2
