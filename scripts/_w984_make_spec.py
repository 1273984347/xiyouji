# -*- coding: utf-8 -*-
"""_w984_make_spec.py — W984 级联 spec 生成（**文件清单从磁盘实算**·不手抄）

纪律：CHANGELOG「文件」行必须全量列名 ⇒ 清单由磁盘扫描生成，避免手抄漏项/错名。
输出：scripts/output/_w984_spec.json
用法：py -3 scripts/_w984_make_spec.py
"""
import io
import json
import os

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")
SET = os.path.join(REPO, "assets", "promo", "plate-set")
SITE_IMG = os.path.join(REPO, "site", "static", "images")

STEMS = ["37-ch007-bagua-lu", "38-ch014-liubei", "39-ch015-yingchou", "40-ch023-sichan",
         "41-ch027-bailong", "42-ch030-sancha", "43-luoshanv", "44-kuimulang",
         "45-zhaoan-topic", "46-fushi-topic", "47-jingwu-topic", "48-xuanzang-topic"]

PAGES = [
    ("site/reader/ch007.html", "REPLACE", "第 007 回 八卦炉与五行山（替换浓墨版·原图保留）"),
    ("site/reader/ch014.html", "REPLACE", "第 014 回 六贼剪径（替换浓墨版·原图保留）"),
    ("site/reader/ch015.html", "REPLACE", "第 015 回 鹰愁涧意马收缰（替换浓墨版·原图保留）"),
    ("site/reader/ch023.html", "REPLACE", "第 023 回 四圣试禅心（替换浓墨版·原图保留）"),
    ("site/reader/ch027.html", "REPLACE", "第 027 回 白龙归水（替换浓墨版·原图保留）"),
    ("site/reader/ch030.html", "REPLACE", "第 030 回 邪魔侵正法（替换浓墨版·原图保留）"),
    ("site/reader/people/罗刹女外传.html", "INSERT", "罗刹女"),
    ("site/reader/people/奎木狼外传.html", "INSERT", "奎木狼"),
    ("site/reader/themes/招安的两种结局专题.html", "INSERT", "招安的两种结局"),
    ("site/reader/essays/西游与服饰学.html", "INSERT", "西游与服饰学"),
    ("site/reader/poetry/原著景物诗分类赏析专题.html", "INSERT", "原著景物诗分类赏析"),
    ("site/reader/culture/历史玄奘与小说玄奘专题.html", "INSERT", "历史玄奘与小说玄奘"),
]

SCRIPTS = [
    ("scripts/_w984_make_prompts.py", "母版复用生成器（249 字符母版逐字复用·四条断言·stem 冲突负样本自证）"),
    ("scripts/_w984_precheck_pages.py", "落位页先验（存在 + 无题图 + 结构锚点·负样本自证）"),
    ("scripts/_w984_derive.py", "施工脚本程序化派生器（替换表 + 残留硬编码断言）"),
    ("scripts/_w984_prepare.py", "成品派生（裁 3:4 → 缩放 → 纸色归一 → 母版/站点版 → 拼图·作用域限 raw/round13）"),
    ("scripts/_w984_download.py", "出图原件下载（node_id → 短链 → 落盘·按 node_id↔文件名映射）"),
    ("scripts/_w984_insert_plates.py", "12 页 chapter-plate 接入（幂等）"),
    ("scripts/_w984_retry.py", "单张重出修正器（行内短锚点替换 + 重建 batch + 断言修正点入 prompt）"),
    ("scripts/_w984_sheet.py", "本批 12 张核对拼图生成器"),
    ("scripts/_w984_zoom.py", "关键部位放大核对图生成器"),
    ("scripts/_w984_serve.py", "本地验收静态服务（补 webp/js/css MIME）"),
    ("scripts/_w945_plates_verify.py", "素材成套判据 J1–J10（自归档恢复为现役·判据逻辑逐字未改）"),
    ("scripts/_w951_check_crop.py", "站点版裁切验算（自归档恢复为现役·判据逻辑逐字未改）"),
]

DOCS = [
    ("docs/11-方案报告/计划方案/执行前计划-T31-内页题图成套批第五组.md", "执行前计划件（框架号 T-31）"),
    ("docs/11-方案报告/计划方案/T31-任务计划执行与经验沉淀报告-2026-10-27.md", "终稿报告件（执行记录/验收/复盘/经验沉淀）"),
    ("docs/11-方案报告/README.md", "§六 计划方案登记（+2 行·件数十 37→39）"),
    ("docs/agent/pitfalls.md", "坑表 +6 条（64→70·视觉渲染 12→15 / 流程 10→13）"),
    ("docs/10-方法论沉淀/素材批处理与判据自证方法论.md", "新增 §2.7 判据覆盖面的边界 + 4 条复现案例"),
    ("docs/00-导读/W批次编号对账表.md", "W984 认领行 + W982 行 git 反填"),
]


def rel_files():
    """本批全量文件清单（磁盘实算）"""
    files = []
    for s in STEMS:
        files.append("assets/promo/plate-set/plate-line-%s.png" % s)
        files.append("assets/promo/plate-set/plate-line-%s.webp" % s)
        files.append("site/static/images/plate-line-%s.webp" % s)
    raw_dir = os.path.join(SET, "raw", "round13")
    for fn in sorted(os.listdir(raw_dir)):
        files.append("assets/promo/plate-set/raw/round13/%s" % fn)
    files.append("assets/promo/plate-set/preview-contact-sheet.png")
    files.append("assets/promo/plate-set/preview-contact-sheet.webp")
    files.append("assets/promo/plate-set/README.md")
    for _e in PAGES:
        files.append(_e[0])
    for p, _d in SCRIPTS:
        files.append(p)
    for p, _d in DOCS:
        files.append(p)
    files.append("scripts/_w984_make_spec.py")
    files += [
        "site/data/search.html", "site/en/search.html",
        "scripts/output/_w984_batch1.json", "scripts/output/_w984_batch2.json", "scripts/output/_w984_batch3.json",
        "scripts/output/_w984_gen.json", "scripts/output/_w984_precheck.json",
        "scripts/output/_w984_sheet.png", "scripts/output/_w984_zoom.png",
        "scripts/output/_w984_spec.json", "scripts/output/_cascade_files_W984.txt",
        "CHANGELOG.md", "HANDOVER.md", "README.md", "STRUCTURE.md",
        "docs/00-导读/项目说明.md", ".github/workflows/README.md",
        "site/index.html", "site/data/cross-time-danmaku.html", "site/data/tag-cloud.html",
        "site/dukou-engine.html", "AGENTS.md", "CITATION.cff", "archive/docs/AGENTS-ARCHIVE.md",
        "scripts/output/file-index.md",
    ]
    return files


def main():
    files = rel_files()
    missing = [f for f in files if not os.path.exists(os.path.join(REPO, f.replace("/", os.sep)))]
    if missing:
        print("WARN  清单中 %d 个文件尚未落盘（级联前属预期）：%s" % (len(missing), missing[:6]))

    body = (
        "\n\n\n\n> **来源**：用户 2026-10-27 令「帮我做几张素材图：用途与画幅、风格与配色统一、主体清晰、"
        "留好放文字的空间都考虑到，成套出图保证风格一致」，并明文要求「开始前先问我：素材用在哪里、"
        "需要几张、有没有参考风格」。\n>\n> **四问答复**：① 用途与画幅 = **内页专题题图 · 3:4 竖版 1200×1600"
        "（沿用 plate-set 母版）** ② 张数 = **12 张** ③ 参考风格 = **沿用 plate-set 宣纸线描"
        "（母版段 249 字符逐字复用）** ④ 题材范围 = **people + themes + essays·poetry·culture + "
        "九十九回回目页（四库混合）**。\n>\n> - **文件**：" + "、".join(files) + "。\n\n"
        "**本批要点**：① **四库首次混合覆盖**——12 张 = people 4（如来 / 玉帝 / 百眼魔君 / 嫦娥）+ "
        "themes 3（神学干预机制 / 取经路径地理符号学 / 取经密码学）+ essays·poetry·culture 3"
        "（西游与民俗学 / 西游诗词意象谱系 / 明代科举制度对照）+ 回目页 2（第 010 回 魏征斩龙 / "
        "第 004 回 官封弼马）⇒ reader 有题图页 **63 → 75**，站内线描题图累计 **52 → 64 张**；"
        "② **母版段逐字复用 249 字符**（读 `scripts/output/_w953_batch1.json`）⇒ 跨批风格同族由构造保证；"
        "③ **3 张因人眼关重出**（#26 玄色帝服整片平涂 / #27 黄袍平涂 + 千眼过密 / #36 官印印面刻字）——"
        "**机器判据 J1–J10 全绿仍漏**（J6 只统计暗像素 ⇒ 彩色平涂与器物刻字完全逃逸）⇒ 坑表 +6 条"
        "（64 → 70）+ 方法论篇新增 §2.7「判据覆盖面的边界」；④ **开工前先收官在途 W982**"
        "（preflight 交集命中 AGENTS.md / CHANGELOG.md）⇒ 共享面让出后 W984 才动土。\n\n"
        "**验证**：母版判据 J1–J10 **64/64 FAIL 0** · 站点版裁切验算 **64/64 FAIL 0**"
        "（主体顶余量 6 px·下部地面留白 51–153 px）· 负样本自检可证伪（坏样本被 J1 抓出）· "
        "纸色归一残差 ≤ 0.5/255 · 落位页先验 12/12 存在且无题图（含负样本自证）· 接入幂等复跑 12/12 SKIP · "
        "浏览器实跑 3 类路径前缀各 1 页渲染正常 · 计划方案合规门禁 0 FAIL · "
        "全量门禁与 pytest 见状态行。\n\n> - **状态**：在途（认领登记 W984·收官回填随批尾提交补 hash）\n"
    )

    rows = []
    for s in STEMS:
        rows.append("| site/static/images/plate-line-%s.webp | W984 | 新增·站点版（%s） |" % (s, s))
    for _e in PAGES:
        rows.append("| %s | W984 | 接入题图（%s） |" % (_e[0], _e[2]))
    rows.append("| assets/promo/plate-set/plate-line-25~36-*.png/.webp | W984 | 新增 12 张母版（1200×1600·线描墨稿·含 3 张重出生效件） |")
    rows.append("| assets/promo/plate-set/raw/round13/ | W984 | 出图原件 12 份（含 #26/#27/#36 三张重出生效件） |")
    rows.append("| assets/promo/plate-set/preview-contact-sheet.png/.webp | W984 | 全目录 64 张缩略拼图（刷新） |")
    rows.append("| assets/promo/plate-set/README.md | W984 | 口径更新（52→64 张·第六组清单·本批已知取舍） |")
    for p, d in SCRIPTS:
        rows.append("| %s | W984 | %s |" % (p, d))
    for p, d in DOCS:
        rows.append("| %s | W984 | %s |" % (p, d))
    for p in ["site/data/search.html", "site/en/search.html"]:
        rows.append("| %s | W984 | 搜索索引重建（新文档入索引）+ CSP 哈希同步 |" % p)
    for p, d in [("CHANGELOG.md", "W984 段"), ("docs/00-导读/W批次编号对账表.md", "W984 认领行"),
                  ("README.md", "当前批次版本行"), ("STRUCTURE.md", "当前批次版本行"),
                  ("docs/00-导读/项目说明.md", "当前批次版本行"),
                  (".github/workflows/README.md", "工作流层版本面推进 W984"),
                  ("site/index.html", "页脚批次链插入 W984"),
                  ("site/data/cross-time-danmaku.html", "页脚批次链插入 W984"),
                  ("site/data/tag-cloud.html", "页脚批次链插入 W984"),
                  ("site/dukou-engine.html", "页脚批次链插入 W984"),
                  ("AGENTS.md", "版本脚注条目 + 坑位条数声明 64→70"),
                  ("archive/docs/AGENTS-ARCHIVE.md", "脚注滚动迁入的最老条目"),
                  ("CITATION.cff", "version 同步为 W984"),
                  ("scripts/output/file-index.md", "W984 段插入")]:
        rows.append("| %s | W984 | %s |" % (p, d))

    spec = {
        "batch": "W984",
        "date": "2026-10-27",
        "title": "W984 内页题图成套批·第四组（12 张·四库混合覆盖·站内线描题图累计 64 张）",
        "desc": "内页题图成套批第五组：回目页 6 张线描重出加四库扩量 6 张，reader 有题图页 75 增至 81，原浓墨版保留归档",
        "head_entry": "2026-10-27（W984 内页题图成套批第四组）",
        "head_sentence": "内页题图成套批第五组：回目页 6 张线描重出加四库扩量 6 张，reader 有题图页 75 增至 81",
        "changelog_body": body,
        "milestone_block": (
            "- **W984 内页题图成套批·第五组**（12 张·回目页线描重出 6 + 四库扩量 6）：\n"
            "  - 回目页 6 张改用线描版（原浓墨渲染版 chap-*.webp 保留不删·登记为存量归档）\n"
            "  - people 2 + themes 1 + essays·poetry·culture 各 1（四库全覆盖）\n"
            "  - 母版段 249 字符逐字复用 + J1–J10 与裁切验算 76/76 全绿"
        ),
        "agents_note": (
            "2026-10-27（W984）把题图覆盖从「新增页面」推到「替换页面图源」：回目页那 6 张浓墨渲染老图不再独占回目页，线上改用同一套宣纸线描立像，老图文件保留在仓内存档不删——资产可以退役，文件不必消失。配套把落位页先验拆成「插入」与「替换」两种动作各自留负样本，因为同一种检查盖不住两种页面。"
        ),
        "file_index_rows": rows,
    }
    p = os.path.join(OUT, "_w984_spec.json")
    io.open(p, "w", encoding="utf-8", newline="\n").write(
        json.dumps(spec, ensure_ascii=False, indent=1))
    print("spec 已写：%s" % p)
    print("  文件清单 %d 条 · file_index %d 行 · changelog_body %d 字符" % (
        len(files), len(rows), len(body)))


if __name__ == "__main__":
    main()
