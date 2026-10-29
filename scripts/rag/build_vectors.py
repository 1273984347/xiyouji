"""
build_vectors.py — 构建稠密检索向量产物（W744·供 rag_enhance 增强档使用）

流程：
  1. 分块：复用 xiyouji_rag._load_docs()（与 BM25 同一语料），按 T-01 口径
     分块（≤380 字/块·去 YAML frontmatter·超长段按句硬切）；
  2. 嵌入：BAAI/bge-small-zh-v1.5（标题前缀 + L2 归一），微批 + 冷却 +
     温度守护（硬件安全模式——本机笔记本有 GPU 重负载保护性关机前科）；
  3. 汇总：scripts/output/rag_vectors.npy + rag_chunks.jsonl + rag_embed_meta.json。

硬件安全模式（仅 GPU）：每批 1500 块（约 3 秒），批间冷却 35 秒（温度 ≥85°C
延长至 60 秒·≥90°C 自动中止）；逐批存盘可断点续跑。CPU 模式无冷却、限 4 线程。

用法（本机：py 启动器按 3.12 运行）：
  py -3.12 scripts/rag/build_vectors.py               # auto 设备（默认·安全模式）
  py -3.12 scripts/rag/build_vectors.py --device cpu  # 强制 CPU（较慢·无 GPU 风险）
  py -3.12 scripts/rag/build_vectors.py --rebuild     # 分块变化后全量重建

注意：本脚本是重计算任务（首次运行还会下载模型约 92 MiB／≈96 MB）。请勿并行多开；
GPU 模式运行期间勿再挂其他重负载（本机散热纪律）。
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import rag_enhance  # noqa: E402 —— 常量与 docs_stat 单一事实源（顶层零重依赖）
import xiyouji_rag  # noqa: E402 —— _load_docs（与 BM25 同语料）

ROOT = rag_enhance.ROOT
OUT = rag_enhance.OUTPUT_DIR
PARTS = os.path.join(OUT, "rag_vectors_parts")
MANIFEST = os.path.join(PARTS, "manifest.json")

CHUNK_MAX = 380       # T-01 分块口径
CHUNK_MIN = 20
TEMPERATURE_WARN = 85.0
TEMPERATURE_ABORT = 90.0
COOL_HOT = 60.0       # 温度 ≥WARN 时的延长冷却


# ============================================================
# 分块（复刻 T-01 prep_corpus 口径·同语料同算法）
# ============================================================

def title_of(doc):
    for h in doc["headings"]:
        h = h.strip()
        if h:
            return h
    return os.path.splitext(os.path.basename(doc["path"]))[0]


def clean_body(text):
    t = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)  # 去 YAML frontmatter
    return t.replace("\r\n", "\n").replace("\r", "\n")


def split_long(p):
    """超长段按句硬切为 <=CHUNK_MAX 片段。"""
    pieces, buf = [], ""
    for s in re.split(r"(?<=[。！？；!?;])", p):
        if not s:
            continue
        if len(buf) + len(s) > CHUNK_MAX and buf:
            pieces.append(buf)
            buf = s
        else:
            buf += s
        while len(buf) > CHUNK_MAX:
            pieces.append(buf[:CHUNK_MAX])
            buf = buf[CHUNK_MAX:]
    if buf:
        pieces.append(buf)
    return [x.strip() for x in pieces if x.strip()]


def chunk_doc(doc):
    """单文档 → [(path, title, text)]（段落聚合·短块合并·保 T-01 口径）。"""
    title = title_of(doc)
    body = clean_body(doc["text"])
    lst, buf = [], ""
    for p in [x.strip() for x in re.split(r"\n\s*\n", body) if x.strip()]:
        if len(p) > CHUNK_MAX:
            if buf:
                lst.append((doc["path"], title, buf))
                buf = ""
            for piece in split_long(p):
                lst.append((doc["path"], title, piece))
            continue
        if len(buf) + len(p) + 1 > CHUNK_MAX and buf:
            lst.append((doc["path"], title, buf))
            buf = p
        else:
            buf = buf + "\n" + p if buf else p
    if buf:
        lst.append((doc["path"], title, buf))
    kept = [x for x in lst if len(x[2]) >= CHUNK_MIN] or (lst[:1] if lst else [])
    if not kept:
        t = clean_body(doc["text"]).strip() or title_of(doc)
        kept = [(doc["path"], title_of(doc), t[:CHUNK_MAX])]
    return kept


def build_chunks(docs):
    chunks = []
    for i, d in enumerate(docs):
        for path, title, text in chunk_doc(d):
            chunks.append({
                "chunk_id": "c%05d" % len(chunks), "doc_idx": i,
                "path": path, "title": title, "text": text,
            })
    return chunks


def chunks_sha1(chunks):
    """分块列表规范化 sha1（manifest/meta 记录·防跨快照续跑混批）。"""
    h = hashlib.sha1()
    for c in chunks:
        h.update(json.dumps(c, ensure_ascii=False, sort_keys=True).encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def build_texts(chunks):
    """嵌入文本 = 标题 + 换行 + 正文（实验口径 title_prefixed=True）。"""
    return [(c["title"] + "\n" + c["text"]) if c.get("title") else c["text"]
            for c in chunks]


# ============================================================
# parts 目录管理（断点续跑·manifest 校验）
# ============================================================

def _write_manifest(count, sha, slice_n, device):
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump({
            "count": count, "slice": slice_n, "chunk_max": CHUNK_MAX,
            "model": rag_enhance.EMBED_MODEL, "chunks_sha1": sha, "device": device,
        }, f, ensure_ascii=False, indent=2)


def decide_resume(args, count, sha):
    """决定续跑 / 新建 / 重建（防跨快照混批）。不合法组合 → SystemExit。"""
    if args.rebuild and os.path.exists(PARTS):
        bak = PARTS + ".bak-" + time.strftime("%Y%m%d-%H%M%S")
        os.rename(PARTS, bak)
        print("REBUILD：旧 parts 已备份为 %s/（可手动删除）" % bak, flush=True)
    mf = None
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding="utf-8") as f:
            mf = json.load(f)
    if mf is None:
        if os.path.exists(PARTS) and any(fn.startswith("part_") for fn in os.listdir(PARTS)):
            raise SystemExit(
                "parts 目录存在但缺少 manifest（无法校验一致性）——如要重建：\n"
                "python scripts/rag/build_vectors.py --rebuild（旧 parts 备份保留·本机 PowerShell 侧改 `py -3`·AGENTS §4.3）")
        os.makedirs(PARTS, exist_ok=True)
        _write_manifest(count, sha, args.slice, args.device)
        return
    same = (mf.get("count") == count and mf.get("slice") == args.slice
            and mf.get("chunks_sha1") == sha
            and mf.get("model") == rag_enhance.EMBED_MODEL)
    if not same:
        raise SystemExit(
            "parts 与当前分块不一致（docs/ 已变或参数不同）——续跑会产生混批产物。\n"
            "如要全量重建：py -3.12 scripts/rag/build_vectors.py --rebuild\n"
            "（旧 parts 将备份保留·不会丢失）")
    print("RESUME：parts manifest 校验通过，跳过已完成批次", flush=True)


def missing_parts(n_parts):
    return [i for i in range(n_parts)
            if not os.path.exists(os.path.join(PARTS, "part_%03d.npy" % i))]


def write_chunks(chunks):
    """原子写 rag_chunks.jsonl（tmp + rename·防半文件）。"""
    fp = os.path.join(OUT, "rag_chunks.jsonl")
    tmp = fp + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    os.replace(tmp, fp)


# ============================================================
# 模型加载与嵌入（重依赖惰性导入·硬件安全模式）
# ============================================================

def gpu_stat():
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu,power.draw", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10)
        if out.returncode == 0:
            return out.stdout.strip().replace("\n", " | ")
    except Exception:
        pass
    return None


def gpu_temp():
    s = gpu_stat()
    if not s:
        return None
    try:
        return float(s.split(",")[0].replace("|", "").strip())
    except Exception:
        return None


def load_embedder(device_raw):
    """导入依赖并加载嵌入模型（离线预置·须在 import ST 之前）。

    device=auto 时自动判定（有 CUDA 用 CUDA）。
    """
    offline = rag_enhance.hf_offline_prepare([rag_enhance.EMBED_MODEL])
    try:
        from sentence_transformers import SentenceTransformer  # 必须先于 torch（段错误坑）
    except ImportError as exc:
        raise SystemExit("缺少依赖：pip install sentence-transformers numpy（%s）" % exc) from exc
    import torch
    device = device_raw
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu":
        torch.set_num_threads(4)  # CPU 限流（硬件纪律）
    t0 = time.time()
    model = SentenceTransformer(rag_enhance.EMBED_MODEL, device=device,
                                local_files_only=offline)
    print("model loaded %.1fs device=%s gpu=%s" % (
        time.time() - t0, device, gpu_stat() if device == "cuda" else "-"), flush=True)
    return model, device


def run_embedding(args, texts, model, device, todo, n_parts):
    """微批嵌入（GPU 冷却 + 温度守护·断点续跑）→ 逐批存盘。"""
    import numpy as np
    print("SAFE_MODE device=%s slice=%d cool=%.0fs warn=%.0fC abort=%.0fC todo=%d/%d"
          % (device, args.slice, args.cool, TEMPERATURE_WARN, TEMPERATURE_ABORT,
             len(todo), n_parts), flush=True)
    t_all = time.time()
    for seq, i in enumerate(todo):
        temp = gpu_temp() if device == "cuda" else None
        if temp is not None and temp >= TEMPERATURE_ABORT:
            raise SystemExit("ABORT：gpu temp %.0fC >= %.0fC（parts 已存盘·续跑即可）"
                             % (temp, TEMPERATURE_ABORT))
        t0 = time.time()
        part = model.encode(texts[i * args.slice:(i + 1) * args.slice], batch_size=64,
                            normalize_embeddings=True, show_progress_bar=False)
        part = np.asarray(part, dtype="float32")
        np.save(os.path.join(PARTS, "part_%03d.npy" % i), part)
        cool = args.cool
        if device == "cuda" and temp is not None and temp >= TEMPERATURE_WARN:
            cool = max(cool, COOL_HOT)
        print("part %03d/%03d rows=%d encode=%.1fs gpu=%s cool=%.0fs wall=%.0fs" % (
            i, n_parts, len(part), time.time() - t0,
            gpu_stat() if device == "cuda" else "-", cool, time.time() - t_all), flush=True)
        if device == "cuda" and cool > 0 and seq < len(todo) - 1:
            time.sleep(cool)


def finalize(n_parts, total):
    """汇总 parts → vectors.npy（原子写）并写出 meta。返回汇总信息。"""
    import numpy as np
    parts = [np.load(os.path.join(PARTS, "part_%03d.npy" % i)) for i in range(n_parts)]
    vecs = np.concatenate(parts, axis=0)[:total]
    if vecs.shape[0] != total:
        raise SystemExit("汇总校验失败：%d 行 ≠ 分块总数 %d——请 --rebuild 重建"
                         % (vecs.shape[0], total))
    fp = os.path.join(OUT, "rag_vectors.npy")
    tmp = fp + ".tmp.npy"
    np.save(tmp, vecs)
    os.replace(tmp, fp)
    return vecs


def write_meta(vecs, sha, device):
    n_docs, m_docs = rag_enhance.docs_stat(xiyouji_rag.DOCS_DIR)
    meta = {
        "model": rag_enhance.EMBED_MODEL,
        "dim": int(vecs.shape[1]),
        "count": int(vecs.shape[0]),
        "device": device,
        "title_prefixed": True,
        "normalized": True,
        "chunk_max": CHUNK_MAX,
        "chunks_sha1": sha,
        "docs_count": n_docs,
        "docs_max_mtime": m_docs,
        "built_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    fp = os.path.join(OUT, "rag_embed_meta.json")
    tmp = fp + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    os.replace(tmp, fp)


# ============================================================
# CLI
# ============================================================

def parse_args():
    ap = argparse.ArgumentParser(description="构建稠密检索向量产物（W744·供增强档使用）")
    ap.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto",
                    help="嵌入设备（默认 auto：有 CUDA 用 CUDA+安全模式，否则 CPU）")
    ap.add_argument("--slice", type=int, default=1500, help="每批块数（默认 1500）")
    ap.add_argument("--cool", type=float, default=35.0, help="GPU 批间冷却秒数（默认 35）")
    ap.add_argument("--rebuild", action="store_true", help="全量重建（旧 parts 备份保留）")
    return ap.parse_args()


def main():
    args = parse_args()
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)

    docs = xiyouji_rag._load_docs()
    chunks = build_chunks(docs)
    sha = chunks_sha1(chunks)
    total = len(chunks)
    n_parts = (total + args.slice - 1) // args.slice
    print("docs=%d chunks=%d parts=%d chunk_sha=%s" % (len(docs), total, n_parts, sha[:12]),
          flush=True)

    decide_resume(args, total, sha)
    write_chunks(chunks)

    todo = missing_parts(n_parts)
    device = args.device
    if todo:
        model, device = load_embedder(args.device)
        run_embedding(args, build_texts(chunks), model, device, todo, n_parts)
    else:
        print("全部批次已存在（%d/%d），跳过嵌入直接汇总" % (n_parts, n_parts), flush=True)
        try:  # resume：device 信息回读（meta 记录用）
            with open(MANIFEST, encoding="utf-8") as f:
                device = json.load(f).get("device", device)
        except Exception:
            pass

    vecs = finalize(n_parts, total)
    write_meta(vecs, sha, device)
    norms = (vecs[:200] ** 2).sum(axis=1) ** 0.5
    print("norm_range=[%.4f,%.4f]" % (float(norms.min()), float(norms.max())), flush=True)
    print("VECTORS_OK count=%d dim=%d device=%s total=%.0fs"
          % (vecs.shape[0], vecs.shape[1], device, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
