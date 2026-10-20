#!/usr/bin/env python3
"""check_perf_shadow.py — 性能影子槽判据件（W849 建立·verify_delivery 第 47 门禁）。

## 这道槽补的是什么洞（W828 备料件 §五 的落地）

perf.yml 用 Lighthouse CI 在 CI 侧断言 LCP/CLS/TBT（desktop 预设 · 5 URL · 3 runs），
是全仓唯一的性能防线。但它在 pre-commit 路径上**不可执行**：lhci 要 Chrome + @lhci/cli，
5 URL × 3 runs 是分钟级，且 CI 的结果从未回流成仓内基线——于是「这次提交有没有让页面
变慢」在每次提交时都是一个没有数据可回答的问题。

本槽把这条盲区收成**影子槽**：不跑浏览器、不设阈值、不判红，只按批采静态成本代理并
累积基线。满 10 批后由用户单独裁决阈值（3D 页单独分档）——这是 W828 §五 约定的顺序，
本批只负责「把槽挂上、把样本攒起来」，阈值一行都不碰。

## 为什么采静态代理而不是跑 LHCI（三条例由）

1. **路径成本**：pre-commit 每次提交都跑，分钟级 + 依赖 Chrome 的门禁会被绕过或拖垮流程；
2. **可比性**：影子期要的是「同一口径的连续样本」，静态量可确定性复算、跨机器同值，
   而 CI 的 LCP 受 runner 冷启与网络抖动影响，单点不可比；
3. **不另立口径**：真 LCP/CLS/TBT 仍以 CI 为权威——`--ingest` 把 `.lighthouseci/
   assertion-results.json` 并进**同一份基线**的样本槽（`lhci` 字段），两侧共用一条时间线。

## 采什么（每页六项 · 全部零依赖可算）

| 项 | 含义 | 与 CWV 的同向关系 |
|:--|:---|:---|
| `html_bytes` | 页面文件字节（含内联 CSS/JS） | 传输量 → LCP 的下载段 |
| `head_bytes` | `<head>` 区字节 | 首屏关键路径长度 |
| `inline_script_bytes` | 无 src 的 `<script>` 内容字节和 | 主线程解析/执行 → TBT |
| `local_dep_bytes` | 本地外链依赖（script src / link stylesheet）实测字节和 | 额外往返与阻塞 → LCP |
| `remote_refs` | 外域引用条数（CDN） | 不可控 RTT → LCP 方差 |
| `blocking_head_refs` | head 内同步脚本（无 defer/async/module）+ 非 print 的样式表 | 渲染阻塞 → FCP/LCP |

## 判据（只有一条会红）

C1 **采集面完整**：perf.yml `collect.url` 的 5 个页面必须在 `site/` 下真实存在——
缺页即 FAIL（CI 那边会 404，属真断链，不是阈值判断）。其余数字**只记录、不判红**。

## 用法

    python scripts/check_perf_shadow.py --gate      # 门禁槽调用：测量 + 与上一批对比（只读）
    python scripts/check_perf_shadow.py --record    # 把本批测量写入基线（收官时跑一次）
    python scripts/check_perf_shadow.py --ingest <assertion-results.json>   # 并入 CI 真数
    python scripts/check_perf_shadow.py --self-test # 判据自测（5 例）

退出码：OK 0 · C1 采集面缺失或测量异常 1。
"""

import json
import os
import re
import sys
import tempfile
from datetime import datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, ".."))
SITE = os.path.join(ROOT, "site")
BASELINE = os.path.join(ROOT, "scripts", "output", "perf_shadow.json")
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")

MARKER = "---- 第 47 门禁 性能影子："
SHADOW_BATCH_TARGET = 10  # 满 10 批后另行裁决阈值（W828 §五）

# perf.yml collect.url 的 5 页（相对 site/）·档位沿用该 workflow 的分档：3D 重页单独一档
PERF_PAGES = (
    ("dashboard.html", "std"),
    ("index.html", "std"),
    ("data/timeline.html", "std"),
    ("data/character-relationship-3d.html", "3d"),
    ("data/text-search.html", "std"),
)

_TAG_RE = re.compile(r"<(script|link)\b([^>]*)>", re.I)
_ATTR_RE = re.compile(r"([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s\"'>]+))")
_BARE_RE = re.compile(r"(?:^|\s)([A-Za-z_:][-A-Za-z0-9_:.]*)(?=\s|=|$)")
_HEAD_RE = re.compile(r"<head\b[^>]*>(.*?)</head>", re.I | re.S)


def _attrs(raw):
    """标签属性串 → 小写键字典；**布尔属性（defer/async 等无值形态）也收**（值记空串）。

    W849 实测教训：只认 key=value 会静默丢掉 `defer`/`async`——渲染阻塞计数虚高
    （首个版本把 index.html 三个 defer 脚本全算成阻塞），而这类误报会让影子基线
    从第一笔就不可信。
    """
    out = {}
    for m in _ATTR_RE.finditer(raw):
        key = m.group(1).lower()
        val = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else (m.group(4) or ""))
        out.setdefault(key, val)
    for m in _BARE_RE.finditer(raw):
        out.setdefault(m.group(1).lower(), "")
    out.pop("", None)
    return out


def _is_remote(ref):
    return ref.startswith(("http://", "https://", "//", "data:"))


def measure_page(site_dir, rel_url, tier):
    """测一页的六项静态成本。页缺失返回 exists=False（C1 判据消费）。"""
    path = os.path.join(site_dir, rel_url)
    rec = {"url": rel_url, "tier": tier, "exists": os.path.isfile(path)}
    if not rec["exists"]:
        return rec
    raw = open(path, encoding="utf-8", errors="replace").read()
    data = raw.encode("utf-8", errors="replace")
    rec["html_bytes"] = len(data)

    head_m = _HEAD_RE.search(raw)
    head_span = (head_m.start(), head_m.end()) if head_m else (0, 0)
    rec["head_bytes"] = len(data[head_span[0]:head_span[1]]) if head_m else 0

    inline_js = 0
    local_dep = 0
    local_cnt = 0
    remote = 0
    blocking = 0
    base_dir = os.path.dirname(path)
    for m in _TAG_RE.finditer(raw):
        tag, attr_raw = m.group(1).lower(), m.group(2)
        a = _attrs(attr_raw)
        in_head = head_span[0] <= m.start() < head_span[1]
        if tag == "script":
            if "src" not in a:
                close = raw.find("</script>", m.end())
                body = raw[m.end():close] if close != -1 else ""
                inline_js += len(body.encode("utf-8", errors="replace"))
                continue
            ref = a["src"].strip()
            non_blocking = any(k in a for k in ("defer", "async")) or a.get("type", "").lower() == "module"
            if in_head and not non_blocking:
                blocking += 1
        else:  # link
            rel = a.get("rel", "").lower()
            if "stylesheet" not in rel:
                continue
            ref = a.get("href", "").strip()
            if in_head and a.get("media", "").lower() not in ("print",):
                blocking += 1
        if not ref:
            continue
        if _is_remote(ref):
            remote += 1
            continue
        local_path = os.path.normpath(os.path.join(base_dir, ref.split("?")[0].split("#")[0]))
        if os.path.isfile(local_path):
            local_dep += os.path.getsize(local_path)
            local_cnt += 1

    rec.update({
        "inline_script_bytes": inline_js,
        "local_dep_bytes": local_dep,
        "local_dep_count": local_cnt,
        "remote_refs": remote,
        "blocking_head_refs": blocking,
    })
    return rec


def measure_all(site_dir=SITE):
    return [measure_page(site_dir, rel, tier) for rel, tier in PERF_PAGES]


def _load_baseline(path=BASELINE):
    if not os.path.isfile(path):
        return {"schema": 1, "samples": []}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("schema", 1)
    data.setdefault("samples", [])
    return data


def _current_batch():
    """现役批次号：取 CHANGELOG 顶段（级联落段后即本批）。"""
    if not os.path.isfile(CHANGELOG):
        return None
    m = re.search(r"^### W(\d+)（", open(CHANGELOG, encoding="utf-8").read(), re.M)
    return "W%s" % m.group(1) if m else None


def _sample_for(pages, batch):
    return {
        "batch": batch,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "captured_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "pages": pages,
        "lhci": None,
    }


def record(pages, batch, path=BASELINE):
    """按批写入/更新样本（同批重跑即覆盖，不重复追加）。返回 (样本数, 是否新增)。"""
    data = _load_baseline(path)
    samples = [s for s in data["samples"] if s.get("batch") != batch]
    added = len(samples) == len(data["samples"])
    old = [s for s in data["samples"] if s.get("batch") == batch]
    sample = _sample_for(pages, batch)
    if old and old[0].get("lhci"):  # 已 ingest 过的真数不因重测丢失
        sample["lhci"] = old[0]["lhci"]
    samples.append(sample)
    samples.sort(key=lambda s: int(str(s.get("batch", "W0"))[1:] or 0))
    data["samples"] = samples
    data["note"] = ("性能影子槽基线（W849 建）：只采静态成本代理，不判红、不设阈值；"
                    "真 LCP/CLS/TBT 由 perf.yml 在 CI 采，可经 --ingest 并入同一批样本。")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return len(samples), added


def ingest(path, batch, baseline=BASELINE):
    """把 CI 侧 `.lighthouseci/assertion-results.json` 的真数并入指定批样本。

    LHCI 该文件是扁平行数组：{auditId, actual, url, passed...}。此处只认三条指标，
    其余（passed/expected）不入库——阈值裁决权在用户，不在本脚本。
    """
    want = {"largest-contentful-paint": "lcp_ms",
            "cumulative-layout-shift": "cls",
            "total-blocking-time": "tbt_ms"}
    rows = json.load(open(path, encoding="utf-8"))
    got = {}
    for row in rows if isinstance(rows, list) else []:
        audit = row.get("auditId") or row.get("audit_id")
        if audit not in want:
            continue
        url = str(row.get("url", "")).split("?")[0].rstrip("/")
        page = url.rsplit("/", 1)[-1] or "index.html"
        got.setdefault(page, {})[want[audit]] = row.get("actual")
    if not got:
        raise SystemExit("ingest：未从 %s 解析出 LCP/CLS/TBT（形态不识别·fail-closed）" % path)
    data = _load_baseline(baseline)
    hit = [s for s in data["samples"] if s.get("batch") == batch]
    if not hit:
        raise SystemExit("ingest：基线无 %s 样本（先跑 --record 建样本）" % batch)
    hit[0]["lhci"] = got
    with open(baseline, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return got


def _fmt_delta(cur, prev, key):
    if not prev or prev.get(key) in (None, 0) or cur.get(key) is None:
        return ""
    ratio = (cur[key] - prev[key]) / float(prev[key]) * 100.0
    return " %+.1f%%" % ratio


def report(pages, baseline_path=BASELINE):
    """打印明细 + 汇总行；返回 (exit_code, summary)。C1 缺页 = 1。"""
    missing = [p["url"] for p in pages if not p.get("exists")]
    data = _load_baseline(baseline_path)
    samples = data["samples"]
    prev_pages = {}
    if samples:
        for p in samples[-1].get("pages", []):
            prev_pages[p["url"]] = p

    print("%-38s %-4s %9s %9s %9s %6s %6s %6s" %
          ("页面", "档", "HTML", "内联JS", "外链依赖", "阻塞头", "外域", "依赖数"))
    for p in pages:
        if not p.get("exists"):
            print("%-38s %-4s   —— 缺页（perf.yml 会 404）" % (p["url"], p["tier"]))
            continue
        print("%-38s %-4s %9d %9d %9d %6d %6d %6d" % (
            p["url"], p["tier"], p["html_bytes"], p["inline_script_bytes"],
            p["local_dep_bytes"], p["blocking_head_refs"], p["remote_refs"],
            p["local_dep_count"]))
        prev = prev_pages.get(p["url"])
        if prev and prev.get("batch") != _current_batch():
            d = _fmt_delta(p, prev, "html_bytes")
            if d:
                print("%-38s %-4s   HTML 相对上一批%s" % ("", "", d))

    batch = _current_batch()
    recorded = any(s.get("batch") == batch for s in samples) if batch else False
    summary = ("%s%d 页采样 · 基线 %d 批 · 影子模式不判红（阈值待 %d 批后裁决）%s----" % (
        MARKER, len(pages), len(samples), SHADOW_BATCH_TARGET,
        "" if recorded else " · 本批样本未入库（收官跑 --record）"))
    if missing:
        print(summary)
        print("C1 采集面缺失：%s（perf.yml collect.url 指向的页面必须存在）" % "、".join(missing))
        return 1, summary
    if len(samples) < SHADOW_BATCH_TARGET:
        print("影子进度：%d/%d 批（满额后另批裁决阈值·3D 页单独分档）" % (len(samples), SHADOW_BATCH_TARGET))
    else:
        print("影子进度：%d 批已满 %d 批目标——可申请阈值裁决（3D 页单独分档）"
              % (len(samples), SHADOW_BATCH_TARGET))
    print(summary)
    return 0, summary


def _self_test():
    """5 例：解析口径 / 缺页判红 / 记录去重 / ingest 落位 / 汇总行存在。"""
    cases = []
    tmp = tempfile.mkdtemp(prefix="perfshadow_")
    page = """<html><head>
<link rel="stylesheet" href="../css/a.css">
<link rel="stylesheet" href="../css/print.css" media="print">
<script src="../js/sync.js"></script>
<script src="../js/later.js" defer></script>
<script src="https://cdn.example.com/lib.js"></script>
<script>var a = 1;</script>
</head><body><link rel="stylesheet" href="body.css"></body></html>"""
    os.makedirs(os.path.join(tmp, "css"), exist_ok=True)
    os.makedirs(os.path.join(tmp, "js"), exist_ok=True)
    os.makedirs(os.path.join(tmp, "data"), exist_ok=True)
    open(os.path.join(tmp, "css", "a.css"), "w").write("x" * 100)
    open(os.path.join(tmp, "js", "sync.js"), "w").write("y" * 20)
    open(os.path.join(tmp, "data", "p.html"), "w", encoding="utf-8").write(page)

    rec = measure_page(tmp, "data/p.html", "std")
    cases.append(("T1 解析：head 内阻塞=3（样式表 1 + 同步脚本 2·defer 与 media=print 不计）",
                  rec["blocking_head_refs"] == 3))
    cases.append(("T2 解析：外域 1 条 · 本地依赖 2 个/120 字节 · 内联 12 字节",
                  rec["remote_refs"] == 1 and rec["local_dep_count"] == 2
                  and rec["local_dep_bytes"] == 120
                  and rec["inline_script_bytes"] == len("var a = 1;")))

    missing = measure_page(tmp, "data/nope.html", "std")
    cases.append(("T3 缺页：exists=False（C1 判据输入）", missing["exists"] is False))

    base = os.path.join(tmp, "perf_shadow.json")
    pages = [rec]
    record(pages, "W849", base)
    record(pages, "W849", base)
    n, added = record(pages, "W850", base)
    cases.append(("T4 记录：同批重跑覆盖（不重复追加）·跨批累积",
                  n == 2 and added is True
                  and [s["batch"] for s in _load_baseline(base)["samples"]] == ["W849", "W850"]))

    lhci = os.path.join(tmp, "assertion-results.json")
    json.dump([
        {"auditId": "largest-contentful-paint", "actual": 1979.6,
         "url": "http://localhost:8000/data/p.html"},
        {"auditId": "cumulative-layout-shift", "actual": 0.02,
         "url": "http://localhost:8000/data/p.html"},
        {"auditId": "total-blocking-time", "actual": 41.0,
         "url": "http://localhost:8000/data/p.html"},
        {"auditId": "first-contentful-paint", "actual": 1200.0,
         "url": "http://localhost:8000/data/p.html"},
    ], open(lhci, "w"))
    got = ingest(lhci, "W849", base)
    cases.append(("T5 ingest：三条指标落位·未登记指标忽略",
                  got == {"p.html": {"lcp_ms": 1979.6, "cls": 0.02, "tbt_ms": 41.0}}))

    code, summary = report(pages, base)
    cases.append(("T6 汇总行含门禁标记与「不判红」口径",
                  code == 0 and summary.startswith(MARKER) and "不判红" in summary))

    ok = 0
    for name, passed in cases:
        print("%s %s" % ("PASS" if passed else "FAIL", name))
        ok += 1 if passed else 0
    print("---- 性能影子槽自测：%d/%d ----" % (ok, len(cases)))
    return 0 if ok == len(cases) else 1


def main(argv):
    args = argv[1:]
    if "--self-test" in args:
        return _self_test()
    batch = None
    if "--batch" in args:
        i = args.index("--batch")
        batch = args[i + 1] if i + 1 < len(args) else None
    batch = batch or _current_batch()
    pages = measure_all()
    if "--record" in args:
        if not batch:
            raise SystemExit("--record 需要批次号（CHANGELOG 顶段解析失败）")
        n, added = record(pages, batch)
        print("%s 已写入 %s（%d 批样本·%s）" % (
            batch, os.path.relpath(BASELINE, ROOT), n, "新增" if added else "更新"))
        return 0
    if "--ingest" in args:
        i = args.index("--ingest")
        if i + 1 >= len(args):
            raise SystemExit("--ingest 需要 assertion-results.json 路径")
        got = ingest(args[i + 1], batch)
        print("%s 已并入 CI 真数：%s" % (batch, json.dumps(got, ensure_ascii=False)))
        return 0
    code, _ = report(pages)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
