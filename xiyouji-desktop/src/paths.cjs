'use strict';

// 路径解析：区分打包态（extraResources 落位 process.resourcesPath）与开发态（仓库同级目录）。

const fs = require('node:fs');
const path = require('node:path');

// 开发态：xiyouji-desktop/src/ 的上两级是仓库根，站点在 <repo>/site/。
const DEV_CONTENT_ROOT = path.resolve(__dirname, '..', '..', 'site');
// 开发态：prepare:content 生成到 xiyouji-desktop/generated/content-version.json。
const DEV_CONTENT_VERSION = path.resolve(__dirname, '..', 'generated', 'content-version.json');

const DEFAULT_CONTENT_VERSION = Object.freeze({ contentBatch: 'dev' });

function isPackaged(app) {
  return Boolean(app && app.isPackaged);
}

/**
 * 站点内容根目录。
 * 打包态：<resources>/site（electron-builder extraResources from ../site to site）
 * 开发态：<repo>/site
 */
function resolveContentRoot(app) {
  if (isPackaged(app)) {
    return path.join(process.resourcesPath, 'site');
  }
  return DEV_CONTENT_ROOT;
}

/** content-version.json 路径。 */
function resolveContentVersionPath(app) {
  if (isPackaged(app)) {
    return path.join(process.resourcesPath, 'content-version.json');
  }
  return DEV_CONTENT_VERSION;
}

/**
 * 读取内容版本信息；文件缺失或损坏时返回 { contentBatch: 'dev' }，绝不抛错。
 * 正常内容形如 { appVersion, contentBatch: 'W803', contentDate: '2026-10-19',
 * docCount: 615, pageCount: 857, vizCount: 87, builtAt }。
 */
function resolveContentVersion(app) {
  const file = resolveContentVersionPath(app);
  try {
    const raw = fs.readFileSync(file, 'utf8');
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      return { ...DEFAULT_CONTENT_VERSION };
    }
    return parsed;
  } catch {
    return { ...DEFAULT_CONTENT_VERSION };
  }
}

module.exports = {
  resolveContentRoot,
  resolveContentVersion,
  resolveContentVersionPath,
  DEFAULT_CONTENT_VERSION,
  DEV_CONTENT_ROOT,
  DEV_CONTENT_VERSION,
};
