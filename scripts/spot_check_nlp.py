#!/usr/bin/env python3
"""spot-check character_nlp.py 输出数据。

Usage:
    # 默认扫描 scripts/output/data/
    python scripts/spot_check_nlp.py
    # 指定 data 目录
    python scripts/spot_check_nlp.py --data-dir path/to/data/
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = ROOT / "scripts" / "output" / "data"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="spot-check character_nlp.py 输出数据")
    parser.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR),
                        help="数据目录（默认 scripts/output/data/）")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.is_absolute():
        data_dir = (ROOT / args.data_dir).resolve()

    if not data_dir.exists():
        print(f"[ERROR] 数据目录不存在: {data_dir}")
        return 1

    print("=== characters.json Top 10 ===")
    chars_path = data_dir / "characters.json"
    if not chars_path.exists():
        print(f"[ERROR] {chars_path} 不存在")
        return 1
    data = load_json(chars_path)
    for i, c in enumerate(data["characters"][:10], 1):
        name = c["name"]
        ac = c["appear_chapters"]
        tm = c["total_mentions"]
        fa = c["first_appear"]
        print(f"{i:2d}. {name:<8} 出场 {ac:3d} 回, 提及 {tm:5d} 次, 首现 第{fa}回")

    print(f"\n人物数: {data['character_count']}")
    print(f"总回数: {data['total_chapters']}")

    all_chars = set([
        "孙悟空","唐僧","猪八戒","沙僧","白龙马","观音","如来","玉帝","太上老君",
        "菩提祖师","二郎神","哪吒","李靖","王母","太白金星","弥勒佛","镇元子",
        "牛魔王","铁扇公主","红孩儿","白骨精","六耳猕猴","黄袍怪","金角大王",
        "银角大王","青牛精","黄风怪","黄眉童子","金鱼精","蝎子精","蜘蛛精",
        "青毛狮子","白象","大鹏","白鹿精"
    ])
    appeared = set(c["name"] for c in data["characters"])
    missing = all_chars - appeared
    print(f"未出场人物: {sorted(missing) if missing else '无'}")

    print("\n=== dialogues.json Top 10 说话者 ===")
    dlg_path = data_dir / "dialogues.json"
    if not dlg_path.exists():
        print(f"[ERROR] {dlg_path} 不存在")
        return 1
    d = load_json(dlg_path)
    for i, s in enumerate(d["speaker_ranking"][:10], 1):
        sp = s["speaker"]
        cnt = s["count"]
        print(f"{i:2d}. {sp:<8} {cnt:5d} 条")

    print(f"\n引语总数: {d['total_dialogues']}")
    print(f"说话者数: {d['speaker_count']}")

    print("\n=== spot-check: 第 100 回全部引语 ===")
    ch100 = [x for x in d["dialogues"] if x["chapter"] == 100]
    print(f"第 100 回引语数: {len(ch100)}")
    for dlg in ch100:
        sp = dlg["speaker"]
        pat = dlg["pattern"]
        q = dlg["quote"][:60]
        print(f"  [{sp}] ({pat}): {q}...")

    print("\n=== spot-check: 第 1 回前 10 条 ===")
    ch1 = [x for x in d["dialogues"] if x["chapter"] == 1]
    print(f"第 1 回引语数: {len(ch1)}")
    for dlg in ch1[:10]:
        sp = dlg["speaker"]
        pat = dlg["pattern"]
        q = dlg["quote"][:50]
        print(f"  [{sp}] ({pat}): {q}...")

    print("\n=== cooccurrence.json 概览 ===")
    co_path = data_dir / "cooccurrence.json"
    if not co_path.exists():
        print(f"[ERROR] {co_path} 不存在")
        return 1
    co = load_json(co_path)
    cl = co["chapter_level"]
    sl = co["scene_levels"] if "scene_levels" in co else co.get("scene_level", {})
    print(f"分回维度: {len(cl['nodes'])} 节点, {len(cl['edges'])} 边")
    if isinstance(sl, dict) and 'nodes' in sl:
        print(f"场景维度: {len(sl['nodes'])} 节点, {len(sl['edges'])} 边")
    print("\n分回维度 Top 5 边:")
    for e in cl["edges"][:5]:
        print(f"  {e['source']} <-> {e['target']}: {e['weight']}")
    if isinstance(sl, dict) and 'edges' in sl:
        print("\n场景维度 Top 5 边:")
        for e in sl["edges"][:5]:
            print(f"  {e['source']} <-> {e['target']}: {e['weight']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
