# -*- coding: utf-8 -*-
"""_w1049_make_spec.py — W1049 批 spec 生成（第五轮 og 扩量）

口径：spec 结构与 W1043 批**同构**（batch/date/title/desc/head_entry/head_sentence/
changelog_body/milestone_block/agents_note/file_index_rows），但**文案按本批实测口径重写**
——不派生上一批脚本（上一批文案块耦合过深·派生易漏改·坑表 E-37 同族教训），
本脚本直接按「本批事实」生成·数据与文案同源·改一处即改两处。

文件清单来源：git 工作树三态实测（staged + unstaged + untracked）⇒ 与实际改动面一致。

用法：py -3 archive/scripts/batches/w10xx/_w1049_make_spec.py
"""
import io
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
OUT = os.path.join(REPO, "scripts", "output")
SPEC = os.path.join(OUT, "_w1049_spec.json")

BATCH = "W1049"
DATE = "2026-10-31"
TITLE = "W1049 回次 og:image 全覆盖批·第五轮（12 张线描立像/场面）"
DESC = ("回次 og:image 全覆盖第五轮：十二张线描立像与场面接入缺口回目页并换专属 og:image")
HEAD_ENTRY = "2026-10-31（W1049 回次 og:image 全覆盖第五轮 12 张）"
HEAD_SENTENCE = DESC

AGENTS_NOTE = ("2026-10-31（W1049）回目页补 og:image，第五轮 12 张。缺口实读 43 回通用 og，"
               "已出 124 slug 全表避重；本批 12 回全部新增题图。")

MILESTONE = ("- **W1049 回次 og:image 全覆盖批·第五轮**（12 张线描立像/场面）：\n"
             "  - 缺口实读 43 回通用 og（用户口径 42 回·差 1 回系旧探针漏查 banner）· 已出母版 124 张 / 唯一 slug 124 个 · 全表避重\n"
             "  - 母版段两变体：立像段逐字 249 字符（6 张）+ 场面段仅改 3 处（6 张）\n"
             "  - 12 主体逐项实读命中 2–16 次（金池长老/文殊菩萨/鹿力大仙/火德星君/女儿国国王/灭法国王 +\n"
             "    四大天王/高太公/银角大王/十代阎君/红鳞大蟒/谛听）· 选材判据含负样本自证 5/5 可证伪\n"
             "  - 3 张重出（97/103/107）⇒ 机器判据全目录 136 张 FAIL 0 · 落位 12 回题图\n"
             "  - 配图覆盖 55 → 67 回 · 通用 og 缺口 43 → 31 回 · 坑表 +3 条（E-54~E-56）")

BODY_HEAD = (
    "\n\n\n\n> **来源**：用户 2026-10-30「先做这两个再继续剩余 42 回扩量」＋ 2026-10-31"
    "「剩余 42 回 og 扩量开始」＋ 同日规模裁决「12 张一批·延续四轮节奏」⇒ 本批为第五轮（W1049）。\n"
    ">\n"
    "> **基线实读**（非引用旧批报告）：已落位专属 og-image **55 回** + 保留既有 card-* 专属 **2 回**"
    "（ch019/ch031）+ 通用 og 缺口 **43 回**；已出母版 **124 张 / 唯一 slug 124 个**。\n"
    ">\n"
    "> **口径订正**：用户表述「剩余 42 回」与实读 **43 回**差 1 回——根因是旧探针"
    "（`_w990_og_gap.py`）只查 `chapter-plate`/`chapter-scene` 未查 `chapter-banner`，"
    "把 ch019/ch031 两回误计为缺口；本批以实读 43 回为准（og 形态分布 55+43+2=100 与"
    "「无任何配图 43 = 通用 og-cover 43」交叉自洽）。\n"
    ">\n"
    "> - **文件**："
)

BODY_POINTS = (
    "**本批要点**：① **缺口口径实读 + 交叉自洽**——通用 og 缺口 **43 回**（用户口径 42 回·"
    "差 1 回已定位到旧探针漏查 `chapter-banner`·两探针差集 = {019, 031}）；"
    "② **12 主体逐项实读证据**——每个主体在该回正文命中 2–16 次（金池长老 10 / 文殊菩萨 10 / "
    "鹿力大仙 6 / 火德星君 5 / 女儿国国王 4 / 灭法国王 10 / 四大天王 7 / 高太公 9 / 银角大王 2 / "
    "十代阎君 3 / 红鳞大蟒 3 / 谛听 16）；选材判据五项全绿 + **负样本自证 5/5 可证伪**"
    "（并修判据自身 key 形态 bug：`basename[2:5]` 与 `[:5]` 混用致目标集全体判空假红）；"
    "③ **母版段两变体**——立像段逐字复用 249 字符（6 张）、场面段仅改 3 处（6 张）；"
    "④ **3 张重出**——全目录机器判据首跑 3 张 FAIL（97 J4=0.0298 擦线 / 103 J3=0.1861 / "
    "107 J3=0.2026）⇒ 目视取证确认 103/107 为真缺陷（铠甲鳞纹密排、山石渲染笔触）、"
    "97 为构图过疏 ⇒ 改 prompt 强化禁项后重出；**97 号二版因「稀疏/留白」措辞与母版段"
    "「占幅五成」打架反使 J4 更低（0.0258）⇒ 三版删掉留白措辞改为显式要求放大占幅 ⇒ J4=0.0375**；"
    "⑤ **og 幂等派生陷阱**——重出母版后重跑落位输出 12 张 og 全部「SKIP 已在位」"
    "⇒ 社交卡仍是旧图 ⇒ 新增 `_w1049_reissue_og.py` 按白名单清退后重新派生；"
    "⑥ **出图接口单批上限 10 张**（12 条直接被拒）⇒ 改 3–5 张/批（4/4 批全成）；"
    "⑦ **坑表 +3 条**（E-54 出图接口批次上限 / E-55 母版段约束不住密排纹理与渲染笔触 / "
    "E-56 og 派生幂等 SKIP 与「下载器复活旧件」同族）。\n\n"
)

BODY_VERIFY = (
    "**验证**：全目录机器判据 **136 张 · FAIL 0**（含 3 张重出后复验）· 落位验收 **0 FAIL**"
    "（12 回题图 + og:image + alt + 暗色规则 + 未覆盖页零回归）· "
    "配图覆盖 **55 → 67 回** · 通用 og 缺口 **43 → 31 回** · "
    "12 个 og 版 1200×630 且 39.6–141.9KB（实测 40566–145292 B·全部 ≤300KB）· 坑表 **140 → 143 条**（计数链四处一致）· "
    "全量门禁见收官提交。\n\n"
)

BODY_STATUS = (
    "> - **状态**：已收官（12 张落地·12 回新增题图·母版族 124 → 136 张·"
    "既有 124 张母版与站点版零改动·3 张重出后机器判据全绿·待用户目视）\n"
)


def _git(*args):
    out = subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO] + list(args),
                         capture_output=True).stdout
    return out.decode("utf-8", "replace")


def _collect_files():
    """本批真实改动面（git 工作树三态实测）。

    W1049 盲审 P0-1/P0-3 修正：
      ① 必须**剔除 W1050 批的六件在途件与其级联面**（用户 2026-10-31 令「摘出勿卷入」）
         —— spec 过宽会让 W1006 的 `--expect-spec` 守卫失效（W1050 的工作会被吸收进本批提交）。
      ② spec 必须与**真实文件集**一致（staged ⊆ spec 且 spec 无幽灵引用）。
    """
    W1050_EXCLUDE = {
        # 用户点名的六件
        "scripts/verify_delivery.py",
        "scripts/check_doc_sync.py",
        "docs/agent/gates.md",
        "scripts/output/_w1050_spec.json",
        "scripts/output/_cascade_files_W1050.txt",
        # 注：**当前态面不在排除表**——本批级联刷新了它们（版本行 → W1049·
        #   workflows 里程碑区间 / CITATION version / 四页脚 / 项目说明 / 三面 /
        #   HANDOVER 头链与里程碑 / stats 三件与 STRUCTURE 的 C5b 标记面），
        #   ⇒ 它们是**本批的合法改动**·必须入 spec。
        #   （原按「W1050 批的级联面」排除它们是错的：本批停泊了 W1050 的版本行，
        #     再由本批自己的级联写入 W1049 ⇒ 归属本批。）
        #   仅以下「纯 W1050 遗产」面仍排除（归档索引登记·属 W1050 批重放范围）：
        #   注：AGENTS-ARCHIVE.md 亦属本批（AGENTS 脚注滚动迁入 W1042 条目·本批级联）⇒ 不排除。
        "archive/docs/CHANGELOG-ARCHIVE.md",
        "archive/docs/file-index-ARCHIVE.md",
        "archive/docs/W批次编号对账表-ARCHIVE.md",
        "scripts/output/tools-inventory.md",
        # 门禁缓存产物（W1049 盲审 P2-2：非本批产物·不入 spec）
        "scripts/output/_vermilion_solid_cache.json",
    }
    files = []

    def add(p):
        p = p.strip().strip('"')
        if p and not p.startswith("tmpe/") and p not in files and p not in W1050_EXCLUDE:
            files.append(p)

    for ln in _git("diff", "--cached", "--name-only").splitlines():
        add(ln)
    for ln in _git("diff", "--name-only").splitlines():
        add(ln)
    for ln in _git("status", "--porcelain").splitlines():
        if ln.startswith("?? "):
            add(ln[3:])
    alive = [p for p in files
             if os.path.exists(os.path.join(REPO, p.replace("/", os.sep)))]
    dropped = [p for p in files if p not in alive]
    if dropped:
        print("[DEBUG] 剔除磁盘已不存在路径 %d 项：%s" % (len(dropped), dropped))
    return sorted(alive)


def note_of(f):
    if f.startswith("archive/scripts/batches/w10xx/_w1049"):
        return "本批工具脚本（归档批次区）"
    if f.startswith("scripts/output/_w1049"):
        return "本批出图批次与结果件"
    if f.startswith("assets/promo/plate-set/raw/round18"):
        return "出图原件（12 份·含 3 张重出）"
    if f.startswith("assets/promo/plate-set/plate-line-"):
        return "新增母版（1200×1600）"
    if f.startswith("assets/promo/plate-set/preview-"):
        return "拼图预览（含本批 12 张）"
    if f.startswith("site/static/images/og-plate-line"):
        return "专属 og:image（1200×630）"
    if f.startswith("site/static/images/plate-line"):
        return "站点版（母版裁切·只裁上部留白）"
    if f.startswith("site/reader/"):
        return "缺口回目页接入题图 + 换专属 og:image"
    if f.startswith("docs/11-方案报告/计划方案/"):
        return "方案报告（执行前计划件）"
    if f.startswith("docs/11-方案报告/"):
        return "方案报告（索引/架构方案）"
    if f == "docs/agent/pitfalls.md":
        return "坑表（+3 条·出图接口/密排纹理/og 幂等派生）"
    if f.startswith("docs/00-"):
        return "台账（认领行与收官回填）"
    if f.startswith("scripts/output/"):
        return "登记面产物（索引/统计/工具清单）"
    return "本批新增/修改"


def main() -> int:
    files = _collect_files()
    print("[DEBUG] files=%d" % len(files))

    rows = ["| %s | %s | %s |" % (f, BATCH, note_of(f)) for f in files]
    body = BODY_HEAD + "、".join(files) + "。\n\n" + BODY_POINTS + BODY_VERIFY + BODY_STATUS

    spec = {
        "batch": BATCH,
        "date": DATE,
        "title": TITLE,
        "desc": DESC,
        "head_entry": HEAD_ENTRY,
        "head_sentence": HEAD_SENTENCE,
        "changelog_body": body,
        "milestone_block": MILESTONE,
        "agents_note": AGENTS_NOTE,
        "file_index_rows": rows,
    }
    with io.open(SPEC, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(spec, ensure_ascii=False, indent=1))
    print("写出 %s · 文件 %d 项" % (os.path.relpath(SPEC, REPO).replace("\\", "/"), len(files)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
