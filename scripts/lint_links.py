#!/usr/bin/env python3
"""lint_links.py — 站内/外链校验工具（纯标准库）。

整合 scripts/output/check_links.py（HTML href/src）与
scripts/audit/w053_verify_links.py（Markdown [text](url)）的能力。

检测范围：
  - HTML/HTM：所有 href / src 属性指向的资源
  - Markdown：所有 [text](url) 形式的链接（fenced code block 与 inline code span
    内不提取——代码中的 [\\\"\\'](--[\\w-]+) 形态会被链接正则误判，W699 实证）

豁免：
  - gitignore 本地产物（docs/S4 双盲件、tmpe/ 等）：git check-ignore 批量判定后剔除
  - 默认排除：node_modules / _template.html / docs/archive/（冻结历史档·禁擅改，其
    出链不修）——排除匹配以仓库相对路径为准

链接分类：
  - 站内（相对路径、纯锚点）：本地文件存在性校验
  - 外链（http/https/mailto/tel 等）：HTTP 探测（可选，默认跳过）

Usage:
    # 默认仅校验站内链接（扫描 site/）
    python scripts/lint_links.py
    # 仅站内
    python scripts/lint_links.py --internal
    # 仅外链
    python scripts/lint_links.py --external
    # 全部（站内 + 外链）
    python scripts/lint_links.py --all
    # 指定扫描目录
    python scripts/lint_links.py --dir site/
    # 自动修复相对路径错误（按 basename 唯一匹配重写）
    python scripts/lint_links.py --fix

Exit code: 0 全部通过 / 1 存在 broken 链接
"""
import argparse
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

ROOT = Path(__file__).resolve().parent.parent

# 视为外链 / 跳过本地校验的 scheme
EXTERNAL_SCHEMES = (
    "http://",
    "https://",
    "//",
    "mailto:",
    "tel:",
    "javascript:",
    "data:",
    "ftp:",
    "file:",
)

# Markdown 链接 [text](url) 或 [text](url "title")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

_FENCE_OPEN_RE = re.compile(r"^\s*(```|~~~)")


def strip_md_code(text):
    """剥离 fenced code block 与 inline code span（仅用于链接提取，W699）。

    代码内的 `[\"\\'](--[\\w-]+)` 形态会被 MD_LINK_RE 误判为链接（W699 实证 2 例）；
    行内 code span 中的路径/正则同样不是可点击链接。剥离以空行占位保行号。
    """
    out = []
    in_fence = False
    fence_char = ""
    for line in text.splitlines():
        m = _FENCE_OPEN_RE.match(line)
        if m:
            mark = m.group(1)
            if not in_fence:
                in_fence, fence_char = True, mark[0]
                out.append("")
                continue
            if mark[0] == fence_char:
                in_fence = False
                out.append("")
                continue
        out.append("" if in_fence else re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def filter_gitignored(files):
    """剔除 .gitignore 排除的本地产物（W699：docs/S4 双盲件曾被扫入 102 条噪音）。

    git check-ignore 批量判定；git 不可用/失败时原样返回（不阻断，CI 环境恒有 git）。
    """
    if not files:
        return files
    try:
        # 字节流显式 UTF-8：Windows text 模式 stdin 走 GBK，中文路径（docs/S4-学术投稿）
        # 编码错位会导致 check-ignore 永不命中（W699 实证）
        r = subprocess.run(
            ["git", "-c", "core.quotePath=false", "check-ignore", "--stdin"],
            input=("\n".join(str(f) for f in files) + "\n").encode("utf-8"),
            capture_output=True, timeout=60, cwd=str(ROOT),
        )
        def _norm(s):
            # check-ignore 对绝对路径走 C 引号：包裹引号 + 内部 \ 转义为 \\（W699 实证）
            return re.sub(r"/{2,}", "/", s.strip().strip('"').replace("\\", "/"))

        ignored = {
            _norm(ln)
            for ln in r.stdout.decode("utf-8", "replace").splitlines()
            if ln.strip()
        }
        if not ignored:
            return files
        kept = [f for f in files if _norm(str(f)) not in ignored]
        print(f"[gitignore] 已排除 {len(files) - len(kept)} 个 gitignore 本地件")
        return kept
    except Exception:
        return files


class HtmlLinkExtractor(HTMLParser):
    """提取 HTML 中所有 href / src，记录行号。"""

    def __init__(self):
        super().__init__()
        self.links = []  # list of (line_no, attr_name, raw_url)

    def _record(self, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.links.append((self.getpos()[0], name, value))

    def handle_starttag(self, tag, attrs):
        self._record(attrs)

    def handle_startendtag(self, tag, attrs):
        self._record(attrs)


def extract_markdown_links(text):
    """逐行扫描 Markdown，返回 (line_no, url) 列表。"""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        for m in MD_LINK_RE.finditer(line):
            out.append((i, m.group(2)))
    return out


def is_external(url):
    u = url.strip().lower()
    return u.startswith(EXTERNAL_SCHEMES)


def is_skip(url):
    u = url.strip()
    if not u:
        return True
    if u.startswith("#"):
        return True
    # POSIX 根绝对路径（W699）：Vite 工程入口（xiyouji-agent-web/index.html 的
    # /src/main.tsx）是构建期改写形态，不适用文件系统站点存在性校验
    if u.startswith("/"):
        return True
    return False


def strip_query_fragment(url):
    """剥离 query 与 fragment，返回 (path_part, rest)。"""
    # 先按 # 分 fragment
    if "#" in url:
        path_part, fragment = url.split("#", 1)
        fragment = "#" + fragment
    else:
        path_part, fragment = url, ""
    # 再按 ? 分 query
    if "?" in path_part:
        path_part, query = path_part.split("?", 1)
        query = "?" + query
    else:
        query = ""
    return path_part, query + fragment


def check_internal(base_file, raw_url):
    """校验站内链接。返回 (ok, resolved_path, display)。"""
    url = raw_url.strip()
    path_part, _rest = strip_query_fragment(url)
    if not path_part:
        # 纯锚点 → 指向当前文件，视 base 文件存在即 OK
        return (base_file.exists(), base_file, url)
    decoded = urllib.parse.unquote(path_part)
    target = (base_file.parent / decoded)
    try:
        target = target.resolve(strict=False)
    except Exception:
        pass
    ok = target.exists()
    return (ok, target, str(target))


def check_external(url, timeout=6):
    """外链 HTTP 探测：先 HEAD，失败则回退 GET。返回 (ok, info)。"""
    # W424：非 http(s) 协议（javascript:/mailto:/file: 等）不属外链，直接视为通过
    if not url.lower().startswith(("http://", "https://")):
        return (True, "非 http(s)，跳过")
    # W424：URL 含非 ASCII（中文路径）时先百分号编码，避免 urllib ascii 编码错误误报 broken
    import urllib.parse as _up
    url = _up.quote(url, safe=":/?#[]@!$&'()*+,;=%-._~")
    _u = _up.urlparse(url)
    if _u.scheme not in ("http", "https"):
        return (False, "non-http scheme")
    import ipaddress as _ipa
    import socket as _socket
    try:
        _infos = _socket.getaddrinfo(_u.hostname, None)
    except Exception as _e:
        return (False, "dns fail %s" % str(_e)[:60])
    for _info in _infos:
        _ip = _ipa.ip_address(_info[4][0])
        if _ip.is_private or _ip.is_loopback or _ip.is_link_local or _ip.is_reserved or _ip.is_multicast or _ip.is_unspecified:
            raise ValueError("blocked private/reserved address: %s" % _ip)
    headers = {"User-Agent": "lint_links/1.0 (+stdlib)"}
    # W536 安全加固：http.client 直连（经上方协议白名单 + 私网 IP 阻断后才可达此处）
    import http.client as _hc
    _pq = _up.urlparse(url)
    for method in ("HEAD", "GET"):
        _conn = None
        try:
            if _pq.scheme == "https":
                _conn = _hc.HTTPSConnection(_pq.hostname, timeout=timeout)
            else:
                _conn = _hc.HTTPConnection(_pq.hostname, timeout=timeout)
            _path = _pq.path or "/"
            if _pq.query:
                _path += "?" + _pq.query
            _conn.request(method, _path, headers=headers)
            _resp = _conn.getresponse()
            return (_resp.status < 400, "HTTP %d" % _resp.status)
        except ValueError as e:
            return (False, str(e)[:80])
        except Exception as e:
            if method == "HEAD":
                continue
            return (False, str(e)[:80])
        finally:
            if _conn is not None:
                _conn.close()
    return (False, "unreachable")


def find_by_basename(scan_root, basename):
    """在 scan_root 下按 basename 查找文件，返回匹配列表。"""
    matches = []
    for p in Path(scan_root).rglob("*"):
        if p.is_file() and p.name == basename:
            matches.append(p)
    return matches


def try_fix(base_file, raw_url, scan_root):
    """对 broken 站内链接尝试按 basename 唯一匹配重写相对路径。

    返回新 url 字符串；无法修复返回 None。
    """
    url = raw_url.strip()
    path_part, rest = strip_query_fragment(url)
    if not path_part:
        return None
    decoded = urllib.parse.unquote(path_part)
    basename = Path(decoded).name
    if not basename:
        return None
    matches = find_by_basename(scan_root, basename)
    if len(matches) != 1:
        return None
    target = matches[0]
    try:
        new_rel = os.path.relpath(target, base_file.parent).replace(os.sep, "/")
    except Exception:
        return None
    if new_rel == path_part:
        return None
    return new_rel + rest


def collect_files(scan_dir):
    base = Path(scan_dir)
    if not base.exists():
        return []
    exts = {".html", ".htm", ".md"}
    return sorted(p for p in base.rglob("*") if p.is_file() and p.suffix.lower() in exts)


def display_path(path):
    try:
        return str(Path(path).relative_to(ROOT)).replace("\\", "/")
    except Exception:
        return str(path)


def main():
    ap = argparse.ArgumentParser(
        description="链接校验工具：HTML href/src + Markdown 链接（纯标准库）"
    )
    ap.add_argument("--internal", action="store_true", help="校验站内链接（默认行为）")
    ap.add_argument(
        "--external", action="store_true", help="校验外链（默认跳过，需联网）"
    )
    ap.add_argument("--all", action="store_true", help="校验全部（站内 + 外链）")
    ap.add_argument("--dir", default="site", help="扫描目录（默认 site/）")
    ap.add_argument("--fix", action="store_true", help="自动修复相对路径错误（按 basename 唯一匹配）")
    ap.add_argument(
        "--exclude",
        nargs="*",
        default=["node_modules", "_template.html", "docs/archive/", "tmpe/",
                 "_w588_ce.html"],
        help="排除含这些路径片段的文件/目录，匹配仓库相对路径"
             "（默认 node_modules/_template.html/docs/archive/ 冻结档/tmpe/ 临时区"
             "/_w588_ce.html W588 渲染快照件·其出链为 site 根相对形态不适用 scripts/ 位）",
    )
    args = ap.parse_args()

    # 未指定任何模式时默认仅站内
    if not (args.internal or args.external or args.all):
        do_internal, do_external = True, False
    else:
        do_internal = args.internal or args.all
        do_external = args.external or args.all

    scan_dir = Path(args.dir)
    if not scan_dir.is_absolute():
        scan_dir = (ROOT / args.dir).resolve()
    if not scan_dir.exists():
        print(f"[ERROR] 扫描目录不存在: {scan_dir}", file=sys.stderr)
        sys.exit(2)

    files = collect_files(scan_dir)
    files = filter_gitignored(files)
    if args.exclude:
        before = len(files)
        # W699 起：排除匹配改为仓库相对路径（扫描 --dir docs 时 "archive/" 不会再
        # 误伤扫描根外同名片段，docs/archive/ 冻结档豁免在全目录口径下均成立）
        files = [
            f for f in files
            if not any(tok in display_path(f) for tok in args.exclude)
        ]
        if len(files) != before:
            print(f"[exclude] 已排除 {before - len(files)} 个文件: {args.exclude}")
    print(f"扫描目录: {display_path(scan_dir)}  文件数: {len(files)}")
    print(f"模式: {'internal' if do_internal else '--'} + {'external' if do_external else '--'}")
    print("-" * 60)

    broken = 0
    checked = 0
    fixed = 0

    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[ERROR] {display_path(f)} 读取失败: {e}", file=sys.stderr)
            continue

        # 收集链接 (line, url)
        links = []
        if f.suffix.lower() in (".html", ".htm"):
            ext = HtmlLinkExtractor()
            try:
                ext.feed(text)
            except Exception:
                pass
            links = [(ln, url) for (ln, _, url) in ext.links]
        else:
            links = extract_markdown_links(strip_md_code(text))

        pending_fixes = []  # (old_url, new_url)

        for line, raw in links:
            url = raw.strip()
            if is_skip(url):
                continue
            if is_external(url):
                if do_external:
                    checked += 1
                    ok, info = check_external(url)
                    if ok:
                        print(f"[OK]     {display_path(f)}:{line}  {url}  ->  {info}")
                    else:
                        broken += 1
                        print(f"[BROKEN] {display_path(f)}:{line}  {url}  ->  {info}")
                continue
            # 站内
            if do_internal:
                checked += 1
                ok, target, _ = check_internal(f, url)
                disp = display_path(target) if target else "?"
                if ok:
                    print(f"[OK]     {display_path(f)}:{line}  {url}  ->  {disp}")
                else:
                    if args.fix:
                        new = try_fix(f, url, ROOT)
                        if new:
                            pending_fixes.append((raw, new))
                            fixed += 1
                            print(f"[FIXED]  {display_path(f)}:{line}  {url}  ->  {new}")
                            continue
                    broken += 1
                    print(f"[BROKEN] {display_path(f)}:{line}  {url}  ->  {disp}")

        # 应用本文件的修复
        if pending_fixes:
            try:
                content = f.read_text(encoding="utf-8")
                for old, new in pending_fixes:
                    content = content.replace(old, new)
                f.write_text(content, encoding="utf-8")
            except Exception as e:
                print(f"[ERROR] 写回修复失败 {display_path(f)}: {e}", file=sys.stderr)

    print("-" * 60)
    summary = f"校验完成: {checked} 链接, {broken} broken"
    if args.fix:
        summary += f", {fixed} 已修复"
    print(summary)
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
