"""W535：GoatCounter 取数自动化 — 决策闸门（W465/W530）的 Step 2 输入。

把「人工登后台抄 UV」换成一条命令，让 judge_gate.py 的判定可随时复算。

接口依据（2026-08-30 核对官方 OpenAPI https://www.goatcounter.com/api.json ，勿凭记忆改）：

    GET /api/v0/stats/total?start=YYYY-MM-DD&end=YYYY-MM-DD
    鉴权：Authorization: Bearer <token>，Content-Type: application/json
    响应：{ stats: [...], total: <访客数·含 events>, total_events: <事件访客数>, total_utc }
    401 = 密钥缺失或错误；403 = 权限不足；限流 4 req/s（本脚本每次仅 2 请求）

页面访客 UV = total - total_events（GoatCounter 把事件访客计入 total，闸门口径要的是页面访客）。

时间窗口径：end = 今天（UTC 日期），近 N 日 = [today-(N-1), today] 闭区间，即「含今天在内的 N 天」。

令牌来源：环境变量 GOATCOUNTER_API_TOKEN，或仓库根 .env（已 gitignore，禁止入库）。
生成方式：GoatCounter 后台右上角用户名 → API → 生成密钥。

用法：
    py -3 scripts/fetch_gate_stats.py                     # 输出 uv7 / uv30 + 推荐命令
    py -3 scripts/fetch_gate_stats.py --json              # 机器可读输出
    py -3 scripts/fetch_gate_stats.py --self-test         # 离线负样本自测（不联网）
    py -3 scripts/fetch_gate_stats.py --fixture <file>    # 用本地响应样本离线演练
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
DEFAULT_SITE = "https://1273984347.goatcounter.com"
TOKEN_KEY = "GOATCOUNTER_API_TOKEN"
TIMEOUT = 30


class FetchError(Exception):
    """取数失败（令牌缺失 / 鉴权 / 网络 / 响应结构异常）。"""


# ---------- 令牌 ----------

def load_token() -> str:
    tok = (os.environ.get(TOKEN_KEY) or "").strip()
    if tok:
        return tok
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line.startswith(f"{TOKEN_KEY}="):
                tok = line.split("=", 1)[1].strip().strip('"').strip("'")
                if tok:
                    return tok
    raise FetchError(
        f"未找到 GoatCounter API 令牌。请生成后写入仓库根 .env（已 gitignore，不要入库）：\n"
        f"    {TOKEN_KEY}=你的密钥\n"
        f"生成路径：GoatCounter 后台 → 右上角用户名 → API → 生成密钥"
    )


# ---------- 时间窗 ----------

def windows(today: date) -> tuple[tuple[str, str], tuple[str, str]]:
    """返回 (近7日, 近30日) 的 (start, end) 闭区间日期串，end = today。"""
    end = today.isoformat()
    return ((today - timedelta(days=6)).isoformat(), end), \
           ((today - timedelta(days=29)).isoformat(), end)


# ---------- 解析（纯函数，便于离线自测） ----------

def parse_total(payload: dict) -> int:
    """从 /stats/total 响应取「页面访客数」。缺字段 / 负值 / 结构异常一律 FetchError。"""
    if not isinstance(payload, dict):
        raise FetchError(f"响应不是 JSON 对象：{type(payload).__name__}")
    if "error" in payload:
        raise FetchError(f"API 返回错误：{payload['error']}")
    if "errors" in payload:
        raise FetchError(f"API 返回错误：{json.dumps(payload['errors'], ensure_ascii=False)}")
    for key in ("total", "total_events"):
        if key not in payload:
            raise FetchError(f"响应缺字段 `{key}`（接口结构可能与 2026-08-30 核对的 OpenAPI 不一致，需重新核对）")
        if not isinstance(payload[key], int):
            raise FetchError(f"字段 `{key}` 不是整数：{payload[key]!r}")
    total, events = payload["total"], payload["total_events"]
    if events > total:
        raise FetchError(f"total_events({events}) > total({total})，无法计算页面访客数")
    return total - events


# ---------- 取数 ----------

def http_error_msg(code: int, body: str) -> str:
    """HTTP 错误 → 可操作中文提示（独立成函数以便离线自测）。"""
    if code in (401, 403):
        return (f"鉴权失败（HTTP {code}）{body}。401=密钥缺失或错误，403=权限不足；"
                f"请到 GoatCounter 后台重新生成密钥并更新 .env 的 {TOKEN_KEY}")
    return f"HTTP {code}：{body}"


def http_json(url: str, token: str) -> dict:
    _u = urllib.parse.urlparse(url)
    if _u.scheme != "https" or not (_u.hostname or "").endswith(".goatcounter.com"):
        raise ValueError("W536 guard: unexpected endpoint: %s" % url)
    import ipaddress as _ipa
    import socket
    for _info in socket.getaddrinfo(_u.hostname, None):
        _ip = _ipa.ip_address(_info[4][0])
        if _ip.is_private or _ip.is_loopback or _ip.is_link_local or _ip.is_reserved or _ip.is_multicast or _ip.is_unspecified:
            raise ValueError("W536 guard: endpoint resolves to private address: %s" % _ip)
    req = urllib.request.Request(
        url,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")[:200]
        except Exception:
            pass
        raise FetchError(http_error_msg(e.code, body)) from e
    except urllib.error.URLError as e:
        raise FetchError(f"网络不可达：{e.reason}（如本机 TLS/代理异常，可换机器或热点重试）") from e
    except json.JSONDecodeError as e:
        raise FetchError(f"响应不是合法 JSON：{e}") from e


def fixture_fetcher(path: Path):
    """离线演练：用本地 JSON 文件代替网络请求（按调用顺序返回 7 日 / 30 日样本）。"""
    payloads = [json.loads(Path(p).read_text(encoding="utf-8")) for p in path]

    def _fake(url: str, token: str) -> dict:
        if not payloads:
            raise FetchError("fixture 样本已用尽")
        return payloads.pop(0)

    return _fake


def collect(fetch, token: str, start7: str, end7: str, start30: str, end30: str) -> dict:
    base = DEFAULT_SITE.rstrip("/")
    p7 = fetch(f"{base}/api/v0/stats/total?start={start7}&end={end7}", token)
    p30 = fetch(f"{base}/api/v0/stats/total?start={start30}&end={end30}", token)
    return {
        "uv7": parse_total(p7),
        "uv30": parse_total(p30),
        "window7": [start7, end7],
        "window30": [start30, end30],
        "raw7": {"total": p7.get("total"), "total_events": p7.get("total_events")},
        "raw30": {"total": p30.get("total"), "total_events": p30.get("total_events")},
    }


# ---------- 自测（离线·负样本优先） ----------

def self_test() -> int:
    cases, failed = [], 0

    def check(name: str, ok: bool, detail: str = "") -> None:
        nonlocal failed
        cases.append((name, ok, detail))
        if not ok:
            failed += 1

    # 1 时间窗：含今天的闭区间
    (s7, e7), (s30, e30) = windows(date(2026, 8, 30))
    check("时间窗 7 日闭区间", (s7, e7) == ("2026-08-24", "2026-08-30"), f"{s7}~{e7}")
    check("时间窗 30 日闭区间", (s30, e30) == ("2026-08-01", "2026-08-30"), f"{s30}~{e30}")

    # 2 正样本：total 120 / events 20 → 100
    check("正样本 UV 计算", parse_total({"total": 120, "total_events": 20}) == 100)
    check("零事件 UV", parse_total({"total": 7, "total_events": 0}) == 7)

    # 3 负样本：结构异常必须被抓到
    for name, payload in [
        ("缺 total 字段", {"total_events": 3}),
        ("缺 total_events 字段", {"total": 10}),
        ("total 非整数", {"total": "12", "total_events": 0}),
        ("事件数大于总数", {"total": 5, "total_events": 9}),
        ("API 返回 error", {"error": "unauthorized"}),
        ("响应非对象", ["x"]),
    ]:
        try:
            parse_total(payload)
            check(f"负样本·{name}", False, "未抛错（漏检）")
        except FetchError as e:
            check(f"负样本·{name}", True, str(e)[:48])

    # 4 缺令牌必须给出可操作提示（不联网）
    saved = os.environ.pop(TOKEN_KEY, None)
    try:
        try:
            load_token()
            check("负样本·缺令牌", False, "未抛错（漏检）")
        except FetchError as e:
            check("负样本·缺令牌", "GoatCounter 后台" in str(e) and TOKEN_KEY in str(e), str(e)[:48])
    finally:
        if saved is not None:
            os.environ[TOKEN_KEY] = saved

    # 5 401/403 必须转成可操作中文提示（含后台路径与令牌键名）
    for code in (401, 403):
        msg = http_error_msg(code, "")
        check(f"负样本·HTTP {code} 提示", "GoatCounter 后台" in msg and TOKEN_KEY in msg, msg[:48])
    check("负样本·HTTP 500 不误报为鉴权", "鉴权失败" not in http_error_msg(500, ""))

    for name, ok, detail in cases:
        print(f"{'OK  ' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))
    print(f"\n自测 {len(cases) - failed}/{len(cases)} 通过")
    return 1 if failed else 0


# ---------- CLI ----------

def main(argv: list[str] | None = None) -> int:
    global DEFAULT_SITE
    ap = argparse.ArgumentParser(description="GoatCounter 取数（决策闸门 Step 2 输入）")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    ap.add_argument("--self-test", action="store_true", help="离线负样本自测")
    ap.add_argument("--fixture", nargs=2, metavar=("F7", "F30"), help="用本地响应样本离线演练")
    ap.add_argument("--site", default=DEFAULT_SITE, help=f"站点地址（默认 {DEFAULT_SITE}）")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    DEFAULT_SITE = args.site

    try:
        fetch = fixture_fetcher(args.fixture) if args.fixture else http_json
        token = "FIXTURE" if args.fixture else load_token()
        (s7, e7), (s30, e30) = windows(date.today())
        data = collect(fetch, token, s7, e7, s30, e30)
    except FetchError as e:
        print(f"FAIL {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"近 7 日 UV  ：{data['uv7']}（{s7} ~ {e7}）")
        print(f"近 30 日 UV ：{data['uv30']}（{s30} ~ {e30}）")
        print(f"原始（含事件）：7 日 total={data['raw7']['total']} events={data['raw7']['total_events']}"
              f" · 30 日 total={data['raw30']['total']} events={data['raw30']['total_events']}")
        print(f"\n下一步（判定）：py -3 scripts/judge_gate.py "
              f"--uv7 {data['uv7']} --uv30 {data['uv30']} --report")
    return 0


if __name__ == "__main__":
    sys.exit(main())
