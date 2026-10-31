# -*- coding: utf-8 -*-
"""_w1049_pitfalls.py — W1049 坑表落仓 + 计数链五处同步（原子替换·可证伪）

纪律：
  · 写既有文件必须「临时文件 + os.replace」原子替换（open(path,'wb') 在 write 前就截断原文件）
  · 读入保留原换行（不全文替换换行符·避免 CRLF→CRCRLF 污染）
  · 插入内容用探测到的真实行尾拼接
  · 命中数断言先行（不符即中止不改）

本批新增 3 条（E-54/E-55/E-56）：
  E-54 出图接口单批上限 10 张 + 9 张批瞬时失败 ⇒ 3–5 张/批最稳
  E-55 母版段「无实心色块」不足以约束「密排纹理/渲染笔触」⇒ 主体段须显式写禁项
  E-56 落位脚本的 og 派生是幂等 SKIP ⇒ 重出母版后 og 仍是旧图（须显式删 og 再重跑）

用法：py -3 archive/scripts/batches/w10xx/_w1049_pitfalls.py [--dry-run]
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))

PIT = os.path.join(REPO, "docs", "agent", "pitfalls.md")
AGENTS = os.path.join(REPO, "AGENTS.md")
HANDOVER = os.path.join(REPO, "HANDOVER.md")
SKILL = os.path.join(REPO, ".agent", "skills", "puti-shouye", "SKILL.md")

NEW_ENTRIES = [
    # (主题节标题前缀, 条目文本)
    ("流程 / 协作 / 取证",
     "- **出图接口有「单批上限 10 张」的硬限，且 9 张批会瞬时失败——3–5 张/批最稳**"
     "（W1049 实证·E-54）：一次请求 12 条直接被拒（`code:400 requests may contain at most 10 "
     "entries`）；改成 9 张/批时**整批瞬时失败**（`connector_tool_error`·latency_ms=0），"
     "但**单张**探测立刻成功 ⇒ 失败与「批大小」相关而非服务端全面不可用。⇒ 拆批到 **3–5 张/批**"
     "后 4/4 批全成；单张仍可能瞬时失败（`err_code:500`·同一批内其他张成功）⇒ **失败件单独重试**"
     "而非整批重发（重发会重复消耗已成功件的生成额度）。⇒ 推广：任何「批量生成/调用」接口都要先"
     "**探一次单件**确认连通性，再定批大小；批内部分失败要按**件**重试而非按**批**重试。"),

    ("CSS / 视觉渲染",
     "- **母版段「无实心色块填充」约束不住「密排纹理」与「渲染笔触」——两者都要在主体段显式禁**"
     "（W1049 实证·E-55）：母版段明写「无实心色块填充、无渐变、无阴影、无光效」，但模型给"
     "**铠甲鳞纹**画成密集排线、给**山石**画成灰擦渲染笔触 ⇒ 整图墨量飙到 0.19–0.20（判据上限 0.12）"
     "而 J6 实心块判据**全绿**（因为它是墨线不是实心块）。⇒ 修法：主体段**追加显式禁项**——"
     "「甲面完全留白·只勾甲片分界线」「不画鳞片阵列·不画细密网纹」「不得用灰擦渲染或阴影渐层」"
     "（重出后同张墨量 0.203 → 0.040）。⇒ 推广：母版段是**通用风格约束**，凡模型有「高频自发倾向」的"
     "元素（鳞纹/网纹/渲染/平涂/刻字）都要在**主体段逐元素补禁项**，否则机器判据只能抓它抓得到的形态。"),

    ("流程 / 协作 / 取证",
     "- **落位脚本的 og 派生是幂等 SKIP ⇒ 重出母版后 og 社交卡仍是旧图**"
     "（W1049 实证·E-56）：母版重出并重新处理后，重跑落位脚本输出 **12 张 og 全部「SKIP 已在位」**"
     "（判据是「文件存在且尺寸 1200×630 且 ≤300KB」⇒ 旧 og 完全满足）⇒ **页面 og:image 指向的仍是旧图**，"
     "而母版/站点版已是新图 ⇒ **肉眼可见的题图与社交卡不一致**。⇒ 与「下载器幂等会复活旧件」"
     "（坑表 E-37）**同族**：任何幂等 SKIP 的派生层（og 派生/缩略图/索引切片）在上游重出后都必须"
     "**显式删产物再重跑**。⇒ 修法：新增 `_w1049_reissue_og.py`——按**白名单**（仅本批重出件）删 og 版"
     "再重跑落位。⇒ 推广：重出链必须**逐层列举派生产物**（原件→母版→站点版→og→切片→索引）并逐层清退，"
     "漏一层就会出现「新母版 + 旧产物」的静默不一致——机器判据全绿也发现不了。"),
]


def read_bytes(p):
    raw = io.open(p, "rb").read()
    text = raw.decode("utf-8")
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return text, nl


def atomic_write(p, text, nl):
    data = text.replace("\n", nl).encode("utf-8")
    tmp = p + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, p)


def atomic_write_raw(p, data):
    tmp = p + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, p)


def insert_into_section(text: str, section_prefix: str, entry: str) -> str:
    """把条目插入指定 `### ` 主题节的末尾（该节最后一个 `- **` 条目之后）。

    实现：定位 `### <section_prefix>` 起点 → 找该节结尾（下一个 `### ` 或文件末）→
          在该节末尾插入条目 ⇒ 保证「声明条数」与「实算条数」按节对齐（C5e 分项对账）。
    """
    m = re.search(r"(?m)^### " + re.escape(section_prefix), text)
    assert m, "主题节未找到：%s" % section_prefix
    start = m.start()
    m_next = re.search(r"(?m)^### ", text[m.end():])
    end = m.end() + m_next.start() if m_next else len(text)
    seg = text[start:end]
    # 该节末尾的非空内容后追加
    seg = seg.rstrip("\n") + "\n" + entry + "\n"
    return text[:start] + seg + text[end:]


def main() -> int:
    dry = "--dry-run" in sys.argv

    # ---------- ① 坑表：按主题节归位插入 3 条 + 主题小节计数 ----------
    text, nl = read_bytes(PIT)
    before_total = len(re.findall(r"^- \*\*", text, re.M))
    already = [e for _sec, e in NEW_ENTRIES if e[:30] in text]
    if already:
        # W1049 盲审 P1-1 修正：**幂等**——本脚本已跑过一次 ⇒ 重跑不得 AssertionError
        #   （原断言 `key not in text` 对已入库条目必然失败 ⇒ 脚本不可重跑）。
        #   处置：已入库则**跳过插入**，只做计数链校准（并如实报告「已存在」）。
        print("坑表：3 条已入库（幂等分支·跳过插入）")
        for _sec, entry in NEW_ENTRIES:
            if entry[:30] in text:
                print("  SKIP  %s…（已存在）" % entry[:24])
    else:
        for sec, entry in NEW_ENTRIES:
            text = insert_into_section(text, sec, entry)
    after_total = len(re.findall(r"^- \*\*", text, re.M))
    expect_total = before_total if already else before_total + 3
    assert after_total == expect_total, \
        "总条数 %d → %d（应 %d）" % (before_total, after_total, expect_total)

    # 主题小节计数同步（按节实算改标题·不靠手算）
    THEME_TITLES = ["CSS / 视觉渲染", "JS / CSP / 运行时", "git / 提交 / 并发",
                    "级联 / CHANGELOG", "数据 / 内容可信度", "流程 / 协作 / 取证"]
    for k in THEME_TITLES:
        m = re.search(r"(?m)^### " + re.escape(k) + r"（(\d+) 条）", text)
        assert m, "主题标题未找到：%s" % k
        old_n = int(m.group(1))
        seg_start = m.start()
        m_next = re.search(r"(?m)^### ", text[m.end():])
        seg_end = m.end() + m_next.start() if m_next else len(text)
        actual = len(re.findall(r"(?m)^- \*\*", text[seg_start:seg_end]))
        if actual != old_n:
            text = (text[:m.start()] + "### %s（%d 条）" % (k, actual)
                    + text[m.end():])
            print("坑表小节「%s」%d → %d（实算修正）" % (k, old_n, actual))
    print("坑表：%d → %d 条" % (before_total, after_total))

    # ---------- ② 计数链四处（AGENTS 总数+分项 / HANDOVER 总数 / SKILL 两处）----------
    # W1049 盲审 P1-1 修正：计数链断言按「**当前实况**」而非「固定旧值」判定 ⇒ 可重跑。
    #   原版断言 `skill_text.count("140 条") == 2` ⇒ 跑一次后即永久失败。
    target_total = after_total          # 坑表实算总数 = 计数链应声明的总数
    agents_text, agents_nl = read_bytes(AGENTS)
    ag_total = re.findall(r"(\d+) 条坑位", agents_text)
    assert len(ag_total) == 1, "AGENTS 总数声明命中 %d 次" % len(ag_total)
    ag_old_total = int(ag_total[0])
    if ag_old_total != target_total:
        agents_text = agents_text.replace("%d 条坑位" % ag_old_total,
                                          "%d 条坑位" % target_total)
    print("AGENTS.md：总数 %d → %d" % (ag_old_total, target_total))
    # 六主题分项行：逐主题独立定位（避免长正则括号配对出错）
    THEME_KEYS = ["CSS / 视觉渲染", "JS / CSP / 运行时", "git / 提交 / 并发",
                  "级联 / CHANGELOG", "数据 / 内容可信度", "流程 / 协作 / 取证"]
    THEME_DELTA = {"CSS / 视觉渲染": 1, "流程 / 协作 / 取证": 2}
    for k in THEME_KEYS:
        pat = re.compile(re.escape(k) + r"（(\d+)）")
        hits = list(pat.finditer(agents_text))
        assert len(hits) == 1, "AGENTS 分项「%s」命中 %d 次" % (k, len(hits))
        old_n = int(hits[0].group(1))
        new_n = old_n + (THEME_DELTA.get(k, 0) if not already else 0)
        if old_n != new_n:
            agents_text = agents_text[:hits[0].start()] + "%s（%d）" % (k, new_n) \
                + agents_text[hits[0].end():]
            print("AGENTS 分项「%s」%d → %d" % (k, old_n, new_n))

    handover_text, handover_nl = read_bytes(HANDOVER)
    ho_pat = re.compile(r"（(\d+) 条·六主题）")
    ho_hits = list(ho_pat.finditer(handover_text))
    assert len(ho_hits) == 1, "HANDOVER C5e 形态命中 %d 次" % len(ho_hits)
    ho_old = int(ho_hits[0].group(1))
    if ho_old != target_total:
        handover_text = (handover_text[:ho_hits[0].start()]
                         + "（%d 条·六主题）" % target_total
                         + handover_text[ho_hits[0].end():])
    handover_text = re.sub(r"（\d+ 条坑·六主题", "（%d 条坑·六主题" % target_total,
                         handover_text)
    print("HANDOVER：%d → %d" % (ho_old, target_total))

    # SKILL.md：**只有**指「坑表总条数」的两处需随总数变（143 条·六主题 / 143 条完整教训）；
    #   「15 条硬判据」「15 条最高频硬判据」是 **skill 自身的条目数**（与坑表无关）⇒ 禁改。
    #   （W1049 盲审后自修：首版用 `re.sub(r"\d+ 条", …)` 误伤这两处 ⇒ 收窄为定点替换。）
    skill_text, skill_nl = read_bytes(SKILL)
    n_skill = 0
    for old_tpl, new_tpl in (
            (r"（\d+ 条·六主题）", "（%d 条·六主题）"),
            (r"\d+ 条完整教训", "%d 条完整教训")):
        m = re.search(old_tpl, skill_text)
        if m:
            old_n = int(re.search(r"\d+", m.group(0)).group(0))
            skill_text = skill_text.replace(m.group(0), new_tpl % target_total)
            n_skill += 1
            print("SKILL：%s %d → %d" % (old_tpl, old_n, target_total))
    # 自证：skill 自身条目数不得被误改
    assert "15 条硬判据" in skill_text, "SKILL「15 条硬判据」被误改（禁止项）"
    assert "15 条最高频硬判据" in skill_text, "SKILL「15 条最高频硬判据」被误改（禁止项）"
    print("SKILL：自证「15 条硬判据」保持不变 ✓（%d 处坑表计数已校准）" % n_skill)

    if dry:
        print("DRY 未落盘")
        return 0

    atomic_write(PIT, text, nl)
    atomic_write(AGENTS, agents_text, agents_nl)
    atomic_write(HANDOVER, handover_text, handover_nl)
    atomic_write(SKILL, skill_text, skill_nl)
    print("已落盘：坑表 + AGENTS + HANDOVER + SKILL（计数链四处一致）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
