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
        <small>需先启动本地 RAG 服务：<code>python scripts/rag/rag_server.py</code></small><br>
        <small>或离线体验渡口写作引擎：<a href="dukou-engine.html" target="_blank" rel="noopener" style="color:#3A6B8C;text-decoration:none;">西游 · 渡口 →</a></small>
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

  // 命中词高亮：先转义，再对查询词包裹 <mark>（转义后无非标签内容，安全）
  function highlight(text, q) {
    let out = escapeHtml(text);
    const toks = (q || '').split(/\s+/).map(t => t.trim()).filter(t => t.length > 1);
    toks.forEach(t => {
      try {
        const re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
        out = out.replace(re, '<mark>$1</mark>');
      } catch (e) {}
    });
    return out;
  }

  // 打字机：逐字揭示（每次对当前切片整体转义，避免截断实体）
  function typeText(el, text) {
    let i = 0;
    (function tick() {
      if (i >= text.length) return;
      el.innerHTML = escapeHtml(text.slice(0, i + 1));
      i++;
      messages.scrollTop = messages.scrollHeight;
      setTimeout(tick, 10);
    })();
  }

  // 源文档相对路径：project-root/docs/...（从 site/data/ 出发）
  function docHref(path) {
    if (!path) return null;
    const p = String(path).replace(/\\/g, '/');
    const idx = p.indexOf('/docs/');
    const rel = idx >= 0 ? p.slice(idx + 1) : p;
    return '../../' + rel;
  }

  // 对话历史持久化（STORAGE_KEY 已声明）
  function pushHistory(role, text) {
    try {
      const h = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      h.push({ role, text });
      if (h.length > 40) h = h.slice(-40);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(h));
    } catch (e) {}
  }
  function loadHistory() {
    try {
      const h = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      if (!h.length) return;
      const hint = messages.querySelector('.rag-msg-hint');
      if (hint) hint.remove();
      h.forEach(m => addMessage(m.role, escapeHtml(m.text)));
    } catch (e) {}
  }

  async function sendQuery() {
    const q = input.value.trim();
    if (!q) return;

    // 多轮上下文（前端补偿，后端无状态）：取最近 4 轮作为 history 带给后端，
    // 待 LLM 接入后后端即可据此注入对话上下文（无需 Key，提前接线）。
    let prior = [];
    try { prior = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch (e) {}
    const ctx = prior.slice(-4).map(m => ({ role: m.role, text: (m.text || '').slice(0, 160) }));

    addMessage('user', escapeHtml(q));
    pushHistory('user', q);
    input.value = '';
    sendBtn.disabled = true;
    sendBtn.textContent = '…';

    if (!serviceOnline) {
      await checkHealth();
      if (!serviceOnline) {
        addMessage('error', '⚠️ RAG 服务未启动。<br>请在终端运行：<code>python scripts/rag/rag_server.py</code><br>然后刷新本页面重试。<br>或离线体验渡口写作引擎：<a href="dukou-engine.html" target="_blank" rel="noopener" style="color:#3A6B8C;">西游 · 渡口 →</a>');
        sendBtn.disabled = false;
        sendBtn.textContent = '问';
        return;
      }
    }

    try {
      const qry = ctx.length
        ? `${RAG_BASE}/query?q=${encodeURIComponent(q)}&k=5&history=${encodeURIComponent(JSON.stringify(ctx))}`
        : `${RAG_BASE}/query?q=${encodeURIComponent(q)}&k=5`;
      const res = await fetch(qry, {
        signal: AbortSignal.timeout(10000)
      });
      const data = await res.json();

      const bubble = addMessage('bot', '').querySelector('.rag-bubble');

      // 主回答：优先「LLM 生成」llm_generated；否则渡口风格摘要 draft；再回退原始片段
      const llm = (data.llm_generated && data.llm_generated.trim()) ? data.llm_generated.trim() : '';
      const draft = (data.draft && data.draft.trim()) ? data.draft.trim() : '';
      if (llm) {
        typeText(bubble, llm);
        if (data.llm_error) {
          const err = document.createElement('div');
          err.className = 'rag-source';
          err.style.color = '#C8463A';
          err.textContent = '⚠️ ' + data.llm_error;
          bubble.appendChild(err);
        }
      } else if (draft) {
        typeText(bubble, draft);
      } else if (data.snippets && data.snippets.length) {
        bubble.innerHTML = data.snippets.map((s, i) => {
          const text = typeof s === 'string' ? s : (s.excerpt || s.path || '');
          return `<strong>${i + 1}.</strong> ${highlight(text, q)}`;
        }).join('<br><br>');
      } else {
        bubble.innerHTML = '未找到相关语料。换个问法试试？';
      }

      // 相关语料（高亮命中词）
      if (data.snippets && data.snippets.length) {
        const ex = document.createElement('div');
        ex.className = 'rag-source';
        ex.innerHTML = '📚 相关语料：' + data.snippets.slice(0, 3).map(s => {
          const text = typeof s === 'string' ? s : (s.excerpt || '');
          return '<div style="margin:4px 0;line-height:1.6">' + highlight(text.slice(0, 140), q) + (text.length > 140 ? '…' : '') + '</div>';
        }).join('');
        bubble.appendChild(ex);
      }

      // 来源标注（可点击跳源文档）
      const sources = (data.snippets || [])
        .filter(s => typeof s === 'object' && s.path)
        .map(s => ({ name: s.path.replace(/\\/g, '/').split('/').pop(), href: docHref(s.path) }))
        .filter((v, i, a) => a.findIndex(x => x.name === v.name) === i);
      if (sources.length) {
        const srcDiv = document.createElement('div');
        srcDiv.className = 'rag-source';
        srcDiv.innerHTML = '📖 来源：' + sources.map(s => s.href
          ? `<a href="${s.href}" target="_blank" rel="noopener" style="color:#3a6b8c;text-decoration:none">${escapeHtml(s.name)} ↗</a>`
          : escapeHtml(s.name)).join(' · ');
        bubble.appendChild(srcDiv);
      }

      // 图谱三元组（{from, relation, to} 对象数组）
      if (data.graph && data.graph.length) {
        const graphDiv = document.createElement('div');
        graphDiv.className = 'rag-graph';
        graphDiv.innerHTML = '🔗 ' + data.graph.slice(0, 6).map(g => {
          const from = g.from || g[0] || '';
          const rel = g.relation || g[1] || '';
          const to = g.to || g[2] || '';
          return `<span>${escapeHtml(from.slice(0,12))} →${escapeHtml(rel)}→ ${escapeHtml(to.slice(0,12))}</span>`;
        }).join('');
        bubble.appendChild(graphDiv);
      }

      // 持久化本轮对话
      const firstSnippet = (data.snippets && data.snippets[0])
        ? (typeof data.snippets[0] === 'string' ? data.snippets[0] : (data.snippets[0].excerpt || '')) : '未找到相关语料。';
      pushHistory('bot', llm || draft || firstSnippet);

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

  // 恢复历史对话
  loadHistory();

  // 页面加载时静默检测服务状态（更新 fab 提示）
  checkHealth().then(() => {
    if (serviceOnline) {
      fab.title = '渡口问津 · 服务在线 · 点击提问';
    }
  });
})();
