# _w555_f3.py — F3: relationships 中英两页 唐僧-孙悟空 共现数统一为 89（权威值=per_chapter/top_pairs_curve）
import io

FIXES = {
    'site/data/relationships.html': [
        ('唐僧-悟空 90 回共现最强', '唐僧-悟空 89 回共现最强'),
        ('唐僧-悟空 90 回最强', '唐僧-悟空 89 回最强'),
        ('以 90 回共现位居关系强度榜首', '以 89 回共现位居关系强度榜首'),
        ('以 88 回共现位居演化曲线榜首', '以 89 回共现位居演化曲线榜首'),
        ('"source": "唐僧",\n                                "target": "孙悟空",\n                                "weight": 90',
         '"source": "唐僧",\n                                "target": "孙悟空",\n                                "weight": 89'),
    ],
    'site/en/relationships.html': [
        ('Tang Sanzang–Wukong at 90 chapters is the strongest link', 'Tang Sanzang–Wukong at 89 chapters is the strongest link'),
        ('Tang Sanzang–Wukong 90 chapters (strongest)', 'Tang Sanzang–Wukong 89 chapters (strongest)'),
        ('tops the relationship-strength ranking with 90 co-occurring chapters', 'tops the relationship-strength ranking with 89 co-occurring chapters'),
        ('leads the evolution curve with 88 co-occurring chapters', 'leads the evolution curve with 89 co-occurring chapters'),
        ('"source": "Tang Sanzang",\n                                "target": "Sun Wukong",\n                                "weight": 90',
         '"source": "Tang Sanzang",\n                                "target": "Sun Wukong",\n                                "weight": 89'),
    ],
}

for path, pairs in FIXES.items():
    s = io.open(path, encoding='utf-8', newline='').read()
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, f'{path}: [{old[:40]}] 命中 {n} 次'
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)
    print(path, '共', len(pairs), '处替换完成')

# 复核：两页不再有 88/90 的该对声明
for path in FIXES:
    s = io.open(path, encoding='utf-8').read()
    assert '88 回共现' not in s and '90 回共现' not in s, path
    assert '88 co-occurring' not in s and '90 co-occurring' not in s and 'at 90 chapters' not in s, path
print('复核通过：两页唐僧-孙悟空 共现声明全部统一为 89')
