'use strict';

// 预加载脚本：sandbox: true 下运行，只通过 contextBridge 暴露只读版本信息与一个更新检查函数。
// 版本信息由主进程通过 webPreferences.additionalArguments 传入（--xiyouji-info=<URL 编码 JSON>），
// 预加载脚本不读取任何文件、不暴露任意 IPC 通道。

const { contextBridge, ipcRenderer } = require('electron');

const INFO_ARG_PREFIX = '--xiyouji-info=';
const CHECK_UPDATES_CHANNEL = 'xiyouji:check-updates';
const GET_VERSION_CHANNEL = 'xiyouji:get-version';

function readFallbackInfo() {
  return {
    appVersion: '',
    contentBatch: 'dev',
    contentDate: '',
    platform: typeof process === 'object' && process ? process.platform || '' : '',
  };
}

function readVersionInfo() {
  const fallback = readFallbackInfo();
  const argv = typeof process === 'object' && process && Array.isArray(process.argv) ? process.argv : [];
  const argument = argv.find((item) => typeof item === 'string' && item.startsWith(INFO_ARG_PREFIX));
  if (argument) {
    try {
      const decoded = JSON.parse(decodeURIComponent(argument.slice(INFO_ARG_PREFIX.length)));
      return {
        appVersion: String(decoded.appVersion || ''),
        contentBatch: String(decoded.contentBatch || 'dev'),
        contentDate: String(decoded.contentDate || ''),
        platform: String(decoded.platform || fallback.platform),
      };
    } catch {
      // 落到下面的同步 IPC 回退。
    }
  }
  // 回退：additionalArguments 不可用时，向主进程同步取只读版本信息。
  try {
    const info = ipcRenderer.sendSync(GET_VERSION_CHANNEL);
    if (info && typeof info === 'object') {
      return {
        appVersion: String(info.appVersion || ''),
        contentBatch: String(info.contentBatch || 'dev'),
        contentDate: String(info.contentDate || ''),
        platform: String(info.platform || fallback.platform),
      };
    }
  } catch {
    // 保持 fallback。
  }
  return fallback;
}

const versionInfo = readVersionInfo();

contextBridge.exposeInMainWorld('xiyouji', Object.freeze({
  appVersion: versionInfo.appVersion,
  contentBatch: versionInfo.contentBatch,
  contentDate: versionInfo.contentDate,
  platform: versionInfo.platform,
  checkForUpdates: () => ipcRenderer.invoke(CHECK_UPDATES_CHANNEL),
}));
