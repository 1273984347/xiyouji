#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_fix_semiotics_embed.py — W563/A-3 γ-1：journey-geo-semiotics 中英两页 EMBEDDED 单源化。

geo_semiotics.json 无生成器、从未存在（全仓扫描仅 data_validate.py 提及同名字段），
原 fetch 在任何模式下都 404、恒走 EMBEDDED 回退——移除死路径与 isMock 假二分。

用法：python scripts/_fix_semiotics_embed.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOAD_CN_OLD = """    async function loadData() {
        try {
            const response = await fetch('../../scripts/output/data/geo_semiotics.json');
            if (!response.ok) throw new Error('fetch failed: ' + response.status);
            const data = await response.json();
            if (!data || !Array.isArray(data.nodes) || !Array.isArray(data.links)) {
                throw new Error('invalid schema');
            }
            return data;
        } catch (e) {
            console.log('[INFO] 使用嵌入数据：', e.message);
            return EMBEDDED_DATA;
        }
    }"""
LOAD_CN_NEW = """    async function loadData() {
        // W563：EMBEDDED 单源。原 fetch 目标 geo_semiotics.json 无生成器、从未存在，
        // fetch 在任何模式下都 404、恒走 EMBEDDED 回退，故移除死路径。
        const data = EMBEDDED_DATA;
        if (!data || !Array.isArray(data.nodes) || !Array.isArray(data.links)) {
            throw new Error('invalid EMBEDDED_DATA schema');
        }
        return data;
    }"""

LOAD_EN_OLD = """    async function loadData() {
        try {
            const response = await fetch('../../scripts/output/data/geo_semiotics.json');
            if (!response.ok) throw new Error('fetch failed: ' + response.status);
            const data = await response.json();
            if (!data || !Array.isArray(data.nodes) || !Array.isArray(data.links)) {
                throw new Error('invalid schema');
            }
            return data;
        } catch (e) {
            console.log('[INFO] Using embedded data:', e.message);
            return EMBEDDED_DATA;
        }
    }"""
LOAD_EN_NEW = """    async function loadData() {
        // W563: EMBEDDED single source. The original fetch target geo_semiotics.json
        // has no generator and never existed — fetch 404'd in every mode and always
        // fell through to EMBEDDED_DATA, so the dead path is removed.
        const data = EMBEDDED_DATA;
        if (!data || !Array.isArray(data.nodes) || !Array.isArray(data.links)) {
            throw new Error('invalid EMBEDDED_DATA schema');
        }
        return data;
    }"""

MAIN_CN_OLD = """        const isMock = data === EMBEDDED_DATA;
        if (isMock) {
            d3.select("#dataSource").html(
                `<strong>当前显示嵌入数据（${data.nodes.length} 个节点）。</strong> 如需加载完整数据，请生成 <code>scripts/output/data/geo_semiotics.json</code> 后刷新。`
            );
        } else {
            d3.select("#dataSource").html(
                `数据源：实时加载自 <code>scripts/output/data/geo_semiotics.json</code>（http server 模式）`
            );
        }"""
MAIN_CN_NEW = """        // W563：EMBEDDED 单源，数据始终来自页面内嵌 EMBEDDED_DATA
        d3.select("#dataSource").html(
            `<strong>当前显示嵌入数据（${data.nodes.length} 个节点）。</strong> 数据源：页面内嵌 EMBEDDED_DATA（W563 单源化）`
        );"""

MAIN_EN_OLD = """        const isMock = data === EMBEDDED_DATA;
        if (isMock) {
            d3.select("#dataSource").html(
                `<strong>Currently showing embedded data (${data.nodes.length} nodes).</strong> To load the full dataset, generate <code>scripts/output/data/geo_semiotics.json</code> and refresh.`
            );
        } else {
            d3.select("#dataSource").html(
                `Data source: loaded live from <code>scripts/output/data/geo_semiotics.json</code> (http server mode)`
            );
        }"""
MAIN_EN_NEW = """        // W563: EMBEDDED single source — data always comes from in-page EMBEDDED_DATA
        d3.select("#dataSource").html(
            `<strong>Currently showing embedded data (${data.nodes.length} nodes).</strong> Data source: in-page EMBEDDED_DATA (single-sourced in W563)`
        );"""


def patch(path, pairs):
    with open(path, encoding="utf-8", newline="") as f:
        s = f.read()
    assert s.count("\r\n") == s.count("\n"), "非纯 CRLF: %s" % path
    s = s.replace("\r\n", "\n")
    for old, new in pairs:
        if old not in s:
            print("锚点未命中:", path)
            sys.exit(2)
        s = s.replace(old, new, 1)
    s = s.replace("\n", "\r\n")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    assert "scripts/output/data/" not in s, "仍有残留: %s" % path
    print("OK", os.path.relpath(path, ROOT))


def main():
    patch(os.path.join(ROOT, "site", "data", "journey-geo-semiotics.html"),
          [(LOAD_CN_OLD, LOAD_CN_NEW), (MAIN_CN_OLD, MAIN_CN_NEW)])
    patch(os.path.join(ROOT, "site", "en", "journey-geo-semiotics.html"),
          [(LOAD_EN_OLD, LOAD_EN_NEW), (MAIN_EN_OLD, MAIN_EN_NEW)])


if __name__ == "__main__":
    main()
