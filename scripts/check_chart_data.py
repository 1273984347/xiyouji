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


RE_HTML_TAG = re.compile(r"</?[A-Za-z][A-Za-z0-9:._-]*(?:\s[^<>]*)?/?>")


def strip_invisible(html):
    """剥掉 script/style/HTML 注释与标签，取可见文本。

    W1047 修（两处根因·非绕过）：
    ① **剥离顺序**：注释**优先**剥。原顺序（script → style → 注释）会被注释里的
       `<script>` **字面量**触发 script 剥离 ⇒ 一路吞到后面真正的 `</script>` ⇒
       注释的 `-->` 被吞掉 ⇒ 注释剥离失配 ⇒ 注释残留（实测 `site/_template.html`
       的「脚本区」注释即此形态）。
    ② **标签按语法约束**：旧式 `<[^>]+>` 起点只要是 `<` 就当标签 ⇒ JS 比较符 `<=`
       被当标签起点 ⇒ 跨行匹配时把**标签之间的正文整段吞掉**（实测
       `site/data/perf-canvas-rendering.html` 吞掉 `n.x <= viewX1 && … n.y >= viewY0`；
       `site/data/game-webnovel.html` 吞掉「灰<6.5」；en 版同两处）。
       新式要求**标签名以字母开头** ⇒ `<=` 不匹配；属性段允许跨行 ⇒ 多行合法标签
       （如 `site/data/ai-dialogue.html` 的跨行 `<input>`）仍剥得干净。
    影子对照实测（857 页）：新法相对旧法**修复** 5 页的误吞，且**零漏剥标签**
    （新法输出中残留标签的页 = 0）。
    """
    body = html[html.find('<body'):] if '<body' in html else html
    body = re.sub(r'<!--[\s\S]*?-->', ' ', body)          # ① 注释优先
    # W1066：标签名大小写不敏感（HTML 规范允许 <SCRIPT>/<Script>）——
    #   原式 `<script[\s\S]*?</script>` 只匹配小写 ⇒ 大写标签会漏剥
    #   （CodeQL js/regex-injection 告警「does not match upper case <SCRIPT> tags」·
    #    该告警同时是真缺陷：漏剥的 <SCRIPT> 内容会被当正文参与判据 ⇒ 假结论）。
    body = re.sub(r'<script\b[\s\S]*?</script\s*>', ' ', body, flags=re.IGNORECASE)
    body = re.sub(r'<style\b[\s\S]*?</style\s*>', ' ', body, flags=re.IGNORECASE)
    return RE_HTML_TAG.sub(' ', body)                       # ② 标签按语法约束


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
    # W1047 新增两例（剥标签两处根因的可证伪锁）：
    # ① JS 比较符 `<=` 不是标签 ⇒ 不得把「标签之间的正文」整段吞掉
    cmp_sample = ('<html><body><p>前文</p><script>var a = 1; if (a <= 2) {}</script>'
                  '<p>中段文字</p><p>后段文字</p></body></html>')
    vis1 = strip_invisible(cmp_sample)
    if '中段文字' not in vis1 or '后段文字' not in vis1:
        print('SELF-TEST FAIL: JS 比较符 `<=` 被当成标签起点⇒正文被吞:', vis1[:160])
        ok = False
    # ② 注释里的 `<script>` 字面量不得触发 script 剥离（否则一路吞到真 `</script>`）
    cmt_sample = ('<html><body><!-- 脚本区说明：页面内 <script> 内嵌数据 -->\n'
                  '<p>可见正文</p>\n<script>var b = 2;</script></body></html>')
    vis2 = strip_invisible(cmt_sample)
    if '可见正文' not in vis2:
        print('SELF-TEST FAIL: 注释内 `<script>` 字面量触发误剥离⇒可见正文被吞:', vis2[:160])
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
