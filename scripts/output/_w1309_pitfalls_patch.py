# -*- coding: utf-8 -*-
import os
ROOT = "D:/xiyouji"

E316 = "- **归档腾窗的迁出量必须取「最小达标」而非固定步长·且与「保留底线」联立·多面正本须统一迁到同一下界**（W1308 实证·E-316·跨项目通用）：治理文档（段式追加 + 字节上限 + 保留底线）腾窗时，规划器若以固定步长（如 chunk=50 段）决定迁出量 ⇒ 迁出量由「步长」而非「体积缺口」决定 ⇒ 实测 file-index 正本 50 段·体积 262,964 B **仅超窗 820 B** 却被迫迁 44 段 ⇒ 正本仅剩 6 段 ⇒ 铁律 22「正本留 ≥ 20 段」断言红 ⇒ 收官链死在 archive 步。⇒ 纪律：① **迁出量取最小达标 k**（体积对 k 单调 ⇒ 二分求最小 k）；② **迁出上界与保留底线联立**（保留底线是规划期约束·不是迁出后的检查）且迁出块须避开不可迁出的段（承载版本推进锚点的「编号规则段」）；③ **多面正本（CHANGELOG / file-index / 台账）存在「两面最小 W 号须一致」硬断言时 ⇒ 只迁超窗的一面必然下界错位** ⇒ 正解是「各面按最小达标规划 ⇒ 取目标下界 = 各面迁出后下界的较大者 ⇒ 两面统一迁出「所有 W < 目标下界」的段」；④ 迁完仍超窗时**不要硬迁**（会把下界推到另一面不可达的位置）⇒ 按铁律口径压缩登记面密度（目录级聚合）而非继续搬段。"

E317 = "- **链首 upsert 的「同号替换」若只替换括号区间⇒条目左侧的日期前缀残留⇒产出双日期⇒下游判据报「无该行」（指错方向）**（W1308 实证·E-317·跨项目通用）：HANDOVER「最后更新」链首条目形态为「YYYY-MM-DD（W#### …）」，而幂等键从「文本」放宽到「批号」后，同号条目**文本变更**走「按批号替换」分支 ⇒ 该分支只替换「（W#### …）」⇒ 左侧日期前缀残留 ⇒ 产出「最后更新：2026-11-232026-11-23（W1308 …）」⇒ 下游登记面一致性闸的正则「最后更新：<日期>（W####」匹配不上 ⇒ 报「HANDOVER 无「最后更新」行 ⇒ 交接链首未维护」——**报错指向链首缺失·真因是形态畸形**。⇒ 纪律：替换区间须自**前缀起算**（helper：条目起点 = 前缀末端）且内容一致但有残留时亦走清理（幂等自愈）；另：判定「该串是否属于末尾文件级块」须用**绝对位置**（段内相对偏移会把末尾块误判成批段）。"

E318 = "- **幂等 upsert 按「行」定位 ⇒ 多行块被当成多块⇒替换只覆盖首行⇒其余行逐次累积成重复段**（W1308 实证·E-318·跨项目通用）：spec 的块内容若为多行（如 milestone_block 两行），写入侧用行正则定位本批块 ⇒ 每行都被当成独立块 ⇒ 替换区间只覆盖首行 ⇒ 第二行永久残留 ⇒ 每跑一次链多一份 ⇒ 实测同一批的 2 行里程碑累积成 6 行 ⇒ 第 31 门禁 C8「同段重复」判红。⇒ 纪律：① 定位层**分界时跳过与前一块同批号的 head**（视为同一块的续行）⇒ 区间覆盖整个多行块；② 写入层 spec 块内容**尽量单行**（多行块会被各类「按行计数」的判据当成多块 ⇒ 体积窗与重复判据同时受害）。"

E319 = "- **窗口类补滚的触发面必须覆盖「内容变更（replaced）」路径·且须循环到达标——一次只滚一块等于没滚**（W1308 实证·E-319·跨项目通用）：里程碑滚动工具内部早有「窗口超限 ⇒ 继续补滚」守卫，但**调用点只在「本批块 inserted」路径触发** ⇒ 「replaced」（spec 内容变更·同批号替换）路径永不动 ⇒ 块数只增不减（实测累积到 11 块 ⇒ C7 体积窗判红）；且每次只淘汰 1 块 ⇒ 即使触发也解不了超限。⇒ 纪律：① 触发条件用**状态集合**（inserted / replaced / moved）而非单一状态；② 滚动量须**循环到达标**（内部守卫「已达标 ⇒ 零变化」使循环自然收敛）；③ 循环前须检查「无盈可滚」（窗口不足 2 块时停·否则会滚到断言失败）。"

E320 = "- **用 git ls-files 展开目录清单时必须加 core.quotepath=false 且必须用 --exclude-standard 排除 .gitignore 面——否则要么漏 add·要么整链中止**（W1308 实证·E-320·跨项目通用）：收官链 add 步把登记面里的「目录分组行」展开为待 add 路径 ⇒ 两个坑同时命中：① git ls-files 默认对非 ASCII 路径**转义**（八进制）⇒ 展开出的路径在磁盘上不存在 ⇒ 被判「尚不存在」跳过 ⇒ 中文路径文件**静默漏 add**；② 若用 os.walk 递归磁盘来展开 ⇒ 把 .gitignore 忽略目录（实测 docs/S2-外部分享、视觉重设计样板/*/_verify_shots）也纳入 ⇒ git add 报「paths are ignored by one of your .gitignore files」⇒ **add 步整链中止**。⇒ 纪律：展开一律走 git 口径（ls-files 加 ls-files --others --exclude-standard）并加 -c core.quotepath=false；分组登记行的展开面必须与「本批实际变更面」对账（展开会把同目录的未改动件也纳入·幂等但需知情）。"

ENTRIES = {"docs/agent/pitfalls-topics/cascade-changelog.md": [("E-316", E316), ("E-317", E317), ("E-318", E318), ("E-319", E319)],
           "docs/agent/pitfalls-topics/git-concurrency.md": [("E-320", E320)]}

for rel, items in ENTRIES.items():
    p = os.path.join(ROOT, rel)
    raw = open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else b"\n"
    t = raw.decode("utf-8").replace("\r\n", "\n")
    for eid, body in items:
        t = t.rstrip("\n") + "\n\n" + body + "\n"
    open(p, "wb").write(t.replace("\n", nl.decode()).encode("utf-8"))
    print("appended", rel, [e for e, _ in items])

ap = os.path.join(ROOT, "archive/docs/pitfalls-detail-ARCHIVE.md")
raw = open(ap, "rb").read()
nl = "\r\n" if b"\r\n" in raw else b"\n"
t = raw.decode("utf-8").replace("\r\n", "\n")
allitems = sorted([i for v in ENTRIES.values() for i in v], key=lambda kv: int(kv[0][2:]))
for eid, body in allitems:
    t = t.rstrip("\n") + "\n\n#### %s（原文全量·W1308 新增）\n\n%s\n" % (eid, body)
open(ap, "wb").write(t.replace("\n", nl.decode()).encode("utf-8"))
print("archive appended", [e for e, _ in allitems])
