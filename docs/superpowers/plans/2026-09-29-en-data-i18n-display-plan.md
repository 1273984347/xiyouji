# EN 站部署数据 i18n 显示面 —— 方案评估（W622 登记·待排期批）

> 起因：W621 修色批登记遗留「en 页部署态怪物名/角色名显示中文」。W622 已修 en/character-appearance
> （35 人全量 ZH2EN map·加载后一次性归一 characters[].name/matrix 键）。本方案覆盖其余 EN 页的
> 同族问题面与两条技术路线的取舍。

## 1. 问题面

部署数据副本 `site/data/json/*.json` 为中文内容（run_all 生成器的原语输出），EN 页 fetch 同一文件
（`../data/json/`），显示面出现中英混排：

- **枚举名层**（怪物名/角色名/地名/阶段名/术语名）：en/methodology-matrix（villain 表 monster/rescuer、
  phase 卡 phase 名）、en/chart-design（scatter tooltip monster 名）、en/journey-route 系（地名）等。
- **长文本层**（analysis/insight/characteristic 分析句）：en/methodology-matrix 表格分析列、
  en/chart-design tooltip 分析段——页面级别名不可行，必须译码数据。

W601 EN 治理只覆盖页脚/互链/泄露，未触及数据显示面；A1-英文站静态模板已英文化，数据层是剩余洼地。

## 2. 两条路线

| 路线 | 做法 | 代价 | 收益 |
|---|---|---|---|
| A 页面别名（W621/W622 同款） | 每页加 ZH2EN map·显示前归一 | 每页 10-40 行 JS·35+ 名词表重复维护 | 快·零数据风险·零门禁波及 |
| B EN 数据副本 | 生成器补 `--lang en` 输出 `site/en/json/*.json`（枚举名+长文本译码），EN 页 fetch 改指 en 副本 | 生成器改造+译码资产+data-drift 基线扩面+fetch 路径门禁复核 | 根治·tooltip/表格/长文本全英·zh/en 双源对称 |

## 3. 建议梯队

1. **快赢层（路线 A）**：en/methodology-matrix（monster 6 名+phase 3 名，复用既有 PHASE_KEY 模式）+
   en/chart-design（monster 6 名）——显示名英化，长文本仍中文（与全站 EN 页现状一致，不劣化）。
2. **根治层（路线 B）**：随需求侧主计划 WP-C（数据审计/生成器批）一并做——en 副本生成+译码资产
   （长文本量级：methodology 15 妖×3 句+chart-design 6 怪×2 段+若干 insight）+门禁对账扩面。
3. **不做**：页面硬编码译文替换数据文本（破坏单一事实源）。

## 4. 验收口径（B 路线时）

- EN 页部署态 `document.body.innerText` 抽样 CJK 密度较现状下降（枚举名层→0）
- data-drift 基线含 en/json 47+ 副本对账
- check_dynamic_links 不新增死链（fetch 路径 `../en/json/`）
