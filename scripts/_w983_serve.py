#!/usr/bin/env python3
"""_w983_serve.py — W983 本地验收用静态服务（补 webp/js/css MIME·避免浏览器拒渲染）

用法：py -3 scripts/_w983_serve.py [端口] [根目录]
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
