#!/usr/bin/env python3
"""package_analysis_sync.py — B-7：把 scripts/ A-H 类目分析脚本同步进 pip 包 analyses/

单一事实源=仓库 scripts/；包内 analyses/ 是同步产物（勿手改）。
规则：仅收非 _ 前缀 .py（一次性/诊断脚本不入包）；5 个耦合仓库语料的脚本照收但
CLI list 标注 coupled（参数化留后续批）。

用法：python scripts/package_analysis_sync.py [--check]
输出：同步清单 scripts/output/_sync_analysis_manifest.json（含耦合标注与时间）。
"""
import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts"
PKG_ANALYSES = ROOT / "packaging" / "xiyouji-analysis" / "src" / "xiyouji_analysis" / "analyses"
MANIFEST = ROOT / "scripts" / "output" / "_sync_analysis_manifest.json"

COUPLED = {
    "A_文本基础/chapter_stats.py",
    "A_文本基础/word_frequency.py",
    "B_人物/character_appearance.py",
    "B_人物/character_nlp.py",
    "F_时间/timeline.py",
}  # 依赖 scripts/utils/ + 仓库语料（jieba 等）——0.1.0 不入包·参数化留后续批


def discover() -> list[tuple[Path, Path, str, bool]]:
    """返回 [(源路径, 目标路径, 相对名, coupled)]（coupled 不入包·仅登记）。"""
    out = []
    for d in sorted(p for p in SRC.iterdir() if p.is_dir() and re.match(r"^[A-Z]", p.name)):
        for script in sorted(d.glob("*.py")):
            if script.name.startswith("_"):
                continue
            rel = f"{d.name}/{script.name}"
            coupled = rel in COUPLED
            dst = PKG_ANALYSES / d.name / script.name
            out.append((script, None if coupled else dst, rel, coupled))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只核对差异不写盘")
    args = ap.parse_args()

    jobs = discover()
    diffs = []
    for src, dst, _rel, _coupled in jobs:
        if dst is None:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists() or src.read_bytes() != dst.read_bytes():
            diffs.append((src, dst))
    if args.check:
        print(f"待同步 {len(diffs)} / {len(jobs)}")
        return 1 if diffs else 0
    for src, dst in diffs:
        shutil.copyfile(src, dst)
    payload = {
        "sync_date": date.today().isoformat(),
        "total_included": sum(1 for _, dst, _, _ in jobs if dst is not None),
        "excluded_coupled": sorted(rel for _, _, rel, c in jobs if c),
        "note": "B-7 0.1.0：32 自包含纯 stdlib 脚本入包·5 coupled（utils/+仓库语料/jieba）排除·参数化留后续批",
    }
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"同步完成：{len(jobs)} 个脚本（本次写入 {len(diffs)}）· 清单 → {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
