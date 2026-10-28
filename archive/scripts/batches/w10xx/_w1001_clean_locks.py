import os
import re
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIT = os.path.join(REPO, ".git")

now = time.time()
removed = []
kept = []
for fn in sorted(os.listdir(GIT)):
    m = re.match(r"^(?:next-)?index-(\d+)\.lock$", fn)
    if not m:
        continue
    p = os.path.join(GIT, fn)
    age_min = (now - os.path.getmtime(p)) / 60.0
    pid = int(m.group(1))
    alive = False
    try:
        os.kill(pid, 0)
        alive = True
    except OSError:
        alive = False
    if alive:
        kept.append((fn, "进程存活"))
        continue
    if age_min < 3:
        kept.append((fn, "仅 %.0f 分钟·过新·留" % age_min))
        continue
    os.remove(p)
    removed.append((fn, "陈旧 %.0f 分钟·进程 %d 不存在" % (age_min, pid)))

print("已清理 %d 个陈旧锁：" % len(removed))
for fn, why in removed:
    print("   %-28s %s" % (fn, why))
if kept:
    print("保留 %d 个：" % len(kept))
    for fn, why in kept:
        print("   %-28s %s" % (fn, why))
