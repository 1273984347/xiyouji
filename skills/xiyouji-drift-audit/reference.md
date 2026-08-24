# xiyouji-drift-audit 参考手册（命令库 + 案例库）

> 本文件是 `xiyouji-drift-audit` 技能的辅助资料，供步骤 1 前通读。命令以 git-bash 为 shell（`cd D:/1/xiyouji` 风格）；多 session 并发时一切当场实测，勿信快照。

## 一、命令库（按步骤组织）

### 步骤 1 取证

```bash
cd D:/1/xiyouji
git log --oneline -3                 # 最近 3 个提交，识别当前批次
git rev-parse --short HEAD           # 当前 HEAD
git status --porcelain               # 工作区/暂存区状态（区分批次归属）
git ls-files --others --exclude-standard   # 未跟踪文件（逐一核对归属）

# 六文档版本行全量 grep（七处）
grep -n "当前版本" CHANGELOG.md | head -2
grep -n "当前版本" README.md | head -1
grep -n "当前版本" STRUCTURE.md | head -1
grep -n "当前版本" docs/00-导读/项目说明.md | head -3    # 含次级行（bump --desc 坑）
grep -n "当前版本" scripts/output/file-index.md | head -3 # 最新段快照行
grep -o "当前 HEAD = [^）]*）" 交接文档.md | head -1
tail -5 AGENTS.md | grep -E "v[0-9]+\.[0-9]+"            # 版本脚注
```

### 步骤 2 门禁基线

```bash
python scripts/verify_delivery.py    # 17 条门禁（随批次递增），全绿≠无漂移
```

### 步骤 3 file-index 段完整性

```bash
# 段结构检查（门禁已自动化，重点看豁免区 W449-W463 边界）
grep -n "^### v\|^## " scripts/output/file-index.md | head -40   # 段标题序列
grep -c "^| W" scripts/output/file-index.md                      # 登记行数
# 豁免区外空壳段：检查 W463 之后各段是否都有登记行
```

### 步骤 4 方法论 README 双向覆盖

```bash
ls docs/10-方法论沉淀/*.md | sed 's|.*/||' | sort > /tmp/md_list.txt
grep -oE "\[[^]]+\]\([^)]+\.md\)" docs/10-方法论沉淀/README.md | grep -oE "[^()/]+\.md" | sort -u > /tmp/idx_list.txt
comm -3 /tmp/md_list.txt /tmp/idx_list.txt   # 差集 = 双向覆盖缺口
grep -n "待创建" docs/10-方法论沉淀/README.md | head   # 待创建占位必须 0
```

### 步骤 5 skills 双轨

```bash
python scripts/sync_skills.py --check   # 双轨 0 漂移
python scripts/sync_skills.py --sync    # 仓库→全局同步（改仓库后执行）
diff -r skills/ ~/.qwenworkcn/skills/ --exclude=*.pyc 2>/dev/null | head -20   # 全量 diff
# skill 内部数字引用（举一反三）
grep -rn "1[3-6] 门禁\|1[3-6]条门禁" skills/ ~/.qwenworkcn/skills/ --include="*.md" 2>/dev/null | grep -v "案例\|W49[0-9] 事发\|历史" | head
```

### 步骤 6 治理文档内容引用核验

```bash
# 文档规范.md：门禁数/脚本清单/行号
grep -n "门禁\|check_" docs/00-导读/文档规范.md | head -30
# 文档规范引用的 scripts/ 文件是否都存在（第 17 门禁已自动化，人工复核行号引用）
grep -oE "scripts/[a-z0-9_]+\.(py|js)" docs/00-导读/文档规范.md | sort -u
# AGENTS §4.2 门禁清单 vs 仓库实际
grep -n "^\s*[0-9]\+\. \*\*" AGENTS.md | head -20
ls scripts/check_*.py scripts/check_*.js | sort
# workflows/README 旁文档（里程碑同步类）
head -3 .github/workflows/README.md
grep -n "W4[5-9][0-9]\|W500" .github/workflows/README.md | head -6
# 其他：新Agent启动Prompt 计数、DESIGN 门禁引用、skills/README、统计口径
grep -n "611\|209\|86\|门禁" 新Agent启动Prompt.md | head -10
grep -n "门禁" DESIGN.md | head -3
```

### 步骤 7 孤儿提交

```bash
git log --oneline | head -60          # 人工核对每个提交的 W 段归属
git log --format="%h %s" --grep="W[0-9]\{3\}" | head   # 带 W 的提交
# 无 W 段的提交 = 候选孤儿，对照 CHANGELOG 版段确认
```

### 修复后验证

```bash
python scripts/verify_delivery.py     # 17 门禁全绿
python scripts/sync_skills.py --check # 双轨 0 漂移
git diff --name-only                  # 确认改动范围，非必要改动 git restore
```

## 二、案例库（W499 三轮回溯 8 类漂移，2026-08-24）

### 类型 A：file-index 段结构损坏（P1）
- **现象**：段空壳/重复/乱序/残留"当前版本"快照行。
- **案例**：W449-W463 历史损坏区（已豁免，维持现状不重排）；W499 后第 17 门禁只防豁免区外新增。
- **判据**：豁免区外空壳段/重复 W 号/最新段残留 = FAIL；豁免区内 = 记录不判。

### 类型 B：方法论 README 索引滞后（P1）
- **现象**：目录 md 与索引链接差集、待创建占位残留、链接陈旧。
- **修复**：差集归并后登记 file-index + CHANGELOG。

### 类型 C：CHANGELOG 编号上限手工漏改（P2→第 17 门禁转正后 FAIL）
- **现象**：编号规则段"W### ID（W001-W###）"上限落后于最新 W 段。
- **教训**：W499 曾手工漏改，仅 WARN。

### 类型 D：治理文档内容引用漂移（P1/P2，W499 盲区核心）
- **现象**：文档规范.md §8 门禁表 / §11.1 门禁列 / §11.2 禁改清单的门禁数、脚本名、行号引用与实际不符（当次 6 处）。
- **根因**（复盘三连）：①审查范围锚定已知漂移模式，漏内容引用型；②方法论 README 被抓是偶然，文档规范.md 未被同等核验——先假设再取证；③门禁全绿给覆盖错觉，文档规范.md 整个在 verify 保护范围外。
- **防线**：第 17 门禁检查项 6（文档规范 scripts 引用存在性）+ 本技能步骤 6。

### 类型 E：旁文档版本/里程碑滞后（P1）
- **现象**：`.github/workflows/README.md` 头部版本停 v2.3.64 W449、里程碑行停 W426，缺 W427-W500 共 74 批次（48 批零同步）。
- **要点**：文档规范 §11.1 第 8 项要求里程碑同步；属"里程碑同步"类，不宜做硬 FAIL（日常工程批次会被卡），靠人工审查。

### 类型 F：暂存批次未登记（P1）
- **现象**：工作区/暂存区有改动但双索引（file-index + CHANGELOG）未登记新批次。
- **处置**：确认批次归属清晰后按双索引铁律登记；W499/W500 双批待提交是常态待办，非漂移。

### 类型 G：孤儿提交（P1/P2）
- **现象**：git log 中无 W 段、无法对应 CHANGELOG 版段的提交。
- **判据**：确认为孤儿则 P1（治理断裂）；历史合并类提交可豁免。

### 类型 H：未跟踪杂项（P3）
- **现象**：非 `_` 前缀脚本/文档未入库（如 baseline_snapshot.py 从未提交）、大文件待决（大厂分析.txt 70KB）。
- **处置**：`_` 前缀豁免；非 `_` 前缀必须入库；待决项标记不判漂移。

### 举一反三型（类型 D 的扩展，W499 第三轮）
- **现象**：skill 内部数字引用滞后——day-review SKILL.md"退出码 0 只代表 15 条门禁通过"（实际 17 条）。
- **修复要点**：去掉硬编码数字改为"全部门禁（现 17 条，随批次递增、以 verify 输出为准）"，从根上防未来再漂。
- **扫描覆盖**：全仓库"14/15/16 门禁"其余引用均为历史事件描述（W493/W495/W498 事发时点），按 E2 判据保留。

## 三、E2 历史保留判据（防误改）

| 表述 | 判定 |
|---|---|
| "退出码 0 只代表 15 条门禁通过"（现役描述） | 漂移，改 |
| "W493 事发时 14 门禁全绿漏网"（历史事件） | 非漂移，保留 |
| "W495 第 15 门禁转正"（历史登记） | 非漂移，保留 |
| 观测基线快照 W464 生成（快照语义） | 计数与当前一致即无漂移 |
| 版本概览.md（内容导读文档） | 无版本行引用即无漂移 |

## 四、修复登记流程（防修复本身造成新漂移）

1. 改治理文档 → 双索引登记：file-index 最新 W 段补行 + CHANGELOG 对应版段文件行补名。
2. 改 skill → 仓库版改完跑 `sync_skills.py --sync` 同步全局，再 `--check` 验证双轨 0 漂移。
3. 修数字引用 → 优先去硬编码（"现 17 条，随批次递增、以 verify 输出为准"），从根防漂。
4. 全部修复后：verify 全绿 + 双轨 --check 0 漂移 + `git diff --name-only` 范围核对。
