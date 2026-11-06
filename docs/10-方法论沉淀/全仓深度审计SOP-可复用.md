# 全仓深度审计 SOP（可复用·2026-11-06 沉淀）

> **版本**：V1.0
> **日期**：2026-11-06
> **来源**：W1149 B1/B2 施工批；承接《全仓逐逻辑深度审计报告》《基础设施口径与门禁全量审计报告》《数据分层与 reader/dataset 修复方案》
> **状态**：现行方法论（工具 + 清单 + 判据模板）
> **读者**：后续接手 Agent、维护者

---

## 1. 什么时候用

出现以下任一情况时，按本 SOP 做**只读全仓审计**，不要直接改代码：

- 用户要求「全仓 / 逐逻辑 / 全面」审查；
- 新增了一个产物族（新目录、新数据树、新页面类型）；
- 某类缺陷反复出现，需要判断是「个例」还是「结构性盲区」；
- 批次收尾前需要确认「本轮声明是否真的落地」。

**第一原则**：先修判据与机制，再改数据；只改数据会把缺陷固化进下一轮快照。

---

## 2. 五维扫描矩阵

每个产物族都按同一张表过一遍；缺哪一维，哪一维就是下次的盲区。

| 维度 | 问什么 | 机器入口 |
|:---|:---|:---|
| 覆盖 | 声明扫全站，实际扫了哪些目录/文件？ | `scripts/audit_repo.py patterns` |
| 失败语义 | 文件缺失、解析失败、扫描面为 0 时，判绿还是判红？ | 逐脚本读 `main()` 与 `except` |
| CI 形态 | 干净检出 / 浅克隆 / 无浏览器时，判据还执行吗？ | 看取数是否依赖 `git status/diff/merge-base` |
| 数据血缘 | 这个文件从哪来、经什么变换、谁消费？ | `scripts/audit_repo.py trees` |
| 同类复发 | 同一写法在其他目录是否也存在？ | `scripts/audit_repo.py patterns` |

---

## 3. 标准流程（七步）

1. **隔离**：`git worktree add <path> -b <branch> HEAD`；先 `reserve_w.py` 取号。
2. **盘点**：列出产物族、文件数、体积、消费方（`audit_repo.py trees`）。
3. **失败语义全扫**：对每个 `check_*` 找「扫描面为空 / 解析失败 / 异常被吞」三条路径。
4. **逐判据深读**：只读源码 + 无写实跑；每条发现必须有「文件:行 + 代码原文或实测值」。
5. **同类写法扫描**：`audit_repo.py patterns`，把结论从「reader 有」升级为「全站分布」。
6. **报告落盘**：`docs/11-方案报告/审查与评审/`，头五要素 + 严重度 + 置信度图例；README 登记。
7. **判据同批落地**：每修一类，新增/扩展一个机器判据 + 负样本；禁止只写文档。

---

## 4. 可直接复用的命令

```
python scripts/audit_repo.py all            # 五维总览（只读·退出码 0/1/2）
python scripts/audit_repo.py reader         # reader 完整性四判据
python scripts/audit_repo.py dataset        # dataset 清单/schema/哨兵/引文状态
python scripts/audit_repo.py trees          # output / site-json / dataset 三树
python scripts/audit_repo.py patterns       # 占位/旧前缀/多 h1/同题全站分布
python scripts/check_reader_integrity.py --self-test
python scripts/check_dataset_manifest.py --self-test
python scripts/check_dataset_provenance.py --self-test
```

`scripts/output/data` 多数是本地生成产物、不入库：新克隆里 `trees` 会报 `output_available=false`，先跑 `run_all.py` 再对拍，不要把它当成「0 文件」缺陷。

---

## 5. 四类高频根因（本项目实证）

| 根因 | 表现 | 修法 |
|:---|:---|:---|
| **CI 形态恒空** | 取数靠 `git status/diff/merge-base`；干净检出或浅克隆为空 ⇒ 判据在 CI 等于没跑 | 改用仓内 spec / manifest / 文件树作判据分母 |
| **扫描面缺口** | 声明「全站」实际只扫 `site/data`；reader / en / 内联脚本成为盲区 | 扫描面与产物族登记表绑定，新目录未登记即 FAIL |
| **子串/注释满足** | `"foreign_keys = ON" in text` 被注释满足；`"gen" in js` 命中 `generate` | 剥注释 + 结构化解析 + 负样本 |
| **多层快照无血缘** | output → site-json → dataset 三层各自手改，无 `derived_from`/hash | manifest + 发布/派生管线 + 新鲜度门禁 |

**反面模式**：为迎合判据补数据、在调用处加特例、用豁免压红灯、修完症状不追问触发条件（铁律 15）。

---

## 6. 发现记录模板（直接抄）

```
| # | 文件:行 | 缺陷 | 证据 | 影响 | 级别 | 置信度 |
| 46 | check_x.py:41,56 | 两侧解析为空 ⇒ 0==0 判绿 | 源码 findall 返回空表；compare 只比 len | 格式重构后第 N 槽空转 | P1 | 高·读源码+实跑 |
```

- 级别：**P0 安全** > **P1 假绿/数据失真** > **P2 加固/覆盖缺口** > **P3 一致性/文案**。
- 置信度必须写「实跑确认 / 读源码确认 / 子代理证据」；未复跑的不要标 ✅。
- 每条都要能回答：**这个判据为什么会被触发？** 答不出就是没找到根因。

---

## 7. 新产物族准入（防复发）

新目录 / 新数据树 / 新页面类型进入仓库时，同一批必须提交三件：

1. **manifest**：来源、变换、消费方、hash；
2. **门禁矩阵条目**：该族由哪些槽覆盖（缺的写 NOTE 与计划）；
3. **生成器 + 负样本**：生成器可重跑，判据至少一例必红。

三件缺一，下一批就会长成新的 reader/dataset 式盲区。
