import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERIC = "https://1273984347.github.io/xiyouji/static/img/og-cover-ink-zh.jpg"

plate_loose = re.compile(r'class="chapter-plate"')
scene_loose = re.compile(r'class="chapter-scene"')
og_re = re.compile(r'<meta property="og:image" content="([^"]+)"')

with_plate = []
with_scene = []
og_generic = []
og_other = []
for f in sorted(glob.glob(os.path.join(ROOT, "site", "reader", "ch*.html"))):
    s = open(f, encoding="utf-8", errors="ignore").read()
    ch = os.path.basename(f)[2:5]
    if plate_loose.search(s):
        with_plate.append(ch)
    if scene_loose.search(s):
        with_scene.append(ch)
    m = og_re.search(s)
    url = m.group(1) if m else None
    if url == GENERIC:
        og_generic.append(ch)
    else:
        og_other.append((ch, url.split("/")[-1] if url else None))

print("回目页总数:", len(glob.glob(os.path.join(ROOT, "site", "reader", "ch*.html"))))
print("含 chapter-plate 的回目页:", len(with_plate), with_plate)
print("含 chapter-scene 的回目页:", len(with_scene), with_scene)
print("og:image = 通用图:", len(og_generic))
print("og:image = 其它图:", len(og_other))
for ch, f in og_other:
    print("   ch%s -> %s" % (ch, f))
