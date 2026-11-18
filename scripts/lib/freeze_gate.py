#!/usr/bin/env python3
"""freeze_gate.py — 存量基线冻结门禁共用语义（W1265 批一·判据补盲）。

为什么需要这一层：新判据在现役站上会**立刻**命中存量违例（这些违例正由并行的页面线修复），
但判据本身不能为了让门禁变绿而放宽 ⇒ 统一采用「基线冻结 + 报告」形态：
判据强度不变，违例照实报出，只是把**已在基线内的存量**记为「存量基线」不计 FAIL，
基线外新增违例照样 FAIL；页面修完后收紧基线即可归零。

三档模式（所有 W1265 新判据统一）：
  门禁默认档（gate）   违例键 ∈ 基线 → 记「存量基线」·不计 FAIL；∉ 基线 → FAIL；
                       基线文件缺失 → FAIL（fail-closed·拒绝通过·不静默跳过）；
                       基线内违例已消失 → 「可收紧」提示（提示删行·不判红）。
  零容忍档（--strict） 任何违例（含基线内）→ FAIL。基线文件此时不参与判定。
  报告档（--report）   只报数·退出码 0（供生成基线与普查用）。

基线文件格式（纯文本·一行一违例键·'#' 开头为注释）：
  # 生成：<时间戳> · 违例 N 条
  <违例键>

违例键约定：<页面相对路径>|<违例码>|<细节>（同页同码同细节只记一条·便于逐条对账）。
"""
from __future__ import annotations

import time
from pathlib import Path

FROZEN_LABEL = "存量基线"


def read_baseline(path: Path) -> tuple[set[str], list[str]]:
    """读基线文件 → (违例键集合, 问题列表)。文件缺失 → 问题含「基线文件缺失」。"""
    if not path.exists():
        return set(), ["基线文件缺失: %s（fail-closed·拒绝通过）" % path]
    keys: set[str] = set()
    problems: list[str] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return set(), ["基线文件不可读: %s（%s）" % (path, exc)]
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        keys.add(s)
    return keys, problems


def write_baseline(path: Path, keys, header_lines: list[str]) -> int:
    """写基线文件（违例键去重排序）。返回写入条数。"""
    uniq = sorted(set(keys))
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = list(header_lines)
    lines.append("# 违例键 %d 条（生成：%s）" % (len(uniq), time.strftime("%Y-%m-%d %H:%M:%S")))
    lines.extend(uniq)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(uniq)


def write_baseline_ratcheted(path: Path, keys, header_lines: list[str], allow_grow: bool = False) -> int:
    """基线棘轮写法（W1277 对抗审查 P3-1·新函数不改 write_baseline 契约）。

    新键数 > 既有键数（冻结面增长=洗白面增长）时默认拒绝，须显式 allow_grow=True
    （CLI 的 --generate-baseline/--update-baseline 即人工复核后的显式动作·E-99 纪律）。
    只降不升：修复导致的缩减恒放行。回归锁：tests/unit/test_w1277_p3_fixes.py。
    """
    file_exists = path.exists()
    old_keys = 0
    if file_exists:
        try:
            old_keys = sum(
                1 for _ln in path.read_text(encoding="utf-8").splitlines()
                if _ln and not _ln.startswith("#")
            )
        except OSError:
            old_keys = 0
    uniq = sorted(set(keys))
    # 首建（文件不存在）恒放行——棘轮只约束「已有基线上的冻结面增长」
    if file_exists and len(uniq) > old_keys and not allow_grow:
        raise AssertionError(
            "基线增长被拒（%d → %d 条·洗白面扩大）——人工复核后以 allow_grow=True 显式放行"
            % (old_keys, len(uniq))
        )
    return write_baseline(path, uniq, header_lines)


def evaluate(violations, baseline: set[str], strict: bool) -> dict:
    """把违例与基线对拍 → {frozen, new_fail, fixed, total}。

    strict=True（零容忍）：全部违例进 new_fail，基线不参与判定。
    strict=False（门禁默认）：基线内 → frozen（不计 FAIL）；基线外 → new_fail（FAIL）。
    """
    vset = set(violations)
    if strict:
        return {"frozen": [], "new_fail": sorted(vset), "fixed": [], "total": len(vset)}
    return {
        "frozen": sorted(vset & baseline),
        "new_fail": sorted(vset - baseline),
        "fixed": sorted(baseline - vset),
        "total": len(vset),
    }


def print_eval(res: dict, marker: str, strict: bool, sample: int = 12) -> None:
    """打印标准口径的判据结论行（marker 行是 verify_delivery 挂槽依据·必须存在）。"""
    print(
        "%s 违例 %d 条 · %s %d 条 · 基线外新增 %d 条 · %s"
        % (
            marker,
            res["total"],
            FROZEN_LABEL,
            len(res["frozen"]),
            len(res["new_fail"]),
            "FAIL" if res["new_fail"] else "OK",
        )
    )
    for k in res["new_fail"][:sample]:
        print("  ✗ 新增/未登记违例 " + k)
    if len(res["new_fail"]) > sample:
        print("  …其余 %d 条略" % (len(res["new_fail"]) - sample))
    if res["frozen"]:
        print("  · %s（%d 条）：%s" % (FROZEN_LABEL, len(res["frozen"]), " / ".join(res["frozen"][:4])))
    if res["fixed"]:
        print("  · 可收紧（基线内违例已消失 %d 条·建议删行）：%s" % (len(res["fixed"]), " / ".join(res["fixed"][:4])))
    if strict:
        print("  · 零容忍模式（--strict）：基线不参与判定·全部违例计 FAIL")
