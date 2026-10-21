# 取经录 · 离线全站桌面版（xiyouji-desktop）

《取经录》的桌面客户端：把整个静态站点（全部解读文档、全站页面、全部数据可视化）打包进安装包，双击即开——**无需联网、无需浏览器**。安装版支持从 GitHub Releases 自动更新。

- **应用版本**：v2.3.0（首个桌面版，独立于站点内容批次的 semver，发布 tag 为 `v2.3.0`）
- **内容批次**：随发布构建注入，不写死在文档里——见应用内「帮助 → 关于」对话框，或安装目录 `resources/content-version.json`
- **内容来源**：仓库根 `site/` 的构建时快照（站点更新 → 随下一个应用版本打包发布）

> 本目录是桌面应用工程（Electron 主进程、本地内容服务、自动更新、打包配置与测试）。站点本身仍在仓库根 `site/`，不在此目录复制副本。

---

## 一、下载安装

**最新版本页**：<https://github.com/1273984347/xiyouji/releases/latest>

**固定直链**（始终指向最新正式版，适合挂到文档/快捷方式里）：

| 平台 | 文件名 | 固定直链 |
|---|---|---|
| Windows x64 | `xiyouji-desktop-win-x64.exe` | <https://github.com/1273984347/xiyouji/releases/latest/download/xiyouji-desktop-win-x64.exe> |
| macOS universal | `xiyouji-desktop-mac-universal.dmg` | <https://github.com/1273984347/xiyouji/releases/latest/download/xiyouji-desktop-mac-universal.dmg> |
| Linux x64 | `xiyouji-desktop-linux-x86_64.AppImage` | <https://github.com/1273984347/xiyouji/releases/latest/download/xiyouji-desktop-linux-x86_64.AppImage> |

产物名在 `electron-builder.yml` 中固定为字面量（不使用 `${arch}` 模板），因此上面的直链不会随构建平台/架构变化而 404。

### Windows 10 / 11

1. 下载 `xiyouji-desktop-win-x64.exe`。
2. 双击运行。若出现 SmartScreen 提示，点「更多信息」→「仍要运行」（原因见下节「未签名提示」）。
3. 安装向导可选择安装目录，默认创建桌面快捷方式与开始菜单项。
4. 从开始菜单或桌面图标启动「取经录」。

### macOS 12 及以上

1. 下载 `xiyouji-desktop-mac-universal.dmg`（universal：同时支持 Apple Silicon 与 Intel）。
2. 双击打开 DMG，把「取经录」拖入「应用程序」。
3. **首次启动**：在「应用程序」中**右键**图标 →「打开」→ 在弹窗中再次确认「打开」。之后可正常双击启动。

### Linux（Ubuntu 20.04+ / 主流发行版）

```bash
chmod +x xiyouji-desktop-linux-x86_64.AppImage
./xiyouji-desktop-linux-x86_64.AppImage
```

若提示缺少 FUSE：`sudo apt install libfuse2`。也可直接双击 AppImage 运行。

---

## 二、自动更新

安装版（打包产物）启动 **3 秒后**自动检查更新，之后**每 4 小时**复查一次：

1. 发现新版本 → 弹窗「发现新版本 vX.Y.Z，是否现在下载？」，点「立即下载」后台下载（下载进度显示在任务栏图标）。
2. 下载完成 → 弹窗「新版本已下载，重启后生效」，点「立即重启」完成升级。
3. 选「稍后」也没关系：退出应用时会自动安装已下载的更新（`autoInstallOnAppQuit`）。

也可以随时手动检查：菜单「**帮助 → 检查更新…**」。当前已是最新版本时会弹出提示；检查失败时会给出错误说明（不会静默失败）。

- 开发模式（`npm start`）或设置环境变量 `XIYOUJI_DISABLE_UPDATE=1` 时自动更新被禁用，菜单手动检查会提示「仅安装版支持自动更新」。
- 更新源由 `electron-builder.yml` 的 `publish` 配置生成到 `resources/app-update.yml`（GitHub Releases：`1273984347/xiyouji`）。

### 未签名提示（务必先读）

当前发布构建**未做代码签名**（无 Apple Developer 证书 / Windows 代码签名证书）：

- **macOS**：Gatekeeper 会拦截首次双击，按上文「右键 → 打开」即可绕过；由于未签名，macOS 上的自动更新可能被系统阻止（见「已知限制」）。
- **Windows**：SmartScreen 可能提示「Windows 已保护你的电脑」，点「更多信息」→「仍要运行」即可。

---

## 三、系统要求与磁盘占用

| 平台 | 最低系统 | 安装包约 | 安装后磁盘约 |
|---|---|---|---|
| Windows | Windows 10（x64） | 约 125 MB | 约 425 MB |
| macOS | macOS 12（universal） | 约 135 MB | 约 440 MB |
| Linux | Ubuntu 20.04+（x64） | 约 125 MB | 约 430 MB |

占用主要来自两部分：Electron 运行时（约 370 MB 解包体积）与站点内容快照（约 55 MB）。以上为量级估算，各平台实际大小以发布页文件为准（Windows 安装包实测 130,705,240 字节）。

---

## 四、开发与构建

环境要求：**Node.js ≥ 22**（`package.json` 的 `engines.node`），Windows 上需 PowerShell 7 或 cmd。

```bash
cd xiyouji-desktop
npm install              # 安装依赖（electron / electron-builder / electron-updater 版本精确锁定）
npm start                # 开发模式启动（直接读仓库根 ../site/，无需先 prepare:content）
npm test                 # 单元测试（node:test，不依赖 electron 二进制、不联网）
npm run prepare:content  # 生成 generated/content-version.json（内容批次/规模）
npm run pack:dir         # 只打包目录（dist/win-unpacked，快速验证）
npm run dist:win         # Windows 安装包（dist/xiyouji-desktop-win-x64.exe + dist/latest.yml）
npm run dist:mac         # macOS DMG + ZIP（需在 macOS 上执行）
npm run dist:linux       # Linux AppImage（需在 Linux 上执行）
```

构建脚本与 CI 约定（名称固定，勿改）：

| 脚本 | 作用 |
|---|---|
| `start` | `electron .` 开发运行 |
| `test` | `node --test`（Node 自动发现 `tests/` 下 `*.test.mjs`；带目录参数的 `node --test tests/` 在 Node 22/24 会按模块路径导入而失败） |
| `prepare:content` | 读取 `../CHANGELOG.md` 首个 W 批次段 + `../scripts/output/stats.json`，写 `generated/content-version.json` |
| `pack:dir` / `dist:win` / `dist:mac` / `dist:linux` | `prepare:content` 后再调 electron-builder（本地构建一律 `--publish never`，真正发布在 CI） |

### 目录结构

```
xiyouji-desktop/
├── src/
│   ├── main.cjs        # 主进程：单实例锁、窗口、安全策略、--self-test
│   ├── server.cjs      # 127.0.0.1 随机端口静态服务（防目录穿越、MIME、缓存头）
│   ├── paths.cjs       # 打包态/开发态内容路径与 content-version 读取
│   ├── updater.cjs     # electron-updater 自动更新（中文对话框、4 小时轮询）
│   ├── menu.cjs        # 中文菜单（应用/编辑/视图/帮助）
│   ├── preload.cjs     # contextBridge 只暴露版本信息 + checkForUpdates()
│   └── logger.cjs      # userData/logs/main.log 文件日志
├── scripts/prepare-content.mjs   # 构建前内容版本准备
├── tests/                        # node:test 单测（服务/内容准备/配置契约）
├── assets/icon.png               # 512×512 应用图标（源自 site/static/icons/icon-512.png）
├── electron-builder.yml          # 三平台打包 + GitHub publish 配置
└── generated/content-version.json # 构建产物（.gitignore 忽略）
```

### 打包实现要点

- 应用代码（`src/**`）打进 `app.asar`；站点内容与内容版本文件走 `extraResources`：`../site` → `resources/site`，`generated/content-version.json` → `resources/content-version.json`。**不在本目录复制 site 副本。**
- 运行时主进程用 Node stdlib `http` 在 `127.0.0.1` 随机端口起本地服务，窗口加载 `http://127.0.0.1:<port>/`；只允许同源导航，外链交系统浏览器，权限请求全部拒绝。
- `resources/app-update.yml` 由 `publish` 配置自动生成，electron-updater 据此走 GitHub Releases。

### 诊断自检（无需窗口）

```bash
npx electron . --self-test
```

成功输出一行 `SELF_TEST_OK {"url":"http://127.0.0.1:..../","bytes":...}` 并以 0 退出；失败输出 `SELF_TEST_FAIL ...` 并以 1 退出。不创建窗口，可在无图形环境/CI 中运行。若运行环境的 Chromium 沙箱不可用（如受限会话），可加 `--no-sandbox --single-process` 再跑。

---

## 五、内容更新机制

- 站点内容真源是仓库根 `site/`，桌面版在**构建时**取快照打进安装包（`extraResources`）。
- 内容更新 = 发一个新应用版本：CI 跑 `prepare:content`（刷新内容批次/规模）→ electron-builder 打包 → 发布到 GitHub Releases；老用户经自动更新拿到新内容。
- `generated/content-version.json` 是「构建时注入」的：应用内「帮助 → 关于」显示内容批次、日期、文档数/页面数/可视化数；开发态缺失该文件时降级为 `contentBatch: "dev"`，不崩溃。
- 发版流程与 CI 工作流说明见仓库 `.github/workflows/` 目录下 README（发布流水线由 CI 负责，本目录只提供构建脚本）。

---

## 六、已知限制

1. **macOS 未签名**：当前构建 `identity: null`（无签名证书）。首次启动需右键→打开；且未签名应用的自动更新可能被 Gatekeeper 阻止，必要时请手动下载新版本 DMG 覆盖安装。
2. **Windows SmartScreen**：未签名 → 首次运行提示「更多信息 → 仍要运行」。
3. **Linux AppImage**：需要 `chmod +x`；部分发行版需安装 FUSE（`libfuse2`）。
4. **内容版本 = 打包时站点快照**：应用内看到的内容与「发布该版本时的仓库 site/」一致；站点线上更新后，桌面版需等新版本发布。
5. **离线为设计目标**：应用不发起内容请求；自动更新是唯一出站网络行为（可在菜单关闭：开发态/`XIYOUJI_DISABLE_UPDATE=1`，或安装后不点「立即下载」）。
6. **仅支持 x64/universal 桌面平台**：未提供 32 位（ia32）与 armv7l 构建；macOS 的 universal 包同时覆盖 Apple Silicon 与 Intel。
7. **本地构建**：macOS / Linux 产物需在对应系统（或 CI 对应 runner）构建，Windows 上只能构建 Windows 产物。

---

## 七、常见问题（FAQ）

**Q：安装后打开是白屏？**
A：应用启动时会先起本地内容服务再加载页面；若持续白屏，查看日志 `<用户数据目录>/logs/main.log`（Windows 为 `%APPDATA%\取经录\logs\main.log`），并把日志附到 GitHub Issue。

**Q：能离线用吗？**
A：可以，全部内容随安装包分发；断网仅影响自动更新检查。

**Q：更新后内容没变？**
A：自动更新只在发布新版本时触发；确认「帮助 → 关于」里的内容批次是否变化，或手动「帮助 → 检查更新…」。

**Q：如何完全卸载？**
A：Windows 在「设置 → 应用」卸载（默认保留用户数据，便于重装）；macOS 将应用拖入废纸篓；Linux 删除 AppImage 文件即可。
