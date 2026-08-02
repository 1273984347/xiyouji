/**
 * rag-chat.js — 渡口问津 · RAG 对话组件
 * ----------------------------------------
 * 浮动对话窗口，调用 scripts/rag/rag_server.py 的 /query 和 /graph 端点。
 * 服务未启动时优雅降级（显示启动提示）。
 *
 * 引入方式（放在 </body> 前）：
 *   <script src="static/js/rag-chat.js"></script>      (site/ 根页面)
 *   <script src="../static/js/rag-chat.js"></script>    (site/data/ 子目录)
 *
 * 依赖：无（纯 vanilla JS + CSS，不依赖 D3 或任何框架）
 * 设计：新中式·数字雅集（朱砂/宣纸/宋体/发丝线）
 */
(function () {
  'use strict';

  const RAG_BASE = 'http://127.0.0.1:8777';
  const STORAGE_KEY = 'rag-chat-history';

  // === 样式注入 ===
  const style = document.createElement('style');
  style.textContent = `
    .rag-fab {
      position: fixed; bottom: 28px; right: 28px; z-index: 900;
      width: 56px; height: 56px; border-radius: 50%;
      background: #C8463A; color: #fff; border: none; cursor: pointer;
      font-size: 22px; display: grid; place-items: center;
      box-shadow: 0 4px 16px rgba(200,70,58,0.3);
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .rag-fab:hover { transform: scale(1.08); box-shadow: 0 6px 24px rgba(200,70,58,0.4); }
    .rag-fab.hidden { display: none; }

    .rag-panel {
      position: fixed; bottom: 28px; right: 28px; z-index: 901;
      width: 380px; max-height: 520px; display: none; flex-direction: column;
      background: #FAF7F0; border: 1px solid #E5DFD0; border-radius: 6px;
      box-shadow: 0 8px 32px rgba(35,32,26,0.12);
      font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
      overflow: hidden;
    }
    .rag-panel.open { display: flex; }

    .rag-header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 14px 18px; background: #221D16; color: #F2EBDC;
    }
    .rag-header .rag-title {
      font-family: 'Noto Serif SC', serif; font-size: 15px; font-weight: 600;
    }
    .rag-header .rag-status { font-size: 11px; color: #A89B7F; margin-top: 2px; }
    .rag-header .rag-close {
      background: none; border: none; color: #A89B7F; font-size: 20px;
      cursor: pointer; padding: 4px; line-height: 1;
    }
    .rag-header .rag-close:hover { color: #F2EBDC; }

    .rag-messages {
      flex: 1; overflow-y: auto; padding: 16px; min-height: 200px; max-height: 320px;
    }
    .rag-msg { margin-bottom: 14px; font-size: 13px; line-height: 1.7; }
    .rag-msg-user { text-align: right; }
    .rag-msg-user .rag-bubble {
      display: inline-block; background: #C8463A; color: #fff;
      padding: 8px 14px; border-radius: 12px 12px 2px 12px; max-width: 85%;
      text-align: left;
    }
    .rag-msg-bot .rag-bubble {
      display: inline-block; background: #fff; border: 1px solid #E5DFD0;
      padding: 10px 14px; border-radius: 2px 12px 12px 12px; max-width: 92%;
    }
    .rag-msg-bot .rag-source {
      margin-top: 8px; padding-top: 8px; border-top: 1px dashed #E5DFD0;
      font-size: 11px; color: #9A9280;
    }
    .rag-msg-bot .rag-graph {
      margin-top: 8px; font-size: 11px; color: #3A6B8C;
    }
    .rag-msg-bot .rag-graph span { display: inline-block; margin: 2px 4px 2px 0; }
    .rag-msg-error .rag-bubble { border-color: #C8463A; color: #8C2A2A; }
    .rag-msg-hint { color: #9A9280; font-size: 12px; text-align: center; padding: 24px 16px; }

    .rag-input-row {
      display: flex; gap: 8px; padding: 12px 14px;
      border-top: 1px solid #E5DFD0; background: #fff;
    }
    .rag-input-row input {
      flex: 1; font-size: 13px; padding: 9px 14px;
      border: 1px solid #E5DFD0; border-radius: 4px;
      background: #FAF7F0; color: #23201A; outline: none;
      font-family: inherit;
    }
    .rag-input-row input:focus { border-color: #C8463A; }
    .rag-input-row button {
      padding: 9px 16px; background: #C8463A; color: #fff;
      border: none; border-radius: 4px; font-size: 13px; font-weight: 500;
      cursor: pointer; white-space: nowrap; font-family: inherit;
    }
    .rag-input-row button:hover { background: #b33d32; }
    .rag-input-row button:disabled { opacity: 0.5; cursor: not-allowed; }

    @media (max-width: 480px) {
      .rag-panel { width: calc(100vw - 24px); right: 12px; bottom: 12px; max-height: 70vh; }
      .rag-fab { bottom: 16px; right: 16px; }
    }
  `;
  document.head.appendChild(style);

  // === DOM 构建 ===
  const fab = document.createElement('button');
  fab.className = 'rag-fab';
  fab.innerHTML = '问';
  fab.setAttribute('aria-label', '渡口问津 · AI 西游助手');
  fab.title = '渡口问津 · 问悟空、问妖怪、问任何西游';

  const panel = document.createElement('div');
  panel.className = 'rag-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', '渡口问津对话窗口');
  panel.innerHTML = `
    <div class="rag-header">
      <div>
        <div class="rag-title">渡口问津</div>
        <div class="rag-status" id="rag-status">检测服务中…</div>
      </div>
      <button class="rag-close" aria-label="关闭">×</button>
    </div>
    <div class="rag-messages" id="rag-messages">
      <div class="rag-msg-hint">
        输入任何关于《西游记》的问题。<br>
        例如：「悟空为什么哭？」「紧箍咒和正则化有什么关系？」「狮驼岭有多难？」<br><br>
        <small>需先启动本地 RAG 服务：<code>python scripts/rag/rag_server.py</code></small>
      </div>
    </div>
    <div class="rag-input-row">
      <input type="text" id="rag-input" placeholder="问悟空、问妖怪、问任何西游…" autocomplete="off">
      <button id="rag-send">问</button>
    </div>
  `;

  document.body.appendChild(fab);
  document.body.appendChild(panel);

  // === 交互逻辑 ===
  const messages = panel.querySelector('#rag-messages');
  const input = panel.querySelector('#rag-input');
  const sendBtn = panel.querySelector('#rag-send');
  const statusEl = panel.querySelector('#rag-status');
  const closeBtn = panel.querySelector('.rag-close');

  let serviceOnline = false;

  fab.addEventListener('click', () => {
    panel.classList.add('open');
    fab.classList.add('hidden');
    input.focus();
    checkHealth();
  });

  closeBtn.addEventListener('click', () => {
    panel.classList.remove('open');
    fab.classList.remove('hidden');
  });

  // ESC 关闭
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && panel.classList.contains('open')) {
      panel.classList.remove('open');
      fab.classList.remove('hidden');
    }
  });

  sendBtn.addEventListener('click', sendQuery);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendQuery(); }
  });

  async function checkHealth() {
    try {
      const res = await fetch(RAG_BASE + '/health', { signal: AbortSignal.timeout(3000) });
      if (res.ok) {
        serviceOnline = true;
        statusEl.textContent = '服务在线 · BM25 + 图谱双层检索';
        statusEl.style.color = '#6B8E5A';
      } else { throw new Error(); }
    } catch {
      serviceOnline = false;
      statusEl.textContent = '服务离线 · 请运行 python scripts/rag/rag_server.py';
      statusEl.style.color = '#C8463A';
    }
  }

  function addMessage(type, html) {
    // 清除初始提示
    const hint = messages.querySelector('.rag-msg-hint');
    if (hint) hint.remove();

    const div = document.createElement('div');
    div.className = `rag-msg rag-msg-${type}`;
    div.innerHTML = `<div class="rag-bubble">${html}</div>`;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
  }

  function escapeHtml(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  async function sendQuery() {
    const q = input.value.trim();
    if (!q) return;

    addMessage('user', escapeHtml(q));
    input.value = '';
    sendBtn.disabled = true;
    sendBtn.textContent = '…';

    if (!serviceOnline) {
      await checkHealth();
      if (!serviceOnline) {
        addMessage('error', '⚠️ RAG 服务未启动。<br>请在终端运行：<code>python scripts/rag/rag_server.py</code><br>然后刷新本页面重试。');
        sendBtn.disabled = false;
        sendBtn.textContent = '问';
        return;
      }
    }

    try {
      const res = await fetch(`${RAG_BASE}/query?q=${encodeURIComponent(q)}&k=5`, {
        signal: AbortSignal.timeout(10000)
      });
      const data = await res.json();

      let html = '';
      // 文本片段
      if (data.snippets && data.snippets.length) {
        html += data.snippets.map((s, i) =>
          `<strong>${i + 1}.</strong> ${escapeHtml(s.slice(0, 200))}${s.length > 200 ? '…' : ''}`
        ).join('<br><br>');
      } else {
        html += '未找到相关语料。换个问法试试？';
      }

      const botMsg = addMessage('bot', html);

      // 来源标注
      if (data.sources && data.sources.length) {
        const srcDiv = document.createElement('div');
        srcDiv.className = 'rag-source';
        srcDiv.innerHTML = '📖 来源：' + data.sources.map(s => escapeHtml(s)).join(' · ');
        botMsg.querySelector('.rag-bubble').appendChild(srcDiv);
      }

      // 图谱三元组
      if (data.graph && data.graph.length) {
        const graphDiv = document.createElement('div');
        graphDiv.className = 'rag-graph';
        graphDiv.innerHTML = '🔗 ' + data.graph.slice(0, 6).map(g =>
          `<span>${escapeHtml(g.from || g[0])} → ${escapeHtml(g.relation || g[1])} → ${escapeHtml(g.to || g[2])}</span>`
        ).join('');
        botMsg.querySelector('.rag-bubble').appendChild(graphDiv);
      }

      // 统计
      if (data.total_docs) {
        const metaDiv = document.createElement('div');
        metaDiv.className = 'rag-source';
        metaDiv.textContent = `索引 ${data.total_docs} 篇文档 · ${data.graph ? data.graph.length : 0} 条图谱三元组`;
        botMsg.querySelector('.rag-bubble').appendChild(metaDiv);
      }

    } catch (e) {
      if (e.name === 'TimeoutError' || e.name === 'AbortError') {
        addMessage('error', '⚠️ 请求超时（10s）。服务可能繁忙，请稍后重试。');
      } else {
        serviceOnline = false;
        statusEl.textContent = '服务离线 · 连接中断';
        statusEl.style.color = '#C8463A';
        addMessage('error', '⚠️ 连接失败。服务可能已停止，请重新运行 rag_server.py。');
      }
    }

    sendBtn.disabled = false;
    sendBtn.textContent = '问';
    messages.scrollTop = messages.scrollHeight;
  }

  // 页面加载时静默检测服务状态（更新 fab 提示）
  checkHealth().then(() => {
    if (serviceOnline) {
      fab.title = '渡口问津 · 服务在线 · 点击提问';
    }
  });
})();
