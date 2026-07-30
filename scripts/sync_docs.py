#!/usr/bin/env python3
"""sync_docs.py - 6 文件文档一致性自动校验

校验 CHANGELOG.md / README.md / STRUCTURE.md / 项目说明.md / 交接文档.md / file-index.md
之间版本号、统计计数、W### 编号、file-index 最新条目的一致性。

解决 E1 铁律模式（prior session 报告"已同步"但实际残留过时数据）。

退出码：0 全部一致 / 1 有不一致
"""
import re
import sys
import argparse
from pathlib import Path

# 项目根目录（脚本位于 scripts/ 下）
ROOT = Path(__file__).resolve().parent.parent

# 6 文件路径
FILES = {
    "CHANGELOG":  ROOT / "CHANGELOG.md",
    "README":     ROOT / "README.md",
    "STRUCTURE":  ROOT / "STRUCTURE.md",
    "项目说明":    ROOT / "docs" / "00-导读" / "项目说明.md",
    "交接文档":    ROOT / "交接文档.md",
    "file-index": ROOT / "scripts" / "output" / "file-index.md",
}

HEADER_LINES = 50  # 头部扫描行数

# 统计字段静态期望值（A1/A2/A6 不变；A3/A4/A5/D 从 CHANGELOG 动态提取后覆盖）
STATIC_EXPECTED = {"A1": 100, "A2": 43, "A6": 2}

# CHANGELOG 最新版本段统计正则（提取最终值，支持 N→M 和 N 两种格式）
CL_PATTERNS = {
    "A3": re.compile(r"A3 人物 (?:\d+→)?(\d+) 篇"),
    "A4": re.compile(r"A4 主题专题 (?:\d+→)?(\d+) 篇"),
    "A5": re.compile(r"A5 文化 (?:\d+→)?(\d+) 篇"),
    "D":  re.compile(r"D 可视化 (?:\d+→)?(\d+) 个"),
}

# 目标文件统计正则（README/STRUCTURE/项目说明 头部格式）
TARGET_PATTERNS = {
    "A1": re.compile(r"A1 逐回解读 (\d+) 回"),
    "A2": re.compile(r"A2 个人随笔 (\d+) 篇"),
    "A3": re.compile(r"A3 人物深化 (\d+) 篇"),
    "A4": re.compile(r"A4 主题专题 (\d+) 篇"),
    "A5": re.compile(r"A5 文化背景 (\d+) 篇"),
    "A6": re.compile(r"A6 诗词 (\d+) 篇"),
    "D":  re.compile(r"(\d+) 个 D3\.js 可视化页面"),
}

UNIT = {"A1": "回", "A2": "篇", "A3": "篇", "A4": "篇", "A5": "篇", "A6": "篇", "D": "个"}

VERSION_RE = re.compile(r"^###\s+(v\d+\.\d+\.\d+)", re.MULTILINE)
ANY_VER_RE = re.compile(r"v\d+\.\d+\.\d+")
WID_RE = re.compile(r"\bW(\d{3})\b")
WID_RANGE_RE = re.compile(r"W\d{3}-W\d{3}")
WID_SUBVER_RE = re.compile(r"W\d{3}\.\d")  # 子版本如 W008.1


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def read_head(path, n=HEADER_LINES):
    return read_text(path).splitlines()[:n]


def extract_individual_wids(text):
    """提取独立 W### ID（排除 range 语句 Wxxx-Wyyy 和子版本 Wxxx.d）"""
    cleaned = WID_RANGE_RE.sub("", text)
    cleaned = WID_SUBVER_RE.sub("", cleaned)
    return sorted(set(int(m) for m in WID_RE.findall(cleaned)))


def get_latest_version(cl_text):
    m = VERSION_RE.search(cl_text)
    return m.group(1) if m else None


def get_latest_section(cl_text):
    """获取最新版本段（从 ### vX.Y.Z 到下一个 ### vX.Y.Z）"""
    matches = list(VERSION_RE.finditer(cl_text))
    if not matches:
        return ""
    start = matches[0].start()
    end = matches[1].start() if len(matches) > 1 else len(cl_text)
    return cl_text[start:end]


def find_line(lines, pattern):
    for i, line in enumerate(lines, 1):
        if pattern.search(line):
            return i
    return 0


def extract_final_value(pattern, text):
    """从 text 中提取统计字段最终值（取所有匹配最大值，处理 N→M 序列）"""
    matches = pattern.findall(text)
    if not matches:
        return None
    return max(int(m) for m in matches)


def rule_version(latest_v, fix=False):
    """规则 1: 版本号一致性 - 校验 4 文件头部 50 行含最新版本号
    注：file-index.md 头部只有"历史归档"说明（含旧版本号），无"当前版本"声明，
    其完整性由规则 4（最新 W### 条目）覆盖，故不纳入此规则。"""
    issues = []
    if not latest_v:
        return ["[ERROR] CHANGELOG.md 顶部未找到版本号"]
    for name in ["README", "STRUCTURE", "项目说明", "交接文档"]:
        path = FILES[name]
        if not path.exists():
            issues.append(f"[MISSING] {name} 文件不存在: {path}")
            continue
        head = read_head(path)
        head_text = "\n".join(head)
        if latest_v in head_text:
            continue
        found = ANY_VER_RE.findall(head_text)
        actual = found[0] if found else "(无)"
        ln = find_line(head, ANY_VER_RE) or 1
        issues.append(f"[MISMATCH] {name}:line {ln} 期望 {latest_v} vs 实际 {actual}")
        if fix and found:
            full = read_text(path)
            new = full.replace(found[0], latest_v, 1)
            path.write_text(new, encoding="utf-8")
            print(f"  [FIXED] {name}: {found[0]} -> {latest_v}")
    return issues


def rule_stats(latest_section, fix=False):
    """规则 2: 统计计数一致性 - 校验 README/STRUCTURE/项目说明 头部统计数字。

    fix=True 时按 expected 值就地替换 actual（仅替换单行内首个匹配的数字）。
    """
    issues = []
    fixed = []
    expected = dict(STATIC_EXPECTED)
    for key, pat in CL_PATTERNS.items():
        v = extract_final_value(pat, latest_section)
        if v is not None:
            expected[key] = v
    for name in ["README", "STRUCTURE", "项目说明"]:
        path = FILES[name]
        if not path.exists():
            issues.append(f"[MISSING] {name} 文件不存在")
            continue
        head = read_head(path)
        head_text = "\n".join(head)
        for key, pat in TARGET_PATTERNS.items():
            if key not in expected:
                continue
            m = pat.search(head_text)
            if not m:
                ln = find_line(head, re.compile(re.escape(key)))
                issues.append(f"[MISMATCH] {name}:line {ln or 1} {key} 期望 {expected[key]}{UNIT[key]} vs 实际 (未找到)")
                continue
            actual = int(m.group(1))
            if actual != expected[key]:
                ln = find_line(head, pat)
                issues.append(f"[MISMATCH] {name}:line {ln} {key} 期望 {expected[key]}{UNIT[key]} vs 实际 {actual}{UNIT[key]}")
                if fix:
                    # 在原文中按精确行替换：找到匹配行，把数字部分替换为期望值
                    full_text = read_text(path)
                    lines = full_text.splitlines(keepends=True)
                    if 0 < ln <= len(lines):
                        old_line = lines[ln - 1]
                        # 用反向引用替换：将 pat 第一个 group 的数字替换为 expected
                        new_line = pat.sub(
                            lambda mm: mm.group(0).replace(mm.group(1), str(expected[key]), 1),
                            old_line, count=1
                        )
                        if new_line != old_line:
                            lines[ln - 1] = new_line
                            path.write_text("".join(lines), encoding="utf-8")
                            fixed.append(f"{name}:line {ln} {key} {actual} -> {expected[key]}")
    if fixed:
        print("  [FIXED] 统计计数已自动更新：")
        for f in fixed:
            print(f"    {f}")
    return issues


def detect_archive_boundary(cl_text):
    """检测 CHANGELOG 归档边界（头部声明 W001-WXXX 已迁移至 archive）。
    返回边界值（WXXX 的 XXX），未检测到返回 0。"""
    m = re.search(r"W(\d{3})-W(\d{3})）已迁移", cl_text[:3000])
    return int(m.group(2)) if m else 0


def rule_wids(cl_text):
    """规则 3: W### 编号连续性 - CHANGELOG 连续 + file-index 条目一致。
    W001-WXXX 已归档至 CHANGELOG-ARCHIVE.md，仅检查归档边界以上的连续性。"""
    issues = []
    cl_wids = extract_individual_wids(cl_text)
    if not cl_wids:
        return ["[ERROR] CHANGELOG 未找到 W### 编号"]
    boundary = detect_archive_boundary(cl_text)
    # 仅检查归档边界以上的 W###（W001-WXXX 已归档，CHANGELOG 仅保留 W(XXX+1)+）
    active = [w for w in cl_wids if w > boundary]
    if not active:
        return ["[ERROR] CHANGELOG 未找到归档边界以上的 W### 编号"]
    cl_min, cl_max = active[0], active[-1]
    expected_seq = set(range(cl_min, cl_max + 1))
    missing = sorted(expected_seq - set(active))
    if missing:
        preview = ", ".join(f"W{w:03d}" for w in missing[:10])
        issues.append(f"[MISMATCH] CHANGELOG W### 跳号 (W{cl_min:03d}-W{cl_max:03d}): 缺 {len(missing)} 个 ({preview})")
    fidx_path = FILES["file-index"]
    if not fidx_path.exists():
        issues.append("[MISSING] file-index.md 不存在")
        return issues
    fidx_text = read_text(fidx_path)
    fidx_wids = set(extract_individual_wids(fidx_text))
    active_fidx = {w for w in fidx_wids if w > boundary}
    active_set = set(active)
    missing_in_fidx = sorted(active_set - active_fidx)
    if missing_in_fidx:
        preview = ", ".join(f"W{w:03d}" for w in missing_in_fidx[:10])
        issues.append(f"[MISMATCH] file-index.md 缺少 {len(missing_in_fidx)} 个 CHANGELOG W### 条目 ({preview})")
    cl_count = len(active_set)
    fidx_count = len(active_fidx & active_set)
    if fidx_count != cl_count:
        issues.append(f"[MISMATCH] W### 条目数 (W>{boundary:03d}): CHANGELOG {cl_count} vs file-index {fidx_count}")
    return issues


def rule_fileindex_latest(cl_text):
    """规则 4: file-index 最新条目 - file-index 应含最新 W### 条目"""
    issues = []
    cl_wids = extract_individual_wids(cl_text)
    if not cl_wids:
        return ["[ERROR] CHANGELOG 无 W### 编号"]
    latest_wid = cl_wids[-1]
    latest_tag = f"W{latest_wid:03d}"
    fidx_path = FILES["file-index"]
    if not fidx_path.exists():
        return ["[MISSING] file-index.md 不存在"]
    fidx_text = read_text(fidx_path)
    if latest_tag not in fidx_text:
        issues.append(f"[MISMATCH] file-index.md 缺少最新 W### 条目 {latest_tag}")
    return issues


def main():
    parser = argparse.ArgumentParser(
        description="6 文件文档一致性自动校验（解决 E1 铁律：prior session 报告'已同步'但残留过时数据）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
校验规则:
  version  版本号一致性（CHANGELOG 最新版本号在其他 5 文件头部 50 行出现）
  stats    统计计数一致性（A1/A2/A3/A4/A5/A6/D 在 README/STRUCTURE/项目说明 一致）
  wids     W### 编号连续性（CHANGELOG W### 连续 + file-index 条目一致）
  fidx     file-index 最新条目（file-index 应含最新 W### 条目）

退出码: 0 全部一致 / 1 有不一致
""")
    parser.add_argument("--rule", choices=["version", "stats", "wids", "fidx"],
                        help="只运行指定规则（默认全部）")
    parser.add_argument("--fix", action="store_true",
                        help="自动修复版本号 + 统计计数不一致")
    args = parser.parse_args()

    cl_path = FILES["CHANGELOG"]
    if not cl_path.exists():
        print(f"[FATAL] CHANGELOG.md 未找到: {cl_path}")
        return 1
    cl_text = read_text(cl_path)
    latest_v = get_latest_version(cl_text)
    latest_section = get_latest_section(cl_text)

    all_ok = True

    if args.rule in (None, "version"):
        print("=== 规则 1: 版本号一致性 ===")
        if latest_v:
            print(f"CHANGELOG 最新版本: {latest_v}")
        issues = rule_version(latest_v, fix=args.fix)
        if issues:
            for i in issues:
                print(f"  {i}")
            all_ok = False
        else:
            print("  [OK] 4 文件头部均含最新版本号")

    if args.rule in (None, "stats"):
        print("\n=== 规则 2: 统计计数一致性 ===")
        issues = rule_stats(latest_section, fix=args.fix)
        if issues:
            for i in issues:
                print(f"  {i}")
            all_ok = False
        else:
            print("  [OK] README/STRUCTURE/项目说明 统计计数一致")

    if args.rule in (None, "wids"):
        print("\n=== 规则 3: W### 编号连续性 ===")
        issues = rule_wids(cl_text)
        if issues:
            for i in issues:
                print(f"  {i}")
            all_ok = False
        else:
            print("  [OK] CHANGELOG W### 编号连续 + file-index 条目一致")

    if args.rule in (None, "fidx"):
        print("\n=== 规则 4: file-index 最新条目 ===")
        issues = rule_fileindex_latest(cl_text)
        if issues:
            for i in issues:
                print(f"  {i}")
            all_ok = False
        else:
            print("  [OK] file-index.md 包含最新 W### 条目")

    print("\n" + "=" * 60)
    if all_ok:
        print("[PASS] 全部一致")
        return 0
    else:
        print("[FAIL] 检测到不一致，请人工确认")
        return 1


if __name__ == "__main__":
    sys.exit(main())
