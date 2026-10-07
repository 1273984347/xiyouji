// engine/tools.ts — 服务端工具集（W680：替代旧厂商 SDK 内建运行时的自主实现）。
// 安全继承（W536/W537 同源纪律）：路径 realpath 守卫（仅 cwd 内）、无 shell（spawn 直调 argv）、
// 命令白名单、输出/写入尺寸上限、目录遍历黑名单。
import fs from "fs";
import path from "path";
import { spawn } from "child_process";
import type { ToolDef, ToolPermissionKind, Toolset } from "./types.js";

const READ_MAX_BYTES = 256 * 1024;
const WRITE_MAX_BYTES = 2 * 1024 * 1024;
const GREP_MATCH_CAP = 2000;
const WALK_FILE_CAP = 5000;
const GREP_FILE_MAX_BYTES = 2 * 1024 * 1024;
const RUN_TIMEOUT_MS = 120 * 1000;
const RUN_MAX_BUFFER = 1024 * 1024;

const SKIP_DIRS = new Set(["node_modules", ".git", ".venv", "venv", "__pycache__", "dist", ".zcode"]);

/** 工具 → 权限分类（index.ts 权限策略消费）。未知工具按 command（最保守）处理。 */
export const TOOL_PERMISSION_KIND: Record<string, ToolPermissionKind> = {
  read_file: "read",
  glob: "read",
  grep: "read",
  write_file: "write",
  edit_file: "write",
  run_command: "command",
};

function guardInside(cwd: string, rel: string, mustExist: boolean): string {
  const root = fs.realpathSync(cwd);
  const target = path.resolve(root, rel);
  const real = mustExist ? fs.realpathSync(target) : fs.realpathSync(path.dirname(target));
  if (real !== root && !real.startsWith(root + path.sep)) {
    throw new Error("路径越界：仅允许项目工作目录内的相对路径");
  }
  return target;
}

function walkFiles(cwd: string): string[] {
  const out: string[] = [];
  const walk = (dir: string): void => {
    if (out.length >= WALK_FILE_CAP) return;
    let entries: fs.Dirent[];
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of entries) {
      if (out.length >= WALK_FILE_CAP) return;
      const full = path.join(dir, e.name);
      if (e.isDirectory()) {
        if (!SKIP_DIRS.has(e.name)) walk(full);
      } else if (e.isFile()) {
        out.push(full);
      }
    }
  };
  walk(cwd);
  return out;
}

function tokenize(cmd: string): string[] {
  const re = /"([^"]*)"|'([^']*)'|(\S+)/g;
  const tokens: string[] = [];
  let m: RegExpExecArray | null;
  while ((m = re.exec(cmd)) !== null) {
    tokens.push(m[1] ?? m[2] ?? m[3] ?? "");
  }
  return tokens;
}

// 命令白名单：只读 git 子命令 + 项目脚本解释器 + pip 查询。命中前缀才放行 spawn。
const RUN_ALLOW: Array<{ first: Set<string>; prefix: RegExp }> = [
  { first: new Set(["python", "python3"]), prefix: /^(python3?|python)\s+scripts\// },
  { first: new Set(["python", "python3"]), prefix: /^python3?\s+-(m|c)\s/ },
  { first: new Set(["node"]), prefix: /^node\s+scripts\// },
  { first: new Set(["git"]), prefix: /^git\s+(log|show|ls-files|grep|diff|status|branch|rev-parse)(\s|$)/ },
  { first: new Set(["pip", "pip3"]), prefix: /^pip3?\s+(show|list)/ },
];

function runAllowed(cmd: string): boolean {
  const tokens = tokenize(cmd);
  const first = tokens[0];
  if (!first) return false;
  return RUN_ALLOW.some((r) => r.first.has(first) && r.prefix.test(cmd.trim()));
}

function definitions(): ToolDef[] {
  const obj = (props: Record<string, unknown>, required: string[]): Record<string, unknown> => ({
    type: "object",
    properties: props,
    required,
  });
  return [
    {
      type: "function",
      function: {
        name: "read_file",
        description: "读取项目工作目录内一个文本文件的内容（UTF-8，上限 256KB）。path 为相对路径。",
        parameters: obj({ path: { type: "string", description: "相对项目根的文件路径，如 docs/00-导读/术语表.md" } }, ["path"]),
      },
    },
    {
      type: "function",
      function: {
        name: "glob",
        description: "按 glob 模式列出项目工作目录内的文件相对路径（如 docs/01-*/第00*.md），上限 5000。",
        parameters: obj({ pattern: { type: "string", description: "glob 模式" } }, ["pattern"]),
      },
    },
    {
      type: "function",
      function: {
        name: "grep",
        description: "在项目工作目录文本文件内做正则检索，返回「路径:行号: 行内容」列表（上限 2000 条）。",
        parameters: obj(
          {
            pattern: { type: "string", description: "正则表达式" },
            glob: { type: "string", description: "可选：仅检索匹配该 glob 的文件（如 docs/**/*.md）" },
          },
          ["pattern"]
        ),
      },
    },
    {
      type: "function",
      function: {
        name: "write_file",
        description: "写入（或覆盖）项目工作目录内一个文本文件（上限 2MB）。写入前先向用户说明用途。",
        parameters: obj(
          { path: { type: "string" }, content: { type: "string", description: "完整文件内容" } },
          ["path", "content"]
        ),
      },
    },
    {
      type: "function",
      function: {
        name: "edit_file",
        description: "对项目内文本文件做唯一匹配替换（old_string 必须在文件中恰好出现一次）。",
        parameters: obj(
          { path: { type: "string" }, old_string: { type: "string" }, new_string: { type: "string" } },
          ["path", "old_string", "new_string"]
        ),
      },
    },
    {
      type: "function",
      function: {
        name: "run_command",
        description:
          "运行白名单命令（python scripts/…、node scripts/…、只读 git 子命令、pip show/list）。仅传 command 字符串，无 shell。",
        parameters: obj({ command: { type: "string", description: "如 python scripts/词频.py --chap 1" } }, ["command"]),
      },
    },
  ];
}

export function createToolset(cwd: string): Toolset {
  const execute = async (name: string, input: Record<string, unknown>): Promise<{ content: string; isError: boolean }> => {
    try {
      switch (name) {
        case "read_file": {
          const p = guardInside(cwd, String(input.path ?? ""), true);
          const st = fs.statSync(p);
          if (!st.isFile()) return { content: `不是文件: ${input.path}`, isError: true };
          if (st.size > READ_MAX_BYTES) {
            const fh = fs.openSync(p, "r");
            const buf = Buffer.alloc(READ_MAX_BYTES);
            fs.readSync(fh, buf, 0, READ_MAX_BYTES, 0);
            fs.closeSync(fh);
            return { content: buf.toString("utf8") + `\n[截断：文件共 ${st.size} 字节，仅返回前 ${READ_MAX_BYTES}]`, isError: false };
          }
          return { content: fs.readFileSync(p, "utf8"), isError: false };
        }
        case "glob": {
          const pattern = String(input.pattern ?? "");
          const root = fs.realpathSync(cwd);
          const all = walkFiles(root);
          // 极简 glob：** 任意层级、* 单层、? 单字符——仅匹配相对路径
          const rel = all.map((f) => path.relative(root, f).split(path.sep).join("/"));
          const rx = new RegExp(
            "^" + pattern.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*\*/g, "\u0001").replace(/\*/g, "[^/]*").replace(/\u0001/g, ".*").replace(/\?/g, ".") + "$"
          );
          const hits = rel.filter((f) => rx.test(f));
          return { content: hits.join("\n") || "（无匹配）", isError: false };
        }
        case "grep": {
          const rx = new RegExp(String(input.pattern ?? ""));
          const glob = typeof input.glob === "string" && input.glob ? input.glob : null;
          const root = fs.realpathSync(cwd);
          const all = walkFiles(root);
          const globRx = glob
            ? new RegExp("^" + glob.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*\*/g, "\u0001").replace(/\*/g, "[^/]*").replace(/\u0001/g, ".*").replace(/\?/g, ".") + "$")
            : null;
          const lines: string[] = [];
          for (const f of all) {
            if (lines.length >= GREP_MATCH_CAP) break;
            const rel = path.relative(root, f).split(path.sep).join("/");
            if (globRx && !globRx.test(rel)) continue;
            const st = fs.statSync(f);
            if (st.size > GREP_FILE_MAX_BYTES) continue;
            let content: string;
            try {
              content = fs.readFileSync(f, "utf8");
            } catch {
              continue; // 二进制等不可解码文件跳过
            }
            const fileLines = content.split("\n");
            for (let i = 0; i < fileLines.length; i++) {
              if (rx.test(fileLines[i])) {
                lines.push(`${rel}:${i + 1}: ${fileLines[i].slice(0, 300)}`);
                if (lines.length >= GREP_MATCH_CAP) break;
              }
            }
          }
          return { content: lines.join("\n") || "（无匹配）", isError: false };
        }
        case "write_file": {
          const content = String(input.content ?? "");
          if (Buffer.byteLength(content, "utf8") > WRITE_MAX_BYTES) {
            return { content: `写入内容超上限（${WRITE_MAX_BYTES} 字节）`, isError: true };
          }
          const p = guardInside(cwd, String(input.path ?? ""), false);
          fs.mkdirSync(path.dirname(p), { recursive: true });
          fs.writeFileSync(p, content, "utf8");
          return { content: `已写入 ${input.path}（${Buffer.byteLength(content, "utf8")} 字节）`, isError: false };
        }
        case "edit_file": {
          const p = guardInside(cwd, String(input.path ?? ""), true);
          const src = fs.readFileSync(p, "utf8");
          const oldStr = String(input.old_string ?? "");
          const newStr = String(input.new_string ?? "");
          const first = src.indexOf(oldStr);
          if (first === -1) return { content: "old_string 在文件中未找到", isError: true };
          if (src.indexOf(oldStr, first + 1) !== -1) return { content: "old_string 在文件中出现多次，需唯一", isError: true };
          fs.writeFileSync(p, src.slice(0, first) + newStr + src.slice(first + oldStr.length), "utf8");
          return { content: `已编辑 ${input.path}`, isError: false };
        }
        case "run_command": {
          const cmd = String(input.command ?? "").trim();
          if (!cmd) return { content: "command 为空", isError: true };
          if (!runAllowed(cmd)) {
            return { content: `命令不在白名单（允许：python/node scripts/…、只读 git 子命令、pip show|list）：${cmd.slice(0, 120)}`, isError: true };
          }
          const tokens = tokenize(cmd);
          const out = await new Promise<{ stdout: string; stderr: string; code: number | null }>((resolve, reject) => {
            const child = spawn(tokens[0], tokens.slice(1), {
              cwd: fs.realpathSync(cwd),
              shell: false,
              timeout: RUN_TIMEOUT_MS,
              env: process.env,
            });
            let stdout = "";
            let stderr = "";
            child.stdout.on("data", (d: Buffer) => {
              if (stdout.length < RUN_MAX_BUFFER) stdout += d.toString("utf8");
            });
            child.stderr.on("data", (d: Buffer) => {
              if (stderr.length < RUN_MAX_BUFFER) stderr += d.toString("utf8");
            });
            child.on("error", reject);
            child.on("close", (code) => resolve({ stdout, stderr, code }));
          });
          const parts = [out.stdout, out.stderr].filter(Boolean).join("\n[stderr]\n");
          return {
            content: (parts || "(无输出)").slice(0, RUN_MAX_BUFFER) + (out.code !== 0 ? `\n[exit ${out.code}]` : ""),
            isError: out.code !== 0,
          };
        }
        default:
          return { content: `未知工具: ${name}`, isError: true };
      }
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      return { content: `工具执行失败: ${msg}`, isError: true };
    }
  };
  return { definitions: definitions(), execute };
}
