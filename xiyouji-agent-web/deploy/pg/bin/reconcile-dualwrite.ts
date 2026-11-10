/**
 * reconcile-dualwrite.ts — 双写期一致性对账器（W1204 · v2 §8.2 档 2 · D-2 第二子批）
 *
 * 用途：双写期（AGENT_WEB_DB_WRITE_MODE=dual）两侧必须逐集合一致，才允许切读、
 * 才允许停写旧库。本器给出可核对的数字，不是「看起来一样」。
 *
 * 为什么走数据源而不是业务接口：StorageBackend 没有「列出全部 messages / feedback」
 * 的读面（feedbackSummary 只给计数）⇒ 集合级对账必须直连两侧数据源（与 W934 迁移器同域）。
 * 判定核心在 server/storage/reconcile-core.ts（与数据源无关·只有一份实现·防两套判定漂移）。
 *
 * 用法：
 *   node --import tsx reconcile-dualwrite.ts --sqlite-a <path> --sqlite-b <path>
 *   node --import tsx reconcile-dualwrite.ts --sqlite <path> --pg <url>
 *   node --import tsx reconcile-dualwrite.ts --sqlite <path>          ← PG 配置走环境变量（**推荐**：口令不入命令行）
 *
 * 退出码：0 = 三重对账全等；1 = 存在差异（须先修差异再切读）；2 = 用法/连接错误。
 */
import Database from "better-sqlite3";
import { Pool } from "pg";
import { BUSINESS_TABLES, reconcileAll, type ReconcileResult, type TableSpec } from "../../../server/storage/reconcile-core.js";

function argOf(name: string): string | undefined {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : undefined;
}

/**
 * PG 连接配置（与 deploy/pg/bin/migrate-sqlite-to-pg.ts 同口径）。
 *
 * 为什么支持环境变量而**不只**支持 --pg <url>：URL 形态会把口令写进进程命令行
 * （同机任何进程都能从 /proc、任务管理器、审计日志里看到）⇒ 口令必须走环境变量。
 * 优先级：AGENT_WEB_PG_* → libpq 标准变量（PGHOST 等）→ 本机默认。
 * 口令**只**从环境变量读，任何输出都不含口令。
 */
function pgEnvConfig(): {
  host: string;
  port: number;
  user: string;
  password: string;
  database: string;
  ssl: boolean;
} {
  const num = (v: string | undefined, d: number) => {
    const n = Number(v);
    return Number.isFinite(n) && n > 0 ? n : d;
  };
  return {
    host: process.env.AGENT_WEB_PG_HOST || process.env.PGHOST || "127.0.0.1",
    port: num(process.env.AGENT_WEB_PG_PORT || process.env.PGPORT, 5432),
    user: process.env.AGENT_WEB_PG_USER || process.env.PGUSER || "postgres",
    password: process.env.AGENT_WEB_PG_PASSWORD || process.env.PGPASSWORD || "",
    database: process.env.AGENT_WEB_PG_DATABASE || process.env.PGDATABASE || "xiyouji",
    ssl: (process.env.AGENT_WEB_PG_SSL || "disable").toLowerCase() === "require",
  };
}

/** 环境变量里是否给出了足够的 PG 配置（省略 --pg 时的判据）。 */
function hasPgEnv(): boolean {
  return Boolean(
    process.env.AGENT_WEB_PG_HOST ||
      process.env.PGHOST ||
      process.env.AGENT_WEB_PG_DATABASE ||
      process.env.PGDATABASE,
  );
}

/** PG 连接的**脱敏**描述（host:port/db（user=…））—— 可安全写进证据与日志。 */
function pgDescribe(cfg: ReturnType<typeof pgEnvConfig>): string {
  return `${cfg.host}:${cfg.port}/${cfg.database}（user=${cfg.user}·ssl=${cfg.ssl ? "require" : "disable"}）`;
}

function readSqliteAll(dbPath: string, spec: TableSpec): Array<Record<string, unknown>> {
  const db = new Database(dbPath, { readonly: true });
  try {
    return db.prepare("SELECT " + spec.cols.join(", ") + " FROM " + spec.name).all() as Array<Record<string, unknown>>;
  } finally {
    db.close();
  }
}

async function readPgAll(pool: Pool, spec: TableSpec): Promise<Array<Record<string, unknown>>> {
  const res = await pool.query("SELECT " + spec.cols.join(", ") + " FROM " + spec.name);
  return res.rows as Array<Record<string, unknown>>;
}

async function main(): Promise<number> {
  const sqliteA = argOf("--sqlite-a");
  const sqliteB = argOf("--sqlite-b");
  const sqliteOnly = argOf("--sqlite");
  const pgUrl = argOf("--pg");
  const results: ReconcileResult[] = [];
  let pool: Pool | null = null;
  try {
    if (sqliteA && sqliteB) {
      results.push(
        ...(await reconcileAll(
          BUSINESS_TABLES,
          async (spec) => readSqliteAll(sqliteA, spec),
          async (spec) => readSqliteAll(sqliteB, spec),
        )),
      );
    } else if (sqliteOnly && (pgUrl || hasPgEnv())) {
      if (pgUrl) {
        pool = new Pool({ connectionString: pgUrl });
      } else {
        const cfg = pgEnvConfig();
        pool = new Pool(cfg);
        console.log("PG 目标（环境变量口径·口令不在命令行）：" + pgDescribe(cfg));
      }
      results.push(
        ...(await reconcileAll(
          BUSINESS_TABLES,
          async (spec) => readSqliteAll(sqliteOnly, spec),
          async (spec) => readPgAll(pool as Pool, spec),
        )),
      );
    } else {
      console.error(
        "用法：--sqlite-a <p> --sqlite-b <p>  或  --sqlite <p> --pg <url>\n" +
          "      （--pg 省略时改从环境变量读 PG 配置：AGENT_WEB_PG_* / PGHOST·PGPORT·PGUSER·PGPASSWORD·PGDATABASE）",
      );
      return 2;
    }
  } catch (err) {
    console.error("对账执行失败：", err);
    return 2;
  } finally {
    if (pool) await pool.end();
  }
  console.log("双写期对账（三重：行数 + 主键集合 + 逐行内容摘要）：");
  for (const r of results) {
    console.log(
      "  " + r.table + "：行数 " + r.source_rows + "/" + r.target_rows + " " + (r.rows_equal ? "OK" : "不等") +
      " · 主键集合 " + (r.pk_sets_equal ? "OK" : "不等") +
      " · 内容 " + (r.content_equal ? "OK" : "不等") +
      " · 时间列逐字节 " + r.timestamp_raw_equal_sampled + "/" + r.timestamp_raw_equal_total,
    );
    if (r.pk_only_in_source.length) console.log("    仅在源侧主键：" + r.pk_only_in_source.join(", "));
    if (r.pk_only_in_target.length) console.log("    仅在目标侧主键：" + r.pk_only_in_target.join(", "));
    for (const m of r.content_mismatch_sample) {
      console.log("    内容不一致 pk=" + m.pk + " src=" + m.source.slice(0, 16) + " tgt=" + m.target.slice(0, 16));
    }
  }
  const allEqual = results.every((r) => r.rows_equal && r.pk_sets_equal && r.content_equal);
  console.log(allEqual ? "结论：两侧一致（可切读；差异为 0 时方可停写旧库）" : "结论：存在差异（不可切读）");
  return allEqual ? 0 : 1;
}

main().then((code) => process.exit(code));
