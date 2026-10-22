// backup.test.ts — W844 会话库与审计日志快照单测（node:test·经 tsx 运行）。
//
// 形态与 server/audit.test.ts 一致：真实临时目录 + 真实 SQLite 文件，无 mock。
// 覆盖：快照三表行数一致 · 审计副本行数一致 · 源库不被回写 · 同日幂等跳过 ·
//       份数上限收敛 · 超龄清理 · 源库缺失不抛 · dry-run 不落盘 · NODE_ENV=test 不产生快照。
// 运行：cd xiyouji-agent-web && node --import tsx --test server/backup.test.ts
import { test, after } from "node:test";
import assert from "node:assert";
import fs from "fs";
import os from "os";
import path from "path";
import Database from "better-sqlite3";
import { backupOnStartup, runBackup } from "./backup.js";

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "xiyouji-backup-test-"));
let seq = 0;

after(() => {
  fs.rmSync(TMP, { recursive: true, force: true });
});

/** 每条用例独占一个工作目录，用例间零串扰。 */
function caseDir(name?: string): string {
  seq += 1;
  const dir = path.join(TMP, name ?? `case-${seq}`);
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

/** 造一个结构等同于 agent-web 会话库的最小库（三表 + 已知行数）。 */
function makeDb(file: string, rows = { sessions: 3, messages: 5, feedback: 2 }): void {
  const db = new Database(file);
  db.exec(`
    CREATE TABLE sessions (id TEXT PRIMARY KEY, title TEXT, created_at TEXT);
    CREATE TABLE messages (id TEXT PRIMARY KEY, session_id TEXT, role TEXT, content TEXT);
    CREATE TABLE feedback (id TEXT PRIMARY KEY, message_id TEXT, rating TEXT);
  `);
  const insS = db.prepare("INSERT INTO sessions VALUES (?, ?, ?)");
  for (let i = 0; i < rows.sessions; i += 1) insS.run(`s${i}`, `会话${i}`, "2026-10-21T00:00:00Z");
  const insM = db.prepare("INSERT INTO messages VALUES (?, ?, ?, ?)");
  for (let i = 0; i < rows.messages; i += 1) insM.run(`m${i}`, `s${i % rows.sessions}`, "user", `内容${i}`);
  const insF = db.prepare("INSERT INTO feedback VALUES (?, ?, ?)");
  for (let i = 0; i < rows.feedback; i += 1) insF.run(`f${i}`, `m${i}`, "up");
  db.close();
}

function countRows(file: string, table: string): number {
  const db = new Database(file, { readonly: true });
  try {
    const row = db.prepare(`SELECT COUNT(*) AS n FROM ${table}`).get() as { n: number };
    return row.n;
  } finally {
    db.close();
  }
}

/** 造一份「看起来是今天的」快照件（文件名带今天日期）与若干历史件。 */
function seedSnapshot(dir: string, stamp: string, prefix: "chat-" | "audit-", ext: string): string {
  const file = path.join(dir, `${prefix}${stamp}${ext}`);
  fs.writeFileSync(file, "seed", "utf8");
  return file;
}

test("快照生成：三表行数一致 + 审计副本行数一致 + 源库不被回写", () => {
  const dir = caseDir();
  const dbPath = path.join(dir, "chat.db");
  const auditPath = path.join(dir, "audit.jsonl");
  const backupDir = path.join(dir, "backups");
  makeDb(dbPath);
  fs.writeFileSync(auditPath, '{"a":1}\n{"a":2}\n{"a":3}\n', "utf8");

  const before = ["sessions", "messages", "feedback"].map((t) => countRows(dbPath, t));
  const res = runBackup({ dbPath, auditPath, backupDir });

  assert.equal(res.ok, true, `快照应成功：${res.error ?? ""}`);
  assert.ok(res.snapshot && fs.existsSync(res.snapshot), "快照文件应存在");
  assert.deepEqual(
    ["sessions", "messages", "feedback"].map((t) => countRows(res.snapshot!, t)),
    before,
    "快照三表行数应与源库一致",
  );
  assert.ok(res.auditCopy && fs.existsSync(res.auditCopy), "审计副本应存在");
  assert.equal(fs.readFileSync(res.auditCopy!, "utf8"), fs.readFileSync(auditPath, "utf8"), "审计副本内容应一致");
  assert.deepEqual(
    ["sessions", "messages", "feedback"].map((t) => countRows(dbPath, t)),
    before,
    "VACUUM INTO 不回写源库——源库行数应不变",
  );

  // 快照里的行数不能是 0（防「快照成功但空库」这种最危险的静默失败）
  assert.ok(countRows(res.snapshot!, "sessions") > 0, "快照库不得为空");
});

test("同日二次执行：幂等跳过，不覆盖已有快照", () => {
  const dir = caseDir();
  const dbPath = path.join(dir, "chat.db");
  const backupDir = path.join(dir, "backups");
  makeDb(dbPath);

  const first = runBackup({ dbPath, backupDir });
  assert.equal(first.ok, true);
  const mtime1 = fs.statSync(first.snapshot!).mtimeMs;

  const second = runBackup({ dbPath, backupDir });
  assert.equal(second.ok, true);
  assert.equal(second.skipped, true, "同日第二次应跳过");
  assert.equal(fs.statSync(second.snapshot!).mtimeMs, mtime1, "已有快照不应被覆盖");
});

test("保留策略：份数上限收敛到 keep（旧的先删）", () => {
  const dir = caseDir();
  const dbPath = path.join(dir, "chat.db");
  const backupDir = path.join(dir, "backups");
  makeDb(dbPath);
  fs.mkdirSync(backupDir, { recursive: true });
  for (const d of ["20260101", "20260102", "20260103", "20260104", "20260105", "20260106"]) {
    seedSnapshot(backupDir, d, "chat-", ".db");
  }

  const res = runBackup({ dbPath, backupDir, keep: 3, maxAgeDays: 3650 });
  assert.equal(res.ok, true);
  const remain = fs.readdirSync(backupDir).filter((f) => f.startsWith("chat-")).sort();
  assert.equal(remain.length, 3, `份数应收敛到 3，实际 ${remain.join(",")}`);
  assert.ok(remain.includes(path.basename(res.snapshot!)), "今日快照不应被自己删掉");
  assert.ok(remain.includes("chat-20260106.db"), "应保留最新的历史件");
});

test("保留策略：超龄件被清理（与份数条件独立）", () => {
  const dir = caseDir();
  const dbPath = path.join(dir, "chat.db");
  const backupDir = path.join(dir, "backups");
  makeDb(dbPath);
  fs.mkdirSync(backupDir, { recursive: true });
  // 100 天前：按文件名日期判定超龄（keep 给足，确保只由天数条件触发）
  seedSnapshot(backupDir, "20250101", "chat-", ".db");
  seedSnapshot(backupDir, "20250101", "audit-", ".jsonl");

  const res = runBackup({ dbPath, backupDir, keep: 100, maxAgeDays: 90 });
  assert.equal(res.ok, true);
  assert.ok(!fs.existsSync(path.join(backupDir, "chat-20250101.db")), "超龄快照应被清理");
  assert.ok(!fs.existsSync(path.join(backupDir, "audit-20250101.jsonl")), "超龄审计副本应被清理");
  assert.ok(res.pruned && res.pruned.length >= 2, "pruned 应记录被清理件");
});

test("同日幂等跳过时仍执行保留策略（超龄件不会因跳过而永存）", () => {
  const dir = caseDir();
  const dbPath = path.join(dir, "chat.db");
  const backupDir = path.join(dir, "backups");
  makeDb(dbPath);
  fs.mkdirSync(backupDir, { recursive: true });
  const first = runBackup({ dbPath, backupDir });
  assert.equal(first.ok, true);
  seedSnapshot(backupDir, "20250101", "chat-", ".db");

  const second = runBackup({ dbPath, backupDir, maxAgeDays: 90 });
  assert.equal(second.skipped, true);
  assert.ok(!fs.existsSync(path.join(backupDir, "chat-20250101.db")), "跳过分支也必须清理超龄件");
});

test("源库不存在：返回 ok=false 而不抛（启动期不可中断）", () => {
  const dir = caseDir();
  const res = runBackup({ dbPath: path.join(dir, "nope.db"), backupDir: path.join(dir, "backups") });
  assert.equal(res.ok, false);
  assert.ok(res.error && res.error.includes("源库不存在"), `错误信息应指明缺失：${res.error}`);
});

test("dry-run（execute=false）不落盘", () => {
  const dir = caseDir();
  const dbPath = path.join(dir, "chat.db");
  const backupDir = path.join(dir, "backups");
  makeDb(dbPath);

  const res = runBackup({ dbPath, backupDir, execute: false });
  assert.equal(res.ok, true);
  assert.equal(fs.existsSync(backupDir), false, "预演不应创建备份目录");
});

test("backupOnStartup：NODE_ENV=test 时不产生任何快照", () => {
  const dir = caseDir();
  const dbPath = path.join(dir, "chat.db");
  const backupDir = path.join(dir, "backups");
  makeDb(dbPath);

  const prevEnv = process.env.NODE_ENV;
  const prevDir = process.env.XIYOUJI_BACKUP_DIR;
  process.env.NODE_ENV = "test";
  process.env.XIYOUJI_BACKUP_DIR = backupDir;
  try {
    backupOnStartup(dbPath, path.join(dir, "audit.jsonl"));
    assert.equal(fs.existsSync(backupDir), false, "测试环境不应落快照");
  } finally {
    if (prevEnv === undefined) delete process.env.NODE_ENV;
    else process.env.NODE_ENV = prevEnv;
    if (prevDir === undefined) delete process.env.XIYOUJI_BACKUP_DIR;
    else process.env.XIYOUJI_BACKUP_DIR = prevDir;
  }
});

test("backupOnStartup：非测试环境下源库缺失也不抛（只记日志）", () => {
  const dir = caseDir();
  const prevEnv = process.env.NODE_ENV;
  process.env.NODE_ENV = "production";
  try {
    assert.doesNotThrow(() => backupOnStartup(path.join(dir, "nope.db")));
  } finally {
    if (prevEnv === undefined) delete process.env.NODE_ENV;
    else process.env.NODE_ENV = prevEnv;
  }
});
