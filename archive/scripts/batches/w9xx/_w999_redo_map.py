import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "output")
REDO = [
    ("457318788092473", "plate-line-53-ch022-liushahe"),
    ("457319596577242", "plate-line-49-ch001-xianshi"),
    ("457319115063794", "plate-line-50-ch003-aoguang"),
    ("457320235299810", "plate-line-51-ch009-yuanshoucheng"),
    ("457320115646560", "plate-line-59-ch089-huangshi"),
]
items = [{"node_id": n, "file": f + ".png"} for n, f in REDO]
p = os.path.join(OUT, "_w999_redo_map.json")
with open(p, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(items, ensure_ascii=False, indent=1))
print("重出映射写出:", os.path.basename(p), "·", len(items), "项")
