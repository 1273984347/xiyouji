/**
 * ToolCallParts.tsx — 工具调用条目的公共展示件（W803-D 自 ToolCallsCollapse 提取）
 *
 * 职责边界：只做**无状态**的展示片段，不持有展开状态、不判定工具类型。
 *
 * 提取动因：重构前 `renderToolDetail` 里 6 个渲染分支各自重复了同一套骨架——
 *   ① 三态状态图标（Loading / CheckCircleFilledIcon / CloseCircleFilledIcon）出现 6 次；
 *   ② 「输出块」的 style（font-mono / 断行 / max-h / border-t / 三处 CSS 变量）出现 12 次；
 *   ③ 标题行尾部「执行中... / 失败 / 完成」的短语逐字重复 6 次。
 * 其中 ② 的四处 CSS 变量与 max-h 只要有一处写错，条目高度/配色就会与其他条目不一致——
 * 这正是「抽复用模块」要消除的风险，而不是单纯为了少打字。
 */
import { Loading } from 'tdesign-react';
import { ChevronDownIcon, ChevronUpIcon, CheckCircleFilledIcon, CloseCircleFilledIcon } from 'tdesign-icons-react';
import type { LucideIcon } from 'lucide-react';
import { truncate, type ToolVisualState } from './toolIcons';

/** 尾部短语：不同分支用词不同（渲染 / 搜索 / 获取 / 写入 / 执行），故由调用方传入。 */
export interface StatusPhrases {
  running: string;
}

/** 三态状态图标：运行中转圈、成功打勾、其余（含失败）红叉。 */
export function ToolStatusIcon({ state }: { state: ToolVisualState }) {
  if (state.isRunning) return <Loading size="small" />;
  if (state.isCompleted && !state.isError) {
    return <CheckCircleFilledIcon style={{ color: 'var(--td-success-color)' }} />;
  }
  return <CloseCircleFilledIcon style={{ color: 'var(--td-error-color)' }} />;
}

/** 尾部状态短语：运行中按分支用词，失败固定「失败」，其余「完成」。 */
export function ToolStatusText({ state, phrases }: { state: ToolVisualState; phrases: StatusPhrases }) {
  return (
    <span className="text-xs" style={{ color: 'var(--td-text-color-placeholder)' }}>
      {state.isRunning ? phrases.running : state.isError ? '失败' : '完成'}
    </span>
  );
}

/** 展开/收起箭头（仅有可展开内容时由调用方条件渲染）。 */
export function ExpandChevron({ expanded, size = 14 }: { expanded: boolean; size?: number }) {
  return expanded ? (
    <ChevronUpIcon size={size} style={{ color: 'var(--td-text-color-placeholder)' }} />
  ) : (
    <ChevronDownIcon size={size} style={{ color: 'var(--td-text-color-placeholder)' }} />
  );
}

/**
 * 条目外框：所有分支共用（圆角、溢出错位裁切、次级容器底色）。
 * `key` 由调用方在 map 处给出，故此处只接收 children。
 */
export function ToolCallShell({ children }: { children: React.ReactNode }) {
  return (
    <div
      className="rounded-lg overflow-hidden transition-all"
      style={{ backgroundColor: 'var(--td-bg-color-secondarycontainer)' }}
    >
      {children}
    </div>
  );
}

/**
 * 标题行：状态图标 + 工具图标 + 主文案 + 尾部短语 + 可选展开箭头。
 * `onClick` 存在时整行可点（即该分支支持展开），不存在时是纯展示行——这一差异即原实现
 * 「Bash/WebFetch/Write 可展开、Skill/WebSearch/通用 不可展开」的载体。
 */
export function ToolCallHeader({
  state,
  icon: ToolIcon,
  iconColor,
  title,
  phrases,
  expandable,
  expanded,
  onToggle,
  titleClassName = 'flex-1 text-sm font-medium truncate',
  titleAttrs,
  trailing,
}: {
  state: ToolVisualState;
  icon: LucideIcon;
  iconColor: string;
  title: React.ReactNode;
  phrases: StatusPhrases;
  expandable?: boolean;
  expanded?: boolean;
  onToggle?: () => void;
  titleClassName?: string;
  titleAttrs?: Record<string, unknown>;
  trailing?: React.ReactNode;
}) {
  return (
    <div
      className={onToggle ? 'flex items-center gap-2 px-3 py-2 cursor-pointer' : 'flex items-center gap-2 px-3 py-2'}
      onClick={onToggle}
    >
      <ToolStatusIcon state={state} />
      <ToolIcon size={16} style={{ color: iconColor }} />
      <span className={titleClassName} style={{ color: 'var(--td-text-color-primary)' }} {...titleAttrs}>
        {title}
      </span>
      <ToolStatusText state={state} phrases={phrases} />
      {trailing}
      {expandable && <ExpandChevron expanded={Boolean(expanded)} />}
    </div>
  );
}

/**
 * 详情/输出块：`border-t` 分隔的单色等宽文本区。
 * 两点变体维度（原 12 处内联样式的全部差异）：
 *  · `maxHeight` 用 Tailwind 类传入（历史取值：24/32/48 三档；null＝不加高度限制）；
 *  · `tone` 决定文字是错误红还是次级灰；
 *  · `mono` 为 false 时不加 `font-mono`——WebFetch 的 URL 块历史上就不是等宽（逐字保留）。
 */
export function ToolCallPanel({
  children,
  maxHeight = 'max-h-32',
  tone = 'muted',
  mono = true,
  leading,
  content,
}: {
  children?: React.ReactNode;
  maxHeight?: 'max-h-24' | 'max-h-32' | 'max-h-48' | null;
  tone?: 'muted' | 'error';
  mono?: boolean;
  /** 前缀标签（如「结果: 」「$ 」「URL: 」）；与 content 二选一或并用。 */
  leading?: React.ReactNode;
  /** 纯文本内容：按 500 字截断（与重构前 `slice(0,500) + '...'` 口径一致）。 */
  content?: string;
}) {
  const classes = [
    'px-3 py-2 text-xs',
    mono ? 'font-mono' : '',
    'whitespace-pre-wrap break-all',
    maxHeight ?? '',
    // 不限高的分支历史上也没有 overflow-y-auto（URL 块）——两者绑定出现，不拆开
    maxHeight ? 'overflow-y-auto' : '',
    'border-t',
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div
      className={classes}
      style={{
        color: tone === 'error' ? 'var(--td-error-color)' : 'var(--td-text-color-secondary)',
        borderColor: 'var(--td-component-stroke)',
        backgroundColor: 'var(--td-bg-color-container)',
      }}
    >
      {leading}
      {content !== undefined && truncate(content, 500)}
      {children}
    </div>
  );
}

/** 结果块的常用组合：前缀标签按是否出错切换「错误: 」/自定义成功词。 */
export function ToolResultPanel({
  result,
  isError,
  successLabel,
}: {
  result: string;
  isError: boolean;
  /** 成功态标签（结果 / 输出 / 内容）。 */
  successLabel: string;
}) {
  return (
    <ToolCallPanel
      tone={isError ? 'error' : 'muted'}
      leading={<span style={{ color: 'var(--td-text-color-placeholder)' }}>{isError ? '错误: ' : successLabel}</span>}
      content={result}
    />
  );
}
