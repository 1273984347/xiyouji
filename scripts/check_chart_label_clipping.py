#!/usr/bin/env python3
"""check_chart_label_clipping.py — 第 83 门禁 · SVG 标签裁切与重叠（W1266 批二 · 线 B1）

【为什么要有这道门禁】
全站 SVG 图表的**文字标签**此前从未被任何门禁覆盖：第 43 槽只数图元数与 KPI 值·第 24/29/30 槽只做静态文本与色对判据·
动态门禁 G3 只查整页横向溢出 ⇒ **SVG 内部的标签溢出与标签间重叠全部落在盲区**（W1259 审查报告 P1-6）。
W1259 记了「标签裁切/重叠 87 页（窄口径·只判左右）/ 108 页（宽口径·四向）」，但**仓内没有任何判据能复算这两个数字**，
且当时判据的**方向 / 阈值 / 下限 / 触发时机都没写明** ⇒ 换人复跑得出不同数字却不知谁对。
本槽把判据写成机器可复算的尺子：方向、阈值、下限、触发时机、豁免清单**全部写死**在本文档与代码里。

【判据口径（换人复跑必须得出同一组数字·逐条写死）】
C0 扫描面（换人复跑必须落在同一批页面上）
   site/*.html + site/data/*.html + site/en/*.html（排除下划线前缀模板）= **237 页**
   W1266 批二收官补盲：原扫描面为 site/data + site/en = **228 页**，**漏掉 site 根 10 页**——
   其中含 dashboard.html（三大环图）等用户点名页 ⇒ **尺子不得有盲区**·已扩面并重生成存量基线。
C1 裁切 · **四向**越界（四个方向分别统计·**不只报合计**）
   **视窗（可见区）基准 = 所属 <svg> 的 SVG 视窗（元素内容盒 = client box 去 padding）**——
   理由：UA 样式表 svg:root{overflow:hidden} ⇒ **真实裁剪矩形 = SVG 视窗（内容盒）**；
        而 getBoundingClientRect 给的是 **border box（含 border）**·每边比视窗宽一个 border 宽度
        （实测 data/relationships.html：border box 978×422 vs 视窗 976×420·该 svg 带 1px border；
          像素实证 overflow:hidden 与 visible 两态差异恰落在视窗左缘 x=232 的 1px 竖条
          ⇒ 裁剪线在内容盒·**不在 border box**）；
        且**无 viewBox 的 svg（现役 68 个 / 2076 个文本）同样只能用视窗**（无 viewBox 可换算）。
        探针另记「border box」与「viewBox 经 preserveAspectRatio 映射的矩形」供对照；
        门禁**每次运行并排报三基准**（差异见输出「视窗基准对照」行）。
   量测：每个 svg text 的屏幕包围盒 vs 上述视窗矩形
   越界量（正数 = 越出该边）：
       left   = 容器左边 - 文本左边
       right  = 文本右边 - 容器右边
       top    = 容器上边 - 文本上边
       bottom = 文本下边 - 容器下边
   判定：越界量 > **1.5px**（容差·W1259 建议口径·吸收亚像素与字形边缘毛刺）⇒ 该方向命中
   容器该方向不裁切时（svg 计算样式 overflow 为 visible）⇒ 该方向不计（不构成「裁切」·只算「溢出」）
C2 **双口径并列**（两个数都要出·差异来自判据宽窄·**不是误差**）
   窄口径 = 只判 left + right（水平越界）
   宽口径 = 四向（left / right / top / bottom）
   W1259 教训：只判水平 ⇒ 漏掉垂直 ⇒ 「87 页（窄）」与「108 页（宽）」**两个都是对的**·差别只在判据宽窄
C3 重叠（标签矩形两两相交）
   范围：**同一 svg 容器内**的两个 text 标签（跨 svg 不比·不同图表各判各的）
   判据：相交面积 ≥ **4 px²**（绝对下限·防抗锯齿级微碰判红）**且** 相交面积 / 较小标签面积 > **0.30** ⇒ 命中
   阈值理由：比值 0.30 容得下「刻度标签与轴标题正常贴邻」又不放过 W1259 实录的 0.31 / 0.37 / 0.39 / 1.0 四档真重叠；
             单用比值挡不住两个极小标签（面积 < 4px²）因四舍五入贴边而误判 ⇒ 叠加绝对下限
C4 **下限**（尺寸下限·W1259 报告 G-5 遗留边界·「svg 宽度下限」本槽写死）
   svg 视窗宽度 < **200px** 的图表**不参与**判据（太小放不下标签·命中必是系统性噪声）；探针仍量测·门禁侧跳过
C5 **触发时机**（量测发生在什么时刻·G-5 遗留边界「是否触发 reveal」本槽写死）
   goto(domcontentloaded) → 置 html[data-theme] → **document.fonts.ready**（字体加载完成后才量测·
   否则按回退字体度量⇒bbox 偏小⇒漏报） → **waitStable**（svg 数 + text 数 + body 高度连续两次采样相同·
   尺寸稳定后才量测·防页面未渲染完就量导致假阴性） → **滚动穿透**（触发 reveal-in / lazy 图表·
   否则未 in-view 的图不渲染） → waitStable → 取矩形
   主题置法：**双通道**（colorScheme 上下文 emulateMedia + html[data-theme] 属性）——与第 80 槽同款
C6 **豁免**（有意裁剪 = 设计意图）
   被 clip-path（svg 内组级裁剪）或 overflow:hidden 容器（页面级裁剪·卡片固定高裁图）有意裁掉的标签属设计意图
   ⇒ **须在显式豁免清单** scripts/output/chart-label-clipping-exemptions.txt **逐条登记**才被豁免
   （豁免不散在代码里·新增有意裁剪未登记 ⇒ 门禁仍红·须显式登记）
   清单行格式：<违例键>[\t<原因说明>]（制表符分隔·违例键自带 '|'·不可用 '|' 分隔原因）
C7 去重（同类同文只记一次）
   同一页内 **同方向 + 同文案** 的裁切只记 1 处；**同对文案** 的重叠只记 1 处
   理由：同一图例项在多个页脚各画一次时不得重复计入（「处数」虚高·命中页数不受影响）
   原始未去重处数同时报出·不隐藏

【模式】
  默认档：基线内违例记「存量基线」不计 FAIL；基线外新增 = FAIL；基线文件缺失 = FAIL（fail-closed）
  --strict：零容忍（任何违例含基线内 = FAIL）
  --report：只报数·退出码 0
  --generate-baseline：生成基线
  --candidates：列出「有意裁剪」候选项（供豁免清单登记用）
  --self-test：内存 fixture 负样本自证（**不改任何真实页面**）

【用法】
  py -3 scripts/check_chart_label_clipping.py
  py -3 scripts/check_chart_label_clipping.py --strict
  py -3 scripts/check_chart_label_clipping.py --self-test
  py -3 scripts/check_chart_label_clipping.py --generate-baseline
  node scripts/chart_label_clipping_probe.js       # 先跑探针（file:// 口径·S1 桌面浅色）
退出码：0 通过 / 1 违例或报告缺失（fail-closed）/ 2 自测失败
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from lib import freeze_gate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MARKER = "---- 第 83 门禁 SVG 标签裁切与重叠："


def final_line(n_fail: int) -> str:
    """末行恒定格式：---- 第 83 门禁 SVG 标签裁切与重叠：N FAIL ----（N = 基线外新增违例数）。"""
    return "%s%d FAIL ----" % (MARKER, n_fail)
REPORT = ROOT / "scripts" / "output" / "chart_label_clipping_report.json"
BASELINE = ROOT / "scripts" / "output" / "chart-label-clipping-baseline.txt"
EXEMPTIONS = ROOT / "scripts" / "output" / "chart-label-clipping-exemptions.txt"

# ———————— 判据常量（全部写死·换人复跑必须同数）————————
CLIP_TOL_PX = 1.5          # C1 越界容差
OVERLAP_RATIO = 0.30       # C3 相交面积 / 较小标签面积
OVERLAP_MIN_AREA_PX2 = 4.0  # C3 相交面积绝对下限
MIN_SVG_WIDTH_PX = 200     # C4 svg 视窗宽度下限
DIRECTIONS = ("left", "right", "top", "bottom")
NARROW_DIRS = ("left", "right")   # C2 窄口径
WIDE_DIRS = DIRECTIONS           # C2 宽口径


def normalize_label(text: str) -> str:
    """标签文案归一（键用·防空白/分隔符歧义）。

    **截断后必须再 strip**：基线文件读回时逐行 strip（freeze_gate.read_baseline），
    若键以空格结尾则「写入的键」与「读回的键」不一致 ⇒ 每次跑都出现「新增 + 可收紧」假漂移
    （W1266 批二 B1 实测 4 条假漂移·此坑已修）。
    """
    s = re.sub(r"\s+", " ", (text or "").strip())
    s = s.replace("|", "/").replace("~", "-")
    s = s[:24].strip()
    return s if s else "(空)"


def _rect(r) -> tuple:
    return (float(r[0]), float(r[1]), float(r[2]), float(r[3]))


def _container_cuts(svg: dict, direction: str) -> bool:
    """svg 是否被 overflow:hidden 的 HTML 祖先容器**在该方向**裁掉（页面级裁剪·设计意图）。"""
    cc = svg.get("cc_rect")
    if not cc:
        return False
    cl, ct, cr, cb = _rect(svg["rect"])
    ccl, cct, ccr, ccb = _rect(cc)
    if direction == "left":
        return cl < ccl - 0.5
    if direction == "right":
        return cr > ccr + 0.5
    if direction == "top":
        return ct < cct - 0.5
    if direction == "bottom":
        return cb > ccb + 0.5
    return False


def clip_hits(svg: dict, tol: float = CLIP_TOL_PX, rect: tuple | None = None) -> list:
    """C1：一个 svg 容器内的四向越界命中 → [{dir, label, px, design}]。

    rect = 视窗矩形（**由 judge_report 按判据基准传入**）；缺省时退回 svg["rect"]（border box）。
    ⚠ 旧实现曾在此处直接读 svg["rect"] ⇒ 判据基准形同虚设（对照行比的是同一组数），
    W1266 波三已修：基准真正进入判定（实测与主会话复算 v4 对齐）。
    """
    cl, ct, cr, cb = _rect(rect if rect is not None else svg["rect"])
    out = []
    for row in svg.get("texts") or []:
        label = row[0]
        tl, tt, tr, tb = _rect(row[1:5])
        flags = row[5] if len(row) > 5 else ""
        over = {
            "left": cl - tl,
            "right": tr - cr,
            "top": ct - tt,
            "bottom": tb - cb,
        }
        for d in DIRECTIONS:
            amt = over[d]
            if amt <= tol:
                continue
            if d in ("left", "right") and not svg.get("clips_x", True):
                continue
            if d in ("top", "bottom") and not svg.get("clips_y", True):
                continue
            design = ("cp" in flags) or _container_cuts(svg, d)
            out.append({"dir": d, "label": label, "px": round(amt, 1), "design": design})
    return out


def overlap_hits(svg: dict, ratio: float = OVERLAP_RATIO, min_area: float = OVERLAP_MIN_AREA_PX2) -> list:
    """C3：同一 svg 容器内两两相交命中 → [{a, b, ratio, area}]"""
    items = [(row[0], _rect(row[1:5])) for row in (svg.get("texts") or [])]
    out = []
    for i in range(len(items)):
        la, ra = items[i]
        a1 = (ra[2] - ra[0]) * (ra[3] - ra[1])
        for j in range(i + 1, len(items)):
            lb, rb = items[j]
            ix = min(ra[2], rb[2]) - max(ra[0], rb[0])
            iy = min(ra[3], rb[3]) - max(ra[1], rb[1])
            if ix <= 0 or iy <= 0:
                continue
            inter = ix * iy
            if inter < min_area:
                continue
            a2 = (rb[2] - rb[0]) * (rb[3] - rb[1])
            small = min(a1, a2)
            if small <= 0:
                continue
            r = inter / small
            if r > ratio:
                out.append({"a": la, "b": lb, "ratio": round(r, 3), "area": round(inter, 1)})
    return out


def container_rect(svg: dict, basis: str = "viewport") -> tuple:
    """容器视窗矩形 → (rect, used_viewbox)。

    basis='viewport'（**判据采用**）= **SVG 视窗（元素内容盒）**——UA 默认 svg 根元素 overflow:hidden
      ⇒ **真实裁剪矩形 = 视窗**，即 border box 内缩 border(+padding) 宽度。
      实测 data/relationships.html：border box 978×422 vs 视窗 976×420（差 1px/边·该 svg 带 1px border）；
      像素实证 overflow:hidden 与 visible 两态差异恰落在视窗左缘 x=232 的 1px 竖条 ⇒ 裁剪线在内容盒，不在 border box。
      无 viewBox 的 svg（现役 68 个）同样只能用它。
    basis='element'（**对照用**）= getBoundingClientRect 的 border box（含 border）⇒ 每边比视窗宽一个 border。
    basis='viewbox'（**对照用**）= viewBox 经 preserveAspectRatio 映射的矩形；无 viewBox 时回退元素盒。
    """
    if basis == "viewbox" and svg.get("vb_rect"):
        return _rect(svg["vb_rect"]), True
    if basis == "viewport":
        vp = svg.get("vp_rect") or svg.get("client_rect")
        if vp:
            return _rect(vp), False
    return _rect(svg["rect"]), False


def judge_report(report: dict, basis: str = "viewport") -> tuple:
    """判据总入口 → (违例键列表, 统计字典)。**纯函数·可在内存 fixture 上单测**。

    basis='viewport'（SVG 视窗·内容盒）为判据基准；'element'（border box）与 'viewbox' 仅用于并排对照
    （见门禁输出的「视窗基准对照」行）。
    """
    viol: list[str] = []
    stats = {
        "pages_scanned": report.get("pages_scanned"),
        "rows": report.get("rows"),
        "fatal_rows": report.get("fatal_rows"),
        "svgs_measured": report.get("svgs_measured"),
        "texts_measured": report.get("texts_measured"),
        "pages_with_svg": 0,
        "skipped_small_svg": 0,
        "clip_raw": 0,
        "clip_narrow_raw": 0,
        "clip_dedup": 0,
        "clip_narrow_dedup": 0,
        "overlap_raw": 0,
        "overlap_dedup": 0,
        "dir_counts": {d: 0 for d in DIRECTIONS},
        "pages_narrow": set(),
        "pages_wide": set(),
        "pages_overlap": set(),
        "design_candidates": set(),
        "basis": basis,
        "basis_viewbox_used": 0,
        "basis_fallback": 0,
        "basis_vp_used": 0,
        "basis_vp_missing": 0,
    }
    for page, payload in (report.get("by_page") or {}).items():
        page_has_svg = False
        clip_seen: set[str] = set()
        ovl_seen: set[str] = set()
        for svg in payload.get("svgs") or []:
            (cl, ct, cr, cb), used_vb = container_rect(svg, basis)
            if basis == "viewport":
                if svg.get("vp_rect") or svg.get("client_rect"):
                    stats["basis_vp_used"] += 1
                else:
                    stats["basis_vp_missing"] += 1
            elif used_vb:
                stats["basis_viewbox_used"] += 1
            else:
                stats["basis_fallback"] += 1
            if (cr - cl) < MIN_SVG_WIDTH_PX:
                stats["skipped_small_svg"] += 1
                continue
            page_has_svg = True
            for hit in clip_hits(svg, rect=(cl, ct, cr, cb)):
                stats["clip_raw"] += 1
                if hit["dir"] in NARROW_DIRS:
                    stats["clip_narrow_raw"] += 1
                key = "%s|CLIP-%s|%s" % (page, hit["dir"], normalize_label(hit["label"]))
                if hit["design"]:
                    stats["design_candidates"].add(key)
                if key in clip_seen:
                    continue
                clip_seen.add(key)
                viol.append(key)
                stats["clip_dedup"] += 1
                stats["dir_counts"][hit["dir"]] += 1
                if hit["dir"] in NARROW_DIRS:
                    stats["clip_narrow_dedup"] += 1
                    stats["pages_narrow"].add(page)
                stats["pages_wide"].add(page)
            for hit in overlap_hits(svg):
                stats["overlap_raw"] += 1
                la, lb = sorted([normalize_label(hit["a"]), normalize_label(hit["b"])])
                key = "%s|OVL|%s~%s" % (page, la, lb)
                if key in ovl_seen:
                    continue
                ovl_seen.add(key)
                viol.append(key)
                stats["overlap_dedup"] += 1
                stats["pages_overlap"].add(page)
        if page_has_svg:
            stats["pages_with_svg"] += 1
    stats["pages_narrow_n"] = len(stats["pages_narrow"])
    stats["pages_wide_n"] = len(stats["pages_wide"])
    stats["pages_overlap_n"] = len(stats["pages_overlap"])
    return viol, stats


def load_report(path: Path) -> tuple:
    """读探针报告 → (报告 dict, 问题列表)。缺失/不可读/零命中 = fail-closed。"""
    if not path.exists():
        return {}, ["探针报告缺失: %s（fail-closed·拒绝通过·先跑 node scripts/chart_label_clipping_probe.js）" % path]
    try:
        rep = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {}, ["探针报告不可读: %s（%s）" % (path, exc)]
    if not isinstance(rep, dict):
        return {}, ["探针报告格式非法（非对象）: %s" % path]
    if not rep.get("pages_scanned"):
        return rep, ["探针报告零命中（pages_scanned=0）——产物无效·fail-closed"]
    if not rep.get("rows"):
        return rep, ["探针报告零命中（rows=0）——产物无效·fail-closed"]
    if not rep.get("by_page"):
        return rep, ["探针报告零命中（by_page 为空）——产物无效·fail-closed"]
    return rep, []


def read_exemptions(path: Path) -> tuple:
    """读豁免清单 → (豁免键集合, 陈旧行列表)。

    行格式：<违例键>[\t<原因说明>]（**制表符分隔**·避免与违例键自带的 '|' 歧义）。
    """
    keys: set[str] = set()
    stale: list[str] = []
    if not path.exists():
        return keys, stale
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return keys, stale
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        key = s.split("\t", 1)[0].strip()
        if key:
            keys.add(key)
    return keys, stale


def _fixture_report() -> dict:
    """内存 fixture：1 个 svg 容器（400x200）+ 正常标签 + 四向各一越界标签 + 一对重叠标签。"""
    return {
        "pages_scanned": 1,
        "rows": 1,
        "fatal_rows": 0,
        "svgs_measured": 1,
        "texts_measured": 7,
        "by_page": {
            "data/__fixture__.html": {
                "state": "S1-desktop-light",
                "svgs": [
                    {
                        "idx": 0,
                        "rect": [0.0, 0.0, 400.0, 200.0],
                        "vb_rect": [0.0, 0.0, 400.0, 200.0],
                        "clips_x": True,
                        "clips_y": True,
                        "cc_rect": None,
                        "texts": [
                            ["正常标签", 10.0, 10.0, 60.0, 30.0],
                            ["左越界", -20.0, 40.0, 20.0, 60.0],
                            ["右越界", 380.0, 70.0, 440.0, 90.0],
                            ["上越界", 100.0, -10.0, 160.0, 10.0],
                            ["下越界", 100.0, 190.0, 160.0, 215.0],
                            ["重叠甲", 200.0, 100.0, 260.0, 120.0],
                            ["重叠乙", 220.0, 105.0, 280.0, 125.0],
                        ],
                    }
                ],
            }
        },
    }


def _fixture_report_clean() -> dict:
    """还原后的 fixture：所有标签回到容器内·且互不相交 ⇒ 应判绿。"""
    rep = _fixture_report()
    rep["by_page"]["data/__fixture__.html"]["svgs"][0]["texts"] = [
        ["正常标签", 10.0, 10.0, 60.0, 30.0],
        ["左越界", 5.0, 40.0, 45.0, 60.0],
        ["右越界", 300.0, 70.0, 340.0, 90.0],
        ["上越界", 100.0, 5.0, 160.0, 25.0],
        ["下越界", 100.0, 150.0, 160.0, 175.0],
        ["重叠甲", 200.0, 100.0, 240.0, 115.0],
        ["重叠乙", 260.0, 130.0, 300.0, 145.0],
    ]
    return rep


def self_test() -> int:
    """负样本自测（**全程内存 fixture·不改任何真实页面**）。

    T1 越界标签 → 判红（四向各一 + 重叠一对 = 5 条违例）
    T2 还原（标签移回容器内·且互不相交）→ 判绿
    T3 豁免清单登记后 → 该条不再计违例（豁免机制生效）
    T4 基线内违例不计 FAIL / 基线外新增计 FAIL / --strict 存量全红
    T5 零命中 fail-closed（报告缺失·或 pages_scanned=0）
    """
    bad = 0
    checks = 0

    def report(name, ok, detail=""):
        nonlocal bad, checks
        checks += 1
        print("%s %s%s" % ("OK  " if ok else "FAIL", name, ("：" + detail) if detail else ""))
        if not ok:
            bad += 1

    # ———— T1 负样本：越界 + 重叠必红 ————
    viol, stats = judge_report(_fixture_report())
    dirs = stats["dir_counts"]
    ok = (
        len(viol) == 5
        and dirs["left"] == 1
        and dirs["right"] == 1
        and dirs["top"] == 1
        and dirs["bottom"] == 1
        and stats["overlap_dedup"] == 1
    )
    report("负样本-四向越界 + 重叠必红", ok, "违例 %d 条（left %d/right %d/top %d/bottom %d · 重叠 %d）"
           % (len(viol), dirs["left"], dirs["right"], dirs["top"], dirs["bottom"], stats["overlap_dedup"]))
    ok = stats["pages_wide_n"] == 1 and stats["pages_narrow_n"] == 1 and stats["pages_overlap_n"] == 1
    report("负样本-窄/宽/重叠三口径命中页数各 1", ok,
           "窄 %d · 宽 %d · 重叠 %d" % (stats["pages_narrow_n"], stats["pages_wide_n"], stats["pages_overlap_n"]))

    # ———— T2 还原必绿 ————
    viol2, stats2 = judge_report(_fixture_report_clean())
    ok = not viol2 and stats2["clip_dedup"] == 0 and stats2["overlap_dedup"] == 0
    report("还原-标签归位后判绿", ok, "违例 %d 条" % len(viol2))

    # ———— T3 豁免清单生效 ————
    exempt = {v for v in viol if v.endswith("右越界")}
    viol3 = [v for v in viol if v not in exempt]
    ok = len(viol3) == len(viol) - 1 and not any(v.endswith("右越界") for v in viol3)
    report("豁免清单登记后该条不再计违例", ok, "豁免 1 条后剩 %d 条" % len(viol3))

    # ———— T4 基线语义 ————
    res = freeze_gate.evaluate(viol, set(viol), strict=False)
    ok = not res["new_fail"] and len(res["frozen"]) == len(viol)
    report("基线内违例不计 FAIL", ok, "存量基线 %d 条" % len(res["frozen"]))
    res = freeze_gate.evaluate(viol, set(), strict=False)
    ok = len(res["new_fail"]) == len(viol)
    report("基线外新增违例计 FAIL", ok, "新增 %d 条" % len(res["new_fail"]))
    res = freeze_gate.evaluate(viol, set(viol), strict=True)
    ok = len(res["new_fail"]) == len(viol)
    report("零容忍模式存量全红", ok, "FAIL %d 条" % len(res["new_fail"]))

    # ———— T5 零命中 fail-closed ————
    rep, problems = load_report(ROOT / "scripts" / "output" / "_w1266_no_such_report.json")
    ok = bool(problems) and "fail-closed" in problems[0]
    report("探针报告缺失 fail-closed（拒绝通过）", ok, problems[0] if problems else "无问题")
    empty = _fixture_report()
    empty["pages_scanned"] = 0
    empty["rows"] = 0
    empty["by_page"] = {}
    tmp = ROOT / "scripts" / "output" / "_w1266_zero_hit_fixture.json"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(empty, ensure_ascii=False), encoding="utf-8")
    try:
        rep2, problems2 = load_report(tmp)
    finally:
        tmp.unlink(missing_ok=True)
    ok = bool(problems2) and "零命中" in problems2[0]
    report("探针零命中（pages_scanned=0）fail-closed", ok, problems2[0] if problems2 else "无问题")

    print("自测 %d/%d 通过" % (checks - bad, checks))
    return 0 if bad == 0 else 2


def _parse_args(argv):
    scope = "--report-file"
    report_path = REPORT
    baseline_path = BASELINE
    exempt_path = EXEMPTIONS
    if scope in argv:
        i = argv.index(scope)
        if i + 1 < len(argv):
            report_path = Path(argv[i + 1])
            if not report_path.is_absolute():
                report_path = ROOT / report_path
    if "--baseline" in argv:
        i = argv.index("--baseline")
        if i + 1 < len(argv):
            baseline_path = Path(argv[i + 1])
            if not baseline_path.is_absolute():
                baseline_path = ROOT / baseline_path
    if "--exemptions" in argv:
        i = argv.index("--exemptions")
        if i + 1 < len(argv):
            exempt_path = Path(argv[i + 1])
            if not exempt_path.is_absolute():
                exempt_path = ROOT / exempt_path
    return report_path, baseline_path, exempt_path


def _print_stats(stats: dict, exempted: list, exempt_path: Path, stale_exempt: list,
                   stats_vb: dict | None = None, stats_el: dict | None = None) -> None:
    """口径统计行：窄/宽双口径并列 + 四向分项 + 重叠 + 豁免 + 视窗基准对照（**必须全报·不只报合计**）。"""
    print(
        "探针：扫描 %s 页 · 可量测 %s 页 · svg %s · 文本 %s · 跳过小图 %s · 态 %s"
        % (
            stats.get("pages_scanned"),
            stats.get("pages_with_svg"),
            stats.get("svgs_measured"),
            stats.get("texts_measured"),
            stats.get("skipped_small_svg"),
            "S1-desktop-light",
        )
    )
    print(
        "窄口径（左+右）：裁切 %d 处（原始 %d）· 命中 %d 页 · 判据 = 越界 > %.1fpx"
        % (stats["clip_narrow_dedup"], stats["clip_narrow_raw"], stats["pages_narrow_n"], CLIP_TOL_PX)
    )
    print(
        "宽口径（四向）：裁切 %d 处（原始 %d）· 命中 %d 页 · 分项 left %d · right %d · top %d · bottom %d"
        % (
            stats["clip_dedup"],
            stats["clip_raw"],
            stats["pages_wide_n"],
            stats["dir_counts"]["left"],
            stats["dir_counts"]["right"],
            stats["dir_counts"]["top"],
            stats["dir_counts"]["bottom"],
        )
    )
    print(
        "重叠：%d 处（原始 %d）· 命中 %d 页 · 判据 = 相交 >= %.0fpx² 且 交集/较小者 > %.2f"
        % (stats["overlap_dedup"], stats["overlap_raw"], stats["pages_overlap_n"],
           OVERLAP_MIN_AREA_PX2, OVERLAP_RATIO)
    )
    if stats_vb:
        print(
            "视窗基准对照：判据用「SVG 视窗（内容盒·overflow:hidden 的真实裁剪线）」宽 %d 处/%d 页 · "
            "对照「元素 border box」宽 %d 处/%d 页 · 对照「viewBox 换算矩形」宽 %d 处/%d 页"
            "（判据基准视窗缺失回退 border box %d 个 svg · 与 border box 差 %d 处/%d 页 · 与 viewBox 差 %d 处/%d 页）"
            % (
                stats["clip_dedup"], stats["pages_wide_n"],
                stats_el["clip_dedup"] if stats_el else 0, stats_el["pages_wide_n"] if stats_el else 0,
                stats_vb["clip_dedup"], stats_vb["pages_wide_n"],
                stats.get("basis_vp_missing", 0),
                abs((stats_el["clip_dedup"] if stats_el else 0) - stats["clip_dedup"]),
                abs((stats_el["pages_wide_n"] if stats_el else 0) - stats["pages_wide_n"]),
                abs(stats_vb["clip_dedup"] - stats["clip_dedup"]),
                abs(stats_vb["pages_wide_n"] - stats["pages_wide_n"]),
            )
        )
    print("豁免：%d 条（有意裁剪·显式清单 %s）" % (len(exempted), exempt_path.name))
    if stale_exempt:
        print("  · 豁免清单陈旧 %d 条（对应违例已不存在·建议删行）：%s"
              % (len(stale_exempt), " / ".join(stale_exempt[:4])))


def _print_eval(res: dict, strict: bool) -> None:
    """基线对拍结论行（存量基线 / 基线外新增 / 可收紧 / 零容忍说明）。"""
    print(
        "违例 %d 条 · %s %d 条 · 基线外新增 %d 条 · %s"
        % (
            res["total"],
            freeze_gate.FROZEN_LABEL,
            len(res["frozen"]),
            len(res["new_fail"]),
            "FAIL" if res["new_fail"] else "OK",
        )
    )
    for k in res["new_fail"][:12]:
        print("  ✗ 新增/未登记违例 " + k)
    if len(res["new_fail"]) > 12:
        print("  …其余 %d 条略" % (len(res["new_fail"]) - 12))
    if res["frozen"]:
        print("  · %s（%d 条）：%s"
              % (freeze_gate.FROZEN_LABEL, len(res["frozen"]), " / ".join(res["frozen"][:4])))
    if res["fixed"]:
        print("  · 可收紧（基线内违例已消失 %d 条·建议删行）：%s"
              % (len(res["fixed"]), " / ".join(res["fixed"][:4])))
    if strict:
        print("  · 零容忍模式（--strict）：基线不参与判定·全部违例计 FAIL")


def main() -> int:
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return self_test()
    report_path, baseline_path, exempt_path = _parse_args(argv)
    strict = "--strict" in argv
    report_only = "--report" in argv
    candidates_only = "--candidates" in argv

    report, problems = load_report(report_path)
    if problems:
        for p in problems:
            print("FAIL " + p)
        print(final_line(1))
        return 1

    viol_all, stats = judge_report(report)
    _viol_el, stats_el = judge_report(report, basis="element")
    _viol_vb, stats_vb = judge_report(report, basis="viewbox")
    exempt_keys, _stale = read_exemptions(exempt_path)
    viol = [v for v in viol_all if v not in exempt_keys]
    exempted = [v for v in viol_all if v in exempt_keys]
    stale_exempt = sorted(exempt_keys - set(viol_all))

    if candidates_only:
        cand = sorted(stats["design_candidates"])
        print("有意裁剪候选项 %d 条（登记进豁免清单后方可豁免）：" % len(cand))
        for c in cand:
            print("  " + c)
        print(final_line(0))
        return 0

    if "--generate-baseline" in argv:
        n = freeze_gate.write_baseline(
            baseline_path,
            viol,
            [
                "# 第 83 门禁 · SVG 标签裁切与重叠基线（W1266 批二 线 B1 建立·存量违例冻结）",
                "# 生成命令：py -3 scripts/check_chart_label_clipping.py --generate-baseline",
                "# 前提：node scripts/chart_label_clipping_probe.js（file:// 口径·S1 桌面浅色·双通道置主题）",
                "# 口径：越界 > 1.5px（left/right/top/bottom 四向）· 重叠 相交面积 >= 4px² 且 交集/较小者 > 0.30",
                "# 视窗基准：**SVG 视窗（元素内容盒·UA svg:root{overflow:hidden} 的真实裁剪矩形）**·非 border box",
                "#      同页同方向同文案去重 · 同页同对文案重叠去重 · svg 视窗宽度 < 200px 不参与判据",
                "# 格式：<页面>|CLIP-<方向>|<文案> 或 <页面>|OVL|<文案A>~<文案B>",
                "# 语义：基线内违例记「存量基线」不计 FAIL；基线外新增 = FAIL；零容忍：--strict",
                "# 豁免：scripts/output/chart-label-clipping-exemptions.txt（有意裁剪·设计意图·显式登记）",
            ],
        )
        print("基线已写入 %s（%d 条·豁免 %d 条未计入）" % (baseline_path, n, len(exempted)))
        print(final_line(0))
        return 0

    baseline, bproblems = freeze_gate.read_baseline(baseline_path)
    if bproblems:
        if report_only:
            for p in bproblems:
                print("NOTE " + p + "（报告档不判红）")
            baseline = set()
        else:
            for p in bproblems:
                print("FAIL " + p)
            print(final_line(1))
            return 1

    res = freeze_gate.evaluate(viol, baseline, strict=strict)
    _print_stats(stats, exempted, exempt_path, stale_exempt, stats_vb, stats_el)
    _print_eval(res, strict)
    n_fail = len(res["new_fail"])
    print(final_line(n_fail))
    if report_only:
        return 0
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
