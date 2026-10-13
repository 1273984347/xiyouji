"""W702 一次性编辑器：外部挑刺 17 项裁决落地（六文档口径清债）。
每处替换断言唯一命中；CRLF 文件自动适配。跑完即删（E1 验证靠 Grep）。"""
import sys

EDITS = {}  # path -> [(old, new, label)]

EDITS["scripts/batch_cascade.py"] = [
    (
        '    out = re.sub(r"> \\*\\*当前版本 v[\\d.]+（[^）]*）\\*\\*： W\\d+ [^·]*·A1-A6",\n'
        '                 f"> **当前版本 {ver}（{date}）**： {batch} {desc} ·A1-A6", s, count=1)',
        '    out = re.sub(r"> \\*\\*当前版本 v[\\d.]+（[^）]*）\\*\\*：\\s*W\\d+ [^·]*·A1-A6",\n'
        '                 f"> **当前版本 {ver}（{date}）**：{batch} {desc}·A1-A6", s, count=1)',
        "README 模板去空格+锚点 \\s* 兼容",
    ),
    (
        '    out = re.sub(r"> 当前版本：v[\\d.]+（[^）]*）— W\\d+ [^—]*— A1-A6",\n'
        '                 f"> 当前版本：{ver}（{date}）— {batch} {desc} — A1-A6", s, count=1)',
        '    out = re.sub(r"> 当前版本：v[\\d.]+（[^）]*）— W\\d+ [^—]*—\\s*A1-A6",\n'
        '                 f"> 当前版本：{ver}（{date}）— {batch} {desc}—A1-A6", s, count=1)',
        "STRUCTURE 模板去空格+锚点 \\s* 兼容",
    ),
    (
        '    out = re.sub(r"> 当前版本 v[\\d.]+（[^）]*）：W\\d+ [^·]*·详细变更见",\n'
        '                 f"> 当前版本 {ver}（{date}）：{batch} {desc} ·详细变更见", s, count=1)',
        '    out = re.sub(r"> 当前版本 v[\\d.]+（[^）]*）：W\\d+ [^·]*·详细变更见",\n'
        '                 f"> 当前版本 {ver}（{date}）：{batch} {desc}·详细变更见", s, count=1)',
        "项目说明模板去空格",
    ),
    (
        '    s = s.replace(tail, "；{}。如与上述权威文档冲突，以权威文档为准。*".format(spec["agents_note"]), 1)',
        '    _sep = "" if s[: s.index(tail)].rstrip().endswith("；") else "；"\n'
        '    s = s.replace(tail, _sep + "{}。如与上述权威文档冲突，以权威文档为准。*".format(spec["agents_note"]), 1)',
        "AGENTS 脚注 join 双分号守卫",
    ),
]

EDITS["CLAUDE.md"] = [
    (
        "python scripts/verify_delivery.py        # 提交前唯一硬门禁（pre-commit 自动跑）",
        "python scripts/verify_delivery.py        # 提交前唯一硬门禁（pre-commit 自动跑）\n"
        "python scripts/verify_delivery.py --scope auto  # 本地提交轻量档（CI 恒全量）",
        "常用命令补 --scope auto 轻量档",
    ),
]

EDITS["CONTRIBUTING.md"] = [
    (
        "W### ID 是双索引的锚点：CHANGELOG 按 W### 顺序记录变更，file-index 按文件记录被哪些 W### 修改过。",
        "W### ID 是双索引的锚点：CHANGELOG 按 W### 顺序记录变更，file-index 按文件记录被哪些 W### 修改过。\n"
        "\n"
        "**W### 认领对账（W663 起）**：W### 编号动工前必须先在 [W批次编号对账表](docs/00-导读/W批次编号对账表.md) "
        "登记认领（唯一对账依据·防并发撞号·登记即豁免 doc-sync 提交-版段对账）；「Grep 现役段 max+1」在版段递延时"
        "可能滞后于已认领号，以对账表为准。",
        "补 W### 认领对账表入口段",
    ),
]

EDITS["docs/00-导读/W批次编号对账表.md"] = [
    (
        "> ## 现势：下一自由号 = **W702**（W701 已由 ZCode 2026-10-11 认领〔BL-20 动工与 S-26 工具化批〕；",
        "> ## 现势：下一自由号 = **W703**（W702 已由 ZCode 2026-10-11 认领〔外部挑刺 17 项裁决与六文档口径清债批〕；"
        "W701 已收官〔BL-20 动工与 S-26 工具化批〕；",
        "现势翻 W703",
    ),
    (
        "**作废**（W686·用户裁决 workflow 方案退役·WF-1 复活随之取消·后续重新设计另认领新号） | ZCode 2026-10-07 |",
        "**作废**（W686·用户裁决 workflow 方案退役·WF-1 复活随之取消·后续重新设计另认领新号） | ZCode 2026-10-07 |\n"
        "| W702 | 外部挑刺 17 项裁决与六文档口径清债批（P0 口径四件〔CHANGELOG 页数口径块实跑刷新 857/856/855/330·reader 622 纳入 "
        "+ AGENTS 第 8 门禁 233→856 页 + README 26→40 项门禁 + STRUCTURE 方法论 6→33 篇〕+ P1〔scripts 30→34 类全建+F 行 "
        "story-timeline 补录 + 第 6 门禁三豁免→五豁免对齐 W700〕+ P2〔v2.3.279/280 四件套补录只增不删 + 第 26 门禁 334→855 页 "
        "+ CONTRIBUTING 对账表认领入口〕+ P3〔batch_cascade 版本行模板去空格 + AGENTS 脚注 join 双分号守卫与存量 4 处归一 "
        "+ CLAUDE.md --scope auto 行〕+ 顺带 JSON 131→135 + 驳回 1 项防新漂移字面量） "
        "| 本次提交（级联 v2.3.296·batch_cascade 原生） | v2.3.296 | **进行中** | ZCode 2026-10-11 |",
        "追加 W702 认领行",
    ),
]

EDITS["AGENTS.md"] = [
    (
        "`scripts/verify_delivery.py` 是提交前唯一硬门禁入口（`.git/hooks/pre-commit` → 本脚本，核心 FAIL 返回非 0 阻断）。内含：",
        "`scripts/verify_delivery.py` 是提交前唯一硬门禁入口（`.git/hooks/pre-commit` → 本脚本·W698 起本地传 `--scope auto` 分级，"
        "CI 与批收尾恒全量，核心 FAIL 返回非 0 阻断）。内含：",
        "§4.2 前言补 scope auto",
    ),
    (
        "6. **docs 全量链接校验**（lint_links 0 broken·W699 扩自 docs/01 至 docs 全量·内建三豁免=docs/archive 冻结档/gitignore 本地件/fenced+inline code 去噪）",
        "6. **docs 全量链接校验**（lint_links 0 broken·W699 扩自 docs/01 至 docs 全量·W700 五改后内建五豁免=fenced+inline code 去噪/"
        "git check-ignore 本地产物/docs/archive 冻结档/POSIX 根绝对路径跳过/_w588_ce.html 快照件）",
        "第 6 门禁三豁免→五豁免",
    ),
    (
        "8. **CSP 漂移**（generate_csp.py --check，233 页哈希 0 漂移）",
        "8. **CSP 漂移**（generate_csp.py --check，856 页哈希 0 漂移·页数随口径演进以实跑为准）",
        "第 8 门禁 233→856",
    ),
    (
        "sitemap 集合一致；334 页扫描；SEO head 属静默腐烂面",
        "sitemap 集合一致；855 页扫描（site 全树减两个模板壳·W702 校真）；SEO head 属静默腐烂面",
        "第 26 门禁 334→855",
    ),
    (
        "（本地件不入仓）；；2026-10-10（v2.3.288",
        "（本地件不入仓）；2026-10-10（v2.3.288",
        "脚注双分号 1/4",
    ),
    (
        "（AGENTS §1/§3）；；2026-10-10（v2.3.289",
        "（AGENTS §1/§3）；2026-10-10（v2.3.289",
        "脚注双分号 2/4",
    ),
    (
        "方法论 README 索引第 34 行；；2026-10-11（v2.3.291",
        "方法论 README 索引第 34 行；2026-10-11（v2.3.291",
        "脚注双分号 3/4",
    ),
    (
        "无 § 结构性变更；；2026-10-11（v2.3.293",
        "无 § 结构性变更；2026-10-11（v2.3.293",
        "脚注双分号 4/4",
    ),
]

EDITS["README.md"] = [
    (
        "- **门禁体系**：每次提交需通过 26 项自动化门禁",
        "- **门禁体系**：每次提交需通过 40 项自动化门禁",
        "26→40 项门禁",
    ),
    (
        "（A4 209 篇 已含）",
        "（A4 209 篇已含）",
        "版本行「已含」空格归一",
    ),
]

EDITS["STRUCTURE.md"] = [
    (
        "（A4 209 篇 已含）",
        "（A4 209 篇已含）",
        "版本行「已含」空格归一",
    ),
    (
        "项目方法论沉淀层——把项目过程中积累的可复利方法论经验集中沉淀为教学材料。已建 6 篇（统一结构：问题背景 + 核心方法论 + 复现案例 + 修复策略 + 关联文档）：",
        "项目方法论沉淀层——把项目过程中积累的可复利方法论经验集中沉淀为教学材料。已建 33 篇（目录实数·W702 校真·含索引 README；"
        "统一结构：问题背景 + 核心方法论 + 复现案例 + 修复策略 + 关联文档；全量篇目与阅读路径见 [README.md](docs/10-方法论沉淀/README.md) 索引）。奠基 6 篇：",
        "方法论 6→33 篇",
    ),
    (
        "## scripts/ Python 脚本（按 34 类组织 A-AH，已建 30 类）",
        "## scripts/ Python 脚本（按 34 类组织 A-AH·34 类子目录全建：A-L 早期基础 / M-U Phase 5 专题 / V-AH Phase 6 跨学科创意；Q+/Q++ 数据内嵌无独立脚本）",
        "scripts 30→34 类全建",
    ),
    (
        "| **F. 时间** | `F_时间/` | timeline.py | （未单独建可视化页） | 三重平行时间线、关键事件时间线 |",
        "| **F. 时间** | `F_时间/` | timeline.py | story-timeline.html（W694 起·第 39 门禁双源同步） | 三重平行时间线、关键事件时间线 |",
        "F 行可视化页补录",
    ),
    (
        "data/ 当前 131 个 JSON 文件",
        "data/ 当前 135 个 JSON 文件",
        "JSON 131→135",
    ),
]

EDITS["CHANGELOG.md"] = [
    (
        "> **全站页数口径**（W459 起，各门禁分母不同）：HTML 共 234 页（site/data 87 + site/en 138 + site 根 9）；"
        "CSP 覆盖 233 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 232 文件（再排除 `_shell.html`）；"
        "inline_css 同步 225 页（site/data + site/en，site 根以 `<link>` 引外部 css）；「可视化页 86」= site/data 87 减 `_shell.html`。",
        "> **全站页数口径**（W459 建·W702 实跑刷新，各门禁分母不同）：HTML 共 857 页（site/data 88 + site/en 138 + site 根 9 + site/reader 622）；"
        "CSP 覆盖 856 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 855 文件（再排除 `_shell.html`）；"
        "check_seo_head 扫 855 页（site 全树减两个模板壳）；inline_css 同步 330 页（site 全树含 INLINED 标记页）；"
        "「可视化页 87」= site/data 88 减 `_shell.html`。",
        "口径块整段实跑刷新",
    ),
    (
        "> - **验证**：verify_delivery 核心全绿；引文 486 条 100%；ruff scripts/ 全绿；受影响 docx（数字人文研究版/南艺版/艺术百家版）重生成 COM 验收 22/13/13 页。\n"
        "### v2.3.279",
        "> - **验证**：verify_delivery 核心全绿；引文 486 条 100%；ruff scripts/ 全绿；受影响 docx（数字人文研究版/南艺版/艺术百家版）重生成 COM 验收 22/13/13 页。\n"
        "> - **文件**：六文档级联（README/STRUCTURE/项目说明/交接/AGENTS 脚注/workflows README）+ CITATION.cff + file-index + 对账表 + "
        "三页脚（index/cross-time-danmaku/tag-cloud）+ dukou-engine 页脚 + scripts/_s5_review_fixes.py（一次性）；S4 稿件面均本地件不入仓（双盲纪律）。"
        "（W702 补录四件套）\n"
        "> - **状态**：已落地（CI 五工作流以推送后 gh run list 为准）。（W702 补录）\n"
        "\n"
        "### v2.3.279",
        "v2.3.280 补录文件/状态",
    ),
    (
        "> - **门禁**：引文 486 条 100%。\n"
        "### v2.3.278",
        "> - **门禁**：引文 486 条 100%。\n"
        "> - **文件**：六文档级联（README/STRUCTURE/项目说明/交接/AGENTS 脚注/workflows README）+ CITATION.cff + file-index + 对账表 + "
        "三页脚（index/cross-time-danmaku/tag-cloud）+ dukou-engine 页脚 + scripts/_s5_round6_edits.py（一次性）；S4 稿件面均本地件不入仓（双盲纪律）。"
        "（W702 补录四件套）\n"
        "> - **状态**：已落地（CI 五工作流以推送后 gh run list 为准）。（W702 补录）\n"
        "\n"
        "### v2.3.278",
        "v2.3.279 补录文件/状态",
    ),
]


def main():
    fail = 0
    for path, edits in EDITS.items():
        with open(path, encoding="utf-8", newline="") as f:
            s = f.read()
        crlf = "\r\n" in s
        for old, new, label in edits:
            o, n = old, new
            if crlf:
                o = old.replace("\n", "\r\n")
                n = new.replace("\n", "\r\n")
            cnt = s.count(o)
            if cnt != 1:
                print("[FAIL] %s :: %s :: 命中 %d" % (path, label, cnt))
                fail += 1
                continue
            s = s.replace(o, n, 1)
            print("[OK] %s :: %s" % (path, label))
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(s)
    if fail:
        print("TOTAL FAIL %d" % fail)
        return 1
    print("ALL EDITS APPLIED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
