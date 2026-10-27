#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w945_cascade.py — W945 四面登记 + 当前态指针（内页专题题图成套批·8 张线描人物题图）

模式承自 _w944_cascade.py：台账行插在 W944 行之后（升序区）；CHANGELOG / file-index 段插在最前（降序区）。
幂等：已存在则跳过；写回用 newline=''（不二次转换 \r\n）。
"""
import argparse
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = "W945"
LEDGER = os.path.join(REPO, "docs", "00-导读", "W批次编号对账表.md")
CHANGELOG = os.path.join(REPO, "CHANGELOG.md")
FILE_INDEX = os.path.join(REPO, "scripts", "output", "file-index.md")

PLATE_FILES = [
    "plate-line-01-wukong.webp",
    "plate-line-02-tangseng.webp",
    "plate-line-03-bajie.webp",
    "plate-line-04-shaseng.webp",
    "plate-line-05-guanyin.webp",
    "plate-line-06-erlangshen.webp",
    "plate-line-07-baigujing.webp",
    "plate-line-08-honghaier.webp",
]

TARGET_PAGES = [
    "site/reader/themes/猴王到行者-五次蜕变.html",
    "site/reader/themes/唐僧-凡躯圣心.html",
    "site/reader/people/猪八戒.html",
    "site/reader/themes/沙僧-沉默者的智慧.html",
    "site/reader/people/观音.html",
    "site/reader/people/二郎神.html",
    "site/reader/people/白骨精.html",
    "site/reader/people/红孩儿.html",
]

CLAIM_ROW = (
    "| W945 | 内页专题题图成套批（用户 2026-10-25 令「在继续帮我做几张素材图」·开工前三问已答："
    "**用途=内页专题题图 3:4 竖版** / **张数=8 张** / **风格=沿用站内线描墨稿风** / **题材=人物专题**）："
    "① **缺口**——站内 `site/reader/` 共 622 页，**仅 11 页有题图**（6 回目页 + 5 专题页），"
    "people/themes/essays/poetry/culture 五库绝大部分页面无题图；② **产出**——8 张**线描墨稿风人物题图**"
    "（3:4 竖版 · 1200×1600 · 宣纸底 #FAF7F0 + 单色墨线 + 赭金 #8A6D3B 细节 + 单处朱砂 #C8463A 点睛 · "
    "**上部 28% 纯纸面留白**供标题叠字 · 主体居中偏下），题材=大圣悟空/唐僧/猪八戒/沙僧/观音/二郎神/白骨精/红孩儿，"
    "每张配一个**独占标志物**（金箍棒/五佛冠+念珠/九齿钉耙/降妖宝杖+骷髅念珠/玉净瓶插杨柳/三尖两刃刀+额间竖目/"
    "三变残影/火尖枪+三昧真火）；③ **接入**——按站内 `chapter-plate` 范式（420px 居中 + 描述性 alt + 暗色模式隐藏）"
    "插入 8 个对应专题页；④ **判据**——J1–J7 机器关（尺寸/顶部留白/墨量/朱砂点/实心块/伪文字/裁切）+ "
    "**J8 人工关**（独占标志物 + 形制级：钉耙齿数/冠形/杆形/瓶插枝/三尖刃/火焰形）；⑤ **前置**——"
    "preflight 取号 W945（max=W944+1）· touches 交集命中 8 条**全部指向本会话自身历史批次**"
    "（W931/W936/W937/W938/W940/W942/W943/W944·台账状态列仍写「在途」但实际早已入库）⇒ "
    "经三态核查（会话清单 + 工作树 + 暂存）确认唯一他方活跃会话为 emoji 图标批（W941·已入库·此刻仅动 site/data/*），"
    "CHANGELOG/file-index/台账工作树干净 ⇒ 人工裁决放行，按 §11.0 纯追加 + 精确暂存写入 | "
    "—（待回填） | —（待回填） | 在途（认领·未收官） | 并行 Agent 会话 2026-10-25（内页专题题图成套批） | "
    "`site/static/images/plate-line-01~08-*.webp`（8 张新增）· `assets/promo/plate-set/`（原件 + README + 拼图）· "
    "`site/reader/themes/猴王到行者-五次蜕变.html` · `site/reader/themes/唐僧-凡躯圣心.html` · "
    "`site/reader/people/猪八戒.html` · `site/reader/themes/沙僧-沉默者的智慧.html` · "
    "`site/reader/people/观音.html` · `site/reader/people/二郎神.html` · "
    "`site/reader/people/白骨精.html` · `site/reader/people/红孩儿.html`（8 页接入题图）· "
    "`scripts/_w945_cascade.py`（本批脚本）· `scripts/_w945_plates_verify.py`（判据）· "
    "`scripts/_w945_insert_plates.py`（页面接入）· `CHANGELOG.md`（W945 版段）· "
    "`docs/00-导读/W批次编号对账表.md`（本行）· `scripts/output/file-index.md`（W945 段） |"
)

CHANGELOG_SEG = """### W945（2026-10-25）：内页专题题图成套（8 张 3:4 线描人物题图·622 页仅 11 页有题图的缺口）

> **来源**：用户 2026-10-25 令「在继续帮我做几张素材图：用途与画幅、风格与配色统一、主体清晰、留好放文字的空间都考虑到，成套出图保证风格一致」，并要求开工前先问三件事。
>
> **三问答复**：① 用途与画幅 = **内页专题题图 · 3:4 竖版** ② 张数 = **8 张** ③ 参考风格 = **沿用站内线描墨稿风**（附加题材范围 = **人物专题**）。
>
> - **文件**：site/static/images/plate-line-01~08-*.webp、assets/promo/plate-set/**、8 个 reader 专题页、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/_w945_cascade.py、scripts/_w945_plates_verify.py、scripts/_w945_insert_plates.py

**缺口**：站内 `site/reader/` 共 **622 页**，其中**仅 11 页**有题图（6 个回目页 + 5 个专题页）——people / themes / essays / poetry / culture 五库绝大部分页面无题图。

**产出**：8 张**线描墨稿风人物题图**，3:4 竖版（`1200×1600`），沿用站内线描语言（宣纸底 `#FAF7F0` + 单色墨线 + 赭金 `#8A6D3B` 细节 + 单处朱砂 `#C8463A` 点睛），**上部 28% 保持纯纸面留白**供标题叠字，主体居中偏下：

| # | 主体 | 独占标志物（形制级） | 接入页 |
|---|---|---|---|
| 01 | 大圣悟空 | 如意金箍棒（两端金箍 + 云纹）+ 凤翅紫金冠 | themes/猴王到行者-五次蜕变 |
| 02 | 唐僧 | 五佛冠 + 念珠 + 九环锡杖 | themes/唐僧-凡躯圣心 |
| 03 | 猪八戒 | 九齿钉耙 + 蒲扇耳 | people/猪八戒 |
| 04 | 沙僧 | 降妖宝杖（月牙刃）+ 骷髅念珠 | themes/沙僧-沉默者的智慧 |
| 05 | 观音菩萨 | 玉净瓶插杨柳枝 + 莲花座 | people/观音 |
| 06 | 二郎神 | 三尖两刃刀 + 额间竖目 | people/二郎神 |
| 07 | 白骨精 | 三变残影（村姑 / 老妇 / 老翁） | people/白骨精 |
| 08 | 红孩儿 | 火尖枪 + 三昧真火 | people/红孩儿 |

**接入范式**：沿用站内 `chapter-plate`（`max-width: 420px` 居中 + 描述性 alt + 浅底图暗色模式隐藏）。

**判据**：J1–J7 机器关（尺寸 / 顶部留白 / 墨量 / 朱砂点 / 实心块 / 伪文字 / 裁切）+ **J8 人工关**（独占标志物 + 形制级细节）——题材与形制机器判据查不出，只能人眼核。

> - **验证**：（见本批脚本输出与对账表回填）
> - **状态**：在途（认领登记 W945·待提交入库）

"""

FILE_INDEX_SEG = (
    "## W945 内页专题题图成套（8 张 3:4 线描人物题图）（2026-10-25）\n\n"
    "| 文件 | W | 说明 |\n"
    "|---|---|---|\n"
    "| site/static/images/plate-line-01-wukong.webp | W945 | 新增·大圣悟空（金箍棒 + 凤翅紫金冠） |\n"
    "| site/static/images/plate-line-02-tangseng.webp | W945 | 新增·唐僧（五佛冠 + 念珠 + 九环锡杖） |\n"
    "| site/static/images/plate-line-03-bajie.webp | W945 | 新增·猪八戒（九齿钉耙 + 蒲扇耳） |\n"
    "| site/static/images/plate-line-04-shaseng.webp | W945 | 新增·沙僧（降妖宝杖 + 骷髅念珠） |\n"
    "| site/static/images/plate-line-05-guanyin.webp | W945 | 新增·观音（玉净瓶插杨柳 + 莲座） |\n"
    "| site/static/images/plate-line-06-erlangshen.webp | W945 | 新增·二郎神（三尖两刃刀 + 额间竖目） |\n"
    "| site/static/images/plate-line-07-baigujing.webp | W945 | 新增·白骨精（三变残影） |\n"
    "| site/static/images/plate-line-08-honghaier.webp | W945 | 新增·红孩儿（火尖枪 + 三昧真火） |\n"
    "| assets/promo/plate-set/ | W945 | 出图原件 + 逐张清单 + J8 自检表 + 拼图 |\n"
    "| scripts/_w945_plates_verify.py | W945 | J1–J7 机器判据 + J8 题材自检表 |\n"
    "| scripts/_w945_insert_plates.py | W945 | 8 页 chapter-plate 接入（幂等） |\n"
    "| scripts/_w945_cascade.py | W945 | 四面登记 + 当前态指针 |\n"
    "| CHANGELOG.md | W945 | W945 版段 |\n"
    "| docs/00-导读/W批次编号对账表.md | W945 | W945 认领行 |\n"
    "\n"
)


def read(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def write(p, t, nl):
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))


def changelog_segs(txt):
    out = []
    for i, ln in enumerate(txt.split("\n")):
        if ln.startswith("### "):
            m = re.search(r"W(\d+)", ln)
            if m:
                out.append((int(m.group(1)), i))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dry = args.dry_run
    rep = []

    # ---- 1) 台账认领行（插在 W944 行之后）----
    t, nl = read(LEDGER)
    if re.search(r"^\| " + BATCH + r" \|", t, re.M):
        rep.append("认领行已存在（幂等跳过）")
    else:
        lines = t.split("\n")
        anchor = None
        for i, ln in enumerate(lines):
            if re.match(r"^\| W944 \|", ln):
                anchor = i
                break
        if anchor is None:
            print("FATAL 未找到 W944 锚点行")
            return 2
        lines.insert(anchor + 1, CLAIM_ROW)
        new_t = "\n".join(lines)
        if len(re.findall(r"^\| W945 \|", new_t, re.M)) != 1:
            print("FATAL 台账行插入异常")
            return 2
        rep.append(("DRY " if dry else "") + "认领行已插入（第 %d 行）" % (anchor + 2))
        if not dry:
            write(LEDGER, new_t, nl)

    # ---- 2) CHANGELOG 段（降序·插在最前）----
    t, nl = read(CHANGELOG)
    if re.search(r"^### " + BATCH + r"（", t, re.M):
        rep.append("CHANGELOG 段已存在（幂等跳过）")
    else:
        # 注意：段标题形态为「### W944（2026-10-25）：…」·括号是全角·其后不是空格
        m = re.search(r"^### W\d+", t, re.M)
        pos = m.start() if m else len(t)
        new_t = t[:pos] + CHANGELOG_SEG + t[pos:]
        nums = [n for n, _ in changelog_segs(new_t)]
        if nums.count(945) != 1:
            print("FATAL CHANGELOG 段序断言失败（count=%d）" % nums.count(945))
            return 2
        if any(nums[i] < nums[i + 1] for i in range(len(nums) - 1)):
            print("FATAL CHANGELOG 非降序")
            return 2
        rep.append(("DRY " if dry else "") + "CHANGELOG 段已插入（段序前 5 = %s）" % nums[:5])
        if not dry:
            write(CHANGELOG, new_t, nl)

    # ---- 3) file-index 段（降序·插在最前）----
    t, nl = read(FILE_INDEX)
    if re.search(r"^## " + BATCH + r" ", t, re.M):
        rep.append("file-index 段已存在（幂等跳过）")
    else:
        m = re.search(r"^## W\d+", t, re.M)
        pos = m.start() if m else len(t)
        new_t = t[:pos] + FILE_INDEX_SEG + t[pos:]
        if len(re.findall(r"^## W945 ", new_t, re.M)) != 1:
            print("FATAL file-index 目标段异常")
            return 2
        rep.append(("DRY " if dry else "") + "file-index 段已插入")
        if not dry:
            write(FILE_INDEX, new_t, nl)

    # ---- 4) README 抬头（当前批次指针）----
    p = os.path.join(REPO, "README.md")
    t, nl = read(p)
    new_t = re.sub(
        r"> \*\*当前批次 W\d+（2026-10-25）\*\*：[^\n]*",
        "> **当前批次 W945（2026-10-25）**：内页专题题图成套（八张 3:4 线描人物题图，接入 8 个 reader 专题页）",
        t, count=1)
    if new_t != t:
        rep.append(("DRY " if dry else "") + "README 抬头已更新")
        if not dry:
            write(p, new_t, nl)
    else:
        rep.append("README 抬头已指向 W945（幂等跳过）")

    # ---- 5) HANDOVER 指针 ----
    # 整行重建（W944 脚本的「逐段替换」写法会把上一批的名字覆写成当前批名 ⇒ 链条污染·此处改为幂等整行重建）
    HANDOVER_LINE = (
        "> 最后更新：2026-10-25（W945 内页专题题图成套批）·2026-10-25（W944 章回插画新组批）·"
        "2026-10-25（W943 全站图片审查批）·2026-10-25（W942 Hero 素材全量复审批）·"
        "2026-10-25（W941 UI 图标位 emoji 治理批 + 东方线描图标集自绘）·"
        "2026-10-25（W940 Hero 素材题材辨识度修正批）·2026-10-25（W938 首屏版式重做 + 图集逐张复核批）·"
        "2026-10-25（W937 首屏版式修正批）·（W449-W549 及更早批次详见 CHANGELOG.md）"
    )
    p = os.path.join(REPO, "HANDOVER.md")
    t, nl = read(p)
    new_t = re.sub(r"> 最后更新：2026-10-25[^\n]*", HANDOVER_LINE, t, count=1)
    # 去重：先删掉本脚本此前插入的所有 W945 进度条目（历史 W944/W943 条目保留）
    new_t = re.sub(r"- \*\*W945 内页专题题图成套批\*\*：[^\n]*\n", "", new_t)
    # 整段替换「标题 + 紧随的 W945 条目」⇒ 幂等（只匹配标题行，插入 1 条）
    new_t = re.sub(
        r"## 一、当前进度（W\d+[^\n]*\n",
        "## 一、当前进度（W945 内页专题题图成套批；更早批次详见 CHANGELOG.md）\n"
        "- **W945 内页专题题图成套批**：reader 622 页中仅 11 页有题图 ⇒ 补 8 张 3:4 线描人物题图"
        "（悟空/唐僧/八戒/沙僧/观音/二郎神/白骨精/红孩儿），按 chapter-plate 范式接入 8 个专题页。\n",
        new_t, count=1)
    new_t = re.sub(
        r"每次完成新 W### 后更新。最后更新：2026-10-25[^\n]*",
        "每次完成新 W### 后更新。最后更新：2026-10-25（W945 内页专题题图成套批）",
        new_t, count=1)
    if new_t != t:
        rep.append(("DRY " if dry else "") + "HANDOVER 指针已更新")
        if not dry:
            write(p, new_t, nl)
    else:
        rep.append("HANDOVER 指针已指向 W945（幂等跳过）")

    # ---- 6) CHANGELOG 规则段 W 号上界 ----
    t, nl = read(CHANGELOG)
    new_t = re.sub(r"（W001-W\d+）", "（W001-W945）", t, count=1)
    if new_t != t:
        rep.append(("DRY " if dry else "") + "CHANGELOG 规则段已更新")
        if not dry:
            write(CHANGELOG, new_t, nl)
    else:
        rep.append("CHANGELOG 规则段已是 W001-W945（幂等跳过）")

    for r in rep:
        print(" -", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
