/**
 * toolIcons.test.ts — 引擎工具名映射回归锁（W1150 新建）
 *
 * 锁定 W1150 修掉的 P1 缺陷：toolIcons 的判定曾用 `name === 'bash'` 等窄等值，
 * 而服务端引擎真实工具名是 `run_command`/`write_file`/`read_file`/`edit_file`
 * （server/engine/tools.ts）⇒ 专用面板永不渲染、汇总条全部退化「其他」。
 * 根修 = 归一函数（小写 + 去下划线）。本测试锁定契约：
 *   ① 引擎真名必须命中正确专用面板分支（run_command→bash、write_file→write）；
 *   ② 引擎真名必须命中正确汇总大类；
 *   ③ 引擎真名不得落入 Wrench 兜底图标；
 *   ④ 历史 PascalCase/无下划线写法保持兼容（不回归）。
 */
import { describe, it, expect } from 'vitest';
import { Terminal, FileText, FolderSearch, Wrench, Edit, Eye } from 'lucide-react';
import { getToolIcon, getToolType, getToolRenderKind } from './toolIcons';

describe('toolIcons · 引擎真名映射（W1150 回归锁）', () => {
  it('run_command 命中 bash 面板与 Terminal 图标（不再 Wrench 兜底）', () => {
    expect(getToolRenderKind('run_command')).toBe('bash');
    expect(getToolType('run_command')).toBe('bash');
    expect(getToolIcon('run_command').icon).toBe(Terminal);
  });

  it('write_file 命中 write 面板与 FileText 图标', () => {
    expect(getToolRenderKind('write_file')).toBe('write');
    expect(getToolType('write_file')).toBe('write');
    expect(getToolIcon('write_file').icon).toBe(FileText);
  });

  it('read_file / edit_file 命中对应汇总大类与专属图标', () => {
    expect(getToolType('read_file')).toBe('read');
    expect(getToolIcon('read_file').icon).toBe(Eye);
    expect(getToolType('edit_file')).toBe('edit');
    expect(getToolIcon('edit_file').icon).toBe(Edit);
    // read/edit 无专用面板属既定设计（通用面板兜底），但不得是 Wrench 兜底图标
    expect(getToolIcon('read_file').icon).not.toBe(Wrench);
    expect(getToolIcon('edit_file').icon).not.toBe(Wrench);
  });

  it('glob / grep 命中 search 大类与 FolderSearch 图标', () => {
    expect(getToolType('glob')).toBe('search');
    expect(getToolType('grep')).toBe('search');
    expect(getToolIcon('glob').icon).toBe(FolderSearch);
  });

  it('历史写法保持兼容（bash/write/read/edit 不回归）', () => {
    expect(getToolRenderKind('bash')).toBe('bash');
    expect(getToolRenderKind('Bash')).toBe('bash');
    expect(getToolRenderKind('write')).toBe('write');
    expect(getToolRenderKind('WriteFile')).toBe('write');
    expect(getToolType('read')).toBe('read');
    expect(getToolType('edit')).toBe('edit');
  });

  it('未知工具仍走 generic + Wrench 兜底', () => {
    expect(getToolRenderKind('totally_unknown')).toBe('generic');
    expect(getToolIcon('totally_unknown').icon).toBe(Wrench);
    expect(getToolType('totally_unknown')).toBe('other');
  });
});
