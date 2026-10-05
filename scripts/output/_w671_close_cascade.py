#!/usr/bin/env python3
"""W666 收官级联（一次性·W663 手工先例复用·W665 chore 版段递延致 batch_cascade new_w=665 撞已认领号）——复刻 batch_cascade.py 全部锚点与断言，两处偏差：
① batch/new_w = W663 硬编码（D1 合并段：工具的 new_w=现役+1=659 与合并段领衔 W663 不符，
   659/660 已被未登记提交占用，对账表为唯一取号权威）；
② workflows README 追加句如实写本批 CI 加固（工具版恒追加「无 workflow 结构改动」与本批事实相反）。
两阶段：先全内存断言零落盘（--apply 才写），写后自检 CR 翻倍/头尾链/段缺失。
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_root = os.path.realpath(ROOT)
BATCH, NEW_W = "W671", 671


def load(path):
    real = os.path.realpath(os.path.join(ROOT, path))
    if not (real == _root or real.startswith(_root + os.sep)):
        raise SystemExit("path escapes project root: %s" % path)
    s = io.open(real, encoding="utf-8", newline="").read()
    return s, ("\r\n" if "\r\n" in s else "\n")


def save(path, content):
    real = os.path.realpath(os.path.join(ROOT, path))
    with io.open(real, "w", encoding="utf-8", newline="") as f:
        f.write(content)


def drop_block(s, bm_start, nl):
    seg = s[bm_start:].split(nl)
    j = 1
    while j < len(seg) and seg[j].startswith("  - "):
        j += 1
    return s[:bm_start] + s[bm_start + len(nl.join(seg[:j]) + nl):]


def main():
    apply_ = "--apply" in sys.argv
    spec = json.load(io.open(os.path.join(ROOT, "scripts", "output", "_w671_spec.json"), encoding="utf-8"))
    ver, date, desc = spec["version"], spec["date"], spec["desc"]
    entry, title = spec["head_entry"], spec["title"]
    assert entry.endswith("）"), "head_entry 须以闭合括号结尾"
    assert "（" not in spec["head_sentence"] and "）" not in spec["head_sentence"], "head_sentence 禁全角括号"
    pend = []

    # ---------- CHANGELOG（合并段领衔 W663） ----------
    p = "CHANGELOG.md"
    s, nl = load(p)
    m = re.search(r"^### (v[\d.]+（[^）]*）：W(\d+))", s, re.M)
    assert m, "CHANGELOG 未找到现役段"
    cur_anchor, cur_w = m.group(0), int(m.group(2))
    assert cur_w == 670, "现役段预期 W670（取证基线）"
    assert BATCH == "W" + str(NEW_W)
    assert ("### " + ver) not in s, ver + " 段已存在"
    old_rule, new_rule = "（W001-W%d）" % cur_w, "（W001-W%d）" % NEW_W
    assert s.count(old_rule) == 1 and s.count(cur_anchor) == 1
    new_title = "### {}（{}）：{}".format(ver, date, title)
    out = s.replace(cur_anchor, new_title + spec["changelog_body"] + nl + cur_anchor, 1)
    out = out.replace(old_rule, new_rule, 1)
    assert out.count(new_title) == 1 and out.count(new_rule) == 1
    pend.append((p, out))

    # ---------- README / STRUCTURE / 项目说明 ----------
    p = "README.md"
    s, nl = load(p)
    out = re.sub(r"> \*\*当前版本 v[\d.]+（[^）]*）\*\*： W\d+ [^·]*·A1-A6",
                 "> **当前版本 %s（%s）**： %s %s ·A1-A6" % (ver, date, BATCH, desc), s, count=1)
    assert out != s, "README 版本行未变化"
    pend.append((p, out))

    p = "STRUCTURE.md"
    s, nl = load(p)
    out = re.sub(r"> 当前版本：v[\d.]+（[^）]*）— W\d+ [^—]*— A1-A6",
                 "> 当前版本：%s（%s）— %s %s — A1-A6" % (ver, date, BATCH, desc), s, count=1)
    assert out != s, "STRUCTURE 版本行未变化"
    pend.append((p, out))

    p = "docs/00-导读/项目说明.md"
    s, nl = load(p)
    out = re.sub(r"> 当前版本 v[\d.]+（[^）]*）：W\d+ [^·]*·详细变更见",
                 "> 当前版本 %s（%s）：%s %s ·详细变更见" % (ver, date, BATCH, desc), s, count=1)
    assert out != s, "项目说明头部版本行未变化"
    out2 = re.sub(r"(\*\*当前版本\*\*：)v[\d.]+（[^）]*）— W\d+ [^·]*",
                  lambda mm: mm.group(1) + "%s（%s）— %s %s" % (ver, date, BATCH, desc), out, count=1)
    pend.append((p, out2))

    # ---------- 交接文档 ----------
    p = "交接文档.md"
    s, nl = load(p)
    assert s.count("））；") == 0, "基线已存在双括号"
    s = s.replace("> 最后更新：", "> 最后更新：" + entry + "·", 1)
    h0 = s.find("> 最后更新：")
    h1 = s.find(nl, h0)
    head_line = s[h0:h1]
    entries = re.findall(r"·20\d{2}-\d{2}-\d{2}（", head_line)
    while len(entries) + 1 > 3:
        note_idx = head_line.find("·（W")
        assert note_idx != -1, "未找到历史注记锚点"
        oldest = head_line.rfind("·20", 0, note_idx)
        head_line = head_line[:oldest] + head_line[note_idx:]
        entries = re.findall(r"·20\d{2}-\d{2}-\d{2}（", head_line)
    s = s[:h0] + head_line + s[h1:]
    s = re.sub(r"；v[\d.]+ W\d+ 起生效）", "；%s %s 起生效）" % (ver, BATCH), s, count=1)
    s = re.sub(r"## 一、当前进度（v[\d.]+ W\d+ [^；]*；更早批次详见 CHANGELOG\.md）",
               "## 一、当前进度（%s %s + 前两批详见 CHANGELOG.md）" % (BATCH, desc), s, count=1)
    fb = re.search(r"- \*\*v[\d.]+ W\d+", s)
    assert fb, "未找到里程碑首块"
    at = s.rfind(nl, 0, fb.start()) + 1
    s = s[:at] + spec["milestone_block"].replace("\n", nl) + nl + s[at:]
    pm = re.search(r"> 历史概要（W(\d+) 及更早）的详细记录见", s)
    assert pm, "未找到历史概要指针"
    oldest_w = pm.group(1)
    blocks_all = list(re.finditer(r"- \*\*(v[\d.]+) (W\d+)[^*]*\*+：", s))
    tgt = [b for b in blocks_all if b.group(2) == "W" + oldest_w]
    assert tgt, "未找到最老里程碑块 W%s；现存 %s" % (oldest_w, [b.group(2) for b in blocks_all])
    bm_start = tgt[0].start()
    eidx = s.find("> 历史概要（W%s 及更早）的详细记录见" % oldest_w, bm_start)
    assert eidx != -1
    s = drop_block(s, bm_start, nl)
    s = s.replace("> 历史概要（W%s 及更早）的详细记录见" % oldest_w,
                  "> 历史概要（W%d 及更早）的详细记录见" % NEW_W, 1)
    hs = re.search(r"当前 HEAD = v[\d.]+ W\d+（[^）]*；详见 CHANGELOG）", s)
    assert hs, "未找到当前 HEAD 句"
    s = s[:hs.start()] + "当前 HEAD = {} {}（{}；详见 CHANGELOG）".format(ver, BATCH, spec["head_sentence"]) + s[hs.end():]
    tail_idx = s.rfind("最后更新：")
    assert tail_idx != -1, "未找到文末最后更新链"
    if entry + "；" not in s[tail_idx: tail_idx + len(entry) + 2]:
        s = s[:tail_idx] + "最后更新：" + entry + "；" + s[tail_idx + len("最后更新："):]
    tline_end = s.find(nl, tail_idx)
    tparts = re.split("；(?=20\\d{2}-)", s[tail_idx:tline_end])
    if len(tparts) > 3:
        s = s[:tail_idx] + "；".join(tparts[:3]) + s[tline_end:]
    assert s.count("））；") == 0, "写入后双括号"
    pend.append((p, s))

    # ---------- workflows README（追加句如实写 CI 加固·保留滚动尾标记） ----------
    p = ".github/workflows/README.md"
    s, nl = load(p)
    BS = chr(92)
    winpath = "`D:" + BS + "xiyouji`"
    pat_wf = re.compile(r"→ W450-W\d+\*\* — 西游记解读项目（" + re.escape(winpath) + r"，v[\d.]+ W\d+）的 GitHub Actions 工作流层。")
    repl_wf = "→ W450-W%d** — 西游记解读项目（%s，%s %s）的 GitHub Actions 工作流层。" % (NEW_W, winpath, ver, BATCH)
    out = pat_wf.sub(lambda mm: repl_wf, s, count=1)
    assert out != s, "workflows 头部未变化"
    out = re.sub(r"> \*\*W450-W\d+\*\*：verify 门禁体系扩展",
                 "> **W450-W%d**：verify 门禁体系扩展" % NEW_W, out, count=1)
    marker = "无 workflow 结构改动）。"
    assert out.count(marker) == 1, "里程碑尾标记 %d 处" % out.count(marker)
    out = out.replace(marker, "无 workflow 结构改动）+ W%d %s·无 workflow 结构改动）。" % (NEW_W, desc), 1)
    pend.append((p, out))

    # ---------- 四页脚 ----------
    for p in ["site/index.html", "site/data/cross-time-danmaku.html", "site/data/tag-cloud.html"]:
        s, _ = load(p)
        mm = re.search(r"v[\d.]+ · W\d+ [^<]*", s)
        assert mm, p + " 页脚未命中"
        pend.append((p, s.replace(mm.group(0), "%s · %s %s · " % (ver, BATCH, desc) + mm.group(0), 1)))
    p = "site/dukou-engine.html"
    s, _ = load(p)
    mm = re.search(r"v[\d.]+ W\d+ [^<]*", s)
    assert mm, p + " 页脚未命中"
    head_short = spec["head_sentence"].split("——")[0]
    pend.append((p, s.replace(mm.group(0), "%s %s %s（%s） · " % (ver, BATCH, desc, head_short) + mm.group(0), 1)))

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
    rows = nl.join(["## %s 共享载体治理（%s·%s）" % (BATCH, date, ver),
                    "", "| 文件 | W | 说明 |", "|---|---|---|"] + spec["file_index_rows"] + ["", ""])
    pend.append((p, s.replace(mm.group(0), rows + mm.group(0), 1)))

    if not apply_:
        print("[DRY-RUN] 13 个面断言与改写全部通过：%s（规则 %s）。加 --apply 落盘。" % (BATCH, new_rule))
        return 0
    for path, content in pend:
        save(path, content)
    manifest = "scripts/output/_cascade_files_%s.txt" % BATCH
    with io.open(os.path.join(ROOT, manifest), "w", encoding="utf-8", newline="") as f:
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
            hl0 = txt.find("> 最后更新：")  # 里程碑块置顶后行号不固定（W665 同款修复）
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
