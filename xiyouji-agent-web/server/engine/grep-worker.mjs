// engine/grep-worker.mjs — grep 匹配 worker（W680 复核加固：独立线程执行 LLM 提供的正则，
// 主线程超时即 terminate，防灾难性回溯阻塞事件循环——REDoS 防护）。
// 协议：postMessage({ files: [{abs, rel}], pattern }) → 回 { lines: [...], error?: string }。
import fs from "node:fs";
import { parentPort, workerData } from "node:worker_threads";

try {
  const rx = new RegExp(workerData.pattern);
  const lines = [];
  const CAP = 2000;
  outer: for (const f of workerData.files) {
    let content;
    try {
      content = fs.readFileSync(f.abs, "utf8");
    } catch {
      continue; // 二进制等不可解码文件跳过
    }
    const fileLines = content.split("\n");
    for (let i = 0; i < fileLines.length; i++) {
      if (rx.test(fileLines[i])) {
        lines.push(`${f.rel}:${i + 1}: ${fileLines[i].slice(0, 300)}`);
        if (lines.length >= CAP) break outer;
      }
    }
  }
  parentPort.postMessage({ lines });
} catch (e) {
  parentPort.postMessage({ lines: [], error: e?.message || String(e) });
}
