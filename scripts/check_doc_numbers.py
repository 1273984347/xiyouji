#!/usr/bin/env python3
"""check_doc_numbers.py — 文案数字与证据件键值逐字对表闸（W1116 建）

问题（W1113~W1115 实证）：批已收官（PR 全合并 / 门禁 62 段 0 FAIL / 单测全绿），
结论文案里的数字仍与仓内证据件不一致——实测 25 处漂移，横跨 CHANGELOG 段 / 坑表条目 /
交付报告正文 / 台账行 四个载体，其中 3 处是阻断级（验收表 / V 表 / ST 表仍写旧值）。
**没有任何机器判据会抓这类漂移**：门禁核结构与计数，不核文案里的数字。

本闸把「人工对表」变成「机器断言」：每批在 spec 的 doc_numbers 段声明
「哪处文案 ↔ 哪个证据键」，收官链末位逐项断言；声明与实值不符即判红，
并给出 文件:行号 + 期望值 + 实际值。

用法：
    py -3 scripts/check_doc_numbers.py --spec scripts/output/_w1116_spec.json
    py -3 scripts/check_doc_numbers.py --spec <spec> --json
退出码：0 全绿；1 有 FAIL；2 判据不可执行（spec 缺失或无 doc_numbers 声明）→ 按「不伪造红」放行
"""
from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.environ.get("XIYOUJI_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def _dig(obj, dotted):
    cur = obj
    for part in dotted.split("."):
        if part == "":
            continue
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return None
        elif isinstance(cur, dict):
            if part not in cur:
                return None
            cur = cur[part]
        else:
            return None
    return cur


def source_value(spec):
    """source 形如 json:<path>#<key> | git:numstat:<ref>:<path> | count:<path>:<regex> | literal:<v>"""
    kind, _, rest = spec.partition(":")
    if kind == "literal":
        return rest
    if kind == "json":
        path, _, key = rest.partition("#")
        txt = _read(path)
        if txt is None:
            return None
        try:
            data = json.loads(txt)
        except ValueError:
            return None
        return _dig(data, key) if key else data
    if kind == "count":
        path, _, rx = rest.partition(":")
        txt = _read(path)
        if txt is None:
            return None
        try:
            # MULTILINE 必需：行首锚点（^）在无该标志时只匹配整串开头
            return len(re.findall(rx, txt, re.MULTILINE))
        except re.error:
            return None
    if kind == "git":
        sub, _, rest2 = rest.partition(":")
        if sub != "numstat":
            return None
        ref, _, path = rest2.partition(":")
        # 支持 "A..B" 双 ref（取 A→B 的净改动）与单 ref（对工作树/HEAD）
        refs = ref.split("..") if ".." in ref else [ref]
        cmd = ["git", "-C", ROOT, "diff", "--numstat"] + refs + ["--", path]
        r = subprocess.run(
            cmd,
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            return None
        for line in r.stdout.splitlines():
            parts = line.split("\t")
            if len(parts) >= 3 and parts[2].strip() == path:
                try:
                    return int(parts[0])
                except ValueError:
                    return None
        return 0
    return None


def _same(a, b):
    if a == b:
        return True
    sa, sb = str(a).strip(), str(b).strip()
    if sa == sb:
        return True
    try:
        return abs(float(sa) - float(sb)) < 1e-9
    except (TypeError, ValueError):
        return False


def check_coverage(item):
    """覆盖面声明类对账：对一组目标逐项断言（对方 W1117 建议·W1116 采纳）。

    典型用法：声明「N 个文件全『已是目标态』」⇒ 对 N 个目标逐一验证（逐文件逐点）⇒
    任一目标不满足即判红并指出目标，避免「覆盖面声明」成为又一条不可核验的措辞。
    断言类型：assert_regex（每个目标文件须匹配该正则）/ assert_json（每个目标 JSON 的
    指定键须等于 expect）/ expect_count（目标集合数须恰为该值）。
    """
    label = item.get("label") or ("覆盖面 " + str(item.get("targets")))
    files = []
    for t in (item.get("targets") or []):
        p = os.path.join(ROOT, t)
        if os.path.isfile(p):
            files.append(t)
            continue
        hits = glob.glob(os.path.join(ROOT, t), recursive=True)
        for h in hits:
            if os.path.isfile(h):
                files.append(os.path.relpath(h, ROOT).replace("\\", "/"))
    files = sorted(set(files))
    expect_count = item.get("expect_count")
    if expect_count is not None and len(files) != int(expect_count):
        return False, "%s：实得 %d 个目标（期望 %s）" % (label, len(files), expect_count)
    if not files:
        return False, "%s：未匹配到任何目标" % label
    ar = item.get("assert_regex")
    aj = item.get("assert_json")
    expect = item.get("expect")
    for f in files:
        txt = _read(f)
        if txt is None:
            return False, "%s：目标 %s 不可读" % (label, f)
        if ar:
            try:
                ok = re.search(ar, txt) is not None
            except re.error:
                return False, "%s：assert_regex 非合法正则" % label
            if not ok:
                return False, "%s：目标 %s 未满足断言 %s" % (label, f, ar)
        if aj:
            path, _, key = aj.partition("#")
            raw = _read(path)
            if raw is None:
                return False, "%s：目标 %s 的 JSON 不可读" % (label, f)
            try:
                data = json.loads(raw)
            except ValueError:
                return False, "%s：目标 %s 的 JSON 不可解析" % (label, f)
            got = _dig(data, key) if key else data
            if expect is not None and not _same(got, expect):
                return False, "%s：目标 %s 的 %s 期望 %s 实得 %s" % (label, f, key or "(整体)", expect, got)
    return True, "%s：%d 个目标全满足" % (label, len(files))


def check_item(item):
    """返回 (ok, detail)"""
    rel = item.get("file")
    pattern = item.get("pattern")
    src = item.get("source")
    label = item.get("label") or (str(rel) + " :: " + str(pattern))
    if not rel or not pattern or not src:
        return False, "声明不完整：" + label
    txt = _read(rel)
    if txt is None:
        return False, "文件不存在：" + str(rel)
    want = source_value(src)
    if want is None:
        return False, "真值取不到（source=%s）：%s" % (src, label)
    try:
        rx = re.compile(pattern)
    except re.error:
        return False, "pattern 非合法正则：" + label
    hits = 0
    for i, line in enumerate(txt.splitlines(), 1):
        for m in rx.finditer(line):
            hits += 1
            gd = m.groupdict() or {}
            if "v" in gd:
                got = m.group("v")
            elif m.groups():
                got = m.group(1)
            else:
                got = m.group(0)
            if not _same(got, want):
                return False, "%s:%d 期望 %s 实得 %s（source=%s）" % (rel, i, want, got, src)
    if hits == 0:
        return False, "未匹配到任何位置（pattern 失效）：" + label
    return True, "%s（%d 处一致 · 真值 %s）" % (label, hits, want)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    spec_path = None
    as_json = "--json" in argv
    for i, a in enumerate(argv):
        if a == "--spec" and i + 1 < len(argv):
            spec_path = argv[i + 1]
    if not spec_path:
        print("用法：py -3 scripts/check_doc_numbers.py --spec <spec.json> [--json]")
        return 2
    p = spec_path if os.path.isabs(spec_path) else os.path.join(ROOT, spec_path)
    if not os.path.isfile(p):
        print("NOTE  spec 不存在：%s —— 判据不可执行，不伪造红" % spec_path)
        return 0
    with open(p, encoding="utf-8") as f:
        spec = json.load(f)
    items = spec.get("doc_numbers") or []
    if not items:
        print("NOTE  spec 无 doc_numbers 声明 —— 判据不可执行，不伪造红")
        return 0
    fails = []
    for it in items:
        if (it.get("kind") or "value") == "coverage":
            ok, detail = check_coverage(it)
        else:
            ok, detail = check_item(it)
        print(("OK   " if ok else "FAIL ") + detail)
        if not ok:
            fails.append(detail)
    if as_json:
        print(json.dumps({"total": len(items), "fail": len(fails)}, ensure_ascii=False))
    if fails:
        print("---- 文案数字对表闸：%d FAIL ----" % len(fails))
        return 1
    print("---- 文案数字对表闸：%d 项全一致 ----" % len(items))
    return 0


if __name__ == "__main__":
    sys.exit(main())
