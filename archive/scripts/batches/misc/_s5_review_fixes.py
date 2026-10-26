"""对抗审读修复批：P1×1 + P2×5 + P3 采纳项（逐处断言）"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\xiyouji\docs\S4-学术投稿'
fails = []

def apply(path, pairs):
    t = open(path, encoding='utf-8', newline='').read()
    for tag, old, new, cnt in pairs:
        n = t.count(old)
        if n != cnt:
            fails.append(f'{os.path.basename(path)} [{tag}] expect {cnt} got {n}')
            continue
        t = t.replace(old, new)
    open(path, 'w', encoding='utf-8', newline='').write(t)
    print('OK', os.path.basename(path), f'({len(pairs)} pairs)')

# ============ 明清稿：L170 数据修正 + 并行措辞 + 注号重排 ============
MQ = [
 ('回次差口径', '横跨全书 86 个回目，平均每 2.9 回出现一次驿传叙事节点',
  '按首末节点回次差横跨 86 个回目（第 12 回至第 98 回），平均每 2.9 回出现一次驿传叙事节点', 1),
 ('并行→伴随', '而是与取经主线并行的"第二叙事线"', '而是伴随取经主线反复出现的"第二叙事线"', 1),
 ('空白段口径', '显著的空白出现在第 30—38 回（宝象国之后至乌鸡国之前，九回无驿传节点）',
  '显著的空白出现在第 30—38 回（宝象国之后至乌鸡国之前，九回无关文节点；第 30 回金亭馆驿属补充集馆驿节点，不计入）', 1),
 ('州郡县三处修正',
  '关文叙事的空间节点几乎全部位于"国"级行政单元（宝象国、乌鸡国、车迟国、女儿国、祭赛国、朱紫国、比丘国、天竺国），而"州郡县"级单元（玉华县）在关文节点中仅一处。补充集则把图景补全：凤仙郡（第 87 回，郡级行政单元，关牒直达天廷）与铜台府地灵县（第 96-97 回，司法递解）显示，州郡县层级经由馆驿投驻与司法案件同样进入驿传网络——"国"级承担关文仪式，"郡县"级承担治理延伸，且第 78 回行者的言论明确区分了"西邦王位"与"府州县"的查验差异：小说对驿递制度的文学转写，严格遵循着明代行政等级的地理语法。',
  '关文叙事的空间节点多数位于"国"级行政单元（宝象国、乌鸡国、车迟国、女儿国、祭赛国、朱紫国、狮驼国、灭法国、比丘国、天竺国），"州郡县"级单元则有四处入集——玉华县（验讫）、金平府（未验）、铜台府（波折）入关文节点表，凤仙郡（第 87 回，郡级行政单元，关牒直达天廷）入补充集——州郡县层级经由验讫、司法与行政诉求同样进入驿传网络。相较"国"级主要承担关文仪式，"州郡县"级更多承担治理延伸与地方变奏，且第 78 回行者的言论明确区分了"西邦王位"与"府州县"的查验差异：小说对驿递制度的文学转写，在明代行政等级的地理语法上与制度史描述高度同构。', 1),
 ('驿递铺三系展开', '（驿递铺三系、勘合验引、信息通道）', '（驿、递、铺三系，勘合验引，信息通道）', 1),
]
# 注号重排（环换）：⑱→⑳, ⑳→㉒, ㉒→⑲, ⑲→㉑, ㉑→⑱
CYCLE = [('\u2467','\u2473'), ('\u2472','\u2473')]  # placeholder 逻辑见下
def renumber(t):
    # 占位三步换
    for old, ph in [('⑱','⟦A⟧'), ('⑳','⟦B⟧'), ('㉒','⟦C⟧'), ('⑲','⟦D⟧'), ('㉑','⟦E⟧')]:
        t = t.replace(old, ph)
    for ph, new in [('⟦A⟧','⑳'), ('⟦B⟧','㉒'), ('⟦C⟧','⑲'), ('⟦D⟧','㉑'), ('⟦E⟧','⑱')]:
        t = t.replace(ph, new)
    return t

for fn in ['01-论文/明清小说方向-投稿版.md', '01-论文/明清小说方向-匿名稿.md']:
    p = os.path.join(ROOT, fn)
    t = open(p, encoding='utf-8', newline='').read()
    for tag, old, new, cnt in MQ:
        n = t.count(old)
        if n != cnt:
            fails.append(f'{fn} [{tag}] expect {cnt} got {n}')
            continue
        t = t.replace(old, new)
    # 注号重排（第 4 条 expected 0 的占位对跳过）
    n18, n19, n20, n21, n22 = (t.count(x) for x in ['⑱','⑲','⑳','㉑','㉒'])
    t = renumber(t)
    # 重排后的头注旧文案（各圈号已被替换）→ 换成最终文案
    t = t.replace('⑳—⑲ 系 2026-10-08 增补：⑳—㉒ GIS 对话·⑱⑲ 制度史近况·均经 CNKI 检索核验',
                  '⑱—㉒ 系 2026-10-08 增补（⑱⑲ 制度史近况·⑳—㉒ GIS 对话·均经 CNKI 检索核验·注号已按出现顺序重排）')
    open(p, 'w', encoding='utf-8', newline='').write(t)
    print('OK', fn, f'重排前 ⑱{n18} ⑲{n19} ⑳{n20} ㉑{n21} ㉒{n22} → 重排后守恒:', all(t.count(x) for x in ['⑱','⑲','⑳','㉑','㉒']))

# ============ 心学稿：指涉错位 + 四要素改述 + 移除行内 [n] ============
XX = [
 ('索隐指涉', '恰恰落入本文第二节所拒斥的逐条"索隐"', '恰恰落入本文结论所拒斥的逐条"索隐"', 1),
 ('四要素改述', '渗透的证据是叙事骨架（弧线、回目命名、人物设置、冲突内核）按心学语法运转，而不是每一个情节单元都携带心学功能。',
  '渗透的证据是叙事骨架——弧线如何分段、回目如何命名、冲突如何设核——整体上按心学语法运转，而不要求每一个情节单元都携带心学功能。', 1),
 ('[14] 标记撤', '宣告了"西游学"的学科自觉[14]；', '宣告了"西游学"的学科自觉；', 1),
 ('[15] 标记撤', '作了晚近的通论性梳理[15]；', '作了晚近的通论性梳理；', 1),
 ('[16] 标记撤', '考察李卓吾评本批点者的心学观[16]；', '考察李卓吾评本批点者的心学观；', 1),
 ('[17] 标记撤', '聚焦小说与泰州王门的关系[17]。', '聚焦小说与泰州王门的关系。', 1),
 ('[18] 标记撤', '故事版本"[18]，但该文止于主题断言', '故事版本"，但该文止于主题断言', 1),
]
for fn in ['01-论文/心学方向-投稿版.md', '01-论文/心学方向-匿名稿.md']:
    apply(os.path.join(ROOT, fn), XX)

# ============ C 轨三文件：误报句改写 + 英摘披露 + [^8] 勾连 + 头注说明 ============
C = [
 ('误报句终测口径', '本批 439 条引文行全部通过，即当批无一合法引文被门禁误拦（观察误报为 0）；跨底本的系统性误报率，与语义层误判率同待影子模式量化（见第六节）。',
  '本批终测无一引文行未命中，即在终测口径下观察误报为 0（写作过程中经语法门禁拦截后修正的引文行，不计入本口径）；跨底本的系统性误报率，与语义层误判率同待影子模式量化（见第六节）。', 1),
 ('英摘三条披露', '— including the eight carried by the two versions of this paper — achieved',
  '— including the eight carried by the two versions of this paper and three more added to the denominator after a gate hardening — achieved', 1),
 ('[^8] 类型勾连', '该基准的结论是：各类引文核验器的可部署性取决于误报率而非召回率。',
  '该基准的结论是：各类引文核验器的可部署性取决于误报率而非召回率（正文所计 14 种幻觉类型，在该基准中归并为三种失效模式诊断）。', 1),
]
CFILES = ['01-论文/可验证性方向-投稿版.md', '01-论文/可验证性方向-匿名稿.md',
          '05-投稿/数字人文研究投稿/可验证性方向-数字人文研究适配版.md']
for fn in CFILES:
    apply(os.path.join(ROOT, fn), C)
# 头注 Markdown 注号说明（条件式）
for fn in CFILES:
    p = os.path.join(ROOT, fn)
    t = open(p, encoding='utf-8', newline='').read()
    if 'Markdown 源注号' in t:
        print('skip(已有) ', os.path.basename(fn))
        continue
    done = False
    for i, ln in enumerate(t):
        if l.startswith('> 体例说明') and not l.endswith('。）'):
            pass
    lines = t.split('\n')
    for i, ln in enumerate(lines):
        if l.startswith('>') and '脚注' in l:
            lines[i] = l + '\n> 注号说明：Markdown 源脚注号为写作标签、非出现顺序，以 Word 版连续圈号为准。'
            done = True
            break
    open(p, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
    print('头注注号说明', 'OK' if done else 'SKIP', os.path.basename(fn))

# ============ B 轨引号规范 ============
B = [('直角引号规范', '设计研究一侧，「新中式」的讨论近年集中在家居与家具场景：或建构「物-境互构」的场景创新模型并作推演评价⑱',
      '设计研究一侧，“新中式”的讨论近年集中在家居与家具场景：或建构“物-境互构”的场景创新模型并作推演评价⑱', 1)]
for fn in ['05-投稿/装饰投稿/设计方向-装饰投稿版.md', '05-投稿/装饰投稿/设计方向-匿名稿.md']:
    apply(os.path.join(ROOT, fn), B)

print()
print('FAILS:', fails if fails else '无')
