"""W676 WP-4.3⑥ site/data + site/en 页脚停滞 sweep（v2）。

bump_version 页脚替换式盲区存量（坑③）：footer-meta 以 vN.N.N · WNNN 开头的页脚，
版本前缀统一重写为当批 v2.3.282 · W676，其余内容（尾注/内嵌 md 原文链接）原样保留；
含 bump 污染链的页脚（一段内多个 vN.N.N · WNNN token，坑②残留）整体收敛为单条。
「2026 · MIT License」许可型页脚不在范围。
"""
import glob
import re
import sys

VER = "v2.3.282 · W676"
PAT = re.compile(r'(class="footer-meta">)(v\d+\.\d+\.\d+ · W\d+.*?)(</div>)', re.S)
VTOK = re.compile(r"v\d+\.\d+\.\d+ · W\d+")
LEAD = re.compile(r"^v\d+\.\d+\.\d+ · W\d+")


def rewrite(m):
    inner = m.group(2)
    toks = VTOK.findall(inner)
    if len(toks) > 1:  # 污染链：整体收敛（原链尾注均为「数据可视化」）
        return m.group(1) + VER + " · 数据可视化" + m.group(3)
    return m.group(1) + LEAD.sub(VER, inner, count=1) + m.group(3)


def main():
    dry = "--dry" in sys.argv
    files = sorted(glob.glob("site/data/*.html") + glob.glob("site/en/*.html"))
    changed = 0
    for f in files:
        with open(f, encoding="utf-8", newline="") as fh:
            text = fh.read()
        new, n = PAT.subn(rewrite, text)
        if n:
            changed += 1
            if not dry:
                with open(f, "w", encoding="utf-8", newline="") as fh:
                    fh.write(new)
            if changed <= 2:
                print("%s -> %s" % (f, PAT.search(new).group(0)[:130]))
    print("共 %d 页页脚重写%s" % (changed, "（dry）" if dry else ""))
    left = 0
    for f in files:
        with open(f, encoding="utf-8", newline="") as fh:
            t = fh.read()
        for m in PAT.finditer(t):
            if not m.group(2).startswith(VER):
                left += 1
                print("LEFT", f, m.group(2)[:60])
    print("非当批页脚残留=%d" % left)
    if left:
        sys.exit(1)


if __name__ == "__main__":
    main()
