#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SD 切片错位（张冠李戴）扫描器。

原理：
- source/原文/shendu/SD###.md 是“深度解读”评论切片，头部 HTML 注释声明其对应原著回号。
- source/原文/分回/第C回.md 是各回原著正文，作为“真实章节内容”的基准（ground truth）。
- 对每个 SD 切片，将其正文与全部 100 回原著正文做字二元组余弦相似度，报告最匹配的 3 回。
- 若切片声明章节 C 不在 top3，或存在另一回 C' 匹配分明显高于 C，则判定疑似错位。
- 同时做 SD 切片两两近重复检测，捕捉“同一段错贴内容落到多个切片”的情况。
- 同时检查 文件名编号 与 头部声明回号 是否一致。

输出：
- 控制台打印疑似错位清单与逐项 top3 相似度。
- 报告写入 .workbuddy/sd_scan_report.md（不在 git 跟踪内）。
"""
import os
import re
import glob
import json
import math
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHENDU = os.path.join(ROOT, "source", "原文", "shendu")
FENHUI = os.path.join(ROOT, "source", "原文", "分回")
REPORT = os.path.join(ROOT, ".workbuddy", "sd_scan_report.md")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def bigrams(text):
    # 去掉空白与标点，保留汉字与少量字符，取相邻二字
    text = re.sub(r"\s+", "", text)
    # 仅保留中文字符用于二元组（评论与正文主要差异在中文专有词）
    chars = [c for c in text if "\u4e00" <= c <= "\u9fff"]
    return Counter(chars[i] + chars[i + 1] for i in range(len(chars) - 1))


def cosine(a, b):
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def parse_claimed(body):
    """从头部注释解析声明回号。"""
    m = re.search(r"推测对应原著回号:\s*第(\d+)回", body)
    if m:
        return int(m.group(1))
    return None


def extract_sd_body(text):
    """去掉头部 HTML 注释与首行 # 标题，保留评论正文。"""
    # 删除 <!-- ... --> 注释块
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    # 删除首个 # 一级标题行
    text = re.sub(r"^#\s.*$", "", text, count=1, flags=re.MULTILINE)
    return text.strip()


def main():
    sd_files = sorted(glob.glob(os.path.join(SHENDU, "SD*.md")))
    fen = {}
    for p in sorted(glob.glob(os.path.join(FENHUI, "第*.md"))):
        m = re.search(r"第(\d+)回", os.path.basename(p))
        if m:
            fen[int(m.group(1))] = p

    # 预计算原著回正文二元组
    fen_bg = {}
    for c, p in fen.items():
        fen_bg[c] = bigrams(read(p))

    # 读取 SD 切片
    sd = {}  # num -> (claimed, body_text, body_bg, filename)
    for p in sd_files:
        base = os.path.basename(p)
        m = re.match(r"SD(\d+)\.md", base)
        if not m:
            continue
        num = int(m.group(1))
        txt = read(p)
        claimed = parse_claimed(txt)
        body = extract_sd_body(txt)
        sd[num] = (claimed, body, bigrams(body), base)

    # 对每个 SD 计算与全部回的相似度
    results = []
    for num in sorted(sd):
        claimed, body, bg, base = sd[num]
        scores = []
        for c in fen_bg:
            scores.append((c, cosine(bg, fen_bg[c])))
        scores.sort(key=lambda x: -x[1])
        top3 = scores[:3]
        top1_c, top1_s = top3[0]
        self_s = dict(scores).get(claimed, 0.0) if claimed else 0.0
        # 判定
        issues = []
        if claimed is None:
            issues.append("无声明回号")
        else:
            if claimed != num:
                issues.append(f"文件名SD{num:03d}≠声明第{claimed}回")
            if claimed not in [c for c, _ in top3]:
                issues.append(f"声明第{claimed}回不在top3(最佳第{top1_c}回)")
            elif top1_c != claimed and top1_s > self_s * 1.03:
                issues.append(f"最佳匹配第{top1_c}回({top1_s:.3f})>声明第{claimed}回({self_s:.3f})")
        results.append({
            "sd": num,
            "base": base,
            "claimed": claimed,
            "self_sim": round(self_s, 4),
            "top3": [(c, round(s, 4)) for c, s in top3],
            "issues": issues,
        })

    # SD 两两近重复
    dup_pairs = []
    nums = sorted(sd)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            a, b = nums[i], nums[j]
            s = cosine(sd[a][2], sd[b][2])
            if s > 0.55:
                dup_pairs.append((a, b, round(s, 4)))

    # 输出报告
    flagged = [r for r in results if r["issues"]]
    lines = []
    lines.append("# SD 切片错位扫描报告\n")
    lines.append(f"- 扫描切片数：{len(results)}")
    lines.append(f"- 疑似错位（有 issue）：{len(flagged)}")
    lines.append(f"- SD 两两近重复对（>0.55）：{len(dup_pairs)}\n")
    lines.append("## 疑似错位清单（按严重度）\n")
    for r in sorted(flagged, key=lambda x: -x["top3"][0][1]):
        lines.append(f"### SD{r['sd']:03d}（{r['base']}）声明第{r['claimed']}回")
        lines.append(f"- issues: {r['issues']}")
        lines.append(f"- self_sim(声明回): {r['self_sim']}")
        lines.append(f"- top3: " + ", ".join(f"第{c}回={s}" for c, s in r["top3"]))
        lines.append("")
    lines.append("## SD 两两近重复（>0.55）\n")
    for a, b, s in sorted(dup_pairs, key=lambda x: -x[2]):
        ca, cb = sd[a][0], sd[b][0]
        lines.append(f"- SD{a:03d}(第{ca}回) ≈ SD{b:03d}(第{cb}回)  cos={s}")
    lines.append("")
    lines.append("## 全部 SD 的 top3（审计留痕）\n")
    for r in results:
        lines.append(
            f"- SD{r['sd']:03d} 声明第{r['claimed']}回 self={r['self_sim']} | "
            + " ".join(f"第{c}={s}" for c, s in r["top3"])
        )

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # 控制台摘要
    print(f"扫描切片: {len(results)} | 疑似错位: {len(flagged)} | 近重复对: {len(dup_pairs)}")
    print("--- 疑似错位（声明回不在 top1 或存在更优匹配）---")
    for r in sorted(flagged, key=lambda x: -x["top3"][0][1]):
        print(f"SD{r['sd']:03d} 声明第{r['claimed']}回 self={r['self_sim']} | top3="
              + ", ".join(f"第{c}={s}" for c, s in r["top3"]) + f" | {r['issues']}")
    print("--- 近重复对 ---")
    for a, b, s in sorted(dup_pairs, key=lambda x: -x[2]):
        print(f"SD{a:03d}≈SD{b:03d} cos={s}")
    print(f"\n完整报告: {REPORT}")


if __name__ == "__main__":
    main()
