#!/usr/bin/env node
// 构建前内容准备：把仓库站点快照与内容规模写入 generated/content-version.json。
// 内容真源：仓库根 site/ + CHANGELOG.md（批次段） + scripts/output/stats.json（计数口径）。
// 本脚本不复制 site/：electron-builder extraResources 直接取 ../site。

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const MODULE_DIR = path.dirname(fileURLToPath(import.meta.url));
const DESKTOP_ROOT = path.resolve(MODULE_DIR, '..');
const REPO_ROOT = path.resolve(DESKTOP_ROOT, '..');

// 新形态（W711 起）：### W803（2026-10-19）：标题
const MODERN_SECTION = /^### W(\d{3,})[（(](\d{4}-\d{2}-\d{2})[）)]/m;
// 历史形态（W001-W710）：### v2.3.304（2026-10-11）：W710 标题
const LEGACY_SECTION = /^### v[\d.]+[（(](\d{4}-\d{2}-\d{2})[）)][：:]\s*W(\d{3,})/m;

/**
 * 从 CHANGELOG 全文提取「首个」内容批次段（新形态或历史形态中位置更靠前者）。
 * @param {string} changelogText
 * @returns {{ contentBatch: string, contentDate: string }}
 */
export function extractContentBatch(changelogText) {
  const text = typeof changelogText === 'string' ? changelogText : '';
  const candidates = [];
  const modern = MODERN_SECTION.exec(text);
  if (modern) {
    candidates.push({ index: modern.index, contentBatch: `W${modern[1]}`, contentDate: modern[2] });
  }
  const legacy = LEGACY_SECTION.exec(text);
  if (legacy) {
    candidates.push({ index: legacy.index, contentBatch: `W${legacy[2]}`, contentDate: legacy[1] });
  }
  if (candidates.length === 0) {
    throw new Error('CHANGELOG.md 中未找到内容批次段（需形如「### W###（YYYY-MM-DD）」或「### vX.Y.Z（YYYY-MM-DD）：W###」）');
  }
  candidates.sort((a, b) => a.index - b.index);
  return { contentBatch: candidates[0].contentBatch, contentDate: candidates[0].contentDate };
}

/**
 * 读取 stats.json 单项数字。兼容实体格式 { value: 615 } 与裸数字 615。
 * @param {Record<string, unknown>} stats
 * @param {string} key
 */
export function readStatValue(stats, key) {
  const entry = stats ? stats[key] : undefined;
  if (typeof entry === 'number' && Number.isFinite(entry)) {
    return entry;
  }
  if (entry && typeof entry === 'object' && typeof entry.value === 'number' && Number.isFinite(entry.value)) {
    return entry.value;
  }
  throw new Error(`scripts/output/stats.json 缺少有效数字字段：${key}`);
}

/**
 * 计算 content-version.json 内容（不写盘，便于测试）。
 * @param {{ repoRoot?: string, desktopRoot?: string }} options
 */
export function computeContentVersion({ repoRoot = REPO_ROOT, desktopRoot = DESKTOP_ROOT } = {}) {
  const packagePath = path.join(desktopRoot, 'package.json');
  let packageJson;
  try {
    packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
  } catch (error) {
    throw new Error(`读取 ${packagePath} 失败：${error && error.message ? error.message : error}`);
  }
  const appVersion = packageJson && packageJson.version;
  if (!appVersion) {
    throw new Error(`${packagePath} 缺少 version 字段`);
  }

  const siteEntry = path.join(repoRoot, 'site', 'index.html');
  if (!fs.existsSync(siteEntry)) {
    throw new Error(`缺少站点入口文件：${siteEntry}（站点内容真源为仓库根 site/）`);
  }

  const changelogPath = path.join(repoRoot, 'CHANGELOG.md');
  let changelogText;
  try {
    changelogText = fs.readFileSync(changelogPath, 'utf8');
  } catch (error) {
    throw new Error(`读取 ${changelogPath} 失败：${error && error.message ? error.message : error}`);
  }
  const { contentBatch, contentDate } = extractContentBatch(changelogText);

  const statsPath = path.join(repoRoot, 'scripts', 'output', 'stats.json');
  let stats;
  try {
    stats = JSON.parse(fs.readFileSync(statsPath, 'utf8'));
  } catch (error) {
    throw new Error(`读取 ${statsPath} 失败：${error && error.message ? error.message : error}`);
  }

  return {
    appVersion: String(appVersion),
    contentBatch,
    contentDate,
    docCount: readStatValue(stats, 'a1_a6_docs'),
    pageCount: readStatValue(stats, 'html_total'),
    vizCount: readStatValue(stats, 'visualization_pages'),
    builtAt: new Date().toISOString(),
  };
}

/**
 * 写 generated/content-version.json（目录不存在则创建）。
 * @param {{ desktopRoot?: string, version: Record<string, unknown> }} options
 * @returns {string} 写入路径
 */
export function writeContentVersionFile({ desktopRoot = DESKTOP_ROOT, version } = {}) {
  if (!version || typeof version !== 'object') {
    throw new Error('writeContentVersionFile 需要 version 对象');
  }
  const generatedDir = path.join(desktopRoot, 'generated');
  fs.mkdirSync(generatedDir, { recursive: true });
  const targetPath = path.join(generatedDir, 'content-version.json');
  fs.writeFileSync(targetPath, `${JSON.stringify(version, null, 2)}\n`, 'utf8');
  return targetPath;
}

/** CLI 主流程：失败打印明确原因并以非 0 退出。 */
export function main() {
  try {
    const version = computeContentVersion();
    const targetPath = writeContentVersionFile({ version });
    console.log(`[prepare-content] 已生成 ${targetPath}`);
    console.log(`[prepare-content] 内容批次 ${version.contentBatch}（${version.contentDate}）· 文档 ${version.docCount} · 页面 ${version.pageCount} · 可视化 ${version.vizCount}`);
    return 0;
  } catch (error) {
    console.error(`[prepare-content] 失败：${error && error.message ? error.message : error}`);
    return 1;
  }
}

const isDirectRun = Boolean(process.argv[1]) && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href;
if (isDirectRun) {
  process.exitCode = main();
}

export { DESKTOP_ROOT, REPO_ROOT };
