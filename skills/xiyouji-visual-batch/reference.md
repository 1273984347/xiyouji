# xiyouji-visual-batch 参考模板与速查

供执行 Phase E 视觉批次时按需取用：§1 探针报告结构、§2 预算核对表、§3 shot_check 脚本骨架、§4 页面分型与根页清单、§5 落地数字基准（W476/W477 实测）。

## 1. 探针报告结构（E0 范式）

```markdown
# Phase E · E<n> 探针取证报告（W4xx）

> 执行：YYYY-MM-DD · 基线 git xxxxxxx（vX.Y.Z W4xx）· 脚本：`scripts/_e<n>_probe.py`（一次性诊断，不入门禁）
> 扫描面：233 页（site 根 9 含 _template + data 87 含 _shell + en 138，探针口径；_shell 不计入统计页）

## P1 · 页面内联 <style> 裸色计数
（裸 hex / rgb()/rgba() 总数、含裸色页数、最多页 Top5、口径判定：图表数据色豁免）

## P2 · transition 形态统计
（含 transition 页数、var(--dur-*) 令牌形态 / all / 裸秒值 三形态计数、秒值分布、契约违规判定）
注意：`.15s` 会被正则截成 `15s` 误报，命中可疑值先人工复核。

## P3 · 根页结构一致性
（真实根页清单、hero/topnav/site-footer 有无矩阵、模板化对象、豁免页）

## P4 · 字体静态盘点
（woff2 清单与体积、子集化状态、font-display、CLS 风险）

## P5 · tokens/system 体积与增量预算
（tokens.css / system.css 现值、预算判定：增量 ≤ +2KB / +6KB）

## P6 · 公共组件选择器页面内联重复面
（选择器 × 内联定义页数表、最大膨胀源判定）

## E<n> 落地数字（本批产出后回填）
- tokens.css：v旧 XXXXXB → v新 XXXXXB（±XXXXB，预算内/外）
- 其他产出与本批实测增量
```

## 2. 预算核对表

| 文件 | W476 前基线 | 预算上限 | W477 后实测 | 判定 |
|:--|:--|:--|:--|:--|
| tokens.css | 5715B | ≤ +2KB（≤ ~7.7KB） | 7463B（+1748B） | ✅ 预算内 |
| system.css | 18904B | ≤ +6KB（≤ ~24.9KB） | 21359B（+2455B） | ✅ 预算内 |
| 单页内联合计 | 24619B | ≤ 33KB | ~29109B | ✅ 预算内 |

复核命令：`cd /d/1/xiyouji && wc -c site/tokens.css site/system.css`。超预算处理顺序：先砍微交互工具类，不砍色彩令牌。

## 3. shot_check.js 脚本骨架

范式：`scripts/_w477_shot_check.js`（一次性脚本，不入门禁/CI）。核心结构：

```js
/* W4xx E<n> 视觉抽查（一次性脚本，不入门禁/CI） */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(__dirname, 'output', 'screenshots', 'w4xx-e<n>');
fs.mkdirSync(OUT, { recursive: true });

const PAGES = [
  ['index', 'site/index.html'],                 // 根页抽样
  ['dashboard', 'site/dashboard.html'],
  ['chapter-stats', 'site/data/chapter-stats.html'],  // 批内可视化页抽样
  // ... 批次内页面 ≥ 6 页
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const results = [];
  for (const [name, rel] of PAGES) {
    const errors = [];
    page.removeAllListeners('pageerror');
    page.on('pageerror', e => errors.push(String(e).slice(0, 120)));
    const url = 'file:///' + path.join(ROOT, rel).replace(/\\/g, '/');
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(1200);
    await page.screenshot({ path: path.join(OUT, name + '.png'), fullPage: false });
    // getComputedStyle 断言：新令牌真实生效（不能只看源码）
    const probe = await page.evaluate(() => {
      const el = document.querySelector('.card, .kpi, .chart-block, .curated-card, .path-card');
      if (!el) return null;
      const cs = getComputedStyle(el);
      return { radius: cs.borderRadius, shadow: cs.boxShadow.slice(0, 60) };
    }).catch(() => null);
    results.push({ name, pageerror: errors.length, errors: errors.slice(0, 2), probe });
  }
  await browser.close();
  const fail = results.filter(r => r.pageerror > 0);
  console.log(JSON.stringify(results, null, 2));
  console.log(fail.length ? 'FAIL: pageerror 非零' : 'OK: pageerror=0');
  process.exit(fail.length ? 1 : 0);
})();
```

验证三件套缺一不可：pageerror=0 → getComputedStyle 断言 → **截图用 Read 工具逐张目视**（阴影过重/圆角崩坏/布局错位只能靠看）。

## 4. 页面分型与根页清单

### 根页（E1 实测修正口径）

真实根页 = **8 页 + `_template.html`**；用户可见 6 页（模板化对象）+ 2 诊断页豁免：

| 页 | hero | topnav | site-footer | 定位 |
|:--|:--|:--|:--|:--|
| index / curated / guide | - | Y | Y | 主入口三页（深色首屏带） |
| dashboard | - | Y | -（自有 footer） | 导航中枢 |
| dukou-engine | - | - | -（长链页脚） | Agent 引擎页，结构全独立 |
| mobile-index | Y | - | - | 移动端入口 |
| rum-viewer / visit-viewer | ±- | - | - | 本地诊断页（**豁免**） |

### E2/E3 传播分型（按方案，批启动时用探针导出精确清单）

- **E2 传播 I**：网络/力导向页（约 16 页）+ 热力/统计页（约 20 页）。
- **E3 传播 II**：3D/Canvas 页（3-4 页，深度令牌仅用于 UI 层不动场景）+ 时间线/地图页 + 其余静态/表格页（约 46 页）。
- 3D 页专项：场景渲染 0 回归；UI 浮层（图例/按钮/tooltip）应用 elev-3。

### 传播范围

- `inline_css.py --force` 只处理含 `../tokens.css` 链接的页面（data 87 + en 138 ≈ 225 页）；**根页无需传播**（同目录 `<link href="tokens.css">` 自动跟随）。

## 5. 落地数字基准（W476/W477 实测，供后续批次参照）

- W476（E0）：tokens.css v2 5715B → v3 7463B（+1748B，预算内）；DESIGN.md 新增 §4A 纸感轻立体体系；225 页重新同步；五门禁全绿。commit：`feat(w476): Phase E0 纸感轻立体宪改 + tokens v3 — 视觉高级感升级轨启动`。
- W477（E1）：system.css v2（21.4KB，预算内）；Noto Sans SC 两档子集化（`_w477_sans_subset.py` 复用 w334 管线，省 ~1.4MB）；根页模板化；全站传播。commit：`feat(w477): Phase E1 组件层 v2 + 根页模板化 — system.css v2 全站传播`。
- 子集化管线：`scripts/archive/w334_font_subset.py`（扫 docs+site 实际用字 → pyftsubset → 覆写 site/static/fonts/ 同名文件，@font-face 不动）。

## 6. 与相邻技能的分工

- `xiyouji-plan-authoring`：写路线图/单批方案（本技能的输入）。
- `xiyouji-plan-review`：评估方案（执行前可选）。
- `xiyouji-version-bump`：本技能第 8 步转交对象（六文档同步 + bump + commit/push），收尾细节以该技能为准。
