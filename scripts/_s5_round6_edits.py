# -*- coding: utf-8 -*-
"""第六轮复审编辑批：措辞三处+误报观察句+DHR 英摘去重+文献清单建账"""
import io, sys, os
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

C100 = [
    ('摘要命中措辞', '当批实测结果：439 条引文行全部命中（含', '当批实测结果：439 条引文行逐字命中公开底本（含', 1),
    ('结论命中措辞', '当批实测给出 439 条引文行 100% 命中、892 个文件、亚秒级的成绩', '当批实测给出 439 条引文行逐字命中公开底本、覆盖 892 个文件、亚秒级完成的成绩', 1),
    ('英摘命中措辞', 'achieved a 100% hit rate across 892 files in under a second', 'achieved a 100% verbatim match rate against the public base text across 892 files in under a second', 1),
    ('误报观察句', '工具把版本学问题从"引文层"推回了它本该在的地方——正文与注释。',
     '工具把版本学问题从"引文层"推回了它本该在的地方——正文与注释。误报的实测口径同样需要交代：本批 439 条引文行全部通过，即当批无一合法引文被门禁误拦（观察误报为 0）；跨底本的系统性误报率，与语义层误判率同待影子模式量化（见第六节）。', 1),
]

apply(os.path.join(ROOT, '01-论文', '可验证性方向-投稿版.md'), C100)
apply(os.path.join(ROOT, '01-论文', '可验证性方向-匿名稿.md'), C100)

# ---- DHR 适配版：去重 + 同四编辑 ----
p = os.path.join(ROOT, '05-投稿', '数字人文研究投稿', '可验证性方向-数字人文研究适配版.md')
t = open(p, encoding='utf-8', newline='').read()
lines = t.split('\n')
# 定位我插入的英摘块（"After generative AI entered"）
a = next(i for i, l in enumerate(lines) if l.startswith('**Abstract**: After generative AI entered'))
# 块结构：a-1 空行, a EN, a+1 空行, a+2 Keywords(我), a+3 空行, a+4 中图分类号, a+5 空行, a+6 作者简介
assert lines[a+2].startswith('**Keywords**: digital humanities') and lines[a+4].startswith('**中图分类号**'), \
    (lines[a+2][:40], lines[a+4][:40])
zz = lines[a+4]
zz2 = lines[a+6]
# 删除我插入的 EN+Keywords 四行（a-1..a+2），保留分类号/简介两行移至原英摘 Keywords 之后
del lines[a-1:a+3]
# 此时原英摘 Keywords 行位置：找最后一个 **Keywords**: digital humanities
b = max(i for i, l in enumerate(lines) if l.startswith('**Keywords**: digital humanities'))
lines[b+1:b+1] = ['', zz, '', zz2]
t = '\n'.join(lines)
# 英摘唯一性断言
assert t.count('**Abstract**') == 1, t.count('**Abstract**')
open(p, 'w', encoding='utf-8', newline='').write(t)
print('OK DHR 去重（Abstract 唯一化）')
apply(p, C100)

# ---- B 轨仪表盘措辞 ----
B = [('仪表盘措辞', '把古典文学做成数据可视化，常得到一块仪表盘：', '把古典文学做成数据可视化，很容易做成一块仪表盘：', 1)]
apply(os.path.join(ROOT, '05-投稿', '装饰投稿', '设计方向-装饰投稿版.md'), B)
apply(os.path.join(ROOT, '05-投稿', '装饰投稿', '设计方向-匿名稿.md'), B)

# ---- 文献清单：HALLMARK 建账 + Resnik DOI 注记 ----
p = os.path.join(ROOT, '06-文献', '00-文献清单.md')
t = open(p, encoding='utf-8', newline='').read()
pairs = [
 ('HALLMARK 建账',
  '| 周月. 中国神话元素在新中式家具设计中的应用研究. 《设计》2026 年第 39 卷第 12 期，第 1-5 页 | 知网（2026-10-08 CNKI 检索核验） |',
  '| 周月. 中国神话元素在新中式家具设计中的应用研究. 《设计》2026 年第 39 卷第 12 期，第 1-5 页 | 知网（2026-10-08 CNKI 检索核验） |\n'
  '| Reizinger P, Brendel W. HALLMARK: Diagnosing Three Failure Modes in LLM Citation Verifiers. arXiv:2607.18360（2026） | arXiv（2026-10-08 摘要核验：**2,526 BibTeX entries**·14 hallucination types·three difficulty tiers·结论=可部署性取决于 FPR 而非 recall——第六轮审读方「2,525」系仓库/论文口径差，引用论文数为正确实践；可验证性方向稿注⑧引·未存 PDF） |'),
 ('Resnik DOI 注记',
  '| `2026_Resnik-Hosseini_幻觉引用可构成研究不端_AccountabilityInResearch.pdf` | Resnik, D. B. & Hosseini, M. Hallucinated citations produced b',
  '| `2026_Resnik-Hosseini_幻觉引用可构成研究不端_AccountabilityInResearch.pdf` | Resnik, D. B. & Hosseini, M. Hallucinated citations produced b'),
]
# Resnik 行追加 DOI（定位该行行尾）
lines = t.split('\n')
for i, l in enumerate(lines):
    if l.startswith('| `2026_Resnik-Hosseini_') and 'DOI' not in l:
        lines[i] = l.rstrip()[:-1] + ' · DOI: 10.1080/08989621.2026.2645390（2026-10-08 Crossref 复核✓） |'
        print('Resnik DOI 注记 OK')
        break
t = '\n'.join(lines)
for tag, old, new, cnt in pairs[1:1]:
    pass
open(p, 'w', encoding='utf-8', newline='').write(t)
# HALLMARK 行插入（在周月行后）
t = open(p, encoding='utf-8', newline='').read()
anchor = '| 周月. 中国神话元素在新中式家具设计中的应用研究. 《设计》2026 年第 39 卷第 12 期，第 1-5 页 | 知网（2026-10-08 CNKI 检索核验） |'
if t.count(anchor) != 1:
    fails.append('清单 周月锚点 ' + str(t.count(anchor)))
else:
    hm = '| Reizinger P, Brendel W. HALLMARK: Diagnosing Three Failure Modes in LLM Citation Verifiers. arXiv:2607.18360（2026） | arXiv（2026-10-08 摘要核验：**2,526 BibTeX entries**·14 hallucination types·three difficulty tiers·结论=可部署性取决于 FPR 而非 recall——第六轮审读方「2,525」系仓库/论文口径差，引用论文数为正确实践；可验证性方向稿注⑧引·未存 PDF） |'
    t = t.replace(anchor, anchor + '\n' + hm)
    open(p, 'w', encoding='utf-8', newline='').write(t)
    print('清单 HALLMARK 建账 OK')

print()
print('FAILS:', fails if fails else '无')
