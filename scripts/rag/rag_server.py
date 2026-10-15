#!/usr/bin/env python3
"""
rag_server.py — 《详解西游记》本地 RAG 查询服务（零依赖）

基于 Python 标准库 http.server，暴露给 dukou-engine.html 调用的本地 API：
  GET /health              → {"status":"ok","routes":N}（W746 起不再触发 BM25 索引）
  GET /query?q=五行山牧童   → {"query","snippets","graph","draft"}
  GET /graph?q=紧箍咒       → {"graph":[...]}  仅图谱三元组
  GET /route?q=天庭权力结构  → {"query","routes":[{file,title,score}]}  语义页面路由
                               （W746·懒加载 page_router·只读页面向量缓存）

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

# W746：语义页面路由（懒加载·/route 只读 page_vectors 缓存·不触发 RAG BM25 索引）
_router_state = {"model": None, "vecs": None, "pages": None}


def _get_router():
    """路由状态懒加载（首次 /route 调用时加载模型与页面向量缓存）。"""
    if _router_state["model"] is None:
        import page_router as PR
        pages = PR.load_pages()
        model = PR._load_model()
        vecs = PR._ensure_cache(model, pages)
        _router_state.update({"model": model, "vecs": vecs, "pages": pages})
    return _router_state


def _routes_count():
    """路由页数：读 page_index.json 指纹（不加载模型·不触发 RAG 索引）。"""
    try:
        import page_router as PR
        with open(PR.CACHE_IDX, encoding="utf-8") as f:
            idx = json.load(f)
        n = len(idx.get("fingerprint", []))
        if n:
            return n
    except Exception:
        pass
    try:
        import page_router as PR
        return len(PR.load_pages())
    except Exception:
        return 0


def _clamp_int(raw, default, lo, hi):
    """P2-1：解析整数并钳制到 [lo, hi]；非法输入回落 default（防 DoS/500）。"""
    try:
        v = int(raw)
    except (TypeError, ValueError):
        v = default
    return max(lo, min(hi, v))


def _sanitize_history(raw):
    """P2-1：history schema 校验——仅允许 list、条目 role∈{user,assistant,bot}、
    text 非空且 ≤2000 字符、条目数 ≤20；非法输入返回 None（防 prompt injection/超长）。"""
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
    except Exception:
        return None
    if not isinstance(parsed, list) or len(parsed) > 20:
        return None
    out = []
    for turn in parsed:
        if not isinstance(turn, dict):
            continue
        role = str(turn.get("role", "")).lower()
        if role not in ("user", "assistant", "bot"):
            continue
        text = str(turn.get("text", "")).strip()
        if not text or len(text) > 2000:
            continue
        out.append({"role": role, "text": text})
    return out or None


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
            # W746：解绑 RAG 索引（dukou-engine 不消费 docs 字段·已实证）——
            # /health 不再触发 1077 篇 BM25 构建；路由页数走 page_index 指纹。
            self._send({"status": "ok", "routes": _routes_count()})
            return
        if parsed.path == "/query":
            query = q.get("q", [""])[0]
            top_k = _clamp_int(q.get("k", ["5"])[0], 5, 1, 50)          # P2-1：范围钳制防 DoS
            hops = _clamp_int(q.get("hops", ["1"])[0], 1, 1, 3)          # P2-1：范围钳制防全图遍历
            history = _sanitize_history(q.get("history", [""])[0])       # P2-1：schema 校验防注入/超长
            res = RAG.answer(query, top_k=top_k, hops=hops, history=history)
            self._send(res)
            return
        if parsed.path == "/graph":
            query = q.get("q", [""])[0]
            triples = RAG.graph_expand(query, hops=_clamp_int(q.get("hops", ["1"])[0], 1, 1, 3))
            self._send({"graph": triples})
            return
        if parsed.path == "/route":
            # W746：语义页面路由（懒加载·失败 fail-fast 500·不静默降级）
            query = q.get("q", [""])[0]
            top_k = _clamp_int(q.get("k", ["5"])[0], 5, 1, 20)
            try:
                import page_router as PR
                st = _get_router()
                results = PR.route(query, st["model"], st["vecs"], st["pages"], top_k=top_k)
                self._send({"query": query, "routes": [
                    {"file": f, "title": t, "score": round(s, 4)} for f, t, s in results]})
            except Exception as exc:
                self._send({"error": "route failed: %s" % exc}, code=500)
            return
        self._send({"error": "not found"}, code=404)

    def log_message(self, *args):
        pass  # 静默


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8777
    host = "127.0.0.1"
    # W746：路由模型主线程预热——torch/sentence-transformers 在 handler 子线程
    # 首次 import 有段错误风险（本机实证：exit 139 静默死亡）；启动时一次付清，
    # /route 只做 encode（轻）。预热失败不阻塞服务（/route 返回 500 说明）。
    try:
        _get_router()
        print("路由模型已预热（/route 就绪）")
    except Exception as exc:
        print("路由模型预热失败（/route 暂不可用）：%s" % exc)
    srv = ThreadingHTTPServer((host, port), Handler)
    print(f"西游·渡口 RAG 服务已启动： http://{host}:{port}")
    print("  按 Ctrl+C 停止。")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")


if __name__ == "__main__":
    main()
