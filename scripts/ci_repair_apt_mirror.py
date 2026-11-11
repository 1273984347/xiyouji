#!/usr/bin/env python3
"""ci_repair_apt_mirror.py — CI runner apt 源回退修复（W1211）

背景（2026-11-11 实证）：GitHub Actions 的 ubuntu runner 把 /etc/apt/apt-mirrors.txt
指向 azure.archive.ubuntu.com。该域名当日连续 90+ 分钟 DNS 解析失败
（Temporary failure resolving 'azure.archive.ubuntu.com'）⇒ npx playwright install
--with-deps 的系统依赖装不上 ⇒ Site Smoke / E2E / Delivery Gate / Agent Web Build
四个 job 同款红（Failed to install browsers / Installation process exited with code: 100）。
GitHub 状态页当时全 operational ⇒ 属 runner 侧网络故障，非仓库内容问题。

本脚本：把 apt 源切到候选镜像并用 apt-get update 实测验证，第一个通过的即采用；
全部候选失败时打 ::warning:: 并以 0 退出——不掩盖后续步骤的真实失败语义。

用法：python scripts/ci_repair_apt_mirror.py
性质：幂等（可重复执行）·只改 runner 临时文件·不碰任何仓库文件·非 Ubuntu 环境直接跳过。
"""

from __future__ import annotations

import os
import subprocess
import sys

MIRRORS = "/etc/apt/apt-mirrors.txt"
AZURE_HOST = "azure.archive.ubuntu.com"
# 候选顺序：官方源优先，国内镜像兜底（runner 在 Azure 区域，两类源都试）
CANDIDATES = ("archive.ubuntu.com", "mirrors.aliyun.com", "mirrors.tuna.tsinghua.edu.cn")
APT_TIMEOUT = "15"
APT_RETRIES = "1"


def rewrite(content: str, host: str) -> str:
    """把 azure 镜像域名整体换成候选 host（其余内容逐字保留）。"""
    return content.replace(AZURE_HOST, host)


def write_mirrors(content: str) -> bool:
    """用 sudo tee 覆盖镜像清单；成功返回 True。"""
    try:
        proc = subprocess.run(
            ["sudo", "tee", MIRRORS],
            input=content,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
    except OSError as exc:
        print(f"::notice::cannot write {MIRRORS}: {exc}")
        return False
    return proc.returncode == 0


def apt_update_ok() -> bool:
    """实测候选源是否可用（apt-get update 成功即视为可用）。"""
    try:
        proc = subprocess.run(
            [
                "sudo",
                "apt-get",
                "update",
                "-qq",
                "-o",
                f"Acquire::http::Timeout={APT_TIMEOUT}",
                "-o",
                f"Acquire::Retries={APT_RETRIES}",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        print(f"::notice::apt-get update unavailable: {exc}")
        return False
    return proc.returncode == 0


def main() -> int:
    if not os.path.isfile(MIRRORS):
        print(f"::notice::no {MIRRORS} (non-Ubuntu image?) - skip")
        return 0
    try:
        with open(MIRRORS, encoding="utf-8", errors="replace") as fh:
            original = fh.read()
    except OSError as exc:
        print(f"::notice::cannot read {MIRRORS}: {exc} - skip")
        return 0
    if AZURE_HOST not in original:
        # 已是别的源（或已被他人修过）⇒ 不动，避免覆盖他人处置
        print(f"::notice::{MIRRORS} has no {AZURE_HOST} - skip")
        return 0
    for host in CANDIDATES:
        if not write_mirrors(rewrite(original, host)):
            print(f"::notice::write failed for {host} - trying next")
            continue
        if apt_update_ok():
            print(f"apt mirror repaired -> {host}")
            return 0
        print(f"apt-get update failed with {host} - trying next")
    print("::warning::all apt mirror candidates failed (Azure DNS still down)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
