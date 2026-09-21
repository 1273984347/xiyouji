# xiyouji-agent-web — 本地/内网部署镜像（W596）
# 定位：本地工程工具（仅回环设计）；如需容器内访问即映射 -p 3000:3000，
# 公网暴露需自行前置反代 + 鉴权 + 配额（见 docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md WP-B-ALT）。
# 构建示例：docker build -t xiyouji-agent-web .
# 运行示例：docker run --rm -p 3000:3000 --env-file .env -v "<仓库根>:/workspace" xiyouji-agent-web
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --no-audit --no-fund
COPY . .
# 容器内工作目录：配合 -v "<仓库根>:/workspace" 使用；未挂载时启动自检会 FATAL 提示（设计行为）
ENV PROJECT_CWD=/workspace
ENV NODE_ENV=production
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD wget -qO- http://127.0.0.1:3000/api/health >/dev/null 2>&1 || exit 1
CMD ["npx", "tsx", "server/index.ts"]
