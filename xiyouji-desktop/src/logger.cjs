'use strict';

// 极简文件日志：写入 <userData>/logs/main.log，每次启动截断（单文件轮转），
// 任何写盘失败都静默吞掉——日志系统自身绝不能拖垮应用。

const fs = require('node:fs');
const path = require('node:path');

function formatValue(value) {
  if (value instanceof Error) {
    return value.stack || `${value.name}: ${value.message}`;
  }
  if (typeof value === 'string') {
    return value;
  }
  try {
    return JSON.stringify(value);
  } catch {
    return String(value);
  }
}

/**
 * @param {import('electron').App} app Electron app 实例（用于定位 userData）
 * @returns {{ file: string, log: Function, warn: Function, error: Function, logError: Function }}
 */
function createLogger(app) {
  let logFile = '';
  try {
    const logDir = path.join(app.getPath('userData'), 'logs');
    fs.mkdirSync(logDir, { recursive: true });
    logFile = path.join(logDir, 'main.log');
    // 每次启动轮转：只保留本次运行的日志。
    fs.writeFileSync(logFile, '', 'utf8');
  } catch {
    logFile = '';
  }

  const write = (level, args) => {
    if (!logFile) {
      return;
    }
    const line = `[${new Date().toISOString()}] [${level}] ${args.map(formatValue).join(' ')}\n`;
    try {
      fs.appendFileSync(logFile, line, 'utf8');
    } catch {
      // 忽略：日志不可写不应导致进程异常。
    }
  };

  return {
    file: logFile,
    log: (...args) => write('INFO', args),
    warn: (...args) => write('WARN', args),
    error: (...args) => write('ERROR', args),
    logError: (context, error) => write('ERROR', [`${context}:`, formatValue(error)]),
  };
}

module.exports = { createLogger };
