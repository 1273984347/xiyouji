// engine/tools.ts — 服务端工具集（W680：替代旧厂商 SDK 内建运行时的自主实现）。
// 安全继承（W536/W537 同源纪律）：路径 realpath 守卫（仅 cwd 内）、无 shell（spawn 直调 argv）、
// 命令白名单、输出/写入尺寸上限、目录遍历黑名单。
// W680 复核加固：受保护路径黑名单（密钥/门禁脚本/.git/会话库——读+写双面）、
// 命令白名单剔除任意代码执行原语（python -m/-c、git --no-index/--output）、
// W764 补拦 git pager/外部工具族（-O/--open-files-in-pager/--ext-diff/--pager=·W760 S-01
// 实证 -O 把 pager 交 sh -c 执行 = RCE）+ 全命令 shell 元字符二次校验（防御纵深，见 run_command）。
// spawn 环境变量过滤（LLM_API_KEY/AGENT_WEB_TOKEN 不下发子进程）、grep 移入 worker 防 ReDoS。
// W752 加固：①细粒度写入允许域 AGENT_WEB_WRITE_SCOPE（黑名单之外再收紧，未设置=零行为变化）；
// ②审计日志 data/audit.jsonl 入 DENY_READ（防 LLM 读回自己的操作史·写面已在 DENY_WRITE 覆盖）。
// 专项单测：server/engine/tools.test.ts（七组·越界/黑名单/白名单精度/允许域/环境过滤/上限）。
import fs from "fs";
import path from "path";
import { spawn } from "child_process";
import { Worker } from "worker_threads";
import type { ToolDef, ToolPermissionKind, Toolset } from "./types.js";

const READ_MAX_BYTES = 256 * 1024;
const WRITE_MAX_BYTES = 2 * 1024 * 1024;
const GREP_MATCH_CAP = 2000;
const GREP_TIMEOUT_MS = 15 * 1000;
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

// —— 受保护路径黑名单（W680 复核：服务端密钥 .env、git hooks、门禁脚本、会话库）——
// 相对路径统一 posix 分隔后匹配；读面挡密钥与会话库，写面另加 .git 与门禁脚本。
const DENY_READ: RegExp[] = [
  /(^|\/)\.env($|\.)/i, // 任意层级的 .env / .env.*（含 xiyouji-agent-web/.env）
  /^xiyouji-agent-web\/data\//, // 会话库 chat.db（历史含工具结果，防二次外泄）
  /(^|\/)data\/audit\.jsonl$/i, // W752 操作审计日志（防 LLM 读回自己的操作史；cwd 为仓库根或其子目录均命中）
];
const DENY_WRITE: RegExp[] = [
  ...DENY_READ,
  /^\.git\//, // hooks 等版本库内部（持久化执行原语）
  /^scripts\/(verify_delivery|bump_version|batch_cascade)\.py$/, // 门禁脚本（铁律 8）
];

// —— W752 细粒度写入允许域（AGENT_WEB_WRITE_SCOPE·可选）——
// 逗号分隔的 posix 前缀（相对工作目录，默认工作目录=仓库根），如 docs/,site/,scripts/output/。
// 语义：`docs/`＝该目录下全部；`README.md`＝该文件（或其同名目录）；`.`＝全仓（等同未设置）。
// 未设置/全空白＝不启用（保持 W680 及以前行为：全工作目录可写，向后兼容零回归）。
// 与 DENY_WRITE 叠加：黑名单优先命中即拒，白名单只收紧不放宽（黑名单外的路径仍可能被允许域拒绝）。
function parseWriteScope(): string[] | null {
  const raw = (process.env.AGENT_WEB_WRITE_SCOPE || "").trim();
  if (!raw) return null;
  const list = raw
    .split(",")
    .map((s) => s.trim().replace(/\\/g, "/").replace(/^\.\//, "").replace(/^\/+/, "").replace(/\/{2,}/g, "/"))
    .filter((s) => s && s !== ".");
  return list.length ? list : null;
}

function withinWriteScope(relPosix: string): boolean {
  const scope = parseWriteScope();
  if (!scope) return true; // 未配置＝不启用允许域
  const ci = process.platform === "win32"; // Windows 文件系统不区分大小写，比较同步放宽
  const rel = ci ? relPosix.toLowerCase() : relPosix;
  return scope.some((p) => {
    const s = ci ? p.toLowerCase() : p;
    return s.endsWith("/") ? rel.startsWith(s) : rel === s || rel.startsWith(s + "/");
  });
}

function toRelPosix(cwd: string, target: string): string {
  return path.relative(cwd, target).split(path.sep).join("/");
}

function checkProtected(relPosix: string, mode: "read" | "write"): void {
  const list = mode === "read" ? DENY_READ : DENY_WRITE;
  for (const rx of list) {
    if (rx.test(relPosix)) throw new Error(`受保护路径，工具拒绝访问：${relPosix}`);
  }
  // 黑名单之后再过允许域（黑名单优先）；未设置 AGENT_WEB_WRITE_SCOPE 时此分支恒不触发
  if (mode === "write" && !withinWriteScope(relPosix)) {
    throw new Error(
      `写入越界：不在 AGENT_WEB_WRITE_SCOPE 允许域内（允许前缀：${(parseWriteScope() ?? []).join(", ")}）：${relPosix}`
    );
  }
}

/** 路径守卫：解析后必须落在 cwd 内（realpath 规范化，防 ../、绝对路径、symlink 逃逸）。 */
function guardPath(cwd: string, rel: string, mode: "read" | "write", mustExist: boolean): string {
  const root = fs.realpathSync(cwd);
  const target = path.resolve(root, rel);
  const relPosix = toRelPosix(root, target);
  if (relPosix.startsWith("..")) throw new Error("路径越界：仅允许项目工作目录内的相对路径");
  checkProtected(relPosix, mode);
  if (mustExist) {
    fs.realpathSync(target); // 不存在即抛错；symlink 指向仓外则解析后判越界
    return target;
  }
  // write：取最深已存在祖先做 realpath 校验（防 symlink 指向仓外），不存在段交由 mkdir 创建
  let probe = path.dirname(target);
  while (true) {
    try {
      const realProbe = fs.realpathSync(probe);
      if (realProbe !== root && !realProbe.startsWith(root + path.sep)) {
        throw new Error("路径越界（symlink 解析后）");
      }
      break;
    } catch (e) {
      if ((e as NodeJS.ErrnoException).code === "ENOENT" && probe !== path.dirname(probe)) {
        probe = path.dirname(probe); // 上级不存在，继续向上找已存在祖先
        continue;
      }
      throw e;
    }
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
        if (/^\.env($|\.)/i.test(e.name)) continue; // 密钥文件不入枚举面（grep/glob）
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

// 命令白名单：项目脚本解释器（仅 scripts/ 下的脚本文件）+ 只读 git 子命令 + pip 查询。
// W680 复核：剔除 python -m/-c（任意代码执行原语）；git 侧 --no-index/--output= 在参数层拦截。
// W764 复核：git 侧 -O/--open-files-in-pager/--ext-diff/--pager= 同入参数层拦截（pager 经 sh -c）。
const RUN_ALLOW: Array<{ first: Set<string>; prefix: RegExp }> = [
  { first: new Set(["python", "python3"]), prefix: /^python3?\s+scripts\// },
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

/** spawn 子进程环境：剔除凭证（LLM_API_KEY/AGENT_WEB_TOKEN 等不下发给 LLM 可执行的子进程）。
 *  W752：导出供专项单测直接断言（纯增加导出，行为不变）。 */
export function childEnv(): NodeJS.ProcessEnv {
  const env = { ...process.env };
  delete env.LLM_API_KEY;
  delete env.AGENT_WEB_TOKEN;
  return env;
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
        description: "读取项目工作目录内一个文本文件的内容（UTF-8，上限 256KB；.env 等敏感路径被拒绝）。path 为相对路径。",
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
        description: "在项目工作目录文本文件内做正则检索，返回「路径:行号: 行内容」列表（上限 2000 条；单次 15 秒超时）。",
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
        description: "写入（或覆盖）项目工作目录内一个文本文件（上限 2MB；.env、.git/、门禁脚本等受保护路径被拒绝）。写入前先向用户说明用途。",
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
        description: "对项目内文本文件做唯一匹配替换（old_string 必须在文件中恰好出现一次；受保护路径被拒绝）。",
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
          const p = guardPath(cwd, String(input.path ?? ""), "read", true);
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
          const rel = all.map((f) => toRelPosix(root, f));
          const rx = new RegExp(
            "^" + pattern.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*\*/g, "\u0001").replace(/\*/g, "[^/]*").replace(/\u0001/g, ".*").replace(/\?/g, ".") + "$"
          );
          const hits = rel.filter((f) => rx.test(f));
          return { content: hits.join("\n") || "（无匹配）", isError: false };
        }
        case "grep": {
          const pattern = String(input.pattern ?? "");
          const glob = typeof input.glob === "string" && input.glob ? input.glob : null;
          const root = fs.realpathSync(cwd);
          const all = walkFiles(root);
          const globRx = glob
            ? new RegExp("^" + glob.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*\*/g, "\u0001").replace(/\*/g, "[^/]*").replace(/\u0001/g, ".*").replace(/\?/g, ".") + "$")
            : null;
          const files: Array<{ abs: string; rel: string }> = [];
          for (const f of all) {
            const rel = toRelPosix(root, f);
            if (globRx && !globRx.test(rel)) continue;
            try {
              if (fs.statSync(f).size > GREP_FILE_MAX_BYTES) continue;
            } catch {
              continue;
            }
            files.push({ abs: f, rel });
          }
          // W680 复核：正则来自 LLM，移入 worker 执行并设 15s 超时（灾难性回溯不再阻塞主线程）
          const lines: string[] = await new Promise((resolve, reject) => {
            const worker = new Worker(new URL("./grep-worker.mjs", import.meta.url), {
              workerData: { files, pattern },
            });
            const timer = setTimeout(() => {
              worker.terminate();
              reject(new Error(`grep 超时（${GREP_TIMEOUT_MS / 1000}s，正则回溯过重或文件集过大）`));
            }, GREP_TIMEOUT_MS);
            worker.on("message", (msg: { lines?: string[]; error?: string }) => {
              clearTimeout(timer);
              if (msg.error) reject(new Error(`grep 失败: ${msg.error}`));
              else resolve(msg.lines ?? []);
            });
            worker.on("error", (err) => {
              clearTimeout(timer);
              reject(err);
            });
          });
          return { content: lines.join("\n") || "（无匹配）", isError: false };
        }
        case "write_file": {
          const content = String(input.content ?? "");
          if (Buffer.byteLength(content, "utf8") > WRITE_MAX_BYTES) {
            return { content: `写入内容超上限（${WRITE_MAX_BYTES} 字节）`, isError: true };
          }
          const p = guardPath(cwd, String(input.path ?? ""), "write", false);
          fs.mkdirSync(path.dirname(p), { recursive: true });
          fs.writeFileSync(p, content, "utf8");
          return { content: `已写入 ${input.path}（${Buffer.byteLength(content, "utf8")} 字节）`, isError: false };
        }
        case "edit_file": {
          const p = guardPath(cwd, String(input.path ?? ""), "write", true);
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
          // W680 复核 + W764 加固：git 参数层逃逸原语拦截（按 token 判定·兼容粘连形态）——
          // ① --no-index 读仓外 / --output= 写任意路径（W680）；
          // ② W764（W760 S-01 落盘实证）：-O / -O=<pager> / --open-files-in-pager —— git 把
          //    pager 交 `sh -c '<pager> "$@"'` 执行（参数未转义）→ 任意命令执行；--ext-diff
          //    （外部 diff 驱动）与 --pager= 同族外呼，一并拦截。
          const GIT_DANGER = /^(--no-index|--output=|--open-files-in-pager|--ext-diff|--pager=)/;
          if (tokens[0] === "git") {
            const bad = tokens.find((t) => t.startsWith("-O") || GIT_DANGER.test(t));
            if (bad) {
              return { content: `git 子命令含被禁止的参数：${bad.slice(0, 60)}`, isError: true };
            }
          }
          // W764 加固（防御纵深）：全命令 shell 元字符二次校验——`;` `&` `>` `<` 反引号与换行
          // 不出现在白名单命令的合法参数中（脚本路径/ref/正则/包名）；`|` 与 `$` 放行
          // （git grep 正则交替/锚点的合法用法）。shell:false 下 node 侧本无 shell，此检兜底
          // 「命令内部再起 shell」的同类逃逸（-O 即此类入口）。
          const badMeta = tokens.find((t) => /[;&<>`\n]/.test(t));
          if (badMeta) {
            return { content: `命令参数含禁止的 shell 元字符（; & > < 反引号 换行）：${badMeta.slice(0, 60)}`, isError: true };
          }
          // W680 复核 + W752 加固：解释器脚本路径双重约束——
          // ① **口径约束**：posix 归一后必须仍以 scripts/ 开头（堵 `scripts/../evil.mjs` 型
          //    「真实存在于根内但不在 scripts/ 下」的绕过；旧实现只查 realpath 是否在根内，
          //    于是根内任意位置的脚本都能被拉起）；
          // ② **越界约束**：realpath 归一后必须仍在仓库根内（堵 symlink/出根）；
          //    不存在即拒绝（ENOENT 属拦截，不属放行）。
          if ((tokens[0] === "python" || tokens[0] === "python3" || tokens[0] === "node") && tokens[1]) {
            const root = fs.realpathSync(cwd);
            const scriptArg = tokens[1].split(path.sep).join("/");
            const norm = path.posix.normalize(scriptArg);
            if (!norm.startsWith("scripts/") || norm.startsWith("../")) {
              return { content: `脚本路径必须落在 scripts/ 内（白名单口径）：${tokens[1]}`, isError: true };
            }
            const scriptReal = fs.realpathSync(path.resolve(root, tokens[1])); // 不存在即拒绝
            if (scriptReal !== root && !scriptReal.startsWith(root + path.sep)) {
              return { content: "脚本路径越界", isError: true };
            }
          }
          const out = await new Promise<{ stdout: string; stderr: string; code: number | null }>((resolve, reject) => {
            const child = spawn(tokens[0], tokens.slice(1), {
              cwd: fs.realpathSync(cwd),
              shell: false,
              timeout: RUN_TIMEOUT_MS,
              env: childEnv(),
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
