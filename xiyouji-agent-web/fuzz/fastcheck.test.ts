// fuzz/fastcheck.test.ts — 属性测试面（property-based testing）。
//
// 为什么在 Jazzer 之外再加一层：OpenSSF Scorecard 的「Fuzzing」检查对 JS/TS 项目
// 只认 **fast-check 的 import**（其 languageFuzzSpecs 按 fast-check 关键字检出），
// 不认 Jazzer.js ⇒ 只接 Jazzer 时该检查项不会转绿。故本文件用 fast-check 表达
// 同一组不变量，两层互为补充：
//   · fuzz/fuzz.ts  → Jazzer.js 覆盖率引导的字节流 fuzz（随机输入）
//   · fuzz/fastcheck.test.ts → fast-check 属性测试（结构化生成 + 收缩）
//
// 被测对象均为 server/engine/tools.ts 的**真实导出**（不臆造 API）：
//   ① createToolset(cwd).execute("run_command") —— 内部走 tokenize() 切词 +
//      runAllowed() 白名单正则；首 token 固定为非白名单词 ⇒ 必被拒 ⇒ **不 spawn 子进程**
//   ② childEnv() —— 子进程环境变量构造，剔除 llm_api_key / agent_web_token 及其大小写变体
//
// 运行方式（在 xiyouji-agent-web/ 目录下执行）：npm run test:prop

import test from "node:test";
import assert from "node:assert/strict";
import fc from "fast-check";
import { createToolset, childEnv } from "../server/engine/tools.ts";

// tools.ts 的 run_command 分支在被拒时返回该文案。
const WHITELIST_HINT = "命令不在白名单";

// 凭证键的两个名字（大小写变体由属性生成器覆盖）。
const CREDENTIAL_KEYS = ["llm_api_key", "agent_web_token"] as const;

// 随机大小写变体：保留原字符集合，只打乱大小写 ⇒ 覆盖 Windows 环境变量名大小写不敏感的场景。
function randomCase(base: string): string {
  return base
    .split("")
    .map((ch) =>
      fc.sample(fc.boolean(), 1)[0] ? ch.toUpperCase() : ch.toLowerCase(),
    )
    .join("");
}

test("run_command 必须拒绝非白名单命令（任意命令尾巴）", async () => {
  const toolset = createToolset(process.cwd());
  await fc.assert(
    fc.asyncProperty(fc.string({ maxLength: 64 }), async (tail) => {
      const res = await toolset.execute("run_command", {
        command: `fuzzcmd ${tail}`,
      });
      assert.equal(res.isError, true, `未拒绝非白名单命令：${String(res.content)}`);
      assert.ok(
        String(res.content).includes(WHITELIST_HINT),
        `拒绝文案异常：${String(res.content)}`,
      );
    }),
    { numRuns: 50 },
  );
});

test("childEnv 必须剔除凭证变量的任意大小写变体", async () => {
  await fc.assert(
    fc.asyncProperty(
      fc.constantFrom(...CREDENTIAL_KEYS),
      fc.integer({ min: 0, max: 255 }),
      async (base, seed) => {
        // 用 seed 决定大小写组合，保证可复现。
        const key = base
          .split("")
          .map((ch, i) => ((seed >> (i % 8)) & 1 ? ch.toUpperCase() : ch.toLowerCase()))
          .join("");
        const original = process.env[key];
        try {
          process.env[key] = "prop-secret";
          const env = childEnv();
          for (const k of Object.keys(env)) {
            assert.ok(
              k.toLowerCase() !== base,
              `childEnv 未过滤凭证变量：${k}`,
            );
          }
        } finally {
          if (original === undefined) delete process.env[key];
          else process.env[key] = original;
        }
      },
    ),
    { numRuns: 50 },
  );
});

test("childEnv 不得误删普通环境变量", async () => {
  await fc.assert(
    fc.asyncProperty(
      fc.stringMatching(/^FCPROBE[A-Za-z0-9]{1,12}$/),
      fc.string({ maxLength: 16 }),
      async (name, value) => {
        const original = process.env[name];
        try {
          process.env[name] = value;
          const env = childEnv();
          assert.equal(env[name], value, `childEnv 误删普通变量：${name}`);
        } finally {
          if (original === undefined) delete process.env[name];
          else process.env[name] = original;
        }
      },
    ),
    { numRuns: 50 },
  );
});
