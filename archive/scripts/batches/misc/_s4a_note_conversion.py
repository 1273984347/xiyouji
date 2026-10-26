#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""_s4a_note_conversion.py — A 轨论文「方案 A」体例改造（一次性·断言式·双稿）

依据：用户裁决（2026-10-06）——①按方案 A 执行体例改造；②专著页码「尽量核补·余留终校」
（公开渠道未核得页码，四个专著注暂不注页码，终校清单见文末 NOTE）；③摘要/关键词同批调整。

改造成果：
- 正文引证全注释化：①—⑰（含合并注号 ①⑩⑬ / ②⑭ / ③⑯ / ④⑮⑰；注号置于句末标点之后）
- 撤「参考文献」节 → 新建「注释」节（文末·圈号·手工字符）
- 摘要 397 字 → ≤300；关键词 6→5（中英同步）；§2.4/§5.3 正文圈号枚举改「第一/其一」防与注号冲突
- 四条正文无引证点的条目（[1]黄肃秋本/[8]浦安迪/[9]刘荫柏/[10]李天飞本）随参考文献表撤除（执行记录登记）

备份：两稿先备份至 tmpe/a_note_bak_20261006/；全量断言通过后才写回。
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(r"d:\xiyouji")
MAIN = ROOT / "docs/S4-学术投稿/01-论文/明清小说方向-投稿版.md"
ANON = ROOT / "docs/S4-学术投稿/01-论文/明清小说方向-匿名稿.md"
BAK = ROOT / "tmpe/a_note_bak_20261006"

NEW_ABSTRACT = """《西游记》中"通关文牒"贯穿取经全程：自长安发牒至灵山缴牒、历十余国倒换关文。本文以数字人文方法重构这一驿递叙事：依托锚点体系与引文机器校验，构建涵盖 30 处驿传节点的数据集（关文节点、馆驿流程节点各 15 处），将驿递书写的空间分布、状态类型与回目密度转化为可量化检验的结构。研究表明：其一，通关文牒叙事遵循明代驿递制度"勘合—验引—放行"的程序语法，是制度书写的文学转写；其二，15 处涉关文地点呈"验讫为主、未验与波折为辅"的类型学分布，未验地点恰是制度失序的神话显影；其三，量化结果与制度史研究（杨正泰、黄仁宇、布罗代尔、魏丕信）形成互证，为古典小说制度书写研究提供可复核的方法路径。"""

NEW_NOTES = """## 注释

①⑩⑬杨正泰：《明代驿站考：附〈寰宇通衢〉〈一统路程图记〉〈士商类要〉》（增订本），上海：上海古籍出版社，2006年。

②⑭［美］黄仁宇：《十六世纪明代中国之财政与税收》，阿风等译，北京：生活·读书·新知三联书店，2001年。

③⑯［法］布罗代尔：《地中海与菲利普二世时代的地中海世界》，唐家龙等译，北京：商务印书馆，1996年。

④⑮⑰［法］魏丕信：《十八世纪中国的官僚制度与荒政》，徐建青译，南京：江苏人民出版社，2003年。

⑤Ping Y, Wang B. Retranslated Chinese classical canon *Journey to the West*: a stylometric comparison between Julia Lovell's retranslation and Arthur Waley's translation[J]. *Digital Scholarship in the Humanities*, 2024, 39(1): 308-320.

⑥Zeng J, Qiu T, Shan L. Assessing reader reception of Arthur Waley's English translation of *Journey to the West*: A topic modeling and sentiment analysis approach[J]. *PLOS ONE*, 2026, 21(6): e0351327.

⑦Jia N, Xin J, Wang Y. Overseas reception of English translations of *Journey to the West*: Temporal dynamics, cross-platform sentiment patterns, and topic modeling[J]. *PLOS ONE*, 2026, 21(4): e0347253.

⑧刘道影、朱明胜：《西游记翻译研究（1980—2018）——基于 CiteSpace 的可视化分析》，《外国语言与文化》2019年第1期。

⑨龙光海：《运河文化与〈西游记〉的书写》，《明清小说研究》2023年第4期。

⑪刘文鹏主持国家社会科学基金重大项目「清代驿站史研究」（项目批准号：19ZDA207）。

⑫本文所引《西游记》原文，均据金陵世德堂本《新刻出像官板大字西游记》（明万历二十年刊本）之电子文本，回次依原刊；引文后以「第N回 line X」标注行号（按底本换行切分、自 1 起计），可经公开语料与脚本复核。
"""

# 公共替换（主稿/匿名稿同文同改；短锚点·各断言恰 1 次）
COMMON: list[tuple[str, str]] = [
    ("制度背景。黄仁宇《十六世纪明代中国之财政与税收》", "制度背景。①黄仁宇《十六世纪明代中国之财政与税收》"),
    ("缩影。布罗代尔《地中海》", "缩影。②布罗代尔《地中海》"),
    ("节奏。魏丕信《十八世纪中国的官僚制度与荒政》", "节奏。③魏丕信《十八世纪中国的官僚制度与荒政》"),
    ("国家治理能力的标尺。", "国家治理能力的标尺。④"),
    ("实证。读者层面是接受计量", "实证。⑤读者层面是接受计量"),
    ("读者接受，Jia 等则在", "读者接受。⑥Jia 等则在"),
    ("阅读一侧。文献层面是版图勾勒", "阅读一侧。⑦文献层面是版图勾勒"),
    ("议题结构的变迁。这一图景的启示", "议题结构的变迁。⑧这一图景的启示"),
    ("空间底座；「交通线路与明清小说书写」", "空间底座。⑨「交通线路与明清小说书写」"),
    ("日常运作；刘文鹏主持的", "日常运作。⑩刘文鹏主持的"),
    ("纳入国家治理框架。", "纳入国家治理框架。⑪"),
    ("简化为各国都城驿所。", "简化为各国都城驿所。⑬"),
    ("勘合分等级、按身份支应。通关文牒在小说中", "勘合分等级、按身份支应。⑭通关文牒在小说中"),
    ("亦是信息上行下行的驿传节点。若按布罗代尔", "亦是信息上行下行的驿传节点。⑮若按布罗代尔"),
    ("不曾脱管。", "不曾脱管。⑯"),
    ("如何权衡言说的风险。", "如何权衡言说的风险。⑰"),
    ("问题：①通关文牒叙事", "问题：第一，通关文牒叙事"),
    ("？②其状态类型", "？第二，其状态类型"),
    ("？③量化结果能否", "？第三，量化结果能否"),
    ("形成了三重互证：①关文", "形成了三重互证：其一，关文"),
    ("验讫者；②", "验讫者；其二，"),
    ("一致；③未验地点的分布", "一致；其三，未验地点的分布"),
    ("依存关系；④凤仙郡一节", "依存关系。此外，凤仙郡一节"),
    ("通关文牒；数字人文；line 号锚点；量化叙事", "通关文牒；数字人文；line 号锚点"),
    ("digital humanities; line-level citation; quantitative narrative", "digital humanities; line-level citation"),
]

MAIN_ONLY: list[tuple[str, str]] = [
    (
        "> 投稿目标：文学遗产 / 明清小说研究 / 数字人文（清华大学主办）",
        "> 投稿目标：文学遗产 / 明清小说研究 / 数字人文（清华大学主办）\n"
        "> 体例改造（2026-10-06）：按《明清小说研究》官方体例执行——正文引证全注释化（①—⑰·含合并注号·注号置句末标点后）、"
        "撤「参考文献」节改建文末「注释」；摘要压缩、关键词 6→5 同批；页码待终校项见执行记录",
    ),
]

ANON_ONLY: list[tuple[str, str]] = [
    ("第三方独立复核。在此之上还设有机器校验层", "第三方独立复核。⑫在此之上还设有机器校验层"),
]

MAIN_12 = [("脚本独立验证。在此之上还设有机器校验层", "脚本独立验证。⑫在此之上还设有机器校验层")]

REF_SECTION_RE = re.compile(
    r"## 参考文献\n\n\[1\] 吴承恩\. 西游记\[M\]\. 黄肃秋, 校注\. 北京: 人民文学出版社, 1980\.\n\n"
    r"\[2\].*?\[10\] 吴承恩\. 西游记\[M\]\. 李天飞, 校注\. 北京: 中华书局, 2014\.",
    re.S,
)


def extract_abstract(text: str) -> str:
    m = re.search(r"## 摘要\n\n(.*?)\n\n\*\*关键词\*\*", text, re.S)
    assert m, "abstract block not found"
    return m.group(1)


def apply_pairs(text: str, pairs: list[tuple[str, str]], label: str, problems: list[str]) -> str:
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            problems.append(f"[{label}] anchor count={n} (expect 1): {old[:48]}…")
            continue
        text = text.replace(old, new)
    return text


def convert(path: Path, label: str, problems: list[str], is_main: bool) -> str | None:
    text = path.read_text(encoding="utf-8")

    # 摘要（全文同文替换 + 长度预警）
    old_abs = extract_abstract(text)
    text = text.replace(old_abs, NEW_ABSTRACT)
    abs_len = len(re.sub(r"\s", "", NEW_ABSTRACT))
    flag = "OK" if 200 <= abs_len <= 300 else "WARN"
    print(f"[{label}] 新摘要 {abs_len} 字（{flag}）")

    # 公共替换 + 本文专属
    text = apply_pairs(text, COMMON, label, problems)
    text = apply_pairs(text, MAIN_12, label, problems) if is_main else apply_pairs(text, ANON_ONLY, label, problems)
    if is_main:
        text = apply_pairs(text, MAIN_ONLY, label, problems)

    # 参考文献 → 注释
    m = REF_SECTION_RE.search(text)
    if not m:
        problems.append(f"[{label}] 参考文献节未匹配")
    else:
        text = text[: m.start()] + NEW_NOTES.rstrip("\n") + text[m.end():]

    # 事后校验
    checks = {
        "残留「## 参考文献」": text.count("## 参考文献"),
        "注释节": text.count("## 注释"),
        "圈号①": text.count("①"), "圈号⑫": text.count("⑫"), "圈号⑰": text.count("⑰"),
    }
    print(f"[{label}] " + " · ".join(f"{k}={v}" for k, v in checks.items()))
    if checks["残留「## 参考文献」"] != 0 or checks["注释节"] != 1:
        problems.append(f"[{label}] 注释节/参考文献核对失败")
    return text


def main() -> int:
    BAK.mkdir(parents=True, exist_ok=True)
    problems: list[str] = []
    out: dict[str, str] = {}
    for path, label, is_main in ((MAIN, "主稿", True), (ANON, "匿名稿", False)):
        shutil.copy2(path, BAK / path.name)
        t = convert(path, label, problems, is_main)
        if t is not None:
            out[label] = t
    if problems:
        print("\n== 断言失败，未写回 ==")
        for p in problems:
            print(" -", p)
        return 1
    for path, label in ((MAIN, "主稿"), (ANON, "匿名稿")):
        path.write_text(out[label], encoding="utf-8")
    print("\n== 双稿已写回（备份于 tmpe/a_note_bak_20261006/）==")
    print("NOTE 页码待终校清单：注①②③④（四个专著条目——杨正泰/黄仁宇/布罗代尔/魏丕信）公开渠道未能核得目标页码，待按纸本或整理本补入")
    print("NOTE 撤除条目：原参考文献 [1] 黄肃秋本 / [8] 浦安迪 / [9] 刘荫柏 / [10] 李天飞本——正文无引证点，随参考文献表撤除（如需保留另议）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())