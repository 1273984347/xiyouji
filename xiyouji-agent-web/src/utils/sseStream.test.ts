/**
 * sseStream.test.ts — SSE 帧解析单测（W825）
 *
 * 覆盖的核心缺陷：一次网络读**不保证落在帧边界**——服务端帧格式为
 * `data: <JSON>\n\n`（server/sse.ts:58），而 tool_result 帧可达 256KB~1MB
 * （server/engine/tools.ts 的 READ_MAX_BYTES / RUN_MAX_BUFFER）→ 必然被切成多片。
 * 旧实现逐片独立 `split('\n')`：半截 JSON 解析失败被 `catch {}` 静默丢弃，
 * 残段不以 `data: ` 开头被跳过 ⇒ **整帧事件凭空消失**（工具条目停在「执行中…」、
 * 文本增量丢字、无报错无日志）。
 *
 * 判据：帧被切成任意片数后，事件必须被完整还原；控制组（整帧一次到达）行为不变。
 */
import { describe, it, expect } from 'vitest';
import { createSseLineSplitter, readChatStream } from './sseStream';

/** 构造一个按给定片段依次吐出的 reader（模拟真实网络分片）。 */
function makeReader(chunks: string[]): ReadableStreamDefaultReader<Uint8Array> {
  const enc = new TextEncoder();
  let i = 0;
  return {
    read: async () =>
      i < chunks.length
        ? { done: false as const, value: enc.encode(chunks[i++]) }
        : { done: true as const, value: undefined },
  } as unknown as ReadableStreamDefaultReader<Uint8Array>;
}

async function collect(chunks: string[]) {
  const out: Array<{ type: string; [k: string]: unknown }> = [];
  for await (const ev of readChatStream(makeReader(chunks))) {
    out.push(ev as { type: string; [k: string]: unknown });
  }
  return out;
}

describe('W825 · createSseLineSplitter（跨块行缓冲）', () => {
  it('半行留在缓冲内·不提前吐出', () => {
    const s = createSseLineSplitter();
    expect(s.push('data: {"type":"te')).toEqual([]); // 半行：不得吐出
    expect(s.push('xt"}')).toEqual([]); // 仍未到换行
    const lines = s.push('\n\n'); // 补齐换行
    expect(lines[0]).toBe('data: {"type":"text"}');
    expect(lines[1]).toBe(''); // 帧尾空行
  });

  it('flush 冲刷流末尾无换行的残留半行', () => {
    const s = createSseLineSplitter();
    expect(s.push('data: {"a":1}')).toEqual([]); // 无换行
    expect(s.flush()).toEqual(['data: {"a":1}']);
    expect(s.flush()).toEqual([]); // 幂等：已冲刷
  });
});

describe('W825 · readChatStream（帧跨片不丢）', () => {
  it('大帧被切成两片时事件仍被完整还原', async () => {
    const payload = JSON.stringify({
      type: 'tool_result',
      toolId: 't1',
      content: 'x'.repeat(200_000), // 模拟 tool_result 的真实体量
    });
    const frame = `data: ${payload}\n\n`;
    const cut = Math.floor(frame.length / 2);
    const events = await collect([frame.slice(0, cut), frame.slice(cut)]);
    expect(events).toHaveLength(1);
    expect(events[0].type).toBe('tool_result');
    expect((events[0] as unknown as { content: string }).content).toHaveLength(200_000);
  });

  it('帧被切成多片（逐字符）时事件仍被还原', async () => {
    const payload = JSON.stringify({ type: 'text', content: '你好，世界' });
    const frame = `data: ${payload}\n\n`;
    const events = await collect(frame.split(''));
    expect(events).toHaveLength(1);
    expect(events[0].type).toBe('text');
  });

  it('多字节字符跨片时解码不出现替换符（解码器跨块复用）', async () => {
    const payload = JSON.stringify({ type: 'text', content: '西游记' });
    const frame = `data: ${payload}\n\n`;
    const enc = new TextEncoder();
    const bytes = enc.encode(frame);
    // 在「西」的多字节序列中间切开（3 字节 UTF-8 → 前 1 字节 / 后 2 字节）
    const cut = bytes.indexOf(enc.encode('西')[0]) + 1;
    const chunks = [bytes.slice(0, cut), bytes.slice(cut)];
    let i = 0;
    const reader = {
      read: async () =>
        i < chunks.length
          ? { done: false as const, value: chunks[i++] }
          : { done: true as const, value: undefined },
    } as unknown as ReadableStreamDefaultReader<Uint8Array>;
    const out: unknown[] = [];
    for await (const ev of readChatStream(reader)) out.push(ev);
    expect(out).toHaveLength(1);
    expect(JSON.stringify(out[0])).not.toContain('�');
  });

  it('控制组：整帧一次到达时行为不变（回归锚）', async () => {
    const frame = `data: ${JSON.stringify({ type: 'text', content: 'ok' })}\n\n`;
    const events = await collect([frame]);
    expect(events).toHaveLength(1);
    expect(events[0].type).toBe('text');
  });

  it('控制组：心跳/注释行与非法 JSON 帧被静默跳过（既有语义不变）', async () => {
    const events = await collect([
      ': keep-alive\n\n',
      'data: {not-json\n\n',
      `data: ${JSON.stringify({ type: 'done', duration: 12 })}\n\n`,
    ]);
    expect(events).toHaveLength(1);
    expect(events[0].type).toBe('done');
  });
});
