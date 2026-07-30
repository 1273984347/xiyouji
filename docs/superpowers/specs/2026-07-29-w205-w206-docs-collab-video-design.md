# W205+W206 两方向并行设计 spec

**日期**：2026-07-29
**状态**：已批准（方案 A 全范围）
**作者**：主代理 + 用户协作

---

## 背景

第二波剩余两方向（文档协作 / 视频化）并行落地。W205 文档协作方向目标场景为"AI 代理协作（subagent 模板）"，W206 视频化方向目标形式为"短 + long 并行（多视频架构）"。

---

## W205 文档协作方向设计

### 目标

建立 AI 代理友好的文档协作体系，让 subagent 能并行产出高质量文档，降低主代理验证成本。

### 交付物（4 项）

1. **`docs/_templates/` 目录新建**（AI 代理文档模板包）：
   - `article-template.md`：新文档骨架（标题/元信息/双索引链接/章节/脚注/W### ID 占位）
   - `handoff-checklist.md`：subagent 交接清单（8 项自检）
   - `validation-checklist.md`：主代理验证 checklist（6 项 spot-check）

2. **`docs/00-导读/项目说明.md` "如何参与"段落重写**：
   - 从 3 行扩展到 AI 代理协作流程说明
   - 文档模板引用 + 交接 checklist 引用 + 命名规范

3. **各 docs/ 子目录 README 骨架**（00-09 共 10 个）：
   - 目录定位 + 文件命名规范 + 双索引链接格式 + 模板引用

4. **`CONTRIBUTING.md` 新建**（替换 README 占位）：
   - AI 代理协作流程 + 模板引用 + 验证 checklist + 三件套同步要求

### 不包含

- PR workflow / CODEOWNERS / 分支策略（AI 代理协作不需要）

---

## W206 视频化方向设计

### 目标

建立多视频架构，落地 1 短视频样例 + 1 longer-form 样例 + MP4 导出 pipeline，为后续视频系列扩展奠定基础。

### 交付物（5 项）

1. **`hyperframes/` 多视频架构改造**：
   - `hyperframes/compositions/` 目录新建
   - 现有 `index.html` 移入并重命名为 `methodology-sharing.html`（同步 v2.2.22→v2.2.27）
   - `hyperframes/compositions/d3-visualizations/` 目录新建
   - `hyperframes/package.json` 新建

2. **短视频样例（video-shortform skill 落地）**：
   - 选 `narratology-13d-network.html`（力导向图 22 节点 28 连线）
   - 输出：`hyperframes/compositions/d3-visualizations/narratology-13d-network.html`（5-8 秒）
   - 内容：标题卡 → 力导向图入场 → 节点高亮 → 结尾版本戳

3. **longer-form 样例（hyperframes skill 新 composition）**：
   - 主题：项目数据仪表盘展示（dashboard 45 KPI）
   - 输出：`hyperframes/compositions/dashboard-showcase.html`（30-45 秒）
   - 内容：项目概览 → dashboard hero → KPI 网格 → 过滤演示 → 搜索演示 → 结尾

4. **MP4 导出 pipeline**：
   - `hyperframes/package.json` 新增 scripts：`render:short` / `render:long` / `render:all`
   - 使用 hyperframes-cli render 命令
   - 输出至 `hyperframes/output/*.mp4`

5. **文档同步**：
   - README.md 新增"视频系列"段落
   - STRUCTURE.md 新增 hyperframes/compositions/ 目录说明
   - 交接文档 S 方向新增 S5 视频化扩展

---

## 并行落地策略

两方向独立，可用 dispatching-parallel-agents 并行：
- Subagent A：W205 文档协作（4 项交付物）
- Subagent B：W206 视频化（5 项交付物）

主代理：派发后等待两 subagent 完成，再统一做 DRL R1b spot-check + 6 项目层文档同步 + mem-wrap-up 收尾。

---

## 验证策略

- W205：Grep spot-check 模板文件存在 + 内容命中 + 各子目录 README 存在
- W206：hyperframes lint + preview + render MP4 文件存在 + 文件大小合理
- DRL R1b：subagent spot-check 8 项反模式
- mem-wrap-up：Step 4a 项目层 + Step 7a memory 层

---

## 风险

1. **W206 hyperframes render 可能失败**：hyperframes-cli 环境问题 → 降级为仅 preview + 截图
2. **W205 10 子目录 README 批量成本**：可降级为仅 00-03 核心 4 个
3. **两方向并行可能资源竞争**：两 subagent 不修改同一文件，无竞态

---

## 后续扩展

- W205 后续：基于模板包扩展 subagent 任务派发 SOP
- W206 后续：基于多视频架构扩展完整视频系列（5+ 短 + 3+ long）
