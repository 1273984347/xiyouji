// tools.test.ts — W752 引擎工具面安全专项单测（node:test·经 tsx 运行）。
//
// 形态与 server/citationGuard.test.ts 一致：真实临时目录（fs.mkdtempSync）+ 真实调用 createToolset，
// 不走 mock——所有断言都是「磁盘真实状态 / 真实返回内容」的机判。
// 覆盖：越界守卫 / 读写黑名单（含哈希未改写证据）/ 命令白名单精度 / 允许域 / 环境过滤 / 尺寸上限。
// 运行：cd xiyouji-agent-web && node --import tsx --test server/engine/tools.test.ts
import { test, after } from "node:test";
import assert from "node:assert";
import fs from "fs";
import os from "os";
import path from "path";
import crypto from "crypto";
import { execFileSync } from "child_process";
import { createToolset, childEnv } from "./tools.js";

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "xiyouji-tools-test-"));
const ROOT = fs.realpathSync(TMP); // 工具集内部亦以 realpath 为根，断言路径与之对齐
const toolset = createToolset(TMP);

// 仓外绝对路径（父目录必然在 root 之外）——用于「绝对路径越界」样本，不依赖平台盘符。
const OUTSIDE_ABS = path.join(path.dirname(ROOT), `xiyouji-outside-${path.basename(ROOT)}.txt`);
const ESCAPED_WRITE = path.join(path.dirname(ROOT), `xiyouji-escaped-${path.basename(ROOT)}.txt`);

function seed(rel: string, content: string): string {
  const p = path.join(ROOT, rel);
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, content, "utf8");
  return p;
}

function sha256(p: string): string {
  return crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
}

const call = (name: string, input: Record<string, unknown>) => toolset.execute(name, input);

/** 允许域环境变量读写（进程级，逐条用例自恢复——node:test 顶层用例串行执行）。 */
async function withWriteScope<T>(value: string | undefined, fn: () => Promise<T> | T): Promise<T> {
  const prev = process.env.AGENT_WEB_WRITE_SCOPE;
  if (value === undefined) delete process.env.AGENT_WEB_WRITE_SCOPE;
  else process.env.AGENT_WEB_WRITE_SCOPE = value;
  try {
    return await fn();
  } finally {
    if (prev === undefined) delete process.env.AGENT_WEB_WRITE_SCOPE;
    else process.env.AGENT_WEB_WRITE_SCOPE = prev;
  }
}

// —— 固定夹具（模块加载时一次性铺盘）——
seed("notes/keep.md", "甲：这是唯一一段。\n乙：普通内容。\n");
seed(".env", "LLM_API_KEY=unit-test-secret-should-never-leak\n");
seed("sub/.env.local", "AGENT_WEB_TOKEN=unit-test-token-should-never-leak\n");
seed("xiyouji-agent-web/data/chat.db", "SQLITE-FAKE-SESSION-LIB\n");
const GATE_FILES = [
  ".git/hooks/pre-commit", // 版本库 hooks（持久化执行原语）
  "scripts/verify_delivery.py", // 铁律 8 门禁脚本
  "scripts/bump_version.py", // 铁律 8 门禁脚本
  "scripts/batch_cascade.py", // 铁律 8 门禁脚本
];
for (const rel of GATE_FILES) seed(rel, `# ORIGINAL ${rel}\n`);

after(() => {
  fs.rmSync(ROOT, { recursive: true, force: true });
  fs.rmSync(OUTSIDE_ABS, { force: true });
  fs.rmSync(ESCAPED_WRITE, { force: true });
});

// ============ T1.1 越界守卫（原语：guardPath 的 realpath 归一 + ".." 前缀判定） ============

test("T1.1a 越界拒绝：read_file ../outside.txt", async () => {
  const r = await call("read_file", { path: "../outside.txt" });
  assert.equal(r.isError, true);
  assert.match(r.content, /越界/);
});

test("T1.1b 越界拒绝：read_file 绝对路径", async () => {
  const r = await call("read_file", { path: OUTSIDE_ABS });
  assert.equal(r.isError, true);
  assert.match(r.content, /越界/);
});

test("T1.1c 越界拒绝：read_file ..\\..\\x 反斜杠变体", async () => {
  const r = await call("read_file", { path: "..\\..\\x.txt" });
  assert.equal(r.isError, true);
  assert.match(r.content, /越界/);
});

test("T1.1d 越界拒绝：read_file 子目录回退 sub/../../outside.txt", async () => {
  const r = await call("read_file", { path: "sub/../../outside.txt" });
  assert.equal(r.isError, true);
  assert.match(r.content, /越界/);
});

test("T1.1e 越界拒绝：write_file ../escaped.txt 且磁盘确无落盘（不是只报错）", async () => {
  fs.rmSync(ESCAPED_WRITE, { force: true });
  const r = await call("write_file", { path: `../${path.basename(ESCAPED_WRITE)}`, content: "EVIL" });
  assert.equal(r.isError, true);
  assert.match(r.content, /越界/);
  assert.equal(fs.existsSync(ESCAPED_WRITE), false, "越界写必须零落盘");
});

// ============ T1.2 读黑名单（原语：DENY_READ 正则，命中即抛「受保护路径」） ============

test("T1.2 读黑名单：.env / sub/.env.local / xiyouji-agent-web/data/chat.db 均拒且不泄内容", async () => {
  const cases: Array<[string, string]> = [
    [".env", "secret"], // 任意层级 .env → 密钥文件
    ["sub/.env.local", "token"], // .env.* 变体
    ["xiyouji-agent-web/data/chat.db", "SQLITE"], // 会话库（历史含工具结果）
  ];
  for (const [p, sentinel] of cases) {
    const r = await call("read_file", { path: p });
    assert.equal(r.isError, true, `${p} 应被拒绝`);
    assert.match(r.content, /受保护路径/, `${p} 应报受保护路径：${r.content}`);
    assert.equal(r.content.includes(sentinel), false, `${p} 不得回泄内容`);
  }
});

// ============ T1.3 写黑名单 + 哈希未改写实证（原语：DENY_WRITE = DENY_READ + .git/ + 门禁脚本） ============

test("T1.3a 写黑名单：四个受保护目标全部拒绝，且写前写后 sha256 一致", async () => {
  for (const rel of GATE_FILES) {
    const abs = path.join(ROOT, rel);
    const before = sha256(abs);
    const r = await call("write_file", { path: rel, content: "EVIL-PAYLOAD" });
    assert.equal(r.isError, true, `${rel} 应被拒绝`);
    assert.match(r.content, /受保护路径/, `${rel} 应报受保护路径：${r.content}`);
    assert.equal(sha256(abs), before, `${rel} 内容必须未被改写`);
    assert.match(fs.readFileSync(abs, "utf8"), /ORIGINAL/, `${rel} 应保持原内容`);
  }
});

test("T1.3b 写黑名单同样覆盖 edit_file（同一 guardPath 写面判据）", async () => {
  const rel = "scripts/verify_delivery.py";
  const abs = path.join(ROOT, rel);
  const before = sha256(abs);
  const r = await call("edit_file", { path: rel, old_string: "ORIGINAL", new_string: "EVIL" });
  assert.equal(r.isError, true);
  assert.match(r.content, /受保护路径/);
  assert.equal(sha256(abs), before, "edit_file 亦不得改写门禁脚本");
});

// ============ T1.4 命令白名单精度（原语：RUN_ALLOW 前缀 + git 参数层 + scripts/ 词法口径 + realpath 越界） ============
//
// W752 残留（如实记账·低危·未实测）：口径约束是**词法**判定，不是 realpath 判定——若 scripts/ 内
// 已存在指向「根内 scripts/ 之外」的符号链接/junction，词法检查与「realpath 仍在根内」两道都会放行；
// 指向仓外的链接仍被 realpath 拒。利用前提是仓内已存在此类链接，而本工具集无创建链接的能力
// （Windows 建链需特权，实测 EPERM SKIP）。独立复核（21 种逃逸形态）未发现可用绕过。

const DENIED_COMMANDS: Array<{ cmd: string; why: string; pattern: RegExp }> = [
  {
    cmd: 'python -c "print(1)"',
    why: "python -c＝任意代码执行原语；RUN_ALLOW 前缀只认 `python scripts/`",
    pattern: /不在白名单/,
  },
  {
    cmd: "python -m http.server",
    why: "python -m＝任意模块执行原语（可拉起网络服务）；同上前缀拦截",
    pattern: /不在白名单/,
  },
  {
    cmd: "python scripts/../evil.py",
    why:
      "`scripts/` 前缀被 ../ 绕过；W752 加固后由路径口径约束拦截（posix 归一后必须仍在 scripts/ 内），" +
      "不再依赖「归一后目标恰好不存在」这一偶然条件",
    pattern: /必须落在 scripts\/ 内|工具执行失败|白名单|越界/,
  },
  {
    cmd: "node scripts/../evil-root.mjs",
    why:
      "W752 加固回归样本：目标**真实存在于根内但不在 scripts/ 下**——旧实现只查 realpath 是否在根内，" +
      "于是根内任意位置的脚本都能被拉起（实测 EVIL-RAN）；加固后必被口径约束拒绝",
    pattern: /必须落在 scripts\/ 内/,
  },
  {
    cmd: "git log --no-index",
    why: "git --no-index＝读仓外任意文件原语；git 参数层显式拦截",
    pattern: /被禁止的参数/,
  },
  {
    cmd: "git show --output=x",
    why: "git --output=＝写任意路径原语；git 参数层显式拦截",
    pattern: /被禁止的参数/,
  },
  {
    cmd: "rm -rf /",
    why: "非白名单首命令（无 shell 直调 argv，rm 从未入列）",
    pattern: /不在白名单/,
  },
  {
    cmd: "python scripts/nonexistent.py",
    why: "scripts/ 内不存在的脚本 → realpath 归一（不存在即拒绝），不会盲跑",
    pattern: /工具执行失败|白名单/,
  },
];

for (const { cmd, why, pattern } of DENIED_COMMANDS) {
  test(`T1.4 命令拒绝：${cmd} —— 拦的是：${why}`, async () => {
    const r = await call("run_command", { command: cmd });
    assert.equal(r.isError, true, `${cmd} 应被拒绝：${r.content}`);
    assert.match(r.content, pattern, `${cmd} 拒绝原因应可判定：${r.content}`);
  });
}

test("T1.4z 命令放行：git status 真实执行成功（isError=false）", async () => {
  // 原语：RUN_ALLOW 的只读 git 子命令（status 在列）+ cwd 内执行 + 无禁用参数 → 真跑
  // 需真实 git 上下文（临时目录先 git init），否则 git 自身 exit 128 会掩盖「放行」判据
  execFileSync("git", ["init", "-q"], { cwd: ROOT, stdio: "ignore" });
  const r = await call("run_command", { command: "git status" });
  assert.equal(r.isError, false, `git status 应放行且退出码 0：${r.content}`);
  assert.match(r.content, /branch|master|main/i, "应返回真实 git 输出");
});

test("T1.4y 前缀绕过闭环：根内真实存在的可执行脚本也不得经 scripts/../ 拉起", async () => {
  // W752 加固的**端到端**回归：判据不能只靠「目标不存在」。这里在根内（scripts/ 之外）
  // 真建一个会写哨兵文件的可执行脚本，断言命令被拒且脚本从未执行（哨兵不存在）。
  const evil = path.join(ROOT, "evil-root.mjs");
  const sentinel = path.join(ROOT, "evil-ran.sentinel");
  fs.writeFileSync(evil, 'import fs from "node:fs";\nfs.writeFileSync("evil-ran.sentinel", "EVIL-RAN");\n', "utf8");
  try {
    const r = await call("run_command", { command: "node scripts/../evil-root.mjs" });
    assert.equal(r.isError, true, `必须拒绝：${r.content}`);
    assert.match(r.content, /必须落在 scripts\/ 内/, r.content);
    assert.equal(fs.existsSync(sentinel), false, "脚本被拉起了（前缀绕过未堵住）");
  } finally {
    if (fs.existsSync(evil)) fs.unlinkSync(evil);
    if (fs.existsSync(sentinel)) fs.unlinkSync(sentinel);
  }
});

// ============ T1.5 正常路径（写/读/编辑语义不因加固而回归） ============

test("T1.5a write_file 落盘内容与读回一致", async () => {
  const w = await call("write_file", { path: "out/deep/新建.md", content: "心猿归正\n" });
  assert.equal(w.isError, false, w.content);
  assert.equal(fs.readFileSync(path.join(ROOT, "out/deep/新建.md"), "utf8"), "心猿归正\n");
  const rd = await call("read_file", { path: "out/deep/新建.md" });
  assert.equal(rd.isError, false);
  assert.equal(rd.content, "心猿归正\n");
});

test("T1.5b edit_file 唯一匹配成功", async () => {
  await call("write_file", { path: "edit/unique.md", content: "甲：这是唯一一段。\n乙：普通内容。\n" });
  const r = await call("edit_file", { path: "edit/unique.md", old_string: "唯一一段", new_string: "唯一一段（已改）" });
  assert.equal(r.isError, false, r.content);
  assert.equal(fs.readFileSync(path.join(ROOT, "edit/unique.md"), "utf8"), "甲：这是唯一一段（已改）。\n乙：普通内容。\n");
});

test("T1.5c edit_file 多处匹配 / 无匹配均报错且不改盘", async () => {
  await call("write_file", { path: "edit/multi.md", content: "重复段\n中间\n重复段\n" });
  const multi = await call("edit_file", { path: "edit/multi.md", old_string: "重复段", new_string: "X" });
  assert.equal(multi.isError, true);
  assert.match(multi.content, /出现多次/);
  const none = await call("edit_file", { path: "edit/multi.md", old_string: "不存在段", new_string: "X" });
  assert.equal(none.isError, true);
  assert.match(none.content, /未找到/);
  assert.equal(fs.readFileSync(path.join(ROOT, "edit/multi.md"), "utf8"), "重复段\n中间\n重复段\n");
});

// ============ T1.6 环境过滤（原语：childEnv 剔除凭证后才下发子进程） ============

test("T1.6 childEnv 剔除 LLM_API_KEY / AGENT_WEB_TOKEN 且不改宿主环境", () => {
  const prevKey = process.env.LLM_API_KEY;
  const prevToken = process.env.AGENT_WEB_TOKEN;
  process.env.LLM_API_KEY = "unit-test-key-should-not-leak";
  process.env.AGENT_WEB_TOKEN = "unit-test-token-should-not-leak";
  try {
    const env = childEnv();
    assert.equal("LLM_API_KEY" in env, false, "LLM_API_KEY 不得下发子进程");
    assert.equal("AGENT_WEB_TOKEN" in env, false, "AGENT_WEB_TOKEN 不得下发子进程");
    assert.equal(process.env.LLM_API_KEY, "unit-test-key-should-not-leak", "不得就地删除宿主进程变量");
    assert.equal(process.env.AGENT_WEB_TOKEN, "unit-test-token-should-not-leak", "不得就地删除宿主进程变量");
    // 非凭证变量保留（PATH 大小写随平台而异，按不区分大小写断言）
    assert.ok(Object.keys(env).some((k) => k.toLowerCase() === "path"), "PATH 等运行必需变量应保留");
  } finally {
    if (prevKey === undefined) delete process.env.LLM_API_KEY;
    else process.env.LLM_API_KEY = prevKey;
    if (prevToken === undefined) delete process.env.AGENT_WEB_TOKEN;
    else process.env.AGENT_WEB_TOKEN = prevToken;
  }
});

// ============ T1.7 尺寸上限（原语：WRITE_MAX_BYTES 早于路径守卫的字节数判定） ============

test("T1.7a write_file 超 2MB 拒绝", async () => {
  const r = await call("write_file", { path: "size/too-big.txt", content: "x".repeat(2 * 1024 * 1024 + 1) });
  assert.equal(r.isError, true);
  assert.match(r.content, /超上限/);
  assert.equal(fs.existsSync(path.join(ROOT, "size/too-big.txt")), false, "超限内容必须零落盘");
});

test("T1.7b write_file 边界 2MB 整放行（上限口径不缩水）", async () => {
  const r = await call("write_file", { path: "size/exact-2mb.txt", content: "y".repeat(2 * 1024 * 1024) });
  assert.equal(r.isError, false, r.content);
  assert.equal(fs.statSync(path.join(ROOT, "size/exact-2mb.txt")).size, 2 * 1024 * 1024);
});

// ============ T1.8 审计日志自读防护（T2 配套：DENY_READ 新增 data/audit.jsonl） ============

test("T1.8 审计日志不可读：xiyouji-agent-web/data/audit.jsonl 命中受保护路径", async () => {
  const r = await call("read_file", { path: "xiyouji-agent-web/data/audit.jsonl" });
  assert.equal(r.isError, true);
  assert.match(r.content, /受保护路径/);
});

// ============ T3 细粒度写入允许域（AGENT_WEB_WRITE_SCOPE） ============

test("T3a 回归样本：未设置 AGENT_WEB_WRITE_SCOPE ＝ 旧行为（scripts/ 与 docs/ 均可写）", async () => {
  await withWriteScope(undefined, async () => {
    const a = await call("write_file", { path: "scripts/legacy-write.py", content: "print(1)\n" });
    assert.equal(a.isError, false, `未设置允许域时 scripts/ 应可写：${a.content}`);
    const b = await call("write_file", { path: "docs/legacy-write.md", content: "# 旧行为\n" });
    assert.equal(b.isError, false, `未设置允许域时 docs/ 应可写：${b.content}`);
  });
});

test("T3b 设置 docs/ 后：docs/ 内通过（含嵌套），scripts/ 拒绝且报出允许域", async () => {
  await withWriteScope("docs/", async () => {
    const ok = await call("write_file", { path: "docs/deep/dir/x.md", content: "在域内\n" });
    assert.equal(ok.isError, false, ok.content);
    assert.equal(fs.readFileSync(path.join(ROOT, "docs/deep/dir/x.md"), "utf8"), "在域内\n");

    const denied = await call("write_file", { path: "scripts/x.py", content: "EVIL" });
    assert.equal(denied.isError, true);
    assert.match(denied.content, /允许域/, `应说明允许域：${denied.content}`);
    assert.match(denied.content, /docs\//, "应回显允许前缀");
    assert.equal(fs.existsSync(path.join(ROOT, "scripts/x.py")), false, "域外写必须零落盘");
  });
});

test("T3c 允许域是前缀边界：docs2/ 不算 docs/ 内（拒绝）", async () => {
  await withWriteScope("docs/", async () => {
    const r = await call("write_file", { path: "docs2/x.md", content: "EVIL" });
    assert.equal(r.isError, true);
    assert.match(r.content, /允许域/);
  });
});

test("T3d 允许域覆盖 edit_file，且域外编辑不改盘", async () => {
  seed("scripts/scope-edit.py", "# ORIGINAL EDIT TARGET\n");
  const abs = path.join(ROOT, "scripts/scope-edit.py");
  const before = sha256(abs);
  await withWriteScope("docs/", async () => {
    const r = await call("edit_file", { path: "scripts/scope-edit.py", old_string: "ORIGINAL", new_string: "EVIL" });
    assert.equal(r.isError, true);
    assert.match(r.content, /允许域/);
  });
  assert.equal(sha256(abs), before, "域外 edit_file 必须零改写");
});

test("T3e 多前缀（含空格/尾斜杠规整）：docs/ 与 scripts/output/ 均放行，scripts/ 其他子目录拒绝", async () => {
  await withWriteScope(" docs/ , scripts/output/ ", async () => {
    const a = await call("write_file", { path: "docs/a.md", content: "A\n" });
    assert.equal(a.isError, false, a.content);
    const b = await call("write_file", { path: "scripts/output/report.json", content: "{}\n" });
    assert.equal(b.isError, false, b.content);
    const c = await call("write_file", { path: "scripts/x.py", content: "EVIL" });
    assert.equal(c.isError, true);
    assert.match(c.content, /允许域/);
  });
});

test("T3f 黑名单优先：允许域设为 docs/ 时 docs/.env 仍报「受保护路径」", async () => {
  await withWriteScope("docs/", async () => {
    const r = await call("write_file", { path: "docs/.env", content: "EVIL" });
    assert.equal(r.isError, true);
    assert.match(r.content, /受保护路径/, "黑名单判据优先于允许域");
    assert.equal(fs.existsSync(path.join(ROOT, "docs/.env")), false);
  });
});

test("T3g 允许域设为 . 等价于未设置（不误伤旧行为）", async () => {
  await withWriteScope(".", async () => {
    const r = await call("write_file", { path: "scripts/dot-scope.py", content: "print(2)\n" });
    assert.equal(r.isError, false, r.content);
  });
});
