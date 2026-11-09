// fuzz.js — Jazzer.js fuzz target 的**入口**（包根）。
//
// 路径语义（W1191 实测，两轮实证）：
//   "jazzer fuzz fuzz"        → 解析为 <包根>/fuzz.js      ⇒ 入口必须放包根
//   "jazzer fuzz fuzz/fuzz.js" → 同样解析为 <包根>/fuzz.js  ⇒ 放在子目录会被当成包根文件
//   "jazzer fuzz fuzz/fuzz.ts" → 被补成 fuzz.ts.js ⇒ 模块找不到
// ⇒ 入口固定为 <包根>/fuzz.js，被测逻辑本体在 fuzz/fuzz.ts（两者导出同一个 fuzz）。
//
// 被测目标与不变量见 fuzz/fuzz.ts 顶部注释（server/engine/tools.ts 的真实导出：
// createToolset 的命令白名单路径 / childEnv 的凭证过滤路径）。
//
// 运行方式（在 xiyouji-agent-web/ 目录下执行）：npm run fuzz

export { fuzz } from "./fuzz/fuzz.ts";
