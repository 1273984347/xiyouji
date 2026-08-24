# 猪八戒 · 数据源与生产规则

## 数据源

- dataset JSON：`dataset/character-relationship-3d.json`、`dataset/pilgrim-team-dynamic-network.json`、`dataset/pilgrim-team-psychology-arc.json`。
- 可视化页：`site/data/character-relationship-3d.html`、`character-presence-timeline.html`、`character-sentiment-arc.html`。
- 英文页：`site/en/character-bajie.html`。
- 全文检索：`dataset/text-search.json`（全书 100 回原文，708441 字，约 2MB——`site/data/text-search.html` 内嵌语料已迁出页面（2026 迁出），仅剩检索壳，必须读 JSON）。

## 生产规则（写八戒内容必读）

- 家族选择：主档案=基础七段；学术=深化专题；创作=方向二。
- W### 溯源、双索引（CHANGELOG/file-index/A1 反链）、verify_delivery 全绿、E1 铁律 Grep 验证。
- 反模式：不套 article-template；禁重跑 w286；"净坛使者"是第 100 回授封，勿写成佛。
- 注意第 18 回（高老庄）与第 19 回（云栈洞）的收服顺序细节，引用前核对原文。
