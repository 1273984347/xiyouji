# 自检清单（5 条 · 只问可核对的事实）

> 用法：每个批次收尾前逐条作答；每条必须附命令输出或行号，只写结论视为未作答。
> 命令一律在本仓库根目录执行；`pwsh` = PowerShell 7，`py -3` = 本机 Python 3.12。

## 1. 本次新增/修改的函数，各被调用几处？

取证：`py -3 scripts/guardrails/once_call.py <改动文件...>`

- 不合格示例："都是合理的封装，放辅助函数更清晰。"（没数调用点）
- 合格示例："新增 2 个：`parse_page` 调用 3 处（rag/a.py:12、rag/b.py:40、rag/c.py:88）；`build_sql` 仅 1 处（同文件），已内联删除。"

## 2. 改动函数里嵌套最深第几层？

取证：`ruff check --config scripts/guardrails/ruff-structure.toml --select PLR1702 <改动文件...>`（不报=未超过阈值 4）。

- 不合格示例："层次不深，读起来还行。"（没给层数）
- 合格示例："`deep_parse` 最深 3 层（阈值 4，未报）；`handle_event` 5 层（被报 `5 > 4`，已拆成两个函数）。"

## 3. diff 里公开 API 的签名/默认值/返回注解/raise 集合，各变了几处？

取证：`py -3 scripts/guardrails/api_diff.py <改动文件...>`（默认 base=HEAD，打 `--strict` 可用于提交前拦截）。

- 不合格示例："只是内部重构，对外没影响。"（未取证）
- 合格示例："0 处（api_diff 输出「变化 0 处，破坏性 无」）；另一文件 2 处：`load()` 新增参数 `encoding`，raise 新增 `ValueError`。"

## 4. 本次新增第三方依赖几个？名字与写在哪份清单？

取证：`git diff <base> -- pyproject.toml scripts/requirements.txt package.json`，只数 `+` 行里的依赖声明。

- 不合格示例："用的都是常用库，应该没问题。"（没点名、没给出处）
- 合格示例："0 个：三份清单 diff 均为空；或在 `scripts/requirements.txt` 新增 `httpx==0.27.0` 1 个。"

## 5. 阻断检查的退出码是多少？失败项分别对应哪条规则？

取证：`pwsh -File scripts/guardrails/check_changed.ps1; echo "EXIT=$LASTEXITCODE"`（真正跑一遍，不引用旧结果）。

- 不合格示例："我本地跑过，应该是绿的。"（没有退出码）
- 合格示例："EXIT=0；once_call 提示 2 条（调用点=1）属提示类，不计入阻断。"
