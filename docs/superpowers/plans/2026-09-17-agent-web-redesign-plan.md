# agent-web「渡口问津」重设计方案（方案 R v2 · R0–R5）

> 创建：2026-09-17；**v2 同日修订（用户裁决：不用任何 CodeBuddy / WorkBuddy 相关的一切——v1 的「双引擎」架构作废**，SDK 工程引擎、CODEBUDDY_* 环境变量、CLI 依赖全部移除，改为自研 OpenAI 兼容 Agent 循环；本文件为完整重写版，v1 不再有效）。
>
> 本文档自包含：全部背景、现状、代码定位、执行步骤、验收标准内嵌于正文；基线数字为 2026-09-17 在本仓库 HEAD `ee077ab`（v2.3.171 W571）工作树实测，复现命令为 `python scripts/_audit_agentweb_baseline.py`（B* 键）+ 本文件 §0 的 C* 残留面扫描（附命令）。执行者无需回溯本次会话即可独立执行。
>
> 批号说明：建议批号 **W574–W578**（R1–R5）为预设，按「CHANGELOG 现役段 max+1」实领（D=572、E=573 之后的空位起）。R0 探针（半天）并入 R1 批内执行。新写一次性脚本不带 W 号。
>
> 与《2026-09-09 体验与服务优化计划（D/E/F/G/H）》的关系（**裁决 C，已获用户确认生效**）：D-H 计划中 agent-web 侧各项并入本方案——F-1 残余→R3、F-2→R1（**其 cost 字段调整为 tokens 计量**，见 R1 步骤 2）、F-3/F-4→R1、G-1→R2、G-3→R3/R4、G-4/G-5→R5、G-2 README 小项→R5；D-H 的 F/G 节降级为需求基线文档不再独立施工，D/E/H 维持原批号。
>
> 背景压缩（30 秒版）：D2 已裁决「重新设计 agent-web」，且用户追加裁决**全量移除 CodeBuddy/WorkBuddy**。现状 = 5,527 行的本机单人 demo：对话/会话/权限人审/SSE 流式骨架齐全（W568 刚根治错误链路主体），但（a）SDK 靠 spawn 外部 CLI 工作，**本机 CLI 已删除，产品整体不可用**（仅 ⚠️ 气泡）；（b）SDK 返回的指标被丢弃、零反馈、零检索增强（裸翻 672 篇文档）；（c）dev-only 无服务化件。v2 方案：**自研单引擎**（OpenAI 兼容 function calling + 工具注册表 + 权限人审 + RAG 检索）替换 SDK，SSE 协议对前端零变更，五个批次落地并完成品牌/依赖退役清扫。

> 生成来源：人工撰写
> 生成模型：GLM-5.3-Flash
> 生成日期：2026-09-17
> 核验状态：未核验

---

## 〇、现状基线（2026-09-17 @ ee077ab/W571 实测）

复现：`python scripts/_audit_agentweb_baseline.py`（B* 键）；C* 为本次新增残留面扫描（命令附右列）。

| # | 事实 | 现状值 | 复现（审计键 / 代码定位） |
|---|------|--------|------------------------|
| F1 | 代码规模 | server + src 共 **27 个 ts/tsx 文件、5,527 行**——小库重建 | `B01_ts_files/loc` |
| F2 | 端点清单 | 11 个：health / check-login / save-env-config / models / sessions×5 / permission-response / chat | `B02_endpoints` |
| F3 | 关键依赖 | react ^19.2.8 · express ^5.2.1 · **@tencent-ai/agent-sdk ^0.3.250（退役对象）** · @tdesign-react/chat ^1.0.2 · @tdesign-react/aigc ^0.1.0-alpha · better-sqlite3 ^13 · dompurify ^3.4.14 | `B03_deps` |
| F4 | 渲染基线 | markdown 渲染已存在：`ChatMarkdown`（@tdesign-react/chat）+ `DOMPurify.sanitize` ×2（ChatMessages.tsx:4,50,102） | `B04_markdown` |
| F5 | 交互缺口 | 复制 0、重新生成 0、编辑消息 0 | `B05_affordances` |
| F6 | 可靠性现状 | error 分支 1（W568 已修，useChat.ts:301）；AbortController 0（假停止）、`response.ok` 0、草稿 `setItem` 0 | `B06_reliability` |
| F7 | 指标现状 | messages 表无 duration/tokens/feedback 列；`/api/stats` 无；SDK done 事件 duration/cost 被丢弃 | `B07_metrics` |
| F8 | 反馈现状 | `/api/feedback` 0、UI 点赞点踩 0 | `B08_feedback` |
| F9 | 双源漂移存量 | useAgents.ts 写死 v2.3.9 ×1 + 旧路径 D:/1/xiyouji ×1；`.env.example` PROJECT_CWD 旧路径 ×2 | `B09_stale` |
| F10 | 检索资产 | rag_server 提供 **GET /health /query /graph**（stdlib http.server）；语料 docstring 口径 **672 篇**，与 D-H 方案 E-1 的 771 口径不一致（R2 统一） | `B10_rag` |
| F11 | CI 覆盖 | ci.yml / security.yml / screenshot-review.yml 三工作流涉及 agent-web | `B11_ci_files` |
| F12 | chat.db 实况 | sessions=7、messages=13（W568 走查数据） | `B12_chatdb` |
| F13 | 无障碍基线 | `prefers-reduced-motion` 0、`aria-label` 0；侧栏 `width: sidebarOpen ? 260 : 0` 固定像素（Sidebar.tsx:37） | `B13_a11y` |
| F14 | **SDK 进程依赖（退役主因）** | SDK dist 内含 codebuddy/claude CLI 名（416 个 dist 文件），靠 spawn 外部 CLI 工作；**本机 CLI 已删除 → 产品当前整体不可用**，错误仅 ⚠️ 气泡 | `B15_sdk_cli_hints` + W568 记录 |
| F15 | 服务化件现状 | express.static 0、AGENT_WEB_HOST 0、限流 0、服务端输入上限 0 | `B16_serve` |
| F16 | 模型与登录 | `/api/models` 经 **SDK 会话** `getAvailableModels()` 取数（index.ts:226-236，SDK 移除后须改为静态配置）；`defaultModel = "claude-sonnet-4"` 硬编码（:80）；`/api/check-login` 区分 `env|cli|none`（CLI 分支随 SDK 退役删除）；`/api/health` 仅 `{status,timestamp}` 空壳；`/api/save-env-config` 含 P0-2 守卫（拒绝运行时覆盖 apiKey/baseUrl，:189-198）——姿态保留、字段名改 LLM_* | server/index.ts 实测 |
| C1 | **CodeBuddy 残留面（退役清扫清单）** | server/index.ts **×12**（SDK 导入 :3、models、check-login CLI 分支、CODEBUDDY_* 读取、sdkQuery :604 等）、SettingsPage.tsx **×8**、README.md **×6**、DEVELOPMENT.md **×9**、.env.example **×5**、package.json 依赖 ×1 | `grep -ric codebuddy <file>` 逐文件 |
| C2 | WorkBuddy 引用 | 产品面 **0**；仅 CHANGELOG 历史段（禁改）、scripts/archive 归档脚本、`scripts/lint_links.py:257` 排除目录默认值 `".workbuddy"`（历史路径过滤，非产品依赖）——**均不属本方案清扫面**，R5 登记 | `grep -rli workbuddy` |
| C3 | 会话恢复依赖 | sessions 表 `sdk_session_id` 列 + index.ts:610 `resume`——SDK 退役后**停用**（多轮上下文改由 DB 消息装配，R2）；列保留不删（nullable 无害） | db.ts:31 + index.ts:610 |

---

## 一、设计目标与原则

七条量化目标：

| 目标 | 验收口径（全部机判） |
|---|---|
| G0 零 CodeBuddy/WorkBuddy | 产品面（xiyouji-agent-web/ 除 node_modules）`grep -ric codebuddy` 全部归 0；`@tencent-ai/agent-sdk` 从 package.json 移除；build/tsc 在无 SDK 状态下通过 |
| G1 可靠性 | 三类故障（流中 error / 非 200 / 进程失联）UI 100% 呈现 + 可重试：e2e ≥5 用例全绿 |
| G2 可观测 | 每条 assistant 消息落库 4 指标（duration_ms / first_token_ms / prompt_tokens / completion_tokens）；`/api/stats` ≥9 字段含 error_rate |
| G3 反馈闭环 | assistant 消息 100% 可 👍/👎；stats 含 feedback_rate |
| G4 检索增强 | 回答默认 RAG-grounded（rag 可达时 sources ≥1）；语料口径对齐 771 |
| G5 服务化 | static + SPA 回退 + 限流 + 输入上限 + HOST 可配 + token 可选 |
| G6 体验 | 真停止/重试/重新生成/复制/会话搜索重命名导出；375px 无横向溢出；键盘可达；reduced-motion 守卫 |

**原则**：① 不回退安全基线（回环绑定默认、目录钳制、P0–P3 审计结论、`AGENT_WEB_ALLOW_BYPASS` 门控、save-env-config 的 P0-2 姿态原样保留）；② 渐进重建（in-place）；③ 一切验收机判 + 真实参数冒烟（W537④）；④ **SSE 事件协议对前端零变更**（init/text/tool/tool_result/permission_request/done/error + 新增 sources）——前端已实现六分支消费（W568），自研循环必须按此协议产出。

---

## 二、关键架构裁决（v2）

### 裁决 A'：自研单引擎（取代 v1 双引擎，全部 CodeBuddy 组件移除）

```
/api/chat (Express SSE)
   └─ server/agent/loop.ts        Agent 循环（maxTurns 10）
        ├─ server/llm/client.ts   OpenAI 兼容流式客户端（chat/completions，SSE 解析，
        │                          delta.content 流式转发 + delta.tool_calls 增量拼装 + usage 捕获）
        ├─ server/agent/tools/    工具注册表（function calling）
        │    ├─ search_docs   → rag_client（GET RAG_BASE/query）        只读·自动允许
        │    ├─ read_file     → PROJECT_CWD 钳制读文件（realpath 校验）  只读·自动允许
        │    ├─ list_dir      → PROJECT_CWD 钳制列目录                  只读·自动允许
        │    ├─ run_python    → 运行 scripts/ 下脚本（cwd 钳制+60s 超时+输出截断）★人审
        │    └─ write_file    → PROJECT_CWD 钳制写文件                   ★人审（acceptEdits 自动）
        └─ server/rag_client.ts   检索（1.5s 超时，降级 ungrounded）
```

- **首轮自动检索**：用户提问先经 rag_client 取 top5 片段注入 system 上下文（RAG-grounded 默认成立，rag 不可达时 `ungrounded` 标注继续回答）；循环中模型仍可主动调 `search_docs` 深挖。
- **权限人审映射**（沿用既有 permissionMode 语义与 InlinePermissionCard UI）：`plan`=仅只读工具；`default`=★人审工具走既有 `permission_request` SSE → 前端卡片 → `/api/permission-response` 链路（**该链路原样复用，只是审批对象从 SDK 工具变为自研工具**）；`acceptEdits`=write_file 自动放行、run_python 仍人审；`bypassPermissions` 维持 `AGENT_WEB_ALLOW_BYPASS=1` 门控。
- **多轮上下文**：从 DB 装配（getMessagesBySession 取 user/assistant 文本，截断窗口最近 20 条）；`sdk_session_id` 停用（C3）。
- **E0' 探针（R0，唯一前置）**：目标端点必须 OpenAI 兼容（OpenAI/DeepSeek/Qwen/GLM/Moonshot/vLLM/Ollama 等均兼容）：

```bash
curl -sS --max-time 30 -X POST "$LLM_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $LLM_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"'$LLM_MODEL'","messages":[{"role":"user","content":"只回复OK"}],"stream":true}'
```
  通过标准：SSE 流含 `data: {"choices":[{"delta":{...`。探针**失败即停止**（v2 无降级引擎——这就是硬前提），结果登记 CHANGELOG。
- **环境变量重定义（品牌退役）**：`LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL`（默认模型）/ `LLM_MODELS`（可选逗号分隔清单→/api/models）；删除 `CODEBUDDY_API_KEY / CODEBUDDY_AUTH_TOKEN / CODEBUDDY_BASE_URL / CODEBUDDY_INTERNET_ENVIRONMENT` 全部读取；保留 `PORT / PROJECT_CWD / AGENT_WEB_TOKEN / AGENT_WEB_ALLOW_BYPASS`，新增 `RAG_BASE`（默认 http://127.0.0.1:8777）。P0-2 姿态照搬：LLM_API_KEY/LLM_BASE_URL 禁止运行时覆盖（save-env-config 同款 400 守卫）。

### 裁决 B：渐进重建（in-place），保留资产清单

**保留**：Express 5 + SSE 骨架与事件协议；sessions/messages CRUD + SQLite WAL；权限人审链路（SSE 事件 + InlinePermissionCard + permission-response API）；W568 错误链路修复；ChatMarkdown + DOMPurify；React 19 + Vite 8 + Tailwind v4 栈。
**替换/重建**：`/api/chat` 的 SDK 调用段 → agent 循环（R2）；`/api/models` SDK 取数 → env 静态配置（R1）；check-login → 简化配置检测（R0）；SettingsPage 登录诊断 → 模型服务配置页（R4）；useChat 状态机与消息交互层（R3）。

### 裁决 C：D-H 计划 agent 侧项并入（已生效）

F-1 残余→R3；F-2→R1（**cost 字段调整为 tokens 计量**——通用 provider 无统一成本口径，cost 列不建，token 数入列）；F-3/F-4→R1；G-1→R2；G-3→R3/R4；G-4/G-5→R5；G-2 README 小项→R5。

### 裁决 D：检索语料口径统一为 771

`scripts/rag/xiyouji_rag.py` 的 `_load_docs()`（:226-242）排除规则对齐四目录（`/_dev/`、`/_templates/`、`/archive`、`/superpowers/`），重建索引断言 corpus=771（当批实跑）。不重写检索算法。

---

## 三、批次拆解

### R0 探针与自检底座（0.5 天，并入 R1 批内执行）

1. **E0' 探针**（裁决 A' 的 curl，需用户提供 LLM_BASE_URL/LLM_API_KEY/LLM_MODEL），结果登记。
2. `/api/check-login` 简化：删除 `cli` 分支与 cliConfigured（CLI 概念随 SDK 退役），改为 `{configured, method:'env'|'none', keyMasked}`——仅检测 LLM_API_KEY。
3. `/api/health` 扩展为环境自检：`{status, timestamp, apiKeyConfigured, baseUrlReachable, ragReachable, toolWhitelist}`（baseUrlReachable=对 LLM_BASE_URL 的 3s 探测；toolWhitelist=当前权限模式允许的工具名数组）。
- **验收**：`curl /api/health` 含 6 键；探针结果两行登记 CHANGELOG；`grep -c "cliConfigured" server/index.ts`==0。
- **明确非目标**：不自动申请/填充 key。

### R1 服务底座与指标（建议批号 W574，3–4 小时）

- **现象**：F7/F15/F16。零指标、零服务化件、models 走 SDK、健康检查空壳。
- **执行步骤**：
  1. **`server/llm/client.ts`**：OpenAI 兼容流式客户端——`chat/completions` POST + SSE 解析（`delta.content` / `delta.tool_calls` 增量拼装 / `finish_reason` / `usage`），超时与 abort 支持，`stream_options:{include_usage:true}`（provider 不返回 usage 时 tokens 落 null）。**本批只交付并单测该客户端，/api/chat 仍走 SDK（零行为变更）**。
  2. **metrics 列**（PRAGMA+ALTER 迁移先例，db.ts:52-62）：messages 表加 `duration_ms REAL`、`first_token_ms REAL`、`prompt_tokens INTEGER`、`completion_tokens INTEGER`、`is_error INTEGER DEFAULT 0`、`feedback INTEGER DEFAULT 0`、`feedback_note TEXT`；现有 SDK 路径的 done 事件（duration/cost 已有，:722）入库 duration_ms，首包时间在 handler 内计时；**错误路径落库**（catch 补 is_error=1 行，沿用 D-H F-2 的「挂起零落库」语义声明——不变更）。
  3. **`GET /api/stats`**：`{sessions, messages_total, assistant_total, errors, error_rate, avg_duration_ms, p50_first_token_ms, total_prompt_tokens, total_completion_tokens, feedback_rate}`（10 字段；分母 0 时比率为 null）。
  4. **`/api/models` 静态化**：删除 SDK 会话取数（:226-236），改为 env 读取——`LLM_MODELS`（逗号分隔 `{modelId}:{name}` 或纯 id 列表）缺省回退 `[{modelId: LLM_MODEL, name: LLM_MODEL}]`；`defaultModel` 硬编码（:80）改读 `LLM_MODEL`。
  5. **限流 + 输入上限**（D-H F-3 原样并入）：4000 字（400 invalid_message）+ 10 次/分/会话内存令牌窗（429 + retryAfterSeconds）。
  6. **静态服务**（D-H F-4 原样并入）：`express.static(dist)` + GET 中间件 SPA 回退（**禁 Express 5 `app.get('*')`**）+ `vite.config.ts` 补 `preview.proxy` + package.json 加 `"start": "tsx server/index.ts"`。
- **验收**：`npx tsc -b` 0 错误；`npm run build` 通过；client.ts 对 mock SSE 的单测断言（content 流拼接、tool_calls 增量拼装、usage 捕获三态）；curl 断言 `/api/stats` 10 字段、4001 字→400、并发 11→第 11 条 429、`/`→200 含 root div、`/some/route`→200；缺省行为回归（/api/chat 现有路径不变、/api/models 返回 env 配置）。
- **回滚**：`git checkout -- xiyouji-agent-web/`；新列 nullable 留库无害。

### R2 自研 Agent 循环上线 + SDK 退役（建议批号 W575，5–7 小时——本批最重）

- **现象**：F14/C1/C3。产品依赖已删除的 CLI；检索裸翻 672 篇；sysprompt 双源漂移。
- **执行步骤**：
  1. **`server/agent/tools/`**：五工具注册表（裁决 A' 表格），每个工具 = `{name, description, parameters(JSON Schema), execute, requiresReview}`；read_file/list_dir/run_python/write_file 全部走 PROJECT_CWD `realpathSync` 钳制（沿用 index.ts:405-411 既有净化函数）；run_python 限 `scripts/` 子树 + 60s 超时 + stdout/stderr 截断 4000 字。
  2. **`server/agent/loop.ts`**：DB 装配上下文（最近 20 条）→ 首轮 rag 检索注入 → llm.client 流式调用 → `delta.tool_calls` 聚齐即执行工具（requiresReview 时走既有 permission_request/permission-response 链路，**超时 5 分钟自动 deny 的既有语义沿用**，index.ts:586-595）→ 结果以 tool 消息回填 → 循环至无 tool_calls 或 maxTurns 10 → 全程按既有 SSE 协议发 `init/text/tool/tool_result/done/error` + 新增 `sources`（rag 命中 `{n,path,title,url}`，url=GitHub blob 与 D-1 口径一致）。
  3. **`/api/chat` 切换**：SDK 调用段（:601-612）替换为 loop 调用；`systemPrompt` 参数消费服务端单源 sysprompt（`server/sysprompt.ts` 导出 `makeSystemPrompt(cwd)`，内容取 index.ts:510-532 无版本号版）——**D-H G-1 并入**：useAgents.ts 删 v2.3.9/旧路径文案、前端默认不再上传提示词副本、NewChatView 预览改「使用服务端内置提示词」、DEFAULT_AGENT.permissionMode 'acceptEdits'→'default'（语义变更照 D-H G-1 登记）。
  4. **rag 口径对齐**（裁决 D）：`_load_docs()` 排除四目录，重建索引输出 `corpus=771`（当批实跑）。
  5. **SDK 退役清扫**（C1 清单逐项）：`npm rm @tencent-ai/agent-sdk`；server/index.ts 12 处（SDK 导入、unstable_* 调用、CODEBUDDY_* 读取、check-login CLI 分支残留、models 残留）清零；SettingsPage.tsx 8 处改为「模型服务配置」文案与 LLM_* 字段；save-env-config 的 body 字段 `apiKey/authToken/internetEnv/baseUrl` → `llmModel/llmModels`（**LLM_API_KEY/LLM_BASE_URL 保持禁止运行时覆盖**——P0-2 守卫原文保留仅换名）；.env.example 5 处重写为 LLM_* 模板；README 6 处 / DEVELOPMENT.md 9 处品牌词替换；`sessions.sdk_session_id` 停用（列保留，读写点删除）；权限模式类型从 SDK import 改为本地 `type PermissionMode = 'default'|'acceptEdits'|'plan'|'bypassPermissions'`。
- **验收**：
  1. `npx tsc -b` 0 错误 + `npm run build` 通过（**node_modules 中 SDK 已移除状态下编译**——G0 硬口径）；
  2. Playwright（mock LLM SSE + mock rag）：单轮问答（text 流 + done + sources ≥1）；工具调用轮（mock 返回 tool_calls → 断言 tool/tool_result 事件与执行结果回填）；人审轮（requiresReview 工具 → permission_request 出现 → /api/permission-response allow 后继续）；rag 超时 → ungrounded 徽标且回答正常；
  3. 真实冒烟（真实 key + rag_server 运行）：问答 1 轮 + 「运行 scripts/ 下的词频脚本并告诉我结果」1 轮（人审放行），CHANGELOG 抄录 sources JSON 与 metrics 行；
  4. **G0 清扫断言**：`grep -ric codebuddy xiyouji-agent-web/ --include="*.ts" --include="*.tsx" --include="*.json" --include="*.md" --include="*.example"`（排除 node_modules）全文件 **0**；`grep -c "agent-sdk" xiyouji-agent-web/package.json`==0；
  5. `corpus=771` 行落 CHANGELOG；`python scripts/verify_delivery.py` 核心全绿。
- **回滚**：本批为引擎替换，回滚=恢复 SDK 的提交粒度 revert（revert 后须重装 SDK 依赖）；清扫断言使半移除状态不可合入。
- **明确非目标**：不做多轮检索 agent 循环优化（单轮注入+按需 search_docs）；不做并行工具执行；不做流式 diff 编辑 UI。

### R3 对话体验重建（建议批号 W576，5–6 小时）

- **现象**：F5/F6/F13。假停止、无重试/重新生成/复制/会话管理、无移动与无障碍基线。
- **执行步骤**：
  1. **useChat 状态机重写**（D-H F-1 残余 + 重新生成）：AbortController 贯穿（handleStop 真 abort，AbortError→「已停止生成」非错误态）；`response.ok` 检查；首包看门狗（`dukou.firstTokenTimeoutMs` 可配默认 60000，测试注入口）；`failAssistant(reason)` 统一出口 + 重试（重发最后失败输入）+ 重新生成（重发上一条 user 输入并替换上一条 assistant）；草稿 `setItem` 修复；`sources` 分支接入。
  2. **消息交互**：复制按钮；重试/重新生成按钮；引用 chip（新开 GitHub blob）；工具执行徽标沿用 ToolCallsCollapse 三态。
  3. **会话管理**：重命名（PATCH 已有补 UI）、前端搜索（标题/内容过滤）、单会话 JSON 导出。
  4. **NewChatView 单产品卡**：「渡口问津」+ 权限模式选择器（已有）+ 工具能力说明（「可检索 771 篇解读、运行分析脚本（需确认）」）。
  5. **移动端与无障碍基线**：≤768px 侧栏抽屉（遮罩+ESC 替换固定 260px）；交互元素键盘可达（div onClick→button/role+tabIndex+onKeyDown）；`prefers-reduced-motion` 守卫（光标闪烁/脉冲动画 reduce 下停）；focus 可见样式。
- **验收**（Playwright route 注入，`scripts/_agentweb_reliability_e2e.js` 扩展）：e2e ≥5 用例全绿（error 注入/非 200/停止后内容不再增长/看门狗触发/重试二次请求）；重新生成断言 body 与上一条 user 一致且旧 assistant 被替换；375px `scrollWidth <= innerWidth` + 抽屉态；`emulateMedia({reducedMotion:'reduce'})` 后动画计算值 none；Tab 聚焦断言；tsc + build 通过。
- **回滚**：`git checkout -- xiyouji-agent-web/src/`。
- **明确非目标**：不做消息编辑分叉；不做语音/图片；不引入新组件库。

### R4 反馈闭环与清理（建议批号 W577，2–3 小时）

- **现象**：F8、死组件 3 个（D-H F27）。
- **执行步骤**：
  1. 反馈：消息尾 👍/👎 → `POST /api/feedback {messageId, value:1|-1, note?≤200字}` → messages.feedback/feedback_note；重复提交覆盖；UI 高亮。
  2. stats 接通 `feedback_rate`（R1 已留字段）；设置页「用量」区（stats 渲染）+ **环境自检卡片**（/api/health 六键：key/端点/RAG/工具白名单，异常项红字提示——LLM_API_KEY 缺失提示「在服务端 .env 配置后重启」）。
  3. 清理（D-H G-3）：`git rm` PermissionDialog/NewChatDialog/AgentConfigDialog；README 技术栈行校正（React 19/Express 5/Vite 8）；`.env.example` PROJECT_CWD 旧路径 `D:/1/xiyouji`→`D:/xiyouji`（×2）。
- **验收**：Playwright 点 👍 → sqlite `feedback==1`，再点 👎 覆盖 -1；stats 含 feedback_rate；tsc+build 过（删组件无残留）；`grep -c "React 18" README.md`==0；`grep -c "D:/1/xiyouji" .env.example`==0；审计复跑 `A15_dead_components=[]`、`B08_feedback endpoint=1`。
- **回滚**：`git checkout -- xiyouji-agent-web/`（删除按提交 revert）。
- **明确非目标**：不做反馈看板；不做 badcase 自动归集。

### R5 入口与部署（建议批号 W578，2–4 小时）

- **现象**：F15 + D-H F16/F17。site/ 零入口、rag-chat 线上必死、部署形态未终裁。
- **执行步骤**：
  1. `AGENT_WEB_HOST` env（默认 `127.0.0.1` 不变，listen 一行改动）；公网硬前提 = `AGENT_WEB_TOKEN` 启用（既有中间件）+ HTTPS 反代用户自备。
  2. site/ 入口：index.html ASK 区（:235-237 一带）与页脚导航加「AI 对话」、dashboard.html 补 AI 卡片（S16=0→≥1）——入口形态按三问 3 的 R5 终裁（公网域名 / 本机说明性入口）。
  3. D-H G-4 并入：rag-chat.js 改造既有 checkHealth 时序（init 探测失败不注入 fab）、4 处开发者文案清除（:132/:189/:290/:381）、验收 `grep -c "rag_server.py"==1`。
  4. D-H G-5 并入：index.html 页脚「移动版」链接。
  5. 文档同步：AGENTS.md §4.4 全段重写（SDK 描述→自研引擎与 LLM_* 环境）；交接文档「三」登记；README 产品线关系（G-2 小项）；**WorkBuddy 遗留登记**（CHANGELOG 历史与 lint_links.py:257 `.workbuddy` 排除默认值不属产品面，不动，仅登记）。
- **验收**：`S16_dashboard_ai_entry_n≥1`、`S14_index_to_mobile_links≥1`、rag-chat `grep -c "rag_server.py"==1`；公网形态时 `curl -H "x-agent-token: $TOKEN" https://<域名>/api/models` 200 且无 token 401；`verify_delivery.py` 核心全绿。
- **回滚**：各文件 `git checkout --`。
- **明确非目标**：多租户/配额/内容审核；HTTPS 证书管理；rag_server 公网化。

---

## 四、批次计划与工作量

| 批次 | 建议批号 | 工作量 | 前置 |
|---|---|---|---|
| R0 探针+自检底座 | 并入 W574 | 0.5 天内 | **用户三问 1：LLM_BASE_URL / LLM_API_KEY / LLM_MODEL** |
| R1 服务底座与指标 | W574 | 3–4 小时 | D（W572）/E（W573）建议先行 |
| R2 Agent 循环 + SDK 退役 | W575 | 5–7 小时 | R0 探针通过；E0' 结果为硬前提（无降级引擎） |
| R3 对话体验重建 | W576 | 5–6 小时 | R1 |
| R4 反馈与清理 | W577 | 2–3 小时 | R1 |
| R5 入口与部署 | W578 | 2–4 小时 | R1（公网件）；部署终裁（三问 3 → R5 执行） |
| H tooltip 试点 | D-H 计划，可并行 | 1–2 小时 | 独立 |

**每批统一验收**：`npx tsc -b` 0 错误 + `npm run build` 通过 + `node scripts/_agentweb_reliability_e2e.js` 累计用例全绿 + `python scripts/verify_delivery.py` 核心全绿（六文档同步）+ `gh run list` 确认 ci.yml/security.yml 绿。

## 五、风险与依赖

1. **自研循环的 tool_calls 兼容性（最高风险）**：各 OpenAI 兼容端点的 `delta.tool_calls` 增量格式与 `finish_reason` 语义存在细节差异——llm.client.ts 单测覆盖主流三种形态（OpenAI 原生/DeepSeek/Qwen-DashScope 兼容模式）；R0 探针同时记录目标端点的实际 delta 样本作对账基准。
2. **无 SDK 意味着 agent 能力自担**：SDK 的会话管理/工具沙箱/权限流由自研层接手——权限流有既有 UI 链路复用，沙箱以「cwd 钳制 + scripts/ 白名单 + 超时 + 输出截断」为界，**强于现状**（现状 SDK 只受 CLI 自身约束）；长任务/多轮深任务能力以 maxTurns 10 为界，够用。
3. **@tdesign-react/aigc alpha**：渲染异常时降级为仅用 @tdesign-react/chat 稳定件。
4. **rag_server stdlib 单进程**：非生产级——公网需进程守护（NSSM/systemd，运维件登记不编码）；不可达已设计静默降级。
5. **单 SQLite（WAL）**：单用户足够；多用户明确非目标。
6. **tokens 计量口径**：provider 不返回 usage 时为 null（stats 分母下降），CHANGELOG 登记实际覆盖率。

## 六、启动前三问（2026-09-18 部分裁决；R 整体暂停）

1. **LLM 接入参数（必需输入，非选择题）**：⏳ **未提供**——`LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL`（任何 OpenAI 兼容端点，如 GLM-OpenAI 兼容 / DeepSeek / Moonshot / vLLM 自托管）。E0' 探针以此裁决，探针不过则 R1/R2 不开工；**恢复开发前必须补齐**。
2. **工具集范围**：✅ **五件套**（search_docs / read_file / list_dir 只读自动 + run_python / write_file 人审，acceptEdits 下 write 自动）——用户 2026-09-18 裁决。
3. **编排确认**：✅ **维持不变**——D（W572）/ E（W573）先行、R1–R5 = W574–W578 框架不变，仅执行时点顺延。

> **R 整体状态：⏸ 暂停（用户 2026-09-18 裁决「暂停开发 agent web」）**。恢复条件 = 用户点名恢复 + 三问 1 的 LLM 接入参数补齐（E0' 探针先行）。暂停期间站点侧 D/E/H 批次不受影响。

## 七、落地状态记录（随执行回写）

| 批次 | 状态（✅/⏸/偏差） | commit | 关键数字（当批实跑） | 偏差说明 |
|---|---|---|---|---|
| R0–R5 | ⏸ **暂停**（2026-09-18 用户裁决；三问 2/3 已裁决、三问 1 待补） | — | — | E0' 探针未执行；恢复前置 = 用户点名 + LLM 接入参数 + E0' 通过；v1 双引擎方案已作废 |
