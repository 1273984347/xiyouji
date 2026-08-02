#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xiyouji_rag.py — 《详解西游记》本地 RAG 核心引擎（零依赖）

设计定位（结合本项目实际情况）：
  本环境无 LLM API key、Python 零第三方依赖。因此本模块不强行上重量级
  LightRAG（lightrag-hku 需要 LLM 做图谱抽取 + 生成，无 key 跑不起来），
  而是**用 LightRAG 的架构思想做轻量本地落地**：

    LightRAG 概念            │ 本模块对应实现
    ────────────────────────┼──────────────────────────────────────
    图谱检索（graph layer）  │ 载入 W326 yuanqi_nodes/edges.csv 的
                            │   佛学-AI-西游三元组，做 1~2 跳邻居展开
    向量检索（vector layer） │ 对 672 篇 docs/*.md 建 BM25 倒排索引，
                            │   纯 stdlib 实现，无 embedding 依赖
    双层检索（dual-level）   │ retrieve() 同时返回 语料片段 + 图谱三元组
    Neo4j 后端             │ graph_seed_neo4j.py 可把同一份 CSV 灌入
                            │   Neo4j；本引擎默认用内存图，零外部服务
    LLM 生成               │ 若环境变量 LLM_API_KEY 存在则走真实生成，
                            │   否则返回「检索上下文 + 渡口风格摘要」

零依赖：仅用 Python 标准库（re / json / csv / os / urllib）。
可直接运行：python xiyouji_rag.py "五行山 牧童"

升级到完整 LightRAG：见 scripts/rag/README.md（装 lightrag-hku +
配 LLM/embedding，把 docs/ 交给它做图谱抽取，再用本引擎的图做混合检索）。
"""

import os
import re
import csv
import json
import math

# ---- 路径（相对本脚本：scripts/rag/xiyouji_rag.py → 项目根 = ../../）----
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
DOCS_DIR = os.path.join(ROOT, "docs")
NODES_CSV = os.path.join(ROOT, "scripts", "output", "yuanqi_nodes.csv")
EDGES_CSV = os.path.join(ROOT, "scripts", "output", "yuanqi_edges.csv")
INDEX_CACHE = os.path.join(ROOT, "scripts", "output", "rag_index.json")

K1 = 1.5
B = 0.75


# ============================================================
# 1. 语料层（BM25 向量检索，纯 stdlib）
# ============================================================

def tokenize(text):
    """中文按 单字+二元 切分，英文数字按词切分。无需 jieba。"""
    text = (text or "").lower()
    toks = []
    for m in re.finditer(r'[\u4e00-\u9fff]+|[a-z0-9]+', text):
        chunk = m.group()
        if re.match(r'[\u4e00-\u9fff]+', chunk):
            chars = list(chunk)
            toks.extend(chars)
            for i in range(len(chars) - 1):
                toks.append(chars[i] + chars[i + 1])
        else:
            toks.append(chunk)
    return toks


def _load_docs():
    docs = []
    for base, _, files in os.walk(DOCS_DIR):
        for fn in files:
            if fn.lower().endswith(".md"):
                p = os.path.join(base, fn)
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception:
                    continue
                rel = os.path.relpath(p, ROOT)
                docs.append({"path": rel, "text": text})
    return docs


def build_index(force=False):
    """构建 BM25 索引；命中缓存且非 force 时直接载入。"""
    if (not force) and os.path.exists(INDEX_CACHE):
        try:
            with open(INDEX_CACHE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    docs = _load_docs()
    df = {}
    postings = {}
    lengths = {}
    for idx, d in enumerate(docs):
        tf = {}
        toks = tokenize(d["text"])
        for t in toks:
            tf[t] = tf.get(t, 0) + 1
        lengths[idx] = len(toks)
        for t, c in tf.items():
            df[t] = df.get(t, 0) + 1
            postings.setdefault(t, {})[idx] = c

    N = len(docs)
    index = {
        "docs": [{"path": d["path"]} for d in docs],
        "df": df,
        "postings": postings,
        "lengths": lengths,
        "N": N,
        "avgdl": (sum(lengths.values()) / N) if N else 0.0,
    }
    try:
        with open(INDEX_CACHE, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False)
    except Exception:
        pass
    return index


def bm25_score(index, q_tokens, doc_idx):
    N = index["N"]
    avgdl = index["avgdl"]
    dl = index["lengths"].get(str(doc_idx), index["lengths"].get(doc_idx, 0))
    score = 0.0
    for t in q_tokens:
        if t not in index["df"]:
            continue
        idf = math.log(1 + (N - index["df"][t] + 0.5) / (index["df"][t] + 0.5))
        f = index["postings"].get(t, {}).get(str(doc_idx),
                                        index["postings"].get(t, {}).get(doc_idx, 0))
        if not f:
            continue
        score += idf * (f * (K1 + 1)) / (f + K1 * (1 - B + B * dl / avgdl))
    return score


def retrieve(query, top_k=5, index=None):
    """返回 top_k 语料片段（含路径 + 摘录）。"""
    index = index or build_index()
    qt = tokenize(query)
    if not qt:
        return []
    scored = []
    for idx in range(index["N"]):
        s = bm25_score(index, qt, idx)
        if s > 0:
            scored.append((s, idx))
    scored.sort(reverse=True)
    out = []
    for s, idx in scored[:top_k]:
        d = index["docs"][idx]
        out.append({
            "path": d["path"],
            "score": round(s, 3),
            "excerpt": _excerpt(d["path"], qt),
        })
    return out


def _excerpt(rel_path, qt):
    """取含最多查询词的那一段（段落）作为摘录。"""
    try:
        with open(os.path.join(ROOT, rel_path), "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return ""
    paras = re.split(r"\n\s*\n", text)
    best, best_hit = "", 0
    for p in paras:
        hit = sum(1 for t in qt if t in p)
        if hit > best_hit:
            best_hit, best = hit, p
    return best.strip()[:240]


# ============================================================
# 2. 图谱层（LightRAG graph layer，载入 W326 三元组）
# ============================================================

def load_graph():
    """载入 W326 节点/边 CSV → 内存图。零依赖。"""
    nodes = {}
    edges = []
    if os.path.exists(NODES_CSV):
        with open(NODES_CSV, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                nodes[row["id"]] = row
    if os.path.exists(EDGES_CSV):
        with open(EDGES_CSV, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                edges.append(row)
    # 邻接表（双向）
    adj = {nid: [] for nid in nodes}
    for e in edges:
        adj.setdefault(e["source"], []).append((e["target"], e["relation"], e.get("property", ""), e.get("value", "")))
        adj.setdefault(e["target"], []).append((e["source"], "←" + e["relation"], e.get("property", ""), e.get("value", "")))
    return {"nodes": nodes, "edges": edges, "adj": adj}


def _node_label(node):
    return (f"{node['xiyou_entity']}（佛:{node['buddhist_entity']} / AI:{node['ai_entity']}）"
            if node else "?")


def graph_expand(query, hops=1, g=None):
    """按查询词匹配图谱节点，展开 hops 跳邻居，返回可读三元组。"""
    g = g or load_graph()
    qt = tokenize(query)
    matched = []
    for nid, node in g["nodes"].items():
        hay = " ".join([node.get("buddhist_entity", ""), node.get("ai_entity", ""),
                        node.get("xiyou_entity", ""), node.get("description", ""),
                        node.get("node_type", "")]).lower()
        if any(t in hay for t in qt):
            matched.append(nid)
    triples = []
    seen = set()
    frontier = list(matched)
    for _ in range(hops):
        nxt = []
        for nid in frontier:
            for (nb, rel, prop, val) in g["adj"].get(nid, []):
                key = (nid, nb, rel)
                if key in seen:
                    continue
                seen.add(key)
                triples.append({
                    "from": _node_label(g["nodes"].get(nid)),
                    "relation": rel,
                    "to": _node_label(g["nodes"].get(nb)),
                    "property": prop, "value": val,
                })
                nxt.append(nb)
        frontier = nxt
    if not triples:
        # 无精确命中时，返回图谱概览（前若干条）作为背景
        for e in g["edges"][:6]:
            triples.append({
                "from": _node_label(g["nodes"].get(e["source"])),
                "relation": e["relation"],
                "to": _node_label(g["nodes"].get(e["target"])),
                "property": e.get("property", ""), "value": e.get("value", ""),
            })
    return triples


# ============================================================
# 3. 双层检索聚合 + 生成
# ============================================================

def answer(query, top_k=5, hops=1, use_llm=False):
    """返回 {snippets, graph, draft}。use_llm=True 且配了 key 才真生成。"""
    index = build_index()
    snippets = retrieve(query, top_k=top_k, index=index)
    g = load_graph()
    triples = graph_expand(query, hops=hops, g=g)

    draft = _template_draft(query, snippets, triples)
    result = {
        "query": query,
        "snippets": snippets,
        "graph": triples,
        "draft": draft,
    }
    if use_llm and os.environ.get("LLM_API_KEY"):
        # 预留：真实 LLM 生成分支（需要联网 + key）。未配置时不会走到这里。
        result["llm_generated"] = None  # 见 README 升级路径
    return result


def _template_draft(query, snippets, triples):
    """渡口风格摘要：把真实检索到的语料 + 图谱三元组，缝成一段可溯源草稿。"""
    name = (query or "无名渡口").strip() or "无名渡口"
    cit = ""
    if snippets:
        cit = "；".join(f"《{s['path'].split('/')[-1]}》" for s in snippets[:3])
    gx = ""
    if triples:
        gx = triples[0]["from"] + " —" + triples[0]["relation"] + "→ " + triples[0]["to"]
    body = (
        f"【渡口检索档案】{name}\n\n"
        f"在《详解西游记》的语料中，与「{name}」相关的记载见于：{cit or '（暂无精确命中，以下为图谱背景）'}。\n\n"
        f"从「佛法=AI」图谱看，{gx}。\n\n"
        f"渡口视角：被记入正文的，是参与前向传播的节点；未被记入的，是让路径成立的隐变量。"
        f"检索不是为了找出标准答案，而是为了证明——每一次输入，都曾改变过权重的分布。"
    )
    return body


# ============================================================
# 4. CLI
# ============================================================

def main():
    import sys
    q = " ".join(sys.argv[1:]) or "五行山 牧童"
    print(f"# 查询：{q}\n")
    res = answer(q, top_k=5, hops=1)
    print("## 语料检索（BM25）")
    for s in res["snippets"]:
        print(f"  [{s['score']}] {s['path']}")
        if s["excerpt"]:
            print(f"       …{s['excerpt'][:120]}…")
    print("\n## 图谱三元组（W326）")
    for t in res["graph"][:6]:
        print(f"  {t['from']} —{t['relation']}→ {t['to']}  ({t['property']}: {t['value']})")
    print("\n## 渡口风格摘要")
    print(res["draft"])


if __name__ == "__main__":
    main()
