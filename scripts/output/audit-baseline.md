# v0.7 Audit Baseline（Phase A 启动基线）

> 创建时间：2026-07-21
> 方法：Chrome DevTools MCP 运行时验证 + Lighthouse 审计
> 服务器：python -m http.server 8000（site/ 目录）

## A0.2 dashboard.html 运行时状态

- **截图**：通过 Chrome DevTools take_screenshot 获取（fullPage，作为响应附件，未存文件因 MCP 路径限制）
- **渲染状态**：35 个 kpi-card 可见，hero 深色渐变正常

## A0.3 dashboard.html console + network

### Console
| msgid | 级别 | 内容 |
|---|---|---|
| 1 | error | Failed to load resource: 404 |
| 2 | log | [INFO] 使用嵌入数据： fetch failed |
| 3 | error | Failed to load resource: 404 |

### Network
| reqid | URL | Status |
|---|---|---|
| 1 | http://localhost:8000/dashboard.html | 200 ✓ |
| 2 | https://d3js.org/d3.v7.min.js | 200 ✓（CDN 正常） |
| 3 | http://localhost:8000/scripts/output/data/hardships_81.json | 404 ✗（符合 F1，output/data 为空） |
| 4 | http://localhost:8000/favicon.ico | 404 ✗（P3，无 favicon） |

## A0.4 抽样运行时验证（4 页）

| 页面 | console error | console warn/log | JS 运行时错误 | 渲染状态 |
|---|---|---|---|---|
| dashboard.html | 2（404 资源） | 1 log（fallback） | 无 | 35 卡片正常 |
| criticism-history.html | 6（404 资源） | 6 log（[INFO] 使用嵌入数据） | 无 | 5 模块正常 |
| relationships.html | 4（404 资源） | 4 warn（[fallback]） | 无 | 4 图表正常 |
| index.html | 0 | 0 | 无 | 导航正常 |

### 发现 P2-1：fallback 日志级别不一致
- criticism-history.html 用 `console.log`（[INFO]）
- relationships.html 用 `console.warn`（[fallback]）
- 建议统一为 `console.log`（fetch 失败走 fallback 是设计预期，非警告）

## A0.5 Lighthouse 审计（3 关键页）

| 页面 | Accessibility | Best Practices | SEO | Agentic Browsing | Failed audits |
|---|---|---|---|---|---|
| dashboard.html | **85** | 96 | 90 | 100 | 4 |
| criticism-history.html | 97 | 96 | 90 | 100 | 3 |
| concept-device.html | 92 | 96 | 90 | **86** | 4 |

### 关键发现
- **P1-1**：dashboard.html Accessibility 85（最低，需提升到 90+）
- **P1-2**：concept-device.html Agentic Browsing 86（最低，其他页 100，需排查交互元素 a11y）
- **P2-2**：所有页 SEO 90（一致，可能有共同改进点如 meta description）

## Baseline 结论

- **运行时健康**：4 页抽样均无 JS 运行时错误，EMBEDDED_DATA fallback 机制工作正常
- **a11y 瓶颈**：dashboard.html（85）和 concept-device.html（92 agentic 86）是 Phase A 修复重点
- **一致性**：fallback 日志级别不统一（P2）
- **预期 404**：所有 JSON fetch 404 是 F1 导致的设计预期行为，非 bug

## 下一步

进入 A1（DRL R0 阶段判定）→ A2（R1 全量静态审查 35 页 + 主代理 spot-check 关键页 a11y 详情）
