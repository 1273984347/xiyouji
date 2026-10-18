/**
 * ToolCallItem.tsx — 单条工具调用条目（W803-D 自 ToolCallsCollapse 拆分）
 *
 * 职责边界：读取该条目的展开状态 → 判定渲染分支 → 交给对应面板。
 * 本组件**不认识**「多条汇总 / 收缩条 / 最新运行中」等布局概念（那些在上层）。
 *
 * 重构前这段逻辑是 `renderToolDetail(tool, index)`：一个 445 行的函数，参数里的
 * `index` 实际未被使用（历史遗留），六个分支各写一遍三态图标与输出块。
 */
import type { ToolCall } from '../../types';
import {
  getToolIcon,
  getToolRenderKind,
  getToolVisualState,
  formatToolInput,
} from './toolIcons';
import {
  SkillToolPanel,
  BashToolPanel,
  WebSearchToolPanel,
  WebFetchToolPanel,
  WriteToolPanel,
  GenericToolPanel,
  type ToolPanelProps,
} from './ToolCallPanels';

interface ToolCallItemProps {
  tool: ToolCall;
  expanded: boolean;
  onToggle: (toolId: string) => void;
}

export function ToolCallItem({ tool, expanded, onToggle }: ToolCallItemProps) {
  const visual = getToolIcon(tool.name);
  const input = tool.input || {};
  const state = getToolVisualState(tool.status, tool.isError);

  const panelProps: ToolPanelProps = {
    tool,
    state,
    visual,
    input,
    expanded,
    onToggle: () => onToggle(tool.id),
  };

  switch (getToolRenderKind(tool.name)) {
    case 'skill':
      return <SkillToolPanel {...panelProps} />;
    case 'bash':
      return <BashToolPanel {...panelProps} />;
    case 'websearch':
      return <WebSearchToolPanel {...panelProps} />;
    case 'webfetch':
      return <WebFetchToolPanel {...panelProps} />;
    case 'write':
      return <WriteToolPanel {...panelProps} />;
    default:
      // 通用面板额外需要序列化后的输入串（Skill 之外的未知工具都走这里）
      return <GenericToolPanel {...panelProps} inputStr={formatToolInput(tool.input)} />;
  }
}
