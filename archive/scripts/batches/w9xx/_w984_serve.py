#!/usr/bin/env python3
"""_w984_serve.py — W983 本地验收用静态服务（补 webp/js/css MIME·避免浏览器拒渲染）

用法：py -3 scripts/_w984_serve.py [端口] [根目录]
默认：8765 · site/
"""
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(SimpleHTTPRequestHandler):
    extensions_map = dict(SimpleHTTPRequestHandler.extensions_map)
    extensions_map.update({
        ".webp": "image/webp",
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".css": "text/css",
        ".json": "application/json",
        ".svg": "image/svg+xml",
        ".woff2": "font/woff2",
    })

    def end_headers(self):
        # 本地验收必须禁用缓存：否则浏览器会复用旧副本 ⇒「改了页面却看不到变化」的假象
        # （W984 实证：同一 URL 反复验收时命中旧 HTML，误判题图「没渲染」；加随机 query 也不保险）
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        SimpleHTTPRequestHandler.end_headers(self)

    def log_message(self, fmt, *args):
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    base = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "site")
    os.chdir(base)
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("serving %s at http://127.0.0.1:%d/ (Ctrl+C to stop)" % (base, port), flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
