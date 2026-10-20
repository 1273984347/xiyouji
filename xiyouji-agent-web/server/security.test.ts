// security.test.ts — W791 BL-29 攻击面负向测试（node:test·经 tsx 运行）
// 运行：cd xiyouji-agent-web && node --import tsx --test server/security.test.ts
// 覆盖三轮外部评审点名的三类攻击面（按 agent-web 真实防护模型映射）：
//   ① 「CORS 预检绕过」→ 认证/权限边界：token 鉴权（401 负样本）+ 权限模式白名单 + cwd 钳制
//      （agent-web 无 CORS 中间件·防护模型=loopback 绑定 + 可选 AGENT_WEB_TOKEN + 限流）
//   ② 「超大 RAG top_k」→ agent-web 无 RAG top_k 参数（检索为 grep 工具·钳制在 Python 侧
//      scripts/rag/rag_server.py·W412）；本面以请求体不可信输入净化（权限模式/cwd）对应覆盖
//   ③ 「SSE 超时未清理」→ 超时/断开/幂等/clearTimer 四路径 + 限流（W681·429 负样本）
// 集成例沿用 feedback.test.mjs 的真实起服范式（spawn tsx CLI·用完即杀·不写业务数据）。
import { test } from "node:test";
import assert from "node:assert";
import { spawn } from "node:child_process";
import fs from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  sanitizePermissionMode,
  resolveWorkingDir,
  createSseGuard,
  SSE_MAX_MS_DEFAULT,
  normalizeHostname,
  isAllowedHost,
} from "./security.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const WEB = path.resolve(HERE, ".."); // xiyouji-agent-web 根
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

// ==================== ① 权限模式白名单（P0-1·防未授权 RCE） ====================

test("白名单内权限模式原样放行", () => {
  for (const m of ["default", "acceptEdits", "plan"] as const) {
    assert.equal(sanitizePermissionMode(m, false), m);
  }
});

test("bypassPermissions 未开 allowBypass 时回落 default（防未授权 RCE）", () => {
  assert.equal(sanitizePermissionMode("bypassPermissions", false), "default");
});

test("bypassPermissions 在 allowBypass 开启时放行（本地单人模式）", () => {
  assert.equal(sanitizePermissionMode("bypassPermissions", true), "bypassPermissions");
});

test("非法权限模式一律回落 default", () => {
  for (const bad of ["BypassPermissions", "root", "", "  ", "default ", 42, null, undefined, {}, ["plan"]]) {
    assert.equal(sanitizePermissionMode(bad, true), "default", `输入 ${JSON.stringify(bad)} 应回落`);
  }
});

// ==================== ② 工作目录钳制（P0-1/W536·realpath + 前缀校验） ====================

test("PROJECT_CWD 内的合法子目录放行", () => {
  const got = resolveWorkingDir(HERE, WEB);
  assert.equal(got, fs.realpathSync(HERE));
});

test("PROJECT_CWD 本身放行", () => {
  assert.equal(resolveWorkingDir(WEB, WEB), fs.realpathSync(WEB));
});

test("目录外路径（含系统临时目录）回落 PROJECT_CWD", () => {
  assert.equal(resolveWorkingDir(os.tmpdir(), WEB), fs.realpathSync(WEB));
});

test(".. 穿越路径回落 PROJECT_CWD", () => {
  assert.equal(resolveWorkingDir(path.join(WEB, "..", ".."), WEB), fs.realpathSync(WEB));
});

test("不存在的目录（realpath 失败）回落 PROJECT_CWD", () => {
  assert.equal(resolveWorkingDir(path.join(WEB, "no-such-dir-w791"), WEB), fs.realpathSync(WEB));
});

test("非字符串 / 空串 cwd 回落 PROJECT_CWD", () => {
  for (const bad of [undefined, null, 42, {}, "", "   "]) {
    assert.equal(resolveWorkingDir(bad, WEB), fs.realpathSync(WEB), `输入 ${JSON.stringify(bad)} 应回落`);
  }
});

// ==================== ③ SSE 守卫（P2-3/W680·超时与断开清理） ====================

interface FakeRes {
  writes: string[];
  ended: number;
  fireClose: () => void;
  res: {
    write: (chunk: string) => boolean;
    end: () => void;
    on: (event: string, cb: () => void) => void;
    off: (event: string, cb: () => void) => void;
  };
}

function fakeRes(): FakeRes {
  const writes: string[] = [];
  const closeCbs: Array<() => void> = [];
  const state = { ended: 0 };
  return {
    writes,
    get ended() {
      return state.ended;
    },
    fireClose: () => closeCbs.forEach((cb) => cb()),
    res: {
      write: (chunk: string) => {
        writes.push(chunk);
        return true;
      },
      end: () => {
        state.ended += 1;
      },
      on: (event: string, cb: () => void) => {
        if (event === "close") closeCbs.push(cb);
      },
      off: (event: string, cb: () => void) => {
        const i = closeCbs.indexOf(cb);
        if (i >= 0) closeCbs.splice(i, 1);
      },
    },
  };
}

function deferred<T = unknown>() {
  let resolve!: (v: T) => void;
  let reject!: (e: Error) => void;
  const p = new Promise<T>((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { p, resolve, reject };
}

test("SSE 默认时限为 10 分钟", () => {
  assert.equal(SSE_MAX_MS_DEFAULT, 10 * 60 * 1000);
});

test("超时路径：中止引擎 + 清算本会话 pending + 写 error 事件（他会话 pending 不动）", async () => {
  const f = fakeRes();
  const mine = deferred<void>();
  const other = deferred<void>();
  const guard = createSseGuard({
    res: f.res,
    sessionId: "s1",
    pendingPermissions: {
      p1: { sessionId: "s1", reject: mine.reject },
      p2: { sessionId: "s2", reject: other.reject },
    },
    maxMs: 40,
  });
  await assert.rejects(mine.p, /SSE 超时/);
  assert.equal(guard.signal.aborted, true, "超时应中止引擎");
  assert.equal(f.ended, 1, "超时应 end 响应");
  assert.ok(
    f.writes.some((w) => w.includes('"type":"error"') && w.includes("请求超时")),
    "应写 error 事件"
  );
  // 他会话 pending 未被清算（Promise 仍挂起·竞态断言：setTimeout 宏任务后排空）
  const raced = await Promise.race([other.p.then(() => "rejected"), sleep(60).then(() => "pending")]);
  assert.equal(raced, "pending", "他会话 pending 不应被清算");
});

test("断开路径：clearTimeout + 清算 pending + 中止引擎 + end（不写 error 事件）", async () => {
  const f = fakeRes();
  const mine = deferred<void>();
  const guard = createSseGuard({
    res: f.res,
    sessionId: "s1",
    pendingPermissions: { p1: { sessionId: "s1", reject: mine.reject } },
    maxMs: 40,
  });
  guard.abortStream();
  await assert.rejects(mine.p, /客户端断开连接/);
  assert.equal(guard.signal.aborted, true);
  assert.equal(f.ended, 1);
  assert.equal(f.writes.length, 0, "断开路径不应写 error 事件");
  await sleep(90); // 越过 maxMs·定时器应已清除不再触发
  assert.equal(f.ended, 1, "定时器未清除（泄漏）");
  assert.equal(f.writes.length, 0);
});

test("abortStream 幂等：重复调用不重复 end", async () => {
  const f = fakeRes();
  const guard = createSseGuard({ res: f.res, sessionId: "s1", pendingPermissions: {}, maxMs: 40 });
  guard.abortStream();
  guard.abortStream();
  guard.abortStream();
  assert.equal(f.ended, 1);
  assert.equal(guard.signal.aborted, true);
});

test("clearTimer 后超时不再触发（正常完成路径语义）", async () => {
  const f = fakeRes();
  const guard = createSseGuard({ res: f.res, sessionId: "s1", pendingPermissions: {}, maxMs: 40 });
  guard.clearTimer();
  await sleep(90);
  assert.equal(guard.signal.aborted, false, "clearTimer 不应中止引擎");
  assert.equal(f.ended, 0);
  assert.equal(f.writes.length, 0);
});

// ==================== 集成：真实起服负样本（限流 / token 鉴权） ====================

async function spawnServer(port: number, extraEnv: Record<string, string> = {}) {
  const token = extraEnv.AGENT_WEB_TOKEN || "";
  // W791 CI 修复配套：绝对路径（禁相对·cwd 敏感）+ 子进程输出捕获（失败时可见根因·禁盲超时）
  const tsxCli = path.join(WEB, "node_modules", "tsx", "dist", "cli.mjs");
  if (!fs.existsSync(tsxCli)) {
    throw new Error(`tsx CLI 不存在：${tsxCli}（先 npm ci/install·依赖树要求 node>=22）`);
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
  const headers: Record<string, string> = token ? { "x-agent-token": token } : {};
  // 40 秒启动预算（CI 冷启动余量·W791 实证 Node 20 下 better-sqlite3 加载失败即进程退出）
  for (let i = 0; i < 80; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${port}/api/health`, { headers });
      if (r.ok || r.status === 401) return child; // 401=token 已生效·服务已就绪
    } catch {
      /* 未起 */
    }
    await sleep(500);
  }
  child.kill();
  throw new Error(`server 未就绪（port ${port}）·子进程输出尾部：\n${out.slice(-1500) || "(无输出)"}`);
}

test("集成：/api 限流第 31 次请求 429（W681·每分钟 30 次上限）", async () => {
  const child = await spawnServer(3211);
  try {
    // waitHealth 已用 1 次；再打 29 次凑满 30（应全 200）
    for (let i = 0; i < 29; i++) {
      const r = await fetch("http://127.0.0.1:3211/api/health");
      assert.equal(r.status, 200, `第 ${i + 2} 次应放行`);
    }
    const over = await fetch("http://127.0.0.1:3211/api/health");
    assert.equal(over.status, 429, "第 31 次应被限流");
    const body = await over.json();
    assert.match(String(body.error), /频繁/);
  } finally {
    child.kill();
  }
});

test("集成：AGENT_WEB_TOKEN 鉴权负样本（无头/错头 401·双正确头式 200）", async () => {
  const SECRET = "w791-test-secret";
  const child = await spawnServer(3212, { AGENT_WEB_TOKEN: SECRET });
  try {
    const noHead = await fetch("http://127.0.0.1:3212/api/health");
    assert.equal(noHead.status, 401, "无 token 应 401");
    const wrong = await fetch("http://127.0.0.1:3212/api/health", { headers: { "x-agent-token": "wrong" } });
    assert.equal(wrong.status, 401, "错 token 应 401");
    const okX = await fetch("http://127.0.0.1:3212/api/health", { headers: { "x-agent-token": SECRET } });
    assert.equal(okX.status, 200, "x-agent-token 正确应放行");
    const okBearer = await fetch("http://127.0.0.1:3212/api/health", {
      headers: { Authorization: `Bearer ${SECRET}` },
    });
    assert.equal(okBearer.status, 200, "Authorization Bearer 正确应放行");
  } finally {
    child.kill();
  }
});

// ==================== ⑤ Host 头校验（W835·防 DNS rebinding） ====================

const HOST_ALLOW = ["127.0.0.1", "localhost", "::1"];

test("normalizeHostname：去端口 / IPv6 去方括号 / 小写 / 去 FQDN 尾点 / 畸形判空", () => {
  assert.equal(normalizeHostname("127.0.0.1:3000"), "127.0.0.1");
  assert.equal(normalizeHostname("127.0.0.1"), "127.0.0.1");
  assert.equal(normalizeHostname("LOCALHOST:5173"), "localhost");
  assert.equal(normalizeHostname("[::1]:3000"), "::1");
  assert.equal(normalizeHostname("[::1]"), "::1");
  assert.equal(normalizeHostname("example.com."), "example.com");
  assert.equal(normalizeHostname("  127.0.0.1:3000  "), "127.0.0.1");
  assert.equal(normalizeHostname(""), "");
  assert.equal(normalizeHostname(undefined), "");
  assert.equal(normalizeHostname(null), "");
  assert.equal(normalizeHostname(42), "");
  assert.equal(normalizeHostname("[:3000"), "", "畸形 IPv6 应判空");
});

test("isAllowedHost：白名单内放行（带端口 / 大小写 / IPv6 / 尾点）", () => {
  for (const h of ["127.0.0.1", "127.0.0.1:3000", "localhost", "localhost:5173", "LOCALHOST:3000", "[::1]:3000", "127.0.0.1."]) {
    assert.equal(isAllowedHost(h, HOST_ALLOW), true, `应放行 ${h}`);
  }
});

test("isAllowedHost：白名单外一律判否（fail-closed）", () => {
  for (const h of ["evil.com", "evil.com:3000", "127.0.0.1.evil.com", "localhost.evil.com", "", undefined, null, 7]) {
    assert.equal(isAllowedHost(h, HOST_ALLOW), false, `应拒绝 ${String(h)}`);
  }
});

/** 用 node:http 直发（fetch/undici 受 forbidden header 约束，无法自定义 Host）。 */
function rawGet(
  port: number,
  p: string,
  headers: Record<string, string>
): Promise<{ status: number; body: string }> {
  return new Promise((resolve, reject) => {
    const req = http.request({ host: "127.0.0.1", port, path: p, method: "GET", headers }, (res) => {
      let body = "";
      res.on("data", (c) => (body += String(c)));
      res.on("end", () => resolve({ status: res.statusCode ?? 0, body }));
    });
    req.on("error", reject);
    req.end();
  });
}

test("集成：Host 头校验负样本（rebinding 主机名 403·回环主机名 200）", async () => {
  const child = await spawnServer(3213);
  try {
    const evil = await rawGet(3213, "/api/health", { Host: "evil.com" });
    assert.equal(evil.status, 403, "非白名单 Host 应 403");
    assert.match(evil.body, /Host/, "错误体应说明是 Host 问题");
    const evilWithPort = await rawGet(3213, "/api/health", { Host: "evil.com:3213" });
    assert.equal(evilWithPort.status, 403, "带端口的非白名单 Host 同样应 403");
    const suffix = await rawGet(3213, "/api/health", { Host: "127.0.0.1.evil.com" });
    assert.equal(suffix.status, 403, "后缀伪装应 403");
    const okIp = await rawGet(3213, "/api/health", { Host: "127.0.0.1:3213" });
    assert.equal(okIp.status, 200, "回环 Host 应放行");
    const okName = await rawGet(3213, "/api/health", { Host: "localhost:3213" });
    assert.equal(okName.status, 200, "localhost Host 应放行");
  } finally {
    child.kill();
  }
});

test("集成：AGENT_WEB_REQUIRE_TOKEN=1 且未设 token → 拒绝启动（fail-closed·不降级为免认证）", async () => {
  const tsxCli = path.join(WEB, "node_modules", "tsx", "dist", "cli.mjs");
  const child = spawn(process.execPath, [tsxCli, "server/index.ts"], {
    cwd: WEB,
    env: { ...process.env, PORT: "3214", AGENT_WEB_TOKEN: "", AGENT_WEB_REQUIRE_TOKEN: "1" },
    stdio: ["ignore", "pipe", "pipe"],
  });
  let out = "";
  child.stdout?.on("data", (d) => {
    out += String(d);
  });
  child.stderr?.on("data", (d) => {
    out += String(d);
  });
  const code = await new Promise<number | null>((resolve) => {
    child.on("exit", (c) => resolve(c));
    setTimeout(() => {
      child.kill();
      resolve(null);
    }, 20000);
  });
  assert.notEqual(code, 0, "应拒绝启动（退出码非 0）");
  assert.match(out, /AGENT_WEB_REQUIRE_TOKEN/, "应打印拒绝原因");
});
