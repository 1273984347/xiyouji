#!/usr/bin/env bash
# agent-guardrails 改动面检查（POSIX / git-bash / Linux CI 版），与 check_changed.ps1 行为对齐：
#   1) ruff（阻塞，宽档阈值）
#   2) 嵌套推导式（阻塞）
#   3) once_call（提示，不阻断）
#   4) api_diff（提示；--strict 时阻断；--strict-api 只把 api_diff 转阻断、阈值保持宽档；--all 时跳过）
# 退出码：0 通过 / 1 有阻断项 / 2 环境缺工具。
#
# 用法：
#   bash scripts/guardrails/check_changed.sh                 # 改动集
#   bash scripts/guardrails/check_changed.sh --strict        # 收紧档（阈值 + api_diff 阻断）
#   bash scripts/guardrails/check_changed.sh --strict-api    # 宽档阈值 + api_diff 阻断（pre-commit 用）
#   bash scripts/guardrails/check_changed.sh --all           # 全仓
#   bash scripts/guardrails/check_changed.sh a.py b.py       # 定向（排障用）

set -u

STRICT=0
API_STRICT=0
ALL=0
TARGETS=()
for arg in "$@"; do
  case "$arg" in
    --strict) STRICT=1; API_STRICT=1 ;;
    --strict-api) API_STRICT=1 ;;
    --all) ALL=1 ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    --*) echo "[FAIL] 未知参数：$arg" >&2; exit 2 ;;
    *) TARGETS+=("$arg") ;;
  esac
done

REPO=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "[FAIL] 不在 git 仓库内" >&2; exit 2; }
cd "$REPO" || exit 2

# 一次性开关（W1077）：pre-commit 框架与手写钩子若在同一次提交里都调用本脚本，
# 第二次看到同一索引树（git write-tree）即跳过，避免重复跑两遍。
STAMP_FILE="$REPO/tmpe/.guardrails_stamp"
TREE=""
if [ "$API_STRICT" -eq 1 ] || [ "${AGENT_GUARDRAILS_STAMP:-0}" = "1" ]; then
  TREE=$(git -C "$REPO" write-tree 2>/dev/null || true)
  if [ -n "$TREE" ] && [ -f "$STAMP_FILE" ] && [ "$(cat "$STAMP_FILE" 2>/dev/null)" = "OK:$TREE" ]; then
    echo "[SKIP] 同一索引已在本次钩子链中检查过（tree $TREE）"
    exit 0
  fi
fi

# Python：py -3 优先（Windows 侧 python 可能是执行存根）；Unix 回落到 python3。
PY=()
if command -v py >/dev/null 2>&1 && py -3 -c "import sys" >/dev/null 2>&1; then
  PY=(py -3)
elif command -v python3 >/dev/null 2>&1 && python3 -c "import sys" >/dev/null 2>&1; then
  PY=(python3)
elif command -v python >/dev/null 2>&1 && python -c "import sys" >/dev/null 2>&1; then
  PY=(python)
else
  echo "[FAIL] 找不到可运行的 Python（py -3 / python3 / python 均不可用）" >&2
  exit 2
fi

RUFF=()
if command -v ruff >/dev/null 2>&1 && ruff --version >/dev/null 2>&1; then
  RUFF=(ruff)
elif "${PY[@]}" -m ruff --version >/dev/null 2>&1; then
  RUFF=("${PY[@]}" -m ruff)
else
  echo "[FAIL] 找不到 ruff（装法：${PY[*]} -m pip install ruff）" >&2
  exit 2
fi

if [ ${#TARGETS[@]} -gt 0 ]; then
  MODE="定向"
  LIST=$(printf '%s\n' "${TARGETS[@]}")
elif [ "$ALL" -eq 1 ]; then
  MODE="全仓"
  LIST=$(git -c core.quotepath=false ls-files -- '*.py' | sort -u)
else
  MODE="改动集"
  LIST=$(
    { git -c core.quotepath=false diff --name-only HEAD 2>/dev/null || true
      git -c core.quotepath=false ls-files --others --exclude-standard
    } | sort -u
  )
fi

# 只留存在且以 .py 结尾的路径；非定向模式下与根 pyproject.toml 一致，豁免 `_` 前缀的一次性脚本，
# 并排除 gitignored 的 tmpe/ 临时脚本区（否则历史脚本会刷一屏 SyntaxWarning）。
PY_FILES=()
while IFS= read -r f; do
  [ -n "$f" ] && [ "$f" != "." ] && [ -f "$f" ] || continue
  case "$f" in *.py) ;; *) continue ;; esac
  if [ ${#TARGETS[@]} -eq 0 ]; then
    case "$(basename "$f")" in _*) continue ;; esac
    case "$f" in tmpe/*) continue ;; esac
  fi
  PY_FILES+=("$f")
done <<< "$LIST"

if [ ${#PY_FILES[@]} -eq 0 ]; then
  echo "[SKIP] 没有可检查的 .py 文件，无阻断项。"
  echo "[SKIP] 非 Python 改动请另跑：${PY[*]} scripts/generate_csp.py --check / ${PY[*]} scripts/verify_delivery.py --scope auto"
  exit 0
fi

echo "== check_changed（$MODE）：${#PY_FILES[@]} 个 .py 文件 =="

RUFF_ARGS=(check --config scripts/guardrails/ruff-structure.toml --output-format concise --no-cache)
if [ "$STRICT" -eq 1 ]; then
  RUFF_ARGS+=(--config lint.mccabe.max-complexity=12 --config lint.pylint.max-nested-blocks=3)
  RUFF_ARGS+=(--config lint.pylint.max-branches=12 --config lint.pylint.max-statements=60)
fi

RC=0
CHUNK=100
N=${#PY_FILES[@]}
for ((i = 0; i < N; i += CHUNK)); do
  SLICE=("${PY_FILES[@]:i:CHUNK}")
  # 1) 项目风格/语法档（显式根配置：避免子目录内同名配置被 ruff 自动发现）
  "${RUFF[@]}" check --config pyproject.toml --output-format concise --no-cache "${SLICE[@]}" || RC=1
  # 2) 结构档（scripts/guardrails/ruff-structure.toml；文件名避开 ruff 自动发现）
  "${RUFF[@]}" "${RUFF_ARGS[@]}" "${SLICE[@]}" || RC=1
  # 3) 嵌套推导式
  "${PY[@]}" scripts/guardrails/check_nested_comprehension.py "${SLICE[@]}" || RC=1
  # 3.5) 改写完整性（阻塞·W1159 E-199 机器判据）
  "${PY[@]}" scripts/guardrails/check_rewrite_integrity.py "${SLICE[@]}" || RC=1
  # 4) 一次性函数（提示）
  "${PY[@]}" scripts/guardrails/once_call.py "${SLICE[@]}"
  # 5) 公开 API 变化（--strict / --strict-api 阻断；--all 跳过）
  if [ "$ALL" -eq 0 ]; then
    if [ "$API_STRICT" -eq 1 ]; then
      "${PY[@]}" scripts/guardrails/api_diff.py --strict "${SLICE[@]}" || RC=1
    else
      "${PY[@]}" scripts/guardrails/api_diff.py "${SLICE[@]}"
    fi
  fi
done

echo "[$([ "$RC" -eq 0 ] && echo OK || echo FAIL)] 汇总（ruff 风格档 / ruff 结构档 / 嵌套推导式$([ "$API_STRICT" -eq 1 ] && echo ' / api_diff')）"
echo "[INFO] once_call 只报告不阻断，判据见 self-check.md 第 1 条"

if [ "$RC" -ne 0 ]; then
  echo "== 结论：有阻断项，请修到 0 再提交 =="
  exit 1
fi
echo "== 结论：通过（提示类输出不阻断）=="
if [ -n "${TREE:-}" ]; then
  mkdir -p "$(dirname "$STAMP_FILE")"
  printf 'OK:%s' "$TREE" > "$STAMP_FILE"
fi
exit 0
