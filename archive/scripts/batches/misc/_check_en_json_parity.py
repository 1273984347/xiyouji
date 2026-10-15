#!/usr/bin/env python3
"""W627 检查器：site/en/json/ EN 数据副本对账（按需运行，非 verify 门禁）。

断言：
  R1 结构对账——每副本与 zh 源的记录数一致（COUNT_GUARDS 同款）；
  R2 CJK 残留不增——残留计数 ≤ 基线（生成时 17·zh 独有子树如实回退）；
  R3 可解析——全部为合法 JSON。
zh 源重生成（run_all）后必须重跑生成链：
  node scripts/_w627_extract_embedded.js && python scripts/_w627_gen_en_data.py

用法：python scripts/_check_en_json_parity.py   # 全过退出码 0
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"D:\xiyouji"
CJK = re.compile(r"[\u4e00-\u9fff]")
BASELINE_CJK = 17  # W627 生成时残留（zh 独有子树：axes/formula 等）
PAIRS = [
    ("villain_matrix", "villain_matrix.json", "villain_positions", 15),
    ("rescue_roi", "rescue_roi.json", "rescue_cases", 10),
    ("monster_clock", "monster_clock.json", "monster_schedules", 6),
]


def count_cjk(o):
    if isinstance(o, dict):
        return sum(count_cjk(v) for v in o.values())
    if isinstance(o, list):
        return sum(count_cjk(v) for v in o)
    return 1 if isinstance(o, str) and CJK.search(o) else 0


fails = []
total_cjk = 0
for _name, fname, key, want in PAIRS:
    zh = json.load(open(ROOT + r"\site\data\json" + "\\" + fname, encoding="utf-8"))
    en = json.load(open(ROOT + r"\site\en\json" + "\\" + fname, encoding="utf-8"))
    got_zh, got_en = len(zh.get(key, [])), len(en.get(key, []))
    if not (got_zh == got_en == want):
        fails.append(f"R1 {fname}: 记录数 {got_zh}/{got_en} != {want}")
    total_cjk += count_cjk(en)
for fname in ["methodology_summary.json", "chart_design_summary.json", "domino_causality.json", "spiral_progress.json"]:
    json.load(open(ROOT + r"\site\en\json" + "\\" + fname, encoding="utf-8"))  # R3 可解析
if total_cjk > BASELINE_CJK:
    fails.append(f"R2 CJK 残留 {total_cjk} > 基线 {BASELINE_CJK}（zh 源文本漂移？重跑生成链）")

if fails:
    print("\n".join("FAIL " + f for f in fails))
    print(f"对账失败：CJK 残留 {total_cjk}/{BASELINE_CJK}")
    sys.exit(1)
print(f"OK  en/json 对账通过：记录数一致 · CJK 残留 {total_cjk} ≤ 基线 {BASELINE_CJK} · 7 文件可解析")
