import { useRef, useCallback } from 'react';
import { Select, Tooltip } from 'tdesign-react';
import { ChatSender } from '@tdesign-react/chat';
import { ChevronDownIcon, LockOnIcon, LockOffIcon, EditIcon, TaskIcon } from 'tdesign-icons-react';
import { Model, PermissionMode } from '../types';

interface ChatInputProps {
  inputValue: string;
  selectedModel: string;
  models: Model[];
  isLoading: boolean;
  /** W1150：模型列表加载中（输入框占位提示「正在获取模型」）。 */
  modelsLoading: boolean;
  permissionMode: PermissionMode;
  onSend: (message: string) => void;
  onStop: () => void;
  onChange: (value: string) => void;
  onModelChange: (modelId: string) => void;
  onPermissionModeChange: (mode: PermissionMode) => void;
}

// 权限模式配置（W1150：颜色改走主题令牌——旧字面 hex 在深色模式下未经调整）
const PERMISSION_MODE_CONFIG: Record<PermissionMode, {
  label: string;
  shortLabel: string;
  icon: React.ReactNode;
  color: string;
  description: string;
}> = {
  'default': {
    label: '默认模式',
    shortLabel: '默认',
    icon: <LockOnIcon />,
    color: 'var(--td-brand-color)',
    description: '每次操作都需要确认'
  },
  'acceptEdits': {
    label: '自动编辑',
    shortLabel: '自动编辑',
    icon: <EditIcon />,
    color: 'var(--td-success-color)',
    description: '自动允许文件编辑操作'
  },
  'plan': {
    label: '仅规划',
    shortLabel: '仅规划',
    icon: <TaskIcon />,
    color: 'var(--td-warning-color)',
    description: '只生成计划，不执行操作'
  },
  'bypassPermissions': {
    label: '全部允许',
    shortLabel: '全部允许',
    icon: <LockOffIcon />,
    color: 'var(--td-error-color)',
    description: '跳过所有权限确认（危险）'
  },
};

export function ChatInput({
  inputValue,
  selectedModel,
  models,
  isLoading,
  modelsLoading,
  permissionMode,
  onSend,
  onStop,
  onChange,
  onModelChange,
  onPermissionModeChange,
}: ChatInputProps) {
  const chatSenderRef = useRef<any>(null);

  const handleSend = useCallback((e: any) => {
    const content = e?.detail?.message || e?.detail || e?.message || inputValue;
    if (content && typeof content === 'string' && content.trim() && selectedModel) {
      onSend(content.trim());
    } else if (inputValue.trim() && selectedModel) {
      onSend(inputValue.trim());
    }
  }, [inputValue, selectedModel, onSend]);

  const handleChange = useCallback((e: any) => {
    const value = e?.detail ?? e ?? '';
    onChange(typeof value === 'string' ? value : '');
  }, [onChange]);

  const currentModeConfig = PERMISSION_MODE_CONFIG[permissionMode];

  return (
    <div 
      className="px-4 pb-6 pt-4"
      style={{ 
        backgroundColor: 'var(--td-bg-color-page)'
      }}
    >
      <div className="max-w-3xl mx-auto">
        <ChatSender
          ref={chatSenderRef}
          value={inputValue}
          // W1150：禁用态给原因（旧实现模型未就绪时输入框灰着但无解释）
          placeholder={
            !selectedModel
              ? (modelsLoading ? '正在获取模型…' : (models.length === 0 ? '未获取到模型，请检查引擎配置' : '请先选择模型'))
              : '输入消息...'
          }
          disabled={!selectedModel}
          loading={isLoading}
          autosize={{ minRows: 1, maxRows: 6 }}
          actions={['send']}
          onSend={handleSend}
          onStop={onStop}
          onChange={handleChange}
        >
          {/* 模型选择器和权限模式选择器放在 footer-prefix 插槽 */}
          <div slot="footer-prefix" className="flex items-center gap-2">
            {/* 模型选择器 */}
            <Select
              value={selectedModel}
              onChange={(value) => onModelChange(value as string)}
              placeholder="选择模型"
              size="small"
              style={{ width: 160 }}
              filterable
              borderless
              // W1150：空列表给解释（旧实现 models 为空时下拉展开是空白面板）
              empty={modelsLoading ? '正在获取模型…' : '未获取到模型，请检查引擎配置'}
              suffixIcon={<ChevronDownIcon />}
            >
              {models.map(model => (
                <Select.Option key={model.modelId} value={model.modelId} label={model.name} />
              ))}
            </Select>
            
            {/* 分隔线 */}
            <div 
              className="h-4 w-px"
              style={{ backgroundColor: 'var(--td-component-stroke)' }}
            />
            
            {/* 权限模式选择器 */}
            <Tooltip content={currentModeConfig.description} placement="top">
              <Select
                value={permissionMode}
                onChange={(value) => onPermissionModeChange(value as PermissionMode)}
                size="small"
                style={{ width: 110 }}
                borderless
                suffixIcon={<ChevronDownIcon />}
                prefixIcon={
                  <span style={{ color: currentModeConfig.color }}>
                    {currentModeConfig.icon}
                  </span>
                }
                popupProps={{
                  overlayInnerStyle: { width: 140 }
                }}
              >
                {(Object.keys(PERMISSION_MODE_CONFIG) as PermissionMode[]).map(mode => {
                  const config = PERMISSION_MODE_CONFIG[mode];
                  return (
                    <Select.Option 
                      key={mode} 
                      value={mode} 
                      label={config.shortLabel}
                    >
                      <div className="flex items-center gap-2">
                        <span style={{ color: config.color }}>{config.icon}</span>
                        <span>{config.shortLabel}</span>
                      </div>
                    </Select.Option>
                  );
                })}
              </Select>
            </Tooltip>
          </div>
        </ChatSender>
      </div>
    </div>
  );
}
