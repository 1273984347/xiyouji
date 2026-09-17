# scripts/_add_feedback_link.py — W572 D-3：全站页脚反馈入口注入（方案 D-3，234 页全修口径）
# 规则：docs/superpowers/plans/2026-09-09-service-experience-and-agent-ops-plans.md §D-3
# 四类形态分派：
#   A 含 <nav aria-label="页脚导航"> → </nav> 前插入（85 页实测）
#   B 含 <div class="footer-index">  → div 内末尾插入（en 页 58 页实测）
#   C 含 <footer> 但无 A/B 锚点      → 最后一个 </footer> 前插入
#   D 无任何页脚特征                 → </body> 前注一行自包含页脚
# 语言：site/en/ 下 Feedback，其余 反馈。幂等：已含 /issues 链接的页跳过。
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
ISSUES_URL = 'https://github.com/1273984347/xiyouji/issues/new'


def fb(label):
    return f'<a href="{ISSUES_URL}" rel="noopener">{label}</a>'


counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
skipped = []
failures = []

pages = sorted(glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True))
for p in pages:
    rp = os.path.relpath(p, ROOT).replace(os.sep, '/')
    label = 'Feedback' if os.sep + 'en' + os.sep in p or '/en/' in rp else '反馈'
    with open(p, encoding='utf-8', newline='') as f:
        s = f.read()
    if ISSUES_URL in s:
        skipped.append(rp)
        continue
    link = fb(label)
    anchor = s.find('aria-label="页脚导航"')
    if anchor != -1:
        nav_end = s.find('</nav>', anchor)
        if nav_end == -1:
            failures.append((rp, 'A 无 </nav>'))
            continue
        s = s[:nav_end] + '\n            ' + link + s[nav_end:]
        counts['A'] += 1
    elif 'footer-index' in s:
        fi = s.find('footer-index')
        div_end = s.find('</div>', fi)
        if div_end == -1:
            failures.append((rp, 'B 无 </div>'))
            continue
        s = s[:div_end] + ' · ' + link + s[div_end:]
        counts['B'] += 1
    elif '<footer' in s:
        foot_end = s.rfind('</footer>')
        if foot_end == -1:
            failures.append((rp, 'C 无 </footer>'))
            continue
        s = s[:foot_end] + '\n<div style="margin-top:8px">' + link + '</div>' + s[foot_end:]
        counts['C'] += 1
    elif '</body>' in s:
        body_end = s.rfind('</body>')
        s = s[:body_end] + '\n<div style="padding:16px 8px;text-align:center">' + link + '</div>\n' + s[body_end:]
        counts['D'] += 1
    else:
        failures.append((rp, '无 </body>'))
        continue
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)

total = sum(counts.values())
print(f'injected A={counts["A"]} B={counts["B"]} C={counts["C"]} D={counts["D"]} total={total}/{len(pages)}')
print(f'skipped_already_has={len(skipped)} {skipped[:3]}')
print(f'failures={len(failures)}')
for item in failures:
    print('FAIL:', item)
