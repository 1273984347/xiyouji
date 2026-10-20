/**
 * setup.ts — vitest 全局测试准备（W808 新建）
 *
 * 职责边界：每个测试文件执行前跑一次的公共准备——注册 jest-dom 断言扩展、
 * 补齐 jsdom 缺失的浏览器 API（matchMedia / scrollIntoView / ResizeObserver）。
 *
 * 动因：agent-web 用了 TDesign 组件与 lucide 图标，它们在 jsdom 下会碰到
 * `window.matchMedia is not a function` 等缺失 API——不补则测试在渲染阶段就崩，
 * 与被测逻辑无关。
 */
import '@testing-library/jest-dom/vitest';
import { afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';

// TDesign / lucide 依赖的 matchMedia（jsdom 未实现）
if (!window.matchMedia) {
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: (query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: () => {},
      removeListener: () => {},
      addEventListener: () => {},
      removeEventListener: () => {},
      dispatchEvent: () => false,
    }),
  });
}

// 滚动相关 API（ChatMessages 的自动滚动用到 scrollIntoView）
if (!Element.prototype.scrollIntoView) {
  Element.prototype.scrollIntoView = function scrollIntoView() {
    /* jsdom 无布局，空实现即可 */
  };
}

// ResizeObserver（TDesign 部分组件用到）
if (!globalThis.ResizeObserver) {
  globalThis.ResizeObserver = class ResizeObserver {
    observe() {}
    unobserve() {}
    disconnect() {}
  } as unknown as typeof ResizeObserver;
}

// 每个测试后卸载已渲染组件，避免跨测试的 DOM 残留
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});
