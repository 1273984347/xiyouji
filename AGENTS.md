# AGENTS.md — 《详解西游记》Agent 行为地图

> **定位**：《详解西游记》＝「一源多形·数字人文可视化解读《西游记》100 回」——docs/ 解读文档 629<!--stats:a1_a6_docs--> 篇 + 纯静态站（file:// 直开）+ 90<!--stats:visualization_pages--> 个 D3/Three 可视化页 + 渡口问津 Web Agent。
> **本文件是 AI 行为地图，不是手册**：铁律＋路由＋命令。规模/目录/架构看 README 与 STRUCTURE（§ 路由表）；治理文件自身的改法看 docs/agent/MAINTAINING.md；现役规模与状态以 `python scripts/agent_start.py` 实读为准（防记忆代读）。

## 一、硬约束（铁律 24 条·每会话为真·违反即返工）

1. **六文档同步（W393 降级）**：每完成一个 W 批次，核心 2（CHANGELOG + HANDOVER）必须写，辅助 4（README/STRUCTURE/项目说明/file-index）里程碑时跑 bump_version.py 补齐。
2. **E1 铁律（声明 ≠ 落地）**：每个文件修改后 Grep spot-check 验证落地，禁止假收敛。
3. **改内联脚本 → 重跑 generate_csp.py**（CSP 哈希失配会整脚本被拒）。
4. **批量改 CSS/JS → 验证括号/引号平衡**（check_structure.py）。
5. **file:// 铁律**：新页面必须内嵌 EMBEDDED 回退、零外域依赖（D3/Three 本地引用 `site/static/js/`，禁 d3js.org/cdnjs 外域 CDN）。**具名例外**（W1167 G0-1 拍板·W1168 收敛为单轨·铁律 16⑦ 留痕）：唯一放行外域是 GoatCounter 回传域 `connect-src https://1273984347.goatcounter.com`；`script-src` 自 W1168 起再次为空集——GA4 轨退役（账号未建 + 大陆可达性差 + web vitals/自定义事件改由自托管链承载），统计改由自托管 `goatcounter.js` + `site/static/js/stats.js` 桥发起。例外全集唯一定义在 `scripts/generate_csp.py`（`EXTERNAL_SCRIPT_HOSTS`/`ANALYTICS_CONNECT_HOSTS`），与配置端点不一致由第 67 槽 C5 + 第 56 槽增量漂移拦下；例外之外任何外域仍为门禁违规。例外仅在线 http(s) 生效，`file://` 下统计桥短路、页面渲染零依赖统计。
6. **新页落地**：可视化页进 site/data/、索引进 site/ 根 + tag-cloud + sitemap；禁往 site/chapters|characters|themes（空遗留目录）。
7. **先取证再假设**：诊断前端显示问题，先拿截图 + Console + 复现条件，再下根因结论（见 docs/10-方法论沉淀/前端显示问题诊断SOP.md）。
8. **禁止擅改**：CHANGELOG 历史段、归档 3 份、.env、SECURITY-AUDIT 档、verify_delivery.py、bump_version.py 等门禁脚本（详见文档规范 §11.2）。
9. **禁重跑 w286_merge_yuanwen_shendu.py**（A1 深度解读 SD 编号会再次错位）。
10. **批量重写脚本改完**：`git diff --name-only` 对比改动范围，非必要改动 `git restore` 回退。
11. **双协议**：代码 MIT + 文本 CC BY-NC 4.0（非商用），拆分 LICENSE / LICENSE-CONTENT.md。
12. **动效契约（W463 固化）**：新增/修改可视化页动效必须遵守 DESIGN.md §5——时长 ≤600ms（白名单仅 hero 600 / count-up 900）、reduced-motion JS 守卫（D3 transition 不受 CSS media 控制，须 `MOYUN_RM` 调用点级或 prototype 级短路）、tooltip 统一 `.chart-tooltip` + `.classed('visible')`；批量改动后重跑 generate_csp.py + duration≤600 扫描。
13. **内容可信度轨（W505-W508 固化）**：docs/01-06 新内容必须走元信息块 v2（第 18 门禁）+ 术语一致性（第 19 门禁）+ 引文硬验证（第 20 门禁）；引文须经 `_cite_probe.py` 提取候选（§4.3），管线产出须过 `_check_pipeline_consistency.py`；归档/删除脚本须同步查 tests/ 引用（W506 教训，见 day-review skill 步骤 4-6）。
14. **修实例必修根（W998 固化）**：修复暴露同类风险时，同批或次批根治，禁止「值得排期/等点号」收尾（真需用户决策的仅限外发动作）；检查任务按委托字面范围执行；跨会话教训权威落坑表与本节，私有记忆仅作镜像（W516 载体铁则·治理季三次用户问责实证）。
15. **禁止补丁加补丁，修复必须从根因（W1039 用户令）**：修法只消症状不除结构因＝补丁（四种典型形态：为迎合判据补数据 / 调用处特例绕过 / 豁免压红 / 不问触发原因）；教训必须转机器判据（硬守卫/断言/自测）→ W1019 实证与四形态全文见归档 E-2 族 / MAINTAINING §二
16. **协作与环境约束（W1039 六则 + I-01 增补⑦·违反即返工）**：① 禁主动创建 automation ② GPU 重负载先获批分批 ③ 禁用 ~/.minimax（以项目面证据判断）④ 命令与路径完整禁缩写 ⑤ 答复显式给推荐 ⑥ 教训落仓（私有记忆仅镜像）⑦ 豁免/白名单/基线新增须用户批准 → 全文见归档 E-2 族对应条目
17. **批次流程铁律（开批占号）**——已被机械化与流程文档承载 → 批次交付流水线 §九 + docs/agent/MAINTAINING.md §六（W1279 退役收敛）
18. **批次流程铁律（提交前三问）**——已被机械化与流程文档承载 → 批次交付流水线 §九 + docs/agent/MAINTAINING.md §六（W1279 退役收敛）
19. **禁用 CodeBuddy/WorkBuddy（W1061 入必载层·用户 2026-10-07 两度重申·此前仅存私有记忆=三问 ③ 违规实例）**：项目一切 AI 功能不使用 CodeBuddy/WorkBuddy 及其任何残留；agent-web 的三选一裁决=保留但换引擎（OpenAI-compatible 自研·W680 收官/W681 事实收官）。任何会话不得引入、恢复或仿建该品牌工具链。
20. **批次流程铁律（Python 自检）**——已被机械化与流程文档承载 → 批次交付流水线 §九 + docs/agent/MAINTAINING.md §六（W1279 退役收敛）
21. **批次流程铁律（推送节奏）**——已被机械化与流程文档承载 → 批次交付流水线 §九 + docs/agent/MAINTAINING.md §六（W1279 退役收敛）
22. **批次流程铁律（体积窗）**——已被机械化与流程文档承载 → 批次交付流水线 §九 + docs/agent/MAINTAINING.md §六（W1279 退役收敛）
23. **批次流程铁律（异常分类）**——已被机械化与流程文档承载 → 批次交付流水线 §九 + docs/agent/MAINTAINING.md §六（W1279 退役收敛）
24. **批次流程铁律（并行隔离）**——已被机械化与流程文档承载 → 批次交付流水线 §九 + docs/agent/MAINTAINING.md §六（W1279 退役收敛）

## 二、路由表（何时读什么·凭本表判断相关性·勿试探性开文件）

| 文件 | 何时读 | 回答什么 |
|---|---|---|
| docs/agent/gates.md | **任何写操作或提交前 → 先跑 verify_delivery.py（退出码非 0 即阻断），红时查对应槽条目** | 门禁触发条件 + 失败处置（薄说明层·判定逻辑在门禁脚本本体） |
| pitfalls.md | 门禁红 / 同类二犯 / 批量改动前 | 421<!--stats:pitfalls_total--> 条坑位判据（**索引壳=仓库根 pitfalls.md**·E-NN 反查表；**六主题正本在 docs/agent/pitfalls-topics/**；docs/agent/pitfalls.md 为二级跳转壳勿读）·六主题：CSS / 视觉渲染（91<!--stats:pitfalls_css-->）·JS / CSP / 运行时（13<!--stats:pitfalls_js-->）·git / 提交 / 并发（39<!--stats:pitfalls_git-->）·级联 / CHANGELOG（26<!--stats:pitfalls_cascade-->）·数据 / 内容可信度（28<!--stats:pitfalls_data-->）·流程 / 协作 / 取证（224<!--stats:pitfalls_flow-->）·叙事细节在归档 |
| archive/docs/pitfalls-detail-ARCHIVE.md | 需要坑位条目全文时 | 叙事/实证细节（#### E-NN 锚·只增不改） |
| docs/10-方法论沉淀/批次交付流水线.md | 批次收官 / 推送前 | 全链 7 步 + 失败模式速查 + 收官链时间纪律 |
| docs/agent/MAINTAINING.md | **改 AGENTS/pitfalls/gates 等治理文件前** | 维护契约全文：退役三标准 / 添加前四问 / 体积预算 / 局部化预留形态 |
| docs/agent/agent-web.md | 动 xiyouji-agent-web/ | Web Agent 引擎/权限/安全边界 |
| HANDOVER.md | 接手 / 查阻塞与进度 | 当前状态（「零、当前阻塞」「一、当前进度」） |
| STRUCTURE.md | 需要目录树/技术栈/数据流 | 架构与目录（本文件不再复制） |
| README.md | 项目是什么 / 人类导航 | 项目全貌、在线站点、双协议 |
| CLAUDE.md | Claude Code 宿主 | `@AGENTS.md` 导入 + Claude 专属段（≤60 行） |
| docs/00-导读/文档规范.md | 元信息块 / 文件管控 | 禁改清单 §11.2、元信息块 v2 |
| DESIGN.md | 动效/视觉改动 | 动效契约 §5（时长三档/reduced-motion/tooltip） |
| docs/00-导读/W批次编号对账表.md | 开批占号 | 批次认领与状态（台账） |

## 三、常用命令（写操作面·完整可粘贴）

```bash
python scripts/reserve_w.py                                    # 开批占号（未占号不动手）
python scripts/preflight_check.py --touches "<清单>" --self W#  # 动工前五检+交集
python scripts/verify_delivery.py --scope docs                 # 文档改动快速档
python scripts/verify_delivery.py --scope full                 # 全量门禁（同树二次跑命中回放缓存）
python scripts/batch_closeout.py --spec scripts/output/_w####_spec.json   # 收官链单入口
python scripts/pre_push_gate.py                                # 推送判据（guardrails→verify→pytest→ci_sim）
git config core.hooksPath .githooks                            # 克隆后一次性·启用仓内 pre-push 闸门（W1288·E-312）
python scripts/safe_commit.py -m "..." --expect-spec scripts/output/_w####_spec.json  # 提交（防代提）
python scripts/generate_csp.py                                 # 改内联脚本后必跑（铁律 3）
py -3 -m pytest tests/unit -q                                  # 单测面
python -m http.server 8000                                     # 站点本地预览（http://127.0.0.1:8000/site/）
```

## 四、本机环境事实（指针）

Windows 单机的解释器三语境 / 编码 / heredoc / curl / 路径等环境坑**无法从仓库推断且每会话相关**——全文由 docs/agent/MAINTAINING.md §八 承载（W1279 迁出·AGENTS 只留指针）。

## 五、维护契约（极简版·全文与退役/添加机制见 docs/agent/MAINTAINING.md）

1. 改治理文件（本文件/pitfalls/gates）前**必读 MAINTAINING.md**——退役三标准、添加前四问、体积预算、路由表从作用域声明生成。
2. 每批核心 2 同步（CHANGELOG + HANDOVER）·批次经台账认领·提交一律 safe_commit（防代提）。
3. 有复用价值的教训落 pitfalls（16-⑥ 载体铁则）·同类两犯的纪律**上提本文件铁律区**（上提后在坑条目预防段标注）。

*本文件由 AGENTS 通读项目后生成于 2026-08-16（v2.3.73 W458）；W458-W707 沿革已迁 [archive/docs/AGENTS-ARCHIVE.md](archive/docs/AGENTS-ARCHIVE.md)（W709 建·W1298-W1298 级联自动滚动·脚注保留最近 5 条·每条 ≤120 字·日期阿拉伯形态·grep 查勿通读）；2026-11-22（W1299）：L-04① 归档孤儿段清偿（13→0·三类根因分别治本）；2026-11-22（W1300）：L-07 闭合（公共口径支持并列多批次锚·本体275→276·口径单一事实源）；2026-11-22（W1301）：L-02 闭合（探针跨run增量缓存·332s→0s·判据零改动）；2026-11-22（W1302）：hero-batch 绢本源件入站 8 张 1920×1078 webp 落 site/static/images/silk-src/；2026-11-22（W1303）西游小游戏三合一 + 十八款合集入口 + 音效/移动端/战绩。如与上述权威文档冲突，以权威文档为准。*
