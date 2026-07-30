"""Detect tables without horizontal scroll wrapper in site/data HTML files.

Usage:
    # from scripts/ directory
    python detect_unwrapped_tables.py
    # with extra HTML files to scan (relative to project root)
    python detect_unwrapped_tables.py --extra site/index.html
"""
from pathlib import Path
from html.parser import HTMLParser
import re
import argparse

ROOT = Path(__file__).resolve().parent.parent
SITE_DATA = ROOT / "site" / "data"
DASHBOARD_FILE = ROOT / "site" / "dashboard.html"


class TableDetector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.stack = []
        self.line = 0

    def getpos(self):
        return super().getpos()

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.stack.append({
            "tag": tag,
            "attrs": attrs_dict,
            "line": self.getpos()[0],
        })
        if tag == "table":
            table_id = attrs_dict.get("id", "")
            table_cls = attrs_dict.get("class", "")
            # Find nearest wrapper div with overflow-x:auto or table-wrap
            wrapped = False
            wrapper_info = ""
            for el in reversed(self.stack[:-1]):
                if el["tag"] == "div":
                    style = el["attrs"].get("style", "")
                    cls = el["attrs"].get("class", "")
                    if ("overflow-x" in style or
                        "table-wrap" in cls or
                        "data-table-wrap" in cls or
                        "climax-wrap" in cls or
                        "table-wrapper" in cls):
                        wrapped = True
                        wrapper_info = f"div.{cls}" if cls else "div[style]"
                        break
            self.tables.append({
                "line": self.getpos()[0],
                "id": table_id,
                "class": table_cls,
                "wrapped": wrapped,
                "wrapper": wrapper_info,
            })

    def handle_endtag(self, tag):
        while self.stack and self.stack.pop()["tag"] != tag:
            pass


def scan_file(path: Path):
    parser = TableDetector()
    parser.feed(path.read_text(encoding="utf-8"))
    return [t for t in parser.tables if not t["wrapped"]]


def main():
    parser = argparse.ArgumentParser(description="Detect tables without horizontal scroll wrapper.")
    parser.add_argument("--extra", nargs="*", help="Additional HTML files to scan (relative to project root)")
    args = parser.parse_args()

    files = sorted(SITE_DATA.glob("*.html"))
    needs_wrap = []

    for f in files:
        unwrapped = scan_file(f)
        if unwrapped:
            needs_wrap.append((f.name, unwrapped))

    # Always scan dashboard.html if it exists.
    if DASHBOARD_FILE.exists():
        unwrapped = scan_file(DASHBOARD_FILE)
        if unwrapped:
            needs_wrap.append((DASHBOARD_FILE.name, unwrapped))

    for rel in (args.extra or []):
        extra_path = ROOT / rel
        if extra_path.exists():
            unwrapped = scan_file(extra_path)
            if unwrapped:
                needs_wrap.append((extra_path.name, unwrapped))
        else:
            print(f"Warning: extra file not found: {extra_path}")

    print("=== Unwrapped tables (need horizontal scroll container) ===")
    for name, tables in needs_wrap:
        for t in tables:
            print(f"{name:40s} L{t['line']:4d}  id={t['id'] or '-':20s}  class={t['class'] or '-'}")
    print(f"\nTotal files with unwrapped tables: {len(needs_wrap)}")

    if needs_wrap:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
