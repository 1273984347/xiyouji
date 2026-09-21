# DEPLOYMENT.md — 「西游记·渡口问津」运行与部署指南（W596）

> **定位（必读）**：本地工程工具。服务仅回环设计（开发态 `127.0.0.1`），**不对公网开放**。
> 公网 AI 能力路线见 `docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md` WP-B-ALT（冻结预案：免费额度 + 200 次/日硬配额，触发条件满足且用户批准后才执行）。

## 1. 本地开发运行

```bash
cd xiyouji-agent-web
npm install
cp .env.example .env        # 填入 CODEBUDDY_API_KEY
npm run dev                 # 后端 :3000 + 前端 :5173（concurrently）
```

- **工作目录**：后端启动时自动解析仓库根（向上探测 `AGENTS.md` + `site/tokens.css`），启动日志打印 `[boot] PROJECT_CWD = ...`；可用环境变量 `PROJECT_CWD` 覆盖（指向其他仓库副本）。目录不存在则 **FATAL 退出**（fail-fast，杜绝静默落空）。
- 安全：默认权限模式 `default`；`bypassPermissions` 仅当服务端 env `AGENT_WEB_ALLOW_BYPASS=1` 放行；可选共享 token `AGENT_WEB_TOKEN`。

## 2. Docker（本地/内网单容器）

```bash
docker build -t xiyouji-agent-web .
docker run --rm -p 3000:3000 --env-file .env \
  -v "D:/xiyouji:/workspace" xiyouji-agent-web
```

- `node:22-alpine`，与 `package.json` engines（Node ≥ 20）对齐。
- 容器内 `PROJECT_CWD=/workspace`——**必须**把仓库根挂载到 `/workspace`（Windows 示例 `-v "D:/xiyouji:/workspace"`）；未挂载时启动自检 FATAL，属设计行为。
- 健康检查：`HEALTHCHECK` 探 `GET /api/health`。
- `ADMIN`/密钥仅经 `--env-file .env` 注入；镜像内不含 `.env`（.dockerignore 已排除）。

## 3. 明确不做（Negative Scope）

- 不提供公网部署形态（无 TLS/鉴权/多租户/配额——那是 WP-B-ALT 触发后的独立批次）。
- 不支持多用户隔离（单 `data/chat.db`，单人本地使用）。
