/**
 * errorMessage.ts — API 错误 → 用户可读文案（W808 新建）
 *
 * 职责边界：把「传输层/协议层的失败」翻译成「人话」。
 * **不决定何时重试、不发起请求**——只产出文案。
 *
 * 动因（W808）：重构前 `useSessions.ts` 等处把失败 `console.error` 掉就完事，
 * 用户界面上「会话列表加载不出来」表现为**一片空白且无任何提示**——
 * 静默吞错是跨边界错误处理的头号反模式。本模块提供统一文案来源。
 *
 * 映射原则（按状态码）：
 *   - 4xx 是**客户端问题**（改输入/登录/等一下），文案要具体可行动；
 *   - 5xx 是**服务端问题**，不暴露内部细节（服务端已保证不返堆栈），
 *     文案统一为「稍后重试」类，避免用户以为是自己的操作错了；
 *   - 网络不可达（TypeError: Failed to fetch）单列——这是最常见的本地场景
 *     （后端没起），文案要直指「后端服务未启动」。
 */

/** 前端 API 客户端抛出的错误类型（与 src/utils/api.ts 的 ApiError 同构）。 */
export interface ApiErrorLike {
  status?: number;
  body?: unknown;
  message?: string;
}

/** 判断值是否为「带 status 的 API 错误」——兼容跨模块/跨版本的结构判定。 */
function hasStatus(value: unknown): value is { status: number; body?: unknown } {
  return (
    typeof value === "object" &&
    value !== null &&
    typeof (value as { status?: unknown }).status === "number"
  );
}

/** 从服务端错误体里取 `error` 字段（服务端统一形状 `{ error: string }`）。 */
function serverMessage(body: unknown): string | undefined {
  if (typeof body !== "object" || body === null) return undefined;
  const message = (body as { error?: unknown }).error;
  return typeof message === "string" && message.trim() ? message : undefined;
}

/**
 * 把任意错误转换为用户可读文案。
 *
 * @param error 捕获到的错误（ApiError / TypeError / 未知）
 * @returns 中文文案（可直接展示给用户）
 */
export function getErrorMessage(error: unknown): string {
  // 网络不可达：fetch 失败抛 TypeError（浏览器文案为 "Failed to fetch"）
  if (error instanceof TypeError) {
    return "无法连接后端服务：请确认 API 服务已启动（默认 http://127.0.0.1:3000）";
  }

  if (hasStatus(error)) {
    const { status, body } = error;

    // 服务端给出的具体语义优先（运营错误的文案是逐字对齐的，可直接展示）
    const fromServer = serverMessage(body);
    if (fromServer) return fromServer;

    switch (status) {
      case 400:
        return "请求内容有误，请检查后重试";
      case 401:
        return "未授权：请在请求头携带 AGENT_WEB_TOKEN（x-agent-token 或 Authorization: Bearer）";
      case 403:
        return "无权访问该资源";
      case 404:
        return "请求的资源不存在";
      case 409:
        return "与既有资源冲突，请刷新后重试";
      case 422:
        return "请求参数校验未通过，请检查填写内容";
      case 429:
        return "请求过于频繁，请稍后再试";
      default:
        break;
    }

    if (status >= 500) return "服务端出错，请稍后重试";
    if (status >= 400) return `请求失败（HTTP ${status}）`;
  }

  if (error instanceof Error && error.message) {
    return error.message;
  }

  return "发生未知错误，请稍后重试";
}

/**
 * 是否属于「可重试」的错误（5xx 与网络不可达）。
 * 用于决定是否自动重试——4xx 是客户端问题，重试无益（skill 纪律：禁重试 4xx）。
 */
export function isRetryable(error: unknown): boolean {
  if (error instanceof TypeError) return true;
  if (hasStatus(error)) return error.status >= 500;
  return false;
}
