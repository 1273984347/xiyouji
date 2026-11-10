/**
 * dualwrite-drill.ts — 双写期写入演练（W1204 · v2 §8.2 档 2 · D-2 第二子批）
 *
 * 为什么需要它：「切读 → 停写旧库」这条链路要有**可复跑的证据**，
 * 就必须能在当前写入模式下真实写入一组**可标记**的探针行，再由对账器读两侧比对。
 *
 * 职责边界（刻意做窄）：
 *  - 本器只负责「造数据 + 报读数」，**不做一致性判定**——
 *    判定只在对账器（reconcile-core.ts）里·只有一份实现·防两套判定漂移。
 *  - 探针行带 "__<tag>_" 前缀 ⇒ 可识别、可按主键清理、不会与真实业务数据混淆。
 *
 * 用法：
 *   node --import tsx deploy/pg/bin/dualwrite-drill.ts --tag w1204 [--json <path>]
 *
 * 写入模式决定探针落到哪里（这正是要观察的对象）：
 *  - primary + sqlite   ⇒ 只进 SQLite（停写旧库后的形态之一）
 *  - dual    + sqlite   ⇒ 进 SQLite 与 PG 两侧（双写期形态）
 *  - primary + postgres ⇒ 只进 PG（停写旧库后的目标形态）
 */
import { backend, backendKind, writeMode } from "../../../server/storage/index.js";

function argOf(name: string): string | undefined {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : undefined;
}

/** 探针标记：只允许字母数字与下划线⇒ 不会污染主键。 */
function sanitizeTag(raw: string): string {
  return raw.replace(/[^A-Za-z0-9_-]/g, "").slice(0, 40) || "probe";
}

async function main(): Promise<number> {
  const tag = sanitizeTag(argOf("--tag") || "w1204");
  const jsonPath = argOf("--json");
  const stamp = new Date().toISOString().replace(/[^0-9]/g, "").slice(0, 17);
  const sid = "__" + tag + "_s_" + stamp;
  const mid = "__" + tag + "_m_" + stamp;
  const fid = "__" + tag + "_f_" + stamp;
  const now = new Date().toISOString();

  const report: Record<string, unknown> = {
    generated_at: now,
    tag,
    backend: backendKind(),
    write_mode: writeMode(),
    probe: { session_id: sid, message_id: mid, feedback_id: fid },
  };

  try {
    await backend.createSession({
      id: sid,
      title: "__" + tag + "_session",
      model: "probe-model",
      sdk_session_id: null,
      created_at: now,
      updated_at: now,
    });
    await backend.createMessage({
      id: mid,
      session_id: sid,
      role: "user",
      content: "__" + tag + "_probe_message",
      model: "probe-model",
      tool_calls: null,
      created_at: now,
    });
    await backend.insertFeedback({
      id: fid,
      session_id: sid,
      message_id: mid,
      verdict: "up",
      comment: "__" + tag + "_probe_feedback",
    });
  } catch (err) {
    report.ok = false;
    report.error = err instanceof Error ? err.message : String(err);
    console.log(JSON.stringify(report, null, 2));
    console.error("写入失败（副库失败时双写层应当 fail-closed 抛错）：", report.error);
    return 1;
  }

  // 读回主库（读只走主库——这是双写层的约定）
  const back = await backend.getSession(sid);
  const msgs = await backend.getMessagesBySession(sid);
  report.ok = true;
  report.readback = {
    session_found: Boolean(back),
    session_updated_at: back ? back.updated_at : null,
    message_count: msgs.length,
  };

  console.log(JSON.stringify(report, null, 2));
  console.log(
    "写入演练完成：backend=" + report.backend + " write_mode=" + report.write_mode +
      " ⇒ 探针主键 " + sid,
  );
  if (jsonPath) {
    const fs = await import("node:fs");
    const path = await import("node:path");
    fs.mkdirSync(path.dirname(jsonPath), { recursive: true });
    fs.writeFileSync(jsonPath, JSON.stringify(report, null, 2), "utf-8");
    console.log("证据已写：" + jsonPath);
  }
  return 0;
}

main().then(
  (code) => process.exit(code),
  (err) => {
    console.error("演练失败：", err instanceof Error ? err.message : String(err));
    process.exit(1);
  },
);
