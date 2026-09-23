"""_w614_notes_polish.py — W614 第四份外部审读分级采纳·文献体例与英文摘要微调（一次性·可重复执行）

采纳面（2026-09-23 用户批准）：
  A 外文刊名斜体（ISO 690·10 处×两稿）+ ⑪ 篇名内 Journey to the West 斜体补一致
  B 英文摘要三处语病（dashboardized / as an empirical case / are distributed）
  C 参考文献 [1][2] 译著加 [美] 国别标识
  D ⑧ 赵薇文补页码 50-64（观其大较 dhcn.cn+维普两源一致·知网终验挂 48h 清单）
    ⑪ PLOS ONE 补 21(4): e0347253（本会话 Crossref 定版 2026-04-21）
  E 版本注记 v2.3→v2.4（投稿版头注/匿名稿头注）
  F 政策核查清单挂载第 8 项（注释元素级终验）
驳回项：中文摘要两方案（现摘要即达标态·方案A 与现稿相似度 0.97）。
不变式：匿名稿 ③ 保持佚名脱敏（不含仓库 URL）；同文件多处替换串行执行。
"""
import sys

ROOT = r"D:\xiyouji"
SUB = ROOT + r"\docs\S4-学术投稿\装饰投稿\学术论文B轨-新中式数字雅集-装饰投稿版.md"
ANON = ROOT + r"\docs\S4-学术投稿\装饰投稿\学术论文B轨-新中式数字雅集-匿名稿.md"
POLICY = ROOT + r"\docs\S4-学术投稿\装饰投稿\装饰投稿政策核查-2026-09.md"

# ---------- 两稿共用替换（old, new, 次数） ----------
COMMON = [
    # B 英文摘要三处
    ("dashboard-ized", "dashboardized", 1),
    ("visualizations of *Journey to the West*, this paper proposes",
     "visualizations of *Journey to the West* as an empirical case, this paper proposes", 1),
    ("encode cultural semantics and distribute across 233 pages",
     "encode cultural semantics and are distributed across 233 pages", 1),
    # A 外文刊名斜体
    ("[J]. Korean Studies, 2023, 47(1): 117-144.",
     "[J]. *Korean Studies*, 2023, 47(1): 117-144.", 1),
    ("[J]. Digital Humanities Quarterly, 2011, 5(1).",
     "[J]. *Digital Humanities Quarterly*, 2011, 5(1).", 1),
    ("[J]. Transactions of the Institute of British Geographers, 2010, 36(1): 89-108.",
     "[J]. *Transactions of the Institute of British Geographers*, 2010, 36(1): 89-108.", 1),
    ("[J]. Cartographica, 2022, 57(1): 11-36.",
     "[J]. *Cartographica*, 2022, 57(1): 11-36.", 1),
    ("[J]. IEEE Transactions on Visualization and Computer Graphics, 2018, 25(6): 2311-2330.",
     "[J]. *IEEE Transactions on Visualization and Computer Graphics*, 2018, 25(6): 2311-2330.", 1),
    ("[J]. Multimodal Technologies and Interaction, 2023, 7(11): 102.",
     "[J]. *Multimodal Technologies and Interaction*, 2023, 7(11): 102.", 1),
    ("[J]. Digital Scholarship in the Humanities, 2024, 39(1): 308-320.",
     "[J]. *Digital Scholarship in the Humanities*, 2024, 39(1): 308-320.", 1),
    ("[J]. Visual Computing for Industry, Biomedicine, and Art, 2020, 3(1): 23.",
     "[J]. *Visual Computing for Industry, Biomedicine, and Art*, 2020, 3(1): 23.", 1),
    ("[J]. Frontiers in Psychology, 2019, 10: 798.",
     "[J]. *Frontiers in Psychology*, 2019, 10: 798.", 1),
    # D ⑪ 篇名斜体一致 + 卷期补全（Crossref 定版）
    ("translations of Journey to the West: Temporal dynamics",
     "translations of *Journey to the West*: Temporal dynamics", 1),
    ("[J]. PLOS ONE, 2026.", "[J]. *PLOS ONE*, 2026, 21(4): e0347253.", 1),
    # D ⑧ 页码（dhcn.cn+维普两源一致）
    ("山东社会科学, 2018(9).", "山东社会科学, 2018(9): 50-64.", 1),
    # C 译著国别
    ("[1] 鲁道夫·阿恩海姆. 艺术与视知觉[M].",
     "[1] [美]鲁道夫·阿恩海姆. 艺术与视知觉[M].", 1),
    ("[2] 蒲安迪. 明代小说四大奇书[M].",
     "[2] [美]蒲安迪. 明代小说四大奇书[M].", 1),
]

# ---------- 版本注记（分稿） ----------
SUB_ONLY = [
    ("《装饰》投稿版 v2.3 · 2026-09-22", "《装饰》投稿版 v2.4 · 2026-09-23", 1),
    ("+ 跨稿结构残留修复（W606）",
     "+ 跨稿结构残留修复（W606）；v2.4 文献体例与英文摘要微调（外文刊名斜体·⑧⑪卷期页码补全·"
     "译著[美]国别·英文摘要三处语病——第四份外部审读分级采纳）", 1),
    ("> 本稿为《装饰》投稿版 v2.3。", "> 本稿为《装饰》投稿版 v2.4。", 1),
]
ANON_ONLY = [
    ("> 双盲评审改编自《装饰》投稿版 v2.3（2026-09-22·语域专业化与参考文献激活同步）",
     "> 双盲评审改编自《装饰》投稿版 v2.4（2026-09-23·文献体例与英文摘要微调同步镜像）", 1),
]

POLICY_APPEND = (
    "8. **注释元素级体例终验（W614 挂载）**：外文刊名斜体与⑧⑪卷期页码已按 v2.4 落稿；48h 复核时以官网投稿须知为准"
    "终验注释元素级格式（第三方收录版为「作者：《文献名》[M]，出版地：出版单位，出版年，起止页码」混合体例——瀚海学术 "
    "2026-01 收录·与官网并行尾注制不冲突），若官网确认该模板则 ①-⑮ 与 [1]-[5] 按全角标点统一重排；"
    "⑧ 赵薇文页码 50-64 据观其大较 dhcn.cn 与维普记录两源一致（另有 11-25 一说疑为电子转载页码）——投稿前知网终验；"
    "⑪ PLOS ONE 21(4): e0347253 已 Crossref 定版（2026-04-21 刊出·W614 会话核验）。\n"
)


def apply(path, pairs):
    t = open(path, encoding="utf-8", newline="").read()
    for old, new, n in pairs:
        c = t.count(old)
        if c != n:
            # 幂等：已应用则跳过
            if t.count(new) == n and c == 0:
                continue
            raise AssertionError(f"{path}: 「{old[:40]}…」出现 {c} 次（期望 {n}）")
        t = t.replace(old, new)
    return t


def main():
    for path, pairs in ((SUB, COMMON + SUB_ONLY), (ANON, COMMON + ANON_ONLY)):
        t = apply(path, pairs)
        # E1 落地断言
        for probe in ("*Korean Studies*", "*PLOS ONE*, 2026, 21(4): e0347253", "2018(9): 50-64.",
                      "[美]鲁道夫·阿恩海姆", "[美]蒲安迪", "dashboardized",
                      "as an empirical case, this paper", "are distributed across 233 pages"):
            assert t.count(probe) == 1, (path, probe)
        assert "dashboard-ized" not in t and "* * " not in t, path
        assert t.count("*") % 2 == 0, ("斜体标记不配对", path)
        open(path, "w", encoding="utf-8", newline="").write(t)
        print("OK", path.split("\\")[-1])
    # 双盲不变式：匿名稿不得出现仓库 URL；投稿版 ③ 含 URL（匿名 ③ 为佚名占位）
    anon = open(ANON, encoding="utf-8").read()
    sub = open(SUB, encoding="utf-8").read()
    assert "github.com/1273984347" not in anon, "匿名稿双盲破坏"
    assert "github.com/1273984347/xiyouji" in sub, "投稿版③自引缺失"
    assert "佚名. 以《西游记》为对象的数字人文可视化项目" in anon, "匿名③占位缺失"

    # 政策核查挂载（幂等）
    p = open(POLICY, encoding="utf-8", newline="").read()
    if "注释元素级体例终验" not in p:
        anchor = "7. **再核查**：投稿前 48h 刷新本核查（AI 政策、篇幅、栏目要求即时性强）。\n"
        assert p.count(anchor) == 1
        p = p.replace(anchor, anchor + POLICY_APPEND)
        open(POLICY, "w", encoding="utf-8", newline="").write(p)
        print("OK 政策核查 +第8项")
    else:
        print("SKIP 政策核查已挂载")

    # 两稿正文差异面复核：除③与头注外，注释与参考文献应逐字一致（切片止于[5]行尾·不含投稿版仓库页脚）
    def notes_refs(t):
        s = t[t.index("## 注释"):]
        return s[: s.index("[5] 竺洪波") + len("[5] 竺洪波. 西游学十二讲[M]. 北京: 中华书局, 2018.")]
    assert notes_refs(anon).replace(
        "佚名. 以《西游记》为对象的数字人文可视化项目[EB/OL].（匿名：项目信息投稿时随作者信息一并提供）",
        "详解西游记项目. 详解西游记[EB/OL]. https://github.com/1273984347/xiyouji［2026-09-23 引用］.",
    ) == notes_refs(sub).replace("［2026-09-23 引用］.", "［2026-09-23 引用］."), "两稿注释/参考文献漂移"
    print("ALL OK")


if __name__ == "__main__":
    sys.exit(main())
