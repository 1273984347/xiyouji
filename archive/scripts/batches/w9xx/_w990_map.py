import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "output")

# 母版命名：延续 plate-set 的 plate-line-NN-<slug> 体系（现有最大编号 48 ⇒ 本批 49–60）
MAP = [
    ("457317661257822", "plate-line-49-ch001-xianshi"),
    ("457316704305464", "plate-line-50-ch003-aoguang"),
    ("457317378953774", "plate-line-51-ch009-yuanshoucheng"),
    ("457317499667436", "plate-line-52-ch011-xiaoyu"),
    ("457318222532750", "plate-line-53-ch022-liushahe"),
    ("457318222532747", "plate-line-54-ch028-qunyao"),
    ("457318169379786", "plate-line-55-ch047-tongtianhe"),
    ("457317520142765", "plate-line-56-ch063-jiutou"),
    ("457317661257839", "plate-line-57-ch066-mile"),
    ("457318169379796", "plate-line-58-ch079-nanpo"),
    ("457317073265262", "plate-line-59-ch089-huangshi"),
    ("457318778908868", "plate-line-60-ch093-geigu"),
]
items = [{"node_id": n, "file": f + ".png"} for n, f in MAP]
p = os.path.join(OUT, "_w999_download_map.json")
with open(p, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(items, ensure_ascii=False, indent=1))
print("映射写出:", os.path.basename(p), "·", len(items), "项")
for it in items:
    print("  ", it["file"], "<-", it["node_id"])
