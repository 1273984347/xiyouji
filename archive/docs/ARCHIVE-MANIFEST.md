# 归档分卷清单（ARCHIVE MANIFEST）

> **本文件由 `scripts/gen_archive_manifest.py --refresh` 生成，勿手改**（`--check` 与磁盘对拍，改盘不改清单即 FAIL）。
> **口径**：每个滚动家族（CHANGELOG / file-index）的卷谱系 × 真实 W 区间 × 体积 × 冻结状态；查「W### 在哪个文件」看本表，不要逐个 grep。
> **冻结条款（W1335·用户 2026-11-27 裁决）**：无范围名的旧二级归档卷冻结为只读，不再追加；新迁出一律按 250 号宽度开范围命名卷（`archive_tier2.py --range-width 250`）。

## 滚动家族卷谱系

| 家族 | 卷文件 | 段数 | W 区间 | 体积 | 状态 |
|:--|:--|--:|:--|--:|:--|
| changelog | `CHANGELOG-ARCHIVE-tier2-W400-W559.md` | 144 | W400–W559 | 299 KB | 在役 |
| changelog | `CHANGELOG-ARCHIVE-tier2-W673-W813.md` | 138 | W673–W813 | 427 KB | 在役 |
| changelog | `CHANGELOG-ARCHIVE-tier2-W814-W874.md` | 59 | W814–W874 | 197 KB | 在役 |
| changelog | `CHANGELOG-ARCHIVE-tier2-W875-W950.md` | 68 | W875–W950 | 210 KB | 在役 |
| changelog | `CHANGELOG-ARCHIVE-tier2.md` | 177 | W277–W672 | 1020 KB | **冻结（只读）** |
| changelog | `CHANGELOG-ARCHIVE.md` | 302 | W951–W1278 | 991 KB | 在役 |
| changelog | *家族合计* | 888 | W277–W1278 | — | 重复号 0 |
| file-index | `file-index-ARCHIVE-tier2-W1080-W1151.md` | 59 | W1080–W1151 | 705 KB | 在役 |
| file-index | `file-index-ARCHIVE-tier2-W335-W979.md` | 570 | W335–W979 | 806 KB | 在役 |
| file-index | `file-index-ARCHIVE-tier2.md` | 115 | W980–W1169 | 901 KB | **冻结（只读）** |
| file-index | `file-index-ARCHIVE.md` | 101 | W1170–W1278 | 384 KB | 在役 |
| file-index | *家族合计* | 845 | W335–W1278 | — | 重复号 0 |

## 其他归档件（无段语义·只记体积）

| 文件 | 体积 |
|:--|--:|
| `AGENTS-ARCHIVE.md` | 321 KB |
| `ARCHIVE-T5-EXEMPTIONS.md` | 1 KB |
| `HANDOVER-ARCHIVE.md` | 336 KB |
| `STRUCTURE-ARCHIVE.md` | 84 KB |
| `W批次编号对账表-ARCHIVE.md` | 795 KB |
| `pitfalls-detail-ARCHIVE.md` | 372 KB |

## 复算

```bash
py -3 scripts/gen_archive_manifest.py --check      # 清单与磁盘一致？（过期即 FAIL）
py -3 scripts/gen_archive_manifest.py --refresh    # 盘面变更后重建清单
py -3 scripts/check_archive_health.py              # T1/T1b 体积 + T5 覆盖 + T6 总量
```
