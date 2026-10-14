#!/usr/bin/env python3
"""聚合数字统计器 stats（W703 建·W704 实体化）——从磁盘实算生成 scripts/output/stats.json（tracked）。

第 31 门禁 C5（check_doc_sync.py 聚合数字对账）的基准真值：治理文档现役叙述面中的
高危聚合句式与 <!--stats:KEY--> 实体标记一律与本文件产物对账，不一致 = FAIL。
第 31 门禁 C5d（W718 挂载）：本脚本 --check（stats.json vs 磁盘实算）由 doc-sync 每批
verify 恒跑背书——「检查过零差异」有机器记录，「漂移未刷新」当场红（W715 漏 --w 实例的防线）。

实体化形态（W704·用户方案「数字制度化」）：每个键 = {value, domain, generator,
introduced_by, last_changed_by}——数字有身份（可正查来源、可反查 W 号）。
变更史落 scripts/output/stats-changelog.json（重跑时 diff 旧值自动追加·--w 记批次），
stats-index.md（W→stats key 反向索引·与 file-index 同构）随史重渲染。

变更史 schema（stats-changelog-v1·W718）：{"_schema", "_field_notes", "entries": [
  {w, date, time, changes: [{key, from, to}], note?}]}——时序流水账（append-only·
只记值变更；零差异检查不入史，由 C5d 门禁与 CHANGELOG 验证栏背书）；按 W 反查用
stats-index.md 反向段（本文件渲染产物）。首条 W704（changes=[]）系建账批开发迭代
产物（终版条件式 append 不可产生·首入库时已在），保留作建账时点标记（note 注明）。

用法：python scripts/stats.py [--w W704]   # 生成/刷新 stats.json + 变更史 + 反向索引
      python scripts/stats.py --check      # 与磁盘现存 stats.json 对比（应零差异·自证）
"""

import argparse
import datetime
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "output", "stats.json")
HIST = os.path.join(HERE, "output", "stats-changelog.json")
INDEX = os.path.join(HERE, "output", "stats-index.md")

CONTENT_DIRS = ["01-全书逐回解读", "02-人物深度分析", "03-主题与情节专题", "04-文化与历史背景", "05-诗词歌赋", "06-个人随笔"]
INLINED_MARK = "(tokens.css + system.css)"  # inline_css.py 注入的标记行特征
HIST_SCHEMA = "stats-changelog-v1"  # W718：变更史结构版本（旧 list 形态 load 时自动迁移）

HIST_FIELD_NOTES = {  # v1 自描述（W718 挑刺第十六次 P1-3/P2：防手工维护漂移+声明查找分工）
    "shape": "时序流水账（append-only·只记值变更）·按 W 反查用 stats-index.md 反向段（本文件渲染产物）",
    "w": "产生变更的批次号（建账前/未记批为 null）",
    "date": "YYYY-MM-DD",
    "time": "HH:MM:SS（W718 起·迁移旧条目为 null）",
    "changes": "值变更 [{key, from, to}]（from/to 为 int·建账前旧值 null）",
    "note": "可选·人工考古注（如首条 W704 建账时点标记）",
    "checks": "零差异检查不入本文件——第 31 门禁 C5d（stats --check 对账·W718 挂载）每批 verify 恒跑背书，检查记录权威载体=verify 输出与 CHANGELOG 验证栏",
}


def migrate_hist(raw):
    """变更史形态归一：旧 list → v1 dict（_schema+_field_notes+entries）；v1 原样返回。
    迁移时补 time=None 与 W704 建账条目来源 note（W718 考古：终版条件式 append 不可产生该
    空条目，系建账批开发迭代产物·首入库时已在——保留作建账时点标记，不删史）。"""
    if isinstance(raw, dict) and raw.get("_schema") == HIST_SCHEMA:
        return raw, False
    entries = [dict(e) for e in raw] if isinstance(raw, list) else []
    for e in entries:
        e.setdefault("time", None)
        if e.get("w") == "W704" and e.get("changes") == []:
            e["note"] = "建账批空变更时点标记（W704 批开发迭代产物·终版条件式 append 不可产生·W718 考古注）"
    return {"_schema": HIST_SCHEMA, "_field_notes": HIST_FIELD_NOTES, "entries": entries}, True

# 实体元数据（W704 登记制：新键必须在此登记 domain 与口径起点；introduced_by=口径首次定义批次，
# 即「该数字成为正式对账口径」的批次——非历史首次出现批次·语义见 stats-index 表头注·W716 补明）
META = {
    "html_total": {"domain": "site/**/*.html（递归全站）", "introduced_by": "W459"},
    "site_data_html": {"domain": "site/data/*.html", "introduced_by": "W459"},
    "site_en_html": {"domain": "site/en/*.html", "introduced_by": "W528"},
    "site_root_html": {"domain": "site/*.html", "introduced_by": "W459"},
    "site_reader_html": {"domain": "site/reader/**/*.html", "introduced_by": "W593"},
    "visualization_pages": {"domain": "site/data_html − _shell.html", "introduced_by": "W459"},
    "csp_covered": {"domain": "html_total − _template.html（generate_csp TEMPLATE_EXCLUDE）", "introduced_by": "W459"},
    "scan_files": {"domain": "html_total − _template.html − _shell.html（check_js_syntax/check_structure）", "introduced_by": "W459"},
    "seo_scanned": {"domain": "html_total − 两模板壳（check_seo_head SEO_EXCLUDE）", "introduced_by": "W591"},
    "inline_css_pages": {"domain": "site 全树含 INLINED 标记页", "introduced_by": "W459"},
    "gate_count": {"domain": "scripts/verify_delivery.py「第 N 槽/门禁」max", "introduced_by": "W493"},
    "a1_a6_docs": {"domain": "docs/01-06 六板块顶层内容 .md（排除 README）", "introduced_by": "W505"},
    "a4_docs": {"domain": "docs/03-主题与情节专题/*.md（排除 README）", "introduced_by": "W722"},  # W722：A4 计数实体化（三处同改·用户裁决 6A）
    "methodology_docs": {"domain": "docs/10-方法论沉淀/*.md（含索引 README）", "introduced_by": "W070"},
    "script_classes": {"domain": "scripts/[A-Z]_* 类目录数", "introduced_by": "W528"},
    "report_docs": {"domain": "docs/11-报告复盘/*.md（含索引 README）", "introduced_by": "W737"},
}


def build():
    """磁盘实算：返回 {key: value} 平面值（实体包装在 main 做）。"""
    site = os.path.join(ROOT, "site")
    htmls = glob.glob(os.path.join(site, "**", "*.html"), recursive=True)
    data_htmls = glob.glob(os.path.join(site, "data", "*.html"))
    template_n = sum(1 for p in htmls if os.path.basename(p) == "_template.html")
    shell_n = sum(1 for p in htmls if os.path.basename(p) == "_shell.html")

    inlined = 0
    for p in htmls:
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                if INLINED_MARK in f.read():
                    inlined += 1
        except OSError:
            continue

    with open(os.path.join(HERE, "verify_delivery.py"), encoding="utf-8") as f:
        gate_max = max(int(x) for x in re.findall(r"第\s*(\d+)\s*(?:槽|门禁)", f.read()))

    a1_a6 = sum(
        len([p for p in glob.glob(os.path.join(ROOT, "docs", d, "*.md")) if not os.path.basename(p).startswith("README")])
        for d in CONTENT_DIRS
    )  # 口径对齐 verify 第 3 门禁：板块顶层内容 .md（排除各板块 README.md·615=621-6）
    a4 = len([p for p in glob.glob(os.path.join(ROOT, "docs", "03-主题与情节专题", "*.md")) if not os.path.basename(p).startswith("README")])
    methodology = len(glob.glob(os.path.join(ROOT, "docs", "10-方法论沉淀", "*.md")))
    classes = [d for d in os.listdir(HERE) if os.path.isdir(os.path.join(HERE, d)) and d[:1].isalpha() and d[:1].isupper()]

    return {
        "html_total": len(htmls),
        "site_data_html": len(data_htmls),
        "site_en_html": len(glob.glob(os.path.join(site, "en", "*.html"))),
        "site_root_html": len(glob.glob(os.path.join(site, "*.html"))),
        "site_reader_html": len(glob.glob(os.path.join(site, "reader", "**", "*.html"), recursive=True)),
        "visualization_pages": len(data_htmls) - shell_n,
        "csp_covered": len(htmls) - template_n,
        # W716：两键当前同算式系近似实算——分母以各器实际排除集为准（三器现同分母=全站减两模板壳），
        # 某器排除面将来变化时须同批改本算式（scan_files/seo_scanned 为两门禁独立分母·刻意不合并）
        "scan_files": len(htmls) - template_n - shell_n,
        "seo_scanned": len(htmls) - template_n - shell_n,
        "inline_css_pages": inlined,
        "gate_count": gate_max,
        "a1_a6_docs": a1_a6,
        "a4_docs": a4,
        "methodology_docs": methodology,
        # json_count 键已移除（W716）：scripts/output/data/ 系 gitignored 本地产物（.gitignore:59），
        # 依赖它的键在无本地产物环境 --check 必红，违反「tracked 基准 CI 可复现」原则（W703 声明对它不成立）
        "script_classes": len(classes),
    "report_docs": len(glob.glob(os.path.join(ROOT, "docs", "11-报告复盘", "*.md"))),
    }


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def render_index(hist, entities):
    """stats-index.md：正向（key 卡）+ 反向（W→变更·倒序）·与 file-index 同构。"""
    lines = [
        "# stats 反向索引（W704 建·与 file-index 同构的第二实体索引）",
        "",
        "> 由 `python scripts/stats.py` 自动生成·禁手改；变更史=scripts/output/stats-changelog.json。",
        "> 正向：给定 stats key 查口径与来路；反向：给定 W 号查它变更了哪些数字。",
        "",
        "## 正向：stats key 实体卡",
        "",
        "| key | value | domain | introduced_by | last_changed_by |",
        "|---|---|---|---|---|",
        # W716 表头注：三字段语义（introduced_by/last_changed_by 为批次视角·generator 恒同值故省略列）
        "> **字段语义（W716 注）**：`introduced_by`=口径首次**正式化**批次（非历史首次出现批次）；`last_changed_by`=stats.py **检出**值变更的最近批次（建账前变更不记，如 site/reader 621→622 系主题枢纽页批次新增、早于建账）；`generator` 恒为 `scripts/stats.py` 故省略列。",
        "",
    ]
    for k in sorted(entities):
        e = entities[k]
        lines.append("| %s | %s | %s | %s | %s |" % (k, e["value"], e["domain"], e["introduced_by"], e["last_changed_by"]))
    lines += ["", "## 反向：W → stats key 变更（新→旧）", ""]
    for entry in reversed(hist["entries"]):
        w = entry.get("w") or "（未记 W）"
        stamp = entry.get("date", "")
        if entry.get("time"):
            stamp += " " + entry["time"]
        lines.append("### %s（%s）" % (w, stamp))
        if entry.get("note"):
            lines.append("- 注：%s" % entry["note"])
        for ch in entry.get("changes", []):
            lines.append("- %s: %s → %s" % (ch["key"], ch["from"], ch["to"]))
        if not entry.get("changes"):
            lines.append("- （无变更·例行重跑）")
        lines.append("")
    with open(INDEX, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--w", help="本批 W 号（记入变更史；缺省记 null 并提示）")
    ap.add_argument("--check", action="store_true", help="与磁盘现存 stats.json 对账（应零差异）")
    args = ap.parse_args()

    values = build()
    old_entities = load_json(OUT, {})

    if args.check:
        diffs = {k: ((old_entities.get(k) or {}).get("value"), v) for k, v in values.items() if (old_entities.get(k) or {}).get("value") != v}
        for k, (o, n) in sorted(diffs.items()):
            print("DRIFT %s: stats.json=%s 磁盘实算=%s" % (k, o, n))
        print(("FAIL  %d 键漂移——重跑 python scripts/stats.py --w <批号> 刷新" if diffs else "OK    stats.json 与磁盘实算零差异（%d 键）") % (len(diffs) or len(values)))
        return 1 if diffs else 0

    today = datetime.date.today().isoformat()
    now = datetime.datetime.now()
    generated_at = now.strftime("%Y-%m-%dT%H:%M:%S")  # W716：补时分秒（同日多批可区分）
    old_plain = {k: (e.get("value") if isinstance(e, dict) else e) for k, e in old_entities.items()}
    changes = [{"key": k, "from": old_plain.get(k), "to": v} for k, v in sorted(values.items()) if old_plain.get(k) != v]
    hist, migrated = migrate_hist(load_json(HIST, []))
    if changes:
        if not args.w:
            print("WARN  检出 %d 键变更但未给 --w——变更史将以 w=null 登记（建议 --w <批号>）" % len(changes))
        hist["entries"].append({"date": today, "time": now.strftime("%H:%M:%S"), "w": args.w, "changes": changes})  # W718：time 字段
        with open(HIST, "w", encoding="utf-8", newline="\n") as f:
            json.dump(hist, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
    elif migrated:
        with open(HIST, "w", encoding="utf-8", newline="\n") as f:  # W718：结构迁移写回（无变更也落盘一次）
            json.dump(hist, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("OK    变更史已迁移 %s（旧 list → entries·W704 条目补注）" % HIST_SCHEMA)

    entities = {}
    for k, v in values.items():
        old_e = old_entities.get(k) if isinstance(old_entities.get(k), dict) else {}
        last_changed = old_e.get("last_changed_by") or META[k]["introduced_by"]
        if any(c["key"] == k for c in changes):
            last_changed = args.w or last_changed
        entities[k] = {
            "value": v,
            "domain": META[k]["domain"],
            "generator": "scripts/stats.py",
            "introduced_by": META[k]["introduced_by"],
            "last_changed_by": last_changed,
        }
    out = {"_generated": generated_at, "_generator": "scripts/stats.py（W704 实体化·第 31 门禁 C5 对账基准·改口径批次须同批 --w 刷新）", "_format": "entity-v1"}
    out.update(entities)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    render_index(hist, entities)

    for k in sorted(values):
        mark = " *" if any(c["key"] == k for c in changes) else ""
        print("%s = %s%s" % (k, values[k], mark))
    print("OK    -> %s%s" % (os.path.relpath(OUT, ROOT), "（变更 %d 键→changelog+index 已更新）" % len(changes) if changes else "（无变更）"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
