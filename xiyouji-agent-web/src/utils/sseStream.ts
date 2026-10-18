/**
 * sseStream.ts — SSE 帧解析复用层（W803-D 新建·自 useChat 提取）
 *
 * 职责边界：把 `ReadableStreamDefaultReader` 里按 `data: <JSON>\n\n` 排布的帧
 * 还原成事件对象序列。**只做解析，不解释事件语义**（谁消费哪个 type 由调用方决定）。
 *
 * 两条不能丢的实现细节（重构前 useChat 内联版如此，均为踩过坑的修复）：
 *  ① 解码器必须**跨块复用**——`TextDecoder` 有内部状态，逐块新建会把跨 chunk 断裂的
 *     多字节 UTF-8 字符（中文回复极易触发）解成替换符 U+FFFD；
 *  ② 必须**先解析后退出**（W568）——错误事件与 EOF 常合并进最后一个 chunk
 *     （`done=true` 且 `value` 非空），旧写法 `if (done) break` 会把该 chunk 整个丢弃，
 *     前端「思考中…」永久挂起；故 `decode(value, { stream: !done })` 后再判定退出。
 */
import type { ToolCall, PermissionRequest } from '../types';

/**
 * 服务端 SSE 事件（与 server/sse.ts 的写出器一一对应）。
 * 字段名即对外契约；`type` 是前端唯一的分派键。
 */
export type ChatStreamEvent =
  | { type: 'init'; sessionId: string; userMessageId: string; assistantMessageId: string; model: string }
  | { type: 'text'; content: string }
  | { type: 'citation_guard'; text: string; unverified: string[] }
  | { type: 'tool'; id?: string; name: string; input?: Record<string, unknown> }
  | { type: 'tool_result'; toolId?: string; content: unknown; isError?: boolean }
  | { type: 'done'; duration?: number }
  | { type: 'error'; message?: string }
  | { type: 'permission_request'; requestId: string; toolUseId: string; toolName: string; input: Record<string, unknown>; sessionId: string; timestamp: number };

/** 事件里出现的工具调用与权限请求形状（供 useChat 组装局部对象）。 */
export type { ToolCall, PermissionRequest };

/**
 * 逐个产出 SSE 事件。
 * 解析失败的帧**静默跳过**（心跳/注释行/半截 JSON 都不应中断整条流）。
 */
export async function* readChatStream(
  reader: ReadableStreamDefaultReader<Uint8Array>
): AsyncGenerator<ChatStreamEvent> {
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    // 先解析后退出（W568）：done 时 stream=false 让解码器吐出最终字符
    const chunk = decoder.decode(value, { stream: !done });

    for (const line of chunk.split('\n')) {
      if (!line.startsWith('data: ')) continue;
      try {
        yield JSON.parse(line.slice(6)) as ChatStreamEvent;
      } catch {
        // 忽略解析错误（重构前同款静默语义）
      }
    }

    if (done) break;
  }
}
