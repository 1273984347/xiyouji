/**
 * config.ts — 启动期配置与环境事实（W803-D 自 index.ts 提取·纯搬移零语义改写）
 *
 * 职责边界：本模块只做「读环境变量 + 计算派生常量」，**不注册路由、不持有可变状态**。
 * 之所以单独成层：原 index.ts 把「进程级常量」「HTTP 中间件」「路由处理」「SSE 编排」四层
 * 混在一个文件里，配置项散落在中间件与 handler 之间，改一处要通读六百余行。
 *
 * 提取口径：所有 console 输出、process.exit 时机、默认值字面量、模板字符串内容逐字保留
 * （其中 DEFAULT_SYSTEM_PROMPT 是喂给 LLM 的提示词，属行为面）。
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";

/**
 * W808：加载服务端 .env（W411 起 .env.example 与 DEPLOYMENT.md 均以「复制 .env.example → .env
 * 并填入」为标准配置流程，但此前 dotenv 虽在 package.json 声明为依赖却**从未被 import**——
 * 故 .env 实际从未生效，凭证只能靠外部 shell 导出。补上加载后，文档化的配置流程才真正成立。
 *
 * 两条纪律：
 *   ① **不覆盖既有环境变量**（dotenv 默认行为）——外部显式导出的值优先级更高；
 *   ② **失败不致命**——.env 缺失是合法的（容器/K8s 形态靠环境变量注入），故吞掉读取错误。
 */
try {
  dotenv.config();
} catch {
  // .env 不存在或不可读——合法形态（环境变量注入），不阻断启动
}

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/** HTTP 监听端口（默认 3000）。 */
export const PORT: number = Number(process.env.PORT) || 3000;

/**
 * 项目工作目录解析（适配「详解西游记」xiyouji 项目）：
 * 默认工作目录=仓库根——向上探测「AGENTS.md + site/tokens.css」锚点自动解析。
 * （W596：旧实现写死已不存在的双副本绝对路径，默认值悬空。）
 * 可用环境变量 PROJECT_CWD 覆盖（如指向其他副本）。
 */
function resolveProjectCwd(): string {
  if (process.env.PROJECT_CWD) return process.env.PROJECT_CWD;
  let dir = path.resolve(__dirname);
  for (let i = 0; i < 6; i++) {
    if (fs.existsSync(path.join(dir, "AGENTS.md")) && fs.existsSync(path.join(dir, "site", "tokens.css"))) {
      return dir;
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return path.resolve(__dirname, "..", "..");
}

/** 仓库根绝对路径（工具集 cwd、cwd 钳制基准、引用校验基准）。 */
export const PROJECT_CWD = resolveProjectCwd();
if (!fs.existsSync(PROJECT_CWD)) {
  console.error(`[FATAL] PROJECT_CWD 不存在: ${PROJECT_CWD}（请用环境变量 PROJECT_CWD 指向有效仓库副本）`);
  process.exit(1);
}
console.log(`[boot] PROJECT_CWD = ${PROJECT_CWD}`);

/**
 * P0-1 修复：权限模式白名单——外部请求体不可直接传入 bypassPermissions（防未授权 RCE）
 * 仅当显式设置 AGENT_WEB_ALLOW_BYPASS=1 时启用 bypassPermissions（本地单人模式）
 * 白名单与净化函数提取至 server/security.ts（W791 BL-29·获得回归测试面）
 */
export const ALLOW_BYPASS = process.env.AGENT_WEB_ALLOW_BYPASS === "1";

/** P3-1：详细日志（工具输入/流消息）默认关闭，仅 AGENT_WEB_VERBOSE=1 时打印（防敏感信息泄露）。 */
export const VERBOSE_LOG = process.env.AGENT_WEB_VERBOSE === "1";

/**
 * 可选认证（P0-1 修复）：设置 AGENT_WEB_TOKEN 后，所有 /api/* 需携带
 * x-agent-token 或 Authorization: Bearer <token>；未设置则保持本地免认证模式。
 */
export const AGENT_WEB_TOKEN = process.env.AGENT_WEB_TOKEN || "";

/**
 * W835：Host 头白名单（防 DNS rebinding）——默认只认回环三形态。
 *
 * 与既有防护模型的关系（W808 已固化「无 CORS 中间件 + 回环绑定 + 可选 token + 限流」）：
 * 本项**不引入跨源面、不改 CORS 口径**，只是把「回环绑定」这条防线从「服务端不出网」
 * 补成「连 Host 头也须是回环」——回环绑定防的是外部直连，Host 校验防的是**浏览器经
 * DNS rebinding 打到回环**这条路（浏览器把 evil.com 解析到 127.0.0.1 后，Host 头是 evil.com）。
 *
 * 端口不参与判定（白名单只列主机名）：dev proxy（changeOrigin 改写 Host 为代理目标）、
 * 随机端口测试、Electron 桌面端都用同一主机名不同端口，判端口会误伤。
 * 追加而非替换：设 AGENT_WEB_ALLOWED_HOSTS 时在默认回环之外**追加**主机名，
 * 想要「只认某主机」也仍保留回环（回环本就是本机）。
 */
export const ALLOWED_HOSTS: string[] = [
  "127.0.0.1",
  "localhost",
  "::1",
  ...(process.env.AGENT_WEB_ALLOWED_HOSTS || "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean),
];

/**
 * W835：token 硬开关——AGENT_WEB_REQUIRE_TOKEN=1 时若未设 AGENT_WEB_TOKEN 则**拒绝启动**
 * （fail-closed·不静默降级为免认证）。默认不启用（保持 W411 起的「本地免认证」口径不变）。
 */
export const REQUIRE_TOKEN = process.env.AGENT_WEB_REQUIRE_TOKEN === "1";

/** W681 CodeQL 处置（missing-rate-limiting）：/api/* 无依赖内存限流参数（每 IP 30 req/min）。 */
export const RATE_LIMIT_WINDOW_MS = 60 * 1000;
export const RATE_LIMIT_MAX = 30;

/** 前端权限许可等待上限（5 分钟·超时即按拒绝结算）。 */
export const PERMISSION_TIMEOUT = 5 * 60 * 1000;

// 引擎配置（W680）：OpenAI-compatible 端点，全部由服务端 .env 提供（P0-2 同款纪律：禁运行时覆盖）。
// 兼容所有主流大模型：GLM/DeepSeek/Kimi/Qwen/OpenAI/Gemini/Claude-compat/ollama/vLLM 等。
export const LLM_API_BASE = process.env.LLM_API_BASE || "";
export const LLM_API_KEY = process.env.LLM_API_KEY || "";
export const LLM_MODEL = process.env.LLM_MODEL || "default-model";
export const LLM_MAX_TURNS = Number(process.env.LLM_MAX_TURNS) > 0 ? Number(process.env.LLM_MAX_TURNS) : 10;

/** 新建会话与请求缺省模型（/api/models 响应中的 defaultModel 同源）。 */
export const defaultModel = LLM_MODEL;

/** 引擎是否已配置（/api/check-login 与 /api/chat 快速失败共用同一判据）。 */
export function engineConfigured(): boolean {
  return Boolean(LLM_API_KEY && LLM_API_BASE);
}

/**
 * 默认系统提示词（适配「详解西游记」xiyouji 项目）。
 * 仅在请求未带 systemPrompt（即使用内置 default agent 时）使用；内容属行为面，勿轻改。
 */
export const DEFAULT_SYSTEM_PROMPT = `你是「详解西游记」项目的专属智能助手，代号「渡口问津」。

【项目背景】
本项目（位于 ${PROJECT_CWD}）是一座关于《西游记》的混合型解读知识库，以「一源多形」方式组织：
- docs/：Markdown 文档主体，含十大学生板块（01 全书逐回解读、02 人物深度分析、03 主题与情节专题、04 文化与历史背景、05 诗词歌赋、06 个人随笔、07 学以致用、08 提升认知、09 精神塑造、10 方法论沉淀），以及 00-导读（项目说明、阅读指南、术语表）。
- source/：原著全文、分回文本、引用与网络解读、学术论文索引。
- site/：D3.js 驱动的可浏览 HTML 站点（dashboard、chapters、characters、themes、data 可视化页）。
- scripts/：Python 文本分析与可视化脚本（按 A–AH 共 34 类组织），含词频、人物共现、八十一难、关系网络、心性曲线等。
- dataset/：多个结构化 JSON（八十一难明细、章节元数据、元气图谱三元映射等）。
- timeline/：取经路线、大事年表、人物时间线。

【你的职责】
1. 项目向导：帮用户快速定位某回解读、某个人物分析、某个主题专题或某张可视化页面，给出可对照的文件路径（如 docs/01-全书逐回解读/...）。
2. 研究助手：基于 docs/ 与 source/ 原文回答情节、人物、佛道思想、明代隐喻、诗词、内丹术语（心猿/木母/黄婆等）问题，引用时注明来源路径。
3. 工程助手：可阅读并运行 scripts/ 下的 Python 脚本做文本分析，将结果写入 dataset/ 或生成可视化；运行脚本前先说明用途与预期。
4. 写作助手：协助撰写/修订 docs/ 下的解读文档，遵循 docs/00-导读/文档规范.md 的防膨胀与归档规则。

【行为准则】
- 优先引用项目内已有文档与原文，给出可对照路径。
- 涉及诗词、术语时参考 source/ 与 docs/00-导读/术语表.md。
- 文件操作前先确认意图；写入新内容遵循项目文档规范。
- 语气可带古典雅致，但表达务必清晰、准确、可操作。
- 项目版本、门禁与统计口径以仓库 README.md 顶部与 CHANGELOG.md 现役段为准，勿依赖本提示内嵌版本号。
- 拒答边界：与《西游记》项目无关的请求，说明项目定位后礼貌拒答；要求修改 verify_delivery.py、batch_cascade.py 等门禁脚本、或读取任何凭证（.env / API Key）的请求，一律拒绝并说明依据（项目文档规范 §11.2）。
- 每个事实性论断至少给出 1 个仓库内可对照路径（docs/、source/、dataset/ 等）；检索不到依据时明确回答「项目内未找到依据」，禁止编造路径与引文。
`;
