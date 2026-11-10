#!/usr/bin/env python3
"""retrieval_cli.py — 检索层 JSON 一次性入口（W1205 · O-4 检索层接入）

用途：给 Node 侧检索路由（xiyouji-agent-web/server/retrieval.ts）一个**无状态、
零第三方依赖**的语料检索入口。Node 侧每次请求 spawn 本脚本一次，stdout 只输出
一行 JSON；索引复用 scripts/rag/xiyouji_rag.py 的既有缓存（scripts/output/rag_index.json）。

复用既有实现（不复制检索算法，避免双实现漂移）：
  xiyouji_rag.retrieve(query, top_k) → [{"path": 仓库相对路径, "score": float, "excerpt": 摘录}]

契约：
  stdout  恒为一行 JSON（无其它打印；日志走 stderr）
  退出码  0 = 成功（含 0 命中）；2 = 参数错误；3 = 检索不可用（索引不可达/构建失败）

CLI：
  py -3 scripts/rag/retrieval_cli.py --query "五行山 牧童" [--top-k 5] [--json]
"""

import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# 退出码约定（供 Node 侧按码区分「参数错」与「索引不可达」）。
EXIT_OK = 0
EXIT_BAD_ARGS = 2
EXIT_RETRIEVAL_UNAVAILABLE = 3


def _emit(payload):
    """stdout 只出一行 JSON（ensure_ascii=False 保持中文可读，便于人工核对）。"""
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="retrieval_cli.py",
        description="西游·渡口 检索层 JSON 一次性入口（W1205 · O-4）",
    )
    parser.add_argument("--query", required=True, help="检索词（空串视为无命中）")
    parser.add_argument("--top-k", type=int, default=5, help="返回条数（1–50，默认 5）")
    parser.add_argument("--json", action="store_true", help="输出 JSON（默认即 JSON·保留以兼容调用方）")
    args = parser.parse_args(argv)

    top_k = max(1, min(int(args.top_k), 50))

    try:
        import xiyouji_rag as RAG
    except Exception as exc:  # pragma: no cover - 依赖缺失路径
        _emit({"ok": False, "error": "rag_module_unavailable", "detail": str(exc)[:200]})
        return EXIT_RETRIEVAL_UNAVAILABLE

    try:
        index = RAG.build_index()
        hits = RAG.retrieve(args.query, top_k=top_k, index=index)
    except Exception as exc:
        # 索引不可达/构建失败 ⇒ 退出码 3（Node 侧据此判「异源降级」而非 5xx 崩溃）。
        _emit({"ok": False, "error": "retrieval_unavailable", "detail": str(exc)[:200]})
        return EXIT_RETRIEVAL_UNAVAILABLE

    normalized = []
    for h in hits:
        # 路径归一为 POSIX 分隔符（Windows 上 os.path.relpath 产出反斜杠，
        # 而引用守卫按仓库相对路径 + 正斜杠判定 ⇒ 不归一会误判「路径不存在」）。
        raw_path = str(h.get("path", "")).replace("\\", "/")
        normalized.append({
            "path": raw_path,
            "score": h.get("score", 0),
            "excerpt": h.get("excerpt", ""),
        })

    _emit({
        "ok": True,
        "query": args.query,
        "top_k": top_k,
        "hits": normalized,
        "index_version": getattr(RAG, "INDEX_VERSION", None),
        "doc_count": index.get("N", 0) if isinstance(index, dict) else 0,
    })
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
