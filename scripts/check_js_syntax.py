"""Check inline JS syntax in HTML files using `node --check`.

Two modes:
    # check a single HTML file's inline JS
    python check_js_syntax.py --file site/data/aesthetics.html

    # batch check all HTML files under site/data/ (also site/dashboard.html if present)
    python check_js_syntax.py --all

    # batch check a custom directory
    python check_js_syntax.py --all --dir path/to/html/dir

When invoked with no arguments, defaults to --all behavior.

Exit code: 0 if all scripts pass, 1 if any failure.
"""
import argparse
import os
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_ROOT = ROOT / "site"
DEFAULT_DATA_DIR = ROOT / "site" / "data"
DASHBOARD_FILE = ROOT / "site" / "dashboard.html"

# W457 扩展：默认 --all 递归扫描 site/ 全站（根 + data + en），
# 排除下划线前缀模板（_shell.html/_template.html 含 {{PAGE_TITLE}} 占位符，node --check 会误报）。
EXCLUDE_PREFIX = "_"

SCRIPT_RE = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.DOTALL)


def collect_site_html_files(root_dir: Path) -> list:
    """递归收集 site/ 下全部 .html，排除下划线前缀模板。"""
    files = []
    for dirpath, _dirs, fnames in os.walk(root_dir):
        for fn in sorted(fnames):
            if fn.endswith(".html") and not fn.startswith(EXCLUDE_PREFIX):
                files.append(Path(dirpath) / fn)
    return files


def check_file(html_file: Path, errors: list, verbose: bool = False) -> int:
    """Check inline JS of one HTML file. Returns count of scripts checked.
    Appends (filename, script_index, stderr) tuples to `errors` on failure.
    """
    if not html_file.exists():
        print(f"[FAIL] {html_file} (file not found)")
        errors.append((html_file.name, 0, "file not found"))
        return 0

    text = html_file.read_text(encoding="utf-8")
    checked = 0

    for i, match in enumerate(SCRIPT_RE.finditer(text)):
        # W591 parity（对齐 check_js_syntax.js:40-45）：非 JS 数据块
        # （application/ld+json、application/json、importmap 等）不是可执行脚本，
        # 不参与语法编译——把 <script type> 数据块当 JS 编译必误报（老逻辑病灶）。
        open_tag = match.group(0)[: match.group(0).index(">") + 1]
        tm = re.search('\\btype\\s*=\\s*"([^"]*)"', open_tag, re.I) or re.search(
            "\\btype\\s*=\\s*'([^']*)'", open_tag, re.I
        )
        stype = tm.group(1).strip().lower() if tm else ""
        if stype and stype not in ("text/javascript", "application/javascript", "module"):
            continue
        script = match.group(1).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        if not script.strip():
            continue
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".js", delete=False, encoding="utf-8"
        )
        tmp.write(script)
        tmp.close()
        try:
            result = subprocess.run(
                ["node", "--check", tmp.name],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode == 0:
                if verbose:
                    print(f"[OK]   {html_file.name} script {i + 1}")
            else:
                err = result.stderr.strip() or result.stdout.strip()
                print(f"[FAIL] {html_file.name} script {i + 1}")
                if err:
                    print(f"       {err}")
                errors.append((html_file.name, i + 1, err))
            checked += 1
        finally:
            os.unlink(tmp.name)
    return checked


def collect_html_files(target_dir: Path) -> list:
    files = sorted(target_dir.glob("*.html"))
    # Always include dashboard.html if it exists and is not already in the dir.
    if DASHBOARD_FILE.exists() and DASHBOARD_FILE.parent != target_dir:
        files.append(DASHBOARD_FILE)
    return files


def main():
    parser = argparse.ArgumentParser(
        description="Check inline JS syntax in HTML files using `node --check`."
    )
    parser.add_argument(
        "--file",
        help="Check a single HTML file's inline JS (relative to project root or absolute).",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Batch check all HTML files under site/data/ (or --dir).",
    )
    parser.add_argument(
        "--dir",
        help="Custom directory to scan when using --all (relative to project root or absolute).",
    )
    args = parser.parse_args()

    errors: list = []

    if args.file:
        # Single-file mode
        f = Path(args.file)
        if not f.is_absolute() and not f.exists():
            candidate = ROOT / args.file
            if candidate.exists():
                f = candidate
            else:
                candidate = DEFAULT_DATA_DIR / args.file
                if candidate.exists():
                    f = candidate
        check_file(f, errors)

    else:
        # Batch mode (default when no --file)
        # W457：全站模式委托 node 单进程版（vm.Script 批量编译，秒级）；
        # 原「每块 spawn node --check」机制在 233 页规模下 120s 内跑不完。
        node_js = ROOT / "scripts" / "check_js_syntax.js"
        if not args.dir and node_js.exists():
            r = subprocess.run(["node", str(node_js)], capture_output=False)
            raise SystemExit(r.returncode)

        if args.dir:
            d = Path(args.dir)
            if not d.is_absolute():
                d = ROOT / args.dir
            target_dir = d
            html_files = collect_html_files(target_dir)
            if not html_files:
                print(f"[FAIL] no HTML files found under {target_dir}")
                raise SystemExit(1)
            print(f"Scanning {len(html_files)} HTML file(s) under {target_dir}\n")
        else:
            html_files = collect_site_html_files(SITE_ROOT)
            if not html_files:
                print(f"[FAIL] no HTML files found under {SITE_ROOT}")
                raise SystemExit(1)
            print(f"Scanning {len(html_files)} HTML file(s) under {SITE_ROOT}\n")

        for html_file in html_files:
            check_file(html_file, errors)

    print()
    if errors:
        print(f"=== {len(errors)} JS syntax error(s) ===")
        for name, idx, err in errors:
            print(f"{name} script {idx}:\n{err}\n")
        raise SystemExit(1)
    else:
        print("All inline scripts pass Node.js syntax check.")
        raise SystemExit(0)


if __name__ == "__main__":
    main()
