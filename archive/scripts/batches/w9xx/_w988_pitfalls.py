#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w988_pitfalls.py — W988 坑表 +6 条与计数链同步（原子替换·保行尾）

新增（编号沿用既有 E-XX 序列，止于 E-10 → 从 E-11 起）：
  CSS / 视觉渲染：E-12 · E-13 · E-15
  git / 提交 / 并发：E-11
  流程 / 协作 / 取证：E-14 · E-16
计数链同步：坑表各节标题条数 · AGENTS.md 两处 · HANDOVER.md 两处

用法：py -3 scripts/_w988_pitfalls.py [--dry-run]
"""
from __future__ import annotations

import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIT = os.path.join(ROOT, "docs", "agent", "pitfalls.md")

CSS_NEW = """- **目测截图会把「设备像素」当「CSS 像素」⇒ 误判 CSS 规则失效**（W988 实证·E-12）：验收时量浏览器渲染尺寸，**禁止**靠目测「框贴不贴边沿」推断 `max-width` 是否生效——截图分辨率 ≠ CSS 视口宽度（Electron 下常差 1.2–1.5 倍）。本批实测：横幅 `max-width: 720px` 在 **728px 宽**的阅读容器里**本就近乎通栏**（目测「贴左沿 ⇒ 规则失效」），若据此改代码会把正确规则改成错误规则。⇒ 修法：① **先找一个已知值做校准锚点**（临时给某元素加 `max-width: 300px` 并描边，量出该框像素宽 ⇒ 得出缩放比）；② 所有测量值除以缩放比换算成 CSS px；③ 只关心相对关系时（如「图在题图上方还是下方」）不受影响，可直接目测。
- **检测「主体」前先问「这族资产里的非墨元素是什么」**（W988 实证·E-13）：按墨迹定位主体做裁切/对齐/检测时，**水墨卡族每张带一枚朱红印章**（右下/左下角）——印章与纸色差值远大于阈值 ⇒ 整幅 bbox 会把印章当成主体的一部分（主体底被拉到画布底、主体顶被拉到印章顶），裁切线整体失准。⇒ 修法：① 主体掩膜**排除朱砂**（判据 `r−g ≥ 35`，朱砂 #C8463A 的 r−g=70；赭金 #8A6D3B 的 r−g=29 不误判）与**赭金**（`luma ≥ 90`，赭金 luma≈112）；② 主体顶用**面积 ≥ 200 px² 的连通簇**的最小顶（整幅 bbox 会被孤立噪点拉歪·W974 实证）；③ 主体底用全部有效簇的最大底（底部地面线常是小簇，漏掉会丢「地面留白」）。本批 27 张实测全部正确。
- **「按主体顶裁」的前提是主体在顶部**（W988 实证·E-15）：1:1 → 宽幅/高图的派生裁切不能一律用「主体顶 − N px」。本批 13 张横幅里 1 张（山门+三人背影）**上部 2/3 是巨石、下部才是人物** ⇒ 通用规则把人物整段切掉，只剩一道门。⇒ 修法：① 逐张看裁切后的主体是否完整（缩略拼图只判趋势，缺陷结论必须回单图）；② 主体重心在下部时**逐张定裁切带**（本批该张改用下带 [389, 889]）；③ 派生脚本要支持**特例带**，且特例**只对目标模式生效**（本批 override 曾误作用到 og 派生 ⇒ 500 高内容被拉成 630 高变形）。
"""

GIT_NEW = """- **写盘行尾二次替换 ⇒ CRLF 变 CRCRLF（批量污染但 diff 静音）**（W988 实证·E-11）：Windows + `core.autocrlf=true` 的仓里，**工作区文件是 CRLF、仓库存 LF**；批量脚本若写盘时做 `text.replace("\\n", "\\r\\n")` ⇒ 读入文本本身已含 CRLF ⇒ **每个换行多一个 CR**（CRLF→CRCRLF），同一文件被改两次还进一步变成 CRCRCRLF。⇒ 危害：① 行尾被整批污染；② `git diff --numstat` 出现「增删比 ≈ 2:1 但非空行数不变」的噪音，**只看「内容对不对」完全看不出问题**。⇒ 修法：① 读入时原样保留换行（`raw.decode()`）；② 写回**原样写字节**（`io.open(tmp,"wb").write(text.encode())`），**禁**对全文做换行替换；③ 插入内容时用探测到的真实行尾拼接；④ 改完跑「CRCRLF 计数 = 0」断言（字节级循环 `replace(b"\\r\\r\\n", b"\\r\\n")` 直至收敛）。本批实测污染 102 个页面。
"""

PROC_NEW = """- **按文件名/关键词匹配题材 ⇒ 对「无题材词」与「通用角色词」双重失效**（W988 实证·E-14）：为既有资产定投放位置/分类/检索时，关键词法两头都不准——本批 27 张卡：**8 张**（`card-21`~`card-27`）文件名不含题材词 ⇒ 命中 **0** 个候选（「候选 0」≠「无落位页」）；**14 张**含「八戒/沙僧」这类通用角色词 ⇒ 命中 **11–14** 个候选（命中所有提及该角色的页）。⇒ 修法：① **实读画面**定题材（拼图一次看全，同族一次性判读）；② 检索只用于**缩小候选范围**，不用于定案；③ 命中数为 0 先怀疑「词没写全」，命中数 > 10 先怀疑「词太通用」。
- **判据自身的缺陷会让「全绿」变成假绿**（W988 实证·E-16）：自建验收判据时，**判据本身会错**，且错法与被测物的错法相反（本批首版把 27 个正常页全判红）。⇒ 三类实证缺陷：① **计数类判据必须行首锚定**——用 `s.count(".chapter-banner {")` 会把 `html[data-theme="dark"] .chapter-banner {` 也算成第二条规则（子串命中）⇒ 改 `re.compile(r"^[ \\t]*\\.chapter-banner \\{", re.M)`；② **负样本必须命中判据的正则形态**——负样本里插一个**空** `<figure class="chapter-banner"></figure>`，判据的正则要求其后跟 `<img src=…>` ⇒ 匹配数不变 ⇒ 「多 figure」检查**恒真而不报警**；③ 每个负样本只破坏**一个维度**，否则一个坏样本会掩盖其它判据（实测「缺CSS」样本命中后，其余三个样本的独立维度全被掩盖）。⇒ 配套：判据报错时**先怀疑判据再怀疑被测物**；判据必须带**负样本自证**并逐条报告命中维度。
"""


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.replace("\r\n", "\n").replace("\n", nl).encode("utf-8"))
    os.replace(tmp, p)


def insert_before_section(text, heading, block):
    """在该节标题行之前插入条目块（保持条目连续）。"""
    i = text.index(heading)
    return text[:i] + block + text[i:]


def main() -> int:
    dry = "--dry-run" in sys.argv
    text, nl = read(PIT)
    orig = text

    # ① 三节各加条目
    text = insert_before_section(text, "### JS / CSP / 运行时", CSS_NEW)
    text = insert_before_section(text, "### 级联 / CHANGELOG", GIT_NEW)
    # 「流程 / 协作 / 取证」是最后一节 ⇒ 追加到文末
    text = text.rstrip("\n") + "\n" + PROC_NEW

    # ② 节标题计数
    text = text.replace("### CSS / 视觉渲染（21 条）", "### CSS / 视觉渲染（24 条）")
    text = text.replace("### git / 提交 / 并发（19 条）", "### git / 提交 / 并发（20 条）")
    text = text.replace("### 流程 / 协作 / 取证（17 条）", "### 流程 / 协作 / 取证（19 条）")

    # ③ 计数链：AGENTS.md 两处 + HANDOVER.md 两处
    others = []
    for rel, subs in [
        ("AGENTS.md", [
            ("索引型——80 条坑位按六主题迁", "索引型——86 条坑位按六主题迁"),
            ("CSS/视觉渲染（21）· JS/CSP/运行时（6）· git/提交/并发（19）· 级联/CHANGELOG（8）· 数据/内容可信度（9）· 流程/协作/取证（17）",
             "CSS/视觉渲染（24）· JS/CSP/运行时（6）· git/提交/并发（20）· 级联/CHANGELOG（8）· 数据/内容可信度（9）· 流程/协作/取证（19）"),
        ]),
        ("HANDOVER.md", [
            ("[docs/agent/pitfalls.md](docs/agent/pitfalls.md)（80 条·六主题）与",
             "[docs/agent/pitfalls.md](docs/agent/pitfalls.md)（86 条·六主题）与"),
            ("（80 条·六主题·含 shell 场景查坑表）", "（86 条·六主题·含 shell 场景查坑表）"),
        ]),
    ]:
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        t, n = read(p)
        for old, new in subs:
            if old not in t:
                print("WARN  未找到待替换文本（%s）：%s" % (rel, old[:50]))
                continue
            t = t.replace(old, new)
        if t != read(p)[0]:
            others.append((p, t, n))

    if dry:
        print("DRY  坑表将改：%d 处；计数链文件：%d 个" % (1 if text != orig else 0, len(others)))
    else:
        write(PIT, text, nl)
        print("OK   坑表已更新（+6 条：CSS +3 · git +1 · 流程 +2）")
        for p, t, n in others:
            write(p, t, n)
            print("OK   计数链已同步：%s" % os.path.relpath(p, ROOT).replace("\\", "/"))

    # ④ 复核
    t2, _ = read(PIT)
    counts = {}
    for m in re.finditer(r"^### .+?（(\d+) 条）", t2, re.M):
        counts[m.group(0).split("（")[0].replace("### ", "")] = int(m.group(1))
    print("各节计数：", counts, "合计", sum(counts.values()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
