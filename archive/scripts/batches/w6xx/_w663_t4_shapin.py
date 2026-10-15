#!/usr/bin/env python3
"""W663/T4 一次性改写器：.github/workflows/*.yml 的 uses 全部改 SHA 钉（@SHA # tag 注释式）。

SHA 来源 = git ls-remote 实测（见 W663 T4 执行记录），禁凭记忆转录。
幂等守卫：检测到已是 SHA 钉（@<40hex>）即跳过该替换。
"""
import glob
import io
import re
import sys

PIN = {
    "actions/checkout@v7": ("3d3c42e5aac5ba805825da76410c181273ba90b1", "v7"),
    "actions/setup-python@v7": ("5fda3b95a4ea91299a34e894583c3862153e4b97", "v7"),
    "actions/upload-artifact@v7": ("043fb46d1a93c77aae656e7c1c64a875d1fc6a0a", "v7"),
    "actions/setup-node@v7": ("820762786026740c76f36085b0efc47a31fe5020", "v7"),
    "nick-fields/retry@v4": ("ad984534de44a9489a53aefd81eb77f87c70dc60", "v4"),
    "actions/cache@v6": ("55cc8345863c7cc4c66a329aec7e433d2d1c52a9", "v6"),
    "github/codeql-action/init@v3": ("1190a975f95ce23525efb6a3fc21ea29567c1b52", "v3"),
    "github/codeql-action/autobuild@v3": ("1190a975f95ce23525efb6a3fc21ea29567c1b52", "v3"),
    "github/codeql-action/analyze@v3": ("1190a975f95ce23525efb6a3fc21ea29567c1b52", "v3"),
    "actions/upload-pages-artifact@v5": ("fc324d3547104276b827a68afc52ff2a11cc49c9", "v5"),
    "actions/deploy-pages@v5": ("368f82528645a54fb793d4d04e342629a3f51346", "v5"),
    "actions/configure-pages@v6": ("45bfe0192ca1faeb007ade9deae92b16b8254a0d", "v6"),
}

total = 0
for path in sorted(glob.glob(".github/workflows/*.yml")):
    text = io.open(path, encoding="utf-8", newline="").read()
    n = 0
    for ref, (sha, tag) in PIN.items():
        old = "uses: " + ref
        new = "uses: %s@%s # %s" % (ref.rsplit("@", 1)[0], sha, tag)
        if new in text:
            continue  # 已钉
        cnt = text.count(old)
        if cnt:
            text = text.replace(old, new)
            n += cnt
    if n:
        io.open(path, "w", encoding="utf-8", newline="").write(text)
        print("%s: %d 处 SHA 钉" % (path, n))
        total += n

# 复核：任何 uses 不得再出现 tag 钉（@vN 形态且后面不是 # 注释）
bad = []
for path in sorted(glob.glob(".github/workflows/*.yml")):
    for i, ln in enumerate(io.open(path, encoding="utf-8"), 1):
        if "uses:" in ln and re.search(r"@\s*v?\d", ln) and not re.search(r"@[0-9a-f]{40}\s*#\s*v", ln):
            bad.append("%s:%d %s" % (path, i, ln.strip()))
if bad:
    print("FAIL 残留 tag 钉：")
    for b in bad:
        print("  " + b)
    sys.exit(1)
print("OK: 全仓 uses 共 %d 处改 SHA 钉，复核 0 残留" % total)
