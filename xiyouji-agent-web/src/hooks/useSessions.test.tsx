/**
 * useSessions.test.tsx — 会话 hook 行为测试（W808 新建）
 *
 * 覆盖 W808 修掉的缺陷④：加载失败此前只 `console.error` 静默吞掉，
 * 界面表现为「会话列表空白且无任何提示」。本测试锁定契约：
 *   ① 失败时 error 状态**必须**有可读文案（不得为空）；
 *   ② 失败时不得把错误体当数据塞进 sessions；
 *   ③ 成功后 error 状态被清空。
 *
 * 测试手法：替身**仅限传输层**（fetch），业务逻辑走真实实现。
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, waitFor, act } from '@testing-library/react';
import { useSessions } from './useSessions';

/** 构造最小 Response 替身。 */
function jsonResponse(status: number, body: unknown): Response {
  const text = body === undefined ? '' : JSON.stringify(body);
  return {
    ok: status >= 200 && status < 300,
    status,
    text: async () => text,
  } as unknown as Response;
}

describe('useSessions · 失败态可见（W808 缺陷④）', () => {
  let fetchMock: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    localStorage.clear();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.unstubAllEnvs();
  });

  it('服务端 500 时：error 有可读文案，且 sessions 保持为空（不把错误当数据）', async () => {
    fetchMock.mockResolvedValue(jsonResponse(500, { error: '服务器内部错误' }));

    const { result } = renderHook(() => useSessions());

    await act(async () => {
      await result.current.fetchSessions();
    });

    await waitFor(() => {
      expect(result.current.error).toBeTruthy();
    });
    expect(result.current.error).toBe('服务器内部错误');
    // 关键断言：错误体不得被塞进会话列表（旧实现会把 {error} 当成功数据）
    expect(result.current.sessions).toHaveLength(0);
  });

  it('网络不可达时：error 指向「无法连接后端服务」', async () => {
    fetchMock.mockRejectedValue(new TypeError('Failed to fetch'));

    const { result } = renderHook(() => useSessions());

    await act(async () => {
      await result.current.fetchSessions();
    });

    await waitFor(() => {
      expect(result.current.error).toContain('无法连接后端服务');
    });
  });

  it('成功时：sessions 被填充且 error 为 null', async () => {
    const now = new Date().toISOString();
    fetchMock.mockResolvedValue(
      jsonResponse(200, {
        sessions: [
          { id: 's1', title: '测试会话', model: 'glm-4.6', created_at: now, updated_at: now, messageCount: 2 },
        ],
      })
    );

    const { result } = renderHook(() => useSessions());

    await act(async () => {
      await result.current.fetchSessions();
    });

    await waitFor(() => {
      expect(result.current.sessions).toHaveLength(1);
    });
    expect(result.current.error).toBeNull();
    expect(result.current.sessions[0].title).toBe('测试会话');
    // createdAt 应被转成 Date 对象（契约：前端内部用 Date）
    expect(result.current.sessions[0].createdAt).toBeInstanceOf(Date);
  });

  it('先失败后成功：error 被清空（错误态不残留）', async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse(500, { error: '服务器内部错误' }));

    const { result } = renderHook(() => useSessions());
    await act(async () => {
      await result.current.fetchSessions();
    });
    await waitFor(() => {
      expect(result.current.error).toBeTruthy();
    });

    fetchMock.mockResolvedValueOnce(jsonResponse(200, { sessions: [] }));
    await act(async () => {
      await result.current.fetchSessions();
    });

    await waitFor(() => {
      expect(result.current.error).toBeNull();
    });
  });

  it('删除会话失败时：error 有文案，且不假装删除成功（会话仍在列表中）', async () => {
    const now = new Date().toISOString();
    fetchMock.mockResolvedValueOnce(
      jsonResponse(200, {
        sessions: [{ id: 's1', title: '保留', model: 'm', created_at: now, updated_at: now }],
      })
    );

    const { result } = renderHook(() => useSessions());
    await act(async () => {
      await result.current.fetchSessions();
    });
    await waitFor(() => {
      expect(result.current.sessions).toHaveLength(1);
    });

    // 删除时服务端返回 404
    fetchMock.mockResolvedValueOnce(jsonResponse(404, { error: '会话不存在：s1' }));
    let nav: string | null = 'unset';
    await act(async () => {
      nav = await result.current.deleteSession('s1');
    });

    expect(result.current.error).toBe('会话不存在：s1');
    expect(nav).toBeNull(); // 失败时不给导航目标
    // 关键断言：失败不该把会话从本地列表里抹掉
    expect(result.current.sessions).toHaveLength(1);
  });
});
