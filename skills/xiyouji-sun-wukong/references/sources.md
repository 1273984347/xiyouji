# 孙悟空 · 数据源与生产规则

## 数据源

- dataset JSON：`dataset/character-relationship-3d.json`（22 节点/32 边）、`dataset/pilgrim-team-dynamic-network.json`、`dataset/pilgrim-team-psychology-arc.json`。
- 可视化页：`site/data/character-relationship-3d.html`、`character-presence-timeline.html`、`character-sentiment-arc.html`、`character-dynamic-network.html`。
- 英文页：`site/en/character-wukong.html`。
- 全文检索：`dataset/text-search.json`（全书 100 回原文，708441 字，约 2MB——`site/data/text-search.html` 内嵌语料已迁出页面（2026 迁出），仅剩检索壳，必须读 JSON）。
- 逐回解读：`docs/01-全书逐回解读/`（第 1、2、7、14、27、56-58、61、100 回为高频入口）。

## 生产规则（写悟空内容必读）

- 家族选择：主档案=基础七段；学术=深化专题；创作=外传/方向二。
- W### 溯源：深化专题/新内容必须带真实 W###（见 CHANGELOG），替换"待补"。
- 双索引：正向 CHANGELOG + 反向 file-index + A1 反链（`../../01-全书逐回解读/第NNN回-*.md`）。
- 门禁：改完跑 `python scripts/verify_delivery.py` 全绿。
- E1 铁律：声称的回目/链接/W### 逐条 Grep 验证。
- 反模式：不套 `docs/_templates/article-template.md` 六段式；禁止重跑 `w286_merge_yuanwen_shendu.py`；外传想象不得与正典冲突（如"齐天大圣"自封于第 4 回）。
