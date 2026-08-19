# 经验捕获格式规范（Experience Capture Format）

> 本文件在快速模式（模式 A Step 2）写入时激活。定义经验写入的格式、质量标准与边界纪律。
> 从 Claude Code vault 版 experience-capture skill 蒸馏而来（剥离项目特定编号 FT/ST、hooks/脚本引用、session 代号）。

## 1. 写入格式（3 个文件，Edit 工具末尾追加）

### experience-log.md（完整条目，权威源）

```markdown
## [日期] — [任务名称] | **Tags:** [tag1, tag2, tag3]

### [新发现 / 踩坑 / Skill 缺口]
[具体内容]

### 根因（如果是踩坑）
[分析]

### 下次怎么做
[具体行动方案]
```

规则：每条经验独立一个块，用 `---` 分隔；任务简述 ≤20 字；内容必须具体（❌「要小心一点」✅「asyncpg 禁止 ::type cast」）；「下次怎么做」必须是可执行的动作。

### experience-quickref.md（速查规则，只写有明确规则的）

```markdown
[编号] [关键词] — [一句话规则]
```

规则：只更新有明确规则的条目，纯描述不写入。

### skill-usage-checklist.md（Skill 缺口）

```markdown
| [Skill名] | [场景] | [为什么没用] |
```

规则：只有「本该用但没用」的缺口才写入，无缺口不创建。

## 2. 质量标准（好经验 vs 差经验）

**好经验**：
- 有具体文件名 / 函数名 / 行号
- 有明确的根因分析
- 「下次怎么做」是可执行的动作

**差经验**（禁止）：
- ❌「要小心一点」
- ❌「代码有 bug」
- ❌「下次注意」

**示例（good）**：

```markdown
## 2026-08-01 — 日志轮转配置修复 | **Tags:** logging, 运维

### 踩坑：logrotate 配置生效但文件未轮转

`/etc/logrotate.d/app.conf` 中 `missingok` 拼写错误导致静默失败，日志文件持续增长。

### 根因
logrotate 对无效配置静默跳过（不报错），人工验证只看了配置存在，未看实际轮转时间戳。

### 下次怎么做
改 logrotate 配置后必须 `logrotate -d` dry-run 验证 + 检查 `/var/lib/logrotate/status` 时间戳是否更新。
```

## 3. 边界纪律（防越权）

- **只写 3 个文件**（experience-log / experience-quickref / skill-usage-checklist），不碰 heuristic / policy / H-rule
- **不做模式分析或升级决策**——那是 self-evolution 全面模式的职责；捕获只记录原始事件
- **用 Edit 工具追加**（不用 bash echo/printf——特殊字符破坏格式），追加到文件末尾，保留顺序
- 捕获是 write-only；升级判定（≥3 次 → pattern/heuristic）由全面模式 Step 4 负责

## 4. 手动触发模式

用户显式说「记住这个」/「经验沉淀」/「capture」时，按快速模式执行本节写入（不等待任务完成自动触发）。

## 5. 编号规则（通用前缀）

- `PI` = 通用 / 流程（Process & Infrastructure）
- `SK` = Skill 使用（Skill usage）

（本地项目可扩展自己的前缀，如 FT / ST 等；开源版只定义通用两个。）

## 6. 与 self-evolution 的关系

```
self-evolution（脑 + 手）
    ├─ 快速模式: 3 问自检 → 按本文件格式直接写入 3 个文件 → 模式升级检查
    └─ 全面模式: 11 维度分析 → 知识层升级 → 行动项执行

本文件（格式参考）:
    - 定义写入格式和质量标准
    - 被快速模式内联执行，不单独作为独立 skill 调用
```
