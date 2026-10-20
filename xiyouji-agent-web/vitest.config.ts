import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

/**
 * vitest.config.ts — 前端单元测试配置（W808 新建）
 *
 * 与 vite.config.ts **刻意分离**：vite.config.ts 承载 dev server 与代理（运行期形态），
 * 本文件只管测试期（jsdom 环境 + setup 文件 + 包含面）。两者共用 @vitejs/plugin-react
 * 以解析 JSX。
 *
 * 测试面分层（skill「三件套」之第一层·单元）：
 *   src/utils/*.test.ts      —— 纯函数与 client 逻辑（无 DOM 依赖）
 *   src/hooks/*.test.tsx     —— hook 行为（需 jsdom + @testing-library/react）
 * 包含面用 include 显式声明，**不扫 src 全部**——避免把组件渲染测试误纳入单测层
 * （组件级交互属 E2E 层，见 e2e/）。
 */
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    include: ['src/**/*.test.ts', 'src/**/*.test.tsx'],
    // e2e/ 目录不属单测层（那是 Playwright 层，由 e2e/ 独立配置驱动）
    exclude: ['node_modules/**', 'dist/**', 'e2e/**'],
    restoreMocks: true,
  },
});
