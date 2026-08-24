#!/usr/bin/env python3
"""W513 二级归档：CHANGELOG-ARCHIVE 的 W001-W399 原始块迁至 docs/archive/CHANGELOG-ARCHIVE-tier2.md。
方案 A（内容二级归档）：archive 超阈值时最老块迁至二级，archive 保留较新段 + 指针。
"""
import os

SRC = "CHANGELOG-ARCHIVE.md"
TIER2_DIR = os.path.join("docs", "archive")
TIER2 = os.path.join(TIER2_DIR, "CHANGELOG-ARCHIVE-tier2.md")

lines = open(SRC, encoding="utf-8").read().splitlines()

# 头部区 = L1-L7（标题 + 说明 + ---），保留在 archive
# 迁移区 = L8 到 L4602（W399 段起点 到 W422 归档段前 = W001-W399 主体）
# 保留区 = L4603 起（W422 归档段 W400-W416 + W511 段）
tier2_start = 7   # 0-indexed: L8
tier2_end = 4602  # 0-indexed: L4602 之前（exclusive），即 L8..L4602

head = lines[:tier2_start]           # L1-L7
migrated = lines[tier2_start:tier2_end]  # L8-L4602（W001-W399 主体）
kept = lines[tier2_end:]             # L4603-末尾（W400+）

# tier2 文件：自含头部 + 迁移区
tier2_content = [
    "# CHANGELOG 二级归档（W001-W399·v0.1-v2.3.17）",
    "",
    "> 本文件为 CHANGELOG-ARCHIVE.md 的二级归档层，承载最早期的 W001-W399 详细变更记录。",
    "> 归档时间：2026-08-25（W513 二级归档批次·方案 A：archive 超阈值时最老块下移）。",
    "> 最新变更见 [CHANGELOG.md](../../CHANGELOG.md)；中间层见 [CHANGELOG-ARCHIVE.md](../../CHANGELOG-ARCHIVE.md)（W400+）。",
    "> 入口维护：CHANGELOG-ARCHIVE.md 头部指针；本文件历史段禁改（文档规范 §11.2 归档约束同适用于二级层）。",
    "",
    "---",
    "",
] + migrated

# archive 保留：头部 + 指针 + 保留区
archive_head = head[:]
# 更新头部描述，追加二级归档指针
archive_head[0] = "# 更新日志归档（W400+）"
archive_head[1] = ""
archive_head[2] = "> 本文件归档 W400+ 的详细变更记录（W417-W464 由 W511 迁入）。更早期 W001-W399（v0.1-v2.3.17）已下移至 [docs/archive/CHANGELOG-ARCHIVE-tier2.md](docs/archive/CHANGELOG-ARCHIVE-tier2.md)。最新变更见 [CHANGELOG.md](CHANGELOG.md)。"
archive_head[3] = "> 归档时间：2026-08-10（W422 归档 W400-W416）+ 2026-08-25（W511 归档 W417-W448 + W449-W464 + W484）· 2026-08-25（W513 二级归档：W001-W399 下移 tier2）"
archive_head[4] = ""
archive_head[5] = "---"

os.makedirs(TIER2_DIR, exist_ok=True)
open(TIER2, "w", encoding="utf-8", newline="\n").write("\n".join(tier2_content) + "\n")
open(SRC, "w", encoding="utf-8", newline="\n").write("\n".join(archive_head + kept) + "\n")

def kb(f):
    return sum(len(l.encode("utf-8")) + 1 for l in f) / 1024

print("迁移行数:", len(migrated), "| 迁移字节: %.1fKB" % kb(migrated))
print("archive 保留行数:", len(archive_head + kept), "| 保留字节: %.1fKB" % kb(archive_head + kept))
print("tier2 行数:", len(tier2_content), "| tier2 字节: %.1fKB" % kb(tier2_content))
print("tier2 路径:", TIER2)
