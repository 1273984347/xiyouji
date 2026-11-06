"""全仓深度审计可复用入口（W1149 沉淀）。

用法：
  python scripts/audit_repo.py reader      # reader 完整性四判据
  python scripts/audit_repo.py dataset     # dataset 清单/schema + 哨兵/引文状态
  python scripts/audit_repo.py trees       # output / site-json / dataset 三树对比
  python scripts/audit_repo.py patterns    # 同类写法全站分布（占位/旧前缀/多 h1/同题）
  python scripts/audit_repo.py all --json  # 全部，JSON 输出

只读：不写任何文件；退出码 0 = 无发现 / 1 = 有发现 / 2 = 基础设施缺失。
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_dataset_manifest  # noqa: E402
import check_reader_integrity  # noqa: E402

SITE = ROOT / "site"
D = ROOT / "dataset"
SJ = SITE / "data" / "json"
OD = ROOT / "scripts" / "output" / "data"

PLACEHOLDER_RE = re.compile(r"（待补）|\(待补\)|待完善|内容建设中|TODO\b|FIXME\b|Lorem ipsum")
DOCS_SOURCE_RE = re.compile(r"docs/source/")
H1_RE = re.compile(r"<h1\b", re.I)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
STRIP = (
    (re.compile(r"<script\b[\s\S]*?</script\s*>", re.I), " "),
    (re.compile(r"<style\b[\s\S]*?</style\s*>", re.I), " "),
    (re.compile(r"<!--[\s\S]*?-->", re.I), " "),
    (re.compile(r"<[^>]+>", re.I), " "),
)


def _html_files(base: Path):
    return sorted(p for p in base.rglob("*.html") if p.is_file())


def _visible(html: str) -> str:
    t = html
    for pat, rep in STRIP:
        t = pat.sub(rep, t)
    return re.sub(r"\s+", " ", t)


def _bag(name: str) -> tuple:
    return tuple(sorted(re.split(r"[-_]", Path(name).stem.lower())))


def reader_report() -> dict:
    fails, n = check_reader_integrity.scan(ROOT)
    return {"pages": n, "fails": fails, "fail_n": len(fails)}


def dataset_report() -> dict:
    fails, n = check_dataset_manifest.scan(ROOT)
    zero, weights, quotes = 0, Counter(), Counter()
    for p in D.glob("*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue

        def walk(obj, fname):
            nonlocal zero
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if str(k).lower() in ("chapter", "回目") and v == 0:
                        zero += 1
                    if str(k).lower() in ("weight", "edge_weight", "event_weight", "score") and isinstance(v, (int, float)):
                        weights[fname] = max(weights.get(fname, 0), float(v))
                    walk(v, fname)
            elif isinstance(obj, list):
                for v in obj:
                    walk(v, fname)

        walk(data, p.name)
        for e in (data.get("events") or []) if isinstance(data, dict) else []:
            if isinstance(e, dict) and e.get("quote_status"):
                quotes[e["quote_status"]] += 1
    return {
        "files": n,
        "fails": fails,
        "fail_n": len(fails),
        "chapter_zero": zero,
        "weight_max": dict(weights),
        "quote_status": dict(quotes),
    }


def trees_report() -> dict:
    def names(base: Path) -> list[str]:
        return sorted(p.name for p in base.glob("*.json")) if base.is_dir() else []

    out_names, sj_names, d_names = names(OD), names(SJ), names(D)
    out_available = len(out_names) > 0
    same_sj_out = 0
    diff_sj_out = []
    for n in sj_names:
        p2 = OD / n
        if not p2.exists():
            continue
        try:
            same_sj_out += 1 if json.loads((SJ / n).read_text(encoding="utf-8")) == json.loads(p2.read_text(encoding="utf-8")) else 0
            if json.loads((SJ / n).read_text(encoding="utf-8")) != json.loads(p2.read_text(encoding="utf-8")):
                diff_sj_out.append(n)
        except Exception:  # noqa: BLE001
            diff_sj_out.append(n)
    out_bag = defaultdict(list)
    for n in out_names:
        out_bag[_bag(n)].append(n)
    d_out_overlap = [(n, out_bag[_bag(n)]) for n in d_names if _bag(n) in out_bag]
    sj_bag = defaultdict(list)
    for n in sj_names:
        sj_bag[_bag(n)].append(n)
    d_sj_overlap = [(n, sj_bag[_bag(n)]) for n in d_names if _bag(n) in sj_bag]

    def size(base: Path) -> int:
        return sum(p.stat().st_size for p in base.glob("*.json")) if base.is_dir() else 0

    return {
        "counts": {"output": len(out_names), "site_json": len(sj_names), "dataset": len(d_names)},
        "bytes": {"output": size(OD), "site_json": size(SJ), "dataset": size(D)},
        "output_available": out_available,
        "note": None if out_available else "scripts/output/data 为本地生成产物（多数不入库）；先跑 run_all.py 再对拍",
        "site_json_vs_output": {"same": same_sj_out, "diff": len(diff_sj_out), "diff_files": diff_sj_out}
        if out_available else {"skipped": True},
        "dataset_vs_output_name_overlap": d_out_overlap if out_available else [],
        "dataset_vs_site_json_name_overlap": d_sj_overlap,
    }


def patterns_report() -> dict:
    placeholders, docs_source, multi_h1, no_h1 = [], [], [], []
    titles = Counter()
    for p in _html_files(SITE):
        rel = p.relative_to(ROOT).as_posix()
        html = p.read_text(encoding="utf-8", errors="replace")
        vis = _visible(html)
        ms = PLACEHOLDER_RE.findall(vis)
        if ms:
            placeholders.append((rel, len(ms), ms[0]))
        n_ds = len(DOCS_SOURCE_RE.findall(html))
        if n_ds:
            docs_source.append((rel, n_ds))
        n_h1 = len(H1_RE.findall(html))
        if n_h1 > 1:
            multi_h1.append((rel, n_h1))
        if n_h1 == 0 and "http-equiv=\"refresh\"" not in html.lower() and "http-equiv='refresh'" not in html.lower():
            no_h1.append(rel)
        tm = TITLE_RE.search(html)
        if tm:
            titles[re.sub(r"\s+", " ", tm.group(1)).strip()] += 1
    dup_titles = [(t, n) for t, n in titles.items() if n > 1]
    return {
        "placeholders": {"pages": len(placeholders), "occ": sum(n for _r, n, _m in placeholders),
                         "sample": placeholders[:5]},
        "docs_source_prefix": {"pages": len(docs_source), "occ": sum(n for _r, n in docs_source), "sample": docs_source[:5]},
        "multi_h1": {"pages": len(multi_h1), "sample": multi_h1[:5]},
        "no_h1_non_redirect": {"pages": len(no_h1), "sample": no_h1[:5]},
        "duplicate_titles": {"groups": len(dup_titles), "sample": dup_titles[:5]},
    }


def run(cmd: str) -> dict:
    if cmd == "reader":
        return {"reader": reader_report()}
    if cmd == "dataset":
        return {"dataset": dataset_report()}
    if cmd == "trees":
        return {"trees": trees_report()}
    if cmd == "patterns":
        return {"patterns": patterns_report()}
    if cmd == "all":
        return {
            "reader": reader_report(),
            "dataset": dataset_report(),
            "trees": trees_report(),
            "patterns": patterns_report(),
        }
    raise SystemExit("未知子命令：%s（可选 reader/dataset/trees/patterns/all）" % cmd)


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    cmd = next((a for a in argv if not a.startswith("-")), "all")
    result = run(cmd)
    if "--json" in argv:
        print(json.dumps(result, ensure_ascii=False, indent=1))
    else:
        for key, val in result.items():
            print("[%s]" % key)
            print(json.dumps(val, ensure_ascii=False, indent=1))
    fails = 0
    for val in result.values():
        if isinstance(val, dict):
            fails += int(val.get("fail_n", 0))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
