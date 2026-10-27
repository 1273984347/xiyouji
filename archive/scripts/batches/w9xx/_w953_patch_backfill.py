# -*- coding: utf-8 -*-
"""_w953_patch_backfill.py — 回填脚本：CHANGELOG 部分改用「索引」为基底 + 追加文件行补齐

背景：CHANGELOG 的「文件」行补齐与「验证/状态」回填分属两个脚本时，精确暂存会互相覆盖
（各自以 HEAD 为基底 ⇒ 后者把前者的改动顶掉）。此处合并为一步：
  基底 = 当前索引版 CHANGELOG（`git show :CHANGELOG.md`）
  → 替换「验证 / 状态」两行
  → 追加「文件」行缺项
  → 精确暂存（写索引），工作树同步
"""
import io
import os
import sys

P = os.path.join(r"D:\xiyouji", "scripts", "_w953_backfill_stage.py")
MISSING_BLOCK = '''

MISSING_FILE_ITEMS = [
    "scripts/output/_w953_batch4.json", "scripts/output/_w953_batch5.json",
    "scripts/_w953_prep_raws2.py", "scripts/_w953_prep_raws3.py",
    "scripts/_w953_update_readme.py", "scripts/_w953_zoom.py",
    "scripts/_w953_fix_cascade.py", "scripts/_w953_backfill_stage.py",
    "assets/promo/plate-set/zoom-w953/w953-recheck.png",
]


def fill_file_line(t):
    """把 W953 段的「文件」行补齐缺项（返回新文本）"""
    lines = t.split("\\n")
    idx, in_seg = None, False
    for i, ln in enumerate(lines):
        if ln.startswith("### W953（"):
            in_seg = True
            continue
        if in_seg and ln.startswith("> - **文件**："):
            idx = i
            break
        if in_seg and ln.startswith("### "):
            break
    if idx is None:
        return t
    add = [f for f in MISSING_FILE_ITEMS if f not in lines[idx]]
    if add:
        lines[idx] = lines[idx].rstrip() + "、" + "、".join(add)
    return "\\n".join(lines)
'''

OLD_HEAD = '''    # ---- CHANGELOG ----
    head_cl = git_show(CHANGELOG_REL)
    new_cl = head_cl'''
NEW_HEAD = '''    # ---- CHANGELOG（基底 = 当前索引版·避免与文件行补齐互相覆盖）----
    head_cl = subprocess.run(["git", "show", ":" + CHANGELOG_REL], cwd=REPO,
                             capture_output=True).stdout.decode("utf-8")
    if not head_cl:
        head_cl = git_show(CHANGELOG_REL)
    new_cl = head_cl'''

OLD_STAGE = '''    if new_cl != head_cl:
        stage(CHANGELOG_REL, new_cl)'''
NEW_STAGE = '''    new_cl = fill_file_line(new_cl)
    if new_cl != head_cl:
        stage(CHANGELOG_REL, new_cl)'''


def main():
    raw = io.open(P, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    t = raw.decode("utf-8").replace("\r\n", "\n")
    n = 0
    if "MISSING_FILE_ITEMS" not in t:
        i = t.index("def git_show(rel):")
        t = t[:i] + MISSING_BLOCK.strip() + "\n\n\n" + t[i:]
        n += 1
    if OLD_HEAD in t:
        t = t.replace(OLD_HEAD, NEW_HEAD, 1)
        n += 1
    if OLD_STAGE in t:
        t = t.replace(OLD_STAGE, NEW_STAGE, 1)
        n += 1
    io.open(P, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))
    print("回填脚本已 patch %d/3 处" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
