"""obs_sample.py 逐批采样件测试（W850）。

背景：架构方案 §12.2 的 Q2（OBS-10/11/14 何时升硬门槛）一直「等连续 10 批样本」，
但此前没有任何采集机制。W850 建 obs_sample.py 把机制补上，本测试锁死它的四条核心
纪律：**不猜数**（没测就记 null+原因）、**不补历史**（样本只能一批批长）、
**不判红**（只记录，阈值升降归 Q2 裁决）、**单次实测不作数**（OBS-11 每页 3 次取
中位数——同机三连测 dashboard 116/1140/104 ms 的实测教训）。

跨平台纪律（pitfalls「latent 三问 + 双平台断言禁例」）：断言全部基于数值/字符串，
零 os.name/盘符/大小写语义；合成目录与本地 HTTP 桩注入，不触真实仓库数据。
"""

import json
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import obs_sample as obs  # noqa: E402

SCRIPT = SCRIPTS / "obs_sample.py"


@pytest.fixture()
def site(tmp_path):
    """合成站点：1 页超 200 KB · 1 页 50 KB · 1 页 1 KB。"""
    s = tmp_path / "site"
    (s / "data").mkdir(parents=True)
    (s / "big.html").write_text("x" * (obs.OBS10_BUDGET_BYTES + 10))
    (s / "data" / "mid.html").write_text("x" * 50000)
    (s / "small.html").write_text("x" * 1000)
    return s


def _write_fake_monitor(tmp_path, monkeypatch, payload):
    """把 PERF_MONITOR 换成一次性假脚本，返回指定 JSON（模拟 perf_monitor 输出）。"""
    fake = tmp_path / "fake_perf_monitor.py"
    pages = ",".join("'%s':%s" % (k, repr(v)) for k, v in payload.items())
    fake.write_text(
        "import json,sys\n"
        "out=sys.argv[sys.argv.index('--json')+1]\n"
        "json.dump({'pages':{%s}},open(out,'w'))\n" % pages,
        encoding="utf-8")
    monkeypatch.setattr(obs, "PERF_MONITOR", str(fake))


def _full_site(site):
    """补足 LCP 采样面的五页（measure_lcp 按 perf.yml 采集集逐页取数）。"""
    for rel in obs.LCP_PAGES:
        p = site / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            p.write_text("<html></html>", encoding="utf-8")
    return site


def test_obs10_max_and_over_budget(site):
    m = obs.measure_page_size(str(site))
    assert m["measured"] is True
    assert m["max_bytes"] == obs.OBS10_BUDGET_BYTES + 10
    assert m["max_page"] == "big.html"
    assert m["total_pages"] == 3
    assert m["over_budget_pages"] == 1  # 50 KB 中页不算超限


def test_obs11_rejects_heuristic(site, tmp_path, monkeypatch):
    """无 playwright 时 perf_monitor 会降级启发式并打 _heuristic —— 估算值不得入基线。"""
    _full_site(site)
    _write_fake_monitor(tmp_path, monkeypatch,
                        {rel: {"LCP": 1.2, "_heuristic": True} for rel in obs.LCP_PAGES})
    got, reason = obs.measure_lcp(str(site))
    assert got is None
    assert "启发式" in reason


def test_obs11_rejects_missing_page(site, tmp_path, monkeypatch):
    """采集面缺页即拒（CI 侧 perf.yml 会 404），不拿其余四页凑数。"""
    _full_site(site)
    os.remove(site / "dashboard.html")
    _write_fake_monitor(tmp_path, monkeypatch,
                        {rel: {"LCP": 0.2} for rel in obs.LCP_PAGES})
    got, reason = obs.measure_lcp(str(site))
    assert got is None
    assert "dashboard.html" in reason


def test_obs11_records_real_values(site, tmp_path, monkeypatch):
    _full_site(site)
    _write_fake_monitor(tmp_path, monkeypatch, {rel: {"LCP": 0.3} for rel in obs.LCP_PAGES})
    got, reason = obs.measure_lcp(str(site))
    assert reason is None
    assert got["measured"] is True
    assert got["max_ms"] == 300.0  # s → ms
    assert set(got["pages"]) == set(obs.LCP_PAGES)


def _write_varying_monitor(tmp_path, monkeypatch, seq):
    """假监视器：按每页调用次序返回 seq 中的值（seq: {basename: [v1, v2, ...]}）。

    用于锁「每页 3 次取中位数」：静态返回值测不出 spike 剔除，必须让同一页
    在三次调用里给出不同值。
    """
    sidecar = tmp_path / "fake_state.json"
    sidecar.write_text(json.dumps({"pages": seq, "calls": {}}), encoding="utf-8")
    fake = tmp_path / "fake_perf_monitor_seq.py"
    fake.write_text(
        "import json,os,sys\n"
        "st=json.load(open(os.environ['FAKE_SIDECAR']))\n"
        "t=sys.argv[sys.argv.index('--target')+1]\n"
        "k=os.path.basename(t)\n"
        "n=st['calls'].get(k,0)\n"
        "v=st['pages'][k][min(n,len(st['pages'][k])-1)]\n"
        "st['calls'][k]=n+1\n"
        "json.dump(st,open(os.environ['FAKE_SIDECAR'],'w'))\n"
        "o=sys.argv[sys.argv.index('--json')+1]\n"
        "json.dump({'pages':{k:{'LCP':v}}},open(o,'w'))\n",
        encoding="utf-8")
    monkeypatch.setenv("FAKE_SIDECAR", str(sidecar))
    monkeypatch.setattr(obs, "PERF_MONITOR", str(fake))


def test_obs11_median_of_runs_rejects_spike(site, tmp_path, monkeypatch):
    """W850 实测教训：同机三连测 dashboard LCP 分别 116 / 1140 / 104 ms。

    单次取值会让基线被噪声支配（一次 spike 就把结论从「远低于 SLO」扭成「贴近 SLO」）。
    每页 3 次取中位数：spike 不进 pages，原始三轮值留档 runs_ms 供查方差。
    """
    _full_site(site)
    seq = {os.path.basename(r):
           ([0.1, 1.1, 0.2] if r == "dashboard.html" else [0.3, 0.3, 0.3])
           for r in obs.LCP_PAGES}
    _write_varying_monitor(tmp_path, monkeypatch, seq)
    got, reason = obs.measure_lcp(str(site))
    assert reason is None
    assert got["runs"] == obs.LCP_RUNS == 3
    assert got["runs_ms"]["dashboard.html"] == [100.0, 1100.0, 200.0]
    assert got["pages"]["dashboard.html"] == 200.0  # 中位数，非均值(466.7)也非最大(1100)
    assert got["max_ms"] == 300.0                    # spike 页不再霸榜
    assert "中位数" in got["engine"]


def test_obs14_unreachable_records_reason():
    """服务不在跑 → 记原因不记值（不猜数）。

    本用例同时锁死代理陷阱：urllib 默认吃 HTTP_PROXY，本机 127.0.0.1 探测会被代理截走
    （实测端口无人听时代理回 502，把「不可达」误报成「服务返回 HTTP 502」）。
    """
    got, reason = obs.measure_first_token(port=59999, timeout=2)
    assert got is None
    assert "不可达" in reason


def test_obs14_reads_metrics():
    """本地 HTTP 桩：count/p50/p95 落位，sloMs 以服务端为准。"""
    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            body = json.dumps({"ok": True, "first_token": {
                "count": 7, "window": 100, "p50": 810, "p95": 1730, "max": 1900,
                "sloMs": 2000}}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    srv = HTTPServer(("127.0.0.1", 0), _Handler)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        got, reason = obs.measure_first_token(port=port)
    finally:
        srv.shutdown()
    assert reason is None
    assert got["count"] == 7 and got["p50_ms"] == 810 and got["p95_ms"] == 1730
    assert got["slo_ms"] == 2000


def test_record_dedup_and_per_metric_progress(site, tmp_path):
    """同批重跑覆盖不重复；三条指标分别计数——OBS-14 没测就不能算它有样本。"""
    base = tmp_path / "obs_samples.json"
    monkey_batch = "W850"
    obs.record(monkey_batch, path=base)
    obs.record(monkey_batch, path=base)
    obs.record("W851", with_first_token=True, port=59999, path=base)
    data = obs._load(str(base))
    assert [s["batch"] for s in data["samples"]] == ["W850", "W851"]
    assert obs._progress(data, "obs10") == 2
    assert obs._progress(data, "obs11") == 0
    assert obs._progress(data, "obs14") == 0  # W851 显式开了 --first-token 但服务不可达
    last = data["samples"][-1]
    assert last["obs14"]["measured"] is False and "不可达" in last["obs14"]["reason"]


def test_cli_self_test_and_status(tmp_path):
    """CLI 面：--self-test 全绿；--status 在空基图上不炸（fail-closed 的反面是可启动）。"""
    r = subprocess.run([sys.executable, str(SCRIPT), "--self-test"],
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "---- OBS 采样件自测：7/7 ----" in r.stdout

    empty = tmp_path / "empty.json"
    empty.write_text(json.dumps({"schema": 1, "target_batches": 10, "samples": []}),
                     encoding="utf-8")
    r2 = subprocess.run([sys.executable, str(SCRIPT), "--status"],
                        capture_output=True, text=True, timeout=60,
                        env=dict(os.environ, PYTHONPATH=str(SCRIPTS)))
    assert r2.returncode == 0
    assert "0/10 批有样本" in r2.stdout
