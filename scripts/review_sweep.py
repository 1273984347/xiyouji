"""review_sweep.py — 全变动复审扫荡器（S-25·W699）。

把「变动类→同类漏网 grep 断言」固化为规则矩阵：输入提交区间（可选），
对现役叙述面/内容面跑零命中断言，输出扫荡报告；命中即 exit 1。

  python scripts/review_sweep.py                          # 全仓扫荡（现役面）
  python scripts/review_sweep.py --range 6154137..efd03fa # 附变更文件清单回放
  python scripts/review_sweep.py --self-test

规则口径=2026-10-10/11 手工复审扫荡矩阵（W694-W695 复盘 E-03）；
排除面=归档/历史段/批次记录/复盘报告合法引用。新增变动类时在 RULES 追加。
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 每条规则：id / 类名 / 命中模式（正则）/ 作用 glob / 路径排除（正则）/ 行级排除（正则）
RULES = [
    {
        "id": "R1", "cls": "旧数据链断言",
        "patterns": [r"供 site/timeline\.html 渲染", r"自动生成，输出到 scripts/output", r"当前无对应可视化页"],
        "globs": ["docs/**/*.md", "timeline/*.md", "scripts/**/*.py", "site/**/*.html"],
        "path_exclude": r"docs[/\\]archive|CHANGELOG|file-index|_w\d|工作复盘与优化分析报告|scripts[/\\]output[/\\]_|review_sweep",
        "line_exclude": None,
    },
    {
        "id": "R2", "cls": "现役文档计数漂移（86/87 族）",
        "patterns": [r"86 个可视化|86 可视化页|87 个 HTML|86 个 D3"],
        "globs": ["README.md", "STRUCTURE.md", "CLAUDE.md", "docs/00-导读/项目说明.md",
                  "docs/00-导读/文档规范.md", "交接文档.md", "AGENTS.md", ".github/workflows/README.md"],
        "path_exclude": None,
        "line_exclude": r"W\d{3}",  # 含历史批次号的行=沿革叙述，合法
    },
    {
        "id": "R3", "cls": "已勘误事实断言",
        "patterns": [r"灭法国与玉华州", r"5048 天", r"第 40 回 红孩儿妖童化身"],
        "globs": ["docs/**/*.md", "timeline/*.md", "site/**/*.html"],
        "path_exclude": r"docs[/\\]archive|工作复盘与优化分析报告|CHANGELOG|review_sweep",
        "line_exclude": r"勘正|驳回|误注|复审",
    },
]


def iter_files(globs):
    seen = set()
    for g in globs:
        for p in ROOT.glob(g):
            if p.is_file() and p.suffix in (".md", ".py", ".html"):
                rp = p.relative_to(ROOT).as_posix()
                if rp not in seen:
                    seen.add(rp)
                    yield rp, p


def run_rules():
    hits = []
    for rule in RULES:
        for rp, p in iter_files(rule["globs"]):
            if rule["path_exclude"] and re.search(rule["path_exclude"], rp):
                continue
            try:
                lines = p.read_text(encoding="utf-8", errors="ignore").split("\n")
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                if rule["line_exclude"] and re.search(rule["line_exclude"], line):
                    continue
                for pat in rule["patterns"]:
                    if re.search(pat, line):
                        hits.append((rule["id"], rule["cls"], rp, i, pat, line.strip()[:110]))
    return hits


def changed_files(rng):
    out = subprocess.run(["git", "-C", str(ROOT), "-c", "core.quotePath=false",
                          "diff", "--name-only", rng],
                         capture_output=True, text=True).stdout
    return [ln for ln in out.splitlines() if ln.strip()]


def self_test():
    probe = "本页数据由脚本生成，供 site/timeline.html 渲染。"
    for rule in RULES:
        for pat in rule["patterns"]:
            if re.search(pat, probe):
                assert not (rule["line_exclude"] and re.search(rule["line_exclude"], probe)), "探针被行级排除误伤"
                print("SELF-TEST PASS：R1 探针被规则 %s（%s）捕获" % (rule["id"], rule["cls"]))
                return
    raise AssertionError("R1 探针未被任何规则捕获")


def main():
    ap = argparse.ArgumentParser(description="全变动复审扫荡器（变动类→零命中断言矩阵）")
    ap.add_argument("--range", dest="rng", help="提交区间（仅用于附变更文件清单回放）")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return 0
    hits = run_rules()
    print("[扫荡] 规则 %d 条 · 命中 %d 处" % (len(RULES), len(hits)))
    for h in hits[:20]:
        print("  HIT [%s %s] %s:%d pattern=%r :: %s" % h)
    if args.rng:
        files = changed_files(args.rng)
        print("[区间 %s] 变更文件 %d 个（清单见上·命中复核按同一规则集）" % (args.rng, len(files)))
    if hits:
        print("FAIL 扫荡命中 %d 处——逐条裁决（修复或登记排除面）后重跑" % len(hits))
        return 1
    print("OK 零残留（口径=现役面；归档/历史段/复盘合法引用已排除）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
