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
 * 跨块行缓冲器（W825）：把「可能被网络分片切断的 SSE 帧」还原为完整行。
 *
 * 背景：服务端帧格式为 `data: <JSON>\n\n`（见 server/sse.ts:58），而一次网络读
 * 并不保证落在帧边界上——`read_file`/`run_command` 的 tool_result 帧可达 256KB~1MB
 * （server/engine/tools.ts 的 READ_MAX_BYTES / RUN_MAX_BUFFER），**必然被切成多片**。
 * 旧实现（此处与 useChat 内联版同款）逐片 `chunk.split('\n')` 后独立处理：
 *   · 第一片是半截 JSON → `JSON.parse` 抛错 → 被 `catch {}` 静默丢弃；
 *   · 第二片是 JSON 残段 → 不以 `data: ` 开头 → 被跳过；
 *   ⇒ **整帧事件凭空消失，无报错无日志**（工具条目永远停在「执行中…」、文本增量丢字）。
 *
 * 修法：把「最后一段可能是半行」留在缓冲里，跨片拼接后再切分。
 * 本函数是**唯一修复点**——`readChatStream` 与 `useChat` 的内联解析共用它，
 * 避免两处实现再次分叉（此前两份实现各自演进·修一处即漏另一处）。
 */
export interface SseLineSplitter {
  /** 喂入一个网络片，返回其中**完整**的行（末尾半行留在缓冲内）。 */
  push(chunk: string): string[];
  /** 流结束：冲刷残留半行（流末尾无换行时用）。 */
  flush(): string[];
}

export function createSseLineSplitter(): SseLineSplitter {
  let pending = '';
  return {
    push(chunk: string): string[] {
      pending += chunk;
      const lines = pending.split('\n');
      pending = lines.pop() ?? '';
      return lines;
    },
    flush(): string[] {
      const rest = pending ? [pending] : [];
      pending = '';
      return rest;
    },
  };
}

/**
 * 逐个产出 SSE 事件。
 * 解析失败的帧**静默跳过**（心跳/注释行/半截 JSON 都不应中断整条流）。
 */
export async function* readChatStream(
  reader: ReadableStreamDefaultReader<Uint8Array>
): AsyncGenerator<ChatStreamEvent> {
  const decoder = new TextDecoder();
  const splitter = createSseLineSplitter();
  while (true) {
    const { done, value } = await reader.read();
    // 先解析后退出（W568）：done 时 stream=false 让解码器吐出最终字符
    const chunk = decoder.decode(value, { stream: !done });
    // W825：跨块行缓冲——done 时冲刷残留半行
    const lines = done ? [...splitter.push(chunk), ...splitter.flush()] : splitter.push(chunk);

    for (const line of lines) {
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
