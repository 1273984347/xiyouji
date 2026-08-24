# xiyouji-day-review 参考手册

SKILL.md 的辅助参考：完整命令库 + 2026-08-22 首跑案例库。执行审查时按需查阅，不要求通读。

## 1. 命令速查表

shell 为 git-bash（`cd D:/1/xiyouji` 风格，**不要用 `cd /d`**）。

### 1.1 取证

```bash
# 当日提交清单（改日期取当日）
git log --since "2026-08-22 00:00" --oneline
git log --since "2026-08-22 00:00" --oneline | wc -l          # 提交数
git log -1 --oneline                                          # 当前 HEAD 末提交

# 工作区状态 + 未跟踪文件
git status --porcelain
git ls-files --others --exclude-standard                       # 只看未跟踪文件

# 单提交体量（大删除量红旗检查）
git show --stat <commit>
git show --shortstat <commit>

# 宣称入库脚本核实
git ls-files scripts/baseline_snapshot.py                      # 有输出=已入库；空=从未提交

# 遗留 worktree
git worktree list
```

### 1.2 门禁

```bash
python scripts/verify_delivery.py       # 交付门禁（15 条）；退出码 0 仅代表门禁过
python scripts/acceptance_snapshot.py   # 验收数字当批现测（M 指标/内联字节/断点）
python scripts/generate_csp.py --check  # CSP 0 漂移
```

### 1.3 渲染抽查（Playwright）

用项目现有 `scripts/_shot_check.js` 或等价 Playwright 脚本，关键断言：

```js
// styled 断言：样式必须真实生效，防"白底+蓝链接+裸文本"的失样式回归
const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
const font = await page.evaluate(() => getComputedStyle(document.body).fontFamily);
// 断点实测：390 / 414（iPhone 常见宽度，常不在门禁回归视口内）
await page.setViewportSize({ width: 390, height: 844 });
// dark 模式：切暗色后截图，Read 目视确认
await page.screenshot({ path: 'dark-check.png' });
```

抽查页选择：当日改过的页面 + 每类至少 1 页（根页 / site/data / site/en / 3D 页）。

### 1.4 声称 vs 实测（INLINED 空块扫 / wc -c 二分 / 线上比对）

```bash
# INLINED 空块正则扫：找"存在但为空"的样式块（W493 清空事故的探测手段）
# 正常块 ≥20KB（verify_delivery 门禁 15 check_inlined_css.py 阈值）；输出低于阈值的可疑页
for f in site/data/*.html site/en/*.html; do
  b=$(python -c "import re;t=open(r'$f',encoding='utf-8').read();m=re.search(r'INLINED[^\n]*\n(.*?)\n\s*</style>',t,re.S);print(len(m.group(1)) if m else -1)")
  [ "$b" -ge 0 ] && [ "$b" -lt 20000 ] && echo "$f $b"
done

# wc -c 二分定位丢失提交：某文件体积骤降 = 内容被清空的现场
git log --oneline -- <文件>            # 列该文件历史提交
git show <提交>:<文件> | wc -c         # 逐版本取字节数，找相邻骤降点
# W493 当次：75,689 → 44,437 字节（全站 INLINED 清空）

# curl 线上站比对（批次含部署时）：线上与本地字节数差大 = 部署未完成/被回滚
curl -s https://1273984347.github.io/xiyouji/site/data/<页>.html | wc -c
wc -c site/data/<页>.html
```

## 2. 首跑案例库（2026-08-22，W496 当日）

当日审查抓出以下问题，均已在 W496 修复。后续审查若遇同型问题，可对照识别。

### 案例 A（P0）：全站 224 页失样式，14 门禁全绿漏网

现象：dark 模式截图抽查发现 chapter-stats 页完全无样式（白底、蓝链接、裸文本）；进一步确认 `site/data/*.html` 与 `site/en/*.html` 全部 224 页的 INLINED CSS 块为空（约 28KB tokens+system 样式全部丢失），**全站失样式**。

根因：W493 的批量脚本清空了 INLINED 块（提交体量从 75,689 字节跌到 44,437 字节——**单提交删除 21 万行的红旗**）。而 14 条文本门禁全部通过——它们只查块存在/体积/哈希/CSP，**不查样式是否真的渲染**。

教训：文本门禁抓不到渲染回归。唯一能抓住的方式是 Playwright styled 断言 + 截图目视（SKILL.md 步骤 3）。事后固化为门禁 15（check_inlined_css.py：INLINED 块内容 ≥20KB），正是「审查发现问题 → 固化为门禁」的 P3 演进路径。

### 案例 B（P1）：baseline_snapshot 从未入库

现象：`git status` 发现 `scripts/baseline_snapshot.py` 与 `observation-baseline-snapshot.md` 未跟踪。项目约定**非 `_` 前缀的脚本/文档必须入库**（`_` 前缀才是一次性不入库）——两个文件都无 `_` 前缀却从未提交 = 「做了但从未入库」。

教训：审查时对每个未跟踪文件逐一判定归属；方案档/交接文档宣称「新建了 xx 脚本」时用 `git ls-files` 核实真入库（SKILL.md 步骤 4 第 4 条）。

### 案例 C（P1）：5 方案档缺回填

现象：`docs/superpowers/plans/` 下当日关联的方案档，遗留项/待办行未回填关闭，宣称「已落地」的条目实测缺证据。

教训：方案档的「落地状态回写」是 plan-authoring 流程的收尾环节，审查时必须逐档核对遗留行是否真关闭、宣称落地项是否真存在（SKILL.md 步骤 4 第 2 条）。

### 案例 D（P2）：断点口径核查

现象：声称「断点残留 0」但 grep 出 4 处匹配。查证后确认 4 处都是 `max-width` **属性声明**而非 `@media` 查询，不在白名单口径内，「残留 0」成立。随后实测 390/414px（不在 W494 回归 5 视口内）6 页无溢出，断点映射无实机回归。

教训：声称与 grep 冲突时先分辨口径再下结论（SKILL.md 陷阱 5）；门禁视口之外常用宽度要补实测（陷阱 6）。

## 3. 报告模板（问题清单）

```markdown
# 当日工作审查报告（YYYY-MM-DD）

审查基线：HEAD <hash>（<vX.Y.Z W###>）· 门禁退出码 <0/n>

## P0（数据丢失/功能失效/门禁假绿）
- [ ] <问题> — 证据：<命令/截图/文件> — 建议：<修复动作>

## P1（文档同步/未入库/声明不符）
- [ ] ...

## P2（卫生/口径）
- [ ] ...

## P3（可选优化）
- [ ] <如：把 XX 检查固化为门禁>

## 修复范围（AskUserQuestion 用户确认后填）
- [ ] 确认修复：<范围>
- [ ] 修复完成：verify_delivery 全绿 + 渲染抽查复验
```
