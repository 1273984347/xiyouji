/**
 * InlinePermissionCard.test.tsx — 权限卡片工具名映射回归锁（W1150 新建）
 *
 * 锁定 W1150 修掉的 P1 缺陷：TOOL_CONFIG 键曾是 PascalCase（'Bash'/'Write'…），
 * 服务端从不发送 ⇒ 全部落入灰色兜底、label 显示原始工具名、
 * run_command（唯一命令执行面）的「危险操作」标记永不出现。
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { InlinePermissionCard } from './InlinePermissionCard';
import { PermissionRequest } from '../types';

function makeRequest(toolName: string, input: Record<string, unknown>): PermissionRequest {
  return {
    requestId: 'req-1',
    toolUseId: 'tu-1',
    toolName,
    input,
    sessionId: 's-1',
    timestamp: Date.now(),
  };
}

describe('InlinePermissionCard · 引擎真名与危险标记（W1150 回归锁）', () => {
  it('run_command 显示「执行命令」标签与「危险操作」标记', () => {
    render(
      <InlinePermissionCard
        request={makeRequest('run_command', { command: 'python scripts/词频.py --chap 1' })}
        onAllow={() => {}}
        onDeny={() => {}}
      />
    );
    expect(screen.getByText('执行命令')).toBeTruthy();
    expect(screen.getByText('危险操作')).toBeTruthy();
    // 命令内容截断展示
    expect(screen.getByText(/python scripts/)).toBeTruthy();
  });

  it('write_file / read_file / grep 显示引擎名对应的中文标签', () => {
    render(
      <InlinePermissionCard
        request={makeRequest('write_file', { path: 'docs/00-导读/术语表.md', content: 'x' })}
        onAllow={() => {}}
        onDeny={() => {}}
      />
    );
    expect(screen.getByText('写入文件')).toBeTruthy();

    const { unmount } = render(
      <InlinePermissionCard
        request={makeRequest('read_file', { path: 'README.md' })}
        onAllow={() => {}}
        onDeny={() => {}}
      />
    );
    expect(screen.getByText('读取文件')).toBeTruthy();
    unmount();

    render(
      <InlinePermissionCard
        request={makeRequest('grep', { pattern: '心猿' })}
        onAllow={() => {}}
        onDeny={() => {}}
      />
    );
    expect(screen.getByText('文本搜索')).toBeTruthy();
  });

  it('write_file 不标危险（旧实现 isDangerous 只认 Bash/Delete 系）', () => {
    render(
      <InlinePermissionCard
        request={makeRequest('write_file', { path: 'a.md', content: 'x' })}
        onAllow={() => {}}
        onDeny={() => {}}
      />
    );
    expect(screen.queryByText('危险操作')).toBeNull();
  });
});
