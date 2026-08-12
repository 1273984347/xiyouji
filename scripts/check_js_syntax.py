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
DEFAULT_DATA_DIR = ROOT / "site" / "data"
DASHBOARD_FILE = ROOT / "site" / "dashboard.html"

SCRIPT_RE = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.DOTALL)


def check_file(html_file: Path, errors: list, verbose: bool = False) -> int:
    """Check inline JS of one HTML file. Returns count of scripts checked.
    Appends (filename, script_index, stderr) tuples to `errors` on failure.
    """
    if not html_file.exists():
        print(f"[FAIL] {html_file} (file not found)")
        errors.append((html_file.name, 0, "file not found"))
        return 0

    text = html_file.read_text(encoding="utf-8")
    scripts = SCRIPT_RE.findall(text)
    checked = 0

    for i, script in enumerate(scripts):
        # Replace HTML entities that would break JS syntax check
        script = script.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
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
                print(f"[OK]   {html_file.name} script {i + 1}")
            else:
                err = result.stderr.strip() or result.stdout.strip()
                print(f"[FAIL] {html_file.name} script {i + 1}")
                if err:
                    print(f"       {err}")
                errors.append((html_file.name, i + 1, err))
            checked += 1
            if verbose and result.returncode == 0 and not err:
                # nothing extra to print on success
                pass
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
        if args.dir:
            d = Path(args.dir)
            if not d.is_absolute():
                d = ROOT / args.dir
            target_dir = d
        else:
            target_dir = DEFAULT_DATA_DIR

        if not target_dir.exists() or not target_dir.is_dir():
            print(f"[FAIL] directory not found: {target_dir}")
            raise SystemExit(1)

        html_files = collect_html_files(target_dir)
        if not html_files:
            print(f"[FAIL] no HTML files found under {target_dir}")
            raise SystemExit(1)

        print(f"Scanning {len(html_files)} HTML file(s) under {target_dir}\n")
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
