# Phase E 遗留收尾（W494）· 批次记录

> 收口报告：[2026-08-22-phase-e-e6-closure-report.md](2026-08-22-phase-e-e6-closure-report.md) §四遗留项
> 用户 2026-08-22 指令：剩余两项（断点规范化 + 图表降级）与字体专项一起排进 W494

## 落地明细

| 项 | 内容 | 验收 |
|:---|:---|:---|
| 断点常量规范化 | 全站 380 处非白名单断点映射到白名单 {375, 480, 640, 768, 1024, 1280, 1536}（两轮：5xx-9xx 按最近白名单 238 处；小断点 220-420 → 375/480、大断点 1000-1440 → 1024/1280/1536 共 142 处）；残留 0 | 5 视口（375/480/640/768/1024）× 11 页溢出 FAIL=0 |
| 图表 ≤640px 降级 | system.css 新增 W494 段（≤640px：图例/legend 纵排 + 轴文字 10px + 图表容器 padding 收窄 + tooltip max-width 220px），CSS 显示层降级、D3 渲染不变；inline_css --force 传播 225 页 | 结构/JS/CSP 门禁全过 |
| 存量响应式缺陷修复 | tag-cloud（CN+EN）搜索 input 缺 box-sizing:border-box 致 375px 溢出 417px → 补上；81-hardships（CN+EN）图表 svg 固定 360px 在 1024px 溢出 → 加 `svg{max-width:100%;height:auto}` | 复测 5 视口 0 溢出 |
| CSP | inline_css 传播后 6 页 hash 漂移 → 重跑 generate_csp.py 归零 | 1189 哈希 0 漂移 |

## 字体切片/瘦身：判定关闭（非推迟，给出根因）

1. **unicode-range 切片不可行**：data/en 225 页为内联架构（inline_css 已移除外部 link 锚点），切片声明只能进 tokens.css 内联——16 片 unicode-range 声明 134KB×225 页远超 33KB 预算线（单页将 +134KB）。
2. **Serif VF 子集化收益 ≈ 0**：NotoSerifSC-VF 3636→3555KB（-81KB，VF 变化轴全保留，woff2 压缩下差异极小），已回滚。
3. **结论**：字体性能现状 = Sans 已子集化（9340 字 773KB）+ Serif VF 3.6MB（标题用字，本地 file:// 首屏加载可接受）；切片/瘦身关闭，不排后续批。

## 门禁

verify_delivery 核心全绿（含 W493 三门禁）；check_structure 0 失衡；CSP 1189 哈希 0 漂移；lint_links 0 broken。

---

## 落地状态记录（执行回写）

| 批次 | 状态 | commit |
|:---|:---|:---|
| W494 本批 | ✅ 完成 | 96aed98（v2.3.93） |

**验收注记（W495 补）**：本批「5 视口×11 页溢出 FAIL=0」回归数据测于 INLINED CSS 被 W493 清空的无样式页面，证明力作废；W495 热修复后以 7 视口（375/390/414/480/640/768/1024）× 7 页「样式+溢出+pageerror」三重断言重测，ALL PASS。
