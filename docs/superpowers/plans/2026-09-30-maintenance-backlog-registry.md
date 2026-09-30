# 维护态 Backlog 登记 — 外部路线图保真度裁决（2026-09-30）

> 来源：外部「项目优化路线图」提案（P0/P1/P2 共 40+ Issue 的完整 playbook）——经逐条对仓库取证裁决后，用户裁决：**不创建 Issue，仅登记 5 项真增量**（登记≠开工·维护态不主动执行）。
> 生成：2026-09-30（W634）·快照基准 v2.3.233 / W633。
> 用途：**重启时的输入清单**——当且仅当归档裁决解除（W626 触发条件）或用户逐项点名时，按下表执行。

## 一、裁决结论

该路线图在「真·早期项目」语境下合格，但对本仓库 **~80% 为重复劳动或倒退**，快照停在 W575 时代（同日第四份旧快照审读）。P0 十三项裁决：**8 项已完成或被超越、3 项大半完成、2 项真增量小项**；P1/P2 大量主张（知识图谱/情感分析/批评史/i18n/暗色/PWA/移动端/RAG）均为已上线能力。

### P0 逐项处置（8 已完成 · 3 大半 · 2 增量）

| 路线图 P0 | 实况 | 处置 |
|---|---|---|
| 死链检查 CI | lint_links（门禁）+check_dynamic_links（第 21 门禁）双轨 | 已完成·lychee 不引 |
| axe 基线扫描 | a11y 门禁 E2-2 + CI 6 矩阵 job | 已被超越 |
| Lighthouse CI | perf.yml 预算门禁（3D 页独立预算） | 已完成 |
| Pagefind 搜索 | W573/594 站内检索（772+233 页·零外域·file://） | 已被超越·不引 |
| 100 回 frontmatter | **100/100 已内嵌 chapter-meta**（num/couplet/main_characters/locations/word_count） | 🔶 见 backlog-5 |
| entities.json | 无独立文件·chapter-meta 即实体源 | 🔶 见 backlog-5 |
| 统一设计 token | tokens/system + 覆盖率门禁 + 对比度门禁 | 已被超越 |
| JSON Schema 校验 | 数据漂移门禁（47 副本）+ 内容一致性门禁（W555）等价 | 有等价物·不另建 |
| sitemap/robots/OG | W591 五项 + 第 26 门禁（W630 挂载）+ robots.txt 在位 | 已完成 |
| CITATION/CONTRIBUTING | 均在（CITATION 已随批级联同步·W628 起） | 已完成 |
| Three.js 性能 | 独立 LHCI 预算 + W563-566 perf 批；懒加载/回退未做 | 🔶 见 backlog-4 |
| markdownlint | 无 | ✅ 见 backlog-3 |

## 二、Backlog 登记（5 项·登记不开工）

| # | 项 | 量级 | 执行要点（重启时照此做） |
|---|---|---|---|
| B-1 | **RSS feed**（site/rss.xml 生成器 + link 标签） | 小 | 仿 gen_sitemap.py 模式；源=docs INDEX 或 CHANGELOG 现役段；入 verify 可选 |
| B-2 | **CodeQL job**（security.yml 增 analyze） | 小 | js/python 两矩阵；注意 runner 时长（security 现有 job 数分钟量级） |
| B-3 | **CODE_OF_CONDUCT.md** | 微小 | Contributor Covenant 中文版即可；README「贡献方式」节加链接 |
| B-4 | **Three.js 懒加载+静态回退**（4 页：relationship-3d ×2/journey-geo-3d/dukou-engine） | 中 | 动态 import() 三脚本（同 W627 fetch 切换模式）；回退=首帧 canvas 截图 or SVG 占位；LHCI 3D 预算（LCP12000/TBT900）复验 |
| B-5 | **A1 chapter-meta 扩字段 + entities.json 聚合**（monsters/treasures/themes/related ×100 篇实体标注；聚合器读 chapter-meta 出 entities/*.json） | 中 | **属内容标注工作·须归档裁决解除或用户点名**；聚合器可先行（纯机械·读 100/100 现有 meta 出 characters/locations 两类）；Schema 沿用 chapter-meta 现有键风格 |

## 三、已否决（与冻结裁决冲突·不再议）

- 社区运营/众包/商业化/双授权——单人+AI 协作模式与商业化否决均有在先裁决；
- 一切内容扩容类（多版本对照/故事化叙事/相似推荐/阅读路径专题）——W626 归档裁决明文冻结，重启条件见 W626；
- 云原生/Astro 迁移/外包组件库——file:// 直开与零外域为设计铁律（AGENTS §6-5），现体系（27 门禁+双索引）已覆盖其试图解决的质量问题。

## 四、本次审计方法论备忘

第四份旧快照审读实证（前三份见 W628 前会话）：外部分析普遍停留在 README 旧叙事（本例 W575 时代），**P0 提案中 ~80% 在仓库已有等价或更强实现**——裁决姿势不变：实证主张逐条跑命令、战略建议对照冻结裁决、「已存在」优先于「新建」。
