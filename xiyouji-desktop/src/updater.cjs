'use strict';

// 自动更新：electron-updater + GitHub Releases。
// 仅在打包态且 XIYOUJI_DISABLE_UPDATE !== '1' 时启用；开发态菜单手动检查会提示「仅安装版支持」。
// 所有中文文案集中在本文件 MESSAGES 常量中。

const FIRST_CHECK_DELAY_MS = 3000;
const CHECK_INTERVAL_MS = 4 * 60 * 60 * 1000;

const MESSAGES = Object.freeze({
  updateAvailableTitle: '发现新版本',
  updateAvailable: (version) => `发现新版本 v${version}，是否现在下载？`,
  updateAvailableDetail: '下载在后台进行，完成后会提示重启安装。',
  downloadNow: '立即下载',
  later: '稍后',
  downloadedTitle: '更新已下载',
  downloaded: '新版本已下载，重启后生效。',
  downloadedDetail: (version) => `新版本 v${version} 已下载完成。选择「稍后」时，将在退出应用时自动安装。`,
  restartNow: '立即重启',
  upToDateTitle: '检查更新',
  upToDate: '当前已是最新版本。',
  errorTitle: '检查更新失败',
  errorMessage: '检查更新时出错，请稍后重试，或前往 GitHub Releases 手动下载最新版本。',
  disabledTitle: '检查更新',
  disabledMessage: '当前运行的是开发模式或已禁用自动更新；仅安装版支持自动更新。',
});

/** 当前更新上下文（由 setupAutoUpdater 注入）。 */
let context = null;

function safeCall(fn, ...args) {
  try {
    return fn(...args);
  } catch {
    return undefined;
  }
}

/**
 * @param {{ app: import('electron').App, dialog: import('electron').Dialog,
 *          getWindow: () => (import('electron').BrowserWindow | null),
 *          log: (...args: any[]) => void }} deps
 * @returns {boolean} 是否启用自动更新
 */
function setupAutoUpdater({ app, dialog, getWindow, log }) {
  const writeLog = typeof log === 'function' ? log : () => {};
  const state = {
    enabled: false,
    autoUpdater: null,
    manualCheck: false,
    errorDialogPending: false,
    timers: [],
    progressStep: -1,
  };

  if (!app || !app.isPackaged) {
    writeLog('[updater] 开发模式（app.isPackaged=false），自动更新未启用');
    context = { app, dialog, getWindow, writeLog, state };
    return false;
  }
  if (process.env.XIYOUJI_DISABLE_UPDATE === '1') {
    writeLog('[updater] 环境变量 XIYOUJI_DISABLE_UPDATE=1，自动更新已禁用');
    context = { app, dialog, getWindow, writeLog, state };
    return false;
  }

  let autoUpdater = null;
  try {
    ({ autoUpdater } = require('electron-updater'));
  } catch (error) {
    writeLog('[updater] electron-updater 加载失败，自动更新停用:', error && error.message ? error.message : error);
    context = { app, dialog, getWindow, writeLog, state };
    return false;
  }

  state.autoUpdater = autoUpdater;
  state.enabled = true;
  context = { app, dialog, getWindow, writeLog, state };

  autoUpdater.autoDownload = false;
  autoUpdater.autoInstallOnAppQuit = true;
  // 用最简单的自定义 logger 接入文件日志（不引入 electron-log 运行时依赖）。
  autoUpdater.logger = {
    info: (message) => writeLog('[updater]', message),
    warn: (message) => writeLog('[updater][warn]', message),
    error: (message) => writeLog('[updater][error]', message),
    debug: () => {},
  };

  const getAliveWindow = () => {
    const win = safeCall(() => (typeof getWindow === 'function' ? getWindow() : null));
    return win && !win.isDestroyed() ? win : null;
  };

  const showMessage = (options) => {
    const win = getAliveWindow();
    try {
      if (win) {
        return dialog.showMessageBox(win, options);
      }
      return dialog.showMessageBox(options);
    } catch (error) {
      writeLog('[updater] 对话框展示失败:', error && error.message ? error.message : error);
      return Promise.resolve({ response: 1 });
    }
  };

  const clearProgress = () => {
    state.progressStep = -1;
    const win = getAliveWindow();
    if (win) {
      safeCall(() => win.setProgressBar(-1));
    }
  };

  const setProgress = (percent) => {
    const win = getAliveWindow();
    if (!win) {
      return;
    }
    safeCall(() => win.setProgressBar(Math.max(0, Math.min(1, percent / 100))));
  };

  const handleError = (error) => {
    writeLog('[updater] 更新出错:', error && error.message ? error.message : error);
    if (!state.manualCheck || state.errorDialogPending) {
      return;
    }
    state.manualCheck = false;
    state.errorDialogPending = true;
    Promise.resolve(
      showMessage({
        type: 'error',
        title: MESSAGES.errorTitle,
        message: MESSAGES.errorMessage,
        detail: String(error && error.message ? error.message : error),
        buttons: ['确定'],
        defaultId: 0,
        noLink: true,
      }),
    ).finally(() => {
      state.errorDialogPending = false;
    });
  };

  autoUpdater.on('checking-for-update', () => {
    writeLog('[updater] 正在检查更新…');
  });

  autoUpdater.on('update-available', (info) => {
    writeLog(`[updater] 发现新版本 v${info && info.version ? info.version : '?'}`);
    void showMessage({
      type: 'info',
      title: MESSAGES.updateAvailableTitle,
      message: MESSAGES.updateAvailable(info && info.version ? info.version : '?'),
      detail: MESSAGES.updateAvailableDetail,
      buttons: [MESSAGES.downloadNow, MESSAGES.later],
      defaultId: 0,
      cancelId: 1,
      noLink: true,
    }).then((result) => {
      if (result && result.response === 0) {
        state.manualCheck = false;
        writeLog('[updater] 用户选择立即下载');
        autoUpdater.downloadUpdate().catch(handleError);
      } else {
        writeLog('[updater] 用户选择稍后下载');
      }
    });
  });

  autoUpdater.on('download-progress', (progress) => {
    const percent = progress && Number.isFinite(progress.percent) ? progress.percent : 0;
    setProgress(percent);
    const step = Math.floor(percent / 10);
    if (step !== state.progressStep) {
      state.progressStep = step;
      writeLog(`[updater] 下载进度 ${Math.floor(percent)}%`);
    }
  });

  autoUpdater.on('update-downloaded', (info) => {
    clearProgress();
    writeLog(`[updater] 新版本 v${info && info.version ? info.version : '?'} 下载完成`);
    void showMessage({
      type: 'info',
      title: MESSAGES.downloadedTitle,
      message: MESSAGES.downloaded,
      detail: MESSAGES.downloadedDetail(info && info.version ? info.version : '?'),
      buttons: [MESSAGES.restartNow, MESSAGES.later],
      defaultId: 0,
      cancelId: 1,
      noLink: true,
    }).then((result) => {
      if (result && result.response === 0) {
        writeLog('[updater] 用户选择立即重启安装');
        setImmediate(() => {
          autoUpdater.quitAndInstall(false, true);
        });
      } else {
        writeLog('[updater] 用户选择稍后，退出应用时自动安装');
      }
    });
  });

  autoUpdater.on('update-not-available', () => {
    const wasManual = state.manualCheck;
    state.manualCheck = false;
    if (!wasManual) {
      writeLog('[updater] 当前已是最新版本（后台检查）');
      return;
    }
    writeLog('[updater] 当前已是最新版本（手动检查）');
    void showMessage({
      type: 'info',
      title: MESSAGES.upToDateTitle,
      message: MESSAGES.upToDate,
      buttons: ['确定'],
      defaultId: 0,
      noLink: true,
    });
  });

  autoUpdater.on('error', handleError);

  const runCheck = (manual) => {
    const currentApp = context && context.app;
    if (!state.enabled || !state.autoUpdater) {
      if (manual) {
        return showMessage({
          type: 'info',
          title: MESSAGES.disabledTitle,
          message: MESSAGES.disabledMessage,
          buttons: ['确定'],
          defaultId: 0,
          noLink: true,
        }).then(() => ({ ok: false, reason: 'disabled' }));
      }
      return Promise.resolve({ ok: false, reason: 'disabled' });
    }
    if (manual) {
      state.manualCheck = true;
    }
    writeLog(`[updater] 触发${manual ? '手动' : '后台'}检查（应用版本 ${currentApp && currentApp.getVersion ? currentApp.getVersion() : '?'}）`);
    return Promise.resolve(state.autoUpdater.checkForUpdates())
      .catch(handleError)
      .then(() => ({ ok: true }));
  };

  state.runCheck = runCheck;

  // 启动 3 秒后首次检查，之后每 4 小时复查一次。
  const firstTimer = setTimeout(() => {
    void runCheck(false);
  }, FIRST_CHECK_DELAY_MS);
  if (typeof firstTimer.unref === 'function') {
    firstTimer.unref();
  }
  const intervalTimer = setInterval(() => {
    void runCheck(false);
  }, CHECK_INTERVAL_MS);
  if (typeof intervalTimer.unref === 'function') {
    intervalTimer.unref();
  }
  state.timers.push(firstTimer, intervalTimer);

  writeLog('[updater] 自动更新已启用（首次检查 3 秒后，之后每 4 小时一次）');
  return true;
}

/**
 * 手动检查更新（菜单/IPC 语境）：禁用态给出中文提示，可用态触发一次检查，
 * 结果通过 update-available / update-not-available / error 事件以对话框呈现。
 */
function checkForUpdatesManually() {
  if (!context) {
    return Promise.resolve({ ok: false, reason: 'not-initialized' });
  }
  if (!context.state || typeof context.state.runCheck !== 'function') {
    return Promise.resolve(
      context.dialog
        ? context.dialog
            .showMessageBox({
              type: 'info',
              title: MESSAGES.disabledTitle,
              message: MESSAGES.disabledMessage,
              buttons: ['确定'],
              defaultId: 0,
              noLink: true,
            })
            .then(() => ({ ok: false, reason: 'disabled' }))
        : { ok: false, reason: 'disabled' },
    );
  }
  return Promise.resolve(context.state.runCheck(true));
}

function isEnabled() {
  return Boolean(context && context.state && context.state.enabled);
}

module.exports = {
  setupAutoUpdater,
  checkForUpdatesManually,
  isEnabled,
  MESSAGES,
  FIRST_CHECK_DELAY_MS,
  CHECK_INTERVAL_MS,
};
