#!/usr/bin/env python3
"""W926 报告第二轮整理（R-11 / R-12 入清单后的排序、小节化、剩余数字订正）"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "docs" / "11-方案报告" / "审查与评审" / "站点交互流程审查复核报告-2026-10-25.md"

R11_ROW = (
    "| **R-11** | P3 | **10 个表单控件确实没有任何标签关联**（中英各 5 条） | "
    "读屏器只播报「选择框 / 文本框」，访客不知该选什么——弹幕页留言框、图谱页搜索框与图谱下拉、"
    "两个 range 滑块（滑块连 placeholder 都没有） | "
    "`cross-time-danmaku.html#user-message`、`graph-explorer.html#graphSel` 与 `#search`、"
    "`journey-map-interactive.html#routeSlider`、`narrative-rhythm-curve.html#chapterSlider`（中英各一份）·"
    "`aria-label` / `aria-labelledby` / `title` 全无 |\n"
)
R12_ROW = (
    "| **R-12** | P1 | `site/en/visualizations.html:1535` 的 `<a href=\"../data/\">site/data/</a>` "
    "指向**没有 `index.html` 的目录** | 线上（GitHub Pages）目录 URL **直接 404**；本地 `http.server` 会返回裸目录清单，"
    "访客看到的是文件列表，而链接文案承诺的是「curated index of the ~85 interactive visualizations」 | "
    "`site/data/` 无 `index.html`（实测）· 本地 http 响应 200 但 body 为目录清单（6,576 字节）· "
    "其余 4 条目录型链接的目标目录均有 `index.html`（浏览器可达） |\n"
)

NEW_SECTIONS = """### 2.7 R-11（P3）10 个表单控件无任何标签关联

**实测**　独立解析逐条复核「控件无 label 关联」清单：22 条中 **12 条是误报**（`<label>起因：<select id="filter-cause">` 这类隐式包裹对读屏器有效），**10 条确无任何标签关联**：

| 控件 | 所在页（中英各一份） | 现状 |
|:---|:---|:---|
| `#user-message` | `data/cross-time-danmaku.html` | 文本域，仅 placeholder |
| `#graphSel` / `#search` | `data/graph-explorer.html` | 下拉 + 搜索框，仅 placeholder |
| `#routeSlider` | `data/journey-map-interactive.html` | range 滑块，无 label 无 placeholder |
| `#chapterSlider` | `data/narrative-rhythm-curve.html` | range 滑块，无 label 无 placeholder |

**访客后果**　读屏器只播报「文本框 / 选择框 / 滑块」，不播报用途——视障访客无从知道"这个滑块调的是什么、这个框是做什么的"。

**建议**　① 文本域与输入框补 `aria-label`（或 `<label class="sr-only">`）；② 两个 range 滑块补 `aria-label` + `aria-valuetext`（如「回目范围」）；③ `graphSel` 补 `aria-label`；④ 补齐后可加门禁：「`input/select/textarea` 缺 label 关联即判红」——本次的 22 → 10 差值正是判据过粗，**门禁必须按真缺陷口径建**。

**验收判据**　① 10 个控件全部具备 label 关联（显式 `for=` / 隐式包裹 / `aria-label` 三选一）；② 复跑 `py -3 scripts/_w926_ia_audit.py` → `controls_without_label_count` = **0**（当前 22，其中 10 为真缺陷）；③ 屏幕阅读器逐控件播报含用途。

### 2.8 R-12（P1）`en/visualizations.html` 指向无 index 的目录 = 生产死链

**实测**　`site/en/visualizations.html:1535`：

```html
<a href="../data/">site/data/</a>
```

而 `site/data/` **没有 `index.html`**。本地 `py -3 -m http.server` 下该 URL 返回 **200 但 body 是裸目录清单**（6,576 字节，含 "Directory listing"）——访客看到的是一列文件名；**GitHub Pages 上目录 URL 直接 404**。

**访客后果**　英文站访客点 "site/data/" → 线上 404 死路；即便在能列出目录的环境下，看到的也是文件清单，而链接文案承诺的是「curated index of the ~85 interactive visualizations」。

**建议**　① 给 `site/data/` 建一个真正的索引页（列出 **87** 个内容页 + 分类入口），让该链接指向它；② 或把该链接改指向已有的可视化索引入口（看板 / 首页可视化卡片区）；③ 顺带把该页的「~85」与现役口径 **87** 对齐。

**验收判据**　① `site/data/index.html` 存在且列出全部 87 个内容页；② `en/visualizations.html` 的该链接指向它；③ 线上（Pages）该 URL 返回 200 且是可读索引页，而非 404 或目录清单。

"""

REPLACEMENTS = [
    # 节头计数 10 → 12
    ("### 0.2 问题清单（10 条 · 按影响用户程度排序）",
     "### 0.2 问题清单（12 条 · 按影响用户程度排序）"),
    # R-04 链接数订正 216 → 211（盲审 N2：四种计数口径均为 211）
    ("`reader/themes/index.html`（209 链）与 `reader/themes-hub.html`（216 链）",
     "`reader/themes/index.html`（209 链）与 `reader/themes-hub.html`（211 链）"),
    # R-12 从 P3 组尾移到 R-05 之后（P1 组内），R-11 留在 P3 组尾
    (R11_ROW + R12_ROW, R12_ROW + R11_ROW),
    # §2.3 正文 themes-hub 链数订正
    ("`site/reader/index.html:1396` 写的是 `<p><a href=\"themes-hub.html\">主题专题导航 hub（209 篇·按族分组）</a></p>`",
     "`site/reader/index.html:1396` 写的是 `<p><a href=\"themes-hub.html\">主题专题导航 hub（209 篇·按族分组）</a></p>`"),
    # 新增 §2.7 / §2.8 小节（插在 §3 之前）
    ("## 3. W858 旧报告 17 条 → 当前状态（闭环表）",
     NEW_SECTIONS + "## 3. W858 旧报告 17 条 → 当前状态（闭环表）"),
]


def main() -> int:
    apply = "--apply" in sys.argv
    text = REPORT.read_text(encoding="utf-8")
    failed = []
    for idx, (old, new) in enumerate(REPLACEMENTS, 1):
        n = text.count(old)
        if n != 1:
            failed.append((idx, n, old[:80]))
            continue
        text = text.replace(old, new, 1)
    if failed:
        print(f"[FAIL] {len(failed)} 条未唯一命中，未写入：")
        for idx, n, sn in failed:
            print(f"  #{idx} 命中 {n} 次 :: {sn}")
        return 1
    if apply:
        REPORT.write_text(text, encoding="utf-8")
        print(f"[APPLIED] {len(REPLACEMENTS)} 处 · 字节 {len(REPORT.read_bytes())}")
    else:
        print(f"[DRY-RUN] {len(REPLACEMENTS)} 处全部唯一命中")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
