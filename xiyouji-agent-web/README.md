# 西游记·渡口问津（xiyouji-agent-web）

基于 **CodeBuddy Agent SDK** 构建的 Web Agent 应用，**已适配本地项目 `D:\1\xiyouji`（详解西游记）**。

打开浏览器即可与「渡口问津」对话：让它检索某回解读、回答佛道思想/诗词/人物问题、运行 `scripts/` 下的 Python 分析脚本、生成可视化，或协助撰写 `docs/` 文档。

## 它和原模板有何不同（适配点）

- **默认工作目录**：后端 `PROJECT_CWD` 与前端「新对话」输入框默认指向 `D:/1/xiyouji`，Agent 直接在该项目上读写与执行。
- **专属 Agent**：默认 Agent「西游记·渡口问津」内置项目结构说明与行为准则的系统提示词（sysprompt），开箱即用，无需手动配置。
- **默认权限模式**：`acceptEdits`（W411 安全加固：默认不做 bypassPermissions，文件编辑自动批准、Bash 等高风险操作仍需人工确认）。新对话时可在底部切换；`bypassPermissions` 需服务端显式 `AGENT_WEB_ALLOW_BYPASS=1` 才生效。
- **界面标识**：应用名「西游记·渡口问津」、Logo「西」、主题色取项目古典红 `#c8463a`。

## 技术栈

- 后端：Node.js + Express + TypeScript（SSE 流式 + SQLite 持久化）
- 前端：React 18 + Vite + TDesign React + Tailwind
- AI：CodeBuddy Agent SDK（`@tencent-ai/agent-sdk`）

## 快速开始

### 1. 安装依赖
```bash
cd D:/1/xiyouji/xiyouji-agent-web
npm install
```

### 2. 配置 CodeBuddy 凭证
```bash
cp .env.example .env
# 编辑 .env，填入 CODEBUDDY_API_KEY
```
也可在应用「设置」页粘贴 API Key，或直接用 `codebuddy login` 的 CLI 登录态。

### 3. 启动
```bash
npm run dev
```
同时拉起后端（:3000）与前端（:5173）。访问 http://localhost:5173

## 使用建议

- **问答 / 检索**：直接问「第 27 回讲了什么」「孙悟空与菩提祖师的关系」「心猿指什么」，Agent 会引用 `docs/`、`source/` 路径。
- **运行分析**：「用 scripts/B_人物 下的共现脚本分析前 20 回人物关系」，Agent 会在 `D:/1/xiyouji` 下执行并把结果写入 `dataset/`。
- **写文档**：「给 03-主题与情节专题 补一篇关于‘紧箍咒’的短文」，Agent 会遵循 `docs/00-导读/文档规范.md`。
- **工作目录**：新建对话时可指定 `PROJECT_CWD` **内的子目录**（W411 起仅允许项目根内，防目录穿越）；项目外目录不受支持，需改 `.env` 的 `PROJECT_CWD` 后重启。

## 安全提示（W411 P0-1 加固）

- **仅回环监听**：后端绑定 `127.0.0.1`（`server/index.ts`），默认不暴露到局域网/公网；vite dev server 同（`vite.config.ts`）。
- **权限模式白名单**：请求体的 `permissionMode` 仅接受 `default / acceptEdits / plan`；`bypassPermissions` 需服务端显式设置 `AGENT_WEB_ALLOW_BYPASS=1` 才放行（本地单人模式）。默认 Agent 已改为 `acceptEdits`。
- **可选认证**：设置 `AGENT_WEB_TOKEN` 环境变量后，所有 `/api/*` 需携带 `x-agent-token` 或 `Authorization: Bearer <token>` 请求头；未设置则保持本地免认证（但仅回环可访问）。
- **工作目录限制**：`cwd` 仅允许 `PROJECT_CWD` 内的路径，越界输入自动回落项目根。
- 在 `acceptEdits` / `default` 下，Agent 的 Bash/写文件等操作会逐项请求人工确认（内联权限卡片）。

## API / 二次开发

端点与定制方式同原模板，详见 [DEVELOPMENT.md](./DEVELOPMENT.md)。核心入口：

- `server/index.ts` —— `PROJECT_CWD` 默认工作目录、`defaultSystemPrompt` 兜底系统提示词
- `src/hooks/useAgents.ts` —— `DEFAULT_AGENT`（项目专属 Agent 配置）
- `src/config.ts` —— 应用名称/主题色
- `src/pages/ChatPage.tsx` —— 新对话默认 `cwd`

## 环境要求

- Node.js 20+（与 CI 构建环境对齐）
- CodeBuddy API Key（https://www.codebuddy.cn）
