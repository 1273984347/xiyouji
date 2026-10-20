/**
 * metrics.ts — 进程内轻量指标（W844 · OBS-14「问答首 token 延迟」）。
 *
 * 为什么自己写而不是引监控：架构方案定的硬约束是「极低成本 + 无云厂商绑定」，
 * 引入 Prometheus/OTel 属常驻服务 + 外部依赖，与该约束冲突。故只做两件事：
 *   ① 结构化日志（sample 落 logger，CI / 日志侧可聚合出长期分布）；
 *   ② 进程内滚动窗口（最近 100 个样本），供 `GET /api/metrics` 直读 p50/p95。
 *
 * 口径边界（写死以免误读）：
 *   - 只统计**出现过文本增量**的请求。纯工具调用没有首 token，记 null 并在
 *     /api/chat 里打一条 reason=no_text_delta 的日志；**不得**把缺样本当作 0 ms。
 *   - 窗口满后淘汰最旧——内存恒定，重启即清零（这是设计，不是缺陷：
 *     长期分布看日志，短窗看现网手感）。
 */

/** 滚动窗口上限（样本数）。 */
export const METRICS_WINDOW = 100;

const samples: number[] = [];

/** 记录一个首 token 延迟样本（毫秒）。非有限值 / 负值直接丢弃，防脏数据污染分位。 */
export function recordFirstToken(ms: number): void {
  if (!Number.isFinite(ms) || ms < 0) return;
  samples.push(Math.round(ms));
  if (samples.length > METRICS_WINDOW) samples.splice(0, samples.length - METRICS_WINDOW);
}

/** 清空窗口（测试用）。 */
export function resetFirstTokenSamples(): void {
  samples.length = 0;
}

/**
 * 分位数（最近秩法·linear-free）。
 *
 * 样本数少时 p95 会等于最大值，这是小样本的正常表现——报告里必须同时给 count，
 * 否则「p95 = 4210 ms」会被读成「一直很慢」而不是「100 次里有 5 次慢」。
 */
function quantile(sorted: number[], q: number): number | null {
  if (sorted.length === 0) return null;
  const idx = Math.min(sorted.length - 1, Math.max(0, Math.ceil(q * sorted.length) - 1));
  return sorted[idx];
}

export interface FirstTokenSummary {
  /** 窗口内样本数（0 表示尚无数据，此时各分位为 null 而非 0） */
  count: number;
  /** 窗口上限 */
  window: number;
  p50: number | null;
  p95: number | null;
  min: number | null;
  max: number | null;
  /** SLO 阈值（毫秒）——先告警级，连续 10 批稳定后再议升硬门槛 */
  sloMs: number;
}

/** OBS-14 的 SLO：问答首 token < 2 s（架构方案 §11.5）。 */
export const FIRST_TOKEN_SLO_MS = 2000;

/** 当前窗口的摘要（只读快照，不改内部状态）。 */
export function firstTokenSummary(): FirstTokenSummary {
  const sorted = [...samples].sort((a, b) => a - b);
  return {
    count: sorted.length,
    window: METRICS_WINDOW,
    p50: quantile(sorted, 0.5),
    p95: quantile(sorted, 0.95),
    min: sorted.length ? sorted[0] : null,
    max: sorted.length ? sorted[sorted.length - 1] : null,
    sloMs: FIRST_TOKEN_SLO_MS,
  };
}
