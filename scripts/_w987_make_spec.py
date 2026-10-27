# -*- coding: utf-8 -*-
"""_w987_make_spec.py — W987 级联 spec 生成（水墨意境卡族启用批）

「文件」行只列**本次提交**的文件（资产面本身未改动文件，仅引用）⇒ 避免第 31 门禁 C4-f「未入提交树」误判。

输出：scripts/output/_w987_spec.json
用法：py -3 scripts/_w987_make_spec.py
"""
import io
import json
import os

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")

DOC_FILES = [
    "site/reader/ch007.html",
    "site/reader/ch014.html",
    "site/reader/ch015.html",
    "site/reader/ch023.html",
    "site/reader/ch027.html",
    "site/reader/ch030.html",
    "assets/promo/README.md",
    "docs/11-方案报告/计划方案/T33-任务计划执行与经验沉淀报告-2026-10-27.md",
    "docs/00-导读/W批次编号对账表.md",
    "docs/11-方案报告/README.md",
    "docs/agent/pitfalls.md",
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
    "scripts/_w987_family_scan.py",
    "scripts/_w987_insert_scenes.py",
    "scripts/output/_w987_family_scan.json",
    "scripts/output/_w987_spec.json",
    "scripts/output/_cascade_files_W987.txt",
]

BODY = (
    "\n\n\n\n> **来源**：用户 2026-10-27 20:50 问「浓墨渲染图可以用在哪里？」→ 20:53 令「开工」（采纳建议顺序：① 归族登记 ② 启用为回目页场景插图）。\n"
    ">\n"
    "> - **文件**：" + "、".join(DOC_FILES) + "。\n\n"
    "**本批要点**：① **实读发现**——站内 `card-*` 27 张 + `chap-*` 6 张 = **33 张 1:1（1200×1200）水墨意境插画全部 0 引用**"
    "（同族两套命名：按回目 / 按角色场景 ⇒ 极易被误当题图用，W984 批即踩过），**闲置规模比用户感知大 5.5 倍**；"
    "② **归族登记**——`assets/promo/README.md` 新增「水墨意境卡族」节：成员表 + **规范边界表**"
    "（画幅 1:1 / 画风水墨晕染 / **可带印章** / **不得填进 `.chapter-plate`** / 暗色模式同样隐藏 / alt 描述画面）+ 引用状态 + 投放位置建议 + 维护约定；"
    "③ **启用 6 张**——6 个回目页（ch007 / ch014 / ch015 / ch023 / ch027 / ch030）新增 `.chapter-scene` 场景图："
    "**首屏仍留题图**（角色立像），场景图下沉到**正文首个 `<h2>` 之前**（限宽 520px·题图 420px）⇒ 同回形成「角色立像 + 水墨意境」双层节奏；"
    "④ **其余 27 张 `card-*` 本批不启用**（题材各异·投放位置需逐张判断·另批），登记待定。\n\n"
    "**验证**：族成员实读 33 张（全部 1200×1200·引用 0）· 6 页接入成功且幂等复跑 6/6 SKIP · "
    "同页题图 1 + 场景图 1 且类名不混 6/6 · `.chapter-scene` 样式与**暗色模式隐藏规则**齐备 6/6 · alt 均真实描述画面 6/6 · "
    "6 个场景图 URL HTTP 200 `image/webp` · 浏览器实跑渲染正常（ch007：首屏题图 → 元信息 → 正文入口场景图 → 原文回目·两图分隔清晰）· "
    "第 48 门禁 0 FAIL · 全量门禁 55/55 段全绿。\n\n"
    "> - **状态**：已收官（内容批与登记面同批落地·母版族 76 张与 6 个浓墨版源文件均未改动）\n"
)

MILESTONE = (
    "- **W987 水墨意境卡族启用批**（33 张 1:1 水墨插画·6 张上回目页场景位）：\n"
    "  - 归族登记：成员 33 张 + 规范边界（可带印章·不进 `.chapter-plate`·暗色隐藏·1:1）+ 投放位置建议\n"
    "  - 6 个回目页新增 `.chapter-scene` 场景图（首屏留题图·场景图下沉到正文首个 `<h2>` 前）\n"
    "  - 实读发现：闲置规模比感知大 5.5 倍（33 张全 0 引用）⇒ 坑表 +3 条（77 → 80）"
)

AGENTS_NOTE = (
    "2026-10-27（W987）做了一件盘点式的活：用户问「浓墨渲染图可以用在哪里」，实读才发现站内躺着 33 张 1:1 水墨意境插画——"
    "除了那 6 张，还有 27 张同样从未上线，同族却分成「按回目」和「按角色场景」两套命名，于是它们看起来像题图的旧版，其实是另一条画风线。"
    "于是做了两件事：给这一族立规矩（可带印章，但绝不填进题图那个容器类名，暗色模式同样得藏起来），"
    "再挑 6 张按回次接进正文——首屏仍留给题图，场景图下沉一层，两张图各司其职。"
    "提醒自己：仓库里的闲置资产，最容易被低估的不是数量，而是没人知道它有多少。"
)

FILE_INDEX_ROWS = [
    "| site/reader/ch007.html | W987 | 新增场景图（`.chapter-scene`·第 007 回八卦炉意境图） |",
    "| site/reader/ch014.html | W987 | 新增场景图（第 014 回猴形剪影意境图） |",
    "| site/reader/ch015.html | W987 | 新增场景图（第 015 回白马崖意境图） |",
    "| site/reader/ch023.html | W987 | 新增场景图（第 023 回静坐烛影意境图） |",
    "| site/reader/ch027.html | W987 | 新增场景图（第 027 回三背影茅屋意境图） |",
    "| site/reader/ch030.html | W987 | 新增场景图（第 030 回黑虎洞穴意境图） |",
    "| assets/promo/README.md | W987 | 新增「水墨意境卡族」节（成员 33 张·规范边界表·投放位置建议·维护约定） |",
    "| docs/11-方案报告/计划方案/T33-任务计划执行与经验沉淀报告-2026-10-27.md | W987 | 终稿报告件（计划 + 执行合一） |",
    "| docs/00-导读/W批次编号对账表.md | W987 | W987 认领行 + 收官状态 |",
    "| docs/11-方案报告/README.md | W987 | §六 计划方案登记 +1 行（序号 40·T-33）· 件数 42 → 43 |",
    "| docs/agent/pitfalls.md | W987 | 坑表 +3 条（77 → 80：资产族归族登记 / 类名隔开规范 / 同页两图首屏留主资产） |",
    "| AGENTS.md | W987 | 坑位条数声明 77 → 80 |",
    "| HANDOVER.md | W987 | 坑位条数指针 77 → 80 |",
    "| CHANGELOG.md | W987 | W987 段 |",
    "| README.md | W987 | 当前批次版本行 |",
    "| STRUCTURE.md | W987 | 当前批次版本行 |",
    "| docs/00-导读/项目说明.md | W987 | 当前批次版本行 |",
    "| .github/workflows/README.md | W987 | 工作流层版本面推进 W987 |",
    "| site/index.html | W987 | 页脚批次链插入 W987 |",
    "| site/data/cross-time-danmaku.html | W987 | 页脚批次链插入 W987 |",
    "| site/data/tag-cloud.html | W987 | 页脚批次链插入 W987 |",
    "| site/dukou-engine.html | W987 | 页脚批次链插入 W987 |",
    "| archive/docs/AGENTS-ARCHIVE.md | W987 | 脚注滚动迁入的最老条目 |",
    "| CITATION.cff | W987 | version 同步为 W987 |",
    "| scripts/output/file-index.md | W987 | W987 段插入 |",
    "| scripts/_w987_family_scan.py | W987 | 族盘点 + 插入点实测（成员/尺寸/引用/行号） |",
    "| scripts/_w987_insert_scenes.py | W987 | 6 页场景图接入（`.chapter-scene`·幂等） |",
    "| scripts/output/_w987_family_scan.json | W987 | 族盘点报告 |",
    "| scripts/output/_w987_spec.json | W987 | 本批级联 spec |",
    "| scripts/output/_cascade_files_W987.txt | W987 | 级联落盘清单 |",
]

SPEC = {
    "batch": "W987",
    "date": "2026-10-27",
    "title": "W987 水墨意境卡族启用批（33 张 1:1 水墨插画·6 张上回目页场景位）",
    "desc": "水墨意境卡族启用：归族登记 33 张从未上线的 1:1 水墨插画并立下规范边界，另启用 6 张为回目页场景插图，首屏仍留题图",
    "head_entry": "2026-10-27（W987 水墨意境卡族启用批）",
    "head_sentence": "水墨意境卡族启用：33 张 1:1 水墨插画归族登记，6 张接进回目页场景位",
    "changelog_body": BODY,
    "milestone_block": MILESTONE,
    "agents_note": AGENTS_NOTE,
    "file_index_rows": FILE_INDEX_ROWS,
}

p = os.path.join(OUT, "_w987_spec.json")
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(SPEC, ensure_ascii=False, indent=1))
print("spec 已写：%s（文件清单 %d 条·file_index %d 行）" % (p, len(DOC_FILES), len(FILE_INDEX_ROWS)))
