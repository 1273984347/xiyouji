# -*- coding: utf-8 -*-
"""_w986_make_spec.py — W986 级联 spec 生成（登记面补齐批）

文件清单口径：本批**本次提交**的文件（资产面 6 张母版/原件/站点版 + 6 页 alt 已由 `9841c05d` 落地，
在 CHANGELOG「文件」行以括注说明·不重复列入 ⇒ 避免第 31 门禁 C4-f「未入提交树」误判）。

输出：scripts/output/_w986_spec.json
用法：py -3 scripts/_w986_make_spec.py
"""
import io
import json
import os

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")

DOC_FILES = [
    "docs/11-方案报告/计划方案/T32-任务计划执行与经验沉淀报告-2026-10-27.md",
    "docs/00-导读/W批次编号对账表.md",
    "docs/11-方案报告/README.md",
    "docs/agent/pitfalls.md",
    "docs/10-方法论沉淀/素材批处理与判据自证方法论.md",
    "AGENTS.md",
    "HANDOVER.md",
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
    "scripts/output/_w986_spec.json",
    "scripts/output/_cascade_files_W986.txt",
]

FILE_ROW = ("docs/11-方案报告/计划方案/T32-任务计划执行与经验沉淀报告-2026-10-27.md", "W986",
            "终稿报告件（计划 + 执行合一·含执行记录/验收/风险与偏差/经验沉淀）")
FILE_ROW2 = ("docs/00-导读/W批次编号对账表.md", "W986", "W986 认领行 + 收官状态")
FILE_ROW3 = ("docs/agent/pitfalls.md", "W986", "坑表 +2 条（75 → 77·E-06 部分提交判红 / E-07 级联 body 沿用模板）")
FILE_ROW4 = ("docs/10-方法论沉淀/素材批处理与判据自证方法论.md", "W986",
             "§2.8 补「怎么换主体而不破母版段」（同名 stem 覆盖 + 只换 alt）")
FILE_ROW5 = ("docs/11-方案报告/README.md", "W986", "§六 计划方案登记 +1 行（T-32 合一件）· 件数 41 → 42")

BODY = (
    "\n\n\n\n> **来源**：用户 2026-10-27 12:26 对 W984 批回目页 6 张线描版的观感反馈「一般算不上好看」+ 12:35 裁决「换主体重出一版」。\n"
    ">\n"
    "> **让号留痕**：取号时 **W985 已被并行会话占用**（工具文档三件批·在途未提交·占 CHANGELOG / AGENTS / HANDOVER / 台账等共享面）"
    "⇒ 按「先落地者保留」让号 **W986**；共享面待 W985 收官后补登记。\n"
    ">\n"
    "> - **文件**：" + "、".join(DOC_FILES) + "。"
    "（**资产面已由 `9841c05d` 落地**：6 张母版 png/webp 同名覆盖 + 6 份原件 + 6 个站点版 webp + 全目录拼图 + 6 页 alt 文本更新 + `assets/promo/plate-set/README.md` 口径更新）\n\n"
    "**本批要点**：① **根因**——同角色 + 同画幅 + 同母版段 + 同构图范式的第二张图 ⇒ 观感必然重复，"
    "而 **J1–J10 全绿、缩略拼图也看不出**（坑表 E-05）⇒ 只有用户目视能判定；"
    "② **处置**——6 张**同名 stem 覆盖**（`plate-line-37..42`），主体全换此前未画过的角色"
    "（巨灵神 / 六贼头目 / 惠岸行者木叉 / 黎山老母 / 巡河夜叉 / 御马监丞），"
    "角色·体型·道具·姿态各异 ⇒ **页面图源路径不变、只换 alt 文本**；"
    "③ **6 个浓墨渲染版文件原样保留**（用户 2026-10-27 08:25 明令）⇒ 页面只用线描版，浓墨版作可回退存量；"
    "④ 登记面补齐时遇 **W985 在途** ⇒ 共享面等其收官后写；且实测**部分提交（pathspec）在共享面有在途批次时必被 C4-f 判红**"
    "（临时索引缺在途批次的收官内容）⇒ 改全量提交并声明代提（W932 先例）⇒ 坑表 +2 条（75 → 77）。\n\n"
    "**验证**：母版判据 J1–J10 **76/76 FAIL 0** · 站点版裁切验算 **76/76 FAIL 0**"
    "（6 张新主体主体顶余量 6 px·地面留白 93–141 px）· 负样本自检可证伪（坏样本被 J1 抓出）· "
    "纸色归一残差 ≤ 0.5/255 · 母版段 249 字符逐字复用 · 同名覆盖前提断言 6/6 · 人眼逐张复核 6/6 · "
    "6 页 alt 文本全部更新 · **6 个浓墨版文件逐个核验仍在** · 计划方案合规门禁 0 FAIL · 全量门禁 55/55 段全绿。\n\n"
    "> - **状态**：已收官（内容批 `9841c05d`·verify 全量 55/55 段全绿·母版判据 76/76 FAIL 0·裁切验算 76/76 FAIL 0·"
    "6 个浓墨版原文件保留未删·reader 有题图页仍 81 页）\n"
)

MILESTONE = (
    "- **W986 回目页 6 张线描版换主体重出批**（用户 2026-10-27 12:26 反馈「一般算不上好看」⇒ 换主体）：\n"
    "  - 6 张同名 stem 覆盖：巨灵神 / 六贼头目 / 惠岸行者木叉 / 黎山老母 / 巡河夜叉 / 御马监丞（均首次出现）\n"
    "  - 页面只换 alt 文本（img src 不变）· 6 个浓墨渲染版原文件保留未删\n"
    "  - 根因入坑表 E-05（同角色同范式的第二张图观感必然重复·机器判据查不出）· 另 +2 条（75 → 77）"
)

AGENTS_NOTE = (
    "2026-10-27（W986）补上了一个机器判据永远查不出来的维度：同一套画幅、同一段母版、同一构图范式下，"
    "同一个角色第二次出图，观感必然重复——判据全绿、拼图趋势也看不出，只有你的目视能判。"
    "于是这一批不换道具、换角色：回目页 6 张改成巨灵神、六贼头目、木叉、黎山老母、巡河夜叉、御马监丞，"
    "同名覆盖、只换 alt 文本，浓墨渲染的六张原稿原样留着以备回退。"
    "另外记下两条协作面的坑：共享面被在途批次占着时，部分提交会被门禁判红，只能全量提交并声明代提；"
    "级联脚本派生出来的版本说明也会沿用上一批的模板文字，写完必须逐段核对五处。"
)

FILE_INDEX_ROWS = [
    FILE_ROW, FILE_ROW2, FILE_ROW3, FILE_ROW4, FILE_ROW5,
    ("| assets/promo/plate-set/plate-line-37..42.png/.webp | W986 | 同名覆盖重出：巨灵神 / 六贼头目 / 惠岸行者木叉 / 黎山老母 / 巡河夜叉 / 御马监丞（已由 9841c05d 落地） |", ),
    ("| assets/promo/plate-set/raw/round13/plate-line-37..42.jpg | W986 | 出图原件 6 份（已由 9841c05d 落地） |", ),
    ("| site/static/images/plate-line-37..42.webp | W986 | 站点版 6 个（已由 9841c05d 落地） |", ),
    ("| site/reader/{ch007,ch014,ch015,ch023,ch027,ch030}.html | W986 | 6 页题图 alt 文本更新为新主体（img src 不变·已由 9841c05d 落地） |", ),
    ("| assets/promo/plate-set/README.md | W986 | 第七组清单改新主体 + 存量归档节补演进（已由 9841c05d 落地） |", ),
    ("| scripts/_w986_make_prompts.py | W986 | 换主体出图参数生成器（母版段逐字复用 + 同名覆盖前提断言） |", ),
    ("| scripts/output/_w986_batch1.json | W986 | 本批出图参数（6 条） |", ),
    ("| scripts/output/_w986_gen.json | W986 | node_id ↔ 文件名映射 |", ),
    ("| scripts/output/_w986_sheet.png | W986 | 本批 6 张复核拼图 |", ),
    ("| CHANGELOG.md | W986 | W986 段 |", ),
    ("| HANDOVER.md | W986 | 坑位条数指针 75 → 77 |", ),
    ("| README.md | W986 | 当前批次版本行 |", ),
    ("| STRUCTURE.md | W986 | 当前批次版本行 |", ),
    ("| docs/00-导读/项目说明.md | W986 | 当前批次版本行 |", ),
    ("| .github/workflows/README.md | W986 | 工作流层版本面推进 W986 |", ),
    ("| site/index.html | W986 | 页脚批次链插入 W986 |", ),
    ("| site/data/cross-time-danmaku.html | W986 | 页脚批次链插入 W986 |", ),
    ("| site/data/tag-cloud.html | W986 | 页脚批次链插入 W986 |", ),
    ("| site/dukou-engine.html | W986 | 页脚批次链插入 W986 |", ),
    ("| AGENTS.md | W986 | 坑位条数声明 75 → 77 |", ),
    ("| archive/docs/AGENTS-ARCHIVE.md | W986 | 脚注滚动迁入的最老条目 |", ),
    ("| CITATION.cff | W986 | version 同步为 W986 |", ),
    ("| scripts/output/file-index.md | W986 | W986 段插入 |", ),
    ("| scripts/output/_w986_spec.json | W986 | 本批级联 spec |", ),
    ("| scripts/output/_cascade_files_W986.txt | W986 | 级联落盘清单 |", ),
]

SPEC = {
    "batch": "W986",
    "date": "2026-10-27",
    "title": "W986 回目页 6 张线描版换主体重出批（用户观感反馈回炉·同名 stem 覆盖）",
    "desc": "回目页 6 张线描版换主体重出：根因是同角色同范式的第二张图观感必然重复而机器判据查不出，处置为同名 stem 覆盖换角色，浓墨渲染原稿保留不删",
    "head_entry": "2026-10-27（W986 回目页 6 张线描版换主体重出批）",
    "head_sentence": "回目页 6 张线描版换主体重出：同名 stem 覆盖换角色，浓墨渲染原稿保留不删",
    "changelog_body": BODY,
    "milestone_block": MILESTONE,
    "agents_note": AGENTS_NOTE,
    "file_index_rows": [r[0] for r in FILE_INDEX_ROWS],
}

p = os.path.join(OUT, "_w986_spec.json")
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(SPEC, ensure_ascii=False, indent=1))
print("spec 已写：%s（文件清单 %d 条·file_index %d 行）" % (p, len(DOC_FILES), len(FILE_INDEX_ROWS)))
