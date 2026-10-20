/**
 * security.ts — 安全边界纯函数与 SSE 守卫（W791 BL-29 提取·行为逐字保留）
 *
 * 从 server/index.ts 提取三类安全硬化逻辑，使其获得可回归测试面（BL-29：
 * 三轮外部评审点名的攻击面此前只有提交信息形式的记录、无回归测试固化）：
 *   ① 权限模式白名单（P0-1：外部请求体不可直接传入 bypassPermissions·防未授权 RCE）
 *   ② 工作目录钳制（P0-1/W536：realpath 规范化后仅允许 PROJECT_CWD 内·非法输入回落默认）
 *   ③ SSE 超时与断开清理（P2-3：总时长上限 + 客户端断开即中止引擎·防悬挂与烧 token）
 *
 * 提取口径：逻辑逐字迁移；仅两处注入化——ALLOW_BYPASS 由调用方传入（原模块级环境读取）、
 * maxMs 可注入（默认 10 分钟不变·供测试用小值）。index.ts 调用点语义等价。
 */
import fs from 'node:fs';
import path from 'node:path';

export type PermissionMode = 'default' | 'acceptEdits' | 'plan' | 'bypassPermissions';

const SAFE_PERMISSION_MODES = new Set(['default', 'acceptEdits', 'plan']);

/**
 * 权限模式白名单净化：仅白名单内值放行；
 * bypassPermissions 仅在 allowBypass（AGENT_WEB_ALLOW_BYPASS=1·本地单人模式）时放行，否则回落 default。
 */
export function sanitizePermissionMode(input: unknown, allowBypass: boolean): PermissionMode {
  if (typeof input === 'string' && SAFE_PERMISSION_MODES.has(input)) return input as PermissionMode;
  if (allowBypass && input === 'bypassPermissions') return 'bypassPermissions';
  return 'default';
}

/**
 * 工作目录钳制：cwd 经 realpath 规范化后必须等于或位于 projectCwd 内，否则回落 projectCwd 本身。
 * projectCwd 同样先 resolve + realpath（realpath 失败保持 resolve 结果·与原实现一致）。
 * 非字符串 / 空串 / 解析失败 / 越界（含 `..` 穿越与符号链接逃逸）一律回落。
 */
export function resolveWorkingDir(cwd: unknown, projectCwd: string): string {
  let base = path.resolve(projectCwd);
  try {
    base = fs.realpathSync(base);
  } catch {
    /* 保持 resolve 结果 */
  }
  if (typeof cwd === 'string' && cwd.trim()) {
    let candidate = path.resolve(cwd);
    try {
      candidate = fs.realpathSync(candidate);
    } catch {
      candidate = '';
    }
    if (candidate && (candidate === base || candidate.startsWith(base + path.sep))) return candidate;
  }
  return base;
}

/**
 * W835：Host 头归一化（防 DNS rebinding 的纯函数层）。
 *
 * 威胁机理：服务端只绑定回环地址（127.0.0.1）且默认免认证，但**浏览器发往 127.0.0.1 的
 * 请求会带上攻击者可控的 Host 头**——攻击者把 evil.com 的 DNS 解析到 127.0.0.1
 * （DNS rebinding），浏览器便以 `Host: evil.com:3000` 请求本地 API；服务端若不校验 Host，
 * 这次请求与正常本地请求无异 ⇒ 攻击者网页可驱动本地 Agent（读文件 / 执行命令）。
 * 端口不参与判定（与 Django ALLOWED_HOSTS 同口径）：代理与测试常改端口，判端口会误伤。
 *
 * 归一化口径：去端口前缀 → IPv6 去方括号 → 小写 → 去 FQDN 尾点。
 */
export function normalizeHostname(hostHeader: unknown): string {
  if (typeof hostHeader !== "string") return "";
  let host = hostHeader.trim().toLowerCase();
  if (!host) return "";
  if (host.startsWith("[")) {
    // IPv6 带方括号形态：[::1]:3000 → ::1（方括号后是端口，整体丢弃）
    const end = host.indexOf("]");
    if (end === -1) return "";
    host = host.slice(1, end);
  } else {
    // 恰一个冒号 ⇒ host:port（去端口）；两个及以上冒号 ⇒ 裸 IPv6（如 ::1）·整体保留。
    // （早前实现按「首个冒号」截断，把裸 IPv6 截成空串 —— 白名单里的 ::1 自身被归一化成空，
    //   导致 [::1]:3000 反而被判否；由本批自测 isAllowedHost 白名单用例当场抓出。）
    const colons = host.split(":").length - 1;
    if (colons === 1) host = host.slice(0, host.indexOf(":"));
  }
  if (host.length > 1 && host.endsWith(".")) host = host.slice(0, -1);
  return host;
}

/**
 * W835：Host 白名单判定——仅当归一化后的主机名落在白名单内才放行。
 * 空 / 缺失 / 畸形 Host 一律判否（fail-closed）。
 */
export function isAllowedHost(hostHeader: unknown, allowlist: readonly string[]): boolean {
  const host = normalizeHostname(hostHeader);
  if (!host) return false;
  return allowlist.some((entry) => normalizeHostname(entry) === host);
}

/** SSE 总时长上限默认值（10 分钟·与原实现一致）。 */
export const SSE_MAX_MS_DEFAULT = 10 * 60 * 1000;

/** 守卫所需的最小 res 面（结构化注入·测试可用替身·不依赖 express 类型）。 */
export interface SseResLike {
  write: (chunk: string) => unknown;
  end: () => unknown;
  on: (event: string, cb: () => void) => unknown;
  off: (event: string, cb: () => void) => unknown;
}

/** 挂起的权限请求（守卫只消费 sessionId 与 reject·index.ts 的 PendingPermission 为超集可指派）。 */
export interface PendingPermissionLike {
  sessionId: string;
  reject: (error: Error) => void;
}

export interface SseGuardDeps {
  res: SseResLike;
  sessionId: string;
  pendingPermissions: Record<string, PendingPermissionLike>;
  /** 总时长上限（毫秒）·缺省 SSE_MAX_MS_DEFAULT·测试注入小值。 */
  maxMs?: number;
}

export interface SseGuard {
  /** 引擎 AbortSignal：超时/断开时中止（不再为已断开客户端烧 token·W680）。 */
  signal: AbortSignal;
  /** 客户端断开处理（幂等·重复调用无害）。 */
  abortStream: () => void;
  /** 正常完成/异常路径清理定时器（不结束流·由调用方随后 res.end()）。 */
  clearTimer: () => void;
}

/**
 * SSE 守卫：总时长上限 + 断开清理 + 引擎中止 + 本会话 pending 权限请求清算。
 * 行为对照 index.ts 原内联实现（P2-3/W680/W568）：
 *   - 超时：abort 引擎 → 清算本会话 pending（reject「SSE 超时」）→ 写 error 事件并 end；
 *   - 断开：clearTimeout → 清算本会话 pending（reject「客户端断开连接」）→ abort 引擎 → end；
 *   - 幂等：aborted 标志防重复；完成路径只 clearTimer 不动流。
 */
export function createSseGuard(deps: SseGuardDeps): SseGuard {
  const maxMs = typeof deps.maxMs === 'number' && deps.maxMs > 0 ? deps.maxMs : SSE_MAX_MS_DEFAULT;
  let aborted = false;
  const engineAbort = new AbortController();
  const sseTimer = setTimeout(() => {
    if (aborted) return;
    aborted = true;
    engineAbort.abort();
    for (const rid of Object.keys(deps.pendingPermissions)) {
      const p = deps.pendingPermissions[rid];
      if (p.sessionId === deps.sessionId) {
        delete deps.pendingPermissions[rid];
        p.reject(new Error('SSE 超时'));
      }
    }
    try {
      deps.res.write(`data: ${JSON.stringify({ type: 'error', message: '请求超时（10 分钟上限）' })}\n\n`);
      deps.res.end();
    } catch {
      /* 客户端可能已断开 */
    }
  }, maxMs);
  const abortStream = () => {
    if (aborted) return;
    aborted = true;
    clearTimeout(sseTimer);
    for (const rid of Object.keys(deps.pendingPermissions)) {
      const p = deps.pendingPermissions[rid];
      if (p.sessionId === deps.sessionId) {
        delete deps.pendingPermissions[rid];
        p.reject(new Error('客户端断开连接'));
      }
    }
    engineAbort.abort();
    try {
      deps.res.end();
    } catch {
      /* 已断开 */
    }
  };
  return {
    signal: engineAbort.signal,
    abortStream,
    clearTimer: () => clearTimeout(sseTimer),
  };
}
