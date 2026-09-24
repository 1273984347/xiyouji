# scripts/_gen_search_index.py — W573 E-1：全站目录索引生成器（常驻留档，内容批次收尾重跑）
# 规则：docs/superpowers/plans/2026-09-09-service-experience-and-agent-ops-plans.md §E-1
# 口径：docs/**/*.md 剔除 /_dev/ /_templates/ /archive /superpowers/ 四类路径（771 篇口径）；
#       site/**/*.html 剔除 _template.html / _shell.html。
# 输出：以幂等标记对 /* SEARCH_INDEX:BEGIN */ … /* SEARCH_INDEX:END */ 内嵌进
#       site/data/search.html 与 site/en/search.html（重复运行先删旧段再插新段）。
# file:// 铁律：索引为内嵌常量，无 fetch。
import glob
import json
import os
import re

try:
    import jieba
    jieba.setLogLevel(60)
except ImportError:  # W594：jieba 缺失时 kw 中文退化为逐字，不失败
    jieba = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
DOCS = os.path.join(ROOT, 'docs')
BLOB = 'https://github.com/1273984347/xiyouji/blob/main/'
EXCLUDE = ('/_dev/', '/_templates/', '/archive', '/superpowers/',
            'S2-学术投稿', 'S2-外部分享', 'S3-方法论外部分享', 'S4-学术投稿')  # W620：四目录移出公开仓库，不入搜索索引
BEGIN = '/* SEARCH_INDEX:BEGIN */'
END = '/* SEARCH_INDEX:END */'


def rd(p):
    with open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


def make_kw(title):
    """W594：标题关键词数组（中文 jieba 切词、英文按词干拆分），供前端 +4 加权，≤12 个。"""
    t = (title or '').strip()
    if not t:
        return []
    if re.search(r'[\u4e00-\u9fa5]', t):
        if jieba is not None:
            words = [w for w in jieba.cut(t)]
        else:
            words = list(t)  # jieba 缺失时退化为逐字（降级不失败）
    else:
        words = re.split(r'[^a-zA-Z0-9]+', t.lower())
    out = []
    for w in words:
        w = w.strip().lower()
        if len(w) >= 2 and w not in out:
            out.append(w)
        if len(out) >= 12:
            break
    return out


def doc_entry(p):
    rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
    s = rd(p)
    lines = s.splitlines()
    title = ''
    for ln in lines:
        if ln.startswith('# '):
            title = ln[2:].strip()
            break
    if not title:
        title = os.path.splitext(os.path.basename(p))[0]
    snippet = ''
    for ln in lines:
        t = ln.strip()
        if not t or t.startswith('#') or t.startswith('```'):
            continue
        clean = re.sub(r'[#*`>\[\]]', '', t)
        clean = re.sub(r'\s+', ' ', clean).strip()
        # 路径清单行不作摘要候选（剔除路径 token 后剩字过短，如「适用页面：site/data/x.html」）
        stripped_paths = re.sub(r'\S*\.(?:html|md|json|py)\S*', '', clean)
        if len(clean) >= 12 and len(stripped_paths) >= 8:  # 跳过过短的残行（分隔线/孤词/纯路径）
            snippet = clean[:100]
            break
    category = rel.split('/')[1] if '/' in rel else ''
    # W594：标题关键词数组（前端 +4 加权）
    kw = make_kw(title)
    # W593：A1 逐回 100 篇站内化——url 指向 reader（kind=reader，打开时同 page 加 ../ 前缀）
    m_ch = re.match(r'docs/01-全书逐回解读/第(\d{3})回-', rel)
    if m_ch:
        return {'kind': 'reader', 'title': title, 'category': category,
                'snippet': snippet, 'url': 'reader/ch%03d.html' % int(m_ch.group(1)), 'kw': kw}
    return {'kind': 'doc', 'title': title, 'category': category,
            'snippet': snippet, 'url': BLOB + rel, 'kw': kw}


def page_entry(p):
    rel_site = os.path.relpath(p, SITE).replace(os.sep, '/')  # 站点根相对（url 与 category 均基于 site/）
    s = rd(p)
    m = re.search(r'<title>([^<]*)</title>', s)
    title = m.group(1).strip() if m else os.path.basename(p)
    md = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', s)
    snippet = md.group(1).strip() if md else ''
    parts = rel_site.split('/')
    category = '' if len(parts) == 1 else parts[0]
    return {'kind': 'page', 'title': title, 'category': category,
            'snippet': snippet, 'url': rel_site, 'kw': make_kw(title)}


doc_files = [p for p in glob.glob(os.path.join(DOCS, '**', '*.md'), recursive=True)
             if not any(x in p.replace(os.sep, '/') for x in EXCLUDE)]
page_files = [p for p in glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True)
              if os.path.basename(p) not in ('_template.html', '_shell.html')
              and '/reader/' not in p.replace(os.sep, '/')]  # W593：reader 页由 docs/01 的 kind=reader 条目承载，避免双条目

# W594：中英双索引分离——docs 全量两份共用；site 页面 zh 版收 zh 页、en 版收 en 页
index_docs = [doc_entry(p) for p in sorted(doc_files)]
page_rels = sorted(page_files)
pages_zh = [page_entry(p) for p in page_rels if '/en/' not in p.replace(os.sep, '/')]
pages_en = [page_entry(p) for p in page_rels if '/en/' in p.replace(os.sep, '/')]
index_zh = index_docs + pages_zh
index_en = index_docs + pages_en


def build_block(const_name, items):
    payload = json.dumps(items, ensure_ascii=False, separators=(',', ':'))
    return BEGIN + '\nconst ' + const_name + ' = ' + payload + ';\n' + END, payload


block_zh, payload_zh = build_block('SITE_SEARCH_INDEX_ZH', index_zh)
block_en, payload_en = build_block('SITE_SEARCH_INDEX_EN', index_en)

targets = [
    (os.path.join(SITE, 'data', 'search.html'), block_zh),
    (os.path.join(SITE, 'en', 'search.html'), block_en),
]
for t, block in targets:
    s = rd(t)
    if BEGIN in s and END in s:
        pre = s[:s.find(BEGIN)]
        post = s[s.find(END) + len(END):]
        s = pre + block + post
    else:
        anchor = s.find('window.SEARCH_INDEX = [')
        if anchor == -1:
            raise SystemExit(f'FAIL 未找到注入锚点: {t}')
        line_start = s.rfind('\n', 0, anchor) + 1
        s = s[:line_start] + block + '\n' + s[line_start:]
    with open(t, 'w', encoding='utf-8', newline='') as f:
        f.write(s)

print(f'docs={len(doc_files)} pages_zh={len(pages_zh)} pages_en={len(pages_en)} '
      f'bytes zh={len(payload_zh.encode("utf-8"))} en={len(payload_en.encode("utf-8"))}')
print('targets=2 embedded')
