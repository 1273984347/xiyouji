# CLAUDE.md — 《详解西游记》AI 速查层

> **定位**：宿主自动加载的 1 分钟速查层——只放「一行规则 + 权威指针」，正文唯一权威在指针目标，本文件禁展开正文；**禁写会漂移的数字与现役值**（版本/计数/门数一律指针化），因此无逐批维护成本、本文件不带版本号。
> **维护契约**：新增必守规则先落权威位置（AGENTS.md §6 或 docs/00-导读/文档规范.md），再在此登记一行；每次改动须复核全部指针目标真实存在；行数上限 60。
> 生成来源：人工撰写（Agent 起草）·生成模型：GLM（ZCode 2026-10-05）·生成日期：2026-10-05·核验状态：已核验（指针逐条 grep 实证·W664）

## 必守规则速查（每条一行 · 权威在指针目标）

1. **E1 铁律**：每个文件修改后 Grep spot-check 验证落地，声明≠落地=假收敛 → AGENTS.md §6-2
2. **写作可验证纪律**：禁「适当/尽快/酌情/相关/必要时」类无判定措辞，量化带单位与比较符，验收标准含期望输出，交付文档头五要素自包含 → docs/00-导读/文档规范.md §4.9
3. **现役口径**：版本号=发布批次编号非 SemVer，「现在什么状态」以 CHANGELOG 顶段为准 → AGENTS.md §1 / CHANGELOG.md 头部
4. **改内联脚本必跑** `python scripts/generate_csp.py`（哈希失配=整脚本被浏览器拒执行）→ AGENTS.md §6-3
5. **批量改 CSS/JS 后**必须验证括号/引号平衡（check_structure.py）→ AGENTS.md §6-4
6. **file:// 铁律**：新页面必须 EMBEDDED 回退 + 零外域依赖 → AGENTS.md §6-5
7. **引文先探针**：写「> 原文引文」前跑 `scripts/_cite_probe.py`，禁凭记忆编造 → AGENTS.md §4.3
8. **级联与并发**：batch_cascade 落盘后按 `_cascade_files_<批号>.txt` 逐面 add；并行批次 pathspec 提交互斥；W 编号动工前在 docs/00-导读/W批次编号对账表.md 登记认领 → AGENTS.md §4.3
9. **commit 规范**：多行信息 Write 临时文件 + `git commit -F`，禁 heredoc；`type(scope): 描述` → AGENTS.md §4.3 / docs/00-导读/文档规范.md §6
10. **禁擅改**：CHANGELOG 历史段、归档、verify_delivery.py、bump_version.py 等管控文件，改动须经用户批准 → docs/00-导读/文档规范.md §11.2

## 常用命令（可直接复制）

```
python scripts/verify_delivery.py        # 提交前唯一硬门禁（pre-commit 自动跑）
python scripts/generate_csp.py --check   # CSP 0 漂移
python scripts/check_doc_sync.py         # 第 31 门禁文档口径体检（--self-test 自测）
python scripts/lint_links.py --dir .     # 全仓链接校验
make ci                                  # lint+test+audit+links 本地预跑 CI
```

## 环境注意（均有仓内出处）

- Windows 多行字符串/heredoc 禁用（Write 临时文件 + `-F` 参数替代）→ AGENTS.md §4.3
- 批量改 md 一律 Python `open(encoding='utf-8')`，禁 PowerShell Set-Content（默认写 UTF-8 BOM）→ AGENTS.md §4.3
- 同文件多个 Edit 必须串行（并行 Edit 基于同一原始内容，后写覆盖先写）→ AGENTS.md §4.3
- 跨 session 动手前先 `git log --oneline -5` + `gh run list` 识别并行增量 → AGENTS.md §4.3

## 接手导航（5 分钟动手）

本文件（1 分钟）→ AGENTS.md 通读（3 分钟）→ 交接文档「零、当前阻塞」「一、当前进度」（1 分钟）→ 动手前跑 `python scripts/verify_delivery.py` 确认基线全绿。
