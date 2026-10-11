# Web Agent（xiyouji-agent-web/）· L2 主题层 · W709 自 AGENTS §4.4 迁入

> **📖 阅读契约（W709）**：查表型——动 xiyouji-agent-web/（引擎/前端/权限）时读。

- 后端 `server/index.ts`（Express + SSE 流式 + SQLite `data/chat.db`），前端 `src/`（React18 + Vite5 + TDesign）。
- 引擎凭证 `LLM_API_BASE`/`LLM_API_KEY`/`LLM_MODEL`（`.env`，由 `.env.example` 复制，已 gitignore·兼容所有主流大模型 OpenAI-compatible 端点·W680）。
- 默认 `PROJECT_CWD`=仓库根（启动时向上探测 AGENTS.md+site/tokens.css 自动解析·env 可覆盖·W596）；专属 Agent「渡口问津」内置项目 sysprompt；权限默认 `default`（UI 可切 `acceptEdits`/`plan`；`bypassPermissions` 仅当服务端 env `AGENT_WEB_ALLOW_BYPASS=1` 时放行，否则降级 default——W411 加固，W537 文档校正）。
- 核心入口：`server/index.ts`、`src/hooks/useAgents.ts`（DEFAULT_AGENT）、`src/config.ts`（主题色 #c8463a「西」Logo）、`src/pages/ChatPage.tsx`。