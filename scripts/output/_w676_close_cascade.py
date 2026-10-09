#!/usr/bin/env python3
"""W676 收官级联（一次性·W679 手工先例复刻）——偏差两处：
① batch/new_w = W676 硬编码（工具的 new_w=现役+1=691 与对账表认领 W676 不符：
   W676-W678 系方案 V1.7 批次四~六预留号、已在历史段登记不能让路，对账表为唯一取号权威）；
② 四页脚步骤——tag-cloud/cross-time-danmaku 已由本批页脚 sweep 盖为 v2.3.282·W676，
   改为断言在位不再前置追加（防双写）；index/dukou-engine 仍走链首前置。
其余复刻 batch_cascade.py 现行全部锚点与断言。两阶段：--apply 才落盘，写后自检。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_root = os.path.realpath(ROOT)
BATCH, NEW_W = "W676", 676


def load(path):
    real = os.path.realpath(os.path.join(ROOT, path))
    if not (real == _root or real.startswith(_root + os.sep)):
        raise SystemExit("path escapes project root: %s" % path)
    s = open(real, encoding="utf-8", newline="").read()
    return s, ("\r\n" if "\r\n" in s else "\n")


def save(path, content):
    real = os.path.realpath(os.path.join(ROOT, path))
    with open(real, "w", encoding="utf-8", newline="") as f:
        f.write(content)


def drop_block(s, bm_start, nl):
    seg = s[bm_start:].split(nl)
    j = 1
    while j < len(seg) and seg[j].startswith("  - "):
        j += 1
    return s[:bm_start] + s[bm_start + len(nl.join(seg[:j]) + nl):]


def main():
    apply_ = "--apply" in sys.argv
    spec = json.load(open(os.path.join(ROOT, "scripts", "output", "_w676_cascade_spec.json"), encoding="utf-8"))
    ver, date, desc, batch = spec["version"], spec["date"], spec["desc"], BATCH
    entry, title = spec["head_entry"], spec["title"]
    assert entry.endswith("）"), "head_entry 须以闭合括号结尾"
    assert "（" not in spec["head_sentence"] and "）" not in spec["head_sentence"], "head_sentence 禁全角括号"
    pend = []

    # ---------- CHANGELOG（偏差①：W676 领衔） ----------
    p = "CHANGELOG.md"
    s, nl = load(p)
    m = re.search(r"^### (v[\d.]+（[^）]*）：W(\d+))", s, re.M)
    assert m, "CHANGELOG 未找到现役段"
    cur_anchor, cur_w = m.group(0), int(m.group(2))
    assert cur_w == 690, "现役段预期 W690（取证基线）"
    assert ("### " + ver) not in s, ver + " 段已存在"
    old_rule, new_rule = "（W001-W%d）" % cur_w, "（W001-W%d）" % NEW_W
    assert s.count(old_rule) == 1 and s.count(cur_anchor) == 1
    new_title = f"### {ver}（{date}）：{title}"
    out = s.replace(cur_anchor, new_title + spec["changelog_body"] + nl + cur_anchor, 1)
    out = out.replace(old_rule, new_rule, 1)
    assert out.count(new_title) == 1 and out.count(new_rule) == 1
    pend.append((p, out))

    # ---------- README / STRUCTURE / 项目说明 ----------
    p = "README.md"
    s, nl = load(p)
    out = re.sub(r"> \*\*当前版本 v[\d.]+（[^）]*）\*\*： W\d+ [^·]*·A1-A6",
                 "> **当前版本 %s（%s）**： %s %s ·A1-A6" % (ver, date, batch, desc), s, count=1)
    assert out != s, "README 版本行未变化"
    pend.append((p, out))

    p = "STRUCTURE.md"
    s, nl = load(p)
    out = re.sub(r"> 当前版本：v[\d.]+（[^）]*）— W\d+ [^—]*— A1-A6",
                 "> 当前版本：%s（%s）— %s %s — A1-A6" % (ver, date, batch, desc), s, count=1)
    assert out != s, "STRUCTURE 版本行未变化"
    pend.append((p, out))

    p = "docs/00-导读/项目说明.md"
    s, nl = load(p)
    out = re.sub(r"> 当前版本 v[\d.]+（[^）]*）：W\d+ [^·]*·详细变更见",
                 "> 当前版本 %s（%s）：%s %s ·详细变更见" % (ver, date, batch, desc), s, count=1)
    assert out != s, "项目说明头部版本行未变化"
    out2 = re.sub(r"(\*\*当前版本\*\*：)v[\d.]+（[^）]*）— W\d+ [^·]*",
                  lambda mm: mm.group(1) + "%s（%s）— %s %s" % (ver, date, batch, desc), out, count=1)
    pend.append((p, out2))

    # ---------- 交接文档 ----------
    p = "交接文档.md"
    s, nl = load(p)
    assert s.count("））；") == 0, "基线已存在双括号，先人工处理"
    s = s.replace("> 最后更新：", "> 最后更新：" + entry + "·", 1)
    h0 = s.find("> 最后更新：")
    h1 = s.find(nl, h0)
    head_line = s[h0:h1]
    entries = re.findall(r"·20\d{2}-\d{2}-\d{2}（", head_line)
    while len(entries) + 1 > 3:
        note_idx = head_line.find("·（W")
        assert note_idx != -1, "未找到历史注记锚点"
        oldest = head_line.rfind("·20", 0, note_idx)
        assert oldest != -1
        head_line = head_line[:oldest] + head_line[note_idx:]
        entries = re.findall(r"·20\d{2}-\d{2}-\d{2}（", head_line)
    s = s[:h0] + head_line + s[h1:]
    s = re.sub(r"；v[\d.]+ W\d+ 起生效）", "；%s %s 起生效）" % (ver, batch), s, count=1)
    s = re.sub(r"## 一、当前进度（v[\d.]+ W\d+ [^；]*；更早批次详见 CHANGELOG\.md）",
               "## 一、当前进度（%s %s + 前两批详见 CHANGELOG.md）" % (batch, desc), s, count=1)
    fb = re.search(r"- \*\*v[\d.]+ W\d+", s)
    assert fb, "未找到里程碑首块"
    at = s.rfind(nl, 0, fb.start()) + 1
    s = s[:at] + spec["milestone_block"].replace("\n", nl) + nl + s[at:]
    pm = re.search(r"> 历史概要（W(\d+) 及更早）的详细记录见", s)
    assert pm, "未找到历史概要指针"
    oldest_w = pm.group(1)
    blocks_all = list(re.finditer(r"- \*\*(v[\d.]+) (W\d+)[^*]*\*+：", s))
    tgt = [b for b in blocks_all if b.group(2) == "W" + oldest_w]
    if not tgt:
        raise AssertionError("未找到最老里程碑块 W%s；现存块 %s" % (oldest_w, [b.group(2) for b in blocks_all]))
    bm_start = tgt[0].start()
    eidx = s.find("> 历史概要（W%s 及更早）的详细记录见" % oldest_w, bm_start)
    assert eidx != -1
    s = drop_block(s, bm_start, nl)
    s = s.replace("> 历史概要（W%s 及更早）的详细记录见" % oldest_w,
                  "> 历史概要（W%d 及更早）的详细记录见" % NEW_W, 1)
    hs = re.search(r"当前 HEAD = v[\d.]+ W\d+（[^）]*；详见 CHANGELOG）", s)
    assert hs, "未找到当前 HEAD 句"
    s = s[:hs.start()] + "当前 HEAD = {} {}（{}；详见 CHANGELOG）".format(ver, batch, spec["head_sentence"]) + s[hs.end():]
    tail_idx = s.rfind("最后更新：")
    assert tail_idx != -1, "未找到文末「最后更新」历史链"
    if entry + "；" not in s[tail_idx: tail_idx + len(entry) + 2]:
        s = s[:tail_idx] + "最后更新：" + entry + "；" + s[tail_idx + len("最后更新："):]
    tline_end = s.find(nl, tail_idx)
    tline = s[tail_idx:tline_end]
    tparts = re.split("；(?=20\\d{2}-)", tline)
    if len(tparts) > 3:
        s = s[:tail_idx] + "；".join(tparts[:3]) + s[tline_end:]
    assert s.count("））；") == 0, "写入后出现双括号 ））；"
    pend.append((p, s))

    # ---------- workflows README ----------
    p = ".github/workflows/README.md"
    s, nl = load(p)
    BS = chr(92)
    winpath = "`D:" + BS + "xiyouji`"
    pat_wf = re.compile(r"→ W450-W\d+\*\* — 西游记解读项目（" + re.escape(winpath) + r"，v[\d.]+ W\d+）的 GitHub Actions 工作流层。")
    repl_wf = "→ W450-W%d** — 西游记解读项目（%s，%s %s）的 GitHub Actions 工作流层。" % (NEW_W, winpath, ver, batch)
    out = pat_wf.sub(lambda m: repl_wf, s, count=1)
    assert out != s, "workflows 头部未变化"
    out = re.sub(r"> \*\*W450-W\d+\*\*：verify 门禁体系扩展",
                 "> **W450-W%d**：verify 门禁体系扩展" % NEW_W, out, count=1)
    marker = "无 workflow 结构改动）。"
    assert out.count(marker) == 1, "里程碑尾标记出现 %d 次" % out.count(marker)
    out = out.replace(marker, "无 workflow 结构改动）+ W%d %s·无 workflow 结构改动）。" % (NEW_W, desc), 1)
    pend.append((p, out))

    # ---------- 页脚（偏差②：data 两页已被 sweep 盖戳只断言；index/dukou 前置） ----------
    for p in ["site/data/cross-time-danmaku.html", "site/data/tag-cloud.html"]:
        s, _ = load(p)
        assert ("%s · %s" % (ver, batch)) in s, p + " 页脚未见本批盖戳（sweep 缺失）"
    p = "site/index.html"
    s, _ = load(p)
    mm = re.search(r"v[\d.]+ · W\d+ [^<]*", s)
    assert mm, p + " 页脚未命中"
    pend.append((p, s.replace(mm.group(0), "%s · %s %s · " % (ver, batch, desc) + mm.group(0), 1)))
    p = "site/dukou-engine.html"
    s, _ = load(p)
    mm = re.search(r"v[\d.]+ W\d+ [^<]*", s)
    assert mm, p + " 页脚未命中"
    head_short = spec["head_sentence"].split("——")[0]
    pend.append((p, s.replace(mm.group(0), "%s %s %s（%s） · " % (ver, batch, desc, head_short) + mm.group(0), 1)))

    # ---------- AGENTS 脚注 ----------
    p = "AGENTS.md"
    s, nl = load(p)
    tail = "。如与上述权威文档冲突，以权威文档为准。*"
    assert s.count(tail) == 1, "AGENTS 脚注尾锚点异常"
    s = s.replace(tail, "；{}。如与上述权威文档冲突，以权威文档为准。*".format(spec["agents_note"]), 1)
    pend.append((p, s))

    # ---------- CITATION.cff ----------
    p = "CITATION.cff"
    s, nl = load(p)
    out = re.sub(r'(?m)^version:\s*"[^"]+"', 'version: "%s"' % ver.lstrip("v"), s, count=1)
    out = re.sub(r'(?m)^date-released:\s*"[^"]+"', 'date-released: "%s"' % date, out, count=1)
    assert out != s, "CITATION 版本/日期未变化"
    pend.append((p, out))

    # ---------- file-index ----------
    p = "scripts/output/file-index.md"
    s, nl = load(p)
    mm = re.search(r"## (W\d+) ", s)
    assert mm, "file-index 未找到最新段"
    derived = re.sub(r"\W\d+ ", "", title.split(" — ")[0].split("（")[0])
    rows = nl.join(["## %s %s（%s·%s）" % (batch, derived, date, ver),
                    "", "| 文件 | W | 说明 |", "|---|---|---|"] + spec["file_index_rows"] + ["", ""])
    pend.append((p, s.replace(mm.group(0), rows + mm.group(0), 1)))

    if not apply_:
        print("[DRY-RUN] 13 个面断言与改写全部通过：%s（规则 %s）。加 --apply 落盘。" % (BATCH, new_rule))
        return 0
    for path, content in pend:
        save(path, content)
    manifest = "scripts/output/_cascade_files_%s.txt" % BATCH
    with open(os.path.join(ROOT, manifest), "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(p2 for p2, _ in pend) + "\n")

    # ---------- 写后自检 ----------
    selfcheck = []
    for path, _ in pend:
        data = open(os.path.join(ROOT, path), "rb").read()
        if b"\r\r" in data:
            selfcheck.append("%s: CR 翻倍残留" % path)
        if path == "交接文档.md":
            txt = data.decode("utf-8")
            sep = "\r\n" if "\r\n" in txt else "\n"
            hl0 = txt.find("> 最后更新：")
            head_line = txt[hl0:txt.find(sep, hl0)] if hl0 != -1 else ""
            he = re.findall(r"（v[\d.]+ (W\d+)）", head_line)
            if not he or he[0] != BATCH:
                selfcheck.append("交接文档: 头链首条非 %s（%s）" % (BATCH, he[:3]))
            tail_txt = txt[txt.rfind("最后更新："):]
            te = re.findall(r"（v[\d.]+ (W\d+)）", tail_txt)
            if tail_txt.count("2026-") > 3 or not te or te[0] != BATCH:
                selfcheck.append("交接文档: 尾链异常（%s）" % te[:3])
            if "## 九、使用说明" not in txt:
                selfcheck.append("交接文档: 「九、使用说明」段缺失")
    for line in selfcheck:
        print("[SELF-CHECK]", line)
    print("[APPLY] 级联完成：%s / %s，共 %d 面；写后自检 %s" % (BATCH, new_rule, len(pend), "发现 %d 项" % len(selfcheck) if selfcheck else "全部通过"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
