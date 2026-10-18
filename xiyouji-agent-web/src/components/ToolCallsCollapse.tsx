/**
 * ToolCallsCollapse.tsx — 工具调用折叠区（W803-D 拆分后的编排层）
 *
 * 职责边界：只做「数据推导 + 三种布局选择」，渲染细节下沉到同目录子模块：
 *   ToolCallItem.tsx    单条条目（分支分派）
 *   ToolCallPanels.tsx  六类工具各自的展示面板
 *   ToolCallParts.tsx   无状态公共片段（状态图标/标题行/输出块/外框）
 *   ToolCallsBar.tsx    整组收缩条 + 已完成回看条
 *   toolIcons.ts        工具名 → 图标/颜色/汇总分类/渲染分支
 *
 * 三种布局（与重构前逐字一致）：
 *   ① 单条工具：运行中直接展开明细；已完成走收缩条 + 可展开明细；
 *   ② 多条且运行中且未展开：只显示回看条 + 最新运行中的那条；
 *   ③ 多条且（无运行中或已展开）：收缩条 + 全部明细。
 *
 * 组件 props 与可观察 DOM（类名/style/文案）保持不变。
 */
import { useState, useEffect, useMemo } from 'react';
import { ToolCall } from '../types';
import { getToolIcon, getToolType } from './toolCalls/toolIcons';
import { ToolCallItem } from './toolCalls/ToolCallItem';
import {
  ToolCallsCollapseBar,
  PreviousStepsBar,
  type ToolSummaryEntry,
} from './toolCalls/ToolCallsBar';

interface ToolCallsCollapseProps {
  toolCalls: ToolCall[];
  isStreaming?: boolean;
}

export function ToolCallsCollapse({ toolCalls, isStreaming = false }: ToolCallsCollapseProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  // 可折叠工具的展开状态（按 toolId 管理）
  const [expandedToolIds, setExpandedToolIds] = useState<Set<string>>(new Set());

  // 切换工具的展开状态
  const toggleToolExpanded = (toolId: string) => {
    setExpandedToolIds(prev => {
      const next = new Set(prev);
      if (next.has(toolId)) {
        next.delete(toolId);
      } else {
        next.add(toolId);
      }
      return next;
    });
  };

  // 是否所有工具都已完成
  const allCompleted = toolCalls.every(tool => tool.status === 'completed' || tool.status === 'error');

  // 是否有任何工具正在运行
  const hasRunning = toolCalls.some(tool => tool.status === 'running');

  // 是否有失败的工具
  const hasError = toolCalls.some(tool => tool.status === 'error');

  // 汇总工具类型（去重）
  const toolSummary = useMemo<ToolSummaryEntry[]>(() => {
    const typeMap = new Map<string, ToolSummaryEntry>();
    toolCalls.forEach(tool => {
      const type = getToolType(tool.name);
      const { icon, color } = getToolIcon(tool.name);
      const existing = typeMap.get(type);
      if (existing) {
        existing.count++;
      } else {
        typeMap.set(type, { type, icon, color, count: 1 });
      }
    });
    return Array.from(typeMap.values());
  }, [toolCalls]);

  // 找到最新的正在运行的工具（用于连续调用时展示）
  const latestRunningTool = useMemo(() => {
    for (let i = toolCalls.length - 1; i >= 0; i--) {
      if (toolCalls[i].status === 'running') {
        return { tool: toolCalls[i], index: i };
      }
    }
    return null;
  }, [toolCalls]);

  // 当有新的工具调用开始时，如果之前是展开状态且所有都完成了，保持折叠
  useEffect(() => {
    if (toolCalls.length === 1 && hasRunning) {
      setIsExpanded(true);
    } else if (allCompleted && !isStreaming) {
      setIsExpanded(false);
    }
  }, [toolCalls.length, hasRunning, allCompleted, isStreaming]);

  const renderToolDetail = (tool: ToolCall) => (
    <ToolCallItem
      key={tool.id}
      tool={tool}
      expanded={expandedToolIds.has(tool.id)}
      onToggle={toggleToolExpanded}
    />
  );

  const collapseBar = (
    <ToolCallsCollapseBar
      isExpanded={isExpanded}
      hasRunning={hasRunning}
      hasError={hasError}
      toolCount={toolCalls.length}
      summary={toolSummary}
      onToggle={() => setIsExpanded(!isExpanded)}
    />
  );

  // 渲染最新运行中的工具（用于连续调用场景）
  const renderLatestRunningTool = () => {
    if (!latestRunningTool) return null;

    const { tool, index } = latestRunningTool;
    const previousCount = index;

    return (
      <div className="space-y-2">
        {previousCount > 0 && (
          <PreviousStepsBar
            previousCount={previousCount}
            summary={toolSummary.slice(0, -1)}
            onExpand={() => setIsExpanded(true)}
          />
        )}

        {renderToolDetail(tool)}
      </div>
    );
  };

  // 单个工具调用的情况
  if (toolCalls.length === 1) {
    const tool = toolCalls[0];

    if (tool.status === 'running') {
      return <div className="w-full">{renderToolDetail(tool)}</div>;
    }

    return (
      <div className="w-full space-y-2">
        {collapseBar}
        {isExpanded && <div className="space-y-2 pl-2">{renderToolDetail(tool)}</div>}
      </div>
    );
  }

  // 多个工具调用的情况
  if (hasRunning && !isExpanded) {
    return <div className="w-full">{renderLatestRunningTool()}</div>;
  }

  return (
    <div className="w-full space-y-2">
      {collapseBar}
      {isExpanded && <div className="space-y-2 pl-2">{toolCalls.map(tool => renderToolDetail(tool))}</div>}
    </div>
  );
}

export default ToolCallsCollapse;
