"""xiyouji-analysis CLI——列出/执行打包的分析脚本。

命令：
  xiyouji-analysis list                     列出全部打包分析（类目/脚本/说明）
  xiyouji-analysis run <类目/脚本名>         执行单个分析（如 G_哲学/philosophy）
      --out DIR   输出目录（默认 ./xiyouji-output/data）
  xiyouji-analysis run-all --out DIR        依序执行全部脚本（失败不中断·末尾汇总）

设计：
  - 脚本以仓库原样分发（零修改），CLI 用子进程执行并透传 --output 参数——
    与仓库内「py 类目/xxx.py --output output/data/」的用法完全同构。
  - 自包含脚本（32 个）开箱即用；读仓库语料的耦合脚本（chapter_stats/word_frequency/
    character_appearance/character_nlp/timeline）在 list 中标注 coupled，
    run 时提示需要仓库工作树（B-7 后续批参数化）。
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

COUPLED = {
    "A_文本基础/chapter_stats.py",
    "A_文本基础/word_frequency.py",
    "B_人物/character_appearance.py",
    "B_人物/character_nlp.py",
    "F_时间/timeline.py",
}


def analyses_dir() -> Path:
    import xiyouji_analysis

    return Path(xiyouji_analysis.analyses_root())


def discover() -> list[tuple[str, Path]]:
    root = analyses_dir()
    out = []
    for cat in sorted(p for p in root.iterdir() if p.is_dir()):
        for script in sorted(cat.glob("*.py")):
            if script.name.startswith("_"):
                continue
            out.append((f"{cat.name}/{script.stem}", script))
    return out


def cmd_list() -> int:
    items = discover()
    for rel, _path in items:
        flag = "  [coupled: 需仓库语料]" if rel + ".py" in COUPLED else ""
        print(f"{rel}{flag}")
    print(f"-- 共 {len(items)} 个分析（coupled {sum(1 for r, _ in items if r + '.py' in COUPLED)} 个）")
    return 0


def cmd_run(target: str, out_dir: Path) -> int:
    items = dict(discover())
    if target not in items:
        print(f"FAIL 未找到分析 {target!r}（xiyouji-analysis list 查看全部）")
        return 1
    script = items[target]
    out_dir.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        [sys.executable, str(script), "--output", str(out_dir)],
        capture_output=True, text=True,
    )
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode != 0:
        print(f"FAIL {target} 退出码 {r.returncode}")
        return 1
    print(f"OK {target} → {out_dir}")
    return 0


def cmd_run_all(out_dir: Path) -> int:
    ok = fail = 0
    failed = []
    for rel, path in discover():
        out_dir.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(
            [sys.executable, str(path), "--output", str(out_dir)],
            capture_output=True, text=True,
        )
        if r.returncode == 0:
            ok += 1
        else:
            fail += 1
            failed.append(rel)
    print(f"---- run-all：成功 {ok} · 失败 {fail} ----")
    for f in failed:
        print("  FAIL", f)
    return 1 if fail else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="xiyouji-analysis", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="列出全部分析")
    p_run = sub.add_parser("run", help="执行单个分析")
    p_run.add_argument("target", help="类目/脚本名，如 G_哲学/philosophy")
    p_run.add_argument("--out", default="xiyouji-output/data", help="输出目录")
    p_all = sub.add_parser("run-all", help="执行全部")
    p_all.add_argument("--out", default="xiyouji-output/data", help="输出目录")
    args = ap.parse_args(argv)

    if args.cmd == "list":
        return cmd_list()
    if args.cmd == "run":
        return cmd_run(args.target, Path(args.out))
    if args.cmd == "run-all":
        return cmd_run_all(Path(args.out))
    return 2


if __name__ == "__main__":
    sys.exit(main())
