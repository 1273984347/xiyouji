#!/usr/bin/env python3
"""批量关闭 / 恢复 GitHub Code scanning 的 Scorecard 整体评级告警（W1205 子任务 A）。

目标：GitHub「Security and quality」面板 · Code scanning 面板剩余 3 条**整体评级项**告警
（CodeReviewID / FuzzingID / CIIBestPracticesID）。这三条**无文件关联**（SARIF 里
location = "no file associated with this alert"），是 OpenSSF Scorecard 的检查项评级，
不是"某文件的具体缺陷"。上批 41 条 pillow 告警的关闭理由是 "inaccurate"（断言不成立），
**本批不适用**——这 3 条断言在仓内**成立**（逐条源码级确证见下），故按用户授权口径
「不能修则按 tolerable_risk 关闭」处置。

═══════════════════════════════════════════════════════════════════════════
依据链（全部为实测·源码级·非推断）
═══════════════════════════════════════════════════════════════════════════

【0】告警来源与指纹（决定「关闭能否粘住」）
  · 产生者：.github/workflows/scorecard.yml（ossf/scorecard-action v2.4.4，锁
    github.com/ossf/scorecard/v5 v5.5.0）→ results.sarif → codeql-action/upload-sarif
    → Code scanning。
  · 指纹：pkg/scorecard/sarif.go 的 createSARIFCheckResult **不填 partialFingerprints**
    （源码注释：Unclear what to use for PartialFingerprints）⇒ GitHub 端按
    「rule id + location」生成默认指纹。本仓 3 条告警 location 恒为
    "no file associated with this alert" + startLine 1 ⇒ 指纹稳定。
  · 实测佐证：#62/#65/#66 自 2026-10-07 起历经多次重跑仍是**同一编号**，而
    most_recent_instance.commit_sha 已推进到最新 run 的 d44c1f4 ⇒ 指纹不随
    消息文本（"Found 0/25 approved changesets" 之类）变化 ⇒ dismiss 后重跑应保持关闭。
    （重跑实测结果见 scripts/output/_w1205_scorecard_alerts.json）

【1】CodeReviewID（severity=high·"Code-Review"）——断言成立·仓内不可修
  判定链：checks/evaluation/code_review.go CodeReview()
          → probes/codeApproved/impl.go approvedRun() / approved()
          → checks/raw/code_review.go CodeReview() / getGithubReviews()
          → clients/githubrepo/graphql.go getCommits()（默认 commit 深度窗口）
  · approved() 的通过条件（v5.5.0 与 main 仅有 nil/空值防御差异，判定语义相同）：
      review.State == "APPROVED" && review.Author.Login != c.Author.Login
    ⇒ **评审人必须 ≠ 提交者本人**；自己 merge 自己的 PR 不算审批
    （getGithubReviews 会把 MergedBy 补成一条 APPROVED，但 MergedBy==Author 时被上述条件否掉）。
  · 仓内事实（GraphQL 实测）：92 个已合并 PR 的 author 与 mergedBy **全部**为唯一
    owner 1273984347，且无任何 APPROVED review ⇒ 结构性 0/N approved。
  · SARIF 实测原文："Found 0/25 approved changesets -- score normalized to 0"。
  · 结论：单人仓无法在仓内达到满分（需第二账号评审 / 引入外部评审平台）；
    CODEOWNERS 文件是否存在**不参与**该判定（该探针只读 commits + PR reviews）。

【2】FuzzingID（severity=medium·"Fuzzing"）——断言成立·风险已被仓内真 fuzz 缓解
  判定链：checks/evaluation/fuzzing.go Fuzzing()
          → probes/fuzzed/impl.go Run()
          → checks/raw/fuzzing.go Fuzzing() / checkCFLite() / checkOSSFuzz()
                                       / checkFuzzFunc() / getProminentLanguages()
          → clients/githubrepo/languages.go languagesHandler.setup()
             （取 GitHub /languages 的**字节数**当作 NumLines）
  · 探针只认三种形态：① .clusterfuzzlite/Dockerfile；② OSS-Fuzz 项目注册；
    ③ **显著语言**的 languageFuzzSpecs（Go/Python/Java/JS/TS… 的内置 fuzzer 规格）。
  · JS/TS 的内置规格**只认 fast-check 的 import**（property-based testing），
    **不认 Jazzer.js**；且只在「显著语言」上做扫描。
  · 仓内事实：xiyouji-agent-web/fuzz/fastcheck.test.ts 已 import fast-check（形态正确），
    但 getProminentLanguages 的门槛 = (总字节/语种数)/4 = 90185399/11/4 = 2049668，
    而 TypeScript 字节仅 605934 ⇒ **TS 非显著 ⇒ 探针根本没扫 TS**。
    显著语言只有 HTML（无 languageFuzzSpecs 条目）与 Python（规格为 import atheris，
    仓内无）⇒ 零 fuzzer ⇒ SARIF 原文 "no fuzzer integrations found"。
  · 风险视角：仓内**确有**真 fuzz（Jazzer.js fuzz/fuzz.ts + fast-check 属性测试 +
    .github/workflows/fuzz.yml 每次 push/PR 常跑）⇒ 真实风险已由仓内 fuzz 覆盖。
  · 根因修法（**需控制器处理**，不在本子任务文件所有权内）：在 .gitattributes 把
    site/** 标记为 linguist-generated/vendored，使其不计入 GitHub 语言统计
    （实测 GitHub /languages 已排除 docs/**：HTML 79,750,689 = 全部 .html 字节
    79,889,413 − docs 的 138,724，差值精确吻合）⇒ 总字节降至约 1163 万 ⇒ 门槛
    约 26.4 万 ⇒ TypeScript 变显著 ⇒ 仓内**现有** fast-check 标记即被探针识别。

【3】CIIBestPractracticesID（severity=low·"CII-Best-Practices"）——断言成立·不可仓内修
  判定链：checks/evaluation/cii_best_practices.go CIIBestPractices()
          → probes/hasOpenSSFBadge/impl.go Run()
          → checks/raw/cii_best_practices.go CIIBestPractices()
          → clients/cii_http_client.go GetBadgeLevel()
             （GET https://www.bestpractices.dev/projects.json?url=<repo URI>）
  · 实测：https://www.bestpractices.dev/projects.json?url=https://github.com/1273984347/xiyouji
    → HTTP 200 且响应体为 [] ⇒ len(parsedResponse)<1 ⇒ BadgeLevel=NotFound ⇒
    探针走 default 分支 ⇒ OutcomeFalse ⇒ "no effort to earn an OpenSSF best practices
    badge detected" ⇒ 0 分（该检查项 enforced 阈值 5）⇒ SARIF 出 result ⇒ 告警。
  · 徽章来自 CII Best Practices **外部登记与评审流程**，仓内无任何可达路径；
    本子任务亦不申请认证、不伪造徽章。

【4】关闭理由枚举（实测·与用户授权口径的映射）
  · Code scanning 的 dismissed_reason 枚举**只有**
    ["false positive", "won't fix", "used in tests", "mitigated"]
    （实测 HTTP 422 回显该枚举）——用户授权口径 tolerable_risk 是 **Dependabot** 的枚举，
    在 Code scanning 侧不可用。
  · 故逐条映射到语义最近值，并在 dismissed_comment 中写明真实依据：
      CodeReviewID      → "won't fix"  （断言成立·需第二账号评审·仓内不可修）
      FuzzingID         → "mitigated" （真实 fuzz 风险已由仓内 Jazzer.js+fast-check 缓解）
      CIIBestPracticesID→ "won't fix"  （断言成立·须走 CII 外部认证·仓内不可修）
    三条均**不是** "false positive"（断言成立），也不是 "used in tests"。

【5】用法
    py -3 scripts/dismiss_scorecard_alerts.py --dry-run        # 只打印将处理的告警
    py -3 scripts/dismiss_scorecard_alerts.py --apply          # 关闭（state=dismissed）
    py -3 scripts/dismiss_scorecard_alerts.py --revert         # 回滚：恢复为 open
    py -3 scripts/dismiss_scorecard_alerts.py --emit-json      # 输出当前告警态 JSON（证据用）

【6】注意
  · 需 gh CLI 且已认证（gh auth status）；凭据只由 gh 自身保管，本脚本不读环境变量里的
    令牌、不打印任何令牌/连接串。
  · 幂等：--apply 跳过已处于目标状态的告警；--revert 只回滚 dismissed_comment 以
    "W1205" 开头的告警（本脚本留下的），不动别人关闭的告警。
  · 每条 PATCH 间隔 0.4 秒，避免触发 API 限流。
  · 注意 API 语义：已 dismissed 的告警再 PATCH state=dismissed 会 400
    "Alert is already dismissed."；改 dismissed_comment 必须同时带 state
    （实测只传 dismissed_comment 会 422）。回滚用 state=open（会同时清空 reason/comment）。
"""
from __future__ import annotations

import json
import subprocess
import sys
import time

REPO = "1273984347/xiyouji"

# 目标 rule id（Scorecard 整体评级项 · 无文件关联）
TARGET_RULES = ("CodeReviewID", "FuzzingID", "CIIBestPracticesID")

# dismissed_comment 前缀标记：--revert 只回滚带此标记的告警（不回滚他人关闭的）
MARKER = "W1205"

# 逐条关闭理由与依据摘要（详见头注释的【1】【2】【3】）
DISMISS_PLAN = {
    "CodeReviewID": {
        "reason": "won't fix",
        "comment": (
            "W1205 实测：Scorecard probes/codeApproved/impl.go approved() 只认"
            "「APPROVED 且评审人≠提交者」；本仓 92 个 PR 全由唯一 owner 自写自合"
            "（author=mergedBy=1273984347）⇒ 结构性 0/N approved ⇒ 断言成立，"
            "仓内不可修（需第二账号评审）。"
        ),
    },
    "FuzzingID": {
        "reason": "mitigated",
        "comment": (
            "W1205 实测：仓内已有真 fuzz（fuzz/fuzz.ts Jazzer.js + fuzz/fastcheck.test.ts "
            "fast-check + .github/workflows/fuzz.yml 常跑）；Scorecard "
            "checks/raw/fuzzing.go 只认 clusterfuzzlite/OSS-Fuzz/显著语言规格，"
            "而 TS 字节 605934 < 门槛 2049668 ⇒ 未被扫描 ⇒ 风险已由仓内 fuzz 缓解。"
        ),
    },
    "CIIBestPracticesID": {
        "reason": "won't fix",
        "comment": (
            "W1205 实测：checks/raw/cii_best_practices.go 取数自 "
            "bestpractices.dev/projects.json?url=<repo>，实测响应 [] ⇒ 无 CII 徽章 ⇒ "
            "断言成立；徽章须走 CII Best Practices 外部认证流程，仓内不可修。"
        ),
    },
}


def gh(*args: str) -> tuple[int, str, str]:
    """调用 gh CLI；返回 (退出码, stdout, stderr)。凭据由 gh 自身管理，不经过本脚本。"""
    proc = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def fetch(state: str) -> list[dict]:
    code, out, err = gh(
        "api", f"repos/{REPO}/code-scanning/alerts?state={state}&per_page=100"
    )
    if code != 0:
        print(f"ERR 获取 code scanning 告警失败：{(err or out).strip()[:200]}")
        return []
    try:
        return json.loads(out or "[]")
    except json.JSONDecodeError:
        print("ERR 解析告警 JSON 失败")
        return []


def rule_of(alert: dict) -> str:
    return ((alert.get("rule") or {}).get("id")) or ""


def is_target(alert: dict) -> bool:
    """是否属于本脚本要处置的 Scorecard 整体评级项。"""
    return rule_of(alert) in TARGET_RULES


def is_ours(alert: dict) -> bool:
    """是否为本脚本关闭的告警（依据 dismissed_comment 的 W1205 标记）。"""
    return (alert.get("dismissed_comment") or "").startswith(MARKER)


def summarize(alert: dict) -> str:
    rule = rule_of(alert)
    severity = ((alert.get("rule") or {}).get("severity")) or "?"
    plan = DISMISS_PLAN.get(rule, {})
    return (
        f"#{alert.get('number')} {rule} severity={severity} state={alert.get('state')} "
        f"reason={plan.get('reason', '-')}"
    )


def main() -> int:
    apply = "--apply" in sys.argv
    revert = "--revert" in sys.argv
    emit_json = "--emit-json" in sys.argv
    dry = "--dry-run" in sys.argv or not (apply or revert)
    if apply and revert:
        print("用法：--apply 与 --revert 互斥")
        return 2

    if revert:
        alerts = [a for a in fetch("dismissed") if is_target(a) and is_ours(a)]
    else:
        alerts = [a for a in fetch("open") if is_target(a)]

    mode = "REVERT" if revert else ("APPLY" if apply else "DRY-RUN")
    print(f"命中 {len(alerts)} 条 · 模式 {mode}")

    if emit_json:
        payload = {
            "repo": REPO,
            "mode": mode,
            "count": len(alerts),
            "alerts": [
                {
                    "number": a.get("number"),
                    "rule": rule_of(a),
                    "severity": (a.get("rule") or {}).get("severity"),
                    "state": a.get("state"),
                    "dismissed_reason": a.get("dismissed_reason"),
                    "dismissed_comment": a.get("dismissed_comment"),
                    "instance_message": (
                        ((a.get("most_recent_instance") or {}).get("message") or {}).get("text")
                    ),
                    "instance_commit_sha": (a.get("most_recent_instance") or {}).get("commit_sha"),
                }
                for a in alerts
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if not apply and not revert:
            return 0

    if dry:
        for alert in alerts:
            print(f"  {summarize(alert)}")
        if not alerts:
            print("  （无命中告警）")
        return 0

    ok = fail = 0
    for alert in alerts:
        number = alert.get("number")
        if revert:
            code, out, err = gh(
                "api",
                "--method",
                "PATCH",
                f"repos/{REPO}/code-scanning/alerts/{number}",
                "-f",
                "state=open",
            )
        else:
            plan = DISMISS_PLAN[rule_of(alert)]
            code, out, err = gh(
                "api",
                "--method",
                "PATCH",
                f"repos/{REPO}/code-scanning/alerts/{number}",
                "-f",
                "state=dismissed",
                "-f",
                f"dismissed_reason={plan['reason']}",
                "-f",
                f"dismissed_comment={plan['comment']}",
            )
        if code == 0:
            ok += 1
        else:
            fail += 1
            print(f"  FAIL #{number}: {(err or out).strip()[:200]}")
        time.sleep(0.4)

    print(f"{'reverted' if revert else 'dismissed'} ok={ok} fail={fail}")
    code, out, _ = gh(
        "api",
        f"repos/{REPO}/code-scanning/alerts?state=open&per_page=100",
        "--jq",
        "length",
    )
    print("open now:", out.strip())
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
