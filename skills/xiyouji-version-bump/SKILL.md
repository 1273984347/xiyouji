---
name: xiyouji-version-bump
description: 西游记项目（D:\1\xiyouji）版本 bump 与六文档同步标准流程 playbook。步骤：预检记录规模描述 → 改 dukou-engine 长链页脚 → 写 CHANGELOG/交接文档/file-index → 跑 bump_version.py → 手动补回规模描述（bump_version.py --desc 会吞掉版本行的"共 611 篇"/"A4 209 篇"，导致 verify_delivery 报 FAIL）→ verify_delivery 全绿 → 收尾三同步（AGENTS 脚注/路线图状态段/方案档 §10 回填，W494 固化）→ git add -u → commit/push。当用户要求"版本 bump"、"升版本"、"W 批次同步"、"六文档同步"、"发新版本"、"version bump"、"W### 提交"时触发。
version: 1.1.0
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

`bump_version.py --desc` 会**吞掉版本行里的规模描述**（如 `A1-A6 共 611 篇 + 86 可视化页（A4 209 篇 已含）`），同时**日期保持旧值**。若不补回，`verify_delivery` 会报 FAIL（`A4 计数不一致（缺 '209 篇'）`）。

跑完脚本后逐处核改三份文档的版本行，共三个子项：

1. **补回规模描述 + 日期**：`README.md`、`STRUCTURE.md`、`docs/00-导读/项目说明.md` 三处版本行的规模描述被吞、日期停留旧值，需手动补回并改成当天。规模描述以第 0 步预检记下的原文为准，不要凭空编。
2. **重写 STRUCTURE.md 版本行（修复畸形尾巴）**：bump 对 STRUCTURE.md 版本行的处理是**追加** ` + W4xx（W4xx 描述）` 到行尾，而非替换旧 W 描述（旧描述滞留、新描述残缺）。整行重写为干净格式：`> 当前版本：v2.3.XX（date）— W4xx <描述> — A1-A6 共 611 篇 + 86 可视化页（A4 209 篇 已含）·详细变更见 [CHANGELOG.md](CHANGELOG.md)。`
3. **核改项目说明 :45 第二处版本行**：`docs/00-导读/项目说明.md` 第 45 行附近有第二处 `- **当前版本**：vX.Y.Z（date）— ...` 行（头部版本行之外），bump **完全不更新**它，需手动核改版本号与日期。

### 第 7 步：verify_delivery 全绿

```bash
cd /d/1/xiyouji && python scripts/verify_delivery.py
```

确认全绿：CSP / 腐蚀 / 数据漂移 / sitemap / A1 导航 / 计数（A4 `209 篇` 必须在 PASS）。CHANGELOG + 交接文档 是 hard gate，README/STRUCTURE/项目说明/file-index 是 WARN，仍要保证无 FAIL。

### 第 8 步：收尾三同步（W494 教训固化，缺任一项 = P1）

六文档之外，每批必须同步三处，commit 前逐项 Grep 验证（E1 铁律：不信任自己刚写的声明）：

1. **AGENTS.md 结构变更 + 版本脚注**：若本批改了门禁/新增或改名 skill/改了流程，同步 AGENTS.md 对应章节（§4.2 门禁清单 / §4.5 skills 清单），并把文末版本脚注更新为 `vX.Y.Z W###` 与本次 bump 一致（用 `git rev-parse --short HEAD` 核对口径）。改技能清单时同步 `skills/README.md` 索引计数。
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
- **顺序不能乱**：footer 必须先改，脚本才读得到新 v/W；CHANGELOG/交接文档/file-index 的完整条目脚本不会代写。
- **漏收尾三同步（W494 教训）**：只做六文档不查 AGENTS 脚注 / 路线图状态段 / 方案档 §10，会被下批 day-review 抓 P1。第 8 步三同步是强制步骤，不是可选。
- **git add -u 而非 git add .**：避免把「工具不入库」的 untracked 文件误提交。
- **Edit 前先 Read**：文件被脚本改动过后，Edit 会报 "File has been modified since read"，需重新 Read 再改。

## 完成验证清单

- [ ] 第 0 步预检已记录当前规模描述原文
- [ ] dukou-engine footer 已插入新 v/W
- [ ] 六文档均已更新且版本一致
- [ ] 三处版本行规模描述已补回、日期正确
- [ ] STRUCTURE 版本行无「+ W4xx」畸形尾巴、项目说明第二处「当前版本」行已核改
- [ ] `verify_delivery.py` 全绿，无 FAIL
- [ ] 收尾三同步完成：AGENTS.md 结构/脚注（含 skills/README 计数）、路线图状态段、方案档 §10 均 Grep 验证落地
- [ ] `git add -u` 后 untracked 文件仍未被暂存
- [ ] commit 已建、push 到 origin main 成功

详细模板（footer 格式、四件套条目、规模描述固定串、commit message 等）见 `reference.md`。
