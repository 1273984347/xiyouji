"""source_collate.py — 原文考据三方对拍器（S-23·W699）。

难簿原文序（source/原文/分回/第099回.md 难簿段）× 回目行（各分回文件首行）
× dataset 章节表（dataset/81-hardships.json）三方对拍：

  python scripts/source_collate.py --full                # 全量 81 难对拍矩阵（Markdown）
  python scripts/source_collate.py --entity 被魔化身     # 单实体三方定位
  python scripts/source_collate.py --chap 36-39          # 章回区间内的难目
  python scripts/source_collate.py --year-table timeline/西游记大事年表.md   # 年表 81 难表回放对拍
  python scripts/source_collate.py --self-test           # 负样本自检

约束：只读不改（BL-8 域的 dataset 修复须作者裁决，本工具只出差异报告）。
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NANBO_CHAP = ROOT / "source" / "原文" / "分回" / "第099回.md"
FENHUI = ROOT / "source" / "原文" / "分回"
DATASET = ROOT / "dataset" / "81-hardships.json"
NANBO_PASSAGE = (r"谨记唐僧难数清：", r"菩萨将难簿目过了一遍")
HARD_81 = ("老鼋淬水", 99)  # 第 81 难系观音令补足，难簿原文只列 80 项

CN_NUM = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def cn2int(s):
    """中文数字→int（支持 一~八十一 形态）。"""
    if not s:
        return None
    if s.startswith("十"):
        rest = s[1:]
        return 10 + (CN_NUM.get(rest, 0) if rest else 0)
    if "十" in s:
        a, _, b = s.partition("十")
        return CN_NUM.get(a, 0) * 10 + (CN_NUM.get(b, 0) if b else 0)
    return CN_NUM.get(s)


def load_nanbo():
    """难簿原文 80 项：[(序, 名)]。按逗号分词逐 token 非贪牙匹配（跨行金銮/殿变虎已归并）。"""
    text = NANBO_CHAP.read_text(encoding="utf-8")
    a = text.find(NANBO_PASSAGE[0])
    b = text.find(NANBO_PASSAGE[1])
    assert a != -1 and b != -1, "难簿段定位失败"
    seg = text[a + len(NANBO_PASSAGE[0]):b].replace("\n", "")
    items = {}
    for tok in seg.split("，"):
        m = re.fullmatch(r"([\u4e00-\u9fa5]+?)([一二三四五六七八九十]+)难", tok.strip())
        if not m:
            continue
        num = cn2int(m.group(2))
        if num and 1 <= num <= 80 and num not in items:
            name = m.group(1)[:-1] if m.group(1).endswith("第") else m.group(1)
            items[num] = name
    assert len(items) == 80, "难簿解析 %d 项（应为 80）" % len(items)
    items[81] = HARD_81[0]
    return [(i, items[i]) for i in sorted(items)]


def load_huimu():
    """回目行：{章: 回目行文本}。"""
    out = {}
    for p in sorted(FENHUI.glob("第*回.md")):
        m = re.match(r"第(\d{3})回", p.name)
        first = p.read_text(encoding="utf-8").split("\n", 1)[0].strip()
        out[int(m.group(1))] = re.sub(r"^#\s*", "", first)
    return out


def load_dataset():
    return json.loads(DATASET.read_text(encoding="utf-8"))["hardships"]


def matrix_rows():
    """全量 81 行：[(难簿序, 难簿名, ds名或None, ds章节或None, 差异标注)]。"""
    nanbo = dict(load_nanbo())
    ds = load_dataset()
    ds_by_name = {d["name"]: d for d in ds}
    rows = []
    for i, name in nanbo.items():
        d = ds_by_name.get(name)
        tags = []
        ds_name, ds_ch = (d["name"], d["chapter"]) if d else (None, None)
        if not d:
            near = [x["name"] for x in ds if name[:2] == x["name"][:2]]
            tags.append("ds缺名" + ("（近似：%s）" % "、".join(near) if near else ""))
        if d and ds_by_name and d.get("index") != i:
            tags.append("ds序=%d" % d["index"])
        rows.append((i, name, ds_name, ds_ch, "；".join(tags)))
    extra = [d for d in ds if d["name"] not in nanbo.values()]
    return rows, extra


def fmt_full():
    rows, extra = matrix_rows()
    hui = load_huimu()
    out = ["| 难簿序 | 难簿名 | dataset 名 | dataset 章节 | 该章回目 | 差异 |", "|---|---|---|---|---|---|"]
    for i, name, dsn, dch, tags in rows:
        hui_txt = hui.get(dch, "—") if isinstance(dch, int) else (hui.get(int(dch), "—") if str(dch).isdigit() else "—")
        out.append("| %d | %s | %s | %s | %s | %s |" % (i, name, dsn or "—", dch or "—", hui_txt, tags or "—"))
    for d in extra:
        out.append("| — | — | %s | %s | — | **ds 多出项**（index=%d） |" % (d["name"], d["chapter"], d["index"]))
    return "\n".join(out), rows, extra


def fmt_entity(name):
    nanbo = dict(load_nanbo())
    ds = {d["name"]: d for d in load_dataset()}
    hits = []
    for i, n in nanbo.items():
        if name in n:
            hits.append("难簿：第 %d 难「%s」" % (i, n))
    if name in ds:
        d = ds[name]
        hits.append("dataset：%s（index=%s·chapter=%s）" % (d["name"], d["index"], d["chapter"]))
        ch = d["chapter"]
        if str(ch).isdigit():
            hits.append("回目：第 %03d 回 %s" % (int(ch), load_huimu().get(int(ch), "—")))
    if not hits:
        return "未命中：%s" % name
    return "\n".join(hits)


def fmt_chap(a, b):
    ds = [d for d in load_dataset() if str(d["chapter"]).isdigit() and a <= int(d["chapter"]) <= b]
    hui = load_huimu()
    out = []
    for d in sorted(ds, key=lambda x: x["index"]):
        ch = int(d["chapter"])
        out.append("- 难簿相关 index=%s「%s」→ 第 %03d 回 %s" % (d["index"], d["name"], ch, hui.get(ch, "—")))
    return "\n".join(out) or "区间内无难目"


def year_table(md_path):
    """年表 81 难表回放：逐行校验 难序→难簿名 一致 + dataset 章节落入对应情节区间。"""
    text = Path(md_path).read_text(encoding="utf-8")
    nanbo = dict(load_nanbo())
    ds = {d["name"]: d for d in load_dataset()}
    issues = []
    n = 0
    for m in re.finditer(r"^\|\s*(\d+)(?:-(\d+))?\s*\|\s*([^|]+?)\s*\|\s*第\s*(\d+)(?:-(\d+))?\s*回", text, re.M):
        n += 1
        lo = int(m.group(1))
        hi = int(m.group(2) or m.group(1))
        names = re.split(r"[·、，]", m.group(3).strip())
        c_lo, c_hi = int(m.group(4)), int(m.group(5) or m.group(4))
        for k in range(lo, hi + 1):
            expect = nanbo.get(k)
            if expect is None:
                issues.append("难序 %d 不在难簿（原文仅 80+补足 81）" % k)
                continue
            if k == 81:
                continue
            hit = next((x for x in names if x in expect or expect in x), None)
            if hit is None:
                issues.append("难序 %d 应为「%s」，年表行难名列 %s 未含" % (k, expect, names))
            d = ds.get(expect)
            if d and str(d["chapter"]).isdigit() and not (c_lo - 3 <= int(d["chapter"]) <= c_hi + 3):
                issues.append("难序 %d「%s」dataset 章节=%s 超出年表区间 %d-%d（容差3）" % (k, expect, d["chapter"], c_lo, c_hi))
    return n, issues


def self_test():
    nanbo = dict(load_nanbo())
    assert nanbo[27] == "被魔化身" and nanbo[5] == "出城逢虎" and nanbo[65] == "比丘救子", "难簿锚点自检失败"
    tmp = ROOT / "scripts" / "output" / "_s23_selftest_tmp.md"
    tmp.write_text(
        "| 27 | 路阻火焰山 | 第 59-61 回 火焰山 |\n"
        "| 81 | 出城逢虎 | 第 13 回 出长安 |\n",
        encoding="utf-8")
    try:
        n, issues = year_table(tmp)
        assert n == 2 and len(issues) >= 2, "负样本未捕获：%s" % issues
    finally:
        tmp.unlink()
    print("SELF-TEST PASS：难簿锚点 3 点全中 + 序名错配/81 错名两负样本全捕获")


def main():
    ap = argparse.ArgumentParser(description="原文考据三方对拍器（难簿序×回目行×dataset）")
    ap.add_argument("--full", action="store_true", help="全量 81 难对拍矩阵")
    ap.add_argument("--entity", help="单实体三方定位")
    ap.add_argument("--chap", help="章回区间如 36-39")
    ap.add_argument("--year-table", help="年表 81 难表回放对拍")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.full:
        out, rows, extra = fmt_full()
        print(out)
        bad = [r for r in rows if r[4]]
        print("\n[汇总] 难簿 81 项 · dataset 命名一致 %d · 名异/缺名 %d · ds 多出 %d"
              % (len(rows) - len(bad), len(bad), len(extra)))
        return 0
    if args.entity:
        print(fmt_entity(args.entity))
        return 0
    if args.chap:
        a, _, b = args.chap.partition("-")
        print(fmt_chap(int(a), int(b or a)))
        return 0
    if args.year_table:
        n, issues = year_table(args.year_table)
        for s in issues:
            print("DIFF", s)
        print("[回放] 解析 %d 行 · 差异 %d 项" % (n, len(issues)))
        return 1 if issues else 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
