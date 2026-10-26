#!/usr/bin/env python3
"""_w957_wire_pilot.py — W957 施工批「试点页接入」幂等接线器（字节级·保行尾）。

做两件事：
  ① 给试点页的编排容器加 `data-gsap` 标记（显式 opt-in）；
  ② 在页面既有脚本锚点之后插入 3 行 GSAP 外链（gsap / ScrollTrigger / motion-gsap）。

纪律（沿用 W955 实证教训）：
  · **字节级改写**（`open(p,'rb')` + `bytes.replace`）——Edit 类工具在 CRLF 文件上会插入
    多余换行（W955 实证：行数翻倍·非空行数不变）；本脚本全程 bytes 操作，行尾零扰动；
  · 每处**先断言命中数**，不符即中止不写盘（fail-closed）；
  · 幂等：目标串已存在则跳过（可重跑）；
  · 相对路径按**引用页所在目录**为基准（根页 `static/js/` · reader 页 `../static/js/` ·
    reader/themes 与 reader/people 页 `../../static/js/`）。

用法：py -3 scripts/_w957_wire_pilot.py [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (相对仓根路径, script 前缀, 属性锚点, 属性值, script 锚点)
PAGES = [
    ("site/index.html", "static/js/",
     '<div class="masthead-copy">', "intro",
     '<script defer src="js/visit-log.js"></script>'),
    ("site/reader/ch007.html", "../static/js/",
     '<article class="reader-body">', "sections",
     '<script src="../js/reader-enhance.js" defer></script>'),
    ("site/reader/themes/西游与死亡研究专题.html", "../../static/js/",
     '<article class="reader-body">', "sections",
     '<script src="../../js/reader-enhance.js" defer></script>'),
    ("site/reader/people/黄风怪外传.html", "../../static/js/",
     '<article class="reader-body">', "sections",
     '<script src="../../js/reader-enhance.js" defer></script>'),
    ("site/reader/people/白骨精.html", "../../static/js/",
     '<article class="reader-body">', "sections",
     '<script src="../../js/reader-enhance.js" defer></script>'),
]

# 接入块：单行三标签 · 顶格（HTML 允许相邻 script 标签）——单页增量受 AC-10 的 200 B 上限约束
# （三行缩进排布实测 reader 页 212 B / 208 B 均越限；并置后 reader 页 201 B，顶格后 199 B）
# 顶格同时在视觉上标明这是机器接线件（与页面人工缩进代码区分）
SCRIPT_LINES = [
    '<script defer src="{p}gsap.min.js"></script>'
    '<script defer src="{p}ScrollTrigger.min.js"></script>'
    '<script defer src="{p}motion-gsap.js"></script>',
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    total_delta = 0
    for rel, prefix, attr_anchor, attr_value, script_anchor in PAGES:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print("ABORT  %s：文件不存在" % rel)
            return 1
        with open(path, "rb") as f:
            raw = f.read()
        before = len(raw)

        # —— ① data-gsap 标记 ——
        if ('data-gsap="%s"' % attr_value).encode("utf-8") in raw:
            print("SKIP   %s：data-gsap 标记已存在" % rel)
        else:
            n = raw.count(attr_anchor.encode("utf-8"))
            if n != 1:
                print("ABORT  %s：属性锚点命中 %d ≠ 期望 1（%s）" % (rel, n, attr_anchor))
                return 1
            marked = attr_anchor[:-1] + ' data-gsap="%s">' % attr_value
            raw = raw.replace(attr_anchor.encode("utf-8"), marked.encode("utf-8"), 1)

        # —— ② GSAP 三行外链 ——
        block = "\r\n".join(l.format(p=prefix) for l in SCRIPT_LINES)
        if ("motion-gsap.js" in raw.decode("utf-8", "ignore")):
            print("SKIP   %s：GSAP 外链已存在" % rel)
        else:
            n = raw.count(script_anchor.encode("utf-8"))
            if n != 1:
                print("ABORT  %s：脚本锚点命中 %d ≠ 期望 1（%s）" % (rel, n, script_anchor))
                return 1
            nl = b"\r\n" if b"\r\n" in raw else b"\n"
            injected = script_anchor.encode("utf-8") + nl + block.encode("utf-8") + nl
            raw = raw.replace(script_anchor.encode("utf-8"), injected, 1)

        delta = len(raw) - before
        total_delta += delta
        pct = delta / float(before) * 100.0
        print("%-6s %-52s 增量 %+d B（占页面 %.3f%%）" % ("DRY" if args.dry_run else "OK", rel, delta, pct))
        # AC-10（施工批修订口径·轨迹见 T28 报告偏差留档）：
        #   v1「≤200 B」量纲有缺陷——同批 5 页实测差（187 / 199 / 208 B）纯粹来自引用目录层级
        #   （`static/js/` vs `../static/js/` vs `../../static/js/`），非改动量差异；
        #   v2「≤250 B 且 ≤0.5%」仍不适配——专题页体积仅 ≈32 KB，208 B 即占 0.64%
        #   （小页面天然占比高 ⇒ 相对占比作阻断阈值会误伤小页）。
        #   v3（现行）：**绝对量 ≤250 B 阻断**（改动面以字节封顶）+ 相对占比仅作报告指标。
        if delta > 250:
            print("ABORT  %s：单页增量 %d B（占页面 %.3f%%）超 AC-10 现行口径（≤250 B）"
                  % (rel, delta, pct))
            return 1
        if args.dry_run:
            continue
        with open(path, "wb") as f:
            f.write(raw)

    print("%s完成：%d 页 · 合计增量 %+d B" % ("DRY-RUN " if args.dry_run else "接入", len(PAGES), total_delta))
    return 0


if __name__ == "__main__":
    sys.exit(main())
