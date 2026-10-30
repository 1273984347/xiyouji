"""_w1044_make_spec.py — W1044 级联 spec 生成（结构照 w10xx/_w1018_make_spec.py·文案换本批）

文件行按 **git 现状全量**列出（不手抄）；desc/head_sentence 禁分隔符「· ; —」；
agents_note 以「阿拉伯日期（W###）」开头且 ≤120 字（W964 定形契约）。

输出：scripts/output/_w1044_spec.json
用法：py -3 archive/scripts/batches/w10xx/_w1044_make_spec.py
"""
from __future__ import annotations

import json
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
OUT = os.path.join(REPO, "scripts", "output")
SPEC = os.path.join(OUT, "_w1044_spec.json")

BATCH = "W1044"
DATE = "2026-10-31"
TITLE = "W1044 W1043 对抗审查发现处置批（og 卡切头根因 / 事实订正 / 判据补覆盖）"
DESC = "W1043 对抗审查发现处置：og 卡切头根因修复与 124 张重裁、slug 唯一数订正、下载脚本去 minimax 回退、判据补覆盖"
HEAD_ENTRY = "2026-10-31（W1044 W1043 对抗审查发现处置）"
HEAD_SENTENCE = "W1043 对抗审查发现处置：og 卡切头根因修复与 124 张重裁、slug 唯一数订正、下载脚本去 minimax 回退、判据补覆盖"
AGENTS_NOTE = ("2026-10-31（W1044）处置 W1043 审查发现：og 裁切上界改用独立墨顶，124 张全量重裁（"
               "存量 43 张同族切墨一并根治）；slug 唯一数 111→112；下载脚本删 minimax 回退。")
MILESTONE = ("- **W1044 W1043 对抗审查发现处置批**（P0 根治 + P1/P2 逐项）：\n"
             "  - og 裁切上界改 `min(subject_top, ink_top)`（独立全墨顶）⇒ 124 张 og 全量重裁，"
             "存量 43 张同族切墨一并根治\n"
             "  - `check_crop.py` 增 og 判据（尺寸/体积/顶边零墨 ≤12px）+ 负样本自证 3 例\n"
             "  - slug 唯一数 111→112（pick 正则大小写漏算）+ 91 号与存量 06 号同角色明示取舍\n"
             "  - 下载脚本删 `~/.minimax` 回退（铁律 16③）×3；AGENTS 分项纳入 C5e；计划件目录卫生判据")

BODY = (
    "\n\n\n\n> **来源**：用户 2026-10-31「好的，执行吧」——承接 W1043 段派发的**对抗式审查**"
    "（只读 subagent·距上次 W1022 已 20 批·按 docs/agent/adversarial-audit-prompt.md 模板）。"
    "审查报告：18 项通过 · P0×1 · P1×3 · P2×10 · P3×5；本批逐项处置（P3 登记后续）。\n"
    ">\n"
    "> **P0（假绿·用户可见）**：12 张 og 中 **5 张顶边切头**（85 如意真仙 / 90 乙救苦天尊 / "
    "91 九灵元圣与十八罗汉 / 95 地涌夫人 / 96 犀牛怪），而「裁切验算 124 张 · FAIL 0」只扫站点版、"
    "**og 无覆盖 ⇒ 假绿**。根因：`subject_band.body_mask` 排除 luma ≥ 90 的亮笔与赭金 ⇒ 白描冠顶/"
    "帽尖被系统性低估；且裁切与「不变量」共用同一个 top ⇒ 恒真、切头也测不出。\n"
    ">\n"
    "> **修法（根因修复·铁律 15）**：① `crop_band` 裁切上界改 `min(subject_top, ink_top)`"
    "（新增 `ink_top()`＝全墨连通簇顶·独立源）+ 居中分支上溢钳制（原实现是 no-op ⇒ 抛错）；"
    "② `check_crop.py` 增 og 判据：尺寸 1200×630 / 体积 ≤300KB / **顶边前 3 行墨 ≤12px**"
    "（纸面噪点容忍）+ `--self-test` 负样本（纯纸判绿、顶墨判红）；"
    "③ **124 张 og 全量重裁**（存量 43 张同族切墨一并根治）⇒ 全量 0 FAIL。\n"
    ">\n"
    "> **P1**：① slug 唯一数 **111 → 112**——`_w1043_pick.py` 正则 `[a-z0-9-]` 大小写敏感，"
    "漏掉唯一大写 slug `plate-line-06-jiuLingyuansheng`；91 号九灵元圣与存量 06 号为**同角色不同构图**"
    "（06 立像 / 91 群像）⇒ 明示取舍并在 HANDOVER / 计划件 / 台账订正；"
    "② 下载脚本删 `~/.minimax/` 路径回退（铁律 16③·W1013/W1018/W1043 三处，缺工具即 fail-closed）；"
    "③ 脚本事实订正：`_w1043_verify.py` docstring 66→43、`_w1043_prepare.py` 100→112、"
    "`_w1043_master.py` 场面清单与「二至十九人」口径。\n"
    ">\n"
    "> **P2**：① AGENTS §4.3 六主题分项 19→20 / 35→44，并把**分项**纳入 C5e 对拍"
    "（原只核总数 ⇒ 分项陈旧而门禁看不见）；② 第 48 槽补**计划方案目录卫生**判据"
    "（非 .md 扩展名 / 0 字节坏件即红）；③ `_w1043_make_spec.py` 说明列误标修正 + file-index 4 行订正；"
    "④ `_w1043_batch_a.json` 清理 93 号旧主体残留请求（10 → 9 条，与 gen 实产一致）。\n"
    ">\n"
    "> **P3 / 后续登记**：subject_band 与 check_crop 尚未接入 `verify_delivery`（CI 侧缺 numpy/scipy 依赖·"
    "见 requirements.txt）⇒ 下一批评估接线与环境声明；验收脚本 ⑥ 项冗余、stage CSS 插入死代码留后续清理；"
    "「裁切依据＝判据依据 ⇒ 不变量恒真」教训（E-47 候选）待下一批入坑表"
    "（并行 W1045 在途改 pitfalls.md·同文件串行）。\n"
    ">\n"
)


def _git(*args):
    out = subprocess.run(["git", "-c", "core.quotepath=false", "-C", REPO] + list(args),
                         capture_output=True).stdout
    return out.decode("utf-8", "replace")


def _collect_files():
    files = []

    def add(p):
        p = p.strip().strip('"')
        if p and not p.startswith("tmpe/") and p not in files:
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
    return sorted(alive)


def main() -> int:
    files = _collect_files()
    print("[DEBUG] files=%d" % len(files))

    def note_of(f):
        if f.startswith("site/static/images/og-"):
            return "og 卡重裁（独立墨顶·顶边零墨）"
        if f.startswith("scripts/subject_band.py"):
            return "裁切上界改独立墨顶 + 居中分支上溢钳制"
        if f.startswith("scripts/check_crop.py"):
            return "og 判据（尺寸/体积/顶边零墨）+ 负样本自证"
        if f.startswith("scripts/check_doc_sync.py"):
            return "C5e 增 AGENTS 六主题分项对拍"
        if f.startswith("scripts/check_plan_template.py"):
            return "第 48 槽增计划件目录卫生判据"
        if f.startswith("scripts/output/"):
            return "本批 spec / 索引链产物"
        if f.startswith("archive/scripts/batches/w10xx/"):
            return "本批脚本与 W1043 报告脚本订正"
        if f.startswith("docs/11-方案报告/计划方案/"):
            return "执行前计划件（事实订正）"
        if f.startswith("docs/"):
            return "登记面（报告/台账/索引）"
        return "本批修改"

    rows = ["| %s | W1044 | %s |" % (f, note_of(f)) for f in files]
    body = BODY + "> - **文件**：" + "、".join(files) + "。\n\n"
    body += ("**验证**：`check_crop.py --self-test` **3 例**（纯纸 2 判绿 + 顶墨 1 判红）· "
             "站点版 **124 张 FAIL 0** · og **124 张 FAIL 0** · `_w1043_verify.py` **0 FAIL** · "
             "`check_doc_sync.py` 自测 **33 项** · 第 48 门禁自测 **9/9** · 全量门禁见收官提交。\n\n")
    body += ("> - **状态**：已收官（P0 根治·124 张 og 重裁·P1×3/P2×4 处置·P3 登记后续）\n")

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
    open(SPEC, "w", encoding="utf-8", newline="\n").write(json.dumps(spec, ensure_ascii=False, indent=1))
    print("spec 写出 · %s · 文件清单 %d 项 · file_index %d 行 · agents_note %d 字"
          % (os.path.basename(SPEC), len(files), len(rows), len(AGENTS_NOTE)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
