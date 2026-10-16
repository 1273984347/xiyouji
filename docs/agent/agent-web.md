# Web Agent（xiyouji-agent-web/）· L2 主题层 · W709 自 AGENTS §4.4 迁入

> **📖 阅读契约（W709）**：查表型——动 xiyouji-agent-web/（引擎/前端/权限）时读。

- 后端 `server/index.ts`（Express 5 + SSE 流式 + SQLite `data/chat.db`）+ 自研 OpenAI-compatible 引擎 `server/engine/`（W680：types/openai-compat/tools/agent-loop 四模块+grep-worker·全主流大模型端点适配），前端 `src/`（React 19 + Vite 8 + TypeScript 7 + TDesign React·W543-W548 五阶段迁移）。
- 引擎能力：流式驱动 + 六工具（read_file/glob/grep/write_file/edit_file/run_command）+ 安全基线（realpath 越界守卫/受保护路径黑名单/命令白名单/凭证仅服务端 .env）；常驻冒烟 `server/engine.smoke.mjs`（12 组机判断言·改引擎必跑）。
- 引擎安全专项单测（W752 建·W764 扩）：`server/engine/tools.test.ts`（38 例·越界/读写黑名单含 sha256 未改写实证/命令白名单精度（含 git pager 族拦截与 shell 元字符校验）/环境过滤/尺寸上限）+ `server/audit.test.ts`（7 例）· `npm run test:server` 一键跑三文件；细粒度写入允许域 `AGENT_WEB_WRITE_SCOPE`（逗号分隔 posix 前缀·默认不设=全工作目录可写·与黑名单叠加时黑名单优先·W752）。
- **run_command 参数层拦截（W680→W764）**：白名单=python/node scripts/… + 只读 git 子命令 + pip show|list；git 侧拦 `--no-index`/`--output=`/`-O`（含 `-O=` 粘连）/`--open-files-in-pager`/`--ext-diff`/`--pager=`（W764 收口 W760 S-01 实证的 pager→sh -c RCE）；全命令 shell 元字符二次校验（`;` `&` `>` `<` 反引号/换行拒·`|` `$` 放行保 git grep 正则）。
- 写操作持久化审计（W752）：`server/audit.ts` 按 JSONL 追加 `data/audit.jsonl`（`AGENT_WEB_AUDIT_LOG` 可覆盖·写入 fail-open 只 console.error·审计文件本体入 DENY_READ 防 LLM 读回操作史），权限桥 `canUseTool` 与工具结果双向接线（allow/deny/结果三类 + phase 区分），只读回放端点 `GET /api/audit?limit=100`（同受 AGENT_WEB_TOKEN 保护）。
- 引擎凭证 `LLM_API_BASE`/`LLM_API_KEY`/`LLM_MODEL`（`.env`，由 `.env.example` 复制，已 gitignore·兼容所有主流大模型 OpenAI-compatible 端点·W680）。
- 默认 `PROJECT_CWD`=仓库根（启动时向上探测 AGENTS.md+site/tokens.css 自动解析·env 可覆盖·W596）；专属 Agent「渡口问津」内置项目 sysprompt；权限默认 `default`（UI 可切 `acceptEdits`/`plan`；`bypassPermissions` 仅当服务端 env `AGENT_WEB_ALLOW_BYPASS=1` 时放行，否则降级 default——W411 加固，W537 文档校正）。
- 核心入口：`server/index.ts`、`src/hooks/useAgents.ts`（DEFAULT_AGENT）、`src/config.ts`（主题色 #c8463a「西」Logo）、`src/pages/ChatPage.tsx`。
- 权威入口：[xiyouji-agent-web/README.md](../../xiyouji-agent-web/README.md)（运行/部署/扩展指南）。