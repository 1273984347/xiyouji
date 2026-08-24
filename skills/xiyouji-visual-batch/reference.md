# xiyouji-visual-batch 参考模板与速查

供执行 Phase E 视觉批次时按需取用：§1 探针报告结构、§2 预算核对表、§3 shot_check 脚本骨架、§4 M-A1 前后对比验收脚本（W488 范式）、§5 页面分型与根页清单、§6 落地数字基准（W476–W488 实测）。

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

## 4. M-A1 前后对比验收脚本骨架（W488 范式）

可感知升级批（视觉重设计/暗色）验收用，强制每页差异像素率 ≥1% + 目视清单 ≥3 处。范式：`git worktree add` 建 before + Playwright 三套截图 + PIL 差异率。

```bash
# before 工作区（旧基线 commit，不污染当前工作区）
cd /d/1/xiyouji && git worktree add C:/tmp/w4xx-before <旧基线commit>
# 验收后清理
cd /d/1/xiyouji && git worktree remove C:/tmp/w4xx-before
```

```js
/* M-A1：before/after/dark 三套 fullPage 截图（一次性脚本） */
const { chromium } = require('playwright');
const path = require('path');
const BEFORE = 'C:/tmp/w4xx-before/site';                 // before 工作区
const AFTER  = path.resolve(__dirname, '..', 'site');     // 当前工作区
const PAGES = ['index', 'dashboard', 'curated', 'guide', 'dukou-engine', 'mobile-index'];

async function shot(root, name, outDir, theme) {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  if (theme) await ctx.addInitScript(() => { try { localStorage.setItem('xy-theme', theme); } catch (_) {} });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e).slice(0, 120)));
  await page.goto('file:///' + path.join(root, name + '.html').replace(/\\/g, '/'),
    { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2200);                        // 等 reveal-in 动画；fullPage 滚动触发全部 IO
  await page.screenshot({ path: path.join(outDir, name + '.png'), fullPage: true });
  await browser.close();
  return errors;                                          // dark 套同时检查 FOUC / pageerror
}

(async () => {
  for (const n of PAGES) {
    await shot(BEFORE, n, 'before', null);
    await shot(AFTER,  n, 'after',  null);
    await shot(AFTER,  n, 'dark',   'dark');
  }
})();
```

PIL 差异像素率（同尺寸逐像素；任一通道差 > 12 算差异像素，W488 实测口径）：

```python
from PIL import Image, ImageChops
import sys
a = Image.open(sys.argv[1]).convert('RGB')
b = Image.open(sys.argv[2]).convert('RGB')
assert a.size == b.size, f'size mismatch: {a.size} vs {b.size}'  # 高度不同先对齐画布
diff = ImageChops.difference(a, b).convert('L')
rate = sum(1 for p in diff.getdata() if p > 12) / (a.size[0] * a.size[1])
print(f'diff rate = {rate*100:.2f}%', 'PASS' if rate >= 0.01 else 'FAIL: <1% 需补静态强化')
```

对比图（左右拼接 + diff 率标注）与目视清单落 `plans/`（每页 ≥3 处可辨差异，如 hero 大数字朱砂/表头淡朱砂/KPI 数字朱砂/导航指示条/夜读按钮/route-strip 朱砂线）。hover/dark 在浅色静态截图不可见是首轮不达标主因，先确认静态差异面积够再截。

## 5. 页面分型与根页清单

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

## 6. 落地数字基准（W476–W488 实测，供后续批次参照）

- W476（E0）：tokens.css v2 5715B → v3 7463B（+1748B，预算内）；DESIGN.md 新增 §4A 纸感轻立体体系；225 页重新同步；五门禁全绿。commit：`feat(w476): Phase E0 纸感轻立体宪改 + tokens v3 — 视觉高级感升级轨启动`。
- W477（E1）：system.css v2（21.4KB，预算内）；Noto Sans SC 两档子集化（`_w477_sans_subset.py` 复用 w334 管线，省 ~1.4MB）；根页模板化；全站传播。commit：`feat(w477): Phase E1 组件层 v2 + 根页模板化 — system.css v2 全站传播`。
- W488（根页可感知批）：6 用户可见根页视觉重设计 + 夜读模式第一批（暗色页内实现，见 SKILL.md 第 2c 步）。M-A1 前后对比差异像素率 index 2.35% / dashboard 5.05% / curated 2.84% / guide 5.88% / dukou-engine 25.98% / mobile-index 7.07%（6/6 ≥1%）；修正过程：首轮 3 页不达标（dashboard 0.63%/guide 0.28%/dukou-engine 0.13%，hover/dark 静态不可见）→ 补标题+KPI 朱砂/表头淡朱砂/route-strip 朱砂线等静态强化 → 达标；system.css +644B、tokens 未增；html 每页 +3.2~6.6KB；暗色冒烟 6 页 pageerror=0 + FOUC=0 + 禁 JS 回退浅色。commit：`feat(w488): 根页视觉重设计+夜读模式 — Phase E 方向 A 第一批（可感知升级 + M-A1 前后对比验收）`。
- 子集化管线：`scripts/archive/w334_font_subset.py`（扫 docs+site 实际用字 → pyftsubset → 覆写 site/static/fonts/ 同名文件，@font-face 不动）。

## 7. 与相邻技能的分工

- `xiyouji-plan-authoring`：写路线图/单批方案（本技能的输入）。
- `xiyouji-plan-review`：评估方案（执行前可选）。
- `xiyouji-version-bump`：本技能第 8 步转交对象（六文档同步 + bump + commit/push），收尾细节以该技能为准。
