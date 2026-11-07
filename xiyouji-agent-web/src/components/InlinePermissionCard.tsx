import { Button } from 'tdesign-react';
import { WarnIcon } from './UiIcons';
import {
  TerminalIcon,
  FileIcon,
  FolderOpenIcon,
  SearchIcon,
  Code1Icon,
  EditIcon,
} from 'tdesign-icons-react';
import { PermissionRequest } from '../types';

interface InlinePermissionCardProps {
  request: PermissionRequest;
  onAllow: () => void;
  onDeny: () => void;
}

// 工具名称到图标和颜色的映射
// W1150 根修：键改为引擎真实工具名（server/engine/tools.ts 的六件套）——
// 旧键是 PascalCase（'Bash'/'Write'/'Read'），服务端从不发送 ⇒ 全部落入灰色兜底、
// 标签显示原始名、run_command 的「危险操作」标记永不出现。
// 颜色统一走 TDesign 主题令牌（亮/暗主题自适应）；紫/橙两色无对应令牌，为既定色板。
const TOOL_CONFIG: Record<string, { icon: React.ReactNode; color: string; label: string }> = {
  'run_command': { icon: <TerminalIcon />, color: 'var(--td-error-color)', label: '执行命令' },
  'write_file': { icon: <EditIcon />, color: 'var(--td-brand-color)', label: '写入文件' },
  'edit_file': { icon: <EditIcon />, color: 'var(--td-brand-color)', label: '编辑文件' },
  'read_file': { icon: <FileIcon />, color: 'var(--td-success-color)', label: '读取文件' },
  'glob': { icon: <FolderOpenIcon />, color: 'var(--td-warning-color)', label: '按模式列文件' },
  'grep': { icon: <SearchIcon />, color: '#8a6be5', label: '文本搜索' },
};

// 获取工具配置
const getToolConfig = (toolName: string) => {
  return TOOL_CONFIG[toolName] || {
    icon: <Code1Icon />,
    color: 'var(--td-text-color-secondary)',
    label: toolName
  };
};

// 获取文件路径或主要信息（入参名与 server/engine/tools.ts 的 schema 对齐）
const getMainInfo = (toolName: string, input: Record<string, unknown>): string => {
  if (toolName === 'run_command' && input.command) {
    const cmd = String(input.command);
    return cmd.length > 60 ? cmd.slice(0, 60) + '...' : cmd;
  }
  if (toolName === 'glob' || toolName === 'grep') {
    if (input.pattern) {
      const pat = String(input.pattern);
      return pat.length > 60 ? pat.slice(0, 60) + '...' : pat;
    }
  }
  if (input.path) {
    return String(input.path);
  }
  // 返回第一个有意义的参数值
  for (const [, value] of Object.entries(input)) {
    if (value && typeof value === 'string') {
      return value.length > 60 ? value.slice(0, 60) + '...' : value;
    }
  }
  return '';
};

export function InlinePermissionCard({ request, onAllow, onDeny }: InlinePermissionCardProps) {
  const toolConfig = getToolConfig(request.toolName);
  const mainInfo = getMainInfo(request.toolName, request.input);
  // run_command 是唯一执行任意命令面（服务端白名单内）的权限点——必须显式标「危险操作」
  const isDangerous = request.toolName === 'run_command';

  return (
    <div className="animate-fade-in flex items-center gap-3 flex-wrap py-2">
      {/* 工具图标和标签 */}
      <div
        className="flex items-center gap-2 px-3 py-1.5 rounded-full"
        style={{
          // color-mix 兼容 CSS 变量取色（旧 `${color}15` 十六进制拼 alpha 只支持字面色）
          backgroundColor: `color-mix(in srgb, ${toolConfig.color} 12%, transparent)`,
          color: toolConfig.color
        }}
      >
        <span className="flex items-center text-base">{toolConfig.icon}</span>
        <span className="text-sm font-medium">{toolConfig.label}</span>
      </div>

      {/* 文件路径/命令 */}
      {mainInfo && (
        <code
          className="text-sm px-2.5 py-1 rounded-md font-mono truncate max-w-[400px]"
          style={{
            backgroundColor: 'var(--td-bg-color-component)',
            color: 'var(--td-text-color-primary)'
          }}
          title={mainInfo}
        >
          {mainInfo}
        </code>
      )}

      {/* 危险操作警告标记 */}
      {isDangerous && (
        <span
          className="text-xs px-2 py-0.5 rounded"
          style={{
            backgroundColor: 'color-mix(in srgb, var(--td-error-color) 10%, transparent)',
            color: 'var(--td-error-color)'
          }}
        >
          <WarnIcon /> 危险操作
        </span>
      )}

      {/* 操作按钮 */}
      <div className="flex items-center gap-2 ml-auto">
        <Button
          size="small"
          theme="danger"
          variant="text"
          onClick={onDeny}
          style={{
            color: 'var(--td-error-color)',
            fontWeight: 500
          }}
        >
          拒绝
        </Button>
        <Button
          size="small"
          theme="success"
          variant="base"
          onClick={onAllow}
          style={{
            backgroundColor: 'var(--td-success-color)',
            borderColor: 'var(--td-success-color)',
            color: 'var(--td-text-color-anti)',
            fontWeight: 500
          }}
        >
          允许
        </Button>
      </div>
    </div>
  );
}
