# scripts/_gen_search_index.py — W573 E-1：全站目录索引生成器（常驻留档，内容批次收尾重跑）
# 规则：docs/superpowers/plans/2026-09-09-service-experience-and-agent-ops-plans.md §E-1
# 口径：docs/**/*.md 剔除 /_dev/ /_templates/ /archive /superpowers/ 四类路径（771 篇口径）；
#       site/**/*.html 剔除 _template.html / _shell.html。
# 输出（W1223 执行批 E 起改形·用户批准）：索引载荷外置为本地 JS 数据件
#       site/data/search-index-zh.js 与 site/en/search-index-en.js（标记对随迁），
#       两搜索页改以同目录 <script src> 引用——单页 HTML 体积从 ~449/~426 KB 降至
#       ~113/~70 KB（容量 #1 治理）。file:// 铁律不破：经典脚本相对路径本地加载，
#       无 fetch、无外域；CSP script-src 'self' 放行（W1222 评估实测）。
#       消费方不变：常量名保持 SITE_SEARCH_INDEX_ZH/EN，页面 app 逻辑零改动。
import glob
import json
import os
import re
import warnings

try:
    with warnings.catch_warnings():
        # W809：jieba 依赖的 pkg_resources 已弃用（setuptools ≥81 警告）——静音以免污染
        # 门禁汇总行的机器解析（stderr 噪声不影响 stdout 标记，但读日志时误导判读）
        warnings.simplefilter("ignore", DeprecationWarning)
        warnings.simplefilter("ignore", UserWarning)
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
    # W661：02-06 板块站内化扩量——url 指向 reader/<sub>/<文件名>.html（页面不存在回退 blob）
    m_sub = re.match(r'docs/(0[2-6]-[^/]+)/(.+)\.md$', rel)
    if m_sub:
        sub = {'02-人物深度分析': 'people', '03-主题与情节专题': 'themes',
               '04-文化与历史背景': 'culture', '05-诗词歌赋': 'poetry',
               '06-个人随笔': 'essays'}.get(m_sub.group(1))
        if sub and os.path.exists(os.path.join(SITE, 'reader', sub, m_sub.group(2) + '.html')):
            return {'kind': 'reader', 'title': title, 'category': category,
                    'snippet': snippet, 'url': 'reader/%s/%s.html' % (sub, m_sub.group(2)), 'kw': kw}
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


def build_block(const_name, items):
    payload = json.dumps(items, ensure_ascii=False, separators=(',', ':'))
    return BEGIN + '\nconst ' + const_name + ' = ' + payload + ';\n' + END, payload


def build_indexes():
    """按当前 docs/ 与 site/ 实况算出两语索引（纯计算·不落盘）。

    W809：原实现把「算」与「写」都放在模块级（import 即写盘），导致「只算不写」的
    新鲜度门禁（check_search_index_fresh.py）无法安全复用本模块——本函数化是挂槽前置：
    门禁侧 import 本模块只调用 build_indexes() 取期望载荷；页面写盘只发生在 main()。
    返回：{'zh': (block_zh, payload_zh), 'en': (block_en, payload_en), 'counts': (docs, pages_zh, pages_en)}
    """
    doc_files = []
    for p in glob.glob(os.path.join(DOCS, '**', '*.md'), recursive=True):
        rel = p.replace(os.sep, '/')
        if not any(x in rel for x in EXCLUDE):
            doc_files.append(p)
    page_files = [p for p in glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True)
                  if os.path.basename(p) not in ('_template.html', '_shell.html')
                  and ('/reader/' not in p.replace(os.sep, '/') or p.replace(os.sep, '/').endswith('reader/themes-hub.html'))]  # W593：reader 页由 docs 条目承载避免双条目；W669 例外=themes-hub（无 docs 对应·导航页入索引）

    # W594：中英双索引分离——docs 全量两份共用；site 页面 zh 版收 zh 页、en 版收 en 页
    index_docs = [doc_entry(p) for p in sorted(doc_files)]
    page_rels = sorted(page_files)
    pages_zh = [page_entry(p) for p in page_rels if '/en/' not in p.replace(os.sep, '/')]
    pages_en = [page_entry(p) for p in page_rels if '/en/' in p.replace(os.sep, '/')]
    index_zh = index_docs + pages_zh
    index_en = index_docs + pages_en
    block_zh, payload_zh = build_block('SITE_SEARCH_INDEX_ZH', index_zh)
    block_en, payload_en = build_block('SITE_SEARCH_INDEX_EN', index_en)
    return {'zh': (block_zh, payload_zh), 'en': (block_en, payload_en),
            'counts': (len(doc_files), len(pages_zh), len(pages_en))}

def main():
    """把两语索引写进外部 JS 数据件并把搜索页改为 <script src> 引用（W1223·幂等）。

    页面外科幂等语义：
    - 首跑（页面仍含内联 BEGIN..END 段）：摘除内联段（保留宿主 script 内的 app 逻辑），
      并在宿主 <script> 开标签前插入外链 <script src="…"></script>（保证常量先于
      app 逻辑求值——renderOffline 等函数体直呼该常量）。
    - 重跑（页面已含外链引用）：只重写 JS 数据件，页面不再动。
    - 两态皆无（结构未知）：SystemExit 拒绝静默。
    """
    built = build_indexes()
    targets = [
        (os.path.join(SITE, 'data', 'search.html'), built['zh'][0], 'search-index-zh.js'),
        (os.path.join(SITE, 'en', 'search.html'), built['en'][0], 'search-index-en.js'),
    ]
    for t, block, js_rel in targets:
        # 1) 外部数据件：整写（幂等）——标记对随迁，第 46 槽判据域同步
        js_path = os.path.join(os.path.dirname(t), js_rel)
        with open(js_path, 'w', encoding='utf-8', newline='') as f:
            f.write(block + '\n')
        # 2) 页面外科（幂等）
        s = rd(t)
        src_tag = '<script src="%s"></script>' % js_rel
        if BEGIN in s and END in s:
            pos = s.find(BEGIN)
            pre = s[:pos]
            post = s[s.find(END) + len(END):]
            s = pre.rstrip('\n') + '\n' + post
            host = s.rfind('<script', 0, pos)
            if host == -1:
                raise SystemExit(f'FAIL 未找到宿主 script 开标签: {t}')
            s = s[:host] + src_tag + '\n' + s[host:]
        elif src_tag in s:
            pass  # 已迁移形态：页面无需再动
        else:
            raise SystemExit(f'FAIL 未找到内联索引段或外链引用锚点: {t}')
        with open(t, 'w', encoding='utf-8', newline='') as f:
            f.write(s)
    n_docs, n_zh, n_en = built['counts']
    print(f'docs={n_docs} pages_zh={n_zh} pages_en={n_en} '
          f'bytes zh={len(built["zh"][1].encode("utf-8"))} en={len(built["en"][1].encode("utf-8"))}')
    print('targets=2 external-js (search-index-zh.js / search-index-en.js)')


if __name__ == '__main__':
    main()
