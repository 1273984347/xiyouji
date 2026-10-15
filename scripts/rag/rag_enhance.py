#!/usr/bin/env python3
"""
rag_enhance.py — 《详解西游记》检索增强引擎（T-01 Phase-1 集成·W744）

定位：xiyouji_rag.py 的可选增强层。核心引擎保持零依赖（仅 stdlib），本模块
承载增强检索所需的重依赖（numpy / sentence-transformers），经 RAG_ENHANCE
四档开关由核心引擎惰性调用：

  off（默认） — 不经本模块（核心引擎现役加权 RRF·行为零变化）
  dense      — BM25 序 + 稠密序（bge-small-zh-v1.5·页级 max 相似度）经加权
               RRF 融合（bm25×1.0 + dense×2.0·k=60），融合池直取 top_k
  rerank     — dense 基础上：融合池 top50 交 cross-encoder（bge-reranker-base）
               重排（v1 配方：文档首 800 字导语为输入）
  rewrite    — rerank 基础上：LLM 查询改写并池（原查询池 ∪ 改写池·按改写查询
               重排）——治「池外」查询（Q24 recall@5 0→1.0、Q29 0→0.667）；
               W745 起内置智能路由：短实体查询（≤6 汉字·无「的」·无疑问词）
               跳过改写直走主链——全量 30 条实测：默认全改写 @5 −0.032（direct
               型 −0.184、简单层 −0.144），按型路由 @5 +0.041、@10 +0.107

实测口径（T-01 Phase-1·30 查询评测集·详见 tmpe/hf-poc/ 实验区）：
  off 0.393 → dense 0.396 → rerank 0.487 recall@5（五系统对照 → 池构造器冠军）。

设计边界：
- 顶层仅 stdlib（可被 CI pytest 与零依赖环境导入·纯逻辑函数单测）；
- numpy / sentence-transformers 在 _ensure_loaded() 内惰性导入（ST 必须先于
  torch——本机实测导入顺序段错误坑）；
- 模型默认 CPU 推理（RAG_DEVICE 环境变量可覆盖；GPU 模式注意本机硬件纪律）；
- 产物/依赖缺失 → RuntimeError 带修复指引（fail-fast·不静默降级）；
- 检索排序与输出构造分离：本模块只返回 [(path, score)]，输出结构
  （path/score/excerpt）由核心引擎统一构造。

产物（build_vectors.py 生成·scripts/output/）：
  rag_vectors.npy     分块嵌入矩阵（float32·L2 归一）
  rag_chunks.jsonl    分块记录（chunk_id/doc_idx/path/title/text）
  rag_embed_meta.json 构建元信息（模型/维度/文档指纹）
"""
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
OUTPUT_DIR = os.path.join(ROOT, "scripts", "output")

# ---- 常量（与 T-01 实验口径一致·改动须重跑评测集） ----
EMBED_MODEL = "BAAI/bge-small-zh-v1.5"
RERANK_MODEL = "BAAI/bge-reranker-base"
QUERY_INSTRUCTION = "为这个句子生成表示以用于检索相关文章："   # bge 官方检索指令
RRF_K = 60
DENSE_WEIGHT = 2.0   # 融合权重：RRF(bm25×1.0, dense×2.0)（实测平台 w∈[2.0,3.0]）
POOL_TOP = 200       # 双路各自召回深度
POOL_K = 50          # 融合池大小（交重排的候选数）
INTRO_CHARS = 800    # v1 重排文本配方：文档首 800 字
RERANK_BATCH = 16    # 重排批大小（实验口径）
ENGINE_LEVELS = ("dense", "rerank", "rewrite")
SHORT_CJK_MAX = 6    # W745 智能路由：短实体判据（≤6 汉字视为短查询·跳过改写）

# 查询改写 prompt（与 T-01 实验一致）
REWRITE_PROMPT = (
    "你是《西游记》检索系统的查询改写器。把用户的口语化问题改写成更利于检索的关键词组合："
    "保留专有名词；补全隐含的同义术语。示例：输入「猴子被压在哪座山下」→输出「五行山 两界山 大闹天宫」；"
    "输入「为什么厉害的妖怪最后都被收走而不是打死」→输出「招安 归化 收编 妖怪 后台 收服」。"
    "只输出一行关键词，不要解释。")


# ============================================================
# 纯逻辑层（stdlib·零重依赖·可单测）
# ============================================================

def rrf_fuse(order_lists, weights, k=RRF_K):
    """加权 RRF 融合多个「路径序」列表 → [(path, fused_score)]（按分降序·去重）。

    与 xiyouji_rag._rrf 同构（idx 域 vs path 域的差异在本层收敛）；
    权重 ≤0 的列表跳过；同分稳定序 = 插入序（先入者在前）。
    """
    fused = {}
    for w, lst in zip(weights, order_lists, strict=True):
        if w <= 0:
            continue
        for rank, p in enumerate(lst):
            fused[p] = fused.get(p, 0.0) + w / (k + rank + 1)
    return sorted(fused.items(), key=lambda x: -x[1])


def merge_pools(*pools):
    """并池：多池按序合并去重（保序·rewrite 档 union 用）。"""
    seen = set()
    out = []
    for pool in pools:
        for p in pool:
            if p not in seen:
                seen.add(p)
                out.append(p)
    return out


def clean_rewrite(raw):
    """LLM 改写输出清理：取首个非空行并 strip（模型偶带解释行）。"""
    if not raw:
        return ""
    for line in str(raw).splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def build_rewrite_messages(query):
    """构造改写请求 messages（provider 兼容 schema）。"""
    return [{"role": "system", "content": REWRITE_PROMPT},
            {"role": "user", "content": query}]


def should_rewrite(query):
    """智能路由：查询是否走改写路径（W745·W744-6b 全量实测落地）。

    依据（全量 30 条对照）：direct 型（短专名）改写 recall@5 −0.184（稀释精准
    关键词 + 污染重排 query）；indirect/concept 型 +0.088/+0.020——「难例才调
    LLM」。判据=短实体形态学规则（与评测集 direct 标签 30/30 一致·小样本·
    后续可用更多数据校准）：

      长度 >6 汉字 | 含「的」结构 | 含疑问词 → 走改写；否则短实体直走主链。
    """
    q = (query or "").strip()
    if not q:
        return False
    cjk = len(re.findall(r"[\u4e00-\u9fff]", q))
    if cjk > SHORT_CJK_MAX:
        return True
    if "的" in q:
        return True
    if re.search(r"(谁|什么|哪|怎么|为什么|为何|如何|吗|呢|多少|几)", q):
        return True
    return False


def doc_rows_from_chunks(chunks):
    """分块记录 → (path_by_idx, doc_rows)。

    path_by_idx: doc_idx → path；doc_rows: doc_idx → [块行号...]（保序）。
    """
    path_by_idx = {}
    doc_rows = {}
    for row, c in enumerate(chunks):
        di = c["doc_idx"]
        path_by_idx[di] = c["path"]
        doc_rows.setdefault(di, []).append(row)
    return path_by_idx, doc_rows


def docs_stat(docs_dir):
    """轻量扫描 docs/：(.md 文件数, 最新 mtime)。

    产物陈旧检测口径（与 build_vectors.py 写入 meta 的口径一致）。
    """
    n, mx = 0, 0.0
    for base, _, files in os.walk(docs_dir):
        for fn in files:
            if fn.lower().endswith(".md"):
                n += 1
                try:
                    mx = max(mx, os.path.getmtime(os.path.join(base, fn)))
                except OSError:
                    pass
    return n, mx


def _hf_hub_cache_dir():
    """解析 HF Hub 缓存根目录（复刻 huggingface_hub 的优先级·纯文件系统）。"""
    for var in ("HF_HUB_CACHE", "HUGGINGFACE_HUB_CACHE"):
        v = os.environ.get(var, "").strip().rstrip("\\/")
        if v:
            return v
    hf_home = os.environ.get("HF_HOME", "").strip()
    if hf_home:
        return os.path.join(hf_home.rstrip("\\/"), "hub")
    xdg = os.environ.get("XDG_CACHE_HOME", "").strip()
    base = xdg if xdg else os.path.join(os.path.expanduser("~"), ".cache")
    return os.path.join(base, "huggingface", "hub")


def hf_model_cached(name):
    """探测模型在 HF 缓存中是否已有快照（纯文件系统·不触发 huggingface_hub import）。"""
    folder = "models--" + name.replace("/", "--")
    snaps = os.path.join(_hf_hub_cache_dir(), folder, "snapshots")
    if not os.path.isdir(snaps):
        return False
    try:
        with os.scandir(snaps) as it:
            return any(True for _ in it)
    except OSError:
        return False


def hf_offline_prepare(model_names):
    """离线预置：必须在首次 import sentence-transformers 之前调用。

    huggingface_hub 的 offline 判定是 import 期常量（实测运行时设置不生效），
    故本地缓存齐全时提前置 HF_HUB_OFFLINE=1——离线可规避受限网络（代理/证书链）
    下 etag 检查卡死；缓存不全则保持联网（提示镜像）。
    用户已显式设置 HF_HUB_OFFLINE 时尊重原设置。返回是否处于离线模式。
    """
    prior = os.environ.get("HF_HUB_OFFLINE")
    if prior not in (None, "", "0", "false"):
        return True
    if model_names and all(hf_model_cached(n) for n in model_names):
        os.environ["HF_HUB_OFFLINE"] = "1"
        print("[rag_enhance] 模型离线加载（本地缓存齐全）", file=sys.stderr)
        return True
    print("[rag_enhance] 本地缓存不全——联网加载"
          "（国内网络可设 HF_ENDPOINT=https://hf-mirror.com）", file=sys.stderr)
    return False


# ============================================================
# 增强引擎（重依赖惰性加载）
# ============================================================

class EnhanceEngine:
    """增强检索引擎。

    level ∈ {dense, rerank, rewrite}（off 档不经本引擎·由核心引擎处理）。
    模型与向量产物在首次 retrieve_ranked 时惰性加载（进程内建议单例）。
    """

    def __init__(self, level, output_dir=None, device=None):
        if level not in ENGINE_LEVELS:
            raise ValueError("EnhanceEngine level 非法：%r（合法：%s）"
                             % (level, "|".join(ENGINE_LEVELS)))
        self.level = level
        self.output_dir = output_dir or OUTPUT_DIR
        self.device = (device or os.environ.get("RAG_DEVICE", "").strip() or "cpu")
        self._loaded = False
        self._np = None
        self._embedder = None
        self._reranker = None
        self._vectors = None
        self._path_by_idx = {}
        self._doc_rows = {}
        self._text_cache = {}

    # ---------- 加载 ----------

    def _product_paths(self):
        return {
            "vectors": os.path.join(self.output_dir, "rag_vectors.npy"),
            "chunks": os.path.join(self.output_dir, "rag_chunks.jsonl"),
            "meta": os.path.join(self.output_dir, "rag_embed_meta.json"),
        }

    def _ensure_loaded(self):
        if self._loaded:
            return
        paths = self._product_paths()
        missing = [p for p in paths.values() if not os.path.exists(p)]
        if missing:
            raise RuntimeError(
                "增强档（RAG_ENHANCE=%s）需要向量产物，缺失：%s。"
                "请先构建：python scripts/rag/build_vectors.py" % (self.level, "、".join(missing)))
        # 离线预置须在 import sentence-transformers 之前（huggingface_hub offline 为 import 期常量）
        need = [EMBED_MODEL] if self.level == "dense" else [EMBED_MODEL, RERANK_MODEL]
        offline = hf_offline_prepare(need)
        try:
            # sentence_transformers 必须先于 torch 导入（本机实测段错误坑）
            from sentence_transformers import CrossEncoder, SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "增强档（RAG_ENHANCE=%s）需要 sentence-transformers + numpy："
                "pip install sentence-transformers numpy" % self.level) from exc
        import numpy as np
        import torch

        torch.set_num_threads(4)  # CPU 限流（本机硬件纪律）

        with open(paths["chunks"], encoding="utf-8") as f:
            chunks = [json.loads(line) for line in f]
        vectors = np.load(paths["vectors"])
        if vectors.shape[0] != len(chunks):
            raise RuntimeError(
                "向量产物损坏：rag_vectors.npy 行数 %d ≠ rag_chunks.jsonl 记录数 %d"
                "——请重跑 build_vectors.py" % (vectors.shape[0], len(chunks)))
        self._path_by_idx, self._doc_rows = doc_rows_from_chunks(chunks)
        self._vectors = vectors
        self._np = np

        self._embedder = SentenceTransformer(EMBED_MODEL, device=self.device,
                                             local_files_only=offline)
        if self.level in ("rerank", "rewrite"):
            self._reranker = CrossEncoder(RERANK_MODEL, device=self.device,
                                          max_length=512, local_files_only=offline)

        self._check_stale(paths["meta"])
        self._loaded = True

    def _check_stale(self, meta_path):
        """构建指纹校验（非阻断）：docs/ 变化时告警提示重建。"""
        try:
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
            import xiyouji_rag as _rag
            n_now, m_now = docs_stat(_rag.DOCS_DIR)
            n_built = int(meta.get("docs_count", -1))
            if n_built >= 0 and (n_built != n_now
                                 or m_now > float(meta.get("docs_max_mtime", 0.0)) + 1.0):
                print("[rag_enhance] 警告：向量产物可能落后于 docs/（构建时 %d 篇 vs 现 %d 篇）"
                      "——增强检索结果可能缺最新文档；重跑 scripts/rag/build_vectors.py 可重建。"
                      % (n_built, n_now), file=sys.stderr)
        except Exception:
            pass

    # ---------- 检索 ----------

    def retrieve_ranked(self, query, top_k=5, index=None, bm25_retrieve=None):
        """增强检索排序 → [(path, score)]。

        score 语义：dense 档=RRF 融合分；rerank/rewrite 档=reranker 原始分。
        bm25_retrieve 由核心引擎注入（依赖注入·避免模块环依赖）。
        """
        if bm25_retrieve is None:
            raise ValueError("retrieve_ranked 需要 bm25_retrieve（核心引擎的现役 BM25 检索函数）")
        self._ensure_loaded()
        bm = [s["path"] for s in bm25_retrieve(query, top_k=POOL_TOP, index=index)]
        dn = self._dense_order(query)
        fused = rrf_fuse([bm, dn], weights=(1.0, DENSE_WEIGHT))
        pool = [p for p, _ in fused[:POOL_K]]
        rank_query = query
        if self.level == "rewrite":
            rewritten = ""
            if should_rewrite(query):
                rewritten = self._rewrite(query)
            else:
                print("[rag_enhance] 智能路由：短实体查询→主链（跳过改写）", file=sys.stderr)
            if rewritten:
                bm2 = [s["path"] for s in bm25_retrieve(rewritten, top_k=POOL_TOP, index=index)]
                dn2 = self._dense_order(rewritten)
                fused2 = rrf_fuse([bm2, dn2], weights=(1.0, DENSE_WEIGHT))
                pool = merge_pools(pool, [p for p, _ in fused2[:POOL_K]])
                rank_query = rewritten
        if self.level in ("rerank", "rewrite"):
            return self._rerank(rank_query, pool)[:top_k]
        return [(p, round(sc, 4)) for p, sc in fused[:top_k]]

    def _dense_order(self, qtext):
        """稠密召回：查询嵌入 → 页级 max 相似度 → top POOL_TOP 路径序。"""
        qv = self._embedder.encode([QUERY_INSTRUCTION + qtext], normalize_embeddings=True)[0]
        sims = self._vectors @ qv
        best = {di: float(sims[rows].max()) for di, rows in self._doc_rows.items()}
        order = sorted(best.items(), key=lambda x: -x[1])[:POOL_TOP]
        return [self._path_by_idx[di] for di, _ in order]

    def _rerank(self, qtext, pool):
        """cross-encoder 重排（v1 配方：文档首 800 字导语）→ [(path, score)]。"""
        texts = [self._intro(p) for p in pool]
        scores = self._reranker.predict([(qtext, t) for t in texts], batch_size=RERANK_BATCH)
        ranked = sorted(zip(pool, scores, strict=True), key=lambda x: -x[1])
        return [(p, round(float(s), 4)) for p, s in ranked]

    def _intro(self, path):
        """文档首 INTRO_CHARS 字导语（v1 配方文本·进程内缓存）。"""
        if path not in self._text_cache:
            try:
                with open(os.path.join(ROOT, path), encoding="utf-8") as f:
                    self._text_cache[path] = f.read()[:INTRO_CHARS]
            except Exception:
                self._text_cache[path] = ""
        return self._text_cache[path]

    def _rewrite(self, query):
        """LLM 查询改写（复用核心引擎 provider 体系）。失败/缺 key → ""（回退原查询）。"""
        key = os.environ.get("LLM_API_KEY", "").strip()
        if not key:
            print("[rag_enhance] RAG_ENHANCE=rewrite 需要 LLM_API_KEY；本次回退原查询。",
                  file=sys.stderr)
            return ""
        try:
            import xiyouji_rag as _rag
            base, fmt = _rag._resolve_endpoint()
            if not _rag._validate_endpoint(base):
                raise ValueError("LLM 端点不合法（P2-2）")
            model = os.environ.get("LLM_MODEL", "").strip() or "gpt-4o-mini"
            msgs = build_rewrite_messages(query)
            if fmt == "anthropic":
                raw = _rag._call_anthropic(base, model, key, msgs)
            else:
                raw = _rag._call_openai(base, model, key, msgs)
            return clean_rewrite(raw)
        except Exception as exc:
            print("[rag_enhance] 查询改写失败（回退原查询）：%s" % exc, file=sys.stderr)
            return ""
