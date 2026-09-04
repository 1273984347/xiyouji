// ESLint flat config — W536 新建
//
// 背景（实证，非记忆）：仓库根的 `.eslintrc.json` 自 ESLint 9 起已完全失效——
// ESLint 9 只读取 `eslint.config.*`，找不到时直接 exit 2 并拒绝运行（本地 9.39.5 实测确认）。
// 此前该故障一直未暴露，原因是 `scripts/node_modules` 长期未安装 eslint，
// `make lint` 走 `shutil.which('eslint')` 分支判定为「未安装」而 skip。
// ESLint 10 已彻底移除 eslintrc 支持，故本批迁移为 flat config，让 `make lint` 的 lint 契约真正成立。
//
// 设计取舍：
//   1. 零新增依赖——不引 `globals` 包，改为手写全局白名单（本仓 JS 体量小，白名单够用且可控）。
//   2. 只覆盖本仓自写 JS。第三方自托管库（d3/three/sankey/goatcounter）、一次性诊断脚本
//      （`scripts/_*.js`，按项目约定不入库门禁）、Playwright 浏览器二进制（`scripts/.pw-browsers/`）
//      一律忽略，避免用第三方代码的问题淹没本仓信号。
//   3. 规则集与原 .eslintrc.json 保持一致（no-unused-vars warn / no-undef error / no-console off），
//      不做规则扩容，避免一次性引入大量存量告警。
//   4. Service Worker 走独立 global 组（self/caches/clients 等）。

const browserGlobals = {
  window: 'readonly',
  document: 'readonly',
  console: 'readonly',
  navigator: 'readonly',
  location: 'readonly',
  history: 'readonly',
  localStorage: 'readonly',
  sessionStorage: 'readonly',
  fetch: 'readonly',
  setTimeout: 'readonly',
  setInterval: 'readonly',
  clearTimeout: 'readonly',
  clearInterval: 'readonly',
  requestAnimationFrame: 'readonly',
  cancelAnimationFrame: 'readonly',
  queueMicrotask: 'readonly',
  alert: 'readonly',
  prompt: 'readonly',
  confirm: 'readonly',
  matchMedia: 'readonly',
  getComputedStyle: 'readonly',
  performance: 'readonly',
  crypto: 'readonly',
  AbortController: 'readonly',
  Blob: 'readonly',
  CustomEvent: 'readonly',
  DOMParser: 'readonly',
  Element: 'readonly',
  Event: 'readonly',
  FileReader: 'readonly',
  FormData: 'readonly',
  HTMLElement: 'readonly',
  Image: 'readonly',
  MutationObserver: 'readonly',
  Node: 'readonly',
  NodeList: 'readonly',
  ResizeObserver: 'readonly',
  IntersectionObserver: 'readonly',
  TextDecoder: 'readonly',
  TextEncoder: 'readonly',
  URL: 'readonly',
  URLSearchParams: 'readonly',
  WebSocket: 'readonly',
  XMLHttpRequest: 'readonly',
  structuredClone: 'readonly',
  innerWidth: 'readonly',
  innerHeight: 'readonly',
  devicePixelRatio: 'readonly',
  screen: 'readonly',
  // 本仓已使用、且首轮扫描实证命中的标准 API（补齐后 4 处 no-undef 全部归零）
  PerformanceObserver: 'readonly',
  AbortSignal: 'readonly',
  XMLSerializer: 'readonly',
  DOMException: 'readonly',
  KeyboardEvent: 'readonly',
  MouseEvent: 'readonly',
  PointerEvent: 'readonly',
  WheelEvent: 'readonly',
  StorageEvent: 'readonly',
  MessageEvent: 'readonly',
  ErrorEvent: 'readonly',
  MediaQueryList: 'readonly',
  CanvasRenderingContext2D: 'readonly',
  WebGLRenderingContext: 'readonly',
  WebGL2RenderingContext: 'readonly',
  SVGSVGElement: 'readonly',
  Worker: 'readonly',
};

const nodeGlobals = {
  require: 'readonly',
  module: 'writable',
  exports: 'writable',
  process: 'readonly',
  Buffer: 'readonly',
  __dirname: 'readonly',
  __filename: 'readonly',
  global: 'readonly',
  setImmediate: 'readonly',
  clearImmediate: 'readonly',
};

const serviceWorkerGlobals = {
  self: 'readonly',
  caches: 'readonly',
  clients: 'readonly',
  registration: 'readonly',
  skipWaiting: 'readonly',
  importScripts: 'readonly',
  indexedDB: 'readonly',
  Request: 'readonly',
  Response: 'readonly',
  Headers: 'readonly',
  CacheStorage: 'readonly',
  ExtendableEvent: 'readonly',
  FetchEvent: 'readonly',
};

export default [
  {
    // 默认：本仓自写 JS（CommonJS / 浏览器脚本）
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: 'commonjs',
      globals: { ...browserGlobals, ...nodeGlobals },
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-undef': 'error',
      'no-console': 'off',
    },
  },
  {
    // ESM 文件（含本配置文件自身）
    files: ['**/*.mjs'],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: 'module',
      globals: { ...browserGlobals, ...nodeGlobals },
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-undef': 'error',
      'no-console': 'off',
    },
  },
  {
    // Service Worker：self / caches / clients 等专用全局
    files: ['site/sw.js'],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: 'script',
      globals: { ...browserGlobals, ...nodeGlobals, ...serviceWorkerGlobals },
    },
  },
  {
    ignores: [
      'node_modules/**',
      // Playwright 下载的浏览器二进制，非本仓代码
      'scripts/.pw-browsers/**',
      // 一次性诊断/批处理脚本（项目约定：`_` 前缀不入库门禁）
      'scripts/_*.js',
      // 生成物
      'scripts/output/**',
      // 子项目：xiyouji-agent-web 有独立工具链
      'xiyouji-agent-web/**',
      // 第三方自托管库
      'site/static/js/d3.v7.min.js',
      'site/static/js/three.r128.min.js',
      'site/static/js/d3-sankey.min.js',
      'site/static/js/goatcounter.js',
      'hyperframes/**',
    ],
  },
];
