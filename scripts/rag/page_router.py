"""page_router.py — 《详解西游记》语义页面路由（W746·T-01 Phase-0 ST-06 转正）。

自然语言查询 → 最相关可视化页面（87 页·site/data/*.html）。
页面源=title + meta description 嵌入（bge-small-zh-v1.5·文档口径·L2 归一），
查询带 bge 检索指令前缀·cosine top-K。产物=scripts/output/page_vectors.npy
+ page_index.json（页面清单指纹变化才重建·gitignored）。

用法：
  py -3.12 scripts/rag/page_router.py "师徒四人的情感变化曲线"   # top5 路由
  py -3.12 scripts/rag/page_router.py --eval                     # 21 题分层评测
  py -3.12 scripts/rag/page_router.py --rebuild                  # 强制重建向量缓存

依赖：sentence-transformers + numpy（可选模块·未装时本脚本不可用，
不影响 xiyouji_rag / rag_server 的零依赖默认路径）。评测基线：
21 题（基线 10+中等 8+难题 1+边界探针 2）·Phase-0 top-3 9/10 持平·
已知边界=词汇鸿沟类查询（R09 等·详见 T-01 报告 recipe card）。
"""
import glob
import json
import os
import re
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
SITE_DATA = os.path.join(ROOT, "site", "data")
OUTPUT_DIR = os.path.join(ROOT, "scripts", "output")
CACHE_VEC = os.path.join(OUTPUT_DIR, "page_vectors.npy")
CACHE_IDX = os.path.join(OUTPUT_DIR, "page_index.json")
EVAL_OUT = os.path.join(OUTPUT_DIR, "page_route_eval.md")
QUERY_INSTRUCTION = "为这个句子生成表示以用于检索相关文章："
EMBED_MODEL = "BAAI/bge-small-zh-v1.5"

if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import rag_enhance  # noqa: E402 离线预置复用

# 评测集（W746 冻结结构：基线 10 + 中等 8 + 难题 1 = 评测集 19·边界探针 2 单列）
# gold 口径=title/desc 机械匹配+语义收敛（T-01 报告·route_gold_draft）
EVAL_QUERIES = [
    ("R01", "我想看孙悟空和唐僧的人物关系图",
     ["character-relationship-3d", "character-dynamic-network", "relationships", "character-semantic-network"]),
    ("R02", "八十一难里哪一难最难",
     ["81-hardships", "hardship-heatmap", "hardship-difficulty-heatmap"]),
    ("R03", "取经路上都经过了哪些地方",
     ["journey-route", "journey-map-interactive", "customs-pass-route", "journey-geo-3d"]),
    ("R04", "师徒四人的情感变化曲线",
     ["character-sentiment-arc", "dialogue-sentiment", "pilgrim-team-psychology-arc", "emotional-heatmap"]),
    ("R05", "妖怪里谁的等级最高",
     ["monster-hierarchy-network", "monster-capability-radar", "monster-background"]),
    ("R06", "书里的诗词有什么节奏特点", ["poetry-rhythm-analysis", "linguistics", "music-structure"]),
    ("R07", "天庭的权力结构是怎样的",
     ["heaven-power-network", "power-resources", "underworld-power-network"]),
    ("R08", "每一回的字数分布", ["chapter-stats", "chapter-structure-graph"]),
    ("R09", "全书高频词有哪些", ["tag-cloud"]),
    ("R10", "通关文牒相关的页面", ["customs-pass-route"]),
    ("R11", "阴间的权力是怎么分配的", ["underworld-power-network", "karma-reincarnation"]),
    ("R12", "观音菩萨在取经路上帮了多少次",
     ["guanyin-six-roles-network", "theological-intervention-network"]),
    ("R13", "妖怪之间有没有弱肉强食的关系",
     ["monster-ecology-network", "monster-sociology", "monster-hierarchy-network"]),
    ("R14", "几个主要人物说话风格有什么区别", ["language-style-radar", "dialogue-sentiment"]),
    ("R15", "书里的法术阵法是怎么分类的", ["magic-system"]),
    ("R16", "用叙事学理论怎么拆解西游记", ["narratology-12d-network", "narratology-16d-network"]),
    ("R17", "取经这一路前后经过了多久", ["story-timeline", "timeline"]),
    ("R18", "历代文人怎么评价西游记", ["criticism-history", "text-evolution"]),
    ("R20", "明朝人自己是怎么看皇权那套的",
     ["ming-political-thought-comparison", "jurisprudence", "heaven-power-network"]),
    ("R19", "取经团队像不像一家创业公司", ["workplace", "risk-project", "business-model"]),
    ("R21", "如果当年孙悟空没大闹天宫会怎样", ["counterfactual"]),
]


def _layer(qid):
    """题层判定（W746 冻结结构·纯函数·单测覆盖）。"""
    n = int(qid[1:])
    if n <= 10:
        return "基线"
    if n <= 18:
        return "中等"
    return "难题" if qid == "R20" else "探针"


def _clean_title(t, name):
    """title 清洗：去站名前后缀（Phase-0 demo 只清了后缀·本版前后都清）。"""
    t = re.sub(r"\s+", " ", t or "").strip()
    t = t.replace(" · 详解西游记", "").replace("详解西游记 · ", "").strip()
    return t or name


def hit_at(expect, top_files, n):
    """top-N 命中判定：gold 组内任一子串命中 top_files 前 n 个（纯函数·单测覆盖）。"""
    return any(any(e in f for e in expect) for f in top_files[:n])


def load_pages(site_data=SITE_DATA):
    """扫描 site/data/*.html → [{file,title,desc}]（排除 _ 前缀模板）。"""
    pages = []
    for p in sorted(glob.glob(os.path.join(site_data, "*.html"))):
        name = os.path.basename(p)
        if name.startswith("_"):
            continue
        t = open(p, encoding="utf-8", errors="ignore").read()
        mt = re.search(r"<title>(.*?)</title>", t, re.S)
        title = _clean_title(mt.group(1) if mt else "", name)
        md = re.search(r'<meta name="description" content="(.*?)">', t, re.S)
        desc = re.sub(r"\s+", " ", md.group(1)).strip() if md else ""
        desc = desc.replace(" · 详解西游记", "").replace("详解西游记 · ", "").strip()
        pages.append({"file": name, "title": title, "desc": desc})
    return pages


def _embed(model, texts):
    return model.encode(texts, normalize_embeddings=True, batch_size=64)


def build_or_load(model, pages, rebuild=False):
    """页面向量：缓存命中（文件清单一致）即加载·否则重建落盘。"""
    import numpy as np
    fp = [p["file"] for p in pages]
    if (not rebuild) and os.path.exists(CACHE_VEC) and os.path.exists(CACHE_IDX):
        try:
            with open(CACHE_IDX, encoding="utf-8") as f:
                idx = json.load(f)
            if idx.get("fingerprint") == fp:
                return np.load(CACHE_VEC)
        except Exception:
            pass
    texts = [(p["title"] + "｜" + p["desc"]) if p["desc"] else p["title"] for p in pages]
    vecs = _embed(model, texts)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    np.save(CACHE_VEC, vecs)
    with open(CACHE_IDX, "w", encoding="utf-8") as f:
        json.dump({"model": EMBED_MODEL, "dim": int(vecs.shape[1]),
                   "fingerprint": fp,
                   "pages": [{k: p[k] for k in ("file", "title", "desc")} for p in pages]},
                  f, ensure_ascii=False)
    return vecs


def route(query, model, vecs, pages, top_k=5):
    """查询 → [(file, title, score)] top_k（cosine）。"""
    import numpy as np
    qv = _embed(model, [QUERY_INSTRUCTION + query])[0]
    sims = vecs @ qv
    order = np.argsort(-sims)[:top_k]
    return [(pages[i]["file"], pages[i]["title"], float(sims[i])) for i in order]


def evaluate(model, vecs, pages):
    """分层评测（W746 冻结口径）：评测集=基线+中等+难题（命中/19）·探针单列·
    top-1/top-3 都报（路由=跳转·top-1 体验权重高）。"""
    stats = {}
    detail = []
    for qid, query, expect in EVAL_QUERIES:
        top = route(query, model, vecs, pages, top_k=5)
        files = [f for f, _, _ in top]
        ok1 = hit_at(expect, files, 1)
        ok3 = hit_at(expect, files, 3)
        lay = _layer(qid)
        st = stats.setdefault(lay, {"n": 0, "t1": 0, "t3": 0})
        st["n"] += 1
        st["t1"] += 1 if ok1 else 0
        st["t3"] += 1 if ok3 else 0
        detail.append((qid, lay, query, ok1, ok3, top[:3]))
    lines = ["# page_router 分层评测（W746 转正版·21 题·冻结结构）", "",
             "判定：top-1/top-3 命中 gold 组内任一即有效。命中率口径=命中/19（评测集）·探针单列。", "",
             "## 分层汇总", "", "| 层 | n | top-1 | top-3 |", "|---|---|---|---|"]
    for lay in ("基线", "中等", "难题", "探针"):
        if lay in stats:
            st = stats[lay]
            lines.append("| %s | %d | %d/%d | %d/%d |" % (lay, st["n"], st["t1"], st["n"], st["t3"], st["n"]))
    ev_n = sum(stats.get(lay, {"n": 0})["n"] for lay in ("基线", "中等", "难题"))
    ev_t1 = sum(stats.get(lay, {"t1": 0})["t1"] for lay in ("基线", "中等", "难题"))
    ev_t3 = sum(stats.get(lay, {"t3": 0})["t3"] for lay in ("基线", "中等", "难题"))
    lines += ["", "**评测集（%d 条）：top-1 %d/%d · top-3 %d/%d**" % (ev_n, ev_t1, ev_n, ev_t3, ev_n), "",
              "## 边界探针（预期 0 命中·miss=符合预期·命中=鸿沟比预想窄）", ""]
    for qid, lay, query, ok1, _ok3, top in detail:
        if lay == "探针":
            lines.append("- %s「%s」：%s（top-1 %s）" % (
                qid, query, "**命中（惊喜）**" if ok1 else "miss（符合预期）",
                top[0][0] if top else "—"))
    lines += ["", "## 逐条明细", "",
              "| qid | 层 | 查询 | top-1 | top-3 | top-1 页面 |", "|---|---|---|---|---|---|"]
    for qid, lay, query, ok1, ok3, top in detail:
        lines.append("| %s | %s | %s | %s | %s | %s |" % (
            qid, lay, query[:22], "✓" if ok1 else "✗", "✓" if ok3 else "✗",
            top[0][0] if top else "—"))
    lines.append("")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(EVAL_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return stats, lines


def _load_model():
    """模型加载（离线优先·CPU）——懒加载入口·rag_server /route 与 CLI 共用。"""
    offline = rag_enhance.hf_offline_prepare([EMBED_MODEL])
    # noqa: I001 —— 禁 isort 重排：sentence_transformers 必须先于 torch（段错误坑·实证 exit 139）
    from sentence_transformers import SentenceTransformer  # noqa: I001
    import torch  # noqa: I001
    torch.set_num_threads(4)
    return SentenceTransformer(EMBED_MODEL, device="cpu", local_files_only=offline)


def _ensure_cache(model, pages, rebuild=False):
    return build_or_load(model, pages, rebuild=rebuild)


def main():
    t0 = time.time()
    pages = load_pages()
    model = _load_model()
    rebuild = "--rebuild" in sys.argv
    cached_before = os.path.exists(CACHE_VEC) and os.path.exists(CACHE_IDX)
    vecs = _ensure_cache(model, pages, rebuild=rebuild)
    print("pages=%d vecs=%s build=%.1fs（%s）" % (
        len(pages), vecs.shape, time.time() - t0,
        "重建" if rebuild or not cached_before else "缓存"), flush=True)
    if "--eval" in sys.argv:
        _stats, lines = evaluate(model, vecs, pages)
        print("\n".join(lines[:20]))
        print("EVAL_OK elapsed=%.1fs" % (time.time() - t0))
        return
    q = " ".join(a for a in sys.argv[1:] if not a.startswith("--")).strip()
    if not q:
        print('用法：py -3.12 scripts/rag/page_router.py "查询" | --eval | --rebuild')
        return
    for rank, (f, title, s) in enumerate(route(q, model, vecs, pages), 1):
        print("%d. `%s` %s（%.3f）" % (rank, f, title, s))


if __name__ == "__main__":
    main()
