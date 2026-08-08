#!/usr/bin/env python3
"""
api_server.py — 《详解西游记》结构化数据 REST API（零依赖）

把 dataset/ 下的 40 个结构化 JSON 包装为可外部调用的 REST 服务。
与 rag_server.py 同风格（仅标准库 http.server），无需 pip install，
直接 `python api_server.py` 即可运行，符合项目「零依赖·随处可跑」原则。

> 关于 FastAPI/Flask：W337 方向原议用 FastAPI，但本项目坚持零依赖、
> 可 file:// 直接打开的工程约束；本服务用 stdlib 落地，行为与 FastAPI
> 等价（路由 + JSON + CORS + OpenAPI 描述）。若需 ASGI/异步吞吐，可把
> 下方 handler 逻辑平移到 FastAPI 的 `@app.get` 即可，无需改动检索逻辑。

路由：
  GET /                       → 人类可读 API 文档页（HTML）
  GET /health                 → {"status":"ok","datasets":N}
  GET /openapi.json           → 接口描述（类 OpenAPI）
  GET /datasets               → 数据集清单 [{name,keys,title,size_kb}]
  GET /dataset/<name>         → 该数据集全量 JSON（404 若无）
  GET /dataset/<name>/keys    → 仅返回顶层键 + 元信息
  GET /search?q=<kw>          → 跨所有数据集递归检索，返回命中路径与片段
  GET /dataset/<name>/raw     → 原文字节（application/json 附件下载）

默认监听 127.0.0.1:8787（参数可改端口）。CORS 允许跨域（前端 file:// 可用）。
"""

import json
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
DATASET_DIR = os.path.join(ROOT, "dataset")

PORT = 8787
HOST = "127.0.0.1"


def _list_datasets():
    out = []
    if not os.path.isdir(DATASET_DIR):
        return out
    for fn in sorted(os.listdir(DATASET_DIR)):
        if not fn.endswith(".json"):
            continue
        name = fn[:-5]
        p = os.path.join(DATASET_DIR, fn)
        size_kb = round(os.path.getsize(p) / 1024, 1)
        try:
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
            keys = list(data.keys()) if isinstance(data, dict) else []
            title = ""
            if isinstance(data, dict) and isinstance(data.get("meta"), dict):
                title = data["meta"].get("title", "")
        except Exception:
            keys, title = [], ""
        out.append({"name": name, "keys": keys, "title": title, "size_kb": size_kb})
    return out


def _load_dataset(name):
    p = os.path.join(DATASET_DIR, name + ".json")
    if not os.path.exists(p):
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _recursive_search(obj, q, path=""):
    """递归检索：字符串包含 q 即命中，返回 (path, snippet)。"""
    hits = []
    ql = q.lower()
    if isinstance(obj, dict):
        for k, v in obj.items():
            hits.extend(_recursive_search(v, q, f"{path}.{k}" if path else k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits.extend(_recursive_search(v, q, f"{path}[{i}]"))
    elif isinstance(obj, str):
        idx = obj.lower().find(ql)
        if idx >= 0:
            start = max(0, idx - 20)
            end = min(len(obj), idx + len(q) + 40)
            snippet = ("…" if start > 0 else "") + obj[start:end] + ("…" if end < len(obj) else "")
            hits.append({"path": path, "snippet": snippet})
    return hits


# ---- 图谱数据（图集注册表，W339 知识图谱探索器）----
def _load_yuanqi_graph():
    d = _load_dataset("yuanqi-graph")
    if not isinstance(d, dict) or "nodes" not in d:
        return None
    return d


def _load_char_graph():
    d = _load_dataset("character-relationship-3d")
    if not isinstance(d, dict):
        return None
    nodes = [{"id": n.get("id"), "label": n.get("name", n.get("id")),
              "group": str(n.get("group", "")), "desc": n.get("desc", ""),
              "importance": n.get("importance", 0)}
             for n in d.get("nodes", []) if isinstance(n, dict)]
    edges = [{"source": e.get("source"), "target": e.get("target"),
              "relation": e.get("type", ""), "property": "", "value": ""}
             for e in d.get("links", []) if isinstance(e, dict)]
    return {"meta": {"title": "取经团队人物关系图谱（3D 投影）",
                     "note": "取经五人 + 关键神佛妖魔的关系网络（group=阵营/身份）。",
                     "schema": "graph", "group_colors": {}, "dimensions": []},
            "nodes": nodes, "edges": edges}


_GRAPH_REGISTRY = {
    "yuanqi-graph": {"title": "佛法=AI=西游 三元映射图谱（W326）", "loader": _load_yuanqi_graph},
    "character-relationship-3d": {"title": "取经团队人物关系图谱（3D 投影）", "loader": _load_char_graph},
}


def _load_graph(name):
    reg = _GRAPH_REGISTRY.get(name)
    if not reg:
        return None
    try:
        return reg["loader"]()
    except Exception:
        return None


def _list_graphs():
    out = []
    for name, reg in _GRAPH_REGISTRY.items():
        g = _load_graph(name)
        if not g:
            continue
        out.append({"name": name, "title": reg.get("title", name),
                    "node_count": len(g.get("nodes", [])),
                    "edge_count": len(g.get("edges", []))})
    return out


def _doc_html():
    ds = _list_datasets()
    rows = "".join(
        f"<tr><td><code>{d['name']}</code></td><td>{d['size_kb']} KB</td>"
        f"<td>{d['title'] or '—'}</td><td><code>{', '.join(d['keys'][:6])}"
        f"{' …' if len(d['keys']) > 6 else ''}</code></td></tr>"
        for d in ds
    )
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>详解西游记 · 数据 API</title>
<style>body{{font-family:system-ui,'Noto Sans SC',sans-serif;max-width:880px;margin:32px auto;padding:0 16px;color:#23201a;line-height:1.6}}
h1{{color:#c8463a}}code{{background:#f3ede2;padding:1px 5px;border-radius:4px;font-size:13px}}
table{{border-collapse:collapse;width:100%;margin:12px 0}}th,td{{border:1px solid #d9cdb8;padding:6px 9px;text-align:left;font-size:14px}}
th{{background:#faf7f2}}a{{color:#3a6b8c}}.ep{{background:#faf7f2;border:1px solid #d9cdb8;border-radius:8px;padding:10px 14px;margin:8px 0}}
.endpoint{{font-weight:600;color:#3a6b8c}}</style></head><body>
<h1>详解西游记 · 结构化数据 API</h1>
<p>零依赖 REST 服务，包装 <code>dataset/</code> 下 {len(ds)} 个结构化 JSON。
所有响应为 <code>application/json; charset=utf-8</code>，允许跨域（CORS）。</p>
<h2>接口</h2>
<div class="ep"><span class="endpoint">GET /health</span> — 存活探测，返回数据集数量</div>
<div class="ep"><span class="endpoint">GET /datasets</span> — 数据集清单（名称/大小/顶层键/标题）</div>
<div class="ep"><span class="endpoint">GET /dataset/&lt;name&gt;</span> — 某数据集全量 JSON</div>
<div class="ep"><span class="endpoint">GET /dataset/&lt;name&gt;/keys</span> — 仅顶层键 + 元信息</div>
<div class="ep"><span class="endpoint">GET /search?q=&lt;关键词&gt;</span> — 跨所有数据集递归检索</div>
<div class="ep"><span class="endpoint">GET /graph</span> — 图集清单（W339 知识图谱探索器）</div>
<div class="ep"><span class="endpoint">GET /graph/&lt;name&gt;</span> — 单图 nodes/edges（yuanqi-graph / character-relationship-3d）</div>
<div class="ep"><span class="endpoint">GET /openapi.json</span> — 接口描述（类 OpenAPI）</div>
<h2>数据集清单（{len(ds)}）</h2>
<table><thead><tr><th>名称</th><th>大小</th><th>标题</th><th>顶层键</th></tr></thead>
<tbody>{rows}</tbody></table>
<p>示例：<a href="/dataset/81-hardships">/dataset/81-hardships</a> ·
<a href="/search?q=%E7%81%AB%E7%84%B0%E5%B1%B1">/search?q=火焰山</a></p>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, obj, code=200, ctype="application/json; charset=utf-8"):
        if isinstance(obj, (dict, list)):
            body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        else:
            body = obj.encode("utf-8") if isinstance(obj, str) else obj
            ctype = ctype or "application/octet-stream"
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        q = urllib.parse.parse_qs(parsed.query)

        if path == "/api" or path == "/docs":
            self._send(_doc_html(), ctype="text/html; charset=utf-8")
            return
        if path == "/health":
            self._send({"status": "ok", "datasets": len(_list_datasets())})
            return
        if path == "/openapi.json":
            self._send({
                "name": "xiyouji-dataset-api", "version": "v2.2.92",
                "baseUrl": f"http://{HOST}:{PORT}",
                "endpoints": [
                    {"path": "/health", "method": "GET", "desc": "存活探测"},
                    {"path": "/datasets", "method": "GET", "desc": "数据集清单"},
                    {"path": "/dataset/<name>", "method": "GET", "desc": "数据集全量"},
                    {"path": "/dataset/<name>/keys", "method": "GET", "desc": "顶层键"},
                    {"path": "/search", "method": "GET", "desc": "跨集检索", "params": ["q"]},
                    {"path": "/graph", "method": "GET", "desc": "图集清单"},
                    {"path": "/graph/<name>", "method": "GET", "desc": "单图（nodes/edges）"},
                ],
            })
            return
        if path == "/datasets":
            self._send(_list_datasets())
            return
        if path == "/search":
            kw = q.get("q", [""])[0].strip()
            if not kw:
                self._send({"error": "missing q"}, code=400)
                return
            res = []
            for d in _list_datasets():
                data = _load_dataset(d["name"])
                if data is None:
                    continue
                hits = _recursive_search(data, kw)
                if hits:
                    res.append({"dataset": d["name"], "hit_count": len(hits), "hits": hits[:20]})
            self._send({"query": kw, "matches": len(res), "results": res})
            return

        # /graph 图集列举 与 /graph/<name> 单图（W339 知识图谱探索器）
        gparts = [p for p in path.split("/") if p]
        if gparts and gparts[0] == "graph":
            if len(gparts) == 1:
                self._send(_list_graphs())
            else:
                g = _load_graph(gparts[1])
                if g is None:
                    self._send({"error": f"graph not found: {gparts[1]}", "try": "/graph"}, code=404)
                else:
                    self._send(g)
            return

        # /dataset/<name> 或 /dataset/<name>/keys
        parts = [p for p in path.split("/") if p]
        if len(parts) >= 2 and parts[0] == "dataset":
            name = parts[1]
            data = _load_dataset(name)
            if data is None:
                self._send({"error": f"dataset not found: {name}"}, code=404)
                return
            if len(parts) == 3 and parts[2] == "keys":
                meta = data.get("meta") if isinstance(data, dict) else None
                self._send({"name": name, "keys": list(data.keys()) if isinstance(data, dict) else [],
                            "meta": meta})
                return
            self._send(data)
            return

        # 静态资源：API 路由未命中时，尝试从 site/ 提供（让 API 同时托管前端）
        static_path = self._resolve_static(path)
        if static_path:
            try:
                with open(static_path, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", self._ctype(static_path))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            except Exception:
                pass

        self._send({"error": "not found", "try": "/datasets"}, code=404)

    @staticmethod
    def _resolve_static(path):
        """把 /data/x.html、/static/js/y.js、/index.html 等映射到 site/ 下真实文件。"""
        rel = path.lstrip("/")
        site_root = os.path.normpath(os.path.join(ROOT, "site"))
        if not rel:
            cand = os.path.join(site_root, "index.html")
            return cand if os.path.isfile(cand) else None
        full = os.path.normpath(os.path.join(site_root, rel))
        if full.startswith(site_root + os.sep) and os.path.isfile(full):
            return full
        return None

    @staticmethod
    def _ctype(p):
        ext = os.path.splitext(p)[1].lower().lstrip(".")
        return {
            "html": "text/html; charset=utf-8", "css": "text/css; charset=utf-8",
            "js": "application/javascript; charset=utf-8", "json": "application/json; charset=utf-8",
            "webmanifest": "application/manifest+json", "png": "image/png", "jpg": "image/jpeg",
            "jpeg": "image/jpeg", "webp": "image/webp", "svg": "image/svg+xml",
            "woff2": "font/woff2", "woff": "font/woff", "ttf": "font/ttf",
        }.get(ext, "application/octet-stream")

    def log_message(self, *args):
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    srv = ThreadingHTTPServer((HOST, port), Handler)
    print(f"西游·数据 API 已启动： http://{HOST}:{port}  （数据集 {len(_list_datasets())} 个）")
    print("  按 Ctrl+C 停止。")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")


if __name__ == "__main__":
    main()
