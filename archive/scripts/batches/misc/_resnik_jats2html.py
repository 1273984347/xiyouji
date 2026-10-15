# 一次性脚本：JATS XML → HTML（Resnik & Hosseini 2026 全文转存·CC BY 4.0·不入库门禁）
# 来源：Europe PMC fullTextXML（NIH Public Access 作者稿）·转存须带署名与许可声明
import html
import sys
import xml.etree.ElementTree as ET

SRC = 'D:/xiyouji/docs/S4-学术投稿/06-文献/_resnik.xml'
OUT = 'D:/xiyouji/docs/S4-学术投稿/06-文献/_resnik.html'

CITATION = ('Resnik, D. B. & Hosseini, M. Hallucinated citations produced by generative '
            'artificial intelligence may constitute research misconduct when citations '
            'function as data in scholarly papers. <em>Accountability in Research</em>, '
            '2026. DOI: 10.1080/08989621.2026.2645390. PMID: 41833014. PMC13051339.')
SOURCE_NOTE = ('本 PDF 为全文转存版：由 Europe PMC 全文 XML（NIH Public Access 作者稿）'
               '重新排版生成，内容完整但<b>非出版社排版</b>。原文依 CC BY 4.0 开放获取，'
               '本转存保留署名与许可声明。出版社排版版：'
               'https://www.tandfonline.com/doi/full/10.1080/08989621.2026.2645390')


def text_of(el):
    return ''.join(el.itertext()).strip()


def inline_html(el):
    """递归序列化行内标记（italic/bold/sub/sup/ext-link/uri），其余取文本。"""
    tag = el.tag
    if tag in ('italic', 'em'):
        return '<em>' + ''.join(inline_html(c) if len(c) else html.escape(c) for c in el) + '</em>'
    if tag in ('bold', 'b'):
        return '<strong>' + ''.join(inline_html(c) if len(c) else html.escape(c) for c in el) + '</strong>'
    if tag == 'sub':
        return '<sub>' + html.escape(text_of(el)) + '</sub>'
    if tag == 'sup':
        return '<sup>' + html.escape(text_of(el)) + '</sup>'
    if tag in ('ext-link', 'uri'):
        href = el.get('{http://www.w3.org/1999/xlink}href') or el.get('href') or text_of(el)
        return f'<a href="{html.escape(href, quote=True)}">{html.escape(text_of(el))}</a>'
    out = []
    if el.text:
        out.append(html.escape(el.text))
    for c in el:
        out.append(inline_html(c))
        if c.tail:
            out.append(html.escape(c.tail))
    return ''.join(out)


def block_html(el, level=0):
    """块级：sec/p/table-wrap/list。"""
    tag = el.tag
    if tag == 'sec':
        title = el.find('title')
        out = []
        if title is not None:
            h = min(2 + level, 4)
            out.append(f'<h{h}>{html.escape(text_of(title))}</h{h}>')
        for c in el:
            if c.tag in ('title', 'label'):
                continue
            out.append(block_html(c, level + 1))
        return ''.join(out)
    if tag == 'p':
        return '<p>' + inline_html(el) + '</p>'
    if tag == 'table-wrap':
        parts = []
        label = el.find('label')
        cap = el.find('caption')
        if label is not None or cap is not None:
            parts.append('<p class="tbl-cap"><strong>' + html.escape(text_of(label) if label is not None else '') +
                         '</strong> ' + (inline_html(cap.find('title')) if cap is not None and cap.find('title') is not None else '') + '</p>')
        tbl = el.find('.//table')
        if tbl is not None:
            rows = []
            for tr in tbl.findall('.//tr'):
                cells = [text_of(tc) for tc in tr]
                rows.append('<tr>' + ''.join(f'<td>{html.escape(c)}</td>' for c in cells) + '</tr>')
            parts.append('<table>' + ''.join(rows) + '</table>')
        return ''.join(parts)
    if tag == 'list':
        items = ['<li>' + inline_html(li) + '</li>' for li in el.findall('list-item')]
        return '<ul>' + ''.join(items) + '</ul>'
    return '' if tag in ('float-group', 'object-id') else '<p>' + inline_html(el) + '</p>'


root = ET.parse(SRC).getroot()
front = root.find('front')
am = front.find('article-meta')
jmeta = front.find('journal-meta')

journal = text_of(jmeta.find('.//journal-title'))
year = text_of(am.find('.//year')) or '2026'
volume = text_of(am.find('.//volume'))
issue = text_of(am.find('.//issue'))
authors = []
for contrib in am.findall('.//contrib-group/contrib'):
    if contrib.get('contrib-type') != 'author':
        continue
    n = contrib.find('.//name')
    if n is not None:
        authors.append((text_of(n.find('surname')), text_of(n.find('given-names'))))
auth_html = ', '.join(f'{html.escape(s)}, {html.escape(g)}' for s, g in authors)

title = text_of(am.find('.//article-title'))
abstract_el = am.find('abstract')
abstract_html = ''.join(block_html(p) for p in abstract_el.findall('.//p')) if abstract_el is not None else ''

body_html = ''.join(block_html(c) for c in root.find('body'))
refs = [text_of(r.find('.//mixed-citation')) or text_of(r) for r in root.findall('.//ref-list/ref')]
refs_html = ''.join(f'<li>{html.escape(r)}</li>' for r in refs)

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>
body{{font-family:Georgia,'Times New Roman',serif;font-size:11pt;line-height:1.55;color:#1a1a1a;max-width:46em;margin:0 auto;padding:0 1em}}
.cover{{border:1px solid #999;padding:1em;margin:1.5em 0;font-size:9.5pt;background:#f7f5f0}}
.cover .cite{{margin:.4em 0}}
.cover .note{{color:#444;margin-top:.6em}}
h1{{font-size:16pt;line-height:1.3}} h2{{font-size:13pt;border-bottom:1px solid #ccc;padding-bottom:.2em}} h3{{font-size:12pt}}
.meta{{color:#555;font-size:10pt}}
p{{text-align:justify}}
table{{border-collapse:collapse;width:100%;font-size:9.5pt;margin:.8em 0}}
td{{border:1px solid #bbb;padding:4px 6px;vertical-align:top}}
.tbl-cap{{font-size:9.5pt}}
.refs li{{font-size:9.5pt;margin:.35em 0}}
.abstract{{background:#f7f5f0;padding:.8em;margin:1em 0}}
a{{color:#1a4b8c}}
footer{{margin-top:2em;font-size:9pt;color:#555;border-top:1px solid #ccc;padding-top:.6em}}
</style></head><body>
<div class="cover"><div><b>转存文献 · 全文版</b></div><div class="cite">{CITATION}</div>
<div class="meta">{html.escape(journal)}{(' · vol ' + volume) if volume else ''}{(' · issue ' + issue) if issue else ''} · {year} · 收录：PMC（NIH Public Access 作者稿 NIHMS2161665）/ PubMed 41833014</div>
<div class="note">{SOURCE_NOTE}</div></div>
<h1>{html.escape(title)}</h1>
<p class="meta">{auth_html}</p>
<div class="abstract"><b>Abstract</b>{abstract_html}</div>
{body_html}
<h2>References</h2><ol class="refs">{refs_html}</ol>
<footer>License: CC BY 4.0（https://creativecommons.org/licenses/by/4.0/）· 原文：https://pmc.ncbi.nlm.nih.gov/articles/PMC13051339/ · 本文件为项目文献存档 docs/S4-学术投稿/06-文献/（2026-09-26 生成）</footer>
</body></html>"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
print('html written:', len(HTML), 'bytes')
