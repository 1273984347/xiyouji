# -*- coding: utf-8 -*-
"""W724 一次性脚本：四页页脚链重建——从损坏链按「token 首现段」打捞原始文本（每批首次插入时段=完整原始），
保留最近 11 条（级联插新批后=12+尾注）+尾注；历史权威在 CHANGELOG 零信息损失。用后即弃。"""
import io
import re

PAGES = [
    ("site/index.html", 'class="footer-meta">', True),
    ("site/data/cross-time-danmaku.html", 'class="footer-meta">', True),
    ("site/data/tag-cloud.html", 'class="footer-meta">', True),
    ("site/dukou-engine.html", "<footer>", False),
]
W = re.compile(r"W(\d{3})")
KEEP = 11

for p, anchor, quoted in PAGES:
    s = io.open(p, encoding="utf-8", newline="").read()
    if quoted:
        m = re.search(re.escape(anchor) + r"([^<]*)<", s)
    else:
        m = re.search(re.escape(anchor) + r"([^<]*)<", s)
    assert m, p + " 未命中链节点"
    node = m.group(1)
    parts = node.split(" · ")
    head, segs, vbuf = [], [], ""
    for seg in parts:
        w = W.search(seg)
        if w:
            key = w.group(1)
            text = (vbuf + seg) if vbuf else seg
            vbuf = ""
            if all(k != key for k, _ in segs):
                segs.append((key, text))
        elif re.fullmatch(r"v[\d.]+", seg.strip()):
            vbuf = seg.strip() + " · "
        elif not segs:
            head.append(seg)
    assert len(segs) >= 5, p + " 首现段不足: %d" % len(segs)
    kept = [t for _, t in segs[: min(KEEP, len(segs))]]
    new_node = " · ".join(head + kept + ["…更早批次详见 CHANGELOG.md"])
    s2 = s[: m.start(1)] + new_node + s[m.end(1):]
    io.open(p, "w", encoding="utf-8", newline="").write(s2)
    toks = W.findall(new_node)
    assert len(toks) == len(set(toks)), p + " 重建后仍有重复"
    print("OK", p.split("/")[-1], "→", len(new_node), "字符·", len(toks), "条·头:", kept[0][:24], "尾:", kept[-1][:24])
