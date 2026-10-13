"""_w694_hotfix_restore.py — 回灌被 inline_css --force 洗掉的页内私有规则（一次性）。

背景：W674 批把部分页面的暗色重映射/reduce-motion 规则追加在 INLINED <style> 块内部，
W694 的 inline_css --force 按源重建该块时将其吞掉 → 暗色门禁 invisible 0→1（语义网双页实证）。
本脚本从 6154137~1 提取「当前文件缺失的行」（剔除旧标记行），按文件自身 EOL 插回
INLINED 块闭合 </style> 之前。
"""
import subprocess
import sys

ROOT = r"D:\xiyouji"
PARENT = "6154137~1"
PAGES = [
    "site/data/character-semantic-network.html",
    "site/en/character-semantic-network.html",
    "site/data/criticism-history.html",
    "site/en/criticism-history.html",
]
MARKER_HINT = "INLINED CSS"


def git_show(path):
    return subprocess.run(
        ["git", "-C", ROOT, "show", "%s:%s" % (PARENT, path)],
        capture_output=True, check=True,
    ).stdout


def main():
    total = 0
    for rel in PAGES:
        raw = open(ROOT + "\\" + rel.replace("/", "\\"), "rb").read()
        eol = b"\r\n" if b"\r\n" in raw else b"\n"
        cur_lines = set(raw.decode("utf-8").splitlines())
        parent_lines = git_show(rel).decode("utf-8").splitlines()
        lost = []
        for ln in parent_lines:
            if ln in cur_lines:
                continue
            if MARKER_HINT in ln:
                continue
            if not ln.strip():
                continue
            lost.append(ln)
        assert lost, "no lost lines found for " + rel
        # 定位 INLINED 块闭合 </style>（标记行之后第一个）
        text = raw.decode("utf-8")
        mpos = text.find(MARKER_HINT)
        assert mpos != -1, "marker missing in " + rel
        spos = text.find("</style>", mpos)
        assert spos != -1, "style close missing after marker in " + rel
        insert = "".join(ln + ("\r\n" if eol == b"\r\n" else "\n") for ln in lost)
        text = text[:spos] + insert + text[spos:]
        open(ROOT + "\\" + rel.replace("/", "\\"), "wb").write(text.encode("utf-8"))
        total += len(lost)
        print("RESTORED %d lines -> %s" % (len(lost), rel))
        for ln in lost:
            print("   | %s" % ln[:110])
    print("ALL-DONE total=%d" % total)


if __name__ == "__main__":
    sys.exit(main())
