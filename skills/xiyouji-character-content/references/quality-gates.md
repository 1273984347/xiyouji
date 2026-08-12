# 质量门禁与项目约束（收尾核对用）

## 1. E1 铁律（声明 ≠ 落地）

每条"已修复/已同步/已添加"的声明都必须 Grep spot-check 验证。人物内容场景：

- 声称的 W### → 在 `CHANGELOG.md` 中确实存在对应段。
- 声称的链接 → `lint_links` 或手动确认目标存在。
- 声称的相邻回/回目号 → 与原著/`docs/01-全书逐回解读/` 文件名一致。

## 2. 双索引（每篇人物内容必带）

- 正向：`[CHANGELOG.md](../../CHANGELOG.md)` 的 W### 段。
- 反向：`scripts/output/file-index.md` 中本文件的条目（新文件必须新增行；格式见该文件 W424 段示例）。
- 相对路径基准：`docs/02-人物深度分析/` 到仓库根是两级（`../../`）。
- A1 反链（基础人物建议加）：`../../01-全书逐回解读/第NNN回-*.md`。

## 3. W### 与版本同步

- 每个新 W### 完成后：CHANGELOG.md / 交接文档.md（HEAD、版本列表、接续编号、页脚最后更新）/ README.md / STRUCTURE.md / docs/00-导读/项目说明.md（两处版本行）/ scripts/output/file-index.md 同步。
- 页脚版本锚点 `site/dukou-engine.html` 需人工插入（bump_version.py 不自动改它）。
- 跑 `python scripts/verify_delivery.py` 必须全绿（六文档版本 / A4 209 / 范围漂移 / 导航 / 链接 / sitemap / 回退 / 数据漂移）。

## 4. 禁改清单（文档规范 §11.2）

- CHANGELOG.md 历史版本段（W001-W423）、归档 3 份、.env、SECURITY-AUDIT 档、verify_delivery.py、bump_version.py、字体源 `assets/fonts/source/`。
- 批量重写脚本改完先 `git diff --name-only` 对比改动范围，对"本应无变化"文件 `git restore` 回退。

## 5. 内容质量规则

- **无占位符**：不留 `XXX`/`TBD`/空段；"待补"仅限双索引 W 段且当 W 内补上。
- **事实准确性**：原著引文必须逐字核对（可标回目）；统计数字标注"待全量数据验证"，不编造。
- **相对链接有效**：人物文内互链（人物谱系表、关联人物、深化专题互链）目标必须存在。
- **轨标取值**：教学讲解 / 个人创作（双轨写作表见 项目说明.md）。

## 6. 反模式（历史教训）

- A3 人物**不套** `docs/_templates/article-template.md` 六段式（模板与线上脱节，L1 贴合率 0%）。
- 禁止重跑 `w286_merge_yuanwen_shendu.py`（SD 编号≠回号；A1 深度解读会错位）。
- 外传/方向二想象不得与原著核心设定冲突（例：白骨精出身不得与"三变戏悟空"矛盾）。
- 别把 A4 主题专题（docs/03）规范误用于 A3 人物。
