"""W963：台账认领行追加 + 版本面/登记面同步（W961 → W963·差异化推广批）。

让号留痕：W962 已被并行会话「归档分段批」占用（touches 含 archive/docs/CHANGELOG-ARCHIVE.md 等）⇒ 本批 W963。
按文件聚合·逐文件读改写一次（W957 批验证结构）· 断言命中数（fail-closed）· 幂等·字节级保行尾。
"""
import io
import os

ROOT = r"D:\xiyouji"

# ---------------- ① 台账认领行 ----------------
LD = os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md")
with io.open(LD, "rb") as f:
    b = f.read()
nl = b"\r\n" if b"\r\n" in b else b"\n"
ROW = ("| W963 | GSAP 动效差异化推广批（用户 2026-10-26 裁决「按页型差异化推广」·**让号**：W962 被并行会话「归档分段批」占用 ⇒ 本批 W963）："
       "① **推广口径**——入口层 8 页接线（7 个 reader 体裁 hub 页：reader/index + themes-hub + themes/people/essays/culture/poetry 五个 index，"
       "编排单元 = `.reader-idx a` 索引条目；+ site/guide.html 编排 `.path-card`）·**cards 模式**新增；"
       "单页增量 **215–238 B**（合计 +1,863 B）；"
       "② **载体增改**——`site/static/js/motion-gsap.js` 新增 **cards 模式**（容器内匹配 `data-gsap-target`（缺省 .card）的元素按序进场·"
       "stagger 自适应封顶序列总时长 ≈1.2 s）；**sections 模式单元收窄为 h2**（初版含 details 折叠块⇒ 折叠块默认折叠、"
       "进场时不可见 ⇒ 属无效动效，折叠块展开编排移交 fold 模式）；"
       "③ **本批不做项（透明留痕）**——site/curated.html（2 个 .curated-grid 分属 3 个 `.section.reveal-in`·"
       "提到共同父会与既有 reveal-in 机制交叠、逐个加则单页 269 B 超 250 B 上限⇒ 留专项）；"
       "**内容层** reader 622 页正文 / data 88 页 / en 138 页（暂不铺 sections）；index.html（已有 intro）；"
       "dashboard / dukou-engine / 404 / rum-viewer / visit-viewer（重交互或工具页）；"
       "④ **验收入口复用**——`_w957_motion_probe.py` 加 `--pages` 参数（默认清单不变）⇒ 新接入页按 48 组实跑验证 | "
       "—（认领占号·本行提交后回填 hash） | —（待回填） | **在途**（认领占号·8 页已接线·待实跑与提交） | "
       "主会话 2026-10-26（GSAP 动效差异化推广批） | "
       "site/reader/index.html · site/reader/themes-hub.html · site/reader/themes/index.html · "
       "site/reader/people/index.html · site/reader/essays/index.html · site/reader/culture/index.html · "
       "site/reader/poetry/index.html · site/guide.html · site/static/js/motion-gsap.js |")
assert b.count(b"| W963 |") == 0
with io.open(LD, "wb") as f:
    f.write(b + ROW.encode("utf-8") + nl)
print("台账 W963 认领行已追加")

# ---------------- ② 版本面 + 登记面同步 ----------------
CHANGELOG_SEG = """### W963（2026-10-26）：GSAP 动效差异化推广批（入口层 8 页 + cards 模式 + sections 单元收窄）

> **来源**：用户 2026-10-26 裁决「按页型差异化推广」（滚动叙事 / 入场编排 / 微交互 / 现有动画体检四类全都要·载体 = site/ 静态站·先出计划再施工）。
>
> - **文件**：site/static/js/motion-gsap.js、site/reader/index.html、site/reader/themes-hub.html、site/reader/themes/index.html、site/reader/people/index.html、site/reader/essays/index.html、site/reader/culture/index.html、site/reader/poetry/index.html、site/guide.html、scripts/_w962_wire_entry.py、scripts/_w957_motion_probe.py

**推广口径（差异化·不一刀切）**：**入口层 8 页**接线 cards 模式——7 个 reader 体裁 hub 页（编排单元 = `.reader-idx a` 索引条目）+ site/guide.html（`.path-card`）；单页增量 **215–238 B**（合计 +1,863 B）。**内容层** reader 622 页正文 / data 88 页 / en 138 页**暂不铺 sections**；index.html 已有 intro 不动；dashboard / dukou-engine / 404 / rum-viewer / visit-viewer 不动（重交互或工具页，动效收益低且干扰风险高）。

**载体增改**：① 新增 **cards 模式**（容器内匹配 `data-gsap-target`（缺省 `.card`）的元素按序进场·stagger 自适应使序列总时长封顶 ≈1.2 s）；② **sections 模式单元收窄为 h2**——初版含 details 折叠块，但折叠块默认折叠、进场时不可见 ⇒ 属**无效动效**，折叠块的展开编排移交 fold 模式（职责分离）。

**本批不做项（透明留痕）**：site/curated.html——其 2 个 `.curated-grid` 分属 3 个 `.section.reveal-in` 区块，属性提到共同父会与既有 reveal-in 进场机制交叠、逐个 grid 加属性则单页增量 269 B 超 250 B 上限 ⇒ 留专项批处理。

**验收入口复用**：`_w957_motion_probe.py` 加 `--pages` 参数（默认清单不变）⇒ 新接入页按 8 页 × 3 视口 × 2 动效偏好态 = 48 组实跑验证（判据沿用 W957 口径：pageerror = 0 · 编排单元残留初始态 = 0 · RM 态载体执行数 = 0）。

**让号留痕**：W962 已被并行会话「归档分段批」占用 ⇒ 本批 **W963**。

**状态**：**已收官**（差异化推广·入口层落地；**内容层推广与 curated 专项待用户裁决范围**）

"""

HANDOVER_ITEM = (
    "- **W963 GSAP 动效差异化推广批**：用户裁决「按页型差异化推广」⇒ 入口层 **8 页**接线 cards 模式"
    "（7 个 reader 体裁 hub 页编排 `.reader-idx a` 索引条目 + site/guide.html 编排 `.path-card`）·"
    "单页增量 215–238 B（合计 +1,863 B）；载体新增 **cards 模式**（`data-gsap-target` 可配置 + stagger 自适应封顶 ≈1.2 s）"
    "并把 **sections 单元收窄为 h2**（折叠块默认折叠 ⇒ 进场属无效动效·展开编排移交 fold 模式）；"
    "**内容层** reader 622 页 / data 88 页 / en 138 页暂不铺 sections；curated.html 留专项（与既有 reveal-in 机制交叠）；"
    "探针加 `--pages` 参数复用；**让号**：W962 被并行会话占用 ⇒ W963。\n"
)

STRUCTURE_ITEM = (
    "- **W963（2026-10-26）**：GSAP 动效差异化推广批（入口层 8 页 + cards 模式）"
    "<!--doc-sync:exempt-->\n"
)

FILE_INDEX_SEG = """## W963 GSAP 动效差异化推广批（入口层 8 页 + cards 模式）（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| site/static/js/motion-gsap.js | W963 | 修改：新增 cards 模式（data-gsap-target 可配置 + stagger 自适应）+ sections 单元收窄为 h2 |
| site/reader/index.html | W963 | 修改：入口层接线（cards 模式·目标 .reader-idx a·增量 229 B） |
| site/reader/themes-hub.html | W963 | 修改：入口层接线（增量 229 B） |
| site/reader/themes/index.html | W963 | 修改：入口层接线（增量 238 B） |
| site/reader/people/index.html | W963 | 修改：入口层接线（增量 238 B） |
| site/reader/essays/index.html | W963 | 修改：入口层接线（增量 238 B） |
| site/reader/culture/index.html | W963 | 修改：入口层接线（增量 238 B） |
| site/reader/poetry/index.html | W963 | 修改：入口层接线（增量 238 B） |
| site/guide.html | W963 | 修改：入口层接线（cards 模式·目标 .path-card·增量 215 B） |
| scripts/_w962_wire_entry.py | W963 | 新增：入口层接线器（字节级·断言命中数·幂等·单页增量上限 250 B） |
| scripts/_w957_motion_probe.py | W963 | 修改：加 --pages 参数（默认清单不变）以便按新接入面实跑 |
| docs/00-导读/W批次编号对账表.md | W963 | 登记：W963 认领行（让号留痕）+ 收官回填 |
| HANDOVER.md | W963 | 同步：一、当前进度增 W963 条目 + 最后更新链前置 + 当前 HEAD |
| CHANGELOG.md | W963 | 新增：W963 版段（四件套） |
| scripts/output/file-index.md | W963 | 登记：W963 段（本段） |

"""

PLAN = {
    "CHANGELOG.md": {
        "replaces": [("编号规则段上限 W001-W961 → W001-W963",
                      "W### ID（W001-W961）", "W### ID（W001-W963）", 1)],
        "inserts": [("新增 W963 版段（插在 W961 段之前）",
                      "### W961（2026-10-26）：", CHANGELOG_SEG, 1, "before")],
    },
    "README.md": {
        "replaces": [("当前批次行 W961 → W963",
                      "> **当前批次 W961（2026-10-26）**：GSAP 写法机检挂 verify_delivery 第 50 槽 + F9 裸 ease 假阳性订正<!--doc-sync:exempt-->",
                      "> **当前批次 W963（2026-10-26）**：GSAP 动效差异化推广批（入口层 8 页 + cards 模式）<!--doc-sync:exempt-->", 1)],
        "inserts": [],
    },
    "docs/00-导读/项目说明.md": {
        "replaces": [("当前批次行 W961 → W963",
                      "> 当前批次 W961（2026-10-26）：GSAP 写法机检挂 verify_delivery 第 50 槽 + F9 裸 ease 假阳性订正·详细变更见",
                      "> 当前批次 W963（2026-10-26）：GSAP 动效差异化推广批（入口层 8 页 + cards 模式）·详细变更见", 1)],
        "inserts": [],
    },
    "CITATION.cff": {
        "replaces": [("批次号形态 version W961 → W963", 'version: "W961"', 'version: "W963"', 1)],
        "inserts": [],
    },
    ".github/workflows/README.md": {
        "replaces": [("头部版本链上限 W450-W961 → W450-W963", "→ W450-W961**", "→ W450-W963**", 1),
                     ("头部项目标识 W961 → W963", "（`D:\\xiyouji`，W961）", "（`D:\\xiyouji`，W963）", 1)],
        "inserts": [],
    },
    "HANDOVER.md": {
        "replaces": [("「一、当前进度」标题 W961 → W963",
                      "## 一、当前进度（W961 GSAP 写法机检挂槽批 + F9 假阳性订正批；更早批次详见 CHANGELOG.md）",
                      "## 一、当前进度（W963 GSAP 动效差异化推广批；更早批次详见 CHANGELOG.md）", 1),
                     ("「最后更新」链首 W961 → W963（两处同起句）",
                      "最后更新：2026-10-26（W961 GSAP 写法机检挂槽批 + F9 假阳性订正批）",
                      "最后更新：2026-10-26（W963 GSAP 动效差异化推广批）", 2),
                     ("「当前 HEAD」W961 → W963",
                      "当前 HEAD = W961（GSAP 写法机检挂 verify_delivery 第 50 槽 + 显式豁免机制 + F9 裸 ease 假阳性订正（7 处表述））",
                      "当前 HEAD = W963（GSAP 动效差异化推广批：入口层 8 页 cards 模式 + 载体新增 cards 模式 + sections 单元收窄为 h2）", 1)],
        "inserts": [("一、当前进度增 W963 条目（接在标题行之后）",
                      "## 一、当前进度（W963 GSAP 动效差异化推广批；更早批次详见 CHANGELOG.md）",
                      HANDOVER_ITEM, 1, "after")],
    },
    "STRUCTURE.md": {
        "replaces": [],
        "inserts": [("里程碑增 W963 条目（前置）", "- **W961（2026-10-26）**：", STRUCTURE_ITEM, 1, "before")],
    },
    "scripts/output/file-index.md": {
        "replaces": [],
        "inserts": [("新增 W963 反向索引段（插在 W961 段之前·倒序）",
                      "## W961 GSAP 写法机检挂槽批", FILE_INDEX_SEG, 1, "before")],
    },
}


def read(rel):
    path = os.path.join(ROOT, rel.replace("/", os.sep))
    with open(path, encoding="utf-8", newline="") as f:
        raw = f.read()
    if "\r\n" in raw:
        nl = "\r\n"
        bare = any(ln == "\n" for ln in raw.split("\r\n"))
    elif "\n" in raw:
        nl = "\n"
        bare = False
    else:
        nl = "\r"
        bare = False
    if bare:
        raise SystemExit("混合行尾：%s" % rel)
    return raw, nl


for rel, spec in PLAN.items():
    raw, nl = read(rel)
    orig = raw
    for desc, old, new, expect in spec["replaces"]:
        n = raw.count(old)
        if n == 0 and raw.count(new) > 0:
            print("SKIP   %s：%s（已应用）" % (rel, desc))
            continue
        if n != expect:
            raise SystemExit("ABORT  %s：命中 %d ≠ 期望 %d（%s）" % (rel, n, expect, desc))
        raw = raw.replace(old, new)
        print("REPL   %s：%s" % (rel, desc))
    for desc, anchor, block, expect, mode in spec["inserts"]:
        n = raw.count(anchor)
        if n != expect:
            raise SystemExit("ABORT  %s：锚点命中 %d ≠ 期望 %d（%s）" % (rel, n, expect, desc))
        if block.split("\n")[0] in raw:
            print("SKIP   %s：%s（已存在）" % (rel, desc))
            continue
        blk = block.replace("\n", nl)
        raw = raw.replace(anchor, (anchor + nl + blk) if mode == "after" else (blk + anchor), 1)
        print("INS    %s：%s" % (rel, desc))
    if raw != orig:
        with open(os.path.join(ROOT, rel.replace("/", os.sep)), "w", encoding="utf-8", newline="") as f:
            f.write(raw)
        print("OK     %s：%d B → %d B" % (rel, len(orig), len(raw)))
print("版本面同步完成：%d 个面" % len(PLAN))
