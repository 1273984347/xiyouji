/**
 * retrieval.test.ts — 检索层接入单测（W1205 · O-4）
 *
 * 运行：cd xiyouji-agent-web && node --import tsx --test server/retrieval.test.ts
 *
 * 覆盖三类（任务书要求）：
 *   ① 可溯源命中        → 引用下发、守卫计数一致；
 *   ② 不可溯源被拦      → 路径不存在 / 摘录与文件不符的命中一律不下发；
 *   ③ 索引不可达时的降级 → 异源降级（cross_source）判定点与明示文案。
 * 另附：同源降级（生成层不可用）、无任何可溯源引用时的异源降级、路由层状态码契约。
 *
 * 纪律：后端与生成层均以**注入的假实现**驱动（不 spawn Python、不调 LLM）——
 *      本文件验证的是判定逻辑与契约；真实链路由集成层另行验证。
 */
import { test } from "node:test";
import assert from "node:assert";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import express from "express";
import {
  AnswerUnavailableError,
  CROSS_SOURCE_NOTICE,
  RetrievalUnavailableError,
  SAME_SOURCE_NOTICE,
  runRetrieval,
  verifyCitation,
  type AnswerLayer,
  type RetrievalBackend,
  type RetrievalHit,
} from "./retrieval.js";
import { registerRetrievalRoutes } from "./retrieval.routes.js";
import { errorHandler } from "./errors.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..", "..");

/** 仓内真源文档（引用守卫的合法落点）。 */
const DOC = "docs/00-导读/术语表.md";

/** 取真源文件里的一段逐字正文（用于构造可溯源命中）。 */
function realExcerpt(length = 40): string {
  const text = fs.readFileSync(path.join(ROOT, DOC), "utf-8");
  return text.replace(/^\u3010[^\u3011]*\u3011\s*/, "").trim().slice(0, length);
}

/** 假后端：返回给定命中列表。 */
function backendOf(hits: RetrievalHit[]): RetrievalBackend {
  return {
    async retrieve(): Promise<RetrievalHit[]> {
      return hits;
    },
  };
}

/** 假后端：抛检索不可达。 */
function brokenBackend(reason = "index_unreachable"): RetrievalBackend {
  return {
    async retrieve(): Promise<RetrievalHit[]> {
      throw new RetrievalUnavailableError(reason, "索引不可达");
    },
  };
}

const GOOD_HIT: RetrievalHit = { path: DOC, score: 12.5, excerpt: realExcerpt() };

// ==================== ① 可溯源命中 ====================

test("可溯源命中：引用下发且守卫计数一致", async () => {
  const out = await runRetrieval(
    "术语",
    { topK: 5, withAnswer: false },
    { backend: backendOf([GOOD_HIT]), cwd: ROOT }
  );
  assert.equal(out.ok, true);
  assert.equal(out.mode, "retrieval_only");
  assert.equal(out.degraded, false);
  assert.equal(out.complianceDegraded, false);
  assert.equal(out.guard.checked, 1);
  assert.equal(out.guard.verified, 1);
  assert.equal(out.guard.dropped, 0);
  assert.equal(out.citations.length, 1);
  assert.equal(out.citations[0].path, DOC);
  assert.ok(out.citations[0].anchor.length > 0, "引用须带段落锚点");
  assert.ok(
    out.citations[0].excerpt.includes(realExcerpt().slice(0, 10)),
    "引用正文须来自真源段落"
  );
});

test("可溯源命中 + 生成层可用 ⇒ full 模式且带回答", async () => {
  const answerLayer: AnswerLayer = {
    async generate(): Promise<string> {
      return "回答正文〔术语表.md〕";
    },
  };
  const out = await runRetrieval(
    "术语",
    { topK: 5, withAnswer: true },
    { backend: backendOf([GOOD_HIT]), answerLayer, cwd: ROOT }
  );
  assert.equal(out.mode, "full");
  assert.equal(out.degraded, false);
  assert.equal(out.complianceDegraded, false);
  assert.equal(out.answer, "回答正文〔术语表.md〕");
  assert.equal(out.citations.length, 1);
});

// ==================== ② 不可溯源被拦 ====================

test("不可溯源命中：路径不存在 → 拦截不下发", async () => {
  const bad: RetrievalHit = { path: "docs/00-导读/不存在的文件-xyz.md", score: 9, excerpt: "任意正文" };
  const out = await runRetrieval(
    "术语",
    { topK: 5, withAnswer: false },
    { backend: backendOf([bad, GOOD_HIT]), cwd: ROOT }
  );
  assert.equal(out.guard.checked, 2);
  assert.equal(out.guard.verified, 1);
  assert.equal(out.guard.dropped, 1);
  assert.equal(out.citations.length, 1);
  assert.ok(
    !out.citations.some((c) => c.path.includes("不存在的文件-xyz")),
    "不可溯源路径不得出现在下发引用里"
  );
});

test("不可溯源命中：摘录与文件不符 → 拦截不下发", async () => {
  const forged: RetrievalHit = {
    path: DOC,
    score: 8,
    excerpt: "这一段文字并不存在于该真源文件之中，用于验证段落级溯源判据。",
  };
  const out = await runRetrieval(
    "术语",
    { topK: 5, withAnswer: false },
    { backend: backendOf([forged]), cwd: ROOT }
  );
  assert.equal(out.guard.checked, 1);
  assert.equal(out.guard.verified, 0);
  assert.equal(out.guard.dropped, 1);
  assert.equal(out.citations.length, 0);
  assert.equal(out.hits.length, 0);
});

test("引用守卫：越界路径与产物目录路径一并拒绝", () => {
  const traversal = verifyCitation({ path: "../../etc/passwd", score: 1, excerpt: "x" }, ROOT);
  assert.equal(traversal.verified, false);
  const product = verifyCitation({ path: "site/index.html", score: 1, excerpt: "x" }, ROOT);
  assert.equal(product.verified, false);
  assert.equal(product.reason, "not_source_dir");
});

// ==================== ③ 索引不可达时的降级 ====================

test("索引不可达：异源降级（cross_source）且带 UI 明示", async () => {
  const out = await runRetrieval(
    "五行山",
    { topK: 5, withAnswer: false },
    { backend: brokenBackend(), cwd: ROOT }
  );
  assert.equal(out.ok, false);
  assert.equal(out.mode, "cross_source_degraded");
  assert.equal(out.degraded, true);
  assert.equal(out.complianceDegraded, true, "异源降级须计入合规降级");
  assert.equal(out.degradation?.kind, "cross_source");
  assert.equal(out.degradation?.reason, "index_unreachable");
  assert.equal(out.notice, CROSS_SOURCE_NOTICE);
  assert.match(out.notice ?? "", /不是检索结果/);
  assert.equal(out.citations.length, 0);
  assert.equal(out.answer, null);
});

test("生成层不可用：同源降级（引用仍可溯源·不计合规降级）", async () => {
  const failing: AnswerLayer = {
    async generate(): Promise<string> {
      throw new AnswerUnavailableError("llm_unreachable", "上游 503");
    },
  };
  const out = await runRetrieval(
    "术语",
    { topK: 5, withAnswer: true },
    { backend: backendOf([GOOD_HIT]), answerLayer: failing, cwd: ROOT }
  );
  assert.equal(out.mode, "same_source_degraded");
  assert.equal(out.degraded, true);
  assert.equal(out.complianceDegraded, false, "同源降级不计入合规降级");
  assert.equal(out.degradation?.kind, "same_source");
  assert.equal(out.degradation?.reason, "llm_unreachable");
  assert.equal(out.notice, SAME_SOURCE_NOTICE);
  assert.equal(out.citations.length, 1, "同源降级时引用照常下发");
  assert.equal(out.answer, null);
});

test("无可溯源引用 + 请求生成：异源降级且不产出无据文本", async () => {
  const answerLayer: AnswerLayer = {
    async generate(): Promise<string> {
      return "不该被调用的回答";
    },
  };
  const forged: RetrievalHit = { path: DOC, score: 1, excerpt: "并不存在于该文件的伪造段落。" };
  const out = await runRetrieval(
    "术语",
    { topK: 5, withAnswer: true },
    { backend: backendOf([forged]), answerLayer, cwd: ROOT }
  );
  assert.equal(out.mode, "cross_source_degraded");
  assert.equal(out.complianceDegraded, true);
  assert.equal(out.degradation?.reason, "no_traceable_citation");
  assert.equal(out.answer, null, "无可溯源引用时不得产出任何文本");
});

// ==================== 路由层契约 ====================

test("路由：缺检索词 400 · 正常检索 200 · 异源降级 503", async () => {
  const app = express();
  registerRetrievalRoutes(app, { backend: backendOf([GOOD_HIT]), cwd: ROOT });
  // 与 server/index.ts 的装配顺序一致：路由之后挂全局错误处理器（类型化错误 → { error } 形状）。
  app.use(errorHandler);
  const server = app.listen(0);
  await new Promise((resolve) => server.once("listening", resolve));
  const port = (server.address() as { port: number }).port;
  const base = "http://127.0.0.1:" + port;

  try {
    const missing = await fetch(base + "/api/retrieval");
    assert.equal(missing.status, 400);
    const missingBody = (await missing.json()) as { error?: string };
    assert.ok(missingBody.error, "400 响应体须带 error 字段");

    const ok = await fetch(base + "/api/retrieval?q=" + encodeURIComponent("术语"));
    assert.equal(ok.status, 200);
    const okBody = (await ok.json()) as { mode: string; citations: unknown[] };
    assert.equal(okBody.mode, "retrieval_only");
    assert.equal(okBody.citations.length, 1);

    const degradedApp = express();
    registerRetrievalRoutes(degradedApp, { backend: brokenBackend(), cwd: ROOT });
    degradedApp.use(errorHandler);
    const degradedServer = degradedApp.listen(0);
    await new Promise((resolve) => degradedServer.once("listening", resolve));
    const degradedPort = (degradedServer.address() as { port: number }).port;
    try {
      const degraded = await fetch("http://127.0.0.1:" + degradedPort + "/api/retrieval?q=" + encodeURIComponent("五行山"));
      assert.equal(degraded.status, 503);
      const degradedBody = (await degraded.json()) as { error?: string; mode?: string; complianceDegraded?: boolean };
      assert.ok(degradedBody.error, "503 响应体须带 error 字段");
      assert.equal(degradedBody.mode, "cross_source_degraded");
      assert.equal(degradedBody.complianceDegraded, true);
    } finally {
      await new Promise((resolve) => degradedServer.close(resolve));
    }
  } finally {
    await new Promise((resolve) => server.close(resolve));
  }
});
