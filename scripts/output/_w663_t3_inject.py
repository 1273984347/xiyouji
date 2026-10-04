#!/usr/bin/env python3
"""W663/T3 一次性注入器：给 verify_delivery.py 的 36 个阻断门禁段插入 section() 上报 + 收尾自洽断言。

幂等守卫：检测到已有 section( 注入即 abort。插入位置 = 每个段标记行（    # ---- 开头）之前；
可选段（RAG 探活）不插不计入。插入后由调用方跑 ruff + verify + 负样本实测。
"""
import io
import sys

TARGET = "scripts/verify_delivery.py"

NAMES = [
    "期望版本", "dukou页脚", "六文档同步", "旁文档同步", "范围漂移", "A4计数", "A1-A6计数",
    "学术引用", "A1导航", "docs01链接", "sitemap覆盖", "内嵌回退", "双源漂移", "CSP漂移",
    "腐蚀插件", "内联语法", "CSS平衡", "token覆盖", "动效禁令", "a11y对比", "INLINED完整",
    "动态链接", "治理契约", "索引健康", "元信息块", "术语一致", "引文核验", "图表自洽",
    "数据一致", "W区间字面量", "SEOhead", "可引用性", "设计令牌对账", "色盲安全", "降级声明", "文档口径",
]

DECL = (
    "# 门禁段自洽锁声明（VERIFY_SECTIONS·W663/T3）：下方名单 == main() 内阻断门禁段标记，\n"
    "# 每段段首 section(name) 上报、收尾断言缺段即红——防「段被删/注释后其余全绿」的假象。\n"
    "EXPECTED_SECTION_NAMES = [\n"
    + "".join('    "%s",\n' % n for n in NAMES)
    + "]\n"
)

src = io.open(TARGET, encoding="utf-8", newline="").read()
if "sections_ran" in src:
    sys.exit("ABORT: 已存在注入（sections_ran），非幂等场景")

lines = src.split("\n")
out = []
ni = 0
inserted = 0
for ln in lines:
    if ln.startswith("    # ---- "):
        if "可选" in ln:
            out.append(ln)
            continue
        if ni >= len(NAMES):
            sys.exit("ABORT: 段标记多于名单（%d 处仍有剩余）" % (ni,))
        out.append('    section("%s")' % NAMES[ni])
        ni += 1
        inserted += 1
    out.append(ln)
if ni != len(NAMES):
    sys.exit("ABORT: 段标记 %d < 名单 %d" % (ni, len(NAMES)))

text = "\n".join(out)

# 1) EXPECTED_SECTION_NAMES 模块级声明：插在 CORE_DOCS 定义之前
anchor = "CORE_DOCS = ["
assert text.count(anchor) == 1
text = text.replace(anchor, DECL + "\n" + anchor, 1)

# 2) section() 闭包：插在 ok() 定义之后（fail/warn 同款形态）
ok_def = '    def ok(msg):\n        print("OK    " + msg)\n'
assert text.count(ok_def) == 1
text = text.replace(
    ok_def,
    ok_def
    + "\n"
    + '    sections_ran = []\n\n    def section(name):\n        sections_ran.append(name)\n',
    1,
)

# 3) 收尾缺段断言：插在汇总打印之前
summary = '    print("\\n==== 交付校验汇总 ====")'
assert text.count(summary) == 1
closing = (
    "    # ---- 门禁段自洽锁（VERIFY_SECTIONS·W663/T3：声明段集合 == 实跑段集合，缺段即红）----\n"
    "    missing_sections = [n for n in EXPECTED_SECTION_NAMES if n not in sections_ran]\n"
    "    if missing_sections:\n"
    '        fail("门禁段实跑 %d ≠ 声明 %d：缺 %s（VERIFY_SECTIONS 自洽锁）"\n'
    "             % (len(set(sections_ran)), len(EXPECTED_SECTION_NAMES), \"、\".join(missing_sections)))\n"
    "    else:\n"
    '        ok("门禁段自洽锁：实跑 %d 段 == 声明 %d 段" % (len(EXPECTED_SECTION_NAMES), len(EXPECTED_SECTION_NAMES)))\n'
    "\n"
)
text = text.replace(summary, closing + summary, 1)

io.open(TARGET, "w", encoding="utf-8", newline="").write(text)
print("OK: 注入 section() %d 处 + 声明名单 %d 项 + 收尾断言" % (inserted, len(NAMES)))
