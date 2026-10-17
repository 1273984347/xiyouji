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

# -------------------------------------------------------------------
# 路径与端口常量
# -------------------------------------------------------------------

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
DATASET_DIR = os.path.join(ROOT, "dataset")

PORT = 8787
HOST = "127.0.0.1"

# CORS 白名单（P3-2）：仅 file://（Origin:null）与本地 API 源放行
_CORS_FILE_ORIGIN = "null"
_CORS_LOCAL_ORIGINS = ("http://127.0.0.1:8787", "http://localhost:8787")
# W681：白名单命中后回显固定常量而非请求头原值（防头注入污点流）
_CORS_RESPONSE_ORIGIN = "http://127.0.0.1:8787"

# 静态资源扩展名 → Content-Type 映射
_MIME_TYPES = {
    "html": "text/html; charset=utf-8",
    "css": "text/css; charset=utf-8",
    "js": "application/javascript; charset=utf-8",
    "json": "application/json; charset=utf-8",
    "webmanifest": "application/manifest+json",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
    "svg": "image/svg+xml",
    "woff2": "font/woff2",
    "woff": "font/woff",
    "ttf": "font/ttf",
}
_DEFAULT_MIME = "application/octet-stream"

# 递归检索片段上下文窗口（字符）
_SNIPPET_BEFORE = 20
_SNIPPET_AFTER = 40
# 单数据集最多返回的命中条数
_HITS_PER_DATASET_LIMIT = 20


# -------------------------------------------------------------------
# 数据集读写
# -------------------------------------------------------------------

def _list_datasets():
    """扫描 dataset/*.json，返回 [{name,keys,title,size_kb}, ...]。"""
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
    """读取 dataset/<name>.json；路径非法/不存在/解析失败返回 None。

    W681 CodeQL 处置：realpath 边界校验（防 ../ 逃逸读仓外文件）。
    """
    root_real = os.path.realpath(DATASET_DIR)
    p = os.path.realpath(os.path.join(root_real, name + ".json"))
    if not (p == root_real or p.startswith(root_real + os.sep)) or not p.endswith(".json"):
        return None
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
            start = max(0, idx - _SNIPPET_BEFORE)
            end = min(len(obj), idx + len(q) + _SNIPPET_AFTER)
            snippet = ("…" if start > 0 else "") + obj[start:end] + ("…" if end < len(obj) else "")
            hits.append({"path": path, "snippet": snippet})
    return hits


# -------------------------------------------------------------------
# 图谱数据（图集注册表，W339 知识图谱探索器）
# -------------------------------------------------------------------

def _load_yuanqi_graph():
    d = _load_dataset("yuanqi-graph")
    if not isinstance(d, dict) or "nodes" not in d:
        return None
    return d


def _load_char_graph():
    d = _load_dataset("character-relationship-3d")
    if not isinstance(d, dict):
        return None
    nodes = [
        {
            "id": n.get("id"),
            "label": n.get("name", n.get("id")),
            "group": str(n.get("group", "")),
            "desc": n.get("desc", ""),
            "importance": n.get("importance", 0),
        }
        for n in d.get("nodes", []) if isinstance(n, dict)
    ]
    edges = [
        {
            "source": e.get("source"),
            "target": e.get("target"),
            "relation": e.get("type", ""),
            "property": "",
            "value": "",
        }
        for e in d.get("links", []) if isinstance(e, dict)
    ]
    return {
        "meta": {
            "title": "取经团队人物关系图谱（3D 投影）",
            "note": "取经五人 + 关键神佛妖魔的关系网络（group=阵营/身份）。",
            "schema": "graph",
            "group_colors": {},
            "dimensions": [],
        },
        "nodes": nodes,
        "edges": edges,
    }


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
        out.append({
            "name": name,
            "title": reg.get("title", name),
            "node_count": len(g.get("nodes", [])),
            "edge_count": len(g.get("edges", [])),
        })
    return out


# -------------------------------------------------------------------
# HTML 文档页
# -------------------------------------------------------------------

def _render_dataset_row(d: dict) -> str:
    """渲染文档页数据表单行。"""
    keys = d["keys"]
    keys_head = ", ".join(keys[:6])
    keys_suffix = " …" if len(keys) > 6 else ""
    return (
        f"<tr><td><code>{d['name']}</code></td><td>{d['size_kb']} KB</td>"
        f"<td>{d['title'] or '—'}</td>"
        f"<td><code>{keys_head}{keys_suffix}</code></td></tr>"
    )


def _doc_html():
    """API 文档页（HTML），逐字保留原有样式与结构。"""
    ds = _list_datasets()
    rows = "".join(_render_dataset_row(d) for d in ds)
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


# -------------------------------------------------------------------
# HTTP 请求处理器
# -------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    # ---- CORS ----

    def _cors_origin(self):
        """CORS 白名单——仅回显 file://（Origin:null）与本地 API 源，其余不带 CORS 头。"""
        origin = self.headers.get("Origin", "")
        if origin == _CORS_FILE_ORIGIN:
            return _CORS_FILE_ORIGIN
        if origin in _CORS_LOCAL_ORIGINS:
            return _CORS_RESPONSE_ORIGIN
        return None

    # ---- 响应封装 ----

    def _send(self, obj, code=200, ctype="application/json; charset=utf-8"):
        """把 obj 序列化并发送响应，附带 CORS 头。"""
        if isinstance(obj, (dict, list)):
            body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        else:
            body = obj.encode("utf-8") if isinstance(obj, str) else obj
            ctype = ctype or _DEFAULT_MIME
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        cors = self._cors_origin()
        if cors:
            self.send_header("Access-Control-Allow-Origin", cors)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, message: str, try_hint: str | None = None, code: int = 404):
        """发送 {"error": message[, "try": hint]} 结构。"""
        payload = {"error": message}
        if try_hint is not None:
            payload["try"] = try_hint
        self._send(payload, code=code)

    # ---- 路由处理 ----

    def _handle_openapi(self):
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

    def _handle_search(self, q):
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
                res.append({
                    "dataset": d["name"],
                    "hit_count": len(hits),
                    "hits": hits[:_HITS_PER_DATASET_LIMIT],
                })
        self._send({"query": kw, "matches": len(res), "results": res})

    def _handle_graph(self, gparts):
        if len(gparts) == 1:
            self._send(_list_graphs())
            return
        g = _load_graph(gparts[1])
        if g is None:
            self._send_error_json(f"graph not found: {gparts[1]}", try_hint="/graph")
        else:
            self._send(g)

    def _handle_dataset(self, parts):
        name = parts[1]
        data = _load_dataset(name)
        if data is None:
            self._send_error_json(f"dataset not found: {name}")
            return
        if len(parts) == 3 and parts[2] == "keys":
            meta = data.get("meta") if isinstance(data, dict) else None
            self._send({
                "name": name,
                "keys": list(data.keys()) if isinstance(data, dict) else [],
                "meta": meta,
            })
            return
        self._send(data)

    # ---- 静态资源 ----

    def _serve_static(self, path: str) -> bool:
        """尝试把 path 作为 site/ 下的静态文件返回；成功返回 True。"""
        static_path = self._resolve_static(path)
        if not static_path:
            return False
        try:
            with open(static_path, "rb") as f:
                body = f.read()
        except Exception:
            return False
        self.send_response(200)
        self.send_header("Content-Type", self._ctype(static_path))
        cors = self._cors_origin()
        if cors:
            self.send_header("Access-Control-Allow-Origin", cors)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        return True

    # ---- 主入口 ----

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        q = urllib.parse.parse_qs(parsed.query)

        # 固定路径路由
        if path in ("/api", "/docs"):
            self._send(_doc_html(), ctype="text/html; charset=utf-8")
            return
        if path == "/health":
            self._send({"status": "ok", "datasets": len(_list_datasets())})
            return
        if path == "/openapi.json":
            self._handle_openapi()
            return
        if path == "/datasets":
            self._send(_list_datasets())
            return
        if path == "/search":
            self._handle_search(q)
            return

        # /graph 图集列举 与 /graph/<name> 单图（W339 知识图谱探索器）
        gparts = [p for p in path.split("/") if p]
        if gparts and gparts[0] == "graph":
            self._handle_graph(gparts)
            return

        # /dataset/<name> 或 /dataset/<name>/keys
        parts = [p for p in path.split("/") if p]
        if len(parts) >= 2 and parts[0] == "dataset":
            self._handle_dataset(parts)
            return

        # 静态资源：API 路由未命中时，尝试从 site/ 提供（让 API 同时托管前端）
        if self._serve_static(path):
            return

        self._send_error_json("not found", try_hint="/datasets")

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
        """扩展名 → Content-Type；未知返回 application/octet-stream。"""
        ext = os.path.splitext(p)[1].lower().lstrip(".")
        return _MIME_TYPES.get(ext, _DEFAULT_MIME)

    def log_message(self, *args):
        """禁用 BaseHTTPRequestHandler 默认 stderr 访问日志。"""
        pass


# -------------------------------------------------------------------
# 启动
# -------------------------------------------------------------------

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
