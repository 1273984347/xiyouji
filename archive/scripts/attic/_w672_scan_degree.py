# scan_degree.py —— relationship-3d 度数实算（WP-3.9 验收用，本批仅基线核对）  计划时点：id=2 悟空 12、id=1 唐僧 7
# 冻结版见 docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md 附录 A
import io, re, collections
src = io.open("site/data/character-relationship-3d.html", encoding="utf-8").read()
i = src.find("links:")
seg = src[i:i + 30000]
deg = collections.Counter()
for lm in re.finditer(r'source:\s*"?([\w·]+)"?[^}]*?target:\s*"?([\w·]+)"?', seg):
    deg[lm.group(1)] += 1; deg[lm.group(2)] += 1
print(deg.most_common(6))
