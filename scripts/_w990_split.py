import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "output")
batch = json.load(open(os.path.join(OUT, "_w999_batch.json"), encoding="utf-8"))
reqs = batch["requests"]
assert len(reqs) == 12, len(reqs)
for i in range(3):
    part = {"requests": reqs[i * 4:(i + 1) * 4]}
    p = os.path.join(OUT, "_w999_batch_%s.json" % "abc"[i])
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(part, ensure_ascii=False, indent=1))
    print("写出", os.path.basename(p), "·", len(part["requests"]), "条 ·",
          [r["output_file"].split("/")[-1] for r in part["requests"]])
