/**
 * chat.e2e.mjs — agent-web 端到端测试（W808 新建·第三层）
 *
 * 纪律（skill「三件套」之第三层·E2E）：
 *   走**真实浏览器 + 真实前端构建产物 + 真实后端 + 真实 SQLite**，
 *   覆盖用户实际点击的完整流程（输入 → 发送 → 流式渲染 → 落库 → 反馈）。
 *
 * 唯一替身是**外部大模型端点**（e2e/mockLlm.mjs）——被测系统全部为真实实现。
 * 理由：真接大模型需凭证 + 花钱 + 网络，且响应不确定无法断言。
 *
 * 运行：cd xiyouji-agent-web && node e2e/chat.e2e.mjs
 * 依赖：playwright + chromium（仓内 scripts/ 已装·本脚本自动解析其路径）
 */
import { spawn } from "node:child_process";
import { createRequire } from "node:module";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Database from "better-sqlite3";
import { startMockLlm } from "./mockLlm.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const WEB = path.resolve(HERE, "..");
const REPO = path.resolve(WEB, "..");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** 解析 playwright（优先本目录，其次仓内 scripts/——与 tests/e2e 的解析范式一致）。 */
function loadPlaywright() {
  const require = createRequire(import.meta.url);
  const candidates = [WEB, path.join(REPO, "scripts")];
  for (const base of candidates) {
    try {
      return require(require.resolve("playwright", { paths: [base] }));
    } catch {
      /* 试下一个 */
    }
  }
  throw new Error("未找到 playwright（先在 scripts/ 或 xiyouji-agent-web/ 安装）");
}

const { chromium } = loadPlaywright();

/** 起真实后端（tsx 直跑 server/index.ts）。 */
async function startBackend(port, llmBaseUrl) {
  const tsxCli = path.join(WEB, "node_modules", "tsx", "dist", "cli.mjs");
  if (!fs.existsSync(tsxCli)) throw new Error(`tsx CLI 不存在：${tsxCli}`);
  // W829：硬守卫——本 E2E 只允许跑在临时库上。若 DB_PATH 指向仓库真实库（data/chat.db），
  // 立即拒绝启动：原实现的清理逻辑会按「最近更新的 session」删库，命中真实会话即不可逆丢失。
  const resolvedDb = path.resolve(DB_PATH);
  if (DB_IS_REAL) {
    throw new Error(`E2E 拒绝在真实库上运行（DB_PATH 指向 ${REAL_DB}）——会删除开发者真实会话`);
  }
  const child = spawn(process.execPath, [tsxCli, "server/index.ts"], {
    cwd: WEB,
    env: {
      ...process.env,
      PORT: String(port),
      AGENT_WEB_TOKEN: "",
      // W829：库路径指向临时库（server/db.ts 据此覆盖·默认路径不变）
      AGENT_WEB_DB_PATH: resolvedDb,
      // 引擎三键指向 mock LLM（真实链路·仅外部端点被替身）
      LLM_API_BASE: llmBaseUrl,
      LLM_API_KEY: "w808-e2e-key",
      LLM_MODEL: "mock-model",
    },
    stdio: ["ignore", "pipe", "pipe"],
  });
  let out = "";
  child.stdout?.on("data", (d) => {
    out += String(d);
  });
  child.stderr?.on("data", (d) => {
    out += String(d);
  });
  for (let i = 0; i < 80; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${port}/api/health`);
      if (r.ok) return { child, output: () => out };
    } catch {
      /* 未起 */
    }
    await sleep(500);
  }
  child.kill();
  throw new Error(`后端未就绪（port ${port}）·输出尾部：\n${out.slice(-1200)}`);
}

/** 起真实前端（vite preview 托管 build 产物 + /api 代理到后端）。 */
async function startFrontend(port, backendPort) {
  const viteBin = path.join(WEB, "node_modules", "vite", "bin", "vite.js");
  if (!fs.existsSync(viteBin)) throw new Error(`vite 不存在：${viteBin}`);
  if (!fs.existsSync(path.join(WEB, "dist", "index.html"))) {
    throw new Error("缺 dist/ 构建产物（先跑 npm run build）");
  }
  const child = spawn(
    process.execPath,
    [viteBin, "preview", "--config", "vite.config.ts", "--port", String(port), "--strictPort"],
    {
      cwd: WEB,
      env: { ...process.env, VITE_API_PROXY_TARGET: `http://127.0.0.1:${backendPort}` },
      stdio: ["ignore", "pipe", "pipe"],
    }
  );
  let out = "";
  child.stdout?.on("data", (d) => {
    out += String(d);
  });
  child.stderr?.on("data", (d) => {
    out += String(d);
  });
  for (let i = 0; i < 80; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${port}/`);
      if (r.ok) return { child, output: () => out };
    } catch {
      /* 未起 */
    }
    await sleep(500);
  }
  child.kill();
  throw new Error(`前端未就绪（port ${port}）·输出尾部：\n${out.slice(-1200)}`);
}

// ==================== 断言辅助 ====================

let passed = 0;
let failed = 0;
const failures = [];

function check(name, condition, detail = "") {
  if (condition) {
    passed += 1;
    console.log(`PASS ${name}`);
  } else {
    failed += 1;
    failures.push(name);
    console.log(`FAIL ${name}${detail ? " → " + detail : ""}`);
  }
}

// ==================== 主流程 ====================

const BACKEND_PORT = 3231;
// 前端端口须避开 Windows WinNAT 保留段（本机实存 3732-4537 连片）——4232 落 4138-4237 内，
// vite preview listen 直接 EACCES（「端口占用是假故障」的保留段形态·pitfalls W975）。
const FRONTEND_PORT = 4600;
const REPLY = "《西游记》测试回复：这是 mock LLM 产出的确定性文本。";

// W829：E2E 必须跑在**临时库**上。
// 成因：原实现库路径写死（server/db.ts 硬编码 data/chat.db），E2E 的清理逻辑
// 按「最近更新的 session」删 feedback/messages/sessions → 若本轮聊天未落库而库中
// 已有历史会话，被删的就是**开发者的真实会话**（含工具结果原文·不可逆·无备份）。
// 现在：后端经 AGENT_WEB_DB_PATH 指向临时库；断言与清理只用该临时库；
// 并在收尾断言**真实库零改动**（大小 + mtime 双比对）。
const REAL_DB = path.join(WEB, "data", "chat.db");
// 允许用环境变量覆盖临时库路径（**仅用于负样本自证**：指向真实库时必须拒绝启动）
const DB_PATH = process.env.AGENT_WEB_DB_PATH
  ? path.resolve(process.env.AGENT_WEB_DB_PATH)
  : path.join(os.tmpdir(), `xiyouji-e2e-${process.pid}-${Date.now()}.db`);
// W829 负样本自证事故订正：守卫必须**三处同源**——① 启动侧拒绝 ② 清理侧不删
// ③ 断言置于全部清理之后。此前仅①有守卫、②③缺位 ⇒ 一次「指向真实库」的自证
// 把真实 data/chat.db 连同 -wal/-shm 删掉（已用 W828 批的 VACUUM INTO 快照复原：
// integrity_check=ok·65 会话/129 消息全量·快照后无新会话故实际零丢失）。
const DB_IS_REAL = path.resolve(DB_PATH) === path.resolve(REAL_DB);
function realDbFingerprint() {
  try {
    const st = fs.statSync(REAL_DB);
    return `${st.size}:${st.mtimeMs}`;
  } catch {
    return "absent";
  }
}
const REAL_DB_BEFORE = realDbFingerprint();

let backend;
let frontend;
let mockLlm;
let browser;
const createdSessionIds = [];

try {
  console.log("== 准备：启动 mock LLM / 真实后端 / 真实前端 ==");
  mockLlm = await startMockLlm(0, { reply: REPLY, chunkSize: 8 });
  backend = await startBackend(BACKEND_PORT, mockLlm.baseUrl);
  frontend = await startFrontend(FRONTEND_PORT, BACKEND_PORT);
  console.log(`   mock LLM: ${mockLlm.baseUrl}`);
  console.log(`   后端:     http://127.0.0.1:${BACKEND_PORT}`);
  console.log(`   前端:     http://127.0.0.1:${FRONTEND_PORT}`);

  browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  // 收集控制台错误与页面异常（前端健康度的硬指标）
  const consoleErrors = [];
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });
  page.on("pageerror", (err) => consoleErrors.push(`pageerror: ${err.message}`));

  // ---------- 步骤 1：首页加载 ----------
  await page.goto(`http://127.0.0.1:${FRONTEND_PORT}/`, { waitUntil: "networkidle" });
  await page.waitForSelector("text=西游记·渡口问津", { timeout: 20000 });
  check("E2E-1 首页加载并渲染标题", true);

  // ---------- 步骤 2：新对话页出现 ----------
  const newChatVisible = await page
    .locator("text=选择一个 Agent 开始对话")
    .isVisible()
    .catch(() => false);
  check("E2E-2 新对话视图出现（Agent 选择）", newChatVisible);

  // ---------- 步骤 3：输入并发送 ----------
  // 注意：TDesign 的 ChatSender 是自定义元素（t-chat-sender），输入框与发送按钮都在
  // **shadow DOM** 内——Playwright 的 CSS 选择器默认穿透 shadow DOM，但 page.evaluate
  // 里的 querySelector 不穿透（故断言一律用 locator，不用 evaluate 查 DOM）。
  const input = page.locator("t-chat-sender textarea").first();
  await input.waitFor({ state: "visible", timeout: 20000 });
  await input.fill("请用一句话介绍《西游记》的主题");
  // 发送按钮：t-icon-send-filled 图标（ChatSender 的 send action）
  const sendBtn = page.locator("t-chat-sender svg.t-icon-send-filled").first();
  await sendBtn.waitFor({ state: "attached", timeout: 10000 });
  await sendBtn.click({ timeout: 10000 });

  // ---------- 步骤 4：流式渲染出 mock 回复 ----------
  await page.waitForSelector(`text=${REPLY.slice(0, 12)}`, { timeout: 30000 });
  check("E2E-4 助手回复渲染到界面（流式链路贯通）", true);

  // ---------- 步骤 5：回复完整（含跨 chunk 拼接） ----------
  const fullReplyVisible = await page
    .locator(`text=${REPLY}`)
    .first()
    .isVisible()
    .catch(() => false);
  check("E2E-5 回复文本完整（跨 chunk 解码无断裂）", fullReplyVisible);

  // ---------- 步骤 6：会话与消息真实落库（W829：断言与清理只针对**临时库**） ----------
  const db = new Database(DB_PATH, { readonly: true });
  const sessions = db.prepare("SELECT id FROM sessions ORDER BY updated_at DESC LIMIT 5").all();
  db.close();
  const sessionId = sessions.length > 0 ? sessions[0].id : "";
  check("E2E-6 会话真实落库", Boolean(sessionId), `sessions=${sessions.length}`);
  createdSessionIds.push(sessionId);

  // ---------- 步骤 7：反馈按钮可点且真实落库（W808 修的真实缺陷） ----------
  // 此前前端提交体缺 sessionId → 服务端恒 400 → 赞/踩从未被记录且界面无异常。
  const upBtn = page.locator('button[title="赞"]').first();
  const hasUpBtn = (await upBtn.count()) > 0;
  check("E2E-7 回复下方出现反馈按钮", hasUpBtn);

  if (hasUpBtn) {
    await upBtn.click({ timeout: 10000 });
    // 等待反馈行落库（前端在请求成功后写入乐观 UI，故以落库为准）
    let feedbackRow = null;
    for (let i = 0; i < 20; i++) {
      const db2 = new Database(DB_PATH, { readonly: true });
      const row = db2
        .prepare(
          `SELECT f.session_id, f.verdict, m.content
             FROM feedback f JOIN messages m ON m.id = f.message_id
            WHERE f.session_id = ? ORDER BY f.created_at DESC LIMIT 1`
        )
        .get(sessionId);
      db2.close();
      if (row) {
        feedbackRow = row;
        break;
      }
      await sleep(300);
    }
    check(
      "E2E-8 反馈真实落库（sessionId 三字段齐备·W808 修复点）",
      Boolean(feedbackRow),
      feedbackRow ? "" : "未查到反馈行——旧实现因缺 sessionId 恒 400"
    );
    if (feedbackRow) {
      check("E2E-9 反馈行归属正确会话", feedbackRow.session_id === sessionId);
      check("E2E-10 反馈 verdict 为 up", feedbackRow.verdict === "up");
    }
  }

  // ---------- 步骤 11：控制台无错误 ----------
  const realErrors = consoleErrors.filter((e) => !/favicon|404 \(Not Found\)/i.test(e));
  check("E2E-11 前端控制台无错误", realErrors.length === 0, realErrors.slice(0, 3).join(" | "));

  await context.close();
} catch (err) {
  failed += 1;
  failures.push(`执行异常：${err?.message || err}`);
  console.log(`FAIL 执行异常 → ${err?.stack || err}`);
} finally {
  // 清理：关浏览器/服务 + 删测试会话与反馈
  try {
    if (browser) await browser.close();
  } catch {
    /* 忽略 */
  }
  try {
    if (frontend) frontend.child.kill();
  } catch {
    /* 忽略 */
  }
  try {
    if (backend) backend.child.kill();
  } catch {
    /* 忽略 */
  }
  try {
    if (mockLlm) await mockLlm.close();
  } catch {
    /* 忽略 */
  }
  // W829：清理只针对**临时库**——若 DB_PATH 指向真实库则**一律不动**
  // （事故订正：此前此处无守卫，一次「指向真实库」的负样本自证把真实
  //   data/chat.db 连同 -wal/-shm 删掉；已用 W828 批的 VACUUM INTO 快照复原）
  if (!DB_IS_REAL) {
    try {
      const db = new Database(DB_PATH);
      for (const sid of createdSessionIds) {
        db.prepare("DELETE FROM feedback WHERE session_id = ?").run(sid);
        db.prepare("DELETE FROM messages WHERE session_id = ?").run(sid);
        db.prepare("DELETE FROM sessions WHERE id = ?").run(sid);
      }
      db.close();
    } catch {
      /* 清理失败不影响结论 */
    }
    try {
      for (const suffix of ["", "-wal", "-shm"]) {
        const f = DB_PATH + suffix;
        if (fs.existsSync(f)) fs.rmSync(f, { force: true });
      }
    } catch {
      /* 临时库清理失败不影响结论 */
    }
  } else {
    console.log("WARN DB_PATH 指向真实库 → 跳过全部清理（不删任何文件与行）");
  }
  // W829：终检断言——真实库零改动（大小 + mtime 双比对）·**置于全部清理之后**
  check("E2E-11 真实库零改动（本 E2E 未触碰 data/chat.db）", realDbFingerprint() === REAL_DB_BEFORE,
    `before=${REAL_DB_BEFORE} after=${realDbFingerprint()}`);
}

console.log(`\n== E2E 结果：${passed} 通过 / ${failed} 失败 ==`);
if (failures.length) console.log(`失败项：${failures.join(" · ")}`);
process.exit(failed ? 1 : 0);
