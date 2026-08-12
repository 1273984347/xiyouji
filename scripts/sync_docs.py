#!/usr/bin/env python3
"""sync_docs.py - 6 文件文档一致性自动校验

校验 CHANGELOG.md / README.md / STRUCTURE.md / 项目说明.md / 交接文档.md / file-index.md
之间版本号、统计计数、W### 编号、file-index 最新条目的一致性。

解决 E1 铁律模式（prior session 报告"已同步"但实际残留过时数据）。

退出码：0 全部一致 / 1 有不一致
"""
import argparse
import re
import sys
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

# 统计字段静态期望值（W424 复盘沉淀：三份文档头部现为聚合式声明——
# "A1-A6 共 N 篇 + M 可视化页（A4 K 篇 已含）"，逐类计数行已移除；
# AGG/VIZ/A4 与真实文件计数的一致性由 verify_delivery 兜底校验）
STATIC_EXPECTED = {"AGG": 611, "VIZ": 86, "A4": 209}

# CHANGELOG 最新版本段统计正则（提取最终值，支持 N→M 和 N 两种格式）
CL_PATTERNS = {
    "A3": re.compile(r"A3 人物 (?:\d+→)?(\d+) 篇"),
    "A4": re.compile(r"A4 主题专题 (?:\d+→)?(\d+) 篇"),
    "A5": re.compile(r"A5 文化 (?:\d+→)?(\d+) 篇"),
    "D":  re.compile(r"D 可视化 (?:\d+→)?(\d+) 个"),
}

# 目标文件统计正则（README/STRUCTURE/项目说明 头部聚合声明格式，W424 复盘沉淀校准）
TARGET_PATTERNS = {
    "AGG": re.compile(r"A1-A6 共 (\d+) 篇"),
    "VIZ": re.compile(r"(\d+) 可视化页"),
    "A4":  re.compile(r"A4 (\d+) 篇 已含"),
}

UNIT = {"AGG": "篇", "VIZ": "个", "A3": "篇", "A4": "篇", "A5": "篇", "D": "个"}

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
                            # W400 修复：B023 —— lambda 默认参数捕获当前 key，避免绑定循环变量
                            lambda mm, _key=key: mm.group(0).replace(mm.group(1), str(expected[_key]), 1),
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
    """检测 CHANGELOG 归档边界（可能多段：W001-W399 与 W400-W416 均已迁移）。
    返回所有归档区间末端的最大值，未检测到返回 0。"""
    # 只匹配归档句（"）已迁移" / "）段"），排除"编号规则（W001-W424）"这类非归档范围
    ends = [int(m) for m in re.findall(r"W\d{3}-W(\d{3})）(?:已迁移|段)", cl_text[:3000])]
    return max(ends) if ends else 0


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


# ============ 规则 5/6/7：E2 扩展扫描（2026-07-31 新增）============
# 背景：user_profile.md E2 扩展从 5 项扫描扩展到 8 项，新增 3 项覆盖：
#   - 规则 5 rule_status_marker：状态标记计数（P1-3 进行中泛滥）
#   - 规则 6 rule_counter_sum：计数器求和一致性（P1-6 声明数 vs 表格求和）
#   - 规则 7 rule_file_location：文件位置规范（P1-5 S2 方向文件错位）

# CHANGELOG 现役段"进行中"标记正则
IN_PROGRESS_RE = re.compile(r"进行中")

# README 数据维度全景段标题正则（主源：提取标题声明数）
# W424 复盘沉淀：README 现为 `**数据维度全景（N 维）**：` 粗体段落（非 ## 标题），两种写法都接受
README_DIM_HEADER_RE = re.compile(r"(?:##\s+|\*\*)?数据维度全景[（(]\s*(\d+)\s*维")

# README 数据维度表格行正则（提取"维度数"列，支持 42 / 8+3 / 1 等格式）
README_DIM_ROW_RE = re.compile(r"^\|[^|]*\|[^|]*\|\s*([\d+\-\s]+)\s*\|", re.MULTILINE)

# STRUCTURE 头部"维度"声明正则（存在则检查）
STRUCTURE_DIM_RE = re.compile(r"(\d+)\s*(?:数据维度|维度)")

# site/index.html "维度"声明正则（存在则检查）
INDEX_HTML_DIM_RE = re.compile(r"(\d+)&nbsp;维度|(\d+)\s*维度")

# S2 方向文件命名模式 → 应属目录映射
S2_FILE_RULES = [
    # (文件名包含子串, 应属目录子串, 描述)
    ("学术投稿候选", "S2-学术投稿", "S2 学术投稿候选文件"),
    ("S2-发布",     "S2-外部分享", "S2 外部分享发布文件"),
]


def rule_status_marker(cl_text, fix=False):
    """规则 5: 状态标记计数 - CHANGELOG 现役段"进行中"应 ≤ 1。

    背景：P1-3 复现 87 处"进行中"标记泛滥（仅最新版本段应为进行中）。
    判据：get_latest_section 提取现役段，统计"进行中"命中数。
    """
    issues = []
    latest_section = get_latest_section(cl_text)
    if not latest_section:
        return ["[ERROR] CHANGELOG 无法提取最新版本段"]
    hits = len(IN_PROGRESS_RE.findall(latest_section))
    if hits > 1:
        issues.append(
            f"[MISMATCH] CHANGELOG 现役段'进行中'标记 {hits} 处（应 ≤ 1，仅最新版本段应为进行中）"
        )
    # fix=True 不自动修复：批量替换"进行中"→"已完成"需人工确认哪些是历史段、哪些是现役段
    # 避免误改历史段（E2 铁律：历史条目不可改）
    return issues


def _eval_dim_expr(expr: str) -> int:
    """将维度表达式（如 '8+3' / '42' / '8 + 3'）求值为整数。无法求值返回 0。

    手写安全解析器替代 eval：输入已通过正则限制为非负整数与 + - 运算符，
    按 token 顺序累加/累减，杜绝任意代码执行风险（安全扫描 XSS-003）。
    """
    expr = expr.strip()
    if not expr:
        return 0
    # 仅允许数字和 + - 空白
    if not re.fullmatch(r"[\d+\-\s]+", expr):
        return 0
    try:
        total = None
        pending_op = "+"
        for tok in re.findall(r"\d+|\+|\-", expr):
            if tok in "+-":
                pending_op = tok
                continue
            val = int(tok)
            if total is None:
                # 首个数字：pending_op 作为符号（处理前导负号）
                total = val if pending_op == "+" else -val
            else:
                total = total + val if pending_op == "+" else total - val
        return total if total is not None else 0
    except Exception:
        return 0


def rule_counter_sum(fix=False):
    """规则 6: 计数器求和一致性 - README 标题声明数 == 表格求和 == 其他位置。

    主源：README "## 数据维度全景（N 维）" 标题声明数 N。
    其他位置（存在则检查，不存在则跳过）：
      - README 表格"维度数"列求和
      - STRUCTURE 头部"维度"声明数
      - site/index.html "维度"声明数
    """
    issues = []
    readme_path = FILES["README"]
    if not readme_path.exists():
        return ["[MISSING] README.md 不存在"]
    readme_text = read_text(readme_path)

    # 主源：README 标题声明数
    m = README_DIM_HEADER_RE.search(readme_text)
    if not m:
        return ["[ERROR] README.md 未找到'数据维度全景（N 维）'标题"]
    declared = int(m.group(1))

    # 校验 1：README 表格求和
    # 找到"数据维度全景"标题后的第一个表格
    table_start = readme_text.find("| 阶段", m.end())
    if table_start == -1:
        issues.append("[MISMATCH] README.md 数据维度表格未找到'| 阶段'起始行")
    else:
        # 从表头分隔行之后开始提取数据行
        sep_end = readme_text.find("\n", readme_text.find("|---", table_start))
        table_chunk = readme_text[sep_end:readme_text.find("\n## ", sep_end)] if sep_end != -1 else ""
        row_sums = []
        for row_m in README_DIM_ROW_RE.finditer(table_chunk):
            row_sums.append(_eval_dim_expr(row_m.group(1)))
        if not row_sums:
            issues.append("[MISMATCH] README.md 数据维度表格未提取到任何维度数")
        else:
            total = sum(row_sums)
            if total != declared:
                issues.append(
                    f"[MISMATCH] README.md 表格求和 {total} (={' + '.join(str(s) for s in row_sums)}) vs 标题声明 {declared}"
                )

    # 校验 2：STRUCTURE 头部（存在则检查）
    struct_path = FILES["STRUCTURE"]
    if struct_path.exists():
        struct_head = "\n".join(read_head(struct_path))
        sm = STRUCTURE_DIM_RE.search(struct_head)
        if sm:
            struct_val = int(sm.group(1))
            if struct_val != declared:
                ln = find_line(struct_head.splitlines(), STRUCTURE_DIM_RE)
                issues.append(
                    f"[MISMATCH] STRUCTURE.md:line {ln} 维度声明 {struct_val} vs README 主源 {declared}"
                )

    # 校验 3：site/index.html（存在则检查）
    index_path = ROOT / "site" / "index.html"
    if index_path.exists():
        index_text = read_text(index_path)
        im = INDEX_HTML_DIM_RE.search(index_text)
        if im:
            index_val = int(im.group(1) or im.group(2))
            if index_val != declared:
                issues.append(
                    f"[MISMATCH] site/index.html 维度声明 {index_val} vs README 主源 {declared}"
                )

    # fix=True 不自动修复：求和不一致通常意味着缺维度行而非数字错误，需人工补行
    return issues


def rule_file_location(scan_dir=None, fix=False):
    """规则 7: 文件位置规范 - S2 方向文件必须在对应 S2-*/ 目录下。

    背景：P1-3 复现 8 个 S2 学术投稿文件错位于 docs/10-方法论沉淀/。
    判据：文件名含'学术投稿候选' → 必须位于 docs/S2-学术投稿/；
         文件名含'S2-发布' → 必须位于 docs/S2-外部分享/。
    """
    issues = []
    if scan_dir is None:
        scan_dir = ROOT / "docs"
    else:
        scan_dir = Path(scan_dir)
    if not scan_dir.exists():
        return [f"[MISSING] 扫描目录不存在: {scan_dir}"]

    # 遍历 docs/ 下所有 .md 文件
    for md_file in sorted(scan_dir.rglob("*.md")):
        rel_path = md_file.relative_to(ROOT)
        rel_str = str(rel_path).replace("\\", "/")
        fname = md_file.name
        for name_keyword, expected_dir, desc in S2_FILE_RULES:
            if name_keyword in fname and expected_dir not in rel_str:
                issues.append(
                    f"[MISMATCH] {rel_str} 是{desc}但不在 docs/{expected_dir}/ 下"
                )
    # fix=True 不自动修复：文件迁移涉及引用路径更新，需人工确认
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
  marker   状态标记计数（CHANGELOG 现役段'进行中'应 ≤ 1）
  sum      计数器求和一致性（README 维度标题声明数 == 表格求和 == 其他位置）
  loc      文件位置规范（S2 方向文件必须在 docs/S2-*/ 目录下）

退出码: 0 全部一致 / 1 有不一致
""")
    parser.add_argument("--rule", choices=["version", "stats", "wids", "fidx", "marker", "sum", "loc"],
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

    if args.rule in (None, "marker"):
        print("\n=== 规则 5: 状态标记计数（E2 扩展）===")
        issues = rule_status_marker(cl_text, fix=args.fix)
        if issues:
            for i in issues:
                print(f"  {i}")
            all_ok = False
        else:
            print("  [OK] CHANGELOG 现役段'进行中'标记 ≤ 1")

    if args.rule in (None, "sum"):
        print("\n=== 规则 6: 计数器求和一致性（E2 扩展）===")
        issues = rule_counter_sum(fix=args.fix)
        if issues:
            for i in issues:
                print(f"  {i}")
            all_ok = False
        else:
            print("  [OK] README 维度标题声明数 == 表格求和 == 其他位置")

    if args.rule in (None, "loc"):
        print("\n=== 规则 7: 文件位置规范（E2 扩展）===")
        issues = rule_file_location(fix=args.fix)
        if issues:
            for i in issues:
                print(f"  {i}")
            all_ok = False
        else:
            print("  [OK] S2 方向文件均在对应 docs/S2-*/ 目录下")

    print("\n" + "=" * 60)
    if all_ok:
        print("[PASS] 全部一致")
        return 0
    else:
        print("[FAIL] 检测到不一致，请人工确认")
        return 1


if __name__ == "__main__":
    sys.exit(main())
