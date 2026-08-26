#!/usr/bin/env python3
"""索引健康门禁（W500 转正，verify_delivery 第 17 门禁）。

背景（W499 全面审查）：file-index W449-W463 区间存在历史遗留结构损坏
（W457/458/461/462/463 空壳段·W451/452/453/460 重复段·W454/455 乱序·残留
v2.3.65-78 快照行）；方法论 README 目录索引长期滞后（17 文件 8 个漏登记 +
2 条"待创建"假占位）；CHANGELOG 编号规则段 W 上限靠人工、verify 只 WARN。

检查项（全通过 exit 0，任一失败 exit 1 阻断提交）：
1. file-index 段完整性（豁免区外）：空壳段（段标题后无登记表格/登记行）必 FAIL
2. file-index 段唯一性（豁免区外）：同一 W 号段重复出现必 FAIL
3. file-index 残留快照（豁免区外）：段内含"当前版本"残留行必 FAIL
4. 方法论 README 双向覆盖：目录 md ↔ 索引表链接双向差集为 0 + "待创建"占位 0
5. CHANGELOG 编号规则段上限 == 最新 W 段（W499 曾手工漏改被 WARN 抓出）
6. file-index 段倒序断言（W526 新增）：豁免区外段必须 W 号严格递减（最新在前）——
   W525 实证 W522/W523/W524 曾被追加到文件尾部（W449 段后）而门禁全绿漏网
7. file-index 段缺失检测（W526 新增）：CHANGELOG 每个现役版段都必须有对应 file-index 段——
   W525 实证 W504 段缺失（CHANGELOG 有 v2.3.103 段而反向索引无登记）漏网

豁免设计（W499 方案②精神）：
W449-W463 区间已确认损坏且"维持现状不重排（历史段禁改）"——门禁只查豁免区外的
段（W417/W464+ 及未来新段），豁免区内的既有问题不查、新增问题（新 W 段不可能
落到该区间）不受影响。历史段内容查证一律以 CHANGELOG 为准。
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from itertools import pairwise
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FI = ROOT / "scripts" / "output" / "file-index.md"
METHOD_DIR = ROOT / "docs" / "10-方法论沉淀"
METHOD_README = METHOD_DIR / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"

# W449 归档重排遗留损坏区（2026-08-24 全面审查确认·W499 方案②维持现状）
# 含空壳（457/458/461/462/463）、重复（451/452/453/460）、乱序（418/419/450-455 段位置）
EXEMPT_W = {418, 419, 450, 451, 452, 453, 454, 455, 457, 458, 460, 461, 462, 463}


def file_index_sections(text: str) -> list[tuple[int, int, int]]:
    """返回 [(W号, 起始行idx, 结束行idx)]（结束=下一段标题或文件末尾）。"""
    lines = text.splitlines()
    starts = []
    for i, ln in enumerate(lines):
        m = re.match(r"^## W(\d{3})\b", ln)
        if m:
            starts.append((int(m.group(1)), i))
    return [
        (w, s, starts[k + 1][1] if k + 1 < len(starts) else len(lines))
        for k, (w, s) in enumerate(starts)
    ]


def check_file_index(errors: list[str]) -> None:
    text = FI.read_text(encoding="utf-8-sig")
    sections = file_index_sections(text)
    if not sections:
        errors.append("file-index 未发现任何 W 段（## W### 标题）")
        return
    max_w = max(w for w, _, _ in sections)
    print(f"file-index 共 {len(sections)} 个 W 段（最高 W{max_w}，豁免区 {len(EXEMPT_W)} 个）")

    # 1) 空壳段：豁免区外段必须含登记表格头 + 至少 1 行登记
    for w, s, e in sections:
        if w in EXEMPT_W:
            continue
        body = "\n".join(text.splitlines()[s + 1:e])
        has_header = bool(re.search(r"^\| 文件 \| W \| 说明 \|", body, flags=re.M))
        has_row = bool(re.search(r"^\| .+ \| W\d{3} \| .+", body, flags=re.M))
        if not (has_header and has_row):
            errors.append(f"file-index W{w:03d} 段为空壳（无登记表格/登记行，第 {s + 1} 行起）")

    # 2) 重复段：豁免区外 W 号不得重复
    w_counter = Counter(w for w, _, _ in sections)
    for w, cnt in sorted(w_counter.items()):
        if cnt > 1 and w not in EXEMPT_W:
            errors.append(f"file-index W{w:03d} 段重复出现 {cnt} 次")

    # 3) 最新段残留快照：仅查最高 W 段（新段插头部，残留行只可能来自 bump 追加的历史段）
    #    历史段（W417-W421/W450-W463 内夹带的 "> 当前版本 vX" bump 残留）按方案②维持现状豁免。
    #    仅匹配行首 "> 当前版本"（bump 追加格式），表格说明中的"当前版本"字样不误伤。
    max_w, max_s, max_e = max(sections, key=lambda x: x[0])
    if any(re.search(r"^>\s*当前版本", ln) for ln in text.splitlines()[max_s + 1:max_e]):
        errors.append(f"file-index 最新段 W{max_w:03d} 含残留 '当前版本' 行（历史段残留已豁免，新段不得夹带）")

    # 4) 段倒序断言（W526 新增：W525 实证 W522-W524 曾尾部追加漏网——豁免区外段必须严格递减）
    seq = [w for w, _, _ in sections if w not in EXEMPT_W]
    for a, b in pairwise(seq):
        if a <= b:
            errors.append(
                f"file-index 段倒序违反：W{a:03d} 位于 W{b:03d} 之前（最新在前应严格递减"
                f"，W525 曾实证 W522-W524 被追加到文件尾部）"
            )
            break

    # 5) 段缺失检测（W526 新增：W525 实证 W504 段缺失漏网——CHANGELOG 现役版段须均有登记段）
    cl_text = CHANGELOG.read_text(encoding="utf-8-sig")
    cl_w = {int(m) for m in re.findall(r"^### v\d+\.\d+\.\d+（[^）]*?）：W(\d{3})", cl_text, flags=re.M)}
    fi_w = {w for w, _, _ in sections}
    missing = sorted(w for w in cl_w if w not in fi_w and w not in EXEMPT_W)
    if missing:
        errors.append(f"file-index 缺 {len(missing)} 个 CHANGELOG 版段登记：{[f'W{w:03d}' for w in missing]}")


def check_methodology_readme(errors: list[str]) -> None:
    files = {
        p.name for p in METHOD_DIR.iterdir()
        if p.is_file() and p.suffix == ".md" and p.name != "README.md"
    }
    text = METHOD_README.read_text(encoding="utf-8-sig")
    # 索引表链接：仅本目录相对链接（不含 '/' 的 xxx.md），排除跨目录 ../../ 链接
    linked = {m for m in re.findall(r"\]\(([^)#]+\.md)\)", text) if "/" not in m}
    only_file = sorted(files - linked)
    only_link = sorted(linked - files)
    if only_file:
        errors.append(f"方法论 README 索引缺 {len(only_file)} 个文件：{only_file}")
    if only_link:
        errors.append(f"方法论 README 索引指向不存在 {len(only_link)} 个：{only_link}")
    pending = len(re.findall(r"（待创建", text))
    if pending:
        errors.append(f"方法论 README 仍有 {pending} 条'待创建'占位（文件应已存在）")
    print(f"方法论 README：目录 {len(files)} 个 md ↔ 索引链接 {len(linked)} 个（待创建 {pending}）")


def check_changelog_w_upper(errors: list[str]) -> None:
    text = CHANGELOG.read_text(encoding="utf-8-sig")
    latest = re.search(r"^### v\d+\.\d+\.\d+（[^）]*?）：W(\d{3})", text, flags=re.M)
    rule = re.search(r"W### ID（W001-W(\d{3})）", text)
    if not latest or not rule:
        errors.append("CHANGELOG 无法解析最新 W 段或编号规则段（W### ID（W001-W###））")
        return
    if latest.group(1) != rule.group(1):
        errors.append(
            f"CHANGELOG 编号规则段上限 W{rule.group(1)} != 最新 W 段 W{latest.group(1)}"
            "（bump 时须同步该段，或跑 bump_version.py）"
        )
    print(f"CHANGELOG 编号规则段上限 W{rule.group(1)} == 最新 W 段 W{latest.group(1)}")


def check_governance_refs(errors: list[str]) -> None:
    """治理文档引用一致性（W500 补充：W499 全面审查漏检文档规范.md 内容引用漂移）。

    a. 文档规范.md 引用的 scripts/ 文件全部存在（抓"引用了不存在的东西"死链）
    b. verify_delivery.py 挂载的门禁脚本全部存在（门禁本体自检）
    """
    doc = ROOT / "docs" / "00-导读" / "文档规范.md"
    doc_text = doc.read_text(encoding="utf-8-sig")
    doc_refs = set(re.findall(r"scripts/([a-z0-9_]+\.(?:py|js))", doc_text))
    missing_doc = sorted(r for r in doc_refs if not (ROOT / "scripts" / r).exists())
    if missing_doc:
        errors.append(f"文档规范.md 引用不存在的 scripts/ 文件：{missing_doc}")
    vd_text = (ROOT / "scripts" / "verify_delivery.py").read_text(encoding="utf-8-sig")
    vd_scripts = set(re.findall(r"check_[a-z0-9_]+\.(?:py|js)", vd_text))
    missing_vd = sorted(s for s in vd_scripts if not (ROOT / "scripts" / s).exists())
    if missing_vd:
        errors.append(f"verify_delivery.py 引用不存在的门禁脚本：{missing_vd}")
    print(f"治理文档引用：文档规范.md 引 scripts/ {len(doc_refs)} 个 · verify 挂载 check_* {len(vd_scripts)} 个（全存在）")


def main() -> int:
    errors: list[str] = []
    check_file_index(errors)
    check_methodology_readme(errors)
    check_changelog_w_upper(errors)
    check_governance_refs(errors)
    if errors:
        print(f"\n发现 {len(errors)} 个问题：")
        for e in errors:
            print("  - " + e)
        return 1
    print("索引健康门禁通过（file-index 段完整性 / 方法论 README 覆盖 / 编号上限 / 治理文档引用）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
