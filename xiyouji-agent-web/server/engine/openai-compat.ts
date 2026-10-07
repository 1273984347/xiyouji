// engine/openai-compat.ts — OpenAI-compatible chat/completions 流式驱动（W680）。
// 兼容性守则（全主流大模型适配）：
//  - 端点/模型全由配置传入，代码零厂商分支；
//  - SSE 解析容忍 CRLF、`data:` 前后空格差异、`:` 注释行、choices 空数组（usage chunk）；
//  - 忽略 reasoning_content 等未知 delta 字段（DeepSeek-R1/GLM-thinking 类推理轨迹不入正文）；
//  - tool_calls 增量按 index 装配（id/name/arguments 可跨 chunk 分片到达）。
import type { ChatMessage, StreamEvent, ToolDef } from "./types.js";

export interface StreamChatOptions {
  baseUrl: string;
  apiKey: string;
  model: string;
  messages: ChatMessage[];
  tools?: ToolDef[];
  signal?: AbortSignal;
  /** 仅供测试注入；生产省略。 */
  fetchImpl?: typeof fetch;
}

interface ToolCallDelta {
  index?: number;
  id?: string;
  function?: { name?: string; arguments?: string };
}

function joinUrl(base: string, path: string): string {
  const b = base.replace(/\/+$/, "");
  return `${b}${path}`;
}

export async function* streamChat(opts: StreamChatOptions): AsyncGenerator<StreamEvent> {
  const doFetch = opts.fetchImpl ?? fetch;
  const body: Record<string, unknown> = {
    model: opts.model,
    messages: opts.messages,
    stream: true,
  };
  if (opts.tools && opts.tools.length > 0) body.tools = opts.tools;

  const resp = await doFetch(joinUrl(opts.baseUrl, "/chat/completions"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${opts.apiKey}`,
    },
    body: JSON.stringify(body),
    signal: opts.signal,
  });

  if (!resp.ok) {
    const errText = await resp.text().catch(() => "");
    throw new Error(`LLM API ${resp.status}: ${errText.slice(0, 300) || resp.statusText}`);
  }
  if (!resp.body) throw new Error("LLM API 响应无正文流");

  // tool_calls 增量装配（按 index）
  const calls = new Map<number, { id: string; name: string; arguments: string }>();
  let finishReason: string | null = null;

  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      let nl: number;
      while ((nl = buffer.indexOf("\n")) !== -1) {
        const rawLine = buffer.slice(0, nl).replace(/\r$/, "");
        buffer = buffer.slice(nl + 1);
        const line = rawLine.trim();
        if (!line || line.startsWith(":")) continue; // 空行 / SSE 注释（keep-alive）
        if (!line.startsWith("data:")) continue;
        const payload = line.slice(5).trim();
        if (payload === "[DONE]") {
          yield {
            type: "finish",
            reason: finishReason,
            toolCalls: [...calls.keys()].sort((a, b) => a - b).map((k) => {
              const c = calls.get(k)!;
              return { id: c.id || `call_${k}`, name: c.name, arguments: c.arguments }; // 空 id 兜底（严格端点对空 tool_call_id 会 400）
            }),
          };
          return;
        }
        let chunk: {
          choices?: Array<{
            delta?: {
              content?: string | null;
              reasoning_content?: string | null;
              tool_calls?: ToolCallDelta[];
            };
            finish_reason?: string | null;
          }>;
        };
        try {
          chunk = JSON.parse(payload);
        } catch {
          continue; // 容忍个别厂商的非 JSON 心跳行
        }
        const choice = chunk.choices?.[0];
        if (!choice) continue; // usage-only chunk 等
        const delta = choice.delta;
        if (delta && typeof delta.content === "string" && delta.content.length > 0) {
          yield { type: "text_delta", delta: delta.content };
        }
        // delta.reasoning_content 有意忽略（推理轨迹不进正文/事件流）
        if (delta && Array.isArray(delta.tool_calls)) {
          for (const tc of delta.tool_calls) {
            const idx = typeof tc.index === "number" ? tc.index : 0;
            const cur = calls.get(idx) ?? { id: "", name: "", arguments: "" };
            if (tc.id) cur.id = tc.id;
            if (tc.function?.name) cur.name = tc.function.name;
            if (tc.function?.arguments) cur.arguments += tc.function.arguments;
            calls.set(idx, cur);
          }
        }
        if (choice.finish_reason) finishReason = choice.finish_reason;
      }
    }
    // 流正常结束但未见 [DONE]（个别端点直连断开）——仍产出已装配结果
    yield {
      type: "finish",
      reason: finishReason,
      toolCalls: [...calls.keys()].sort((a, b) => a - b).map((k) => {
        const c = calls.get(k)!;
        return { id: c.id || `call_${k}`, name: c.name, arguments: c.arguments };
      }),
    };
  } finally {
    reader.releaseLock();
  }
}
