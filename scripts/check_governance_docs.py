#!/usr/bin/env python3
"""check_governance_docs.py — 治理文档维护契约门禁（W477 后 · WARN 起步）

防「追加式乱写」（W419-W424 启动 Prompt / 交接文档膨胀先例，2026-08-18 治理）：
  1. 新Agent启动Prompt.md 五段骨架（【第 1 步】…【第 5 步】顺序）与「维护契约」存在
  2. 启动 Prompt 不含过时口径黑名单（旧 LHCI / 安全快照 / 速记段标题）
  3. 启动 Prompt 关键短语重复上限（generate_csp / 209 / LCP ≤ 2）
  4. 交接文档「当前 HEAD」与 CHANGELOG 最新版本段一致（版本 vX.Y.Z + W###；短 SHA 会逐 commit 变动，不作为校验项）
  5. CHANGELOG 编号规则 W001-W### 与最新版本段 W 一致
  6. 文档规范 §11.5 登记的 10 份治理文档均含「维护契约」
退出码：0 全过；1 任一检查失败。
"""

import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)


def read_rel(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def main():
    issues = []

    prompt = read_rel("新Agent启动Prompt.md")
    handoff = read_rel("交接文档.md")
    changelog = read_rel("CHANGELOG.md")

    # 1. 启动 Prompt 五段骨架 + 维护契约
    steps = [int(m) for m in re.findall(r"【第 (\d) 步", prompt)]
    if steps != [1, 2, 3, 4, 5]:
        issues.append("启动 Prompt 五段骨架异常（期望 1-5 顺序，实际 %s）" % steps)
    if "维护契约" not in prompt:
        issues.append("启动 Prompt 缺少「维护契约」头注")

    # 2. 启动 Prompt 过时口径黑名单
    blacklist = [
        "5000→4500", "CLS 0.3→0.2", "159 页", "680 内联脚本哈希",
        "W420-W424 治理要点", "复盘沉淀速记",
    ]
    for pat in blacklist:
        if pat in prompt:
            issues.append("启动 Prompt 含过时口径「%s」（应删除，只留现役值）" % pat)

    # 3. 启动 Prompt 关键短语重复上限
    for phrase, cap in (("generate_csp", 2), ("209", 2), ("LCP", 2)):
        cnt = prompt.count(phrase)
        if cnt > cap:
            issues.append("启动 Prompt 短语「%s」出现 %d 次（上限 %d，应去重）" % (phrase, cnt, cap))

    # 4. 交接文档 HEAD 与 CHANGELOG 最新版本段一致
    hm = re.search(r"当前 HEAD = (v[\d.]+) W(\d+)", handoff)
    cm = re.search(r"^### (v[\d.]+)（.*?）：W(\d+)", changelog, re.M)
    if not hm or not cm:
        issues.append("无法解析 HEAD 或 CHANGELOG 最新段（hm=%s cm=%s）" % (bool(hm), bool(cm)))
    else:
        hv, hw = hm.group(1), hm.group(2)
        cv, cw = cm.group(1), cm.group(2)
        if (hv, hw) != (cv, cw):
            issues.append("交接文档 HEAD=%s W%s 与 CHANGELOG 最新段 v%s W%s 不一致" % (hv, hw, cv, cw))
    # 5. CHANGELOG 编号规则 W001-W### 与最新版本段一致
    wm = re.search(r"W001-W(\d+)", changelog)
    if wm and cm:
        if wm.group(1) != cm.group(2):
            issues.append("CHANGELOG 编号规则 W001-W%s 与最新段 W%s 不一致" % (wm.group(1), cm.group(2)))

    # 6. §11.5 登记的 10 份治理文档均含维护契约
    gov_docs = [
        "新Agent启动Prompt.md", "交接文档.md", "AGENTS.md", "STRUCTURE.md",
        "CHANGELOG.md", "DESIGN.md", "README.md", "docs/00-导读/项目说明.md",
        "scripts/output/file-index.md", "docs/10-方法论沉淀/README.md",
    ]
    missing = [rel for rel in gov_docs if "维护契约" not in read_rel(rel)]
    if missing:
        issues.append("以下治理文档缺少「维护契约」：%s" % "、".join(missing))

    if issues:
        for it in issues:
            print("FAIL  " + it)
        print("治理文档维护契约检查失败：%d 项" % len(issues))
        return 1
    print("治理文档维护契约通过（骨架/黑名单/重复/HEAD/编号/契约覆盖 6 项全过）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
