import { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Model, Session, PermissionMode, CustomAgent, PermissionRequest } from '../types';
import { NewChatView } from '../components/NewChatView';
import { ChatMessages } from '../components/ChatMessages';
import { ChatInput } from '../components/ChatInput';

interface ChatPageProps {
  currentSession: Session | undefined;
  models: Model[];
  selectedModel: string;
  agents: CustomAgent[];
  isLoading: boolean;
  /** W1150：模型列表加载中（输入框占位提示用）。 */
  modelsLoading: boolean;
  /** W1150：当前会话的消息是否正在拉取（切换历史会话期间防「新对话」落地页闪现）。 */
  messagesLoading: boolean;
  inputValue: string;
  permissionRequest: PermissionRequest | null;
  permissionMode: PermissionMode;
  onSendMessage: (message: string, newChatOptions?: NewChatOptions, onNavigate?: (path: string, opts?: { replace?: boolean }) => void) => void;
  onStop: () => void;
  onInputChange: (value: string) => void;
  onModelChange: (modelId: string) => void;
  onPermissionAllow: () => void;
  onPermissionDeny: () => void;
  onPermissionModeChange: (mode: PermissionMode) => void;
}

interface NewChatOptions {
  agentId: string;
  cwd: string;
  permissionMode: PermissionMode;
}

export function ChatPage({
  currentSession,
  models,
  selectedModel,
  agents,
  isLoading,
  modelsLoading,
  messagesLoading,
  inputValue,
  permissionRequest,
  permissionMode,
  onSendMessage,
  onStop,
  onInputChange,
  onModelChange,
  onPermissionAllow,
  onPermissionDeny,
  onPermissionModeChange,
}: ChatPageProps) {
  const navigate = useNavigate();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // 新对话页面状态
  const [newChatAgentId, setNewChatAgentId] = useState('default');
  // W1150：工作目录默认空（留空 = 使用后端默认）——旧默认硬编码开发机路径
  // 'D:/1/xiyouji'，其他环境会静默携带无效 cwd 建会话
  const [newChatCwd, setNewChatCwd] = useState('');

  // 自动滚动到底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [currentSession?.messages]);

  // 处理发送消息
  const handleSend = useCallback((message: string) => {
    if (!currentSession) {
      // 新对话
      onSendMessage(message, {
        agentId: newChatAgentId,
        cwd: newChatCwd,
        permissionMode: permissionMode,
      }, (path, opts) => {
        // 重置新对话选项
        setNewChatAgentId('default');
        setNewChatCwd('');
        navigate(path, opts);
      });
    } else {
      onSendMessage(message);
    }
  }, [currentSession, newChatAgentId, newChatCwd, permissionMode, onSendMessage, navigate]);

  // W1150：消息在途拉取期间不显示「新对话」落地页——旧判据只看 messages.length===0，
  // 切换历史会话时异步拉取未完成 ⇒ 先闪现落地页再跳回对话
  const showNewChatView = !messagesLoading && (!currentSession || currentSession.messages.length === 0);
  const showMessagesLoading = messagesLoading && (!currentSession || currentSession.messages.length === 0);

  return (
    <>
      {/* 消息区域 */}
      <div className="flex-1 overflow-y-auto p-6">
        {showMessagesLoading ? (
          <div className="flex-1 flex items-center justify-center h-full" role="status" aria-label="会话消息加载中">
            <div
              className="animate-pulse flex flex-col items-center gap-3"
              style={{ color: 'var(--td-text-color-placeholder)' }}
            >
              <span className="text-sm">正在加载会话消息…</span>
            </div>
          </div>
        ) : showNewChatView ? (
          <NewChatView
            agents={agents}
            models={models}
            selectedModel={selectedModel}
            newChatAgentId={newChatAgentId}
            newChatCwd={newChatCwd}
            newChatPermissionMode={permissionMode}
            onSelectModel={onModelChange}
            onSelectAgent={setNewChatAgentId}
            onSetCwd={setNewChatCwd}
            onSetPermissionMode={onPermissionModeChange}
          />
        ) : (
          <ChatMessages
            messages={currentSession!.messages}
            models={models}
            messagesEndRef={messagesEndRef}
            // W808：反馈接口需要 sessionId（服务端三字段齐备校验）——此前未传，赞/踩恒 400
            sessionId={currentSession!.id}
            onRegenerate={(msg) => {
              const ms = currentSession!.messages;
              const idx = ms.findIndex(x => x.id === msg.id);
              const prevUser = [...ms.slice(0, idx)].reverse().find(x => x.role === 'user');
              if (prevUser) onSendMessage(prevUser.content);
            }}
            permissionRequest={permissionRequest}
            onPermissionAllow={onPermissionAllow}
            onPermissionDeny={onPermissionDeny}
          />
        )}
      </div>

      {/* 输入区域 */}
      <ChatInput
        inputValue={inputValue}
        selectedModel={selectedModel}
        models={models}
        isLoading={isLoading}
        modelsLoading={modelsLoading}
        permissionMode={permissionMode}
        onSend={handleSend}
        onStop={onStop}
        onChange={onInputChange}
        onModelChange={onModelChange}
        onPermissionModeChange={onPermissionModeChange}
      />
    </>
  );
}
