#!/usr/bin/env python3
"""check_w_range_literal.py — W 号区间字面量门禁（W628 挂载·第 27 门禁）。

背景（W628 审计根因）：外部综述照抄 README 过期字面量「W001-W575」——此类
「CHANGELOG 覆盖上限」声明散落在级联与门禁覆盖面之外的叙述行里，写死后必然漂移。

规则：
  R1 现役叙述面文件中，「W001-Wxxx」形式的覆盖上限字面量，终点必须等于
     CHANGELOG 现役 max W。豁免：含「对应」（编号映射规则）或「tier2」（归档
     三段式描述）的行。非 001 起始的区间（如 W454-W457 报告覆盖范围）属历史
     叙述，不在本门禁范围。
  R2 CITATION.cff 的 version 必须与 CHANGELOG 现役版本一致（外部引用面）。

现役叙述面 = README / STRUCTURE / CONTRIBUTING / 新Agent启动Prompt /
docs/00-导读（非归档）/ docs/10-方法论沉淀/README / .github/workflows/README /
xiyouji-agent-web/README。CHANGELOG/file-index/交接文档/AGENTS/归档/S*/site 为
历史段或级联自维护面，豁免。

用法：python scripts/check_w_range_literal.py [--self-test]
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
CFF = os.path.join(ROOT, "CITATION.cff")

FILES = [
    "README.md", "STRUCTURE.md", "CONTRIBUTING.md", "新Agent启动Prompt.md",
    "docs/00-导读/文档规范.md", "docs/00-导读/项目说明.md", "docs/00-导读/统计口径说明.md",
    "docs/10-方法论沉淀/README.md", ".github/workflows/README.md", "xiyouji-agent-web/README.md",
]
ALLOW_SUBSTR = ("对应", "tier2")  # 编号映射规则 / 归档三段式描述
RANGE_RE = re.compile(r"W001\s*[-–~]\s*W(\d+)")


def current_state():
    s = open(CHANGELOG, encoding="utf-8").read()
    m = re.search(r"^### (v[\d.]+)（[^）]*）：W(\d+)", s, re.M)
    if not m:
        raise SystemExit("FAIL 未能在 CHANGELOG 定位现役版段")
    return m.group(1), int(m.group(2))


def check(cur_v, max_w):
    fails = []
    scanned = 0
    for rel in FILES:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            fails.append(f"{rel}: 文件缺失（叙述面清单与仓库失配）")
            continue
        scanned += 1
        for i, ln in enumerate(open(p, encoding="utf-8").read().split("\n"), 1):
            for m in RANGE_RE.finditer(ln):
                if int(m.group(1)) != max_w and not any(a in ln for a in ALLOW_SUBSTR):
                    fails.append(f"{rel}:{i} 「{m.group(0)}」终点 {m.group(1)} != W{max_w}（覆盖上限声明须随现役更新或改引用式）")
    cff = open(CFF, encoding="utf-8").read()
    mv = re.search(r'^version:\s*"?([\d.]+)"?', cff, re.M)
    if not mv or mv.group(1) != cur_v.lstrip("v"):
        fails.append(f"CITATION.cff version={mv.group(1) if mv else '缺失'} != 现役 {cur_v.lstrip('v')}（外部引用面）")
    return fails, scanned


def self_test():
    ok = []
    drift = '├── CHANGELOG.md           # 更新日志（W001-W575）'
    ok.append(("过期覆盖上限被拦截", RANGE_RE.search(drift) and int(RANGE_RE.search(drift).group(1)) != 999_999))
    mapping = '**W### 编号规则**：W001-W099 对应 v0.1-v2.0.72；W100+ 对应 v2.1.0+'
    ok.append(("「对应」映射行豁免", any(a in mapping for a in ALLOW_SUBSTR)))
    tier2 = '（CHANGELOG-ARCHIVE-tier2.md：W001-W399；现役 W485+）'
    ok.append(("tier2 归档描述豁免", any(a in tier2 for a in ALLOW_SUBSTR)))
    hist = 'W454-W457 白屏根因复盘'
    ok.append(("非 001 起始历史区间不在范围", not RANGE_RE.search(hist)))
    bad = 0
    for name, passed in ok:
        print(("OK   " if passed else "FAIL ") + name)
        bad += 0 if passed else 1
    print(f"自测 {len(ok) - bad}/{len(ok)} 通过")
    return bad


def main():
    if "--self-test" in sys.argv:
        return 1 if self_test() else 0
    cur_v, max_w = current_state()
    fails, scanned = check(cur_v, max_w)
    if fails:
        print("\n".join("FAIL " + f for f in fails))
        print(f"W 号区间字面量门禁：{len(fails)} 处漂移（现役 {cur_v} W{max_w}·扫描 {scanned} 文件）")
        return 1
    print(f"W 号区间字面量门禁通过（现役 {cur_v} W{max_w}·扫描 {scanned} 文件·覆盖上限字面量 0 漂移·CITATION 同步）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
