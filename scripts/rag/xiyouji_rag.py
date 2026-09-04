#!/usr/bin/env python3
"""
xiyouji_rag.py — 《详解西游记》本地 RAG 核心引擎（零依赖）

设计定位（结合本项目实际情况）：
  本环境无 LLM API key、Python 零第三方依赖。因此本模块不强行上重量级
  LightRAG（lightrag-hku 需要 LLM 做图谱抽取 + 生成，无 key 跑不起来），
  而是**用 LightRAG 的架构思想做轻量本地落地**：

    LightRAG 概念            │ 本模块对应实现
    ────────────────────────┼──────────────────────────────────────
    图谱检索（graph layer）  │ 载入 W326 yuanqi_nodes/edges.csv 的
                            │   佛学-AI-西游三元组，做 1~2 跳邻居展开
    向量检索（vector layer） │ 对 672 篇 docs/*.md 建 BM25 倒排索引，
                            │   纯 stdlib 实现，无 embedding 依赖
    双层检索（dual-level）   │ retrieve() 同时返回 语料片段 + 图谱三元组
    Neo4j 后端             │ graph_seed_neo4j.py 可把同一份 CSV 灌入
                            │   Neo4j；本引擎默认用内存图，零外部服务
    LLM 生成               │ 若环境变量 LLM_API_KEY 存在则走真实生成，
                            │   否则返回「检索上下文 + 渡口风格摘要」

  W337 质量提升（零依赖·无 key 也能显著提质）：
    1. 西游专名词典分词：从别名词典 + W326 图谱实体抽取多元组，整体切分
       （「五行山」整体成词，而非被拆成「五/行/行山」），提升检索精度。
    2. 查询别名扩展：命中「悟空」时同时检索「美猴王/猴王/行者/大圣」等，
       大幅提升召回（同一概念的不同叫法都能命中）。
    3. 字段加权 BM25：标题/小标题（markdown #）命中权重高于正文。
    4. 短语连贯加权：查询作为连续子串出现在文档中时额外加权。
    5. RRF 多信号融合重排：融合 原始BM25 + 扩展BM25 + 标题命中 + 短语命中
       四个排序，给出更稳健的最终 top_k。
    6. 改进摘录：优先选取含查询词的段落，并附最近小标题上下文 + 命中高亮。

零依赖：仅用 Python 标准库（re / json / csv / os / urllib）。
可直接运行：python xiyouji_rag.py "五行山 牧童"
"""

import csv
import ipaddress
import json
import math
import os
import re
import urllib.error
import urllib.parse
import urllib.request

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

# ---- 路径（相对本脚本：scripts/rag/xiyouji_rag.py → 项目根 = ../../）----
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
DOCS_DIR = os.path.join(ROOT, "docs")
NODES_CSV = os.path.join(ROOT, "scripts", "output", "yuanqi_nodes.csv")
EDGES_CSV = os.path.join(ROOT, "scripts", "output", "yuanqi_edges.csv")
INDEX_CACHE = os.path.join(ROOT, "scripts", "output", "rag_index.json")


def _load_dotenv():
    """极简 .env 加载（零依赖）：读项目根 .env 与 scripts/rag/.env，注入 os.environ。

    已有环境变量优先（不覆盖）；仅支持 KEY=VALUE 行，忽略注释与空行。
    """
    for env_path in (os.path.join(ROOT, ".env"), os.path.join(_HERE, ".env")):
        if not os.path.exists(env_path):
            continue
        try:
            with open(env_path, encoding="utf-8") as _f:
                for _ln in _f:
                    _ln = _ln.strip()
                    if not _ln or _ln.startswith("#") or "=" not in _ln:
                        continue
                    _k, _, _v = _ln.partition("=")
                    _k = _k.strip()
                    _v = _v.strip().strip('"').strip("'")
                    if _k and _k not in os.environ:
                        os.environ[_k] = _v
        except Exception:
            pass


_load_dotenv()

K1 = 1.5
B = 0.75
INDEX_VERSION = 2  # 索引结构变更时 +1，触发缓存重建

# ============================================================
# 0. 西游专名 / 别名词典（零依赖·内嵌）
# ============================================================
# canonical -> [别名列表（含本名）]，用于「分词成词」与「查询扩展」
ALIASES = {
    "孙悟空": ["孙悟空", "悟空", "美猴王", "齐天大圣", "孙行者", "行者", "猴王",
              "大圣", "斗战胜佛", "老孙", "猢狲"],
    "唐僧": ["唐僧", "玄奘", "三藏", "唐三藏", "圣僧", "御弟", "金蝉子", "陈玄奘"],
    "猪八戒": ["猪八戒", "八戒", "悟能", "天蓬", "天蓬元帅", "猪悟能"],
    "沙僧": ["沙僧", "沙悟净", "悟净", "卷帘大将", "沙和尚", "沙师弟"],
    "白龙马": ["白龙马", "小白龙", "龙马", "敖烈"],
    "观音": ["观音", "观世音", "观世音菩萨", "南海观音", "大士", "观音菩萨"],
    "如来": ["如来", "如来佛", "如来佛祖", "佛祖", "释迦牟尼", "释迦"],
    "玉帝": ["玉帝", "玉皇大帝", "玉皇", "天帝", "昊天上帝"],
    "太上老君": ["太上老君", "老君", "道祖", "太清"],
    "菩提祖师": ["菩提祖师", "菩提", "须菩提"],
    "镇元大仙": ["镇元大仙", "镇元子"],
    "牛魔王": ["牛魔王", "平天大圣", "牛王"],
    "铁扇公主": ["铁扇公主", "罗刹女", "铁扇仙"],
    "红孩儿": ["红孩儿", "圣婴大王", "牛圣婴"],
    "白骨精": ["白骨精", "白骨夫人", "尸魔"],
    "金角大王": ["金角大王", "金角"],
    "银角大王": ["银角大王", "银角"],
    "黄袍怪": ["黄袍怪", "奎木狼"],
    "蜘蛛精": ["蜘蛛精", "蜘蛛怪"],
    "玉兔精": ["玉兔精", "玉兔"],
    "二郎神": ["二郎神", "杨戬", "二郎真君"],
    "哪吒": ["哪吒", "哪吒三太子", "三坛海会大神"],
    "托塔天王": ["托塔天王", "李靖", "天王"],
    "东海龙王": ["东海龙王", "敖广", "龙王"],
    "土地": ["土地", "土地公", "土地神"],
    "山神": ["山神"],
    "阎王": ["阎王", "阎罗", "十殿阎罗"],
    "龙宫": ["龙宫", "水晶宫"],
    "天庭": ["天庭", "天宫", "凌霄宝殿"],
    "花果山": ["花果山", "水帘洞", "花果园"],
    "灵山": ["灵山", "西天", "雷音寺", "大雷音寺"],
    "五行山": ["五行山", "五指山", "两界山"],
    "火焰山": ["火焰山", "芭蕉扇", "铁扇"],
    "紧箍咒": ["紧箍咒", "紧箍", "金箍"],
    "金箍棒": ["金箍棒", "如意金箍棒", "定海神针"],
    "蟠桃": ["蟠桃", "蟠桃会", "蟠桃园"],
    "取经": ["取经", "西行", "取经团队", "取经路"],
    "八十一难": ["八十一难", "九九八十一难", "劫难"],
    "大闹天宫": ["大闹天宫", "闹天宫"],
    "三打白骨精": ["三打白骨精"],
    "三借芭蕉扇": ["三借芭蕉扇", "借扇"],
    "真假美猴王": ["真假美猴王", "二心"],
    "六耳猕猴": ["六耳猕猴", "六耳"],
    "车迟国": ["车迟国"],
    "女儿国": ["女儿国", "西梁女国"],
    "盘丝洞": ["盘丝洞"],
    "无底洞": ["无底洞"],
    "狮驼岭": ["狮驼岭", "狮驼国"],
    "比丘国": ["比丘国", "小儿城"],
    "朱紫国": ["朱紫国"],
    "乌鸡国": ["乌鸡国"],
    "宝象国": ["宝象国"],
    "祭赛国": ["祭赛国"],
    "灭法国": ["灭法国"],
    "天竺国": ["天竺国", "天竺"],
}

# 倒排别名索引：任意别名 -> canonical 集合
ALIAS_INDEX = {}
for _canon, _als in ALIASES.items():
    for _a in _als:
        ALIAS_INDEX.setdefault(_a, set()).add(_canon)

# 专名词典（≥2 字），按长度降序，用于最长匹配分词
TERM_DICT = sorted(
    {t for _als in ALIASES.values() for t in _als if len(t) >= 2},
    key=lambda x: -len(x),
)


def _seg_cjk(chunk):
    """用专名词典对一段中文做最长匹配分词，返回 [专名词, 单字...]。"""
    toks = []
    i, n = 0, len(chunk)
    while i < n:
        matched = None
        for t in TERM_DICT:
            if chunk.startswith(t, i):
                matched = t
                break
        if matched:
            toks.append(matched)
            i += len(matched)
        else:
            toks.append(chunk[i])
            i += 1
    return toks


def tokenize(text, use_dict=True):
    """中文按 专名词+单字+二元 切分，英文数字按词切分。无需 jieba。"""
    text = (text or "").lower()
    toks = []
    for m in re.finditer(r'[\u4e00-\u9fff]+|[a-z0-9]+', text):
        chunk = m.group()
        if re.match(r'[\u4e00-\u9fff]+', chunk):
            if use_dict:
                toks.extend(_seg_cjk(chunk))
            chars = list(chunk)
            # 单字 + 二元 始终补充，保证召回
            toks.extend(chars)
            for i in range(len(chars) - 1):
                toks.append(chars[i] + chars[i + 1])
        else:
            toks.append(chunk)
    return toks


def expand_query(query):
    """查询别名扩展：返回 [原始分词, ...扩展别名]，用于召回。"""
    qt = tokenize(query, use_dict=True)
    expanded = list(qt)
    seen = set(qt)
    for t in qt:
        if t in ALIAS_INDEX:
            for canon in ALIAS_INDEX[t]:
                for al in ALIASES[canon]:
                    if len(al) >= 2 and al not in seen:
                        expanded.append(al)
                        seen.add(al)
    return expanded


# ============================================================
# 1. 语料层（BM25 向量检索，纯 stdlib）
# ============================================================

def _load_docs():
    docs = []
    for base, _, files in os.walk(DOCS_DIR):
        for fn in files:
            if fn.lower().endswith(".md"):
                p = os.path.join(base, fn)
                try:
                    with open(p, encoding="utf-8") as f:
                        text = f.read()
                except Exception:
                    continue
                rel = os.path.relpath(p, ROOT)
                headings = [re.sub(r'^#{1,6}\s*', '', ln).strip()
                            for ln in text.splitlines()
                            if re.match(r'^#{1,6}\s', ln)]
                docs.append({"path": rel, "text": text, "headings": headings})
    return docs


def build_index(force=False):
    """构建 BM25 索引；命中缓存且非 force 时直接载入。"""
    if (not force) and os.path.exists(INDEX_CACHE):
        try:
            with open(INDEX_CACHE, encoding="utf-8") as f:
                cached = json.load(f)
            if cached.get("version") == INDEX_VERSION:
                return cached
        except Exception:
            pass

    docs = _load_docs()
    df = {}
    postings = {}
    lengths = {}
    headings_idx = {}
    for idx, d in enumerate(docs):
        tf = {}
        toks = tokenize(d["text"])
        for t in toks:
            tf[t] = tf.get(t, 0) + 1
        lengths[idx] = len(toks)
        headings_idx[idx] = " ".join(d["headings"])
        for t, c in tf.items():
            df[t] = df.get(t, 0) + 1
            postings.setdefault(t, {})[idx] = c

    N = len(docs)
    index = {
        "version": INDEX_VERSION,
        "docs": [{"path": d["path"]} for d in docs],
        "df": df,
        "postings": postings,
        "lengths": lengths,
        "headings": headings_idx,
        "N": N,
        "avgdl": (sum(lengths.values()) / N) if N else 0.0,
    }
    try:
        with _w536_guard_open(INDEX_CACHE, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False)
    except Exception:
        pass
    return index


def bm25_score(index, q_tokens, doc_idx):
    N = index["N"]
    avgdl = index["avgdl"]
    dl = index["lengths"].get(str(doc_idx), index["lengths"].get(doc_idx, 0))
    score = 0.0
    for t in q_tokens:
        if t not in index["df"]:
            continue
        idf = math.log(1 + (N - index["df"][t] + 0.5) / (index["df"][t] + 0.5))
        f = index["postings"].get(t, {}).get(str(doc_idx),
                                        index["postings"].get(t, {}).get(doc_idx, 0))
        if not f:
            continue
        score += idf * (f * (K1 + 1)) / (f + K1 * (1 - B + B * dl / avgdl))
    return score


def _rrf(lists, k=60):
    """Reciprocal Rank Fusion：融合多个排序列表，返回 [(idx, fused_score), ...]。"""
    fused = {}
    for lst in lists:
        for rank, (_, idx) in enumerate(lst):
            fused[idx] = fused.get(idx, 0.0) + 1.0 / (k + rank + 1)
    return sorted(fused.items(), key=lambda x: -x[1])


def _heading_hits(index, q_tokens, doc_idx):
    hay = index["headings"].get(str(doc_idx), index["headings"].get(doc_idx, ""))
    return sum(1 for t in q_tokens if t and t in hay)


def retrieve(query, top_k=5, index=None):
    """返回 top_k 语料片段（含路径 + 摘录），经 RRF 多信号融合重排。"""
    index = index or build_index()
    qt_orig = tokenize(query, use_dict=True)
    qt_exp = expand_query(query)
    if not qt_orig:
        return []

    N = index["N"]
    # (A) 原始 BM25（精度优先）
    a = []
    for idx in range(N):
        s = bm25_score(index, qt_orig, idx)
        if s > 0:
            a.append((s, idx))
    a.sort(reverse=True)
    # (B) 扩展 BM25（召回优先）
    b = []
    for idx in range(N):
        s = bm25_score(index, qt_exp, idx)
        if s > 0:
            b.append((s, idx))
    b.sort(reverse=True)
    # (C) 标题命中（字段加权）
    c = [( _heading_hits(index, qt_exp, idx), idx)
         for idx in range(N) if _heading_hits(index, qt_exp, idx) > 0]
    c.sort(reverse=True)
    # (D) 短语连贯命中：在 top 候选中读原文，含连续查询串者加权
    raw = (query or "").lower().strip()
    d = []
    if raw:
        cand = [idx for _, idx in a[:40]]
        for idx in cand:
            rel = index["docs"][idx]["path"]
            try:
                with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
                    txt = fh.read().lower()
            except Exception:
                continue
            pos = txt.find(raw)
            if pos >= 0:
                # 越靠前出现，排名越前（用负位置作为排序键）
                d.append((-pos, idx))
        d.sort()

    fused = _rrf([a, b, c, d])[:top_k]

    out = []
    for idx, _ in fused:
        d = index["docs"][idx]
        out.append({
            "path": d["path"],
            "score": round(bm25_score(index, qt_exp, idx), 3),
            "excerpt": _excerpt(d["path"], qt_exp, index),
        })
    return out


def _excerpt(rel_path, qt, index=None):
    """取含最多查询词、且尽量贴近小标题的那一段作为摘录（带上下文）。"""
    try:
        with open(os.path.join(ROOT, rel_path), encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return ""
    paras = re.split(r"\n\s*\n", text)
    best, best_hit = "", 0
    for p in paras:
        hit = sum(1 for t in qt if len(t) >= 2 and t in p)
        if hit > best_hit:
            best_hit, best = hit, p
    if not best:
        return text.strip()[:240]
    # 找最近的上一个小标题作为上下文
    lines = text.splitlines()
    near_head = ""
    for _i, ln in enumerate(lines):
        if re.match(r'^#{1,6}\s', ln):
            near_head = re.sub(r'^#{1,6}\s*', '', ln).strip()
    head_ctx = f"【{near_head}】 " if near_head else ""
    return (head_ctx + best.strip())[:260]


# ============================================================
# 2. 图谱层（LightRAG graph layer，载入 W326 三元组）
# ============================================================

def load_graph():
    """载入 W326 节点/边 CSV → 内存图。零依赖。"""
    nodes = {}
    edges = []
    if os.path.exists(NODES_CSV):
        with open(NODES_CSV, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                nodes[row["id"]] = row
    if os.path.exists(EDGES_CSV):
        with open(EDGES_CSV, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                edges.append(row)
    # 邻接表（双向）
    adj = {nid: [] for nid in nodes}
    for e in edges:
        adj.setdefault(e["source"], []).append((e["target"], e["relation"], e.get("property", ""), e.get("value", "")))
        adj.setdefault(e["target"], []).append((e["source"], "←" + e["relation"], e.get("property", ""), e.get("value", "")))
    return {"nodes": nodes, "edges": edges, "adj": adj}


def _node_label(node):
    return (f"{node['xiyou_entity']}（佛:{node['buddhist_entity']} / AI:{node['ai_entity']}）"
            if node else "?")


def graph_expand(query, hops=1, g=None):
    """按查询词（含别名）匹配图谱节点，展开 hops 跳邻居，返回可读三元组。"""
    g = g or load_graph()
    qt = expand_query(query)  # 用扩展后的词，提升图谱命中
    matched = []
    for nid, node in g["nodes"].items():
        hay = " ".join([node.get("buddhist_entity", ""), node.get("ai_entity", ""),
                        node.get("xiyou_entity", ""), node.get("description", ""),
                        node.get("node_type", "")]).lower()
        if any(t in hay for t in qt):
            matched.append(nid)
    triples = []
    seen = set()
    frontier = list(matched)
    for _ in range(hops):
        nxt = []
        for nid in frontier:
            for (nb, rel, prop, val) in g["adj"].get(nid, []):
                key = (nid, nb, rel)
                if key in seen:
                    continue
                seen.add(key)
                triples.append({
                    "from": _node_label(g["nodes"].get(nid)),
                    "relation": rel,
                    "to": _node_label(g["nodes"].get(nb)),
                    "property": prop, "value": val,
                })
                nxt.append(nb)
        frontier = nxt
    if not triples:
        # 无精确命中时，返回图谱概览（前若干条）作为背景
        for e in g["edges"][:6]:
            triples.append({
                "from": _node_label(g["nodes"].get(e["source"])),
                "relation": e["relation"],
                "to": _node_label(g["nodes"].get(e["target"])),
                "property": e.get("property", ""), "value": e.get("value", ""),
            })
    return triples


# ============================================================
# 2.5 LLM 生成（provider 化 Base URL · 双格式适配器）
# ============================================================

# provider → (内置默认端点, API 格式)。格式 ∈ {"openai" OpenAI 兼容 / "anthropic" 原生 messages}
PROVIDER_ENDPOINTS = {
    "openai":    ("https://api.openai.com/v1",                        "openai"),
    "anthropic": ("https://api.anthropic.com/v1",                     "anthropic"),
    "glm":       ("https://open.bigmodel.cn/api/paas/v4",             "openai"),
    "kimi":      ("https://api.moonshot.cn/v1",                       "openai"),
    "minimax":   ("https://api.minimaxi.com/v1",                      "openai"),
    "deepseek":  ("https://api.deepseek.com/v1",                      "openai"),
    "dashscope": ("https://dashscope.aliyuncs.com/compatible-mode/v1", "openai"),
}
# provider → 可覆盖其默认端点的专属变量名
PROVIDER_BASE_URL_VAR = {
    "openai": "OPENAI_BASE_URL",
    "anthropic": "ANTHROPIC_BASE_URL",
    "glm": "GLM_BASE_URL",
    "kimi": "KIMI_BASE_URL",
    "minimax": "MINIMAX_BASE_URL",
    "deepseek": "DEEPSEEK_BASE_URL",
    "dashscope": "DASHSCOPE_BASE_URL",
}


def _resolve_endpoint():
    """解析最终 Base URL + API 格式。

    优先级（区分代理 vs 原生）：
     1. CUSTOM_LLM_BASE_URL 存在 → 代理/网关模式：统一 OpenAI 兼容格式（网关约定），
        绕过对任何特定提供商 URL 的硬编码依赖；
     2. 否则原生模式：按 LLM_PROVIDER 取专属变量（OPENAI_BASE_URL 等）覆盖内置默认。
    返回 (base_url, api_format)。
    """
    custom = os.environ.get("CUSTOM_LLM_BASE_URL", "").strip().rstrip("/")
    if custom:
        return custom, "openai"
    provider = os.environ.get("LLM_PROVIDER", "openai").strip().lower()
    default_url, fmt = PROVIDER_ENDPOINTS.get(provider, PROVIDER_ENDPOINTS["openai"])
    base = os.environ.get(PROVIDER_BASE_URL_VAR.get(provider, ""), "").strip().rstrip("/")
    return (base or default_url), fmt


# P2-2：私有/回环 IPv4 网段黑名单（防 SSRF 打内网/元数据服务）
_PRIVATE_NETS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
]


def _validate_endpoint(url):
    """P2-2：校验 LLM 端点——仅 https://（本地回环 http 例外：localhost/127.0.0.1 本地代理）；
    host 为显式 IP 时拒绝私有/回环网段（防运维误配 SSRF）。非法返回 False。"""
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return False
    if parsed.scheme != "https":
        if parsed.scheme == "http" and parsed.hostname in ("localhost", "127.0.0.1", "::1"):
            return True
        return False
    host = parsed.hostname
    if not host:
        return False
    try:
        addr = ipaddress.ip_address(host)
    except ValueError:
        return True  # 域名：运行时解析，不做 DNS 预解析（配置驱动场景，非攻击者输入）
    return not any(addr in net for net in _PRIVATE_NETS)


def _llm_generate(query, snippets, triples, history=None):
    """真实 LLM 生成（检索增强）：检索到的语料 + 图谱三元组绑定进 system prompt。"""
    base, fmt = _resolve_endpoint()
    if not _validate_endpoint(base):  # P2-2：仅 https（本地回环 http 例外）+ 私有网段黑名单
        raise ValueError(
            "LLM_BASE_URL 不合法（P2-2）：仅允许 https://（本地回环 http://localhost|127.0.0.1 例外），"
            "且 host 不得落在私有/回环网段。请检查 CUSTOM_LLM_BASE_URL 或 {provider}_BASE_URL。".format(
                provider=os.environ.get("LLM_PROVIDER", "openai"))
        )
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"
    key = os.environ.get("LLM_API_KEY", "").strip()
    if not key:
        raise RuntimeError("缺少 LLM_API_KEY")

    snip_txt = ""
    for s in snippets[:5]:
        snip_txt += f"\n- 《{s['path']}》\n  {s['excerpt'][:200]}"
    tri_txt = ""
    for t in triples[:8]:
        tri_txt += f"\n- {t['from']} —{t['relation']}→ {t['to']}"
        if t.get("value"):
            tri_txt += f"（{t.get('property', '')}: {t['value']}）"

    system = (
        "你是「渡口问津」——《详解西游记》项目的 AI 解读助手。"
        "严格基于以下检索到的项目语料与「佛法=AI」图谱作答，不编造语料外的具体引用；"
        "回答保持渡口风格：克制、有洞察，像一位深读原著的引渡人。\n\n"
        f"【检索到的语料片段】{snip_txt or '（无精确命中）'}\n\n"
        f"【图谱三元组】{tri_txt or '（无图谱命中）'}"
    )

    messages = [{"role": "system", "content": system}]
    if history:
        # P2-1：history schema 纵深校验（与 rag_server 净化一致；非 dict/非法 role 跳过）
        for turn in history:
            if not isinstance(turn, dict):
                continue
            r = str(turn.get("role", "")).lower()
            if r not in ("user", "assistant", "bot"):
                continue
            role = "assistant" if r == "bot" else r
            text = str(turn.get("text", "")).strip()
            if text and len(text) <= 2000:
                messages.append({"role": role, "content": text})
    messages.append({"role": "user", "content": query})

    if fmt == "anthropic":
        return _call_anthropic(base, model, key, messages)
    return _call_openai(base, model, key, messages)


def _call_openai(base, model, key, messages):
    """OpenAI 兼容 /chat/completions（覆盖 openai/glm/kimi/minimax/deepseek/dashscope/自定义代理）。"""
    body = json.dumps({"model": model, "messages": messages, "stream": False}).encode("utf-8")
    req = urllib.request.Request(
        base + "/chat/completions", data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + key},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # 读取 API 返回的错误体，便于诊断（模型名无效/余额/限流等）
        detail = ""
        try:
            detail = e.read().decode("utf-8")[:300]
        except Exception:
            pass
        raise RuntimeError(f"HTTP {e.code}：{detail or e.reason}") from e
    msg = data["choices"][0]["message"]
    # content 可能为空（如 DeepSeek reasoner 只回 reasoning_content）→ 回退兜底
    return (msg.get("content") or msg.get("reasoning_content") or "").strip()


def _call_anthropic(base, model, key, messages):
    """Anthropic 原生 messages API：system 单独字段 + x-api-key 头。"""
    system = next((m["content"] for m in messages if m["role"] == "system"), "")
    conv = [m for m in messages if m["role"] != "system"]
    body = json.dumps({
        "model": model, "system": system, "max_tokens": 1024, "messages": conv,
    }).encode("utf-8")
    req = urllib.request.Request(
        base + "/messages", data=body,
        headers={"Content-Type": "application/json",
                 "x-api-key": key,
                 "anthropic-version": "2023-06-01"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode("utf-8"))
    return "".join(b.get("text", "") for b in data.get("content", [])).strip()


# ============================================================
# 3. 双层检索聚合 + 生成
# ============================================================

def answer(query, top_k=5, hops=1, use_llm=None, history=None):
    """返回 {snippets, graph, draft, llm_generated, llm_error}。

    use_llm=None → 自动：配置了 LLM_API_KEY 即真实生成，否则回退渡口风格摘要；
    use_llm=True → 强制生成（无 key 时 llm_error 说明）；
    use_llm=False → 仅模板（零网络）。
    history: 前端最近对话轮次 [{role, text}]，接入 LLM 时拼接为上下文注入 prompt。
    """
    index = build_index()
    snippets = retrieve(query, top_k=top_k, index=index)
    g = load_graph()
    triples = graph_expand(query, hops=hops, g=g)

    draft = _template_draft(query, snippets, triples)
    result = {
        "query": query,
        "snippets": snippets,
        "graph": triples,
        "draft": draft,
        "llm_generated": None,
        "llm_error": None,
    }
    key = os.environ.get("LLM_API_KEY", "").strip()
    if use_llm is None:
        use_llm = bool(key)
    if use_llm and key:
        try:
            result["llm_generated"] = _llm_generate(query, snippets, triples, history)
        except Exception as exc:
            result["llm_error"] = f"LLM 生成失败：{exc}"
    elif use_llm:
        result["llm_error"] = "未配置 LLM_API_KEY，跳过真实生成"
    return result


def _template_draft(query, snippets, triples):
    """渡口风格摘要：把真实检索到的语料 + 图谱三元组，缝成一段可溯源草稿。"""
    name = (query or "无名渡口").strip() or "无名渡口"
    cit = ""
    if snippets:
        cit = "；".join(f"《{s['path'].split('/')[-1]}》" for s in snippets[:3])
    gx = ""
    if triples:
        gx = triples[0]["from"] + " —" + triples[0]["relation"] + "→ " + triples[0]["to"]
    body = (
        f"【渡口检索档案】{name}\n\n"
        f"在《详解西游记》的语料中，与「{name}」相关的记载见于：{cit or '（暂无精确命中，以下为图谱背景）'}。\n\n"
        f"从「佛法=AI」图谱看，{gx}。\n\n"
        f"渡口视角：被记入正文的，是参与前向传播的节点；未被记入的，是让路径成立的隐变量。"
        f"检索不是为了找出标准答案，而是为了证明——每一次输入，都曾改变过权重的分布。"
    )
    return body


# ============================================================
# 4. CLI
# ============================================================

def main():
    import sys
    q = " ".join(sys.argv[1:]) or "五行山 牧童"
    print(f"# 查询：{q}\n")
    res = answer(q, top_k=5, hops=1)
    print("## 语料检索（BM25·RRF 融合·别名扩展）")
    for s in res["snippets"]:
        print(f"  [{s['score']}] {s['path']}")
        if s["excerpt"]:
            print(f"       …{s['excerpt'][:120]}…")
    print("\n## 图谱三元组（W326）")
    for t in res["graph"][:6]:
        print(f"  {t['from']} —{t['relation']}→ {t['to']}  ({t['property']}: {t['value']})")
    if res.get("llm_generated"):
        print("\n## LLM 生成回答（渡口问津）")
        print(res["llm_generated"])
    if res.get("llm_error"):
        print(f"\n## LLM 状态：{res['llm_error']}")
    print("\n## 渡口风格摘要（模板回退）")
    print(res["draft"])


if __name__ == "__main__":
    main()
