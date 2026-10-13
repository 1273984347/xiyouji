#!/usr/bin/env python3
"""W628 取证：全仓「现役叙述面」内容漂移审计（只读）。

范围：根级文档 + docs/00-导读 + 方法论 README + workflows README + agent-web README
豁免（历史段/级联自维护/归档/数据）：CHANGELOG.md、scripts/output/file-index.md、
docs/archive/**、AGENTS.md（脚注随级联）、交接文档.md（头链随级联·历史段禁改）、
docs/S2/S3/S4/superpowers（冻结面）、site/**（生成物）、*.json。

类别：
  R1 W 号区间字面量（W520 禁令）：W001-Wxxx / Wxxx-Wyyy，终点 != 现役 max
  R2 时效版本断言：当前版本/当前 HEAD/最新 等语境里的 vX.Y.Z / Wxxx
  R3 门禁数量声明：N 项门禁 / 门禁 N 条（与 AGENTS §4.2 编号口径比对）
  R4 CITATION.cff version 字段
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"D:\xiyouji"
CUR_W = 627
CUR_V = "v2.3.227"

FILES = [
    "README.md", "STRUCTURE.md", "CONTRIBUTING.md", "CITATION.cff",
    "新Agent启动Prompt.md", "docs/00-导读/文档规范.md", "docs/00-导读/项目说明.md",
    "docs/00-导读/统计口径说明.md", "docs/10-方法论沉淀/README.md",
    ".github/workflows/README.md", "xiyouji-agent-web/README.md",
]

RANGE_RE = re.compile(r"W(\d+)\s*[-–~]W(\d+)")
VERSION_CTX = re.compile(r"(当前版本|当前 HEAD|最新版本|currentVersion)[^。\n]{0,60}")
VER_LIT = re.compile(r"v2\.3\.\d+")
W_LIT_CTX = re.compile(r"(当前|最新|现役)[^。\n]{0,40}W(\d+)")
GATE_RE = re.compile(r"(\d+)\s*项(?:自动化)?门禁|(?:门禁|检查)\s*凡?\s*(\d+)\s*条")

for rel in FILES:
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        print(f"-- skip(缺失) {rel}")
        continue
    s = open(p, encoding="utf-8").read()
    lines = s.split("\n")
    for i, ln in enumerate(lines, 1):
        for m in RANGE_RE.finditer(ln):
            end = int(m.group(2))
            if end != CUR_W:
                print(f"R1 {rel}:{i}  「{m.group(0)}」 终点 {end} != {CUR_W}  | {ln.strip()[:80]}")
        if VERSION_CTX.search(ln):
            for v in VER_LIT.finditer(ln):
                if v.group(0) != CUR_V:
                    print(f"R2 {rel}:{i}  版本字面量 {v.group(0)} != {CUR_V}（当前语境）| {ln.strip()[:80]}")
        for m in W_LIT_CTX.finditer(ln):
            if int(m.group(2)) not in (CUR_W,):
                print(f"R2 {rel}:{i}  「{m.group(0)[:50]}」 W{m.group(2)} != W{CUR_W} | {ln.strip()[:80]}")
        for m in GATE_RE.finditer(ln):
            n = m.group(1) or m.group(2)
            print(f"R3 {rel}:{i}  门禁数声明 = {n} | {ln.strip()[:80]}")

# R4 CITATION.cff version 字段
cff = open(os.path.join(ROOT, "CITATION.cff"), encoding="utf-8").read()
mv = re.search(r"^version:\s*(\S+)", cff, re.M)
if mv:
    print(f"R4 CITATION.cff version = {mv.group(1)}（现役 {CUR_V}）")

# 实际门禁计数：AGENTS §4.2 编号 1-25（16 退役·26 待裁决未挂）
print("\n-- 口径参考：AGENTS §4.2 列 25 项（#16 退役编号保留 → 活跃 24；#26 check_seo_head 待裁决未挂载）")
