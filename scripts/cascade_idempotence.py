#!/usr/bin/env python3
"""cascade_idempotence.py — 级联**插入型面**的幂等写入原语（W1122）。

病根（W1117 R-01）：级联各插入型面**各自为战**、无统一的「本批号在本面是否已落内容」判定
⇒ 行为不一致：有的**静默重复**（交接文档头链 entry / 里程碑块 / AGENTS 脚注条目 /
  workflows 尾标记），有的 fail-closed（CHANGELOG 段断言「batch == 顶段+1」·页脚链 token 去重断言）。
⇒ 后果：**落段后无法重跑级联**（要么断言炸·要么文档内容静默重复）。

本模块提供**单一事实源**的幂等 upsert 原语：
  · 本批条目不存在 ⇒ 插入（既有行为）
  · 本批条目已存在且**内容一致** ⇒ **零变化**（可重复执行）
  · 本批条目已存在但**内容不一致** ⇒ **替换为新内容**（真正的「重跑级联修正」路径）

判据强度不降：原「已存在即断言失败」的 fail-closed 语义，由「内容不一致 ⇒ 替换」覆盖；
替换后内容与 spec 逐字一致 ⇒ 不会留下 stale 内容。
"""
from __future__ import annotations

import re


def upsert_entry(text, locate, build, insert_at):
    """幂等 upsert 一个「批次条目」。

    locate(text) -> (start, end) | None  本批条目已落内容的区间（不含 end）
    build() -> str                   本批条目应有的新内容（**含其边界换行**·由调用方保证形态）
    insert_at(text) -> int          本批条目不存在时的插入点
    返回 (新文本, 状态)；状态 ∈ {"inserted", "unchanged", "replaced"}
    """
    span = locate(text)
    new = build()
    if span is None:
        pos = insert_at(text)
        return text[:pos] + new + text[pos:], "inserted"
    s, e = span
    if text[s:e].strip() == new.strip():
        return text, "unchanged"
    return text[:s] + new + text[e:], "replaced"


def locate_entry(text, start_re, end_re=None):
    """通用定位：从 start_re 首个匹配起点，到 end_re 匹配起点（不含）的区间。

    end_re 为 None 时 ⇒ 终点取「起点所在行的行尾（含换行）」。
    """
    m = re.search(start_re, text, re.M)
    if not m:
        return None
    s = m.start()
    if end_re is None:
        nl = text.find("\n", s)
        e = len(text) if nl == -1 else nl + 1
    else:
        m2 = re.compile(end_re, re.M).search(text, m.end())
        e = m2.start() if m2 else len(text)
    return s, e
