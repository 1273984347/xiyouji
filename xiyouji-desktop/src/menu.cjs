'use strict';

const { Menu } = require('electron');
const { resolveContentVersion } = require('./paths.cjs');

const ONLINE_SITE_URL = 'https://1273984347.github.io/xiyouji/';
const PROJECT_URL = 'https://github.com/1273984347/xiyouji';

function formatCount(value) {
  return value === undefined || value === null ? '?' : String(value);
}

/** 生成「关于」对话框正文：应用版本 + 内容批次 + 内容规模。 */
function buildAboutMessage(app, contentVersion) {
  const version = contentVersion || {};
  const appVersion = app && typeof app.getVersion === 'function' ? app.getVersion() : '';
  const batch = version.contentBatch || 'dev';
  const date = version.contentDate ? `（${version.contentDate}）` : '';
  const lines = [
    `取经录 桌面版 v${appVersion}`,
    `内容批次：${batch}${date}`,
  ];
  if (version.docCount || version.pageCount || version.vizCount) {
    lines.push(
      `内容规模：${formatCount(version.docCount)} 篇文档 · ${formatCount(version.pageCount)} 个页面 · ${formatCount(version.vizCount)} 个可视化`,
    );
  }
  lines.push('');
  lines.push('离线全站桌面版：全部内容随应用打包，无需联网即可浏览。');
  lines.push(`在线站点：${ONLINE_SITE_URL}`);
  lines.push(`项目主页：${PROJECT_URL}`);
  return lines.join('\n');
}

/**
 * 构建中文应用菜单（应用 / 编辑 / 视图 / 帮助）。
 * @param {{ app: import('electron').App, dialog: import('electron').Dialog,
 *          shell: import('electron').Shell,
 *          checkForUpdates: () => Promise<any>,
 *          getWindow?: () => (import('electron').BrowserWindow | null) }} options
 */
function buildMenu({ app, dialog, shell, checkForUpdates, getWindow }) {
  const isMac = process.platform === 'darwin';
  const contentVersion = resolveContentVersion(app);

  const showAbout = () => {
    const options = {
      type: 'info',
      title: `关于${app && app.name ? ` ${app.name}` : '取经录'}`,
      message: '取经录 桌面版',
      detail: buildAboutMessage(app, contentVersion),
      buttons: ['确定'],
      defaultId: 0,
      noLink: true,
    };
    let win = null;
    try {
      win = typeof getWindow === 'function' ? getWindow() : null;
    } catch {
      win = null;
    }
    if (win && !win.isDestroyed()) {
      return dialog.showMessageBox(win, options);
    }
    return dialog.showMessageBox(options);
  };

  const template = [];

  if (isMac) {
    template.push({ role: 'appMenu' });
  } else {
    template.push({
      label: '应用',
      submenu: [
        { label: '关于取经录', click: showAbout },
        { type: 'separator' },
        { label: '退出', role: 'quit' },
      ],
    });
  }

  template.push({
    label: '编辑',
    submenu: [
      { label: '撤销', role: 'undo' },
      { label: '重做', role: 'redo' },
      { type: 'separator' },
      { label: '剪切', role: 'cut' },
      { label: '复制', role: 'copy' },
      { label: '粘贴', role: 'paste' },
      { type: 'separator' },
      { label: '全选', role: 'selectAll' },
    ],
  });

  const viewSubmenu = [
    { label: '刷新', role: 'reload' },
    { label: '强制刷新', role: 'forceReload' },
    { type: 'separator' },
    { label: '实际大小', role: 'resetZoom' },
    { label: '放大', role: 'zoomIn' },
    { label: '缩小', role: 'zoomOut' },
    { type: 'separator' },
    { label: '全屏', role: 'togglefullscreen' },
  ];
  if (!app.isPackaged) {
    viewSubmenu.push({ type: 'separator' }, { label: '开发者工具', role: 'toggleDevTools' });
  }
  template.push({ label: '视图', submenu: viewSubmenu });

  template.push({
    label: '帮助',
    submenu: [
      {
        label: '检查更新…',
        click: () => {
          Promise.resolve()
            .then(() => checkForUpdates())
            .catch(() => {});
        },
      },
      { label: '访问在线站点', click: () => shell.openExternal(ONLINE_SITE_URL) },
      { type: 'separator' },
      { label: '关于', click: showAbout },
    ],
  });

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
  return menu;
}

module.exports = {
  buildMenu,
  buildAboutMessage,
  ONLINE_SITE_URL,
  PROJECT_URL,
};
