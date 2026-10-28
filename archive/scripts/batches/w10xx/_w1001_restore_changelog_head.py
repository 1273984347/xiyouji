"""_w1001_restore_changelog_head.py — 恢复被并行批次级联覆盖丢失的 CHANGELOG 头部

诊断（W1001 批）：HEAD 的 CHANGELOG 顶行直接是 `### W1000` 段 ⇒
`# 更新日志` + 阅读契约 + 「W### 编号规则」等**头部整块丢失**（并行会话 W1000 批的级联
把新段插到了文件最顶，覆盖了头部）⇒ 连带 `batch_cascade` 的编号规则锚点断言失败
（`s.count("（W001-W1000）") == 1` ⇒ 0）⇒ 级联跑不动 ⇒ 14 个版本面无法推进。

修法：从 git 历史取**最后一个含完整头部**的 CHANGELOG 版本，把头部（到第一个 `### W` 段之前）
原样拼回工作树顶部；并把编号规则改成级联期望的**全角括号形态** `（W001-W1000）`
（cur_w=1000 ⇒ 级联会自动推进为 `（W001-W1001）`）。

用法：py -3 scripts/_w1001_restore_changelog_head.py [--dry-run]
"""
import io
import os
import re
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(REPO, "CHANGELOG.md")


def git_show(rev):
    return subprocess.run(["git", "show", rev + ":CHANGELOG.md"],
                          capture_output=True, text=True, cwd=REPO).stdout


def main() -> int:
    dry = "--dry-run" in "--dry-run" in os.sys.argv
    cur = io.open(CH, encoding="utf-8").read()
    if cur.startswith("# 更新日志"):
        print("SKIP  CHANGELOG 头部已在")
    else:
        # 从历史里找最后一个含完整头部的版本
        revs = subprocess.run(["git", "log", "--format=%H", "-60", "--", "CHANGELOG.md"],
                              capture_output=True, text=True, cwd=REPO).stdout.split()
        head_text = None
        src = None
        for rv in revs:
            txt = git_show(rv)
            if txt.startswith("# 更新日志"):
                i = txt.find("\n### ")
                if i > 0:
                    head_text = txt[:i]
                    src = rv[:9]
                    break
        if not head_text:
            print("FAIL  git 历史里找不到含完整头部的 CHANGELOG 版本")
            return 1
        # 编号规则：只改**编号规则那一行**的形态（其余行原样保留——
        # 上一版用无差别 re.sub 把「历史版本归档」等叙述行的编号区间也改了 ⇒ 污染历史表述）
        cur_w = re.search(r"^### W(\d{3,4})", cur, re.M)
        cur_w = cur_w.group(1) if cur_w else "1000"
        hl = head_text.split("\n")
        for i, ln in enumerate(hl):
            if "编号规则" in ln:
                hl[i] = re.sub(r"[（(]W001-W\d{3,4}[)）]", "（W001-W%s）" % cur_w, ln)
        head_text = "\n".join(hl)
        new = head_text + cur
        if dry:
            print("DRY  CHANGELOG 头部将从 %s 恢复（%d 字符）" % (src, len(head_text)))
        else:
            tmp = CH + ".tmp"
            io.open(tmp, "wb").write(new.encode("utf-8"))
            os.replace(tmp, CH)
            print("OK   CHANGELOG 头部已从 %s 恢复（%d 字符）" % (src, len(head_text)))
        print("     编号规则形态：", "（W001-W%s）" % cur_w,
              "→", "存在" if "（W001-W%s）" % cur_w in head_text else "缺失")

    # 复核
    t = io.open(CH, encoding="utf-8").read()
    print("     顶行：", t.split("\n")[0][:60])
    print("     现役段：", re.findall(r"^### (W\d{3,4})", t, re.M)[:4])
    print("     编号规则串：", re.findall(r"（W001-W\d{4}）", t))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
