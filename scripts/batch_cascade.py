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
_root = os.path.realpath(ROOT)



def load(path):
    _root = os.path.realpath(ROOT)
    _real = os.path.realpath(os.path.join(ROOT, path))
    if not (_real == _root or _real.startswith(_root + os.sep)):
        raise SystemExit("path escapes project root: %s" % path)
    s = open(_real, encoding="utf-8", newline="").read()
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
    # W557 修复：仅淘汰最老块本身。旧实现从块起点整段删到指针，当块区漂移到
    # 「零、当前阻塞」HEAD 句之前时会连正文一起吞掉（W557 dry-run 实证）。
    # 终点取（下一块起点 / 下一引用行 / 下一标题行 / 指针 / 块行行尾）中最先出现者。
    cands = [eidx]
    for _pat in ("\n- **", "\n>", "\n#", "\n"):
        _j = s.find(_pat, bm_start + 1)
        if _j != -1:
            cands.append(_j)
    _end = min(cands)
    s = s[:bm_start] + s[_end:]
    s = s.replace(f"> 历史概要（W{oldest_w} 及更早）的详细记录见",
                  f"> 历史概要（W{new_w} 及更早）的详细记录见", 1)
    hs = re.search(r"当前 HEAD = v[\d.]+ W\d+（[^）]*；详见 CHANGELOG）", s)
    assert hs, "未找到当前 HEAD 句"
    s = s[:hs.start()] + "当前 HEAD = {} {}（{}；详见 CHANGELOG）".format(ver, batch, spec["head_sentence"]) + s[hs.end():]
    # W560 修复：尾链 prepend 必须锚定文末行（旧实现 s.replace("最后更新：", ..., 1) 命中的是
    # 头链首处 → 头链 entry 双写「E；E·」，W556/W557/W558 三批实证）。改用 rfind 定位文末行。
    tail_idx = s.rfind("最后更新：")
    assert tail_idx != -1, "未找到文末「最后更新」历史链"
    if entry + "；" not in s[tail_idx : tail_idx + len(entry) + 2]:
        s = s[:tail_idx] + "最后更新：" + entry + "；" + s[tail_idx + len("最后更新："):]
    # W560: 尾链维持 ≤3 条（交接文档维护契约②）
    tline_end = s.find(nl, tail_idx)
    tline = s[tail_idx:tline_end]
    tparts = re.split("；(?=20\\d{2}-)", tline)
    if len(tparts) > 3:
        s = s[:tail_idx] + "；".join(tparts[:3]) + s[tline_end:]
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
    rows = nl.join(["## {} {}（{}·{}）".format(batch, re.sub(r"\W\d+ ", "", spec["title"].split(" — ")[0].split("（")[0]), date, ver),
                    "", "| 文件 | W | 说明 |", "|---|---|---|"] + spec["file_index_rows"] + ["", ""])
    pend.append((p, s.replace(mm.group(0), rows + mm.group(0), 1), nl))

    # ---------- 落盘 ----------
    if not args.apply:
        print(f"[DRY-RUN] 9 个面断言与改写全部通过：{batch}（规则 {new_rule}）。加 --apply 落盘。")
        return 0
    # W560 修复：newline 恒为 ""——旧实现对 CRLF 文件传 newline=nl，io 层把 content 中
    # 既有 \r\n 的每个 \n 再翻译一次 → \r 翻倍（实测累计至 4×CR，全页视觉损毁）。
    for path, content, _nl in pend:
        _real = os.path.realpath(os.path.join(ROOT, path))
        if not (_real == _root or _real.startswith(_root + os.sep)):
            raise SystemExit("path escapes project root: %s" % path)
        with open(_real, "w", encoding="utf-8", newline="") as f:
            f.write(content)

    # ---------- 写后自检 + 自愈（W560：并入 _cascade_fix.py 与 jiacheck 要点） ----------
    selfcheck = []
    for path, _, _nl in pend:
        _real = os.path.realpath(os.path.join(ROOT, path))
        data = open(_real, "rb").read()
        if b"\r\r" in data:
            out = []
            for line in data.split(b"\n"):
                out.append(line.rstrip(b"\r") + b"\r" if line else b"")
            data = b"\n".join(out)
            with open(_real, "wb") as f:
                f.write(data)
            selfcheck.append(f"{path}: CR 串已收敛（自愈）")
        if path == "交接文档.md":
            txt = data.decode("utf-8")
            sep = "\r\n" if "\r\n" in txt else "\n"
            head_line = txt.split(sep)[6]
            head_entries = re.findall(r"v2\.3\.1\d\d (W\d+)", head_line)
            if not head_entries or head_entries[0] != batch:
                selfcheck.append(f"交接文档: 头链首条非 {batch}（{head_entries[:3]}）——需人工核查")
            tail_txt = txt[txt.rfind("最后更新："):]
            tail_entries = re.findall(r"v2\.3\.1\d\d (W\d+)", tail_txt)
            if tail_txt.count("2026-") > 3 or not tail_entries or tail_entries[0] != batch:
                selfcheck.append(f"交接文档: 尾链异常（{tail_entries[:3]}）——需人工核查")
            if "## 九、使用说明" not in txt:
                selfcheck.append("交接文档: 「九、使用说明」段缺失——需人工核查")
    for line in selfcheck:
        print("[SELF-CHECK]", line)
    print(f"[APPLY] 级联完成：{batch} / {new_rule}，共 {len(pend)} 个文件；写后自检 {'发现 %d 项' % len(selfcheck) if selfcheck else '全部通过'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# spec 字段说明：
# batch/version/date/title/desc/head_entry/head_sentence/changelog_body/milestone_block/agents_note/file_index_rows
# 注意：head_entry 为交接文档头尾链条目全文（以 ） 结尾，不带分隔符）；
#       changelog_body 以两个换行开头；milestone_block 多行以 \n 分隔（脚本会按文件行尾归一）。
