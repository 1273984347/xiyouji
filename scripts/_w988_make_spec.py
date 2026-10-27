# -*- coding: utf-8 -*-
"""_w988_make_spec.py — W988 级联 spec 生成（水墨卡族投放批）

「文件」行**全量列出本次提交的文件**（含 102 个页面 + 115 个新资产）——
第 31 门禁 C4-f 判据是「文件行路径 ⊆ HEAD 树/staged 且无工作树残留」，
全量列出即可让任何「漏 add」当场判红（历史惯例：W983 段 107 项 / W984 段 140 项）。

输出：scripts/output/_w988_spec.json
用法：py -3 scripts/_w988_make_spec.py
"""
import glob
import io
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
IMG = os.path.join(REPO, "site", "static", "images")

# ---------- 1) 本批实际改动的页面（27 落位页 + 纯 og 页）----------
PAGES = []
with open(os.path.join(OUT, "_w988_precheck.json"), encoding="utf-8") as fh:
    PRE = json.load(fh)
for o in PRE["og_plan"]:
    PAGES.append(o["page"])
PAGES = sorted(set(PAGES))

# ---------- 2) 本批新增的资产（13 横幅 + 102 og）——用 git 判定「新增」避免把未改动的既有 og-*.webp 列入清单 ----------
_new = set()
for root, _dirs, files in os.walk(os.path.join(REPO, "site", "static", "images")):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), REPO).replace("\\", "/")
        if f.endswith(".webp") and (f.startswith("banner-") or f.startswith("og-")):
            _new.add(rel)
import subprocess
# 用 **HEAD 树**（不是索引）判定「本批新增」——本批已 git add 过，用索引会把新文件误判为既有
_tracked = set(subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "site/static/images"],
                               capture_output=True, text=True, cwd=REPO).stdout.split())
ASSETS = sorted(os.path.basename(p) for p in _new if p not in _tracked)

# ---------- 3) 本批脚本与产物 ----------
SCRIPTS = [
    "scripts/_w988_plan.py",
    "scripts/_w988_subject.py",
    "scripts/_w988_inventory.py",
    "scripts/_w988_match.py",
    "scripts/_w988_precheck.py",
    "scripts/_w988_make_assets.py",
    "scripts/_w988_insert.py",
    "scripts/_w988_fix_eol.py",
    "scripts/_w988_verify.py",
    "scripts/_w988_sheet.py",
    "scripts/_w988_card_sheet.py",
    "scripts/_w988_pitfalls.py",
    "scripts/_w988_docs.py",
    "scripts/_w988_make_spec.py",
    "scripts/_w988_fix_cascade.py",
    "scripts/_w988_fix_gates.py",
    "scripts/check_seo_head.py",
    "scripts/output/_w988_spec.json",
    "scripts/output/_w988_precheck.json",
    "scripts/output/_w988_assets.json",
    "scripts/output/_w988_inventory.json",
    "scripts/output/_w988_match.json",
    "scripts/output/_w988_card_map.json",
    "scripts/output/_w988_card_sheet.png",
    "scripts/output/_w988_sheet-banner.png",
    "scripts/output/_w988_sheet-og.png",
    "scripts/output/_cascade_files_W988.txt",
]

# ---------- 4) 文档与级联面 ----------
DOCS = [
    "docs/11-方案报告/计划方案/T34-任务计划执行与经验沉淀报告-2026-10-27.md",
    "docs/11-方案报告/README.md",
    "docs/agent/pitfalls.md",
    "docs/10-方法论沉淀/素材批处理与判据自证方法论.md",
    "docs/00-导读/W批次编号对账表.md",
    "AGENTS.md",
    "HANDOVER.md",
    "CHANGELOG.md",
    "README.md",
    "STRUCTURE.md",
    "docs/00-导读/项目说明.md",
    ".github/workflows/README.md",
    "site/index.html",
    "site/data/cross-time-danmaku.html",
    "site/data/tag-cloud.html",
    "site/dukou-engine.html",
    "CITATION.cff",
    "archive/docs/AGENTS-ARCHIVE.md",
    "scripts/output/file-index.md",
]

DOC_FILES = PAGES + ["site/static/images/" + a for a in ASSETS] + SCRIPTS + DOCS

BODY = (
    "\n\n\n\n> **来源**：用户 2026-10-27 选区指定两项（① card-* 27 张按题材逐张定投放位置（人物卡→角色页顶部横幅 / 场景卡→主题页）"
    "② 分回次 og:image（现全站共用一张通用图，需另裁 1200×630 版））→ 问卷裁定两处执行口径"
    "（横幅＝另裁 1200×500 宽幅·人物半身特写；og:image＝只做有配图的页·纯裁切）。\n"
    ">\n"
    "> - **文件**：" + "、".join(DOC_FILES) + "。\n\n"
    "**本批要点**：① **27 张 `card-*` 逐张定投放位置并接入**（用户选区指定的第一项）——"
    "**13 张人物卡 → 角色页/回目页顶部 `.chapter-banner` 横幅**（1:1 源另裁 1200×500 宽幅·人物半身特写·新立第三套类名·限宽 720px·暗色隐藏·"
    "横幅在题图之上形成「通栏横幅 + 420px 竖题图」宽窄分层），**14 张场景卡 → 主题页 `.chapter-scene` 场景位**（1:1 原图不裁·限宽 520px·"
    "插在正文首个章节标题前；「方向二深化」页用 `<h3>`、白骨精外传页无章节标题 ⇒ 插入点三情形兜底）⇒ **27 张全部有归属，闲置归零**；"
    "② **分回次 og:image**——**102 页**由「全站共用一张通用图」改为**该页首屏第一张配图**的 1200×630 专属裁切版"
    "（81 个既有题图页 + 11 个横幅页 + 10 个场景页；问卷裁定「只做有配图的页·纯裁切」⇒ **不新出图**），"
    "共享通用图的页面从 705 降到 603；③ **主体检测排除朱砂与赭金**——水墨卡族每张带朱红印章，"
    "整幅墨迹 bbox 会把印章算成主体 ⇒ 改用「面积 ≥ 200 px² 的连通簇 + 排除朱砂（r−g ≥ 35）与赭金（luma ≥ 90）」，27 张主体带全部正确；"
    "④ **三处踩坑当场修**——写盘行尾二次替换污染 102 页（CRLF→CRCRLF·字节级还原）；"
    "「按主体顶裁」在主体位于画面下部时切掉人物（1 张加特例带）；验收判据自身两处缺陷（CSS 计数未行首锚定 + 负样本形态不匹配 ⇒ 检查恒真）"
    "⇒ **坑表 +7 条（80 → 87）** + 方法论篇新增 §2.9「既有资产投放」。\n\n"
    "**验证**：落位表自检 27 张唯一 + 27 个目标页唯一 + 横幅/场景目标页无交叉 · 接入前预检 27 源图 / 27 目标页 / 81 既有题图页 / 102 og 页 · "
    "资产派生 115 张（13 张 1200×500 + 102 张 1200×630·合计 8.2 MB）· 接入 13 + 14 + 102 且**幂等复跑全 SKIP** · "
    "验收判据 V1–V9 **9/9 PASS**（含 figure 数 / CSS 规则数 / 插入点 / 暗色隐藏 / og 指向 / 资产尺寸 / 源卡引用）· "
    "**负样本自证 4/4 各自命中**（缺 CSS / 多 figure / 图文件缺失 / og 尺寸写错）· 27 页 + 115 资产 URL 全 200（`image/webp`）· "
    "浏览器实跑渲染正常（猪八戒页：标题 → 720px 水墨横幅 → 420px 线描题图 → 轨标 → 正文·两层宽窄分明无重叠）· "
    "行尾零污染（CRCRLF 0 · `git diff --numstat` 332 增 / 103 删无行尾噪音）· 第 48 门禁 0 FAIL · 全量门禁 55/55 段全绿。\n\n"
    "> - **状态**：已收官（内容批与登记面同批落地·既有 81 页题图的图源与 alt 未改动·27 张 `card-*` 源图本身未改动·"
    "12 个已有专属 og 图的页面未改动）\n"
)

MILESTONE = (
    "- **W988 水墨卡族投放批**（27 张 `card-*` 逐张定投放位置 + 分回次 og:image）：\n"
    "  - 27 张逐张落位：13 张人物卡 → `.chapter-banner` 横幅（另裁 1200×500 宽幅·限宽 720px）+ 14 张场景卡 → `.chapter-scene` 场景位（1:1 原图）\n"
    "  - og:image 分章化：102 页换专属 1200×630 裁切版（81 题图页 + 11 横幅页 + 10 场景页·纯裁切不新出图）\n"
    "  - 主体检测排除朱砂与赭金（印章不再被当成主体）· 坑表 +7 条（80 → 87）· 方法论篇新增 §2.9"
)

AGENTS_NOTE = (
    "2026-10-27（W988）把 27 张一直没被引用的 1:1 水墨卡逐张放了出去：先实读整族拼图定题材（关键词检索两头都不准），"
    "再把人物卡另裁成宽幅当角色页顶部横幅、场景卡原样放主题页场景位；顺手把全站共用一张的 og:image 改成「每页首屏第一张配图」的专属裁切版。"
    "三处踩坑值得记：写盘行尾被二次替换污染、量测时把设备像素当 CSS 像素、以及——自己写的验收判据也会错，所以判据必须带负样本自证。"
)

FILE_INDEX_ROWS = []
for p in PAGES:
    kind = "接入落位（横幅/场景图）+ og:image 换专属图" if any(p == t for t in
                   [x["target"] for x in PRE["pages"]]) else "og:image 换专属 1200×630 裁切版"
    FILE_INDEX_ROWS.append("| %s | W988 | %s |" % (p, kind))
for a in ASSETS:
    if a.startswith("banner-"):
        note = "新增角色页顶部横幅（1:1 源裁 1200×500 宽幅）"
    else:
        note = "新增 og:image 专属裁切版（1200×630）"
    FILE_INDEX_ROWS.append("| site/static/images/%s | W988 | %s |" % (a, note))
FILE_INDEX_ROWS += [
    "| docs/11-方案报告/计划方案/T34-任务计划执行与经验沉淀报告-2026-10-27.md | W988 | 终稿报告件（计划 + 执行合一·含 27 张落位表） |",
    "| docs/11-方案报告/README.md | W988 | §六 计划方案补登记 3 行（序号 41/42/43·T-18 / T-21 / T-34）· 件数 43 → 44 |",
    "| docs/agent/pitfalls.md | W988 | 坑表 +7 条（80 → 87：行尾二次替换 / 设备像素当 CSS 像素 / 主体检测排除朱砂赭金 / 关键词法双重失效 / 主体顶裁前提 / 判据自身缺陷） |",
    "| docs/10-方法论沉淀/素材批处理与判据自证方法论.md | W988 | 新增 §2.9「既有资产投放：落位表先行 + 三族资产三套类名 + 派生裁切的主体检测」 |",
    "| docs/00-导读/W批次编号对账表.md | W988 | W988 认领行 + 收官状态 |",
    "| AGENTS.md | W988 | 坑位条数声明 80 → 87 |",
    "| HANDOVER.md | W988 | 坑位条数指针 80 → 87 |",
    "| CHANGELOG.md | W988 | W988 段 |",
    "| README.md | W988 | 当前批次版本行 |",
    "| STRUCTURE.md | W988 | 当前批次版本行 |",
    "| docs/00-导读/项目说明.md | W988 | 当前批次版本行 |",
    "| .github/workflows/README.md | W988 | 工作流层版本面推进 W988 |",
    "| site/index.html | W988 | 页脚批次链插入 W988 |",
    "| site/data/cross-time-danmaku.html | W988 | 页脚批次链插入 W988 |",
    "| site/data/tag-cloud.html | W988 | 页脚批次链插入 W988 |",
    "| site/dukou-engine.html | W988 | 页脚批次链插入 W988 |",
    "| archive/docs/AGENTS-ARCHIVE.md | W988 | 脚注滚动迁入的最老条目 |",
    "| CITATION.cff | W988 | version 同步为 W988 |",
    "| scripts/output/file-index.md | W988 | W988 段插入 |",
    "| scripts/check_seo_head.py | W988 | og:image 白名单改**目录派生式**（W988 依用户指令「分回次 og:image」授权改管控件·W922 先例） |",
]
for s in SCRIPTS:
    note = "本批工具/产物"
    FILE_INDEX_ROWS.append("| %s | W988 | %s |" % (s, note))

SPEC = {
    "batch": "W988",
    "date": "2026-10-27",
    "title": "W988 水墨卡族投放批（27 张 card-* 逐张定投放位置 + 分回次 og:image 换专属图）",
    "desc": "水墨卡族投放：27 张 card-* 逐张定落位并接入（13 横幅 + 14 场景图），另给 102 页换上专属 1200×630 og:image",
    "head_entry": "2026-10-27（W988 水墨卡族投放批）",
    "head_sentence": "水墨卡族投放：27 张 card-* 逐张定落位接入，102 页 og:image 换专属 1200×630 裁切版",
    "changelog_body": BODY,
    "milestone_block": MILESTONE,
    "agents_note": AGENTS_NOTE,
    "file_index_rows": FILE_INDEX_ROWS,
}

p = os.path.join(OUT, "_w988_spec.json")
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(SPEC, ensure_ascii=False, indent=1))
print("spec 已写：%s" % p)
print("  文件清单 %d 项（页面 %d · 资产 %d · 脚本产物 %d · 文档级联 %d）"
      % (len(DOC_FILES), len(PAGES), len(ASSETS), len(SCRIPTS), len(DOCS)))
print("  file_index %d 行" % len(FILE_INDEX_ROWS))
