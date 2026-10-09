"""W676 WP-4.3① narratology-13d → narratology-16d 重命名全牵连面（ZH+EN）。

范围：页内 9+7 处自引（canonical/og:url/hreflang×3/cite/EN 链/fetch 路径）→ git mv 两页
→ 全站引用面（sitemap/index/dukou-engine/tag-cloud/search/poetry-rhythm/perf-canvas/
  pilgrim-team + EN 镜像 + reader 主题 4 页 + datahub-index.js）→ tests ×4
→ 视觉基线 png（gitignore 本地件）随名 → hreflang-pairs.json 同步改名。
不动（超范围留档）：dataset/ 真源（批次四禁改）、hyperframes/、scripts/ 历史报告。
"""
import subprocess
import sys

OLD = "narratology-13d"
NEW = "narratology-16d"

RENAME = [
    "site/data/narratology-13d-network.html",
    "site/en/narratology-13d-network.html",
]
BASELINES = [
    "tests/e2e/baseline/narratology-13d-network.png",
    "tests/e2e/current/narratology-13d-network.png",
]
SWEEP = [
    "site/sitemap.xml",
    "site/index.html",
    "site/dukou-engine.html",
    "site/data/perf-canvas-rendering.html",
    "site/data/pilgrim-team-psychology-arc.html",
    "site/data/tag-cloud.html",
    "site/data/search.html",
    "site/data/poetry-rhythm-analysis.html",
    "site/en/pilgrim-team-psychology-arc.html",
    "site/en/perf-canvas-rendering.html",
    "site/en/poetry-rhythm-analysis.html",
    "site/en/search.html",
    "site/en/visualizations.html",
    "site/en/tag-cloud.html",
    "site/reader/themes/取经数字人文专题.html",
    "site/reader/themes/取经团队决策论专题.html",
    "site/reader/themes/取经网络叙事学深化专题.html",
    "site/reader/themes/西游与复杂性科学专题.html",
    "site/static/js/datahub-index.js",
    "tests/e2e/test_narratology_render.py",
    "tests/test_narratology_data.py",
    "tests/e2e/test_deep.js",
    "tests/e2e/test_visual.js",
    "scripts/output/hreflang-pairs.json",
]


def replace_in(path, expect_min=1):
    with open(path, encoding="utf-8", newline="") as fh:
        text = fh.read()
    n = text.count(OLD)
    if n < expect_min:
        print("SKIP %s（%d 处 < 预期 %d）" % (path, n, expect_min))
        return 0
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text.replace(OLD, NEW))
    print("OK   %s：%d 处" % (path, n))
    return n


def main():
    dry = "--dry" in sys.argv
    total = 0
    for p in RENAME:
        with open(p, encoding="utf-8", newline="") as fh:
            t = fh.read()
        print("%s 页内自引 %d 处" % (p, t.count(OLD)))
    for p in SWEEP:
        with open(p, encoding="utf-8", newline="") as fh:
            t = fh.read()
        print("%s 引用 %d 处" % (p, t.count(OLD)))
    if dry:
        print("DRY 结束")
        return

    for p in RENAME + SWEEP:
        total += replace_in(p)

    for p in RENAME:
        r = subprocess.run(["git", "mv", p, p.replace(OLD, NEW)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("git mv FAIL", p, r.stderr)
            sys.exit(1)
        print("git mv", p, "->", p.replace(OLD, NEW))

    import os
    for p in BASELINES:
        if os.path.exists(p):
            os.rename(p, p.replace(OLD, NEW))
            print("mv baseline", p)

    # 自检：site/ 全树 0 残留
    r = subprocess.run(["git", "grep", "-l", OLD, "--", "site/"],
                       capture_output=True, text=True)
    leftover = [x for x in r.stdout.splitlines() if x.strip()]
    print("site/ 残留：%d" % len(leftover))
    for x in leftover:
        print("  LEFT", x)
    if leftover:
        sys.exit(1)
    print("OK 总计 %d 处，site/ 清零" % total)


if __name__ == "__main__":
    main()
