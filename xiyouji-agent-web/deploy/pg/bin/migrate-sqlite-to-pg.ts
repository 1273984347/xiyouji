/**
 * migrate-sqlite-to-pg.ts — SQLite → PostgreSQL 数据迁移器 + 三重对账（W934 · D-2a）
 *
 * 用法：
 *   node --import tsx deploy/pg/bin/migrate-sqlite-to-pg.ts \
 *     --sqlite "D:\xiyouji\xiyouji-agent-web\data\chat.db" \
 *     --json "D:\xiyouji\scripts\output\_w934_d2a_migrate.json"
 *
 * 三段动作：
 *   ① 应用迁移序列（migrations/*.sql 按版本号升序·未记账的才执行·执行后记账）
 *   ② 迁移业务数据（sessions → messages → feedback·外键依赖序）
 *   ③ 三重对账（行数 + 主键集合 + 逐行内容摘要）
 *
 * 六条硬纪律：
 *  1. **源库只读**：`new Database(path, { readonly: true, fileMustExist: true })`。
 *     chat.db 是全仓唯一不可重建的数据（W844 批记）⇒ 迁移器绝不能写它。
 *  2. **不借道应用 API 写数据**：应用侧 `createMessage` 会顺手把会话的
 *     `updated_at` 刷成「现在」——那是**在线写入**的语义，迁移必须**逐字节保真**
 *     ⇒ 迁移器用参数化 SQL 直写，不走 `StorageBackend`。
 *     （后端本身能不能写对，由 `server/storage/storage.test.ts` 的契约测试另行证明。）
 *  3. **禁字符串拼接 SQL**：全部走 `$1/$2` 参数化。
 *  4. **口令不出现在任何输出**：错误信息只带 host/port/db/user。
 *  5. **不静默跳过脏数据**：时间值非法时**报错并指出行号与原值**，不悄悄修。
 *  6. **对账要比集合，不能只比计数**（决策 D-08）：行数相等但内容错位是**假对账**
 *     （删一行补一行仍相等）⇒ 三重对账逐项给出可核对的数字。
 */
import Database from "better-sqlite3";
import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Pool, type PoolClient } from "pg";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DEPLOY_ROOT = path.resolve(HERE, "..");
const MIGRATIONS_DIR = path.join(DEPLOY_ROOT, "migrations");

// ============= 参数 =============

interface Args {
  sqlite: string;
  json: string | null;
  skipMigrations: boolean;
  dryRun: boolean;
}

function parseArgs(argv: string[]): Args {
  const get = (flag: string): string | null => {
    const i = argv.indexOf(flag);
    return i >= 0 && argv[i + 1] ? argv[i + 1] : null;
  };
  return {
    sqlite: get("--sqlite") ?? path.resolve(process.cwd(), "data", "chat.db"),
    json: get("--json"),
    skipMigrations: argv.includes("--skip-migrations"),
    dryRun: argv.includes("--dry-run"),
  };
}

/** PG 连接配置（与 server/storage/postgres.ts 同口径·口令只从环境变量取）。 */
function pgConfig() {
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
  };
}

// ============= 小工具 =============

function sha256(text: string): string {
  // 用 node:crypto 的真 sha256（迁移记账的 checksum 字段语义要求标准摘要·
  // 自制哈希会让「摘要」不可与其它工具交叉校验）
  return createHash("sha256").update(text, "utf-8").digest("hex");
}

/** ISO 时间串 → Date；非法则抛错并带定位（纪律 5）。 */
function mustDate(iso: unknown, where: string): Date {
  const s = String(iso);
  const d = new Date(s);
  if (Number.isNaN(d.getTime())) {
    throw new Error(`时间值非法（${where}）：${JSON.stringify(s)}`);
  }
  return d;
}

/** 任意可解析的时间值 → 规范 ISO 字符串（用于对账）。 */
function normIso(v: unknown): string {
  if (v instanceof Date) return v.toISOString();
  const d = new Date(String(v));
  return Number.isNaN(d.getTime()) ? `INVALID(${String(v)})` : d.toISOString();
}

/** 源库行 → 规范化的可比形态（时间列转 ISO·其余原样）。 */
function canon(row: Record<string, unknown>, timeCols: string[]): string {
  const out: Record<string, unknown> = {};
  for (const k of Object.keys(row).sort()) {
    const v = row[k];
    out[k] = timeCols.includes(k) ? normIso(v) : v === null || v === undefined ? null : String(v);
  }
  return JSON.stringify(out);
}

// ============= 迁移序列 =============

interface MigrationFile {
  version: number;
  name: string;
  file: string;
  sql: string;
  checksum: string;
}

function loadMigrations(): MigrationFile[] {
  const files = fs
    .readdirSync(MIGRATIONS_DIR)
    .filter((f) => /^\d{4}_.*\.sql$/.test(f))
    .sort();
  return files.map((f) => {
    const version = Number(f.slice(0, 4));
    const sql = fs.readFileSync(path.join(MIGRATIONS_DIR, f), "utf-8");
    return { version, name: f.replace(/\.sql$/, ""), file: f, sql, checksum: sha256(sql) };
  });
}

/** 应用迁移序列（未记账的才执行）。 */
async function applyMigrations(pool: Pool, dryRun: boolean): Promise<Array<Record<string, unknown>>> {
  const out: Array<Record<string, unknown>> = [];
  const client = await pool.connect();
  try {
    const hasTable = await client.query(
      `SELECT to_regclass('public.schema_migrations') IS NOT NULL AS present`
    );
    const present = hasTable.rows[0]?.present === true;
    const applied = new Set<number>();
    if (present) {
      const r = await client.query("SELECT version FROM schema_migrations");
      for (const row of r.rows) applied.add(Number(row.version));
    }

    for (const m of loadMigrations()) {
      if (applied.has(m.version)) {
        out.push({ version: m.version, name: m.name, action: "skipped(已记账)" });
        continue;
      }
      if (dryRun) {
        out.push({ version: m.version, name: m.name, action: "dry-run(未执行)" });
        continue;
      }
      // 迁移文件自带 BEGIN/COMMIT（单事务语义）⇒ 用**无参数**的多语句查询执行
      await client.query(m.sql);
      await client.query(
        `INSERT INTO schema_migrations (version, name, checksum) VALUES ($1, $2, $3)
         ON CONFLICT (version) DO UPDATE SET name = EXCLUDED.name, checksum = EXCLUDED.checksum`,
        [m.version, m.name, m.checksum]
      );
      out.push({ version: m.version, name: m.name, action: "applied", checksum: m.checksum });
    }
  } finally {
    client.release();
  }
  return out;
}

// ============= 数据迁移 =============

interface TableSpec {
  name: string;
  pk: string;
  timeCols: string[];
  cols: string[];
  selectSql: string;
  /** PG 侧读回语句（**写死的静态 SQL**——不拼表名/列名，标识符插值一律不用）。 */
  targetSelectSql: string;
  /** PG 侧写入语句（静态 SQL + 固定占位符个数）。 */
  targetInsertSql: string;
}

const TABLES: TableSpec[] = [
  {
    name: "sessions",
    pk: "id",
    timeCols: ["created_at", "updated_at"],
    cols: ["id", "title", "model", "sdk_session_id", "created_at", "updated_at"],
    selectSql: "SELECT id, title, model, sdk_session_id, created_at, updated_at FROM sessions",
    targetSelectSql:
      "SELECT id, title, model, sdk_session_id, created_at, updated_at FROM sessions",
    targetInsertSql: `INSERT INTO sessions (id, title, model, sdk_session_id, created_at, updated_at)
                VALUES ($1,$2,$3,$4,$5,$6) ON CONFLICT (id) DO NOTHING`,
  },
  {
    name: "messages",
    pk: "id",
    timeCols: ["created_at"],
    cols: ["id", "session_id", "role", "content", "model", "created_at", "tool_calls"],
    selectSql:
      "SELECT id, session_id, role, content, model, created_at, tool_calls FROM messages",
    targetSelectSql:
      "SELECT id, session_id, role, content, model, created_at, tool_calls FROM messages",
    targetInsertSql: `INSERT INTO messages (id, session_id, role, content, model, created_at, tool_calls)
                VALUES ($1,$2,$3,$4,$5,$6,$7) ON CONFLICT (id) DO NOTHING`,
  },
  {
    name: "feedback",
    pk: "id",
    timeCols: ["created_at"],
    cols: ["id", "session_id", "message_id", "verdict", "comment", "created_at"],
    selectSql:
      "SELECT id, session_id, message_id, verdict, comment, created_at FROM feedback",
    targetSelectSql:
      "SELECT id, session_id, message_id, verdict, comment, created_at FROM feedback",
    targetInsertSql: `INSERT INTO feedback (id, session_id, message_id, verdict, comment, created_at)
                VALUES ($1,$2,$3,$4,$5,$6) ON CONFLICT (id) DO NOTHING`,
  },
];

/** 源库（SQLite·只读）取数。 */
function readSource(sqlitePath: string): Map<string, Array<Record<string, unknown>>> {
  const db = new Database(sqlitePath, { readonly: true, fileMustExist: true });
  try {
    const map = new Map<string, Array<Record<string, unknown>>>();
    for (const t of TABLES) {
      const rows = db.prepare(t.selectSql).all() as Array<Record<string, unknown>>;
      map.set(t.name, rows);
    }
    return map;
  } finally {
    db.close();
  }
}

/** 目标库（PG）取数（静态 SQL·不拼标识符）。 */
async function readTarget(
  client: PoolClient,
  t: TableSpec
): Promise<Array<Record<string, unknown>>> {
  const { rows } = await client.query(t.targetSelectSql);
  return rows as Array<Record<string, unknown>>;
}

/** 写入目标库（参数化·禁拼接）。 */
async function writeTarget(
  client: PoolClient,
  t: TableSpec,
  rows: Array<Record<string, unknown>>
): Promise<number> {
  let n = 0;
  for (const row of rows) {
    const vals: unknown[] = [];
    for (const c of t.cols) {
      const v = row[c];
      vals.push(t.timeCols.includes(c) ? mustDate(v, `${t.name}.${c}`) : v ?? null);
    }
    // 幂等：同主键已存在则跳过（重跑迁移器不产生重复行）
    // 语句是**静态 SQL + 全占位符**（连 ON CONFLICT 目标列都写死在语句里）
    const res = await client.query(t.targetInsertSql, vals);
    n += res.rowCount ?? 0;
  }
  return n;
}

// ============= 对账 =============

interface ReconcileResult {
  table: string;
  source_rows: number;
  target_rows: number;
  rows_equal: boolean;
  pk_sets_equal: boolean;
  content_equal: boolean;
  pk_only_in_source: string[];
  pk_only_in_target: string[];
  content_mismatch_sample: Array<{ pk: string; source: string; target: string }>;
  /** 逐字节时间串相等的抽样数（AC-07） */
  timestamp_raw_equal_sampled: number;
  timestamp_raw_equal_total: number;
}

async function reconcile(
  client: PoolClient,
  t: TableSpec,
  sourceRows: Array<Record<string, unknown>>
): Promise<ReconcileResult> {
  const targetRows = await readTarget(client, t);

  const srcMap = new Map<string, Record<string, unknown>>();
  for (const r of sourceRows) srcMap.set(String(r[t.pk]), r);
  const tgtMap = new Map<string, Record<string, unknown>>();
  for (const r of targetRows) tgtMap.set(String(r[t.pk]), r);

  const srcPks = [...srcMap.keys()].sort();
  const tgtPks = [...tgtMap.keys()].sort();
  const pkOnlyInSource = srcPks.filter((k) => !tgtMap.has(k));
  const pkOnlyInTarget = tgtPks.filter((k) => !srcMap.has(k));
  const pkSetsEqual =
    pkOnlyInSource.length === 0 && pkOnlyInTarget.length === 0 && srcPks.length === tgtPks.length;

  // 逐行内容比对（时间列走规范化 ISO⇒比的是「同一时刻」而非「同一串」）
  const contentMismatches: Array<{ pk: string; source: string; target: string }> = [];
  let tsRawEqual = 0;
  let tsRawTotal = 0;
  for (const pk of srcPks) {
    const s = srcMap.get(pk)!;
    const g = tgtMap.get(pk);
    if (!g) continue;
    const sc = canon(s, t.timeCols);
    const gc = canon(g, t.timeCols);
    if (sc !== gc && contentMismatches.length < 10) {
      contentMismatches.push({ pk, source: sc, target: gc });
    }
    // 逐字节时间串比对（AC-07）：源库原串 vs 目标侧 toISOString()
    for (const tc of t.timeCols) {
      tsRawTotal++;
      if (String(s[tc]) === normIso(g[tc])) tsRawEqual++;
    }
  }
  const contentEqual = contentMismatches.length === 0;

  return {
    table: t.name,
    source_rows: sourceRows.length,
    target_rows: targetRows.length,
    rows_equal: sourceRows.length === targetRows.length,
    pk_sets_equal: pkSetsEqual,
    content_equal: contentEqual,
    pk_only_in_source: pkOnlyInSource.slice(0, 20),
    pk_only_in_target: pkOnlyInTarget.slice(0, 20),
    content_mismatch_sample: contentMismatches,
    timestamp_raw_equal_sampled: tsRawEqual,
    timestamp_raw_equal_total: tsRawTotal,
  };
}

// ============= 主流程 =============

async function main(): Promise<number> {
  const args = parseArgs(process.argv.slice(2));
  const cfg = pgConfig();
  const target = `${cfg.host}:${cfg.port}/${cfg.database}（user=${cfg.user}）`;

  if (!fs.existsSync(args.sqlite)) {
    console.error(`FAIL 源库不存在：${args.sqlite}`);
    return 1;
  }
  console.log(`== SQLite → PostgreSQL 迁移（W934 · D-2a）==`);
  console.log(`源库（只读）：${args.sqlite}`);
  console.log(`目标库：${target}`);

  const source = readSource(args.sqlite);
  for (const t of TABLES) {
    console.log(`  源表 ${t.name}：${source.get(t.name)!.length} 行`);
  }

  const pool = new Pool({
    host: cfg.host,
    port: cfg.port,
    user: cfg.user,
    password: cfg.password,
    database: cfg.database,
    max: 4,
    connectionTimeoutMillis: 10_000,
  });

  const report: Record<string, unknown> = {
    generated_at: new Date().toISOString(),
    source_sqlite: args.sqlite,
    target: target,
    dry_run: args.dryRun,
  };

  try {
    // ① 迁移序列
    if (args.skipMigrations) {
      report.migrations = [];
      console.log("① 迁移序列：已按 --skip-migrations 跳过");
    } else {
      const mig = await applyMigrations(pool, args.dryRun);
      report.migrations = mig;
      console.log("① 迁移序列：");
      for (const m of mig) console.log(`   v${m.version} ${m.name} → ${m.action}`);
    }

    // ② 数据迁移
    const written: Record<string, number> = {};
    if (args.dryRun) {
      for (const t of TABLES) written[t.name] = 0;
      console.log("② 数据迁移：dry-run（未写入）");
    } else {
      const client = await pool.connect();
      try {
        await client.query("BEGIN");
        for (const t of TABLES) {
          const n = await writeTarget(client, t, source.get(t.name)!);
          written[t.name] = n;
        }
        await client.query("COMMIT");
      } catch (err) {
        await client.query("ROLLBACK").catch(() => undefined);
        throw err;
      } finally {
        client.release();
      }
      report.written = written;
      console.log("② 数据迁移：" + Object.entries(written).map(([k, v]) => `${k}=${v}`).join(" · "));
    }

    // ③ 三重对账
    const client = await pool.connect();
    try {
      const rec: ReconcileResult[] = [];
      for (const t of TABLES) rec.push(await reconcile(client, t, source.get(t.name)!));
      report.reconciliation = rec;
      console.log("③ 对账：");
      for (const r of rec) {
        console.log(
          `   ${r.table}：行数 ${r.source_rows}→${r.target_rows} ${r.rows_equal ? "OK" : "不等"} · ` +
            `主键集合 ${r.pk_sets_equal ? "OK" : "不等"} · 内容 ${r.content_equal ? "OK" : "不等"} · ` +
            `时间串逐字节 ${r.timestamp_raw_equal_sampled}/${r.timestamp_raw_equal_total}`
        );
        for (const m of r.content_mismatch_sample) {
          console.log(`      ! ${r.table}[${m.pk}] 源=${m.source}`);
          console.log(`        ${" ".repeat(r.table.length + 3)}目标=${m.target}`);
        }
      }
    } finally {
      client.release();
    }
  } finally {
    await pool.end();
  }

  const rec = report.reconciliation as ReconcileResult[] | undefined;
  const allOk = rec ? rec.every((r) => r.rows_equal && r.pk_sets_equal && r.content_equal) : false;
  report.all_equal = allOk;
  console.log(allOk ? "== 对账全部一致 ==" : "== 对账存在差异（见上） ==");

  if (args.json) {
    fs.mkdirSync(path.dirname(args.json), { recursive: true });
    fs.writeFileSync(args.json, JSON.stringify(report, null, 2), "utf-8");
    console.log(`证据已写：${args.json}`);
  }

  return allOk ? 0 : 2;
}

main().then(
  (code) => process.exit(code),
  (err) => {
    console.error("FAIL 迁移失败：", err instanceof Error ? err.message : String(err));
    process.exit(1);
  }
);
