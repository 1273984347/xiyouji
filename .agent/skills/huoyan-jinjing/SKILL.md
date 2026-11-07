---
name: huoyan-jinjing
description: |
  详解西游记项目的「全仓巡检」速查 skill（火眼金睛）。当需要做全仓审计、扫描
  新目录/新数据树、判断门禁是否假绿、对照多层数据快照、清理重复内容，或为
  新产物族设计准入时使用。只给判据与入口，完整方法论文档在
  docs/10-方法论沉淀/全仓深度审计SOP-可复用.md。
license: MIT
compatibility: any-agent
---

# 火眼金睛 · 全仓巡检速查

> **编制位出处**：《取经编制表》悟空位 · 火眼金睛（第 7 回）。
> 「你不知老孙在这太上老君八卦炉中炼了七七四十九日，炼成火眼金睛。」——
> 火眼金睛不是看得更远，是**能认出 disguise**：假绿、盲区、被注释满足的判据。
> 本 skill 只放速查子集；完整方法论文档：
> [docs/10-方法论沉淀/全仓深度审计SOP-可复用.md](../../../docs/10-方法论沉淀/全仓深度审计SOP-可复用.md)

## 一、悟空 · 火眼金睛：先扫五维（缺一维就是下次的盲区）

1. **覆盖**：声明「全站」实际扫了哪些目录？`python scripts/audit_repo.py patterns`。
2. **失败语义**：文件缺失 / 解析失败 / 扫描面为 0 时，判绿还是判红？读 `main()` 与 `except`。
3. **CI 形态**：取数是否靠 `git status/diff/merge-base`？干净检出/浅克隆为空 ⇒ CI 上等于没跑。
4. **数据血缘**：这个文件从哪来、经什么变换、谁消费？`python scripts/audit_repo.py trees`。
5. **同类复发**：同一写法在 `site/data`、`site/en`、`site/reader`、`dataset`、`output` 是否也有？

## 二、唐僧 · 紧箍咒：判据必须能念紧（fail-closed）

6. **判据不可执行 ⇒ 判红（退出码 2）**，不许 `except: pass` 后给绿。
7. **禁止纯子串满足**：`"foreign_keys = ON" in text` 会被注释满足；`"gen" in js` 会命中 `generate`。先剥注释/字符串，再结构化解析。
8. **禁止只判一种写法**：`<SCRIPT>` 大小写、`--open=` 前缀缩写、协议相对 `//cdn`、无引号 `src=//`，都要进负样本。
9. **每条新判据必须配负样本**：至少一例「必红」；没有负样本的判据＝未证明可证伪。

## 三、八戒 · 九齿钉耙：数据清理先分级

10. **占位词**：出厂页面禁「（待补）/待完善/TODO/FIXME/Lorem」；源头在 docs/模板，补 HTML 会被下次生成覆盖。
11. **空值**：`[]` 与 `null` 不是同一件事——`none`（确无）与 `unknown`（待补）必须用 `<field>_status` / `field_status` 标注。
12. **哨兵**：`chapter=0` 不是「无回目」的合法表达；用 `null` + `chapter_scope`，禁止数字哨兵。
13. **量纲**：权重 0–1 与 4–10 不能混用；每个文件声明 `_schema.weight_scale`，只声明、不擅自重标定。

## 四、沙僧 · 行李担：清单必须与磁盘对拍

14. **README 表格、大小、条目数必须由脚本从磁盘生成**（`python scripts/gen_dataset_index.py`）；手写清单三周必漂。
15. **manifest 三件套**：`source / derived_from / consumers`；派生目标不存在或 hash 不符 ⇒ 判红。
16. **三树分工**：`scripts/output/data`（计算权威）→ `site/data/json`（运行时发布）→ `dataset`（对外快照）。不物理合并，用 manifest 连接。
17. **台账窗口**：正本 ≤ 60 行；归档必须保留在途行（`archive_ledger_rows.py --keep 59 --apply`）。

## 五、白龙马 · 驮经：链接与发布管线

18. **GitHub 链接必须映射仓内真实文件**：`blob|tree/main/<path>` 逐条解析；`docs/source/` 旧前缀是生成器单点缺陷，不是页面问题。
19. **相对链接内联**：reader 页生成后必须 `inline_css.py --reader --inline-links`（`build_reader.py` 已内置自动调用），否则 622 页退回外链。
20. **改 md 的连锁顺序**：改 md → `_gen_search_index.py` → `generate_csp.py` → 跑门禁；顺序反了必红。
21. **改内联脚本必重算 CSP**：`python scripts/generate_csp.py`，`--check` 必须 0 漂移。

## 六、观音 · 三根救命毫毛：修复三原则

22. **先修判据/机制，再改数据**；只改数据会把缺陷固化进下一轮快照（铁律 15）。
23. **同批回归锁**：修哪类，就在同批加「必红」负样本；否则下一形态复发。
24. **提交前三问**：本批问题全解决或登记去向？防复发判据/坑表落地？其他 Agent 能否从项目文件了解？

## 七、十分钟巡检命令（可直接复制）

```
python scripts/audit_repo.py all                # 五维总览（reader/dataset/trees/patterns）
python scripts/audit_repo.py reader             # 占位/GitHub 链接/单 h1/标题唯一
python scripts/audit_repo.py dataset            # README/量纲/哨兵/空值/引文状态
python scripts/check_reader_integrity.py --self-test
python scripts/check_dataset_manifest.py --self-test
python scripts/check_dataset_provenance.py --self-test
python scripts/check_inlined_css.py             # 849 页 INLINED 块完整性（含 reader）
```

## 八、何时停手（如来 · 五指山）

发现 30+ 条时**不要一把抓**：按 P0 安全 → P1 假绿/数据失真 → P2 覆盖缺口 → P3 一致性分批；
每批只修一类，并同批落判据。把「其余发现」写进报告与台账，比一次改 77 处更安全。

## 与项目其他载体的分工

- 避坑速查 → 本目录 `puti-shouye`（菩提授业·15 条）；
- 全量坑表 → `pitfalls.md`（六主题）；
- 门禁全量定义 → `docs/agent/gates.md`；
- 完整审计方法 → `docs/10-方法论沉淀/全仓深度审计SOP-可复用.md`；
- 可执行入口 → `scripts/audit_repo.py`。
