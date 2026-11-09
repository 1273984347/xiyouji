"""W1168 第 67 槽「统计事件契约」判据单测（TDD：先红后绿）。

三面对拍：事件清单正本 ↔ 代码落点 ↔ metric 反向链。
N6/N7 是与 N1-N5 同权重的正样本——守卫误伤（模板槽位当名字）与漏判同为缺陷。
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
GATE = SCRIPTS / "check_stat_events.py"


def _load():
    spec = importlib.util.spec_from_file_location("stat_events", GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_analytics_check_mode_runs_and_covers_bridge(tmp_path):
    """注入器的 --check 分支必须真能跑（W1168 实证潜伏 NameError：单测只覆盖 --dry-run，
    而 --check 里残留的 ga4_on 在被删变量后成为未定义名——不被执行就不会暴露的保护逻辑
    等于没有保护逻辑·铁律 23）。顺带断言桥脚本随块分发且旧双轨 MARK 已被迁移掉。
    """
    r = subprocess.run([sys.executable, "scripts/w1167_analytics_inject.py", "--check"],
                       capture_output=True, text=True, encoding="utf-8", timeout=300, cwd=str(ROOT))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "CHECK PASS" in r.stdout, r.stdout
    txt = (ROOT / "site" / "data" / "81-hardships-view.html").read_text(encoding="utf-8")
    assert "ANALYTICS v2 w1168" in txt
    assert "static/js/stats.js" in txt, "桥未随注入器分发"
    assert "ANALYTICS-DUAL v1" not in txt, "旧 MARK 未迁移（会留下第二份块⇒双份上报）"


def test_csp_exception_surface_is_single_domain():
    """GA4 退役后具名例外收缩为 GoatCounter 单域（第 67 槽 C5 与 CSP 白名单同源）。"""
    sys.path.insert(0, str(SCRIPTS))
    try:
        import generate_csp as csp
    finally:
        sys.path.remove(str(SCRIPTS))
    assert csp.EXTERNAL_SCRIPT_HOSTS == [], csp.EXTERNAL_SCRIPT_HOSTS
    assert csp.ANALYTICS_CONNECT_HOSTS.strip() == "https://1273984347.goatcounter.com"


def test_c2_multi_file_landing_all_must_exist(tmp_path):
    """N11 一个事件常有多个落点（3D 复位＝中/英/journey 三页）：`emitter.files` 必须逐个验。

    只支持单 file 的话，要么被迫只声明一个页面（另两页缺控件也无人知），要么拆成三组
    重名事件（C1 会判跨组重名）——两种都是把真实形态塞进不合身的 schema。
    """
    mod = _load()
    # 夹具路径与 _tree 的落点面保持一致（html 写在 site/data/ 下）：否则「落点不存在」是
    # 被夹具构造错触发而非被测行为触发，两态断里的第一次「红」也是假红（W1168 实证）
    btn = '<button id="reset-view" data-goatcounter-click="reset_view">复位</button>\n'
    root = _tree(tmp_path, [_group(names=["reset_view"], emitter={
        "files": [
            {"file": "site/data/a.html", "token": 'data-goatcounter-click="reset_view"'},
            {"file": "site/data/b.html", "token": 'data-goatcounter-click="reset_view"'},
        ]})],
        js={"stats.js": "// XYstats\n"},
        html={"a.html": btn})
    codes, fails = _codes(mod, root)
    assert "C2" in codes and any("site/data/b.html" in f for f in fails), fails
    assert not any("site/data/a.html" in f for f in fails), fails
    # 补齐第二个落点后应转绿
    (tmp_path / "site" / "data" / "b.html").write_text(btn, encoding="utf-8")
    codes2, fails2 = _codes(mod, root)
    assert "C2" not in codes2, fails2


def test_repo_manifest_and_landing_agree():
    """现网实跑：清单每项都有落点、落点事件名都在清单内 ⇒ 退出码 0 且违规 0。

    汇总行形态沿用 65/66 槽（`违规 N · OK|FAIL`），不另造第四种格式——
    多一种形态就多一处 verify_delivery marker 与人工读数的漂移面。
    """
    r = subprocess.run([sys.executable, "scripts/check_stat_events.py"], cwd=str(ROOT),
                       capture_output=True, text=True, encoding="utf-8", timeout=180)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "统计事件契约" in r.stdout
    assert "违规 0 · OK" in r.stdout, r.stdout


def _tree(tmp_path, groups, *, js=None, html=None, nav_items=None, py=None):
    """合成树：判据只认 scripts/ + site/ 两面，负样本全在临时目录构造、不触仓库。"""
    (tmp_path / "scripts" / "output").mkdir(parents=True)
    (tmp_path / "site" / "data").mkdir(parents=True)
    (tmp_path / "spark-output" / "context").mkdir(parents=True)
    (tmp_path / "scripts" / "output" / "_w1168_stat_events.json").write_text(
        json.dumps({"version": 1, "groups": groups}, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "spark-output" / "context" / "metric.json").write_text(
        json.dumps({"instrumentation_gaps": [{"event": "nav_click"},
                                             {"event": "page_view + FCP/LCP"},
                                             {"event": "badge_view"}]}, ensure_ascii=False),
        encoding="utf-8")
    if nav_items is not None:
        # 生成的「导航正本」夹具：既提供 names_from 的派生源，也自带 emitter token。
        # 用**非 f-string**——f'' 会在 import 时真去求值 {event}，夹具就变成会崩的可执行代码。
        (tmp_path / "scripts" / "nav_truth.py").write_text(
            'TPL = \'<a data-goatcounter-click="{event}">x</a>\'\n'
            "ZH_ITEMS = %r\n" % (nav_items,), encoding="utf-8")
    for name, body in (js or {}).items():
        (tmp_path / "site" / name).write_text(body, encoding="utf-8")
    for name, body in (html or {}).items():
        (tmp_path / "site" / "data" / name).write_text(body, encoding="utf-8")
    for name, body in (py or {}).items():
        (tmp_path / "scripts" / name).write_text(body, encoding="utf-8")
    return str(tmp_path)


def _codes(mod, root):
    fails, _notes, _stats = mod.scan(root)
    return [f[:2] for f in fails], fails


def _group(**kw):
    g = {"group": "nav_click", "kind": "click", "metric": "nav_click",
         "emitter": {"file": "site/stats.js", "token": "XYstats"}, "names": ["nav-guide"],
         "runtime_layer": "bridge"}
    g.update(kw)
    return g


def test_c2_landing_declared_but_missing_is_red(tmp_path):
    """N1 C2 有清单无落点：emitter token 不在文件里 ⇒ 判红（反制「已埋」失真）。"""
    mod = _load()
    root = _tree(tmp_path, [_group(emitter={"file": "site/stats.js", "token": "XYstats.count"})],
                 js={"stats.js": "// 接线还没做，这里什么都没有\n"})
    codes, fails = _codes(mod, root)
    assert "C2" in codes, fails


def test_c3_rogue_event_in_runtime_js_is_red(tmp_path):
    """N2 C3 运行时 JS 发出清单外事件名 ⇒ 判红。"""
    mod = _load()
    root = _tree(tmp_path, [_group()],
                 js={"stats.js": "XYstats.count('nav-guide');\nXYstats.count('rogue_evt', 1);\n"})
    codes, fails = _codes(mod, root)
    assert "C3" in codes and any("rogue_evt" in f for f in fails), fails


def test_c4_rogue_attr_in_page_is_red(tmp_path):
    """N3 C4 页面被手工加埋点属性（绕过分发正本）⇒ 判红。"""
    mod = _load()
    root = _tree(tmp_path, [_group()],
                 js={"stats.js": "// XYstats defined\n"},
                 html={'a.html': '<a data-goatcounter-click="hand_written_evt">x</a>\n'})
    codes, fails = _codes(mod, root)
    assert "C4" in codes and any("hand_written_evt" in f for f in fails), fails


def test_c1_bad_slug_and_duplicate_names_are_red(tmp_path):
    """N4 C1 事件名不合 slug（大写开头）或组内重复 ⇒ 判红。"""
    mod = _load()
    root = _tree(tmp_path, [_group(names=["Nav-Guide", "dup", "dup"])],
                 js={"stats.js": "// XYstats\n"})
    codes, fails = _codes(mod, root)
    assert "C1" in codes, fails


def test_c5_group_without_metric_is_red(tmp_path):
    """N5 C5 组未声明服务的指标 ⇒ 判红（埋点与指标反向链断）。"""
    mod = _load()
    root = _tree(tmp_path, [_group(metric="")], js={"stats.js": "// XYstats\n"})
    codes, fails = _codes(mod, root)
    assert "C5" in codes, fails


def test_template_placeholder_is_not_mistaken_for_event_name(tmp_path):
    """N6 正样本：分发器里的模板槽位（`{event}` / `%s`）不是事件名，不得误伤。

    首版判据未区分「写死的名字」与「运行时填充的槽位」时，注入器正本自己会被判红——
    本例锁住这条，防止将来有人把过滤条件删掉来「让门禁变绿」。
    """
    mod = _load()
    src = ('TPL = f\'<a data-goatcounter-click="{event}">x</a>\'\n'
           'ALT = \'<a data-goatcounter-click="%s">y</a>\'\n')
    root = _tree(tmp_path, [_group(names=["nav-guide"])],
                 js={"stats.js": "// XYstats\n"}, py={"nav_inject.py": src})
    codes, fails = _codes(mod, root)
    assert codes == [], fails


def test_names_derived_from_canonical_module(tmp_path):
    """N7 names_from 从正本派生（清单不重抄名字）：判据看到的集合＝正本列表。

    清单里重抄一遍事件名 = 双源漂移（改正本不改清单即失真），故派生形态必须可用。
    """
    mod = _load()
    group = _group(names=["__unused__"],
                   emitter={"file": "scripts/nav_truth.py", "token": "data-goatcounter-click"},
                   names_from={"module": "nav_truth", "lists": ["ZH_ITEMS"], "index": 2})
    root = _tree(tmp_path, [group],
                 nav_items=[["导读", "guide.html", "nav-guide"], ["看板", "dashboard.html", "nav-dash"]],
                 js={"stats.js": "// XYstats\n"})
    fails, _notes, stats = mod.scan(root)
    assert stats["names"] == 2, stats
    assert stats["groups"] == 1
    # 派生出的两个名字要真的进入比对集：rogue 名仍能被抓到（证明派生不是摆设）
    (tmp_path / "site" / "stats.js").write_text("XYstats.count('not_in_nav_list');\n", encoding="utf-8")
    codes, fails2 = _codes(mod, root)
    assert "C3" in codes, fails2


def test_missing_manifest_is_fail_closed(tmp_path):
    """N8 基础设施缺失必须 fail-closed（退出码 2），不得静默当成「无违规」。"""
    (tmp_path / "scripts" / "output").mkdir(parents=True)
    root = str(tmp_path)
    mod = _load()
    try:
        mod.scan(root)
        raise AssertionError("清单缺失应抛 OSError")
    except OSError as exc:
        assert "清单正本不可读" in str(exc)


def test_c3_catches_internal_alias_call_form(tmp_path):
    """N9 C3 必须认「模块内别名调用」——W1168 实测假绿形态：

    stats.js 对外是 `window.XYstats.count`，模块内部却是 `api.count('debug_error')`。
    只匹配全局限定名时，桥自己发的事件**完全不在扫描面内**（清单外也 0 FAIL），
    这比漏判更危险：它给出「门禁通过」的错误信心。
    """
    mod = _load()
    # 夹具含 window.XYstats 赋值以满足 C2 落点声明，让 C3 成为唯一可能的违规（否则 C2 先红会遮蔽被测点）
    root = _tree(tmp_path, [_group()],
                 js={"stats.js": "var api = {};\nwindow.XYstats = api;\napi.count('debug_error', 'boom');\n"})
    codes, fails = _codes(mod, root)
    assert "C3" in codes and any("debug_error" in f for f in fails), fails


def test_c3_does_not_scan_vendored_libraries(tmp_path):
    """N10 vendor 库（d3/three/min）不入扫描面：`.count('字面量')` 在压缩库里必然撞出噪音，

    噪音会淹没真违规（同「守卫误伤同样是缺陷」）。运行时自有库仍要扫。
    """
    mod = _load()
    root = _tree(tmp_path, [_group()], js={
        "d3.v7.min.js": "x.count('whatever_literal');\n",
        "three.r128.min.js": "y.count('another_literal');\n",
        "chart-a11y.js": "XYstats.count('rogue_own_code');\n",
    })
    codes, fails = _codes(mod, root)
    assert "C3" in codes, fails
    joined = "\n".join(fails)
    assert "rogue_own_code" in joined, fails
    assert "whatever_literal" not in joined and "another_literal" not in joined, fails



# ---- stats.js 运行面（node + DOM 桩执行真源码·断言真实行为）----

STATS = ROOT / "site" / "static" / "js" / "stats.js"


def _harness(scenario: str) -> str:
    """DOM 桩 + 场景脚本：桩只提供环境，断言打在生产代码的真实行为上。"""
    return r"""
const fs = require('fs');
const path = require('path');
const src = fs.readFileSync(process.env.STATS_PATH, 'utf8');

function makeEnv(opts) {
  const sent = [];
  const warns = [];
  const loadHandlers = [];
  const listeners = {};
  const elements = opts.elements || [];
  const doc = {
    documentElement: { style: {}, getAttribute: () => null },
    body: { appendChild: () => {} },
    addEventListener: (t, f) => { (listeners[t] = listeners[t] || []).push(f); },
    removeEventListener: () => {},
    querySelectorAll: (sel) => (sel === '[data-goatcounter-view]' ? elements : []),
    visibilityState: 'visible',
    title: 'T',
    readyState: 'loading',
    createElement: () => ({ style: {}, setAttribute: () => {}, addEventListener: () => {}, parentNode: null }),
  };
  const win = {
    location: { protocol: opts.protocol, hostname: opts.hostname, pathname: '/p.html', search: '' },
    document: doc,
    navigator: { sendBeacon: () => true },
    screen: { width: 1200 },
    addEventListener: (t, f) => { (listeners[t] = listeners[t] || []).push(f); },
    removeEventListener: () => {},
    setTimeout: (f) => f(),
    IntersectionObserver: opts.noIO ? undefined : function (cb) {
      this.observe = (el) => { cb([{ isIntersecting: true, target: el }], this); };
      this.unobserve = () => {};
    },
  };
  if (opts.ready) {
    win.goatcounter = { count: (v) => sent.push(v), url: () => 'u', get_data: () => ({}) };
  }
  const console_ = { warn: (m) => warns.push(String(m)), error: (m) => warns.push(String(m)), log: () => {} };
  const sandbox = { window: win, document: doc, navigator: win.navigator, location: win.location,
                    console: console_, setTimeout: win.setTimeout,
                    IntersectionObserver: win.IntersectionObserver };
  sandbox.window = win;
  win.self = win;
  const vm = require('vm');
  vm.createContext(sandbox);
  vm.runInContext(src, sandbox);
  return { win, sent, warns, listeners, doc };
}

function fire(listeners, type, ev) {
  (listeners[type] || []).forEach((f) => f(ev || {}));
}
""" + scenario + "\nrequire('fs').writeSync(1, JSON.stringify(result));\n"


def _run(tmp_path, scenario: str) -> dict:
    harness = _harness(scenario)
    js = tmp_path / "harness.js"
    js.write_text(harness, encoding="utf-8")
    import os
    env = dict(os.environ, STATS_PATH=str(STATS))
    r = subprocess.run(["node", str(js)], capture_output=True, text=True,
                       encoding="utf-8", timeout=60, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    return json.loads(r.stdout)


def test_bridge_queues_until_goatcounter_ready(tmp_path):
    """B1 就绪前入队、就绪后冲刷——async 加载顺序不能吞掉早期事件。"""
    scenario = r"""
let env = makeEnv({protocol:'https:', hostname:'example.github.io', ready:false});
env.win.XYstats.count('nav_click_test', 'x');
const queued = env.sent.length;
env.win.goatcounter = { count: (v) => env.sent.push(v) };
fire(env.listeners, 'load');
result = {queued: queued, flushed: env.sent.length, names: env.sent.map(s => s.path)};
"""
    out = _run(tmp_path, scenario)
    assert out["queued"] == 0, out
    assert out["flushed"] == 1, out
    assert out["names"] == ["nav_click_test"], out


def test_bridge_silent_on_file_protocol(tmp_path):
    """B2 file:// 不发也不 warn：859 页离线双击时 console 噪声会污染 H3 健康监控。"""
    scenario = r"""
let env = makeEnv({protocol:'file:', hostname:'', ready:true});
env.win.XYstats.count('nav_click_test', 'x');
result = {sent: env.sent.length, warns: env.warns.length};
"""
    out = _run(tmp_path, scenario)
    assert out["sent"] == 0 and out["warns"] == 0, out


def test_bridge_marks_events_as_goatcounter_events(tmp_path):
    """B3 事件必须带 event:true——否则 GoatCounter 记成页面浏览，路径维度被污染。"""
    scenario = r"""
let env = makeEnv({protocol:'https:', hostname:'example.github.io', ready:true});
env.win.XYstats.count('badge_view', '实时数据');
result = {one: env.sent[0]};
"""
    out = _run(tmp_path, scenario)
    assert out["one"]["event"] is True, out
    assert out["one"]["path"] == "badge_view", out


def test_bridge_exposure_observer_fires_once_per_element(tmp_path):
    """B4 声明式曝光：进入视口上报一次，重复 observe 不重报（badge_view 的实现前提）。"""
    scenario = r"""
const el = {dataset: {goatcounterView: 'badge_view', goatcounterBoundView: ''}};
let env = makeEnv({protocol:'https:', hostname:'example.github.io', ready:true, elements: [el]});
env.win.XYstats.observeViews();
env.win.XYstats.observeViews();
result = {sent: env.sent.map(s => s.path)};
"""
    out = _run(tmp_path, scenario)
    assert out["sent"] == ["badge_view"], out


def test_bridge_reports_js_errors(tmp_path):
    """B5 window error/unhandledrejection ⇒ debug_error（全站覆盖，不必改 234 个 rum 消费者）。"""
    scenario = r"""
let env = makeEnv({protocol:'https:', hostname:'example.github.io', ready:true});
fire(env.listeners, 'error', {message: 'boom'});
result = {sent: env.sent.map(s => s.path)};
"""
    out = _run(tmp_path, scenario)
    assert "debug_error" in out["sent"], out


def test_bridge_never_throws_when_goatcounter_absent(tmp_path):
    """B6 统计是增强面：goatcounter 缺失/被拦截时桥不得抛错影响页面（file:// 铁律）。"""
    scenario = r"""
let env = makeEnv({protocol:'https:', hostname:'example.github.io', ready:false, noIO: true});
let threw = null;
try { env.win.XYstats.count('nav_click_test'); env.win.XYstats.observeViews(); }
catch (e) { threw = String(e); }
result = {threw: threw};
"""
    out = _run(tmp_path, scenario)
    assert out["threw"] is None, out



def test_c6_runtime_layer_declared_and_legal(tmp_path):
    """C6 运行层是清单的必填面：探针据声明选读取层，缺声明或值越界即判红。

    动机（W1168 实测）：P6 只读 XYstats 桥层，而 reset_view 声明为 data-goatcounter-click
    由 goatcounter.js 原生处理 ⇒ 计数走的是入口层。判据读错面即恒 0，属仪器坏不是接线坏；
    把「读哪一层」写进清单正本，探针就不必再猜，两层并读的模糊断言也随之消失。
    """
    mod = _load()
    ok_js = {"stats.js": "XYstats.count('nav-guide');\n"}
    # 三棵树各占独立子根：_tree 在根下 mkdir，同根二次调用即 FileExistsError
    for sub, group, expect in (("ok", _group(runtime_layer="bridge"), False),
                               ("missing", _group(runtime_layer=None), True),
                               ("illegal", _group(runtime_layer="kafka"), True)):
        codes, fails = _codes(mod, _tree(tmp_path / sub, [group], js=ok_js))
        assert ("C6" in codes) is expect, (sub, codes, fails)
    codes, fails = _codes(mod, _tree(tmp_path / "msg", [_group(runtime_layer="kafka")], js=ok_js))
    assert any("kafka" in f for f in fails), fails


def test_repo_manifest_declares_runtime_layer_every_group():
    """现势清单每组的运行层都必须声明且合法（清单是正本，不是注释）。"""
    d = json.loads((ROOT / "scripts" / "output" / "_w1168_stat_events.json").read_text(encoding="utf-8"))
    missing = [g["group"] for g in d["groups"] if g.get("runtime_layer") not in ("bridge", "goatcounter")]
    assert not missing, missing


def test_probe_reads_layer_declared_in_manifest():
    """探针的取数层由清单派生：声明 goatcounter 的组只读计数入口层，反之只读桥层。"""
    sys.path.insert(0, str(ROOT / "scripts"))
    import stat_event_probe as probe

    xy = [["reader_progress", "50"], ["badge_view", ""]]
    gc = [["reset_view", True, "t"], ["nav-guide", True, "t"]]
    assert probe._layer_records("bridge", xy, gc) == xy
    assert probe._layer_records("goatcounter", xy, gc) == gc
    # 现势正本：reset_view 是声明式（入口层），search_perform 是桥层
    assert probe._declared_layer("reset_view") == "goatcounter"
    assert probe._declared_layer("search_perform") == "bridge"
    # 未登记事件名必须 fail-closed 抛出，不静默退回某一层
    try:
        probe._declared_layer("no_such_event")
    except LookupError:
        pass
    else:
        raise AssertionError("未登记事件名应 fail-closed，而不是默认某一层")


def test_probe_self_test_executes():
    """探针的两层拦截 + 捕获单源锁必须有实质执行面（第 42 槽 C1：新增脚本须带测试引用）。

    同时它锁住本批两处仪器根修的**方向**：包装必须透传原实现（否则测的是桩不是桥），
    且 storage 可用时不得双写（否则 P3 型双计会伪装成「埋点重复」的产品缺陷）。
    """
    r = subprocess.run([sys.executable, "scripts/stat_event_probe.py", "--self-test"],
                       capture_output=True, text=True, encoding="utf-8", timeout=180, cwd=str(ROOT))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "SELF_TEST_OK" in r.stdout, r.stdout
    assert "捕获单源" in r.stdout, r.stdout


def test_gate_self_test_executes_with_negative_samples():
    """第 67 槽 `--self-test` 不得是永远绿的占位（铁律 23：保护逻辑要有它真生效的证据）。"""
    r = subprocess.run([sys.executable, "scripts/check_stat_events.py", "--self-test"],
                       capture_output=True, text=True, encoding="utf-8", timeout=180, cwd=str(ROOT))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "SELF_TEST_OK（10 例）" in r.stdout, r.stdout
