#!/usr/bin/env python3
"""sync_search_corpus.py — 站内搜索语料生成器（W1316 建）。

把 `dataset/text-search.json`（权威语料：与 `source/原文/分回` 逐回全等·去空白归一·
由 `check_citations.py` 语料保真检机器对账）渲染为 `site/static/js/text-search-app.js`
内嵌的 `EMBEDDED_DATA.chapters` 块。

背景（W1316 取证）：原 chapters 块是**第三份语料副本**——与分回 md 去空白归一
0/100 回一致、与权威 JSON 仅 8/100 回一致（少 789 字·92 回不一致，多为漏标点/僻字，
与 W737「恢复丢段与僻字」方向相反）。本脚本以 JSON 为唯一事实源重建，消灭手改副本。

用法：
  py -3 scripts/sync_search_corpus.py            # 生成（幂等·无差异不写盘）
  py -3 scripts/sync_search_corpus.py --check    # 只核对：有差异 exit 1（CI/推前干跑门禁）
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_REL = Path("dataset") / "text-search.json"
JS_REL = Path("site") / "static" / "js" / "text-search-app.js"

EMBED_MARKER = "    const EMBEDDED_DATA = {"
CHAPTERS_MARKER = "        chapters: ["


def _header() -> str:
    """内嵌块头注释（不含数字字面量——字符数由页面 KPI 运行时计算，防静态漂移）。"""
    return (
        "    /* ==========================================================\n"
        "       EMBEDDED_DATA：内嵌原著文本（全书 100 回·W1316 起由 scripts/sync_search_corpus.py 生成）\n"
        "       架构：chapters 数组由生成器从 dataset/text-search.json 渲染·禁手改（改语料=改 JSON 后重跑）\n"
        "       文本源：dataset/text-search.json（权威源=source/原文/分回·check_citations.py 语料保真检机器对账）\n"
        "       ========================================================== */\n"
    )


def _header_span(js: str) -> tuple[int, int]:
    """内嵌块头注释的 [起, 止) 下标（止于 `*/` 与随后的换行）。"""
    ci = js.index(EMBED_MARKER)
    start = js.rindex("    /* ====", 0, ci)
    end = js.index("*/", start) + 2
    if js[end:end + 1] == "\n":
        end += 1
    return start, end


def _chapters_span(js: str) -> tuple[int, int]:
    """`chapters: [...]` 的 [起, 止) 下标（方括号配对·跳过模板字面量与双引号串）。"""
    start = js.index(CHAPTERS_MARKER, js.index(EMBED_MARKER))
    lb = js.index("[", start)
    depth = 0
    in_tpl = False
    in_dq = False
    esc = False
    i = lb
    while i < len(js):
        ch = js[i]
        if in_tpl:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == "`":
                in_tpl = False
        elif in_dq:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_dq = False
        elif ch == "`":
            in_tpl = True
        elif ch == '"':
            in_dq = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return start, i + 1
        i += 1
    raise ValueError("未找到 chapters 数组闭合（JS 结构异常）")


def _validate(chapters: list) -> None:
    """fail-closed 校验：结构/数量/危险序列（不可安全嵌入 JS 即拒绝生成）。"""
    if len(chapters) != 100:
        raise SystemExit("sync_search_corpus: 语料应含 100 回，实得 %d" % len(chapters))
    nums = [c.get("num") for c in chapters]
    if nums != list(range(1, 101)):
        raise SystemExit("sync_search_corpus: 章节号须为 1..100 连续，实得前五 %r" % (nums[:5],))
    for c in chapters:
        for key in ("title", "fullTitle", "text"):
            if not isinstance(c.get(key), str) or not c[key]:
                raise SystemExit("sync_search_corpus: 第 %s 回缺字段 %s" % (c.get("num"), key))
        if "`" in c["text"] or "${" in c["text"]:
            raise SystemExit("sync_search_corpus: 第 %s 回正文含模板字面量危险序列（` 或 ${）" % c["num"])
        for key in ("title", "fullTitle"):
            if '"' in c[key] or "\\" in c[key] or "\n" in c[key]:
                raise SystemExit("sync_search_corpus: 第 %s 回 %s 含不可安全入双引号的字符" % (c["num"], key))


def render_chapters(chapters: list) -> str:
    """按 text-search-app.js 既有形态渲染 chapters 数组（缩进/逗号/末块空行逐字保留）。"""
    out = [CHAPTERS_MARKER + "\n"]
    last = len(chapters) - 1
    for i, ch in enumerate(chapters):
        out.append("            {\n")
        out.append("                num: %d,\n" % ch["num"])
        out.append('                title: "%s",\n' % ch["title"])
        out.append('                fullTitle: "%s",\n' % ch["fullTitle"])
        out.append("                text: `%s`\n" % ch["text"])
        out.append("            },\n" if i < last else "            }\n\n")
    out.append("        ]")
    return "".join(out)


def sync(root: Path = ROOT, check: bool = False) -> tuple[bool, str]:
    """重建内嵌语料块；返回 (是否有差异, 摘要)。check=True 时不写盘。"""
    root = Path(root)
    data = json.loads((root / JSON_REL).read_text(encoding="utf-8"))
    chapters = data.get("chapters") or []
    _validate(chapters)

    js = (root / JS_REL).read_text(encoding="utf-8")
    hs, he = _header_span(js)
    cs, ce = _chapters_span(js)
    new_js = js[:hs] + _header() + js[he:cs] + render_chapters(chapters) + js[ce:]

    changed = new_js != js
    if changed and not check:
        (root / JS_REL).write_text(new_js, encoding="utf-8", newline="")
    summary = "%d 回 · 字符 %d" % (len(chapters), sum(len(c["text"]) for c in chapters))
    return changed, summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="站内搜索语料生成器（W1316）")
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
