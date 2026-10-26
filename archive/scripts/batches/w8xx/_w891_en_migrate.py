#!/usr/bin/env python3
"""_w891_en_migrate.py — W891 en 四渠收尾迁移（A 容器 + nav-back 样式统一·一次性件）。

**A 渠（v4 §3.3 裁决 3）**：
1. `max-width: 1320px` → `max-width: var(--container-wide)`（值保留·仅页级 CSS，跳过 INLINED 块）；
2. `max-width: 1024px / 1280px`（容器用法·非 @media 断点）→ `var(--container-content)`（1120·
   v4 §3.3 归并 11 页·值变属裁决内）；@media 断点先以占位符保护、替换后还原。
3. 768/640/480/375/280/400/220 一律不动（断点与小固定宽·非容器档位）。

**nav-back 样式统一（W887 记账的候选）**：49 页同款 `.nav-back`（实底 var(--accent) + 白字）
→ 文字态链接：背景 transparent·字 `--accent-text`（落 bg 4.5:1·白名单「朱砂文字」内）·
hover `--accent-tint` 取代 `--rebel` 实底；padding/圆角保留（保持可点击形状）。

**D 渠**：本脚本不处理——值保留令牌化由 `_w862_tokenize_spacing.py` 对 138 页整批跑（3,149 处）。

用法：py -3 scripts/_w891_en_migrate.py [--dry]
"""

import os
import re
import sys

EN = "site/en"
INLINED_OPEN = "<!-- INLINED CSS"

# @media 断点占位保护
_MQ = re.compile(r"(@media[^{]*max-width:\s*)(\d+)(px)")
_CONTAINER = re.compile(r"max-width:\s*(\d+)px")
_NAV_BLOCK = re.compile(r"\.nav-back\s*\{([^}]*)\}")
_NAV_HOVER = re.compile(r"\.nav-back:hover\s*\{([^}]*)\}")


def split_inlined(s):
    """返回 (头, 内联块, 尾)——内联块范围 [INLINED 标记, 其后第一个 </style>]。"""
    st = s.find(INLINED_OPEN)
    if st < 0:
        return s, "", ""
    end = s.find("</style>", st)
    if end < 0:
        return s, "", ""
    return s[:st], s[st:end], s[end:]


def migrate_container(head, tail):
    """A 渠：跳 INLINED·保护 @media·1320→wide / 1024·1280→content。返回 (head, tail, n1, n2)。"""
    n1 = n2 = 0

    def do(text):
        nonlocal n1, n2
        # 1) 保护 @media 断点
        mq_saved = []

        def protect(m):
            mq_saved.append(m.group(0))
            return "\x00MQ%d\x00" % (len(mq_saved) - 1)

        text = _MQ.sub(protect, text)
        # 2) 容器替换
        def repl(m):
            nonlocal n1, n2
            v = m.group(1)
            if v == "1320":
                n1 += 1
                return "max-width: var(--container-wide)"
            if v in ("1024", "1280"):
                n2 += 1
                return "max-width: var(--container-content)"
            return m.group(0)

        text = _CONTAINER.sub(repl, text)
        # 3) 还原断点
        for i, saved in enumerate(mq_saved):
            text = text.replace("\x00MQ%d\x00" % i, saved)
        return text

    return do(head), do(tail), n1, n2


def migrate_nav(s):
    """nav-back：实底→文字态。返回 (s, changed)。"""
    changed = False

    def block(m):
        nonlocal changed
        b = m.group(1)
        nb = re.sub(r"background:\s*var\(--accent\)\s*;", "background: transparent;", b)
        nb = re.sub(r"(?<!-)\bcolor:\s*var\(--paper-warm\)\s*;", "color: var(--accent-text);", nb)
        if nb != b:
            changed = True
        return ".nav-back {" + nb + "}"

    s = _NAV_BLOCK.sub(block, s)

    def hover(m):
        nonlocal changed
        b = m.group(1)
        nb = re.sub(r"background:\s*var\(--rebel\)\s*;", "background: var(--accent-tint);", b)
        if nb != b:
            changed = True
        return ".nav-back:hover {" + nb + "}"

    return _NAV_HOVER.sub(hover, s), changed


def main(argv):
    dry = "--dry" in argv
    n_pages = 0
    t1 = t2 = t3 = 0
    for fn in sorted(os.listdir(EN)):
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(EN, fn)
        s = open(fp, encoding="utf-8").read()
        head, mid, tail = split_inlined(s)
        head2, tail2, n1, n2 = migrate_container(head, tail)
        s2 = head2 + mid + tail2
        s2, c3 = migrate_nav(s2)
        if n1 or n2 or c3:
            n_pages += 1
            t1 += n1
            t2 += n2
            t3 += 1 if c3 else 0
            if not dry:
                with open(fp, "w", encoding="utf-8", newline="") as f:
                    f.write(s2)
    print("[%s] en %d 页：1320→wide %d 处 · 1024/1280→content %d 处 · nav-back 文字态 %d 页"
          % ("DRY" if dry else "APPLY", n_pages, t1, t2, t3))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
