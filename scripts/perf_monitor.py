# -*- coding: utf-8 -*-
"""W236-E E6 性能监控·Core Web Vitals 持续监控·Playwright + Lighthouse

对 site/ 下全部页面进行 Core Web Vitals 持续监控，输出 JSON + Markdown 报告。

监控 5 项核心指标：
  - LCP  Largest Contentful Paint  （≤2.5s 优良）
  - CLS  Cumulative Layout Shift   （≤0.1 优良）
  - INP  Interaction to Next Paint （≤200ms 优良）
  - TBT  Total Blocking Time       （≤200ms 优良）
  - FCP  First Contentful Paint    （≤1.8s 优良）

用法：
    py scripts/perf_monitor.py --target site/data/timeline.html
    py scripts/perf_monitor.py --all
    py scripts/perf_monitor.py --all --output scripts/output/perf-report.md

实现说明：
  - 优先使用 Playwright 真实浏览器采集 web vitals（LCP/CLS/FCP/INP）；
  - 若 lighthouse-cli 可用则补充 TBT 与全量审计分数；
  - 任一环境缺失时降级为静态启发式估算（基于 HTML 体积/脚本数/同步阻塞），
    保证脚本在无浏览器环境仍可输出可读报告。
仅依赖 stdlib + 可选 playwright/lighthouse。
"""
import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"
DATA_DIR = SITE_DIR / "data"
DEFAULT_OUTPUT = ROOT / "scripts" / "output" / "perf-report.md"
DEFAULT_JSON = ROOT / "scripts" / "output" / "perf-report.json"

# 指标优良阈值（秒/无量纲），来源于 web.dev/vitals
THRESHOLDS = {
    "LCP": {"good": 2.5, "needs": 4.0},   # 秒
    "CLS": {"good": 0.1, "needs": 0.25},  # 无量纲
    "INP": {"good": 0.2, "needs": 0.5},   # 秒
    "TBT": {"good": 0.2, "needs": 0.6},   # 秒
    "FCP": {"good": 1.8, "needs": 3.0},   # 秒
}


# ---------------------------------------------------------------------------
# 页面发现
# ---------------------------------------------------------------------------

def discover_pages():
    """发现 site/ 下所有 HTML 页面（含 dashboard/index + data/* 共 68+ 页）。"""
    pages = []
    if (SITE_DIR / "index.html").exists():
        pages.append(SITE_DIR / "index.html")
    if (SITE_DIR / "dashboard.html").exists():
        pages.append(SITE_DIR / "dashboard.html")
    if DATA_DIR.exists():
        pages.extend(sorted(DATA_DIR.glob("*.html")))
    return pages


def file_url(path):
    return "file:///" + str(path).replace("\\", "/")


# ---------------------------------------------------------------------------
# 采集器：Playwright 真实浏览器
# ---------------------------------------------------------------------------

VITALS_SCRIPT = """
() => {
  return new Promise((resolve) => {
    const result = { LCP: 0, CLS: 0, FCP: 0, INP: 0 };
    const obs = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.entryType === 'largest-contentful-paint') result.LCP = entry.startTime / 1000;
        if (entry.entryType === 'layout-shift') result.CLS += entry.value;
        if (entry.entryType === 'first-contentful-paint') result.FCP = entry.startTime / 1000;
        if (entry.entryType === 'event' && entry.interactionId) {
          result.INP = Math.max(result.INP, entry.duration / 1000);
        }
      }
    });
    try {
      obs.observe({ type: 'largest-contentful-paint', buffered: true });
      obs.observe({ type: 'layout-shift', buffered: true });
      obs.observe({ type: 'first-contentful-paint', buffered: true });
      obs.observe({ type: 'event', buffered: true });
    } catch (e) { /* 老版本浏览器不支持 */ }
    setTimeout(() => { resolve(result); }, 2500);
  });
}
"""


def collect_with_playwright(pages):
    """尝试用 Playwright 采集 web vitals，失败返回 None。"""
    try:
        from playwright.sync_api import sync_playwright  # noqa: WPS433
    except ImportError:
        return None
    results = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        try:
            for p in pages:
                ctx = browser.new_context(viewport={"width": 1280, "height": 800})
                page = ctx.new_page()
                vitals = {"LCP": 0.0, "CLS": 0.0, "FCP": 0.0, "INP": 0.0}
                try:
                    page.goto(file_url(p), wait_until="networkidle", timeout=15000)
                    page.wait_for_timeout(2000)
                    vitals = page.evaluate(VITALS_SCRIPT)
                except Exception as exc:  # noqa: BLE001
                    vitals = {"error": str(exc)}
                results[p.name] = vitals
                # TBT 无法直接采集，留待 lighthouse 或启发式补齐
                results[p.name].setdefault("TBT", None)
                ctx.close()
        finally:
            browser.close()
    return results


def collect_tbt_with_lighthouse(pages):
    """若 lighthouse-cli 可用，补充 TBT；失败返回空 dict。"""
    tbt_map = {}
    if not _has_command("lighthouse"):
        return tbt_map
    for p in pages:
        try:
            proc = subprocess.run(
                ["lighthouse", file_url(p), "--output=json", "--quiet", "--chrome-flags=--headless"],
                capture_output=True, text=True, timeout=60, check=False,
            )
            data = json.loads(proc.stdout) if proc.stdout else {}
            audits = data.get("audits", {})
            tbt = audits.get("total-blocking-time", {}).get("numericValue")
            if tbt is not None:
                tbt_map[p.name] = tbt / 1000.0
        except Exception:  # noqa: BLE001
            continue
    return tbt_map


# ---------------------------------------------------------------------------
# 降级采集：静态启发式估算
# ---------------------------------------------------------------------------

SCRIPT_RE = re.compile(r"<script\b[^>]*>", re.IGNORECASE)
SYNC_SCRIPT_RE = re.compile(r"<script\b(?![^>]*\b(?:async|defer)\b)[^>]*>", re.IGNORECASE)
CSS_RE = re.compile(r"<link\b[^>]*rel=['\"]stylesheet['\"][^>]*>", re.IGNORECASE)
IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)


def heuristic_metrics(html_text):
    """基于 HTML 静态特征估算 Core Web Vitals（无浏览器环境降级方案）。"""
    size_kb = len(html_text.encode("utf-8")) / 1024
    n_scripts = len(SCRIPT_RE.findall(html_text))
    n_sync = len(SYNC_SCRIPT_RE.findall(html_text))
    n_css = len(CSS_RE.findall(html_text))
    n_imgs = len(IMG_RE.findall(html_text))
    # 经验估算公式：体积主导 LCP/FCP，同步脚本主导 TBT/INP，图片+css 主导 CLS
    fcp = round(0.4 + size_kb / 200, 3)
    lcp = round(fcp + 0.3 + n_imgs * 0.05, 3)
    tbt = round(n_sync * 0.08 + n_css * 0.02, 3)
    inp = round(n_sync * 0.05 + 0.05, 3)
    cls = round(min(0.25, n_imgs * 0.008 + n_css * 0.005), 3)
    return {"LCP": lcp, "CLS": cls, "INP": inp, "TBT": tbt, "FCP": fcp,
            "_heuristic": True, "_size_kb": round(size_kb, 1),
            "_scripts": n_scripts, "_sync_scripts": n_sync}


# ---------------------------------------------------------------------------
# 评级
# ---------------------------------------------------------------------------

def grade(metric, value):
    """返回 good/needs/poor 三档评级。"""
    if value is None:
        return "n/a"
    th = THRESHOLDS[metric]
    if value <= th["good"]:
        return "good"
    if value <= th["needs"]:
        return "needs"
    return "poor"


# ---------------------------------------------------------------------------
# 报告生成
# ---------------------------------------------------------------------------

def build_report(results, scan_mode, duration):
    """组装报告数据结构 + markdown 文本。"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = {"total": len(results), "good": 0, "needs": 0, "poor": 0, "errors": 0}
    metric_stats = {m: {"good": 0, "needs": 0, "poor": 0} for m in THRESHOLDS}
    for name, vitals in results.items():
        if "error" in vitals:
            summary["errors"] += 1
            continue
        for m in THRESHOLDS:
            g = grade(m, vitals.get(m))
            if g == "good":
                metric_stats[m]["good"] += 1
                summary["good"] += 1
            elif g == "needs":
                metric_stats[m]["needs"] += 1
                summary["needs"] += 1
            elif g == "poor":
                metric_stats[m]["poor"] += 1
                summary["poor"] += 1

    md = []
    md.append("# W236-E Core Web Vitals 性能监控报告\n")
    md.append(f"- 扫描时间：{timestamp}")
    md.append(f"- 扫描模式：{scan_mode}")
    md.append(f"- 页面总数：{summary['total']}")
    md.append(f"- 耗时：{duration:.1f}s")
    md.append(f"- 汇总：good={summary['good']} / needs={summary['needs']} / poor={summary['poor']} / errors={summary['errors']}\n")
    md.append("## 一、5 项指标分布\n")
    md.append("| 指标 | 优良阈值 | good | needs | poor |")
    md.append("|------|---------|------|-------|------|")
    for m, th in THRESHOLDS.items():
        s = metric_stats[m]
        md.append(f"| {m} | ≤{th['good']} | {s['good']} | {s['needs']} | {s['poor']} |")
    md.append("\n## 二、逐页明细（前 20 条）\n")
    md.append("| 页面 | LCP | CLS | INP | TBT | FCP | 评级 |")
    md.append("|------|-----|-----|-----|-----|-----|------|")
    for name, vitals in list(results.items())[:20]:
        if "error" in vitals:
            md.append(f"| {name} | - | - | - | - | - | error |")
            continue
        lcp = vitals.get("LCP", 0)
        cls = vitals.get("CLS", 0)
        inp = vitals.get("INP", 0)
        tbt = vitals.get("TBT") or 0
        fcp = vitals.get("FCP", 0)
        worst = "good"
        for m, v in [("LCP", lcp), ("CLS", cls), ("INP", inp), ("TBT", tbt), ("FCP", fcp)]:
            g = grade(m, v)
            if g == "poor":
                worst = "poor"
                break
            if g == "needs" and worst != "poor":
                worst = "needs"
        flag = "" if vitals.get("_heuristic") else " ｜ 实测"
        md.append(f"| {name}{flag} | {lcp} | {cls} | {inp} | {tbt} | {fcp} | {worst} |")
    md.append("\n## 三、趋势分析\n")
    md.append("- LCP：D3 力导向图页面（narratology/character-network）通常偏高，需关注渲染阻塞。")
    md.append("- CLS：图表异步加载页易出现布局抖动，建议为容器预留宽高。")
    md.append("- INP：同步脚本密集页交互响应偏弱，需拆分长任务。")
    md.append("- TBT：依赖 lighthouse 采集；降级模式下按同步脚本数估算。")
    md.append("- FCP：体积主导，HTML > 200KB 的页面建议拆分懒加载。\n")
    md.append("## 四、优化建议\n")
    md.append("1. 为 D3 容器设置固定宽高，消除 CLS 抖动。")
    md.append("2. 给非首屏 `<script>` 加 `defer`，降低 TBT/INP。")
    md.append("3. 大型网络图（13d/monster-hierarchy）启用 `requestIdleCallback` 分片渲染。")
    md.append("4. 图片资源补全 `width/height` 或 `aspect-ratio`。")
    md.append("5. 持续以 `--all` 周期扫描，对比历史 JSON 追踪回归。\n")
    report = {
        "version": "W236-E",
        "timestamp": timestamp,
        "scan_mode": scan_mode,
        "duration_sec": round(duration, 2),
        "summary": summary,
        "metric_stats": metric_stats,
        "thresholds": THRESHOLDS,
        "pages": results,
    }
    return report, "\n".join(md)


# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------

def _has_command(cmd):
    try:
        subprocess.run([cmd, "--version"], capture_output=True, timeout=10, check=False)
        return True
    except Exception:  # noqa: BLE001
        return False


def parse_args(argv):
    ap = argparse.ArgumentParser(description="W236-E Core Web Vitals 持续监控")
    ap.add_argument("--target", help="单页面相对路径，例如 site/data/timeline.html")
    ap.add_argument("--all", action="store_true", help="扫描全部 68 页面")
    ap.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Markdown 报告输出路径")
    ap.add_argument("--json", default=str(DEFAULT_JSON), help="JSON 报告输出路径")
    return ap.parse_args(argv)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def run(argv=None):
    args = parse_args(argv or sys.argv[1:])
    if not args.target and not args.all:
        print("错误：需指定 --target 或 --all", file=sys.stderr)
        return 2

    if args.target:
        target = ROOT / args.target if not Path(args.target).is_absolute() else Path(args.target)
        pages = [target]
        scan_mode = f"single:{target.name}"
    else:
        pages = discover_pages()
        scan_mode = "all"

    pages = [p for p in pages if p.exists()]
    if not pages:
        print("错误：未发现可扫描页面", file=sys.stderr)
        return 2

    print(f"W236-E 性能监控启动：{len(pages)} 页面 · 模式 {scan_mode}")
    start = time.time()

    results = collect_with_playwright(pages)
    if results is None:
        print("Playwright 不可用，降级为静态启发式估算。")
        results = {}
        for p in pages:
            try:
                results[p.name] = heuristic_metrics(p.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                results[p.name] = {"error": str(exc)}
    else:
        tbt_map = collect_tbt_with_lighthouse(pages)
        for name, vitals in results.items():
            if name in tbt_map:
                vitals["TBT"] = tbt_map[name]

    duration = time.time() - start
    report, md = build_report(results, scan_mode, duration)

    out_md = Path(args.output)
    out_json = Path(args.json)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md, encoding="utf-8")
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"报告已生成：{out_md}")
    print(f"JSON 已生成：{out_json}")
    print(f"耗时 {duration:.1f}s · good={report['summary']['good']} needs={report['summary']['needs']} poor={report['summary']['poor']}")
    # 存在 poor 视为需关注，返回 1
    return 1 if report["summary"]["poor"] > 0 else 0


if __name__ == "__main__":
    sys.exit(run())
# FILE_INDEX: scripts/perf_monitor.py | W236-E | E6 性能监控
