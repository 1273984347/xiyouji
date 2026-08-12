#!/usr/bin/env python3
"""lint_links.py — 站内/外链校验工具（纯标准库）。

整合 scripts/output/check_links.py（HTML href/src）与
scripts/audit/w053_verify_links.py（Markdown [text](url)）的能力。

检测范围：
  - HTML/HTM：所有 href / src 属性指向的资源
  - Markdown：所有 [text](url) 形式的链接

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
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

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
    headers = {"User-Agent": "lint_links/1.0 (+stdlib)"}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return (resp.status < 400, f"HTTP {resp.status}")
        except Exception as e:
            if method == "HEAD":
                continue
            return (False, str(e)[:80])
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
        default=["node_modules", ".workbuddy", "_template.html"],
        help="排除含这些路径片段的文件/目录（默认 node_modules/.workbuddy/_template.html）",
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
    if args.exclude:
        before = len(files)
        files = [
            f for f in files
            if not any(tok in str(f.relative_to(scan_dir)) for tok in args.exclude)
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
            links = extract_markdown_links(text)

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
