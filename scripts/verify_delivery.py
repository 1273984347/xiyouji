#!/usr/bin/env python3
"""
verify_delivery.py — 零依赖交付校验门禁（Senior Developer 设立）

解决两类工程顽疾：
  1) 「旧疾」：单文件连续多次 Edit 时描述段丢失 → 校验文档均含最新版本号 + W### 里程碑 token。
  2) 「范围漂移」：已评审/已记录 scope 之外又发生了改动（如 html 里出现 W334 标记但文档只记到 W333）
     → 校验 site/dukou-engine.html 中引用的所有 W### 是否都已在文档中记录。

降级六文档同步（W393）：
  - 核心 2 份（CHANGELOG.md / 交接文档.md）= 跨 session 连续性真载体，缺失 v/W 仍【阻断】。
  - 辅助 4 份（README.md / STRUCTURE.md / 项目说明.md / file-index.md）= 每次 W### 的纯手工税，
    缺失仅【WARN 不阻断】，里程碑时跑 scripts/bump_version.py 一键补齐。

零依赖：仅标准库。可直接运行：
  python scripts/verify_delivery.py            # 静态校验（提交前门禁）
  python scripts/verify_delivery.py --health   # 额外探测 RAG /health（环境项，仅告警不阻断）

退出码：核心 FAIL 1；仅辅助 WARN 0。可直接挂到 .git/hooks/pre-commit（辅助 WARN 不再阻断提交）。
"""

import json
import os
import re
import sys
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, ".."))  # scripts/.. = 项目根 xiyouji

# 降级六文档同步（W393）：核心 2 份硬门禁，辅助 4 份仅 WARN 不阻断
# W413 修正（2026-08-09）：严格审查后交接文档恢复入库（无敏感内容），恢复为核心硬门禁
CORE_DOCS = [
    "CHANGELOG.md",
    "交接文档.md",
]
AUX_DOCS = [
    "README.md",
    "STRUCTURE.md",
    os.path.join("docs", "00-导读", "项目说明.md"),
    os.path.join("scripts", "output", "file-index.md"),
]
DOCS = CORE_DOCS + AUX_DOCS
HTML = os.path.join(ROOT, "site", "dukou-engine.html")

# 四份含 A4 计数语义的文档（W413 修正：交接文档恢复入库，恢复 4 份检查）
A4_DOCS = ["README.md", "STRUCTURE.md",
           os.path.join("docs", "00-导读", "项目说明.md"), "交接文档.md"]
EXPECT_A4 = "201 篇"  # W342 gap-fill（权力五联对照 W084 + 妖怪身份政治）后：199→201


def _read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def main():
    fails = 0
    warns = 0

    def fail(msg):
        nonlocal fails
        fails += 1
        print("FAIL  " + msg)

    def warn(msg):
        nonlocal warns
        warns += 1
        print("WARN  " + msg)

    def ok(msg):
        print("OK    " + msg)

    # ---- 读取 html，提取 footer 版本 + 扫描所有 W### ----
    html = _read(HTML)
    if not html:
        fail("找不到 %s（未生成或被忽略）" % HTML)
    m = re.search(r"v(\d+\.\d+\.\d+)\s+W(\d+)", html)
    ver = m.group(1) if m else None
    wnum = m.group(2) if m else None
    html_w = [int(x) for x in re.findall(r"W(\d{3})", html)]
    max_w_html = max(html_w) if html_w else 0

    if ver and wnum:
        ok("dukou-engine.html footer 版本 v%s W%s" % (ver, wnum))
    else:
        fail("dukou-engine.html footer 未解析出 vX.Y.Z W###")

    # ---- 降级六文档同步校验（W393）----
    # 核心 2 份（CHANGELOG/交接文档）缺失 v/W → 阻断；
    # 辅助 4 份（README/STRUCTURE/项目说明/file-index）缺失 → WARN 不阻断。
    doc_all = ""
    for d in DOCS:
        p = os.path.join(ROOT, d)
        c = _read(p)
        doc_all += c
        core = d in CORE_DOCS
        if not c:
            if core:
                fail("缺失核心文档: %s" % d)
            else:
                warn("缺失辅助文档（不阻断，可跑 scripts/bump_version.py）: %s" % d)
            continue
        if ver and ("v" + ver) not in c:
            if core:
                fail("%s 不含版本 v%s（旧疾风险·核心阻断）" % (d, ver))
            else:
                warn("%s 不含版本 v%s（辅助文档，跑 scripts/bump_version.py 同步，不阻断）" % (d, ver))
            continue
        if wnum and ("W" + wnum) not in c:
            if core:
                fail("%s 不含 W%s 里程碑 token（旧疾风险·核心阻断）" % (d, wnum))
            else:
                warn("%s 不含 W%s 里程碑 token（辅助文档，跑 scripts/bump_version.py 同步，不阻断）" % (d, wnum))
            continue
        ok("%s 含 v%s / W%s" % (d, ver, wnum))

    # ---- 范围漂移检测 ----
    doc_w = [int(x) for x in re.findall(r"W(\d{3})", doc_all)]
    max_w_doc = max(doc_w) if doc_w else 0
    if max_w_html > max_w_doc:
        fail("范围漂移：%s 引用到 W%d，但六文档最高仅记到 W%d（疑似未记录的改动，需补记或回退）"
             % (os.path.basename(HTML), max_w_html, max_w_doc))
    else:
        ok("无范围漂移（html 最高 W%d ≤ 文档最高 W%d）" % (max_w_html, max_w_doc))

    # ---- A4 计数一致性 ----
    miss = []
    for d in A4_DOCS:
        c = _read(os.path.join(ROOT, d))
        if EXPECT_A4 not in c:
            miss.append(d)
    if miss:
        fail("A4 计数不一致（缺 '%s'）：%s" % (EXPECT_A4, ", ".join(miss)))
    else:
        ok("A4 计数一致（四份文档均含 '%s'）" % EXPECT_A4)

    # ---- 可选：RAG /health 探活（仅告警，不阻断）----
    if "--health" in sys.argv:
        try:
            r = urllib.request.urlopen("http://127.0.0.1:8777/health", timeout=5)
            body = json.loads(r.read().decode("utf-8"))
            ok("/health 存活：%s" % body)
        except Exception as e:
            print("WARN  /health 不可达（环境项，不阻断提交）：%s" % e)

    print("\n==== 交付校验汇总 ====")
    if fails == 0:
        print("核心全部通过 ✅" + ("（%d 项辅助 WARN，不阻断）" % warns if warns else ""))
        return 0
    print("%d 项核心 FAIL ❌（%d 项辅助 WARN）" % (fails, warns))
    return 1


if __name__ == "__main__":
    sys.exit(main())
