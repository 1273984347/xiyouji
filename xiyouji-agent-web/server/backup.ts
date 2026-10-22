/**
 * backup.ts — 会话库与审计日志的本地快照（W844 批次施工件·Q1「会话库纳入备份与保留期」）
 *
 * 目的：为「Q1 会话库纳入备份与保留期策略」提供可执行实现，解决两项现状缺口：
 *   ① chat.db 及其 WAL 伴生文件与 audit.jsonl 全部位于 gitignored 目录 → 既不在 Git 里、
 *      也无任何备份 → 是全仓唯一「不可重建」的数据；
 *   ② 直接拷贝 chat.db 主文件会丢失 WAL 中尚未 checkpoint 的最近提交。
 *
 * 号段说明：本件原定为 W828 批（tmpe/w828/ 工地备料），因当时 CHANGELOG 顶段号序链
 * 断裂（W828 缺口）无法级联立段，内容未施工；W842 修复号序链后以 W844 承接落地，
 * 逻辑与验证证据沿用备料件（2026-10-20 对真实库实跑 ALL PASS）。
 *
 * 实现约束（不可放宽）：
 *   - 必须用 SQLite 的 `VACUUM INTO` 生成一致性快照（SQLite ≥ 3.27），**禁**用文件拷贝；
 *     本机 better-sqlite3 内置 SQLite 3.53.4 · Python 侧 sqlite3 3.49.1 · CLI 3.53.4。
 *   - 每日一份（文件名按日期，重复启动幂等跳过）+ 保留最近 7 份 + 超过 90 天清理。
 *   - 备份对象两件：会话库快照（.db）与审计日志副本（.jsonl，追加式文本 → 直接拷贝）。
 *   - 备份件年龄以**文件名日期**为主判据（构造即含日期），mtime 仅兜底（复制/触碰会漂移）。
 *   - 绝不抛错中断启动：异常一律落日志并继续。
 *
 * 验证（2026-10-20 · tmpe/w828/backup_probe.py 对真实库实跑 · ALL PASS）：
 *   V1 只读源库 VACUUM INTO 成功 · V2 快照三表行数 == 源库（sessions 65 / messages 129 /
 *   feedback 0）· V3 审计副本 46 行 == 源 46 行 · V4a 同日二次执行跳过 · V4b/V4c 超龄件
 *   被清理 · V4d 份数收敛到 7 · V5 源库行数未变（VACUUM INTO 不回写源）。
 *   首跑曾暴露两处设计缺陷并已修：① 幂等早退整段跳过保留策略 → 过期件永不清理；
 *   ② 份数与天数两条件被错误嵌套成「仅在超份数时才查超龄」→ 90 天规则实际失效。
 */

import fs from "fs";
import os from "os";
import path from "path";
import Database from "better-sqlite3";
import { logger } from "./logger.js";

/** 备份根目录：默认落在仓外（%LOCALAPPDATA%\xiyouji\backups），避免明文误入 Git。
 *  `XIYOUJI_BACKUP_DIR` 可覆盖（测试隔离 / 指定盘位）。 */
function defaultBackupDir(): string {
  const override = (process.env.XIYOUJI_BACKUP_DIR || "").trim();
  if (override) return path.resolve(override);
  const local = process.env.LOCALAPPDATA;
  const base = local && local.trim() ? local : path.join(os.homedir(), ".local", "share");
  return path.join(base, "xiyouji", "backups");
}

export interface BackupOptions {
  /** 源库路径（agent-web 的 data/chat.db） */
  dbPath: string;
  /** 审计日志路径（agent-web 的 data/audit.jsonl，可不存在） */
  auditPath?: string;
  /** 备份根目录（默认仓外） */
  backupDir?: string;
  /** 保留最近 N 份（默认 7） */
  keep?: number;
  /** 超过 N 天清理（默认 90） */
  maxAgeDays?: number;
  /** 是否真正执行（默认 true；false = dry-run 只报告） */
  execute?: boolean;
}

export interface BackupResult {
  ok: boolean;
  /** 今日快照已存在而跳过 */
  skipped?: boolean;
  /** 生成的快照文件 */
  snapshot?: string;
  /** 审计日志副本 */
  auditCopy?: string;
  /** 清理掉的旧文件 */
  pruned?: string[];
  /** 失败原因（ok=false 时） */
  error?: string;
}

function dateStamp(d = new Date()): string {
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}`;
}

/** 备份件年龄：文件名日期为主判据（chat-YYYYMMDD.db / audit-YYYYMMDD.jsonl），mtime 兜底。 */
function snapshotDate(f: string, fallbackMtimeMs: number): number {
  const m = /(\d{8})/.exec(f);
  if (m) {
    const t = Date.parse(`${m[1].slice(0, 4)}-${m[1].slice(4, 6)}-${m[1].slice(6, 8)}T00:00:00Z`);
    if (!Number.isNaN(t)) return t;
  }
  return fallbackMtimeMs;
}

/**
 * 保留策略：份数上限与超龄两个条件**独立**取并集。
 * （首跑缺陷：二者曾被错误嵌套成「仅在超出份数时才查超龄」，且幂等早退时整段不执行。）
 */
function prune(backupDir: string, keep: number, maxAgeDays: number): string[] {
  const cutoff = Date.now() - maxAgeDays * 24 * 3600 * 1000;
  const pruned: string[] = [];
  for (const [prefix, ext] of [
    ["chat-", ".db"],
    ["audit-", ".jsonl"],
  ] as const) {
    let files: string[] = [];
    try {
      files = fs.readdirSync(backupDir).filter((f) => f.startsWith(prefix) && f.endsWith(ext)).sort();
    } catch {
      continue;
    }
    const victims = new Set<string>();
    if (files.length > keep) {
      for (const f of files.slice(0, files.length - keep)) victims.add(f); // 超份数 → 删最旧
    }
    for (const f of files) {
      try {
        const st = fs.statSync(path.join(backupDir, f));
        if (snapshotDate(f, st.mtimeMs) < cutoff) victims.add(f); // 超龄 → 删（与份数条件独立）
      } catch {
        /* 单件 stat 失败不阻断整体 */
      }
    }
    for (const f of victims) {
      try {
        fs.unlinkSync(path.join(backupDir, f));
        pruned.push(f);
      } catch {
        /* 单件清理失败不阻断整体 */
      }
    }
  }
  return pruned;
}

/**
 * 执行一次快照。
 *
 * @param opts 备份参数
 */
export function runBackup(opts: BackupOptions): BackupResult {
  const backupDir = opts.backupDir ?? defaultBackupDir();
  const keep = opts.keep ?? 7;
  const maxAgeDays = opts.maxAgeDays ?? 90;
  const execute = opts.execute !== false;
  const stamp = dateStamp();
  const dbTarget = path.join(backupDir, `chat-${stamp}.db`);
  const auditTarget = path.join(backupDir, `audit-${stamp}.jsonl`);

  try {
    if (!fs.existsSync(opts.dbPath)) {
      return { ok: false, error: `源库不存在：${opts.dbPath}` };
    }

    // 幂等：今日快照已存在则跳过生成，**但仍执行保留策略**（prune 幂等无害）
    if (fs.existsSync(dbTarget)) {
      return { ok: true, skipped: true, snapshot: dbTarget, pruned: prune(backupDir, keep, maxAgeDays) };
    }

    if (!execute) {
      return { ok: true, snapshot: dbTarget, auditCopy: auditTarget };
    }

    fs.mkdirSync(backupDir, { recursive: true });

    // ① 会话库一致性快照：VACUUM INTO（非文件拷贝）
    //    源库以只读方式打开：VACUUM INTO 只写目标文件、不回写源库，故源库可只读。
    const src = new Database(opts.dbPath, { readonly: true, fileMustExist: true });
    try {
      src.prepare("VACUUM INTO ?").run(dbTarget);
    } finally {
      src.close();
    }

    // ② 审计日志副本（JSONL 追加式文本 → 直接拷贝）
    let auditCopy: string | undefined;
    if (opts.auditPath && fs.existsSync(opts.auditPath)) {
      fs.copyFileSync(opts.auditPath, auditTarget);
      auditCopy = auditTarget;
    }

    return { ok: true, snapshot: dbTarget, auditCopy, pruned: prune(backupDir, keep, maxAgeDays) };
  } catch (err) {
    return { ok: false, error: err instanceof Error ? err.message : String(err) };
  }
}

/**
 * 启动期调用入口：失败只记日志、绝不中断启动。
 *
 * @param dbPath 源库路径
 * @param auditPath 审计日志路径
 */
export function backupOnStartup(dbPath: string, auditPath?: string): void {
  if (process.env.NODE_ENV === "test") return; // 测试环境不产生快照
  const res = runBackup({ dbPath, auditPath });
  if (!res.ok) {
    logger.warn("会话库快照失败（不阻断启动）", { error: res.error });
    return;
  }
  if (res.skipped) {
    logger.info("会话库快照已存在（今日已备份）", { snapshot: res.snapshot, pruned: res.pruned });
    return;
  }
  logger.info("会话库快照完成", { snapshot: res.snapshot, auditCopy: res.auditCopy, pruned: res.pruned });
}
