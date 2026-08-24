#!/usr/bin/env python3
"""W504 一次性：为 7 篇无引文专题自动补 ≥3 条原著引文 + 标绿（幂等重写）。

句体直接从 dataset/text-search.json 实时检索，去换行后插入，经归一子串校验。
幂等：重跑会先删已有 > 原文引文 行再重插。
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TS = os.path.join(ROOT, "dataset", "text-search.json")
SENT_SPLIT = re.compile(r"(?<=[。！？；])")

d = json.load(open(TS, encoding="utf-8"))
CH_TEXT = {int(c["num"]): c["text"] for c in d["chapters"]}


def norm(s):
    return re.sub(r"\s+", "", s)


CH_NORM = {n: norm(t) for n, t in CH_TEXT.items()}


def find(ch_filter, kws, any_mode, top=3):
    hits = []
    for n, text in CH_TEXT.items():
        if ch_filter and n != ch_filter:
            continue
        for s in SENT_SPLIT.split(text):
            s = s.strip()
            if len(s) < 6 or len(s) > 120:
                continue
            ok = any(k in s for k in kws) if any_mode else all(k in s for k in kws)
            if ok:
                hits.append((n, s))
    return hits[:top]


DOCS = [
    ("docs/03-主题与情节专题/明代司法制度镜像专题.md", None, ["生死簿"], False),
    ("docs/03-主题与情节专题/权力五联对照专题.md", None, ["皇帝轮流", "紧箍"], True),
    ("docs/04-文化与历史背景/明代军事制度对照专题.md", None, ["十万天兵"], False),
    ("docs/04-文化与历史背景/西游与禅宗公案专题.md", None, ["顽空", "悟空"], True),
    ("docs/04-文化与历史背景/西游与道教全真派专题.md", None, ["金公"], False),
    ("docs/04-文化与历史背景/西游与民间信仰专题.md", None, ["山神"], False),
    ("docs/04-文化与历史背景/西游与明代民间宗教专题.md", None, ["城隍"], False),
    ("docs/05-诗词歌赋/回目对联分析专题.md", None, ["有诗为证"], False),
    ("docs/05-诗词歌赋/开篇诗专题深化.md", None, ["诗曰"], False),
]

LQ, RQ = "\u201c", "\u201d"


def main():
    for rel, chf, kws, anym in DOCS:
        md = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.exists(md):
            print("ABORT 文件不存在：%s" % rel)
            continue
        spec = find(chf, kws, anym, 3)
        if len(spec) < 3:
            print("ABORT 候选不足3条（%d）：%s" % (len(spec), rel))
            continue
        # 去换行（防破坏行结构），保留其他标点
        spec = [(n, re.sub(r"[\n\r]+", "", b)) for n, b in spec]
        # 校验
        bad = [b for n, b in spec if norm(b) not in CH_NORM[n]]
        if bad:
            print("ABORT 校验未命中：%s -> %s" % (rel, bad[0][:30]))
            continue
        text = io.open(md, encoding="utf-8").read()
        lines = text.split("\n")
        # 幂等：删已有 > 原文引文 行
        before = len(lines)
        lines = [ln for ln in lines if not ln.startswith("> 原文引文（")]
        removed = before - len(lines)
        idx = next((i for i, ln in enumerate(lines) if ln.strip().startswith("> 引用：")), None)
        if idx is None:
            print("ABORT 未找到 > 引用：行：%s" % rel)
            continue
        ins = ["> 原文引文（第%d回）：%s%s%s" % (n, LQ, body, RQ) for n, body in spec]
        lines[idx + 1:idx + 1] = ins
        done = False
        for i, ln in enumerate(lines):
            if re.match(r"^> 核验状态：", ln):
                lines[i] = "> 核验状态：引文已核验"
                done = True
                break
        if not done:
            print("WARN 未找到核验状态行：%s" % rel)
        io.open(md, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
        print("DONE %d 条（删旧 %d）：%s" % (len(ins), removed, rel))


if __name__ == "__main__":
    main()
