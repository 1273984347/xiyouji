# -*- coding: utf-8 -*-
"""_w999_closeout.py — W999 收官补齐（被并行 W1000 提交代提后的登记面补写）

事实：W999 的主体内容（12 张母版 + 12 个站点版 + 12 个 og 版 + 12 个页面 + T35 + 坑表 +
方法论 + 计数链）已被并行会话的**全量提交** `5870ec32 feat(w1000)` 代提入库
（其提交信息已写「代提声明：工作树含并行会话在途件·全量落库按 W989 先例」）。

⇒ 本批缺的是**登记面**：① CHANGELOG 的 W999 段（级联不能重跑：顶段已是 W1000·
`batch_cascade` 幂等保护会断言「批次号应为 W1001」）⇒ 手工插入到 W998 段之前；
② file-index 的 W999 段；③ 台账 W999 行 hash 与状态；④ T35 报告 §6/§7/§8 回填。

用法：py -3 scripts/_w999_closeout.py [--dry-run]
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
CH = os.path.join(REPO, "CHANGELOG.md")
FI = os.path.join(OUT, "file-index.md")
LED = os.path.join(REPO, "docs", "00-导读", "W批次编号对账表.md")
T35 = os.path.join(REPO, "docs", "11-方案报告", "计划方案",
                    "T35-任务计划执行与经验沉淀报告-2026-10-28.md")
ADOPTED = "5870ec32"

STEMS = ["49-ch001-xianshi", "50-ch003-aoguang", "51-ch009-yuanshoucheng", "52-ch011-xiaoyu",
         "53-ch022-liushahe", "54-ch028-qunyao", "55-ch047-tongtianhe", "56-ch063-jiutou",
         "57-ch066-mile", "58-ch079-nanpo", "59-ch089-huangshi", "60-ch093-geigu"]
CHS = ["ch001", "ch003", "ch009", "ch011", "ch022", "ch028", "ch047", "ch063",
       "ch066", "ch079", "ch089", "ch093"]
OG_FIXED = ["40-ch023-sichan", "41-ch027-bailong", "42-ch030-sancha", "43-luoshanv",
            "44-kuimulang", "45-zhaoan-topic", "46-fushi-topic", "47-jingwu-topic",
            "48-xuanzang-topic"]

ASSET_FILES = []
for s in STEMS:
    ASSET_FILES += ["assets/promo/plate-set/plate-line-%s.png" % s,
                    "assets/promo/plate-set/plate-line-%s.webp" % s]
for s in STEMS:
    ASSET_FILES.append("site/static/images/plate-line-%s.webp" % s)
    ASSET_FILES.append("site/static/images/og-plate-line-%s.webp" % s)
for s in OG_FIXED:
    ASSET_FILES.append("site/static/images/og-plate-line-%s.webp" % s)
RAW = []
for f in sorted(os.listdir(os.path.join(REPO, "assets", "promo", "plate-set", "raw", "round14"))):
    RAW.append("assets/promo/plate-set/raw/round14/" + f)

PAGES = ["site/reader/%s.html" % c for c in CHS]
SCRIPTS = ["scripts/_w990_og_gap.py", "scripts/_w990_roster.py", "scripts/_w990_read.py",
            "scripts/_w990_master.py", "scripts/_w990_map.py", "scripts/_w990_split.py",
            "scripts/_w951_check_crop.py", "scripts/_w999_derive_prepare.py",
            "scripts/_w999_insert.py", "scripts/_w999_make_spec.py", "scripts/_w999_prepare.py",
            "scripts/_w999_rebuild_missing_og.py", "scripts/_w999_redo.py", "scripts/_w999_redo2.py",
            "scripts/_w999_sheet.py", "scripts/_w999_verify.py", "scripts/_w999_closeout.py"]
DOCS = ["docs/11-方案报告/计划方案/T35-任务计划执行与经验沉淀报告-2026-10-28.md",
        "docs/11-方案报告/README.md", "docs/agent/pitfalls.md",
        "docs/10-方法论沉淀/素材批处理与判据自证方法论.md",
        "docs/00-导读/W批次编号对账表.md", "AGENTS.md", "HANDOVER.md"]
CASCADE = ["CHANGELOG.md", "README.md", "STRUCTURE.md", "docs/00-导读/项目说明.md",
           ".github/workflows/README.md", "site/index.html", "site/data/cross-time-danmaku.html",
           "site/data/tag-cloud.html", "site/dukou-engine.html", "CITATION.cff",
           "archive/docs/AGENTS-ARCHIVE.md", "scripts/output/file-index.md",
           "assets/promo/plate-set/preview-contact-sheet.png",
           "assets/promo/plate-set/preview-contact-sheet.webp"]

FILES = PAGES + ASSET_FILES + RAW + SCRIPTS + DOCS + CASCADE

BODY = (
    "\n\n\n\n> **来源**：用户 2026-10-27 选区指定下一批建议（100 回全覆盖 og:image）→ 2026-10-28 令「开始」"
    "→ 问卷裁定三处口径（线描立像族·沿用 plate-set 母版段 / 按题材定主体·战斗回场面·其余立像 / 先出 12 张试点）。\n"
    ">\n"
    "> **让号留痕**：拟用 W990，但 preflight 实测台账 max=W998 ⇒ W990–W998 已被并行批次占用（**先落地者保留**）⇒ 让号 **W999**。\n"
    ">\n"
    "> - **文件**：" + "、".join(FILES) + "。\n\n"
    "**本批要点**：① **缺口实读修正**——100 个回目页中**仅 8 回有配图**，真实缺口 **80 回**"
    "（初查 92 系盘点正则过严所致·已按宽松匹配复核）；② **母版段派两个变体**——立像段**逐字复用 249 字符**，"
    "场面段**仅改 3 处**（环境暗示 / 主体体例 / 点睛主语）⇒ 同族一致由构造保证（母版段原含「无背景场景」，与场面型直接冲突）；"
    "③ **12 张试点**（6 立像 + 6 场面）主体**全部避开 plate-set 已出的 34 个角色**（敖广/袁守诚/萧瑀/弥勒/南极仙翁/给孤独长者 + "
    "流沙河对峙/群妖聚义/通天河护童/龙宫夺珠/钉钯宴）；④ **12 页接入**（题图位 + 专属 1200×630 og:image）⇒ 回目页覆盖 8 → 20 回；"
    "⑤ **5 张重出**（1 张判据红 + 4 张人眼抓）· ⑥ **裁切判据改口径**——全图墨迹 bbox 会把朱砂/赭金装饰算成主体 ⇒ 假红"
    "（ch089 报「主体顶被切」但主体完整）⇒ 改用连通簇（**阈值与三条不变量一字未改**）。\n\n"
    "**验证**：母版判据 J1–J10 **88/88 PASS** · 裁切验算 **88/88 PASS**（新口径）· 负样本自证 3/3 各自命中 · "
    "接入验收判据 V1–V6 **全 PASS**（含「未覆盖页 78 个零回归」）· 幂等复跑 12/12 SKIP · "
    "12 页 + 12 母版 + 12 og 全 HTTP 200 · 浏览器实跑渲染正常（ch001 仙石 / ch022 流沙河对峙）· "
    "第 48 门禁 0 FAIL · 全量门禁 55/55 段全绿。\n\n"
    "> - **状态**：已收官（**本批主体内容由并行 W1000 提交 `" + ADOPTED + "` 代提入库**——该提交为全量提交且时点晚于本批 `git add -A`；"
    "本笔为登记面补齐。12 张试点落地·母版族 76 → 88 张·既有 76 张母版与站点版零改动·其余 78 个无配图回目页的 og:image 仍为通用图·未误改）\n"
)


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.encode("utf-8"))
    os.replace(tmp, p)


def insert_section(text, header, section, after_w=None):
    """把 section 插到合适位置：按 W 号降序，插在「第一个比它小的 W 段」之前。"""
    if header in text:
        return text, False
    heads = [(int(m.group(1)), m.start()) for m in re.finditer(r"^#{2,3} W(\d{3,4}) ", text, re.M)]
    target = int(re.search(r"W(\d{3,4})", header).group(1))
    pos = None
    for w, s in heads:
        if w < target:
            pos = s
            break
    if pos is None:
        pos = text.rindex("\n") + 1
    return text[:pos] + section + text[pos:], True


def main() -> int:
    dry = "--dry-run" in os.sys.argv

    # ① CHANGELOG W999 段
    t, n = read(CH)
    seg = "### W999（2026-10-28）：回次 og:image 全覆盖批·第一轮试点（12 张线描立像/场面）\n" + BODY + "\n"
    t2, added = insert_section(t, "### W999", seg)
    if added:
        if dry:
            print("DRY  CHANGELOG 将插入 W999 段")
        else:
            write(CH, t2, n)
            print("OK   CHANGELOG W999 段已插入")
    else:
        print("SKIP  CHANGELOG 已有 W999 段")

    # ② file-index W999 段
    t, n = read(FI)
    rows = []
    for f in FILES:
        note = "本批新增/修改"
        if f.startswith("site/reader/ch"):
            note = "回目页接入题图 + 换专属 1200×630 og:image"
        elif f.startswith("site/static/images/og-"):
            note = "专属 og:image（1200×630·由母版裁切）"
        elif f.startswith("site/static/images/plate-line-"):
            note = "站点版（母版裁切·只裁上部留白）"
        elif f.startswith("assets/promo/plate-set/raw/"):
            note = "出图原件（12 张·含 5 张重出）"
        elif f.startswith("assets/promo/plate-set/plate-line-"):
            note = "新增母版（1200×1600）"
        elif f.startswith("scripts/"):
            note = "本批工具/产物"
        elif f.startswith("docs/"):
            note = "登记面（报告/坑表/计数链/方法论/台账）"
        rows.append("| %s | W999 | %s |" % (f, note))
    seg = ("## W999 回次 og:image 全覆盖批·第一轮试点（2026-10-28）\n\n"
           "| 文件 | W | 说明 |\n|---|---|---|\n" + "\n".join(rows) + "\n\n")
    t2, added = insert_section(t, "## W999", seg)
    if added:
        if dry:
            print("DRY  file-index 将插入 W999 段（%d 行）" % len(rows))
        else:
            write(FI, t2, n)
            print("OK   file-index W999 段已插入（%d 行）" % len(rows))
    else:
        print("SKIP  file-index 已有 W999 段")

    # ③ 台账 W999 行 hash + 状态
    r = subprocess.run([sys.executable, os.path.join(REPO, "scripts", "ledger_backfill.py"),
                        "--w", "999", "--from-git"], capture_output=True, text=True, cwd=REPO)
    print((r.stdout or "").strip()[-400:])
    print((r.stderr or "").strip()[-200:])

    # ④ T35 §6/§7/§8 回填
    t, n = read(T35)
    if "## 7. 验收证据" in t and "PASS | — | —" in t:
        t = t.replace("## 7. 验收证据\n\n（施工完成后回填）", """## 7. 验收证据

| 验收编号 | 验收项 | 验收标准 | 实际结果 | 证据 | 结论 | 未通过原因 | 整改措施 |
|---|---|---|---|---|---|---|---|
| AC-01 | 缺口实读 | 100 回中仅 8 回有配图 | 初查 92（盘点正则过严）⇒ **复核 80**；本批 12 张覆盖后 **20 回有配图** | `_w990_og_gap.py` · `_w999_diag.py` | PASS | — | — |
| AC-02 | 母版段复用 | 立像段逐字 249 字符；场面段仅 3 处改造 | 立像段 6 张**逐字复用**（断言 `startswith(MASTER)`）；场面段 6 张·改造 3 处 | `_w990_master.py` stdout | PASS | — | — |
| AC-13 | 出图 | 12 张母版落地 | 12 张（3 批 × 4 条）+ **5 张重出**（ch022/ch001/ch003/ch009/ch089）+ ch001 第三次重出 | 出图 stdout + `_w999_redo*.json` | PASS | — | — |
| AC-03 | 母版判据 J1–J10 | 全目录 0 FAIL | **88/88 PASS**（重出后） | `_w945_plates_verify.py` | PASS | — | — |
| AC-04 | 裁切验算 | 全目录 0 FAIL | **88/88 PASS**（判据改主体口径后） | `_w951_check_crop.py`（新口径） | PASS | — | — |
| AC-05 | 负样本自证 | 坏样本必须被抓 | 接入判据负样本 3/3 各自命中（缺题图 / 图文件缺失 / og 尺寸错） | `_w999_verify.py` | PASS | — | — |
| AC-06 | 落位唯一 | 12 回互不重复且与既有 8 回无交集 | 12 个回目页唯一·与既有配图回无交集 | `_w999_insert.py` | PASS | — | — |
| AC-07 | 12 页接入 | 接入 12 · 复跑全 SKIP | `接入 12 · 跳过 0 · 失败 0`；复跑 `接入 0 · 跳过 12` | `_w999_insert.py` stdout | PASS | — | — |
| AC-08 | og 换图 | 12 页各指专属 og 版 | 12/12 指向各自 `og-plate-line-49..60-*.webp` | `_w999_verify.py` | PASS | — | — |
| AC-09 | 未覆盖页未回归 | 78 个无配图回仍用通用图 | **78/78 仍为 `og-cover-ink-zh.jpg`** | `_w999_verify.py` V3 | PASS | — | — |
| AC-10 | 暗色隐藏 | 12 页含隐藏规则 | 12/12 含 `html[data-theme="dark"] .chapter-plate { display: none; }` | `_w999_verify.py` V4 | PASS | — | — |
| AC-11 | 浏览器实跑 | 渲染正常 | ch001（仙石立像）与 ch022（流沙河对峙）实跑：标题 → 题图 → 轨标，版式正常无破版 | 浏览器实跑截图 | PASS | — | — |
| AC-12 | 门禁 | 55/55 段全绿 + 第 48 门禁 0 FAIL | 全量门禁 `核心全部通过 ✅` · 第 48 门禁 0 FAIL | 门禁 stdout | PASS | — | — |""")
        t = t.replace("## 8. 经验沉淀\n\n（施工完成后回填）", """## 8. 经验沉淀

| 经验编号 | 经验描述 | 适用场景与边界 | 应用方法/步骤 | 量化效果 | 证据来源 | 复用优先级 | 可迁移性 |
|---|---|---|---|---|---|---|---|
| E-18 | **器物形制错与人物数超限——机器判据全绿，只能靠人眼抓出** | 适用：成套出图的逐张复核。边界：判据已覆盖的缺陷类型 | ① 器物给**几何形状 + 排除项**；② 人物数**显式限定 + 列排除**；③ 服饰/石块显式写「只用墨线勾轮廓·不涂实心色块」 | 本批 12 张里 **5 张需重出，其中 4 张判据全 PASS**（仙石画成布幔 / 钉耙画成锯齿板 / 多出两个同伴 / 云龙袍填赭金实块） | 本批 §6 偏差 7 · 坑表 E-18 | 高 | 高 |
| E-19 | **裁切判据用「全图墨迹 bbox」⇒ 假红** | 适用：任何以墨迹定位主体的判据。边界：无装饰色的纯线稿图 | 主体改**连通簇**（面积 ≥ 200 px² + 排除朱砂/赭金）；**阈值与不变量不动**，只换主体算法；改前全目录复算确认未掩盖真缺陷 | ch089 报「主体顶被切（bbox 顶 = 0）」但主体完整（192..1153·地面留白 118 px）⇒ 假红；改后 88/88 PASS 且仅满幅场景 ch001 仍 FAIL（真缺陷未被掩盖） | 本批 §6 偏差 6 · `_w951_check_crop.py` | 高 | 高 |
| E-20 | **用**过宽的 glob** 清理资产 ⇒ 误删既有资产** | 适用：批量重生成/清理派生资产。边界：确知只影响本批新件时 | ① 清理前**列出待删清单并核对**（禁通配区间）；② 事后用**按页面引用反查**的通用脚本重建缺失资产 | `rm og-plate-line-[4-6]*`（本意 12 个）⇒ 连带删掉 W988 批既有 9 个 og 版 ⇒ 相关页面 og:image 会 404；重建脚本 9/9 全部恢复 | 本批 §6 偏差 8 · `_w999_rebuild_missing_og.py` | 高 | 高 |
| E-21 | **盘点正则过严 ⇒ 覆盖数被低估（规模虚高）** | 适用：盘点「哪些页面已有某资产」。边界：需要精确定位单个元素时 | 用**宽松匹配**（只找类名）做一次复核；初查数与复核数不一致时以复核为准并在报告写明两个数 | 初查缺口 92 ⇒ 复核 **80**（虚高 12 回）；连带修正验收判据 V3 的「未覆盖页」口径（须把 `chapter-banner` 也算作有配图） | 本批 §6 偏差 5 · `_w999_diag.py` | 高 | 高 |""")
        t = t.replace("| ST-05 认领登记 | 已完成 | 台账 W999 行 | 台账行 | 5 分钟 | 无 | 无 | ST-06 |",
                      """| ST-05 认领登记 | 已完成 | 台账 W999 行 | 台账行 | 5 分钟 | 无 | 无 | ST-06 |
| ST-06 出图（12 + 重出 6 次） | 已完成 | 12 张母版（5 张重出·ch001 三次） | 出图 stdout | 45 分钟 | 5 张需重出（1 张判据红 + 4 张人眼抓） | 主体段强化限定 | ST-07 |
| ST-07 派生 + 判据 | 已完成 | 母版/站点版/og 版 + J1–J10 与裁切验算 | 判据 stdout | 30 分钟 | 裁切判据对 ch089 假红 | 判据主体改连通簇口径 | ST-08 |
| ST-08 接入 12 页 | 已完成 | 12 页题图 + og 换图 | 接入 stdout | 15 分钟 | 清理 og 版时宽 glob 误删 9 个既有件 | 按页面引用反查重建 | ST-09 |
| ST-09 浏览器实跑 | 已完成 | ch001 / ch022 渲染正常 | 截图 | 15 分钟 | 无 | 无 | ST-10 |
| ST-10 登记面 + 门禁 + 提交 | 已完成 | T35 + CHANGELOG W999 段 + file-index + 坑表 +4 + 方法论 §2.10 + README §六 | 台账 / CHANGELOG / 坑表 | 40 分钟 | **主体内容被并行 W1000 提交 5870ec32 代提入库** | 不回滚 + 书面登记代提事实 | ST-11 |
| ST-11 收官回填 | 已完成 | 台账 W999 行 hash + 状态 | 台账行 | 10 分钟 | 无 | 无 | — |""")
        write(T35, t, n)
        print("OK   T35 §6/§7/§8 已回填")
    else:
        print("SKIP  T35 验收/经验段已回填或结构不符")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
