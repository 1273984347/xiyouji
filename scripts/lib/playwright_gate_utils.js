#!/usr/bin/env node
/**
 * playwright_gate_utils.js — Playwright 门禁公共辅助（W775 重构提取）
 *
 * 被 check_chart_values / check_screenshot_gates 共用：
 * 统一 launch 参数、离线页面创建（file:// 直开 + 拦截外域 http(s)）、file:// 导航。
 *
 * 注意：check_data_drift.js 不依赖 Playwright，故本模块独立于 gate_common.js，
 * 由需要浏览器的门禁按需 require，避免无浏览器环境下的加载开销。
 */
'use strict';

const path = require('path');
const { toPosixPath } = require('./gate_common');

const DEFAULT_VIEWPORT = { width: 1280, height: 800 };
const DEFAULT_DEVICE_SCALE = 1;

/** 启动无头 Chromium（统一 headless 参数）。 */
async function launchHeadlessBrowser() {
  const { chromium } = require('playwright');
  return chromium.launch({ headless: true });
}

/**
 * 创建离线页面：拦截 http(s) 外域请求（站点设计口径 file:// 直开），
 * 并收集 pageerror。
 * @returns {Promise<{context: import('playwright').BrowserContext, page: import('playwright').Page, pageErrors: string[]}>}
 */
async function createOfflinePage(browser, viewport = DEFAULT_VIEWPORT) {
  const context = await browser.newContext({ viewport, deviceScaleFactor: DEFAULT_DEVICE_SCALE });
  const page = await context.newPage();
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(String((e && e.message) || e).slice(0, 300)));
  await page.route(
    (u) => u.protocol === 'http:' || u.protocol === 'https:',
    (route) => route.abort()
  );
  return { context, page, pageErrors };
}

/** file:// 导航到绝对路径。 */
async function gotoFileUrl(page, absPath, waitUntil = 'load', timeout = 20000) {
  const url = 'file:///' + toPosixPath(absPath);
  await page.goto(url, { waitUntil, timeout });
}

module.exports = {
  DEFAULT_VIEWPORT,
  launchHeadlessBrowser,
  createOfflinePage,
  gotoFileUrl,
};
