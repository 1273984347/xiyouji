#!/usr/bin/env python3
"""check_chart_data.py — 图表静态自洽门禁（W551 挂载·verify_delivery 第 24 门禁）。

来源：W550 全站截图审查实证的三类批量图表缺陷（10 页桑基缺引用 / 4 组饼图措辞×树图实现
错配 / 12 页连线画布被不透明 svg 遮挡），均为门禁盲区积累数月后由人工大审查清账。
本门禁在文本层拦住同类复发。

检查项（阻断级 FAIL，均为零误报的纯文本规则）：
  R1  调用 d3.sankey( 的页面必须引用 d3-sankey 脚本，且引用的磁盘文件存在
  R2  可见文本含饼图系措辞（饼图/环形图/圆环图/Pie Chart/Donut Chart）且实现为
      treemap（d3.treemap 存在）且无任何弧形实现（d3.arc/d3.pie 均为 0）→ 错配
  R3  （W654·PD-1b）可见文本命中 §4B 图型词表（桑基/和弦/树图/力导向/折线/面积/柱形条形）
      但页内实现签名不存在 → 措辞×实现错配（词表见 FAMILIES·与 DESIGN.md §4B 选型章联动）

  设计取舍（W551）：连线画布遮挡、桑基空渲染、reveal 空带、横向溢出等需要真实渲染
  状态的缺陷由 check_screenshot_gates.js（Playwright 动态门禁）覆盖——静态代理
  （CSS 声明/DOM 顺序）经实证不可靠（monster-hierarchy 有不透明背景但边可见，
  canvas 与 svg 的先后顺序 CSS 无法表达）。

--self-test：对内置负样本断言 R1/R2/R3 各自命中、好样本与 R3 正样本不命中（W654 扩至 6 例）。
--spec-check DESIGN.md：解析 §4B 选型章表体行与空单元格（AC-4：行 9·空格 0）。
"""

import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PIE_WORDS = re.compile(r'饼图|环形图|圆环图|Pie Chart|Donut Chart')
SANKEY_CALL = re.compile(r'd3\.sankey\s*\(')
SANKEY_INC = re.compile(r'src="([^"]*d3-sankey[^"]*\.js)"')
TREEMAP = re.compile(r'd3\.treemap')
ARC = re.compile(r'd3\.arc')
PIE_IMPL = re.compile(r'd3\.pie')

# R3（W654·PD-1b）：§4B 图型词表 ↔ 实现签名（与 DESIGN.md §4B 选型章联动·加词须同批改章）
# 实现签名放宽口径：自定义实现（EMBEDDED_DATA.sankey 等无 d3 调用的手写图）以关键词在位为准；
# 辖区限 site/data（D-5/D1 先例——选型章管数据图表页·导航/根页的散文提及不属管辖）
FAMILIES = [
    ('桑基', ('桑基图', '桑基流', '桑基'), re.compile(r'sankey', re.I)),
    ('和弦', ('和弦图', '和弦'), re.compile(r'chord', re.I)),
    ('树图', ('矩形树图', '树图'), re.compile(r'treemap', re.I)),
    ('力导向', ('力导向图', '力导向'), re.compile(r'forceSimulation|d3\.force|nodePos|iters\s*=', re.I)),
    ('折线', ('折线图',), re.compile(r'd3\.line\s*\(|\.line\(', re.I)),
    ('面积', ('面积图',), re.compile(r'd3\.area\s*\(|\.area\(', re.I)),
    ('柱形', ('柱状图', '条形图'), re.compile(r'append\(["\']rect|scaleBand|bar', re.I)),
]


def strip_invisible(html):
    """剥掉 script/style/HTML 注释与标签，取可见文本。"""
    body = html[html.find('<body'):] if '<body' in html else html
    body = re.sub(r'<script[\s\S]*?</script>', ' ', body)
    body = re.sub(r'<style[\s\S]*?</style>', ' ', body)
    body = re.sub(r'<!--[\s\S]*?-->', ' ', body)
    return re.sub(r'<[^>]+>', ' ', body)


def strip_js_comments(js):
    js = re.sub(r'/\*[\s\S]*?\*/', ' ', js)
    return re.sub(r'(?m)//.*$', ' ', js)


def check_page(path, r3_scope=None):
    """返回 fails 列表。path 为绝对路径；r3_scope=None 时按 site/data 辖区自动判定。"""
    fails = []
    with open(path, encoding='utf-8', errors='ignore') as f:
        html = f.read()
    visible = strip_invisible(html)

    # R1: sankey 调用 ↔ 脚本引用
    js_all = ' '.join(re.findall(r'<script[\s\S]*?</script>', html))
    if SANKEY_CALL.search(strip_js_comments(js_all)):
        incs = SANKEY_INC.findall(html)
        if not incs:
            fails.append('R1 调用 d3.sankey 但未引用 d3-sankey 脚本')
        else:
            in_site = os.path.realpath(path).startswith(os.path.realpath(os.path.join(ROOT, 'site')) + os.sep)
            if in_site:
                for rel in set(incs):
                    fp = os.path.normpath(os.path.join(os.path.dirname(path), rel))
                    if not os.path.exists(fp):
                        fails.append(f'R1 引用的 sankey 脚本不存在: {rel}')
    # R2: 饼图措辞 × treemap 实现 × 无弧形实现
    if PIE_WORDS.search(visible) and TREEMAP.search(html) and not ARC.search(html) and not PIE_IMPL.search(html):
        words = sorted(set(PIE_WORDS.findall(visible)))
        fails.append(f'R2 饼图系措辞 × treemap 实现 × 无弧形实现（错配）: {words}')
    # R3（W654·PD-1b）: §4B 图型措辞 ↔ 实现签名（辖区=site/data·D-5/D1 先例）
    if r3_scope is None:
        r3_scope = os.path.realpath(path).startswith(os.path.realpath(os.path.join(ROOT, 'site', 'data')) + os.sep)
    if r3_scope:
        for fam, words, impl in FAMILIES:
            if any(w in visible for w in words) and not impl.search(html):
                fails.append(f'R3 措辞×实现错配（{fam}）: {words}')

    return fails


def spec_check(design_path):
    """AC-4：解析 DESIGN.md §4B 选型章表体行与空单元格。"""
    with open(design_path, encoding='utf-8') as f:
        s = f.read()
    i = s.find('## 4B. 图表选型与数据契约')
    if i == -1:
        print('spec-check FAIL: DESIGN.md 缺 §4B 选型章')
        return 1
    seg = s[i:]
    j = seg.find('\n## ', 1)
    if j != -1:
        seg = seg[:j]
    rows = [row for row in seg.split('\n')
            if row.startswith('| ') and '数据形态约束' not in row and not row.startswith('|---')]
    empty = sum(1 for row in rows for cell in row.strip().strip('|').split('|') if not cell.strip())
    print(f'spec-check: §4B 表体行 {len(rows)} · 空单元格 {empty}')
    ok = len(rows) == 9 and empty == 0
    if not ok:
        print('spec-check FAIL（期望行 9·空格 0）')
    return 0 if ok else 1


GOOD_SAMPLE = '''<!DOCTYPE html><html><head><style>
canvas[class*="link-canvas"] + svg { background: transparent !important; }
</style></head><body>
<script src="../static/js/d3.v7.min.js"></script>
<script src="../static/js/d3-sankey.min.js"></script>
<script>d3.sankey(); var t = d3.treemap(); var a = d3.arc();</script>
<h2>分布饼图</h2><div id="c"></div>
<script>document.createElement('canvas'); canvas.className = 'link-canvas';</script>
</body></html>'''

BAD_SANKEY = '''<html><body>
<script src="../static/js/d3.v7.min.js"></script>
<script>var layout = d3.sankey();</script>
</body></html>'''

BAD_PIE = '''<html><body>
<script>var t = d3.treemap();</script>
<h2>稀有度分布饼图</h2><p>Rarity Distribution Pie Chart</p>
</body></html>'''

BAD_R3_SANKEY = '''<html><body>
<script>var t = d3.treemap();</script>
<h2>三教关系桑基图</h2>
</body></html>'''

BAD_R3_CHORD = '''<html><body>
<h2>法宝流转和弦图</h2><p>实体对称关系</p>
</body></html>'''

GOOD_R3 = '''<html><body>
<script src="../static/js/d3-sankey.min.js"></script>
<script>var layout = d3.sankey();</script>
<h2>三教关系桑基图</h2>
</body></html>'''


def self_test():
    import tempfile
    ok = True
    good = os.path.join(tempfile.gettempdir(), '_cgd_good.html')
    with open(good, 'w', encoding='utf-8') as f:
        f.write(GOOD_SAMPLE)
    fails = check_page(good, r3_scope=True)
    if fails:
        print('SELF-TEST FAIL: 好样本被误报:', fails)
        ok = False
    for name, sample, needle in [
        ('R1 缺 sankey 引用', BAD_SANKEY, 'R1'),
        ('R2 饼图措辞错配', BAD_PIE, 'R2'),
        ('R3 桑基措辞×treemap 实现', BAD_R3_SANKEY, 'R3'),
        ('R3 和弦措辞无实现', BAD_R3_CHORD, 'R3'),
    ]:
        bad = os.path.join(tempfile.gettempdir(), '_cgd_bad.html')
        with open(bad, 'w', encoding='utf-8') as f:
            f.write(sample)
        fails = check_page(bad, r3_scope=True)
        if not any(f.startswith(needle) for f in fails):
            print(f'SELF-TEST FAIL: 负样本「{name}」未命中 {needle}:', fails)
            ok = False
    good_r3 = os.path.join(tempfile.gettempdir(), '_cgd_good_r3.html')
    with open(good_r3, 'w', encoding='utf-8') as f:
        f.write(GOOD_R3)
    fails = check_page(good_r3, r3_scope=True)
    if fails:
        print('SELF-TEST FAIL: R3 正样本（措辞+实现匹配）被误报:', fails)
        ok = False
    print('self-test:', 'PASS（负样本命中 · 好样本放行）' if ok else 'FAIL')
    return ok


def main():
    ap = argparse.ArgumentParser(description='图表静态自洽门禁（W551 挂载·R3 于 W654 扩充）')
    ap.add_argument('--self-test', action='store_true', help='内置负样本自检（6 例）')
    ap.add_argument('--spec-check', metavar='DESIGN_MD', help='AC-4：解析 §4B 选型章表体行与空单元格')
    args = ap.parse_args()

    if args.self_test:
        sys.exit(0 if self_test() else 1)
    if args.spec_check:
        sys.exit(spec_check(args.spec_check))

    pages = sorted(glob.glob(os.path.join(ROOT, 'site', '*.html'))
                   + glob.glob(os.path.join(ROOT, 'site', 'data', '*.html'))
                   + glob.glob(os.path.join(ROOT, 'site', 'en', '*.html')))
    n_fail = 0
    for p in pages:
        fails = check_page(p)
        if fails:
            n_fail += 1
            print('FAIL %s — %s' % (os.path.relpath(p, ROOT), '；'.join(fails)))
    print('图表静态自洽门禁：%d 页扫描 · FAIL %d 页' % (len(pages), n_fail))
    sys.exit(1 if n_fail else 0)


if __name__ == '__main__':
    main()
