# -*- coding: utf-8 -*-
"""_w1049_stage_faces.py — 精确暂存本批级联面（逐文件判定 W1049 vs W1050 归属）

背景：工作树的 20 项级联面暂存是 **W1050 批**的级联（版本行指向 W1050），
而本批 W1049 的段已由 backfill 按号序落工作树。⇒ 提交前须把级联面改成
「**HEAD 版 + 本批 W1049 段/版本行**」，且**不得**卷入 W1050 的内容。

判定口径（逐文件·可复核）：
  · CHANGELOG.md        → 以工作树版为准（工作树含 W1049 段 + W1050 段）
                          ⇒ 需**剔除 W1050 段**后再暂存
  · file-index.md 等登记面 → 同上（含 W1049 段 + W1050 段）
  · 其余级联面（README/STRUCTURE/CITATION/site 页脚…）→ 版本行指向「当前最高号」。
                          当前最高号 = W1050（并行批）⇒ 本批 W1049 号更小，
                          **这些面本批不动**（W1050 批重放时会重跑级联刷新）
  · 台账 → 已由 _w1049_stage_ledger.py 精确暂存

用法：py -3 archive/scripts/batches/w10xx/_w1049_stage_faces.py [--dry-run]
"""
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))

# 含 W1049/W1050 段的登记面：需剔除 W1050 段后暂存
SEG_FACES = [
    "CHANGELOG.md",
    "scripts/output/file-index.md",
]
# 本批不动的级联面（版本行指向最高号 W1050 ⇒ 属 W1050 批重放范围）
DEFER_FACES = [
    ".github/workflows/README.md",
    "CITATION.cff",
    "README.md",
    "STRUCTURE.md",
    "archive/docs/AGENTS-ARCHIVE.md",
    "archive/docs/CHANGELOG-ARCHIVE.md",
    "archive/docs/W批次编号对账表-ARCHIVE.md",
    "archive/docs/file-index-ARCHIVE.md",
    "docs/00-导读/项目说明.md",
    "scripts/output/README.md",
    "scripts/output/index.md",
    "scripts/output/stats.json",
    "scripts/output/tools-inventory.md",
    "site/data/cross-time-danmaku.html",
    "site/data/tag-cloud.html",
    "site/dukou-engine.html",
    "site/index.html",
]


def git(*a, **kw):
    return subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO] + list(a),
                          capture_output=True, **kw)


def strip_w1050_segment(text: str) -> str:
    """从登记面文本里剔除 `W1050` 整段（到下一个同级标题或段尾）。

    两种标题层级都支持：
      · CHANGELOG.md   → `### W1050（…）标题`
      · file-index.md → `## W1050 标题`
    段体边界：标题行 + 其后直到下一个**同级或更高级**标题行之前的全部内容。
    """
    lines = text.split("\n")
    out = []
    skipping = False
    skip_prefix = None
    for ln in lines:
        m = re.match(r"^(#{2,3})\s+W(\d{3,4})", ln)
        if m:
            level = len(m.group(1))
            if m.group(2) == "1050":
                skipping = True
                skip_prefix = "#" * level
                continue
            if skipping:
                # 遇到同级或更高级标题 ⇒ 结束跳过
                if len("#" * level) <= len(skip_prefix):
                    skipping = False
                    skip_prefix = None
                    out.append(ln)
                continue
        if skipping:
            continue
        out.append(ln)
    return "\n".join(out)


def main() -> int:
    dry = "--dry-run" in sys.argv

    print("== ① 登记面（CHANGELOG / file-index）：剔除 W1050 段后暂存 ==")
    for f in SEG_FACES:
        abs_p = os.path.join(REPO, f.replace("/", os.sep))
        if not os.path.exists(abs_p):
            print("  SKIP  %s 不存在" % f)
            continue
        raw = io.open(abs_p, "rb").read()
        text = raw.decode("utf-8")
        stripped = strip_w1050_segment(text)
        n_removed = len(text.split("\n")) - len(stripped.split("\n"))
        has_1049 = bool(re.search(r"(?m)^#{2,3}\s+W1049\b", stripped))
        print("  %s：剔除 W1050 段 %d 行 · W1049 段在位=%s"
              % (f, n_removed, has_1049))
        if not has_1049:
            print("  FAIL  %s 剔除后无 W1049 段（中止）" % f)
            return 1
        if dry:
            continue
        blob = git("hash-object", "-w", "--stdin", input=stripped.encode("utf-8"),
                   check=True).stdout.decode().strip()
        git("update-index", "--cacheinfo", "100644,%s,%s" % (blob, f), check=True)
        print("  OK    已暂存（blob=%s）" % blob[:10])

    print("\n== ② 本批不动的级联面（属 W1050 批重放范围·从暂存区撤出）==")
    for f in DEFER_FACES:
        staged = git("diff", "--cached", "--name-only").stdout.decode("utf-8", "replace")
        if f not in staged.splitlines():
            continue
        if dry:
            print("  DRY  将撤出暂存：%s" % f)
            continue
        git("restore", "--staged", "--", f, check=True)
        print("  OK    已撤出暂存（工作树内容保留·W1050 批重放时取用）：%s" % f)

    print("\n== 复核：暂存区剩余 ==")
    staged = git("diff", "--cached", "--name-only").stdout.decode("utf-8", "replace").splitlines()
    for f in staged:
        print("  %s" % f)
    print("  共 %d 项" % len(staged))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
