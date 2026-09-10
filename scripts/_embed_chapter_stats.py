#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_embed_chapter_stats.py — W563/A-3 β 类：chapter-stats 中英两页 EMBEDDED 单源化。

前置：scripts/output/data/chapter_stats.json 已由修复后的生成器产出真实数据
（100 回；此前因 scripts/utils/text_loader.py 只匹配 第*.txt 而长期为全零空壳）。

变换（每页）：
  1. 在 loadData 前插入 const EMBEDDED_DATA = <minified JSON>;
  2. loadData 由「fetch 越界路径 + 失败落 mock」改为「直接使用 EMBEDDED_DATA」；
  3. 数据源徽标文案同步（无越界路径字样）。
MOCK_DATA 分支保留为空数据兜底（当前不可达）。

用法：python scripts/_embed_chapter_stats.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "scripts", "output", "data", "chapter_stats.json")
PAGES = [
    os.path.join(ROOT, "site", "data", "chapter-stats.html"),
    os.path.join(ROOT, "site", "en", "chapter-stats.html"),
]

CN_OLD = """    // 加载数据（fetch 失败则用 mock 数据 + 提示）
    async function loadData() {
        try {
            const response = await fetch('../../scripts/output/data/chapter_stats.json');
            if (!response.ok) throw new Error('fetch failed: ' + response.status);
            const data = await response.json();
            if (!data || !data.per_chapter || data.per_chapter.length === 0) {
                throw new Error('empty data');
            }
            document.getElementById('dataSource').innerHTML =
                '数据源：实时加载自 <code>../../scripts/output/data/chapter_stats.json</code>（http server 模式） · 共 <strong>' + data.total_chapters + '</strong> 回';
            return { data, isMock: false };
        } catch (e) {
            console.log('[INFO] 使用 mock 数据：', e.message);
            return { data: MOCK_DATA, isMock: true };
        }
    }"""
CN_NEW = """    // W563：EMBEDDED 单源。chapter_stats 生成器经 text_loader 第*.md 扩展名修复后
    // 首次产出真实统计；曾 fetch ../../scripts/output/data/chapter_stats.json，
    // 部署根=site/ 必 404，且该 JSON 曾为全零空壳，页面长期展示 mock 假数据。
    const EMBEDDED_DATA = __DATA__;
    async function loadData() {
        const data = EMBEDDED_DATA;
        if (!data || !data.per_chapter || data.per_chapter.length === 0) {
            console.log('[INFO] 使用 mock 数据：EMBEDDED_DATA 为空');
            return { data: MOCK_DATA, isMock: true };
        }
        document.getElementById('dataSource').innerHTML =
            '数据源：内嵌 chapter_stats.json（EMBEDDED 单源 · W563） · 共 <strong>' + data.total_chapters + '</strong> 回';
        return { data, isMock: false };
    }"""

EN_OLD = """    // 加载数据（fetch 失败则用 mock 数据 + 提示）
    async function loadData() {
        try {
            const response = await fetch('../../scripts/output/data/chapter_stats.json');
            if (!response.ok) throw new Error('fetch failed: ' + response.status);
            const data = await response.json();
            if (!data || !data.per_chapter || data.per_chapter.length === 0) {
                throw new Error('empty data');
            }
            document.getElementById('dataSource').innerHTML =
                'Data source: live from <code>../../scripts/output/data/chapter_stats.json</code> (http server mode) · <strong>' + data.total_chapters + '</strong> chapters';
            return { data, isMock: false };
        } catch (e) {
            console.log('[INFO] using mock data:', e.message);
            return { data: MOCK_DATA, isMock: true };
        }
    }"""
EN_NEW = """    // W563: EMBEDDED single source. chapter_stats generator produced real data
    // only after the text_loader "第*.md" extension fix; the page used to fetch
    // ../../scripts/output/data/chapter_stats.json (always 404 in deploy, deploy
    // root = site/) and fall back to mock because that JSON was an all-zero stub.
    const EMBEDDED_DATA = __DATA__;
    async function loadData() {
        const data = EMBEDDED_DATA;
        if (!data || !data.per_chapter || data.per_chapter.length === 0) {
            console.log('[INFO] using mock data: EMBEDDED_DATA is empty');
            return { data: MOCK_DATA, isMock: true };
        }
        document.getElementById('dataSource').innerHTML =
            'Data source: embedded chapter_stats.json (EMBEDDED single source · W563) · <strong>' + data.total_chapters + '</strong> chapters';
        return { data, isMock: false };
    }"""


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    assert data["total_chapters"] == 100 and len(data["per_chapter"]) == 100, "生成器产出异常，拒绝嵌入"
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    pairs = [(PAGES[0], CN_OLD, CN_NEW), (PAGES[1], EN_OLD, EN_NEW)]
    for path, old, new in pairs:
        with open(path, encoding="utf-8", newline="") as f:
            s = f.read()
        assert s.count("\r\n") == s.count("\n"), "非纯 CRLF，拒绝处理: %s" % path
        s = s.replace("\r\n", "\n")
        if old not in s:
            print("锚点未命中（可能已处理）:", path)
            sys.exit(2)
        s = s.replace(old, new.replace("__DATA__", payload), 1)
        s = s.replace("\n", "\r\n")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        print("OK", os.path.relpath(path, ROOT))
    # 残留核验
    for path in PAGES:
        s = open(path, encoding="utf-8", newline="").read()
        assert "scripts/output/data/" not in s, "仍有越界字面量: %s" % path
        assert "EMBEDDED_DATA" in s
    print("两页均无 scripts/output/data 残留 · EMBEDDED_DATA 已嵌入")


if __name__ == "__main__":
    main()
