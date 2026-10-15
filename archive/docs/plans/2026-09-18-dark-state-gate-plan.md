# 暗色态门禁常驻化方案（O2 挂载评估·W570 报告 WBS 1）

> 创建：2026-09-18。来源：W572 入库报告（2026-09-16）§7.2 WBS 1「O2 暗色门禁常驻化方案入档（T0+1）」。
> 决策点：本方案为挂载评估——实施与否由用户确认（沿 W551/W569 门禁挂载先例：方案 + 基线数据 → 用户明示）。

## 1. 目标与背景

夜间模式经 `prefers-color-scheme` 自动应用于 230/232 页，而验收体系（截图审查/a11y/复审）全部浅色单态——暗色缺陷 318 处/44 页（光晕感知诚实基线，W571）无一被门禁拦截，靠用户感知暴露。本方案把暗色态检测并入 CI，只拦新增、不追溯存量。

## 2. 方案

复用既有审计器 `scripts/_audit_render_states.js`（--states 参数化已支持），新增 CI job（或并入 screenshot-review workflow 尾部）：

```yaml
- name: Render-state dark audit（S2 抽查）
  run: node scripts/_audit_render_states.js --states S2-desktop-dark --pages <图表页清单>
```

- **范围**：首期限「图表页」（site/data + en 对应有 svg 的页面，约 120 页）——根页与章节页暗色已有适配或无图表。
- **判定**：对比 `scripts/output/render-state-audit-baseline.jsonl`（318 处基线快照）——**同页同类型缺陷数只增即 FAIL**（新增拦截），存量不阻断。
- **成本**：CI 时长 +8–10 分钟/批（120 页 × ~4s + 启动）；本地复跑同命令。
- **配套**：① 基线快照随批更新（缺陷修复批下降后手动刷新，防锁死）；② 审计器跑批并行化（O1，35→15 分钟）作为前置优化，可选。

## 3. 验收与回滚

- 挂载后首批：S2 抽查 FAIL 数 = 0（基线内）；此后任何暗色新增缺陷在提交前/CI 拦截。
- 回滚：删除 job 即回滚，无副作用。

## 4. 待决点

1. 是否挂载（用户确认）；2. 全量 232 页 vs 图表页 120 页抽查范围；3. 基线快照的更新责任（修复批 Agent 手动刷新 vs 自动化）。

## 5. 落地状态（2026-09-18 W579，用户裁决「挂载」）

- **三待决点裁决**：① 挂载——已批准并实施；② 范围=全站含 `<svg` 图表页 **163 页**（方案估 120 实测 163；site/data 78 + en 79 + 站点根 6，`--scope charts` 机判口径单一来源，方案原 `--pages <清单>` 形态改为 `--scope` 参数）；③ 基线更新=修复批 Agent 手动 `node scripts/check_dark_state_gate.js --update-baseline`（防锁死）。
- **实施**：screenshot-review workflow 增独立 `dark-state-gate` job（与主截图 job 并行，不延长墙钟；页脚-only push 跳过；失败上传审计产物 artifact）。
- **基线**：`scripts/output/render-state-audit-baseline.jsonl`（S2-desktop-dark × 163 页）——**318 处/44 页，与 W571 诚实基线完全对账**（lowContrast 16 + invisible 302）；暗色已应用 163/163。
- **判定口径**：同页同类型（pageError / lowContrast / invisible）只增即 FAIL；**对方案的偏离声明：hOverflow 不入本门禁**（视口相关非主题相关，S1 截图门禁已覆盖，避免双门禁抖动误报）。另含「暗色未应用」回归拦截（基线暗色已应用而当前未应用）。
- **验证**：--self-test 5/5；同环境双跑 163 页计数零差异；实弹篡改（+1 lowContrast）→ FAIL 定位准确、还原 → PASS；CI 五工作流见 push 后确认。
- **成本实测**：本地 163 页扫描 ≈ 12 分钟/次（CI 并行 job 内，不占主截图 job 墙钟）。
