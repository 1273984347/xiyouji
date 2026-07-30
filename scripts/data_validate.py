#!/usr/bin/env python3
"""data_validate.py — output/data/ JSON 结构完整性校验

用途：
    扫描 scripts/output/data/ 下所有 .json 文件，校验：
    1. 文件可被 json.loads 正确解析（语法完整性）
    2. 解析结果非空（非空对象 / 非空数组）
    3. 可选：已知文件顶层键名契约校验（KEY_SCHEMA 字典）

    解决问题：100+ JSON 数据文件驱动 D3.js 可视化，损坏/空文件会
    静默破坏页面渲染，无统一校验机制。

使用方式：
    # 默认扫描 scripts/output/data/
    python scripts/data_validate.py
    # 指定目录
    python scripts/data_validate.py --dir path/to/data/
    # 仅列出问题文件，不输出每个文件的 OK
    python scripts/data_validate.py --quiet
    # 指定单个文件
    python scripts/data_validate.py --file path/to/foo.json

退出码：0 全部通过 / 1 存在失败
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = ROOT / "scripts" / "output" / "data"

# 已知文件顶层结构契约（可选校验）：filename -> 期望顶层类型
# 留空表示仅做语法 + 非空校验；如需键名契约可扩展为 {"type": "dict", "keys": [...]}
EXPECTED_TYPES = {
    # 大多数分析输出为 dict（含统计字段）；少数为 list
    "characters.json": dict,
    "cooccurrence.json": dict,
    "hardships_81.json": dict,
    "journey_route.json": dict,
    "chapter_stats_sample.json": dict,
    "character_appearance_sample.json": dict,
}


def validate_one(path: Path) -> tuple[bool, str]:
    """校验单个 JSON 文件，返回 (ok?, 原因)。"""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return False, f"读取失败: {e}"

    if not text.strip():
        return False, "文件为空"

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return False, f"JSON 解析失败: {e.msg} (line {e.lineno} col {e.colno})"

    if data is None:
        return False, "解析结果为 null"
    if isinstance(data, (list, dict)) and len(data) == 0:
        return False, f"解析结果为空 {'[]' if isinstance(data, list) else '{}'}"

    # 可选：顶层类型契约
    expected = EXPECTED_TYPES.get(path.name)
    if expected is not None and not isinstance(data, expected):
        got = "dict" if isinstance(data, dict) else "list" if isinstance(data, list) else type(data).__name__
        want = "dict" if expected is dict else "list" if expected is list else expected.__name__
        return False, f"顶层类型不匹配: 期望 {want}, 实际 {got}"

    return True, ""


def main():
    parser = argparse.ArgumentParser(description="output/data/ JSON 结构完整性校验")
    parser.add_argument("--dir", default=str(DEFAULT_DATA_DIR),
                        help="数据目录（默认 scripts/output/data/）")
    parser.add_argument("--file", default=None,
                        help="仅校验单个文件（覆盖 --dir）")
    parser.add_argument("--quiet", action="store_true",
                        help="仅输出失败项，不打印每个 OK 文件")
    args = parser.parse_args()

    if args.file:
        targets = [Path(args.file)]
        if not targets[0].is_absolute():
            targets[0] = (ROOT / args.file).resolve()
    else:
        data_dir = Path(args.dir)
        if not data_dir.is_absolute():
            data_dir = (ROOT / args.dir).resolve()
        if not data_dir.exists():
            print(f"[ERROR] 数据目录不存在: {data_dir}")
            return 1
        targets = sorted(data_dir.glob("*.json"))

    if not targets:
        print("[ERROR] 未找到任何 .json 文件")
        return 1

    ok_count = 0
    fail_count = 0
    failures = []

    for path in targets:
        if not path.exists():
            print(f"[MISS] {path}")
            fail_count += 1
            failures.append((path, "文件不存在"))
            continue
        ok, reason = validate_one(path)
        if ok:
            ok_count += 1
            if not args.quiet:
                print(f"[OK]   {path.name}")
        else:
            print(f"[FAIL] {path.name}: {reason}")
            fail_count += 1
            failures.append((path, reason))

    print("\n" + "=" * 60)
    print(f"汇总：{ok_count} OK / {fail_count} FAIL / {len(targets)} 总计")
    if failures:
        print("\n失败列表：")
        for path, reason in failures:
            print(f"  {path.name}  ->  {reason}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
