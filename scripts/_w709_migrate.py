# -*- coding: utf-8 -*-
"""W709 一次性：AGENTS 分层搬迁（BL-24 按图施工）——§4.2/§4.3/§4.4 迁 L2 + BL-23 脚注归档。

守恒断言：40 门禁条目/31 坑位条目/§4.4 全文/脚注条目数——迁移前后计数一致才落盘。
"""
import io
import re

P = "AGENTS.md"
s = io.open(P, encoding="utf-8", newline="").read()
assert "\r" not in s, "混行尾——先归一"
nl = "\n"
lines = s.split(nl)

# ---------- 定位三节 ----------
i42 = next(i for i, l in enumerate(lines) if l.startswith("### 4.2 "))
i43 = next(i for i, l in enumerate(lines) if l.startswith("### 4.3 "))
i44 = next(i for i, l in enumerate(lines) if l.startswith("### 4.4 "))
i5 = next(i for i, l in enumerate(lines) if l.startswith("## 5. "))

sec42 = lines[i42:i43]
sec43 = lines[i43:i44]
sec44 = lines[i44:i5]

# ---------- §4.2：前言 + 40 条 ----------
# 前言=标题到第一条「1. **」之间（含契约与 scope 段）
i_first_gate = next(i for i, l in enumerate(sec42) if re.match(r"^1\. \*\*", l))
preamble42 = sec42[:i_first_gate]
gate_lines = sec42[i_first_gate:]
gates = [l for l in gate_lines if re.match(r"^\d+\. \*\*", l)]
assert len(gates) == 40, len(gates)

# ---------- §4.3：31 条 ----------
tip_idx = [i for i, l in enumerate(sec43) if l.startswith("- **") or l.startswith("-  **")]
assert len(tip_idx) == 31, len(tip_idx)
tips = []
for k, i in enumerate(tip_idx):
    end = tip_idx[k + 1] if k + 1 < len(tip_idx) else len(sec43)
    tips.append(sec43[i:end])
assert len(tips) == 31

# 六主题分组（索引按 §4.3 条目原序）
GROUPS = [
    ("CSS / 视觉渲染", [1, 13, 14, 16, 17, 26, 27, 28, 29]),
    ("JS / CSP / 运行时", [0, 18, 25]),
    ("git / 提交 / 并发", [5, 6, 8, 9, 12, 22, 11]),
    ("级联 / CHANGELOG", [3, 4, 15, 21]),
    ("数据 / 内容可信度", [2, 7, 19, 24]),
    ("流程 / 协作 / 取证", [10, 20, 23, 30]),
]
flat = [i for _, idx in GROUPS for i in idx]
assert sorted(flat) == list(range(31)), "分组索引未守恒"

# ---------- 生成 gates.md ----------
g42_title = "### 4.2 交付门禁体系（verify_delivery.py，pre-commit 强制）"
gate_groups = [("内容与同步类（1-5）", 0, 5), ("结构与加载类（6-11）", 5, 11), ("声明与完整性类（12-15）", 11, 15), ("数据与一致性类（16-26）", 15, 26), ("编号与质量防线类（27-40）", 26, 40)]
gates_md = [
    "# 交付门禁体系全量定义（40 槽 · L2 主题层 · W709 自 AGENTS §4.2 迁入）",
    "",
    "> **📖 阅读契约（W709）**：查表型——改 site/、加门禁、动 verify_delivery.py 时按编号查；每条含完整口径与历史实证；编号与 AGENTS §4.2 摘要一一对应。",
    "> **何时读**：门禁失败要懂原因 / 新增门禁要挂槽 / 复核某条防线范围。**读完你应该能**：说出任一槽位拦什么、豁免与基线在哪。",
    "",
    "## 何时触发速查",
    "",
    "| 组 | 槽位 | 主题 |",
    "|---|---|---|",
]
for name, a, b in gate_groups:
    gates_md.append("| %s | %d-%d | %s |" % (name, a + 1, b, "、".join(re.match(r"^(\d+)\. \*\*(.+?)\*\*", g).group(2)[:14] for g in gates[a:b])))
gates_md += ["", "## 完整定义", "", "以下为 AGENTS §4.2 原文全量（W709 迁入·内容零改动·仅按组分节）：", ""]
gates_md.append(preamble42[0].rstrip())
gates_md.append("")
for name, a, b in gate_groups:
    gates_md.append("### %s" % name)
    gates_md.append("")
    gates_md.extend(x.rstrip() for x in gates[a:b])
    gates_md.append("")
# 非条目行（契约/scope 说明段）
extra42 = [l.rstrip() for l in gate_lines if not re.match(r"^\d+\. \*\*", l) and l.strip() and not l.startswith(("### 4.3",))]
if extra42:
    gates_md.append("### 附：scope 分级与契约（原文）")
    gates_md.append("")
    gates_md.extend(extra42)
    gates_md.append("")
with io.open("docs/agent/gates.md", "w", encoding="utf-8", newline="") as f:
    f.write(nl.join(gates_md))
print("gates.md:", len(gates_md), "行 · 门禁 40 守恒")

# ---------- 生成 pitfalls.md ----------
pit_md = [
    "# 工具链坑位全量（L2 主题层 · W709 自 AGENTS §4.3 迁入）",
    "",
    "> **📖 阅读契约（W709）**：查表型——改 CSS/JS/git/级联/数据面踩坑排查时按主题查；每条含根因与修法。",
    "> **何时读**：同类缺陷第二次出现 / 批量修改前 / 排查静默失效。**读完你应该能**：避开全部已知坑族。",
    "",
    "## shell 场景查坑表（W706 场景分层铁律的速查面）",
    "",
    "| 场景 | 禁止 | 允许 |",
    "|---|---|---|",
    "| 写 md/文本文件 | `Set-Content` / `Add-Content` / `>` 重定向 | Write 工具或 Python `open(encoding='utf-8', newline='')` |",
    "| 多行 commit 信息 | `cat <<EOF` / 任意 shell heredoc | Write 临时文件 + `git commit -F` |",
    "| 多行复杂转义逻辑 | 任何 shell 多行（含 bash heredoc·W706 三败） | 落 Python 脚本文件再调用 |",
    "| 路径传 Python | `/c/...`（MSYS 形态） | `C:/...`（盘符形态） |",
    "| 判退出码 | PowerShell `echo $?`（是布尔） | 管道前显式取 `$?`/`$LASTEXITCODE` |",
    "| 中文路径分类 | 直接拼 git 输出 | `git -c core.quotePath=false` |",
    "| Word COM/注册表/ACL | 强行 bash | PowerShell（Windows 原生域·W615/W693 先例） |",
    "",
    "## 六主题坑位（原文全量·内容零改动）",
    "",
]
for name, idx in GROUPS:
    pit_md.append("### %s（%d 条）" % (name, len(idx)))
    pit_md.append("")
    for i in idx:
        pit_md.extend(x.rstrip() for x in tips[i])
    pit_md.append("")
with io.open("docs/agent/pitfalls.md", "w", encoding="utf-8", newline="") as f:
    f.write(nl.join(pit_md))
print("pitfalls.md:", len(pit_md), "行 · 坑位 31 守恒")

# ---------- 生成 agent-web.md ----------
aw = [l.rstrip() for l in sec44 if l.strip() and not l.startswith("### 4.4")]
agentweb_md = [
    "# Web Agent（xiyouji-agent-web/）· L2 主题层 · W709 自 AGENTS §4.4 迁入",
    "",
    "> **📖 阅读契约（W709）**：查表型——动 xiyouji-agent-web/（引擎/前端/权限）时读。",
    "",
] + aw
with io.open("docs/agent/agent-web.md", "w", encoding="utf-8", newline="") as f:
    f.write(nl.join(agentweb_md))
print("agent-web.md:", len(agentweb_md), "行")

# ---------- AGENTS 新三节 ----------
new42 = [
    "### 4.2 交付门禁体系（verify_delivery.py，pre-commit 强制 · 摘要层）",
    "",
    "> **📖 阅读契约（W709）**：索引型——本节=40 槽摘要；完整定义（口径/豁免/历史实证）→ [docs/agent/gates.md](docs/agent/gates.md)；失败排查时按编号查 gates.md。",
    "",
    "verify_delivery.py 是提交前唯一硬门禁入口（`.git/hooks/pre-commit` → 本脚本·W698 起本地传 `--scope auto` 分级，CI 与批收尾恒全量，核心 FAIL 返回非 0 阻断）。内含 40 槽，五组：",
    "",
]
for name, a, b in gate_groups:
    new42.append("**%s**：" % name)
    for g in gates[a:b]:
        m = re.match(r"^(\d+)\. \*\*(.+?)\*\*", g)
        new42.append("%s. **%s**" % (m.group(1), m.group(2)))
    new42.append("")
new42.append("**完整定义 → [docs/agent/gates.md](docs/agent/gates.md)**（原文全量·五组分节·内容零改动）。")

new43 = [
    "### 4.3 工具链要点（摘要层 · 坑位全量已迁 L2）",
    "",
    "> **📖 阅读契约（W709）**：索引型——31 条坑位按六主题迁 [docs/agent/pitfalls.md](docs/agent/pitfalls.md)（含 shell 场景查坑表）；本节保留主题视图与高频铁则。",
    "",
]
# 保留 W706 主题视图块（在 sec43 中定位）
i_tv = next((i for i, l in enumerate(sec43) if l.startswith("**主题视图")), None)
if i_tv is not None:
    i_tv_end = next(i for i in range(i_tv, len(sec43)) if not sec43[i].strip())
    new43.extend(x.rstrip() for x in sec43[i_tv:i_tv_end])
    new43.append("")
new43 += [
    "**最高频铁则（全文见 pitfalls.md）**：改内联脚本必跑 generate_csp.py；批量改 CSS/JS 验括号平衡；多行逻辑禁 shell heredoc 落 Python 文件；同文件 Edit 串行；级联后按清单 git add。",
    "",
    "**六主题目录 → [docs/agent/pitfalls.md](docs/agent/pitfalls.md)**：CSS/视觉渲染（9）· JS/CSP/运行时（3）· git/提交/并发（7）· 级联/CHANGELOG（4）· 数据/内容可信度（4）· 流程/协作/取证（4）。",
]

new44 = [
    "### 4.4 Web Agent（xiyouji-agent-web/ · 摘要层）",
    "",
    "> **📖 阅读契约（W709）**：索引型——引擎/前端/权限细节 → [docs/agent/agent-web.md](docs/agent/agent-web.md)。",
    "",
    "后端 `server/index.ts`（Express + SSE 流式 + SQLite）+ 自研 OpenAI-compatible 引擎 `server/engine/`（W680·全主流大模型端点适配）；凭证 `LLM_API_BASE`/`LLM_API_KEY`/`LLM_MODEL` 配服务端 .env；核心入口与安全边界（权限四模式/受保护路径/命令白名单）见 L2。",
]

# 组装新 AGENTS
new_lines = lines[:i42] + new42 + [""] + new43 + [""] + new44 + lines[i5:]
s_new = nl.join(new_lines)

# ---------- BL-23：脚注切分 ----------
i_fn = s_new.find("*本文件由 AGENTS 通读项目后生成于")
tail_mark = "。如与上述权威文档冲突，以权威文档为准。*"
i_fn_end = s_new.find(tail_mark)
assert i_fn != -1 and i_fn_end != -1
footnote = s_new[i_fn : i_fn_end + len(tail_mark)]
assert footnote.count("2026-") >= 50
# 切分：保留 W701 起（首现「2026-10-11（v2.3.295 W701）」），此前部分迁 ARCHIVE
i_keep = footnote.find("2026-10-11（v2.3.295 W701）")
assert i_keep > 0, "W701 锚点"
archived_part = footnote[:i_keep].rstrip().rstrip("，；")
kept_part = footnote[i_keep:]
assert archived_part.count("（v") >= 100, archived_part.count("（v")

arch_md = [
    "# AGENTS.md 版本沿革归档（W458-W700 段 · W709 自脚注迁入）",
    "",
    "> **📖 阅读契约（W709）**：禁读型——查历史沿革用 grep 关键词单段取用；W701 起仍在 AGENTS.md 脚注；本文件内容零改动（原文迁移）。",
    "",
    "以下为 AGENTS.md 版本脚注 2026-08-16（v2.3.73 W458）至 2026-10-11（v2.3.294 W700）段的原文（单行沿革链·W709 BL-23 迁入）：",
    "",
    "```text",
    archived_part,
    "```",
]
with io.open("docs/archive/AGENTS-ARCHIVE.md", "w", encoding="utf-8", newline="") as f:
    f.write(nl.join(arch_md))

new_footnote = ("*本文件由 AGENTS 通读项目后生成于 2026-08-16（v2.3.73 W458）；W458-W700 沿革已迁 "
                "[docs/archive/AGENTS-ARCHIVE.md](docs/archive/AGENTS-ARCHIVE.md)（W709 BL-23·grep 查勿通读）；" + kept_part)
s_new = s_new[:i_fn] + new_footnote + s_new[i_fn_end + len(tail_mark) :]

with io.open(P, "w", encoding="utf-8", newline="") as f:
    f.write(s_new)
print("AGENTS 新行数:", s_new.count("\n") + 1, "（原 292）")
print("脚注保留条目数（W701+）:", kept_part.count("（v"))
print("DONE")
