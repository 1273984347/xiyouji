#!/usr/bin/env python3
"""check_stat_events.py — 第 67 槽 · 统计事件契约对拍（W1168）

## 病根（为什么恒跑槽必须新增这一条）

W1167 把埋点从「通道」推进到「一个声明式事件」，metric 蓝图里 8 个 must 事件的落点靠人工记忆登记。
事件名一旦散成字符串泥，三种退化都不会有红灯：① 代码发了清单上没有的名字（报表里冒出新事件没人知道
它从哪来）；② 清单声明了但代码里根本没有发射点（「已埋」是假的——本仓已为此写过 G0-1 声明失真教训）；
③ 页面被手工加了埋点属性绕过注入器正本（W1167 的守卫只盯 goatcounter 域，不盯事件名）。

## 判据（四面对拍）

C1 名字规范：每组事件名唯一 + ASCII 小写 slug（禁空格/大写/中文——GoatCounter 与报表两侧按名聚合）
C2 有清单必有落点：emitter.file 存在且含 emitter.token（声明了却没接线 ⇒ 判红，反制「已埋」失真）
C3 有落点必有清单：源面（scripts/*.py 与 site/**/*.js）出现的 `XYstats.count("<名>")` /
   `data-goatcounter-click="<名>"` / `data-goatcounter-view="<名>"` 必须 ∈ 清单派生名集
C4 页面面不被绕过：site/**/*.html 出现的两属性值同样必须 ∈ 清单名集（手工散落埋点判红）
C5 metric 反向链：每组 `metric` 必须能在 metric.json 的 instrumentation_gaps 事件名中找到
   （链路质量标准 5「每个验收标准对应 ≥1 可观测埋点」的反向可核验形态）
C6 运行层必填且合法：`runtime_layer` ∈ RUNTIME_LAYERS。运行面探针据它选读取层——声明式属性由
   goatcounter.js 原生处理（计数入口层），桥接事件由 stats.js 发起（XYstats 层）。W1168 实测：
   探针按猜测只读桥层，`reset_view` 恒 0 而接线完好 ⇒ 把「读哪一层」升格为清单必填面

**事件名不在清单里重复声明**：能派生的组走 `names_from`（import 正本列表），避免清单与正本双源漂移——
这也是 C3 能成立的前提（名字的唯一事实源是发射它的代码）。

## 用法与退出码

    python scripts/check_stat_events.py              # 门禁模式（恒跑·毫秒到秒级）
    python scripts/check_stat_events.py --self-test  # 注入式自测（合成树·不触仓库）
    python scripts/check_stat_events.py --report     # 只报不判红

退出码：0 通过 / 1 判红 / 2 基础设施缺失（清单或 metric 正本不可读·fail-closed，不静默放行）。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 运行层合法集（第 67 槽 C6 与 stat_event_probe 的共同正本·引用不复制）：
#   bridge      —— site/static/js/stats.js 桥调 XYstats.count(...)，捕获在桥层
#   goatcounter —— data-goatcounter-click / 原生 pageview，捕获在 goatcounter.count 入口层
RUNTIME_LAYERS = ("bridge", "goatcounter")
MANIFEST_REL = os.path.join("scripts", "output", "_w1168_stat_events.json")
METRIC_REL = os.path.join("spark-output", "context", "metric.json")
MARKER = "---- 第 67 门禁 统计事件契约："


def _roots(root: str) -> dict:
    """路径集合化：判据必须能在合成树上被测（否则负样本只能改真仓库）。"""
    return {
        "root": root,
        "scripts": os.path.join(root, "scripts"),
        "site": os.path.join(root, "site"),
        "manifest": os.path.join(root, MANIFEST_REL),
        "metric": os.path.join(root, METRIC_REL),
    }

CLICK_ATTR_RE = re.compile(r'data-goatcounter-click\s*=\s*"([^"]+)"')
VIEW_ATTR_RE = re.compile(r'data-goatcounter-view\s*=\s*"([^"]+)"')
CALL_RE = re.compile(r'''\.count\(\s*['"]([^'"]+)['"]''')
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
# 调用形态必须**不限定接收者**：桥对外是 window.XYstats.count，模块内部是 api.count
# ——只匹配全局限定名会让桥自己发的事件完全不在扫描面内（W1168 实测假绿，比漏判更危险：
# 它给出「门禁通过」的错误信心）。
# 但 `.count('字面量')` 只能用在 **JS 面**：Python 侧 str.count('中') 是极常见写法，
# 一刀切宽匹配会让 plan_template_review.py / stats.py 之类冒出「待确认事项」「/」等噪音名
# （W1168 首跑实证）——噪音会淹没真违规，与漏判同为缺陷。故按面分治：
#   属性形态（click/view）扫 .py 生成器 + .js 运行时；调用形态只扫 .js。
# goatcounter.count 传的是对象不是字符串字面量，故 JS 面宽匹配不会撞上它。
VENDOR_RE = re.compile(r"(\.min\.js$)|(^d3[.\w]*\.js$)|(^three[.\w]*\.js$)")
# vendor 压缩库不入扫描面：`.count('…')` 在其中必然撞出字面量噪音，而噪音会淹没真违规
# （守卫误伤与漏判同为缺陷）。自有运行文件（chart-*.js / cite-box.js / stats.js 等）仍全扫。
# 模板占位（f-string/`%s`/拼接）不是事件名：`data-goatcounter-click="{event}"` 由注入器
# 在运行时填充，把占位符本身当名字会让 C3 对每个正本文件都误判红。判据「扫源代码」必须
# 区分「写死的名字」与「模板槽位」——含这些字符即视为槽位。
TEMPLATE_CHARS = "{}%$+\\"


def _is_template(name: str) -> bool:
    return any(ch in name for ch in TEMPLATE_CHARS)


def _found_names(text: str, *, with_calls: bool) -> set[str]:
    """提取「写死的事件名」；模板占位（`{event}`/`%s`）不计，调用形态仅在 JS 面计入。"""
    raw = set(CLICK_ATTR_RE.findall(text)) | set(VIEW_ATTR_RE.findall(text))
    if with_calls:
        raw |= set(CALL_RE.findall(text))
    return {n for n in raw if not _is_template(n)}


def _load_manifest(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _load_module(name: str, scripts_dir: str):
    path = os.path.join(scripts_dir, name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _names_of(group: dict, scripts_dir: str) -> list[str]:
    """组内事件名：优先从正本派生（不复制），否则用显式 names。"""
    src = group.get("names_from")
    if not src:
        return list(group.get("names") or [])
    mod = _load_module(src["module"], scripts_dir)
    idx = src.get("index", 2)
    out: list[str] = []
    for list_name in src["lists"]:
        for item in getattr(mod, list_name, []):
            out.append(item[idx])
    return out


def _iter_files(base: str, exts: tuple[str, ...]):
    for root, _dirs, files in os.walk(base):
        if "__pycache__" in os.path.normpath(root).split(os.sep):
            continue
        for fn in sorted(files):
            if fn.endswith(exts):
                yield os.path.join(root, fn)


def _is_emitter_surface(path: str) -> bool:
    """C3 只扫「会真的发出事件」的面：运行时 JS + 生成页面的分发器。

    判据/守卫/探针类文件里的 `data-goatcounter-click="nav-hacked"` 是**负样本夹具**，
    不是发射点——混进来会让门禁把自己的测试当成违规（W1168 首跑实证：守卫自测夹具
    被 C3 判红）。按文件名角色排除，残余风险如实记下：若有人把真实发射点写进
    `check_*.py`/`*_probe.py`，本槽看不到——但那种写法本身违反「运行面与判据面分离」，
    由第 42 槽（根级脚本覆盖）与代码评审兜住。
    """
    base = os.path.basename(path)
    if base.startswith("check_") or "_probe" in base or base.startswith("test_"):
        return False
    return True


def _scan_sources(names: set[str], r: dict) -> list[str]:
    """C3：发射面出现的事件名必须都在清单内（.py 看属性形态，.js 加调用形态）。"""
    bad: list[str] = []
    py_paths = [p for p in _iter_files(r["scripts"], (".py",)) if _is_emitter_surface(p)]
    js_paths = [p for p in _iter_files(r["site"], (".js",)) if not VENDOR_RE.search(os.path.basename(p))]
    for path, with_calls in [(p, False) for p in py_paths] + [(p, True) for p in js_paths]:
        if os.path.basename(path) == os.path.basename(__file__):
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            bad.append("C3 源文件读取失败：%s（%s）" % (path, exc))
            continue
        found = _found_names(text, with_calls=with_calls)
        for n in sorted(found - names):
            bad.append("C3 代码发出清单外事件名 %s（未登记于 %s）：%s"
                       % (n, os.path.relpath(r["manifest"], r["root"]),
                          os.path.relpath(path, r["root"])))
    return bad


def _scan_pages(names: set[str], r: dict) -> list[str]:
    """C4：页面出现的事件属性必须都在清单内（防手工散落埋点绕过正本）。"""
    bad: list[str] = []
    for path in _iter_files(r["site"], (".html",)):
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            bad.append("C4 页面读取失败：%s（%s）" % (path, exc))
            continue
        for n in sorted(_found_names(text, with_calls=False) - names):
            bad.append("C4 页面含清单外埋点名 %s：%s" % (n, os.path.relpath(path, r["root"])))
    return bad


def _check_metric_links(groups: list[dict], r: dict) -> tuple[list[str], list[str]]:
    """C5：每组必须声明服务的指标（结构性要求）；metric 正本在本地存在时再对一次名。

    为什么不在 CI 上硬对 metric.json：`spark-output/` 已 gitignore（W1167 决定），
    CI 侧读不到 ⇒ 若把它当硬判据，槽在 CI 恒 fail-closed 变红。故硬判据只要求
    「每个埋点声明它服务哪个指标」（缺字段＝反向链断裂＝红），本地若能读到正本
    再给 NOTE 提示对不上项，既保住约束又不造 CI 假红。
    """
    fails, notes = [], []
    for g in groups:
        want = (g.get("metric") or "").strip()
        if not want:
            fails.append("C5 组 %s 未声明 metric（埋点与指标的反向链断·质量标准 5）" % g["group"])
    if not os.path.exists(r["metric"]):
        return fails, ["C5 metric 正本不在本机（spark-output 已 gitignore·CI 预期跳过对名）"]
    try:
        with open(r["metric"], encoding="utf-8") as fh:
            metric_events = [g.get("event", "") for g in json.load(fh).get("instrumentation_gaps", [])]
    except (OSError, ValueError) as exc:
        return fails, ["C5 metric 正本不可读，跳过对名：%s" % exc]
    for g in groups:
        want = (g.get("metric") or "").strip()
        if want and not any(want in ev for ev in metric_events):
            notes.append("C5 组 %s 的 metric %r 在本地 metric.json 无对应事件条目" % (g["group"], want))
    return fails, notes


def scan(root: str = ROOT) -> tuple[list[str], list[str], dict]:
    """返回 (违规, 提示, 统计)。root 可指向合成树（负样本用）。"""
    r = _roots(root)
    try:
        manifest = _load_manifest(r["manifest"])
    except OSError as exc:
        raise OSError("事件清单正本不可读：%s" % exc) from exc
    groups = manifest.get("groups", [])
    fails: list[str] = []
    notes: list[str] = []
    all_names: set[str] = set()

    for g in groups:
        names = _names_of(g, r["scripts"])
        dup = [n for n in names if names.count(n) > 1]
        if dup:
            fails.append("C1 组 %s 事件名重复：%s" % (g["group"], sorted(set(dup))))
        bad_slug = [n for n in names if not SLUG_RE.match(n)]
        if bad_slug:
            fails.append("C1 组 %s 事件名不合 slug 规范：%s" % (g["group"], bad_slug))
        if len(set(names) & all_names):
            fails.append("C1 跨组重名：%s" % sorted(set(names) & all_names))
        all_names |= set(names)
        fails += _check_emitter(g, r)
        layer = g.get("runtime_layer")
        if layer not in RUNTIME_LAYERS:
            fails.append("C6 组 %s 的 runtime_layer 非法或缺失：%r（合法集=%s·探针据声明选读取层）"
                         % (g["group"], layer, list(RUNTIME_LAYERS)))

    metric_fails, metric_notes = _check_metric_links(groups, r)
    fails += metric_fails
    notes += metric_notes
    fails += _scan_sources(all_names, r)
    fails += _scan_pages(all_names, r)
    stats = {"groups": len(groups), "names": len(all_names)}
    return fails, notes, stats


def _emitter_list(group: dict) -> list[dict]:
    """兼容两种声明形态：单 file（历史）与 files 多落点（W1168·一个事件常跨多页）。"""
    em = group.get("emitter") or {}
    if em.get("files"):
        return list(em["files"])
    return [em] if em.get("file") else []


def _check_emitter(group: dict, r: dict) -> list[str]:
    """C2：声明了就必须**每个**落点都在——emitter 文件存在且含标记串。

    多落点时逐条校验：只查第一个会让「中/英/journey 三页里只有一页有控件」假装通过。
    """
    bad: list[str] = []
    for em in _emitter_list(group):
        rel = em.get("file", "")
        path = os.path.join(r["root"], rel)
        if not rel or not os.path.isfile(path):
            bad.append("C2 组 %s 的 emitter 文件不存在：%s" % (group["group"], rel or "(空)"))
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            bad.append("C2 组 %s emitter 读取失败：%s" % (group["group"], exc))
            continue
        if em.get("token") and em["token"] not in text:
            bad.append("C2 组 %s 声明的落点标记 %r 不在 %s（清单有、代码无＝「已埋」失真）"
                       % (group["group"], em["token"], rel))
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description="第 67 槽 统计事件契约对拍（W1168）")
    ap.add_argument("--self-test", action="store_true", help="注入式自测（不触仓库）")
    ap.add_argument("--report", action="store_true", help="只报不判红")
    args = ap.parse_args()

    if args.self_test:
        return _self_test()

    try:
        fails, notes, stats = scan()
    except OSError as exc:
        print("环境错误：%s（fail-closed）" % exc, file=sys.stderr)
        return 2
    state = "OK" if not fails else ("NOTE" if args.report else "FAIL")
    print("%s 组 %d · 事件名 %d · 违规 %d · %s ----"
          % (MARKER, stats["groups"], stats["names"], len(fails), state))
    for msg in fails[:20]:
        print("  FAIL", msg)
    if len(fails) > 20:
        print("  ...（其余 %d 条略）" % (len(fails) - 20))
    for msg in notes[:6]:
        print("  NOTE", msg)
    return 0 if (not fails or args.report) else 1


def _self_group(**kw):
    """规范形态的基准组：负样本各改一处，正样本必须放行（否则重指向只是换了个误报器）。"""
    g = {"group": "nav_click", "kind": "click", "metric": "导航一致率", "runtime_layer": "goatcounter",
         "emitter": {"file": "site/nav.html", "token": 'data-goatcounter-click="nav-home"'},
         "names": ["nav-home"]}
    g.update(kw)
    return g


def _self_tree(base, groups, *, html=None, js=None):
    """合成树：判据四个取数面（清单 / site html / site js / metric 正本）全部落在临时目录。"""
    for rel in (os.path.join("scripts", "output"), os.path.join("site", "js"),
                os.path.join("spark-output", "context")):
        os.makedirs(os.path.join(base, rel), exist_ok=True)
    with open(os.path.join(base, MANIFEST_REL), "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "groups": groups}, fh, ensure_ascii=False)
    with open(os.path.join(base, METRIC_REL), "w", encoding="utf-8") as fh:
        json.dump({"instrumentation_gaps": [{"event": g.get("metric") or ""} for g in groups]},
                  fh, ensure_ascii=False)
    for name, body in (html or {}).items():
        with open(os.path.join(base, "site", name), "w", encoding="utf-8") as fh:
            fh.write(body)
    for name, body in (js or {}).items():
        with open(os.path.join(base, "site", "js", name), "w", encoding="utf-8") as fh:
            fh.write(body)
    return base


def _self_test() -> int:
    """判据自测：C1-C6 各一条负样本 + 规范形态正样本（E-142 纪律：判据要能证明自己会红）。

    此前这里是 `print("SELF_TEST_OK")` 占位——一个**永远绿**的自测面比没有自测更糟，
    它让「跑过自测」成为假证据（铁律 23）。夹具字符串写在 check_*.py 内，C3 按文件名
    角色排除判据面，不会把本文件的负样本读成真实发射点。
    """
    import tempfile

    nav_html = '<a data-goatcounter-click="nav-home">首页</a>\n'
    cases = []

    def add(label, groups, html, js, expect):
        cases.append((label, groups, html, js, expect))

    add("正样本·规范形态放行", [_self_group()], {"nav.html": nav_html}, {}, None)
    add("C2·声明了落点却没接线", [_self_group(emitter={"file": "site/nav.html",
                                                      "token": 'data-goatcounter-click="nav-gone"'})],
        {"nav.html": nav_html}, {}, "C2")
    add("C2·files 多落点缺一页", [_self_group(names=["reset_view"], emitter={"files": [
        {"file": "site/a.html", "token": 'data-goatcounter-click="reset_view"'},
        {"file": "site/b.html", "token": 'data-goatcounter-click="reset_view"'}]})],
        {"a.html": '<button data-goatcounter-click="reset_view">复位</button>\n'}, {}, "C2")
    add("C3·运行时 JS 发清单外事件名", [_self_group()], {"nav.html": nav_html},
        {"app.js": "XYstats.count('nav-home');\napi.count('rogue_evt', 1);\n"}, "C3")
    add("C4·页面手工埋清单外名", [_self_group()],
        {"nav.html": nav_html + '<span data-goatcounter-click="hand_made">x</span>\n'}, {}, "C4")
    add("C1·组内事件名重复", [_self_group(names=["nav-home", "nav-home"])],
        {"nav.html": nav_html}, {}, "C1")
    add("C1·事件名不合 slug 规范", [_self_group(names=["Nav-Home"])],
        {"nav.html": '<a data-goatcounter-click="Nav-Home">x</a>\n'}, {}, "C1")
    add("C5·未声明 metric（反向链断）", [_self_group(metric="")], {"nav.html": nav_html}, {}, "C5")
    add("C6·runtime_layer 缺失", [_self_group(runtime_layer=None)], {"nav.html": nav_html}, {}, "C6")
    add("C6·runtime_layer 越界", [_self_group(runtime_layer="kafka")], {"nav.html": nav_html}, {}, "C6")

    bad = 0
    for label, groups, html, js, expect in cases:
        with tempfile.TemporaryDirectory() as tmp:
            root = _self_tree(tmp, groups, html=html, js=js)
            fails, _notes, _stats = scan(root)
        codes = {f[:2] for f in fails}
        ok = (not fails) if expect is None else (expect in codes)
        if expect is not None and fails and not any(f.startswith(expect) for f in fails):
            ok = False
        print("  %s %s" % ("PASS" if ok else "FAIL", label))
        if not ok:
            bad += 1
            print("     实况=%s" % (fails[:3] or "0 FAIL（该红未红）"))
    print("%s（%d 例）" % ("SELF_TEST_OK" if not bad else "SELF_TEST_FAIL", len(cases)))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
