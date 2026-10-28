# -*- coding: utf-8 -*-
"""_w1005_serve.py — W1005 本地验收静态服务（webp/js/css MIME + no-store）

`_w983_serve.py` 已随 W977 一次性件退役批归档 ⇒ 本批临时补一个同口径的。
用法：py -3 scripts/_w1005_serve.py [端口] [根目录]
"""
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class H(SimpleHTTPRequestHandler):
    extensions_map = dict(SimpleHTTPRequestHandler.extensions_map)
    extensions_map.update({".webp": "image/webp", ".js": "text/javascript",
                           ".mjs": "text/javascript", ".css": "text/css",
                           ".json": "application/json", ".svg": "image/svg+xml"})

    def end_headers(self):
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
    print("serving %s at http://127.0.0.1:%d/" % (base, port))
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()


if __name__ == "__main__":
    main()
