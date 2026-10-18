/**
 * toolIcons.ts — 工具调用展示元数据（W803-D 自 ToolCallsCollapse 提取）
 *
 * 职责边界：把「工具名 → 图标 / 颜色 / 汇总分类 / 渲染分支」的映射集中一处。
 * 重构前这些映射散落在 756 行组件的两个函数 + `renderToolDetail` 的一串
 * `toolNameLower === '...'` 判定里——同一条映射要改三个地方，且汇总条与条目
 * 明细可能给出不一致的图标。
 *
 * 注意：这里的工具名是**引擎工具名**（read_file / write_file / run_command …），
 * 判定一律走小写归一（历史兼容 PascalCase 与带下划线两种写法）。
 */
import {
  Terminal,
  Sparkles,
  Search,
  Globe,
  Wrench,
  FileText,
  FolderSearch,
  Edit,
  Trash2,
  Eye,
  Image,
  Zap,
  type LucideIcon,
} from 'lucide-react';

/** 工具图标与颜色（`color` 为 CSS 值，直接进 style，禁用主题令牌之外的字面色）。 */
export interface ToolVisual {
  icon: LucideIcon;
  color: string;
}

/** 汇总条用的工具大类（同一类只出一个徽标 + 计数）。 */
export type ToolType =
  | 'skill'
  | 'bash'
  | 'websearch'
  | 'webfetch'
  | 'write'
  | 'read'
  | 'edit'
  | 'delete'
  | 'search'
  | 'image'
  | 'task'
  | 'other';

/**
 * 工具名 → 图标与颜色。
 * 之所以保留逐个 `if` 而非查表：原实现的判定顺序即优先级（如 `search|grep` 先于
 * `listdir|ls` 命中），改成表会改变 `ls` 这类同时匹配多条的落点。
 */
export function getToolIcon(toolName: string): ToolVisual {
  const name = toolName.toLowerCase();

  // Skill 技能调用
  if (name === 'skill') {
    return { icon: Sparkles, color: 'var(--td-warning-color)' };
  }
  // Bash 命令执行
  if (name === 'bash') {
    return { icon: Terminal, color: 'var(--td-text-color-secondary)' };
  }
  // Web 搜索
  if (name === 'websearch') {
    return { icon: Search, color: '#1890ff' };
  }
  // Web 抓取
  if (name === 'webfetch') {
    return { icon: Globe, color: '#52c41a' };
  }
  // 写入文件
  if (name === 'write') {
    return { icon: FileText, color: '#fa8c16' };
  }
  // 读取文件
  if (name === 'read' || name === 'readfile') {
    return { icon: Eye, color: '#722ed1' };
  }
  // 编辑文件
  if (name === 'edit' || name === 'editfile') {
    return { icon: Edit, color: '#fa8c16' };
  }
  // 删除文件
  if (name === 'delete' || name === 'deletefile') {
    return { icon: Trash2, color: '#ff4d4f' };
  }
  // 搜索
  if (name === 'search' || name === 'grep') {
    return { icon: FolderSearch, color: '#13c2c2' };
  }
  // 列出目录
  if (name === 'listdir' || name === 'ls') {
    return { icon: FolderSearch, color: '#13c2c2' };
  }
  // 图片生成
  if (name === 'imagegen') {
    return { icon: Image, color: '#f5222d' };
  }
  // 任务
  if (name === 'task') {
    return { icon: Zap, color: '#faad14' };
  }

  // 默认图标
  return { icon: Wrench, color: 'var(--td-text-color-secondary)' };
}

/** 工具名 → 汇总大类（用于收缩条右侧的图标汇总与去重计数）。 */
export function getToolType(toolName: string): ToolType {
  const name = toolName.toLowerCase();

  if (name === 'skill') return 'skill';
  if (name === 'bash') return 'bash';
  if (name === 'websearch') return 'websearch';
  if (name === 'webfetch') return 'webfetch';
  if (name === 'write') return 'write';
  if (name === 'read' || name === 'readfile') return 'read';
  if (name === 'edit' || name === 'editfile') return 'edit';
  if (name === 'delete' || name === 'deletefile') return 'delete';
  if (name === 'search' || name === 'grep' || name === 'listdir') return 'search';
  if (name === 'imagegen') return 'image';
  if (name === 'task') return 'task';

  return 'other';
}

/**
 * 条目渲染分支：决定走哪种专用面板（skill / bash / websearch / webfetch / write），
 * 未命中即走通用面板。抽出来的理由是「分支判定」与「分支渲染」原先是同一段 400 行代码。
 */
export type ToolRenderKind = 'skill' | 'bash' | 'websearch' | 'webfetch' | 'write' | 'generic';

export function getToolRenderKind(toolName: string): ToolRenderKind {
  const name = toolName.toLowerCase();
  if (name === 'skill') return 'skill';
  if (name === 'bash') return 'bash';
  if (name === 'websearch') return 'websearch';
  if (name === 'webfetch') return 'webfetch';
  if (name === 'write') return 'write';
  return 'generic';
}

/** 工具条目的处理态（running / 成功 / 失败），统一由 status + isError 推出。 */
export interface ToolVisualState {
  isRunning: boolean;
  isCompleted: boolean;
  isError: boolean;
}

export function getToolVisualState(status: string, isErrorFlag?: boolean): ToolVisualState {
  const isRunning = status === 'running';
  return {
    isRunning,
    isCompleted: status === 'completed',
    isError: status === 'error' || Boolean(isErrorFlag),
  };
}

/** 结果文本截断（条目内最多 500 字，超出补省略号）。 */
export function truncate(text: string, max: number): string {
  return text.length > max ? text.slice(0, max) + '...' : text;
}

/** 通用面板的输入序列化（对象 → 缩进 JSON；空对象返回 null 以隐藏整块）。 */
export function formatToolInput(inputObj: Record<string, unknown> | undefined): string | null {
  if (!inputObj || Object.keys(inputObj).length === 0) return null;
  try {
    return JSON.stringify(inputObj, null, 2);
  } catch {
    return String(inputObj);
  }
}
