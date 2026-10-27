# -*- coding: utf-8 -*-
"""_w988_pitfalls2.py — W988 坑表补第 7 条（E-17）+ 计数链 86 → 87 + T34 §8 补 E-17

新增坑位（W988 批第二条与「批量新增 + 级联」相关的坑）：
  E-17 级联 spec 的「本批新增」判定**不能用 git 索引**（已 add 的新文件会被误判为既有），
       且级联的幂等保护（断言「批次号应为 W+1」）使它**不能重跑** ⇒ 只能段内定向订正。

用法：py -3 scripts/_w988_pitfalls2.py [--dry-run]
"""
import io
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIT = os.path.join(REPO, "docs", "agent", "pitfalls.md")
T34 = os.path.join(REPO, "docs", "11-方案报告", "计划方案",
                   "T34-任务计划执行与经验沉淀报告-2026-10-27.md")

NEW_ITEM = (
    "- **级联 spec 的「本批新增」判定不能用 git 索引，且级联不能重跑**（W988 实证·E-17）："
    "批量新增文件（资产/页面）后再生成级联 spec 时，若用 `git ls-files`（**索引**）判定「本批新增」，"
    "已被 `git add -A` 的新文件会被误判为既有 ⇒ 「文件」行与 file-index 段**漏列**（本批实测漏 115 个资产文件）。"
    "⇒ 修法：① 判定用 **HEAD 树**（`git ls-tree -r --name-only HEAD <dir>`）而非索引；"
    "② 注意 `batch_cascade` 有**幂等保护**（重跑时断言「批次号应为 W+1」）⇒ 段已写入后**不能重跑级联**，"
    "只能做**段内定向订正**（限定在该批段范围内替换「文件」行与 file-index 段表格）；"
    "③ 订正脚本本身必须**最后**执行且其后再 `git add`，否则第 31 门禁 C4-f「文件清单有工作树未提交残留」判红（本批实测连续三轮红）。\n"
)

T34_ROW = (
    "| E-17 | **级联 spec 的「本批新增」判定不能用 git 索引，且级联不能重跑** | 适用：批量新增文件后再生成级联 spec / 级联段已写入后的订正。边界：单文件小改不适用 | "
    "① 判定用 **HEAD 树**（`git ls-tree -r HEAD`）而非索引（已 add 的新文件会被误判为既有）�� "
    "② `batch_cascade` 有幂等保护（断言「批次号应为 W+1」）⇒ 段写入后不能重跑，只能**段内定向订正**；"
    "③ 订正脚本最后执行且其后再 `git add`（否则 C4-f 判「工作树未提交残留」） | "
    "本批实测：漏列 115 个资产文件（文件行 144 → 259 项）+ 连续三轮 C4-f 残留红 | "
    "本批偏差 6 · `_w988_make_spec.py` + `_w988_fix_cascade.py` | 高 | 高 |\n"
)


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.replace("\r\n", "\n").replace("\n", nl).encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in os.sys.argv

    # ① 坑表：插到 git 节之前 + 节计数 20 → 21
    t, n = read(PIT)
    assert "E-17" not in t, "E-17 已存在"
    i = t.index("### 级联 / CHANGELOG")
    t = t[:i] + NEW_ITEM + t[i:]
    t = t.replace("### git / 提交 / 并发（20 条）", "### git / 提交 / 并发（21 条）")
    if dry:
        print("DRY  坑表 +1 条（E-17）· git 节 20 → 21")
    else:
        write(PIT, t, n)
        print("OK   坑表 +1 条（E-17）· git 节 20 → 21 · 合计 87")

    # ② 计数链：AGENTS.md 两处 + HANDOVER.md 两处
    for rel, subs in [
        ("AGENTS.md", [
            ("索引型——86 条坑位按六主题迁", "索引型——87 条坑位按六主题迁"),
            ("git/提交/并发（20）", "git/提交/并发（21）"),
            ("现役 80 条·增量沿革见各条目自注与 CHANGELOG·W987 校", "现役 87 条·增量沿革见各条目自注与 CHANGELOG·W988 校"),
        ]),
        ("HANDOVER.md", [
            ("（86 条·六主题）与", "（87 条·六主题）与"),
            ("（86 条·六主题·含 shell 场景查坑表）", "（87 条·六主题·含 shell 场景查坑表）"),
        ]),
    ]:
        p = os.path.join(REPO, rel.replace("/", os.sep))
        t, n = read(p)
        miss = []
        for old, new in subs:
            if old not in t:
                miss.append(old[:40])
                continue
            t = t.replace(old, new)
        if miss:
            print("WARN  %s 未找到：%s" % (rel, miss))
        if dry:
            print("DRY  %s 计数链 86 → 87" % rel)
        else:
            write(p, t, n)
            print("OK   %s 计数链 86 → 87" % rel)

    # ③ T34 §8 补 E-17 行
    p = T34
    t, n = read(p)
    if "E-17" in t:
        print("SKIP  T34 已有 E-17")
    else:
        anchor = "| E-16 |"
        i = t.index(anchor)
        j = t.index("\n", t.index("| 高 | 高 |", i)) + 1
        t = t[:j] + T34_ROW + t[j:]
        if dry:
            print("DRY  T34 §8 补 E-17 行")
        else:
            write(p, t, n)
            print("OK   T34 §8 补 E-17 行")

    # ④ 复核
    t2, _ = read(PIT)
    counts = {}
    for m in re.finditer(r"^### .+?（(\d+) 条）", t2, re.M):
        counts[m.group(0).split("（")[0].replace("### ", "")] = int(m.group(1))
    real = len(re.findall(r"^- \*\*", t2, re.M))
    print("各节计数：%s · 声明合计 %d · 实算条目 %d" % (counts, sum(counts.values()), real))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
