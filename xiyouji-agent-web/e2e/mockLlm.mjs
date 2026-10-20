/**
 * mockLlm.mjs — OpenAI-compatible 假 LLM 端点（E2E 用·W808 新建）
 *
 * 职责边界：实现 `/chat/completions` 的最小 OpenAI-compatible SSE 响应，
 * 让 E2E 能在**不接真实大模型、不消耗配额**的前提下跑通完整聊天链路。
 *
 * 为什么需要它：agent-web 的聊天流要经过「浏览器 → Express → 引擎 → LLM 端点」四段。
 * 若把 LLM 端点排除在测试外，则「引擎到 LLM 的协议适配」这一段永远无测试面；
 * 而真接大模型又需要凭证 + 花钱 + 网络。本模块是**外部依赖的替身**——
 * 被测系统（前端 + 后端 + 引擎）全部是真实实现。
 *
 * 协议对齐点（对齐 server/engine/openai-compat.ts 的解析口径）：
 *   - `data: {json}\n\n` 帧格式；
 *   - 文本增量放 `choices[0].delta.content`；
 *   - 收尾放 `choices[0].finish_reason` + `data: [DONE]`；
 *   - 允许跨 chunk 拆字（此处分两次发同样的字，验证前端的跨块解码）。
 */
import http from "node:http";

/** 构造一个假 LLM 服务。 */
export function createMockLlmServer(options = {}) {
  const reply = options.reply ?? "《西游记》测试回复：这是 mock LLM 产出的确定性文本。";
  const chunkSize = options.chunkSize ?? 8;

  const server = http.createServer((req, res) => {
    // 只认 POST /chat/completions（引擎的 joinUrl 口径：baseUrl + "/chat/completions"）
    if (!req.url || !req.url.endsWith("/chat/completions") || req.method !== "POST") {
      res.writeHead(404, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "not found" }));
      return;
    }

    // 读掉请求体（不读会导致客户端侧 backpressure 挂起）
    let body = "";
    req.on("data", (c) => {
      body += c;
    });
    req.on("end", () => {
      res.writeHead(200, {
        "Content-Type": "text/event-stream; charset=utf-8",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      });

      // 按 chunkSize 切片分帧发出（验证前端的跨块 UTF-8 解码与流式渲染）
      const chunks = [];
      for (let i = 0; i < reply.length; i += chunkSize) chunks.push(reply.slice(i, i + chunkSize));

      let index = 0;
      const sendNext = () => {
        if (index < chunks.length) {
          const piece = chunks[index++];
          res.write(
            `data: ${JSON.stringify({
              choices: [{ delta: { content: piece }, index: 0 }],
            })}\n\n`
          );
          setTimeout(sendNext, 5);
          return;
        }
        // 收尾帧：finish_reason + [DONE]
        res.write(`data: ${JSON.stringify({ choices: [{ delta: {}, finish_reason: "stop", index: 0 }] })}\n\n`);
        res.write("data: [DONE]\n\n");
        res.end();
      };

      sendNext();
    });
  });

  return server;
}

/** 启动并返回 { server, baseUrl, close }。 */
export async function startMockLlm(port = 0, options = {}) {
  const server = createMockLlmServer(options);
  await new Promise((resolve) => server.listen(port, "127.0.0.1", resolve));
  const address = server.address();
  const actualPort = typeof address === "object" && address ? address.port : port;
  return {
    server,
    baseUrl: `http://127.0.0.1:${actualPort}/v1`,
    close: () => new Promise((resolve) => server.close(() => resolve())),
  };
}
