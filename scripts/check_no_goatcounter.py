#!/usr/bin/env python3
"""check_no_goatcounter.py — 统计「具名例外面」对账守卫（W806 建立 · W1167 重指向）。

## 沿革：为什么判据变了而守卫没被删

W806 裁决「彻底退役 GoatCounter」（站点代码实测 HTTP 404·采不到数据却仍每页发一次无效
外域请求），当时的守卫形态是**存在即红**：埋点标签 / CSP 外域放行 / 自托管脚本 / 注入器
四类任一命中即 FAIL。

W1167 用户拍板 G0-1 把统计改为**双轨具名例外**（GoatCounter 大陆面 + GA4 海外面·
decision_log 见 spark-output/context/brief.json），该裁决被推翻。但原守卫守的从来不是
GoatCounter 这个名字，而是「**统计外域面失控却零红灯**」——新口径下这个风险更大（现在
确实有外域了），所以本批**重指向判据，而不是删守卫、也不是加豁免把红灯压下去**（铁律 15）。

「不得存在」→「必须等于具名例外全集」：

## 检查项（全过 exit 0，任一 FAIL exit 1，正本不可读 exit 2）

C1 规范形态：页面出现**追踪标签** `data-goatcounter=` 必须同时含注入器 MARK ⇒ 缺 MARK＝
   手工散落埋点（不可幂等重放、下一批注入器会漏管该页）
C2 端点唯一：页面出现的 goatcounter host 必须等于配置正本 endpoint ⇒ 换成他人账号即红
C3 脚本唯一：site/ 下 goatcounter 命名文件只能是注入器声明的那一份 ⇒ 第二份混跑即红
C4 入口唯一：scripts/ 下写 goatcounter **任一属性形态**（追踪标签或事件属性）的 py，
   只能是声明过的正本写入口 ⇒ 例外面被第二个写入口改写即红
   （判据分形态是 W1167 自证抓出的：初版用 `data-goatcounter` 前缀子串，把导航正本
    `data-goatcounter-click`（事件属性）误判成追踪标签——事件与标签用途不同，须分别定义）
C5 双源一致：配置正本 endpoint ∈ generate_csp.ANALYTICS_CONNECT_HOSTS ⇒ 注入面与 CSP
   白名单分叉即红（本批 CHANGELOG 承诺「两处同源·不靠人工记忆」的可验证形态·铁律 23）

## 口径说明（沿用 W806 的两条范围纪律）

- 扫描限「运行时面」（site/ + scripts/），**不扫 docs/ 与 CHANGELOG**——历史记录与拍板
  说明本就应保留对 GoatCounter 的文字引用，扫它们会把「记录事实」误判成「越界」。
- 判定用**具体形态**（`data-goatcounter` / `*.goatcounter.com`）而非裸词：注释里提
  GoatCounter 是合法且必要的（rum.js / visit-log.js 的口径说明即属此类）。
- 正样本不止「干净树」，还必须有「规范形态放行」一条——否则重指向只是换了个误报器。

跨平台断言纪律（pitfalls「latent 三问 + 双平台断言禁例」）：比对全部基于文件名与内容子串
（大小写不敏感），零 os.name/盘符断言；负样本用系统临时目录合成树（两平台同构·不触仓库）。

用法：
    python scripts/check_no_goatcounter.py             # 门禁模式
    python scripts/check_no_goatcounter.py --self-test # 注入式自测（2 正 6 负·不触仓库）

退出码：0 全过；1 有 FAIL；2 参数/环境/正本不可读（fail-closed，绝不静默放行）。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

MARKER = "---- W1167 守卫 统计具名例外面对账："

# 追踪标签形态（属性名恰为 data-goatcounter）：C1/C2 用它，避免把事件属性误当标签
TAG_RE = re.compile(r"data-goatcounter\s*=")
# 任一 goatcounter 属性形态（标签或事件）：C4 写入口面用它
WRITER_RE = re.compile(r"data-goatcounter[-=]")
DOMAIN_HINT = "goatcounter.com"
FILENAME_PATTERN = "goatcounter"
HOST_RE = re.compile(r"https?://([a-z0-9.\-]+goatcounter\.com)")


def _repo_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_truth() -> dict:
    """从三个正本读例外面全集（引用不复制——正本改了守卫自动跟随）。

    任一正本不可读即抛，由 main 走退出码 2：守卫最怕的不是报红，而是「读不到 ⇒ 当作
    没事」的静默放行（铁律 23·W1121 实证形态）。
    """
    scripts_dir = os.path.join(_repo_root(), "scripts")
    sys.path.insert(0, scripts_dir)
    try:
        import generate_csp as csp  # CSP 例外域正本
        import w1167_analytics_inject as inj  # 注入器正本：MARK / CONFIG / 脚本相对路径
        import w1167_nav_inject as nav  # 导航正本：事件属性（data-goatcounter-click）写入口
    except Exception as exc:  # noqa: BLE001 - 正本缺失属基础设施故障，必须 fail-closed
        raise OSError("正本不可读：%s" % exc) from exc
    finally:
        sys.path.remove(scripts_dir)

    # 写入口全集从**事件清单正本**派生（引用不复制）：清单里声明为 emitter 的 scripts/*.py
    # 就是「被批准的写入口」，加一个事件不必再改守卫；反之新增一个不进清单的写入口必红。
    # W1168 实证：徽标正本开始写 data-goatcounter-view 后，硬编码两元素的写入口集合当场
    # 把 88 页的分发判成越界——那是登记面陈腐，不是越界。
    with open(os.path.join(scripts_dir, "output", "_w1168_stat_events.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    listed_writers = set()
    for g in manifest.get("groups", []):
        for em in ([g["emitter"]] if isinstance(g.get("emitter"), dict)
                   else (g.get("emitter") or {}).get("files", []) or []):
            rel = (em or {}).get("file") or ""
            if rel.startswith("scripts/") and rel.endswith(".py"):
                listed_writers.add(os.path.basename(rel))

    with open(inj.CONFIG, encoding="utf-8") as f:
        cfg = json.load(f)
    endpoint = (cfg.get("goatcounter_endpoint") or "").strip()
    m = HOST_RE.search(endpoint.lower())
    if not m:
        raise OSError("配置正本无合法 goatcounter_endpoint：%s" % inj.CONFIG)
    csp_blob = getattr(csp, "ANALYTICS_CONNECT_HOSTS", "")
    if not csp_blob:
        raise OSError("generate_csp.ANALYTICS_CONNECT_HOSTS 读不到（改名/清空？）")
    return {
        "mark": inj.MARK,
        "endpoint": endpoint,
        "endpoint_host": m.group(1),
        "canon_script": inj.rel_static("x.html"),           # 唯一自托管脚本相对路径
        # 声明过的写入口（两个形态各有各的正本，都是「具名例外」的一部分）：
        # 追踪标签由统计注入器分发，事件属性 data-goatcounter-click 由导航正本分发
        "canon_writers": ({os.path.basename(inj.__file__), os.path.basename(nav.__file__)}
                          | listed_writers),
        "csp_hosts": {h.lower() for h in HOST_RE.findall(csp_blob.lower())},
    }


def _iter_html(site_dir: str):
    for root, _dirs, files in os.walk(site_dir):
        for fn in sorted(files):
            if fn.lower().endswith(".html"):
                yield os.path.join(root, fn)


def _iter_files(base_dir: str):
    for root, _dirs, files in os.walk(base_dir):
        for fn in sorted(files):
            yield os.path.join(root, fn)


def _is_ignored(path: str) -> bool:
    """守卫自身与 Python 字节码产物不参与判定（自指误报防线·沿用 W806 设计）。

    按**文件名**排除而非仅 realpath：同名副本（测试合成树里的拷贝）同属守卫形态，
    不该被判成注入器。
    """
    if os.path.basename(path) == os.path.basename(__file__):
        return True
    if os.path.realpath(path) == os.path.realpath(__file__):
        return True
    return "__pycache__" in os.path.normpath(path).split(os.sep)


def _scan_page(path: str, truth: dict) -> list[str]:
    """C1 / C2：单页判据——标签须在规范块内，端点须等于正本。"""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            content = f.read()
    except OSError as exc:
        return ["C1 页面读取失败：%s（%s）" % (path, exc)]
    low = content.lower()
    extra = sorted({h for h in HOST_RE.findall(low)} - {truth["endpoint_host"]})
    fails: list[str] = []
    if TAG_RE.search(low):
        if truth["mark"] not in content:
            fails.append("C1 追踪标签缺注入器 MARK（手工散落埋点·不可幂等重放）：%s" % path)
        if extra:
            fails.append("C2 页面放行非正本 goatcounter 域 %s（正本=%s）：%s"
                         % (extra, truth["endpoint_host"], path))
    elif DOMAIN_HINT in low and extra:
        # 无标签却出现该域＝只剩 CSP connect-src 残留——越界端点同样判红
        fails.append("C2 CSP 残留非正本 goatcounter 域 %s：%s" % (extra, path))
    return fails


def _scan_site_files(site_dir: str, truth: dict) -> list[str]:
    """C3：site/ 下 goatcounter 命名文件只允许注入器声明的那一份。"""
    canon_js = os.path.normpath(os.path.join(site_dir, truth["canon_script"])).lower()
    return ["C3 站点残留第二份追踪脚本（正本仅 %s）：%s" % (truth["canon_script"], path)
            for path in _iter_files(site_dir)
            if not _is_ignored(path)
            and FILENAME_PATTERN in os.path.basename(path).lower()
            and os.path.normpath(path).lower() != canon_js]


def _scan_script(path: str, truth: dict) -> list[str]:
    """C4：单脚本判据——写 goatcounter 任一属性形态者只允许声明过的正本写入口。"""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            body = f.read().lower()
    except OSError as exc:
        return ["C4 脚本读取失败：%s（%s）" % (path, exc)]
    if not WRITER_RE.search(body):
        return []
    return ["C4 出现第二个写 goatcounter 属性的入口（正本=%s）：%s"
            % (sorted(truth["canon_writers"]), path)]


def scan(site_dir: str, scripts_dir: str, truth: dict | None = None) -> list[str]:
    """返回 FAIL 明细列表（空列表 = 全过）。纯函数形态：--self-test 复用同一判据。

    拆成单页/单脚本判据函数是结构档要求（合一实现时 `scan` 复杂度 18>15、分支 17>16
    被 ruff 结构档当场拦下·W1167 实证），同时让「哪一类例外面越界」在代码层可见。
    """
    if truth is None:
        truth = _load_truth()
    fails: list[str] = []
    for path in _iter_html(site_dir):
        fails += _scan_page(path, truth)
    fails += _scan_site_files(site_dir, truth)
    for path in _iter_files(scripts_dir):
        if _is_ignored(path) or not path.lower().endswith(".py"):
            continue
        base = os.path.basename(path)
        # 判据/探针面里的 `data-goatcounter-*` 是**负样本夹具与扫描正则**，不是发射点——
        # 与第 67 槽 C3 的 _is_emitter_surface 同一口径（守卫把自己的测试读成违规即误报，
        # W1168 实证：check_stat_events / stat_event_probe 双双被 C4 判越界）。
        if base.startswith("check_") or "_probe" in base or base.startswith("test_"):
            continue
        if base not in truth["canon_writers"]:
            fails += _scan_script(path, truth)
    # C5：配置正本 ↔ CSP 白名单 双源一致
    if truth["endpoint_host"] not in truth["csp_hosts"]:
        fails.append("C5 双源分叉：配置端点 %s 不在 ANALYTICS_CONNECT_HOSTS %s 内"
                     % (truth["endpoint_host"], sorted(truth["csp_hosts"])))
    return fails


def _self_test() -> int:
    """注入式自测：2 正（干净树 + 规范形态）·6 负（C1-C5 含事件属性形态），合成树不触仓库。"""
    import shutil
    import tempfile

    try:
        truth = _load_truth()
    except OSError as exc:
        print("SELF_TEST_FAIL 正本不可读：%s" % exc)
        return 2

    tmp = tempfile.mkdtemp(prefix="analytics_exception_surface_")
    ok = True
    try:
        site = os.path.join(tmp, "site")
        scripts = os.path.join(tmp, "scripts")
        os.makedirs(os.path.join(site, "static", "js"))
        os.makedirs(scripts)
        page = os.path.join(site, "index.html")
        tracker = os.path.join(site, "static", "js", "goatcounter.js")
        legacy = os.path.join(site, "static", "js", "goatcounter-legacy.js")
        adhoc = os.path.join(scripts, "ad_hoc_inject.py")
        canonical = ('%s\n<script data-goatcounter="%s" async src="static/js/goatcounter.js">'
                     '</script>\n' % (truth["mark"], truth["endpoint"]))

        def write(text: str) -> None:
            with open(page, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)

        def touch(path: str, body: str) -> None:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(body)

        def case(label: str, expect: list[str], t: dict | None = None) -> None:
            nonlocal ok
            got = scan(site, scripts, t or truth)
            hit = [g for g in got if g.startswith(tuple(expect))] if expect else []
            passed = (not got) if not expect else bool(hit)
            print("  %s %s" % ("PASS" if passed else "FAIL", label))
            if not passed:
                ok = False
                print("    期望命中前缀 %r·实得 %r" % (expect, got))

        # 正样本 1：完全干净
        write("<html><head></head><body>ok</body></html>\n")
        case("clean-tree-must-pass", [])
        # 正样本 2：规范形态必须放行（本批评据改造的核心正向证据）
        write(canonical)
        touch(tracker, "// tracker\n")
        case("canonical-form-must-pass", [])
        # 负样本 1（C1）：有标签、无 MARK
        write('<script data-goatcounter="%s" async src="static/js/goatcounter.js"></script>\n'
              % truth["endpoint"])
        case("unguarded-tag-must-fail-C1", ["C1"])
        # 负样本 2（C2）：端点换成他人账号
        write('%s\n<script data-goatcounter="https://someone-else.goatcounter.com/count" '
              'async src="static/js/goatcounter.js"></script>\n' % truth["mark"])
        case("foreign-endpoint-must-fail-C2", ["C2"])
        # 负样本 3（C3）：影子脚本
        write(canonical)
        touch(legacy, "// second tracker\n")
        case("shadow-tracker-must-fail-C3", ["C3"])
        os.remove(legacy)
        # 负样本 4（C4）：第二个注入入口（追踪标签形态）
        touch(adhoc, 'TAG = "<script data-goatcounter=…>"\n')
        case("second-injector-must-fail-C4", ["C4"])
        os.remove(adhoc)
        # 负样本 5（C4·事件属性形态）：W1167 自证抓出的判据不精确形态——
        # 只写 data-goatcounter-click 的越权脚本同样必须拦（前缀子串版会把它误当标签命中，
        # 精确分形态后它一度漏网；本例锁住「两种形态都在写入口面内」）
        touch(adhoc, 'ATTR = \'data-goatcounter-click="nav-hacked"\'\n')
        case("second-event-writer-must-fail-C4", ["C4"])
        os.remove(adhoc)
        # 负样本 6（C5）：CSP 白名单与配置正本分叉
        desync = dict(truth)
        desync["csp_hosts"] = {"other.goatcounter.com"}
        case("csp-desync-must-fail-C5", ["C5"], desync)
        os.remove(tracker)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if ok:
        print("SELF_TEST_OK")
        return 0
    print("SELF_TEST_FAIL")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description="统计具名例外面对账守卫（W806 建立·W1167 重指向）")
    ap.add_argument("--self-test", action="store_true", help="注入式自测（不触仓库）")
    args = ap.parse_args()

    if args.self_test:
        return _self_test()

    root = _repo_root()
    site_dir = os.path.join(root, "site")
    scripts_dir = os.path.join(root, "scripts")
    if not os.path.isdir(site_dir) or not os.path.isdir(scripts_dir):
        print("环境错误：未找到 site/ 或 scripts/ 目录", file=sys.stderr)
        return 2
    try:
        truth = _load_truth()
    except OSError as exc:
        print("环境错误：%s（fail-closed，不静默放行）" % exc, file=sys.stderr)
        return 2

    fails = scan(site_dir, scripts_dir, truth)
    print(MARKER + ("%d FAIL" % len(fails) if fails else
                    "0 FAIL（例外面==具名全集·端点 %s·脚本 %s）"
                    % (truth["endpoint_host"], truth["canon_script"])))
    for msg in fails[:20]:
        print("  FAIL", msg)
    if len(fails) > 20:
        print("  ...（其余 %d 条略）" % (len(fails) - 20))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
