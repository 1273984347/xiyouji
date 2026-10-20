import { useState, useCallback, useRef, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Message, ToolCall, PermissionRequest, PermissionMode, Session, CustomAgent, ContentBlock } from '../types';
import { api, ApiError } from '../utils/api';
import { getErrorMessage } from '../utils/errorMessage';
import { createSseLineSplitter } from '../utils/sseStream';

const STORAGE_KEYS = {
  draftInput: 'draftInput',
};

interface UseChatOptions {
  currentSession: Session | undefined;
  currentSessionId: string | null;
  selectedModel: string;
  getAgent: (id: string) => CustomAgent | undefined;
  addSession: (session: Session) => void;
  updateSession: (sessionId: string, updates: Partial<Session>) => void;
  updateSessionMessages: (sessionId: string, updater: (messages: Message[]) => Message[]) => void;
  updateSessionModel: (sessionId: string, modelId: string) => void;
  setCurrentSessionId: (id: string | null) => void;
  setSessions: React.Dispatch<React.SetStateAction<Session[]>>;
}

interface NewChatOptions {
  agentId: string;
  cwd: string;
  permissionMode: PermissionMode;
}

export function useChat(options: UseChatOptions) {
  const {
    currentSession,
    currentSessionId,
    selectedModel,
    getAgent,
    updateSessionModel,
    setCurrentSessionId,
    setSessions,
  } = options;

  const [isLoading, setIsLoading] = useState(false);
  const [inputValue, setInputValue] = useState(() => {
    return localStorage.getItem(STORAGE_KEYS.draftInput) || '';
  });
  const [permissionRequest, setPermissionRequest] = useState<PermissionRequest | null>(null);

  // W825：进行中的 SSE 请求句柄——「停止」按钮与组件卸载据此真正中止请求
  // （此前无 AbortController：停止只改 UI 状态，服务端继续跑完本轮；
  //   且 isLoading 复位后可再次发送 → 同一会话两条并发流同时写状态）
  const abortRef = useRef<AbortController | null>(null);

  // W825：组件卸载时中止在途请求（切页/切会话后无人观察的流继续改全局状态）
  useEffect(() => {
    return () => {
      abortRef.current?.abort();
      abortRef.current = null;
    };
  }, []);

  // 保存输入框内容到 localStorage（防抖）
  const saveInput = useCallback((value: string) => {
    setInputValue(value);
  }, []);

  // 发送消息
  const sendMessage = useCallback(async (
    messageContent: string,
    newChatOptions?: NewChatOptions,
    onNavigate?: (path: string) => void
  ) => {
    if (!messageContent.trim() || isLoading) return;

    let sessionId = currentSessionId;
    let currentCwd = currentSession?.cwd;
    let currentAgentId = currentSession?.agentId || 'default';
    let currentPermissionMode = currentSession?.permissionMode || 'default';
    
    // 如果没有当前会话，使用新对话页面的选项创建新会话
    if (!sessionId && newChatOptions) {
      const selectedAgent = getAgent(newChatOptions.agentId);
      const agentPermissionMode = selectedAgent?.permissionMode || 'default';
      const finalPermissionMode = newChatOptions.permissionMode !== 'default' 
        ? newChatOptions.permissionMode 
        : agentPermissionMode;
      
      const newSession: Session = {
        id: uuidv4(),
        title: messageContent.slice(0, 30) + (messageContent.length > 30 ? '...' : ''),
        model: selectedModel,
        agentId: newChatOptions.agentId,
        cwd: newChatOptions.cwd || undefined,
        permissionMode: finalPermissionMode,
        createdAt: new Date(),
        messages: []
      };
      
      setSessions(prev => [newSession, ...prev]);
      setCurrentSessionId(newSession.id);
      sessionId = newSession.id;
      currentCwd = newSession.cwd;
      currentAgentId = newSession.agentId || 'default';
      currentPermissionMode = newSession.permissionMode || 'default';
      
      updateSessionModel(newSession.id, selectedModel);
      
      onNavigate?.(`/chat/${newSession.id}`);
    }

    const tempUserMessageId = uuidv4();
    const tempAssistantMessageId = uuidv4();

    const userMessage: Message = {
      id: tempUserMessageId,
      role: 'user',
      content: messageContent,
      timestamp: new Date()
    };

    const assistantMessage: Message = {
      id: tempAssistantMessageId,
      role: 'assistant',
      content: '',
      model: selectedModel,
      timestamp: new Date(),
      isStreaming: true,
      contentBlocks: []
    };

    setSessions(prev => prev.map(s => {
      if (s.id === sessionId) {
        const newTitle = s.messages.length === 0 
          ? messageContent.slice(0, 30) + (messageContent.length > 30 ? '...' : '')
          : s.title;
        return {
          ...s,
          title: newTitle,
          messages: [...s.messages, userMessage, assistantMessage]
        };
      }
      return s;
    }));

    setInputValue('');
    localStorage.removeItem(STORAGE_KEYS.draftInput);
    setIsLoading(true);

    const agent = getAgent(currentAgentId);
    const systemPrompt = agent?.systemPrompt;

    // W825：为本次请求建 AbortController（供「停止」按钮与卸载清理中止）
    // ——须在 try 外声明：catch/finally 分支要能清掉它（块作用域不可见）。
    const controller = new AbortController();
    abortRef.current = controller;
    // W825：init 事件会把这两个 id 由 temp 改写为 real——同样须在 try 外声明，
    // 否则 catch/finally 分支看不到（此前声明在 try 内·块作用域）→
    // 错误文案写不进任何消息·isStreaming 永不复位（「思考中…」永久挂起）。
    let realSessionId: string = sessionId!;
    let realAssistantMessageId = tempAssistantMessageId;

    try {
      // W808：SSE 请求也须带共享 token——否则服务端开了 AGENT_WEB_TOKEN 后聊天流直接 401，
      // 而此前此处**不判 res.ok**，401 的 JSON 体被当流读取（读不到 'data: ' 帧），
      // 表现为「思考中…」永久挂起（与 W568 修复的挂起症状同形，根因不同）。
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(import.meta.env?.VITE_AGENT_WEB_TOKEN
            ? { 'x-agent-token': import.meta.env.VITE_AGENT_WEB_TOKEN as string }
            : {}),
        },
        // W825：挂 AbortSignal——「停止」与组件卸载据此真正中止请求
        // （此前无 signal：停止按钮只改 UI 状态，服务端继续跑完本轮）
        signal: controller.signal,
        body: JSON.stringify({
          sessionId,
          message: messageContent,
          model: selectedModel,
          systemPrompt,
          cwd: currentCwd,
          permissionMode: currentPermissionMode,
        })
      });

      // W808：非 2xx 时服务端返回 JSON 错误体（而非 SSE 流）——必须先判状态码，
      // 否则会把错误体当流解析，产出「无事件即结束」的静默失败。
      if (!response.ok) {
        const errBody = await response.json().catch(() => null);
        throw new ApiError(
          response.status,
          errBody,
          errBody && typeof errBody.error === 'string' ? errBody.error : undefined
        );
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      // W825：跨块行缓冲——与 utils/sseStream.ts 共用同一实现（单一修复点·两处解析不再分叉）
      const splitLines = createSseLineSplitter();
      let fullContent = '';
      let usedModel = selectedModel;
      let currentToolCalls: ToolCall[] = [];
      let contentBlocks: ContentBlock[] = [];
      let currentTextBlock: string = '';  // 当前正在积累的文本块
      // W825：realSessionId / realAssistantMessageId 已上移到 try 外（catch/finally 需见）

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          // W568：先解析后退出——错误事件与 EOF 常合并在最后一个 chunk（done=true 且 value 非空），
          // 旧写法 if (done) break 会把该 chunk 丢弃，导致「思考中…」永久挂起
          const chunk = decoder.decode(value, { stream: !done });

          // W825：跨块行缓冲（半行留待下一片·done 时冲刷）——tool_result 帧可达 1MB
          // 必然被网络切分；旧实现逐片独立切分 → 半截 JSON 解析失败被 catch 静默丢弃
          // → 整帧事件凭空消失（工具条目停在「执行中…」·文本增量丢字·无报错无日志）
          const lines = done
            ? [...splitLines.push(chunk), ...splitLines.flush()]
            : splitLines.push(chunk);

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));
                
                if (data.type === 'init') {
                  realSessionId = data.sessionId;
                  realAssistantMessageId = data.assistantMessageId;
                  usedModel = data.model;
                  
                  if (realSessionId !== sessionId) {
                    setSessions(prev => prev.map(s => 
                      s.id === sessionId ? { ...s, id: realSessionId } : s
                    ));
                    setCurrentSessionId(realSessionId);
                    sessionId = realSessionId;
                  }
                  
                  setSessions(prev => prev.map(s => {
                    if (s.id === realSessionId) {
                      return {
                        ...s,
                        messages: s.messages.map(m => 
                          m.id === tempAssistantMessageId 
                            ? { ...m, id: realAssistantMessageId }
                            : m
                        )
                      };
                    }
                    return s;
                  }));
                } else if (data.type === 'text') {
                  fullContent += data.content;
                  currentTextBlock += data.content;
                  
                  // 更新或创建最后一个文本块
                  const lastBlock = contentBlocks[contentBlocks.length - 1];
                  if (lastBlock && lastBlock.type === 'text') {
                    lastBlock.text = currentTextBlock;
                  } else if (currentTextBlock) {
                    contentBlocks.push({ type: 'text', text: currentTextBlock });
                  }
                  
                  setSessions(prev => prev.map(s => {
                    if (s.id === realSessionId) {
                      return {
                        ...s,
                        messages: s.messages.map(m => 
                          m.id === realAssistantMessageId 
                            ? { ...m, content: fullContent, model: usedModel, toolCalls: [...currentToolCalls], contentBlocks: [...contentBlocks] }
                            : m
                        )
                      };
                    }
                    return s;
                  }));
                } else if (data.type === 'citation_guard') {
                  // W599：服务端引用校验回写——最终文本块以校验结果为准（含未核实路径警示）
                  fullContent = data.text;
                  const lastGuardBlock = contentBlocks[contentBlocks.length - 1];
                  if (lastGuardBlock && lastGuardBlock.type === 'text') {
                    lastGuardBlock.text = data.text;
                  } else if (data.text) {
                    contentBlocks.push({ type: 'text', text: data.text });
                  }
                  setSessions(prev => prev.map(s => {
                    if (s.id === realSessionId) {
                      return {
                        ...s,
                        messages: s.messages.map(m =>
                          m.id === realAssistantMessageId
                            ? { ...m, content: fullContent, model: usedModel, toolCalls: [...currentToolCalls], contentBlocks: [...contentBlocks] }
                            : m
                        )
                      };
                    }
                    return s;
                  }));
                } else if (data.type === 'tool') {
                  // 如果有累积的文本，先结束当前文本块
                  currentTextBlock = '';
                  
                  const toolCall: ToolCall = {
                    id: data.id || uuidv4(),
                    name: data.name,
                    input: data.input,
                    status: 'running'
                  };
                  currentToolCalls.push(toolCall);
                  
                  // 添加工具调用块
                  contentBlocks.push({ type: 'tool_use', toolCall });
                  
                  setSessions(prev => prev.map(s => {
                    if (s.id === realSessionId) {
                      return {
                        ...s,
                        messages: s.messages.map(m => 
                          m.id === realAssistantMessageId 
                            ? { ...m, toolCalls: [...currentToolCalls], contentBlocks: [...contentBlocks] }
                            : m
                        )
                      };
                    }
                    return s;
                  }));
                } else if (data.type === 'tool_result') {
                  const toolId = data.toolId;
                  const toolIndex = toolId 
                    ? currentToolCalls.findIndex(t => t.id === toolId)
                    : currentToolCalls.length - 1;
                  
                  if (toolIndex >= 0) {
                    currentToolCalls[toolIndex].status = data.isError ? 'error' : 'completed';
                    currentToolCalls[toolIndex].isError = data.isError || false;
                    currentToolCalls[toolIndex].result = typeof data.content === 'string' 
                      ? data.content 
                      : JSON.stringify(data.content);
                    
                    // 同步更新 contentBlocks 中对应的工具调用
                    const blockIndex = contentBlocks.findIndex(
                      b => b.type === 'tool_use' && b.toolCall.id === currentToolCalls[toolIndex].id
                    );
                    if (blockIndex >= 0) {
                      (contentBlocks[blockIndex] as { type: 'tool_use'; toolCall: ToolCall }).toolCall = { ...currentToolCalls[toolIndex] };
                    }
                    
                    setSessions(prev => prev.map(s => {
                      if (s.id === realSessionId) {
                        return {
                          ...s,
                          messages: s.messages.map(m => 
                            m.id === realAssistantMessageId 
                              ? { ...m, toolCalls: [...currentToolCalls], contentBlocks: [...contentBlocks] }
                              : m
                          )
                        };
                      }
                      return s;
                    }));
                  }
                } else if (data.type === 'done') {
                  setSessions(prev => prev.map(s => {
                    if (s.id === realSessionId) {
                      return {
                        ...s,
                        messages: s.messages.map(m => 
                          m.id === realAssistantMessageId 
                            ? { ...m, isStreaming: false, durationSec: typeof data.duration === 'number' ? Math.round((data.duration / 1000) * 10) / 10 : undefined }
                            : m
                        )
                      };
                    }
                    return s;
                  }));
                } else if (data.type === 'error') {
                  // W568：SSE error 事件此前被静默丢弃，前端「思考中…」永久挂起（后端 catch 路径实际有推送）
                  const errorMessage: string = data.message || '处理请求时发生错误';
                  setSessions(prev => prev.map(s => {
                    if (s.id === realSessionId) {
                      return {
                        ...s,
                        messages: s.messages.map(m =>
                          m.id === realAssistantMessageId
                            ? {
                                ...m,
                                // W825：错误文案**追加为文本块**——此前只写 content，而
                                // ChatMessages.renderAssistantContent 优先渲染 contentBlocks
                                // （非空即跳过 content）⇒ 错误提示在有内容块时**完全不可见**
                                contentBlocks: [...(m.contentBlocks ?? []), { type: 'text', text: `⚠️ ${errorMessage}` }],
                                isStreaming: false,
                              }
                            : m
                        )
                      };
                    }
                    return s;
                  }));
                } else if (data.type === 'permission_request') {
                  console.log('[Permission] Request received:', data);
                  setPermissionRequest({
                    requestId: data.requestId,
                    toolUseId: data.toolUseId,
                    toolName: data.toolName,
                    input: data.input,
                    sessionId: data.sessionId,
                    timestamp: data.timestamp
                  });
                }
              } catch {
                // 忽略解析错误
              }
            }
          }

          if (done) break;
        }
      }
    } catch (error) {
      // W808：错误文案经统一映射（此前固定写死「发生错误，请重试」，401/429/网络不可达全同形）
      const errorText = getErrorMessage(error);
      console.error('Chat error:', error);
      setSessions(prev => prev.map(s => {
        if (s.id === sessionId) {
          return {
            ...s,
            messages: s.messages.map(m =>
              // W825：init 事件已把消息 id 由 temp 换成 real（见上），故这里必须**两者都匹配**
              // ——旧实现只匹配 tempAssistantMessageId → init 之后的任何异常都匹配不到任何消息
              // → 错误文案不写入、isStreaming 永为 true（「思考中…」永久挂起·反馈按钮永不出现）
              m.id === tempAssistantMessageId || m.id === realAssistantMessageId
                ? {
                    ...m,
                    content: `⚠️ ${errorText}`,
                    // 与 SSE error 事件同口径：错误**追加为文本块**（保留已生成的部分回答·
                    // 同时让错误可见——contentBlocks 非空时 ChatMessages 跳过 content）
                    contentBlocks: [...(m.contentBlocks ?? []), { type: 'text', text: `⚠️ ${errorText}` }],
                    isStreaming: false,
                  }
                : m
            )
          };
        }
        return s;
      }));
    } finally {
      setIsLoading(false);
      if (abortRef.current === controller) abortRef.current = null;
      // W825：兜底清流式态——流可能未收到 done 事件就结束（连接被掐断·服务端异常关闭），
      // 此前 isStreaming 仅在 done/error 事件里复位 ⇒ 消息永久停在「思考中…」
      setSessions(prev => prev.map(s => {
        if (s.id !== sessionId) return s;
        return {
          ...s,
          messages: s.messages.map(m =>
            m.id === tempAssistantMessageId || m.id === realAssistantMessageId
              ? { ...m, isStreaming: false }
              : m
          )
        };
      }));
    }
  }, [currentSession, currentSessionId, selectedModel, getAgent, updateSessionModel, setCurrentSessionId, setSessions, isLoading]);

  // 处理停止事件
  const handleStop = useCallback(() => {
    console.log('ChatSender stop event');
    // W825：**真正中止**在途 SSE 请求（此前只改 UI 状态——流继续推进、答案继续增长、
    // 服务端继续跑完本轮；且 isLoading 复位后可再次发送 → 同一会话两条并发流同时写状态）
    abortRef.current?.abort();
    abortRef.current = null;
    setIsLoading(false);
    // 结束流式态：被中止的消息不再显示「思考中…」
    setSessions(prev => prev.map(s => ({
      ...s,
      messages: s.messages.map(m => (m.isStreaming ? { ...m, isStreaming: false } : m)),
    })));
  }, []);

  // 处理权限允许
  const handlePermissionAllow = useCallback(async () => {
    if (!permissionRequest) return;
    
    console.log('[Permission] User allowed:', permissionRequest.requestId);
    
    // W808：改走统一 client（自动带 token + 判 res.ok——此前 401 被静默忽略，
    // 用户点了「允许」却什么都没发生，挂起表里的请求一直等到超时）
    await api.permissionResponse({
      requestId: permissionRequest.requestId,
      behavior: 'allow'
    }).catch((err) => {
      console.error('[Permission] 提交许可回执失败:', err);
    });

    setPermissionRequest(null);
  }, [permissionRequest]);

  // 处理权限拒绝
  const handlePermissionDeny = useCallback(async () => {
    if (!permissionRequest) return;
    
    console.log('[Permission] User denied:', permissionRequest.requestId);
    
    await api.permissionResponse({
      requestId: permissionRequest.requestId,
      behavior: 'deny',
      message: '用户拒绝了此操作'
    }).catch((err) => {
      console.error('[Permission] 提交许可回执失败:', err);
    });

    setPermissionRequest(null);
  }, [permissionRequest]);

  return {
    isLoading,
    inputValue,
    setInputValue: saveInput,
    permissionRequest,
    sendMessage,
    handleStop,
    handlePermissionAllow,
    handlePermissionDeny,
  };
}
