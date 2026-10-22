/**
 * useChat.streaming.test.ts — 流式链路三项修复的**源码级回归锚**（W825）
 *
 * 为什么用源码级断言而不是 hook 行为测试：
 *   useChat 的三条修复都在「流式会话状态机」内部（catch/finally 分支的消息 id 匹配、
 *   停止按钮的中止链路、fetch 的 signal 接线），要行为化测试需整套 mock
 *   fetch/SSE/sessions 三层夹具，成本远大于锚点价值，且易随夹具漂移。
 *   本仓已有同型先例（tests/unit/test_preflight_check.py 的 W821 干扰日志用例）。
 *   本文件**不测运行时行为**，只钉住「关键接线不得被回退」这一不变量；
 *   运行时行为由 sseStream.test.ts（帧解析）+ 集成测试 + 手工验证覆盖。
 *
 * 钉住的不变量：
 *   ① catch 分支必须**同时**匹配 tempAssistantMessageId 与 realAssistantMessageId
 *      （init 事件把 id 由 temp 改写为 real·只匹配 temp ⇒ init 之后的任何异常都
 *        匹配不到消息 ⇒ 错误文案写不进·isStreaming 永不复位）；
 *   ② finally 分支必须复位消息的 isStreaming（流未收到 done 就结束时兜底）；
 *   ③ fetch 必须带 signal（AbortController 接线）且 handleStop 必须调 abort
 *      （「停止」此前只改 UI 状态·流继续推进·服务端继续跑完本轮）。
 */
import { describe, it, expect } from 'vitest';

// W829：用 Vite 的 import.meta.glob 以**原始文本**读同目录源文件（`?raw`）——
// 不用 node:fs：前端 tsconfig 不含 node types（src 下的测试按仓内惯例不引 node API）。
const SRC = (
  import.meta.glob('./useChat.ts', { query: '?raw', import: 'default', eager: true })['./useChat.ts'] ?? ''
) as string;

describe('W825 · useChat 流式链路不变量', () => {
  it('① catch 分支同时匹配 temp 与 real 两个消息 id', () => {
    const catchBlock = SRC.slice(SRC.indexOf('} catch (error) {'));
    const branch = catchBlock.slice(0, catchBlock.indexOf('} finally {'));
    expect(branch).toMatch(/m\.id === tempAssistantMessageId\s*\|\|\s*m\.id === realAssistantMessageId/);
  });

  it('② finally 分支复位流式态（兜底清「思考中…」）', () => {
    const finallyBlock = SRC.slice(SRC.lastIndexOf('} finally {'));
    expect(finallyBlock).toMatch(/isStreaming:\s*false/);
    expect(finallyBlock).toMatch(/setIsLoading\(false\)/);
  });

  it('③ fetch 带 AbortSignal 且「停止」真正 abort', () => {
    expect(SRC).toMatch(/signal:\s*controller\.signal/);
    expect(SRC).toMatch(/new AbortController\(\)/);
    const stop = SRC.slice(SRC.indexOf('const handleStop'));
    expect(stop.slice(0, stop.indexOf('}, []);'))).toMatch(/abortRef\.current\?\.abort\(\)/);
  });

  it('④ 错误文案追加为文本块（contentBlocks 非空时 ChatMessages 会跳过 content）', () => {
    expect(SRC).toMatch(/contentBlocks:\s*\[\.\.\.\(m\.contentBlocks \?\? \[\]\)/);
  });
});
