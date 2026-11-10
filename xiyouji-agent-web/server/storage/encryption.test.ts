/**
 * encryption.test.ts — 列级加密单测（W1205 · D-3 合规批 · §12.4）
 *
 * 覆盖七条：
 *  ① 往返一致且**密文不含明文**；
 *  ② 用错误密钥读出 ⇒ 失败且**不泄露明文**；
 *  ③ AAD 绑列（密文搬到别的列解不开）；
 *  ④ **密钥不入库、不落盘、不进日志**；
 *  ⑤ 存储层：明文**落库前已加密**，读回仍是明文；
 *  ⑥ 幂等（已加密的值不二次加密——双写期两侧要同一份密文）；
 *  ⑦ 未配置密钥 ⇒ 明文落库（现役形态逐字不变）。
 *
 * 运行：cd xiyouji-agent-web && node --import tsx --test server/storage/encryption.test.ts
 */
import { test } from "node:test";
import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import Database from "better-sqlite3";
import { createSqliteBackend } from "./sqlite.js";
import {
  ENCRYPTION_PREFIX,
  columnAad,
  decryptColumn,
  describeCipher,
  encryptColumn,
  isEncryptedValue,
  maybeDecryptColumn,
  maybeEncryptColumn,
  parseEncryptionKeyMaterial,
  requireEncryptionKey,
  resolveEncryptionKey,
} from "./encryption.js";
import { ComplianceError, ComplianceErrorCode, isComplianceError } from "../compliance/errors.js";

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "xiyouji-encryption-test-"));

/** 测试密钥材料（造值·非真实凭据）。 */
const KEY_MATERIAL = Buffer.alloc(32, 9).toString("base64");
const OTHER_KEY_MATERIAL = Buffer.alloc(32, 4).toString("base64");
const CIPHER = { keyId: "k-test", key: parseEncryptionKeyMaterial(KEY_MATERIAL) };
const OTHER_CIPHER = { keyId: "k-other", key: parseEncryptionKeyMaterial(OTHER_KEY_MATERIAL) };

const SECRET = "这是不该落盘的机密正文·机密正文";

test("X1 往返一致：密文不含明文，解密回原文", () => {
  const aad = columnAad("messages", "content");
  const env = { content: SECRET };
  const ct = encryptColumn(SECRET, aad, CIPHER);
  assert.ok(ct.startsWith(ENCRYPTION_PREFIX), "密文应带信封前缀");
  assert.ok(isEncryptedValue(ct));
  assert.equal(ct.includes(SECRET), false, "密文不得含明文");
  assert.equal(decryptColumn(ct, aad, CIPHER), SECRET, "解密应还原原文");
  assert.equal(env.content, SECRET, "原串不被就地改写");
});

test("X2 错误密钥 ⇒ 解密失败且不泄露明文", () => {
  const aad = columnAad("messages", "content");
  const ct = encryptColumn(SECRET, aad, CIPHER);
  assert.throws(
    () => decryptColumn(ct, aad, OTHER_CIPHER),
    (err: unknown) => {
      assert.ok(isComplianceError(err), "应为 ComplianceError");
      assert.equal(err.code, ComplianceErrorCode.ENCRYPTION_DECRYPT_FAILED);
      const text = err.message + " " + JSON.stringify(err.detail);
      assert.equal(text.includes(SECRET), false, "错误消息不得含明文");
      assert.equal(text.includes(ct), false, "错误消息不得含密文");
      assert.equal(text.includes(KEY_MATERIAL), false, "错误消息不得含密钥");
      return true;
    },
  );
});

test("X3 AAD 绑列：密文搬到别的列解不开", () => {
  const ct = encryptColumn(SECRET, columnAad("messages", "content"), CIPHER);
  assert.throws(
    () => decryptColumn(ct, columnAad("messages", "tool_calls"), CIPHER),
    (err: unknown) => isComplianceError(err) && err.code === ComplianceErrorCode.ENCRYPTION_DECRYPT_FAILED,
    "跨列解密必须失败",
  );
});

test("X4 密钥解析：未配置⇒null；形态非法⇒拒绝（不回显原值）；密钥标识可查", () => {
  assert.equal(resolveEncryptionKey({} as NodeJS.ProcessEnv), null, "未配置密钥⇒不加密（现役形态不变）");
  assert.equal(resolveEncryptionKey({ [ "AGENT_WEB_DATA_KEY" ]: KEY_MATERIAL } as NodeJS.ProcessEnv)?.keyId, "k1");
  assert.throws(
    () => parseEncryptionKeyMaterial("not-a-key"),
    (err: unknown) => {
      assert.ok(isComplianceError(err));
      assert.equal(err.code, ComplianceErrorCode.ENCRYPTION_KEY_INVALID);
      assert.equal(err.message.includes("not-a-key"), false, "非法密钥不得回显");
      return true;
    },
  );
  assert.throws(
    () => requireEncryptionKey({} as NodeJS.ProcessEnv),
    (err: unknown) => isComplianceError(err) && err.code === ComplianceErrorCode.ENCRYPTION_KEY_MISSING,
  );
  assert.equal(describeCipher(CIPHER), "keyId=k-test", "日志里只允许出现密钥标识");
  assert.equal(describeCipher(CIPHER).includes(KEY_MATERIAL), false);
});

test("X5 幂等：已加密的值不二次加密（双写期两侧必须同一份密文）", () => {
  const env = { AGENT_WEB_DATA_KEY: KEY_MATERIAL } as NodeJS.ProcessEnv;
  const aad = columnAad("messages", "content");
  const once = maybeEncryptColumn(SECRET, aad, env);
  const twice = maybeEncryptColumn(once, aad, env);
  assert.equal(twice, once, "二次加密必须原样返回");
  assert.equal(maybeDecryptColumn(once, aad, env), SECRET);
  // 存量明文行仍可读（不因启用加密而读不出历史数据）
  assert.equal(maybeDecryptColumn(SECRET, aad, env), SECRET, "存量明文原样返回");
});

test("X6 存储层：明文落库前已加密 · 读回仍是明文 · 密钥与明文都不在库文件里", async () => {
  const prevKey = process.env.AGENT_WEB_DATA_KEY;
  process.env.AGENT_WEB_DATA_KEY = KEY_MATERIAL;
  const dbPath = path.join(TMP, "enc-" + Date.now() + ".db");
  const backend = createSqliteBackend(dbPath);
  const now = "2026-03-04T05:06:07.000Z";
  try {
    await backend.createSession({
      id: "s-enc",
      title: "机密会话标题",
      model: "m",
      sdk_session_id: null,
      created_at: now,
      updated_at: now,
      data_class: "L3",
    });
    await backend.createMessage({
      id: "m-enc",
      session_id: "s-enc",
      role: "user",
      content: SECRET,
      model: null,
      created_at: now,
      tool_calls: null,
      data_class: "L3",
    });

    // 直读底层库（绕开应用层）⇒ 落库值必须是密文
    const raw = new Database(dbPath, { readonly: true });
    let rawContent = "";
    let rawTitle = "";
    try {
      rawContent = String((raw.prepare("SELECT content FROM messages WHERE id = ?").get("m-enc") as { content: string }).content);
      rawTitle = String((raw.prepare("SELECT title FROM sessions WHERE id = ?").get("s-enc") as { title: string }).title);
    } finally {
      raw.close();
    }
    assert.ok(rawContent.startsWith(ENCRYPTION_PREFIX), "消息正文落库前必须已加密");
    assert.ok(rawTitle.startsWith(ENCRYPTION_PREFIX), "会话标题（L3 敏感列）落库前必须已加密");
    assert.equal(rawContent.includes(SECRET), false, "落库值不得含明文");

    // 应用层读回 ⇒ 仍是明文（业务不受影响）
    const msg = await backend.getMessagesBySession("s-enc");
    assert.equal(msg.length, 1);
    assert.equal(msg[0].content, SECRET, "读回必须解密成明文");
    const sess = await backend.getSession("s-enc");
    assert.equal(sess?.title, "机密会话标题", "会话标题读回必须解密");

    // 密钥与明文都不得出现在库文件（含 WAL）里
    for (const suffix of ["", "-wal"]) {
      const f = dbPath + suffix;
      if (!fs.existsSync(f)) continue;
      const bytes = fs.readFileSync(f);
      assert.equal(bytes.includes(Buffer.from(SECRET, "utf8")), false, "库文件不得含明文（" + suffix + "）");
      assert.equal(bytes.includes(Buffer.from(KEY_MATERIAL, "utf8")), false, "库文件不得含密钥（" + suffix + "）");
      assert.equal(bytes.includes(CIPHER.key), false, "库文件不得含密钥材料（" + suffix + "）");
    }
  } finally {
    await backend.close();
    if (prevKey === undefined) delete process.env.AGENT_WEB_DATA_KEY;
    else process.env.AGENT_WEB_DATA_KEY = prevKey;
  }
});

test("X7 未配置密钥 ⇒ 明文落库（现役形态逐字不变）", async () => {
  const prevKey = process.env.AGENT_WEB_DATA_KEY;
  delete process.env.AGENT_WEB_DATA_KEY;
  const dbPath = path.join(TMP, "plain-" + Date.now() + ".db");
  const backend = createSqliteBackend(dbPath);
  const now = "2026-03-04T05:06:07.000Z";
  try {
    await backend.createSession({
      id: "s-plain",
      title: "明文会话",
      model: "m",
      sdk_session_id: null,
      created_at: now,
      updated_at: now,
      data_class: "L3",
    });
    await backend.createMessage({
      id: "m-plain",
      session_id: "s-plain",
      role: "user",
      content: SECRET,
      model: null,
      created_at: now,
      tool_calls: null,
      data_class: "L3",
    });
    const raw = new Database(dbPath, { readonly: true });
    let rawContent = "";
    try {
      rawContent = String((raw.prepare("SELECT content FROM messages WHERE id = ?").get("m-plain") as { content: string }).content);
    } finally {
      raw.close();
    }
    assert.equal(rawContent, SECRET, "未配密钥时不加密（现役形态不变）");
  } finally {
    await backend.close();
    if (prevKey === undefined) delete process.env.AGENT_WEB_DATA_KEY;
    else process.env.AGENT_WEB_DATA_KEY = prevKey;
  }
});
