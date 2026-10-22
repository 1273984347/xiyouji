// metrics.test.ts — W844 首 token 指标窗口单测（node:test·经 tsx 运行）。
//
// 覆盖：空窗口给出 null 而非 0 · 样本入窗与分位计算 · 滚动淘汰（窗口恒定）·
//       脏数据丢弃 · 重置 · SLO 常量与摘要形状。
// 运行：cd xiyouji-agent-web && node --import tsx --test server/metrics.test.ts
import { test, beforeEach } from "node:test";
import assert from "node:assert";
import {
  FIRST_TOKEN_SLO_MS,
  METRICS_WINDOW,
  firstTokenSummary,
  recordFirstToken,
  resetFirstTokenSamples,
} from "./metrics.js";

beforeEach(() => {
  resetFirstTokenSamples();
});

test("空窗口：count=0 且各分位为 null（不得返回 0）", () => {
  const s = firstTokenSummary();
  assert.equal(s.count, 0);
  assert.equal(s.window, METRICS_WINDOW);
  assert.equal(s.p50, null, "无样本时 p50 必须是 null——0 会被读成「快到 0 毫秒」");
  assert.equal(s.p95, null);
  assert.equal(s.min, null);
  assert.equal(s.max, null);
  assert.equal(s.sloMs, FIRST_TOKEN_SLO_MS);
  assert.equal(FIRST_TOKEN_SLO_MS, 2000, "OBS-14 的 SLO 是首 token < 2 s（架构方案 §11.5）");
});

test("分位数：最近秩法（1..100 → p50=50 · p95=95）", () => {
  for (let i = 1; i <= 100; i += 1) recordFirstToken(i);
  const s = firstTokenSummary();
  assert.equal(s.count, 100);
  assert.equal(s.p50, 50);
  assert.equal(s.p95, 95);
  assert.equal(s.min, 1);
  assert.equal(s.max, 100);
});

test("滚动窗口：超过上限后淘汰最旧，count 恒定在 window", () => {
  for (let i = 1; i <= METRICS_WINDOW + 20; i += 1) recordFirstToken(i);
  const s = firstTokenSummary();
  assert.equal(s.count, METRICS_WINDOW, `样本数应恒定在 ${METRICS_WINDOW}`);
  assert.equal(s.min, 21, "最旧的 20 个应被淘汰");
  assert.equal(s.max, METRICS_WINDOW + 20);
});

test("脏数据丢弃：非有限值与负值不入窗", () => {
  recordFirstToken(Number.NaN);
  recordFirstToken(Number.POSITIVE_INFINITY);
  recordFirstToken(-5);
  recordFirstToken(120);
  assert.equal(firstTokenSummary().count, 1, "只有合法样本入窗");
  assert.equal(firstTokenSummary().p50, 120);
});

test("样本取整：小数毫秒按四舍五入入窗", () => {
  recordFirstToken(99.6);
  assert.equal(firstTokenSummary().p50, 100);
});

test("重置：清空后回到空窗口语义", () => {
  recordFirstToken(500);
  assert.equal(firstTokenSummary().count, 1);
  resetFirstTokenSamples();
  const s = firstTokenSummary();
  assert.equal(s.count, 0);
  assert.equal(s.p95, null);
});

test("摘要是快照：改动内部状态不影响已取出的对象", () => {
  recordFirstToken(300);
  const s = firstTokenSummary();
  recordFirstToken(900);
  assert.equal(s.count, 1, "已取出的摘要不应随后续写入变化");
  assert.equal(firstTokenSummary().count, 2);
});
