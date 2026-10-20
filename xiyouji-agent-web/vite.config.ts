import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  // 读取 .env（含非 VITE_ 前缀的键——共享 token 需要在服务端侧消费，不进浏览器包）
  const env = loadEnv(mode, process.cwd(), '');

  // W808：共享 token 由 dev server 在**代理层**注入请求头——
  // 浏览器全程不持有该 token（不进 JS bundle、不进 localStorage），与「禁存 token 于前端」的纪律一致。
  // 未设置 AGENT_WEB_TOKEN 时不注入（服务端此时也未开启鉴权，行为与重构前一致）。
  const agentToken = env.AGENT_WEB_TOKEN || '';

  // W808：代理目标可覆盖（E2E 测试需把代理指向测试实例端口·默认仍是 3000）
  const apiTarget = process.env.VITE_API_PROXY_TARGET || env.VITE_API_PROXY_TARGET || 'http://localhost:3000';

  return {
    plugins: [react()],
    server: {
      host: '127.0.0.1',  // P0-1 修复：dev server 不暴露到局域网/公网
      port: 5173,
      allowedHosts: true,
      proxy: {
        '/api': {
          target: apiTarget,
          changeOrigin: true,
          // W808：代理层注入共享 token（仅在服务端配置了 token 时）
          ...(agentToken ? { headers: { 'x-agent-token': agentToken } } : {}),
        }
      }
    },
    preview: {
      // W808：preview 模式同样提供 /api 代理（E2E 用 build 产物跑真实前端时需要）
      host: '127.0.0.1',
      port: 4173,
      proxy: {
        '/api': {
          target: apiTarget,
          changeOrigin: true,
          ...(agentToken ? { headers: { 'x-agent-token': agentToken } } : {}),
        }
      }
    },
    css: {
      preprocessorOptions: {
        less: {
          javascriptEnabled: true
        }
      }
    }
  };
});
