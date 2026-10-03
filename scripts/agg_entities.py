#!/usr/bin/env python3
"""agg_entities.py — B-5 聚合器先行（W651 启动·读 100 回 chapter-meta 出 entities 两类）

数据源：docs/01-全书逐回解读/第NNN回-*.md 内嵌注释
  <!-- chapter-meta: {"num": .., "main_characters": [..], "locations": [..], ...} -->
输出（纯聚合·零新造事实·schema 沿用 chapter-meta 现有键风格）：
  dataset/entities/characters.json  按 main_characters 聚合：出场回数/回目列表/首秀回
  dataset/entities/locations.json   按 locations 聚合：覆盖回数/回目列表/首现回

用途：B-5 第一步——为「扩字段 + 学术增强（Wikidata QID 对齐）」提供实体底表；
聚合不做别名归并（行者/悟空的分账属学术裁决面），消费方按需处理。

用法：python scripts/agg_entities.py            # 生成 + 校验 100/100 覆盖
     python scripts/agg_entities.py --check    # 只校验不写盘（CI/复核用）
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
A1_DIR = ROOT / "docs" / "01-全书逐回解读"
OUT_DIR = ROOT / "dataset" / "entities"
RE_META = re.compile(r"<!--\s*chapter-meta:\s*(\{.*?\})\s*-->", re.S)


def collect() -> tuple[dict[int, dict], list[str]]:
    """返回 (按回号的 meta 字典, 问题清单)。"""
    metas: dict[int, dict] = {}
    problems: list[str] = []
    files = sorted(A1_DIR.glob("第*回-*.md"))
    for p in files:
        text = p.read_text(encoding="utf-8")
        m = RE_META.search(text)
        if not m:
            problems.append(f"{p.name}: 缺 chapter-meta 注释")
            continue
        try:
            meta = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            problems.append(f"{p.name}: chapter-meta JSON 解析失败 {e}")
            continue
        num = meta.get("num")
        if not isinstance(num, int):
            problems.append(f"{p.name}: num 非整数")
            continue
        if num in metas:
            problems.append(f"{p.name}: num={num} 重复")
        metas[num] = meta
    return metas, problems


def aggregate(metas: dict[int, dict], key: str) -> dict:
    ent: dict[str, dict] = {}
    for num in sorted(metas):
        for name in metas[num].get(key, []):
            e = ent.setdefault(name, {"name": name, "chapters": [], "count": 0})
            e["chapters"].append(num)
            e["count"] = len(e["chapters"])
    rows = sorted(ent.values(), key=lambda x: (-x["count"], x["chapters"][0], x["name"]))
    for r in rows:
        r["first_chapter"] = r["chapters"][0]
    return {
        "title": f"A1 chapter-meta 实体聚合（{key}）",
        "w_id": "W651",
        "generated": __import__("datetime").date.today().isoformat(),
        "source": "docs/01-全书逐回解读/ 100 回 chapter-meta 注释（agg_entities.py 纯聚合·零新造事实·不做别名归并）",
        "method": "按 main_characters/locations 逐回列表聚合：出场回数/回目列表/首秀回",
        "count": len(rows),
        "entities": rows,
    }


def main() -> int:
    check_only = "--check" in sys.argv
    metas, problems = collect()
    coverage = f"chapter-meta 覆盖 {len(metas)}/100"
    if len(metas) != 100:
        problems.append(f"覆盖不足：{coverage}")
    for p in problems:
        print("FAIL " + p)
    if problems:
        return 1
    print(coverage)

    characters = aggregate(metas, "main_characters")
    locations = aggregate(metas, "locations")
    print(f"characters {characters['count']} 名 · locations {locations['count']} 处")
    top_c = characters["entities"][:3]
    print("  characters top3：" + "、".join(f"{e['name']}({e['count']})" for e in top_c))

    if check_only:
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, payload in (("characters", characters), ("locations", locations)):
        out = OUT_DIR / f"{name}.json"
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"写出 {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
