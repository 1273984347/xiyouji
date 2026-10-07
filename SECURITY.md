# 安全策略（Security Policy）

> 本文件为 OpenSSF Scorecard Security-Policy 检查项与社区安全报告渠道的落点（W683）。

## 报告漏洞

- **依赖漏洞**：本仓已启用 Dependabot alerts（依赖图自动监测）。发现后按「升级/overrides/热修」三段处置，处置记录入 CHANGELOG 对应 W 段（先例：W537/W680 deps 热修）。
- **站点与服务端问题**（XSS/CSP/路径越界等）：优先 [GitHub Issues](https://github.com/1273984347/xiyouji/issues) 提交，标题带 `[security]` 前缀；涉及未公开漏洞细节的，请改用 GitHub 的 **Private vulnerability reporting**（仓库 Security 页 → Report a vulnerability）私密提交。
- **门禁脚本**（verify_delivery.py / batch_cascade.py 等）相关问题：同走 Issues——门禁脚本属「禁擅改」清单，不接受未批改动。

## 处置口径

1. **P0/P1**（可被外部触发 / 数据损坏 / 密钥泄露路径）：当批热修 + 独立安全复核（先例：W680 引擎更换批 10 项裁决）。
2. **P2/P3**：登记 Backlog 或随下一相关批次修复。
3. 所有安全相关变更必须带**可复算验证**（负样本必红 / 恢复必绿），参照文档规范 §4.9。

## 已知设计取舍（非漏洞，勿重复报告）

- `site/` 为纯静态站，`style-src` 保留 `unsafe-inline` 为工程取舍（159 页内联 CSS 哈希化不可维护，W424）；
- agent-web 仅绑定 `127.0.0.1` 回环、默认无认证；外网暴露需显式设置 `AGENT_WEB_TOKEN`（W411）；
- 引擎工具面对 LLM 输出设有受保护路径黑名单与命令白名单（W680 复核加固），剩余低危项见引擎蓝图。

## 支持的版本

仅最新 `main` 分支获得安全修复；历史版本段（CHANGELOG 归档）不回溯修复。
