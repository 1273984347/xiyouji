# 归档分卷清单（ARCHIVE MANIFEST）

> **本文件由 `scripts/gen_archive_manifest.py --refresh` 生成，勿手改**（`--check` 与磁盘对拍，改盘不改清单即 FAIL）。
> **口径**：每个滚动家族（CHANGELOG / file-index）的卷谱系 × 真实 W 区间 × 体积 × 冻结状态；查「W### 在哪个文件」看本表，不要逐个 grep。
> **冻结条款（W1335·用户 2026-11-27 裁决）**：无范围名的旧二级归档卷冻结为只读，不再追加；新迁出一律按 250 号宽度开范围命名卷（`archive_tier2.py --range-width 250`）。

## 滚动家族卷谱系

| 家族 | 卷文件 | 段数 | W 区间 | 体积 | 状态 |
|:--|:--|--:|:--|--:|:--|
| changelog | `CHANGELOG-ARCHIVE.md` | 1 | W5–W5 | 0 KB | 在役 |
| changelog | *家族合计* | 1 | W5–W5 | — | 重复号 0 |
| file-index | *家族合计* | 0 | W-–W- | — | 重复号 0 |

## 其他归档件（无段语义·只记体积）

| 文件 | 体积 |
|:--|--:|
| `HANDOVER-ARCHIVE.md` | 0 KB |

## 复算

```bash
py -3 scripts/gen_archive_manifest.py --check      # 清单与磁盘一致？（过期即 FAIL）
py -3 scripts/gen_archive_manifest.py --refresh    # 盘面变更后重建清单
py -3 scripts/check_archive_health.py              # T1/T1b 体积 + T5 覆盖 + T6 总量
```
