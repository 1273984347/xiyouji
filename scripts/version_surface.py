"""version_surface.py — 版本面（跨文件字面量）幂等推进器（W1114）。

**为什么存在**：级联工具 batch_cascade.py 把「版本面字面量推进」与「CHANGELOG / file-index 段插入」
耦合在同一条命令里，且该命令**非幂等**（段已存在即断言失败）⇒ 落段后若只想「把现役批次号字面量
推进到目标号」（rebase / 回退 / 返工场景），无路可走。

本模块把「版本面」独立出来：

* 只做**跨文件字面量**推进：README 抬头 / STRUCTURE 头部 / 项目说明头部与列表行 / CITATION.cff /
  workflows README 区间 / 交接文档「当前 HEAD」句与「一、当前进度」标题；
* **幂等**：已是目标态 ⇒ 零变化（可重复跑）；
* **fail-closed**：正则在该文件里找不到锚点 ⇒ 报错（不静默跳过·防正则失配被当成「已是目标」）；
* **不碰段插入**（CHANGELOG 段 / file-index 段 / 里程碑块 / 页脚链 ⇒ 属 batch_cascade 职责）。

用法：
    python scripts/version_surface.py --batch W1114 --date 2026-11-03 --desc "<描述>" [--check|--apply]
    python scripts/version_surface.py --self-test
"""

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WINPATH = chr(96) + "D:" + chr(92) + "xiyouji" + chr(96)  # workflows README 里的本机路径（反斜杠需转义）


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def save(rel, text):
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8", newline="") as f:
        f.write(text)


def _sub_once(text, pattern, repl, label, flags=re.M, tail_anchor=None):
    """替换一次并判定幂等。

    返回 (新文本, 是否变化)：
    * 有变化 ⇒ 真改了；
    * 无变化且正则能匹配 ⇒ 该处文本本就等于替换结果 ⇒ **幂等命中**（已是目标态）；
    * 无变化且正则匹配不到 ⇒ **正则失配** ⇒ fail-closed（防失配被当成「已是目标」而静默放过）。
    """
    if callable(repl):
        out = re.sub(pattern, repl, text, count=1, flags=flags)
    else:
        # 字面替换：repl 里的反斜杠/\d 不得被当成 replacement 模板转义（W717 同源教训）
        out = re.sub(pattern, lambda _m: repl, text, count=1, flags=flags)
    if out != text:
        if out.count("\n") != text.count("\n"):
            raise AssertionError("%s 替换吞行（行锚定失效）" % label)
        return out, True
    if re.search(pattern, text, flags=flags):
        if tail_anchor is not None and out.count(tail_anchor) != 1:
            raise AssertionError("%s 尾部锚点异常（描述含右括号或标题重复）" % label)
        return text, False
    raise AssertionError("%s 未找到锚点（正则失配·fail-closed）" % label)


# ---------------------------------------------------------------------------
# W1117 追加：批次级单调守卫（不回退）
#
# 病根：版本面表达的是「**现在是什么**」⇒ 只能指向**最高号**批次。而落段批号
# 与合并次序可以不一致（并行会话乱序合并的真实场景：对方 W1118 先合入 main，
# 我方 W1117 后落段）⇒ 若按「把版本面推进到本批号」的语义执行，会把 README /
# STRUCTURE / 项目说明 / CITATION / workflows README / HANDOVER / 编号规则段
# **全部回退**到低号 ⇒ 抹掉已合并批次的现役标记，且与 backfill_changelog.py
# 明文的「当前态六面该指向最高号·被一批历史段拉回去是错的」相悖。
#
# 正解：推进器改为**单调**——目标批号 ≤ 该文件当前批号 ⇒ 该文件**零变化**
# （不回退·也不 fail-closed·该面本就不该由低号批改写）。
# 与 backfill_changelog.py 的「编号规则只升不降」同一语义（单一事实源精神）。
# ---------------------------------------------------------------------------


def _bnum(batch):
    """批号 → 整数（'W1117' → 1117）。"""
    s = str(batch)
    return int(s[1:] if s.upper().startswith("W") else s)


# 各文件「现役批号」所在位（只匹配现役位置·不扫正文历史引用）。
_CURRENT_BATCH_PATTERNS = {
    "CHANGELOG.md": [r"（W001-W(?P<w>\d+)）"],
    "README.md": [r"当前批次 W(?P<w>\d+)（"],
    "STRUCTURE.md": [r"当前批次：W(?P<w>\d+)（"],
    "docs/00-导读/项目说明.md": [r"当前批次 W(?P<w>\d+)（"],
    "CITATION.cff": [r'(?m)^version:\s*"W(?P<w>\d+)"'],
    ".github/workflows/README.md": [r"W450-W(?P<w>\d+)"],
    "HANDOVER.md": [r"当前 HEAD = W(?P<w>\d+)",
                    r"## 一、当前进度（(?:v[\d.]+ )?W(?P<w>\d+) "],
}


def _current_batch(rel, text):
    """返回该文件现役批号（取各现役位上的最大值）；取不到 ⇒ None（该文件无版本面）。"""
    pats = _CURRENT_BATCH_PATTERNS.get(rel)
    if not pats:
        return None
    nums = []
    for pat in pats:
        for m in re.finditer(pat, text):
            g = m.group("w")
            if g is None:
                continue
            nums.append(int(g))
    return max(nums) if nums else None


def advance_readme(text, batch, date, desc):
    pat = r"> \*\*当前(?:版本 v[\d.]+|批次 W\d+)（[^）]*）\*\*：[ \t]*(?:v[\d.]+[ \t]+)?(?:W\d+[ \t]+)?[^\n\r·]*·A1-A6"
    return _sub_once(text, pat, "> **当前批次 %s（%s）**：%s·A1-A6" % (batch, date, desc), "README 版本行")


def advance_structure(text, batch, date, desc):
    pat = r"> 当前(?:版本：v[\d.]+|批次：W\d+)（[^）]*）—[ \t]*(?:v[\d.]+[ \t]+)?(?:W\d+[ \t]+)?[^\n\r—]*—[ \t]*A1-A6"
    return _sub_once(text, pat, "> 当前批次：%s（%s）— %s—A1-A6" % (batch, date, desc), "STRUCTURE 版本行")


def advance_project_note_head(text, batch, date, desc):
    pat = r"> 当前(?:版本 v[\d.]+|批次 W\d+)（[^）]*）：[ \t]*(?:v[\d.]+[ \t]+)?(?:W\d+[ \t]+)?[^\n\r·]*·详细变更见"
    return _sub_once(text, pat, "> 当前批次 %s（%s）：%s·详细变更见" % (batch, date, desc), "项目说明头部版本行")


def advance_project_note_item(text, batch, date, desc):
    pat = r"(\*\*当前(?:版本|批次)\*\*：)(?:v[\d.]+|W\d+)（[^）]*）—[ \t]*(?:v[\d.]+[ \t]+)?(?:W\d+[ \t]+)?[^\n\r]*"
    tail = "%s（%s）— %s" % (batch, date, desc)
    return _sub_once(text, pat, lambda m: m.group(1) + tail, "项目说明「当前版本」列表行")


def advance_citation(text, batch, date):
    out, c1 = _sub_once(text, r'(?m)^version:[ \t]*"[^"]+"', 'version: "%s"' % batch, "CITATION version")
    out, c2 = _sub_once(out, r'(?m)^date-released:[ \t]*"[^"]+"', 'date-released: "%s"' % date, "CITATION date-released")
    return out, (c1 or c2)


def advance_workflows_readme(text, batch):
    """workflows README 的两处「W450-W####」区间。

    ⚠️ 区间里的批次号是**纯数字**（batch 去掉前导 W）——cascade 原实现用 ctx.new_w（纯数字）·
    若直接塞带 W 的 batch 会产出「W450-WW1114」双 W（自测实证）。
    """
    num = batch[1:] if batch.startswith("W") else batch
    pat_head = (r"→ W450-W\d+\*\* — 西游记解读项目（" + re.escape(WINPATH)
                + r"，(?:v[\d.]+\s+)?W\d+）的 GitHub Actions 工作流层。")
    out, c1 = _sub_once(text, pat_head,
                        "→ W450-W%s** — 西游记解读项目（%s，%s）的 GitHub Actions 工作流层。" % (num, WINPATH, batch),
                        "workflows README 头部区间")
    out, c2 = _sub_once(out, r"> \*\*W450-W\d+\*\*：verify 门禁体系扩展",
                        "> **W450-W%s**：verify 门禁体系扩展" % num,
                        "workflows README 门禁体系区间")
    return out, (c1 or c2)


def advance_changelog_rule(text, batch):
    """CHANGELOG 编号规则段上限「（W001-W####）」推进到本批号（幂等）。

    W1117：原由级联工具在插段时一并改写（与段插入耦合·属非幂等面）⇒ 本批把它明确划为
    **版本面字面量**（跨文件字面量面）·级联改为调用本函数（单一事实源·只引用不复制）。
    """
    num = batch[1:] if batch.startswith("W") else batch
    # W1117 单调守卫：编号规则段上限语义是「已用到的最大 W 号」⇒ 只升不降
    # （与 backfill_changelog.py 的同名规则一致）⇒ 当前值 ≥ 目标号 ⇒ 零变化。
    m = re.search(r"（W001-W(\d+)）", text)
    if m and int(m.group(1)) >= _bnum(batch):
        return text, False
    return _sub_once(text, r"（W001-W\d+）", "（W001-W%s）" % num, "CHANGELOG 编号规则段上限")


def advance_handover_current_head(text, batch, head_sentence):
    # W1117：[^）]* 会匹配换行 ⇒ 改 [^\n\r）]*（行锚定）
    pat = r"当前 HEAD = (?:v[\d.]+ )?W\d+（[^\n\r）]*；详见 CHANGELOG）"
    out, changed = _sub_once(text, pat, "当前 HEAD = %s（%s；详见 CHANGELOG）" % (batch, head_sentence),
                             "交接文档「当前 HEAD」句",
                             tail_anchor="；详见 CHANGELOG）")
    return out, changed


def advance_handover_progress(text, batch, desc):
    # W1117 修正则过窄：原用 [^；]* 匹配 desc（隐含假设 desc 不含分号）⇒ desc 一旦含
    # 「；」，第一次推进后文本出现两个「；」⇒ 第二次推进即失配 ⇒ fail-closed（非幂等·贵方实证）。
    # ⇒ 改为 [^\n\r）]*（行内 · 容许分号 · 不跨行 · 遇右括号止）
    pat = r"## 一、当前进度（(?:v[\d.]+ )?W\d+ [^\n\r）]*；更早批次详见 CHANGELOG\.md）"
    out, changed = _sub_once(text, pat, "## 一、当前进度（%s %s；更早批次详见 CHANGELOG.md）" % (batch, desc),
                             "交接文档「一、当前进度」标题",
                             tail_anchor="；更早批次详见 CHANGELOG.md）")
    return out, changed


POINTS = [
    ("CHANGELOG.md", advance_changelog_rule),
    ("README.md", advance_readme),
    ("STRUCTURE.md", advance_structure),
    ("docs/00-导读/项目说明.md", advance_project_note_head),
    ("docs/00-导读/项目说明.md", advance_project_note_item),
    ("CITATION.cff", advance_citation),
    (".github/workflows/README.md", advance_workflows_readme),
    ("HANDOVER.md", advance_handover_current_head),
    ("HANDOVER.md", advance_handover_progress),
]


def advance_text(text, rel, batch, date, desc, head_sentence):
    """把**已读入的文本**里属于 rel 的版本面字面量推进到目标态（纯函数·不碰 IO）。

    **W1114 修正（判据可驱动性）**：本函数**不读文件**——读文件由调用方（级联工具）用
    自己的 load() 完成 ⇒ 判据 scripts/check_cascade_line_anchor.py 才能通过 monkeypatch
    级联的 load() 注入**合成样本**（若本模块自己读盘，判据就会读到磁盘真实文件 ⇒
    合成样本驱动机制失效 ⇒ 判据整体误判）。⇒ 返回 (新文本, 是否变化)。
    """
    # W1117 单调守卫：版本面只表达「现在是什么」⇒ 指向最高号批次。
    # 目标批号 ≤ 该文件现役批号 ⇒ 该文件零变化（不回退·低号批不改写现役面）。
    cur = _current_batch(rel, text)
    if cur is not None and cur > _bnum(batch):
        return text, False
    out = text
    changed = False
    for target, fn in POINTS:
        if target != rel:
            continue
        if fn is advance_changelog_rule:
            out, c = fn(out, batch)
        elif fn is advance_citation:
            out, c = fn(out, batch, date)
        elif fn is advance_workflows_readme:
            out, c = fn(out, batch)
        elif fn is advance_handover_current_head:
            out, c = fn(out, batch, head_sentence)
        elif fn is advance_handover_progress:
            out, c = fn(out, batch, desc)
        else:
            out, c = fn(out, batch, date, desc)
        changed = changed or c
    return out, changed


def advance_file(rel, batch, date, desc, head_sentence):
    """读盘 + 推进某文件的全部版本面点（便捷包装；**级联工具请用 advance_text** 以保判据可驱动）。"""
    return advance_text(load(rel), rel, batch, date, desc, head_sentence)


def advance_all(batch, date, desc, head_sentence, check=False):
    """推进全部版本面字面量；返回 [(相对路径, 是否变化)]。

    check=True => 只算不落盘（返回变化清单）。
    """
    results = []
    for rel, _fn in POINTS:
        if rel in [r for r, _ in results]:
            continue
        out, changed = advance_file(rel, batch, date, desc, head_sentence)
        if changed and not check:
            save(rel, out)
        results.append((rel, changed))
    return results


def self_test():
    """自测：幂等性 + 失配 fail-closed。"""
    b, d = "W9001", "2099-01-01"
    desc = "自测描述"
    src = {
        "README.md": "> **当前批次 W8000（2000-01-01）**：旧描述·A1-A6<!--x-->\n",
        "STRUCTURE.md": "> 当前批次：W8000（2000-01-01）— 旧描述—A1-A6\n",
        "docs/00-导读/项目说明.md": (
            "> 当前批次 W8000（2000-01-01）：旧描述·详细变更见 CHANGELOG\n"
            "- **当前版本**：W8000（2000-01-01）— 旧描述\n"),
        "CITATION.cff": 'version: "W8000" # 注释\ndate-released: "2000-01-01"\n',
        ".github/workflows/README.md": (
            "> x → W450-W8000** — 西游记解读项目（%s，W8000）的 GitHub Actions 工作流层。\n"
            "> **W450-W8000**：verify 门禁体系扩展\n" % WINPATH),
        "HANDOVER.md": (
            "xx 当前 HEAD = W8000（旧描述；详见 CHANGELOG）。\n"
            "## 一、当前进度（W8000 旧描述；更早批次详见 CHANGELOG.md）\n"),
    }
    ok = True
    for rel, fn in POINTS:
        text = src[rel]
        if fn is advance_citation:
            out, _ = fn(text, b, d)
            out2, changed2 = fn(out, b, d)
        elif fn is advance_workflows_readme:
            out, _ = fn(text, b)
            out2, changed2 = fn(out, b)
        elif fn is advance_handover_current_head:
            out, _ = fn(text, b, desc)
            out2, changed2 = fn(out, b, desc)
        elif fn is advance_handover_progress:
            out, _ = fn(text, b, desc)
            out2, changed2 = fn(out, b, desc)
        else:
            out, _ = fn(text, b, d, desc)
            out2, changed2 = fn(out, b, d, desc)
        if out2 != out or changed2:
            print("FAIL  %s 幂等失败（第二次执行有变化）" % rel)
            ok = False
    # 负样本：锚点缺失 ⇒ fail-closed
    try:
        _sub_once("无锚点的文本\n", r"> 当前批次 W\d+", "x", "负样本")
        print("FAIL  负样本未 fail-closed")
        ok = False
    except AssertionError:
        pass
    print("version_surface 自测：%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="版本面（跨文件字面量）幂等推进器")
    ap.add_argument("--batch", help="目标批次号（如 W1114）")
    ap.add_argument("--date", help="目标日期（YYYY-MM-DD）")
    ap.add_argument("--desc", help="批次描述（不含 ·；—）")
    ap.add_argument("--head-sentence", help="交接文档「当前 HEAD」句用的描述")
    ap.add_argument("--check", action="store_true", help="只算不落盘")
    ap.add_argument("--apply", action="store_true", help="落盘")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not (a.batch and a.date and a.desc):
        ap.error("须提供 --batch / --date / --desc")
    head_sentence = a.head_sentence or a.desc
    results = advance_all(a.batch, a.date, a.desc, head_sentence, check=not a.apply)
    for rel, changed in results:
        print("[%s] %s" % ("版本面推进" if changed else "已是目标态", rel))
    return 0


if __name__ == "__main__":
    sys.exit(main())
