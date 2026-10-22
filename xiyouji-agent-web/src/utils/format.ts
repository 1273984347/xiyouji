/**
 * format.ts — 展示层格式化复用（W803-D 新建）
 *
 * 职责边界：纯字符串转换，无副作用、无 React 依赖。
 * 收敛动因：`formatModelName` 在 Header.tsx 与 ChatMessages.tsx 各写一份（逐字相同），
 * 会话标题截断口径在 useChat 出现三处——口径分散即「同一概念多种叫法」的温床。
 */
import type { Model } from '../types';

/**
 * 模型 ID → 展示名：先查模型列表的 name，再剥掉厂商前缀与连字符。
 * 剥前缀后为空则回落原 name（如 name 恰为 "GPT" 时仍显示 "GPT" 而非空串）。
 */
export function formatModelName(modelId: string, models: Model[]): string {
  const model = models.find((m) => m.modelId === modelId);
  const name = model?.name || modelId;
  return (
    name
      .replace(/^(Claude|GPT|Gemini|Kimi|DeepSeek|Qwen|GLM)\s*/i, '')
      .replace(/-/g, ' ')
      .trim() || name
  );
}

/**
 * 会话标题 = 首条消息前 30 字（超出加省略号）。
 * 建会话、首条消息后回填标题、无会话时改标题三处共用同一口径。
 */
export function titleFromMessage(message: string): string {
  return message.slice(0, 30) + (message.length > 30 ? '...' : '');
}
