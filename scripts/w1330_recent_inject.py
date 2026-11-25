"""W1330 最近浏览埋点注入器（正本=本文件；目标页固定 site/data/**）。

规则：每个 site/data 内容页在 </body> 前加载 ../static/js/recent.js（defer），
记录「最近浏览」供 dashboard.html 回显；不注入看板自身/模板壳/EN 页。

用法：
  python scripts/w1330_recent_inject.py --dry-run
  python scripts/w1330_recent_inject.py --apply
  python scripts/w1330_recent_inject.py --check   # 每页恰一次 + 目标集守恒 + 看板不加载

幂等：已含 MARK 的页整块替换为规范块；行尾按 .gitattributes 契约落 LF。
"""
import io
import re
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "site" / "data"
DASH = ROOT / "site" / "dashboard.html"
JS = ROOT / "site" / "static" / "js" / "recent.js"
MARK = "<!-- RECENT-TRACKER v1 w1330 -->"
TAG = '<script src="../static/js/recent.js" defer></script>'
BLOCK = f"    {MARK}\n    {TAG}"
SKIP = {"_shell.html", "_template.html"}


def _pages():
    return sorted(p for p in DATA.glob("*.html") if p.name not in SKIP)


def process(txt):
    action = "insert"
    if MARK in txt:
        new, n = re.subn(re.escape(MARK) + r".*?</script>", BLOCK.strip(), txt, count=1, flags=re.S)
        if not n:
            return txt, "mark-broken"
        action = "update"
        txt = new
    if "recent.js" in txt and action == "update":
        return txt, action
    if "recent.js" in txt:
        return txt, "already"
    if "</body>" not in txt:
        return txt, "no-body"
    txt = txt.replace("</body>", BLOCK + "\n</body>", 1)
    return txt, action


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dry-run"
    stats, changed, fail = {}, [], []
    for f in _pages():
        txt = f.read_text(encoding="utf-8")
        had_crlf = b"\r\n" in f.read_bytes()
        new, action = process(txt)
        stats[action] = stats.get(action, 0) + 1
        if action == "mark-broken":
            fail.append(f"{f.name}: MARK 后无 </script>")
            continue
        if new != txt or had_crlf:
            changed.append(f.name)
            if mode == "--apply":
                f.write_text(new, encoding="utf-8", newline="\n")
            elif mode == "--check":
                fail.append(f"{f.name}: 未注入/需归一（action={action}）")
    print(f"mode={mode}  目标页={len(_pages())}  stats={stats}  实际改动={len(changed)}")

    if mode == "--check":
        if not JS.is_file():
            fail.append("缺 site/static/js/recent.js")
        else:
            js = JS.read_text(encoding="utf-8")
            for token in ("xy-recent-pages", "MAX = 5", "localStorage"):
                if token not in js:
                    fail.append(f"recent.js 缺关键 token：{token}")
        dash = DASH.read_text(encoding="utf-8")
        if "recent.js" in dash:
            fail.append("dashboard.html 不应加载 recent.js（自身不入最近浏览）")
        for token in ("xy-recent-pages", "initRecent", "initBackTop", "readHashState", "applyHashState"):
            if token not in dash:
                fail.append(f"dashboard.html 缺交互 token：{token}")
        # 目标集守恒：reference 恰好 = 90 页，且不存在第 2 处
        refs = [f.name for f in _pages() if f.read_text(encoding="utf-8").count("recent.js") == 1]
        if len(refs) != len(_pages()):
            fail.append(f"引用守恒失败：{len(refs)}/{len(_pages())} 页恰一次")
        print(f"CHECK {'FAIL' if fail else 'PASS'}  问题 {len(fail)} 条")
        for x in fail[:40]:
            print("  -", x)
        sys.exit(1 if fail else 0)
    if fail:
        for x in fail:
            print("  -", x)
        sys.exit(1)


if __name__ == "__main__":
    main()
