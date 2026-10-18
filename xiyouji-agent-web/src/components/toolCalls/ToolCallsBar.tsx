/**
 * ToolCallsBar.tsx — 工具调用汇总条（W803-D 自 ToolCallsCollapse 提取）
 *
 * 职责边界：两种「不展开明细」的横条——
 *  ① `ToolCallsCollapseBar`：整组工具的收缩条（左侧状态+文案+计数，右侧图标汇总）；
 *  ② `PreviousStepsBar`：连续调用场景里「N 个步骤已完成」的回看条。
 *
 * 提取动因：重构前这两条横条内联在 JSX 里，与条目渲染、展开状态、数据推导挤在同一组件，
 * 且两处的容器样式（component 底色 + hover:opacity-80 + 圆角）逐字重复。
 */
import { Loading } from 'tdesign-react';
import { ChevronDownIcon, ChevronUpIcon, CheckCircleFilledIcon, CloseCircleFilledIcon } from 'tdesign-icons-react';
import type { LucideIcon } from 'lucide-react';

/** 汇总条里的一类工具（图标 + 颜色 + 该类的条数）。 */
export interface ToolSummaryEntry {
  type: string;
  icon: LucideIcon;
  color: string;
  count: number;
}

/** 整组收缩条：点击切换整组展开/收起。 */
export function ToolCallsCollapseBar({
  isExpanded,
  hasRunning,
  hasError,
  toolCount,
  summary,
  onToggle,
}: {
  isExpanded: boolean;
  hasRunning: boolean;
  hasError: boolean;
  toolCount: number;
  summary: ToolSummaryEntry[];
  onToggle: () => void;
}) {
  return (
    <div
      className="flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer transition-all hover:opacity-80"
      style={{ backgroundColor: 'var(--td-bg-color-component)' }}
      onClick={onToggle}
    >
      {/* 左侧：展开图标 + 状态图标 + 文字 + 数量 */}
      <div className="flex items-center gap-1.5">
        {isExpanded ? (
          <ChevronUpIcon size={16} style={{ color: 'var(--td-text-color-secondary)' }} />
        ) : (
          <ChevronDownIcon size={16} style={{ color: 'var(--td-text-color-secondary)' }} />
        )}
        {hasRunning ? (
          <Loading size="small" />
        ) : hasError ? (
          <CloseCircleFilledIcon size={16} style={{ color: 'var(--td-error-color)' }} />
        ) : (
          <CheckCircleFilledIcon size={16} style={{ color: 'var(--td-success-color)' }} />
        )}
        <span className="text-sm" style={{ color: 'var(--td-text-color-primary)' }}>
          {hasRunning ? '执行中...' : isExpanded ? '收起步骤' : '查看步骤'}
        </span>
        {toolCount > 1 && (
          <span className="text-xs" style={{ color: 'var(--td-text-color-placeholder)' }}>
            ({toolCount})
          </span>
        )}
      </div>

      {/* 右侧：工具图标汇总 */}
      <div className="flex items-center gap-1">
        <ToolSummaryBadges summary={summary} showCount />
      </div>
    </div>
  );
}

/**
 * 已完成步骤的回看条（点击展开整组明细）。
 * `summary` 由调用方预先剔除「正在运行的最后一类」（原实现为 `summary.slice(0, -1)`）。
 */
export function PreviousStepsBar({
  previousCount,
  summary,
  onExpand,
}: {
  previousCount: number;
  summary: ToolSummaryEntry[];
  onExpand: () => void;
}) {
  return (
    <div
      className="flex items-center justify-between gap-1.5 px-3 py-1.5 rounded-lg cursor-pointer transition-all hover:opacity-80"
      style={{ backgroundColor: 'var(--td-bg-color-component)' }}
      onClick={onExpand}
    >
      <div className="flex items-center gap-1.5">
        <ChevronDownIcon size={14} style={{ color: 'var(--td-text-color-placeholder)' }} />
        <CheckCircleFilledIcon size={14} style={{ color: 'var(--td-success-color)' }} />
        <span className="text-xs" style={{ color: 'var(--td-text-color-secondary)' }}>
          {previousCount} 个步骤已完成
        </span>
      </div>
      {/* 已完成工具的图标汇总 */}
      <div className="flex items-center gap-1">
        {summary.map(({ type, icon: Icon, color }) => (
          <Icon key={type} size={12} style={{ color }} />
        ))}
      </div>
    </div>
  );
}

/** 图标汇总徽标：`showCount` 为真且计数 >1 时附数字（收缩条用；回看条只要图标）。 */
function ToolSummaryBadges({ summary, showCount }: { summary: ToolSummaryEntry[]; showCount?: boolean }) {
  return (
    <>
      {summary.map(({ type, icon: Icon, color, count }) => (
        <div
          key={type}
          className="flex items-center gap-0.5 px-1.5 py-0.5 rounded"
          style={{ backgroundColor: 'var(--td-bg-color-secondarycontainer)' }}
          title={`${type} x${count}`}
        >
          <Icon size={12} style={{ color }} />
          {showCount && count > 1 && (
            <span className="text-xs" style={{ color: 'var(--td-text-color-placeholder)', fontSize: '10px' }}>
              {count}
            </span>
          )}
        </div>
      ))}
    </>
  );
}
