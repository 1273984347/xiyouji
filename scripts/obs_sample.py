#!/usr/bin/env python3
"""obs_sample.py — OBS-10/11/14 逐批采样件（W850 建·Q2 裁决的取数入口）。

## 为什么需要它

架构方案 §12.2 的 Q2 悬而未决：「OBS-10–OBS-14 三条新指标何时从告警级升为硬门槛」，
倾向答案是「连续 10 个批次实测稳定后再升」。问题是——**这 10 批样本此前没有任何采集
机制**：OBS-10 只有 perf_monitor.py 的预算校验（且其 html 预算是 2026-07-30 的 50 KB，
与现役页面体量早已脱节，见下）；OBS-11 只在 CI 的 perf.yml 里跑；OBS-14 只有 agent-web
服务运行时的进程内窗口。没有逐批记录，Q2 就只能一直「等样本」。

本件把「每批收尾记一次」变成一条命令，三条指标分别计数、分别达标判断。

## 三条指标与取数方式

| 指标 | 口径（架构方案） | 取数 | 默认 |
|:--|:--|:--|:--|
| OBS-10 | 单页 HTML ≤ 200 KB（§8.3） | 静态扫 `site/**/*.html`，秒级 | **开** |
| OBS-11 | 首屏 LCP < 1.5 s（§11.5 SLO） | `--lcp`：复用 `perf_monitor.py` + playwright 测 perf.yml 五页，**每页 3 次取中位数** | 关（浏览器 ~8 s/页×3） |
| OBS-14 | 问答首 token < 2 s（§11.5 SLO） | `--first-token`：读 agent-web `/api/metrics` 的滚动窗口 | 关（需服务在跑） |

## 口径纪律（本件的核心约束）

- **不猜数**：没测就记 `measured=false` + `reason`，绝不用估值或上一次的值顶替。
  OBS-11 尤其如此——`perf_monitor.py` 在无 playwright 时会降级为启发式估算并给页面
  打 `_heuristic` 标记，本件见到该标记**拒绝入样**（估算值进基线 = 基线从第一笔就是假的）。
- **单次实测不作数**：OBS-11 每页跑 3 次取中位数。W850 实测教训：同机三连测 dashboard
  的 LCP 分别 116 / 1140 / 104 ms——单次 spike 能把结论从「远低于 SLO」扭成「贴近 SLO」。
  原始三轮值一并入库（`runs_ms`），中位数进 `pages`，趋势看中位数、方差看原始值。
- **不补历史**：样本只能一批一批长出来，不为凑 10 批回填。
- **不判红**：本件只记录与陈述。阈值要不要升为硬门槛，是 Q2 的用户裁决，不是脚本裁决。
- **按指标分别计数**：三条的「10 批」各自独立——OBS-14 可能长期只有 2 批有样本，
  那就如实显示 2/10，不拿 OBS-10 的批次数充数。

## 用法

    python scripts/obs_sample.py --record                 # 每批收尾跑（OBS-10 静态量）
    python scripts/obs_sample.py --record --lcp           # 顺带采 LCP（浏览器）
    python scripts/obs_sample.py --record --first-token   # 顺带采首 token（服务在跑时）
    python scripts/obs_sample.py --status                 # 看三条各自的样本进度
    python scripts/obs_sample.py --self-test              # 判据自测

退出码：OK 0 · 采样/解析异常 1。
"""

import json
import os
import statistics
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, ".."))
SITE = os.path.join(ROOT, "site")
SAMPLES = os.path.join(ROOT, "scripts", "output", "obs_samples.json")
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
PERF_MONITOR = os.path.join(_HERE, "perf_monitor.py")

TARGET_BATCHES = 10  # Q2：连续 10 批稳定后再议升硬门槛

# 架构方案 §8.3 / §11.5 的口径（只陈述，不作为判红依据）
OBS10_BUDGET_BYTES = 200 * 1024
OBS11_SLO_MS = 1500
OBS14_SLO_MS = 2000

# 与 perf.yml collect.url 同集的五页（OBS-11 采样面）
LCP_PAGES = ("dashboard.html", "index.html", "data/timeline.html",
             "data/character-relationship-3d.html", "data/text-search.html")

# OBS-11 每页重复测量次数，取中位数（W850 实测教训：单次 LCP 在本机方差极大——
# 同机三连测 dashboard 分别 116 / 1140 / 104 ms，一次 spike 能把结论从「远低于 SLO」
# 扭成「贴近 SLO」。Lighthouse 自身也是多跑取中位，此处对齐该口径）。
LCP_RUNS = 3

DEFAULT_PORT = 3000


def measure_page_size(site_dir=SITE):
    """OBS-10：全站单页 HTML 字节最大值 + 超预算页数（静态·秒级）。"""
    sizes = []
    total = 0
    for root, _dirs, files in os.walk(site_dir):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            try:
                s = os.path.getsize(p)
            except OSError:
                continue
            total += s
            sizes.append((s, os.path.relpath(p, site_dir).replace(os.sep, "/")))
    if not sizes:
        raise SystemExit("OBS-10 采样失败：%s 下无 HTML 页面" % site_dir)
    sizes.sort(reverse=True)
    return {
        "measured": True,
        "max_bytes": sizes[0][0],
        "max_page": sizes[0][1],
        "over_budget_pages": sum(1 for s, _ in sizes if s > OBS10_BUDGET_BYTES),
        "total_pages": len(sizes),
        "total_bytes": total,
        "budget_bytes": OBS10_BUDGET_BYTES,
    }


def measure_lcp(site_dir=SITE, timeout=240, runs=LCP_RUNS):
    """OBS-11：复用 perf_monitor.py 实测五页 LCP（ms），每页跑 runs 次取中位数。

    返回 (数据, 拒绝原因)。拒收三类非实测：
    ① playwright 不可用导致 perf_monitor 降级启发式（页内 `_heuristic`）；
    ② 单页采集异常（该页无 LCP 值）；
    ③ 采集面缺页——宁缺勿假。
    中位数口径见 LCP_RUNS 注释：单次实测方差太大， spike 不得入基线。
    """
    raw = {}       # rel -> [每次运行的 ms]
    for rel in LCP_PAGES:
        path = os.path.join(site_dir, rel)
        if not os.path.isfile(path):
            return None, "缺页 %s（perf.yml 采集面不完整）" % rel
        vals = []
        for i in range(runs):
            with tempfile.TemporaryDirectory(prefix="obslcp_") as td:
                out = os.path.join(td, "r.json")
                try:
                    subprocess.run([sys.executable, PERF_MONITOR, "--target", path,
                                    "--json", out],
                                   capture_output=True, text=True, timeout=timeout,
                                   check=False)
                except Exception as e:  # 超时/启动失败等
                    return None, "perf_monitor 执行异常（%s）" % e
                if not os.path.isfile(out):
                    return None, "perf_monitor 未产出 JSON（%s 第 %d 次）" % (rel, i + 1)
                data = json.load(open(out, encoding="utf-8"))
            page = data.get("pages", {}).get(rel.replace(os.sep, "/"), {})
            if not page:
                page = data.get("pages", {}).get(os.path.basename(rel), {})
            if page.get("_heuristic"):
                return None, "playwright 不可用·perf_monitor 降级为启发式估算——估算值不入基线"
            lcp = page.get("LCP")
            if lcp is None:
                return None, "%s 无 LCP 实测值（第 %d 次）" % (rel, i + 1)
            vals.append(round(float(lcp) * 1000, 1))  # s → ms
        raw[rel] = vals
    pages = {rel: round(statistics.median(v), 1) for rel, v in raw.items()}
    return {"measured": True, "pages": pages, "runs": runs,
            "runs_ms": raw, "max_ms": max(pages.values()),
            "slo_ms": OBS11_SLO_MS,
            "engine": "perf_monitor.py + playwright（无节流本机口径·每页 %d 次取中位数）" % runs}, None


def measure_first_token(port=DEFAULT_PORT, token=None, timeout=5):
    """OBS-14：读 agent-web `/api/metrics` 的首 token 滚动窗口。返回 (数据, 原因)。

    **绕过代理**：urllib 默认吃 HTTP_PROXY/HTTPS_PROXY 环境变量——本机 127.0.0.1 的
    探测会被代理截走（W850 实测：端口没人听时代理返回 502，于是「不可达」被误报成
    「服务返回 HTTP 502」）。localhost 探测必须显式清空 ProxyHandler。
    """
    url = "http://127.0.0.1:%d/api/metrics" % port
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", "Bearer %s" % token)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=timeout) as r:
            body = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return None, "服务需 token（--token 或环境变量 OBS_SAMPLE_TOKEN）"
        return None, "服务返回 HTTP %d" % e.code
    except Exception as e:
        return None, "agent-web 服务不可达（%s:%d·%s）" % ("127.0.0.1", port, type(e).__name__)
    ft = body.get("first_token") or {}
    if not ft or not ft.get("count"):
        return None, "服务在跑但窗口无样本（尚无问答流量·窗口上限 %s）" % ft.get("window")
    return {"measured": True, "count": ft.get("count"), "p50_ms": ft.get("p50"),
            "p95_ms": ft.get("p95"), "max_ms": ft.get("max"),
            "slo_ms": ft.get("sloMs", OBS14_SLO_MS)}, None


def _skip(metric, reason):
    return {"measured": False, "reason": reason}


def _load(path=SAMPLES):
    if not os.path.isfile(path):
        return {"schema": 1, "target_batches": TARGET_BATCHES, "samples": []}
    data = json.load(open(path, encoding="utf-8"))
    data.setdefault("schema", 1)
    data.setdefault("target_batches", TARGET_BATCHES)
    data.setdefault("samples", [])
    return data


def _current_batch():
    if not os.path.isfile(CHANGELOG):
        return None
    import re
    m = re.search(r"^### W(\d+)（", open(CHANGELOG, encoding="utf-8").read(), re.M)
    return "W%s" % m.group(1) if m else None


def record(batch, with_lcp=False, with_first_token=False, port=DEFAULT_PORT,
           token=None, path=SAMPLES):
    """写入/更新本批样本（同批重跑覆盖）。返回样本 dict。"""
    obs11, obs11_reason = (measure_lcp() if with_lcp else (None, None))
    obs14, obs14_reason = (measure_first_token(port, token) if with_first_token
                           else (None, None))
    sample = {
        "batch": batch,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "captured_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "obs10": measure_page_size(),
        "obs11": obs11 if obs11 else _skip(
            "obs11", obs11_reason or "未测（需 --lcp·默认不跑浏览器）"),
        "obs14": obs14 if obs14 else _skip(
            "obs14", obs14_reason or "未测（需 --first-token·默认不读服务）"),
    }
    data = _load(path)
    data["samples"] = [s for s in data["samples"] if s.get("batch") != batch]
    data["samples"].append(sample)
    data["samples"].sort(key=lambda s: int(str(s.get("batch", "W0"))[1:] or 0))
    data["note"] = ("OBS-10/11/14 逐批采样（W850 建·Q2 取数入口）：未测即记 null+原因，"
                    "按指标分别计 10 批；不判红，阈值升降由 Q2 裁决。")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return sample


def _progress(data, key):
    n = sum(1 for s in data["samples"] if s.get(key, {}).get("measured"))
    return n


def status(path=SAMPLES):
    """打印三条指标各自的样本进度（陈述式·不判红）。"""
    data = _load(path)
    samples = data["samples"]
    print("OBS 采样进度（目标 %d 批·按指标分别计数）" % TARGET_BATCHES)
    for key, label, _thr in (("obs10", "OBS-10 单页 HTML ≤200 KB", "%d B" % OBS10_BUDGET_BYTES),
                            ("obs11", "OBS-11 LCP <1.5 s", "%d ms" % OBS11_SLO_MS),
                            ("obs14", "OBS-14 首 token <2 s", "%d ms" % OBS14_SLO_MS)):
        n = _progress(data, key)
        line = "  %-28s %2d/%d 批有样本" % (label, n, TARGET_BATCHES)
        latest = samples[-1].get(key, {}) if samples else {}
        if latest.get("measured"):
            if key == "obs10":
                line += " · 最新最大 %s B（%s）· 超限 %d 页 / %d 页" % (
                    "{:,}".format(latest["max_bytes"]), latest["max_page"],
                    latest["over_budget_pages"], latest["total_pages"])
            elif key == "obs11":
                line += " · 最新最大 %s ms（%s 口径）" % (latest["max_ms"], latest["engine"])
            else:
                line += " · 最新 p50 %s ms / p95 %s ms（count=%s）" % (
                    latest["p50_ms"], latest["p95_ms"], latest["count"])
        elif latest.get("reason"):
            line += " · 上一批：%s" % latest["reason"]
        print(line)
    if samples:
        print("  样本批：%s" % "、".join(s["batch"] for s in samples))
        print("  权威值以本文件为准（段内/台账数字为落盘时点快照）")
    return 0


def _self_test():
    """7 例：OBS-10 量测 / 超预算计数 / OBS-11 拒收启发式 / OBS-11 中位数去 spike / OBS-14 不可达 / 记录去重 / 进度计数。"""
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer

    cases = []
    tmp = tempfile.mkdtemp(prefix="obssample_")
    site = os.path.join(tmp, "site")
    os.makedirs(os.path.join(site, "data"), exist_ok=True)
    open(os.path.join(site, "small.html"), "w").write("x" * 1000)
    open(os.path.join(site, "big.html"), "w").write("x" * (OBS10_BUDGET_BYTES + 10))
    open(os.path.join(site, "data", "mid.html"), "w").write("x" * 50000)

    m = measure_page_size(site)
    cases.append(("T1 OBS-10：最大值取最大页·页数 3", m["max_bytes"] == OBS10_BUDGET_BYTES + 10
                  and m["total_pages"] == 3))
    cases.append(("T2 OBS-10：超 200 KB 计数=1（不含 50 KB 中页）",
                  m["over_budget_pages"] == 1))

    # T3：伪造 perf_monitor 输出带 _heuristic → 必须拒收
    fake = os.path.join(tmp, "fake_perf_monitor.py")
    pages = ",".join("'%s':{'LCP':1.2,'_heuristic':True}" % r for r in LCP_PAGES)
    open(fake, "w").write(
        "import json,sys;"
        "out=sys.argv[sys.argv.index('--json')+1];"
        "json.dump({'pages':{%s}},open(out,'w'))" % pages)
    global PERF_MONITOR
    real_pm = PERF_MONITOR
    PERF_MONITOR = fake
    for rel in LCP_PAGES:  # 五页都要在，否则先被「缺页」拦下、走不到启发式分支
        d = os.path.join(site, os.path.dirname(rel))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(site, rel), "w").write("<html></html>")
    got, reason = measure_lcp(site)
    PERF_MONITOR = real_pm
    cases.append(("T3 OBS-11：启发式估算值拒收入样", got is None and "启发式" in reason))

    # T3b：每页 3 次取中位数——spike 不得把结论带偏（W850 实测：同机三连测 dashboard
    # 116 / 1140 / 104 ms，单次取值时基线完全被噪声支配）。假监视器按调用次序返回值。
    sidecar = os.path.join(tmp, "state.json")
    with open(sidecar, "w") as f:
        json.dump({"pages": {os.path.basename(r):
                             ([0.1, 1.1, 0.2] if r == "dashboard.html" else [0.3, 0.3, 0.3])
                             for r in LCP_PAGES}, "calls": {}}, f)
    open(fake, "w").write(
        "import json,os,sys;"
        "st=json.load(open(os.environ['FAKE_SIDECAR']));"
        "t=sys.argv[sys.argv.index('--target')+1];"
        "k=os.path.basename(t);"
        "n=st['calls'].get(k,0);"
        "v=st['pages'][k][min(n,len(st['pages'][k])-1)];"
        "st['calls'][k]=n+1;"
        "json.dump(st,open(os.environ['FAKE_SIDECAR'],'w'));"
        "o=sys.argv[sys.argv.index('--json')+1];"
        "json.dump({'pages':{k:{'LCP':v}}},open(o,'w'))")
    os.environ["FAKE_SIDECAR"] = sidecar
    PERF_MONITOR = fake
    got2, reason2 = measure_lcp(site)
    PERF_MONITOR = real_pm
    os.environ.pop("FAKE_SIDECAR", None)
    cases.append(("T3b OBS-11：每页 3 次取中位数·spike 不入样（dashboard 中位 200 ms 非 1100 ms）",
                  got2 is not None and reason2 is None
                  and got2["pages"]["dashboard.html"] == 200.0
                  and got2["runs_ms"]["dashboard.html"] == [100.0, 1100.0, 200.0]
                  and got2["max_ms"] == 300.0))

    # T4：服务不可达 → measured=false + 原因（不猜数）
    got, reason = measure_first_token(port=59999, timeout=2)
    cases.append(("T4 OBS-14：服务不可达记原因不记值",
                  got is None and "不可达" in reason))

    # T5：同批重跑覆盖 + 跨批累积 + 按指标计数
    base = os.path.join(tmp, "obs_samples.json")
    record("W850", path=base)
    record("W850", path=base)
    record("W851", with_first_token=True, port=59999, path=base)
    d = _load(base)
    cases.append(("T5 记录：同批覆盖不重复·跨批累积·obs14 只 1 批有样本但记的是 null",
                  [s["batch"] for s in d["samples"]] == ["W850", "W851"]
                  and _progress(d, "obs10") == 2 and _progress(d, "obs14") == 0))

    # T6：本地起一个假 /api/metrics → OBS-14 真取数成功
    class _H(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != "/api/metrics":
                self.send_response(404)
                self.end_headers()
                return
            body = json.dumps({"ok": True, "first_token": {
                "count": 12, "window": 100, "p50": 810, "p95": 1730, "max": 1900,
                "sloMs": 2000}}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):
            pass

    srv = HTTPServer(("127.0.0.1", 0), _H)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        got, reason = measure_first_token(port=port)
    finally:
        srv.shutdown()
    cases.append(("T6 OBS-14：真取数 count/p50/p95 落位",
                  got is not None and got["count"] == 12 and got["p50_ms"] == 810))

    ok = sum(1 for _, p in cases if p)
    for name, passed in cases:
        print("%s %s" % ("PASS" if passed else "FAIL", name))
    print("---- OBS 采样件自测：%d/%d ----" % (ok, len(cases)))
    return 0 if ok == len(cases) else 1


def main(argv):
    args = argv[1:]
    if "--self-test" in args:
        return _self_test()
    if "--status" in args:
        return status()
    port = DEFAULT_PORT
    if "--port" in args:
        port = int(args[args.index("--port") + 1])
    token = os.environ.get("OBS_SAMPLE_TOKEN")
    if "--token" in args:
        token = args[args.index("--token") + 1]
    batch = None
    if "--batch" in args:
        batch = args[args.index("--batch") + 1]
    batch = batch or _current_batch()
    if "--record" not in args:
        print("未指定动作：--record（记本批）/ --status（看进度）/ --self-test")
        return 1
    if not batch:
        raise SystemExit("--record 需要批次号（CHANGELOG 顶段解析失败）")
    sample = record(batch, "--lcp" in args, "--first-token" in args, port, token)
    print("%s 已写入 %s" % (batch, os.path.relpath(SAMPLES, ROOT)))
    for key in ("obs10", "obs11", "obs14"):
        v = sample[key]
        if v.get("measured"):
            if key == "obs10":
                print("  OBS-10 最大 %s B（%s）· 超 200 KB %d/%d 页"
                      % ("{:,}".format(v["max_bytes"]), v["max_page"],
                         v["over_budget_pages"], v["total_pages"]))
            elif key == "obs11":
                print("  OBS-11 最大 LCP %s ms" % v["max_ms"])
            else:
                print("  OBS-14 p50 %s ms / p95 %s ms（count=%s）"
                      % (v["p50_ms"], v["p95_ms"], v["count"]))
        else:
            print("  %s 未测：%s" % (key.upper(), v["reason"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
