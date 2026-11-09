"""W1153 回归锁 · rag_server CORS 白名单 + 限速 + 异常不回显（深度审计 #30）。

原缺陷：回环 RAG 服务 `Access-Control-Allow-Origin: *`（任意网页可跨域读取本仓
docs/source 片段）+ /route 500 回显内部异常（泄露本地路径/模型栈）+ 无速率限制。

运行：py -3 -m pytest tests/unit/test_w1153_rag_cors.py -v
"""
import importlib
import sys
import threading
import urllib.request
from pathlib import Path

SCRIPTS_RAG = Path(__file__).resolve().parent.parent.parent / "scripts" / "rag"
if str(SCRIPTS_RAG) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_RAG))

rs = importlib.import_module("rag_server")


def _stub_headers(origin):
    class _H:
        def get(self, k, d=""):
            return origin if k == "Origin" else d

    class _Stub:
        headers = _H()

    return _Stub()


def test_cors_whitelist():
    """正样本：file://(null) 与本地站点源回显·其余来源不带 CORS 头。"""
    h = rs.Handler.__new__(rs.Handler)
    h.headers = _stub_headers("null").headers
    assert h._cors_origin() == "null"
    h.headers = _stub_headers("http://127.0.0.1:8000").headers
    assert h._cors_origin() == rs._CORS_RESPONSE_ORIGIN
    h.headers = _stub_headers("https://evil.example").headers
    assert h._cors_origin() is None, "外域来源必须拿不到 CORS 头"
    h.headers = _stub_headers("").headers
    assert h._cors_origin() is None


def test_rate_limit():
    """限速：同 IP 窗口内超过阈值即拒。"""
    rs._rate_hits.clear()
    ok = [rs._rate_ok("1.2.3.4") for _ in range(rs._RATE_LIMIT)]
    assert all(ok), "阈值内必须全放行"
    assert rs._rate_ok("1.2.3.4") is False, "超阈值必须拒绝"
    assert rs._rate_ok("5.6.7.8") is True, "其他 IP 不受影响"


def test_route_error_no_internal_echo():
    """/route 异常只回固定文案（不回显 %s 异常详情）。"""
    import types

    rs._rate_hits.clear()

    def _boom(*a, **k):
        raise RuntimeError("D:\\xiyouji\\models\\secret-path 泄露探测")

    stub = types.ModuleType("page_router")
    stub.route = _boom
    stub.load_pages = lambda: []
    saved = sys.modules.get("page_router")
    sys.modules["page_router"] = stub
    try:
        h = rs.Handler.__new__(rs.Handler)
        h.path = "/route?q=x"
        h.client_address = ("127.0.0.1", 12345)
        h.headers = _stub_headers("null").headers
        captured = {}
        h._send = lambda obj, code=200: captured.update(obj=obj, code=code)
        h.do_GET()
        assert captured["code"] == 500
        assert captured["obj"] == {"error": "route failed"}, captured["obj"]
        assert "secret-path" not in str(captured["obj"]), "内部异常详情不得回显"
    finally:
        if saved is not None:
            sys.modules["page_router"] = saved
        else:
            sys.modules.pop("page_router", None)
