# W808 提交 pathspec 清单（供提交方使用）

> 用途：W808 批（Web Agent 全栈加固）的显式 pathspec——防 `git add -A` 把并行批改动卷走。
> 生成时间：2026-10-20 · 配套说明见同目录说明段落。

## 硬约束

1. **必须用显式 pathspec 提交**（`git commit -F <msgfile> -- <本清单文件>`），
   禁 `git add -A` / `git add .`（会把并行批 W810 的两页搜索页卷进本提交）。
2. **禁 `--no-verify`**（pre-commit hook 已修好：jieba==0.42.1 已按 scripts/requirements.txt
   固定版本装入 workbuddy 解释器，第 46 槽门禁现 0 FAIL，可走正常提交路径）。
3. **禁 `git add -A` 重扫**：本清单即最终应入提交的文件集，工作树另有 2 个未暂存文件
   （并行批 W810 的改动，见下「必须排除」）。

## 必须排除（并行批 W810 的工作树改动）

```
site/data/search.html
site/en/search.html
```

两页各删 1 行 legacy 死数组 `window.SEARCH_INDEX = [...]` + 重算 CSP 哈希——属 W810
「站内搜索死代码清理批」，已在工作树但不在本批暂存区。

## C3 门禁耦合（重要·勿拆分 AGENTS.md 与 verify_delivery.py）

第 31 门禁 doc-sync 的 C3 判据：`AGENTS.md §4.2 最高槽号 == verify_delivery.py 最高「第 N 槽」`。

- 本批暂存的 `AGENTS.md` 已含 **`46. 搜索索引新鲜度（check_search_index_fresh.py·W809）`**
  ——该行属 **W809** 的改动（与本批 W808 的级联脚注同处一文件）。
- `HEAD` 的 `verify_delivery.py` 最高槽 = **45**；暂存版 = **46**（W809 挂载第 46 槽）。

**故：若提交 `AGENTS.md` 而不带 `verify_delivery.py`，提交树将出现 a_max=46 / v_max=45
的错配 → C3 判红。** 两者必须同落一个提交，或都暂不落。

本清单已把 W809 的 `verify_delivery.py` 一并纳入（见下），以保证提交树口径自洽。
W809 的其余 5 个文件（`check_search_index_fresh.py` / `_gen_search_index.py` /
`docs/agent/gates.md` / `tests/unit/test_check_search_index_fresh.py` /
`scripts/output/_w809_spec.json`）**亦一并纳入**——理由：
`verify_delivery.py` 挂载第 46 槽后若缺 `check_search_index_fresh.py`，门禁索引健康段
会判「挂载脚本不存在」而红；三份生成索引（`scripts/index.md`、`scripts/output/index.md`、
`tests/unit/index.md`）已列入这批新文件，缺一即触发第 45 门禁 C2/C3 清单漂移。

> 结论：W809 的「门禁挂载」实体改动与 W808 同落一次提交，W809 后续只需按其
> `_w809_spec.json` 补 CHANGELOG 版段与对账表收官登记（号序仍为 W808 → W809 → W810）。

## 本批提交文件清单（85 个）

见同目录 `w808_commit_files.txt`（每行一个 repo 相对路径，可直接喂给 `git commit --`）。
含本说明文件自身与该清单文件。

> 校验方式：`git diff --cached --name-only` 与清单文件逐项对拍——85 == 85，
> 且两页 W810 搜索页**不在**其中。
