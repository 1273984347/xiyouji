// audit.test.ts — W752 写操作持久化审计单测（node:test·经 tsx 运行）。
//
// 形态与 server/citationGuard.test.ts 一致：真实临时文件 + 真实读写，无 mock。
// 覆盖：追加/读回/字段契约 · 超限截断 · 坏行容忍 · 审计失败 fail-open（不可写路径不抛）。
// 运行：cd xiyouji-agent-web && node --import tsx --test server/audit.test.ts
import { test, after } from "node:test";
import assert from "node:assert";
import fs from "fs";
import os from "os";
import path from "path";
import { appendAudit, auditLogPath, auditTarget, readAudit } from "./audit.js";
import type { AuditEntry } from "./audit.js";

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "xiyouji-audit-test-"));
let seq = 0;

/** 每条用例独占一个审计文件（通过 AGENT_WEB_AUDIT_LOG 覆盖），用例间零串扰。 */
async function withLogFile<T>(fn: (file: string) => Promise<T> | T, name?: string): Promise<T> {
  seq += 1;
  const file = path.join(TMP, name ?? `case-${seq}`, "audit.jsonl");
  const prev = process.env.AGENT_WEB_AUDIT_LOG;
  process.env.AGENT_WEB_AUDIT_LOG = file;
  try {
    return await fn(file);
  } finally {
    if (prev === undefined) delete process.env.AGENT_WEB_AUDIT_LOG;
    else process.env.AGENT_WEB_AUDIT_LOG = prev;
  }
}

const entry = (over: Partial<AuditEntry> = {}): Omit<AuditEntry, "ts"> & { ts?: string } => ({
  sessionId: "sess-1",
  tool: "write_file",
  phase: "permission",
  decision: "allow",
  kind: "write",
  path: "docs/x.md",
  bytes: 6,
  reason: "acceptEdits 写面自动放行",
  ...over,
});

after(() => fs.rmSync(TMP, { recursive: true, force: true }));

test("A1 追加两条→读回两条（字段契约完整·顺序旧→新）", async () => {
  await withLogFile(async (file) => {
    appendAudit(entry());
    appendAudit(entry({ tool: "run_command", kind: "command", decision: "deny", path: undefined, command: "rm -rf /", bytes: undefined, isError: true, reason: "命令不在白名单" }));

    // 一行一条合法 JSON（JSONL 契约）
    const lines = fs.readFileSync(file, "utf8").trim().split("\n");
    assert.equal(lines.length, 2);
    for (const l of lines) assert.doesNotThrow(() => JSON.parse(l));

    const r = readAudit(100);
    assert.equal(r.entries.length, 2);
    assert.equal(r.total, 2);
    assert.equal(r.skipped, 0);

    const e0 = r.entries[0];
    assert.equal(e0.sessionId, "sess-1");
    assert.equal(e0.tool, "write_file");
    assert.equal(e0.phase, "permission");
    assert.equal(e0.decision, "allow");
    assert.equal(e0.kind, "write");
    assert.equal(e0.path, "docs/x.md");
    assert.equal(e0.bytes, 6);
    assert.equal(typeof e0.ts, "string");
    assert.ok(!Number.isNaN(Date.parse(e0.ts)), "ts 应为可解析时间戳");

    const e1 = r.entries[1];
    assert.equal(e1.tool, "run_command");
    assert.equal(e1.decision, "deny");
    assert.equal(e1.command, "rm -rf /");
    assert.equal(e1.isError, true);
    assert.match(String(e1.reason), /白名单/);
    assert.equal("path" in e1, false, "未提供的字段不应写入（日志不留空键噪声）");
  });
});

test("A2 超限截断：limit 取最近 N 条（默认/非法值回落 100）", async () => {
  await withLogFile(async () => {
    for (let i = 1; i <= 5; i++) appendAudit(entry({ reason: `第${i}条` }));
    const r2 = readAudit(2);
    assert.equal(r2.entries.length, 2);
    assert.equal(r2.total, 5, "total 是日志内可解析总数，不随 limit 变");
    assert.match(String(r2.entries[0].reason), /第4条/);
    assert.match(String(r2.entries[1].reason), /第5条/);

    assert.equal(readAudit(100).entries.length, 5);
    assert.equal(readAudit(99999).entries.length, 5, "超过上限的 limit 仍能读全（内部封顶 1000）");
    assert.equal(readAudit(0).entries.length, 5, "limit=0 为非法值 → 回落默认 100");
    assert.equal(readAudit(Number.NaN).entries.length, 5, "limit=NaN 为非法值 → 回落默认 100");
  });
});

test("A3 坏行容忍：解析失败/缺关键字段只计数不抛，合法行照常读回", async () => {
  await withLogFile(async (file) => {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    const good1 = { ts: "2026-10-15T00:00:00.000Z", sessionId: "s", tool: "write_file", phase: "result", decision: "allow", kind: "write" };
    const good2 = { ...good1, tool: "edit_file" };
    fs.writeFileSync(
      file,
      [JSON.stringify(good1), "{ 这不是 JSON", JSON.stringify({ ts: "2026-10-15T00:00:01.000Z" }), "", JSON.stringify(good2), "   "].join("\n") + "\n",
      "utf8"
    );
    const r = readAudit(10);
    assert.equal(r.entries.length, 2, "合法行应全部读回");
    assert.equal(r.total, 2);
    assert.equal(r.skipped, 2, "坏 JSON + 缺 tool 各计一条坏行；空行不计");
    assert.equal(r.entries[0].tool, "write_file");
    assert.equal(r.entries[1].tool, "edit_file");
  });
});

test("A4 审计失败 fail-open：不可写路径不抛异常，只 console.error；读侧同为空不抛", async () => {
  await withLogFile(async () => {
    // 父路径是普通文件 → mkdirSync 必失败（磁盘满/权限类故障的可复现替身）
    const blocker = path.join(TMP, "blocker-file");
    fs.writeFileSync(blocker, "not a directory", "utf8");
    process.env.AGENT_WEB_AUDIT_LOG = path.join(blocker, "audit.jsonl");

    const origError = console.error;
    const logged: string[] = [];
    console.error = ((...args: unknown[]) => {
      logged.push(args.map(String).join(" "));
    }) as typeof console.error;
    try {
      assert.doesNotThrow(() => appendAudit(entry()), "审计写入失败绝不能向上抛（fail-open）");
    } finally {
      console.error = origError;
    }
    assert.ok(logged.some((l) => l.includes("[audit] 写入失败")), `应落一条 console.error：${logged.join(" | ")}`);
  });
});

test("A5 缺文件/不可读路径：readAudit 返回空且不抛", async () => {
  await withLogFile(async (file) => {
    assert.deepEqual(readAudit(10), { entries: [], total: 0, skipped: 0 }, "文件不存在＝空日志");
    const blocker = path.join(TMP, "blocker-file-2");
    fs.writeFileSync(blocker, "x", "utf8");
    process.env.AGENT_WEB_AUDIT_LOG = path.join(blocker, "audit.jsonl");
    assert.deepEqual(readAudit(10), { entries: [], total: 0, skipped: 0 }, "不可读路径＝空日志");
    assert.equal(fs.existsSync(file), false);
  });
});

test("A6 默认路径＝xiyouji-agent-web/data/audit.jsonl（可用 AGENT_WEB_AUDIT_LOG 覆盖）", () => {
  const prev = process.env.AGENT_WEB_AUDIT_LOG;
  delete process.env.AGENT_WEB_AUDIT_LOG;
  try {
    const p = auditLogPath().split(path.sep).join("/");
    assert.match(p, /\/xiyouji-agent-web\/data\/audit\.jsonl$/);
    process.env.AGENT_WEB_AUDIT_LOG = "  ";
    assert.equal(auditLogPath(), auditLogPath(), "空白覆盖值应回落默认（幂等）");
    process.env.AGENT_WEB_AUDIT_LOG = path.join(TMP, "custom.jsonl");
    assert.equal(auditLogPath(), path.join(TMP, "custom.jsonl"));
  } finally {
    if (prev === undefined) delete process.env.AGENT_WEB_AUDIT_LOG;
    else process.env.AGENT_WEB_AUDIT_LOG = prev;
  }
});

test("A7 auditTarget：提取 path/command/bytes，命令超长截断", () => {
  assert.deepEqual(auditTarget({ path: "docs/a.md", content: "你好" }), { path: "docs/a.md", bytes: 6 });
  assert.deepEqual(auditTarget({ command: "git status" }), { command: "git status" });
  assert.deepEqual(auditTarget(undefined), {});
  assert.deepEqual(auditTarget({}), {});
  const long = auditTarget({ command: "x".repeat(900) });
  assert.equal(String(long.command).length, 500, "命令字段截断至 500");
});
