/**
 * encryption.ts — 列级加密（应用层 · W1205 · D-3 合规批 · 架构方案 v2 §12.4）
 *
 * 方案 §12.4「PG 静态数据 · L3/L4 列级加密 · 实现方式：应用层加密（密钥不入库）」。
 * 本模块是该口径的**唯一实现**（SQLite 与 PG 两个后端共用——同源同码 ⇒ 语义一致）。
 *
 * 四条硬纪律：
 *  1) **密钥不入库、不落盘、不进日志**——只从环境变量读（AGENT_WEB_DATA_KEY）；
 *  2) **错误不泄露明文**——解密失败只报「密钥不匹配或密文被篡改」，不带明文/密文；
 *  3) **AAD 绑列**——密文与 (表.列) 绑定 ⇒ 密文被搬到别的列解不开（防列间搬运）；
 *  4) **幂等**——已加密的值再过一次不二次加密（双写期两侧必须拿到**同一份**密文，
 *     否则对账器会判「内容不等」⇒ 切读被永久阻断）。
 *
 * 为什么用 GCM 而不是 CBC：GCM 带认证标签 ⇒ 密文被篡改会解密失败（而不是解出垃圾）。
 *
 * 为什么 SQLite 侧也做：§12.4 的加密要求是**按数据级别**（L3/L4）而非按存储产品；
 * 单机部署的 SQLite 同样装着 L3 会话正文 ⇒ 不加密就是缺口。
 * 两个后端共用同一模块 ⇒ 不存在「PG 加密了、SQLite 没加密」的双标。
 */
import { randomBytes, createCipheriv, createDecipheriv } from "crypto";
import { ComplianceError, ComplianceErrorCode } from "../compliance/errors.js";
import { SENSITIVE_COLUMNS } from "../compliance/data-class.js";

/** 密文信封前缀（含版本号 ⇒ 将来换算法可并存解析）。 */
export const ENCRYPTION_PREFIX = "enc:v1:";

/** 密钥环境变量名（**只从环境变量读**）。 */
export const ENCRYPTION_KEY_ENV = "AGENT_WEB_DATA_KEY";

/** 密钥标识环境变量名（用于密钥轮换时区分版本；**不含密钥材料**）。 */
export const ENCRYPTION_KEY_ID_ENV = "AGENT_WEB_DATA_KEY_ID";

/** 密钥长度（AES-256 ⇒ 32 字节）。 */
export const ENCRYPTION_KEY_BYTES = 32;

/** 列级加密上下文（**只含密钥标识与密钥材料**；日志侧只能用 describeCipher）。 */
export interface ColumnCipher {
  /** 密钥标识（日志/错误里出现它是安全的）。 */
  keyId: string;
  /** 密钥材料（**禁进日志/禁落盘/禁进错误消息**）。 */
  key: Buffer;
}

/** 密文信封的字段顺序：enc:v1:<keyId>:<ivB64>:<tagB64>:<ctB64>（共 6 段）。 */
const ENVELOPE_PARTS = 6;

/**
 * 解析密钥材料（base64 或 64 位 hex ⇒ 32 字节）。
 *
 * 形态非法 ⇒ 抛 COMPLIANCE_ENCRYPTION_KEY_INVALID（**不回显原值**：回显等于把密钥写进日志）。
 */
export function parseEncryptionKeyMaterial(raw: string): Buffer {
  const text = raw.trim();
  if (text === "") {
    throw new ComplianceError(ComplianceErrorCode.ENCRYPTION_KEY_INVALID, "加密密钥为空");
  }
  let buf: Buffer | null = null;
  if (/^[0-9a-fA-F]{64}$/.test(text)) {
    buf = Buffer.from(text, "hex");
  } else {
    const decoded = Buffer.from(text, "base64");
    // base64 解码不严格：非法字符会被忽略 ⇒ 必须回读校验长度
    if (decoded.length === ENCRYPTION_KEY_BYTES) buf = decoded;
  }
  if (!buf || buf.length !== ENCRYPTION_KEY_BYTES) {
    throw new ComplianceError(
      ComplianceErrorCode.ENCRYPTION_KEY_INVALID,
      "加密密钥形态非法（须为 32 字节的 base64 或 hex）",
      { expectedBytes: ENCRYPTION_KEY_BYTES }
    );
  }
  return buf;
}

/**
 * 解析加密上下文（从环境变量）。
 *
 * 未配置 ⇒ 返回 null（**不加密**：保持现役单机形态逐字不变）。
 * 配置了但形态非法 ⇒ 抛错（fail-closed：配错了密钥却跑起来 ⇒ 数据「加密失败」而无人知晓）。
 */
export function resolveEncryptionKey(env: NodeJS.ProcessEnv = process.env): ColumnCipher | null {
  const raw = (env[ENCRYPTION_KEY_ENV] || "").trim();
  if (raw === "") return null;
  const keyId = (env[ENCRYPTION_KEY_ID_ENV] || "k1").trim() || "k1";
  if (keyId.includes(":")) {
    throw new ComplianceError(ComplianceErrorCode.ENCRYPTION_KEY_INVALID, "密钥标识非法（禁含冒号）");
  }
  return { keyId, key: parseEncryptionKeyMaterial(raw) };
}

/** 解析加密上下文（未配置 ⇒ 抛 COMPLIANCE_ENCRYPTION_KEY_MISSING）。 */
export function requireEncryptionKey(env: NodeJS.ProcessEnv = process.env): ColumnCipher {
  const cipher = resolveEncryptionKey(env);
  if (!cipher) {
    throw new ComplianceError(
      ComplianceErrorCode.ENCRYPTION_KEY_MISSING,
      "列级加密密钥缺失（L3/L4 落库要求加密）",
      { env: ENCRYPTION_KEY_ENV }
    );
  }
  return cipher;
}

/** 密钥上下文的安全描述（**只含密钥标识**·日志与错误里唯一允许出现的东西）。 */
export function describeCipher(cipher: ColumnCipher): string {
  return "keyId=" + cipher.keyId;
}

/** AAD（附加认证数据）：绑定表与列 ⇒ 密文不可跨列搬运。 */
export function columnAad(table: string, column: string): string {
  return table + "." + column;
}

/** 该值是不是密文信封。 */
export function isEncryptedValue(value: unknown): boolean {
  return typeof value === "string" && value.startsWith(ENCRYPTION_PREFIX);
}

/**
 * 加密一个列值（严格：不做幂等判断，调用方自行决定）。
 *
 * @param plaintext 明文（禁为空串以外的空值）
 * @param aad       绑定的列（columnAad(table, column)）
 * @param cipher    密钥上下文
 */
export function encryptColumn(plaintext: string, aad: string, cipher: ColumnCipher): string {
  if (typeof plaintext !== "string") {
    throw new ComplianceError(ComplianceErrorCode.ENCRYPTION_DECRYPT_FAILED, "待加密值不是字符串");
  }
  const iv = randomBytes(12);
  const enc = createCipheriv("aes-256-gcm", cipher.key, iv);
  enc.setAAD(Buffer.from(aad, "utf8"));
  const ct = Buffer.concat([enc.update(plaintext, "utf8"), enc.final()]);
  const tag = enc.getAuthTag();
  return [
    "enc",
    "v1",
    cipher.keyId,
    iv.toString("base64"),
    tag.toString("base64"),
    ct.toString("base64"),
  ].join(":");
}

/**
 * 解密一个列值（严格）。
 *
 * 失败（密钥不匹配 / 密文被篡改 / 信封残缺）⇒ 抛 COMPLIANCE_ENCRYPTION_DECRYPT_FAILED，
 * **错误消息与明细里不含明文、不含密文、不含密钥**。
 */
export function decryptColumn(value: string, aad: string, cipher: ColumnCipher): string {
  const parts = typeof value === "string" ? value.split(":") : [];
  if (parts.length !== ENVELOPE_PARTS || parts[0] !== "enc" || parts[1] !== "v1") {
    throw new ComplianceError(ComplianceErrorCode.ENCRYPTION_DECRYPT_FAILED, "密文信封残缺或格式非法");
  }
  try {
    const iv = Buffer.from(parts[3], "base64");
    const tag = Buffer.from(parts[4], "base64");
    const ct = Buffer.from(parts[5], "base64");
    const dec = createDecipheriv("aes-256-gcm", cipher.key, iv);
    dec.setAAD(Buffer.from(aad, "utf8"));
    dec.setAuthTag(tag);
    return Buffer.concat([dec.update(ct), dec.final()]).toString("utf8");
  } catch {
    // 关键：这里**不能**把原始值/明文拼进消息——那等于在日志里泄密
    throw new ComplianceError(
      ComplianceErrorCode.ENCRYPTION_DECRYPT_FAILED,
      "解密失败（密钥不匹配或密文被篡改）",
      { aad, keyId: cipher.keyId }
    );
  }
}

/**
 * 幂等加密（双写期两侧必须拿到**同一份**密文 ⇒ 已加密的值不再加密）。
 *
 * 未配置密钥 ⇒ 原样返回（保持现役形态）。
 */
export function maybeEncryptColumn(
  plaintext: string,
  aad: string,
  env: NodeJS.ProcessEnv = process.env
): string {
  if (isEncryptedValue(plaintext)) return plaintext;
  const cipher = resolveEncryptionKey(env);
  if (!cipher) return plaintext;
  return encryptColumn(plaintext, aad, cipher);
}

/**
 * 幂等解密。
 *
 *  - 未配置密钥且值不是信封 ⇒ 原样返回（存量明文行仍可读）；
 *  - 未配置密钥但值是信封 ⇒ 抛 ENCRYPTION_KEY_MISSING（**不能把密文当明文交出去**）；
 *  - 是信封且有密钥 ⇒ 解密（失败即抛，不返回任何明文）。
 */
export function maybeDecryptColumn(
  value: string,
  aad: string,
  env: NodeJS.ProcessEnv = process.env
): string {
  if (!isEncryptedValue(value)) return value;
  const cipher = resolveEncryptionKey(env);
  if (!cipher) {
    throw new ComplianceError(
      ComplianceErrorCode.ENCRYPTION_KEY_MISSING,
      "存量密文存在但加密密钥缺失（拒绝返回密文冒充明文）",
      { env: ENCRYPTION_KEY_ENV }
    );
  }
  return decryptColumn(value, aad, cipher);
}

/**
 * 按表加密敏感列（写路径用）。
 *
 * 只动 SENSITIVE_COLUMNS 里列出的列（L3 表的敏感列；L2 反馈表不加密）。
 * 未配置密钥 ⇒ 原样返回。
 */
export function encryptSensitiveColumns<T extends object>(
  row: T,
  table: string,
  env: NodeJS.ProcessEnv = process.env
): T {
  if (!resolveEncryptionKey(env)) return row;
  const cols = SENSITIVE_COLUMNS[table] || [];
  const out: Record<string, unknown> = { ...(row as Record<string, unknown>) };
  for (const col of cols) {
    const v = out[col];
    if (typeof v !== "string" || v === "") continue;
    // 幂等：已是信封的值原样保留（双写期两侧要拿到同一份密文）
    out[col] = maybeEncryptColumn(v, columnAad(table, col), env);
  }
  return out as T;
}

/**
 * 按表解密敏感列（读路径用）。
 *
 * 存量明文行原样返回（兼容加密启用前的数据）；信封值解密失败即抛。
 */
export function decryptSensitiveColumns<T extends object>(
  row: T,
  table: string,
  env: NodeJS.ProcessEnv = process.env
): T {
  if (!resolveEncryptionKey(env)) {
    // 无密钥：明文行原样返回；信封行抛错（见 maybeDecryptColumn 的口径）
    const cols = SENSITIVE_COLUMNS[table] || [];
    const rec = row as Record<string, unknown>;
    for (const col of cols) {
      if (isEncryptedValue(rec[col])) {
        maybeDecryptColumn(String(rec[col]), columnAad(table, col), env);
      }
    }
    return row;
  }
  const cols = SENSITIVE_COLUMNS[table] || [];
  const out: Record<string, unknown> = { ...(row as Record<string, unknown>) };
  for (const col of cols) {
    const v = out[col];
    if (typeof v !== "string" || v === "") continue;
    out[col] = maybeDecryptColumn(v, columnAad(table, col), env);
  }
  return out as T;
}
