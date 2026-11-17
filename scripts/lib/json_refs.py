#!/usr/bin/env python3
"""json_refs.py — 页面 JSON 数据引用抽取（W1265 批一·判据补盲共用）。

被 1-2（EN 页不得指向中文数据集）与 1-10（页面引用 → 已部署 闭合性）两判据共用。
口径必须可复现：换人复跑得同一组数字，故每条规则写死在此。

抽取对象：页面**运行时真的会发起 fetch 的 JSON 目标**。

规则：
  R1 装载调用 = (fetch | d3.json | loadJson | load_json | fetchJSON | fetchJson | getJSON) 后紧跟 "("。
     只取**第一个实参**——loadJson(path, fallback) 的第二参是回退值不是路径
     （审查报告《被证伪的初判》第 1 条已实证：把它当路径键会全站假绿）。
  R2 目标解析（按优先级）：
     L1 字面量实参              → 该字符串
     L2 路径常量 + 字面量       → 前缀常量值 + 字面量（base='json/' + 'x.json'）
     L3 路径常量 + 文件名表     → 前缀 + 表内每个文件名（DATA_DIR + f·f 来自 FILES 表）
     L4 路径常量 + 未知标识符   → 若文件内**唯一**一张文件名表 → 前缀 + 该表全部文件名
     L5 无法解析                → 记入未解析计数（不计违例·但必须报出·防探针盲区）
  R3 路径常量 = (const|let|var) NAME = '<以 / 结尾或含 json/ 的字符串>'。
  R4 文件名表 = (const|let|var) NAME = { ... } 的扁平对象·值为 '*.json' 字符串。
  R5 注释先剥离（HTML 注释 + 块注释 + 整行 // 注释）——注释里的示例路径不是调用点。
"""
from __future__ import annotations

import re
from pathlib import Path

LOADER_RE = re.compile(r"(?:fetch|d3\.json|loadJson|load_json|fetchJSON|fetchJson|getJSON)\s*\(\s*([^,)]{1,200})")
RE_HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
RE_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
RE_LINE_COMMENT = re.compile(r"(?m)^[ \t]*//.*$")
RE_PREFIX_CONST = re.compile(r"(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(['\"])([^'\"]+)\2")
RE_MAP_CONST = re.compile(r"(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*\{")
RE_JSON_STR = re.compile(r"(['\"])([^'\"]*\.json)\1")
RE_LITERAL_JSON = re.compile(r"(['\"])([^'\"]+\.json)\1")
RE_PREFIX_PLUS_LITERAL = re.compile(r"([A-Za-z_$][\w$]*)\s*\+\s*(['\"])([^'\"]+\.json)\2")
RE_TWO_IDENTS = re.compile(r"([A-Za-z_$][\w$]*)\s*\+\s*([A-Za-z_$][\w$]*)")
RE_ONE_IDENT = re.compile(r"([A-Za-z_$][\w$]*)")


def strip_comments(src: str) -> str:
    """剥离 HTML 注释 / JS 块注释 / 行注释——**字符串字面量内的注释符不算注释**。

    W1265 实测教训：正则式块注释匹配会因页面内一处「字符串里的 /*」把后续 45KB 代码
    整段吞掉（cave-estate.html 实测 142776 → 97536 字节·全部 fetch 调用被吞⇒EN 判据漏检 1 页）。
    ⇒ 改为逐字符扫描器：识别字符串（' " 反引号）→ 串内不判注释；
      /* 无配对 */ 时按字面量处理（不吞后续代码）。
    """
    out: list[str] = []
    i = 0
    n = len(src)
    quote_chars = ("'", '"', chr(96))
    while i < n:
        ch = src[i]
        if ch == "<" and src.startswith("<!--", i):
            end = src.find("-->", i + 4)
            i = n if end < 0 else end + 3
            out.append(" ")
            continue
        if ch == "/" and i + 1 < n:
            nxt = src[i + 1]
            if nxt == "/":
                end = src.find("\n", i)
                i = n if end < 0 else end
                out.append(" ")
                continue
            if nxt == "*":
                end = src.find("*/", i + 2)
                if end < 0:
                    out.append(ch)
                    i += 1
                    continue
                i = end + 2
                out.append(" ")
                continue
        if ch in quote_chars:
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == ch:
                    j += 1
                    break
                j += 1
            out.append(src[i:j])
            i = j
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _balanced_object(src: str, open_idx: int) -> str | None:
    """取 '{' 起的对象字面量正文（括号配平·跳过字符串）。失败返回 None。"""
    depth = 0
    in_str = ""
    esc = False
    for i in range(open_idx, len(src)):
        ch = src[i]
        if in_str:
            if esc:
                esc = False
                continue
            if ch == "\\":
                esc = True
                continue
            if ch == in_str:
                in_str = ""
            continue
        if ch in "'\"":
            in_str = ch
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return src[open_idx + 1 : i]
    return None


def _collect_prefixes(src: str) -> dict[str, str]:
    """R3：路径常量表。"""
    out: dict[str, str] = {}
    for m in RE_PREFIX_CONST.finditer(src):
        val = m.group(3)
        if val.endswith("/") or "json" in val:
            out[m.group(1)] = val
    return out


def _collect_maps(src: str) -> dict[str, list[str]]:
    """R4：文件名表（扁平对象·值为 *.json 字符串）。"""
    out: dict[str, list[str]] = {}
    for m in RE_MAP_CONST.finditer(src):
        body = _balanced_object(src, m.end() - 1)
        if not body:
            continue
        files = [mm.group(2) for mm in RE_JSON_STR.finditer(body)]
        if files:
            out[m.group(1)] = files
    return out


def extract_targets(html: str) -> tuple[list[str], list[str]]:
    """抽取页面的 JSON 装载目标 → ([(目标, 解析规则 L1..L5)], 未解析实参列表)。"""
    src = strip_comments(html)
    prefixes = _collect_prefixes(src)
    maps = _collect_maps(src)
    targets: list[tuple[str, str]] = []
    unresolved: list[str] = []
    for m in LOADER_RE.finditer(src):
        arg = m.group(1).strip()
        lit = RE_LITERAL_JSON.fullmatch(arg)
        if lit:
            targets.append((lit.group(2), "L1"))
            continue
        cat = RE_PREFIX_PLUS_LITERAL.fullmatch(arg)
        if cat and cat.group(1) in prefixes:
            targets.append((prefixes[cat.group(1)] + cat.group(3), "L2"))
            continue
        two = RE_TWO_IDENTS.fullmatch(arg)
        if two and two.group(1) in prefixes:
            if two.group(2) in maps:
                targets.extend((prefixes[two.group(1)] + f, "L3") for f in maps[two.group(2)])
                continue
            if len(maps) == 1:
                targets.extend((prefixes[two.group(1)] + f, "L4") for f in next(iter(maps.values())))
                continue
            unresolved.append(arg)
            continue
        single = RE_ONE_IDENT.fullmatch(arg)
        if single and single.group(1) in maps and len(prefixes) == 1:
            targets.extend((next(iter(prefixes.values())) + f, "L5") for f in maps[single.group(1)])
            continue
        unresolved.append(arg)
    return targets, unresolved


def resolve_http_path(page_rel: str, target: str) -> str:
    """http 语义下的服务器路径（以 site/ 为根·POSIX 风格）。

    页面 site/en/x.html 引用 '../data/json/y.json' → /data/json/y.json（与部署形态一致）。
    目标以 '/' 开头 → 视为服务器根相对（site/ 为根）。
    """
    page_dir = str(Path(page_rel).parent).replace("\\", "/")
    if target.startswith("/"):
        return str(Path(target.lstrip("/"))).replace("\\", "/")
    return str(Path(page_dir) / target).replace("\\", "/")


def norm_path(p: str) -> str:
    """归一化 POSIX 路径（去掉 ./ 与多余分隔·保留 .. 以便判定越出 site/）。"""
    parts: list[str] = []
    for seg in p.replace("\\", "/").split("/"):
        if seg in ("", "."):
            continue
        if seg == "..":
            if parts and parts[-1] != "..":
                parts.pop()
            else:
                parts.append("..")
            continue
        parts.append(seg)
    return "/".join(parts)
