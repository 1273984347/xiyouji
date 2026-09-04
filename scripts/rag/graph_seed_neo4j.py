#!/usr/bin/env python3
"""
graph_seed_neo4j.py — 把 W326 佛学-AI-西游 三元组导入 Neo4j（对齐 LightRAG Neo4j 后端）

本模块做两件事：
  1. 生成 scripts/output/rag_graph.json —— 内存图的可移植快照（无 Neo4j 时也能用）。
  2. 生成 scripts/output/neo4j_seed.cypher —— 用 LOAD CSV 把 W326 节点/边灌入 Neo4j 的脚本。

LightRAG 原生支持 Neo4j 作为存储后端。本脚本让本项目的「佛法=AI」语义图
（yuanqi_nodes/edges.csv，W326 产出）可以直接成为 LightRAG 知识图谱的种子，
而不是从零让 LLM 重新抽取——这是"结合项目实际"的关键：复用已沉淀的图谱。

用法：
  python graph_seed_neo4j.py            # 生成 rag_graph.json + neo4j_seed.cypher
  # 之后在 Neo4j Browser 执行 neo4j_seed.cypher 即可（需先 cypher-shell 或 Browser 导入 csv）

零依赖（仅标准库）。节点类型 / 关系类型 与原 W326《三维语义映射表》保持一致。
"""

import csv
import json
import os

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
NODES_CSV = os.path.join(ROOT, "scripts", "output", "yuanqi_nodes.csv")
EDGES_CSV = os.path.join(ROOT, "scripts", "output", "yuanqi_edges.csv")
GRAPH_JSON = os.path.join(ROOT, "scripts", "output", "rag_graph.json")
CYPHER = os.path.join(ROOT, "scripts", "output", "neo4j_seed.cypher")


def read_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def build():
    nodes = read_csv(NODES_CSV)
    edges = read_csv(EDGES_CSV)
    # 快照
    snap = {
        "nodes": nodes,
        "edges": edges,
        "node_types": sorted({n["node_type"] for n in nodes}),
        "relations": sorted({e["relation"] for e in edges}),
    }
    with _w536_guard_open(GRAPH_JSON, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)

    # Cypher
    lines = []
    lines.append("// 西游·佛法=AI 语义图 → Neo4j 种子脚本（W326 产出）")
    lines.append("// 在 Neo4j Browser / cypher-shell 中执行前，请先把 yuanqi_nodes.csv / yuanqi_edges.csv")
    lines.append("// 放到 Neo4j import 目录，或修改下方 url 为绝对路径。\n")
    lines.append("LOAD CSV WITH HEADERS FROM 'file:///yuanqi_nodes.csv' AS row")
    lines.append("CREATE (n:Yuanqi {id: row.id, nodeType: row.node_type,")
    lines.append("  buddhist: row.buddhist_entity, ai: row.ai_entity,")
    lines.append("  xiyou: row.xiyou_entity, desc: row.description});\n")
    lines.append("LOAD CSV WITH HEADERS FROM 'file:///yuanqi_edges.csv' AS row")
    lines.append("MATCH (a:Yuanqi {id: row.source}), (b:Yuanqi {id: row.target})")
    lines.append("CREATE (a)-[:REL {type: row.relation, property: row.property,")
    lines.append("  value: row.value}]->(b);\n")
    lines.append("// 索引（可选，加速检索）")
    lines.append("CREATE INDEX yuanqi_id IF NOT EXISTS FOR (n:Yuanqi) ON (n.id);")
    lines.append("CREATE INDEX yuanqi_type IF NOT EXISTS FOR (n:Yuanqi) ON (n.nodeType);")
    cypher = "\n".join(lines)
    with _w536_guard_open(CYPHER, "w", encoding="utf-8") as f:
        f.write(cypher)

    return len(nodes), len(edges), GRAPH_JSON, CYPHER


def main():
    n, e, gj, cp = build()
    print(f"节点 {n} / 边 {e}")
    print(f"快照 → {gj}")
    print(f"Cypher → {cp}")


if __name__ == "__main__":
    main()
