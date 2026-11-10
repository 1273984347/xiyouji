#!/usr/bin/env python3
"""批量关闭 / 恢复 GitHub Dependabot 的 pillow 告警（W1202·GitHub「Security and quality」面板归零）。

## 依据链（全部为本仓实测·非推断）

1. **41 条告警的断言**：`dependency.package.name` ∈ {Pillow, pillow}、`version_requirement = "= 12.3.0"`、
   `manifest_path = "scripts/requirements.txt"`、`scope = runtime`、`relationship = direct`、
   `updated_at` 停在 2026-10-22 与 2026-10-24（两批 W1191/W1193 的改清单尝试后未重算）。
2. **仓库侧早已修复**：`scripts/requirements.txt` 自 W890（commit 654a289c·2026-10-23）起钉
   `pillow==13.0.0`，而 13.0.0 正是全部 41 条 advisory 的 `first_patched_version` ⇒
   告警断言的「12.3.0 被依赖」在仓库侧**不成立**。
3. **依赖图里的 12.3.0 是历史条目，且无仓内清除路径**（W1198–W1201 四批实测）：
   - SBOM API：pillow 三个 SPDXID（13.0.0×2 / 12.3.0×1），12.3.0 被 main 以 `DEPENDS_ON` 直接引用
   - Graph Update run 日志的 `manifests → resolved` 段：每次解析结果**只有** `pkg:pypi/pillow@13.0.0`
   - 内容变更只**新增**条目（10-22 实证）
   - **删除 manifest 使路径消失亦不清理**（W1199 删除态被 Graph Update 正确解析后残留仍在）
   - Dependency submission API 是**追加**语义（官方文档 "in addition to"）
   ⇒ 结论：依赖图历史条目在仓内**无清除路径**，41 条告警不可能靠重算归零。
4. **因此用人工关闭**：`dismiss_reason=inaccurate`（语义为「该断言不成立」）而非 fix_started /
   tolerable_risk ⇒ **不是掩盖真实未修版本项**（真实未修不存在：仓库已钉 13.0.0，且 CI 的 pip audit
   审计哈希化清单 51 项闭包，漏洞检测不中断）。

## 用法

    py -3 scripts/dismiss_pillow_alerts.py --dry-run   # 只打印将处理的告警
    py -3 scripts/dismiss_pillow_alerts.py --apply     # 关闭（state=dismissed + reason=inaccurate）
    py -3 scripts/dismiss_pillow_alerts.py --revert    # 回滚：把这些告警恢复为 open

## 注意

- 需 `gh` CLI 且已认证（`gh auth status`）；只读仓库元数据 + PATCH 告警状态。
- 每条 PATCH 间隔 0.4 秒，避免触发 API 限流。
- 脚本幂等：已处于目标状态的对象会被跳过。
"""
from __future__ import annotations

import json
import subprocess
import sys
import time

REPO = "1273984347/xiyouji"
TARGET_PKG = "pillow"
TARGET_MANIFEST = "scripts/requirements.txt"
COMMENT = ("W1198-W1202 实测：仓库自 2026-10-23 起已钉 pillow==13.0.0（= 全部 advisory 的 "
           "first_patched_version）·依赖图中的 pillow@12.3.0 为 2026-10-22 前的历史条目"
           "（内容变更只新增·删除路径不清理·submission API 追加语义）⇒ 本告警断言不成立")


def gh(*args: str) -> tuple[int, str, str]:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def fetch(state: str) -> list[dict]:
    code, out, _ = gh("api", f"repos/{REPO}/dependabot/alerts?state={state}&per_page=100")
    if code != 0:
        print("ERR 获取告警失败")
        return []
    return json.loads(out or "[]")


def is_target(alert: dict) -> bool:
    dep = alert.get("dependency") or {}
    pkg = (dep.get("package") or {}).get("name", "").lower()
    return pkg == TARGET_PKG and dep.get("manifest_path") == TARGET_MANIFEST


def main() -> int:
    apply = "--apply" in sys.argv
    revert = "--revert" in sys.argv
    dry = "--dry-run" in sys.argv or not (apply or revert)
    if apply and revert:
        print("用法：--apply 与 --revert 互斥")
        return 2

    if revert:
        alerts = [a for a in fetch("dismissed")
                  if is_target(a) and a.get("dismissed_reason") == "inaccurate"]
    else:
        alerts = [a for a in fetch("open") if is_target(a)]

    print(f"open/dismissed 命中 {len(alerts)} 条 · 模式 {'REVERT' if revert else ('APPLY' if apply else 'DRY-RUN')}")
    if dry:
        for alert in alerts[:5]:
            dep = alert.get("dependency") or {}
            print(f"  #{alert['number']} {dep.get('package', {}).get('name')} "
                  f"{dep.get('version_requirement')}")
        if len(alerts) > 5:
            print(f"  … 其余 {len(alerts) - 5} 条同类")
        return 0

    ok = fail = 0
    for alert in alerts:
        if revert:
            code, out, err = gh("api", "--method", "PATCH",
                                f"repos/{REPO}/dependabot/alerts/{alert['number']}",
                                "-f", "state=open",
                                "-f", "dismissed_reason=")
        else:
            code, out, err = gh("api", "--method", "PATCH",
                                f"repos/{REPO}/dependabot/alerts/{alert['number']}",
                                "-f", "state=dismissed",
                                "-f", "dismissed_reason=inaccurate",
                                "-f", f"dismissed_comment={COMMENT}")
        if code == 0:
            ok += 1
        else:
            fail += 1
            print(f"  FAIL #{alert['number']}: {(err or out).strip()[:120]}")
        time.sleep(0.4)
    print(f"{'reverted' if revert else 'dismissed'} ok={ok} fail={fail}")
    code, out, _ = gh("api", f"repos/{REPO}/dependabot/alerts?state=open&per_page=100", "--jq", "length")
    print("open now:", out.strip())
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
