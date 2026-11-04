#!/usr/bin/env python3
r"""check_design_asset_manifest.py — assets/design 目录清单对拍判据（W1135·遗留③）

背景：design 审查 P2-5 报「assets/design/ 12 处 README/index.md 文件清单失准」，
其中 3 类是**声明了磁盘上不存在的文件**（各 index.md 声明生成器路径 ·
logo/README.md 写 `48.png` 实为 `favicon-48.png` · assets/design/README.md
声明 20 个不存在的文件且漏 `index.html`）。W1105 批只订正 2 处真失准，
其余登记次批 ⇒ W1135 批定向订正并把口径固化为机器判据。

两个条目来源（缺一不可）
----------------------
① **反引号条目**：`\`path.ext\`` 形态 ⇒ 路径按「含 '/' 相对 assets/design ·
   否则相对 md 所在目录」解析。
② **代码块目录树**：树形缩进表达层级 ⇒ 须按**缩进栈**还原目录上下文
   （只认反引号会让整段过期的树漏检 —— design 审查 P2-5 的真凶：旧树整段
   指向已废弃的一次性工作区 tmpe/_reports/logo-explore-v2/）。

判据边界（首版误报 20+ 条后收敛）
--------------------------------
硬错（FAIL）只判**本目录/子目录内的文件名声明**：
  · 裸文件名（无 '/'）按「md 所在目录」解析 ⇒ 磁盘无 ⇒ FAIL；
  · 含 '/' 的条目按「相对 assets/design」解析 ⇒ 磁盘无 ⇒ FAIL
    （前缀写法 `../tools/x.py` 由此口径覆盖）。
不判（降为 NOTE）的四类，避免过度判红：
  ① **外部引用**：首段是仓库其他顶层目录（site/ docs/ scripts/ 等）⇒
     属待办描述或生成器模板固定声明，不是本目录资产清单；
  ② **通配/占位**：含 * < > { } … 等字符（`*-mark-mono.svg`、
     `icon-{16,32}.png`、`RECEIPT-W<号>.md`）；
  ③ **枚举合并写法**：`favicon-16/32/48.png`（前缀+枚举，非真实路径）；
  ④ **仓库根引用**：`STRUCTURE.md` 等根文件（生成器模板固定声明）。
「磁盘存在但未声明」只作 NOTE —— 目录文档未必穷举全部文件。

用法：py -3 scripts/check_design_asset_manifest.py [--report]
退出码：0 = 通过；1 = 有 FAIL；2 = 基础设施缺失（fail-closed）
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "assets", "design")

CODE_RE = re.compile(r"`([^`\n]{1,160})`")
CODE_BLOCK_RE = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.DOTALL)
TREE_LINE_RE = re.compile(r"^([\s\u2502]*)(?:\u251c\u2500\u2500|\u2514\u2500\u2500)\s*(.+?)\s*$")
CMD_TOKEN_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.\\\\/-]*\.(?:png|svg|py|json|html|md|ico|js|css|txt|yaml|yml)\b")
EXT_RE = re.compile(r"\.(png|svg|py|json|html|md|ico|js|css|txt|yaml|yml)$")
WILDCARD_HINTS = ("*", "<", ">", "{", "}", "\u2026", "...")
EXTERNAL_ROOTS = ("site", "docs", "scripts", "archive", "tests", "hyperframes")


def _looks_wildcard(token):
    return any(h in token for h in WILDCARD_HINTS)


def _is_external(token):
    head = token.split("/", 1)[0]
    return head in EXTERNAL_ROOTS


def _is_enumeration(token):
    """`favicon-16/32/48.png` 形态：末段之前的部分不是真实目录 ⇒ 枚举合并写法。"""
    if "/" not in token:
        return False
    head = token.rsplit("/", 1)[0]
    for base in (BASE, ROOT):
        if os.path.isdir(os.path.join(base, head.replace("/", os.sep))):
            return False
    return True


def _resolve(token, md_dir):
    """→ (绝对路径 or None, 状态)；状态 ∈ ok/missing/wildcard/external/enumeration/rootref。"""
    token = token.strip().lstrip("./")
    if token.startswith("../"):
        token = token[3:]
    if _looks_wildcard(token):
        return None, "wildcard"
    if _is_external(token):
        return None, "external"
    if _is_enumeration(token):
        return None, "enumeration"
    cands = []
    if "/" in token:
        cands.append(os.path.join(BASE, token.replace("/", os.sep)))
        cands.append(os.path.join(md_dir, token.replace("/", os.sep)))
    else:
        cands.append(os.path.join(md_dir, token))
        cands.append(os.path.join(BASE, token))
    for c in cands:
        if os.path.exists(c):
            return os.path.normpath(c), "ok"
    if "/" not in token and os.path.exists(os.path.join(ROOT, token)):
        return None, "rootref"
    return None, "missing"


def _cmd_line_tokens(line):
    """非树行 → 命令形态路径条目 [(token, token)]。

    命令里的裸文件名多在注释中 ⇒ 不作清单条目（仅收含 '/' 的 token）。
    """
    out = []
    for cm in CMD_TOKEN_RE.finditer(line):
        tok = cm.group(0).replace("\\", "/")
        if "/" not in tok:
            continue
        out.append((tok, tok))
    return out


def _tree_line_tokens(tm, dirs):
    """树行 → 条目列表 [(相对 BASE 的路径, 原始 token)]。

    目录行（以 '/' 结尾）只更新 dirs 层级栈并返回空列表；文件行按 dirs 栈还原前缀。
    """
    indent = tm.group(1).replace("\u2502", " ").replace("\u251c", " ").replace("\u2514", " ")
    depth = len(indent) // 4
    body = tm.group(2).strip()
    parts = [p.strip() for p in body.split("\u00b7")]
    first = parts[0].split()[0] if parts[0].split() else ""
    if first.endswith("/"):
        dirs[depth] = first.rstrip("/")
        return []
    prefix = "/".join(dirs[d] for d in sorted(dirs) if d < depth)
    out = []
    for part in parts:
        bits = part.split()
        if not bits:
            continue
        tok = bits[0]
        if not EXT_RE.search(tok):
            continue
        out.append((prefix + "/" + tok if prefix else tok, tok))
    return out


def _code_tokens(text):
    """代码块内**目录树**条目 → [(相对 BASE 的路径, 原始 token)]（按缩进栈还原层级）。"""
    out = []
    for m in CODE_BLOCK_RE.finditer(text):
        dirs = {}
        for line in m.group(1).splitlines():
            tm = TREE_LINE_RE.match(line)
            if not tm:
                out.extend(_cmd_line_tokens(line))
                continue
            out.extend(_tree_line_tokens(tm, dirs))
    return out


def declared_entries(md_path):
    """→ [(原始条目, 绝对路径 or None, 状态)]（反引号条目 + 目录树条目，去重）。"""
    text = open(md_path, encoding="utf-8", errors="replace").read()
    md_dir = os.path.dirname(md_path)
    out = []
    seen = set()
    tokens = []
    for m in CODE_RE.finditer(text):
        token = m.group(1).strip()
        if " " in token or not EXT_RE.search(token):
            continue
        tokens.append(token)
    for rel, _tok in _code_tokens(text):
        tokens.append(rel)
    for token in tokens:
        key = token.strip()
        if key in seen:
            continue
        seen.add(key)
        hit, status = _resolve(token, md_dir)
        out.append((token, hit, status))
    return out


def md_files():
    for dirpath, _dirs, files in os.walk(BASE):
        for name in sorted(files):
            if name in ("README.md", "INDEX.md"):
                full = os.path.join(dirpath, name)
                yield full, os.path.relpath(full, ROOT).replace(os.sep, "/")


def main() -> int:
    ap = argparse.ArgumentParser(description="assets/design 目录清单对拍判据（W1135）")
    ap.add_argument("--report", action="store_true", help="只报不判红")
    args = ap.parse_args()

    if not os.path.isdir(BASE):
        print("FAIL 基础设施缺失：assets/design/ 目录不存在（fail-closed）")
        return 2

    fails = []
    notes = []
    checked = 0
    for full, rel in md_files():
        entries = declared_entries(full)
        for token, _hit, status in entries:
            if status == "ok":
                checked += 1
                continue
            if status == "missing":
                checked += 1
                fails.append("%s 声明的 `%s` 磁盘不存在" % (rel, token))
            else:
                notes.append("%s 的 `%s`（%s·不判红）" % (rel, token, status))
        declared = {h for _t, h, _s in entries if h}
        for name in sorted(os.listdir(os.path.dirname(full))):
            if name in ("README.md", "INDEX.md"):
                continue
            cand = os.path.normpath(os.path.join(os.path.dirname(full), name))
            if os.path.isdir(cand) or not EXT_RE.search(name):
                continue
            if cand not in declared:
                notes.append("%s 未声明同目录文件 `%s`" % (rel, name))

    print("---- 第 59 门禁 design 资产清单对拍：判定条目 %d · 失准 %d · 提示 %d ----"
          % (checked, len(fails), len(notes)))
    for n in notes:
        print("  NOTE " + n)
    for f in fails:
        print("FAIL  " + f)
    if fails and not args.report:
        print("---- 第 59 门禁 design 资产清单对拍：%d FAIL ----" % len(fails))
        return 1
    print("---- 第 59 门禁 design 资产清单对拍：0 FAIL ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
