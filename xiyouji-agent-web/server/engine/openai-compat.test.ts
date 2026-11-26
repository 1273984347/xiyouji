// openai-compat.test.ts — W1334 usage 承接单测（node:test·经 tsx 运行）。
//
// 覆盖：① 请求侧携带 stream_options.include_usage；② usage 帧（choices 空数组）产出 usage 事件；
//       ③ 上游不回传 usage 时不产出 usage 事件（缺样本，不得凭空造 0）；
//       ④ 端点 400 拒收 stream_options 时回退重试一次（第二次不带该字段）；
//       ⑤ tool_calls 增量装配与 usage 互不干扰。
// 运行：cd xiyouji-agent-web && node --import tsx --test server/engine/openai-compat.test.ts
import { test } from "node:test";
import assert from "node:assert";
import { streamChat } from "./openai-compat.js";
import type { StreamEvent } from "./types.js";

const DONE = "data: [DONE]";

function sse(obj: unknown): string {
  return `data: ${JSON.stringify(obj)}`;
}

/** 把 SSE 文本包装成 Response（body 为可 getReader() 的流）。 */
function sseResponse(lines: string[], status = 200): Response {
  return new Response(lines.join("\n"), { status });
}

interface Captured {
  bodies: Array<Record<string, unknown>>;
}

/** 假 fetch：按调用次序取响应工厂，并记录每次请求体；超出序列则复用最后一个。 */
function fakeFetch(responses: Array<() => Response>): { impl: typeof fetch; captured: Captured } {
  const captured: Captured = { bodies: [] };
  let i = 0;
  const impl = (async (_url: string | URL | Request, init?: RequestInit) => {
    captured.bodies.push(JSON.parse(String(init?.body ?? "{}")) as Record<string, unknown>);
    const factory = responses[Math.min(i, responses.length - 1)];
    i += 1;
    return factory();
  }) as unknown as typeof fetch;
  return { impl, captured };
}

async function collect(gen: AsyncGenerator<StreamEvent>): Promise<StreamEvent[]> {
  const out: StreamEvent[] = [];
  for await (const ev of gen) out.push(ev);
  return out;
}

function textOf(events: StreamEvent[]): string[] {
  return events.filter((e) => e.type === "text_delta").map((e) => (e.type === "text_delta" ? e.delta : ""));
}

const baseOpts = {
  baseUrl: "http://llm.local/v1",
  apiKey: "test-key",
  model: "test-model",
  messages: [{ role: "user" as const, content: "问" }],
};

test("请求体携带 stream_options.include_usage（流式默认不回传 usage）", async () => {
  const { impl, captured } = fakeFetch([() => sseResponse([DONE])]);
  await collect(streamChat({ ...baseOpts, fetchImpl: impl }));
  assert.deepEqual(captured.bodies[0].stream_options, { include_usage: true });
});

test("usage 帧（choices 为空数组）产出 usage 事件，且不干扰 finish", async () => {
  const { impl } = fakeFetch([
    () =>
      sseResponse([
        sse({ choices: [{ delta: { content: "心猿" } }] }),
        sse({ choices: [{ delta: {}, finish_reason: "stop" }] }),
        sse({ choices: [], usage: { prompt_tokens: 12, completion_tokens: 34, total_tokens: 46 } }),
        DONE,
      ]),
  ]);
  const events = await collect(streamChat({ ...baseOpts, fetchImpl: impl }));
  const usage = events.filter((e) => e.type === "usage");
  assert.equal(usage.length, 1, "usage 帧必须产出且只产出一条 usage 事件");
  assert.deepEqual(usage[0].type === "usage" ? usage[0].usage : null, {
    inputTokens: 12,
    outputTokens: 34,
    totalTokens: 46,
  });
  assert.deepEqual(textOf(events), ["心猿"]);
  const finish = events.filter((e) => e.type === "finish");
  assert.equal(finish.length, 1);
  assert.equal(finish[0].type === "finish" ? finish[0].reason : undefined, "stop");
});

test("上游不回传 usage：不得凭空产出 usage 事件（缺样本 ≠ 0 token）", async () => {
  const { impl } = fakeFetch([
    () =>
      sseResponse([
        sse({ choices: [{ delta: { content: "甲" } }] }),
        sse({ choices: [{ delta: {}, finish_reason: "stop" }] }),
        DONE,
      ]),
  ]);
  const events = await collect(streamChat({ ...baseOpts, fetchImpl: impl }));
  assert.equal(events.filter((e) => e.type === "usage").length, 0);
});

test("usage 字段残缺时只补可推导项：total 缺失用 input+output 兜底", async () => {
  const { impl } = fakeFetch([
    () => sseResponse([sse({ choices: [], usage: { prompt_tokens: 5, completion_tokens: 7 } }), DONE]),
  ]);
  const events = await collect(streamChat({ ...baseOpts, fetchImpl: impl }));
  const usage = events.find((e) => e.type === "usage");
  assert.ok(usage && usage.type === "usage", "缺 total_tokens 仍应产出 usage（用恒等式兜底）");
  assert.deepEqual(usage && usage.type === "usage" ? usage.usage : null, {
    inputTokens: 5,
    outputTokens: 7,
    totalTokens: 12,
  });
});

test("端点 400 拒收 stream_options：回退重试一次且第二次不带该字段", async () => {
  const { impl, captured } = fakeFetch([
    () => sseResponse(["bad request: unknown field stream_options"], 400),
    () => sseResponse([sse({ choices: [{ delta: { content: "退" } }] }), DONE]),
  ]);
  const events = await collect(streamChat({ ...baseOpts, fetchImpl: impl }));
  assert.equal(captured.bodies.length, 2, "应恰好重试一次");
  assert.deepEqual(captured.bodies[0].stream_options, { include_usage: true });
  assert.equal("stream_options" in captured.bodies[1], false, "回退请求不得再带 stream_options");
  assert.deepEqual(textOf(events), ["退"], "回退后的正文流要正常产出");
});

test("tool_calls 增量装配与 usage 共存", async () => {
  const { impl } = fakeFetch([
    () =>
      sseResponse([
        sse({
          choices: [
            { delta: { tool_calls: [{ index: 0, id: "c1", function: { name: "read_file", arguments: '{"pa' } }] } },
          ],
        }),
        sse({ choices: [{ delta: { tool_calls: [{ index: 0, function: { arguments: 'th":"a.md"}' } }] } }] }),
        sse({ choices: [{ delta: {}, finish_reason: "tool_calls" }] }),
        sse({ choices: [], usage: { prompt_tokens: 1, completion_tokens: 2, total_tokens: 3 } }),
        DONE,
      ]),
  ]);
  const events = await collect(streamChat({ ...baseOpts, fetchImpl: impl }));
  const finish = events.find((e) => e.type === "finish");
  assert.ok(finish && finish.type === "finish");
  assert.equal(finish && finish.type === "finish" ? finish.toolCalls.length : -1, 1);
  assert.equal(finish && finish.type === "finish" ? finish.toolCalls[0].name : "", "read_file");
  assert.equal(finish && finish.type === "finish" ? finish.toolCalls[0].arguments : "", '{"path":"a.md"}');
  assert.equal(events.filter((e) => e.type === "usage").length, 1);
});
