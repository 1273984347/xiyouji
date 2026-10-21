'use strict';

// 《取经录》离线全站桌面版 —— Electron 主进程。
// 启动流程：单实例锁 → 本地静态服务（127.0.0.1 随机端口）→ BrowserWindow 加载 → 中文菜单 → 自动更新。
// 诊断模式：`electron . --self-test` 不创建窗口，只验证内容服务可返回首页后退出（无窗口环境可跑）。

const http = require('node:http');
const path = require('node:path');
const { app, BrowserWindow, dialog, ipcMain, session, shell } = require('electron');

const { createContentServer } = require('./server.cjs');
const { resolveContentRoot, resolveContentVersion } = require('./paths.cjs');
const { createLogger } = require('./logger.cjs');
const { buildMenu } = require('./menu.cjs');
const updater = require('./updater.cjs');

const APP_USER_MODEL_ID = 'com.xiyouji.desktop';
const APP_TITLE = '取经录';
const SELF_TEST_FLAG = '--self-test';
const IS_SELF_TEST = process.argv.includes(SELF_TEST_FLAG);

const logger = createLogger(app);

let contentServer = null;
let mainWindow = null;
let selfTestExitDone = false;

app.setAppUserModelId(APP_USER_MODEL_ID);

// 单实例锁：自检模式允许在已有实例运行时执行（诊断用途）。
const hasSingleInstanceLock = app.requestSingleInstanceLock();
if (!hasSingleInstanceLock && !IS_SELF_TEST) {
  logger.log('[app] 检测到已有实例，本实例退出');
} else {
  bootstrap();
}

function bootstrap() {
  app.on('second-instance', () => {
    focusMainWindow();
  });

  registerProcessErrorHandlers();

  app.whenReady().then(onReady).catch((error) => {
    logger.logError('[app] whenReady 失败', error);
    if (!IS_SELF_TEST) {
      dialog.showErrorBox(`${APP_TITLE} 启动失败`, errorText(error));
    }
    app.exit(1);
  });

  app.on('before-quit', () => {
    closeContentServer();
  });

  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit();
    }
  });

  app.on('activate', () => {
    if (!IS_SELF_TEST && contentServer && BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    }
  });
}

function errorText(error) {
  if (error instanceof Error) {
    return error.stack || `${error.name}: ${error.message}`;
  }
  if (typeof error === 'string') {
    return error;
  }
  try {
    return JSON.stringify(error);
  } catch {
    return String(error);
  }
}

function registerProcessErrorHandlers() {
  process.on('uncaughtException', (error) => {
    logger.logError('[app] uncaughtException', error);
    showCrashDialog(error);
  });
  process.on('unhandledRejection', (reason) => {
    logger.logError('[app] unhandledRejection', reason);
    showCrashDialog(reason);
  });
}

function showCrashDialog(error) {
  if (IS_SELF_TEST) {
    return;
  }
  try {
    dialog.showErrorBox(`${APP_TITLE} 运行错误`, `应用遇到未预期的错误，详情已写入日志：\n${logger.file}\n\n${errorText(error)}`);
  } catch {
    // 对话框本身不可用时仅保留日志。
  }
}

async function onReady() {
  if (IS_SELF_TEST) {
    await runSelfTest();
    return;
  }

  const rootDir = resolveContentRoot(app);
  try {
    contentServer = await createContentServer({ rootDir });
    logger.log(`[app] 本地内容服务已启动：${contentServer.url}（root=${rootDir}）`);
  } catch (error) {
    logger.logError('[app] 本地内容服务启动失败', error);
    dialog.showErrorBox(`${APP_TITLE} 启动失败`, `本地内容服务启动失败：\n${errorText(error)}`);
    app.exit(1);
    return;
  }

  installSecurityPolicy();
  registerIpcHandlers();
  createMainWindow();
  updater.setupAutoUpdater({
    app,
    dialog,
    getWindow: () => mainWindow,
    log: (...args) => logger.log(...args),
  });
  buildMenu({
    app,
    dialog,
    shell,
    getWindow: () => mainWindow,
    checkForUpdates: () => updater.checkForUpdatesManually(),
  });

  const contentVersion = resolveContentVersion(app);
  logger.log(`[app] 应用版本 v${app.getVersion()}，内容批次 ${contentVersion.contentBatch || 'dev'}`);
}

function installSecurityPolicy() {
  session.defaultSession.setPermissionRequestHandler((_webContents, _permission, callback) => {
    callback(false);
  });
  if (typeof session.defaultSession.setPermissionCheckHandler === 'function') {
    session.defaultSession.setPermissionCheckHandler(() => false);
  }
}

function registerIpcHandlers() {
  ipcMain.handle('xiyouji:check-updates', async () => updater.checkForUpdatesManually());
  // 只读版本信息（preload 在 additionalArguments 不可用时的同步回退通道）。
  ipcMain.on('xiyouji:get-version', (event) => {
    event.returnValue = buildVersionInfo();
  });
}

function buildVersionInfo() {
  const contentVersion = resolveContentVersion(app);
  return {
    appVersion: app.getVersion(),
    contentBatch: contentVersion.contentBatch || 'dev',
    contentDate: contentVersion.contentDate || '',
    platform: process.platform,
  };
}

function createMainWindow() {
  const versionInfo = buildVersionInfo();
  const windowOptions = {
    width: 1440,
    height: 900,
    minWidth: 960,
    minHeight: 600,
    backgroundColor: '#faf7f2',
    title: APP_TITLE,
    icon: path.join(__dirname, '..', 'assets', 'icon.png'),
    show: false,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webSecurity: true,
      spellcheck: false,
      preload: path.join(__dirname, 'preload.cjs'),
      additionalArguments: [`--xiyouji-info=${encodeURIComponent(JSON.stringify(versionInfo))}`],
    },
  };

  mainWindow = new BrowserWindow(windowOptions);

  mainWindow.once('ready-to-show', () => {
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.show();
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  const webContents = mainWindow.webContents;

  webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:\/\//i.test(url)) {
      void shell.openExternal(url).catch((error) => logger.logError('[window] 打开外链失败', error));
    }
    return { action: 'deny' };
  });

  webContents.on('will-navigate', (event, targetUrl) => {
    if (isSameOrigin(targetUrl)) {
      return;
    }
    event.preventDefault();
    logger.warn(`[window] 已阻止导航到非同源地址：${targetUrl}`);
    if (/^https?:\/\//i.test(targetUrl)) {
      void shell.openExternal(targetUrl).catch((error) => logger.logError('[window] 打开外链失败', error));
    }
  });

  webContents.on('did-fail-load', (_event, errorCode, errorDescription, validatedUrl) => {
    logger.error(`[window] 页面加载失败 code=${errorCode} desc=${errorDescription} url=${validatedUrl}`);
  });

  mainWindow.loadURL(contentServer.url).catch((error) => {
    logger.logError('[window] loadURL 失败', error);
  });
}

function isSameOrigin(targetUrl) {
  try {
    const target = new URL(targetUrl);
    const base = new URL(contentServer.url);
    return target.origin === base.origin;
  } catch {
    return false;
  }
}

function focusMainWindow() {
  if (!mainWindow || mainWindow.isDestroyed()) {
    return;
  }
  if (mainWindow.isMinimized()) {
    mainWindow.restore();
  }
  mainWindow.show();
  mainWindow.focus();
}

function closeContentServer() {
  if (!contentServer) {
    return;
  }
  const server = contentServer;
  contentServer = null;
  logger.log('[app] 正在关闭本地内容服务');
  server.close().catch((error) => logger.logError('[app] 关闭本地内容服务失败', error));
}

// ---------------------------------------------------------------------------
// --self-test：不创建窗口，直接验证内容服务能返回首页，然后退出。
// 成功输出一行 `SELF_TEST_OK {"url":...,"bytes":...}` 并以 0 退出；
// 失败输出 `SELF_TEST_FAIL ...` 并以 1 退出。无窗口环境可跑。
// ---------------------------------------------------------------------------

function httpGet(targetUrl) {
  return new Promise((resolve, reject) => {
    const request = http.get(targetUrl, (response) => {
      const chunks = [];
      response.on('data', (chunk) => chunks.push(chunk));
      response.on('end', () => {
        resolve({
          statusCode: response.statusCode,
          headers: response.headers,
          body: Buffer.concat(chunks),
        });
      });
      response.on('error', reject);
    });
    request.on('error', reject);
    request.setTimeout(15000, () => {
      request.destroy(new Error('请求内容服务超时（15s）'));
    });
  });
}

async function runSelfTest() {
  let testServer = null;
  let exitCode = 1;
  let line = '';

  try {
    const rootDir = resolveContentRoot(app);
    testServer = await createContentServer({ rootDir });
    logger.log(`[self-test] 内容服务已启动：${testServer.url}`);

    const rootResponse = await httpGet(testServer.url);
    if (rootResponse.statusCode !== 200) {
      throw new Error(`GET "/" 期望 200，实际 ${rootResponse.statusCode}`);
    }
    const rootBody = rootResponse.body.toString('utf8');
    if (!rootBody.includes('西游记')) {
      throw new Error('GET "/" 响应体未包含「西游记」');
    }

    const indexUrl = new URL('index.html', testServer.url).href;
    const indexResponse = await httpGet(indexUrl);
    if (indexResponse.statusCode !== 200) {
      throw new Error(`GET "/index.html" 期望 200，实际 ${indexResponse.statusCode}`);
    }
    const indexBody = indexResponse.body.toString('utf8');
    if (!indexBody.includes('西游记')) {
      throw new Error('GET "/index.html" 响应体未包含「西游记」');
    }

    exitCode = 0;
    line = `SELF_TEST_OK ${JSON.stringify({
      url: testServer.url,
      bytes: rootResponse.body.length,
      indexBytes: indexResponse.body.length,
      status: rootResponse.statusCode,
    })}`;
  } catch (error) {
    line = `SELF_TEST_FAIL ${JSON.stringify({
      url: testServer ? testServer.url : null,
      error: error && error.message ? error.message : String(error),
    })}`;
  } finally {
    if (testServer) {
      await testServer.close().catch(() => {});
    }
  }

  writeSelfTestLine(exitCode, line);
}

function writeSelfTestLine(exitCode, line) {
  const exit = (code) => {
    if (selfTestExitDone) {
      return;
    }
    selfTestExitDone = true;
    app.exit(code);
  };
  try {
    process.stdout.write(`${line}\n`, () => exit(exitCode));
  } catch {
    exit(exitCode);
  }
  // stdout 不可用时兜底退出，避免自检进程悬挂。
  const timer = setTimeout(() => exit(exitCode), 5000);
  if (typeof timer.unref === 'function') {
    timer.unref();
  }
}
