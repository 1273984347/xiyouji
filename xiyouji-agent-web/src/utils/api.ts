/**
 * api.ts — 前端 HTTP 调用复用层（W803-D 新建）
 *
 * 职责边界：把「同一条 REST 契约」收敛成一处调用，**不含 React 状态**。
 * 收敛动因：重构前 4 个 hook/组件各自手写 `fetch(url, { method, headers, body: JSON.stringify(...) })`
 * 与 `await res.json()`，其中 JSON 头只对写请求有意义，漏写即静默 400（Express 不解析体，
 * `req.body` 为空对象，路由按缺字段处理）——这是重复代码里最容易踩的一类坑。
 *
 * 注意：聊天流（POST /api/chat 的 SSE 解析）不在本模块，见 src/utils/sseStream.ts。
 * 所有函数**不吞异常**：网络错误照常抛出，由调用方决定兜底文案（保持重构前各处的 catch 语义）。
 */

/** 带 JSON 请求体的写请求（POST/PATCH/DELETE），返回解析后的 JSON。 */
export async function postJson<T = any>(url: string, body: unknown): Promise<T> {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json() as Promise<T>;
}

/** 带 JSON 请求体的 PATCH。 */
export async function patchJson<T = any>(url: string, body: unknown): Promise<T> {
  const res = await fetch(url, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json() as Promise<T>;
}

/** 无请求体的 DELETE。 */
export async function del<T = any>(url: string): Promise<T> {
  const res = await fetch(url, { method: 'DELETE' });
  return res.json() as Promise<T>;
}

/** 无请求体的 GET。 */
export async function getJson<T = any>(url: string): Promise<T> {
  const res = await fetch(url);
  return res.json() as Promise<T>;
}
