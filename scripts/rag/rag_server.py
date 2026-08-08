#!/usr/bin/env python3
"""
rag_server.py — 《详解西游记》本地 RAG 查询服务（零依赖）

基于 Python 标准库 http.server，暴露给 dukou-engine.html 调用的本地 API：
  GET /health              → {"status":"ok"}
  GET /query?q=五行山牧童   → {"query","snippets","graph","draft"}
  GET /graph?q=紧箍咒       → {"graph":[...]}  仅图谱三元组

零依赖：仅标准库。直接运行：
  python rag_server.py            # 默认 127.0.0.1:8777
  python rag_server.py 9000       # 指定端口

dukou-engine.html 通过 fetch('http://127.0.0.1:8777/query?q=...') 调用；
服务端未启动时，前端自动回退到原模板引擎（见 dukou-engine.html）。

这是 LightRAG 架构的轻量落地：图谱层(W326 CSV) + 向量层(BM25) 双层检索，
Neo4j 后端路径见 graph_seed_neo4j.py。完整 lightrag-hku 升级见 README.md。
"""

import json
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xiyouji_rag as RAG


class Handler(BaseHTTPRequestHandler):
    def _send(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")  # 允许前端 file:// 跨域
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/health":
            self._send({"status": "ok", "docs": RAG.build_index()["N"]})
            return
        if parsed.path == "/query":
            query = q.get("q", [""])[0]
            top_k = int(q.get("k", ["5"])[0])
            hops = int(q.get("hops", ["1"])[0])
            history = None
            raw_h = q.get("history", [""])[0]
            if raw_h:
                try:
                    history = json.loads(raw_h)
                except Exception:
                    history = None
            res = RAG.answer(query, top_k=top_k, hops=hops, history=history)
            self._send(res)
            return
        if parsed.path == "/graph":
            query = q.get("q", [""])[0]
            triples = RAG.graph_expand(query, hops=int(q.get("hops", ["1"])[0]))
            self._send({"graph": triples})
            return
        self._send({"error": "not found"}, code=404)

    def log_message(self, *args):
        pass  # 静默


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8777
    host = "127.0.0.1"
    srv = ThreadingHTTPServer((host, port), Handler)
    print(f"西游·渡口 RAG 服务已启动： http://{host}:{port}")
    print("  按 Ctrl+C 停止。")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")


if __name__ == "__main__":
    main()
