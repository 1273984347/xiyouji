# 批次收官 Checklist（W1022 沉淀 · 按顺序执行，别跳步）

> 每步都注明「跳过会红哪个槽」。本清单是 W1019–W1022 连续四批踩坑后的收敛，**顺序本身有依赖**。

## 0. 开工前
- [ ] `python scripts/preflight_check.py`：体积窗、touches 交集、各触发器提示位
      （touches 报「与在途自己冲突」属自指，确认无他方在途即可）
- [ ] 台账追加认领行（`| W#### | … | 在途（…） |`）

## 1. 写 spec（`scripts/output/_w####_spec.json`）
- [ ] `changelog_body` **必须以 `\n\n` 开场**——否则级联把段标题与正文粘成同一行（W1019 实证·precheck 已拦）
- [ ] `desc` 禁 `·` `；` `—`；`head_sentence` 禁 `；` `—`（否则下一批锚点正则失配）
- [ ] `desc` / `head_sentence` 禁**裸聚合数字**（`N 页/项/篇/个/类`）——会写入版本抬头行，第 31 槽 C5c 必红
- [ ] `agents_note` ≤120 字且以「阿拉伯日期（W###）」开场
- [ ] `changelog_body` 含 `**文件**：` 行（第 31 槽 C4-f 据它对账）
- [ ] `file_index_rows` 覆盖**全集**，含：新增件、修改件、**删除侧旧路径**（`git mv` 的两端都要）

## 2. 级联
- [ ] `batch_cascade.py --spec …`（dry-run，10 面断言全过再往下）
- [ ] `batch_cascade.py --spec … --apply`

## 3. 回窗（级联自带，但独立跑更稳）
- [ ] `archive_segments.py --apply`（CHANGELOG + file-index 段窗 109）
- [ ] `archive_ledger_rows.py --apply`（台账行窗 60）

## 4. 上批一次性脚本归位
- [ ] 台账 max 一变，**上一批**的 `scripts/_w####_*.py` 立刻变「历史批」
      ⇒ 第 42 槽 C4 判滞留；`git mv` 到 `archive/scripts/batches/w10xx/`
      （不归位则本批提交后立刻红，且下一批开不了工）

## 5. 目录文档（顺序不能反）
- [ ] **先 `git add -A`**
- [ ] 再 `python scripts/gen_folder_docs.py --refresh`（生成器按 Git 索引收集，顺序反了必漏新件）
- [ ] 再 `git add -A`（把生成结果收进索引）

## 6. 计数、统计与文档连锁
- [ ] **若本批新增/修改了 `docs/**.md`**（顺序不能反，W1022/W1023 连踩两次）：
      `python scripts/_gen_search_index.py` → `python scripts/generate_csp.py`
      ——前者不做第 46 槽报条目数不符；后者不做第 20 槽报 CSP 漂移（索引里含内联脚本，哈希会变）
- [ ] 新增测试会改 `pytest_collected`：实测 `pytest --collect-only -q` 末行，
      同步 `pytest.ini` 与 `docs/11-方案报告/…/系统架构方案v2…md` 两处 `<!--stats:pytest_collected-->`
- [ ] `python scripts/stats.py --w W####` 刷新，再 `--check` 求 24 键零差异

## 7. 全量门禁（约 13 分钟·务必后台跑）
- [ ] `python scripts/verify_delivery.py`（前台 15 分钟会超时被杀，且杀掉不留完整日志）
- [ ] 只接受「核心全部通过 ✅」；任何 FAIL 按 `gate-triage-template.md` 五步法定位

## 8. 提交（两笔）
- [ ] 第一笔 `feat(w####): …`——pre-commit 会再跑一遍全量，绿灯才算真的绿
- [ ] 台账回填 commit 号与状态 → 第二笔 `docs(w####): 台账回填…`

## 9. 收官后
- [ ] 坑表：本次是否踩了**新形态**的坑？**改完必须实算分项**——`grep -c '^- \*\*'` 按主题逐段数，别手算（W1024 实证：六主题 26/6/26/19/11/34 之和是 122，我手算成 121 并写进 AGENTS/HANDOVER，而 AGENTS 的分项行当时还停在 25/25/15/10/28=109 的旧值上、长期无人核）⇒ 同步四处：`docs/agent/pitfalls.md` 各段标题 + AGENTS 总数 + AGENTS 分项行 + HANDOVER 两处就地并入对应主题（禁追加尾部段落），同步四处计数
- [ ] 若本次产生了「应回写模板」的新检查项 → 回写 `docs/agent/*-template.md` 并更新其校准戳
- [ ] 工作区记忆：追加当日日志（只写有跨会话价值的东西，不记临时路径与搜索过程）

---

**最常见的三个失败**：① `changelog_body` 漏前导空行 → 标题粘连，只能段内定向订正（级联不可重跑）；
② 目录文档 refresh 早于 `git add` → 漏新件，第 45 槽红；③ `git mv` 只把新路径写进 spec → 第 51 槽判「代提他方件」。
