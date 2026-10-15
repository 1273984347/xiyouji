# 安全与代码审查报告 — xiyouji-agent-web（西游记·渡口问津 Web Agent）

- **审查对象**：`D:/1/xiyouji/xiyouji-agent-web/`（Node + Express + TypeScript 后端，React 18 + Vite 前端，SQLite `data/chat.db`，基于 `@tencent-ai/agent-sdk`）
- **审查日期**：2026-08-11
- **审查范围**：安全相关源码（排除 `node_modules/`、`dist/`、`.git/`、`*.map`、已编译 `server/*.js` 镜像）
- **审查方法**：`Read` + `Grep` 针对 API_KEY/TOKEN/secret/eval/exec/child_process/Function/bypassPermissions/PROJECT_CWD/CORS/setHeader/innerHTML/dangerouslySetInnerHTML/sqlite/SQL/fetch/http:///process.env
- **说明**：离线审查，无法执行 `npm audit`；依赖结论基于 `package-lock.json` 实际解析版本。

---

## 总体结论（Verdict）

**本地开发 / 单人使用：安全（Safe for localhost dev）。**

**不建议在公网/局域网无防护暴露。公开暴露前必须满足：**
1. 设置 `AGENT_WEB_TOKEN`（开启 `/api/*` 认证）；
2. **保持 `AGENT_WEB_ALLOW_BYPASS` 关闭**（默认已关闭）；
3. 理解 `PROJECT_CWD` 不是沙箱——Agent 可在该目录子树内读取文件、运行 Bash（经权限确认），应把 `PROJECT_CWD` 指向不可包含密钥、且损坏后果可接受的项目副本；
4. 置于带身份验证的反向代理之后（当前服务仅绑定 `127.0.0.1`，本身不对外）。

该应用已实施了较多“前序审计”修复（源码多处 `P0-1`/`P0-2`/`P2-3` 注释），整体安全水位明显高于典型玩具项目。未发现高危硬编码密钥、命令注入或 SQL 注入。

---

## 逐项发现

### 1. 硬编码密钥 / Token — P3（低）
- **未发现**源码中硬编码真实 `CODEBUDDY_API_KEY`、`CODEBUDDY_AUTH_TOKEN`、`AGENT_WEB_TOKEN`。
- 仓库内仅 `xiyouji-agent-web/.env.example`（占位符 `your_api_key_here`）。真实密钥应在服务端 `.env`（父目录 `D:/1/xiyouji/.env` 不在本仓库范围，未纳入审查）。
- `server/index.ts:118-138` `/api/check-login` 返回的密钥已做脱敏（`slice(0,8)+****+slice(-4)`），不直接泄露。
- **建议**：确保 `.env` 被 `.gitignore` 忽略且永不上传；CI 中扫描密钥。

### 2. AGENT_WEB_TOKEN 认证 — P1（高，默认关闭）
- `server/index.ts:49-57`：认证**可选**。仅当 `AGENT_WEB_TOKEN` 非空时才注册鉴权中间件；否则 `/api/*` 完全免认证。
- 校验方式同时接受 `x-agent-token` 头与 `Authorization: Bearer <token>`，相等比较（`auth === AGENT_WEB_TOKEN`），逻辑正确无绕过（常量时间比较非必须，但建议后续改进）。
- **风险**：默认部署无认证。但服务绑定 `127.0.0.1`（`index.ts:761`），不对外，故本地可接受。一旦用户为“局域网共享”把监听地址改掉而不设 token，则任何人可驱动 Agent。
- **建议**：将认证设为默认开启（无 token 时拒绝启动或打印醒目警告）；或文档强制要求暴露前必设 token。

### 3. 路径穿越 / 任意文件读取（经 PROJECT_CWD）— P2（中，已缓解）
- `server/index.ts:73-79` `resolveWorkingDir()`：`path.resolve` 后用 `candidate === root || candidate.startsWith(root + path.sep)` 校验，越界即回落 `PROJECT_CWD`。逻辑正确，普通 `../` 穿越被拦截。
- 前端 `cwd` 来自 `ChatPage.tsx:54`（默认 `D:/1/xiyouji`）并经服务端净化，无法逃逸子树。
- **理论残留（Windows 特例）**：Windows 8.3 短文件名（如 `XIYOU~1`）与大小写不敏感可能使 `startsWith` 校验被物理路径绕过；且服务端**无文件读取类 API**（无 `/api/file`、`express.static`），Agent 文件读取走 SDK 限定于 cwd，故实际利用面极窄。
- **建议**：Windows 下可对解析后的 `candidate` 再做一次大小写归一化比较；保持“不新增任意文件读取接口”的约定。

### 4. 命令注入 / 代码注入 — P2（中，已缓解）
- 应用自身代码**未使用** `eval(`、`Function(`、`child_process`、`exec(`（全仓 Grep 无命中于 `src`/`server/index.ts`）。
- 命令执行的**唯一**来源是 Agent SDK 的 Bash 工具，由 `canUseTool` 回调（`index.ts:537-589`）接管：
  - 默认/acceptEdits/plan 模式下，每个工具调用都通过 SSE `permission_request` 推送到前端，等待用户在 UI 点击允许/拒绝（`index.ts:558-562`、`/api/permission-response`）。
  - 仅在 `effectivePermissionMode === 'bypassPermissions'`（`index.ts:542`）时直接放行——而该模式默认不可达（见 #7）。
- **建议**：保持工具权限确认链路；对 Bash 类工具可额外加关键词黑名单（写 `~/.bashrc`、下载执行等）作为纵深防御。

### 5. 提示注入面（Prompt Injection）— P2（中）
- 用户聊天文本 `message` 直接作为 `prompt`（`index.ts:594`）送入 Agent；自定义 Agent 的 `systemPrompt` 可由客户端请求体 `systemPrompt` 字段完全覆盖（`index.ts:403,599`）。
- 系统提示词内含 `PROJECT_CWD` 路径（`index.ts:506`、`useAgents.ts:15`）——属于预期行为（向导功能）。
- **边界**：受 `resolveWorkingDir`（cwd 限制）+ 工具权限确认双重约束；注入可诱导 Agent 读/写 `PROJECT_CWD` 内文件或运行命令（需用户点允许），但无法逃逸目录、无法获得服务端密钥（密钥不进提示词、不回显原始值）。
- **建议**：对 `systemPrompt` 来源做服务端白名单（仅允许前端已保存的自定义 Agent id，而非任意字符串）；降低“自定义系统提示词即完整覆盖默认提示词”的权限。

### 6. CORS 配置 — P3（低，安全默认）
- 无 `cors` 中间件，也未设置 `Access-Control-Allow-Origin`。浏览器跨域请求默认被拒——属“默认拒绝”安全行为，不是配置错误。
- 开发期由 Vite `proxy`（`vite.config.ts:10-15`）将 `/api` 代理到 `localhost:3000`，同源无 CORS 需求。
- **注意**：`vite.config.ts:9` `allowedHosts: true` 会放行任意 Host 头（仅影响 Vite dev server，且已 `host:'127.0.0.1'` 绑定）。若日后放开 dev server 监听地址，需收紧 `allowedHosts`。
- **建议**：如未来前后端分离部署，显式配置精确 `Access-Control-Allow-Origin`，**切勿**使用 `*` + `credentials`。

### 7. bypassPermissions 默认值 — P1（高，但默认关闭=良好）
- `server/index.ts:60-70`：白名单 `SAFE_PERMISSION_MODES = {default, acceptEdits, plan}`；`sanitizePermissionMode()` 拒绝白名单外的值，除非 `ALLOW_BYPASS && input==="bypassPermissions"`。
- `ALLOW_BYPASS = process.env.AGENT_WEB_ALLOW_BYPASS === "1"`（`index.ts:62`）——**默认 false**。
- 前端默认 `permissionMode: 'acceptEdits'`（`useAgents.ts:37`，注释明确“不做 bypassPermissions”）。
- **影响评估**：若启用 `AGENT_WEB_ALLOW_BYPASS=1`，任何（已认证的，取决于 #2）客户端可请求 `bypassPermissions`，Agent 将不经确认运行所有工具/Bash——在 `PROJECT_CWD` 内等同于 RCE。这是“是否安全”的关键开关。
- **结论**：默认安全；该能力被环境变量与输入净化双重门控，设计合理。
- **建议**：保持默认关闭；若启用，务必同时启用 `AGENT_WEB_TOKEN` 并仅在受信单人环境使用；文档显著标注风险。

### 8. 依赖漏洞 — P3（低，版本均较新；无法离线 audit）
基于 `package-lock.json` 实际解析版本：
- `express` **4.22.2**（>= 4.21.2，已修 CVE-2025-27152 等 4.x 已知项）
- `vite` **5.4.21**（已含 esbuild dev-server CVE 修复）
- `dompurify` **3.4.13`（近期版）
- `react` **18.3.1`（已修 18.2/18.3 已知问题）
- `better-sqlite3` **12.11.1`（近期版）
- `@tencent-ai/agent-sdk` **0.3.237`（近期版）
- `@tdesign-react/aigc` **0.1.0-alpha.15`（**alpha 预发布**，供应链/稳定性注意项，非已知 CVE）

- **说明**：无法离线运行 `npm audit`，以上为版本层面判断。alpha 依赖建议在锁定 commit/哈希后谨慎升级。
- **建议**：定期 `npm audit`；对 `@tdesign-react/aigc` 固定版本并关注上游安全公告。

### 9. SQLite 注入（chat.db）— P3（低，已参数化）
- `server/db.ts`：所有读写均使用 `better-sqlite3` **预处理语句 + `?` 占位符**（`getSession`、`createSession`、`updateSession`、`deleteSession`、`getMessagesBySession`、`createMessage` 等）。
- `updateSession`/`updateMessage` 的字段名由**代码内固定白名单**拼接（`db.ts:110-132, 177-193`），值仍走参数绑定，**无字符串拼接注入**。
- `CREATE TABLE`/`ALTER TABLE`/`DELETE` 为固定 SQL 字面量，无可变输入。
- **结论**：无 SQL 注入风险。

### 10. XSS（Agent 输出/用户输入渲染）— P3（低，已缓解）
- 用户消息：`ChatMessages.tsx:160` 以 React 文本子节点 `{message.content}` 渲染，**自动转义**，安全。
- 助手消息：`ChatMessages.tsx:50,102` 经 `DOMPurify.sanitize()` 后再交给 `ChatMarkdown`（其内部 `html:true`），注释明确此为对抗“unsafeHTML 无消毒”的修复（P2-6）。
- 全仓 Grep：**无** `dangerouslySetInnerHTML` / `innerHTML` 使用（仅 `DOMPurify`/普通渲染）。工具结果经 `ToolCallsCollapse` 以文本渲染，未用 innerHTML。
- **建议**：保持 DOMPurify 在每次 Markdown 渲染前调用；升级 `@tdesign-react/chat` 时回归验证其是否仍默认 `html:true`。

---

## 其他观察（非阻断）

- **“双份源码”footgun**：`server/index.ts` 与编译产物 `server/index.js`、`server/db.js`、`*.d.ts` 共存于 `server/`（Grep 可见 `index.js` 也含安全修复副本）。`tsx` 实际运行 `.ts`，但若有人误执行 `node server/index.js` 会跑可能陈旧的镜像。建议将编译输出导向独立 `dist/`（已在 `.gitignore` 忽略 `dist/`），并忽略 `server/*.js`/`*.d.ts`。
- **运行时改环境变量**：`/api/save-env-config`（`index.ts:192-226`）拒绝覆盖 `apiKey`/`baseUrl`（P0-2 修复，防密钥劫持+SSRF），但允许运行时设置 `CODEBUDDY_AUTH_TOKEN`/`CODEBUDDY_INTERNET_ENVIRONMENT` 到进程环境。无认证时本地可调；暴露前须依赖 #2 的 token。
- **SSE 生命周期**：`index.ts:471-500` 已加断开清理与 10 分钟总超时，避免客户端断开后流/悬挂权限请求继续运行。设计良好。
- **监听绑定**：`index.ts:761` 与 `vite.config.ts:7` 均显式 `127.0.0.1`——默认不对外，是本项目最重要的“默认安全”保障。

---

## 风险矩阵

| # | 项 | 严重度 | 默认状态 |
|---|----|--------|----------|
| 1 | 硬编码密钥 | P3 | 无真实密钥 |
| 2 | AGENT_WEB_TOKEN 认证 | P1 | 默认关闭（本地可接受） |
| 3 | 路径穿越 | P2 | 已缓解，Windows 8.3 理论残留 |
| 4 | 命令/代码注入 | P2 | 经 SDK+Bash 权限确认，已缓解 |
| 5 | 提示注入 | P2 | 受 cwd+权限确认约束 |
| 6 | CORS | P3 | 默认拒绝（安全） |
| 7 | bypassPermissions 默认 | P1 | 默认关闭（良好） |
| 8 | 依赖漏洞 | P3 | 版本均较新 |
| 9 | SQLite 注入 | P3 | 已参数化 |
| 10 | XSS | P3 | 已 DOMPurify+转义 |

**最高优先级行动**：若任何暴露需求 → 开启 `AGENT_WEB_TOKEN` 并**保持 `AGENT_WEB_ALLOW_BYPASS` 关闭**。
