#!/usr/bin/env python3
"""W677 批次五机械修复（WP-5.1–5.4·ZH+EN 12 文件面）。

每处改动带出现次数/结构断言，任一失配即整体中止不落盘。
EN social-media duration 双调用已净（镜像无此缺陷·留档）；其余 EN 镜像同病对称修复。
"""
import io
import re
import sys

FILES = {}


def load(f):
    t = io.open(f, "r", encoding="utf-8", newline="").read()
    FILES[f] = t
    return t


def nl_of(t):
    return "\r\n" if "\r\n" in t else "\n"


def lines_of(t):
    return t.split(nl_of(t))


def find_blocks(t, start_pat, end_strip="})"):
    """返回 [start_idx, end_idx]（0-based 闭区间）：起点行匹配 start_pat，终点行为首个 strip==end_strip。"""
    L = lines_of(t)
    for i, ln in enumerate(L):
        if re.search(start_pat, ln):
            j = i
            while j < len(L) and L[j].strip() != end_strip:
                j += 1
            assert j < len(L), "未找到终点 %r（自 %d 行）" % (end_strip, i + 1)
            return i, j
    raise AssertionError("未找到起点 %r" % start_pat)


def drop_idx(lines, a, b):
    return lines[:a] + lines[b + 1:]


def apply_str(f, old, new, n):
    t = FILES[f]
    _nl = nl_of(t)
    old = old.replace("\n", _nl)
    new = new.replace("\n", _nl)
    c = t.count(old)
    assert c == n, "%s: %r 期望 %d 实得 %d" % (f, old[:50], n, c)
    FILES[f] = t.replace(old, new)


def main():
    dry = "--dry" in sys.argv

    # ---------- A. relationships：删陈旧 cooccurrence_timeline 键（份2==生成器真源已验） ----------
    for f in ["site/data/relationships.html", "site/en/relationships.html"]:
        load(f)
        L = lines_of(FILES[f])
        idxs = [i for i, ln in enumerate(L) if "cooccurrence_timeline: {" in ln]
        assert len(idxs) == 2, f + " 键数异常"
        assert L[idxs[0] + 1].strip() == ",", f + " 键间非逗号行"
        FILES[f] = nl_of(FILES[f]).join(drop_idx(L, idxs[0], idxs[0] + 1))
        assert FILES[f].count("cooccurrence_timeline: {") == 1, f + " 删除后仍多键"

    # ---------- B. tag-cloud：①ID 失配 ②死函数 ③点击即跳前的死渲染 ----------
    for f in ["site/data/tag-cloud.html", "site/en/tag-cloud.html"]:
        load(f)
        apply_str(f, 'getElementById("tag-search")', 'getElementById("search-input")', 1)
        a, b = find_blocks(FILES[f], r"function setupTouchNav\(\)", "}")
        assert a + 1 < b, f + " setupTouchNav 体异常"
        L = drop_idx(lines_of(FILES[f]), a, b)
        calls = [i for i, ln in enumerate(L) if ln.strip() == "setupTouchNav();"]
        assert len(calls) == 1, f + " setupTouchNav 调用数异常"
        FILES[f] = nl_of(FILES[f]).join(drop_idx(L, calls[0], calls[0]))
        apply_str(f, "        renderRecommendations(d);\n", "", 1)

    # ---------- C. visual-art：keyframes 移静态块 + 删 JS 追加 ----------
    for f in ["site/data/visual-art.html", "site/en/visual-art.html"]:
        load(f)
        t = FILES[f]
        halo = t.index('<style id="audit-halo">')
        close = t.rfind("</style>", 0, halo)
        assert close != -1, f + " 主样式块闭合未找到"
        kf = "        @keyframes heart-breath { 0%, 100% { fill-opacity: 0; } 50% { fill-opacity: 0.35; } }" + nl_of(t)
        FILES[f] = t[:close] + kf + t[close:]
        a, b = find_blocks(FILES[f], r"// 添加 keyframes 心形呼吸动画", "document.head.appendChild(styleEl);")
        FILES[f] = nl_of(FILES[f]).join(drop_idx(lines_of(FILES[f]), a, b))

    # ---------- D. timeline：load 启动改 DOMContentLoaded + 定位父改 .tl-wrap ----------
    for f in ["site/data/timeline.html", "site/en/timeline.html"]:
        load(f)
        apply_str(f, "window.addEventListener('load', main);",
                  "window.addEventListener('DOMContentLoaded', main);", 1)
        apply_str(f, "getElementById('timeline-section')", "querySelector('.tl-wrap')", 1)

    # ---------- E. text-search：动态注入补 onerror 兜底 ----------
    load("site/data/text-search.html")
    apply_str("site/data/text-search.html",
              "      s.src = '../static/js/text-search-app.js';\n",
              "      s.src = '../static/js/text-search-app.js';\n"
              "      s.onerror = function () { console.warn('[text-search] text-search-app.js 加载失败，站内检索功能不可用'); };\n", 1)
    load("site/en/text-search.html")
    apply_str("site/en/text-search.html",
              "      s.src = '../static/js/text-search-app.js';\n",
              "      s.src = '../static/js/text-search-app.js';\n"
              "      s.onerror = function () { console.warn('[text-search] text-search-app.js failed to load; search unavailable'); };\n", 1)

    # ---------- F. theological：header 全局选择器加语义类 ----------
    for f in ["site/data/theological-intervention-network.html", "site/en/theological-intervention-network.html"]:
        load(f)
        t = FILES[f]
        m = re.search(r"(^)header \{", t, re.M)
        assert m, f + " header{ 未命中"
        FILES[f] = t[:m.start()] + ".page-head {" + t[m.end():]
        apply_str(f, "<header>", '<header class="page-head">', 1)

    # ---------- G. six-senses：.node-label 删 fill（JS attr 分型色复活） ----------
    for f in ["site/data/six-senses-narratology-network.html", "site/en/six-senses-narratology-network.html"]:
        load(f)
        apply_str(f, ".node-label { font-size: 11px; fill: var(--ink); pointer-events: none; }",
                  ".node-label { font-size: 11px; pointer-events: none; }", 1)

    # ---------- H. social-media：徽章对比度 + duration 双调用 + typical_posts 渲染 ----------
    for f, n_e9, sample in [("site/data/social-media.html", 6, "代表性发帖："),
                            ("site/en/social-media.html", 6, "Sample post: ")]:
        load(f)
        apply_str(f, "#e9b885", "#7a571b", n_e9)
        t = FILES[f]
        m = re.search(r"^(\s*)\.pc-bio \{", t, re.M)
        assert m, f + " .pc-bio 未命中"
        indent = m.group(1)
        rule = (indent + ".pc-sample {\n"
                + indent + "    font-size: 0.78rem;\n"
                + indent + "    color: var(--ink-soft);\n"
                + indent + "    line-height: 1.5;\n"
                + indent + "    margin: 6px 0 0;\n"
                + indent + "}\n")
        FILES[f] = t[:m.start()] + rule + t[m.start():]
        nl = nl_of(FILES[f])
        bio_old = "\n".join(['      card.append("div").attr("class", "pc-bio").text(p.bio);', ""])
        bio_new = "\n".join([
            '      card.append("div").attr("class", "pc-bio").text(p.bio);',
            "",
            "      if (p.typical_posts && p.typical_posts.length) {",
            '          card.append("div").attr("class", "pc-sample").text(' + repr(sample) + ' + p.typical_posts[0]);',
            "      }",
            ""])
        apply_str(f, bio_old, bio_new, 1)
    # duration 双调用仅 ZH 有病（EN 已净·镜像无此缺陷留档）
    _sm = "site/data/social-media.html"
    _t = FILES[_sm]
    _pat1 = re.compile(r"\.duration\(MOYUN_RM\?0:250\)(\r?\n\s*)\.delay\(200 \+ idx \* 120\)")
    _c1 = len(_pat1.findall(_t))
    assert _c1 == 1, "sm duration 对① 命中 %d" % _c1
    _t = _pat1.sub(r"\1.delay(200 + idx * 120)", _t, count=1)
    _pat2 = re.compile(r"\.transition\(\)\.duration\(MOYUN_RM\?0:250\)(\r?\n\s*)\.delay\(500 \+ idx \* 120\)")
    _c2 = len(_pat2.findall(_t))
    assert _c2 == 1, "sm duration 对② 命中 %d" % _c2
    _t = _pat2.sub(r".transition()\1.delay(500 + idx * 120)", _t, count=1)
    _pat3 = re.compile(r"\.duration\(MOYUN_RM\?0:250\)(\r?\n\s*)\.delay\(i \* 100\)\.duration\(MOYUN_RM\?0:600\)")
    _c3 = len(_pat3.findall(_t))
    assert _c3 == 1, "sm duration 对③ 命中 %d" % _c3
    _t = _pat3.sub(r"\1.delay(i * 100).duration(MOYUN_RM?0:600)", _t, count=1)
    FILES[_sm] = _t
    apply_str("site/data/social-media.html",
              ".duration(MOYUN_RM?0:250).delay(i * 100 + 600).duration(MOYUN_RM?0:400)",
              ".delay(i * 100 + 600).duration(MOYUN_RM?0:400)", 1)
    apply_str("site/data/social-media.html",
              ".duration(MOYUN_RM?0:250).delay(i * 100 + 700).duration(MOYUN_RM?0:400)",
              ".delay(i * 100 + 700).duration(MOYUN_RM?0:400)", 1)

    # ---------- I. text-evolution：tickValues 改域内动态生成 ----------
    for f in ["site/data/text-evolution.html", "site/en/text-evolution.html"]:
        load(f)
        apply_str(f, ".tickValues([1200, 1300, 1400, 1500, 1600, 1700, 1800])",
                  ".tickValues(d3.ticks(y.domain()[0], y.domain()[1], 7))", 1)

    # ---------- J. workplace：viewBox 首调死代码删除 ----------
    for f in ["site/data/workplace.html", "site/en/workplace.html"]:
        load(f)
        nl = nl_of(FILES[f])
        old = nl.join(["const h = 260;", "        svg.attr(\"viewBox\", `0 0 ${w} ${h}`);", ""])
        c = FILES[f].count(old)
        assert c == 1, f + " viewBox 首调上下文命中 %d" % c
        FILES[f] = FILES[f].replace(old, nl.join(["const h = 260;", ""]))

    # ---------- K. underworld：同人物串联死循环删除（数据 actor 全唯一已验） ----------
    for f, cpat in [("site/data/underworld-power-network.html", r"// 连线（同一人物事件串联）"),
                    ("site/en/underworld-power-network.html", r"// Connecting lines")]:
        load(f)
        a, b = find_blocks(FILES[f], cpat, "});")
        FILES[f] = nl_of(FILES[f]).join(drop_idx(lines_of(FILES[f]), a, b))

    # ---------- L. risk-project：里程碑标签侧别数学修正 ----------
    for f in ["site/data/risk-project.html", "site/en/risk-project.html"]:
        load(f)
        apply_str(f, "upDown * (r + 4) * (upDown < 0 ? -1 : 1)", "upDown * (r + 4)", 1)

    # ---------- 落盘与自检 ----------
    if dry:
        print("[DRY] 全部断言通过，共 %d 文件面" % len(FILES))
        return 0
    for f, t in FILES.items():
        with io.open(f, "w", encoding="utf-8", newline="") as fh:
            fh.write(t)
    checks = [
        ("site/data/relationships.html", "cooccurrence_timeline: {", 1),
        ("site/en/relationships.html", "cooccurrence_timeline: {", 1),
        ("site/data/tag-cloud.html", "tag-search", 0),
        ("site/data/tag-cloud.html", "setupTouchNav", 0),
        ("site/en/tag-cloud.html", "setupTouchNav", 0),
        ("site/data/visual-art.html", "appendChild(styleEl)", 0),
        ("site/en/visual-art.html", "appendChild(styleEl)", 0),
        ("site/data/timeline.html", "getElementById('timeline-section')", 0),
        ("site/data/text-search.html", "onerror", 1),
        ("site/en/text-search.html", "onerror", 1),
        ("site/data/theological-intervention-network.html", "^header {", 0),
        ("site/data/six-senses-narratology-network.html", "fill: var(--ink); pointer-events", 0),
        ("site/data/social-media.html", "#e9b885", 0),
        ("site/en/social-media.html", "#e9b885", 0),
        ("site/data/social-media.html", ".duration(MOYUN_RM?0:250).delay", 0),
        ("site/data/text-evolution.html", "tickValues([1200", 0),
        ("site/data/underworld-power-network.html", "同一人物事件串联", 0),
        ("site/en/underworld-power-network.html", "Connecting lines", 0),
        ("site/data/risk-project.html", "upDown < 0 ? -1 : 1", 0),
    ]
    bad = 0
    for f, pat, want in checks:
        c = FILES[f].count(pat)
        flag = "" if c == want else "  <-- FAIL"
        if c != want:
            bad += 1
        print("%s %r = %d（期望 %d）%s" % (f.split("/")[-1], pat[:34], c, want, flag))
    print("OK 落盘 %d 文件，自检失败 %d" % (len(FILES), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
