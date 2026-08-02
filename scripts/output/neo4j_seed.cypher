// 西游·佛法=AI 语义图 → Neo4j 种子脚本（W326 产出）
// 在 Neo4j Browser / cypher-shell 中执行前，请先把 yuanqi_nodes.csv / yuanqi_edges.csv
// 放到 Neo4j import 目录，或修改下方 url 为绝对路径。

LOAD CSV WITH HEADERS FROM 'file:///yuanqi_nodes.csv' AS row
CREATE (n:Yuanqi {id: row.id, nodeType: row.node_type,
  buddhist: row.buddhist_entity, ai: row.ai_entity,
  xiyou: row.xiyou_entity, desc: row.description});

LOAD CSV WITH HEADERS FROM 'file:///yuanqi_edges.csv' AS row
MATCH (a:Yuanqi {id: row.source}), (b:Yuanqi {id: row.target})
CREATE (a)-[:REL {type: row.relation, property: row.property,
  value: row.value}]->(b);

// 索引（可选，加速检索）
CREATE INDEX yuanqi_id IF NOT EXISTS FOR (n:Yuanqi) ON (n.id);
CREATE INDEX yuanqi_type IF NOT EXISTS FOR (n:Yuanqi) ON (n.nodeType);