"""check_story_timeline_sync.py — 故事内时间线双源同步校验（W694 六轮外审 P1-4 落地）。

比对 scripts/F_时间/timeline.py 的 KEY_EVENTS 与 site/data/story-timeline.html 的
EMBEDDED_DATA.timeline 逐条（chapter/event/characters/顺序）一致，并校验 phase
区间映射与 chapter 匹配。任一失配 = FAIL（防人工同步漂移——当前同步为人工，
本脚本即机器防线；挂载 verify 为候批事项）。

用法：
    python scripts/check_story_timeline_sync.py             # 校验
    python scripts/check_story_timeline_sync.py --self-test # 负样本自检
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = ROOT / "scripts" / "F_时间" / "timeline.py"
HTML = ROOT / "site" / "data" / "story-timeline.html"

PHASE_RANGES = [("p1", 1, 7), ("p2", 8, 12), ("p3", 13, 22), ("p4", 23, 97), ("p5", 98, 100)]

RE_PY = re.compile(r'\{"chapter": (\d+), "event": "([^"]+)", "characters": \[([^\]]*)\]\}')
RE_HTML = re.compile(r"\{ chapter: (\d+),\s+phase: '(\w+)', event: '([^']+)', characters: \[([^\]]*)\] \}")
RE_ITEM = re.compile(r'"([^"]+)"|\x27([^\x27]+)\x27')


def phase_of(ch):
    for key, lo, hi in PHASE_RANGES:
        if lo <= ch <= hi:
            return key
    return None


def parse_py():
    src = PY.read_text(encoding="utf-8")
    m = re.search(r"KEY_EVENTS = \[(.*?)\n\]", src, re.S)
    assert m, "timeline.py 未找到 KEY_EVENTS 块"
    ast.literal_eval("[" + m.group(1).strip().rstrip(",") + "]")  # 字面量合法性
    out = []
    for ch, ev, chars in RE_PY.findall(m.group(1)):
        out.append((int(ch), ev, tuple(RE_ITEM.findall(chars) and [a or b for a, b in RE_ITEM.findall(chars)])))
    return out


def parse_html():
    src = HTML.read_text(encoding="utf-8")
    out = []
    for ch, phase, ev, chars in RE_HTML.findall(src):
        out.append((int(ch), ev, tuple(a or b for a, b in RE_ITEM.findall(chars)), phase))
    return out


def compare(py_events, html_events):
    issues = []
    if len(py_events) != len(html_events):
        issues.append("条数不一致：py=%d html=%d" % (len(py_events), len(html_events)))
        return issues
    for i, (p, h) in enumerate(zip(py_events, html_events, strict=False)):
        ch_p, ev_p, chars_p = p
        ch_h, ev_h, chars_h, phase = h
        if (ch_p, ev_p, chars_p) != (ch_h, ev_h, chars_h):
            issues.append("第 %d 条不一致：py=%s html=%s" % (i + 1, (ch_p, ev_p, list(chars_p)), (ch_h, ev_h, list(chars_h))))
        if phase != phase_of(ch_h):
            issues.append("第 %d 条 phase=%s 与 chapter=%d 区间不符" % (i + 1, phase, ch_h))
    return issues


def main():
    if "--self-test" in sys.argv:
        py_events = parse_py()
        html_events = parse_html()
        assert compare(py_events, html_events) == [], "正样本应零失配"
        mutated = [(c, e + "X", ch, ph) for c, e, ch, ph in html_events]
        assert compare(py_events, mutated), "事件篡改负样本未被捕获"
        mutated2 = html_events[1:]
        assert compare(py_events, mutated2), "缺条负样本未被捕获"
        mutated3 = [(c, e, ch, "p1" if ph != "p1" else "p9") for c, e, ch, ph in html_events]
        assert compare(py_events, mutated3), "phase 非法负样本未被捕获"
        print("SELF-TEST PASS：正样本零失配 + 篡改/缺条/phase 三类负样本全捕获")
        return 0
    issues = compare(parse_py(), parse_html())
    if issues:
        print("FAIL 故事内时间线双源失配 %d 项：" % len(issues))
        for s in issues[:10]:
            print("  -", s)
        print("---- 第 39 门禁 故事内时间线双源同步：失配 %d 项 ----" % len(issues))
        return 1
    n = len(parse_py())
    print("OK 故事内时间线双源一致（KEY_EVENTS %d 条 == EMBEDDED_DATA %d 条·phase 区间全匹配）" % (n, n))
    print("---- 第 39 门禁 故事内时间线双源同步：KEY_EVENTS %d 条 == EMBEDDED_DATA %d 条 · 失配 0 · phase 区间全匹配 ----" % (n, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
