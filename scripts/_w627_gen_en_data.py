#!/usr/bin/env python3
"""W627 i18n 根治层：生成 EN 数据副本 site/en/json/*.json（路线 B）。

原理：两 EN 页的 EMBEDDED 回退数据本身是全套英文（含长文本），按 W625 同款「机械配对」
纪律与 zh 部署 JSON 合并——EN 值优先（非 CJK 判定），缺失回退 zh 值并如实计数。
形状差异（phase_analysis 字典→数组、application_scenarios 字符串→对象）取 EMBEDDED 形状
（与页面渲染器期望一致，W621/W625 页内 shim 随之自然空转）。
schedule 类字典（zh 时辰键 × emb 拼音键）按键集不相交且等长时按插入序位置配对。

用法：
  node scripts/_w627_extract_embedded.js            # 先提取 EMBEDDED（Node 原生解析）
  python scripts/_w627_gen_en_data.py               # 生成 site/en/json/*.json + 对账报告
幂等：输出只依赖两源文件，重跑结果一致。
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"D:\xiyouji"
CJK = re.compile(r"[\u4e00-\u9fff]")
OUT_DIR = ROOT + r"\site\en\json"

# (逻辑名, zh 部署文件, EMBEDDED 来源页, EMBEDDED 键)
PAIRS = [
    ("villain_matrix", "villain_matrix.json", "methodology", "villain_matrix"),
    ("rescue_roi", "rescue_roi.json", "methodology", "rescue_roi"),
    ("methodology_summary", "methodology_summary.json", "methodology", "summary"),
    ("monster_clock", "monster_clock.json", "chart", "monster_clock"),
    ("chart_design_summary", "chart_design_summary.json", "chart", "summary"),
    ("domino_causality", "domino_causality.json", "chart", "domino_causality"),
    ("spiral_progress", "spiral_progress.json", "chart", "spiral_progress"),
]
# 记录数护栏：合并前后必须一致（防错位）
COUNT_GUARDS = {
    "villain_matrix": ("villain_positions", 15),
    "rescue_roi": ("rescue_cases", 10),
    "monster_clock": ("monster_schedules", 6),
}


def merge(zh, emb, path=""):
    """EN 优先合并：返回 (合并结果, en_count, zh_count)。"""
    if isinstance(emb, str):
        if not CJK.search(emb):
            return emb, 1, 0
        return (zh if isinstance(zh, str) else emb), 0, 1
    if isinstance(emb, list) and isinstance(zh, list):
        if len(emb) == len(zh):
            out, ec, zc = [], 0, 0
            for i, (z, e) in enumerate(zip(zh, emb, strict=True)):
                m, a, b = merge(z, e, f"{path}[{i}]")
                out.append(m)
                ec, zc = ec + a, zc + b
            return out, ec, zc
        return emb, 1, 0  # 长度不一致：取 EMBEDDED（EN 页渲染器期望的形状）
    if isinstance(emb, dict) and isinstance(zh, dict):
        common = set(zh) & set(emb)
        if not common and len(zh) == len(emb) and zh:
            # 键集不相交且等长（schedule 时辰×拼音）：按插入序位置配对
            out, ec, zc = {}, 0, 0
            for (zk, zv), (ek, ev) in zip(zh.items(), emb.items(), strict=True):
                m, a, b = merge(zv, ev, f"{path}.{zk}")
                out[ek] = m  # 键用 EMBEDDED 侧（EN 页按 EN 键查）
                ec, zc = ec + a, zc + b
            return out, ec, zc
        out, ec, zc = {}, 0, 0
        for k, zv in zh.items():
            if k in emb:
                m, a, b = merge(zv, emb[k], f"{path}.{k}")
                out[k] = m
                ec, zc = ec + a, zc + b
            else:
                out[k] = zv
                zc += 1
        for k, ev in emb.items():
            if k not in zh:
                out[k] = ev
                ec += 1
        return out, ec, zc
    # 类型不一致（dict↔list、str↔dict 等）：取 EMBEDDED 形状
    if emb is not None:
        return emb, 1, 0
    return zh, 0, 1


def count_cjk(o):
    n = 0
    if isinstance(o, dict):
        return sum(count_cjk(v) for v in o.values())
    if isinstance(o, list):
        return sum(count_cjk(v) for v in o)
    if isinstance(o, str) and CJK.search(o):
        return 1
    return n


def main():
    emb_all = json.load(open(ROOT + r"\scripts\output\_w627_embedded_en.json", encoding="utf-8"))
    import os
    os.makedirs(OUT_DIR, exist_ok=True)
    report = []
    for name, zh_file, page, emb_key in PAIRS:
        zh = json.load(open(ROOT + r"\site\data\json" + "\\" + zh_file, encoding="utf-8"))
        emb = emb_all[page].get(emb_key)
        assert emb is not None, f"EMBEDDED 缺 {page}.{emb_key}"
        merged, en_n, zh_n = merge(zh, emb, name)
        # 记录数护栏
        if name in COUNT_GUARDS:
            key, want = COUNT_GUARDS[name]
            got_zh = len(zh.get(key, []))
            got_en = len(merged.get(key, []))
            assert got_zh == got_en == want, f"{name}.{key}: {got_zh}/{got_en} != {want}"
        dst = OUT_DIR + "\\" + zh_file
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            json.dump(merged, f, ensure_ascii=False, indent=1)
        cjk = count_cjk(merged)
        report.append(f"{zh_file}: EN字段={en_n} zh回退={zh_n} CJK残留={cjk}")
    print("\n".join(report))
    total_cjk = sum(int(r.rsplit("=", 1)[1]) for r in report)
    print(f"[OK] 7 文件生成于 site/en/json/，CJK 残留合计 {total_cjk}（zh 独有子树如实回退）")


if __name__ == "__main__":
    main()
