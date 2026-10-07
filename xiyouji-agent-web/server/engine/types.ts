// engine/types.ts — 引擎类型契约（W680 引擎更换）
// 被测协议 = OpenAI-compatible chat/completions（覆盖 GLM/DeepSeek/Kimi/Qwen/OpenAI/Gemini/Claude-compat/ollama/vLLM 等）。

/** 工具权限分类——服务端策略（index.ts canUseTool）据此放行/询问/拒绝。 */
export type ToolPermissionKind = "read" | "write" | "command";

/** 权限模式（与旧 SDK 时代四值语义一致）。 */
export type PermissionMode = "default" | "acceptEdits" | "plan" | "bypassPermissions";

/** canUseTool 决策（形状与旧 SDK PermissionResult 一致，前端许可桥零改动迁移）。 */
export interface PermissionDecision {
  behavior: "allow" | "deny";
  updatedInput?: Record<string, unknown>;
  message?: string;
}

export type CanUseTool = (
  toolName: string,
  input: Record<string, unknown>,
  options: { toolUseID: string }
) => Promise<PermissionDecision>;

/** OpenAI-compatible function 工具定义。 */
export interface ToolDef {
  type: "function";
  function: {
    name: string;
    description: string;
    parameters: Record<string, unknown>;
  };
}

/** 引擎内部消息（OpenAI chat 格式）。 */
export interface ChatMessage {
  role: "system" | "user" | "assistant" | "tool";
  content: string | null;
  tool_calls?: Array<{
    id: string;
    type: "function";
    function: { name: string; arguments: string };
  }>;
  tool_call_id?: string;
}

/** chat/completions 流式事件（由 openai-compat 产出）。 */
export type StreamEvent =
  | { type: "text_delta"; delta: string }
  | { type: "finish"; reason: string | null; toolCalls: Array<{ id: string; name: string; arguments: string }> };

/** 引擎工具执行结果。 */
export interface ToolExecution {
  content: string;
  isError: boolean;
}

export interface Toolset {
  definitions: ToolDef[];
  execute: (name: string, input: Record<string, unknown>) => Promise<ToolExecution>;
}

/** 已执行工具的记录（写库与前端 toolCalls 展示同构）。 */
export interface ToolCallRecord {
  id: string;
  name: string;
  input: Record<string, unknown>;
  status: "running" | "completed" | "error";
  result?: string;
  isError?: boolean;
}

/** agent 循环的流式处理器（index.ts 据此发 SSE）。 */
export interface AgentTurnHandlers {
  onText: (delta: string) => void;
  onToolCall: (call: { id: string; name: string; input: Record<string, unknown> }) => void;
  onToolResult: (toolId: string, content: string, isError: boolean) => void;
}

export interface AgentTurnOptions {
  config: { baseUrl: string; apiKey: string; model: string };
  /** 完整消息序列（system + 历史 + 本轮 user）。 */
  messages: ChatMessage[];
  toolset: Toolset;
  canUseTool: CanUseTool;
  maxTurns: number;
  signal?: AbortSignal;
  handlers: AgentTurnHandlers;
  /** 仅供测试注入 fetch 实现；生产省略。 */
  fetchImpl?: typeof fetch;
}

export interface AgentTurnResult {
  text: string;
  toolCalls: ToolCallRecord[];
  durationMs: number;
  turns: number;
}
