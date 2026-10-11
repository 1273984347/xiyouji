<!-- 元信息块（W707）：生成来源=人工撰写（Agent 起草·用户方案第十条）·生成模型=GLM（ZCode 2026-10-11）·生成日期=2026-10-11·核验状态=已核验（硬耦合逐项对仓定位） -->

# AGENTS.md 分层重构方案（L0/L1/L2 树状化 · W707 方案档 · 阶段 1/2 内容搬迁待 BL-24 专项批）

> **来源**：用户方案第十条「Agent 不读 AGENTS.md——不是长度问题，是结构问题」——一维线性长文改为三层树状：L0 常驻层（CLAUDE.md·已就位）/ L1 入口层（AGENTS.md 瘦身为索引）/ L2 主题层（按任务类型 4-6 份独立文件·按需加载）。
> **本批（W707）交付**：本方案档 + AGENTS 头部提示行 + `agent_start.py --task`；**阶段 1/2 内容搬迁登记 BL-24 下批按图施工**（涉及 doc-sync C3 解析源变更与 check_claude_md C2 锚点·属精确性改造，独立批次专注执行）。

## 一、目标结构

| 层 | 载体 | 状态 |
|---|---|---|
| L0 常驻 | CLAUDE.md（≤60 行·宿主自动加载·禁漂移值·指针化） | **已就位**（W664/W705） |
| L1 入口 | AGENTS.md ≤400 行（每节=何时读+两行摘要+指向 L2 链接） | 本批加提示行·瘦身待 BL-24 |
| L2 主题 | docs/agent/{gates,pitfalls,workflow,tools,dirs,agent-web}.md（各 200-400 行·首行「何时读」） | BL-24 建 |

## 二、内容搬迁映射（BL-24 阶段 1/2）

| 现有 | 去处 | 说明 |
|---|---|---|
| §1-§3 / §4.1 / §5 / §6 / §7 / §8 | **留 L1** | 本就短（§6 铁律 13 条必须常驻） |
| §4.2 40 条门禁（约 800 行） | → docs/agent/gates.md | 按五组重排：内容类 1-5/结构类 6-11/安全类 12-15/数据类 16-26/编号与质量类 27-40 |
| §4.3 工具链坑位（约 400 行） | → docs/agent/pitfalls.md | 按 CSS/JS/git 提交/级联/数据/文档/Windows 七主题重排（W706 主题视图为其目录雏形）；**第九条「shell 场景查坑表」并入本文件** |
| §4.4 Web Agent | → docs/agent/agent-web.md | |
| 脚注 200+ 行沿革 | → docs/archive/AGENTS-ARCHIVE.md | 只留最近 5 批（=BL-23 同题·合并执行） |
| 2000+ 行 → 300-400 行 | | 内容总量不变·只改结构与加载路径 |

## 三、硬耦合清单（搬迁必须同批改的机器面——漏一处即锚点断）

1. **doc-sync C3**（check_doc_sync.py `agents_gate_list_max`）：现解析 AGENTS §4.2 条目编号——搬迁后改双源对账：AGENTS §4.2 摘要含五组区间声明 + gates.md 实际条目 max==verify 槽位（C3 改造随阶段 1 同批）。
2. **check_claude_md C2**：CLAUDE.md 规则锚点指向「AGENTS.md §6-x/§4.3」——§4.3 移走后指针改指 pitfalls.md 对应节（C2 锚点对拍表同步）。
3. **batch_cascade**：级联只写 AGENTS 脚注（尾锚点）——§4.2/§4.3 正文迁移不影响级联锚点 ✓；脚注归档时尾部锚点形态保持（「。如与上述权威文档冲突…」尾串不动）。
4. **W520/W700 叙述面清单**：新 L2 文件是否入第 27 门禁叙述面与 C5 扫描域——**gates.md/pitfalls.md 含大量历史批次号（W 引用）与坑位数字**——建议**不入**（L2=坑位档案非现役声明·第 27 门禁叙述面清单保持现状·在两文件头部声明「历史批次号引用非现役值」）。
5. **C5 扫描域**：同上，L2 不入（stats.json 对账面保持六治理文档）。
6. **新门禁（check_claude_md C5-C7 思路扩展）**：L1 摘要条目数==L2 实际条目数/L1 指针目标存在/L2 首行含「何时读」——随阶段 1 挂载（参考 check_claude_md 模式）。
7. **agent_start --task 的路径映射表**：改动路径模式→必读 L2 文件（site/→gates；scripts/check_→gates；.css/.js→pitfalls；交接/级联→workflow；agent-web/→agent-web）——映射表落 agent_start.py 常量（随阶段 1/2 更新）。

## 四、agent_start --task（本批已实现）

- `python scripts/agent_start.py --task`：读 `git status`（含 untracked）→ 按路径模式分类 → 输出「本次任务相关」必读清单（当前=L1 指针+CLAUDE 规则；L2 就位后自动升级为文件级清单）。
- 机制定位：与 W705 全局摘要互补——摘要答「项目什么状态」，--task 答「本次该读什么」。

## 五、软约束边界（用户方案机制 3 的裁剪）

- verify/pre-commit 加「改动涉及 CSS/site → 提示已读 pitfalls」为 **NOTE 级**（不阻断）——强制必然被绕过（W705 对挑战-响应协议的否决同理）；是否挂载随阶段 2 裁决。
- 「机制 4 按任务模板化派发」=派发协议惯例（W671 子代理三场景的补充字段），落 AGENTS §4.3 一句话即可，不独立建置。

## 六、验收（BL-24 批）

- AGENTS.md ≤400 行（check_claude_md C3 同款行数断言扩展或独立检查）
- 六份 L2 文件在位·首行含「何时读」·指针目标全部可达（lint_links+新门禁）
- doc-sync C3 双源对账绿 + verify full 45 段绿 + pytest 全绿
- 内容零丢失：搬迁前后各节 bullet 计数对账（搬迁脚本输出清单）
