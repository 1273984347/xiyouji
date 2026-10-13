#!/usr/bin/env python3
"""W625 快赢层：从 EMBEDDED（英）×部署 JSON（中）机械配对生成 ZH2EN 映射表。

配对纪律：两源结构同构（同生成器产物·同序），按下标一一配对；任何长度/键失配即中止。
输出：可直接粘贴进 EN 页的 JS const 块（紧凑单行）。
"""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"D:\xiyouji"


def jload(p):
    return json.load(open(ROOT + p, encoding="utf-8"))


def js_obj(pairs, indent="    "):
    """按值排序输出 JS 对象字面量（键含中文·值含引号转义）。"""
    rows = ", ".join(f'{json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}' for k, v in pairs)
    return rows


# ---------- methodology-matrix ----------
vm = jload(r"\site\data\json\villain_matrix.json")
rr = jload(r"\site\data\json\rescue_roi.json")

page = open(ROOT + r"\site\en\methodology-matrix.html", encoding="utf-8").read()


def emb_array(src, key):
    """从页面截取「key: [ ... ]」数组字面量并宽松解析（裸键加引号/尾逗号容忍）。key 须含「: [」。"""
    i = src.index(key)
    depth = 0
    j = src.index("[", i)
    k = j
    while True:
        c = src[k]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                break
        k += 1
    txt = src[j:k + 1]
    txt = re.sub(r"(\w+)\s*:", r'"\1":', txt)          # 裸键加引号
    txt = re.sub(r",(\s*[}\]])", r"\1", txt)            # 尾逗号
    return json.loads(txt)


emb_vm_pos = emb_array(page, "villain_positions: [")
emb_rr_cases = emb_array(page, "rescue_cases: [")

assert len(emb_vm_pos) == len(vm["villain_positions"]) == 15, "villain_positions 长度失配"
assert len(emb_rr_cases) == len(rr["rescue_cases"]) == 10, "rescue_cases 长度失配"

M_MONSTER = sorted({(z["monster"], e["monster"]) for z, e in zip(vm["villain_positions"], emb_vm_pos, strict=True)})
R_MONSTER = sorted({(z["monster"], e["monster"]) for z, e in zip(rr["rescue_cases"], emb_rr_cases, strict=True)})
RESCUER = sorted({(z["rescuer"], e["rescuer"]) for z, e in zip(rr["rescue_cases"], emb_rr_cases, strict=True)})
PHASE = sorted({(z["rescue_phase"], e["rescue_phase"]) for z, e in zip(rr["rescue_cases"], emb_rr_cases, strict=True)})
QUAD = sorted({(z["quadrant"], e["quadrant"]) for z, e in zip(vm["villain_positions"], emb_vm_pos, strict=True)})
assert len(QUAD) == 4 and len(PHASE) == 3, "象限/阶段枚举数异常"

print("// ===== en/methodology-matrix =====")
print("const MONSTER_EN = { " + js_obj(M_MONSTER) + " };")
print("const RMONSTER_EN = { " + js_obj(R_MONSTER) + " };")
print("const RESCUER_EN = { " + js_obj(RESCUER) + " };")
print("const PHASE_EN = { " + js_obj(PHASE) + " };")
print("const QUADRANT_ID = { " + js_obj(QUAD) + " };")

# ---------- chart-design ----------
mc = jload(r"\site\data\json\monster_clock.json")
cd = open(ROOT + r"\site\en\chart-design.html", encoding="utf-8").read()
emb_sched = emb_array(cd, "monster_schedules: [")
emb_hours = emb_array(cd, "twelve_hours: [")
assert len(emb_sched) == len(mc["monster_schedules"]) == 6
assert len(emb_hours) == len(mc["twelve_hours"]) == 12

HOUR = sorted({(z["hour"], e["hour"]) for z, e in zip(mc["twelve_hours"], emb_hours, strict=True)})
ACTG = sorted({(z["activity_general"], e["activity_general"]) for z, e in zip(mc["twelve_hours"], emb_hours, strict=True)})
MON = sorted({(z["monster"], e["monster"]) for z, e in zip(mc["monster_schedules"], emb_sched, strict=True)})
CAT = sorted({(z["category"], e["category"]) for z, e in zip(mc["monster_schedules"], emb_sched, strict=True)})
BG = sorted({(z["background"], e["background"]) for z, e in zip(mc["monster_schedules"], emb_sched, strict=True)})
RES = sorted({(z["resource"], e["resource"]) for z, e in zip(mc["monster_schedules"], emb_sched, strict=True)})

sched_pairs = {}
sched_keys = {}
for z, e in zip(mc["monster_schedules"], emb_sched, strict=True):
    assert len(z["schedule"]) == len(e["schedule"]) == 12, f"{z['monster']} schedule 长度失配"
    for (zk, zv), (ek, ev) in zip(z["schedule"].items(), e["schedule"].items(), strict=True):
        sched_keys[zk] = ek
        sched_pairs[(zk, zv)] = ev
SCHED_KEY = sorted(sched_keys.items())
SCHED_ACT = sorted(sched_pairs.items())

print("\n// ===== en/chart-design =====")
print("const HOUR_EN = { " + js_obj(HOUR) + " };")
print("const ACTGEN_EN = { " + js_obj(ACTG) + " };")
print("const MSTATE_EN = { " + js_obj(MON + CAT + BG + RES) + " };")
print("const SKEY_EN = { " + js_obj(SCHED_KEY) + " };")
print("const SACT_EN = { " + js_obj([(k[0] + "|" + k[1], v) for k, v in SCHED_ACT]) + " };")

# 消歧校验：同键不同值 = 0（否则 map 会错译）——villain/rescue 两表英译并存·各用各表不合并
for name, pairs in [("MONSTER", M_MONSTER), ("RMONSTER", R_MONSTER), ("RESCUER", RESCUER), ("PHASE", PHASE),
                    ("QUAD", QUAD), ("HOUR", HOUR), ("ACTGEN", ACTG), ("MSTATE", MON + CAT + BG + RES),
                    ("SKEY", SCHED_KEY), ("SACT", [(k[0] + "|" + k[1], v) for k, v in SCHED_ACT])]:
    keys = [k for k, _ in pairs]
    assert len(keys) == len(set(keys)), f"{name} 键冲突"
print("\n[OK] 全部映射无键冲突；SACT 共 %d 条" % len(SCHED_ACT))

# 片段落盘（供粘贴与复查）
buf = io.StringIO()
print("// ===== en/methodology-matrix（W625 快赢层·由 _w625_build_zh2en_maps.py 生成·勿手改） =====", file=buf)
print("const MONSTER_EN = { " + js_obj(M_MONSTER) + " };", file=buf)
print("const RMONSTER_EN = { " + js_obj(R_MONSTER) + " };", file=buf)
print("const RESCUER_EN = { " + js_obj(RESCUER) + " };", file=buf)
print("const PHASE_EN = { " + js_obj(PHASE) + " };", file=buf)
print("const QUADRANT_ID = { " + js_obj(QUAD) + " };", file=buf)
print("", file=buf)
print("// ===== en/chart-design（同上·SACT 键=「时辰|活动」复合） =====", file=buf)
print("const HOUR_EN = { " + js_obj(HOUR) + " };", file=buf)
print("const ACTGEN_EN = { " + js_obj(ACTG) + " };", file=buf)
print("const MSTATE_EN = { " + js_obj(MON + CAT + BG + RES) + " };", file=buf)
print("const SKEY_EN = { " + js_obj(SCHED_KEY) + " };", file=buf)
print("const SACT_EN = { " + js_obj([(k[0] + "|" + k[1], v) for k, v in SCHED_ACT]) + " };", file=buf)
open(ROOT + r"\scripts\_w625_maps_snippet.js", "w", encoding="utf-8", newline="\n").write(buf.getvalue())
print("snippet -> scripts/_w625_maps_snippet.js")
