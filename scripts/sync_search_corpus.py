#!/usr/bin/env python3
"""sync_search_corpus.py — 站内搜索语料生成器（W1316 建·W1317 压缩存储）。

把 `dataset/text-search.json`（权威语料：与 `source/原文/分回` 逐回全等·去空白归一·
由 `check_citations.py` 语料保真检机器对账）渲染为 `site/static/js/text-search-app.js`
内嵌的 `EMBEDDED_CORPUS_GZ_B64` 载荷。

背景（W1316 取证）：原 chapters 块是**第三份语料副本**——与分回 md 去空白归一
0/100 回一致、与权威 JSON 仅 8/100 回一致（少 789 字·92 回不一致，多为漏标点/僻字，
与 W737「恢复丢段与僻字」方向相反）。本脚本以 JSON 为唯一事实源重建，消灭手改副本。

W1317（容量 #4 治理）：内嵌形态由「逐回明文模板字面量」改为「gzip(JSON)+base64 单串」
（2.15 MB → 约 1.2 MB）；运行时由 text-search-app.js 的 `decodeCorpus()` 以
`DecompressionStream('gzip')` 解压回填 `EMBEDDED_DATA.chapters`（file:// 可用·
零外域依赖）。明文块已不存在——事实源仍是 dataset/text-search.json，禁手改 base64 串。

确定性：JSON 序列化键序固定（num/title/fullTitle/text）+ gzip mtime=0 ⇒ 同机重跑
字节稳定；跨平台 zlib 实现差异由「解码后逐条对拍」判据吸收（--check 不比字节）。

用法：
  py -3 scripts/sync_search_corpus.py            # 生成（幂等·无差异不写盘）
  py -3 scripts/sync_search_corpus.py --check    # 只核对：有差异 exit 1（CI/推前干跑门禁）
"""
from __future__ import annotations

import argparse
import base64
import gzip
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_REL = Path("dataset") / "text-search.json"
JS_REL = Path("site") / "static" / "js" / "text-search-app.js"

PAYLOAD_CONST = "EMBEDDED_CORPUS_GZ_B64"
# 载荷整行（行首缩进随行·便于生成器整行替换而不动周边缩进）；
# 内容类不限 base64 字符——载荷损坏时仍能定位并重建（合法性由 decode 侧校验）
_PAYLOAD_RE = re.compile(
    r'^[ \t]*const\s+' + PAYLOAD_CONST + r'\s*=\s*"([^"\n]*)";[ \t]*\n?',
    re.M,
)
_HEADER_ANCHOR = "    /* ===="


def _header() -> str:
    """内嵌块头注释（不含数字字面量——字符数由页面 KPI 运行时计算，防静态漂移）。"""
    return (
        "    /* ==========================================================\n"
        "       EMBEDDED_DATA：内嵌原著文本（全书 100 回·W1316 起由 scripts/sync_search_corpus.py 生成·\n"
        "       W1317 起 gzip+base64 压缩存储）\n"
        "       架构：正文压缩存于下方 EMBEDDED_CORPUS_GZ_B64（生成器渲染·禁手改）；运行时\n"
        "             decodeCorpus() 以 DecompressionStream('gzip') 解压回填 EMBEDDED_DATA.chapters\n"
        "       文本源：dataset/text-search.json（权威源=source/原文/分回·check_citations.py 语料保真检机器对账）\n"
        "       ========================================================== */\n"
    )


def _payload_span(js: str) -> tuple[int, int]:
    """`EMBEDDED_CORPUS_GZ_B64` 载荷整行的 [起, 止) 下标（缺失即 fail-closed）。"""
    m = _PAYLOAD_RE.search(js)
    if not m:
        raise ValueError("未找到 EMBEDDED_CORPUS_GZ_B64 载荷（JS 结构异常）")
    return m.start(), m.end()


def _header_span(js: str) -> tuple[int, int]:
    """内嵌块头注释的 [起, 止) 下标（止于 `*/` 与随后的换行）。"""
    ps, _ = _payload_span(js)
    start = js.rindex(_HEADER_ANCHOR, 0, ps)
    end = js.index("*/", start) + 2
    if js[end:end + 1] == "\n":
        end += 1
    return start, end


def _project(ch: dict) -> dict:
    """载荷投影（键序固定·只保留运行时消费的四个字段）。"""
    return {"num": ch["num"], "title": ch["title"],
            "fullTitle": ch["fullTitle"], "text": ch["text"]}


def encode_payload(chapters: list) -> str:
    """chapters → base64(gzip(compact JSON))（确定性：键序固定·mtime=0）。"""
    payload = json.dumps([_project(c) for c in chapters],
                         ensure_ascii=False, separators=(",", ":"))
    return base64.b64encode(
        gzip.compress(payload.encode("utf-8"), compresslevel=9, mtime=0)).decode("ascii")


def decode_payload(js: str) -> list:
    """从 JS 文本解出 chapters；载荷缺失/不可解压/非数组 → 返回 []（调用方按差异处理）。"""
    m = _PAYLOAD_RE.search(js)
    if not m:
        return []
    try:
        raw = gzip.decompress(base64.b64decode(m.group(1), validate=True))
        data = json.loads(raw.decode("utf-8"))
    except (OSError, ValueError):
        return []
    return data if isinstance(data, list) else []


def render_payload(b64: str) -> str:
    return '    const %s = "%s";\n' % (PAYLOAD_CONST, b64)


def _validate(chapters: list) -> None:
    """fail-closed 校验：结构/数量/字段（不可安全入 JSON 即拒绝生成）。"""
    if len(chapters) != 100:
        raise SystemExit("sync_search_corpus: 语料应含 100 回，实得 %d" % len(chapters))
    nums = [c.get("num") for c in chapters]
    if nums != list(range(1, 101)):
        raise SystemExit("sync_search_corpus: 章节号须为 1..100 连续，实得前五 %r" % (nums[:5],))
    for c in chapters:
        for key in ("title", "fullTitle", "text"):
            if not isinstance(c.get(key), str) or not c[key]:
                raise SystemExit("sync_search_corpus: 第 %s 回缺字段 %s" % (c.get("num"), key))


def sync(root: Path = ROOT, check: bool = False) -> tuple[bool, str]:
    """重建内嵌压缩载荷；返回 (是否有差异, 摘要)。check=True 时不写盘。"""
    root = Path(root)
    data = json.loads((root / JSON_REL).read_text(encoding="utf-8"))
    chapters = data.get("chapters") or []
    _validate(chapters)
    expected = [_project(c) for c in chapters]

    js = (root / JS_REL).read_text(encoding="utf-8")
    hs, he = _header_span(js)
    ps, pe = _payload_span(js)
    changed = decode_payload(js) != expected or js[hs:he] != _header()
    if changed and not check:
        new_js = js[:hs] + _header() + js[he:ps] + render_payload(encode_payload(chapters)) + js[pe:]
        (root / JS_REL).write_text(new_js, encoding="utf-8", newline="")
    summary = "%d 回 · 字符 %d · 载荷 %d B（base64）" % (
        len(chapters), sum(len(c["text"]) for c in chapters),
        len(encode_payload(chapters)))
    return changed, summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="站内搜索语料生成器（W1316 建·W1317 压缩存储）")
    ap.add_argument("--check", action="store_true", help="只核对差异，有差异 exit 1")
    args = ap.parse_args(argv)

    changed, summary = sync(ROOT, check=args.check)
    if args.check:
        if changed:
            print("[sync_search_corpus] FAIL 内嵌语料与 dataset/text-search.json 不一致（%s）"
                  "——跑 py -3 scripts/sync_search_corpus.py 重建" % summary)
            return 1
        print("[sync_search_corpus] OK 内嵌语料与 dataset/text-search.json 一致（%s）" % summary)
        return 0
    print("[sync_search_corpus] %s（%s）" % ("已重建" if changed else "无差异（幂等）", summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
