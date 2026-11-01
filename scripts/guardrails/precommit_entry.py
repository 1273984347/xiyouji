"""precommit_entry.py — pre-commit 本地 hook 入口（W1077）。

为什么需要：Windows PATH 上的 `bash` 常是 WSL 中继（C:\\Windows\\system32\\bash.exe），
直接 entry 写 `bash` 会报 `execvpe(/bin/bash) failed`。本入口显式定位可用的 bash：
  1) 环境变量 AGENT_GUARDRAILS_BASH
  2) Windows：Git for Windows 的 bin/bash.exe
  3) PATH 里的 bash（Linux/macOS）
找到后调用 scripts/guardrails/check_changed.sh --strict-api <files>；
找不到则跳过（不阻断），并打印提示。
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / "scripts" / "guardrails" / "check_changed.sh"

WINDOWS_BASH_CANDIDATES = (
    r"C:\Program Files\Git\bin\bash.exe",
    r"C:\Program Files (x86)\Git\bin\bash.exe",
)


def find_bash() -> str | None:
    env = os.environ.get("AGENT_GUARDRAILS_BASH", "").strip()
    if env and Path(env).is_file():
        return env
    if os.name == "nt":
        for cand in WINDOWS_BASH_CANDIDATES:
            if Path(cand).is_file():
                return cand
    for name in ("bash", "sh"):
        found = shutil.which(name)
        if found:
            return found
    return None


def main(argv: list[str]) -> int:
    if not argv:
        return 0
    bash = find_bash()
    if not bash:
        print("[SKIP] 未找到 bash，agent-guardrails 检查跳过（不阻断）。")
        return 0
    return subprocess.call([bash, str(CHECK), "--strict-api", *argv], cwd=str(ROOT))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
