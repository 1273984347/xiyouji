#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_w930_spec_build.py — 生成 W930 批的 batch_cascade spec（不落盘级联，只写 spec 文件）

纪律（来自 `scripts/batch_cascade.py` 的 precheck 与字段说明）：
  · `title` 必须以 batch 号领衔；
  · `desc` 禁含 `·` `；` `—`（会写入版本行并破坏下一批锚点正则）；
  · `head_sentence` 禁含 `；` `—`（写入 HEAD 句）；禁含全角括号；
  · `head_entry` 必须以 `）` 结尾；
  · `changelog_body` 以两个换行开头，且**必须**含 `> - **文件**：` 行（repo 相对路径）；
    该行的每个路径须 ∈ HEAD 树 ∪ staged，否则第 31 门禁 C4-f 判「未入提交树」。
    ⇒ 本 spec 的文件清单写**改名后的新名**（`scripts/_w930_*` / `scripts/output/_w930_*`）。

用法：py -3 scripts/_w930_spec_build.py
产出：scripts/output/_w930_spec.json
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "scripts" / "output" / "_w930_spec.json"

# ---- 本批新增/改动的文件（repo 相对路径 · 改名后的新名）----
FILES = [
    "docs/11-方案报告/计划方案/T21-任务计划执行与经验沉淀报告-2026-10-25.md",
    "docs/11-方案报告/计划方案/执行前计划-T21-界面布局复核与落地方案.md",
    "docs/11-方案报告/README.md",
    "docs/00-导读/W批次编号对账表.md",
    "scripts/_w930_claim_row.py",
    "scripts/_w930_rename_prefix.py",
    "scripts/_w930_report_normalize.py",
    "scripts/_w930_spec_build.py",
    "scripts/_w930_layout_static.py",
    "scripts/_w930_layout_diff.py",
    "scripts/_w930_layout_attr.py",
    "scripts/_w930_layout_detail.py",
    "scripts/_w930_layout_residual.py",
    "scripts/_w930_layout_probe.mjs",
    "scripts/_w930_layout_probe_app.mjs",
    "scripts/output/_w930_layout_static.json",
    "scripts/output/_w930_layout_metrics.json",
    "scripts/output/_w930_layout_metrics_app.json",
    "scripts/output/_w930_layout_diff.json",
    "scripts/output/_w930_layout_attr.json",
    "scripts/output/_w930_visible_leak.json",
    "scripts/output/_w930_plan_review.json",
    "scripts/output/_w930_spec.json",
]

CHANGELOG_BODY = """

> **来源**：用户 2026-10-25 令「帮我优化现有界面布局：先帮我做好信息层级梳理、区块分布与留白、操作动线、不同屏幕适配都过一遍，每处调整讲清理由」；问卷答复 = 范围全站都做（静态站 + reader + agent-web）· 主攻信息层级（一屏信息量过载）· 先出审查报告与落地方案、用户过一遍再动代码。

> - **文件**：{files}

**定位：复核 + 补审，不是重做**——用户指令的四维与 W854《界面布局审计报告》（2026-10-21）几乎逐字相同，按 W926 §7.1 E-03「同一条指令重复下达时先查历史再动手」判为复核 + 补审：重跑 W854 探针（站点 11 组 + 应用 6 组，新旧 metrics JSON 逐项对拍）+ 补 W854 与 W926 均未覆盖的维度 + 出可施工落地方案。**W 号二次让号**（W928 归并行 D-1 实跑批、W929 归并行 Hero 素材图批，按「先落地者保留」）⇒ 本批取 W930，框架号 T21。

**W854 十八条的四天后现状（重跑探针实测，非复述）**：已修 6（S1 首屏内容入口 / S2 字号倒挂 / S3 手机层级坍塌 / S4 首页九区块同级 / S7 四套容器并存 / S9 hub 非链接）· 部分修 4（S5 间距刻度 / S6 令牌消费 / S8 目录页动线 / S14 卡片列数与触达目标）· 仍存 7（S1 衍生 mega 数字未降级 / S10 可视化页顶栏仅五入口 / S11 断点体系 / S12 KPI 不收缩 / S13 长段 77.9 字每行 / A1 / A4 / A5 / A6）· 未判定 1（A2 应用侧留白，服务端未起不可测）。首页三任务区由 W865 与 T-08 批施工落地。

**三条新发现（W854 与 W926 均未覆盖）**：① **N1** @1440 首页同标签混两档字号——「精选必看」「全卷索引」是 h3 但 24px，同区十张卡片 h3 为 20px，语义层级与视觉层级错位且仅在宽屏发作；② **N2** @375 首页 hero 山脉装饰图压正文文字（副标题被裁），静态几何审计与交互审计均不覆盖元素重叠；③ **N3** 可见工程批次号不只污染文本（796 页 6,827 处），同时是布局度量的基准污染源——W926 批次往四页页脚注入批次行使页高升 20 至 215 像素、元素数升 1 至 7，任何以页高或元素数为判据的布局审计都会被带偏。

**v4 令牌落地进度差**：容器族已消费（0 页至 851 页）· 间距族已消费（330 页至 857 页）· **排版族与语义 gap 族仍为 0 消费**（`tokens.css` 已定义九个排版角色与六档语义 gap）⇒ 改版者改了令牌值却看不到任何变化。间距刻度命中：原口径 43.3% 降至 31.2% 是判据失真（令牌化改造不被硬编码像素正则计入），修正口径 86.2% 为真值，两套口径同时输出以便旧数字仍可复算。

**六批可施工落地方案**（每批带理由与可机检验收判据，共约 8.5 人日）：B1 应用侧移动端可用性（@375 主区 115 像素至目标 320 像素以上）· B2 可见文本去工程化与页脚收口 · B3 排版与间距刻度消费化 · B4 可视化页自适应降级（KPI 与长行）· B5 首页宽屏层级与断点体系 · B6 目录页动线与触达目标。**本批不含任何界面代码改动**。

**四件套**：文件见上（改名后新名）· 验证：渲染实测 17 组 + 静态复算 1 次 + 独立复算 1 次 + 第 48 门禁双件全项符合（计划件判 PLAN 符合 23 项、报告件判 REPORT 符合 13 项，模糊词零命中）· 状态：方案件已落库，施工待用户拍板 U1 至 U4 · 边界：线上部署态、A1 运行时、A2 留白、英文站 138 页逐页、reader 620 页逐页、N2 影响面共六项显式声明未验证。

**诚实性边界**：本批只出报告与方案，不改 `site/` 与应用源码；级联器固定面会向三页页脚注入本批批次链行（共四行），该行为同时是 N3 所指污染源之一，已显式登记为 B2 的整改对象，不在本批静默处理。
""".format(files="、".join(FILES))

MILESTONE = """- **W930 界面布局复核与落地方案**：
  - W854 十八条四天后现状逐条重测（已修 6 / 部分修 4 / 仍存 7 / 未判定 1）+ 三条新发现（宽屏同标签字号两档 / 375 装饰压字 / 可见工程文本污染布局度量）
  - v4 令牌落地进度差已对拍（容器族与间距族已消费，排版族与语义 gap 族仍为零）
  - 六批可施工落地方案与四道可机检验收判据已出，待用户拍板后施工
  - 本批对界面代码零改动（级联器固定面三页页脚批次链行除外，已显式登记）"""

AGENTS_NOTE = """二〇二五年十月二十五日（W930）把四天前那份界面布局审计重新量了一遍。做法不是重扫一遍，是把上次的探针原样再跑一遍——只改了落点，这样新旧两天的数字能直接对拍。结论有点反直觉：十八条里已经修好六条，四条修了一半，七条还在原地，但最该先修的那条不在这个列表里——是应用在手机上的可用性，四百像素的屏幕里侧栏占掉二百六十，主区只剩一百一十五。另外新看出三件事：宽屏上同一级标题有三种尺寸、手机上装饰的山把正文压住了、还有最要命的一条——页面里露着几千处工程批次号，不只是难看，它把版面高度这些量尺都弄脏了，别的批次量出来的高度差有一半是它造成的。所以这批没动一行界面代码，只把六批怎么做、每批凭什么这么做、做完怎么验都写清楚了，等人拍板。"""

SPEC = {
    "batch": "W930",
    "version": "V1.0",
    "date": "2026-10-25",
    "title": "W930 界面布局复核与落地方案（信息层级四维复核 + 三条新发现 + 六批可施工方案）",
    "desc": "W854 十八条四天后现状复核 + 三条新发现 + 六批可施工落地方案",
    "head_entry": "2026-10-25（W930 界面布局复核与落地方案）",
    "head_sentence": "W854 十八条四天后现状逐条重测已修六条，三条新发现补上布局审计盲区，六批落地方案待拍板",
    "changelog_body": CHANGELOG_BODY,
    "milestone_block": MILESTONE,
    "agents_note": AGENTS_NOTE,
    "file_index_rows": [
        "| docs/11-方案报告/计划方案/T21-任务计划执行与经验沉淀报告-2026-10-25.md | W930 | 四维复核结论（18 条现状表）+ 三条新发现 + 六批可施工落地方案 + 6 条未验证项 |",
        "| docs/11-方案报告/计划方案/执行前计划-T21-界面布局复核与落地方案.md | W930 | T-21 框架件·执行前计划（九表齐备：标识/目标/边界/ASM/ST/V/R/D/自包含） |",
        "| docs/11-方案报告/README.md | W930 | §六 计划方案 +1 行（篇数 24→25） |",
        "| docs/00-导读/W批次编号对账表.md | W930 | W930 认领行（二次让号依据 + touches 声明） |",
        "| scripts/_w930_layout_static.py | W930 | 静态复算（间距刻度 / 令牌消费 / 断点清点·原口径 + 修正口径两套输出） |",
        "| scripts/_w930_layout_diff.py | W930 | 新旧逐项对拍（缺失字段标 MISSING 不填 0） |",
        "| scripts/_w930_layout_attr.py | W930 | 增量归因（区分布局劣化与内容增量） |",
        "| scripts/_w930_layout_detail.py | W930 | 标题字号序列 + 应用侧几何对拍 |",
        "| scripts/_w930_layout_residual.py | W930 | 容器档位 / 长段字数每行 / 顶栏入口数 / 应用侧留白 |",
        "| scripts/_w930_layout_probe.mjs | W930 | 站点渲染探针 11 组（复用 W854 探针改落点 + 目录自建） |",
        "| scripts/_w930_layout_probe_app.mjs | W930 | 应用渲染探针 6 组（复用 W854 探针改落点） |",
        "| scripts/_w930_claim_row.py | W930 | 台账认领行登记脚本（幂等·不覆盖他人认领的号） |",
        "| scripts/_w930_rename_prefix.py | W930 | 产物前缀统一改名脚本（幂等 + 残留校验） |",
        "| scripts/_w930_report_normalize.py | W930 | 报告件归一为纯报告侧（去触发词 + 补报告侧 token） |",
        "| scripts/output/_w930_layout_static.json | W930 | 静态复算证据 |",
        "| scripts/output/_w930_layout_metrics.json | W930 | 站点渲染实测证据（11 组） |",
        "| scripts/output/_w930_layout_metrics_app.json | W930 | 应用渲染实测证据（6 组） |",
        "| scripts/output/_w930_layout_diff.json | W930 | 新旧对拍证据 |",
        "| scripts/output/_w930_layout_attr.json | W930 | 增量归因证据 |",
        "| scripts/output/_w930_visible_leak.json | W930 | 可见工程批次号复算证据（796 页 6,827 处） |",
        "| scripts/output/_w930_plan_review.json | W930 | 第 48 门禁判据矩阵证据（双件全项符合） |",
        "| scripts/output/_w930_spec.json | W930 | 本批级联 spec |",
    ],
}


def main() -> int:
    # 自检：分隔符黑名单 + 领衔断言 + 文件行存在
    for field, banned in (("desc", ("·", "；", "—")), ("head_sentence", ("；", "—"))):
        for sep in banned:
            if sep in SPEC[field]:
                print("FATAL: spec.%s 含禁用分隔符 %r" % (field, sep))
                return 2
    if not SPEC["title"].startswith(SPEC["batch"]):
        print("FATAL: title 未以 batch 号领衔")
        return 2
    if "**文件**：" not in SPEC["changelog_body"]:
        print("FATAL: changelog_body 缺「**文件**：」行")
        return 2
    if not SPEC["head_entry"].endswith("）"):
        print("FATAL: head_entry 未以闭合括号结尾")
        return 2
    if "（" in SPEC["head_sentence"] or "）" in SPEC["head_sentence"]:
        print("FATAL: head_sentence 含全角括号")
        return 2
    # spec 自身由本脚本即将产出 ⇒ 豁免存在性自检（其余任一缺失即报错）
    missing = [
        f for f in FILES
        if f != "scripts/output/_w930_spec.json" and not (REPO / f).exists()
    ]
    if missing:
        print("FATAL: 文件清单中下列路径在磁盘不存在（会被 C4-f 判未入提交树）：")
        for m in missing:
            print("   -", m)
        return 3
    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(
        json.dumps(SPEC, ensure_ascii=False, indent=1)
    )
    print(f"spec 已写出：{OUT}")
    print(f"文件清单 {len(FILES)} 件（全部在磁盘存在）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
