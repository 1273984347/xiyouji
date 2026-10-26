#!/usr/bin/env python3
"""一次性：A 轨驿递稿《数据核验与复现》审计（2026-09-28）。

只读审计（不改动任何源文件）：逐项核验
docs/S4-学术投稿/01-论文/明清小说方向-投稿版.md（投稿版 + 匿名稿）
的全部量化断言，对照：
- 底本语料行号口径 site/static/js/text-search-app.js（同 scripts/audit/line_check.py）
- 词汇统计口径 dataset/text-search.json（同 scripts/check_citations.py）
- 引文门禁 scripts/check_citations.py（子进程实跑）
- 图表文件 图表/A-图1、A-图2 与可视化页 site/data/customs-pass-route.html（STATIONS 数据）
结果落盘 tmpe/audit_a_track_paper_data.json；控制台输出逐项判定与差异项。
"""
import json
import re
import statistics
import struct
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
S4 = ROOT / "docs" / "S4-学术投稿"
MD = S4 / "01-论文" / "明清小说方向-投稿版.md"
MD_ANON = S4 / "01-论文" / "明清小说方向-匿名稿.md"
TS_JS = ROOT / "site" / "static" / "js" / "text-search-app.js"
TS_JSON = ROOT / "dataset" / "text-search.json"
PAGE = ROOT / "site" / "data" / "customs-pass-route.html"
FIG1 = S4 / "07-图表" / "A-图1-驿路时间线-灰度.png"
FIG2 = S4 / "07-图表" / "A-图2-涉关文地点地理类型分布-灰度.png"
OUT = ROOT / "tmpe" / "audit_a_track_paper_data.json"


# ---------------- 语料加载 ----------------
def load_js_chapters():
    js = TS_JS.read_text(encoding="utf-8")
    out = {}
    for num in range(1, 101):
        pat = re.compile(
            r"num:\s*" + str(num) + r",\s*\n\s*title:\s*\"[^\"]*\",\s*\n\s*fullTitle:\s*\"[^\"]*\",\s*\n\s*text:\s*`([^`]*)`",
            re.DOTALL,
        )
        m = pat.search(js)
        if m:
            out[num] = m.group(1)
    return out


def load_json_chapters():
    d = json.loads(TS_JSON.read_text(encoding="utf-8"))
    return {int(c["num"]): c["text"] for c in d["chapters"]}


def line_of(text, frag):
    idx = text.find(frag)
    if idx < 0:
        return None
    return text.count("\n", 0, idx) + 1


def locate(text, frag):
    """逐级定位：①原始连续命中（exact）→ ②去空白归一后连续命中（normalized·行号经索引映射还原）
    → ③按标点切段的局部命中（fallback·属非连续片段）。②与项目门禁（check_citations）同归一口径。"""
    line = line_of(text, frag)
    if line:
        return line, frag, "exact"
    nf = re.sub(r"\s+", "", frag)
    if nf:
        nt = re.sub(r"\s+", "", text)
        idx = nt.find(nf)
        if idx >= 0:
            cnt, raw = 0, 0
            for i, c in enumerate(text):
                if not c.isspace():
                    if cnt == idx:
                        raw = i
                        break
                    cnt += 1
            return text.count("\n", 0, raw) + 1, frag, "normalized"
    for part in sorted(re.split(r"[，。；、·：]", frag), key=len, reverse=True):
        part = part.strip()
        if len(part) >= 3:
            line = line_of(text, part)
            if line:
                return line, part, "fallback"
    return None, "", "none"


# ---------------- 表格解析 ----------------
def parse_tables(md_text):
    t1, t2, other_lines = [], [], []
    for ln in md_text.splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            other_lines.append(ln)
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) >= 4 and cells[0].startswith("第"):
            m = re.match(r"^第\s*(\d+)(?:\s*[-—]\s*(\d+))?\s*回$", cells[0])
            if not m:
                continue
            row = {
                "chapter": int(m.group(1)),
                "chapter_end": int(m.group(2)) if m.group(2) else None,
                "cells": cells,
            }
            (t1 if len(cells) == 5 else t2).append(row)
        else:
            other_lines.append(ln)
    return t1, t2, "\n".join(other_lines)


def parse_anchor_claims(row, is_t1):
    """从行内锚点单元切出 (chapter, line, snippet) 子声明。

    「NN 回」前缀沿单元内后续分段继承（如表 1 铜台府行：`line 5 … / 97 回 line 31 报官 · line 75 解状递上`
    —— 第三段的 97 回取自第二段前缀）。
    """
    anchor = row["cells"][-1]
    out = []
    current_ch = row["chapter"]
    prev = None
    for part in re.split(r"\s*/\s*|\s*·\s*", anchor):
        part = part.strip()
        m = re.match(r"^(?:(\d+)\s*回\s*)?line\s*(\d+)\s+(.+)$", part)
        if not m:
            # 「·」后接无 line 前缀的纯片段（如表 1 狮驼行「八百里狮驼岭 · 三个魔头」）：
            # 视为同一条锚点的补充片段，沿用上一条声明的回目与行号。
            if prev is not None and part:
                out.append({"chapter": prev["chapter"], "claimed_line": prev["claimed_line"],
                            "snippet": part})
            continue
        if m.group(1):
            current_ch = int(m.group(1))
        prev = {"chapter": current_ch, "claimed_line": int(m.group(2)), "snippet": m.group(3).strip()}
        out.append(prev)
    return out


# 正文锚点（自当前稿逐条摘录；snippet=None 为关键词核验型）
BODY_CLAIMS = [
    ("正文4.1-54回-迎阳驿对话", 54, 13, "请他们都进驿内，正厅坐下，即唤看茶"),
    ("正文4.1-54回-启奏倒换", 54, 13, "进城启奏我王，倒换关文"),
    ("正文4.1-88回-投宿问路", 88, 9, None),
    ("正文4.2-12回-通行宝印", 12, 51, "写了取经文牒，用了通行宝印"),
    ("正文4.2-68回-西邦王位", 68, 3, "朱紫国必是西邦王位，却要倒换关文"),
    ("正文4.2-78回-府州县径过", 78, 3, "若是西邸王位，须要倒换关文；若是府州县，径过"),
    ("正文4.2-46回-用了宝印", 46, 1, "即将关文用了宝印"),
    ("正文4.4-54回-印关文", 54, 73, "今日即印关文，打发他去也"),
    ("正文4.3-97回-报官", 97, 31, "报官"),
    ("正文4.3-97回-坐名告你", 97, 31, "坐名告你"),
    ("正文4.3-97回-投递解状", 97, 67, "投递解状"),
    ("正文5.2-12回-首节点", 12, 51, "写了取经文牒"),
    ("正文5.3-98回-如来阅牒", 98, 29, "将通关文牒奉上，如来一一看了"),
]


def verify_claim(chapters, ch, claimed_line, snippet):
    text = chapters.get(ch, "")
    if snippet is None:
        ls = text.split("\n")
        actual = ls[claimed_line - 1] if 0 <= claimed_line - 1 < len(ls) else ""
        hit_kw = [k for k in ("驿", "馆", "投宿", "进城", "问路", "问老施主", "玉华县") if k in actual]
        return {
            "status": "OK~关键词" if hit_kw else "REVIEW",
            "actual_line": claimed_line,
            "actual_text": actual[:120],
            "hit_keywords": hit_kw,
        }
    line, hit, mode = locate(text, snippet)
    if line is None:
        return {"status": "NOT_FOUND", "actual_line": None, "hit": ""}
    if line == claimed_line:
        st = {"exact": "OK", "normalized": "OK~归一", "fallback": "OK~片段"}[mode]
    else:
        st = "MISMATCH"
    return {"status": st, "actual_line": line, "hit": hit, "mode": mode}


def main():
    md_text = MD.read_text(encoding="utf-8")
    anon_text = MD_ANON.read_text(encoding="utf-8")
    chapters = load_js_chapters()
    jchapters = load_json_chapters()
    assert len(chapters) == 100, "语料解析异常：%d 回" % len(chapters)

    t1, t2, _ = parse_tables(md_text)
    t1a, t2a, _ = parse_tables(anon_text)

    claims = []
    for row in t1:
        for c in parse_anchor_claims(row, True):
            c["source"] = "表1-%d回-%s" % (row["chapter"], row["cells"][1])
            c["result"] = verify_claim(chapters, c["chapter"], c["claimed_line"], c["snippet"])
            claims.append(c)
    for row in t2:
        for c in parse_anchor_claims(row, False):
            c["source"] = "表2-%d回-%s" % (row["chapter"], row["cells"][1])
            c["result"] = verify_claim(chapters, c["chapter"], c["claimed_line"], c["snippet"])
            claims.append(c)
    for src, ch, ln, snip in BODY_CLAIMS:
        claims.append({
            "source": src, "chapter": ch, "claimed_line": ln, "snippet": snip,
            "result": verify_claim(chapters, ch, ln, snip),
        })

    ok = sum(1 for c in claims if c["result"]["status"].startswith("OK"))
    bad = [c for c in claims if not c["result"]["status"].startswith("OK")]
    from collections import Counter as _Counter
    status_tally = dict(_Counter(c["result"]["status"] for c in claims))

    # ---------------- 统计复算 ----------------
    st1 = [r["cells"][2] for r in t1]
    typ = {k: st1.count(k) for k in ("发牒", "验讫", "未验", "波折", "传经不验")}
    ver_nodes = [r["chapter"] for r in t1 if r["cells"][2] == "验讫"]
    ver_split = (sum(1 for c in ver_nodes if c <= 60), sum(1 for c in ver_nodes if c > 60))
    unv_nodes = [r["chapter"] for r in t1 if r["cells"][2] == "未验"]
    starts1 = sorted(r["chapter"] for r in t1)
    starts2 = sorted(r["chapter"] for r in t2)
    all_starts = sorted(starts1 + starts2)
    span = max(starts1) - min(starts1)
    avg30 = round(span / 30, 1)
    avg15 = round(span / 15, 1)
    buckets = [0] * 5
    for x in all_starts:
        buckets[(x - 1) // 20] += 1
    gaps = [starts1[i + 1] - starts1[i] for i in range(len(starts1) - 1)]

    def blank_runs(starts, extra):
        present = set(starts) | set(extra)
        runs, run_start = [], None
        for c in range(12, 101):
            if c in present:
                if run_start is not None:
                    runs.append((run_start, c - 1, c - run_start))
                    run_start = None
            elif run_start is None:
                run_start = c
        if run_start is not None:
            runs.append((run_start, 100, 101 - run_start))
        return sorted(runs, key=lambda r: -r[2])

    runs1 = blank_runs(starts1, [97, 99, 100])          # 96-97、98-100 跨回节点展开
    runs2 = blank_runs(starts2, [46])
    half1 = (sum(1 for c in starts1 if c <= 50), sum(1 for c in starts1 if c > 50))
    half2 = (sum(1 for c in starts2 if c <= 50), sum(1 for c in starts2 if c > 50))

    vocab = {}
    chap_with = set()
    for w in ("关文", "倒换", "文牒"):
        n = sum(t.count(w) for t in jchapters.values())
        vocab[w] = n
        for k, t in jchapters.items():
            if w in t:
                chap_with.add(k)
    vocab_total = sum(vocab.values())

    # 馆驿专名
    house_rows = [r for r in t2 if r["cells"][2] == "馆驿"]
    named = [r["cells"][1] for r in house_rows if any(k in r["cells"][1] for k in ("金亭馆驿", "迎阳驿", "会同馆"))]

    # 日均里程
    daily = round(108000 / (14 * 365), 1)

    stats = {
        "nodes_total": len(t1) + len(t2), "t1_n": len(t1), "t2_n": len(t2),
        "typology": typ,
        "typology_pct": {k: round(v / 15 * 100, 1) for k, v in typ.items()},
        "verify_split_le60_gt60": ver_split,
        "unverified_chapters": unv_nodes,
        "span": span, "avg_per_30": avg30, "avg_per_15": avg15,
        "buckets_20": buckets, "last_vs_first_bucket_x": buckets[4] / max(buckets[0], 1),
        "half_split_t1": half1, "half_split_t2": half2,
        "gaps_min": min(gaps), "gaps_max": max(gaps), "gaps_median": statistics.median(gaps),
        "blank_runs_t1_top5": runs1[:5], "blank_runs_t2_top5": runs2[:5],
        "vocab": vocab, "vocab_total": vocab_total,
        "vocab_chapters": len(chap_with), "vocab_range": [min(chap_with), max(chap_with)],
        "house_total": len(house_rows), "house_named": len(named),
        "daily_li": daily,
        "jiukey": ("九颗" in jchapters.get(29, "")),
    }

    # ---------------- 引文门禁 & 字数 ----------------
    def cite_check(p):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_citations.py"), "--file", str(p)],
                           capture_output=True, text=True, encoding="utf-8")
        m = re.search(r"共 (\d+) 条引文行", r.stdout)
        return {"lines": int(m.group(1)) if m else None, "exit": r.returncode, "out": r.stdout.strip()}

    cite_main, cite_anon = cite_check(MD), cite_check(MD_ANON)

    def main_count(text):
        i, j = text.find("## 一、"), text.find("## 参考文献")
        sl = re.sub(r"\s+", "", text[i:j])
        return {
            "nows": len(sl),
            "minus_hr": len(sl) - 3 * sl.count("---"),
            "minus_pipes": len(sl) - sl.count("|"),
            "minus_hr_pipes": len(sl) - 3 * sl.count("---") - sl.count("|"),
        }

    wc_main, wc_anon = main_count(md_text), main_count(anon_text)

    # ---------------- 图表与页面数据 ----------------
    def png_dims(p):
        with open(p, "rb") as f:
            d = f.read(33)
        w, h = struct.unpack(">II", d[16:24])
        return {"w": w, "h": h, "bytes": p.stat().st_size}

    page_entries = re.findall(
        r'\{ ch:(\d+), name:"([^"]+)", status:"(\w+)", pill:"([^"]+)", cite:"([^"]+)"', PAGE.read_text(encoding="utf-8"))
    page_cmp = []
    for (ch, name, status, pill, cite) in page_entries:
        row = next((r for r in t1 if r["cells"][1] == name or name.startswith(r["cells"][1])), None)
        same = bool(row) and row["cells"][3] == status and ("第%d回" % row["chapter"]) in cite
        page_cmp.append({"ch": int(ch), "name": name, "status": status,
                         "match_t1": same, "cite": cite,
                         "t1_chapter": row["chapter"] if row else None})

    figures = {
        "page_entries": len(page_entries),
        "page_all_match_t1": all(p["match_t1"] for p in page_cmp),
        "page_mismatch": [p for p in page_cmp if not p["match_t1"]],
        "fig1": png_dims(FIG1), "fig2": png_dims(FIG2),
    }

    result = {
        "generated": "2026-09-28",
        "manuscript": str(MD.relative_to(ROOT)).replace("\\", "/"),
        "claims_total": len(claims), "claims_ok": ok,
        "claims_status_tally": status_tally,
        "claims_by_section": {
            "表1": sum(1 for c in claims if c["source"].startswith("表1")),
            "表2": sum(1 for c in claims if c["source"].startswith("表2")),
            "正文": sum(1 for c in claims if c["source"].startswith("正文")),
        },
        "claims": claims,
        "claims_not_ok": [{"source": c["source"], "snippet": c["snippet"], "result": c["result"]} for c in bad],
        "t1_rows": len(t1), "t2_rows": len(t2), "t2_anon_rows": len(t2a),
        "stats": stats, "citations": {"main": cite_main, "anon": cite_anon},
        "wordcount": {"main": wc_main, "anon": wc_anon},
        "figures": figures,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

    print("== 锚点声明核验 ==  total:", len(claims), "| OK:", ok, "| 异常:", len(bad))
    for b in bad:
        print("   !", json.dumps(b, ensure_ascii=False))
    print("== 统计复算 ==")
    for k in ("nodes_total", "typology", "verify_split_le60_gt60", "span", "avg_per_30", "avg_per_15",
              "buckets_20", "half_split_t1", "half_split_t2", "gaps_min", "gaps_max", "gaps_median",
              "vocab_total", "vocab_chapters", "vocab_range", "house_total", "house_named", "daily_li", "jiukey"):
        print("   %s = %s" % (k, stats[k]))
    print("   空白段 top5（表1口径）:", runs1[:5])
    print("   空白段 top5（表2口径）:", runs2[:5])
    print("== 引文门禁 ==", cite_main["lines"], "条 /", cite_anon["lines"], "条（匿名）")
    print("== 字数 ==", wc_main, wc_anon)
    print("== 图表 ==", json.dumps(figures, ensure_ascii=False))
    print("written:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())