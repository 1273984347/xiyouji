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
  R4  （W1342）族注册完备性：site/data 实际渲染的图表族必须已在 §4B 表内——表外族
      （W1341 审查实证雷达族 27 页在用却不在表内）⇒ 该族无禁用条件/无降级档/零判据
  R5  （W1342）雷达族规模判据：基线外页面（新页/改动页）须声明
      `<!-- chart-radar-meta: axes=N series=M -->`，且轴 ≤8、单图系列 ≤3；基线名单
      `scripts/output/radar-family-baseline.txt` 冻结存量 27 页（W1341 审查实测的超载面）
      辖区（W1350 扩面）：site/data + site/en——EN 镜像页与 ZH 同受规模约束（R4 仍限
      site/data，选型章的登记对象是中文数据图表页）
  R7  （W1354）雷达族口径判据：雷达族页面须在页内写明 `口径：`（轴值来源与可复算入口），
      防「评分从哪来」整族留白（W1341 P1 实证：单图 3/4 轴取值恒等却无处说明口径）。
      基线内页面豁免（与 R5 同名单）；**辖区 site/data + site/en**——英文页用「Caliber:」
      等价行（W1355 补齐 27 个 EN 雷达页后扩面，与 R5 辖区一致）。
  R8  （W1355）等分索引盘 × 占比措辞错配：`d3.pie()...value(1)` 是**等分排布**（索引语义），
      不承载占比；若页面同时以「占比 N%」形式主张占比 ⇒ FAIL（实测来源：karma-reincarnation
      10 类各 1 例被写成「占比 10%」）。否定式（非占比/不代表占比）不命中。
  R9  （W1357·批 C-1）地图族口径判据：① 含 `d3.geo*` 的页面须声明
      `<!-- chart-map-meta: projection=geo|schematic basemap=self -->`；② 已声明者形态须合法；
      ③ 任何页面出现外部瓦片/地图服务域即 FAIL（file:// 零外域·铁律 5）。

  设计取舍（W551）：连线画布遮挡、桑基空渲染、reveal 空带、横向溢出等需要真实渲染
  状态的缺陷由 check_screenshot_gates.js（Playwright 动态门禁）覆盖——静态代理
  （CSS 声明/DOM 顺序）经实证不可靠（monster-hierarchy 有不透明背景但边可见，
  canvas 与 svg 的先后顺序 CSS 无法表达）。

--self-test：对内置负样本断言 R1/R2/R3 各自命中、R4/R5/R7/R8/R9 各自命中与放行、好样本与
R3 正样本不命中（W654 扩至 6 例·W1342 扩至 10 例）。
--spec-check DESIGN.md：解析 §4B 选型章表体行与空单元格（AC-4：行 10·空格 0）。
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

# §4B 表体行数（W1342：随「雷达图」入表 9 → 10；改表须同批改此常量，spec-check 才不假红/假绿）
EXPECT_SPEC_ROWS = 10

# R4（W1342）：族注册完备性——渲染签名（id/function 级，非正文关键词）。
# 为什么不复用 FAMILIES：R3 是「措辞→实现」正向判据，把「雷达」加进 R3 词表会把
#   「页脚链到 language-style-radar.html」这类纯提及误判成错配（W1341 实测 6 页此形态）。
RADAR_SIG = re.compile(r'id="[^"]*radar|class="[^"]*radar-|function\s+\w*[Rr]adar|render\w*Radar', re.I)
FAMILY_SIGS = [
    # (族标签, 渲染签名, §4B 章内用于判「已注册」的词——取表内原词，不给表加别名)
    ('雷达', RADAR_SIG, '雷达图'),
    ('和弦', re.compile(r'chord', re.I), '和弦图'),
    ('桑基', re.compile(r'sankey', re.I), '桑基图'),
    ('树图', re.compile(r'treemap|d3\.pack\s*\(', re.I), '树图'),
    ('力导向', re.compile(r'forceSimulation', re.I), '力导向图'),
    ('折线', re.compile(r'd3\.line\s*\(', re.I), '折线图'),
    ('面积', re.compile(r'd3\.area\s*\(|d3\.stack\s*\(', re.I), '面积图'),
    ('柱形', re.compile(r'scaleBand', re.I), '条形图'),
    ('弧形', re.compile(r'd3\.pie\s*\(', re.I), '弧形图'),
    ('画布', re.compile(r'THREE\.', re.I), '画布'),
]

# R5（W1342）：雷达族规模判据（阈值取自 DESIGN §4B 雷达行「禁用条件」）
RADAR_META = re.compile(r'chart-radar-meta:\s*axes=(\d+)\s+series=(\d+)')
RADAR_MAX_AXES = 8
RADAR_MAX_SERIES = 3
RADAR_BASELINE = os.path.join(ROOT, 'scripts', 'output', 'radar-family-baseline.txt')

# R7（W1354 立·W1355 扩面）：雷达族口径判据——页内须有「口径：」或英文「Caliber:」行
CALIBER = re.compile(r'口径：|Caliber:')

# R8（W1355）：等分索引盘 × 占比措辞错配。
#   签名：d3.pie()...value(1)（等分排布）——只承载「排布/索引」语义，不承载占比。
#   措辞：必须带数字的占比主张（「占比 10%」）才算主张；「非占比/不代表占比」等否定式不命中。
RE_EQUAL_PIE = re.compile(r'd3\.pie\(\)[\s\S]{0,240}?\.value\(\s*(?:d\s*=>\s*)?1\s*\)')
RE_SHARE_WORD = re.compile(r'占比\s*[：:]?\s*\d')

# R9（W1357·批 C-1）：地图族口径判据
#   ① 含 d3.geo* 的页面必须声明 chart-map-meta（projection=geo basemap=self）
#   ② 凡声明 chart-map-meta 的页面，形态必须合法（projection ∈ geo|schematic，且 basemap=self）
#   ③ 任何页面引用外部瓦片/地图服务域 = 违反 file:// 零外域铁律（铁律 5）
RE_MAP_META = re.compile(r'chart-map-meta:\s*projection=(geo|schematic)\s+basemap=self\b')
RE_GEO_SIG = re.compile(r'd3\.geo[A-Z]')
RE_MAP_EXT = re.compile(r'tile\.openstreetmap|api\.mapbox|webapi\.amap|arcgisonline|cesium\.ion', re.I)


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
    #   结束标签放宽到 `</script` + 任意空白 + 可选属性 + `>`（HTML 允许 </script bar>
    #   与 </script\t\n bar> 这类带属性/畸形空白形态·CodeQL 要求正则能匹配该形态）。
    #   属性段用**否证式** `(?:(?!>)[\s\S])*` 而非 `[^>]*`：
    #     ① 语义等价（逐字符否证「不是 >」⇒ 可跨行）；
    #     ② **不含 `[^…]` 字符类** ⇒ 不被第 31 门禁的跨行改写扫描器判 🔴 高危
    #        （`[^…]*` 类 + re.sub + 无尾锚点 ⇒ 判「可跨行静默删内容」·W1014 判据）。
    body = re.sub(r'<script(?:(?!>)[\s\S])*>[\s\S]*?</script[ \t\r\n]*(?:(?!>)[\s\S])*>',
                  ' ', body, flags=re.IGNORECASE)
    body = re.sub(r'<style(?:(?!>)[\s\S])*>[\s\S]*?</style[ \t\r\n]*(?:(?!>)[\s\S])*>',
                  ' ', body, flags=re.IGNORECASE)
    return RE_HTML_TAG.sub(' ', body)                       # ② 标签按语法约束


def strip_js_comments(js):
    js = re.sub(r'/\*[\s\S]*?\*/', ' ', js)
    return re.sub(r'(?m)//.*$', ' ', js)


def _check_sankey_refs(html, path, incs):
    """R1 引用面：sankey 脚本引用存在性（W1237 拆 def·判定逐字未改）。"""
    if not incs:
        return ['R1 调用 d3.sankey 但未引用 d3-sankey 脚本']
    in_site = os.path.realpath(path).startswith(os.path.realpath(os.path.join(ROOT, 'site')) + os.sep)
    if not in_site:
        return []
    fails = []
    for rel in set(incs):
        fp = os.path.normpath(os.path.join(os.path.dirname(path), rel))
        if not os.path.exists(fp):
            fails.append(f'R1 引用的 sankey 脚本不存在: {rel}')
    return fails


def check_page(path, r3_scope=None):
    """返回 fails 列表。path 为绝对路径；r3_scope=None 时按 site/data 辖区自动判定。"""
    fails = []
    with open(path, encoding='utf-8', errors='ignore') as f:
        html = f.read()
    visible = strip_invisible(html)

    # R1: sankey 调用 ↔ 脚本引用
    js_all = ' '.join(re.findall(r'<script[\s\S]*?</script>', html))
    if SANKEY_CALL.search(strip_js_comments(js_all)):
        fails.extend(_check_sankey_refs(html, path, SANKEY_INC.findall(html)))
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

    # R7（W1354）已在 main 的雷达辖区循环里判；R8（W1355）：等分索引盘不得自称「占比」
    if RE_EQUAL_PIE.search(strip_js_comments(js_all)) and RE_SHARE_WORD.search(visible):
        fails.append('R8 等分索引盘自称占比（d3.pie().value(1) 的等分只承载排布语义·不承载占比）')
    # R9（W1357·批 C-1）：地图族口径
    if RE_GEO_SIG.search(html) and not RE_MAP_META.search(html):
        fails.append('R9 地图族页面缺 chart-map-meta 声明（须 projection=geo basemap=self）')
    if 'chart-map-meta:' in html and not RE_MAP_META.search(html):
        fails.append('R9 chart-map-meta 形态非法（须 projection=geo|schematic 且 basemap=self）')
    if RE_MAP_EXT.search(html):
        fails.append('R9 引用外部瓦片/地图服务域（file:// 零外域铁律禁外部底图）')

    return fails


def design_segment(design_path):
    """取 DESIGN.md §4B 章全文（到下一个二级标题止）；缺章返回 None。"""
    with open(design_path, encoding='utf-8') as f:
        s = f.read()
    i = s.find('## 4B. 图表选型与数据契约')
    if i == -1:
        return None
    seg = s[i:]
    j = seg.find('\n## ', 1)
    return seg[:j] if j != -1 else seg


def family_registry_fails(htmls, design_path):
    """R4（W1342）：站内实际渲染的族若不在 §4B 章内 → [(族名, 命中页数)]。

    判据方向是「实族 ⊆ 表内族」：表内族可以零页在用（如和弦），表外族一页在用即 FAIL。
    """
    seg = design_segment(design_path)
    if seg is None:
        return [('§4B 章缺失', 0)]
    fam_key = {f: k for f, _s, k in FAMILY_SIGS}
    hits = {}
    for html in htmls:
        for fam, sig, _key in FAMILY_SIGS:
            if sig.search(html):
                hits[fam] = hits.get(fam, 0) + 1
    return [(fam, n) for fam, n in sorted(hits.items()) if fam_key[fam] not in seg]


def radar_scale_fails(rel, html, baseline):
    """R5（W1342）：雷达族规模判据。rel 为仓库相对路径；基线内页面豁免（存量冻结）。"""
    if not RADAR_SIG.search(html):
        return []
    if rel.replace('\\', '/') in baseline:
        return []
    m = RADAR_META.search(html)
    if not m:
        return ['R5 雷达族页面缺规模声明（须 <!-- chart-radar-meta: axes=N series=M -->·存量页入基线）']
    axes, series = int(m.group(1)), int(m.group(2))
    fails = []
    if axes > RADAR_MAX_AXES:
        fails.append(f'R5 雷达轴数 {axes} > §4B 上限 {RADAR_MAX_AXES}（禁用条件：改热力矩阵）')
    if series > RADAR_MAX_SERIES:
        fails.append(f'R5 雷达系列数 {series} > §4B 上限 {RADAR_MAX_SERIES}（禁用条件：改单选雷达 + 排序点图）')
    return fails


def radar_caliber_fails(rel, html, baseline):
    """R7（W1354）：雷达族口径判据——页内须写明「口径：」（轴值来源与可复算入口）。

    只判存在性（文本级），不判口径内容正确与否——内容正确性由批 A-3 逐页取证与
    数据源区块对拍保证；存在性判据负责「新页与改动页不得再留白」。
    """
    if not RADAR_SIG.search(html):
        return []
    if rel.replace('\\', '/') in baseline:
        return []
    if not CALIBER.search(html):
        return ['R7 雷达族页面缺「口径：」/「Caliber:」行（须写明轴值来源与复算或数据源入口·存量页入基线）']
    return []


def load_baseline(path=None):
    """读基线名单（一行一路径·# 后为注释）。"""
    path = path or RADAR_BASELINE
    if not os.path.exists(path):
        return set()
    out = set()
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.split('#', 1)[0].strip()
            if line:
                out.add(line.replace('\\', '/'))
    return out


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
    ok = len(rows) == EXPECT_SPEC_ROWS and empty == 0
    if not ok:
        print(f'spec-check FAIL（期望行 {EXPECT_SPEC_ROWS}·空格 0·改表须同批改 EXPECT_SPEC_ROWS）')
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
    # W1342 新增四例（R4/R5 的可证伪锁——判据放宽或写歪都会在这里红）：
    radar_html = '<html><body><svg id="chart-radar"></svg></body></html>'
    design_no_radar = os.path.join(tempfile.gettempdir(), '_cgd_design_no_radar.md')
    with open(design_no_radar, 'w', encoding='utf-8') as f:
        f.write('## 4B. 图表选型与数据契约\n\n| 桑基图 | 折线图 |\n\n## 4C. 其他\n')
    unreg = family_registry_fails([radar_html], design_no_radar)
    if not any(fam == '雷达' for fam, _n in unreg):
        print('SELF-TEST FAIL: R4 表外族（雷达）未检出:', unreg)
        ok = False
    design_with_radar = os.path.join(tempfile.gettempdir(), '_cgd_design_with_radar.md')
    with open(design_with_radar, 'w', encoding='utf-8') as f:
        f.write('## 4B. 图表选型与数据契约\n\n| 雷达图 | 桑基图 |\n\n## 4C. 其他\n')
    if family_registry_fails([radar_html], design_with_radar):
        print('SELF-TEST FAIL: R4 已注册族被误报:', family_registry_fails([radar_html], design_with_radar))
        ok = False
    meta_ok = '<!-- chart-radar-meta: axes=5 series=3 -->'
    if radar_scale_fails('site/data/x.html', radar_html + meta_ok, set()):
        print('SELF-TEST FAIL: R5 合规声明被误报:', radar_scale_fails('site/data/x.html', radar_html + meta_ok, set()))
        ok = False
    if not radar_scale_fails('site/data/x.html', radar_html, set()):
        print('SELF-TEST FAIL: R5 缺规模声明未检出')
        ok = False
    if not radar_scale_fails('site/data/x.html', radar_html + '<!-- chart-radar-meta: axes=12 series=9 -->', set()):
        print('SELF-TEST FAIL: R5 超限（12 轴/9 系列）未检出')
        ok = False
    if radar_scale_fails('site/data/x.html', radar_html + '<!-- chart-radar-meta: axes=12 series=9 -->',
                         {'site/data/x.html'}):
        print('SELF-TEST FAIL: R5 基线内页面未豁免')
        ok = False
    # W1354 新增两例（R7 口径判据的可证伪锁）：
    if not radar_caliber_fails('site/data/x.html', radar_html + meta_ok, set()):
        print('SELF-TEST FAIL: R7 无口径行未检出')
        ok = False
    if radar_caliber_fails('site/data/x.html', radar_html + meta_ok + '口径：轴值取自 dataset/x.json', set()):
        print('SELF-TEST FAIL: R7 合规口径行被误报')
        ok = False
    # W1355 新增两例（R8 等分盘×占比措辞的可证伪锁）：
    if not (RE_EQUAL_PIE.search('const p = d3.pie().value(d => 1).sort(null);')
            and RE_SHARE_WORD.search('每类 1 例 · 占比 10%')):
        print('SELF-TEST FAIL: R8 等分盘自称占比未检出')
        ok = False
    if RE_SHARE_WORD.search('等分排列（等分仅为索引排布，不代表占比）'):
        print('SELF-TEST FAIL: R8 否定式措辞被误报')
        ok = False
    # W1357 新增两例（R9 地图口径的可证伪锁）：
    if not RE_MAP_META.search('<!-- chart-map-meta: projection=geo basemap=self -->'):
        print('SELF-TEST FAIL: R9 合法声明未识别')
        ok = False
    if RE_MAP_META.search('<!-- chart-map-meta: projection=schematic basemap=osm -->'):
        print('SELF-TEST FAIL: R9 外部底图被误判为合规')
        ok = False
    print('self-test:', 'PASS（负样本命中 · 好样本放行）' if ok else 'FAIL')
    return ok


def r5_scope_pages(pages):
    """R5 辖区（W1350）：site/data + site/en。

    R4 族注册仍限 site/data（选型章登记对象=中文数据图表页）；但雷达规模是**图型契约**，
    EN 镜像页与 ZH 同构、同受「维度 ≤8 / 单图实体 ≤3」约束——W1350 收口前 EN 侧 27 页
    全部无声明且单图系列 4–17，属辖区留白（ZH 已清零、EN 仍旧形态），不是合规差异。
    """
    site = os.path.realpath(os.path.join(ROOT, 'site'))
    dirs = [os.path.join(site, 'data') + os.sep, os.path.join(site, 'en') + os.sep]
    out = []
    for p in pages:
        real = os.path.realpath(p)
        for d in dirs:
            if real.startswith(d):
                out.append(p)
                break
    return out


def main():
    ap = argparse.ArgumentParser(description='图表静态自洽门禁（W551 挂载·R3 于 W654 扩充）')
    ap.add_argument('--self-test', action='store_true', help='内置负样本自检（16 例）')
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

    # R4 辖区 site/data（选型章管数据图表页）；R5 辖区 site/data + site/en（W1350 扩面）
    data_dir = os.path.join(ROOT, 'site', 'data')
    data_pages = [p for p in pages
                  if os.path.realpath(p).startswith(os.path.realpath(data_dir) + os.sep)]
    r5_pages = r5_scope_pages(pages)
    texts = {}
    for p in r5_pages:
        with open(p, encoding='utf-8', errors='ignore') as f:
            texts[p] = f.read()
    for fam, n in family_registry_fails([texts[p] for p in data_pages],
                                        os.path.join(ROOT, 'DESIGN.md')):
        n_fail += 1
        print('FAIL R4 族未在 DESIGN §4B 注册：%s（%d 页在用·先入表再改页）' % (fam, n))
    baseline = load_baseline()
    for p in r5_pages:
        rel = os.path.relpath(p, ROOT)
        fails = radar_scale_fails(rel, texts[p], baseline) + radar_caliber_fails(rel, texts[p], baseline)
        if fails:
            n_fail += 1
            print('FAIL %s — %s' % (rel, '；'.join(fails)))

    print('图表静态自洽门禁：%d 页扫描 · 基线豁免 %d 页 · FAIL %d 页'
          % (len(pages), len(baseline), n_fail))
    sys.exit(1 if n_fail else 0)


if __name__ == '__main__':
    main()
