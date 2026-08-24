#!/usr/bin/env python3
"""引文候选提取探针（E-A 沉淀，W507 永久化）。

为 docs/01-06 新文档（方向二深化/深化专题/学术轨）从 dataset/text-search.json
提取可命中的 `> 原文引文（第N回）` 候选句。写作时必须先用本工具取候选，禁止凭记忆
编造引文（W503 铁律变体，2026-08-25 W505 高翠兰篇编造 FAIL 教训）。

用法：
  py scripts/_cite_probe.py --kw 菩提祖师,须菩提          # 多关键词（任一命中即候选）
  py scripts/_cite_probe.py --kw 黑熊精 --chap 16-17      # 限定回目区间
  py scripts/_cite_probe.py --kw 高翠兰 --min-len 10 --max-len 80
  py scripts/_cite_probe.py --kw 金角大王 --frag          # 片段模式（无句读也可）

完整句模式输出 `[第N回] <候选句>`：候选句去除全部空白后必为 chapters[N-1].text 的精确子串，可直接放入 `> 原文引文（第N回）：“…”` 行。

说明：诊断工具（_ 前缀），不入库门禁、不参与 CI。
"""
import argparse
import json
import re


def main():
    ap = argparse.ArgumentParser(description="引文候选提取探针")
    ap.add_argument("--kw", required=True, help="关键词，逗号分隔（任一命中即候选）")
    ap.add_argument("--chap", default="1-100", help="回目区间，如 16-17（默认 1-100）")
    ap.add_argument("--min-len", type=int, default=8, help="候选最短长度（默认 8）")
    ap.add_argument("--max-len", type=int, default=100, help="候选最大长度（默认 100）")
    ap.add_argument("--frag", action="store_true", help="片段模式：关键词±20字（无需完整句）")
    args = ap.parse_args()

    kws = [k.strip() for k in args.kw.split(",") if k.strip()]
    if not kws:
        raise SystemExit("--kw 不能为空")
    parts = [int(x) for x in args.chap.split("-")]
    c0, c1 = (parts[0], parts[0]) if len(parts) == 1 else (parts[0], parts[1])
    pat = re.compile("|".join(kws))
    sent_re = re.compile(r"[^。！？\r\n]*" + pat.pattern + r"[^。！？\r\n]*[。！？]")

    chapters = json.load(open("dataset/text-search.json", encoding="utf-8"))["chapters"]
    total = 0
    for ch in chapters:
        n = int(ch["num"])
        if not (c0 <= n <= c1):
            continue
        text = ch["text"]
        if not pat.search(text):
            continue
        if args.frag:
            for m in pat.finditer(text):
                frag = text[max(0, m.start() - 20):m.end() + 40].replace("\n", " ").strip()
                if args.min_len <= len(frag) <= args.max_len:
                    print(f"[第{n}回] …{frag}…")
                    total += 1
        else:
            for m in sent_re.finditer(text):
                sent = m.group(0).strip()
                if args.min_len <= len(sent) <= args.max_len:
                    print(f"[第{n}回] {sent}")
                    total += 1
    print(f"--- 共 {total} 条候选（第{c0}-{c1}回 · 关键词 {'/'.join(kws)}）---")


if __name__ == "__main__":
    main()
