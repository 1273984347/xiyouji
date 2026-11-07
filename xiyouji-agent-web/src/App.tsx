import { useState, useEffect, useCallback } from 'react';
import { Routes, Route, Navigate, useNavigate, useParams, useLocation } from 'react-router-dom';
import { Button } from 'tdesign-react';
import '@tdesign-react/chat/es/style/index.js';

import { useAgents } from './hooks/useAgents';
import { useTheme } from './hooks/useTheme';
import { useSessions } from './hooks/useSessions';
import { useModels } from './hooks/useModels';
import { useChat } from './hooks/useChat';
import { PermissionMode } from './types';

import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { SettingsPage } from './components/SettingsPage';
import { ChatPage } from './pages/ChatPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<AppContent />} />
      <Route path="/chat/:sessionId" element={<AppContent />} />
      <Route path="/settings" element={<AppContent />} />
      {/* W1150：通配兜底——旧路由表无 * 项，未知路径（失效收藏/手输错地址）整页空白连侧栏都不渲染 */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function AppContent() {
  const navigate = useNavigate();
  const { sessionId: urlSessionId } = useParams<{ sessionId: string }>();
  const location = useLocation();
  const isSettingsPage = location.pathname === '/settings';
  
  // Hooks
  const { theme, toggleTheme } = useTheme();
  const { agents, addAgent, updateAgent, deleteAgent, getAgent } = useAgents();
  const { models, selectedModel, setSelectedModel, fetchModels, error: modelsError, isLoading: modelsLoading } = useModels();
  const {
    sessions,
    setSessions,
    currentSessionId,
    setCurrentSessionId,
    currentSession,
    sessionModels,
    fetchSessions,
    deleteSession,
    updateSessionModel,
    addSession,
    updateSession,
    updateSessionMessages,
    error: sessionsError,
    setError: setSessionsError,
    isLoading: sessionsLoading,
    messagesLoadingId,
  } = useSessions();

  // W808：把加载失败暴露到界面（此前失败只进 console，表现为「列表空白且无提示」）
  const loadError = sessionsError ?? modelsError ?? null;
  const [retrying, setRetrying] = useState(false);

  // 聊天 Hook
  const {
    isLoading,
    inputValue,
    setInputValue,
    permissionRequest,
    sendMessage,
    handleStop,
    handlePermissionAllow,
    handlePermissionDeny,
  } = useChat({
    currentSession,
    currentSessionId,
    selectedModel,
    getAgent,
    addSession,
    updateSession,
    updateSessionMessages,
    updateSessionModel,
    setCurrentSessionId,
    setSessions,
  });

  // 获取当前会话的 Agent
  const currentAgent = currentSession?.agentId ? getAgent(currentSession.agentId) : getAgent('default');

  // 从 URL 同步 sessionId
  useEffect(() => {
    if (urlSessionId && urlSessionId !== currentSessionId) {
      setCurrentSessionId(urlSessionId);
    } else if (!urlSessionId && !isSettingsPage && currentSessionId) {
      setCurrentSessionId(null);
    }
  }, [urlSessionId, isSettingsPage, currentSessionId, setCurrentSessionId]);

  // 当切换会话时，恢复该会话的模型选择
  useEffect(() => {
    if (currentSessionId && sessionModels[currentSessionId]) {
      setSelectedModel(sessionModels[currentSessionId]);
    } else if (currentSession) {
      setSelectedModel(currentSession.model);
    }
  }, [currentSessionId, sessionModels, currentSession, setSelectedModel]);

  // 初始加载会话列表
  useEffect(() => {
    fetchSessions();
  }, [fetchSessions]);

  // 更新当前会话的模型
  const updateCurrentSessionModel = useCallback((modelId: string) => {
    setSelectedModel(modelId);
    if (currentSessionId) {
      updateSessionModel(currentSessionId, modelId);
    }
  }, [currentSessionId, updateSessionModel, setSelectedModel]);

  // 删除会话处理
  const handleDeleteSession = useCallback(async (sessionId: string) => {
    const navigateTo = await deleteSession(sessionId);
    if (navigateTo) {
      navigate(navigateTo);
    }
  }, [deleteSession, navigate]);

  // 侧边栏事件处理
  const handleNewChat = useCallback(() => {
    setCurrentSessionId(null);
    navigate('/');
  }, [navigate, setCurrentSessionId]);

  const handleSelectSession = useCallback((sessionId: string) => {
    setCurrentSessionId(sessionId);
    navigate(`/chat/${sessionId}`);
  }, [navigate, setCurrentSessionId]);

  const handleOpenSettings = useCallback(() => {
    navigate('/settings');
  }, [navigate]);

  // Sidebar 状态
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // 权限模式状态
  const [permissionMode, setPermissionMode] = useState<PermissionMode>('default');

  // W1150：URL 指向的会话不存在（列表已加载且无加载失败）⇒ 显式提示而非静默渲染「新对话」
  const sessionNotFound =
    !isSettingsPage &&
    Boolean(urlSessionId) &&
    !sessionsLoading &&
    !sessionsError &&
    !currentSession;

  return (
    <div 
      className="flex h-screen w-screen"
      style={{ backgroundColor: 'var(--td-bg-color-page)' }}
    >
      {/* 侧边栏 */}
      <Sidebar
        sessions={sessions}
        currentSessionId={currentSessionId}
        isSettingsPage={isSettingsPage}
        sidebarOpen={sidebarOpen}
        sessionsLoading={sessionsLoading}
        agents={agents}
        getAgent={getAgent}
        onNewChat={handleNewChat}
        onSelectSession={handleSelectSession}
        onDeleteSession={handleDeleteSession}
        onOpenSettings={handleOpenSettings}
      />

      {/* 主内容区 */}
      <main 
        className="flex-1 flex flex-col min-w-0"
        style={{ backgroundColor: 'var(--td-bg-color-page)' }}
      >
        {/* 顶部栏 */}
        <Header
          isSettingsPage={isSettingsPage}
          sidebarOpen={sidebarOpen}
          theme={theme}
          currentSession={currentSession}
          currentAgent={currentAgent}
          models={models}
          modelsLoading={modelsLoading}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          onToggleTheme={toggleTheme}
          onRefreshModels={fetchModels}
        />

        {/* W808：加载失败横幅（此前失败只进 console，界面无任何提示） */}
        {loadError && (
          <div
            role="alert"
            className="flex items-start justify-between gap-3 px-4 py-2 text-sm"
            style={{
              backgroundColor: 'var(--td-error-color-light)',
              color: 'var(--td-error-color)',
              borderBottom: '1px solid var(--td-error-color-light)',
            }}
          >
            <span>{loadError}</span>
            {/* W1150：裸 button 改带 loading 态的重试按钮（双击不再并发重复拉取） */}
            <Button
              size="small"
              variant="text"
              loading={retrying}
              onClick={async () => {
                setRetrying(true);
                try {
                  setSessionsError(null);
                  await Promise.all([fetchSessions(), fetchModels()]);
                } finally {
                  setRetrying(false);
                }
              }}
              style={{ color: 'inherit', textDecoration: 'underline' }}
            >
              重试
            </Button>
          </div>
        )}

        {/* 设置页面或聊天页面 */}
        {isSettingsPage ? (
          <SettingsPage
            agents={agents}
            onAdd={addAgent}
            onUpdate={updateAgent}
            onDelete={deleteAgent}
          />
        ) : sessionNotFound ? (
          <div className="flex-1 flex items-center justify-center p-8">
            <div
              className="flex flex-col items-center gap-4 rounded-lg px-10 py-8"
              style={{
                backgroundColor: 'var(--td-bg-color-container)',
                border: '1px solid var(--td-component-border)',
                color: 'var(--td-text-color-secondary)',
              }}
            >
              <span className="text-base font-medium" style={{ color: 'var(--td-text-color-primary)' }}>
                会话不存在或已被删除
              </span>
              <span className="text-sm">链接指向的会话在当前列表中找不到，可能已被删除或来自其他工作目录。</span>
              <Button theme="primary" onClick={() => navigate('/')}>
                返回首页
              </Button>
            </div>
          </div>
        ) : (
          <ChatPage
            currentSession={currentSession}
            models={models}
            selectedModel={selectedModel}
            agents={agents}
            isLoading={isLoading}
            modelsLoading={modelsLoading}
            messagesLoading={messagesLoadingId !== null && messagesLoadingId === currentSessionId}
            inputValue={inputValue}
            permissionRequest={permissionRequest}
            permissionMode={permissionMode}
            onSendMessage={sendMessage}
            onStop={handleStop}
            onInputChange={setInputValue}
            onModelChange={updateCurrentSessionModel}
            onPermissionAllow={handlePermissionAllow}
            onPermissionDeny={handlePermissionDeny}
            onPermissionModeChange={setPermissionMode}
          />
        )}
      </main>
    </div>
  );
}

export default App;
