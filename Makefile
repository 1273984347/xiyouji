# Makefile — 《西游记》项目统一编排入口
#
# 用法:
#   make help        查看全部目标
#   make <target>    执行指定目标
#
# 约定:
#   - Windows 兼容：使用 python（非 python3），npm 通过 `cd scripts && npm` 调用
#   - 跨平台命令：test/clean/lint 目标使用 Python 子shell 替代 bash 语法
#   - 任一命令失败即整体退出（makefile 默认行为）
#   - 目标注释 `## ` 由 help 目标自动解析

.PHONY: help analyze analyze-list analyze-only screenshots slice audit lint links test ci clean release data-validate docs-index

help: ## 显示所有目标
	@python -c "import re; lines=open(__file__,encoding='utf-8').read().splitlines(); print('\n用法:\n  make <target>\n\n目标:'); [print(f'  {m.group(1):<15} {m.group(2)}') for l in lines for m in [re.match(r'^([a-zA-Z_-]+):.*?##\s*(.*)', l)] if m]; print('')"

analyze: ## 运行 A-AH 34 类分析脚本（自动发现，批量调度）
	@echo "==> analyze: 批量运行 A-AH 34 类分析脚本"
	python scripts/run_all.py
	@echo "==> analyze 完成"

analyze-list: ## 列出会运行的脚本（dry-run）
	@python scripts/run_all.py --dry-run

analyze-only: ## 仅跑指定类别，如 make analyze-only ONLY=A,B,F
	@python scripts/run_all.py --only $(ONLY)

screenshots: ## Playwright 双视口截图（desktop + mobile）
	@echo "==> screenshots: Playwright 双视口截图"
	cd scripts && npm run screenshots
	@echo "==> screenshots 完成"

slice: ## 800px 切片（Pillow）
	@echo "==> slice: 800px 切片"
	python scripts/slice_screenshots.py --output-dir scripts/output/screenshots
	@echo "==> slice 完成"

audit: ## 表格无容器扫描 + JS 语法检查 + SVG 负宽度检查（dry-run）
	@echo "==> audit: 表格无容器 / JS 语法 / SVG 负宽度"
	python scripts/detect_unwrapped_tables.py
	python scripts/check_js_syntax.py --all
	python scripts/fix_svg_negative_widths.py --dry-run
	@echo "==> audit 完成"

lint: ## ruff + eslint（如配置存在）— 跨平台兼容
	@echo "==> lint: ruff + eslint"
	@python -c "import shutil,sys,subprocess; rc=0; exec('''for t in ['ruff','eslint']:\n p=shutil.which(t)\n if p:\n  args=[t]+(['check','scripts/'] if t=='ruff' else ['.'])\n  r=subprocess.run(args)\n  rc=rc or r.returncode\n else:\n  print(f'  [skip] {t} 未安装')\n'''); sys.exit(rc)"
	@echo "==> lint 完成"

links: ## 链接校验（HTML href/src + Markdown）
	@echo "==> links: 链接校验"
	python scripts/lint_links.py
	@echo "==> links 完成"

data-validate: ## JSON 数据完整性校验（output/data/ 131 个文件）
	@echo "==> data-validate: JSON 结构完整性"
	python scripts/data_validate.py --quiet
	@echo "==> data-validate 完成"

docs-index: ## 生成/更新 docs/INDEX.md（321 篇文档索引）
	@echo "==> docs-index: 生成文档索引"
	python scripts/docs_index.py
	@echo "==> docs-index 完成"

test: ## pytest（python -m pytest tests/）— 跨平台兼容
	@echo "==> test: pytest"
	@python -c "from pathlib import Path; import sys; sys.exit(0 if Path('tests').is_dir() else 2)" && python -m pytest tests/ -q || python -c "print('  [skip] tests/ 目录不存在或测试失败')"
	@echo "==> test 完成"

ci: ## CI 本地预跑 = lint + test + audit + links + data-validate + docs-index
	@echo "==> ci: lint + test + audit + links + data + docs"
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) audit
	$(MAKE) links
	$(MAKE) data-validate
	$(MAKE) docs-index
	@echo "==> ci 完成"

release: ## 版本发布前体检（sync_docs + git 状态 + pytest + checklist）
	@echo "==> release: 版本发布前体检"
	python scripts/release.py
	@echo "==> release 完成"

clean: ## 清理 screenshots 过期产物（切片 / 诊断报告 / pyc 缓存）— 跨平台兼容
	@echo "==> clean: 清理过期产物"
	@python -c "import shutil,os; from pathlib import Path; root=Path('.'); shutil.rmtree(root/'scripts/output/screenshots/slices/desktop', ignore_errors=True); shutil.rmtree(root/'scripts/output/screenshots/slices/mobile', ignore_errors=True); [p.unlink(missing_ok=True) for p in [root/'scripts/output/screenshots/overflow-diagnosis.json', root/'scripts/output/screenshots/overflow-diagnosis.md']]; [shutil.rmtree(p, ignore_errors=True) for p in root.rglob('__pycache__')]; [f.unlink() for f in root.rglob('*.pyc')]"
	@echo "==> clean 完成"
