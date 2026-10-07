// engine/agent-loop.ts — 工具循环（W680：替代旧厂商 SDK agent 循环的自主实现）。
// 语义：每轮 streamChat → 文本增量透传 handlers.onText → 若装配出 tool_calls 则逐个走
// canUseTool 权限桥 → 执行/拒绝 → 结果以 role:"tool" 回传继续；无工具调用即收尾。
// maxTurns 封顶 LLM 调用次数；文本跨轮累计（与旧 SDK fullResponse 口径一致）。
import { streamChat } from "./openai-compat.js";
import type {
  AgentTurnOptions,
  AgentTurnResult,
  ChatMessage,
  ToolCallRecord,
} from "./types.js";

export async function runAgentTurn(opts: AgentTurnOptions): Promise<AgentTurnResult> {
  const started = Date.now();
  const messages: ChatMessage[] = [...opts.messages];
  const toolCalls: ToolCallRecord[] = [];
  let fullText = "";
  let turns = 0;

  while (turns < opts.maxTurns) {
    turns += 1;
    if (opts.signal?.aborted) throw new Error("请求已中止");

    let turnText = "";
    let finishToolCalls: Array<{ id: string; name: string; arguments: string }> = [];

    for await (const ev of streamChat({
      baseUrl: opts.config.baseUrl,
      apiKey: opts.config.apiKey,
      model: opts.config.model,
      messages,
      tools: opts.toolset.definitions,
      signal: opts.signal,
      fetchImpl: opts.fetchImpl,
    })) {
      if (ev.type === "text_delta") {
        turnText += ev.delta;
        opts.handlers.onText(ev.delta);
      } else {
        finishToolCalls = ev.toolCalls;
      }
    }

    fullText += turnText;

    if (finishToolCalls.length === 0) {
      return { text: fullText, toolCalls, durationMs: Date.now() - started, turns };
    }

    // 回写 assistant（含 tool_calls 原始形态）
    messages.push({
      role: "assistant",
      content: turnText.length > 0 ? turnText : null,
      tool_calls: finishToolCalls.map((c) => ({
        id: c.id,
        type: "function" as const,
        function: { name: c.name, arguments: c.arguments },
      })),
    });

    for (const call of finishToolCalls) {
      let input: Record<string, unknown> = {};
      try {
        const parsed = call.arguments.trim() ? JSON.parse(call.arguments) : {};
        if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
          input = parsed as Record<string, unknown>;
        } else {
          throw new Error("工具参数不是对象");
        }
      } catch (e) {
        const msg = `工具参数解析失败（${call.name}）: ${e instanceof Error ? e.message : String(e)}`;
        toolCalls.push({ id: call.id, name: call.name, input: {}, status: "error", result: msg, isError: true });
        opts.handlers.onToolCall({ id: call.id, name: call.name, input: {} });
        opts.handlers.onToolResult(call.id, msg, true);
        messages.push({ role: "tool", tool_call_id: call.id, content: msg });
        continue;
      }

      opts.handlers.onToolCall({ id: call.id, name: call.name, input });

      const decision = await opts.canUseTool(call.name, input, { toolUseID: call.id });
      let execution;
      if (decision.behavior === "allow") {
        execution = await opts.toolset.execute(call.name, decision.updatedInput ?? input);
      } else {
        execution = { content: decision.message || "用户拒绝了此操作", isError: false };
      }

      opts.handlers.onToolResult(call.id, execution.content, execution.isError);
      toolCalls.push({
        id: call.id,
        name: call.name,
        input,
        status: decision.behavior === "allow" ? (execution.isError ? "error" : "completed") : "completed",
        result: execution.content,
        isError: execution.isError,
      });
      messages.push({ role: "tool", tool_call_id: call.id, content: execution.content });
    }
  }

  throw new Error(`已达最大轮次（maxTurns=${opts.maxTurns}），任务未完成`);
}
