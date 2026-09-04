#!/usr/bin/env python3
"""batch_cascade.py — W 批次文档级联常驻脚本（W542 新建·AGENTS §4.3 三新规④配套）。

用法：
  python scripts/batch_cascade.py --spec <spec.json>             # dry-run：全部断言跑通但不写盘
  python scripts/batch_cascade.py --spec <spec.json> --apply     # 断言全过后统一落盘

两阶段设计：第一阶段在内存中对全部 9 个面做断言与改写，任何锚点失配立即中止（零落盘）；
第二阶段仅在 --apply 时统一写入。写入后自检交接文档无 `））；` 双括号。

spec 字段见文末说明（JSON）。
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path):
    s = open(os.path.join(ROOT, path), encoding="utf-8", newline="").read()
    return s, ("\r\n" if "\r\n" in s else "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    spec = json.load(open(args.spec, encoding="utf-8"))
    batch, ver, date = spec["batch"], spec["version"], spec["date"]
    desc = spec["desc"]
    entry = spec["head_entry"]
    assert entry.endswith("）"), "head_entry 必须以闭合括号结尾"
    pend = []  # (path, content, nl)

    # ---------- CHANGELOG ----------
    p = "CHANGELOG.md"
    s, nl = load(p)
    m = re.search(r"^### (v[\d.]+（[^）]*）：W(\d+))", s, re.M)
    assert m, "CHANGELOG 未找到现役段"
    cur_anchor, cur_w = m.group(0), int(m.group(2))  # group(0) 含 ### 前缀，替换时保持段标题完整
    new_w = cur_w + 1
    assert batch == "W" + str(new_w), f"批次号应为 W{new_w}"
    assert ("### " + ver) not in s, ver + " 段已存在"
    old_rule, new_rule = f"（W001-W{cur_w}）", f"（W001-W{new_w}）"
    assert s.count(old_rule) == 1 and s.count(cur_anchor) == 1
    new_title = "### {}（{}）：{}".format(ver, date, spec["title"])
    out = s.replace(cur_anchor, new_title + spec["changelog_body"] + nl + cur_anchor, 1)
    out = out.replace(old_rule, new_rule, 1)
    assert out.count(new_title) == 1 and out.count(new_rule) == 1
    pend.append((p, out, nl))

    # ---------- README / STRUCTURE / 项目说明 ----------
    p = "README.md"
    s, nl = load(p)
    out = re.sub(r"> \*\*当前版本 v[\d.]+（[^）]*）\*\*： W\d+ [^·]*·A1-A6",
                 f"> **当前版本 {ver}（{date}）**： {batch} {desc} ·A1-A6", s, count=1)
    assert out != s, "README 版本行未变化"
    pend.append((p, out, nl))

    p = "STRUCTURE.md"
    s, nl = load(p)
    out = re.sub(r"> 当前版本：v[\d.]+（[^）]*）— W\d+ [^—]*— A1-A6",
                 f"> 当前版本：{ver}（{date}）— {batch} {desc} — A1-A6", s, count=1)
    assert out != s, "STRUCTURE 版本行未变化"
    pend.append((p, out, nl))

    p = "docs/00-导读/项目说明.md"
    s, nl = load(p)
    out = re.sub(r"> 当前版本 v[\d.]+（[^）]*）：W\d+ [^·]*·详细变更见",
                 f"> 当前版本 {ver}（{date}）：{batch} {desc} ·详细变更见", s, count=1)
    assert out != s, "项目说明头部版本行未变化"
    out2 = re.sub(r"(\*\*当前版本\*\*：)v[\d.]+（[^）]*）— W\d+ [^·]*",
                  rf"\g<1>{ver}（{date}）— {batch} {desc}", out, count=1)
    pend.append((p, out2, nl))

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
    s = re.sub(r"；v[\d.]+ W\d+ 起生效）", f"；{ver} {batch} 起生效）", s, count=1)
    s = re.sub(r"## 一、当前进度（v[\d.]+ W\d+ [^；]*；更早批次详见 CHANGELOG\.md）",
               f"## 一、当前进度（{batch} {desc} + 前两批详见 CHANGELOG.md）", s, count=1)
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
        raise AssertionError(f"未找到最老里程碑块 W{oldest_w}；现存块 {[b.group(2) for b in blocks_all]}")
    bm_start = tgt[0].start()
    eidx = s.find(f"> 历史概要（W{oldest_w} 及更早）的详细记录见", bm_start)
    assert eidx != -1
    s = s[:bm_start] + s[eidx:]
    s = s.replace(f"> 历史概要（W{oldest_w} 及更早）的详细记录见",
                  f"> 历史概要（W{new_w} 及更早）的详细记录见", 1)
    hs = re.search(r"当前 HEAD = v[\d.]+ W\d+（[^）]*；详见 CHANGELOG）", s)
    assert hs, "未找到当前 HEAD 句"
    s = s[:hs.start()] + "当前 HEAD = {} {}（{}；详见 CHANGELOG）".format(ver, batch, spec["head_sentence"]) + s[hs.end():]
    s = s.replace("最后更新：", "最后更新：" + entry + "；", 1)
    # 尾链（文末「最后更新」历史链）同步 prepend——头链已占第一个命中，此处取最后一个命中
    last_idx = s.rfind("最后更新：")
    if last_idx != -1 and entry + "；" not in s[last_idx:last_idx + len(entry) + 2]:
        s = s[:last_idx] + "最后更新：" + entry + "；" + s[last_idx + len("最后更新："):]
    assert s.count("））；") == 0, "写入后出现双括号 ））；"
    pend.append((p, s, nl))

    # ---------- workflows README ----------
    p = ".github/workflows/README.md"
    s, nl = load(p)
    BS = chr(92)
    winpath = "`d:" + BS + "1" + BS + "xiyouji`"
    pat_wf = re.compile(r"→ W450-W\d+\*\* — 西游记解读项目（" + re.escape(winpath) + r"，v[\d.]+ W\d+）的 GitHub Actions 工作流层。")
    repl_wf = f"→ W450-W{new_w}** — 西游记解读项目（{winpath}，{ver} {batch}）的 GitHub Actions 工作流层。"
    out = pat_wf.sub(lambda m: repl_wf, s, count=1)
    assert out != s, "workflows 头部未变化"
    out = re.sub(r"> \*\*W450-W\d+\*\*：verify 门禁体系扩展",
                 f"> **W450-W{new_w}**：verify 门禁体系扩展", out, count=1)
    marker = "无 workflow 结构改动）。"
    assert out.count(marker) == 1, f"里程碑尾标记出现 {out.count(marker)} 次"
    out = out.replace(marker, f"无 workflow 结构改动）+ {new_w} {desc}·无 workflow 结构改动）。", 1)
    pend.append((p, out, nl))

    # ---------- 四页脚 ----------
    for p in ["site/index.html", "site/data/cross-time-danmaku.html", "site/data/tag-cloud.html"]:
        s, _ = load(p)
        mm = re.search(r"v[\d.]+ · W\d+ [^<]*", s)
        assert mm, p + " 页脚未命中"
        pend.append((p, s.replace(mm.group(0), f"{ver} · {batch} {desc} · " + mm.group(0), 1), None))
    p = "site/dukou-engine.html"
    s, _ = load(p)
    mm = re.search(r"v[\d.]+ W\d+ [^<]*", s)
    assert mm, p + " 页脚未命中"
    head_short = spec["head_sentence"].split("——")[0]
    pend.append((p, s.replace(mm.group(0), f"{ver} {batch} {desc}（{head_short}） · " + mm.group(0), 1), None))

    # ---------- AGENTS 脚注 ----------
    p = "AGENTS.md"
    s, nl = load(p)
    tail = "。如与上述权威文档冲突，以权威文档为准。*"
    assert s.count(tail) == 1, "AGENTS 脚注尾锚点异常"
    s = s.replace(tail, "；{}。如与上述权威文档冲突，以权威文档为准。*".format(spec["agents_note"]), 1)
    pend.append((p, s, nl))

    # ---------- file-index ----------
    p = "scripts/output/file-index.md"
    s, nl = load(p)
    mm = re.search(r"## (W\d+) ", s)
    assert mm, "file-index 未找到最新段"
    rows = nl.join(["## {} {}（{}·{}）".format(batch, spec["title"].split(" — ")[0].split("（")[0], date, ver),
                    "", "| 文件 | W | 说明 |", "|---|---|---|"] + spec["file_index_rows"] + ["", ""])
    pend.append((p, s.replace(mm.group(0), rows + mm.group(0), 1), nl))

    # ---------- 落盘 ----------
    if not args.apply:
        print(f"[DRY-RUN] 9 个面断言与改写全部通过：{batch}（规则 {new_rule}）。加 --apply 落盘。")
        return 0
    for path, content, nl in pend:
        if nl is None:
            open(os.path.join(ROOT, path), "w", encoding="utf-8", newline="").write(content)
        else:
            open(os.path.join(ROOT, path), "w", encoding="utf-8", newline="").write(content)
    print(f"[APPLY] 级联完成：{batch} / {new_rule}，共 {len(pend)} 个文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# spec 字段说明：
# batch/version/date/title/desc/head_entry/head_sentence/changelog_body/milestone_block/agents_note/file_index_rows
# 注意：head_entry 为交接文档头尾链条目全文（以 ） 结尾，不带分隔符）；
#       changelog_body 以两个换行开头；milestone_block 多行以 \n 分隔（脚本会按文件行尾归一）。
