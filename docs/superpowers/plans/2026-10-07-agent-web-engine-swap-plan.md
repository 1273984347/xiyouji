# agent-web 引擎去 CodeBuddy 化方案（Engine Swap Plan · V1.0）

> **头五要素**
> - **版本**：V1.0（首发）
> - **日期**：2026-10-07
> - **来源**：用户两次指令（「不用 CodeBuddy」「完全删除关于 CodeBuddy 和 WorkBuddy 的所有内容」）+ 本日裁决三选一结果 = **保留渡口问津但更换驱动引擎**；集成面为 2026-10-07 对 `server/index.ts`（826 行）实读实测
> - **状态**：待开工——本档为执行蓝图；W680-W682 三批推进（§六），动工批按对账表认领（避开预留号）
> - **读者**：执行 Agent（跨 session）/ 项目维护者。自包含：集成面、新引擎规格、删除清单、验收命令均在本档内。
>
> 生成来源：人工撰写（Agent 起草）·生成模型：GLM（ZCode session 2026-10-07）·生成日期：2026-10-07·核验状态：已核验（§二集成面全部来自当日 server/index.ts 实读；历史段豁免边界见 §五）

---

## 一、裁决与目标

1. **用户裁决链**：① 项目不用 CodeBuddy（含 CLI 登录路线排除）；② 完全删除关于 CodeBuddy 和 WorkBuddy 的所有内容；③ agent-web 的命运 = **保留但换引擎**（三选一裁决：整体退役/保留换引擎/只清提及——用户选保留换引擎）。
2. **目标**：`xiyouji-agent-web` 后端引擎从 `@tencent-ai/agent-sdk`（CodeBuddy Agent SDK）整体替换为 **OpenAI-compatible chat-completions 协议驱动**（可配置 BASE_URL/MODEL，覆盖 GLM/DeepSeek/Moonshot/ollama/vLLM 等一切兼容端点）；全仓现役面 CodeBuddy/WorkBuddy 品牌引用清零；前端 SSE 协议与交互行为保持不变。
3. **唯一豁免面（铁律 8 推论）**：CHANGELOG 历史段、归档 3 份、file-index-archive 中的历史提及**不改写**（历史事实记录）。若用户要求连历史段一并清除，须明确推翻铁律 8 后另立批执行。

## 二、集成面清单（2026-10-07 实测）

### 2.1 server/index.ts（826 行）中 SDK 触点

| 行号 | SDK API | 用途 | 新引擎对应物 |
|---|---|---|---|
| L3 | `query`/`unstable_v2_createSession`/`unstable_v2_authenticate`/`PermissionResult`/`CanUseTool`/`PermissionMode` | 全部导入 | 新 `server/engine/` 模块自有类型 |
| L90-91 | `PermissionMode` | `sanitizePermissionMode` 四值校验 | 自有枚举，逻辑照抄 |
| L177 | `unstable_v2_authenticate` | 登录态健康检查 | 删除（新引擎无 CLI 登录态；健康检查改 LLM 端点连通性探针） |
| L266 | `unstable_v2_createSession` | 会话创建 | 删除（会话已是自有 SQLite 实体） |
| L585 | `canUseTool` 回调 | 工具权限桥接前端（SSE permission_request + 超时 deny + bypass 直通） | **保留原逻辑**，签名改为新引擎工具调用 |
| L642 | `sdkQuery({...})` | agent 主循环：`cwd/model/maxTurns:10/systemPrompt/permissionMode/canUseTool/resume` | 新引擎 `runAgentTurn()`（§三） |

### 2.2 前端 SSE 事件契约（8 事件，保持逐字段不变）

`init` / `text` / `tool` / `tool_result` / `permission_request` / `citation_guard` / `done` / `error`——`src/` 前端不改（SettingsPage 凭证区除外，§四）。

### 2.3 其余引用面（tracked 全仓 grep 实测 35 文件）

- **代码/配置（功能性）**：`xiyouji-agent-web/package.json`（`@tencent-ai/agent-sdk: ^0.3.266` 唯一依赖处）、`server/index.ts`、`evals/run_eval.mjs`（动态 import + W679 补丁的 `CODEBUDDY_*` dotenv 引导）、`src/components/SettingsPage.tsx`（L300-488 凭证 UI 整段）、`.env.example`（`CODEBUDDY_*` 五键）。
- **治理/叙述文档**：AGENTS.md（§2/§4.4）、README.md、STRUCTURE.md、交接文档.md、Makefile、.gitignore、docs/superpowers/plans/ 3 份历史方案、`docs/_dev/` 1 份、`site/dukou-engine.html`、agent-web 三份 md。
- **历史面（豁免）**：CHANGELOG.md 历史段、CHANGELOG-ARCHIVE、file-index-archive、docs/archive/、scripts/archive/。
- **本日 W679 批产物**：`2026-10-07-workflow-industrialization-plan.md`（WF-1 建在 SDK 上）+ `scripts/output/_w679_spec.json`——随本方案修订。

## 三、新引擎规格

### 3.1 模块与配置

- 新建 `server/engine/`：`types.ts`（事件/工具/权限类型）、`openai-compat.ts`（协议驱动）、`tools.ts`（服务端工具集）、`agent-loop.ts`（工具循环）。`server/index.ts` 改为消费 engine 模块，对外 HTTP/SSE 层不动。
- `.env` 新键（ neutral 命名，无品牌）：`LLM_API_BASE`（如 `https://open.bigmodel.cn/api/paas/v4`）、`LLM_API_KEY`、`LLM_MODEL`（如 `glm-4.x`）、可选 `LLM_MAX_TURNS`（默认沿用 10）。
- 模型选择：前端 `selectedModel` 直传 `LLM_MODEL` 覆盖逻辑保持现有 UI 语义。

### 3.2 agent 循环（替代 sdkQuery）

1. 组装 `messages`：system（现有 sysprompt 逻辑不变）+ 会话历史（**从 SQLite 重建**，替代 SDK `resume`——`db.ts` 已存 messages，无需新表）+ 本轮 user 输入。
2. 调用 `POST {LLM_API_BASE}/chat/completions`（`stream: true`，`tools` 数组）；流式增量拼装 `text` 事件（对齐现有 text 粒度语义）。
3. 遇 `tool_calls`：逐个走现有 canUseTool 权限桥（bypass 直通/default-acceptEdits-plan 分类见 3.3）→ 服务端执行 → 发 `tool`/`tool_result` 事件 → 以 `role:"tool"` 消息回传继续循环；`maxTurns` 封顶（超限发 error 事件收尾）。
4. 结束发 `done`；异常发 `error`（现有 error 分支语义保持）。

### 3.3 服务端工具集（替代 SDK 内建运行时）

| 工具 | 行为 | 权限分类 |
|---|---|---|
| `read_file(path)` | cwd 内相对路径读取（复用 W536 式路径守卫） | default 放行 |
| `glob(pattern)` / `grep(pattern, glob?)` | cwd 内检索 | default 放行 |
| `write_file(path, content)` / `edit_file(path, old, new)` | 写入（路径守卫 + 大小上限） | acceptEdits 放行；default 走 permission_request；plan 一律 deny |
| `run_command(cmd, args)` | 仅白名单前缀（`python scripts/`、`node scripts/`、`git log`/`git show` 等只读 git 子命令），禁 shell 拼接 | default/plan 走 permission_request；白名单外 deny |

**安全继承**：路径守卫（越界拒）、禁动态执行、cwd 钳制（W536/W537 加固模式全量保留）；`AGENT_WEB_ALLOW_BYPASS=1` 门禁语义不变。

### 3.4 citationGuard 与拒答边界（W599 资产）

提示词级注入与响应级校验为引擎无关层——位置不动，仅将其挂接点从 SDK 流改为 engine 事件流。

## 四、删除清单（现役面）

| 层 | 动作 |
|---|---|
| 依赖 | `package.json` 移除 `@tencent-ai/agent-sdk`；lockfile 同步；npm audit 复验 |
| 代码 | `server/index.ts` SDK 导入与调用点全部替换；`evals/run_eval.mjs` 重写为驱动新引擎（直调 engine 模块，保留机判三规则与 --self-check）；SettingsPage 凭证区改 LLM_* 三字段 |
| 配置 | `.env.example`：删 `CODEBUDDY_*` 五键，增 `LLM_API_BASE/LLM_API_KEY/LLM_MODEL` |
| 文档 | AGENTS §2 技术栈行 + §4.4 改写（「渡口问津」引擎描述）、README/STRUCTURE/交接/Makefile/`.gitignore`/agent-web 三 md/`site/dukou-engine.html` 相应提及清零（`grep -ric "codebuddy\|workbuddy"` 现役面 = 0） |
| W679 产物修订 | workflow-industrialization-plan.md：§5.6 P0-1 改判（CODEBUDDY 键作废→LLM_* 键）、WF-1 状态改「待新引擎就位后执行（W682）」 |

**历史段豁免**：§一.3 所列面不改写。

## 五、批次划分

| 批 | 内容 | 验收（可复算） |
|---|---|---|
| W680 | engine 四模块 + agent-loop + 工具集 + 权限映射 + run_eval 重写 + SettingsPage/.env.example 切换 + package.json 去依赖 | ① `npm run build` exit 0；② `npm audit --omit=dev --audit-level=high` exit 0 且 `npm ls @tencent-ai/agent-sdk` 空；③ 起服 + 假端点冒烟：/api/chat SSE 事件序列含 init/text/done（mock LLM 或录制响应）；④ 现有 pytest/集成测试中涉 SDK 用例改写后全绿 |
| W681 | 真端点联调（用户配 LLM_* 三键）+ 权限四模式实测 + citationGuard/e2e 回归 + 文档面引用清零 + W679 方案修订入库 | ① 用户端点真跑一轮含工具调用的对话（读 docs 文件并引用）SSE 全 8 事件各 ≥1 次；② 四权限模式 × write_file 行为矩阵实测记录；③ `git -c core.quotePath=false grep -il "codebuddy\|workbuddy" -- .` 仅余 §一.3 豁免面 |
| W682 | WF-1 复活：新引擎跑 golden-50 基线（原 §5.3 WP-1.1/1.2/验收 A1-1~6 全口径，timeout 公式不变） | workflow-industrialization-plan §5.4 验收表全过（对象=新引擎） |

**用户侧前置（W681 前）**：提供任一 OpenAI-compatible 端点写入 `xiyouji-agent-web/.env`：`LLM_API_BASE` / `LLM_API_KEY` / `LLM_MODEL` 三键（GLM/DeepSeek/Moonshot/ollama 均可）。

## 六、风险与对策

| # | 风险 | 对策 |
|---|---|---|
| R1 | agent 循环行为与 SDK 时代不一致（工具选择质量/多轮收敛） | SSE 事件对拍清单 + e2e 回归 + maxTurns 封顶；SDK 时代行为不承诺逐字节等价，承诺协议等价 |
| R2 | run_command 白名单过窄废掉「跑脚本」能力 | 白名单首版只读 git + `python scripts/` 前缀；扩充走批次增量+权限桥 |
| R3 | 会话历史从 SQLite 重建与 SDK resume 语义差异（工具调用中间态） | 历史只存 user/assistant 文本与工具摘要（现有表结构已如此），循环内中间态不跨轮保留——与现有 DB 记录口径一致 |
| R4 | 历史段提及残留与用户「完全删除」预期不符 | §一.3 显式声明豁免边界，开工前用户可推翻铁律 8 另立批 |
| R5 | 品牌清除波及引用脚本/门禁（lint_links 等） | W681 文档清零后跑 `python scripts/verify_delivery.py` 核心全绿为准 |

## 七、收官判据（DoD）

1. `npm ls @tencent-ai/agent-sdk` 空输出且 `git grep -i "agent-sdk"` 现役面 0 命中；
2. §五 W680-W682 验收列逐条勾毕；
3. `git -c core.quotePath=false grep -il "codebuddy\|workbuddy" -- .` 输出 ⊆ §一.3 豁免面清单；
4. `python scripts/verify_delivery.py` 核心全绿 + CI 五工作流绿；
5. WF-1 基线（golden-50）在新引擎上产出 results json（A1-1/A1-2 达标）。
