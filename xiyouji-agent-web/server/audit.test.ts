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
import {
  appendAudit,
  auditDegradation,
  auditDegradationMarkerPath,
  auditLogPath,
  auditTarget,
  clearAuditDegradation,
  purgeAuditBefore,
  purgeExpiredAudit,
  readAudit,
} from "./audit.js";
import type { AuditEntry } from "./audit.js";
import { AUDIT_REQUIRED_FIELDS, isStructuredAuditEvent } from "./compliance/audit-event.js";

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

test("A8 结构化事件：§12.3 的 11 个必填字段齐全 + 派生规则正确", async () => {
  await withLogFile(async (file) => {
    clearAuditDegradation(); // 隔离：前序用例故意制造过降级，进程内状态会延续
    appendAudit(entry());
    const e = JSON.parse(fs.readFileSync(file, "utf8").trim().split("\n")[0]);
    for (const f of AUDIT_REQUIRED_FIELDS) {
      assert.ok(f in e, "必填字段 " + f + " 应存在");
    }
    assert.equal(isStructuredAuditEvent(e), true, "新写入的事件应通过结构校验");
    assert.match(e.event_id, /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i, "event_id 应是 UUID");
    assert.equal(e.actor, "sess-1", "actor 缺省派生自会话 ID");
    assert.equal(e.action, "permission", "phase=permission ⇒ action=permission");
    assert.equal(e.target, "docs/x.md", "target 缺省派生自 path");
    assert.equal(e.result, "ok", "result 缺省派生自 isError");
    assert.equal(e.data_class, "L4", "审计事件自身分级 = L4（§12.1）");
    assert.equal(e.trace_id, "");
    assert.equal(e.source_ip, "");
    assert.equal(e.schema_version, 1);
    // 显式提供的新字段优先于派生
    appendAudit(entry({ trace_id: "trace-1", source_ip: "10.0.0.1", data_class: "L3", action: "write" }));
    const e2 = JSON.parse(fs.readFileSync(file, "utf8").trim().split("\n")[1]);
    assert.equal(e2.trace_id, "trace-1");
    assert.equal(e2.source_ip, "10.0.0.1");
    assert.equal(e2.data_class, "L3");
    assert.equal(e2.action, "write");
  });
});

test("A9 C-7 只增不改：存量旧格式行仍可解析，且与新格式行共存", async () => {
  await withLogFile(async (file) => {
    const legacy = { ts: "2026-01-01T00:00:00.000Z", sessionId: "s", tool: "write_file", phase: "result", decision: "allow", kind: "write" };
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, JSON.stringify(legacy) + "\n", "utf8");
    appendAudit(entry());
    const r = readAudit(10);
    assert.equal(r.entries.length, 2, "旧行与新行都应读回");
    assert.equal(r.skipped, 0, "旧行不得被计为坏行");
    assert.equal(r.entries[0].event_id, undefined, "旧行本来就没有新字段（读侧须容忍）");
    assert.equal(isStructuredAuditEvent(r.entries[0]), false);
    assert.equal(isStructuredAuditEvent(r.entries[1]), true, "新行结构完整");
  });
});

test("A10 F10 合规降级：写入失败 ⇒ 告警 + 降级标记落盘 + 缺口窗口（不得静默）", async () => {
  await withLogFile(async (file) => {
    clearAuditDegradation();
    // 把审计日志路径本身建成目录 ⇒ append 必失败（EISDIR）；父目录可写 ⇒ 降级标记能落盘
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.mkdirSync(file, { recursive: true });
    const origError = console.error;
    const logged: string[] = [];
    console.error = ((...args: unknown[]) => {
      logged.push(args.map(String).join(" "));
    }) as typeof console.error;
    try {
      assert.doesNotThrow(() => appendAudit(entry()), "审计失败仍不得带崩工具调用（fail-open 保留）");
    } finally {
      console.error = origError;
    }
    assert.ok(
      logged.some((l) => l.includes("[audit] 写入失败") && l.includes("合规降级")),
      "必须告警且明示合规降级（不得静默）：" + logged.join(" | "),
    );
    const state = auditDegradation();
    assert.equal(state.degraded, true, "写入失败必须标记「合规降级」");
    assert.ok(state.failures >= 1, "失败次数须可查");
    assert.ok(state.gapStart !== null, "缺口窗口起点须可查");
    const marker = auditDegradationMarkerPath();
    assert.equal(fs.existsSync(marker), true, "降级标记须落盘（重启后仍可见）");
    const markerBody = JSON.parse(fs.readFileSync(marker, "utf8")) as { degraded: boolean; failures: number };
    assert.equal(markerBody.degraded, true);
    assert.ok(markerBody.failures >= 1);
  });
});

test("A11 恢复时补记缺口窗口事件（期间不可补造丢失事件）并解除降级", async () => {
  await withLogFile(async (file) => {
    clearAuditDegradation();
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.mkdirSync(file, { recursive: true });
    const origError = console.error;
    console.error = (() => undefined) as typeof console.error;
    try {
      appendAudit(entry());
      appendAudit(entry({ tool: "edit_file" }));
    } finally {
      console.error = origError;
    }
    assert.equal(auditDegradation().failures, 2, "两次失败都应计数");
    // 恢复：把占位的目录移开 ⇒ 写入恢复
    fs.rmSync(file, { recursive: true, force: true });
    appendAudit(entry({ tool: "run_command" }));

    const lines = fs.readFileSync(file, "utf8").trim().split("\n");
    assert.equal(lines.length, 2, "应有 1 条恢复事件 + 1 条缺口补记事件（失败的 2 条不可补造）");
    const gap = JSON.parse(lines[1]) as { action: string; kind: string; gap?: { start: string; end: string; failures: number }; reason: string; data_class: string };
    assert.equal(gap.action, "ops", "缺口补记事件的动作应是运维类");
    assert.equal(gap.kind, "audit_gap");
    assert.equal(gap.data_class, "L4");
    assert.ok(gap.gap, "缺口窗口须结构化记录");
    assert.equal(gap.gap.failures, 2);
    assert.ok(gap.gap.start <= gap.gap.end, "缺口窗口区间须有序");
    assert.match(gap.reason, /不可补/, "须明示缺失期间不可补");
    assert.equal(auditDegradation().degraded, false, "恢复后应解除降级");
    assert.equal(fs.existsSync(auditDegradationMarkerPath()), false, "降级标记应被清除");
  });
});

test("A12 到期销毁：只删过期行 + 销毁留证（销毁动作本身写一条新事件）", async () => {
  await withLogFile(async (file) => {
    clearAuditDegradation(); // 隔离：避免前序降级补记事件混入计数
    appendAudit(entry({ ts: "2020-01-01T00:00:00.000Z" }));
    appendAudit(entry({ ts: "2026-01-01T00:00:00.000Z" }));
    appendAudit(entry({ ts: "2026-11-01T00:00:00.000Z" }));
    // 截止时刻取 2020 与 2026-01-01 之间 ⇒ 只有 2020 那条到期
    const r = purgeAuditBefore("2025-06-01T00:00:00.000Z");
    assert.equal(r.removed, 1, "只应销毁截止时刻之前的 1 条（2026-01-01 仍在留存期内）");
    assert.equal(r.kept, 2);
    const lines = fs.readFileSync(file, "utf8").trim().split("\n");
    assert.equal(lines.length, 3, "销毁后应剩 2 条留存期内事件 + 1 条销毁留证");
    const evidence = JSON.parse(lines[lines.length - 1]) as { action: string; data_class: string; reason: string; event_id: string };
    assert.equal(evidence.action, "destroy", "销毁留证事件的动作应是 destroy");
    assert.equal(evidence.data_class, "L4");
    assert.match(evidence.reason, /销毁/);
    assert.equal(evidence.event_id, r.evidenceEventId, "留证事件 ID 须可对账");
    // 留存期内的事件未被修改（只追加）
    const kept = readAudit(100);
    assert.equal(kept.entries.length, 3);
    assert.equal(kept.entries[0].ts, "2026-01-01T00:00:00.000Z");
  });
});

test("A13 purgeExpiredAudit：按生效留存期（审计默认 180 天）销毁到期事件", async () => {
  await withLogFile(async () => {
    appendAudit(entry({ ts: "2020-01-01T00:00:00.000Z" }));
    appendAudit(entry({ ts: new Date().toISOString() }));
    const r = purgeExpiredAudit();
    assert.equal(r.removed, 1, "2020 年的事件已超 180 天留存期");
    assert.equal(r.kept, 1, "当期事件必须保留");
  });
});

test("A7 auditTarget：提取 path/command/bytes，命令超长截断", () => {
  assert.deepEqual(auditTarget({ path: "docs/a.md", content: "你好" }), { path: "docs/a.md", bytes: 6 });
  assert.deepEqual(auditTarget({ command: "git status" }), { command: "git status" });
  assert.deepEqual(auditTarget(undefined), {});
  assert.deepEqual(auditTarget({}), {});
  const long = auditTarget({ command: "x".repeat(900) });
  assert.equal(String(long.command).length, 500, "命令字段截断至 500");
});
