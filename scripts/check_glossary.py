#!/usr/bin/env python3
"""术语一致性门禁（W502 第 19 门禁）：术语表.md ↔ dataset/glossary.json 双向同步 + 规范词锚定。

- C1 双向同步：术语表.md 逐行解析结果与 glossary.json 逐组逐条核对，diff = 0。
- C2 规范词锚定（仅「一、人物称谓」组）：文档含某变体称谓但规范词（指代，含传递归一）
  出现次数 = 0 → 违规；存量违规冻结于 scripts/output/glossary-baseline.txt，新增文档违规 = 0。
- 复合词掩码：先遮盖含变体子串的复合术语（心猿意马/金公木母黄婆），避免子串误报。
- 已知局限：CJK 子串匹配无词边界，基线豁免兜底；新文档偶发误报时应在正文补规范词。

用法：
  python scripts/check_glossary.py                  # 门禁模式（C1 + C2 vs 基线）
  python scripts/check_glossary.py --generate       # 由术语表.md 重建 glossary.json
  python scripts/check_glossary.py --build-baseline # 冻结当前违规为基线
  python scripts/check_glossary.py --file <md>      # 单文件检查（不走基线）
口径见 docs/00-导读/文档规范.md §4.7。
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOSSARY_MD = os.path.join(ROOT, "docs", "00-导读", "术语表.md")
GLOSSARY_JSON = os.path.join(ROOT, "dataset", "glossary.json")
BASELINE = os.path.join(ROOT, "scripts", "output", "glossary-baseline.txt")
VARIANT_GROUP = "一、人物称谓"
CONTENT_DIRS = [
    "01-全书逐回解读", "02-人物深度分析", "03-主题与情节专题",
    "04-文化与历史背景", "05-诗词歌赋", "06-个人随笔",
]


def parse_md(path=None):
    """解析术语表.md → {"groups": [{"name","type","entries":[...]}]}。"""
    path = path or GLOSSARY_MD
    lines = open(path, encoding="utf-8").read().splitlines()
    groups, cur = [], None
    for ln in lines:
        if ln.startswith("## "):
            name = ln[3:].strip()
            cur = {"name": name,
                   "type": "variant" if name == VARIANT_GROUP else "term",
                   "entries": []}
            groups.append(cur)
            continue
        if cur is None or not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        if cells[0] in ("称谓", "术语", "地名", "法宝") or set(cells[0]) <= {"-", ":", " "}:
            continue  # 表头 / 分隔行
        if cur["type"] == "variant":
            variants = [v.strip() for v in cells[0].split("/") if v.strip()]
            cur["entries"].append({"variants": variants, "canonical": cells[1]})
        else:
            cur["entries"].append({"term": cells[0]})
    return {"groups": groups}


def load_json():
    return json.load(open(GLOSSARY_JSON, encoding="utf-8"))


def diff_c1(md, js):
    """C1：逐组逐条核对，返回差异清单。"""
    diffs = []
    mg, jg = md["groups"], js.get("groups", [])
    if [g["name"] for g in mg] != [g.get("name") for g in jg]:
        return ["分组序列不一致：md=%s json=%s"
                % ([g["name"] for g in mg], [g.get("name") for g in jg])]
    for a, b in zip(mg, jg):
        ea = sorted(json.dumps(e, ensure_ascii=False, sort_keys=True) for e in a["entries"])
        eb = sorted(json.dumps(e, ensure_ascii=False, sort_keys=True) for e in b.get("entries", []))
        for x in ea:
            if x not in eb:
                diffs.append("[%s] md 有 json 无：%s" % (a["name"], x))
        for x in eb:
            if x not in ea:
                diffs.append("[%s] json 有 md 无：%s" % (a["name"], x))
    return diffs


def build_variant_map(md):
    """变体→规范词映射（传递归一：圣僧→唐僧→玄奘 归一为 玄奘）。"""
    parent = {}
    for g in md["groups"]:
        if g["type"] != "variant":
            continue
        for e in g["entries"]:
            for v in e["variants"]:
                parent[v] = e["canonical"]

    def resolve(x):
        seen = set()
        while x in parent and x not in seen:
            seen.add(x)
            x = parent[x]
        return x

    vmap = {v: resolve(v) for v in parent}
    return vmap


def mask_terms(md):
    """需掩码的复合词：长度 ≥4 且含其他变体子串的术语（心猿意马/金公木母黄婆）。"""
    vmap = build_variant_map(md)
    variants = set(vmap)
    compounds = set()
    for g in md["groups"]:
        pool = [e.get("term", "") for e in g["entries"]]
        if g["type"] == "variant":
            pool += [c for e in g["entries"] for c in e["variants"]] + \
                    [e["canonical"] for e in g["entries"]]
        for t in pool:
            if len(t) >= 4 and any(v in t and v != t for v in variants):
                compounds.add(t)
    return sorted(compounds, key=len, reverse=True)


def scan_doc(text, vmap, compounds):
    """返回该文本的违规规范词集合（掩码后含变体但无规范词）。"""
    masked = text
    for c in compounds:
        masked = masked.replace(c, "□" * len(c))
    bad = set()
    for v, canon in vmap.items():
        if v in masked and canon not in masked:
            bad.add(canon)
    return bad


def iter_content_files():
    for d in CONTENT_DIRS:
        dp = os.path.join(ROOT, "docs", d)
        if not os.path.isdir(dp):
            continue
        for fn in sorted(os.listdir(dp)):
            if fn.endswith(".md") and fn != "README.md":
                yield os.path.join("docs", d, fn).replace("\\", "/")


def all_violations(md):
    """全量扫描 → {文件: [规范词...]}。"""
    vmap = build_variant_map(md)
    compounds = mask_terms(md)
    out = {}
    for rel in iter_content_files():
        text = open(os.path.join(ROOT, rel.replace("/", os.sep)), encoding="utf-8").read()
        bad = scan_doc(text, vmap, compounds)
        if bad:
            out[rel] = sorted(bad)
    return out


def load_baseline():
    if not os.path.exists(BASELINE):
        return set()
    pairs = set()
    for ln in open(BASELINE, encoding="utf-8"):
        ln = ln.strip()
        if ln:
            pairs.add(ln)
    return pairs


def main():
    ap = argparse.ArgumentParser(description="术语一致性门禁（W502）")
    ap.add_argument("--generate", action="store_true", help="由术语表.md 重建 glossary.json")
    ap.add_argument("--build-baseline", action="store_true", help="冻结当前违规为基线")
    ap.add_argument("--file", help="单文件检查（不走基线）")
    args = ap.parse_args()

    md = parse_md()

    if args.generate:
        data = {"source": "docs/00-导读/术语表.md", "note": "由 check_glossary.py --generate 解析，勿手改",
                "groups": md["groups"]}
        with open(GLOSSARY_JSON, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        n = sum(len(g["entries"]) for g in md["groups"])
        print("glossary.json 已生成：%d 组 %d 条目" % (len(md["groups"]), n))
        return 0

    if args.build_baseline:
        viol = all_violations(md)
        pairs = sorted("%s\t%s" % (f, c) for f, cs in viol.items() for c in cs)
        with open(BASELINE, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(pairs) + ("\n" if pairs else ""))
        print("基线已冻结：%d 篇文档 %d 条违规对" % (len(viol), len(pairs)))
        return 0

    if args.file:
        vmap = build_variant_map(md)
        bad = scan_doc(open(args.file, encoding="utf-8").read(), vmap, mask_terms(md))
        if bad:
            print("FAIL %s：用了变体称谓但缺规范词 %s" % (args.file, sorted(bad)))
            return 1
        print("PASS %s" % args.file)
        return 0

    # 门禁模式
    errs = []
    try:
        js = load_json()
        diffs = diff_c1(md, js)
        errs += diffs
    except FileNotFoundError:
        errs.append("dataset/glossary.json 不存在（先跑 --generate）")

    base = load_baseline()
    viol = all_violations(md)
    cur = set("%s\t%s" % (f, c) for f, cs in viol.items() for c in cs)
    new_viol = sorted(cur - base)
    if new_viol:
        for p in new_viol[:10]:
            errs.append("新违规 %s" % p)

    if errs:
        for e in errs[:12]:
            print("FAIL %s" % e)
        print("术语一致性门禁：C1 差异+新违规共 %d 项" % len(errs))
        return 1
    print("术语一致性门禁通过：C1 同步 0 差异（%d 组）·C2 基线违规 %d 条（冻结豁免）·新违规 0"
          % (len(md["groups"]), len(base)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
