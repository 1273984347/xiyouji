/**
 * api.integration.test.ts — 前后端契约集成测试（W808 新建·第二层）
 *
 * 纪律（skill「三件套」之第二层·集成测试）：
 *   **真实起服 + 真实 HTTP + 真实 SQLite**，断言真实响应与真实落库状态——
 *   **不用 mock 冒充**。mock 只能证明「代码符合 mock 的假设」，不能证明「契约真的成立」。
 *
 * 覆盖 W808 引入/改动的对外行为：
 *   ① /api/ready 就绪探针（W808 新增）——依赖可用时 200，不可用时 503；
 *   ② request ID 全链路（W808 新增）——响应头回写 + 上游 ID 沿用；
 *   ③ 边界校验（W808 新增）——非法入参被拒且状态码符合既有契约；
 *   ④ 错误体形状恒为 `{ error: string }`（W808 全局错误处理器收敛后不得变形）；
 *   ⑤ 未命中路由的 /api 返回 JSON 404（此前落到 Express 默认 HTML 404）；
 *   ⑥ 优雅关闭（W808 新增）——SIGTERM 后进程干净退出。
 *
 * 运行：cd xiyouji-agent-web && node --import tsx --test server/api.integration.test.ts
 */
import { test } from "node:test";
import assert from "node:assert";
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Database from "better-sqlite3";
import { gracefulShutdown } from "./shutdown.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const WEB = path.resolve(HERE, "..");
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/** 起服并等待就绪；返回子进程与基址。 */
async function spawnServer(port: number, extraEnv: Record<string, string> = {}) {
  const tsxCli = path.join(WEB, "node_modules", "tsx", "dist", "cli.mjs");
  if (!fs.existsSync(tsxCli)) {
    throw new Error(`tsx CLI 不存在：${tsxCli}（先 npm ci/install）`);
  }
  const child = spawn(process.execPath, [tsxCli, "server/index.ts"], {
    cwd: WEB,
    env: { ...process.env, PORT: String(port), AGENT_WEB_TOKEN: "", ...extraEnv },
    stdio: ["ignore", "pipe", "pipe"],
  });
  let out = "";
  child.stdout?.on("data", (d) => {
    out += String(d);
  });
  child.stderr?.on("data", (d) => {
    out += String(d);
  });

  const base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 80; i++) {
    try {
      const r = await fetch(`${base}/api/health`);
      if (r.ok || r.status === 401) return { child, base, output: () => out };
    } catch {
      /* 未起 */
    }
    await sleep(500);
  }
  child.kill();
  throw new Error(`server 未就绪（port ${port}）·子进程输出尾部：\n${out.slice(-1500) || "(无输出)"}`);
}

// ==================== ① 就绪探针 ====================

test("集成：/api/ready 就绪探针返回 200 且 checks.database=ok", async () => {
  const { child, base } = await spawnServer(3213);
  try {
    const r = await fetch(`${base}/api/ready`);
    assert.equal(r.status, 200, "依赖可用时就绪探针应 200");
    const body = (await r.json()) as { status: string; checks: Record<string, { status: string }> };
    assert.equal(body.status, "ok");
    assert.equal(body.checks.database.status, "ok", "SQLite 应可达");
  } finally {
    child.kill();
  }
});

// ==================== ② request ID 全链路 ====================

test("集成：响应头回写 X-Request-Id（服务端生成）", async () => {
  const { child, base } = await spawnServer(3214);
  try {
    const r = await fetch(`${base}/api/health`);
    const rid = r.headers.get("x-request-id");
    assert.ok(rid, "响应应带 X-Request-Id 头");
    assert.ok(rid.length > 0);
    assert.ok(rid.length <= 64, "request ID 长度受限");
  } finally {
    child.kill();
  }
});

test("集成：上游提供的 X-Request-Id 被沿用（跨服务链路不断链）", async () => {
  const { child, base } = await spawnServer(3215);
  try {
    const sent = "upstream-req-abc123";
    const r = await fetch(`${base}/api/health`, { headers: { "X-Request-Id": sent } });
    assert.equal(r.headers.get("x-request-id"), sent, "上游 ID 应被沿用");
  } finally {
    child.kill();
  }
});

test("集成：上游提供的超长 X-Request-Id 被截断到 64 字符（防日志字段膨胀）", async () => {
  const { child, base } = await spawnServer(3216);
  try {
    const long = "x".repeat(200);
    const r = await fetch(`${base}/api/health`, { headers: { "X-Request-Id": long } });
    const rid = r.headers.get("x-request-id");
    assert.ok(rid);
    assert.equal(rid.length, 64, "超长 ID 应被截断到 64");
  } finally {
    child.kill();
  }
});

// ==================== ③ 边界校验 ====================

test("集成：POST /api/feedback 非法入参返回 400 invalid body（既有契约逐字保留）", async () => {
  const { child, base } = await spawnServer(3217);
  try {
    const r = await fetch(`${base}/api/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sessionId: "s", messageId: "m", verdict: "meh" }), // verdict 非法
    });
    assert.equal(r.status, 400, "既有契约钉的是 400");
    const body = (await r.json()) as { error: string };
    assert.equal(body.error, "invalid body", "文案逐字保留");
  } finally {
    child.kill();
  }
});

test("集成：POST /api/feedback 缺 sessionId 返回 400（W808 修的真实缺陷：前端曾漏传）", async () => {
  const { child, base } = await spawnServer(3218);
  try {
    // 前端 W808 修复前的载荷形状（缺 sessionId）——必须被拒
    const r = await fetch(`${base}/api/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messageId: "m-w808", verdict: "up" }),
    });
    assert.equal(r.status, 400, "缺 sessionId 应被拒");
    const body = (await r.json()) as { error: string };
    assert.equal(body.error, "invalid body");
  } finally {
    child.kill();
  }
});

test("集成：POST /api/feedback 三字段齐备时 200 且真实落库（集成断言落库状态）", async () => {
  const { child, base } = await spawnServer(3219);
  const mark = `w808-int-${Date.now()}`;
  try {
    const r = await fetch(`${base}/api/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sessionId: "w808-sess", messageId: mark, verdict: "up" }),
    });
    assert.equal(r.status, 200);
    const body = (await r.json()) as { ok: boolean; inserted: number };
    assert.equal(body.ok, true);
    assert.equal(body.inserted, 1, "首次应插入 1 行");

    // 真实查 SQLite（不是查 mock）
    const db = new Database(path.join(WEB, "data", "chat.db"), { readonly: true });
    const row = db.prepare("SELECT session_id, verdict FROM feedback WHERE message_id = ?").get(mark) as
      | { session_id: string; verdict: string }
      | undefined;
    db.close();
    assert.ok(row, "反馈行应真实落库");
    assert.equal(row.session_id, "w808-sess");
    assert.equal(row.verdict, "up");
  } finally {
    child.kill();
    // 清理测试行
    try {
      const db = new Database(path.join(WEB, "data", "chat.db"));
      db.prepare("DELETE FROM feedback WHERE message_id = ?").run(mark);
      db.close();
    } catch {
      /* 清理失败不影响断言结论 */
    }
  }
});

test("集成：GET /api/sessions/:id 不存在时返回 404 且文案为「会话不存在」", async () => {
  const { child, base } = await spawnServer(3220);
  try {
    const r = await fetch(`${base}/api/sessions/w808-does-not-exist`);
    assert.equal(r.status, 404);
    const body = (await r.json()) as { error: string };
    assert.match(body.error, /会话不存在/);
  } finally {
    child.kill();
  }
});

test("集成：未命中路由的 /api 返回 JSON 404（此前落到 Express 默认 HTML）", async () => {
  const { child, base } = await spawnServer(3221);
  try {
    const r = await fetch(`${base}/api/w808-no-such-endpoint`);
    assert.equal(r.status, 404);
    const body = (await r.json()) as { error: string };
    assert.match(body.error, /接口不存在/);
  } finally {
    child.kill();
  }
});

// ==================== ④ 错误体形状恒定 ====================

test("集成：错误响应体恒为 { error: string }（无堆栈泄漏·字段不多不少）", async () => {
  const { child, base } = await spawnServer(3222);
  try {
    const r = await fetch(`${base}/api/sessions/w808-missing-404`);
    const raw = await r.text();
    const body = JSON.parse(raw) as Record<string, unknown>;
    assert.deepEqual(Object.keys(body), ["error"], "错误体应只有 error 一个键");
    assert.equal(typeof body.error, "string");
    assert.ok(!raw.includes("at Object."), "响应体不得含堆栈栈帧");
    assert.ok(!raw.includes("node_modules"), "响应体不得含内部路径");
  } finally {
    child.kill();
  }
});

// ==================== ④b 聊天路由的入参校验 ====================

test("集成：POST /api/chat 消息为空返 400 +「消息不能为空」（既有契约逐字保留）", async () => {
  const { child, base } = await spawnServer(3225);
  try {
    const r = await fetch(`${base}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "" }),
    });
    assert.equal(r.status, 400, "空消息应 400");
    const body = (await r.json()) as { error: string };
    assert.equal(body.error, "消息不能为空", "文案逐字保留");
  } finally {
    child.kill();
  }
});

test("集成：POST /api/chat 缺 message 字段同样返 400 +「消息不能为空」", async () => {
  const { child, base } = await spawnServer(3226);
  try {
    const r = await fetch(`${base}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model: "glm-4.6" }),
    });
    assert.equal(r.status, 400);
    const body = (await r.json()) as { error: string };
    assert.equal(body.error, "消息不能为空");
  } finally {
    child.kill();
  }
});

test("集成：POST /api/chat 其余字段类型非法返 400 且文案与「消息为空」区分", async () => {
  const { child, base } = await spawnServer(3227);
  try {
    // message 合法但 model 类型非法（对象）——不应被误报为「消息不能为空」
    const r = await fetch(`${base}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "你好", model: { bad: true } }),
    });
    assert.equal(r.status, 400);
    const body = (await r.json()) as { error: string };
    assert.notEqual(body.error, "消息不能为空", "非空消息的字段错误不应复用该文案");
    assert.equal(body.error, "请求参数不合法");
  } finally {
    child.kill();
  }
});

test("集成：POST /api/chat 超长消息被拒（边界校验生效）", async () => {
  const { child, base } = await spawnServer(3228);
  try {
    const r = await fetch(`${base}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "x".repeat(60_000) }),
    });
    assert.equal(r.status, 400, "超长消息应被边界校验拒绝");
  } finally {
    child.kill();
  }
});

// ==================== ⑤ 会话 CRUD 全链路 ====================
test("集成：会话 CRUD 全链路（建 → 列 → 改 → 删）状态真实流转", async () => {
  const { child, base } = await spawnServer(3223);
  let sessionId = "";
  try {
    // 建
    const created = await fetch(`${base}/api/sessions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "W808 集成会话", model: "glm-4.6" }),
    });
    assert.equal(created.status, 200);
    const createdBody = (await created.json()) as { session: { id: string; title: string } };
    sessionId = createdBody.session.id;
    assert.equal(createdBody.session.title, "W808 集成会话");

    // 真实查库确认落库
    const db = new Database(path.join(WEB, "data", "chat.db"), { readonly: true });
    const persisted = db.prepare("SELECT title FROM sessions WHERE id = ?").get(sessionId) as
      | { title: string }
      | undefined;
    db.close();
    assert.ok(persisted, "会话应真实落库");
    assert.equal(persisted.title, "W808 集成会话");

    // 列（应含新会话）
    const list = await fetch(`${base}/api/sessions`);
    const listBody = (await list.json()) as { sessions: Array<{ id: string; messageCount: number }> };
    const found = listBody.sessions.find((s) => s.id === sessionId);
    assert.ok(found, "列表应含新建会话");
    assert.equal(typeof found.messageCount, "number");

    // 改
    const patched = await fetch(`${base}/api/sessions/${sessionId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "W808 已改名" }),
    });
    assert.equal(patched.status, 200);
    const patchedBody = (await patched.json()) as { success: boolean };
    assert.equal(patchedBody.success, true);

    // 删
    const deleted = await fetch(`${base}/api/sessions/${sessionId}`, { method: "DELETE" });
    assert.equal(deleted.status, 200);
    const deletedBody = (await deleted.json()) as { success: boolean };
    assert.equal(deletedBody.success, true);

    // 删后再取应 404
    const after = await fetch(`${base}/api/sessions/${sessionId}`);
    assert.equal(after.status, 404, "删除后再取应 404");
  } finally {
    child.kill();
    // 清理（防测试数据残留）
    try {
      const db = new Database(path.join(WEB, "data", "chat.db"));
      db.prepare("DELETE FROM sessions WHERE id = ?").run(sessionId);
      db.close();
    } catch {
      /* 忽略 */
    }
  }
});

// ==================== ⑥ 优雅关闭 ====================

test("集成：优雅关闭流程（跨平台·直接调用关闭单元）——停服 → 关库 → 退出码 0", async () => {
  // 平台无关的验证面：直接调用 server/shutdown.ts 的关闭流程（依赖注入），
  // 断言「server.close 被调用 → 数据库被关闭 → 退出码 0」的**顺序与结果**。
  // 真实信号位（SIGTERM）见下一条——该条为 POSIX 专属，真实执行位=CI（Linux）。
  const calls: string[] = [];
  let exitCode: number | null = null;

  const code = await gracefulShutdown("SIGTERM", {
    server: {
      close(cb: (err?: Error) => void) {
        calls.push("server.close");
        cb();
      },
    } as unknown as Pick<import("node:http").Server, "close">,
    closeDatabase: () => {
      calls.push("closeDatabase");
    },
    log: () => {},
    exit: (c) => {
      exitCode = c;
    },
  });

  assert.equal(code, 0, "正常关闭应返回退出码 0");
  assert.equal(exitCode, 0, "应调用 exit(0)");
  assert.deepEqual(calls, ["server.close", "closeDatabase"], "顺序：先停服再关库");
});

test("集成：优雅关闭在 server.close 抛错时返回退出码 1（不吞错）", async () => {
  let exitCode: number | null = null;
  const code = await gracefulShutdown("SIGTERM", {
    server: {
      close(cb: (err?: Error) => void) {
        cb(new Error("关闭失败"));
      },
    } as unknown as Pick<import("node:http").Server, "close">,
    closeDatabase: () => {},
    log: () => {},
    exit: (c) => {
      exitCode = c;
    },
  });

  assert.equal(code, 1, "关闭出错应返回 1");
  assert.equal(exitCode, 1);
});

// POSIX 专属：Windows 的 child.kill('SIGTERM') 是无条件终止（无信号语义），
// 故本条在 Windows 上不可判定——按仓内「双平台断言禁例」纪律标注真实执行位=CI（Linux）。
test("集成：SIGTERM 触发优雅关闭（进程干净退出·退出码 0）", { skip: process.platform === "win32" ? "Windows 无 SIGTERM 语义（child.kill 为无条件终止）·真实执行位=CI（Linux）" : false }, async () => {
  const { child, base } = await spawnServer(3224);
  // 确认服务活着
  const alive = await fetch(`${base}/api/health`);
  assert.equal(alive.status, 200);

  const exitCode = await new Promise<number | null>((resolve) => {
    child.on("exit", (code) => resolve(code));
    child.kill("SIGTERM");
    setTimeout(() => {
      child.kill("SIGKILL");
    }, 15_000);
  });

  assert.equal(exitCode, 0, "SIGTERM 应触发优雅关闭并以 0 退出");
});
