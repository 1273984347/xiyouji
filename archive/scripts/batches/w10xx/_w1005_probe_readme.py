import glob
import os
import re

print("=== 1) 站点首页是否用 .hero（含 banner 图）===")
s = open("site/index.html", encoding="utf-8").read()
print("   site/index.html 含 class=\"hero\":", 'class="hero"' in s)
for m in re.finditer(r'<img[^>]+src="([^"]+)"', s):
    print("   img:", m.group(1))

print()
print("=== 2) 全仓含 flyer 的脚本/文档（渲染器）===")
for f in glob.glob("**/*", recursive=True):
    if not f.endswith((".py", ".js", ".md", ".html", ".json", ".ps1", ".bat")):
        continue
    if any(x in f for x in ("node_modules", "archive/", ".git/", "site/en/")):
        continue
    if "flyer" in os.path.basename(f).lower():
        print("   ", f)

print()
print("=== 3) assets/images/index-preview.png 的生成线索（仓库内提及）===")
for f in glob.glob("**/*.md", recursive=True):
    if any(x in f for x in ("node_modules", "archive/", ".git/")):
        continue
    t = open(f, encoding="utf-8", errors="ignore").read()
    if "index-preview" in t:
        for m in re.finditer(r"[^\n]*index-preview[^\n]*", t):
            print("   %-44s %s" % (f[:44], m.group(0).strip()[:130]))

print()
print("=== 4) 项目说明.md 版本行（门禁 C6：desc 含「·」）===")
t = open("docs/00-导读/项目说明.md", encoding="utf-8").read()
for i, ln in enumerate(t.split("\n")[:12]):
    if "当前批次" in ln or "当前版本" in ln:
        print("   %4d| %s" % (i + 1, ln[:260]))
