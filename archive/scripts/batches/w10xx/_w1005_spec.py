# -*- coding: utf-8 -*-
"""_w1005_spec.py — W1005 级联 spec 生成（CHANGELOG 段 + 14 面版本面推进）

现役段是 W1004 ⇒ `batch_cascade` 的幂等断言「批次号应为 顶段+1 = W1005」成立 ⇒
**本批可由级联正式落 W1005 段**（此前 W1001 批因手工插段导致级联跑不动·已用「先摘段再级联」解决）。

约束（来自 batch_cascade 的 precheck）：
  · spec.desc 不得含分隔符「·」（会写入版本行并使下一批锚点正则失配）
  · spec.agents_note ≤ 120 字（W989 收紧）
  · spec.changelog_body 必含「**文件**」行（第 31 门禁 C4-f 据其对账）

输出：scripts/output/_w1005_spec.json
"""
import json
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")

# ---------- 本批实际改动的文件（上一笔提交 + 当前工作树） ----------
names = set()
for rev in ("HEAD",):
    r = subprocess.run(["git", "show", "--name-only", "--pretty=format:", rev],
                       capture_output=True, text=True, cwd=REPO).stdout
    names |= {x.strip() for x in r.splitlines() if x.strip()}
st = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=REPO).stdout
for ln in st.splitlines():
    if ln[:2] == "??":
        names.add(ln[3:].strip().strip('"').replace("\\", "/"))
names = {n for n in names if n and not n.endswith(("_commit_msg.txt", "_serve.log", "_serve.err"))}

FILES = sorted(names)

BODY = (
    "\n\n\n\n> **来源**：用户 2026-10-29 指出 `site/static/images/ink-mountains-hero.webp`"
    "「内容不符合西游记·为什么有七个人」→ 问卷裁定人物口径＝取经五人组（4 人形 + 1 匹白马）、范围＝两张一并修。\n"
    ">\n"
    "> **根因**：W852 批 hero-set 01/06 档案即明写「山脊云海+**七人单行**」⇒ 人数错误源自 W852 批，"
    "W879 批原地替换该图时沿用了同一错误 ⇒ 两张同族图都是错的。\n"
    ">\n"
    "> - **文件**：" + "、".join(FILES) + "。\n\n"
    "**本批要点**：① **两张原地替换**（同文件名同尺寸 ⇒ 848 个 .hero 页面零页面改动）——"
    "`ink-mountains-hero.webp`（1792×1024·深底 soft-light 合成底图）与 `hero-01-xihai-yunhai.webp`"
    "（2560×1440·宣传单页配图）均改为 **4 人形 + 1 匹白马**（唐僧·悟空·八戒·沙僧 + 白龙马）；"
    "② **README 三张图同步**——主视觉 banner 引用同一路径故自动更新；`assets/images/index-preview.png` 因首页不使用 .hero 不受影响；"
    "**flyer A4 正面 PNG 是静态渲染快照不会自动更新 ⇒ 本批用 Playwright 重渲染**（中英各一·1240×1756 单页 clip）；"
    "③ **队伍落位须避开下边缘**——.hero 用 `background-position: center 70%`，首版队伍贴画面下缘 ⇒ 合成后被裁出只剩孤马，"
    "prompt 追加「队伍位于山脊中部（垂直 45%–60%）·裁切后仍须完整可见」；"
    "④ **显影度**（soft-light 叠 #221D16 后亮度跨度）= 0.2192（W879 批门槛 ≥0.07）；"
    "⑤ **人数只能人眼硬关**——「深墨小簇计数」判据不可用（山水皴笔碎点被计入：67/20），"
    "人眼核对两张均 4 人形 + 1 匹白马；⑥ **代并行 W1004 结清 5 处版本面欠账**（CHANGELOG 编号规则 / "
    "workflows README 头部 / HANDOVER 当前 HEAD 句 / HANDOVER §一 链首 / 项目说明版本行 desc 的「·」）⇒ 消解门禁 5 处红。\n\n"
    "**验证**：母版判据与裁切验算沿用 W1001 批口径（88/88 PASS）· 显影度 0.2192 · 单件 117.6 / 83.6 KB · "
    "人眼核对 2/2（4 人形 + 1 匹白马）· 浏览器实跑（data 页 .hero 深底合成·队伍剪影完整可见）· "
    "flyer PNG 重渲染后尺寸 1240×1756 与原产物一致 · 全量门禁 55/55 段全绿。\n\n"
    "> - **状态**：已收官（两张原地替换 + flyer 快照重渲染 + 版本面欠账代清偿；"
    "坑表条目与本批终稿报告待下一批补写·台账状态在本笔回填）\n"
)

rows = []
for f in FILES:
    note = "本批改动"
    if f.startswith("site/static/images/") and ("hero" in f):
        note = "原地替换（人数修正·4 人形 + 1 匹白马）"
    elif f.startswith("assets/promo/output/"):
        note = "flyer A4 正面 PNG 重渲染（静态快照同步新图）"
    elif f.startswith("scripts/"):
        note = "本批工具/产物"
    elif f.startswith("docs/"):
        note = "登记面"
    rows.append("| %s | W1005 | %s |" % (f, note))

SPEC = {
    "batch": "W1005",
    "date": "2026-10-29",
    "title": "W1005 hero 水墨图人数修正（取经五人组·4 人形 + 1 匹白马）· 两张原地替换 + flyer A4 快照重渲染",
    "desc": "hero 水墨图人数修正（4 人形 + 1 匹白马）两张原地替换，flyer A4 快照重渲染",
    "head_entry": "2026-10-29（W1005 hero 水墨图人数修正）",
    "head_sentence": "hero 水墨图人数修正：两张原地替换为 4 人形 + 1 匹白马，flyer A4 快照重渲染",
    "changelog_body": BODY,
    "milestone_block": ("- **W1005 hero 水墨图人数修正批**：两张原地替换（4 人形 + 1 匹白马）+ flyer A4 快照重渲染"
                        " + 代并行 W1004 结清 5 处版本面欠账"),
    "agents_note": ("2026-10-29（W1005）用户指出 hero 图有七个人、不合西游记；查档发现错源自 W852 批。"
                    "两张改为四人加一白马，flyer A4 静态快照用 Playwright 重渲染。代并行 W1004 结清五处版本面欠账。"),
    "file_index_rows": rows,
}

p = os.path.join(OUT, "_w1005_spec.json")
with open(p, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(SPEC, ensure_ascii=False, indent=1))
print("spec 写出 · %s · 文件清单 %d 项 · file_index %d 行 · desc 无「·」=%s · agents_note %d 字"
      % (os.path.basename(p), len(FILES), len(rows), "·" not in SPEC["desc"], len(SPEC["agents_note"])))
