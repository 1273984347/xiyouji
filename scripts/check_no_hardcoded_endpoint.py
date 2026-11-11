#!/usr/bin/env python3
"""check_no_hardcoded_endpoint.py — 产物面「服务端地址硬编码」守卫（W1205 · 契约 C-8）

判定目标（架构方案 v2 §10.6 / §5.4 禁止依赖形态 #8）：
  静态产物（L2）不得内嵌 L3 的服务地址——回环地址、内网 IP、裸域名服务地址都算。
  产物里允许出现的只有三种形态：
    ① 构建期占位符（__XIJ_SERVICE_BASE__，待部署期注入）；
    ② 部署期注入后的「已声明」地址（须以 --expected-endpoint / XIJ_SERVICE_BASE 声明）；
    ③ 开发者本机专用构建（文件内须带显式标记 xij-build-profile:developer-local，
       且标记里写明注入的地址——豁免必须可审计）。
  禁止依赖形态 #8 的原话：「L2 产物中出现服务地址即视为产物反向成为部署事实」。

用法（仓内三档归位：本脚本属「跨批复用判据」⇒ 转正到 scripts/ 顶层·无 _ 前缀）：
  py -3 scripts/check_no_hardcoded_endpoint.py                          # 扫 site/
  py -3 scripts/check_no_hardcoded_endpoint.py --root site --json out.json
  py -3 scripts/check_no_hardcoded_endpoint.py --expected-endpoint https://rag.example.com
  py -3 scripts/check_no_hardcoded_endpoint.py --strict                 # 连「提及」也判红
  py -3 scripts/check_no_hardcoded_endpoint.py --self-test              # 负样本自证

退出码：0 = 无违规；1 = 有违规；2 = 自测失败 / 用法错误。

术语：
  violation = 服务地址（scheme URL 或 host:port）落在非法形态上 ⇒ 判红
  mention   = 裸主机名提及（无 scheme、无端口）⇒ 不是服务地址，默认只登记不判红
  pattern   = 命中在正则字面量内（本地地址检测模式）⇒ 不是服务地址
"""

import argparse
import json
import os
import re
import sys
import tempfile

# ---------------------------------------------------------------- 常量

#: 构建期占位符（与 scripts/inject_service_endpoint.py 一致）。
PLACEHOLDER = "__XIJ_SERVICE_BASE__"

#: 开发者本机专用构建的显式标记（产物内可见·豁免凭此放行）。
DEV_LOCAL_MARKER = "xij-build-profile:developer-local"

#: 公开主机白名单（W1205 实测产物面 1045 个文本文件的全量 URL 主机分布得出·15 个）。
#: 新增外域须经复核再入列——否则一律判红（防止产物悄悄长出新的外域依赖）。
PUBLIC_HOST_ALLOWLIST = frozenset({
    "1273984347.github.io",
    "github.com",
    "api.github.com",
    "1273984347.goatcounter.com",
    "www.goatcounter.com",
    "www.w3.org",
    "gsap.com",
    "schema.org",
    "creativecommons.org",
    "d3js.org",
    "www.sitemaps.org",
    "developers.cloudflare.com",
    "docs.netlify.com",
    "cdnjs.cloudflare.com",
    "opensource.org",
})

#: 文本文件扩展名（其余按二进制跳过·避免把图片当文本扫）。
TEXT_EXTS = frozenset({
    ".html", ".htm", ".xhtml", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".css", ".json", ".md", ".txt", ".xml", ".svg", ".webmanifest", ".map",
    ".yml", ".yaml", ".ini", ".cfg", ".conf", ".htaccess",
})

#: 扫描时跳过的目录。
SKIP_DIRS = frozenset({".git", "node_modules", ".venv", "__pycache__", ".cache"})

#: URL（带 scheme）匹配：取 host 与可选端口。
URL_RE = re.compile(
    r"(?P<scheme>https?|wss?|ftp)://(?P<host>\[[0-9A-Fa-f:]+\]|[A-Za-z0-9._~%\-]+)(?::(?P<port>\d{1,5}))?"
)

#: 裸主机（无 scheme）：主机名 + 可选端口。
BARE_HOST_RE = re.compile(
    r"(?<![\w./\-])"
    r"(?P<host>localhost|127\.\d{1,3}\.\d{1,3}\.\d{1,3}|0\.0\.0\.0|"
    r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|"
    r"172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|169\.254\.\d{1,3}\.\d{1,3})"
    r"(?::(?P<port>\d{1,5}))?"
)

#: CSP 指令（命中即「浏览器真连」的位置）。
CSP_KEYS = (
    "default-src", "connect-src", "script-src", "style-src", "img-src",
    "font-src", "frame-src", "worker-src", "media-src", "manifest-src",
    "prefetch-src", "form-action", "base-uri",
)

#: 网络调用位置（命中即「浏览器真连」的位置）。
NETWORK_TOKENS = (
    "fetch(", "XMLHttpRequest", ".open(", "WebSocket", "EventSource",
    "sendBeacon", "src=", "href=", "url(", "@import", "importScripts",
    "serviceWorker.register", "new Image("
)

#: 正则字面量前置关键字（判定斜杠起的是正则而非除号）。
REGEX_KEYWORDS = (
    "return", "typeof", "case", "in", "of", "new", "delete", "void",
    "do", "else", "yield", "await", "instanceof",
)


# ---------------------------------------------------------------- 工具

def classify_host(host):
    """把主机名分类：loopback / private / link_local / public_allowed / bare_domain。"""
    h = (host or "").strip().lower().rstrip(".,;:")
    if h in ("localhost", "0.0.0.0", "::1", "[::1]"):
        return "loopback"
    if re.match(r"^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$", h):
        return "loopback"
    if re.match(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$", h):
        return "private"
    if re.match(r"^192\.168\.\d{1,3}\.\d{1,3}$", h):
        return "private"
    if re.match(r"^172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}$", h):
        return "private"
    if re.match(r"^169\.254\.\d{1,3}\.\d{1,3}$", h):
        return "link_local"
    if h in PUBLIC_HOST_ALLOWLIST:
        return "public_allowed"
    return "bare_domain"


def host_port(host, port):
    """拼 host:port 形态（用于与期望地址比对）。"""
    h = (host or "").strip().lower().rstrip(".,;:")
    return h + (":" + port if port else "")


def endpoint_key(url):
    """把期望地址归一为 host:port（去 scheme·去尾斜杠·去路径）。"""
    if not url:
        return ""
    m = re.match(r"^[A-Za-z][A-Za-z0-9+\-]*://(?P<host>[^/?#]+)", url.strip())
    if not m:
        return url.strip().lower().rstrip("/")
    return m.group("host").lower().rstrip("/")


def _prev_code_char(text, i):
    """返回 i 之前最近的非空白字符及其位置。"""
    j = i - 1
    while j >= 0 and text[j] in " \t\r\n":
        j -= 1
    return (text[j] if j >= 0 else ""), j


def _is_regex_start(text, i):
    """斜杠处是否开启一个正则字面量。"""
    # 方案分隔符（http://）不是正则起点——否则会把 URL 里的 // 吞成正则区间（真违规被假绿）。
    if i >= 2 and text[i - 1] == ":" and text[i - 2] == ":":
        return False
    prev, j = _prev_code_char(text, i)
    if prev == "":
        return True
    # 注意：< 与 > 不入列——HTML 闭合标签（</code>）会让后面整行被当成正则区间，
    # 把真违规吞成「检测模式」（W1205 实测：en/cave-estate.html 与 en/material-archaeology.html 曾因此假绿）。
    if prev in "(,=:[!&|?{};+-*%^~":
        return True
    if prev.isalpha():
        word = ""
        k = j
        while k >= 0 and (text[k].isalnum() or text[k] == "_"):
            word = text[k] + word
            k -= 1
        return word.lower() in REGEX_KEYWORDS
    return False


def _find_regex_end(text, i):
    """从正则起点找闭合斜杠（返回闭合位置+1；找不到返回 None）。"""
    n = len(text)
    k = i + 1
    in_class = False
    while k < n:
        c = text[k]
        if c == "\\":
            k += 2
            continue
        if c == "[":
            in_class = True
        elif c == "]":
            in_class = False
        elif c == "/" and not in_class:
            # 斜杠斜杠 / 斜杠星号 ⇒ 命中的是注释起点，不是正则闭合 ⇒ 该处不成正则区间。
            if k + 1 < n and text[k + 1] in "/*":
                return None
            return k + 1
        elif c == "\n":
            return None
        k += 1
    return None


def _skip_string(text, i, quote):
    """跳过字符串字面量，返回闭合引号之后的下标。"""
    n = len(text)
    j = i
    while j < n:
        if text[j] == "\\":
            j += 2
            continue
        if text[j] == quote:
            break
        j += 1
    return min(j + 1, n)


def _skip_line_comment(text, i):
    """跳过行注释，返回下一行起点。"""
    j = text.find("\n", i)
    return len(text) if j < 0 else j + 1


def _skip_block_comment(text, i):
    """跳过块注释，返回其后下标。"""
    j = text.find("*/", i)
    return len(text) if j < 0 else j + 2


def _scan_slash(text, i, spans):
    """处理斜杠：行注释 / 块注释 / 正则字面量 / 普通字符。返回下一个下标。"""
    if text.startswith("//", i):
        return _skip_line_comment(text, i + 2)
    if text.startswith("/*", i):
        return _skip_block_comment(text, i + 2)
    if _is_regex_start(text, i):
        end = _find_regex_end(text, i)
        if end is not None:
            spans.append((i, end))
            return end
    return i + 1


def find_regex_spans(text):
    """找出正则字面量的字符区间（本地地址检测模式不该判红）。

    实现：按 JS 词法逐段走——字符串与注释内的斜杠不算正则起点，方案分隔符（://）也不算。
    （W1205 实测：首版未跳过字符串，把 870 处公开 URL 误判成正则区间 ⇒ 8 个含真违规的文件被假绿吞掉；
     次版把 HTML 闭合标签 </code> 当成正则起点 ⇒ 另有 2 个文件假绿。本版两处均已根修。）
    """
    spans = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c in "\"'`":
            i = _skip_string(text, i + 1, c)
            continue
        if c == "/":
            i = _scan_slash(text, i, spans)
            continue
        i += 1
    return spans


def in_spans(offset, spans):
    """偏移量是否落在正则字面量区间内。"""
    for start, end in spans:
        if start <= offset < end:
            return True
    return False


def line_col(text, offset):
    """返回偏移量所在行号（1 起）与列号（1 起）。"""
    line = text.count("\n", 0, offset) + 1
    line_start = text.rfind("\n", 0, offset) + 1
    return line, offset - line_start + 1


def role_of(line_text):
    """判定命中所在位置的角色：csp / network / prose。"""
    low = line_text.lower()
    if any(k in low for k in CSP_KEYS):
        return "csp"
    if any(t in low for t in NETWORK_TOKENS):
        return "network"
    return "prose"


def parse_dev_local_marker(text):
    """解析开发者本机专用构建标记，返回 (endpoint, marker_line) 或 (None, None)。

    标记形态：xij-build-profile:developer-local endpoint=http://127.0.0.1:8777
    """
    for raw_line in text.splitlines():
        if DEV_LOCAL_MARKER in raw_line:
            m = re.search(r"endpoint=(\S+)", raw_line)
            return (m.group(1) if m else ""), raw_line.strip()
    return None, None


def iter_text_files(root):
    """遍历 root 下可读文本文件（跳过二进制扩展名与隐藏目录）。"""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(filenames):
            ext = os.path.splitext(fn)[1].lower()
            if fn.startswith("_") and ext == "":
                ext = ".txt"
            if ext not in TEXT_EXTS and fn not in ("_headers", ".htaccess"):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, encoding="utf-8") as f:
                    yield path, f.read()
            except (OSError, UnicodeDecodeError):
                continue


# ---------------------------------------------------------------- 扫描

def _build_finding(rel_path, text, lines, m, host, port, expected_keys, exempt_allowed, marker_endpoint):
    """构造一条违规记录；返回 None 表示该命中合法（不判红）。"""
    host_class = classify_host(host)
    if host_class == "public_allowed":
        return None
    if PLACEHOLDER in (host or "") or PLACEHOLDER in m.group(0):
        return None
    line_no, col = line_col(text, m.start())
    line_text = lines[line_no - 1] if line_no - 1 < len(lines) else ""
    key = host_port(host, port)
    entry = {
        "file": rel_path,
        "line": line_no,
        "col": col,
        "host": (host or "").lower().rstrip(".,;:"),
        "port": port,
        "class": host_class,
        "role": role_of(line_text),
        "text": m.group(0)[:160],
        "line_text": line_text.strip()[:200],
    }
    if host_class in ("loopback", "private", "link_local"):
        if key in exempt_allowed:
            return None
        entry["reason"] = ("回环/内网地址未落在开发者本机专用构建标记内"
                           if marker_endpoint else "回环/内网地址硬编码（契约 C-8 禁止）")
        return entry
    if key in expected_keys:
        return None
    entry["reason"] = "裸域名服务地址未声明（须以 --expected-endpoint 声明为部署期注入结果）"
    return entry


def _record_pattern(rel_path, text, m, host, patterns):
    """记录正则字面量内的本地地址检测模式（不是服务地址·只登记）。"""
    patterns.append({
        "file": rel_path,
        "line": line_col(text, m.start())[0],
        "host": (host or "").lower(),
        "text": m.group(0)[:120],
        "note": "正则字面量内的本地地址检测模式·非服务地址",
    })


def scan_text(rel_path, text, expected_keys, strict):
    """扫描单个文件，返回 (violations, mentions, patterns, exempt_info)。"""
    violations = []
    mentions = []
    patterns = []
    spans = find_regex_spans(text)
    marker_endpoint, marker_line = parse_dev_local_marker(text)
    exempt_allowed = set()
    if marker_endpoint:
        exempt_allowed.add(endpoint_key(marker_endpoint))
    lines = text.splitlines()

    def add(m, host, port):
        """把一条命中归类：检测模式 / 违规 / 合法。"""
        if in_spans(m.start(), spans):
            _record_pattern(rel_path, text, m, host, patterns)
            return
        entry = _build_finding(rel_path, text, lines, m, host, port,
                                expected_keys, exempt_allowed, marker_endpoint)
        if entry is not None:
            violations.append(entry)

    for m in URL_RE.finditer(text):
        add(m, m.group("host"), m.group("port"))

    for m in BARE_HOST_RE.finditer(text):
        host = m.group("host")
        port = m.group("port")
        if port:
            add(m, host, port)
            continue
        if not in_spans(m.start(), spans):
            mentions.append({
                "file": rel_path,
                "line": line_col(text, m.start())[0],
                "host": host.lower(),
                "text": m.group(0)[:80],
            })

    if strict:
        violations.extend(_strict_mentions(mentions))

    exempt_info = None
    if marker_endpoint:
        exempt_info = {"file": rel_path, "marker": marker_line, "endpoint": marker_endpoint}
    return violations, mentions, patterns, exempt_info


def _strict_mentions(mentions):
    """严格档：裸主机名「提及」也判红。"""
    return [{
        "file": item["file"],
        "line": item["line"],
        "col": 1,
        "host": item["host"],
        "port": None,
        "class": "mention",
        "role": "prose",
        "text": item["text"],
        "line_text": "",
        "reason": "严格档：裸主机名提及也判红",
    } for item in mentions]


def scan_roots(roots, expected_keys, strict=False):
    """扫描多个 root，汇总结果。"""
    violations = []
    mentions = []
    patterns = []
    exempted = []
    scanned = 0
    for root in roots:
        if not os.path.isdir(root):
            continue
        for path, text in iter_text_files(root):
            scanned += 1
            try:
                rel = os.path.relpath(path, os.getcwd())
            except ValueError:
                # 跨盘符（临时目录在别的卷）⇒ 退回绝对路径，不让自测炸在 relpath 上。
                rel = path
            rel = rel.replace("\\", "/")
            v, m, p, ex = scan_text(rel, text, expected_keys, strict)
            violations.extend(v)
            mentions.extend(m)
            patterns.extend(p)
            if ex:
                exempted.append(ex)
    return {
        "scanned_files": scanned,
        "violations": violations,
        "mentions": mentions,
        "patterns": patterns,
        "exempted": exempted,
    }


# ---------------------------------------------------------------- 自测

def self_test():
    """负样本自证：违规必红 / 合法形态必绿 / 豁免可审计。

    每次自证都在临时目录里造样本文件，跑完即删（不留痕）。
    """
    cases = []
    tmpdir = tempfile.mkdtemp(prefix="xij_endpoint_guard_")
    try:
        def write(name, content):
            p = os.path.join(tmpdir, name)
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
            return p

        write("violation.js", "const RAG_BASE = 'http://127.0.0.1:8777';\n")
        write("clean.js", "const RAG_BASE = '" + PLACEHOLDER + "';\n")
        write("devlocal.js",
              "/* " + DEV_LOCAL_MARKER + " endpoint=http://127.0.0.1:8777 */\n"
              "const RAG_BASE = 'http://127.0.0.1:8777';\n")
        write("pattern.js", "var RE = /^(localhost$|^127\\.)/;\n")
        write("expected.js", "const RAG_BASE = 'https://rag.example.com';\n")

        def run(names, expected_keys=()):
            res = scan_roots([tmpdir], set(expected_keys))
            return [v for v in res["violations"] if os.path.basename(v["file"]) in names]

        checks = [
            ("负样本·硬编码回环地址必红", len(run({"violation.js"})) == 1),
            ("正样本·占位符必绿", len(run({"clean.js"})) == 0),
            ("开发者本机专用构建豁免且可审计",
             len(run({"devlocal.js"})) == 0
             and any(os.path.basename(e["file"]) == "devlocal.js"
                     for e in scan_roots([tmpdir], set())["exempted"])),
            ("本地地址检测模式不算服务地址", len(run({"pattern.js"})) == 0),
            ("未声明的裸域名地址必红", len(run({"expected.js"})) == 1),
            ("已声明的部署地址必绿",
             len(run({"expected.js"}, {"rag.example.com"})) == 0),
        ]
        for name, ok in checks:
            cases.append((name, ok))
            print(("PASS  " if ok else "FAIL  ") + name)
        failed = [n for n, ok in cases if not ok]
        if failed:
            print("自测结论：失败 %d 例：%s" % (len(failed), "、".join(failed)))
        else:
            print("自测结论：全部通过（%d/%d）" % (len(cases), len(cases)))
        return 0 if not failed else 2
    finally:
        for fn in os.listdir(tmpdir):
            try:
                os.remove(os.path.join(tmpdir, fn))
            except OSError:
                pass
        try:
            os.rmdir(tmpdir)
        except OSError:
            pass


# ---------------------------------------------------------------- 入口

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="check_no_hardcoded_endpoint.py",
        description="产物面服务端地址硬编码守卫（W1205 · 契约 C-8）",
    )
    parser.add_argument("--root", action="append", default=None,
                        help="扫描根目录（可多次·默认 site）")
    parser.add_argument("--expected-endpoint", action="append", default=[],
                        help="已声明的部署期地址（可多次）")
    parser.add_argument("--json", default=None, help="结果 JSON 落盘路径")
    parser.add_argument("--strict", action="store_true",
                        help="严格档：裸主机名「提及」也判红")
    parser.add_argument("--self-test", action="store_true", help="负样本自证（造临时件·跑完即删）")
    parser.add_argument("--gate", action="store_true",
                        help="门禁模式：输出汇总行（第 70 槽挂载用·W1208）")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    roots = args.root or ["site"]
    expected = list(args.expected_endpoint)
    env_expected = os.environ.get("XIJ_SERVICE_BASE", "")
    if env_expected.strip():
        expected.extend([e.strip() for e in env_expected.split(",") if e.strip()])
    expected_keys = {endpoint_key(e) for e in expected if e}

    result = scan_roots(roots, expected_keys, strict=args.strict)
    report = {
        "ok": not result["violations"],
        "roots": roots,
        "expected_endpoints": sorted(expected_keys),
        "scanned_files": result["scanned_files"],
        "violation_count": len(result["violations"]),
        "violations": result["violations"],
        "mention_count": len(result["mentions"]),
        "mentions": result["mentions"],
        "pattern_count": len(result["patterns"]),
        "patterns": result["patterns"],
        "exempted": result["exempted"],
    }

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    print("扫描根：%s · 文本文件 %d 个" % (", ".join(roots), report["scanned_files"]))
    print("违规 %d · 提及 %d · 检测模式 %d · 豁免 %d"
          % (report["violation_count"], report["mention_count"],
             report["pattern_count"], len(report["exempted"])))
    for v in report["violations"]:
        print("  [违规] %s:%d:%d  %s  (%s/%s)  %s"
              % (v["file"], v["line"], v["col"], v["host"], v["class"], v["role"], v["reason"]))
    for e in report["exempted"]:
        print("  [豁免] %s  ← %s" % (e["file"], e["marker"]))
    if args.gate:
        # 第 70 槽汇总行（verify_delivery._StrictGate 依此判「确实执行过」·防静默跳过）
        print("---- 第 70 门禁 产物服务地址：违规 %d · %s ----"
              % (report["violation_count"], "OK" if report["ok"] else "FAIL"))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
