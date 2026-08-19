# 项目级 Skills 索引（17 个）

> 2026-08-19 治理：AGENTS.md §4.5 已同步为 17 个（W484 修复 14 个 + W485 收录 visual-batch / plan-authoring / plan-review）；5 个角色 skill 的 `agents/openai.yaml` 已修复；三个 TRAE 蒸馏 skill 已做平台适配（路径占位符 + 工具映射，见各 SKILL.md 文首「平台适配」）。2026-08-19 W486：四个会话流程 skill 已同步上游协议修正（verdict 7 词全序 / R0 4 件套 / 过拟合警报增强版 / P2 ≤ N_max / work-log 路径 / bridge_note 定义 / 整合版协调声明）。2026-08-19 W487：二轮同步（DRL 未安装降级声明 + experience-capture 格式规范 + self-evolution 触发词扩充）。

| Skill | 类别 | 用途 | 何时用 |
|---|---|---|---|
| agent-session-loop | 会话流程 | 审查 → 收尾 → 沉淀 三阶段整合流水线 | 收尾 / 复检 / 复盘 / retro、长文档或批量修复后 |
| deep-review-loop | 会话流程 | DRL 5 轮深度审查（R0→R3 + V1→V5 + 4 层过拟合防护） | plan/spec/skill 写完后、批量修复、怀疑假收敛 |
| mem-wrap-up | 会话流程 | 7 步 session 收尾 + memory 审计 + 文档同步 spot-check | session 收尾、文档与代码不一致 |
| self-evolution | 会话流程 | 快速 3 问 / 全面 11 维度复盘 + 知识层升级 | 任务完成、全面复盘 / 周汇总 / retro |
| xiyouji-sun-wukong | 角色 | 孙悟空知识库与内容生产规范 | 悟空相关问答 / 创作 / 扩写 |
| xiyouji-zhu-bajie | 角色 | 猪八戒知识库与内容生产规范 | 八戒相关问答 / 创作 / 扩写 |
| xiyouji-sha-seng | 角色 | 沙僧知识库与内容生产规范 | 沙僧相关问答 / 创作 / 扩写 |
| xiyouji-tangseng | 角色 | 唐僧知识库与内容生产规范 | 唐僧相关问答 / 创作 / 扩写 |
| xiyouji-bai-longma | 角色 | 白龙马知识库与内容生产规范 | 白龙马相关问答 / 创作 / 扩写 |
| xiyouji-character-content | 内容 | A3 人物深度分析四家族模板 + 质量门禁 | 撰写 / 修改人物分析 |
| xiyouji-characters-knowledge | 知识 | 人物问答取证（roster 211 + 数据源优先级） | 人物问答 / 事实核查 |
| xiyouji-version-bump | 流程 | 版本 bump + 六文档同步 | W 批次提交 |
| xiyouji-en-translation | 流程 | 英文站可视化页英文化 | 续译 / 拆页翻译 |
| xiyouji-s4-submission | 流程 | S4 学术投稿前准备 | 投稿检查 / line 号校核 / 匿名稿 |
| xiyouji-visual-batch | 流程 | Phase E 视觉批次执行管线（探针→令牌化→传播→验证→门禁→version-bump） | 执行视觉批次 / E1-E7 / 令牌化 / 传播批次 |
| xiyouji-plan-authoring | 流程 | W 批次路线图/方案撰写（九段结构 + 实测取证 + 三问收尾） | 写方案 / 路线图 / roadmap / 阶段规划 |
| xiyouji-plan-review | 流程 | 方案/文档评估（取证硬门槛 + 五维评估 + 证据基线表） | 评估方案 / plan review / 方案审查 |

## 说明

- 四个会话流程 skill 源自 TRAE 全局，仓库版已做平台适配：运行路径一律用 `<memory_root>` / `<skills_root>` 占位符，工具名按各文件文首「平台适配」映射（TRAE Task → 平台子代理、RunCommand → shell/PowerShell 等）。
- W486（2026-08-19）已把上游 GitHub 四仓库的 Claude Code 协议修正同步入库（协议内容层对齐，工程件如 evals/CI/fragment-lint 不随副本进入）。
- W487（2026-08-19）二轮同步：mem-wrap-up 补 DRL 未安装降级声明；self-evolution 触发词扩充并新增 `references/experience-capture-format.md`（经验写入格式规范）。
- agent-session-loop 的 `references/` 为精简快速路径，完整协议以三个独立 skill（deep-review-loop / mem-wrap-up / self-evolution）当前版本为准。
- visual-batch / plan-authoring / plan-review 三 skill 于 W485 从 `D:\1\skills`（全局目录）收录入库，playbook 内容与 Phase E 方案/批次记录配套。
- 角色 / 内容 / 知识 skill 为 agent 可安装格式（`agents/openai.yaml`）。
- 维护自检：`python scripts/_check_skills.py`（frontmatter / openai.yaml 残留 / references 链接）。
