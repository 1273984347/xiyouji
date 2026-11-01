# -*- coding: utf-8 -*-
# W1074 批施工脚本：序列第 2 批（动线与可达）+ 第 3 批（生产净面）合并实施
# 幂等设计：每处先查旧形态，命中才改；已应用则断言新形态在位
import io, glob, re, sys

APPLY = '--apply' in sys.argv
CHANGES = []

def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, t):
    if APPLY: io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

def patch(path, pairs):
    t = rd(path)
    for old, new, tag in pairs:
        n = t.count(old)
        if n >= 1:
            t = t.replace(old, new)
            CHANGES.append((path, tag, n))
        else:
            assert new in t, f"{path}: neither old nor new for [{tag}]"
            CHANGES.append((path, tag + ' ·已应用跳过', 0))
    wr(path, t)

# ============ 1. site/index.html（N-08 / N-07 / N-09 / R-07） ============
patch('site/index.html', [
    ('.masthead-copy { max-width: 620px; }',
     '/* W1074（N-08 根修）：min-width:0 —— .masthead 为 flex 容器，本元素作为 flex 项默认\n'
     '   min-width:auto，其内 .masthead-facts 的 .mega-row（flex-shrink:0）把 min-content 撑到\n'
     '   359.28px，超出父内容宽 327px（375−24×2）⇒ 375 视口横向溢出 8px。允许收缩后由\n'
     '   .masthead-facts 的 flex-wrap 承接窄屏换行。 */\n'
     '        .masthead-copy { max-width: 620px; min-width: 0; }', 'N-08 copy min-width'),
    ('.masthead-facts {\n            display: flex; align-items: flex-start; gap: 18px;',
     '.masthead-facts {\n            display: flex; flex-wrap: wrap; align-items: flex-start; gap: 18px;', 'N-08 facts wrap'),
    ('role="button" role="listitem"', 'role="button"', 'R-07 双 role'),
    ('<a href="en/index.html" hreflang="en" style="display:inline-block;padding:6px var(--space-2)">English</a>\n            ', '', 'N-09 EN 去重'),
    ('N · NARRATOLOGY 13D', 'N · NARRATOLOGY 16D', 'N-07 kicker'),
    ('<h3>叙事学十三维</h3>', '<h3>叙事学十六维</h3>', 'N-07 h3'),
    ('<p>全书叙事机制的十三维网络。</p>', '<p>全书叙事机制的十六维网络。</p>', 'N-07 desc'),
])

# ============ 2. 100 个章回页：返回导读出站改站内（N-04） ============
n04 = 0
for f in sorted(glob.glob('site/reader/ch0*.html') + glob.glob('site/reader/ch1*.html')):
    t = rd(f)
    old = 'https://github.com/1273984347/xiyouji/blob/main/docs/00-导读/阅读指南.md">返回导读<'
    new = '../guide.html">返回导读<'
    n = t.count(old)
    if n == 1:
        wr(f, t.replace(old, new)); n04 += 1
    else:
        assert new in t, f"{f}: 返回导读 neither form"
CHANGES.append(('site/reader/ch*.html ×100', 'N-04 返回导读站内化', n04))

# ============ 3. site/reader/index.html（N-05 套壳 + R-03 hub 入口） ============
t = rd('site/reader/index.html')
if 'site-header' not in t:
    header_css = ("\n/* W1074（N-05）：目录页补站内壳（页头/页脚/h1）——此前 622 链接零出口 */\n"
        ".site-header{display:flex;align-items:center;justify-content:space-between;gap:16px;"
        "padding:14px 24px;border-bottom:1px solid var(--line);background:var(--paper);}"
        ".site-header .brand{font-family:var(--font-serif);font-weight:700;color:var(--ink);text-decoration:none;}"
        ".site-header nav{display:flex;gap:18px;flex-wrap:wrap;}"
        ".site-header nav a{color:var(--ink-soft);text-decoration:none;font-size:14px;}"
        ".site-header nav a:hover{color:var(--accent);}"
        ".catalog-title{font-family:var(--font-serif);font-size:30px;margin:0 0 6px;color:var(--ink);}"
        ".hub-links{margin:10px 0 0;font-size:13px;color:var(--ink-soft);}"
        ".hub-links a{color:var(--accent-2);text-decoration:none;}"
        ".site-footer{margin-top:48px;padding:20px 24px;border-top:1px solid var(--line);color:var(--ink-faint);font-size:13px;}"
        ".site-footer a{color:var(--accent-2);text-decoration:none;}\n")
    m = re.search(r'(<style>)', t)
    assert m, 'reader/index style tag not found'
    t = t[:m.end()] + header_css + t[m.end():]
    header_html = (
        '<a class="skip-link" href="#main">跳到主要内容</a>\n'
        '<header class="site-header" role="banner">\n'
        '  <a class="brand" href="../index.html">取经录 · 详解西游记</a>\n'
        '  <nav aria-label="主导航">\n'
        '    <a href="../index.html">首页</a>\n'
        '    <a href="../guide.html">导读</a>\n'
        '    <a href="../dashboard.html">数据看板</a>\n'
        '    <a href="../data/text-search.html">全文检索</a>\n'
        '    <a href="../en/">EN</a>\n'
        '  </nav>\n'
        '</header>\n')
    mb = re.search(r'(<body[^>]*>)', t)
    assert mb, 'reader/index body tag not found'
    t = t[:mb.end()] + '\n' + header_html + t[mb.end():]
    mo = re.search(r'<main class="reader-wrap"([^>]*)>', t)
    assert mo, 'reader main tag not found'
    t = t[:mo.start()] + '<main class="reader-wrap" id="main"' + mo.group(1) + '>' + t[mo.end():]
    t = t.replace('<main class="reader-wrap" id="main" data-gsap="cards" data-gsap-target=".reader-idx a">',
                  '<main class="reader-wrap" id="main" data-gsap="cards" data-gsap-target=".reader-idx a">\n'
                  '<h1 class="catalog-title">站内阅读 · 全目录</h1>', 1)
    hub_row = ('<p class="hub-links">按分类浏览全部： '
               '<a href="people/index.html">人物深度 hub</a> · '
               '<a href="themes-hub.html">主题专题 hub</a> · '
               '<a href="culture/index.html">文化背景 hub</a></p>')
    anchor = '</nav>'
    i = t.find(anchor)
    assert i != -1
    t = t[:i + len(anchor)] + '\n' + hub_row + t[i + len(anchor):]
    fb = t.rfind('</body>')
    assert fb != -1
    footer = ('<footer class="site-footer"><a href="../index.html">首页</a> · '
              '<a href="../dashboard.html">数据看板</a> · '
              '<a href="../guide.html">导读</a> · 取经录 · 详解西游记</footer>\n')
    t = t[:fb] + footer + t[fb:]
    CHANGES.append(('site/reader/index.html', 'N-05 壳+R-03 hub 行', 1))
else:
    CHANGES.append(('site/reader/index.html', 'N-05 已应用跳过', 0))
wr('site/reader/index.html', t)

# ============ 4. site/reader/themes/index.html → 指向 hub 的跳转页（R-04） ============
stub = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<meta name="robots" content="noindex,follow">\n'
        '<title>主题专题 · 目录（已并入导航 hub）</title>\n'
        '<meta http-equiv="refresh" content="0; url=../themes-hub.html">\n'
        '<style>body{font-family:serif;background:#FAF7F0;color:#23201A;display:flex;min-height:100vh;'
        'align-items:center;justify-content:center;margin:0}a{color:#C8463A}</style>\n</head>\n<body>\n'
        '<main><p>主题专题目录已并入 <a href="themes-hub.html">主题专题导航 hub</a>（正在跳转…）。</p></main>\n</body>\n</html>\n')
old_themes = rd('site/reader/themes/index.html')
if 'W1074' not in old_themes:
    wr('site/reader/themes/index.html', stub)
    CHANGES.append(('site/reader/themes/index.html', 'R-04 归一跳转', 1))
else:
    CHANGES.append(('site/reader/themes/index.html', 'R-04 已应用跳过', 0))

# ============ 5. site/data/search.html（N-02 移除 /datasets 在线分支 + 文案） ============
patch('site/data/search.html', [
    ('function probe(){\n  apiFetch("/datasets").then(function(list){\n    API_OK=true;\n    setBanner("已连接数据 API · 共 "+list.length+" 个数据集 · 输入关键词跨集检索。",false);\n  }).catch(function(){\n    API_OK=false;\n    setBanner("当前为离线目录检索：覆盖全部研究文档与站点页面（标题 / 分类 / 摘要匹配，取前 50 条）。",true);\n  });\n}',
     'function probe(){\n  /* W1074（N-02 根修）：/datasets 数据 API 在纯静态部署与 /xiyouji/ 子路径下不存在，\n     原 probe 每次加载必发一个注定 404 的请求——在线分支移除，恒走离线目录检索。 */\n  API_OK=false;\n  setBanner("当前为离线目录检索：覆盖全部研究文档与站点页面（标题 / 分类 / 摘要匹配，取前 50 条）。",true);\n}', 'N-02 probe 移除'),
    ('<p>W338 数据 API 接入 · 在线跨 42 数据集递归检索（/search）· 离线 file:// 降级到内置数据集索引</p>',
     '<p>全站目录检索 · 一站查研究文档与站内页面（离线可用）</p>', 'N-02 横幅文案'),
    ('<span class="hint">在线命中「数据集 + 片段」；离线仅按数据集名称/标题过滤。</span>', '', 'N-02 hint 移除'),
])

# ============ 6. site/dashboard.html（N-02 移除 /datasets + drill 文案） ============
patch('site/dashboard.html', [
    ('if(!window.DATAHUB_INDEX){return;}\n              fetch("/datasets",{cache:"no-store"}).then(function(r){if(!r.ok)throw 0;return r.json();})\n                .then(function(list){render(list);})\n                .catch(function(){ render(window.DATAHUB_INDEX); });',
     'if(!window.DATAHUB_INDEX){return;}\n              /* W1074（N-02 根修）：/datasets 在纯静态部署不存在（原每次加载必 404）——直接用内置索引。 */\n              render(window.DATAHUB_INDEX);', 'N-02 fetch 移除'),
    ('启动数据 API 后访问 <code>/dataset/"+r.数据集+"</code> 查看完整 JSON。',
     '完整 JSON 可在站内 <code>data/json/</code> 目录获取。', 'N-02 drill 文案'),
])

# ============ 7. site/404.html（R-08 补返回上一页） ============
t = rd('site/404.html')
if 'backBtn' not in t:
    m = re.search(r'(<a href="data/text-search\.html"[^>]*>[^<]*</a>)', t)
    assert m, '404 exits anchor not found'
    t = t[:m.end()] + '\n  <button id="backBtn" type="button" style="margin-left:12px;background:none;border:1px solid #23201A;color:#23201A;padding:6px 14px;border-radius:4px;cursor:pointer;font:inherit">返回上一页</button>' + t[m.end():]
    sb = t.rfind('</body>')
    t = t[:sb] + '<script>document.getElementById("backBtn").addEventListener("click",function(){history.back();});</script>\n' + t[sb:]
    t = t.replace('零 JS、零外域、零图片；入口四链接（首页/数据看板/标签云/全文检索）。',
                  '零外域、零图片；入口四链接（首页/数据看板/标签云/全文检索）+ 返回上一页（W1074 R-08·单段内联脚本随 CSP 哈希管理）。')
    wr('site/404.html', t)
    CHANGES.append(('site/404.html', 'R-08 返回上一页', 1))
else:
    CHANGES.append(('site/404.html', 'R-08 已应用跳过', 0))

# ============ 8. R-11 五控件 aria-label（中英存在性实测） ============
patch('site/data/graph-explorer.html', [
    ('<select id="graphSel"></select>', '<select id="graphSel" aria-label="选择图谱"></select>', 'R-11 graphSel'),
    ('<input type="text" id="search" placeholder="节点名（如 悟空 / 阿赖耶识）">',
     '<input type="text" id="search" aria-label="搜索节点" placeholder="节点名（如 悟空 / 阿赖耶识）">', 'R-11 search'),
])
patch('site/data/cross-time-danmaku.html', [
    ('<textarea id="user-message" placeholder="留下你的弹幕·成为批评史的一部分..."></textarea>',
     '<textarea id="user-message" aria-label="弹幕内容" placeholder="留下你的弹幕·成为批评史的一部分..."></textarea>', 'R-11 danmaku'),
])
patch('site/data/journey-map-interactive.html', [
    ('<input type="range" min="0" max="16" value="0" class="timeline-slider" id="routeSlider" style="width:50%; min-width:260px;">',
     '<input type="range" min="0" max="16" value="0" class="timeline-slider" id="routeSlider" aria-label="取经路线进度" style="width:50%; min-width:260px;">', 'R-11 routeSlider'),
])
patch('site/data/narrative-rhythm-curve.html', [
    ('<input type="range" min="1" max="100" value="1" class="timeline-slider" id="chapterSlider">',
     '<input type="range" min="1" max="100" value="1" class="timeline-slider" id="chapterSlider" aria-label="章节选择">', 'R-11 chapterSlider'),
])
en_hits = 0
for f in glob.glob('site/en/data/*.html'):
    t = rd(f)
    pairs = []
    if 'id="graphSel"' in t and 'aria-label' not in t[t.find('id="graphSel"')-40:t.find('id="graphSel"')+40]:
        pairs.append(('<select id="graphSel"></select>', '<select id="graphSel" aria-label="Select graph"></select>'))
    if 'id="search"' in t:
        i = t.find('id="search"')
        seg = t[max(0,i-60):i+120]
        if 'aria-label' not in seg:
            pairs.append(('<input type="text" id="search"', '<input type="text" id="search" aria-label="Search nodes"'))
    if 'id="user-message"' in t and t.count('id="user-message"') == 1:
        i = t.find('id="user-message"')
        if 'aria-label' not in t[max(0,i-40):i+60]:
            pairs.append(('<textarea id="user-message"', '<textarea id="user-message" aria-label="Message"'))
    if pairs:
        for old, new in pairs:
            if old in t:
                t = t.replace(old, new); en_hits += 1
        wr(f, t)
CHANGES.append(('site/en/data/*.html', 'R-11 EN 控件', en_hits))

# ============ 9. N-03 遗留核验 + story/customs 孤儿页入口（R-03 vis 页） ============
csg = rd('site/data/chapter-structure-graph.html')
add_links = ''
if 'story-timeline' not in csg:
    add_links += ' · <a href="story-timeline.html">叙事时间线</a>'
if 'customs-pass-route' not in csg:
    add_links += ' · <a href="customs-pass-route.html">取经路线关隘</a>'
if add_links:
    m = re.search(r'(<a href="\.\./dashboard\.html"[^>]*>[^<]*返回 dashboard[^<]*</a>)', csg)
    assert m, 'chapter-structure 相关页面行未定位'
    csg = csg[:m.end()] + add_links + csg[m.end():]
    wr('site/data/chapter-structure-graph.html', csg)
    CHANGES.append(('site/data/chapter-structure-graph.html', 'R-03 vis 页入口', 1))
else:
    CHANGES.append(('site/data/chapter-structure-graph.html', 'vis 入口已存在·跳过', 0))

print('== W1074 changes ==')
for p, tag, n in CHANGES:
    print(f'  {p} :: {tag} (x{n})')
if not APPLY:
    print('DRY-RUN：加 --apply 落盘')
else:
    print('APPLIED')
