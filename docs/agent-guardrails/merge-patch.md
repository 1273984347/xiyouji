# 合并补丁块（可直接套用；本文件不是规则正文）

> 背景：仓库根目录**已有** `CLAUDE.md`（52 行 / 16 条，宿主自动加载）与 `AGENTS.md`（31 KB 治理手册）。
> 所以本目录不再放第二份 `CLAUDE.md` —— 那永远不会被自动加载。这里只给「插入位置 + 可复制措辞」。
> 行号基于本批 HEAD `f647726e` 实读；合并前请用 `git show HEAD:CLAUDE.md | Select-String "^16\."` 复核锚点。

## 1. 去重映射：8 条候选里 7 条已被根文件覆盖

| # | 候选规则（初稿） | 根 `CLAUDE.md` 现状 | 结论 |
|---|---|---|---|
| 1 | 改内联脚本重跑 CSP | 第 14 行 规则 4 | **去重**，不重复写 |
| 2 | 提交前跑 verify_delivery | 第 32-33 行「常用命令」+ 第 6 行维护契约 | 已有，仅需在新增规则行里引用 |
| 3 | 提交前跑 pytest | 无（仅 `make ci` 间接覆盖，第 37 行） | **新增 1 行命令** |
| 4 | Python 改完跑结构检查 | 无 | **真新增**（规则 1 条 + 命令 1 行） |
| 5 | file:// 铁律 | 第 16 行 规则 6 | 去重 |
| 6 | 计数/版本同步、历史段禁改 | 第 13 行 规则 3 + 第 20 行 规则 10 + 第 35 行命令 | 去重 |
| 7 | PowerShell BOM / md 编码 / 同文件 Edit 串行 | 第 43-44 行「环境注意」 | 去重 |
| 8 | 禁改门禁脚本、禁 CodeBuddy | 第 20 行 规则 10 + 第 24 行 规则 14 | 去重 |

结论：**只新增 1 条规则（规则 17）+ 2 条命令**。根文件 52 行 → 55 行，仍满足 ≤60 行维护契约。

## 2. 补丁 A：根 `CLAUDE.md` 必守规则（1 条）

**位置**：第 26 行（`16. **提交前三问**…`）之后、第 28 行 `## 常用命令` 之前。整块插入：

```markdown
17. **Python 改动自检**：改完跑 `pwsh -File scripts/guardrails/check_changed.ps1`（ruff 风格档 + 结构档 + 嵌套推导式，退出码 0 才算过）；单测 `py -3 -m pytest tests -q`；提交前 `py -3 scripts/verify_delivery.py --scope auto` → docs/agent-guardrails/README.md
```

## 3. 补丁 B：根 `CLAUDE.md` 常用命令（2 行）

**位置**：第 35 行（`python scripts/check_doc_sync.py …`）之后、第 36 行（`python scripts/lint_links.py …`）之前。整块插入：

```
pwsh -File scripts/guardrails/check_changed.ps1   # Python 改动结构检查（只扫改动文件；Unix/CI 用 .sh）
py -3 -m pytest tests -q                  # 单测（pytest.ini 自带 -v，-q 只降噪）
```

> Windows 侧 `python` 是执行存根，故这里写 `py -3`；根文件其它 `python …` 是可移植形态，两种写法并存不冲突。

## 4. 补丁 C：`AGENTS.md` §6 权威层（1 条）

**位置**：第 278 行（`19. **禁用 CodeBuddy/WorkBuddy…`）之后、第 280 行 `---` 之前。整块插入：

```markdown
20. **Python 改动结构检查（W#### 立·用户令）**：改动 .py 后必须跑 `pwsh -File scripts/guardrails/check_changed.ps1`（ruff 风格档/结构档/嵌套推导式，退出码 0 才过；`api_diff.py` 报破坏性变化须在提交说明写明）；阈值与收紧路线见 docs/agent-guardrails/README.md；新增阈值/豁免须按 16-⑦ 报批。
```

`W####` 合并时用 `python scripts/reserve_w.py` 的返回值填（禁手填猜测号）。

> 为什么先落 AGENTS 再落 CLAUDE：根 `CLAUDE.md` 第 6 行维护契约要求「新增必守规则先落权威位置（AGENTS §6 或文档规范），再在此登记一行」。顺序反了会违反自身契约。

## 5. 补丁 D：`pyproject.toml` 增量片段（**阶段 2 才合并**）

**现在不要合并**：实测全仓命中 C901@15 = 30 条、PLR0912@16 = 20 条、PLR0915@80 = 4 条，合计约 54 条；一旦进 `select`，`make lint` 与 CI 立刻全仓红——违反「一开全红没人会留着」。

达到「阶段 2」触发条件后再合并（见 README §6）。片段（保留原有 `select` 六类，仅追加三类）：

```toml
[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "C90", "PLR0912", "PLR0915"]  # 新增后三类
# ignore 保持原样（E501 / UP031）

[tool.ruff.lint.mccabe]
max-complexity = 15

[tool.ruff.lint.pylint]
max-branches = 16
max-statements = 80
```

**为什么 `PLR1702` 不进 pyproject**：它只在 `preview = true` 下生效；而 preview 会连带改变已启用规则的行为——实测同一文件 E231 从 0 涨到 30 条（`scripts/spot_check_nlp.py`），全仓 E231/E302/E305/E241 多出约 70 条，与 CI（跑根配置、未开 preview）结论不一致。故嵌套深度单独留在 `scripts/guardrails/ruff-structure.toml`。

## 6. 两套配置为什么不打架（加载优先级）

ruff 0.16.9 的**自动发现文件名只有三个**：`ruff.toml` / `.ruff.toml` / `pyproject.toml`。
本目录配置特意命名 `ruff-structure.toml` —— **不在自动发现列表内**，因此：

| 场景 | 实际加载 | 规则集 |
|---|---|---|
| `ruff check .`（CI / make lint） | 根 `pyproject.toml` | E/F/W/I/UP/B（CI 同源） |
| `ruff check <任何文件>`（不带 --config） | 仍是 `pyproject.toml` | 同上 |
| `check_changed.ps1` / `.sh` | `--config` 显式加载 `ruff-structure.toml` | C90/PLR0912/PLR0915/PLR1702 |

- 优先级：**显式 `--config` > 目录发现**；本目录文件不会再被结构档「劫持」（旧文件名 `ruff.toml` 时实测会发生，已改名根治）。
- 规则集互不重叠：结构档只 select 四条结构规则，preview 的副作用被限制在这四条内。
- 复核命令（应输出 `All checks passed!`，证明未被自动接管）：
  `ruff check tests/fixtures/_sample.py`
  应输出 2 条（证明显式加载有效）：
  `ruff check --config scripts/guardrails/ruff-structure.toml tests/fixtures/_sample.py`

## 7. 提交钩子 / CI 片段

**钩子**（现役是手写 `.git/hooks/pre-commit`，**不要** `pre-commit install`，会覆盖它）。
在 `verify_delivery` 调用之后整块追加（`$ROOT` 是钩子里已有的仓库根变量）。
注意：实际挂载版只检查**暂存区**的 .py（`git diff --cached --diff-filter=ACM`），并豁免 `tmpe/` 与 `_` 前缀；`--strict-api` = 宽档阈值 + api_diff 阻断（once_call 仍只提示）：

```sh
# agent-guardrails：只检查暂存区的 .py（追加在 gitleaks + verify_delivery 之后，不替换任何既有检查）
STAGED_PY=$(git -C "$ROOT" diff --cached --name-only --diff-filter=ACM -- '*.py' | while IFS= read -r f; do
  [ -n "$f" ] || continue
  case "$f" in tmpe/*) continue ;; esac
  case "${f##*/}" in _*) continue ;; esac
  [ -f "$ROOT/$f" ] && printf '%s\n' "$f"
done)
if [ -n "$STAGED_PY" ]; then
  bash "$ROOT/scripts/guardrails/check_changed.sh" --strict-api $STAGED_PY || exit 1
fi
```

**CI**（新增一步；全仓模式会自动跳过 `api_diff`，避免逐文件 `git show`）：

```yaml
- name: agent-guardrails（改动集）
  shell: bash
  run: bash scripts/guardrails/check_changed.sh --all
```

## 8. 合并后自检（三条命令都要真实跑）

```
py -3 scripts/verify_delivery.py --scope auto
pwsh -File scripts/guardrails/check_changed.ps1
ruff check --config scripts/guardrails/ruff-structure.toml tests/fixtures/_sample.py
```

期望：前两条退出码 0（改动集无 .py 时第二条会打印 `[SKIP]` 并退出 0）；第三条输出 2 条错误（样板本来就违规）。
