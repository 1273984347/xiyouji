#!/usr/bin/env python3
"""_tmpe_groups.py — 一次性：按切片索引构建 judge 视觉审查分组。

桌面：全部页面（有切片用切片，否则用整页图）。
移动：site 根 9 页 + 采集期有 pageerror/console/layout/external 告警的页面。
每组 ≤12 张图，整页不跨组。
输出：tmpe/report/judge-groups.json
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMPE = os.path.join(ROOT, 'tmpe')
REPORT_DIR = os.path.join(TMPE, 'report')

MAX_IMAGES = 12


def main():
    with open(os.path.join(REPORT_DIR, 'manifest.json'), encoding='utf-8') as f:
        manifest = json.load(f)
    with open(os.path.join(REPORT_DIR, 'slice-index.json'), encoding='utf-8') as f:
        index = json.load(f)

    by_vp = {'desktop': [], 'mobile': []}
    for r in manifest['results']:
        if r.get('error'):
            continue
        vp = r['viewport']
        key = f"{vp}|{r['rel']}"
        info = index.get(key, {})
        if info.get('slices'):
            images = info['slices']
        else:
            images = [r['png']]
        if vp == 'mobile':
            is_root = '/' not in r['rel']
            flagged = bool(r.get('pageErrors') or r.get('consoleErrors') or r.get('layoutIssues') or r.get('externalRequests'))
            if not (is_root or flagged):
                continue
        by_vp[vp].append({'page': r['rel'], 'viewport': vp, 'images': images})

    groups = []
    for kind in ('desktop', 'mobile'):
        cur, cur_n = [], 0
        for item in by_vp[kind]:
            n = len(item['images'])
            if cur and cur_n + n > MAX_IMAGES:
                groups.append({'kind': kind, 'items': cur, 'images': cur_n})
                cur, cur_n = [], 0
            cur.append(item)
            cur_n += n
        if cur:
            groups.append({'kind': kind, 'items': cur, 'images': cur_n})

    with open(os.path.join(REPORT_DIR, 'judge-groups.json'), 'w', encoding='utf-8') as f:
        json.dump(groups, f, ensure_ascii=False, indent=2)

    d = [g for g in groups if g['kind'] == 'desktop']
    m = [g for g in groups if g['kind'] == 'mobile']
    d_pages = sum(len(g['items']) for g in d)
    m_pages = sum(len(g['items']) for g in m)
    print(f"desktop groups: {len(d)} ({d_pages} pages, {sum(g['images'] for g in d)} images)")
    print(f"mobile  groups: {len(m)} ({m_pages} pages, {sum(g['images'] for g in m)} images)")


if __name__ == '__main__':
    main()
