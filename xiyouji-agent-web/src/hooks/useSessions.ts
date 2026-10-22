import { useState, useEffect, useCallback } from 'react';
import { Session, Message } from '../types';
import { api } from '../utils/api';
import { getErrorMessage } from '../utils/errorMessage';

const STORAGE_KEYS = {
  sessionModels: 'sessionModels',
};

export function useSessions() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  /** W808：加载失败的用户可读文案（null = 无错误）。此前失败只 console.error，UI 表现为空白无提示。 */
  const [error, setError] = useState<string | null>(null);
  /** W808：会话列表是否正在加载（供 UI 显示加载态·skill 纪律：禁空白屏）。 */
  const [isLoading, setIsLoading] = useState(false);
  
  // 每个会话的模型选择缓存
  const [sessionModels, setSessionModels] = useState<Record<string, string>>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEYS.sessionModels);
      if (saved) {
        return JSON.parse(saved);
      }
    } catch {
      // 忽略：缓存损坏时用空缓存继续
    }
    return {};
  });

  // 获取当前会话
  const currentSession = sessions.find(s => s.id === currentSessionId);

  // 从 API 加载会话列表
  const fetchSessions = useCallback(async () => {
    setIsLoading(true);
    try {
      // W808：改走统一 client（非裸 fetch）——服务端错误不再被当成功数据返回
      const data = await api.listSessions();
      setError(null);

      const loadedSessions: Session[] = (data.sessions ?? []).map((s) => ({
        id: s.id,
        title: s.title,
        model: s.model,
        createdAt: new Date(s.created_at),
        messages: []
      }));
      setSessions(loadedSessions);
    } catch (err) {
      // W808：失败态可见（此前静默吞错 → 用户只见空白列表）
      setError(getErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  }, []);

  // 加载单个会话的消息
  const loadSessionMessages = useCallback(async (sessionId: string) => {
    try {
      const data = await api.getSession(sessionId);

      if (data.messages) {
        const messages: Message[] = data.messages.map((m) => ({
          id: m.id,
          role: m.role,
          content: m.content,
          model: m.model ?? undefined,
          timestamp: new Date(m.created_at),
          toolCalls: (m.tool_calls as never) ?? undefined
        }));
        
        setSessions(prev => prev.map(s => 
          s.id === sessionId ? { ...s, messages } : s
        ));
      }
    } catch (err) {
      setError(getErrorMessage(err));
    }
  }, []);

  // 删除会话
  const deleteSession = useCallback(async (sessionId: string): Promise<string | null> => {
    try {
      // W808：改走统一 client——删除失败时不再「本地假装删掉了」
      await api.deleteSession(sessionId);
      setError(null);
      
      let navigateTo: string | null = null;
      
      setSessions(prev => {
        const filtered = prev.filter(s => s.id !== sessionId);
        return filtered;
      });
      
      // 确定导航目标
      const remaining = sessions.filter(s => s.id !== sessionId);
      if (currentSessionId === sessionId) {
        if (remaining.length > 0) {
          navigateTo = `/chat/${remaining[0].id}`;
          setCurrentSessionId(remaining[0].id);
        } else {
          navigateTo = '/';
          setCurrentSessionId(null);
        }
      }
      
      return navigateTo;
    } catch (err) {
      setError(getErrorMessage(err));
      return null;
    }
  }, [sessions, currentSessionId]);

  // 保存每个会话的模型选择到 localStorage
  const updateSessionModel = useCallback((sessionId: string, modelId: string) => {
    setSessionModels(prev => {
      const updated = { ...prev, [sessionId]: modelId };
      localStorage.setItem(STORAGE_KEYS.sessionModels, JSON.stringify(updated));
      return updated;
    });
    setSessions(prev => prev.map(s => 
      s.id === sessionId ? { ...s, model: modelId } : s
    ));
  }, []);

  // 添加新会话
  const addSession = useCallback((session: Session) => {
    setSessions(prev => [session, ...prev]);
    setCurrentSessionId(session.id);
  }, []);

  // 更新会话
  const updateSession = useCallback((sessionId: string, updates: Partial<Session>) => {
    setSessions(prev => prev.map(s => 
      s.id === sessionId ? { ...s, ...updates } : s
    ));
  }, []);

  // 更新会话消息
  const updateSessionMessages = useCallback((sessionId: string, updater: (messages: Message[]) => Message[]) => {
    setSessions(prev => prev.map(s => 
      s.id === sessionId ? { ...s, messages: updater(s.messages) } : s
    ));
  }, []);

  // 当切换会话时，加载该会话的消息
  useEffect(() => {
    if (currentSessionId) {
      const session = sessions.find(s => s.id === currentSessionId);
      if (session && session.messages.length === 0) {
        loadSessionMessages(currentSessionId);
      }
    }
  }, [currentSessionId, sessions, loadSessionMessages]);

  return {
    sessions,
    setSessions,
    currentSessionId,
    setCurrentSessionId,
    currentSession,
    sessionModels,
    fetchSessions,
    loadSessionMessages,
    deleteSession,
    updateSessionModel,
    addSession,
    updateSession,
    updateSessionMessages,
    error,
    setError,
    isLoading,
  };
}
