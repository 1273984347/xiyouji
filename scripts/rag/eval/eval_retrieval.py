#!/usr/bin/env python3
"""eval_retrieval.py — 仓内检索评测（W844 · Q4「评测集入仓」的复算入口）。

判据定义（写死口径，避免「recall」被随口解释）：
    recall@k = |gold ∩ top-k| / |gold|          —— 该题召回了几成标准答案文档
    hit@k    = 1{gold ∩ top-k ≠ ∅}              —— 该题是否「至少命中一篇」
    汇总值   = 各题 recall@k 的**算术平均**（题权重相等，不按 gold 数量加权）

为什么按题平均而不是按文档平均：按文档平均会让 gold 有 15 篇的题权重是 1 篇题的 15 倍，
指标就变成「长尾答案集好不好召回」而不是「用户问一句能不能找到东西」。

三档口径（`--mode`）：
    off    现役零依赖加权 RRF（默认·CI 可跑）
    dense  加稠密召回（需 numpy + sentence-transformers + 模型与向量产物）
    rewrite 稠密 + LLM 改写路由（另需 LLM_API_KEY）
    后两档若依赖缺失**直接报错退出**，不得静默降级成 off——那会把「没测」伪装成「测了」。

用法：
    py -3 scripts/rag/eval/eval_retrieval.py                       # off 档 · 100 题 · 出报告
    py -3 scripts/rag/eval/eval_retrieval.py --queries scripts/rag/eval/queries_30q_frozen.jsonl
    py -3 scripts/rag/eval/eval_retrieval.py --mode dense --allow-missing-deps
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAG_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(RAG_DIR))
DEFAULT_QUERIES = os.path.join(HERE, "queries_100q.jsonl")
DEFAULT_REPORT = os.path.join(ROOT, "scripts", "output", "rag_eval_report.md")

KS = (1, 5, 10)


def norm(p):
    """路径归一：反斜杠转正斜杠（冻结集沿用 Windows 分隔符，索引侧是各自平台形态）。"""
    return p.replace("\\", "/")


def load_queries(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def evaluate(rows, mode, ks=KS):
    """跑一遍评测；返回 {per_query:[…], summary:{…}}。"""
    os.environ["RAG_ENHANCE"] = mode
    if RAG_DIR not in sys.path:
        sys.path.insert(0, RAG_DIR)
    import xiyouji_rag  # noqa: E402

    top_k = max(ks)
    index = xiyouji_rag.build_index()
    indexed = {norm(d["path"]) for d in index["docs"]}

    per_query, skipped = [], []
    for r in rows:
        gold = {norm(p) for p in r["gold"]}
        # 只统计「gold 至少有一篇在索引内」的题——否则 recall 天生为 0，
        # 记成「检索失败」会把「题集与索引面不一致」这个真问题糊过去。
        in_index = gold & indexed
        if not in_index:
            skipped.append(r["qid"])
            continue
        hits = xiyouji_rag.retrieve(r["query"], top_k=top_k, index=index)
        ranked = [norm(h["path"]) for h in hits]
        rec = {}
        for k in ks:
            topk = set(ranked[:k])
            rec["recall@%d" % k] = len(in_index & topk) / float(len(in_index))
            rec["hit@%d" % k] = 1.0 if (in_index & topk) else 0.0
        per_query.append(
            {
                "qid": r["qid"],
                "query": r["query"],
                "type": r.get("type", "?"),
                "origin": r.get("origin", "frozen"),
                "gold_n": len(in_index),
                "gold_out_of_index": sorted(gold - indexed),
                **rec,
            }
        )
    return {"per_query": per_query, "skipped": skipped}


def aggregate(per_query, key):
    """按 key（origin / type）分组求均值；返回 [{group, n, recall@k…}]。"""
    groups = {}
    for q in per_query:
        groups.setdefault(q[key], []).append(q)
    out = []
    for g, items in sorted(groups.items()):
        row = {key: g, "n": len(items)}
        for k in KS:
            row["recall@%d" % k] = sum(i["recall@%d" % k] for i in items) / len(items)
            row["hit@%d" % k] = sum(i["hit@%d" % k] for i in items) / len(items)
        out.append(row)
    return out


def pct(x):
    return "%.3f" % x


def render_report(rows, res, mode, elapsed, queries_path):
    per = res["per_query"]
    total = {
        "n": len(per),
        **{
            "recall@%d" % k: sum(i["recall@%d" % k] for i in per) / len(per)
            for k in KS
        },
        **{"hit@%d" % k: sum(i["hit@%d" % k] for i in per) / len(per) for k in KS},
    }
    by_origin = aggregate(per, "origin")
    by_type = aggregate(per, "type")

    lines = []
    lines.append("# RAG 检索评测报告（生成物·可重跑覆盖）")
    lines.append("")
    lines.append("> 生成器：`scripts/rag/eval/eval_retrieval.py`（W844）· 档位 `%s` · 题集 `%s`"
                 % (mode, os.path.relpath(queries_path, ROOT).replace("\\", "/")))
    lines.append("> 复算入口：`py -3 scripts/rag/eval/eval_retrieval.py`（默认 off 档 + 100 题）")
    lines.append("> 用时 %.1f s · 参与统计 %d 题" % (elapsed, total["n"]))
    if res["skipped"]:
        lines.append("> **跳过 %d 题**（gold 全在索引外）：%s" % (len(res["skipped"]), "、".join(res["skipped"])))
    lines.append("")
    lines.append("## 一、总表")
    lines.append("")
    lines.append("| 口径 | recall@1 | recall@5 | recall@10 | hit@1 | hit@5 | hit@10 |")
    lines.append("|:---|---:|---:|---:|---:|---:|---:|")
    lines.append("| 全量（%d 题） | %s | %s | %s | %s | %s | %s |"
                 % (total["n"], pct(total["recall@1"]), pct(total["recall@5"]), pct(total["recall@10"]),
                    pct(total["hit@1"]), pct(total["hit@5"]), pct(total["hit@10"])))
    lines.append("")
    lines.append("## 二、按题源分组（**不可合并解读**）")
    lines.append("")
    lines.append("| 题源 | 题数 | recall@1 | recall@5 | recall@10 | 说明 |")
    lines.append("|:---|---:|---:|---:|---:|:---|")
    note = {
        "frozen": "人工题·接近真实提问·**主指标**",
        "anchor": "标题派生·问句由模板生成·偏易·只看标题面覆盖",
    }
    for r in by_origin:
        lines.append("| %s | %d | %s | %s | %s | %s |"
                     % (r["origin"], r["n"], pct(r["recall@1"]), pct(r["recall@5"]), pct(r["recall@10"]),
                        note.get(r["origin"], "")))
    lines.append("")
    lines.append("## 三、按题型分组")
    lines.append("")
    lines.append("| 题型 | 题数 | recall@1 | recall@5 | recall@10 |")
    lines.append("|:---|---:|---:|---:|---:|")
    for r in by_type:
        lines.append("| %s | %d | %s | %s | %s |"
                     % (r["type"], r["n"], pct(r["recall@1"]), pct(r["recall@5"]), pct(r["recall@10"])))
    lines.append("")
    lines.append("## 四、逐题明细")
    lines.append("")
    lines.append("| qid | 题型 | 题源 | gold 数 | 索引外 gold | recall@1 | recall@5 | recall@10 | 问句 |")
    lines.append("|:--|:--|:--|---:|---:|---:|---:|---:|:---|")
    for q in per:
        ooi = len(q["gold_out_of_index"])
        lines.append("| %s | %s | %s | %d | %d | %s | %s | %s | %s |"
                     % (q["qid"], q["type"], q["origin"], q["gold_n"], ooi,
                        pct(q["recall@1"]), pct(q["recall@5"]), pct(q["recall@10"]), q["query"]))
    lines.append("")
    lines.append("## 五、口径与局限（读数字前先读这段）")
    lines.append("")
    lines.append("1. **recall 是按题平均**，不按 gold 文档数加权——否则 gold 有 15 篇的题会压过只有 1 篇的题。")
    lines.append("2. **只统计 gold 至少一篇在索引内的题**；被跳过的题会单独列出，不得当作 0 分混算。")
    lines.append("3. `origin=anchor` 的 70 题由文档标题派生，**难度显著低于**人工 30 题；")
    lines.append("   两个分组的数字只在各自组内做前后对比，**不可跨组比较**，也不可拿全量均值当「真实体验」。")
    lines.append("4. 索引面 = `docs/**/*.md` 中经 `xiyouji_rag._load_docs()` 收录的文档；")
    lines.append("   站点页面（`site/**`）与 622 页 reader 不在检索面内，故不以它们作 gold。")
    lines.append("5. 大件（`chunks.jsonl` / `vectors.npy` / `rag_index_t01.json`，合计 170 MB+）**不入库**；")
    lines.append("   `dense`/`rewrite` 档需本地重建产物，故仓内默认只跑 `off`。")
    lines.append("")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="仓内检索评测（W844）")
    ap.add_argument("--queries", default=DEFAULT_QUERIES)
    ap.add_argument("--mode", default="off", choices=("off", "dense", "rewrite", "rerank"))
    ap.add_argument("--out", default=DEFAULT_REPORT, help="报告输出路径（''=不写盘）")
    ap.add_argument("--json", dest="json_out", default="", help="可选：逐题明细 JSON 输出路径")
    ap.add_argument("--allow-missing-deps", action="store_true",
                    help="增强档依赖缺失时退化为 off 并显式标注（默认直接报错）")
    args = ap.parse_args()

    rows = load_queries(args.queries)
    if not rows:
        print("[FAIL] 题集为空：%s" % args.queries)
        return 1

    started = time.time()
    try:
        res = evaluate(rows, args.mode)
    except (ImportError, RuntimeError, ValueError) as exc:
        if not args.allow_missing_deps:
            print("[FAIL] %s 档不可用：%s" % (args.mode, exc))
            print("       仓内默认只保证 off 档可跑；增强档需本地重建向量产物与依赖。")
            print("       确需降级请显式加 --allow-missing-deps（报告会标注降级事实）。")
            return 1
        print("[WARN] %s 档不可用（%s）——按 --allow-missing-deps 降级为 off" % (args.mode, exc))
        res = evaluate(rows, "off")
        args.mode = "off（降级）"
    elapsed = time.time() - started

    per = res["per_query"]
    if not per:
        print("[FAIL] 没有任何题可统计（gold 全在索引外）——题集与索引面不一致")
        return 1
    total_r5 = sum(i["recall@5"] for i in per) / len(per)
    total_r10 = sum(i["recall@10"] for i in per) / len(per)
    print("[EVAL] 档位=%s · 题数=%d（跳过 %d）· recall@5=%.3f · recall@10=%.3f · %.1fs"
          % (args.mode, len(per), len(res["skipped"]), total_r5, total_r10, elapsed))
    for r in aggregate(per, "origin"):
        print("       origin=%-7s n=%-3d recall@1=%.3f recall@5=%.3f recall@10=%.3f"
              % (r["origin"], r["n"], r["recall@1"], r["recall@5"], r["recall@10"]))

    if args.out:
        text = render_report(rows, res, args.mode, elapsed, args.queries)
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print("[WRITE] %s" % os.path.relpath(args.out, ROOT).replace("\\", "/"))

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        print("[WRITE] %s" % os.path.relpath(args.json_out, ROOT).replace("\\", "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
