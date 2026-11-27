// trace.test.ts — W1339（方案 D D-1/D-2）单测：trace 写入器 + 引擎逐轮 trace。
//
// 覆盖：① 只追加与回读（含 session 过滤）；② 坏行容忍计数；③ 留存期销毁；
//       ④ 写入失败 fail-open 但可见（degradation）；⑤ 错误消息脱敏/截断；
//       ⑥ runAgentTurn 的 turnTrace（有 usage / 无 usage 两态）。
// 运行：cd xiyouji-agent-web && node --import tsx --test server/trace.test.ts
import { test } from "node:test";
import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {
  appendTrace,
  readTrace,
  purgeExpiredTrace,
  traceDegradation,
  resetTraceDegradationForTest,
  traceLogPath,
} from "./trace.js";
import { runAgentTurn } from "./engine/agent-loop.js";
import type { AgentTurnOptions, StreamEvent } from "./engine/types.js";

function tmpTraceFile(): string {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "trace-test-"));
  return path.join(dir, "trace.jsonl");
}

function baseRecord(over: Partial<Parameters<typeof appendTrace>[0]> = {}) {
  return {
    session_id: "s-1",
    request_id: "r-1",
    model: "test-model",
    level: "info" as const,
    turns: 1,
    duration_ms: 12,
    usage_reported: true,
    input_tokens: 3,
    output_tokens: 4,
    total_tokens: 7,
    tool_calls: [],
    turn_trace: [],
    error: null,
    ...over,
  };
}

test("appendTrace 只追加 + readTrace 回读（含 session 过滤与坏行计数）", () => {
  const file = tmpTraceFile();
  const old = process.env.AGENT_WEB_TRACE_LOG;
  process.env.AGENT_WEB_TRACE_LOG = file;
  try {
    appendTrace(baseRecord({ request_id: "r-1", session_id: "s-1" }));
    appendTrace(baseRecord({ request_id: "r-2", session_id: "s-2" }));
    fs.appendFileSync(file, "not-json\n", "utf8");

    const all = readTrace(10);
    assert.equal(all.total, 2);
    assert.equal(all.skipped, 1);
    assert.deepEqual(all.entries.map((e) => e.request_id), ["r-1", "r-2"]);
    assert.equal(all.entries[0].schema_version, 1);
    assert.ok(all.entries[0].event_id.length > 0);

    const one = readTrace(10, { sessionId: "s-2" });
    assert.deepEqual(one.entries.map((e) => e.request_id), ["r-2"]);
    assert.equal(one.total, 2, "total 按全量计数（过滤只影响返回集）");
  } finally {
    if (old === undefined) delete process.env.AGENT_WEB_TRACE_LOG;
    else process.env.AGENT_WEB_TRACE_LOG = old;
  }
});

test("readTrace：文件不存在 = 空（不抛）", () => {
  const file = path.join(os.tmpdir(), "trace-does-not-exist-" + Date.now() + ".jsonl");
  const old = process.env.AGENT_WEB_TRACE_LOG;
  process.env.AGENT_WEB_TRACE_LOG = file;
  try {
    assert.equal(traceLogPath(), file);
    assert.deepEqual(readTrace(5), { entries: [], total: 0, skipped: 0 });
  } finally {
    if (old === undefined) delete process.env.AGENT_WEB_TRACE_LOG;
    else process.env.AGENT_WEB_TRACE_LOG = old;
  }
});

test("purgeExpiredTrace：只删早于留存期的记录，坏行保留（不因销毁误删）", () => {
  const file = tmpTraceFile();
  const old = process.env.AGENT_WEB_TRACE_LOG;
  process.env.AGENT_WEB_TRACE_LOG = file;
  try {
    const oldTs = new Date(Date.now() - 400 * 86400000).toISOString(); // 400 天前 > 180 天
    const newTs = new Date().toISOString();
    appendTrace(baseRecord({ request_id: "old", ts: oldTs }));
    appendTrace(baseRecord({ request_id: "new", ts: newTs }));
    fs.appendFileSync(file, "broken-line\n", "utf8");

    const r = purgeExpiredTrace();
    assert.equal(r.removed, 1);
    assert.equal(r.kept, 2, "新记录 + 坏行都保留");

    const after = readTrace(10);
    assert.deepEqual(after.entries.map((e) => e.request_id), ["new"]);
    assert.equal(after.skipped, 1, "坏行仍被读侧计为 skipped");
  } finally {
    if (old === undefined) delete process.env.AGENT_WEB_TRACE_LOG;
    else process.env.AGENT_WEB_TRACE_LOG = old;
  }
});

test("appendTrace：写入失败不抛（fail-open）但 degradation 可见", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "trace-test-dir-"));
  const old = process.env.AGENT_WEB_TRACE_LOG;
  const oldWarn = console.warn;
  process.env.AGENT_WEB_TRACE_LOG = dir; // 目标是目录 ⇒ appendFileSync 必失败
  console.warn = () => {}; // 静音本条预期告警，避免测试输出噪音
  resetTraceDegradationForTest();
  try {
    assert.doesNotThrow(() => appendTrace(baseRecord()));
    const d = traceDegradation();
    assert.equal(d.degraded, true);
    assert.equal(d.failures, 1);
    assert.ok(d.lastError && d.lastError.length > 0);
    assert.ok(d.lastErrorAt);
  } finally {
    console.warn = oldWarn;
    resetTraceDegradationForTest();
    if (old === undefined) delete process.env.AGENT_WEB_TRACE_LOG;
    else process.env.AGENT_WEB_TRACE_LOG = old;
  }
});

test("appendTrace：错误消息脱敏（sk-*）且截断 ≤ 301 字符", () => {
  const file = tmpTraceFile();
  const old = process.env.AGENT_WEB_TRACE_LOG;
  process.env.AGENT_WEB_TRACE_LOG = file;
  try {
    const long = "sk-abcdefgh12345678 " + "x".repeat(400);
    appendTrace(baseRecord({ level: "error", error: { name: "UpstreamError", message: long } }));
    const rec = readTrace(1).entries[0];
    assert.equal(rec.error?.name, "UpstreamError");
    assert.ok(!rec.error?.message.includes("sk-abcdefgh12345678"), "凭证形态必须脱敏");
    assert.ok(rec.error?.message.includes("sk-***"));
    assert.ok((rec.error?.message.length ?? 0) <= 301);
  } finally {
    if (old === undefined) delete process.env.AGENT_WEB_TRACE_LOG;
    else process.env.AGENT_WEB_TRACE_LOG = old;
  }
});

// ---- runAgentTurn 逐轮 trace（D-2）----

function sse(obj: unknown): string {
  return `data: ${JSON.stringify(obj)}`;
}

function fakeFetch(lines: string[]): typeof fetch {
  return (async () => new Response(lines.join("\n"), { status: 200 })) as unknown as typeof fetch;
}

/** 按调用次序返回不同响应（工具轮 → 文本轮）。 */
function seqFetch(responses: string[][]): typeof fetch {
  let i = 0;
  return (async () => {
    const lines = responses[Math.min(i, responses.length - 1)];
    i += 1;
    return new Response(lines.join("\n"), { status: 200 });
  }) as unknown as typeof fetch;
}

function turnOpts(fetchImpl: typeof fetch): AgentTurnOptions {
  return {
    config: { baseUrl: "http://llm.local/v1", apiKey: "k", model: "m" },
    messages: [{ role: "user", content: "问" }],
    toolset: { definitions: [], execute: async () => ({ content: "", isError: false }) },
    canUseTool: async () => ({ behavior: "allow" }),
    maxTurns: 3,
    handlers: { onText: () => {}, onToolCall: () => {}, onToolResult: () => {} },
    fetchImpl,
  };
}

test("runAgentTurn：逐轮 trace 记录轮次/耗时/正文长度/工具名/该轮 usage", async () => {
  const impl = fakeFetch([
    sse({ choices: [{ delta: { content: "心猿" } }] }),
    sse({ choices: [{ delta: {}, finish_reason: "stop" }] }),
    sse({ choices: [], usage: { prompt_tokens: 2, completion_tokens: 3, total_tokens: 5 } }),
    "data: [DONE]",
  ]);
  const result = await runAgentTurn(turnOpts(impl));
  assert.equal(result.turns, 1);
  assert.equal(result.turnTrace.length, 1);
  const t = result.turnTrace[0];
  assert.equal(t.turn, 1);
  assert.ok(t.durationMs >= 0);
  assert.equal(t.textChars, 2, "「心猿」两个字符");
  assert.deepEqual(t.toolCalls, []);
  assert.deepEqual(t.usage, { inputTokens: 2, outputTokens: 3, totalTokens: 5 });
  assert.deepEqual(result.usage, { inputTokens: 2, outputTokens: 3, totalTokens: 5 });
});

test("runAgentTurn：上游不回传 usage ⇒ 该轮 trace.usage=null（缺样本 ≠ 0）", async () => {
  const impl = fakeFetch([
    sse({ choices: [{ delta: { content: "甲" } }] }),
    sse({ choices: [{ delta: {}, finish_reason: "stop" }] }),
    "data: [DONE]",
  ]);
  const result = await runAgentTurn(turnOpts(impl));
  assert.equal(result.usage, null);
  assert.equal(result.turnTrace.length, 1);
  assert.equal(result.turnTrace[0].usage, null);
});

test("runAgentTurn：工具轮次写入 turnTrace.toolCalls（按模型请求顺序）", async () => {
  const impl = seqFetch([
    [
      sse({
        choices: [
          { delta: { tool_calls: [{ index: 0, id: "c1", function: { name: "read_file", arguments: '{"path":"a.md"}' } }] } },
        ],
      }),
      sse({ choices: [{ delta: {}, finish_reason: "tool_calls" }] }),
      "data: [DONE]",
    ],
    [
      sse({ choices: [{ delta: { content: "已读" } }] }),
      sse({ choices: [{ delta: {}, finish_reason: "stop" }] }),
      "data: [DONE]",
    ],
  ]);
  const result = await runAgentTurn(turnOpts(impl));
  assert.equal(result.turns, 2);
  assert.equal(result.turnTrace.length, 2);
  assert.deepEqual(result.turnTrace[0].toolCalls, ["read_file"]);
  assert.deepEqual(result.turnTrace[1].toolCalls, []);
  assert.equal(result.toolCalls.length, 1, "工具实际执行记录走 toolCalls（turnTrace 只留名字）");
});
