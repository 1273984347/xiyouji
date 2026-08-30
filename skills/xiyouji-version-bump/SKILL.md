---
name: xiyouji-version-bump
description: 西游记项目（D:\1\xiyouji）版本 bump 与六文档同步标准流程 playbook。步骤：预检记录规模描述 → 改 dukou-engine 长链页脚 → 写 CHANGELOG/交接文档/file-index → 跑 bump_version.py → 手动补回规模描述（bump_version.py --desc 会吞掉版本行的"共 N 篇"/"A4 209 篇"——值随批次校正、以 README 版本行与 verify 输出为准，当前 N=615，不补回则 verify_delivery 报 FAIL）→ verify_delivery 全绿 → 收尾三同步（AGENTS 脚注/路线图状态段/方案档 §10 回填，W494 固化）→ git add -u → commit/push。当用户要求"版本 bump"、"升版本"、"W 批次同步"、"六文档同步"、"发新版本"、"version bump"、"W### 提交"时触发。
version: 1.4.0
---

# 西游记项目版本 Bump 与六文档同步

给 xiyouji 项目（`D:\1\xiyouji`）发新版本的固定流程。每个 W 批次都要重跑一遍，含一个非显而易见的工具陷阱（见「陷阱清单」），必须逐字执行。

## 何时触发

触发（正向）：

- 用户要求"版本 bump"、"升版本"、"发新版本"、"W 批次同步"、"六文档同步"。
- 用户说"W### 提交"、"把这批改动提交并升版本"。
- 一轮内容/工程改动完成后，需要走 verify_delivery + 版本号推进 + commit/push 收尾。

排除（反向）：

- 只改内容、不涉及版本号推进的普通编辑，不需要走本流程。
- 尚未完成实际改动就提前想 commit，先回去把活干完。

## 前置条件

- 项目在 `D:\1\xiyouji`，git 分支 `main`，remote `origin`。
- 六文档清单（本流程要动的全部文件）：

| 文档 | 路径 | 用途 |
|---|---|---|
| CHANGELOG | `CHANGELOG.md` | 批次四件套条目（核心门禁 hard gate） |
| 交接文档 | `交接文档.md` | 跨 session 主入口（核心门禁 hard gate） |
| README | `README.md` | 版本行 + 规模描述 |
| STRUCTURE | `STRUCTURE.md` | 版本行 + 规模描述 |
| 项目说明 | `docs/00-导读/项目说明.md` | 版本行 + 规模描述 |
| file-index | `scripts/output/file-index.md` | 文件变更索引表 |

- 关键脚本：`scripts/bump_version.py`（同步）、`scripts/verify_delivery.py`（门禁）。

## 标准流程（预检 + 九步）

严格按顺序执行，不要跳步。

### 第 0 步：预检——记录当前规模描述

跑任何改动作前，先用 grep 抓取并**记下当前版本行里的规模描述确切字符串**（`A1-A6 共 N 篇 + M 可视化页（A4 X 篇 已含）`）：

```bash
cd /d/1/xiyouji && grep -h "当前版本" README.md STRUCTURE.md docs/00-导读/项目说明.md
```

把三段完整版本行抄下来（至少记下规模描述这段）。这串数字会在第 5 步被 `bump_version.py --desc` 吞掉，必须靠这里记下的原文在第 6 步原样补回。**没做预检就不准跑 bump。**

**预检附加项（W534 立）**：用 grep 取页脚链首判断「页脚是否滞后」时，必须用 `head` 取**首个**匹配，不能用 `tail`——

```bash
cd /d/1/xiyouji && grep -o 'v2\.3\.[0-9]* W[0-9]\{3\}' site/dukou-engine.html | head -2   # 链首 = 现役
```

长链页脚是「新在前·旧在后」，`tail` 取到的是**最旧**条目。W534 实证：误用 `tail -3` 把链尾的 `v2.3.128 W529` 读成当前版本，凭此报出「页脚滞后 4 批」的**假漂移**（实际链首 `v2.3.132 W533` 与现役一致，页脚零滞后）。**报页脚类漂移前先确认取的是链首。**

### 第 1 步：改 dukou-engine 长链页脚

`bump_version.py` 从 `site/dukou-engine.html` 的 footer 读当前 v/W，所以**必须先改 footer 再跑脚本**。

用 Read 读 `site/dukou-engine.html` 的 footer 区域（长链页脚），在版本链最前端插入新版本，格式：

```
<footer>佛法=AI · 缘起即算法 · v新 W新 <本次批次一句话描述> · v旧 W旧 <旧描述> ...
```

只 prepend，不动历史链。

### 第 2 步：写 CHANGELOG 新批次条目

在 `CHANGELOG.md` 归档说明之后、旧版本条目之前，插入新 `### v新（date）：W新 <描述>` 段，按「来源 / 文件 / 验证 / 状态」四件套写，10-20 行。

### 第 3 步：写交接文档

`交接文档.md` 至少改 6 处：顶部「最后更新」行、阻塞段状态、已完成里程碑概要、当前进度标题、当前版本号段（v / W / Git HEAD / 下一 W）、文末「最后更新」行。

### 第 4 步：写 file-index

在 `scripts/output/file-index.md` 顶部插入新 `## W新 <描述>（date·v新）` 段，含文件表格（文件 / W / 说明）。

### 第 5 步：跑 bump_version.py

```bash
cd /d/1/xiyouji && python scripts/bump_version.py --desc "W新 <描述>" --note "W新 <描述>"
```

脚本会读 footer（第 1 步已改），同步 README/STRUCTURE/项目说明 的版本行、W 范围，以及 index/cross-time-danmaku/tag-cloud 简单页脚。**它不会**写 CHANGELOG 完整条目，也**不会**改 dukou-engine footer（这两样靠前面手写）。

### 第 6 步：手动修复版本行（陷阱，必做）

`bump_version.py --desc` 会**吞掉版本行里的规模描述**（如 `A1-A6 共 615 篇 + 86 可视化页（A4 209 篇 已含）`），同时**日期保持旧值**。若不补回，`verify_delivery` 会报 FAIL（`A4 计数不一致（缺 '209 篇'）`）。

跑完脚本后逐处核改三份文档的版本行，共四个子项：

1. **补回规模描述 + 日期**：`README.md`、`STRUCTURE.md`、`docs/00-导读/项目说明.md` 三处版本行的规模描述被吞、日期停留旧值，需手动补回并改成当天。规模描述以第 0 步预检记下的原文为准，不要凭空编。
2. **重写 STRUCTURE.md 版本行（修复畸形尾巴）**：bump 对 STRUCTURE.md 版本行的处理是**追加** ` + W4xx（W4xx 描述）` 到行尾，而非替换旧 W 描述（旧描述滞留、新描述残缺）。整行重写为干净格式：`> 当前版本：v2.3.XX（date）— W4xx <描述> — A1-A6 共 615 篇 + 86 可视化页（A4 209 篇 已含）·详细变更见 [CHANGELOG.md](CHANGELOG.md)。`
3. **核改项目说明 :45 第二处版本行**：`docs/00-导读/项目说明.md` 第 45 行附近有第二处 `- **当前版本**：vX.Y.Z（date）— ...` 行（头部版本行之外），bump **完全不更新**它，需手动核改版本号与日期。
4. **核对三简单页脚链首描述与历史条目（坑④，W531 立·W532 复现）**：`bump_version.py` 对 `site/index.html`、`site/data/cross-time-danmaku.html`、`site/data/tag-cloud.html` 的简单页脚是**原地替换链首的 `vX.Y.Z · W###` 数字**，描述文本会**滞留上一批文案**（W531 实测链首变成 `v2.3.131 · W532 skills 部署全查…` 这类错配，W532 再次复现），且上一批条目被原地顶掉、历史链静默断裂。`verify_delivery` 不校验这三处（WARN 级盲区）。正解：把链首描述改写为本批一句话，并手动 prepend 上一批条目回历史链，然后 Grep 复核。

### 第 7 步：verify_delivery 全绿

```bash
cd /d/1/xiyouji && python scripts/verify_delivery.py
```

确认全绿：CSP / 腐蚀 / 数据漂移 / sitemap / A1 导航 / 计数（A4 `209 篇` 必须在 PASS）。CHANGELOG + 交接文档 是 hard gate，README/STRUCTURE/项目说明/file-index 是 WARN，仍要保证无 FAIL。

### 第 8 步：收尾三同步（W494 教训固化，缺任一项 = P1）

六文档之外，每批必须同步三处，commit 前逐项 Grep 验证（E1 铁律：不信任自己刚写的声明）：

0. **同步范围受归属策略约束（W533）**：`sync_skills.py --sync` 只覆盖 xiyouji-* 等「仓库为真源」的技能；四个通用会话流程 skill（agent-session-loop / deep-review-loop / mem-wrap-up / self-evolution）的 master 在全局安装版、仓库副本为镜像，改它们须改全局后用 `--take-global` 回写仓库，**不得** --sync（工具已按 MIRROR_SKILLS 强制拦截）。
1. **AGENTS.md 结构变更 + 版本脚注**：若本批改了门禁/新增或改名 skill/改了流程，同步 AGENTS.md 对应章节（§4.2 门禁清单 / §4.5 skills 清单），并把文末版本脚注更新为 `vX.Y.Z W###` 与本次 bump 一致（用 `git rev-parse --short HEAD` 核对口径）。改技能清单时同步 `skills/README.md` 索引计数。**改/新增任何 skill 后必须：`python scripts/sync_skills.py --sync` 同步全局安装版（仓库为真源）+ `python scripts/check_skills_index.py` 过索引门禁（已挂 verify_delivery，漏同步会直接 FAIL）。**
2. **路线图状态段回写**：`docs/superpowers/plans/` 下本批对应的方案档，若含状态段/§10 落地状态表，补上本次执行批次的状态（✅ + commit）。
3. **方案档落地状态回填**：本批方案档 §8/§10 里声称"已落地"的每一项，实测存在后回填 commit；漏回填 = 下批 day-review 会抓 P1。

> 教训出处：W494（2026-08-22）用户"文档同步你做了吗"指出 AGENTS 脚注 / 路线图状态段 / 方案档 §10 三处遗漏后固化。day-review skill 的步骤 4 是这三处的检查者，本步是执行者，二者配对。

### 第 9 步：git add -u → commit → push

```bash
cd /d/1/xiyouji && git status --short        # 先看清改动 + untracked
cd /d/1/xiyouji && git add -u                 # 只暂存 tracked 修改
cd /d/1/xiyouji && git status --short | grep '^??'   # 确认 untracked 未入暂存
```

项目约定「工具不入库」：`git add -u` 只暂存已跟踪文件的修改，排除未跟踪的审查脚本/截图。commit message 用 `feat(wXXX): <描述> — <关键点>` + 要点列表，最后 `git push origin main`。

## 陷阱清单

- **跳过第 0 步预检**：没记下当前规模描述原文就跑 bump，第 6 步只能凭记忆补，极易补错数字导致 verify_delivery FAIL。预检是强制前置。
- **bump_version.py --desc 吞规模描述**：这是最常踩的坑。跑脚本后必须手动补回 README/STRUCTURE/项目说明 三处规模描述，否则 verify_delivery FAIL。（W459 实测：v2.3.74 批次该坑未复现——规模描述被保留，疑似与版本行既有格式有关；预检与跑后核对仍必须每次执行，不可凭单次经验跳过。）
- **项目说明头部版本行无加粗**：`docs/00-导读/项目说明.md` 头部版本行格式为 `> 当前版本 vX.Y.Z（date）：`（无 `**` 加粗，与 README 的 `> **当前版本 ...**` 不同），脚本替换时匹配串要区分。
- **STRUCTURE 版本行追加畸形尾巴**：bump 对 STRUCTURE.md 版本行是**追加** ` + W4xx（W4xx 描述）` 而非替换旧描述（旧 W 描述滞留、新描述残缺），需重写整行，否则版本行格式畸形且描述错误。
- **项目说明 :45 第二处版本行漏改**：`docs/00-导读/项目说明.md` 第 45 行附近的 `- **当前版本**：...` 行（头部版本行之外的第二处）bump **完全不更新**，需手动核改版本号 + 日期。
- **日期不更新**：bump_version 不刷新版本行日期，需手动改成当天。
- **bump 简单页脚描述滞留（坑④，W531/W532 双复现）**：三简单页脚链首只换 v/W 数字、描述留在上一批，且历史条目被原地顶掉；verify 不校验，必须跑完 bump 手动 Grep `v新 · W新` 核描述并补回上一批条目。
- **顺序不能乱**：footer 必须先改，脚本才读得到新 v/W；CHANGELOG/交接文档/file-index 的完整条目脚本不会代写。
- **漏收尾三同步（W494 教训）**：只做六文档不查 AGENTS 脚注 / 路线图状态段 / 方案档 §10，会被下批 day-review 抓 P1。第 8 步三同步是强制步骤，不是可选。
- **git add -u 而非 git add .**：避免把「工具不入库」的 untracked 文件误提交。
- **Edit 前先 Read**：文件被脚本改动过后，Edit 会报 "File has been modified since read"，需重新 Read 再改。
- **多行中文 commit message 在 Git Bash 下必须传 Windows 路径（坑⑤，W534 立）**：`git commit -F /c/Users/.../msg.txt` 会报 `fatal: could not read log file`——Git Bash 的 POSIX 路径（`/c/...`）不会自动转换给 Windows 版 git.exe。正解：`git commit -F "C:/Users/12739/AppData/Local/Temp/msg.txt"`（先 Write 临时文件 → 提交 → 删除）。多行中文提交信息一律走临时文件 + `-F`，不走 shell heredoc（E34）。
- **取页脚链首误用 `tail` 会造出假漂移（W534 实证）**：见第 0 步预检附加项。报「页脚滞后」类结论前必须 `head` 复核链首。
- **裁剪交接文档膨胀前必须逐批断言 + 归一化比对（坑⑧，W534 立）**：里程碑概要与「一、当前进度」标题会随批次无限堆叠（W534 时标题已达 8509 字符 / 概要 29 版）。裁剪属删除历史，**必须先脚本化断言每个将删 W### 在 CHANGELOG 三件套（现役 / CHANGELOG-ARCHIVE.md / docs/archive/CHANGELOG-ARCHIVE-tier2.md）有对应版本段**，断言全过再 `--apply`（dry-run 先行）。两个实证陷阱：① 标题条目锚点必须用 `v2\.3\.\d+ W(\d{3})` 按条目切分——用裸 `W\d{3}` 会被描述正文内嵌的 W 号污染（111 个真实条目误判为 132 个）；② W 号比对前必须归一化（里程碑侧捕获带 `W` 前缀、标题侧只有数字），否则会造出「断言全过 / 全不过」的假结果。末块行范围会延伸到段尾空行，回退掉尾部空行以保留「列表 → 空行 → 注记」的 Markdown 衔接。
- **改完交接文档长行后必须整行复读（W534 实证）**：第 3 步改「一、当前进度」标题时，若 old_string 只截取标题前缀而 new_string 未把被截掉的旧版本描述拼回，会**静默吞掉上一批描述**（本次误删「v2.3.132 W533 skills 归属策略显式化」片段，靠事后 python 打印整行复核才捕获）。长行编辑一律：Edit 后立刻打印整行前 260 字符核对。

## 完成验证清单

- [ ] 第 0 步预检已记录当前规模描述原文
- [ ] 第 0 步附加项：页脚链首用 `head` 复核（未用 `tail` 误判）
- [ ] dukou-engine footer 已插入新 v/W
- [ ] 六文档均已更新且版本一致
- [ ] 三处版本行规模描述已补回、日期正确
- [ ] STRUCTURE 版本行无「+ W4xx」畸形尾巴、项目说明第二处「当前版本」行已核改
- [ ] 三简单页脚（index/cross-time-danmaku/tag-cloud）链首描述==本批、上一批条目已补回历史链（坑④）
- [ ] `verify_delivery.py` 全绿，无 FAIL
- [ ] 收尾三同步完成：AGENTS.md 结构/脚注（含 skills/README 计数）、路线图状态段、方案档 §10 均 Grep 验证落地
- [ ] `git add -u` 后 untracked 文件仍未被暂存
- [ ] commit 已建、push 到 origin main 成功

详细模板（footer 格式、四件套条目、规模描述固定串、commit message 等）见 `reference.md`。
