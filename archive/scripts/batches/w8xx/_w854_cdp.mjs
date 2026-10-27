// _w854_cdp.mjs — W854 界面布局审计探针共用 CDP 客户端（Node 24 内置 WebSocket·零依赖）
// 被 _w854_layout_probe.mjs / _w854_layout_probe_app.mjs import；一次性诊断件·不入 CI
export async function waitPort(port) {
  for (let i = 0; i < 60; i++) {
    try { const r = await fetch(`http://127.0.0.1:${port}/json/version`); if (r.ok) return await r.json(); } catch {}
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error('chrome debug port not ready');
}

export class CDP {
  constructor(ws) { this.ws = ws; this.id = 0; this.pending = new Map(); this.events = []; this.waiters = []; }
  static async connect(url) {
    const ws = new WebSocket(url);
    await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
    const c = new CDP(ws);
    ws.onmessage = (m) => {
      const msg = JSON.parse(m.data);
      if (msg.id && c.pending.has(msg.id)) { const { res, rej } = c.pending.get(msg.id); c.pending.delete(msg.id); msg.error ? rej(new Error(JSON.stringify(msg.error))) : res(msg.result); }
      else if (msg.method) { c.events.push(msg); for (const w of c.waiters.slice()) { if (w.method === msg.method) { c.waiters.splice(c.waiters.indexOf(w), 1); w.res(msg.params); } } }
    };
    return c;
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((res, rej) => { this.pending.set(id, { res, rej }); this.ws.send(JSON.stringify({ id, method, params })); setTimeout(() => { if (this.pending.has(id)) { this.pending.delete(id); rej(new Error('timeout ' + method)); } }, 60000); });
  }
  waitEvent(method, timeout = 30000) {
    const hit = this.events.find(e => e.method === method);
    if (hit) return Promise.resolve(hit.params);
    return new Promise((res, rej) => { const w = { method, res }; this.waiters.push(w); setTimeout(() => { const i = this.waiters.indexOf(w); if (i >= 0) { this.waiters.splice(i, 1); rej(new Error('event timeout ' + method)); } }, timeout); });
  }
  static async newTarget(port) {
    try { return await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' })).json(); }
    catch { return await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`)).json(); }
  }
}
