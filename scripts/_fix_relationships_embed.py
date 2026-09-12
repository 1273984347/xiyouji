#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_fix_relationships_embed.py — W565/C-2：relationships 中英两页 EMBEDDED 单源化。

最小 diff（方案档 §C-2）：
  1. loadJson 函数体改为直接返回 fallback（六处调用保持不动，path 参数保留于签名）；
  2. 删除已死的 baseUrl 行；
  3. badge 与数据来源说明文案同步（去除 fetch 表述；「4 份 JSON」陈旧口径一并修正为 6 组数据）。
收益：部署态省 6 次请求 / ~225KB（data）/ ~240KB（en）双传输；file:// 行为不变。
W554 铁律对齐：EMBEDDED 升级为唯一数据源仍含完整数据；无 fetch 即无越界路径问题。

用法：python scripts/_fix_relationships_embed.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOAD_OLD = """    // ===== loadJson: fetch first, fallback to EMBEDDED =====
    async function loadJson(path, fallback) {
        try {
            const res = await fetch(path);
            if (!res.ok) throw new Error('HTTP ' + res.status);
            return await res.json();
        } catch (e) {
            console.warn('[fallback] ' + path + ' → embedded data:', e.message);
            return fallback;
        }
    }"""
LOAD_NEW = """    // ===== loadJson: EMBEDDED 单源（W565）=====
    async function loadJson(path, fallback) {
        // 数据与页面同源生成，部署态不再重复 fetch（每次访问省 6 次请求 / ~225KB 传输）
        console.info('[DATA] EMBEDDED 单源:', path);
        return fallback;
    }"""

CN_PAIRS = [
    (LOAD_OLD, LOAD_NEW),
    ("        const baseUrl = 'json/';\n", ""),
    ('<span class="data-badge">fetch + EMBEDDED fallback</span>',
     '<span class="data-badge">EMBEDDED 内嵌单源（W565）</span>'),
    ('数据来源：scripts/D_关系网络/ 生成脚本 · 共 4 份 JSON 输出，本页 fetch 失败时自动回退到内嵌 EMBEDDED 数据，支持 file:// 协议双击打开。',
     '数据来源：scripts/D_关系网络/ 生成脚本 · 6 组数据全部内嵌于页面（EMBEDDED 单源 · W565），file:// 协议双击可用。'),
]

EN_PAIRS = [
    (LOAD_OLD, LOAD_NEW),
    ("        const baseUrl = '../data/json/';\n", ""),
    ('<span class="data-badge">fetch + EMBEDDED fallback</span>',
     '<span class="data-badge">EMBEDDED single source (W565)</span>'),
    ('Data source: D-series relationship generator scripts · 4 JSON outputs in total; on fetch failure this page falls back to the embedded EMBEDDED data, so it works over the file:// protocol when double-clicked.',
     'Data source: D-series relationship generator scripts · all 6 datasets embedded in this page (EMBEDDED single source · W565), works over the file:// protocol when double-clicked.'),
]


def patch(path, pairs):
    with open(path, encoding="utf-8", newline="") as f:
        s = f.read()
    assert s.count("\r\n") == s.count("\n"), "非纯 CRLF: %s" % path
    s = s.replace("\r\n", "\n")
    for old, new in pairs:
        if old not in s:
            print("锚点未命中:", path, "|", old[:60].replace("\n", "⏎"))
            sys.exit(2)
        s = s.replace(old, new, 1)
    assert "const baseUrl" not in s, "baseUrl 残留: %s" % path
    s = s.replace("\n", "\r\n")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("OK", os.path.relpath(path, ROOT))


def main():
    patch(os.path.join(ROOT, "site", "data", "relationships.html"), CN_PAIRS)
    patch(os.path.join(ROOT, "site", "en", "relationships.html"), EN_PAIRS)


if __name__ == "__main__":
    main()
