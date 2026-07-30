#!/usr/bin/env python3
"""drl_spotcheck.py — DRL 真循环 spot-check 工具

用途：
    辅助 DRL（Deep Review Loop）执行 spot-check，对"修复声明"进行独立验证，
    对应 user_profile.md 中 E1 升级版铁律 + Subagent 工具证据不可盲信原则。

    核心场景：
      1. prior session 报告"修复已落地" -> 本工具用 Grep 验证文件内容是否实际包含修复后的值
      2. prior session 报告"已保护 X 不受影响" -> 本工具用 Grep 验证 X 是否真的未被改动
      3. subagent 报告"0 finding" -> 本工具独立 Grep 验证关键声明

使用方式：
    # 验证修复落地：搜索"修复前的值"应 0 命中，"修复后的值"应 >=1 命中
    python scripts/drl_spotcheck.py --file path/to/file.md --old "旧值" --new "新值"

    # 验证"未改动"声明：搜索某关键词应仍存在
    python scripts/drl_spotcheck.py --file path/to/file.md --must-still-contain "关键词"

    # 批量验证多个修复点
    python scripts/drl_spotcheck.py --batch spotcheck.yaml
    # spotcheck.yaml 格式：
    #   - file: path/to/file.md
    #     checks:
    #       - old: "旧值1"
    #         new: "新值1"
    #       - must_still_contain: "关键词"

退出码：0 全部 spot-check 通过 / 1 有失败
"""
import argparse
import re
import sys
from pathlib import Path


def check_replacement(file_path: Path, old: str, new: str) -> tuple[bool, str]:
    """验证修复落地：old 应 0 命中，new 应 >=1 命中。"""
    if not file_path.exists():
        return False, f"[MISS] 文件不存在: {file_path}"
    text = file_path.read_text(encoding="utf-8")

    old_hits = len(re.findall(re.escape(old), text))
    new_hits = len(re.findall(re.escape(new), text))

    if old_hits > 0 and new_hits == 0:
        return False, f"[FAIL] 修复未落地：old='{old}' 命中 {old_hits} 次，new='{new}' 命中 0 次"
    if old_hits > 0 and new_hits > 0:
        return False, f"[WARN] 部分修复：old='{old}' 仍命中 {old_hits} 次（new='{new}' 已命中 {new_hits} 次，可能多处需 replace_all）"
    if old_hits == 0 and new_hits == 0:
        return False, f"[WARN] 两值均未命中：old='{old}' 0 次 + new='{new}' 0 次（可能行号/路径有误）"
    # old=0 + new>=1
    return True, f"[OK] 修复已落地：old='{old}' 0 次，new='{new}' {new_hits} 次"


def check_must_contain(file_path: Path, keyword: str) -> tuple[bool, str]:
    """验证"未改动"声明：keyword 应仍存在。"""
    if not file_path.exists():
        return False, f"[MISS] 文件不存在: {file_path}"
    text = file_path.read_text(encoding="utf-8")
    hits = len(re.findall(re.escape(keyword), text))
    if hits == 0:
        return False, f"[FAIL] 声明未改动但关键词消失：'{keyword}' 命中 0 次"
    return True, f"[OK] 关键词仍存在：'{keyword}' 命中 {hits} 次"


def run_batch(batch_path: Path) -> int:
    """批量验证（YAML 格式）。"""
    try:
        import yaml
    except ImportError:
        sys.exit("[ERROR] 批量模式需要 PyYAML：pip install pyyaml")
    data = yaml.safe_load(batch_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        sys.exit("[ERROR] batch 文件顶层应为 list")

    all_ok = True
    for item in data:
        file_path = Path(item["file"])
        checks = item.get("checks", [])
        for chk in checks:
            if "old" in chk and "new" in chk:
                ok, msg = check_replacement(file_path, chk["old"], chk["new"])
            elif "must_still_contain" in chk:
                ok, msg = check_must_contain(file_path, chk["must_still_contain"])
            else:
                ok, msg = False, f"[ERROR] 无法识别的 check 格式: {chk}"
            print(f"  {msg}")
            if not ok:
                all_ok = False
    return 0 if all_ok else 1


def main():
    parser = argparse.ArgumentParser(
        description="DRL 真循环 spot-check 工具（E1 升级版铁律落地）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
典型场景：
  # 1. 验证修复落地
  python scripts/drl_spotcheck.py --file README.md --old "v2.2.14" --new "v2.2.15"

  # 2. 验证"未改动"声明
  python scripts/drl_spotcheck.py --file docs/foo.md --must-still-contain "关键术语"

  # 3. 批量验证（YAML）
  python scripts/drl_spotcheck.py --batch spotcheck.yaml
""")
    parser.add_argument("--file", help="待验证的文件路径")
    parser.add_argument("--old", help="修复前的值（应 0 命中）")
    parser.add_argument("--new", help="修复后的值（应 >=1 命中）")
    parser.add_argument("--must-still-contain", help="应仍存在的关键词（验证未改动声明）")
    parser.add_argument("--batch", help="批量验证 YAML 文件路径")
    args = parser.parse_args()

    if args.batch:
        return run_batch(Path(args.batch))

    if not args.file:
        parser.error("必须指定 --file 或 --batch")

    file_path = Path(args.file)

    if args.old and args.new:
        ok, msg = check_replacement(file_path, args.old, args.new)
        print(msg)
        return 0 if ok else 1

    if args.must_still_contain:
        ok, msg = check_must_contain(file_path, args.must_still_contain)
        print(msg)
        return 0 if ok else 1

    parser.error("必须指定 --old/--new 对 或 --must-still-contain")


if __name__ == "__main__":
    sys.exit(main())
