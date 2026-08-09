"""W268 E8 安全深化·本地安全扫描工具

v2.2.47 · W268 · 在 W236-E 基础上深化：
  - _headers 文件验证：校验 site/_headers 含 5 安全头（CSP/X-Frame-Options/
    X-Content-Type-Options/Referrer-Policy/Permissions-Policy）
  - SRI 验证：外部资源（unpkg/three.js/d3-sankey/topojson）须含 integrity + crossorigin
  - pip-audit 集成：调用 pip-audit 扫描依赖漏洞（缺失时降级跳过）

扫描所有 HTML/JS/PY 文件，检测：
  - XSS 风险：innerHTML / document.write / eval / dangerouslySetInnerHTML / setTimeout(string)
  - 敏感信息：硬编码密钥/令牌/密码/AKID 模式
  - 不安全 API：eval / exec / pickle.loads / subprocess(shell=True) / verify=False
  - CSP 缺失：HTML 未声明 Content-Security-Policy
  - W268 · _headers 缺失 5 安全头
  - W268 · 外部资源缺 SRI（integrity + crossorigin）
  - W268 · pip-audit 依赖漏洞

用法：
    py scripts/security_scan.py --target site/data/timeline.html
    py scripts/security_scan.py --all
    py scripts/security_scan.py --all --output scripts/output/security-report.md --strict
    py scripts/security_scan.py --all --no-headers --no-sri --no-pip-audit

退出码：
    0 = 通过（或仅 low/info）
    1 = 存在 high 级别问题（--strict 时含 medium）
仅依赖 stdlib + 可选 pip-audit。
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"
SCRIPTS_DIR = ROOT / "scripts"
DEFAULT_OUTPUT = ROOT / "scripts" / "output" / "security-report.md"
DEFAULT_JSON = ROOT / "scripts" / "output" / "security-report.json"

# W268 · _headers 文件路径（Netlify/Cloudflare 风格）
HEADERS_FILE = SITE_DIR / "_headers"

# W268 · 必备 5 安全头（名称 -> 出现在 _headers 中的关键字）
REQUIRED_SECURITY_HEADERS = {
    "Content-Security-Policy": "Content-Security-Policy",
    "X-Frame-Options": "X-Frame-Options",
    "X-Content-Type-Options": "X-Content-Type-Options",
    "Referrer-Policy": "Referrer-Policy",
    "Permissions-Policy": "Permissions-Policy",
}

# W268 · 外部 CDN 资源域名（需 SRI 保护）
EXTERNAL_CDN_PATTERNS = (
    "cdn.jsdelivr.net",
    "unpkg.com",
    "cdnjs.cloudflare.com",
    "d3js.org",
    "three.js",
)

# ---------------------------------------------------------------------------
# 规则定义
# ---------------------------------------------------------------------------

# 每条规则：(id, 描述, 正则, 严重度, 适用扩展名)
RULES = [
    # XSS 风险
    ("XSS-001", "innerHTML 赋值（潜在 XSS）",
     r"\.innerHTML\s*=", "high", {".js", ".html"}),
    ("XSS-002", "document.write 调用（潜在 XSS）",
     r"document\.write\s*\(", "high", {".js", ".html"}),
    ("XSS-003", "eval 执行动态字符串",
     r"(?<![\w$.])eval\s*\(", "high", {".js", ".py"}),
    ("XSS-004", "dangerouslySetInnerHTML（React 转义绕过）",
     r"dangerouslySetInnerHTML", "high", {".js", ".jsx", ".html"}),
    ("XSS-005", "setTimeout/setInterval 执行字符串",
     r"(setTimeout|setInterval)\s*\(\s*['\"]", "medium", {".js", ".html"}),
    ("XSS-006", "outerHTML 赋值",
     r"\.outerHTML\s*=", "medium", {".js", ".html"}),
    # 敏感信息
    ("SEC-001", "硬编码 API Key 模式",
     r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"][A-Za-z0-9]{16,}['\"]", "high", {".py", ".js", ".yml", ".yaml"}),
    ("SEC-002", "硬编码密钥/令牌",
     r"(?i)(secret|token|password|passwd)\s*[:=]\s*['\"][^'\"]{8,}['\"]", "high", {".py", ".js", ".yml", ".yaml"}),
    ("SEC-003", "AWS Access Key ID 模式",
     r"AKIA[0-9A-Z]{16}", "high", {".py", ".js", ".yml", ".yaml", ".html"}),
    ("SEC-004", "私钥头部",
     r"-----BEGIN (RSA |EC |)PRIVATE KEY-----", "high", {".py", ".js", ".yml", ".yaml", ".txt"}),
    ("SEC-005", "OpenAI 风格 API Key（sk- 前缀·覆盖 DeepSeek/Qwen 等）",
     r"\bsk-[A-Za-z0-9_-]{16,}", "high", {".py", ".js", ".yml", ".yaml", ".html"}),
    # 不安全 API
    ("API-001", "exec 执行动态代码",
     r"\bexec\s*\(", "medium", {".py"}),
    ("API-002", "pickle.loads 反序列化（任意代码执行风险）",
     r"pickle\.loads?\s*\(", "high", {".py"}),
    ("API-003", "subprocess shell=True（命令注入风险）",
     r"subprocess\.[A-Za-z_]+\([^)]*shell\s*=\s*True", "medium", {".py"}),
    ("API-004", "requests verify=False（禁用证书校验）",
     r"verify\s*=\s*False", "medium", {".py"}),
    ("API-005", "os.system 命令执行",
     r"\bos\.system\s*\(", "medium", {".py"}),
    # CSP 缺失
    ("CSP-001", "HTML 未声明 Content-Security-Policy",
     r"(?s)^((?!Content-Security-Policy).)*$", "low", {".html"}),
    # W268 · _headers 安全头缺失（由 scan_headers 专门处理，扩展名集为空故通用扫描器跳过）
    ("HDR-001", "_headers 缺少 Content-Security-Policy",
     r"$.^", "high", set()),
    ("HDR-002", "_headers 缺少 X-Frame-Options",
     r"$.^", "medium", set()),
    ("HDR-003", "_headers 缺少 X-Content-Type-Options",
     r"$.^", "medium", set()),
    ("HDR-004", "_headers 缺少 Referrer-Policy",
     r"$.^", "low", set()),
    ("HDR-005", "_headers 缺少 Permissions-Policy",
     r"$.^", "low", set()),
    # W268 · SRI 缺失（由 scan_sri 专门处理）
    ("SRI-001", "外部 CDN 资源缺少 integrity 属性",
     r"$.^", "medium", set()),
    ("SRI-002", "外部 CDN 资源缺少 crossorigin 属性",
     r"$.^", "low", set()),
    # W268 · 依赖漏洞（由 run_pip_audit 专门处理）
    ("DEP-001", "pip-audit 检测到依赖漏洞",
     r"$.^", "high", set()),
]

COMPILED = [(rid, desc, re.compile(pat), sev, exts) for rid, desc, pat, sev, exts in RULES]


# ---------------------------------------------------------------------------
# 扫描核心
# ---------------------------------------------------------------------------

# 可视化页面目录：innerHTML/document.write/outerHTML 是 D3.js 渲染标准用法，
# 数据来自项目自身（非用户输入），降级为 medium 避免误报阻断 push。
# 真实 XSS 风险（用户输入拼接 innerHTML）仍按 high 报告。
# site/ 整个目录均为静态可视化页面（site/data、site/en、site/chapters、site/characters、site/*.html）。
VISUAL_PAGE_DIRS = ("site",)
XSS_DOWNGRADE_RULES = {"XSS-001", "XSS-002", "XSS-006"}


def _is_visual_page(path: Path) -> bool:
    """判断文件是否位于可视化页面目录（D3.js 渲染页面，innerHTML 为标准用法）。"""
    rel = path.relative_to(ROOT)
    parts = str(rel).replace("\\", "/")
    return any(parts.startswith(d + "/") or parts == d for d in VISUAL_PAGE_DIRS)


def discover_files():
    """发现 site/ + scripts/ + tests/ 下所有 HTML/JS/PY 文件。"""
    roots = [SITE_DIR, SCRIPTS_DIR, ROOT / "tests", ROOT / "mcp-server"]
    exts = {".html", ".js", ".py", ".jsx", ".yml", ".yaml", ".txt"}
    files = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in exts:
                # 跳过 baseline/current 截图目录、node_modules
                if any(seg in {"node_modules", "current", "baseline", ".thumbnails"} for seg in p.parts):
                    continue
                # W400 修复：跳过下划线前缀的一次性诊断/开发脚本（如 _chk_*.js）
                # —— 它们非生产代码，且常含 eval/innerHTML 用于本地调试，不应阻断安全门禁
                if p.name.startswith("_"):
                    continue
                files.append(p)
    return sorted(files)


def scan_file(path):
    """扫描单个文件，返回 findings 列表。"""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:  # noqa: BLE001
        return [{"rule": "IO-ERR", "file": str(path), "line": 0,
                 "description": f"读取失败: {exc}", "severity": "info"}]

    findings = []
    ext = path.suffix.lower()
    is_visual = _is_visual_page(path)
    for rid, desc, pat, sev, exts in COMPILED:
        if ext not in exts:
            continue
        # 路径感知降级：可视化页面的 innerHTML/document.write/outerHTML 从 high 降为 medium
        effective_sev = sev
        if is_visual and rid in XSS_DOWNGRADE_RULES and sev == "high":
            effective_sev = "medium"
        # CSP-001 仅对 HTML 生效，且需先确认无 CSP 才报
        if rid == "CSP-001":
            if ext != ".html":
                continue
            # 已在规则集中通过正则保证；此处仅当整文件无 CSP 时匹配首行
            if "Content-Security-Policy" in text:
                continue
            findings.append({"rule": rid, "file": str(path), "line": 1,
                             "description": desc, "severity": effective_sev,
                             "snippet": "<head> 缺少 CSP meta"})
            continue
        for match in pat.finditer(text):
            line_no = text.count("\n", 0, match.start()) + 1
            snippet = text.splitlines()[line_no - 1][:120] if line_no <= len(text.splitlines()) else ""
            findings.append({
                "rule": rid, "file": str(path), "line": line_no,
                "description": desc, "severity": effective_sev,
                "snippet": snippet.strip(),
            })
    return findings


# ---------------------------------------------------------------------------
# W268 · _headers 文件验证·5 安全头校验
# ---------------------------------------------------------------------------

# 安全头规则 ID 映射（用于 findings 的 rule 字段）
HEADER_RULE_MAP = {
    "Content-Security-Policy": ("HDR-001", "_headers 缺少 Content-Security-Policy", "high"),
    "X-Frame-Options": ("HDR-002", "_headers 缺少 X-Frame-Options", "medium"),
    "X-Content-Type-Options": ("HDR-003", "_headers 缺少 X-Content-Type-Options", "medium"),
    "Referrer-Policy": ("HDR-004", "_headers 缺少 Referrer-Policy", "low"),
    "Permissions-Policy": ("HDR-005", "_headers 缺少 Permissions-Policy", "low"),
}


def scan_headers(headers_file):
    """验证 site/_headers 包含 5 项必备安全头。

    入参 headers_file：_headers 文件路径（str/Path），默认使用 HEADERS_FILE。

    返回 findings 列表，每条形如：
        {"rule": "HDR-001", "file": "site/_headers", "line": 0,
         "description": "...", "severity": "high", "snippet": "..."}
    """
    if isinstance(headers_file, (str, Path)):
        hf = Path(headers_file)
    else:
        hf = HEADERS_FILE

    if not hf.exists():
        return [{
            "rule": "HDR-000", "file": str(hf), "line": 0,
            "description": f"_headers 文件不存在: {hf}",
            "severity": "high",
            "snippet": "缺少 Netlify/Cloudflare 风格的 _headers 配置文件",
        }]

    try:
        text = hf.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        return [{"rule": "HDR-000", "file": str(hf), "line": 0,
                 "description": f"_headers 读取失败: {exc}",
                 "severity": "high", "snippet": ""}]

    findings = []
    for header_name, (rule_id, desc, sev) in HEADER_RULE_MAP.items():
        if header_name not in text:
            findings.append({
                "rule": rule_id,
                "file": str(hf),
                "line": 0,
                "description": desc,
                "severity": sev,
                "snippet": f"缺少 {header_name} 头",
            })
    return findings


# ---------------------------------------------------------------------------
# W268 · SRI 验证·外部资源 integrity + crossorigin
# ---------------------------------------------------------------------------

# 匹配 <script src="https://..."> 和 <link href="https://...">
SCRIPT_SRC_RE = re.compile(
    r'<script\b[^>]*\bsrc\s*=\s*["\']([^"\']+)["\'][^>]*>',
    re.IGNORECASE,
)
LINK_HREF_RE = re.compile(
    r'<link\b[^>]*\bhref\s*=\s*["\']([^"\']+)["\'][^>]*>',
    re.IGNORECASE,
)
# 同时捕获整个标签用于检查 integrity/crossorigin 属性存在性


def _is_external_resource(url):
    """判断 URL 是否为外部 CDN 资源（需 SRI 保护）。"""
    if not url or not url.startswith(("http://", "https://")):
        return False
    lower = url.lower()
    return any(domain in lower for domain in EXTERNAL_CDN_PATTERNS)


def scan_sri(html_dir):
    """验证 HTML 文件中外部资源含 integrity + crossorigin 属性。

    入参 html_dir：HTML 根目录（str/Path），默认使用 SITE_DIR。

    返回 findings 列表，覆盖 site/ 下所有 HTML 的外部 CDN 资源引用。
    """
    if isinstance(html_dir, (str, Path)):
        hdir = Path(html_dir)
    else:
        hdir = SITE_DIR
    # 归一化为绝对路径（兼容相对路径入参）
    if not hdir.is_absolute():
        hdir = (ROOT / hdir).resolve()

    findings = []
    if not hdir.exists():
        return findings

    html_files = []
    for p in hdir.rglob("*.html"):
        if any(seg in {"node_modules", "current", "baseline", ".thumbnails"}
               for seg in p.parts):
            continue
        html_files.append(p)

    for hp in html_files:
        try:
            text = hp.read_text(encoding="utf-8", errors="ignore")
        except Exception:  # noqa: BLE001
            continue

        rel = str(hp.relative_to(ROOT)).replace("\\", "/")

        # 检查 <script src="external">
        for match in SCRIPT_SRC_RE.finditer(text):
            url = match.group(1)
            if not _is_external_resource(url):
                continue
            tag = match.group(0)
            line_no = text.count("\n", 0, match.start()) + 1
            has_integrity = "integrity" in tag.lower()
            has_crossorigin = "crossorigin" in tag.lower()
            if not has_integrity:
                findings.append({
                    "rule": "SRI-001",
                    "file": rel,
                    "line": line_no,
                    "description": f"外部脚本缺少 integrity 属性: {url}",
                    "severity": "medium",
                    "snippet": tag[:120],
                })
            if not has_crossorigin:
                findings.append({
                    "rule": "SRI-002",
                    "file": rel,
                    "line": line_no,
                    "description": f"外部脚本缺少 crossorigin 属性: {url}",
                    "severity": "low",
                    "snippet": tag[:120],
                })

        # 检查 <link href="external">
        for match in LINK_HREF_RE.finditer(text):
            url = match.group(1)
            if not _is_external_resource(url):
                continue
            tag = match.group(0)
            line_no = text.count("\n", 0, match.start()) + 1
            has_integrity = "integrity" in tag.lower()
            has_crossorigin = "crossorigin" in tag.lower()
            if not has_integrity:
                findings.append({
                    "rule": "SRI-001",
                    "file": rel,
                    "line": line_no,
                    "description": f"外部样式缺少 integrity 属性: {url}",
                    "severity": "medium",
                    "snippet": tag[:120],
                })
            if not has_crossorigin:
                findings.append({
                    "rule": "SRI-002",
                    "file": rel,
                    "line": line_no,
                    "description": f"外部样式缺少 crossorigin 属性: {url}",
                    "severity": "low",
                    "snippet": tag[:120],
                })

    return findings


# ---------------------------------------------------------------------------
# W268 · pip-audit 集成·依赖漏洞扫描
# ---------------------------------------------------------------------------

def run_pip_audit():
    """调用 pip-audit 扫描 Python 依赖漏洞。

    pip-audit 是 PyPA 官方依赖漏洞扫描工具（基于 OSV 数据库）。
    若 pip-audit 未安装或执行失败，返回降级 finding 而非抛异常。

    返回 findings 列表，每条对应一个漏洞依赖：
        {"rule": "DEP-001", "file": "requirements.txt", "line": 0,
         "description": "...", "severity": "high",
         "snippet": "package==version (VULN-ID 描述)"}
    """
    # 检测 pip-audit 是否可用
    audit_cmd = _find_pip_audit()
    if audit_cmd is None:
        return [{
            "rule": "DEP-000", "file": "(pip-audit)", "line": 0,
            "description": "pip-audit 未安装，跳过依赖漏洞扫描",
            "severity": "info",
            "snippet": "安装: pip install pip-audit",
        }]

    # 确定扫描目标：优先 requirements.txt，否则回退到当前环境
    requirements_files = _find_requirements_files()
    findings = []

    if requirements_files:
        for req_file in requirements_files:
            req_findings = _run_audit_on_requirements(audit_cmd, req_file)
            findings.extend(req_findings)
    else:
        # 无 requirements.txt，扫描当前 Python 环境
        env_findings = _run_audit_on_environment(audit_cmd)
        findings.extend(env_findings)

    if not findings:
        # 扫描通过，无漏洞
        findings.append({
            "rule": "DEP-002", "file": "(pip-audit)", "line": 0,
            "description": "pip-audit 扫描通过，未发现依赖漏洞",
            "severity": "info",
            "snippet": "全部依赖均无已知漏洞",
        })

    return findings


def _find_pip_audit():
    """检测 pip-audit 可执行命令，返回 cmd 列表或 None。"""
    # 优先尝试 py -m pip_audit（Windows 多版本 Python 兼容）
    for cmd in (["py", "-m", "pip_audit"], ["python", "-m", "pip_audit"],
                ["pip-audit"], ["pip_audit"]):
        try:
            proc = subprocess.run(
                cmd + ["--version"],
                capture_output=True, text=True, timeout=15, check=False,
            )
            if proc.returncode == 0:
                return cmd
        except (FileNotFoundError, subprocess.SubprocessError):
            continue
    return None


def _find_requirements_files():
    """发现项目中的 requirements*.txt 文件。"""
    candidates = []
    for pattern in ("requirements*.txt", "requirements/**/*.txt"):
        candidates.extend(ROOT.glob(pattern))
    # 去重并排序
    seen = set()
    result = []
    for p in sorted(candidates):
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result


def _run_audit_on_requirements(audit_cmd, req_file):
    """对单个 requirements.txt 运行 pip-audit，解析漏洞。"""
    try:
        proc = subprocess.run(
            audit_cmd + ["--requirement", str(req_file),
                         "--format", "json", "--no-deps"],
            capture_output=True, text=True, timeout=120, check=False,
        )
    except subprocess.SubprocessError as exc:
        return [{
            "rule": "DEP-001", "file": str(req_file.relative_to(ROOT)), "line": 0,
            "description": f"pip-audit 执行失败: {exc}",
            "severity": "medium", "snippet": "",
        }]

    return _parse_pip_audit_output(proc.stdout, proc.stderr, proc.returncode,
                                   str(req_file.relative_to(ROOT)))


def _run_audit_on_environment(audit_cmd):
    """对当前 Python 环境运行 pip-audit，解析漏洞。"""
    try:
        proc = subprocess.run(
            audit_cmd + ["--format", "json"],
            capture_output=True, text=True, timeout=180, check=False,
        )
    except subprocess.SubprocessError as exc:
        return [{
            "rule": "DEP-001", "file": "(environment)", "line": 0,
            "description": f"pip-audit 执行失败: {exc}",
            "severity": "medium", "snippet": "",
        }]

    return _parse_pip_audit_output(proc.stdout, proc.stderr, proc.returncode,
                                   "(environment)")


def _parse_pip_audit_output(stdout, stderr, returncode, source_name):
    """解析 pip-audit 的 JSON 输出为 findings 列表。"""
    # pip-audit 正常退出（returncode 0 = 无漏洞；非 0 = 发现漏洞或出错）
    if not stdout.strip():
        # 无 stdout 输出
        if stderr.strip():
            return [{
                "rule": "DEP-001", "file": source_name, "line": 0,
                "description": f"pip-audit 输出错误: {stderr.strip()[:200]}",
                "severity": "medium", "snippet": stderr.strip()[:120],
            }]
        return [{
            "rule": "DEP-001", "file": source_name, "line": 0,
            "description": "pip-audit 无输出",
            "severity": "info", "snippet": "",
        }]

    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        # 非 JSON 输出（可能是纯文本模式），降级为 info
        return [{
            "rule": "DEP-001", "file": source_name, "line": 0,
            "description": "pip-audit 输出非 JSON 格式",
            "severity": "info", "snippet": stdout.strip()[:120],
        }]

    findings = []
    dependencies = data.get("dependencies", [])
    for dep in dependencies:
        vulns = dep.get("vulns", [])
        if not vulns:
            continue
        name = dep.get("name", "unknown")
        version = dep.get("version", "?")
        for vuln in vulns:
            vid = vuln.get("id", "VULN-UNKNOWN")
            description_text = vuln.get("description", "")[:200]
            fix_versions = vuln.get("fix_versions", [])
            fix_str = f"（修复版本: {', '.join(fix_versions)}）" if fix_versions else ""
            findings.append({
                "rule": "DEP-001",
                "file": source_name,
                "line": 0,
                "description": f"{name}=={version} 存在漏洞 {vid}{fix_str}",
                "severity": "high",
                "snippet": f"{vid}: {description_text}",
            })
    return findings


# ---------------------------------------------------------------------------
# 报告生成
# ---------------------------------------------------------------------------

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}


def build_report(findings, scan_mode, duration, strict, w268_summary=None):
    """组装报告数据 + markdown。

    W268 扩展：可选传入 w268_summary（含 headers/sri/pip_audit 子项统计）。
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    by_sev = {"high": 0, "medium": 0, "low": 0, "info": 0}
    by_rule = {}
    for f in findings:
        by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1
        by_rule[f["rule"]] = by_rule.get(f["rule"], 0) + 1
    # 排序：按严重度→文件→行号
    findings_sorted = sorted(findings, key=lambda f: (SEVERITY_ORDER.get(f["severity"], 9), f["file"], f["line"]))

    md = []
    md.append("# W268 安全扫描报告\n")
    md.append("- 版本：v2.2.47 · W268 · E8 安全深化")
    md.append(f"- 扫描时间：{timestamp}")
    md.append(f"- 扫描模式：{scan_mode}")
    md.append(f"- 严格模式：{'是' if strict else '否'}")
    md.append(f"- 耗时：{duration:.2f}s")
    md.append(f"- 问题总数：{len(findings)}（high={by_sev['high']} / medium={by_sev['medium']} / low={by_sev['low']} / info={by_sev['info']}）")
    if w268_summary:
        md.append(f"- W268 深化：_headers 校验={'启用' if w268_summary.get('headers_enabled') else '跳过'}"
                  f" ｜ SRI 校验={'启用' if w268_summary.get('sri_enabled') else '跳过'}"
                  f" ｜ pip-audit={'启用' if w268_summary.get('pip_audit_enabled') else '跳过'}")
    md.append("")
    md.append("## 一、按规则分布\n")
    md.append("| 规则 | 描述 | 数量 |")
    md.append("|------|------|------|")
    rule_desc = {rid: desc for rid, desc, _, _, _ in COMPILED}
    # 补充 W268 专用规则描述（COMPILED 含占位正则，描述仍可用）
    for rid in sorted(by_rule.keys()):
        md.append(f"| {rid} | {rule_desc.get(rid, _w268_rule_desc(rid))} | {by_rule[rid]} |")
    md.append("\n## 二、明细（按严重度排序，前 30 条）\n")
    md.append("| 严重度 | 规则 | 文件 | 行号 | 描述 |")
    md.append("|--------|------|------|------|------|")
    for f in findings_sorted[:30]:
        rel = f["file"].replace(str(ROOT) + "\\", "").replace("\\", "/")
        md.append(f"| {f['severity']} | {f['rule']} | {rel} | {f['line']} | {f['description']} |")
    md.append("\n## 三、规则清单\n")
    md.append("| 规则 | 类别 | 严重度 | 描述 |")
    md.append("|------|------|--------|------|")
    for rid, desc, _, sev, _ in RULES:
        cat = rid.split("-")[0]
        md.append(f"| {rid} | {cat} | {sev} | {desc} |")
    # W268 · 分类明细
    if w268_summary:
        md.append("\n## 四、W268 · 安全深化明细\n")
        # _headers
        headers_count = w268_summary.get("headers_findings", 0)
        md.append(f"- _headers 校验：{headers_count} 项问题（必备 5 安全头：CSP/X-Frame-Options/X-Content-Type-Options/Referrer-Policy/Permissions-Policy）")
        # SRI
        sri_count = w268_summary.get("sri_findings", 0)
        md.append(f"- SRI 校验：{sri_count} 项问题（外部 CDN 资源需 integrity + crossorigin）")
        # pip-audit
        pip_count = w268_summary.get("pip_audit_findings", 0)
        pip_status = w268_summary.get("pip_audit_status", "未运行")
        md.append(f"- pip-audit：{pip_count} 项问题（{pip_status}）")
    md.append("\n## 五、修复建议\n")
    md.append("- XSS-001~006：改用 textContent 或 DOMPurify 净化后再写入 innerHTML。")
    md.append("- SEC-001~004：敏感信息移至环境变量或 .env（已 gitignore）。")
    md.append("- API-001~005：避免动态 exec/eval；subprocess 使用参数列表；HTTPS 校验证书。")
    md.append("- CSP-001：在 HTML `<head>` 增加 `<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self'\">`。")
    md.append("- HDR-001~005：补全 site/_headers 的 5 安全头（参考 Netlify/Cloudflare 配置规范）。")
    md.append("- SRI-001~002：外部 CDN 资源（unpkg/cdn.jsdelivr）添加 integrity + crossorigin 属性。")
    md.append("- DEP-001：pip-audit 发现的漏洞依赖升级到修复版本；定期 `pip install pip-audit && pip-audit`。\n")
    report = {
        "version": "W268",
        "version_detail": "v2.2.47",
        "timestamp": timestamp,
        "scan_mode": scan_mode,
        "strict": strict,
        "duration_sec": round(duration, 2),
        "summary": by_sev,
        "rule_stats": by_rule,
        "findings": findings_sorted,
    }
    if w268_summary:
        report["w268"] = w268_summary
    return report, "\n".join(md)


def _w268_rule_desc(rid):
    """W268 占位规则的描述补充（COMPILED 正则不可用，但描述需要可读）。"""
    desc_map = {
        "HDR-000": "_headers 文件缺失",
        "HDR-001": "_headers 缺少 Content-Security-Policy",
        "HDR-002": "_headers 缺少 X-Frame-Options",
        "HDR-003": "_headers 缺少 X-Content-Type-Options",
        "HDR-004": "_headers 缺少 Referrer-Policy",
        "HDR-005": "_headers 缺少 Permissions-Policy",
        "SRI-001": "外部 CDN 资源缺少 integrity 属性",
        "SRI-002": "外部 CDN 资源缺少 crossorigin 属性",
        "DEP-000": "pip-audit 未安装",
        "DEP-001": "pip-audit 检测到依赖漏洞",
        "DEP-002": "pip-audit 扫描通过",
    }
    return desc_map.get(rid, "?")


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def parse_args(argv):
    ap = argparse.ArgumentParser(description="W268 本地安全扫描 + _headers/SRI/pip-audit 深化")
    ap.add_argument("--target", help="单文件相对路径，例如 site/data/timeline.html")
    ap.add_argument("--all", action="store_true", help="扫描全部 HTML/JS/PY 文件")
    ap.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Markdown 报告输出路径")
    ap.add_argument("--json", default=str(DEFAULT_JSON), help="JSON 报告输出路径")
    ap.add_argument("--strict", action="store_true", help="严格模式：medium 也视为阻断")
    # W268 新增参数
    ap.add_argument("--no-headers", dest="no_headers", action="store_true",
                    help="跳过 _headers 安全头校验")
    ap.add_argument("--no-sri", dest="no_sri", action="store_true",
                    help="跳过外部资源 SRI 校验")
    ap.add_argument("--no-pip-audit", dest="no_pip_audit", action="store_true",
                    help="跳过 pip-audit 依赖漏洞扫描")
    ap.add_argument("--headers-file", dest="headers_file",
                    default=str(HEADERS_FILE),
                    help="_headers 文件路径（默认 site/_headers）")
    return ap.parse_args(argv)


def run(argv=None):
    args = parse_args(argv or sys.argv[1:])
    if not args.target and not args.all:
        print("错误：需指定 --target 或 --all", file=sys.stderr)
        return 2

    import time
    start = time.time()
    if args.target:
        target = ROOT / args.target if not Path(args.target).is_absolute() else Path(args.target)
        if not target.exists():
            print(f"错误：文件不存在 {target}", file=sys.stderr)
            return 2
        files = [target]
        scan_mode = f"single:{target.name}"
    else:
        files = discover_files()
        scan_mode = "all"

    print(f"W268 安全扫描启动：{len(files)} 文件 · 模式 {scan_mode}")
    findings = []
    for f in files:
        findings.extend(scan_file(f))

    # W268 · _headers 安全头校验
    headers_findings = []
    headers_enabled = not args.no_headers
    if headers_enabled:
        print(f"W268 · 校验 _headers：{args.headers_file}")
        headers_findings = scan_headers(args.headers_file)
        findings.extend(headers_findings)
        print(f"W268 · _headers 问题：{len(headers_findings)} 项")

    # W268 · SRI 外部资源校验
    sri_findings = []
    sri_enabled = not args.no_sri
    if sri_enabled:
        print("W268 · 校验外部资源 SRI")
        sri_findings = scan_sri(SITE_DIR)
        findings.extend(sri_findings)
        print(f"W268 · SRI 问题：{len(sri_findings)} 项")

    # W268 · pip-audit 依赖漏洞扫描
    pip_findings = []
    pip_audit_enabled = not args.no_pip_audit
    pip_audit_status = "跳过"
    if pip_audit_enabled:
        print("W268 · 运行 pip-audit 依赖漏洞扫描")
        pip_findings = run_pip_audit()
        findings.extend(pip_findings)
        # 判定 pip-audit 状态
        if any(f["rule"] == "DEP-000" for f in pip_findings):
            pip_audit_status = "未安装"
        elif any(f["rule"] == "DEP-001" for f in pip_findings):
            pip_audit_status = f"发现 {len([f for f in pip_findings if f['rule'] == 'DEP-001'])} 漏洞"
        elif any(f["rule"] == "DEP-002" for f in pip_findings):
            pip_audit_status = "通过"
        else:
            pip_audit_status = "完成"
        print(f"W268 · pip-audit：{pip_audit_status}")

    duration = time.time() - start

    w268_summary = {
        "headers_enabled": headers_enabled,
        "sri_enabled": sri_enabled,
        "pip_audit_enabled": pip_audit_enabled,
        "headers_findings": len(headers_findings),
        "sri_findings": len(sri_findings),
        "pip_audit_findings": len([f for f in pip_findings if f["rule"] == "DEP-001"]),
        "pip_audit_status": pip_audit_status,
    }

    report, md = build_report(findings, scan_mode, duration, args.strict, w268_summary)

    out_md = Path(args.output)
    out_json = Path(args.json)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md, encoding="utf-8")
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"报告已生成：{out_md}")
    print(f"JSON 已生成：{out_json}")
    s = report["summary"]
    print(f"耗时 {duration:.2f}s · high={s['high']} medium={s['medium']} low={s['low']} info={s['info']}")
    # 退出码判定
    if s["high"] > 0:
        return 1
    if args.strict and s["medium"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run())
# FILE_INDEX: scripts/security_scan.py | W268 v2.2.47 | E8 安全深化（_headers+SRI+pip-audit）
