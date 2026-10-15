# scripts/_collapse_index_footer.py — W572 D-4：首页页脚版本串收敛（方案 D-4）
# index.html footer-meta（40 个版本号 + 46 个 W 号的工程日志）收敛为「链首 1 组 + 完整更新日志链接」。
# 设计约束：保留「vX.Y.Z · W###」形态，兼容 bump_version.py:150-151 的替换正则（F32，禁改门禁脚本）。
# en/index.html 按条件处理（版本 token > 3 才收敛）。
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW_META = (
    '<div class="footer-meta">2026 · MIT License · 持续更新中 · '
    'v2.3.172 · W572 站点可达性与信任信号（方案D） · '
    '<a href="https://github.com/1273984347/xiyouji/blob/main/CHANGELOG.md" rel="noopener">完整更新日志</a>'
    '</div>'
)

for name, threshold in (('site/index.html', 3), ('site/en/index.html', 3)):
    p = os.path.join(ROOT, name)
    with open(p, encoding='utf-8', newline='') as f:
        s = f.read()
    tokens = re.findall(r'v\d+\.\d+\.\d+', s)
    m = re.findall(r'<div class="footer-meta">[^<]*</div>', s, re.S)
    print(f'{name}: version_tokens={len(tokens)} footer_meta_divs={len(m)}')
    if len(tokens) <= threshold:
        print(f'  -> 跳过（version_tokens={len(tokens)} <= {threshold}，无长链）')
        continue
    if len(m) != 1:
        print(f'  -> FAIL: footer-meta div 数量异常（{len(m)}），不动作')
        continue
    s = s.replace(m[0], NEW_META, 1)
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)
    print('  -> 已收敛（1 组版本链 + 完整更新日志链接）')
