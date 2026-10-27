# -*- coding: utf-8 -*-
"""_w988_record_adoption.py — W988 并行代提事实的登记（CHANGELOG 段状态行 + T34 补记）

事实：W988 主体内容（115 个资产 + 102 个页面 + T34 + 坑表 + 13 个脚本）在本批
`git add -A` 之后，被并行会话的**全量提交** `1fb1b14f chore(w989)` 一并带入入库
⇒ 本批主体不是以「W988」提交信息入库的，而是**被并行 W989 提交代提**。

按「共享面代提须书面留痕」纪律，本脚本在两处如实登记：
  ① CHANGELOG 的 W988 段「状态」行 → 写明主体内容由 `1fb1b14f`（并行 W989 提交）代提
  ② T34 终稿报告 §6 执行记录 → 加一条「偏差 6」记录该事实与后续处置

用法：py -3 scripts/_w988_record_adoption.py [--dry-run]
"""
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(REPO, "CHANGELOG.md")
T34 = os.path.join(REPO, "docs", "11-方案报告", "计划方案",
                   "T34-任务计划执行与经验沉淀报告-2026-10-27.md")

OLD_STATUS = ("> - **状态**：已收官（内容批与登记面同批落地·既有 81 页题图的图源与 alt 未改动·"
              "27 张 `card-*` 源图本身未改动·12 个已有专属 og 图的页面未改动）")
NEW_STATUS = ("> - **状态**：已收官（**本批主体内容由并行会话的 W989 提交 `1fb1b14f` 代提入库**——"
              "该提交为全量提交且时点晚于本批 `git add -A`，故本批 115 个资产 / 102 个页面 / "
              "T34 报告 / 坑表 / 13 个脚本一并随之入库；本批另有一笔收官补齐提交登记代提事实与 "
              "E-17 坑位·既有 81 页题图的图源与 alt 未改动·27 张 `card-*` 源图本身未改动·"
              "12 个已有专属 og 图的页面未改动）")

DEVIATION_6 = ("| 偏差 6 | **本批主体内容被并行会话的 W989 提交代提入库** | 原计划为「W988 单笔提交」 | "
               "并行会话 `1fb1b14f chore(w989)` 是**全量提交**且发生在本批 `git add -A` 之后 ⇒ "
               "它把本批已暂存的 115 个资产 / 102 个页面 / T34 / 坑表 / 13 个脚本一并带入 | "
               "共享面（AGENTS.md / CHANGELOG.md / HANDOVER.md）被在途批次占用 ⇒ 全量提交必然代提"
               "（W986 批同族·坑表 E-06）；本批内容在 `git add -A` 之后才被并行批次提交捕获 | "
               "① 不回滚（回滚会连带撤销并行 W989 的合法改动）② 在 CHANGELOG W988 段「状态」行与本件 §6 如实登记代提事实 "
               "③ 台账 W988 行的 hash 与状态列写明「主体内容由 1fb1b14f 代提 + 收官补齐笔」 | 主会话 | 2026-10-27 |\n")

DEVIATION_7 = ("| 偏差 7 | 级联 spec 的「本批新增」判定用了 git **索引**，115 个资产漏列「文件」行 | "
               "原计划用 git 判定本批新增文件 | 判据脚本用 `git ls-files`（索引）判定 ⇒ 本批已 `git add -A` "
               "的新资产被误判为既有 ⇒ 「文件」行漏列 115 项；且 `batch_cascade` 的幂等保护（重跑断言"
               "「批次号应为 W+1」）使其**不能重跑** | ① 判定改用 **HEAD 树**（`git ls-tree -r HEAD`）；"
               "② 改做**段内定向订正**（限定 W988 段范围内替换「文件」行与 file-index 段表格）；"
               "③ 订正脚本必须最后执行且其后再 `git add`（否则 C4-f 判「工作树未提交残留」·实测连续三轮红） | "
               "主会话 | 2026-10-27 |\n")


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.replace("\r\n", "\n").replace("\n", nl).encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in os.sys.argv

    # ① CHANGELOG W988 段状态行
    t, n = read(CH)
    if "1fb1b14f" in t:
        print("SKIP  CHANGELOG 已登记代提事实")
    else:
        i = t.index("### W988")
        j = t.index("### W989") if "### W989" in t else t.index("### W987")
        seg = t[i:j]
        assert OLD_STATUS in seg, "W988 段状态行锚点失配"
        seg2 = seg.replace(OLD_STATUS, NEW_STATUS, 1)
        t2 = t[:i] + seg2 + t[j:]
        if dry:
            print("DRY  CHANGELOG W988 段状态行已订正")
        else:
            write(CH, t2, n)
            print("OK   CHANGELOG W988 段状态行已订正")

    # ② T34 §6 偏差表加两行 + 修正 E-17 证据列的偏差编号
    t, n = read(T34)
    if "| 偏差 6 |" in t:
        print("SKIP  T34 已有偏差 6")
    else:
        anchor = "| 偏差 5 |"
        i = t.index(anchor)
        j = t.index("\n", i) + 1
        t2 = t[:j] + DEVIATION_6 + DEVIATION_7 + t2_base(t[j:]) if False else \
            t[:j] + DEVIATION_6 + DEVIATION_7 + t[j:]
        t2 = t2.replace("本批偏差 6 · `_w988_make_spec.py`", "本批偏差 7 · `_w988_make_spec.py`")
        if dry:
            print("DRY  T34 §6 已加偏差 6/7 + E-17 编号修正")
        else:
            write(T34, t2, n)
            print("OK   T34 §6 已加偏差 6/7 + E-17 编号修正")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
