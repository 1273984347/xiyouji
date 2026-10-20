/**
 * api.test.ts — 前端 API client 单元测试（W808 新建）
 *
 * 覆盖 W808 修掉的三个真实缺陷（每个都有「负样本」——旧实现下必红）：
 *   ① 不判 res.ok → 服务端 500 的错误体被当成功数据返回；
 *   ② 不注入共享 token → 服务端开 AGENT_WEB_TOKEN 后全站 401；
 *   ③ 基址硬编码 → 无法指向独立部署的后端。
 *
 * 测试手法：注入 fetch 替身（**不 mock 业务逻辑**——只替身传输层），
 * 断言「请求怎么发出去」与「失败怎么冒出来」。
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { api, ApiError, getJson, postJson, patchJson, del } from '../utils/api';

/** 构造一个最小 Response 替身（只实现 client 实际用到的面）。 */
function jsonResponse(status: number, body: unknown): Response {
  const text = body === undefined ? '' : JSON.stringify(body);
  return {
    ok: status >= 200 && status < 300,
    status,
    text: async () => text,
  } as unknown as Response;
}

describe('api client · 缺陷①：不判 res.ok（错误不得当成功数据返回）', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('GET 遇 500 时抛 ApiError（携带 status 与 body），不返回错误体当数据', async () => {
    fetchMock.mockResolvedValue(jsonResponse(500, { error: '服务器内部错误' }));

    await expect(api.health()).rejects.toBeInstanceOf(ApiError);

    try {
      await api.health();
      expect.unreachable('应当抛出 ApiError');
    } catch (err) {
      const apiErr = err as ApiError;
      expect(apiErr.status).toBe(500);
      expect(apiErr.body).toEqual({ error: '服务器内部错误' });
      expect(apiErr.message).toBe('服务器内部错误');
    }
  });

  it('GET 遇 404 时抛 ApiError 且 status 正确', async () => {
    fetchMock.mockResolvedValue(jsonResponse(404, { error: '接口不存在：GET /api/health' }));
    await expect(api.health()).rejects.toMatchObject({ status: 404 });
  });

  it('POST 遇 400 时抛 ApiError（旧实现会静默返回 {error} 供上层当数据用）', async () => {
    fetchMock.mockResolvedValue(jsonResponse(400, { error: 'invalid body' }));
    await expect(api.feedback({ sessionId: 's', messageId: 'm', verdict: 'up' })).rejects.toMatchObject({
      status: 400,
      message: 'invalid body',
    });
  });

  it('PATCH 遇 422（校验失败）时抛 ApiError', async () => {
    fetchMock.mockResolvedValue(jsonResponse(422, { error: '请求参数校验失败' }));
    await expect(api.updateSession('sess-1', { title: 'x' })).rejects.toMatchObject({ status: 422 });
  });

  it('DELETE 遇 404 时抛 ApiError', async () => {
    fetchMock.mockResolvedValue(jsonResponse(404, { error: '会话不存在：sess-1' }));
    await expect(api.deleteSession('sess-1')).rejects.toMatchObject({ status: 404 });
  });

  it('2xx 时正常返回解析后的 body', async () => {
    fetchMock.mockResolvedValue(jsonResponse(200, { status: 'ok', timestamp: '2026-10-20T00:00:00Z' }));
    const result = await api.health();
    expect(result.status).toBe('ok');
  });

  it('204 无内容响应不抛解析错（返回 undefined）', async () => {
    fetchMock.mockResolvedValue({ ok: true, status: 204, text: async () => '' } as unknown as Response);
    await expect(getJson('/api/no-content')).resolves.toBeUndefined();
  });

  it('非 JSON 响应体不被当作数据（返回 undefined 而非抛解析错）', async () => {
    fetchMock.mockResolvedValue({
      ok: true,
      status: 200,
      text: async () => '<html>not json</html>',
    } as unknown as Response);
    await expect(getJson('/api/html')).resolves.toBeUndefined();
  });

  it('网络层失败原样抛出 TypeError（供 errorMessage 映射为「后端未启动」）', async () => {
    fetchMock.mockRejectedValue(new TypeError('Failed to fetch'));
    await expect(api.health()).rejects.toBeInstanceOf(TypeError);
  });
});

describe('api client · 缺陷②：共享 token 注入', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    vi.resetModules();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.unstubAllEnvs(); // 必须清 env 存根：否则 VITE_API_BASE_URL 会泄漏到后续用例
    vi.resetModules();
  });

  it('未配置 token 时不带 x-agent-token 头（本地免认证模式）', async () => {
    fetchMock.mockResolvedValue(jsonResponse(200, { status: 'ok' }));
    await api.health();
    const [, init] = fetchMock.mock.calls[0];
    expect((init.headers as Record<string, string>)['x-agent-token']).toBeUndefined();
  });

  it('配置 VITE_AGENT_WEB_TOKEN 时自动带上 x-agent-token 头', async () => {
    vi.stubEnv('VITE_AGENT_WEB_TOKEN', 'secret-token-123');
    // 重新导入模块以读取新的 env（模块级常量在 import 时求值）
    const mod = await import('../utils/api');

    fetchMock.mockResolvedValue(jsonResponse(200, { status: 'ok' }));
    await mod.api.health();

    const [, init] = fetchMock.mock.calls[0];
    expect((init.headers as Record<string, string>)['x-agent-token']).toBe('secret-token-123');
  });

  it('写请求带 Content-Type 且带 token（两个头并存）', async () => {
    vi.stubEnv('VITE_AGENT_WEB_TOKEN', 'secret-token-456');
    const mod = await import('../utils/api');

    fetchMock.mockResolvedValue(jsonResponse(200, { ok: true, inserted: 1 }));
    await mod.api.feedback({ sessionId: 's', messageId: 'm', verdict: 'up' });

    const [, init] = fetchMock.mock.calls[0];
    const headers = init.headers as Record<string, string>;
    expect(headers['Content-Type']).toBe('application/json');
    expect(headers['x-agent-token']).toBe('secret-token-456');
  });
});

describe('api client · 缺陷③：基址可配置', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    vi.resetModules();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.unstubAllEnvs(); // 必须清 env 存根：否则 VITE_API_BASE_URL 会泄漏到后续用例
    vi.resetModules();
  });

  it('配置 VITE_API_BASE_URL 时拼到路径前（支持后端独立域名）', async () => {
    vi.stubEnv('VITE_API_BASE_URL', 'http://api.example.com:3000');
    const mod = await import('../utils/api');

    fetchMock.mockResolvedValue(jsonResponse(200, { status: 'ok' }));
    await mod.api.health();

    expect(fetchMock.mock.calls[0][0]).toBe('http://api.example.com:3000/api/health');
  });

  it('基址尾部斜杠被规整（不产生双斜杠路径）', async () => {
    vi.stubEnv('VITE_API_BASE_URL', 'http://api.example.com:3000/');
    const mod = await import('../utils/api');

    fetchMock.mockResolvedValue(jsonResponse(200, { status: 'ok' }));
    await mod.api.health();

    expect(fetchMock.mock.calls[0][0]).toBe('http://api.example.com:3000/api/health');
  });

  it('未配置基址时用同源相对路径（走 Vite proxy）', async () => {
    const mod = await import('../utils/api');
    fetchMock.mockResolvedValue(jsonResponse(200, { status: 'ok' }));
    await mod.api.health();
    expect(fetchMock.mock.calls[0][0]).toBe('/api/health');
  });
});

describe('api client · 端点路径契约', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('各端点打到正确的路径与方法（路径即契约）', async () => {
    fetchMock.mockResolvedValue(jsonResponse(200, {}));

    await api.listSessions();
    expect(fetchMock.mock.calls[0][0]).toBe('/api/sessions');

    fetchMock.mockClear();
    await api.getSession('s1');
    expect(fetchMock.mock.calls[0][0]).toBe('/api/sessions/s1');

    fetchMock.mockClear();
    await api.createSession({ title: 't' });
    expect(fetchMock.mock.calls[0][0]).toBe('/api/sessions');
    expect(fetchMock.mock.calls[0][1].method).toBe('POST');

    fetchMock.mockClear();
    await api.deleteSession('s1');
    expect(fetchMock.mock.calls[0][0]).toBe('/api/sessions/s1');
    expect(fetchMock.mock.calls[0][1].method).toBe('DELETE');

    fetchMock.mockClear();
    await api.permissionResponse({ requestId: 'r1', behavior: 'allow' });
    expect(fetchMock.mock.calls[0][0]).toBe('/api/permission-response');

    fetchMock.mockClear();
    await api.feedbackSummary();
    expect(fetchMock.mock.calls[0][0]).toBe('/api/feedback/summary');

    fetchMock.mockClear();
    await api.ready();
    expect(fetchMock.mock.calls[0][0]).toBe('/api/ready');
  });

  it('audit 端点带 limit 查询参数', async () => {
    fetchMock.mockResolvedValue(jsonResponse(200, {}));
    await api.audit(50);
    expect(fetchMock.mock.calls[0][0]).toBe('/api/audit?limit=50');
  });
});
