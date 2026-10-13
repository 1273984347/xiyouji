# scripts/_fix_site_links.py — W572 D-1：越界锚链接改写为 GitHub blob/tree（方案 D-1）
# 规则：docs/superpowers/plans/2026-09-09-service-experience-and-agent-ops-plans.md §D-1
# 只改 <a href> 解析后落在 site/（部署根）之外的锚链接；repo 内不存在的不改（输出手工清单）。
# 附带：journey-spacetime.html 的 A1_DOC_MAP 消费点前缀字面量（:1551，两处）改为 GitHub blob 前缀。
# 幂等：改写后 href 以 https:// 开头，重跑自动跳过。
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
REPO = 'https://github.com/1273984347/xiyouji'
BLOB = REPO + '/blob/main/'
TREE = REPO + '/tree/main/'

SKIP = ('http://', 'https://', '//', 'mailto:', 'javascript:', 'data:', '#', 'tel:')
import re  # noqa: E402

HREF_RE = re.compile(r'<a\b[^>]*?href=("([^"]*)"|\'([^\']*)\')', re.I)


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, '/')


changed = []  # (file, old, new)
manual = []   # (file, href, repo_rel)

pages = sorted(glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True))
for p in pages:
    with open(p, encoding='utf-8', newline='') as f:
        s = f.read()
    out = []
    for m in HREF_RE.finditer(s):
        raw = m.group(2) if m.group(2) is not None else m.group(3)
        if raw is None:
            continue
        h = raw.strip()
        if not h or h.startswith(SKIP):
            continue
        hp = h.split('#')[0].split('?')[0]
        if not hp:
            continue
        tgt = os.path.normpath(os.path.join(os.path.dirname(p), hp))
        if tgt == SITE or tgt.startswith(SITE + os.sep):
            continue
        repo_rel = os.path.relpath(tgt, ROOT).replace(os.sep, '/')
        fs = os.path.join(ROOT, repo_rel)
        suffix = h[len(hp):]
        if os.path.isdir(fs):
            new = TREE + repo_rel + suffix
        elif os.path.isfile(fs):
            new = BLOB + repo_rel + suffix
        else:
            manual.append((rel(p), h, repo_rel))
            continue
        out.append((m.start(1), m.end(1), s[m.start(1)] + new + s[m.end(1) - 1], h, new))
    if out:
        buf = []
        pos = 0
        for start, end, lit, h, new in out:
            buf.append(s[pos:start])
            buf.append(lit)
            pos = end
            changed.append((rel(p), h, new))
        buf.append(s[pos:])
        s = ''.join(buf)
        with open(p, 'w', encoding='utf-8', newline='') as f:
            f.write(s)

# A1_DOC_MAP 消费点前缀（journey-spacetime.html:1551 附近，字面量出现 2 次）
jsp = os.path.join(SITE, 'data', 'journey-spacetime.html')
OLD_PREFIX = '"../../docs/01-全书逐回解读/"'
NEW_PREFIX = '"' + BLOB + 'docs/01-全书逐回解读/"'
with open(jsp, encoding='utf-8', newline='') as f:
    js = f.read()
n_prefix = js.count(OLD_PREFIX)
if n_prefix:
    js = js.replace(OLD_PREFIX, NEW_PREFIX)
    with open(jsp, 'w', encoding='utf-8', newline='') as f:
        f.write(js)

print(f'rewritten_anchors={len(changed)} files={len(set(c[0] for c in changed))}')
print(f'a1_doc_map_prefix_replaced={n_prefix} (expect 2)')
print(f'manual_list={len(manual)}')
for item in manual:
    print('MANUAL:', item)
print('SAMPLES:')
for c in changed[:5]:
    print(' ', c)
