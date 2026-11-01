# -*- coding: utf-8 -*-
# W1071 批一次性施工脚本：N-01 搜索行链接化 + R-01 生产早退 + N-03 属性入标签 + N-06 计数 + 双入口明示
# 用法：python scripts/_w1071_search_docmap.py --apply   （缺省 dry-run 只打印 diff 统计）
import io, json, re, sys

APPLY = '--apply' in sys.argv
ROOT = 'site'

def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, t): io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

changes = []

# ---------- 1. N-01: 从 reader 总目录构建 title→href 映射并注入 search.html ----------
reader = rd(f'{ROOT}/reader/index.html')
seg = reader[reader.find('catalog-jump'):]
pairs = re.findall(r'<a href="(ch\d+\.html|(?:people|themes|culture|essays|poetry)/[^"]+)"[^>]*>((?:[^<]|<[^a])*)</a>', seg)
# 清洗标题（去内部标签残片）
clean = []
for href, txt in pairs:
    txt = re.sub(r'<[^>]+>', '', txt).strip()
    if txt:
        clean.append((href, txt))
dups = {}
site_doc_map = {}
for href, txt in clean:
    k = re.sub(r'\s+', '', txt)
    if k in site_doc_map and site_doc_map[k] != href:
        dups[k] = (site_doc_map[k], href)
        continue
    site_doc_map[k] = '../reader/' + href
print(f"map entries={len(site_doc_map)} dups={len(dups)}")
for k, v in list(dups.items())[:5]:
    print("  DUP:", k, v)

sh = rd(f'{ROOT}/data/search.html')
block = ("var SITE_DOC_MAP=" + json.dumps(site_doc_map, ensure_ascii=False, separators=(',', ':')) + ";\n"
         "var siteDocHref=function(t){if(!t)return null;var k=String(t).replace(/\\s+/g,'');var h=SITE_DOC_MAP[k];return h||null;};\n")
if 'var SITE_DOC_MAP=' in sh:
    sh = re.sub(r'var SITE_DOC_MAP=\{.*?\};\nvar siteDocHref=[^\n]*\n', lambda m: block, sh, flags=re.S)
    changes.append(('search.html', 'map replaced'))
else:
    anchor = 'function renderOffline(q){'
    assert sh.count(anchor) == 1
    sh = sh.replace(anchor, block + anchor)
    changes.append(('search.html', 'map inserted'))

old_drill = '      var hit=scored.filter(function(x){return (x.d.title||"—")===row.标题;})[0];\n      var u=hit?(hit.d.kind==="doc"?hit.d.url:"../"+hit.d.url):"";'
new_drill = ('      var hit=scored.filter(function(x){return (x.d.title||"—")===row.标题;})[0];\n'
             '      var sh2=hit?siteDocHref(hit.d.title):null;\n'
             '      var u=sh2?sh2:(hit?(hit.d.kind==="doc"?hit.d.url:"../"+hit.d.url):"");')
if sh.count(old_drill) == 1:
    sh = sh.replace(old_drill, new_drill)

old_tail = "  });\n}\n\nfunction renderOnline(q){"
new_tail = ("  });\n"
            "  var tb=rc.querySelector(\"table tbody\");\n"
            "  if(tb){Array.prototype.forEach.call(tb.rows,function(tr){var cell=tr.cells[1];if(!cell)return;var h=siteDocHref(cell.textContent);if(h){var a=document.createElement(\"a\");a.href=h;a.textContent=cell.textContent;cell.textContent=\"\";cell.appendChild(a);}});}\n"
            "}\n\nfunction renderOnline(q){")
if sh.count(old_tail) == 1:
    sh = sh.replace(old_tail, new_tail)
changes.append(('search.html', 'rows linked + drill override'))

# ---------- 2. R-01 A 案: rag-chat.js 生产环境早退 ----------
rc = rd(f'{ROOT}/static/js/rag-chat.js')
guard = ("(function () {\n  'use strict';\n\n"
         "  // W1071（A 案·用户 2026-10-31 裁决）：生产环境不注入——本组件依赖访客本机 RAG 服务，\n"
         "  // 仅 localhost / 127.0.0.1 / file:// 调试态出现；线上不再渲染浮钮/面板/健康检查。\n"
         "  var __host = location.hostname;\n"
         "  if (__host !== 'localhost' && __host !== '127.0.0.1' && __host !== '' && location.protocol !== 'file:') { return; }\n")
old_head = "(function () {\n  'use strict';\n"
assert rc.count(old_head) == 1
rc = rc.replace(old_head, guard)
wr(f'{ROOT}/static/js/rag-chat.js', rc)
changes.append(('rag-chat.js', 'prod early-return'))

# ---------- 3. N-03: 4 页属性移入开标签 ----------
tag_fixes = [
    (f'{ROOT}/guide.html',
     '<div class="paths-grid"> data-gsap="cards" data-gsap-target=".path-card"',
     '<div class="paths-grid" data-gsap="cards" data-gsap-target=".path-card">'),
    (f'{ROOT}/reader/index.html',
     '<main class="reader-wrap"> data-gsap="cards" data-gsap-target=".reader-idx a"',
     '<main class="reader-wrap" data-gsap="cards" data-gsap-target=".reader-idx a">'),
    (f'{ROOT}/reader/essays/index.html',
     '<main class="reader-wrap"> data-gsap="cards" data-gsap-target=".reader-idx a"',
     '<main class="reader-wrap" data-gsap="cards" data-gsap-target=".reader-idx a">'),
    (f'{ROOT}/reader/themes-hub.html',
     '<main class="reader-wrap"> data-gsap="cards" data-gsap-target=".reader-idx a"',
     '<main class="reader-wrap" data-gsap="cards" data-gsap-target=".reader-idx a">'),
]
for p, old, new in tag_fixes:
    t = rd(p)
    n = t.count(old)
    if n == 1:
        wr(p, t.replace(old, new))
        changes.append((p, 'data-gsap into tag'))
    else:
        assert new in t, f"{p}: neither old nor new form (count={n})"
        changes.append((p, 'data-gsap already fixed·skip'))

# ---------- 4. N-06: 首页计数对齐 stats（615→616 + 86→87，加对账标记） ----------
idx = rd(f'{ROOT}/index.html')
for old, new, tag in [
    ('<div class="stat"><div class="num">615</div><div class="lbl">篇 · 研究文档</div></div>',
     '<div class="stat"><div class="num">616<!--stats:a1_a6_docs--></div><div class="lbl">篇 · 研究文档</div></div>', 'stat616'),
    ('<p class="card-meta">55 KPI · 86 PAGES · SITE SEARCH</p>',
     '<p class="card-meta">55 KPI · 87<!--stats:visualization_pages--> PAGES · SITE SEARCH</p>', 'meta87'),
    ('<p class="ask-note">离线可搜（全站索引内置）· 想写「被忽略者」档案？试试 <a href="dukou-engine.html">西游·渡口写作引擎</a></p>',
     '<p class="ask-note">离线可搜（全站索引内置）· 查原著原文逐字请用 <a href="data/text-search.html">全文检索</a> · 想写「被忽略者」档案？试试 <a href="dukou-engine.html">西游·渡口写作引擎</a></p>', 'note'),
]:
    if old in idx:
        idx = idx.replace(old, new)
        changes.append(('index.html', tag + ' applied'))
    else:
        assert new in idx, f'index.html: neither form for {tag}'
        changes.append(('index.html', tag + ' already applied·skip'))
wr(f'{ROOT}/index.html', idx)

wr(f'{ROOT}/data/search.html', sh)

print("== changes ==")
for p, what in changes:
    print(f"  {p}: {what}")
if not APPLY:
    print("DRY-RUN：加 --apply 落盘")
else:
    print("APPLIED")
