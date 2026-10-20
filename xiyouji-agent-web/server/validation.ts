/**
 * validation.ts — 请求体边界校验（W808 新建）
 *
 * 职责边界：定义各 /api 端点的入参 schema，并提供「校验 → 抛类型化错误」的统一出口。
 * **不碰业务语义**（校验通过后该怎么处理由路由层决定）。
 *
 * 动因（W808）：重构前各路由用手写 `typeof` 判据散落校验（如 routes.ts 的
 * `typeof sessionId !== "string" || …`），判据不统一、越界值（超长字符串、
 * 非法枚举、错误类型数组）不被拦截。本层以 Zod 统一表达「什么形状才算合法」。
 *
 * 三条纪律：
 *   ① **零信任**——所有外部入参一律经本层；schema 未知字段默认剥离（strip），
 *      防「塞进本该忽略的字段」这类隐式契约漂移；
 *   ② **失败即类型化**——校验不通过抛 ValidationError（422），由全局错误处理器
 *      统一序列化（不再由各路由手写 400 分支）；
 *   ③ **不泄内部**——Zod 的原始 issue 会被归一为「字段路径 + 可读文案」，
 *      原始错误对象不直接返回给客户端。
 */
import { z } from "zod";
import { ValidationError } from "./errors.js";

/** 校验失败时的对外表现（状态码 + 文案）——供各端点对齐其**既有契约**。 */
export interface ValidationFailure {
  /** HTTP 状态码。 */
  statusCode: number;
  /** 响应体 `error` 字段的文案。 */
  message: string;
}

/**
 * 把 Zod 的 issue 列表归一为 `{ path, message }`（前端可定位到表单项）。
 *
 * 路径拼接规则：`a.b[0].c` 形态（与前端表单字段路径一致）。
 */
function toFieldErrors(error: z.ZodError): Array<{ path: string; message: string }> {
  return error.issues.map((issue) => {
    const path = issue.path
      .map((seg) => (typeof seg === "number" ? `[${seg}]` : seg))
      .join(".")
      .replace(/\.\[/g, "[");
    return { path, message: issue.message };
  });
}

/**
 * 校验请求体：通过则返回**类型收窄后**的数据（不再是 unknown），失败抛 ValidationError。
 *
 * @param schema 目标 schema
 * @param body 待校验的请求体（外部输入，不可信）
 * @param failure 可选——失败时的对外表现（状态码 + 文案）。
 *   **缺省为 422 + 明细**；但若该端点已有**文档化的既有契约**（如 /api/feedback 的
 *   `400 invalid body`），必须显式传入以保持对外契约零改动。
 * @returns 校验通过的类型化数据
 * @throws ValidationError——由全局错误处理器统一序列化
 */
export function parseBody<T extends z.ZodTypeAny>(
  schema: T,
  body: unknown,
  failure?: ValidationFailure
): z.infer<T> {
  const result = schema.safeParse(body);
  if (!result.success) {
    if (failure) {
      throw new ValidationError(toFieldErrors(result.error), failure.message, failure.statusCode);
    }
    throw new ValidationError(toFieldErrors(result.error));
  }
  return result.data;
}

/**
 * 会话 ID 形态：非空字符串 + 限长 64。
 *
 * 刻意**不**强制 UUID 形态：重构前 /api/chat 对未知 sessionId 的处理是
 * 「查不到 → 以该 id 新建会话」，这是既有行为的一部分；收紧为 uuid 会改变该语义。
 * 限长 64 足以挡住超长/日志注入类输入。
 */
const sessionIdSchema = z.string().min(1).max(64);

/** 模型 ID 形态：非空字符串 + 限长 200（防超长注入到日志与下游请求）。 */
const modelSchema = z.string().min(1).max(200);

/**
 * POST /api/feedback 请求体。
 * 契约：sessionId + messageId 必填字符串、verdict 必填 up/down、comment 可选（截断 500）。
 */
export const feedbackBodySchema = z.object({
  sessionId: z.string().min(1),
  messageId: z.string().min(1),
  verdict: z.enum(["up", "down"]),
  comment: z.string().max(500).optional(),
});

/**
 * POST /api/sessions 请求体（建会话）。
 * 契约：model 与 title 均可选——缺省走服务端默认模型与「新对话」标题。
 */
export const createSessionBodySchema = z.object({
  model: modelSchema.optional(),
  title: z.string().min(1).max(200).optional(),
});

/**
 * PATCH /api/sessions/:sessionId 请求体（更新会话）。
 * 契约：title / model 均可选；两者皆缺时由路由判定为「无更新字段」。
 */
export const updateSessionBodySchema = z.object({
  title: z.string().min(1).max(200).optional(),
  model: modelSchema.optional(),
});

/**
 * POST /api/chat 请求体（流式对话）。
 *
 * 字段口径与重构前逐字一致：sessionId 可空（空则新建会话）、message 必填、
 * model/systemPrompt/cwd/permissionMode 可选。
 *
 * 注意：cwd 与 permissionMode **只做类型校验**——语义净化（路径钳制 / 权限模式白名单）
 * 仍由 server/security.ts 的 resolveWorkingDir 与 sanitizePermissionMode 负责，
 * 本层不重复实现那套安全逻辑（避免两处规则漂移）。
 */
export const chatBodySchema = z.object({
  sessionId: sessionIdSchema.optional().nullable(),  message: z.string().min(1).max(50_000),
  model: modelSchema.optional(),
  systemPrompt: z.string().max(100_000).optional(),
  cwd: z.string().max(4096).optional(),
  permissionMode: z.string().max(64).optional(),
});

/**
 * POST /api/permission-response 请求体（前端许可回执）。
 * 契约：requestId 必填、behavior 必填 allow/deny、message 可选。
 */
export const permissionResponseBodySchema = z.object({
  requestId: z.string().min(1),
  behavior: z.enum(["allow", "deny"]),
  message: z.string().max(2000).optional(),
});
