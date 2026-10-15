#!/usr/bin/env python3
"""_w551_fix_content.py — 一次性：§8.3 遗留问题内容修复（A 桑基补链 / B 文案对齐 / C 13d 口径统一）。
`_` 前缀：不入门禁、不参与 CI。执行后必须重跑 generate_csp.py。
"""

import re

def read(f):
    with open(f, encoding='utf-8', newline='') as fh:
        return fh.read()

def write(f, s):
    with open(f, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)

def sub_once(s, old, new, f, tag):
    n = s.count(old)
    assert n == 1, f'{f} [{tag}] 期望 1 处，实际 {n}: {old[:60]}'
    return s.replace(old, new)

# ---------- A. six-senses 桑基补链（CN/EN 各 16 条） ----------
CN_LINKS = '''{ source: "妖食", target: "唐僧肉", value: 2 },
      // W550 补全：时间/空间/嗅觉/触觉 术语→案例（三层结构闭环）
      { source: "循环结构", target: "轮回转世", value: 2 },
      { source: "线性结构", target: "取经历程", value: 2 },
      { source: "永恒结构", target: "五行山五百年", value: 2 },
      { source: "瞬间结构", target: "筋斗云", value: 2 },
      { source: "垂直结构", target: "天宫地府", value: 2 },
      { source: "水平结构", target: "西行万里", value: 2 },
      { source: "封闭结构", target: "无底洞", value: 2 },
      { source: "开放结构", target: "花果山", value: 2 },
      { source: "仙气", target: "蟠桃宴", value: 2 },
      { source: "妖风", target: "黄风怪", value: 2 },
      { source: "烟火", target: "火焰山", value: 2 },
      { source: "药香", target: "紫金红葫芦", value: 2 },
      { source: "金箍", target: "紧箍咒", value: 2 },
      { source: "兵器", target: "九齿钉钯", value: 2 },
      { source: "肌肤", target: "荆棘岭", value: 2 },
      { source: "法器", target: "紫金铃", value: 2 }'''

EN_LINKS = '''{ source: "Demonic Food", target: "Tang Sanzang\u2019s Flesh", value: 2 },
      // W550: Time/Space/Smell/Touch term-to-case links (close the three-layer flow)
      { source: "Cyclic Structure", target: "Reincarnation Cycle", value: 2 },
      { source: "Linear Structure", target: "The Journey West", value: 2 },
      { source: "Eternal Structure", target: "Five Hundred Years Under the Mountain", value: 2 },
      { source: "Instant Structure", target: "Somersault Cloud", value: 2 },
      { source: "Vertical Structure", target: "Heaven and the Underworld", value: 2 },
      { source: "Horizontal Structure", target: "Ten-Thousand-Li March", value: 2 },
      { source: "Closed Structure", target: "The Bottomless Pit", value: 2 },
      { source: "Open Structure", target: "Flower-Fruit Mountain", value: 2 },
      { source: "Immortal Aura", target: "Peach Banquet", value: 2 },
      { source: "Demonic Wind", target: "Yellow Wind Demon", value: 2 },
      { source: "Smoke and Fire", target: "Flaming Mountain", value: 2 },
      { source: "Medicinal Aroma", target: "Purple-Gold Red Gourd", value: 2 },
      { source: "Golden Fillet", target: "The Tightening Spell", value: 2 },
      { source: "Weapons", target: "Nine-Toothed Rake", value: 2 },
      { source: "Skin", target: "Thorn Ridge", value: 2 },
      { source: "Ritual Artifact", target: "Purple-Gold Bells", value: 2 }'''

f = 'site/data/six-senses-narratology-network.html'
s = read(f)
s = sub_once(s, '{ source: "妖食", target: "唐僧肉", value: 2 }', CN_LINKS, f, 'sankey-cn')
n5 = s.count('案例数: 5')
s = s.replace('案例数: 5', '案例数: 4')
write(f, s)
print(f'[A] OK {f}（+16 链；案例数 5→4 x{n5}）')

f = 'site/en/six-senses-narratology-network.html'
s = read(f)
s = sub_once(s, '{ source: "Demonic Food", target: "Tang Sanzang\u2019s Flesh", value: 2 }', EN_LINKS, f, 'sankey-en')
write(f, s)
print(f'[A] OK {f}（+16 链）')

# ---------- B. relationships 文案对齐图表（88/78） ----------
for f, edits in {
    'site/data/relationships.html': [
        ('以 89 回共现位居演化曲线榜首', '以 88 回共现位居演化曲线榜首'),
        ('以约 70 回共现居第二', '以 78 回共现居第二'),
    ],
    'site/en/relationships.html': [
        ('leads the evolution curve with 89 co-occurring chapters', 'leads the evolution curve with 88 co-occurring chapters'),
        ('ranks second at about 70 co-occurring chapters', 'ranks second at 78 co-occurring chapters'),
    ],
}.items():
    s = read(f)
    for old, new in edits:
        s = sub_once(s, old, new, f, 'prose')
    write(f, s)
    print(f'[B] OK {f}')

# ---------- C. 13d 口径统一 16（CN/EN） ----------
f = 'site/data/narratology-13d-network.html'
s = read(f)
s = sub_once(s, '<title>十七维叙事学关系图谱', '<title>十六维叙事学关系图谱', f, 'title')
s = sub_once(s, 'NARRATOLOGY 17-DIMENSION NETWORK', 'NARRATOLOGY 16-DIMENSION NETWORK', f, 'subtitle')
s = sub_once(s, '<div class="kpi-value">17</div><div class="kpi-label">叙事学维度</div>', '<div class="kpi-value">16</div><div class="kpi-label">叙事学维度</div>', f, 'kpi')
n13 = s.count('十三维')
s = s.replace('十三维', '十六维')
s = sub_once(s, 'OVERVIEW: 13-DIMENSION NARRATOLOGY FRAMEWORK', 'OVERVIEW: 16-DIMENSION NARRATOLOGY FRAMEWORK', f, 'sub')
write(f, s)
print(f'[C] OK {f}（17→16 标题/KPI；十三维→十六维 x{n13}）')

f = 'site/en/narratology-13d-network.html'
s = read(f)
s = sub_once(s, '<title>Seventeen-Dimension Narratology Network', '<title>Sixteen-Dimension Narratology Network', f, 'title')
s = sub_once(s, 'Seventeen-Dimension Narratology Network</a>', 'Sixteen-Dimension Narratology Network</a>', f, 'crumb') if 'Seventeen-Dimension Narratology Network</a>' in s else s
s = sub_once(s, '<div class="kpi-value">17</div><div class="kpi-label">Narratology Dimensions</div>', '<div class="kpi-value">16</div><div class="kpi-label">Narratology Dimensions</div>', f, 'kpi')
n13 = s.count('Thirteen-Dimension')
s = s.replace('Thirteen-Dimension', 'Sixteen-Dimension')
s = sub_once(s, 'OVERVIEW: 13-DIMENSION NARRATOLOGY FRAMEWORK', 'OVERVIEW: 16-DIMENSION NARRATOLOGY FRAMEWORK', f, 'sub')
s = sub_once(s, 'the theoretical expansion "seven senses \u2192 twelve dimensions \u2192 thirteen dimensions"', 'the theoretical expansion "seven senses \u2192 twelve dimensions \u2192 sixteen dimensions"', f, 'history')
write(f, s)
print(f'[C] OK {f}（17→16；Thirteen→Sixteen x{n13}）')

print('\n内容修复完成')
