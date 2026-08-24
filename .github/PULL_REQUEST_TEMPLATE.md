<!-- 感谢贡献！提交前请确认以下要点（详见 CONTRIBUTING.md 与 交接文档.md）。 -->

## 变更类型

- [ ] 内容（docs/ 解读、人物、主题等）
- [ ] 可视化（site/data/ 或 site/en/ 页面）
- [ ] 文档 / 治理（README、AGENTS.md、方法论等）
- [ ] 工程（脚本、门禁、CI/CD）

## 关联 W 批次

<!-- 如 W499；内容批次见 CHANGELOG.md 最新段。无则填"无"。 -->

## 改动范围

<!-- 运行 git diff --name-only 后粘贴改动文件清单；批量改动请确认无非必要 diff。 -->

## 验证

- [ ] `python scripts/verify_delivery.py` 核心全绿
- [ ] 改内联脚本后已重跑 `python scripts/generate_csp.py`（如涉及）
- [ ] 新增文档已同步双索引（CHANGELOG / file-index）与六文档（如涉及）
- [ ] 新增可视化页已登记 tag-cloud / sitemap（如涉及）
- [ ] 声称的回目 / 链接 / W### 已逐条 Grep 验证（E1 铁律）

## 备注

<!-- 其他需要 reviewer 注意的事项 -->
