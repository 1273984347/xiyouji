# -*- coding: utf-8 -*-
"""_w984_derive.py — 从 W983 脚本**程序化派生** W984 施工脚本（替换表 + 残留硬编码断言）

纪律（W952 教训机制化）：派生产物源码里若仍出现源批次号 / 源轮次目录 / 源 stem 段，
立即中止（fail-closed），不产出文件。

派生 5 件：
  _w983_prepare.py  → _w984_prepare.py   （成品派生·作用域 raw/round13）
  _w983_download.py → _w984_download.py  （node_id → 原件下载）
  _w983_sheet.py    → _w984_sheet.py     （本批 12 张核对拼图）
  _w983_zoom.py     → _w984_zoom.py      （关键部位放大核对图）
  _w983_make_spec.py→ _w984_make_spec.py （级联 spec 生成·清单从磁盘实算）

用法：py -3 scripts/_w984_derive.py [--dry-run]
"""
import io
import os
import re
import sys

REPO = r"D:\xiyouji"
SCRIPTS = os.path.join(REPO, "scripts")

STEMS_NEW = '''STEMS = ["37-ch007-bagua-lu", "38-ch014-liubei", "39-ch015-yingchou", "40-ch023-sichan",
         "41-ch027-bailong", "42-ch030-sancha", "43-luoshanv", "44-kuimulang",
         "45-zhaoan-topic", "46-fushi-topic", "47-jingwu-topic", "48-xuanzang-topic"]'''

# ⚠️ 块边界正则必须以 `]\n` 收尾（不能用 `^\]$`）：
#    STEMS 是**单行列表**（行尾是 `"]`），`^\]$` 匹配不到 ⇒ 正则会跨块把 PAGES 一并吞掉（W984 实测）。
STEMS_OLD_RE = re.compile(r"^STEMS = \[.*?\]\n", re.S | re.M)

PAGES_NEW = '''PAGES = [
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
]'''

PAGES_OLD_RE = re.compile(r"^PAGES = \[.*?\]\n", re.S | re.M)


def read(name):
    return io.open(os.path.join(SCRIPTS, name), encoding="utf-8", newline="").read()


def common(txt):
    for a, b in [("_w983_", "_w984_"), ("w983", "w984"), ("W983", "W984"),
                 ("round12", "round13"), ("_w983_", "_w984_")]:
        txt = txt.replace(a, b)
    return txt


def derive_prepare():
    t = common(read("_w983_prepare.py"))
    t = t.replace("既有 52 张母版与站点版零改动", "既有 64 张母版与站点版零改动")
    t = t.replace("既有 52 + 本批 12", "既有 64 + 本批 12")
    t = t.replace("全目录 64 张", "全目录 76 张")
    t = t.replace("既有 52 张不重写", "既有 64 张不重写")
    return t


def derive_download():
    return common(read("_w983_download.py"))


def derive_sheet():
    t = common(read("_w983_sheet.py"))
    t = STEMS_OLD_RE.sub(STEMS_NEW, t)
    t = t.replace('_w983_sheet.png', '_w984_sheet.png')
    t = t.replace('scripts", "output", "_w984_sheet.png"', 'scripts", "output", "_w984_sheet.png"')
    return t


def derive_zoom():
    t = common(read("_w983_zoom.py"))
    # ITEMS 整块替换为本批特写项
    items = '''ITEMS = [
    ("37-ch007-bagua-lu", (300, 700, 900, 1300), "37 第 007 回·八卦炉与铁链特写"),
    ("45-zhaoan-topic", (500, 700, 1050, 1250), "45 招安·诏书与官印特写（查是否刻字）"),
]'''
    t = re.sub(r"^ITEMS = \[.*?^\]$", items, t, flags=re.S | re.M)
    return t


def derive_spec():
    t = common(read("_w983_make_spec.py"))
    t = STEMS_OLD_RE.sub(lambda m: STEMS_NEW + "\n", t)
    t = PAGES_OLD_RE.sub(lambda m: PAGES_NEW + "\n", t)
    # PAGES 在本批是三元组（页面, 动作, 题材）⇒ 同步修正两处解包
    t = t.replace("    for p, _d in PAGES:\n        files.append(p)",
                  "    for _e in PAGES:\n        files.append(_e[0])")
    t = t.replace('    for p, d in PAGES:\n        rows.append("| %s | W984 | 接入题图（%s） |" % (p, d))',
                  '    for _e in PAGES:\n'
                  '        rows.append("| %s | W984 | 接入题图（%s） |" % (_e[0], _e[2]))')
    # 文件清单：raw 目录 + 输出物前缀
    t = t.replace('"assets/promo/plate-set/raw/round12/%s" % fn', '"assets/promo/plate-set/raw/round13/%s" % fn')
    t = t.replace('os.path.join(SET, "raw", "round12")', 'os.path.join(SET, "raw", "round13")')
    t = t.replace('"scripts/output/_w983_', '"scripts/output/_w984_')
    t = t.replace('"scripts/_w983_make_spec.py"', '"scripts/_w984_make_spec.py"')
    t = t.replace('"scripts/_w983_prepare.py"', '"scripts/_w984_prepare.py"')
    t = t.replace('"scripts/_w983_download.py"', '"scripts/_w984_download.py"')
    t = t.replace('"scripts/_w983_insert_plates.py"', '"scripts/_w984_insert_plates.py"')
    t = t.replace('"scripts/_w983_make_prompts.py"', '"scripts/_w984_make_prompts.py"')
    t = t.replace('"scripts/_w983_sheet.py"', '"scripts/_w984_sheet.py"')
    t = t.replace('"scripts/_w983_zoom.py"', '"scripts/_w984_zoom.py"')
    t = t.replace('"scripts/_w983_retry.py"', '"scripts/_w984_retry.py"')
    # 计划件/报告件路径
    t = t.replace('"docs/11-方案报告/计划方案/执行前计划-T30-内页题图成套批第四组.md", "执行前计划件（框架号 T-30）"',
                  '"docs/11-方案报告/计划方案/执行前计划-T31-内页题图成套批第五组.md", "执行前计划件（框架号 T-31）"')
    t = t.replace('"docs/11-方案报告/计划方案/T30-任务计划执行与经验沉淀报告-2026-10-27.md", "终稿报告件（执行记录/验收/复盘/经验沉淀）"',
                  '"docs/11-方案报告/计划方案/T31-任务计划执行与经验沉淀报告-2026-10-27.md", "终稿报告件（执行记录/验收/复盘/经验沉淀）"')
    # 标题与描述
    t = t.replace('"title": "W983 内页题图成套批·第四组（12 张·四库混合覆盖·站内线描题图累计 64 张）"',
                  '"title": "W984 内页题图成套批·第五组（12 张·回目页线描重出 6 + 四库扩量 6·站内线描题图累计 76 张）"')
    t = t.replace('"desc": "内页题图成套批第四组：四库混合覆盖 12 张，reader 有题图页 63 增至 75，3 张因人眼关重出（判据盲区实证）"',
                  '"desc": "内页题图成套批第五组：回目页 6 张线描重出加四库扩量 6 张，reader 有题图页 75 增至 81，原浓墨版保留归档"')
    t = t.replace('"head_entry": "2026-10-27（W983 内页题图成套批第四组）"',
                  '"head_entry": "2026-10-27（W984 内页题图成套批第五组）"')
    t = t.replace('"head_sentence": "内页题图成套批第四组：12 张四库混合覆盖，reader 有题图页 63 增至 75"',
                  '"head_sentence": "内页题图成套批第五组：回目页 6 张线描重出加四库扩量 6 张，reader 有题图页 75 增至 81"')
    # milestone / agents_note / changelog_body 的文字块整体替换
    # ⚠️ 用 lambda 包裹替换值：re.sub 的「字符串模板」形式会把模板里的 \n 解释成真换行
    #    （W984 实测：派生产物直接语法错）⇒ lambda 形式不做转义解释。
    t = re.sub(r'"milestone_block": \(.*?\),\n        "agents_note"',
               lambda m: ('"milestone_block": (\n'
               '            "- **W984 内页题图成套批·第五组**（12 张·回目页线描重出 6 + 四库扩量 6）：\\n"\n'
               '            "  - 回目页 6 张改用线描版（原浓墨渲染版 chap-*.webp 保留不删·登记为存量归档）\\n"\n'
               '            "  - people 2 + themes 1 + essays·poetry·culture 各 1（四库全覆盖）\\n"\n'
               '            "  - 母版段 249 字符逐字复用 + J1–J10 与裁切验算 76/76 全绿"\n'
               '        ),\n        "agents_note"'), t, flags=re.S)
    t = re.sub(r'"agents_note": \(.*?\),\n        "file_index_rows"',
               lambda m: ('"agents_note": (\n'
               '            "2026-10-27（W984）把题图覆盖从「新增页面」推到「替换页面图源」：回目页那 6 张浓墨渲染老图不再独占回目页，'
               '线上改用同一套宣纸线描立像，老图文件保留在仓内存档不删——资产可以退役，文件不必消失。'
               '配套把落位页先验拆成「插入」与「替换」两种动作各自留负样本，因为同一种检查盖不住两种页面。"\n'
               '        ),\n        "file_index_rows"'), t, flags=re.S)
    return t


FORBIDDEN = {
    "_w984_prepare.py": ["w983", "W983", "round12"],
    "_w984_download.py": ["w983", "W983", "round12"],
    "_w984_sheet.py": ["w983", "W983", "round12"],
    "_w984_zoom.py": ["w983", "W983", "round12"],
    "_w984_make_spec.py": ["w983", "W983", "round12"],
}


def main() -> int:
    dry = "--dry-run" in sys.argv
    jobs = [
        ("_w984_prepare.py", derive_prepare()),
        ("_w984_download.py", derive_download()),
        ("_w984_sheet.py", derive_sheet()),
        ("_w984_zoom.py", derive_zoom()),
        ("_w984_make_spec.py", derive_spec()),
    ]
    ok = True
    for name, txt in jobs:
        bad = [b for b in FORBIDDEN[name] if b in txt]
        if bad:
            print("ABORT  %s 残留源批次硬编码 %s ⇒ 漏改·不产出" % (name, bad))
            ok = False
            continue
        if dry:
            print("DRY-RUN  %s（%d 字符）" % (name, len(txt)))
            continue
        io.open(os.path.join(SCRIPTS, name), "w", encoding="utf-8", newline="\n").write(txt)
        print("写出 %s（%d 字符）" % (name, len(txt)))
    if not ok:
        return 2
    print("\n派生完成：%d 件（残留硬编码断言全过）" % len(jobs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
