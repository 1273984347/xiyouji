// fuzz/fuzz.ts — OpenSSF Scorecard「Fuzzing」检查项的 fuzz target（JS/TS 工具面）。
//
// 被测目标（均取自 server/engine/tools.ts 的**真实导出**，不臆造 API）：
//   ① createToolset(cwd) —— 工具集工厂。其 execute("run_command") 内部先走
//      tokenize()（引号/转义切词）再走 runAllowed()（命令白名单正则）两条纯字符串路径。
//   ② childEnv() —— spawn 子进程环境变量构造；纯字符串大小写不敏感凭证过滤。
//      （TOOL_PERMISSION_KIND 为常量表，无字符串处理逻辑，故不作被测入口。）
//
// 运行方式（在 xiyouji-agent-web/ 目录下执行）：
//   npm run fuzz
//   package.json 的 scripts.fuzz 必须是：
//     "fuzz": "jazzer fuzz fuzz/fuzz.js"
//   （写成 "jazzer fuzz fuzz" 会被解析为 <包根>/fuzz.js——不存在 ⇒ ERR_MODULE_NOT_FOUND；
//    写成 "jazzer fuzz fuzz/fuzz.ts" 会被 Jazzer 补成 fuzz.ts.js ⇒ 同样找不到。）
//   故本目录提供 fuzz.js 作为 Jazzer 入口，逻辑本体在本 .ts 文件，两者导出同一个 fuzz。
//
// 依赖：@jazzer.js/core（由 package.json 的 devDependencies 提供·另一并行 Agent 改动）。
//   Jazzer.js 传给入口的入参是 Buffer；用 FuzzedDataProvider 把字节流解成字符串喂被测函数。

import { FuzzedDataProvider } from "@jazzer.js/core";
import { createToolset, childEnv } from "../server/engine/tools.ts";

// —— 不变量 1：命令白名单（runAllowed）必须拒绝白名单外的命令 ——
// 白名单提示串：tools.ts 的 run_command 分支在被拒时返回该文案。
const WHITELIST_HINT = "命令不在白名单";

// —— 不变量 2：凭证过滤（childEnv）必须大小写不敏感且不误伤 ——
// tools.ts 的 childEnv() 删除 llm_api_key / agent_web_token 及其任意大小写变体。
const CREDENTIAL_KEY_RE = /^(llm_api_key|agent_web_token)$/i;

// 逐个设置并立即还原：Windows 环境变量名大小写不敏感，同批设置多个大小写变体会互相覆盖。
function assertCredentialFiltered(key: string): void {
  const original = process.env[key];
  try {
    process.env[key] = "fuzz-secret";
    const env = childEnv();
    for (const k of Object.keys(env)) {
      if (CREDENTIAL_KEY_RE.test(k)) {
        throw new Error(`childEnv 未过滤凭证变量：${k}`);
      }
    }
  } finally {
    if (original === undefined) delete process.env[key];
    else process.env[key] = original;
  }
}

export async function fuzz(buffer: Buffer): Promise<void> {
  const data = new FuzzedDataProvider(buffer);
  const tail = data.consumeRemainingAsString();

  // ① 命令切词 + 白名单校验（tools.ts 的 run_command 分支）。
  // 首 token 固定为非白名单词 ⇒ 必然被拒 ⇒ **绝不会 spawn 子进程**（fuzz 无副作用）。
  // 尾部为 fuzz 字节流 ⇒ 覆盖 tokenize() 的引号/转义切词与 runAllowed() 的正则判定。
  const toolset = createToolset(process.cwd());
  const res = await toolset.execute("run_command", { command: `fuzzcmd ${tail}` });
  if (res.isError !== true) {
    throw new Error(`run_command 未拒绝非白名单命令：${res.content}`);
  }
  if (typeof res.content !== "string" || !res.content.includes(WHITELIST_HINT)) {
    throw new Error(`run_command 拒绝文案异常：${String(res.content)}`);
  }

  // ② 子进程环境变量凭证过滤（childEnv）。
  // 关键边界：大小写变体必须同样被剔除；非凭证键必须原样保留。
  for (const key of ["LLM_API_KEY", "Agent_Web_Token", "agent_web_token"]) {
    assertCredentialFiltered(key);
  }

  const safe = tail.replace(/[^A-Za-z0-9_]/g, "").slice(0, 24).toUpperCase();
  const probe = `FUZZPROBE${safe}`;
  const probeOriginal = process.env[probe];
  try {
    process.env[probe] = "fuzz-value";
    const env = childEnv();
    if (env[probe] !== "fuzz-value") {
      throw new Error(`childEnv 误删非凭证变量：${probe}`);
    }
  } finally {
    if (probeOriginal === undefined) delete process.env[probe];
    else process.env[probe] = probeOriginal;
  }
}
