// citationGuard.ts — W599 引用校验：对最终回答中的仓库相对路径做存在性核实
// 方案：docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md WP-I
//   - 真实存在的路径 → 转 GitHub blob 链接（每条仅首现转换）
//   - 不存在的路径 → 文末追加「⚠️ 未能核实的引用路径」警示块（不删原文，不阻断展示）
import fs from "fs";
import path from "path";

const BLOB = "https://github.com/1273984347/xiyouji/blob/main/";
// 仓库相对路径候选：限定已知顶层目录与常见文件扩展名，避免把普通句子切碎
const PATH_RE =
  /(?:docs|source|site|dataset|scripts|mcp-server|assets|tests)\/[^\s()[\]{}「」『』《》"'`<>|，。；、！？：]+?\.(?:md|html|json|py|js|ts|txt|yml|yaml|css)/g;

export interface CitationGuardResult {
  text: string;
  unverified: string[];
  linked: number;
}

export function applyCitationGuard(raw: string, cwd: string): CitationGuardResult {
  if (!raw) return { text: raw, unverified: [], linked: 0 };
  const seen = new Set<string>();
  const unverified = new Set<string>();
  let linked = 0;

  const text = raw.replace(PATH_RE, (match: string, offset: number, full: string) => {
    const cleaned = match.replace(/[.,;:]+$/, "");
    const prevChar = full.slice(Math.max(0, offset - 1), offset);
    if (prevChar === "(" || prevChar === "/") return match; // 已处于链接/URL 内，不二次包装
    if (seen.has(cleaned)) return cleaned;
    seen.add(cleaned);
    if (fs.existsSync(path.join(cwd, cleaned))) {
      linked++;
      return `[${cleaned}](${BLOB}${cleaned})`;
    }
    unverified.add(cleaned);
    return cleaned;
  });

  let finalText = text;
  if (unverified.size > 0) {
    finalText +=
      "\n\n> ⚠️ 未能核实的引用路径（未在仓库内找到，请勿直接采信）：" +
      [...unverified].map((u) => `\n> - ${u}`).join("");
  }
  return { text: finalText, unverified: [...unverified], linked };
}
