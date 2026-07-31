# -*- coding: utf-8 -*-
"""W267 E6 性能监控深化·Core Web Vitals 持续监控 + RUM + 警报 + 趋势 + 预算

v2.2.47 · W267 · 在 W236-E 基础上深化：
  - RUM 真实用户监控：解析 site/js/rum.js 采集的浏览器端指标
  - Core Web Vitals alerting：LCP>2.5s / CLS>0.1 / INP>200ms 触发警报
  - 历史趋势对比：对比当前快照与基线 perf-baseline.json
  - 性能预算验证：HTML/CSS/JS/图片/字体/总量超预算即报告

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
    py scripts/perf_monitor.py --rum scripts/output/rum-events.json
    py scripts/perf_monitor.py --check-budget scripts/output/perf-budget.json
    py scripts/perf_monitor.py --compare-trend scripts/output/perf-baseline.json

实现说明：
  - 优先使用 Playwright 真实浏览器采集 web vitals（LCP/CLS/FCP/INP）；
  - 若 lighthouse-cli 可用则补充 TBT 与全量审计分数；
  - 任一环境缺失时降级为静态启发式估算（基于 HTML 体积/脚本数/同步阻塞），
    保证脚本在无浏览器环境仍可输出可读报告。
  - W267 新增：RUM 解析 + 阈值警报 + 趋势对比 + 预算校验，可独立调用。
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
RUM_JS_PATH = SITE_DIR / "js" / "rum.js"
DEFAULT_BUDGET = ROOT / "scripts" / "output" / "perf-budget.json"
DEFAULT_BASELINE = ROOT / "scripts" / "output" / "perf-baseline.json"

# W267 · Core Web Vitals 警报阈值（秒/无量纲）—— 超过即触发 alert
ALERT_THRESHOLDS = {
    "lcp": 2.5,   # 秒
    "cls": 0.1,   # 无量纲
    "inp": 0.2,   # 秒（200ms）
}

# W267 · 资源体积分类正则（用于性能预算校验）
RESOURCE_EXT_MAP = {
    "html": {".html", ".htm"},
    "css": {".css"},
    "js": {".js", ".mjs"},
    "image": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif", ".ico"},
    "font": {".woff", ".woff2", ".ttf", ".otf", ".eot"},
}

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
# W267 · RUM 真实用户监控·解析浏览器端采集数据
# ---------------------------------------------------------------------------

def collect_rum_metrics(rum_source):
    """解析 site/js/rum.js 采集并发送至 /api/rum 的 RUM 数据。

    支持两种输入：
      - 文件路径（str/Path）：读取 JSON 文件（单对象或 events 数组）
      - 已解析的 dict / list：直接使用

    rum.js 上报数据格式（单条事件）：
        {
          "page": "index.html",
          "ts": 1719000000000,
          "metrics": {"lcp": 1.2, "cls": 0.05, "inp": 0.15, "tbt": 0.2, "fcp": 0.8},
          "nav": "navigate",
          "ua": "Mozilla/5.0 ..."
        }

    返回统一结构的 dict：
        {
          "events": int,            # 事件总数
          "pages": {page: {lcp, cls, inp, tbt, fcp, samples}},
          "aggregate": {lcp_p75, cls_p75, inp_p75, tbt_p75, fcp_p75},
          "alerts": [...]           # 触发的警报（委托 check_alerts）
        }
    """
    if isinstance(rum_source, (str, Path)):
        rum_path = Path(rum_source)
        if not rum_path.exists():
            return {"error": f"RUM 数据文件不存在: {rum_path}", "events": 0,
                    "pages": {}, "aggregate": {}, "alerts": []}
        try:
            data = json.loads(rum_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return {"error": f"RUM 数据 JSON 解析失败: {exc}", "events": 0,
                    "pages": {}, "aggregate": {}, "alerts": []}
    else:
        data = rum_source

    # 归一化为事件列表
    if isinstance(data, dict) and "events" in data and isinstance(data["events"], list):
        events = data["events"]
    elif isinstance(data, list):
        events = data
    elif isinstance(data, dict):
        events = [data]
    else:
        return {"error": "RUM 数据格式不被支持（需 dict/list/events 数组）",
                "events": 0, "pages": {}, "aggregate": {}, "alerts": []}

    pages = {}
    for ev in events:
        if not isinstance(ev, dict):
            continue
        metrics = ev.get("metrics", {})
        page = ev.get("page", "unknown")
        bucket = pages.setdefault(page, {
            "lcp": [], "cls": [], "inp": [], "tbt": [], "fcp": [], "samples": 0,
        })
        for key in ("lcp", "cls", "inp", "tbt", "fcp"):
            val = metrics.get(key)
            if isinstance(val, (int, float)) and val >= 0:
                bucket[key].append(val)
        bucket["samples"] += 1

    # 计算每页 P75（Core Web Vitals 官方百分位）
    def _p75(values):
        if not values:
            return None
        ordered = sorted(values)
        idx = max(0, int(len(ordered) * 0.75) - 1)
        return round(ordered[idx], 4)

    aggregate = {}
    for key in ("lcp", "cls", "inp", "tbt", "fcp"):
        all_vals = []
        for bucket in pages.values():
            all_vals.extend(bucket[key])
        aggregate[f"{key}_p75"] = _p75(all_vals)

    # 汇总每页 P75 用于警报判定
    page_summary = {}
    for page, bucket in pages.items():
        page_summary[page] = {
            "lcp": _p75(bucket["lcp"]),
            "cls": _p75(bucket["cls"]),
            "inp": _p75(bucket["inp"]),
            "tbt": _p75(bucket["tbt"]),
            "fcp": _p75(bucket["fcp"]),
            "samples": bucket["samples"],
        }

    alerts = check_alerts(page_summary)

    return {
        "events": len(events),
        "pages": page_summary,
        "aggregate": aggregate,
        "alerts": alerts,
    }


# ---------------------------------------------------------------------------
# W267 · Core Web Vitals alerting 阈值警报
# ---------------------------------------------------------------------------

def check_alerts(metrics):
    """对 Core Web Vitals 指标进行阈值校验，触发警报列表。

    阈值（来源于 web.dev 官方"良好"边界）：
      - LCP > 2.5s   → alert
      - CLS > 0.1    → alert
      - INP > 200ms  → alert（0.2 秒）

    入参 metrics 支持两种形式：
      - 单页面：{"lcp": 1.2, "cls": 0.05, "inp": 0.15, ...}
      - 多页面：{"index.html": {"lcp": ...}, "dashboard.html": {...}}

    返回警报列表，每条形如：
        {"page": "index.html", "metric": "lcp", "value": 3.1,
         "threshold": 2.5, "severity": "high", "message": "..."}
    """
    alerts = []

    def _inspect(page_name, values):
        if not isinstance(values, dict):
            return
        for metric, threshold in ALERT_THRESHOLDS.items():
            val = values.get(metric)
            if not isinstance(val, (int, float)):
                continue
            if val > threshold:
                # 二次判定严重度：超过 needs 阈值视为 high，否则 medium
                if metric == "lcp":
                    severity = "high" if val > 4.0 else "medium"
                elif metric == "cls":
                    severity = "high" if val > 0.25 else "medium"
                else:  # inp
                    severity = "high" if val > 0.5 else "medium"
                unit = "s" if metric in ("lcp", "inp") else ""
                alerts.append({
                    "page": page_name,
                    "metric": metric.upper(),
                    "value": val,
                    "threshold": threshold,
                    "severity": severity,
                    "message": (
                        f"{metric.upper()}={val}{unit} 超过阈值 {threshold}{unit}"
                        f"（页面 {page_name}）"
                    ),
                })

    # 多页面：dict 的 value 是 dict
    if metrics and all(isinstance(v, dict) for v in metrics.values()):
        for page, values in metrics.items():
            _inspect(page, values)
    elif isinstance(metrics, dict):
        # 单页面：直接校验
        _inspect("current", metrics)

    # 按严重度排序（high 优先）
    severity_rank = {"high": 0, "medium": 1, "low": 2}
    alerts.sort(key=lambda a: (severity_rank.get(a["severity"], 9), a["page"]))
    return alerts


# ---------------------------------------------------------------------------
# W267 · 历史趋势对比·当前快照 vs 基线
# ---------------------------------------------------------------------------

def compare_trend(current, baseline):
    """对比当前 Core Web Vitals 快照与历史基线，输出回归/改善明细。

    入参：
      - current: dict，形如 {"index.html": {"lcp": 1.2, "cls": 0.05, ...}, ...}
                 若传入 perf-report.json 的 pages 字段（含 LCP/CLS/... 大写键），
                 会自动归一化为小写键。
      - baseline: dict 或文件路径。
                 若为路径则读取 perf-baseline.json；
                 若为 dict 且含 "pages" 键则取其 pages 子对象。

    返回：
        {
          "regressions": [...],   # 指标变差（delta > 0 视为回归）
          "improvements": [...],  # 指标改善
          "unchanged": [...],
          "new_pages": [...],     # 当前存在但基线无
          "removed_pages": [...], # 基线存在但当前无
          "summary": {"regressions": n, "improvements": n, "unchanged": n}
        }
    """
    # 归一化 current
    current_norm = _normalize_vitals(current)
    # 归一化 baseline
    if isinstance(baseline, (str, Path)):
        bl_path = Path(baseline)
        if not bl_path.exists():
            return {"error": f"基线文件不存在: {bl_path}",
                    "regressions": [], "improvements": [],
                    "unchanged": [], "new_pages": [], "removed_pages": [],
                    "summary": {"regressions": 0, "improvements": 0, "unchanged": 0}}
        try:
            baseline_data = json.loads(bl_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return {"error": f"基线 JSON 解析失败: {exc}",
                    "regressions": [], "improvements": [],
                    "unchanged": [], "new_pages": [], "removed_pages": [],
                    "summary": {"regressions": 0, "improvements": 0, "unchanged": 0}}
    else:
        baseline_data = baseline

    if isinstance(baseline_data, dict) and "pages" in baseline_data:
        baseline_pages = baseline_data["pages"]
        baseline_unit = baseline_data.get("unit", {})
    else:
        baseline_pages = baseline_data or {}
        baseline_unit = {}

    # 单位对齐：若基线声明 lcp/inp/tbt/fcp 单位为 milliseconds，
    # 则转换为 seconds（与 perf_monitor 内部表示一致）。
    # CLS 为无量纲，无需转换。
    baseline_pages = _convert_baseline_units(baseline_pages, baseline_unit)

    baseline_norm = _normalize_vitals(baseline_pages)

    regressions = []
    improvements = []
    unchanged = []
    new_pages = []
    removed_pages = []

    cur_pages = set(current_norm.keys())
    bl_pages = set(baseline_norm.keys())
    new_pages.extend(sorted(cur_pages - bl_pages))
    removed_pages.extend(sorted(bl_pages - cur_pages))

    metrics_keys = ("lcp", "cls", "inp", "tbt", "fcp")
    for page in sorted(cur_pages & bl_pages):
        cur_v = current_norm[page]
        bl_v = baseline_norm[page]
        for key in metrics_keys:
            cv = cur_v.get(key)
            bv = bl_v.get(key)
            if not isinstance(cv, (int, float)) or not isinstance(bv, (int, float)):
                continue
            if bv == 0:
                # 基线为 0 时只要有数值即视为新增（避免除零）
                delta = cv
                ratio = 1.0 if cv > 0 else 0.0
            else:
                delta = round(cv - bv, 4)
                ratio = round((cv - bv) / bv, 4)
            # 容忍 5% 抖动，避免噪声
            if abs(ratio) < 0.05 and abs(delta) < 0.02:
                unchanged.append({"page": page, "metric": key.upper(),
                                  "current": cv, "baseline": bv,
                                  "delta": delta, "delta_pct": ratio})
            elif delta > 0:
                regressions.append({"page": page, "metric": key.upper(),
                                    "current": cv, "baseline": bv,
                                    "delta": delta, "delta_pct": ratio})
            else:
                improvements.append({"page": page, "metric": key.upper(),
                                     "current": cv, "baseline": bv,
                                     "delta": delta, "delta_pct": ratio})

    return {
        "regressions": regressions,
        "improvements": improvements,
        "unchanged": unchanged,
        "new_pages": new_pages,
        "removed_pages": removed_pages,
        "summary": {
            "regressions": len(regressions),
            "improvements": len(improvements),
            "unchanged": len(unchanged),
        },
    }


def _normalize_vitals(pages_data):
    """将 perf-report.json 的 pages（含大写 LCP/CLS/...）归一化为小写键。

    同时接受 perf-baseline.json 的 {"lcp": ..., "cls": ...} 格式。
    """
    if not isinstance(pages_data, dict):
        return {}
    key_map = {"LCP": "lcp", "CLS": "cls", "INP": "inp", "TBT": "tbt", "FCP": "fcp"}
    normalized = {}
    for page, vals in pages_data.items():
        if not isinstance(vals, dict):
            continue
        item = {}
        for k, v in vals.items():
            if k in key_map:
                item[key_map[k]] = v
            elif k in ("lcp", "cls", "inp", "tbt", "fcp"):
                item[k] = v
        if item:
            normalized[page] = item
    return normalized


def _convert_baseline_units(pages_data, unit_map):
    """根据基线的 unit 声明，将毫秒值转换为秒（与 perf_monitor 内部一致）。

    unit_map 形如 {"lcp": "milliseconds", "cls": "dimensionless", ...}
    仅对声明为 milliseconds / ms 的指标做 /1000 转换。
    """
    if not isinstance(pages_data, dict) or not isinstance(unit_map, dict):
        return pages_data
    ms_markers = {"milliseconds", "ms", "millisecond"}
    needs_convert = {k for k, u in unit_map.items()
                     if isinstance(u, str) and u.lower() in ms_markers}
    if not needs_convert:
        return pages_data
    converted = {}
    for page, vals in pages_data.items():
        if not isinstance(vals, dict):
            converted[page] = vals
            continue
        item = dict(vals)
        for key in needs_convert:
            if key in item and isinstance(item[key], (int, float)):
                item[key] = round(item[key] / 1000.0, 6)
        converted[page] = item
    return converted


# ---------------------------------------------------------------------------
# W267 · 性能预算验证·资源体积校验
# ---------------------------------------------------------------------------

def check_budget(budget):
    """校验 site/ 下资源体积是否超出性能预算。

    入参 budget 支持：
      - 文件路径（str/Path）：读取 perf-budget.json
      - dict：直接使用预算配置

    预算配置格式（单位 bytes）：
        {"html": 51200, "css": 102400, "js": 204800,
         "image": 512000, "font": 102400, "total": 921600}

    返回：
        {
          "budget": {...},
          "actual": {"html": N, "css": N, ..., "total": N},
          "violations": [{"category": "js", "actual": 250000,
                          "budget": 204800, "over": 45200, "severity": "high"}],
          "summary": {"total_categories": 6, "violations": n, "passed": bool}
        }
    """
    if isinstance(budget, (str, Path)):
        budget_path = Path(budget)
        if not budget_path.exists():
            return {"error": f"预算文件不存在: {budget_path}",
                    "budget": {}, "actual": {}, "violations": [],
                    "summary": {"total_categories": 0, "violations": 0, "passed": False}}
        try:
            budget_cfg = json.loads(budget_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return {"error": f"预算 JSON 解析失败: {exc}",
                    "budget": {}, "actual": {}, "violations": [],
                    "summary": {"total_categories": 0, "violations": 0, "passed": False}}
    elif isinstance(budget, dict):
        budget_cfg = budget
    else:
        return {"error": "budget 参数需为路径或 dict",
                "budget": {}, "actual": {}, "violations": [],
                "summary": {"total_categories": 0, "violations": 0, "passed": False}}

    # 统计 site/ 下所有资源体积，按类别归集
    actual = {cat: 0 for cat in RESOURCE_EXT_MAP}
    actual["total"] = 0
    if SITE_DIR.exists():
        for p in SITE_DIR.rglob("*"):
            if not p.is_file():
                continue
            # 跳过 .thumbnails / current / baseline 等非生产资源
            if any(seg in {"node_modules", "current", "baseline", ".thumbnails"}
                   for seg in p.parts):
                continue
            ext = p.suffix.lower()
            size = p.stat().st_size
            categorized = False
            for cat, exts in RESOURCE_EXT_MAP.items():
                if ext in exts:
                    actual[cat] += size
                    categorized = True
                    break
            # 所有文件计入 total（含未分类资源）
            actual["total"] += size

    # 仅识别有效的预算类别（过滤 JSON 中的 version/description 等元数据字段）
    valid_categories = set(RESOURCE_EXT_MAP.keys()) | {"total"}
    budget_clean = {k: v for k, v in budget_cfg.items()
                    if k in valid_categories and isinstance(v, int) and v > 0}

    violations = []
    for cat, limit in budget_clean.items():
        used = actual.get(cat, 0)
        if used > limit:
            over = used - limit
            # 严重度：超 50% 为 high，超 20% 为 medium，否则 low
            ratio = over / limit
            if ratio >= 0.5:
                severity = "high"
            elif ratio >= 0.2:
                severity = "medium"
            else:
                severity = "low"
            violations.append({
                "category": cat,
                "actual": used,
                "budget": limit,
                "over": over,
                "over_pct": round(ratio, 4),
                "severity": severity,
                "message": (
                    f"{cat} 资源 {used} bytes 超出预算 {limit} bytes"
                    f"（超出 {over} bytes，{ratio*100:.1f}%）"
                ),
            })

    violations.sort(key=lambda v: ({"high": 0, "medium": 1, "low": 2}.get(v["severity"], 9),
                                   -v["over"]))
    return {
        "budget": budget_clean,
        "actual": actual,
        "violations": violations,
        "summary": {
            "total_categories": len(budget_clean),
            "violations": len(violations),
            "passed": len(violations) == 0,
        },
    }


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

def build_report(results, scan_mode, duration, alerts=None, rum=None, trend=None, budget=None):
    """组装报告数据结构 + markdown 文本。

    W267 扩展：可选传入 alerts / rum / trend / budget 子报告，整合到最终输出。
    """
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
    md.append("# W267 Core Web Vitals 性能监控报告\n")
    md.append(f"- 版本：v2.2.47 · W267 · E6 性能监控深化")
    md.append(f"- 扫描时间：{timestamp}")
    md.append(f"- 扫描模式：{scan_mode}")
    md.append(f"- 页面总数：{summary['total']}")
    md.append(f"- 耗时：{duration:.1f}s")
    md.append(f"- 汇总：good={summary['good']} / needs={summary['needs']} / poor={summary['poor']} / errors={summary['errors']}")
    if alerts:
        md.append(f"- 警报：{len(alerts)} 条（high={sum(1 for a in alerts if a['severity']=='high')}"
                  f" / medium={sum(1 for a in alerts if a['severity']=='medium')}）")
    md.append("")
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
    md.append("- FCP：体积主导，HTML > 200KB 的页面建议拆分懒加载。")

    # W267 · Core Web Vitals 警报
    if alerts:
        md.append("\n## 四、W267 · Core Web Vitals 警报\n")
        md.append(f"共 {len(alerts)} 条警报（阈值：LCP>2.5s / CLS>0.1 / INP>200ms）。\n")
        md.append("| 严重度 | 页面 | 指标 | 当前值 | 阈值 | 说明 |")
        md.append("|--------|------|------|--------|------|------|")
        for a in alerts[:30]:
            md.append(f"| {a['severity']} | {a['page']} | {a['metric']} | {a['value']} | {a['threshold']} | {a['message']} |")

    # W267 · RUM 真实用户监控
    if rum and "error" not in rum:
        md.append("\n## 五、W267 · RUM 真实用户监控\n")
        md.append(f"- 事件总数：{rum.get('events', 0)}")
        agg = rum.get("aggregate", {})
        if agg:
            md.append("- 全站 P75 汇总：")
            for key in ("lcp_p75", "cls_p75", "inp_p75", "tbt_p75", "fcp_p75"):
                if key in agg and agg[key] is not None:
                    md.append(f"  - {key} = {agg[key]}")
        pages_rum = rum.get("pages", {})
        if pages_rum:
            md.append("\n| 页面 | LCP(P75) | CLS(P75) | INP(P75) | TBT(P75) | FCP(P75) | 样本 |")
            md.append("|------|----------|----------|----------|----------|----------|------|")
            for page, v in list(pages_rum.items())[:20]:
                md.append(f"| {page} | {v.get('lcp')} | {v.get('cls')} | {v.get('inp')} | {v.get('tbt')} | {v.get('fcp')} | {v.get('samples', 0)} |")
    elif rum and "error" in rum:
        md.append(f"\n## 五、W267 · RUM 真实用户监控\n\n- 错误：{rum['error']}\n")

    # W267 · 历史趋势对比
    if trend and "error" not in trend:
        md.append("\n## 六、W267 · 历史趋势对比\n")
        ts = trend.get("summary", {})
        md.append(f"- 回归 {ts.get('regressions', 0)} 项 / 改善 {ts.get('improvements', 0)} 项 / 持平 {ts.get('unchanged', 0)} 项")
        if trend.get("new_pages"):
            md.append(f"- 新增页面：{', '.join(trend['new_pages'])}")
        if trend.get("removed_pages"):
            md.append(f"- 移除页面：{', '.join(trend['removed_pages'])}")
        regressions = trend.get("regressions", [])
        if regressions:
            md.append("\n### 回归明细（前 20 条）\n")
            md.append("| 页面 | 指标 | 当前 | 基线 | delta | delta% |")
            md.append("|------|------|------|------|-------|--------|")
            for r in regressions[:20]:
                md.append(f"| {r['page']} | {r['metric']} | {r['current']} | {r['baseline']} | +{r['delta']} | +{r['delta_pct']*100:.1f}% |")
        improvements = trend.get("improvements", [])
        if improvements:
            md.append("\n### 改善明细（前 20 条）\n")
            md.append("| 页面 | 指标 | 当前 | 基线 | delta | delta% |")
            md.append("|------|------|------|------|-------|--------|")
            for imp in improvements[:20]:
                md.append(f"| {imp['page']} | {imp['metric']} | {imp['current']} | {imp['baseline']} | {imp['delta']} | {imp['delta_pct']*100:.1f}% |")
    elif trend and "error" in trend:
        md.append(f"\n## 六、W267 · 历史趋势对比\n\n- 错误：{trend['error']}\n")

    # W267 · 性能预算验证
    if budget and "error" not in budget:
        md.append("\n## 七、W267 · 性能预算验证\n")
        bp = budget.get("summary", {})
        md.append(f"- 类别数：{bp.get('total_categories', 0)}")
        md.append(f"- 违反：{bp.get('violations', 0)} 项")
        md.append(f"- 结论：{'通过' if bp.get('passed') else '未通过'}\n")
        md.append("| 类别 | 实际(bytes) | 预算(bytes) | 状态 |")
        md.append("|------|------------|------------|------|")
        actual = budget.get("actual", {})
        budget_cfg = budget.get("budget", {})
        all_cats = sorted(set(list(actual.keys()) + list(budget_cfg.keys())))
        for cat in all_cats:
            if cat == "total":
                continue
            used = actual.get(cat, 0)
            limit = budget_cfg.get(cat)
            if isinstance(limit, int) and limit > 0:
                status = "超出" if used > limit else "通过"
                md.append(f"| {cat} | {used} | {limit} | {status} |")
            else:
                md.append(f"| {cat} | {used} | - | 未设预算 |")
        if "total" in actual:
            total_limit = budget_cfg.get("total")
            if isinstance(total_limit, int) and total_limit > 0:
                status = "超出" if actual["total"] > total_limit else "通过"
                md.append(f"| **total** | **{actual['total']}** | **{total_limit}** | **{status}** |")
        violations = budget.get("violations", [])
        if violations:
            md.append("\n### 违反明细\n")
            for v in violations:
                md.append(f"- [{v['severity']}] {v['message']}")
    elif budget and "error" in budget:
        md.append(f"\n## 七、W267 · 性能预算验证\n\n- 错误：{budget['error']}\n")

    md.append("\n## 八、优化建议\n")
    md.append("1. 为 D3 容器设置固定宽高，消除 CLS 抖动。")
    md.append("2. 给非首屏 `<script>` 加 `defer`，降低 TBT/INP。")
    md.append("3. 大型网络图（13d/monster-hierarchy）启用 `requestIdleCallback` 分片渲染。")
    md.append("4. 图片资源补全 `width/height` 或 `aspect-ratio`。")
    md.append("5. 持续以 `--all` 周期扫描，对比历史 JSON 追踪回归。")
    md.append("6. W267 · 接入 site/js/rum.js 采集真实用户 Core Web Vitals，结合 P75 警报阈值闭环。")
    md.append("7. W267 · 性能预算纳入 CI，超预算资源阻止合并。\n")
    report = {
        "version": "W267",
        "version_detail": "v2.2.47",
        "timestamp": timestamp,
        "scan_mode": scan_mode,
        "duration_sec": round(duration, 2),
        "summary": summary,
        "metric_stats": metric_stats,
        "thresholds": THRESHOLDS,
        "alert_thresholds": ALERT_THRESHOLDS,
        "pages": results,
    }
    if alerts is not None:
        report["alerts"] = alerts
    if rum is not None:
        report["rum"] = rum
    if trend is not None:
        report["trend"] = trend
    if budget is not None:
        report["budget"] = budget
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
    ap = argparse.ArgumentParser(description="W267 Core Web Vitals 持续监控 + RUM + 趋势 + 预算")
    ap.add_argument("--target", help="单页面相对路径，例如 site/data/timeline.html")
    ap.add_argument("--all", action="store_true", help="扫描全部 68 页面")
    ap.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Markdown 报告输出路径")
    ap.add_argument("--json", default=str(DEFAULT_JSON), help="JSON 报告输出路径")
    # W267 新增参数
    ap.add_argument("--rum", help="RUM 数据文件路径（site/js/rum.js 上报的 JSON）")
    ap.add_argument("--check-budget", dest="check_budget",
                    default=str(DEFAULT_BUDGET),
                    help="性能预算配置路径（默认 scripts/output/perf-budget.json）")
    ap.add_argument("--compare-trend", dest="compare_trend",
                    default=str(DEFAULT_BASELINE),
                    help="基线快照路径用于趋势对比（默认 scripts/output/perf-baseline.json）")
    ap.add_argument("--no-trend", action="store_true", help="跳过趋势对比")
    ap.add_argument("--no-budget", action="store_true", help="跳过预算校验")
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

    print(f"W267 性能监控启动：{len(pages)} 页面 · 模式 {scan_mode}")
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

    # W267 · 阈值警报（基于采集结果，统一小写键）
    alerts_input = {}
    for name, vitals in results.items():
        if "error" in vitals:
            continue
        alerts_input[name] = {
            "lcp": vitals.get("LCP"),
            "cls": vitals.get("CLS"),
            "inp": vitals.get("INP"),
            "tbt": vitals.get("TBT"),
            "fcp": vitals.get("FCP"),
        }
    alerts = check_alerts(alerts_input)

    # W267 · RUM 真实用户监控
    rum_report = None
    if args.rum:
        print(f"W267 · 解析 RUM 数据：{args.rum}")
        rum_report = collect_rum_metrics(args.rum)
        # RUM 警报合并进主警报列表
        if rum_report and "alerts" in rum_report:
            alerts.extend(rum_report["alerts"])

    # W267 · 历史趋势对比
    trend_report = None
    if not args.no_trend and Path(args.compare_trend).exists():
        print(f"W267 · 趋势对比基线：{args.compare_trend}")
        trend_report = compare_trend(alerts_input, args.compare_trend)
    elif not args.no_trend:
        print(f"W267 · 基线不存在，跳过趋势对比：{args.compare_trend}")

    # W267 · 性能预算校验
    budget_report = None
    if not args.no_budget:
        print(f"W267 · 性能预算校验：{args.check_budget}")
        budget_report = check_budget(args.check_budget)

    report, md = build_report(results, scan_mode, duration, alerts=alerts,
                              rum=rum_report, trend=trend_report, budget=budget_report)

    out_md = Path(args.output)
    out_json = Path(args.json)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md, encoding="utf-8")
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"报告已生成：{out_md}")
    print(f"JSON 已生成：{out_json}")
    print(f"耗时 {duration:.1f}s · good={report['summary']['good']} needs={report['summary']['needs']} poor={report['summary']['poor']}")
    if alerts:
        print(f"W267 · 触发警报 {len(alerts)} 条（high={sum(1 for a in alerts if a['severity']=='high')}"
              f" / medium={sum(1 for a in alerts if a['severity']=='medium')}）")
    if budget_report and "summary" in budget_report:
        bp = budget_report["summary"]
        print(f"W267 · 预算校验：{'通过' if bp['passed'] else '违反 ' + str(bp['violations']) + ' 项'}")
    if trend_report and "summary" in trend_report:
        ts = trend_report["summary"]
        print(f"W267 · 趋势对比：回归 {ts['regressions']} / 改善 {ts['improvements']} / 持平 {ts['unchanged']}")
    # 存在 poor 或 high 警报或预算违反 视为需关注，返回 1
    has_high_alert = any(a["severity"] == "high" for a in alerts)
    has_budget_violation = bool(budget_report and budget_report.get("violations"))
    if report["summary"]["poor"] > 0 or has_high_alert or has_budget_violation:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run())
# FILE_INDEX: scripts/perf_monitor.py | W267 v2.2.47 | E6 性能监控深化（RUM+警报+趋势+预算）
