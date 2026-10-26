"""W949 · 字段图标位白名单**重建**（由扫描器实测产出 + 程序附理由）

口径纪律：白名单条目必须与扫描器输出**逐字节同形**（ZWJ 序列与 VS16 整体保留），
           故白名单不再手写字符，而是由扫描器实测 + 理由模板生成。
"""
import json
import pathlib
import sys

sys.path.insert(0, "scripts")
from check_icon_fields import scan_field_icons  # noqa: E402

REASON = {
    ("ai-dialogue.html", "avatar"): "名人头像位·「人物 + 身份」组合符（如 🧑‍🎓）表达人物专属身份·通用图标集无法替代·待设计专属头像族",
    ("narrative-experiment.html", "avatar"): "剧本角色头像位·角色专属象征（莲/叶/水晶/冠）·待设计专属图标族",
    ("narrative-experiment.html", "icon"): "指标卡图标位·指标专属象征（成功/收视/曝光/回报）·待设计专属图标族",
    ("methodology-matrix.html", "icon"): "情景卡图标位·情景专属象征（闪电/戒指/公文包/火箭）·待设计专属图标族",
    ("chart-design.html", "stage"): "螺旋阶段符号位·阶段专属象征（山/骷髅/耳/扇/莲）·待设计专属图标族",
    ("cross-time-danmaku.html", "flag"): "国籍标识位·国旗是复杂旗帜图案（线性图标集无法表达）·待裁决：改文字国名 or 自绘国旗族",
}
OWNER = "W950"

hits = scan_field_icons()
out = []
for h in hits:
    base = h["file"].split("/")[-1]
    key = (base, h["field"])
    reason = REASON.get(key) or REASON.get((base, h["field"])) or "待归类"
    if base == "cross-time-danmaku.json":
        reason = REASON[("cross-time-danmaku.html", "flag")] + "·数据源"
    out.append({"file": h["file"], "line": h["line"], "field": h["field"],
                "chars": h["chars"], "reason": reason, "owner": OWNER})

p = pathlib.Path("scripts/output/_w949_icon_field_allowlist.json")
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"白名单重建：{len(out)} 条 → {p}")
from collections import Counter  # noqa: E402
print("  按字段:", dict(Counter(o["field"] for o in out)))
print("  按文件:", dict(Counter(o["file"] for o in out)))
