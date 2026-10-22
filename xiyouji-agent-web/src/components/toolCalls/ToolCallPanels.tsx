/**
 * ToolCallPanels.tsx — 工具调用条目的分支渲染（W803-D 自 ToolCallsCollapse 拆分）
 *
 * 职责边界：一类工具一个面板组件，各自只关心「这种工具的标题写什么、展开后显示什么」。
 * 重构前这六种分支是 `renderToolDetail` 里六个连排的 `if (...) { return (...) }`，
 * 共约 400 行挤在一个函数体内——改 Bash 的展示要滑过 Skill/WebSearch/WebFetch 的 JSX。
 *
 * 文案与结构逐字保留（用户可见面）：`使用 {skill} 技能` / `搜索: ` / `获取网页内容` /
 * `写入 {filename}` / `执行命令` / `$ ` / `URL: ` / `路径: ` / `内容:` 等一律不动。
 */
import type { ToolCall } from '../../types';
import {
  ToolCallShell,
  ToolCallHeader,
  ToolCallPanel,
  ToolResultPanel,
} from './ToolCallParts';
import { truncate, type ToolVisual } from './toolIcons';
import type { ToolVisualState } from './toolIcons';

/** 所有面板共用的入口参数（由 ToolCallItem 组装，面板本身不认识布局状态）。 */
export interface ToolPanelProps {
  tool: ToolCall;
  state: ToolVisualState;
  visual: ToolVisual;
  input: Record<string, unknown>;
  /** 该条目当前是否展开（无展开概念的分支忽略此值）。 */
  expanded: boolean;
  /** 切换展开（无展开概念的分支忽略此值）。 */
  onToggle: () => void;
}

/**
 * Skill：标题为「使用 X 技能」，无展开交互；参数与结果各占一块。
 */
export function SkillToolPanel({ tool, state, visual, input }: ToolPanelProps) {
  const skillName = (input.skill || 'Unknown') as string;
  const skillArgs = (input.args || '') as string;

  return (
    <ToolCallShell>
      <ToolCallHeader
        state={state}
        icon={visual.icon}
        iconColor={visual.color}
        phrases={{ running: '执行中...' }}
        title={
          <>
            使用 <span style={{ color: 'var(--td-brand-color)' }}>{skillName}</span> 技能
          </>
        }
        titleClassName="flex-1 text-sm font-medium"
      />

      {/* Skill 参数块：历史上非等宽（与结果块不同），逐字保留 */}
      {skillArgs && (
        <ToolCallPanel mono={false} maxHeight="max-h-24" content={truncate(String(skillArgs), 300)} />
      )}

      {tool.result && <ToolResultPanel result={tool.result} isError={state.isError} successLabel="结果: " />}
    </ToolCallShell>
  );
}

/**
 * Bash：标题取 description（缺省「执行命令」），展开后显示 `$ command`。
 */
export function BashToolPanel({ tool, state, visual, input, expanded, onToggle }: ToolPanelProps) {
  const command = (input.command || '') as string;
  const description = (input.description || '执行命令') as string;

  return (
    <ToolCallShell>
      <ToolCallHeader
        state={state}
        icon={visual.icon}
        iconColor={visual.color}
        phrases={{ running: '执行中...' }}
        title={description || '执行命令'}
        expandable={Boolean(command)}
        expanded={expanded}
        onToggle={onToggle}
      />

      {expanded && command && (
        <ToolCallPanel
          leading={<span style={{ color: 'var(--td-text-color-placeholder)' }}>$ </span>}
          content={truncate(command, 500)}
        />
      )}

      {tool.result && <ToolResultPanel result={tool.result} isError={state.isError} successLabel="输出: " />}
    </ToolCallShell>
  );
}

/**
 * WebSearch：标题为「搜索: {query}」，无展开交互。
 */
export function WebSearchToolPanel({ tool, state, visual, input }: ToolPanelProps) {
  const query = (input.query || '') as string;

  return (
    <ToolCallShell>
      <ToolCallHeader
        state={state}
        icon={visual.icon}
        iconColor={visual.color}
        phrases={{ running: '搜索中...' }}
        title={
          <>
            搜索: <span style={{ color: '#1890ff' }}>{query || '...'}</span>
          </>
        }
        titleClassName="flex-1 text-sm font-medium"
      />

      {tool.result && <ToolResultPanel result={tool.result} isError={state.isError} successLabel="结果: " />}
    </ToolCallShell>
  );
}

/**
 * WebFetch：标题取 prompt（缺省「获取网页内容」），展开后显示 URL。
 */
export function WebFetchToolPanel({ tool, state, visual, input, expanded, onToggle }: ToolPanelProps) {
  const url = (input.url || '') as string;
  const prompt = (input.prompt || '获取网页内容') as string;

  return (
    <ToolCallShell>
      <ToolCallHeader
        state={state}
        icon={visual.icon}
        iconColor={visual.color}
        phrases={{ running: '获取中...' }}
        title={prompt}
        expandable={Boolean(url)}
        expanded={expanded}
        onToggle={onToggle}
      />

      {/* 展开显示 URL（不截断·URL 本体即信息；历史上此块非等宽且不限高，逐字保留） */}
      {expanded && url && (
        <ToolCallPanel
          maxHeight={null}
          mono={false}
          leading={<span style={{ color: 'var(--td-text-color-placeholder)' }}>URL: </span>}
          content={url}
        />
      )}

      {tool.result && <ToolResultPanel result={tool.result} isError={state.isError} successLabel="内容: " />}
    </ToolCallShell>
  );
}

/**
 * Write：标题为「写入 {文件名}」（title 属性给全路径），展开后显示完整路径与内容（1000 字上限）。
 */
export function WriteToolPanel({ tool, state, visual, input, expanded, onToggle }: ToolPanelProps) {
  const filePath = (input.file_path || '') as string;
  const content = (input.content || '') as string;
  // 提取文件名（仅用于标题展示）
  const fileName = filePath.split('/').pop() || filePath;

  return (
    <ToolCallShell>
      <ToolCallHeader
        state={state}
        icon={visual.icon}
        iconColor={visual.color}
        phrases={{ running: '写入中...' }}
        title={
          <>
            写入 <span style={{ color: '#fa8c16' }}>{fileName}</span>
          </>
        }
        titleAttrs={{ title: filePath }}
        expandable={Boolean(content)}
        expanded={expanded}
        onToggle={onToggle}
      />

      {expanded && (
        <ToolCallPanel maxHeight="max-h-48">
          <div className="mb-2" style={{ color: 'var(--td-text-color-placeholder)' }}>
            路径: {filePath}
          </div>
          {content && (
            <div>
              <span style={{ color: 'var(--td-text-color-placeholder)' }}>内容:</span>
              <pre className="mt-1 whitespace-pre-wrap">{truncate(content, 1000)}</pre>
            </div>
          )}
        </ToolCallPanel>
      )}

      {tool.result && <ToolResultPanel result={tool.result} isError={state.isError} successLabel="结果: " />}
    </ToolCallShell>
  );
}

/**
 * 通用面板：标题直接用工具名；无展开交互，输入以缩进 JSON 展示（300 字上限）。
 */
export function GenericToolPanel({ tool, state, visual, inputStr }: ToolPanelProps & { inputStr: string | null }) {
  return (
    <ToolCallShell>
      <ToolCallHeader
        state={state}
        icon={visual.icon}
        iconColor={visual.color}
        phrases={{ running: '执行中...' }}
        title={tool.name}
      />

      {inputStr && (
        <ToolCallPanel
          maxHeight="max-h-24"
          leading={<span style={{ color: 'var(--td-text-color-placeholder)' }}>输入: </span>}
          content={truncate(inputStr, 300)}
        />
      )}

      {tool.result && <ToolResultPanel result={tool.result} isError={state.isError} successLabel="结果: " />}
    </ToolCallShell>
  );
}
