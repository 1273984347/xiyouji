/**
 * errorMessage.test.ts — 错误文案映射单元测试（W808 新建）
 *
 * 覆盖 W808 修掉的缺陷④：`useSessions` 等处把失败 `console.error` 掉就完事，
 * 用户界面上「加载不出来」表现为**一片空白且无任何提示**。
 *
 * 本测试锁定「每个失败态都有可读文案」这一契约——任何一条落到兜底文案都视为回归。
 */
import { describe, it, expect } from 'vitest';
import { getErrorMessage, isRetryable } from '../utils/errorMessage';
import { ApiError } from '../utils/api';

describe('getErrorMessage · 服务端语义优先', () => {
  it('服务端给出的 error 文案直接透出（运营错误逐字对齐）', () => {
    const err = new ApiError(400, { error: 'invalid body' }, 'invalid body');
    expect(getErrorMessage(err)).toBe('invalid body');
  });

  it('服务端文案优先于状态码默认文案', () => {
    const err = new ApiError(500, { error: '引擎未配置：请在服务端 .env 设置 LLM_API_BASE' });
    expect(getErrorMessage(err)).toBe('引擎未配置：请在服务端 .env 设置 LLM_API_BASE');
  });
});

describe('getErrorMessage · 状态码兜底文案', () => {
  const cases: Array<[number, string]> = [
    [400, '请求内容有误，请检查后重试'],
    [401, '未授权：请在请求头携带 AGENT_WEB_TOKEN（x-agent-token 或 Authorization: Bearer）'],
    [403, '无权访问该资源'],
    [404, '请求的资源不存在'],
    [409, '与既有资源冲突，请刷新后重试'],
    [422, '请求参数校验未通过，请检查填写内容'],
    [429, '请求过于频繁，请稍后再试'],
    [500, '服务端出错，请稍后重试'],
    [503, '服务端出错，请稍后重试'],
  ];

  for (const [status, expected] of cases) {
    it(`${status} → ${expected}`, () => {
      // 构造无服务端文案的情形（body 里没有 error 字段）以走状态码兜底分支
      const err = { status, body: {} };
      expect(getErrorMessage(err)).toBe(expected);
    });
  }

  it('未列举的 4xx 给出带状态码的通用文案', () => {
    expect(getErrorMessage({ status: 418, body: {} })).toBe('请求失败（HTTP 418）');
  });
});

describe('getErrorMessage · 网络层失败', () => {
  it('TypeError（fetch 失败）→ 指向「后端未启动」', () => {
    const msg = getErrorMessage(new TypeError('Failed to fetch'));
    expect(msg).toContain('无法连接后端服务');
    expect(msg).toContain('3000');
  });

  it('其它 Error 回落到其 message', () => {
    expect(getErrorMessage(new Error('磁盘已满'))).toBe('磁盘已满');
  });

  it('非 Error 值 → 未知错误兜底（不返回 undefined）', () => {
    expect(getErrorMessage('some string')).toBe('发生未知错误，请稍后重试');
    expect(getErrorMessage(null)).toBe('发生未知错误，请稍后重试');
    expect(getErrorMessage(undefined)).toBe('发生未知错误，请稍后重试');
  });
});

describe('isRetryable · 禁重试 4xx（skill 纪律）', () => {
  it('5xx 可重试', () => {
    expect(isRetryable({ status: 500, body: {} })).toBe(true);
    expect(isRetryable({ status: 503, body: {} })).toBe(true);
  });

  it('4xx 不可重试（客户端问题，重试无益）', () => {
    expect(isRetryable({ status: 400, body: {} })).toBe(false);
    expect(isRetryable({ status: 401, body: {} })).toBe(false);
    expect(isRetryable({ status: 404, body: {} })).toBe(false);
    expect(isRetryable({ status: 422, body: {} })).toBe(false);
    expect(isRetryable({ status: 429, body: {} })).toBe(false);
  });

  it('网络不可达可重试', () => {
    expect(isRetryable(new TypeError('Failed to fetch'))).toBe(true);
  });
});
