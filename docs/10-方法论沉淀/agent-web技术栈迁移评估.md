# agent-web 技术栈大版本迁移评估

> 用途：`xiyouji-agent-web`（Web Agent「渡口问津」）主版本依赖升级的可行性评估与批次规划。
> 创建：2026-09-02（W536）·触发源：dependabot PR #9 / #11 CI 红灯
> 配套：`.github/dependabot.yml`（W536 起 agent-web 主版本升级单独排队）

## 零、结论摘要

**当前处置**：agent-web 的两个 major PR（#9 dev-deps、#11 prod-deps）**不合并**，dependabot 配置已加 `ignore: semver-major` 规则让它们退出每周自动更新队列，转为专项迁移批次处理。

**判断依据**：这两个 PR 各跨 1-3 个大版本（TypeScript 5→7、Vite 5→8、Tailwind 3→4、React 18→19、Express 4→5），属于**框架级范式变更**，不是"改几处类型错误"能吸收的。CI 暴露的两处报错只是最先撞上的门槛，其后还有配置迁移与运行时语义变更。

**成本再评估（本批实证修正了先验）**：实际迁移成本**低于初始预估**——Express 5 的三个经典破坏点在本仓暴露面为零（详见 §二），uuid 14 的 ESM-only 约束对本仓无影响。真正的成本集中在 **Tailwind v4 配置范式迁移** 与 **TypeScript 7 / Vite 8 的未知兼容性** 两项。

---

## 一、已验证事实（实证清单，非记忆推演）

| # | 事实 | 取证方式 |
|:--:|:---|:---|
| 1 | PR#9 / #11 的 CI 红灯根因各 1 处 | `gh run view --log-failed` 实拉日志 |
| 2 | PR#9 报错：`src/main.tsx(7,8) TS2882: Cannot find module or type declarations for side-effect import of './index.css'` | CI 日志（run 33387889224） |
| 3 | PR#11 报错：`src/pages/ChatPage.tsx(103,13) TS2322: RefObject<HTMLDivElement \| null> is not assignable to RefObject<HTMLDivElement>` | CI 日志（run 33387878932） |
| 4 | 两 PR 的完整版本跨度 | `gh api pulls/{9,11}/files` 取 package.json patch |
| 5 | Express 5 破坏点暴露面为零（无 `'*'` 通配路由、无 `req.query`、无 `res.send(status)`/`sendStatus`） | Grep `server/*.js` `server/*.ts` |
| 6 | uuid 仅前端 3 处使用（`src/hooks/useAgents.ts`、`src/hooks/useChat.ts` ×2），经 Vite 打包 | Grep + 读取 `src/hooks/` |
| 7 | Tailwind 确实在用：`src/index.css` 3 行 `@tailwind` 指令 + `tailwind.config.js` JS 配置（含 `theme.extend.colors` 自定义）+ `postcss.config.js` 挂 `tailwindcss` 插件 | 读文件 |
| 8 | 运行时入口是 `server/index.ts`（`tsx` 执行），`server/index.js` 为编译产物；`engines.node >= 20` | `package.json` |
| 9 | 本仓 ESLint 配置在 ESLint 9 下已失效（`.eslintrc.json` 不被读取，exit 2）—— W536 已迁移为 flat config | 本地 9.39.5 / 10.9.1 双版本实测 |

**未验证项（本批未做，需专项批次内验证）**：

- TypeScript 7 对本仓 `tsconfig.json` 选项（`allowImportingTsExtensions` / `verbatimModuleSyntax` / `moduleResolution: bundler`）的兼容性
- Vite 8 对 `vite.config.ts` 及 Node 版本下限的要求
- React 19 与 `tdesign-react` 1.18 / `@tdesign-react/chat` 的运行时兼容性
- Tailwind v4 下现有 `theme.extend` 自定义项（颜色/圆角/阴影等）的等价迁移写法
- better-sqlite3 13 的 Node ABI 与预编译产物可用性

---

## 二、分栈破坏点评估

评级口径：**高** = 必须改配置或代码且验证成本高；**中** = 需改动但路径明确；**低** = 已实证无影响或改动极小。

| 栈 | 版本跨度 | 评级 | 实证影响面 | 处置要点 |
|:---|:---|:--:|:---|:---|
| **Tailwind CSS** | 3.4 → 4.3 | **高** | `src/index.css` 3 行 `@tailwind` 指令 + `tailwind.config.js` JS 配置（含自定义 colors/borderRadius 等）+ `postcss.config.js` | v4 改 CSS-first 范式：`@import "tailwindcss"` 取代三条指令，`@theme` 块取代 `theme.extend`，PostCSS 插件改名 `@tailwindcss/postcss`（需新增依赖）。自定义项逐条转写 |
| **TypeScript** | 5.3 → 7.0 | **高** | 全量 `tsc -b`；已撞 TS2882（CSS side-effect import） | TS 7 是 Go 原生编译器重写版，选项兼容性未验证。CSS 导入问题可先由 `src/vite-env.d.ts`（`/// <reference types="vite/client" />`）或 `allowArbitraryExtensions` 解决 |
| **Vite** | 5.0 → 8.2 | **中高** | `vite.config.ts` + 构建脚本；`engines.node >= 20` | 跨 3 个大版本，Node 下限可能抬高至 22+；配置 API 需逐项核对。`@vitejs/plugin-react` 4→6 同步升 |
| **React / React DOM** | 18.2 → 19.2 | **中** | 已撞 TS2322（ref 类型）；`createRoot` 写法无需改 | `useRef<T>(null)` 返回类型变为 `RefObject<T \| null>`，下游 prop 类型需放宽。TDesign 组件库运行时兼容性未验证（见上） |
| **better-sqlite3** | 12.6 → 13.0 | **中** | 服务端原生模块 | 需匹配 Node ABI 的预编译产物，`npm ci` 后必须实跑一次服务端验证 |
| **dotenv** | 16.4 → 17.4 | **低** | 服务端读 `.env` | 主版本升级，API 基本稳定，需冒烟 |
| **uuid** | 11.1 → 14.0 | **低** | 仅前端 3 处，经 Vite 打包（本就 ESM） | v14 转 ESM-only——**本仓无影响**（服务端未使用） |
| **Express** | 4.18 → 5.2 | **低**（修正先验） | 无 `'*'` 通配路由、无 `req.query`、无 `res.send(status)` | 三大经典破坏点暴露面均为零；需冒烟验证中间件与错误处理链 |
| **@types/node** | 20 → 26 | **中** | 类型层 | 需与 Node 运行时版本对齐，否则类型与运行时脱节 |
| **TDesign 系** | tdesign-react 1.12→1.18、tdesign-icons-react 0.5→0.6 | **中** | 全量 UI | 版本跨度不大但需视觉回归；与 React 19 的组合兼容性未验证 |

---

## 三、建议迁移顺序

按「先解耦、后升级」排序，每个阶段独立可验证、可回滚：

1. **阶段 1（低风险前置）**：`dotenv` → `uuid` → `Express 5` → `@types/node`。四项均有明确验证手段，且 Express 5 破坏面已实证为零。完成后服务端即可跑在 Express 5 上。
2. **阶段 2（类型层）**：`TypeScript 7` + `@types/react 19` + `@types/react-dom 19`。先解决 TS2882（加 `vite-env.d.ts`）与 TS2322（放宽 ref prop 类型），拿到 0 error 的类型基线。
3. **阶段 3（构建层）**：`Vite 8` + `@vitejs/plugin-react 6`。需确认 Node 版本下限，必要时同步调整 `engines` 与 CI 的 Node 版本矩阵。
4. **阶段 4（样式层，成本最高）**：`Tailwind v4` 配置范式迁移 + `postcss` 插件替换 + 自定义 theme 转写。建议单独一批，配合视觉回归截图验证。
5. **阶段 5（UI 层）**：`React 19` + `tdesign-react` 1.18。放在最后，因为组件库兼容性依赖前面各层的稳定性，且验证需人工走查。

每个阶段结束的硬门禁：本地 `npm run build` 通过 + `pytest` 全绿 + CI 全绿 + 关键页面截图无视觉回归。

---

## 四、决策选项与当前处置

| 选项 | 说明 | 代价 |
|:--:|:---|:---|
| **A（当前采用）** | 暂不迁移，dependabot 忽略 agent-web 主版本升级，登记为专项待办 | agent-web 停留在旧技术栈；安全修复若落在 major 版本需人工判断 |
| B | 按 §三 分 5 个阶段逐栈迁移 | 5 个批次的工程量，且需人工视觉回归 |
| C | 最小可用迁移——只做阶段 1（4 个低风险包） | 收益有限（React/TS/Vite 仍落后），但半小时内可闭环 |

**当前采用 A 的原因**：项目战略重心是发布与读者数据验证（决策闸门待 GoatCounter UV 回填），agent-web 是平行入口而非主站；在主站数据未验证前，投入 5 个批次做子项目技术栈迁移的优先级不足。

**解除条件**：任一时刻决定做迁移时，删除 `.github/dependabot.yml` 中 agent-web 段的 `ignore` 规则，dependabot 会在下次扫描重新生成 PR。

---

## 五、相关文件

- `.github/dependabot.yml`：W536 起 agent-web 主版本升级单独排队（含解除条件注释）
- `eslint.config.mjs`：W536 新建，flat config（`.eslintrc.json` 自 ESLint 9 起已失效）
- `docs/10-方法论沉淀/前端显示问题诊断SOP.md`：视觉回归验证方法
