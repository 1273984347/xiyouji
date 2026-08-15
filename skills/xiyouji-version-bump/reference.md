# 西游记版本 Bump 参考模板与细节

本文件是 `SKILL.md` 的补充，存放逐字可抄的模板、六文档确切锚点、坑位机理与当前已知规模值。执行时以项目当前实际值为准，本文档数值只作基准参照。

## 六文档锚点（读改前先定位）

| 文档 | 关键锚点 |
|---|---|
| `CHANGELOG.md` | 顶部归档说明 `> **历史版本归档**...` 之后，旧版本 `### v2.3.XX` 之前 |
| `交接文档.md` | 顶部 `> 最后更新：`；阻塞段 `零、当前阻塞`；`## 一、当前进度（...`；`### 已完成里程碑概要`；`### 当前版本号`（含 Git HEAD / W### 已用到 / 下一版本段）；文末 `最后更新：` |
| `README.md` | `> **当前版本 vX.Y.Z（date）**：...` |
| `STRUCTURE.md` | `> 当前版本：vX.Y.Z（date）— ...` |
| `docs/00-导读/项目说明.md` | 头部 `> 当前版本 vX.Y.Z（date）：...` 及 :45 附近的第二处 `- **当前版本**：...`（bump 漏改，需手动核改版本号 + 日期） |
| `scripts/output/file-index.md` | 顶部 `---` 之后、旧 `## WXXX ...` 之前 |

## 长链页脚格式（dukou-engine.html）

```
<footer>佛法=AI · 缘起即算法 · v2.3.40 W425 GoatCounter 真实跨访客统计接入（...）· v2.3.39 W424 ... · v2.3.37 W422 ... · ...</footer>
```

新版本 prepend 在 `缘起即算法 · ` 之后、旧版本之前，格式 `v新 W新 <一句话描述> · `。

## 规模描述固定串（bump_version.py 会吞掉的）

当前基准（W425 时）：

```
A1-A6 共 611 篇 + 86 可视化页（A4 209 篇 已含）
```

其中分项：A1 逐回 100 / A2 44 / A3 211 / A4 209 / A5 34 / A6 13，合计 611；可视化 86 页；dataset 41。

**执行要点（对应 SKILL.md 第 0 步预检）**：跑任何改动作前，先抓取三段版本行原文并记下规模描述确切字符串，跑完 bump 后原样补回，不要凭记忆写数字。

```bash
cd /d/1/xiyouji && grep -h "当前版本" README.md STRUCTURE.md docs/00-导读/项目说明.md
```

## CHANGELOG 四件套条目模板

```markdown
### v2.3.40（2026-08-14）：W425 GoatCounter 真实跨访客统计接入 — 全站 160 页注入 + CSP 白名单 + _headers 同步

> **来源**：用户完成 GoatCounter 注册（site code `1273984347`），按 [访问统计方案](docs/00-导读/访问统计方案.md) 把注入脚本落地。
> - **执行（注入）**：`scripts/inject_goatcounter.py --site 1273984347` 全站 160 页注入。
> - **执行（CSP）**：`generate_csp.py` 白名单追加 gc.zgo.at（script-src）+ 1273984347.goatcounter.com（connect-src），重生成 159 页 CSP，680 内联哈希 0 漂移。
> - **文件**：scripts/generate_csp.py、site/_headers、site/**/*.html（160 页）、六文档。
> - **验证**：verify_delivery 核心全绿（CSP/腐蚀/数据漂移/sitemap/A1 导航/计数 611）。
> - **状态**：已 commit 933a688、已 push origin/main。
```

四件套 = 来源（为什么做）/ 文件（改了什么）/ 验证（怎么验证的）/ 状态（是否已提交）。

## 交接文档 6 处改法

1. 顶部「最后更新」：prepend `2026-08-14（v2.3.40 W425 ...）·`
2. 阻塞段：把已解决的事项状态更新（如 GoatCounter 从"待注册"改为"已接入，待流量回传"）
3. 已完成里程碑概要：插入 `- **v新 W新 <描述>（date）**：` 里程碑块
4. 当前进度标题：prepend 新版本到 `## 一、当前进度（` 之后
5. 当前版本号段：更新 `- **v新**（date）`、`Git HEAD`、`W### 编号已用到 **W新**`、`下一版本段编号：**W新+1**`
6. 文末「最后更新」：prepend 新条目

## file-index 表格模板

```markdown
## W425 GoatCounter 真实跨访客统计接入（2026-08-14·v2.3.40）

| 文件 | W | 说明 |
|---|---|---|
| scripts/generate_csp.py | W425 | v2.3.40 修改·EXTERNAL_SCRIPT_HOSTS 追加 gc.zgo.at + connect-src 追加计数端点 |
| site/_headers | W425 | v2.3.40 修改·Netlify/CF CSP 白名单同步 |
| site/**/*.html（160 页） | W425 | v2.3.40 批量注入 GoatCounter 计数脚本 |
```

## bump_version.py 行为细节

- 入口：`python scripts/bump_version.py [--version X.Y.Z] [--w WXXX] [--desc "..."] [--note "..."]`
- 默认从 `site/dukou-engine.html` footer parse 当前 v/W。
- `--desc`：替换版本行的主描述 → **吞掉规模描述**；对 STRUCTURE.md 版本行是**追加** ` + W4xx（W4xx 描述）` 畸形尾巴而非替换旧描述（W448 实测），需手动重写整行。
- `--note`：设置 file-index 里程碑标题（缺省用 w）。
- 会同步：SYNC_DOCS（README/STRUCTURE/项目说明/file-index/交接文档/CHANGELOG 的 W 范围 + index/cross-time-danmaku/tag-cloud 简单页脚）、AUX_VERSION_DOCS（README/STRUCTURE/项目说明 版本行）。
- **不会**：写 CHANGELOG 完整条目、改 dukou-engine footer、更新日期、更新 `docs/00-导读/项目说明.md` 的 `- **当前版本**：` 第二处版本行（:45 附近，需手动核改）。

## verify_delivery.py 门禁口径

- hard gate（FAIL 即挡）：CHANGELOG + 交接文档（版本号/条目存在）。
- WARN（仍需修到无 FAIL）：README/STRUCTURE/项目说明/file-index 版本行、A4 计数「209 篇」、A1 导航邻接、sitemap 覆盖、site/data fallback、数据漂移、CSP 漂移、腐蚀门禁。
- 计数口径：A1-A6 合计 611（A4 209），可视化 86 页，dataset 41。

## commit message 模板

```
feat(w425): GoatCounter 真实跨访客统计接入 — 全站 160 页注入 + CSP 白名单 + _headers 同步

- inject_goatcounter.py --site 1273984347 全站 site/**/*.html 160 页注入计数脚本
- generate_csp.py 外部脚本白名单追加 gc.zgo.at + connect-src 追加计数端点，重生成 159 页 CSP（680 哈希 0 漂移）
- site/_headers Netlify/CF CSP 白名单同步
- 版本 v2.3.39 W424 → v2.3.40 W425 + 六文档同步
- verify_delivery 核心全绿（CSP/腐蚀/数据漂移/sitemap/A1 导航/计数 611）
```

## 项目协作约定

- 「工具不入库」：审查脚本（如 `_csp_check.js`、`quality_review.py`）、截图产物等 untracked 文件**有意不提交**，用 `git add -u` 只暂存 tracked 修改。
- `交接文档.md` 是跨 session 主入口，每轮 bump 必须同步。
- 远程：`github.com/1273984347/xiyouji.git`，分支 `main`。
