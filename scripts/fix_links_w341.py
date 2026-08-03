#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_links_w341.py — W341 死链巡检·机械修复（零依赖）

仅修复"低风险、目标文件确实存在"的断链：
  1. 章节导航用了被截断的回目文件名（补全为全名）
  2. site/data 页面裸 href="dashboard.html" -> ../dashboard.html
  3. docs 跨目录专题链接路径/文件名差一字（目标存在）
  4. S2 学术投稿候选误引 10-方法论沉淀 文件（改名类）
  5. S3 相对路径 off-by-one（../CHANGELOG / ../site/data）
  6. CHANGELOG-ARCHIVE / file-index-archive 归档路径修正 + 移除已删示例链接
  7. 移除 .trae-cn 外部引用占位链接 / 修正 scripts/README 示例误报

不动（留给用户判断）：
  - docs 深化专题引用已重组的 source/原文/*.txt（~44 处，需映射新位置或删除）
  - 引用了根本不存在的专题文件（权力五联对照 / 妖怪身份政治 / 西游与三教合一 / 西游与弗洛伊德·荣格·拉康精神分析 等）
  - site/_template.html（模板相对路径问题，待核对生成逻辑）
  - .github/workflows/README.md 引用不存在的 deploy.yml（陈旧，跳过）
  - scripts/node_modules 第三方依赖（忽略）

用法：
    python scripts/fix_links_w341.py            # 执行修复并打印变更摘要
    python scripts/fix_links_w341.py --dry-run  # 只报告，不写文件
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 每个文件对应的 (old, new)；第三元素为 'regex' 表示正则替换
EDITS = [
    # ---- 1. 章节导航截断回目名 -> 全名 ----
    ("docs/01-全书逐回解读/第017回-孙行者大闹黑风山.md", [
        ("第019回-云栈洞悟空收八戒.md", "第019回-云栈洞悟空收八戒浮屠山玄奘受心经.md")]),
    ("docs/01-全书逐回解读/第018回-观音院唐僧脱难高老庄行者降魔.md", [
        ("第019回-云栈洞悟空收八戒.md", "第019回-云栈洞悟空收八戒浮屠山玄奘受心经.md")]),
    ("docs/01-全书逐回解读/第022回-八戒大战流沙河.md", [
        ("第019回-云栈洞悟空收八戒.md", "第019回-云栈洞悟空收八戒浮屠山玄奘受心经.md")]),
    ("docs/01-全书逐回解读/第028回-花果山群妖聚义.md", [
        ("第031回-猪八戒义激猴王.md", "第031回-猪八戒义激猴王孙行者智降妖怪.md")]),
    ("docs/01-全书逐回解读/第029回-脱难江流来国土承恩八戒转山林.md", [
        ("第031回-猪八戒义激猴王.md", "第031回-猪八戒义激猴王孙行者智降妖怪.md")]),
    ("docs/01-全书逐回解读/第030回-邪魔侵正法意马忆心猿.md", [
        ("第031回-猪八戒义激猴王.md", "第031回-猪八戒义激猴王孙行者智降妖怪.md")]),
    ("docs/01-全书逐回解读/第032回-平顶山功曹传信.md", [
        ("第031回-猪八戒义激猴王.md", "第031回-猪八戒义激猴王孙行者智降妖怪.md")]),
    ("docs/01-全书逐回解读/第041回-心猿遭火败木母被魔擒.md", [
        ("第042回-大圣殷勤拜南海.md", "第042回-大圣殷勤拜南海观音慈善缚红孩.md")]),
    ("docs/01-全书逐回解读/第045回-三清观大圣留名.md", [
        ("第042回-大圣殷勤拜南海.md", "第042回-大圣殷勤拜南海观音慈善缚红孩.md")]),

    # ---- 2. site/data 裸 dashboard.html -> ../dashboard.html ----
    ("site/data/chapter-structure-graph.html", [(r'href="dashboard\.html"', 'href="../dashboard.html', "regex")]),
    ("site/data/character-relationship-3d.html", [(r'href="dashboard\.html"', 'href="../dashboard.html', "regex")]),
    ("site/data/journey-map-interactive.html", [(r'href="dashboard\.html"', 'href="../dashboard.html', "regex")]),
    ("site/data/language-style-radar.html", [(r'href="dashboard\.html"', 'href="../dashboard.html', "regex")]),
    ("site/data/narrative-rhythm-curve.html", [(r'href="dashboard\.html"', 'href="../dashboard.html', "regex")]),

    # ---- 3. docs 跨目录专题链接（路径/文件名差一字，目标存在）----
    ("docs/03-主题与情节专题/取经美学专题.md", [
        ("声音政治学专题.md", "取经声音政治学专题.md"),
        ("媒介考古学专题.md", "取经媒介考古学专题.md")]),
    ("docs/04-文化与历史背景/明代宗教制度对照专题.md", [
        ("明代司法制度深化对照专题.md", "明代司法制度深化专题.md")]),
    ("docs/04-文化与历史背景/明代科举制度对照专题.md", [
        ("明代司法制度深化对照专题.md", "明代司法制度深化专题.md")]),
    ("docs/03-主题与情节专题/西游与政治思想史专题.md", [
        ("明代思想史对照专题.md", "../04-文化与历史背景/明代思想史对照专题.md")]),

    # ---- 4. S2 学术投稿候选误引 10-方法论沉淀（路径错 + 改名）----
    # 仅替换链接目标部分，保留链接文字
    ("docs/S2-学术投稿/学术投稿候选-中国文论视角下的西游记多维解读.md", [
        (r'\]\(DRL真循环\.md\)', '](../10-方法论沉淀/DRL真循环.md)', "regex"),
        (r'\]\(三skill闭环\.md\)', '](../10-方法论沉淀/三skill闭环.md)', "regex"),
        (r'\]\(E1铁律\.md\)', '](../10-方法论沉淀/E1铁律.md)', "regex"),
        (r'\]\(双索引可追溯\.md\)', '](../10-方法论沉淀/双索引可追溯改造.md)', "regex"),
        (r'\]\(Preflight三轨验证\.md\)', '](../10-方法论沉淀/Preflight与Subagent模板.md)', "regex")]),
    ("docs/S2-学术投稿/学术投稿候选-西游记叙事学多维解读方法论.md", [
        (r'\]\(DRL真循环\.md\)', '](../10-方法论沉淀/DRL真循环.md)', "regex"),
        (r'\]\(三skill闭环\.md\)', '](../10-方法论沉淀/三skill闭环.md)', "regex"),
        (r'\]\(E1铁律\.md\)', '](../10-方法论沉淀/E1铁律.md)', "regex"),
        (r'\]\(双索引可追溯\.md\)', '](../10-方法论沉淀/双索引可追溯改造.md)', "regex"),
        (r'\]\(Preflight三轨验证\.md\)', '](../10-方法论沉淀/Preflight与Subagent模板.md)', "regex")]),

    # ---- 5. S2/S3 相对路径 off-by-one ----
    ("docs/S2-外部分享/S2-发布-西游与团队动力学心理学.md", [
        ("../site/data/pilgrim-team-dynamic-network.html", "../../site/data/pilgrim-team-dynamic-network.html")]),
    ("docs/S3-方法论外部分享/W302-S3-发布-双索引可追溯改造.md", [
        ("../CHANGELOG.md", "../../CHANGELOG.md")]),

    # ---- 6. CHANGELOG-ARCHIVE 归档路径修正 + 移除已删示例链接 ----
    ("CHANGELOG-ARCHIVE.md", [
        ("../../../source/引用与网络解读/学术论文索引.md", "source/引用与网络解读/学术论文索引.md"),
        ("版本演变.md", "docs/04-文化与历史背景/版本演变.md"),
        ("../06-个人随笔/西游与经济学.md", "docs/06-个人随笔/西游与经济学.md"),
        ("[source/原文/示例-两回.txt](source/原文/示例-两回.txt)", "source/原文/示例-两回.txt")]),

    # ---- 6b. file-index-archive 归档路径修正 ----
    ("scripts/output/file-index-archive.md", [
        ("取经团队动力学.md", "../../docs/03-主题与情节专题/取经团队动力学.md"),
        ("妖魔谱系政治学专题.md", "../../docs/03-主题与情节专题/妖魔谱系政治学专题.md"),
        ("取经路线社会学研究专题.md", "../../docs/03-主题与情节专题/取经路线社会学研究专题.md"),
        ("版本演变.md", "../../docs/04-文化与历史背景/版本演变.md")]),

    # ---- 7. .trae-cn 外部引用占位 / scripts/README 示例误报 ----
    ("docs/10-方法论沉淀/README.md", [
        ("[user_profile](../../../.trae-cn/memory/user_profile.md)", "user_profile")]),
    ("scripts/README.md", [
        ("Markdown [text](url)", "Markdown `[text](url)`")]),
]


def main():
    dry = "--dry-run" in sys.argv
    total_changed = 0
    total_links = 0
    for rel, pairs in EDITS:
        p = ROOT / rel
        if not p.exists():
            print(f"[SKIP] 文件不存在: {rel}")
            continue
        text = p.read_text(encoding="utf-8")
        new_text = text
        file_changes = 0
        for item in pairs:
            old, new = item[0], item[1]
            is_regex = len(item) > 2 and item[2] == "regex"
            if is_regex:
                count = len(re.findall(old, new_text))
                if count:
                    new_text = re.sub(old, new, new_text)
            else:
                count = new_text.count(old)
                if count:
                    new_text = new_text.replace(old, new)
            if count:
                file_changes += count
                total_links += count
                print(f"  {rel}: [{old[:30]}] -> [{new[:30]}]  x{count}")
        if file_changes and not dry:
            p.write_text(new_text, encoding="utf-8")
            total_changed += 1
        if file_changes:
            print(f"[{'DRY' if dry else 'FIX'}] {rel}: {file_changes} 处")
    print("-" * 60)
    print(f"改动文件: {total_changed}  修复链接: {total_links}" + ("  (dry-run)" if dry else ""))


if __name__ == "__main__":
    main()
