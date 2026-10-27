#!/usr/bin/env python3
"""一次性：W987 归族登记 + 坑表 +3 条 + 计数链 77 → 80 + README §六 登记

字节级替换 + 原子替换；锚点断言命中数=1（fail-closed）。
"""
import io
import os
import sys

PROMO = os.path.join("assets", "promo", "README.md")
PIT = os.path.join("docs", "agent", "pitfalls.md")
AG = "AGENTS.md"
HO = "HANDOVER.md"
RM = os.path.join("docs", "11-方案报告", "README.md")

INK_SECTION = """## 水墨意境卡族（33 张 · 1:1 · 与题图族刻意分开）

站内另有一条**从未上线的视觉资产线**：**33 张 1:1（1200×1200）水墨意境插画**，实读特征 = 宣纸底 + 水墨晕染 + 大留白 + **每张一枚朱红印章**（与题图族的工笔白描是两条画风）。

| 子族 | 数量 | 命名依据 | 成员示例 |
|---|---|---|---|
| `site/static/images/card-*.webp` | 27 | 角色 / 场景题材 | `card-01-huoshan`（火山）· `card-07-baiyao`（白妖群像）· `card-19-shaseng-dujiang`（沙僧渡江） |
| `site/static/images/chap-*.webp` | 6 | 回目 | `chap-07`（第 007 回八卦炉）· `chap-15`（第 015 回白马崖）· `chap-30`（第 030 回黑虎） |

**规范边界（W987 确立 · 不可混用）**：

| 维度 | 题图族 `plate-line-*` | 水墨意境卡族 `card-*` / `chap-*` |
|---|---|---|
| 画幅 | 1200×1600（3:4） | 1200×1200（1:1） |
| 画风 | 工笔白描线描（宣纸底 + 纯墨线 + 单点朱砂） | 水墨写意晕染（宣纸底 + 浓淡墨 + **朱红印章**） |
| 母版段约束 | 禁文字 / 书法 / 印章 / 实心填充 | **不适用**（本族带印章与浓墨） |
| 页面容器类名 | `.chapter-plate`（限宽 420px·首屏标题下） | `.chapter-scene`（限宽 520px·正文首个 `<h2>` 前） |
| 暗色模式 | 隐藏（浅底贴深色底成亮斑） | **同样隐藏**（同因） |
| alt 文本 | 描述画面主体 | 描述画面主体（已写） |

**W987 批已启用**：6 个回目页（ch007 / ch014 / ch015 / ch023 / ch027 / ch030）新增 `.chapter-scene` 场景图 ⇒ 本族首次以「场景插图」身份上线。**其余 27 张 `card-*` 仍为未引用存量**（题材各异，投放位置需逐张判断，另批处理）。

**可用的投放位置（建议）**：① 回目页正文场景位（已用）；② 角色页 / 主题页顶部的意境横幅（`card-*` 逐张判断）；③ 分回次 / 分主题的社交分享图（需另裁 1200×630 版）；④ 线下 A4 宣传单页插图（物料不受题图母版段约束）。**不可用**：暗色模式、首页首屏轮播（hero 族为 21:9 宽幅，与 1:1 不匹配）。

**维护约定**：本族**不得**被填进 `.chapter-plate` 范式（题图母版段禁印章/禁文字）⇒ 引用时一律用 `.chapter-scene`；族成员盘点命令见 `scripts/_w987_family_scan.py`（成员数 / 尺寸分布 / 引用现状 / 插入点），新增同族文件后须重跑并更新本节。

---

"""

VISUAL = [
    "- **资产族必须归族登记：同族两套命名 + 全部 0 引用 = 「事实闲置但无人知道」**（W987 实证·E-08）："
    "仓库里长期存在、未被引用的视觉资产时，**闲置规模极易被低估**——本批实测：`card-*` 27 张 + `chap-*` 6 张 = 33 张 1:1 水墨图，"
    "**全部 0 引用**（`card-*` 27 张同样从未上线），而用户只问起了其中 6 张 ⇒ 真实闲置面比感知大 5.5 倍。"
    "⇒ 做法：① 按「命名族 + 尺寸族 + 画风族」三个维度扫出成员；② 在**手写**导读里登记：成员清单 + 命名分歧 + 规范边界 + 引用状态 + 投放位置建议；"
    "③ 登记节写明盘点命令（可复算）。",

    "- **不同画风族要靠「类名」而非「注释」隔开规范**（W987 实证·E-09）："
    "同一站点并存两套画风/两套资产规范时（题图禁印章 vs 意境图带印章），若沿用同一个容器类名 ⇒ 后一族的资产会继承前一族的约束（或违反之）。"
    "⇒ 做法：① 新立独立类名（`.chapter-scene` vs `.chapter-plate`）并写独立样式块；② 规范差异写进资产导读的「规范边界」表；"
    "③ 验收项固定包含「同页两图各有 1 个且类名不混」。"
    "⇒ 本批实测：6 页题图与场景图并存 6/6 合规，题图母版段的「禁印章/禁文字」不被场景图继承。",

    "- **同页两图：首屏留给主资产，第二资产下沉到正文入口**（W987 实证·E-10）："
    "一页需要两类视觉资产时，把两类图都堆在标题下会显得重复。⇒ 做法：① 首屏（标题下）放主资产（题图·角色立像）；"
    "② 次资产（意境图）放在正文**首个 `<h2>` 之前**；③ 两者限宽分级（题图 420px / 场景图 520px）+ 足够留白分隔。"
    "⇒ 本批 6 页实跑：首屏观感不变，场景图在正文入口形成第二层阅读节奏，无拥挤感。",
]

README_ROW = (
    "| 40 | T-33《任务计划执行与经验沉淀报告》— 水墨意境卡族启用批（33 张 1:1 水墨插画·6 张上回目页场景位·2026-10-27·V1.0·W987） | "
    "[T33-任务计划执行与经验沉淀报告-2026-10-27.md](计划方案/T33-任务计划执行与经验沉淀报告-2026-10-27.md) | "
    "框架第三十三次执行：用户 2026-10-27 20:50 问「浓墨渲染图可以用在哪里？」→ 20:53 令「开工」（采纳我提的顺序：先归族登记、再启用为回目页场景插图）；"
    "① **实读发现**——站内 `card-*` 27 张 + `chap-*` 6 张 = **33 张 1:1 水墨意境图全部 0 引用**（闲置规模比感知大 5.5 倍）"
    "且同族两套命名（按回目 / 按角色场景）易被误当题图用（W984 批即踩过）；"
    "② **归族登记**——`assets/promo/README.md` 新增「水墨意境卡族」节（成员 / 命名分歧 / **规范边界表**：禁印章·不进 `.chapter-plate`·暗色隐藏·1:1 / 引用状态 / 投放位置建议）；"
    "③ **启用 6 张**——6 个回目页新增 `.chapter-scene` 场景图（限宽 520px·插在正文首个 `<h2>` 前·首屏仍留题图）；"
    "④ 验收：6/6 页题图+场景图各 1 且类名不混 · 暗色隐藏规则齐 · 6 图 HTTP 200 image/webp · 接入幂等 6/6 SKIP · 浏览器实跑渲染正常；"
    "⑤ 坑表 **+3 条（77 → 80）**（资产族归族登记 / 类名隔开规范 / 同页两图首屏留主资产）|"
)

REPL_PROMO = [
    ("## 投放接线（W898 起）", INK_SECTION + "## 投放接线（W898 起）"),
]
REPL_PIT = [
    ("### CSS / 视觉渲染（18 条）", "### CSS / 视觉渲染（21 条）"),
]
REPL_AG = [
    ("> **📖 阅读契约（W709）**：索引型——77 条坑位按六主题迁",
     "> **📖 阅读契约（W709）**：索引型——80 条坑位按六主题迁"),
    ("CSS/视觉渲染（18）· JS/CSP/运行时（6）· git/提交/并发（19）· 级联/CHANGELOG（8）· 数据/内容可信度（9）· 流程/协作/取证（17）。"
     "计数口径 = 各节顶层「- **」条目数（现役 77 条·增量沿革见各条目自注与 CHANGELOG·W986 校）。",
     "CSS/视觉渲染（21）· JS/CSP/运行时（6）· git/提交/并发（19）· 级联/CHANGELOG（8）· 数据/内容可信度（9）· 流程/协作/取证（17）。"
     "计数口径 = 各节顶层「- **」条目数（现役 80 条·增量沿革见各条目自注与 CHANGELOG·W987 校）。"),
]
REPL_HO = [
    ("> [docs/agent/pitfalls.md](docs/agent/pitfalls.md)（77 条·六主题）",
     "> [docs/agent/pitfalls.md](docs/agent/pitfalls.md)（80 条·六主题）"),
    ("> **雷区权威 = [docs/agent/pitfalls.md](docs/agent/pitfalls.md)（77 条·六主题·含 shell 场景查坑表）**；",
     "> **雷区权威 = [docs/agent/pitfalls.md](docs/agent/pitfalls.md)（80 条·六主题·含 shell 场景查坑表）**；"),
]


def atomic_write(path, data):
    tmp = path + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, path)


def edit(path, repls):
    raw = io.open(path, "rb").read()
    for old, new in repls:
        ob, nb = old.encode("utf-8"), new.encode("utf-8")
        n = raw.count(ob)
        if n != 1:
            print("ABORT  %s 命中数 %d（期望 1）· %s" % (path, n, old[:40]))
            sys.exit(2)
        raw = raw.replace(ob, nb)
    atomic_write(path, raw)
    print("已改 %s（%d 处）" % (path, len(repls)))


def main():
    # ① 归族登记
    edit(PROMO, REPL_PROMO)

    # ② 坑表 +3（视觉渲染节，插到 JS 节标题之前）
    raw = io.open(PIT, encoding="utf-8", newline="").read()
    anchor = "### JS / CSP / 运行时（6 条）"
    if raw.count(anchor) != 1:
        print("ABORT  坑表 JS 节锚点异常")
        return 2
    raw = raw.replace(anchor, "\n".join(VISUAL) + "\n\n" + anchor)
    for old, new in REPL_PIT:
        if raw.count(old) != 1:
            print("ABORT  节标题锚点异常：%s" % old)
            return 2
        raw = raw.replace(old, new)
    atomic_write(PIT, raw.encode("utf-8"))
    print("已改 坑表：+3 条（视觉渲染 21）· 总数 77 → 80")

    # ③ AGENTS ×2 / HANDOVER ×2
    edit(AG, REPL_AG)
    edit(HO, REPL_HO)

    # ④ README §六：+1 行 + 标题件数
    raw = io.open(RM, encoding="utf-8", newline="").read()
    old_title = "### 六、计划方案（42 件）"
    if raw.count(old_title) != 1:
        print("ABORT  README §六 标题锚点异常")
        return 2
    raw = raw.replace(old_title, "### 六、计划方案（43 件）")
    anchor = "\n### 七、历史归档指针"
    if raw.count(anchor) != 1:
        print("ABORT  README §七 锚点异常")
        return 2
    raw = raw.replace(anchor, ("\n" + README_ROW + "\n").encode("utf-8").decode("utf-8") + anchor)
    atomic_write(RM, raw.encode("utf-8"))
    print("已改 README §六：+1 行（序号 40·T-33）· 标题 42 → 43 件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
