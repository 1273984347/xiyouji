#!/usr/bin/env python3
"""内容空缺审计：以 dataset/*.json 结构化图谱为基准，找出『高被引但无落地正文』的真实缺口。

方法：
  1. 抽取所有 dataset/*.json 中的具名实体（network/sankey 节点、radar/timeline 的 monster 字段、
     yuanqi-graph 节点 label+别名）。
  2. 统计每个实体出现在多少个不同的结构化数据源中（跨语料被引度数）。
  3. 与 docs/ 全部 .md 文档做双向子串匹配（实体名 vs 文档 basename）。
  4. 输出：出现于 >=2 个源、且无任何文档落地的实体 = 候选真实缺口。
"""
import json
import glob
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- Phase 1: 抽取实体 ----------
entity_files = defaultdict(set)  # label -> {source files}


def add(label, src):
    label = (label or "").strip()
    if not label or len(label) < 2:
        return
    if re.search(r"[\d\.\-%/]", label):
        return  # 跳过纯数字/比例
    entity_files[label].add(src)


for f in sorted(glob.glob(os.path.join(ROOT, "dataset", "*.json"))):
    base = os.path.basename(f)
    try:
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
    except Exception:
        continue
    if not isinstance(d, dict):
        continue
    # network 节点
    net = d.get("network") or {}
    for n in net.get("nodes") or []:
        if isinstance(n, dict):
            for k in ("label", "name", "title", "id"):
                if k in n and isinstance(n[k], str):
                    add(n[k], base)
                    break
    # sankey 节点
    sk = d.get("sankey") or {}
    for n in sk.get("nodes") or []:
        if isinstance(n, dict):
            for k in ("label", "name", "title"):
                if k in n and isinstance(n[k], str):
                    add(n[k], base)
                    break
    # radar/timeline 的 monster 字段
    for r in d.get("radar") or []:
        if isinstance(r, dict) and isinstance(r.get("monster"), str):
            add(r["monster"], base)
    for t in d.get("timeline") or []:
        if isinstance(t, dict) and isinstance(t.get("monster"), str):
            add(t["monster"], base)
    # 通用 nodes/vertices
    for key in ("nodes", "vertices"):
        for n in d.get(key) or []:
            if isinstance(n, dict):
                for k in ("label", "name", "title", "id"):
                    if k in n and isinstance(n[k], str):
                        add(n[k], base)
                        break
    # yuanqi-graph：节点 label + 各维度别名
    for n in d.get("nodes") or []:
        if isinstance(n, dict):
            if isinstance(n.get("label"), str):
                add(n["label"], base)
            for al in (n.get("aliases") or {}).values():
                if isinstance(al, str):
                    add(al, base)

# ---------- Phase 2: 文档清单 ----------
doc_basenames = []
for root, _, files in os.walk(os.path.join(ROOT, "docs")):
    for fn in files:
        if fn.endswith(".md"):
            doc_basenames.append(fn[:-3])
doc_norm = {b.lower(): b for b in doc_basenames}


def has_doc(label):
    L = label.lower()
    if L in doc_norm:
        return doc_norm[L]
    for b in doc_basenames:
        bl = b.lower()
        if L in bl or bl in L:  # 双向子串
            return b
    return None


# ---------- Phase 3: 匹配 ----------
gaps = []
matched = []
for label, files in entity_files.items():
    if len(files) < 2:  # 至少被 2 个结构化源引用
        continue
    hit = has_doc(label)
    if hit is None:
        gaps.append((label, len(files), sorted(files)))
    else:
        matched.append((label, len(files), hit))

gaps.sort(key=lambda x: -x[1])
matched.sort(key=lambda x: -x[1])

print(f"结构化实体（出现在 >=2 个源）: {len(gaps) + len(matched)}")
print(f"  ├─ 已有落地文档: {len(matched)}")
print(f"  └─ 高被引且无落地文档（缺口）: {len(gaps)}")
print("\n===== 候选真实缺口（按跨源被引数降序）=====")
for label, cnt, files in gaps:
    print(f"  [{cnt:2d}源] {label}  <- {', '.join(files)}")

print("\n===== 已有文档的高被引实体 TOP20（对照用，验证匹配有效）=====")
for label, cnt, hit in matched[:20]:
    print(f"  [{cnt:2d}源] {label} -> {hit}")
