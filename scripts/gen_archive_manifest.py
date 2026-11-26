#!/usr/bin/env python3
"""gen_archive_manifest.py — 归档分卷清单生成与校验（W1335 建 · 归档分卷 C 先行 · B 终态）

背景（W1335 评估实测）：
  §11.2 只定义了 `<原名>-tier2.md` 单卷形态，实践中却长出 4 个范围命名卷（CHANGELOG 家族）
  与 2 个（file-index 家族）⇒ 规范落后于实践、无清单可查「W### 在哪个文件」、无覆盖判据
  （实测 CHANGELOG 家族区间内缺 114 号、file-index 缺 99 号，无人知晓是否丢段）。

本工具做三件事：
  ① 扫 archive/docs 下全部归档件 → 每卷的段数 / 真实 W 区间 / 体积 / 冻结状态；
  ② 产 **机读** scripts/output/archive-manifest.json + **人读** archive/docs/ARCHIVE-MANIFEST.md；
  ③ `--check` 与磁盘对拍（清单过期即 FAIL——防「登记面名存实亡」，项目已多次踩此坑）。

冻结条款（用户 2026-11-27 裁决）：**无范围名的旧卷**（CHANGELOG-ARCHIVE-tier2.md /
  file-index-ARCHIVE-tier2.md）冻结为只读——不再追加，仅由清单标注其真实区间。新迁出一律
  按 250 号宽度开范围命名卷（archive_tier2.py --range-width 250）。

用法：
  py -3 scripts/gen_archive_manifest.py --refresh   # 重生成清单（两面）
  py -3 scripts/gen_archive_manifest.py --check     # 对拍（exit 0 一致 / 1 过期）
  py -3 scripts/gen_archive_manifest.py --self-test
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ARCH = os.path.join(ROOT, "archive", "docs")
MANIFEST_JSON = os.path.join(ROOT, "scripts", "output", "archive-manifest.json")
MANIFEST_MD = os.path.join(ARCH, "ARCHIVE-MANIFEST.md")

# 新卷宽度（W 号跨度）——用户 2026-11-27 裁决 250
RANGE_WIDTH = 250
# 冻结卷：无范围名的旧二级归档（不再追加）
FROZEN = ("CHANGELOG-ARCHIVE-tier2.md", "file-index-ARCHIVE-tier2.md")
# 台账「无段可查」的合法说明词（作废 / 在途 / 合并入他段 / 追记 / 收编 / 占位空号 / 让号）
# W1335 口径修正：判据从「台账有行即须有段」收紧为「台账声明**已收官**才须有段」——
# 否则作废批、在途预约、合并段、追记全会被误报（首版实测 12 号误报，逐条核对后定此口径）。
NO_SEG_MARKERS = (
    "作废", "在途", "待批次落段", "待回填", "合并段", "追记", "收编", "占位空号",
    "让号", "空号", "无产出", "未产出", "成果已并入", "预约",
)
# 台账声明「已完结」的证据词——命中且无段 ⇒ 真缺段（FAIL）
SEG_EXPECT_MARKERS = ("已收官", "已闭环", "已落地", "已推送")

FAMILIES = {
    "changelog": {
        "glob": "CHANGELOG-ARCHIVE*.md",
        "seg": re.compile(r"(?m)^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（)"),
        "groups": 2,
        "live": "CHANGELOG.md",
    },
    "file-index": {
        "glob": "file-index-ARCHIVE*.md",
        "seg": re.compile(r"(?m)^## (W\d+) "),
        "groups": 1,
        "live": os.path.join("scripts", "output", "file-index.md"),
    },
}


def seg_numbers(text, fam):
    """卷内 W 号集合（changelog 双形态 / file-index 单组形态）。"""
    cfg = FAMILIES[fam]
    out = set()
    for m in cfg["seg"].finditer(text):
        if cfg["groups"] == 2:
            out.add(int(m.group(1) or m.group(2)))
        else:
            out.add(int(m.group(1)[1:]))
    return out


def live_numbers(fam):
    """正本（在役滚动文档）的 W 号集合。"""
    p = os.path.join(ROOT, FAMILIES[fam]["live"])
    if not os.path.exists(p):
        return set()
    return seg_numbers(open(p, encoding="utf-8").read(), fam)


def scan_family(arch_dir, fam):
    """扫一个家族的卷谱系 → (volumes, union, duplicates)。纯函数（arch_dir 可注入）。"""
    volumes, union, seen = [], set(), {}
    for p in sorted(glob.glob(os.path.join(arch_dir, FAMILIES[fam]["glob"]))):
        name = os.path.basename(p)
        text = open(p, encoding="utf-8").read()
        ws = seg_numbers(text, fam)
        if not ws:
            continue
        for w in ws:
            seen.setdefault(w, []).append(name)
        union |= ws
        volumes.append({
            "file": name,
            "bytes": os.path.getsize(p),
            "segs": len(ws),
            "w_min": min(ws),
            "w_max": max(ws),
            "frozen": name in FROZEN,
        })
    dup = {str(w): sorted(set(n)) for w, n in seen.items() if len(set(n)) > 1}
    return volumes, union, dup


def other_archives(arch_dir):
    """非滚动家族的归档件（只记体积·无段语义）。"""
    out = []
    for p in sorted(glob.glob(os.path.join(arch_dir, "*ARCHIVE*.md"))):
        name = os.path.basename(p)
        if any(re.match(FAMILIES[f]["glob"].replace("*", ".*"), name) for f in FAMILIES):
            continue
        if name == os.path.basename(MANIFEST_MD):
            continue
        out.append({"file": name, "bytes": os.path.getsize(p)})
    return out


def build(arch_dir=None):
    """构造清单载荷（纯函数·不含时间戳以便 --check 对拍）。"""
    arch_dir = arch_dir or ARCH
    payload = {"range_width": RANGE_WIDTH, "frozen": list(FROZEN), "families": {}, "others": []}
    for fam in FAMILIES:
        volumes, union, dup = scan_family(arch_dir, fam)
        payload["families"][fam] = {
            "volumes": volumes,
            "covered": len(union),
            "w_min": min(union) if union else None,
            "w_max": max(union) if union else None,
            "duplicates": dup,
        }
    payload["others"] = other_archives(arch_dir)
    return payload


def load_ledger_rows():
    """台账（正本 + 台账归档）的 {W号: 行文本}——T5 覆盖判据的事实源。"""
    rows = {}
    for rel in (os.path.join("docs", "00-导读", "W批次编号对账表.md"),
                os.path.join("archive", "docs", "W批次编号对账表-ARCHIVE.md")):
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8"):
            m = re.match(r"^\|\s*W(\d{3,4})\s*\|", ln)
            if m:
                rows[int(m.group(1))] = ln
    return rows


def load_t5_exemptions():
    """T5 显式豁免簿：`archive/docs/ARCHIVE-T5-EXEMPTIONS.md` 内 `- W### 理由` 行。

    为什么要有豁免簿而不是继续扩关键词：关键词只覆盖「台账自述」形态，而 W934 这类
    **历史缺口**（全仓无任何段承载该批内容）无法自述 ⇒ 必须由人工核实后显式登记，
    理由随行落盘、可审计（拒「悄悄+1」的黑名单）。
    """
    p = os.path.join(ARCH, "ARCHIVE-T5-EXEMPTIONS.md")
    out = {}
    if not os.path.exists(p):
        return out
    for ln in open(p, encoding="utf-8"):
        m = re.match(r"^\s*-\s*W(\d{3,4})\s+(.+?)\s*$", ln)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


def t5_coverage(families, ledger_rows, exemptions=None):
    """T5 覆盖完备性（纯函数·供门禁与单测）。

    判据（W1335 定稿）：台账登记号若**声明已收官/已闭环/已落地/已推送**，必须在正本或某卷
    找到段；找不到 ⇒ 真缺段。行内自带「作废/在途/合并段/追记/收编/占位空号/让号」等说明
    ⇒ 记为豁免（合法无段）。人工核实过、台账无法自述的历史缺口 → 显式豁免簿。
    同家族内一号多卷 = 重复。
    → dict(missing, duplicates, explained, exempt, checked)
    """
    exemptions = exemptions or {}
    missing, explained, exempt = [], 0, []
    for w, row in sorted(ledger_rows.items()):
        found = False
        for fam_data in families.values():
            ws = fam_data.get("_union")
            if ws is not None and w in ws:
                found = True
                break
        if found:
            continue
        if any(mk in row for mk in NO_SEG_MARKERS):
            explained += 1
        elif w in exemptions:
            exempt.append(w)
        elif any(mk in row for mk in SEG_EXPECT_MARKERS):
            missing.append(w)
        else:
            explained += 1  # 无任何完成证据的行（早期「已登记」形态）不判缺段
    duplicates = {}
    for fam, data in families.items():
        if data.get("duplicates"):
            duplicates[fam] = data["duplicates"]
    return {"missing": missing, "duplicates": duplicates, "explained": explained,
            "exempt": exempt, "checked": len(ledger_rows)}


def _render_md(payload):
    lines = [
        "# 归档分卷清单（ARCHIVE MANIFEST）",
        "",
        "> **本文件由 `scripts/gen_archive_manifest.py --refresh` 生成，勿手改**（`--check` 与磁盘对拍，"
        "改盘不改清单即 FAIL）。",
        "> **口径**：每个滚动家族（CHANGELOG / file-index）的卷谱系 × 真实 W 区间 × 体积 × 冻结状态；"
        "查「W### 在哪个文件」看本表，不要逐个 grep。",
        "> **冻结条款（W1335·用户 2026-11-27 裁决）**：无范围名的旧二级归档卷冻结为只读，不再追加；"
        "新迁出一律按 %d 号宽度开范围命名卷（`archive_tier2.py --range-width %d`）。" % (
            payload["range_width"], payload["range_width"]),
        "",
        "## 滚动家族卷谱系",
        "",
        "| 家族 | 卷文件 | 段数 | W 区间 | 体积 | 状态 |",
        "|:--|:--|--:|:--|--:|:--|",
    ]
    for fam, data in payload["families"].items():
        for v in data["volumes"]:
            lines.append("| %s | `%s` | %d | W%d–W%d | %.0f KB | %s |" % (
                fam, v["file"], v["segs"], v["w_min"], v["w_max"], v["bytes"] / 1024,
                "**冻结（只读）**" if v["frozen"] else "在役"))
        lines.append("| %s | *家族合计* | %d | W%s–W%s | — | 重复号 %d |" % (
            fam, data["covered"],
            data["w_min"] if data["w_min"] is not None else "-",
            data["w_max"] if data["w_max"] is not None else "-",
            len(data["duplicates"])))
    lines += [
        "",
        "## 其他归档件（无段语义·只记体积）",
        "",
        "| 文件 | 体积 |",
        "|:--|--:|",
    ]
    for o in payload["others"]:
        lines.append("| `%s` | %.0f KB |" % (o["file"], o["bytes"] / 1024))
    lines += [
        "",
        "## 复算",
        "",
        "```bash",
        "py -3 scripts/gen_archive_manifest.py --check      # 清单与磁盘一致？（过期即 FAIL）",
        "py -3 scripts/gen_archive_manifest.py --refresh    # 盘面变更后重建清单",
        "py -3 scripts/check_archive_health.py              # T1/T1b 体积 + T5 覆盖 + T6 总量",
        "```",
        "",
    ]
    return "\n".join(lines)


def _rel(p):
    """仓库内相对路径；跨盘符（单测 tmp_path 在 C:）时退回绝对路径。"""
    try:
        return os.path.relpath(p, ROOT)
    except ValueError:
        return p


def refresh():
    payload = build()
    os.makedirs(os.path.dirname(MANIFEST_JSON), exist_ok=True)
    with open(MANIFEST_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    with open(MANIFEST_MD, "w", encoding="utf-8", newline="\n") as f:
        f.write(_render_md(payload))
    print("[OK] 清单已重建：%s + %s" % (_rel(MANIFEST_JSON), _rel(MANIFEST_MD)))
    return 0


def check():
    disk = build()
    if not os.path.exists(MANIFEST_JSON):
        print("FAIL  清单缺失：%s（修法=--refresh）" % os.path.relpath(MANIFEST_JSON, ROOT))
        return 1
    saved = json.load(open(MANIFEST_JSON, encoding="utf-8"))
    # 判据面 = 卷谱系 / 冻结清单 / 卷宽（须与磁盘一致）；others 体积只是信息面——
    # 台账归档等「非滚动件」每批都在变，若纳入判据会让清单每批必刷（W1335 实测自锁）。
    if saved.get("others") != disk.get("others"):
        print("NOTE  其他归档件体积有变动（信息面·不判过期）——需要清单显示最新值时跑 --refresh")
    if saved.get("families") == disk.get("families") and \
            saved.get("frozen") == disk.get("frozen") and \
            saved.get("range_width") == disk.get("range_width"):
        total = sum(len(v["volumes"]) for v in disk["families"].values())
        print("---- 归档分卷清单：%d 家族 · %d 卷 · 与磁盘一致 · OK ----" % (len(disk["families"]), total))
        return 0
    diffs = []
    for fam in disk["families"]:
        a = saved.get("families", {}).get(fam, {})
        b = disk["families"][fam]
        if a != b:
            diffs.append("%s 家族卷谱系不一致（清单 %d 卷 / 磁盘 %d 卷）" % (
                fam, len(a.get("volumes", [])), len(b["volumes"])))
    if saved.get("frozen") != disk.get("frozen"):
        diffs.append("冻结清单不一致")
    if saved.get("range_width") != disk.get("range_width"):
        diffs.append("range_width 不一致")
    print("FAIL  归档清单已过期（修法=py -3 scripts/gen_archive_manifest.py --refresh）：")
    for d in diffs or ["载荷与磁盘不一致"]:
        print("  · " + d)
    return 1


def self_test():
    import tempfile
    fails = []
    td = tempfile.mkdtemp()
    open(os.path.join(td, "CHANGELOG-ARCHIVE.md"), "w", encoding="utf-8").write(
        "### W105（2026-01-01）：甲\n\n### W104（2026-01-01）：乙\n")
    open(os.path.join(td, "CHANGELOG-ARCHIVE-tier2.md"), "w", encoding="utf-8").write(
        "### W103（2026-01-01）：丙\n")
    vols, union, dup = scan_family(td, "changelog")
    if union != {103, 104, 105}:
        fails.append("changelog 段号解析错：%s" % sorted(union))
    if not any(v["frozen"] for v in vols):
        fails.append("冻结卷未被标注")
    # file-index 形态
    open(os.path.join(td, "file-index-ARCHIVE.md"), "w", encoding="utf-8").write("## W205 甲\n\n## W204 乙\n")
    _v, union2, _d = scan_family(td, "file-index")
    if union2 != {204, 205}:
        fails.append("file-index 段号解析错：%s" % sorted(union2))
    # T5：台账声明已收官但无段 → missing；带占位空号/合并段说明 → explained
    fams = {"changelog": {"_union": {104, 105}, "duplicates": {}}}
    rows = {
        104: "| W104 | 甲 | — | — | 已收官 |",
        105: "| W105 | 乙 | — | — | 已收官 |",
        106: "| W106 | 丙 | — | — | 已收官 |",
        107: "| W107 | 丁 | — | — | 占位空号 |",
        108: "| W108 | 戊 | — | — | 合并段·D1 |",
    }
    res = t5_coverage(fams, rows)
    if res["missing"] != [106]:
        fails.append("T5 缺段识别错：%s" % res["missing"])
    if res["explained"] != 2:
        fails.append("T5 豁免计数错：%s" % res["explained"])
    print("---- 自测：%s ----" % ("3/3 通过" if not fails else "FAIL " + "；".join(fails)))
    return 0 if not fails else 2


def main():
    ap = argparse.ArgumentParser(description="归档分卷清单（W1335）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--refresh", action="store_true")
    g.add_argument("--check", action="store_true")
    g.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.refresh:
        return refresh()
    return check()


if __name__ == "__main__":
    sys.exit(main())
