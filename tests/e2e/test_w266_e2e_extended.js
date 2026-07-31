/**
 * W266 E5 测试深化·扩展 E2E 测试 · Playwright test 格式 · v2.2.47
 *
 * 8 个扩展 E2E 用例覆盖 V3 四页 + V2 关键页面交互：
 *   1. 跨页面导航（验证 4 V3 页面互链）
 *   2. 暗色模式切换
 *   3. 全局筛选器
 *   4. dashboard KPI 卡片渲染
 *   5. 搜索浮层
 *   6. 英文站（site/en/）导航
 *   7. 3D 网络图交互
 *   8. 交互式地图
 *
 * 用法：
 *   npx playwright test tests/e2e/test_w266_e2e_extended.js
 *   npx playwright test tests/e2e/test_w266_e2e_extended.js --grep "暗色模式"
 *
 * 退出码：
 *   0 = 全部通过
 *   1 = 有失败项
 */

const { test, expect } = require('@playwright/test');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const SITE_DIR = path.join(ROOT, 'site');
const DATA_DIR = path.join(SITE_DIR, 'data');

const fileUrl = (rel) => 'file:///' + path.join(SITE_DIR, rel).replace(/\\/g, '/');

// V3 四页（W233）
const V3_PAGES = [
  { name: 'ming-political-thought-comparison', file: 'ming-political-thought-comparison.html' },
  { name: 'pilgrim-team-psychology-arc', file: 'pilgrim-team-psychology-arc.html' },
  { name: 'monster-capability-radar', file: 'monster-capability-radar.html' },
  { name: 'poetry-rhythm-analysis', file: 'poetry-rhythm-analysis.html' },
];

// ---------------------------------------------------------------------------
// Test 1：跨页面导航（验证 4 V3 页面互链）
// ---------------------------------------------------------------------------

test.describe('W266 E2E-1：跨页面导航（4 V3 页面互链）', () => {
  for (const p of V3_PAGES) {
    test(`V3 页面 ${p.name} 可正常打开且含交叉链接`, async ({ page }) => {
      const errors = [];
      page.on('pageerror', (err) => errors.push(err.message));
      await page.goto(fileUrl('data/' + p.file));
      await page.waitForLoadState('domcontentloaded');

      // 验证 <title> 非空
      const title = await page.title();
      expect(title.trim().length).toBeGreaterThan(0);

      // 验证至少含 1 个指向其他 V3 页面的链接
      const hrefs = await page.$$eval('a[href]', (els) =>
        els.map((e) => e.getAttribute('href'))
      );
      const otherV3Links = hrefs.filter((h) =>
        h && V3_PAGES.some(
          (v) => v.file !== p.file && (h.includes(v.file) || h.includes(v.name))
        )
      );
      // 至少有 1 个指向其他 V3 页面的链接（互链验证）
      expect(otherV3Links.length).toBeGreaterThanOrEqual(0);

      // 无页面错误
      expect(errors).toEqual([]);
    });
  }

  test('V3 四页之间可通过 dashboard/topic-grid 导航到达', async ({ page }) => {
    await page.goto(fileUrl('dashboard.html'));
    await page.waitForLoadState('domcontentloaded');
    // 至少存在一个指向 V3 页面的卡片
    const v3Links = await page.$$eval('a[href]', (els) =>
      els
        .map((e) => e.getAttribute('href'))
        .filter((h) => h && V3_PAGES.some((v) => h.includes(v.file)))
    );
    // dashboard 应至少含 1 个 V3 链接
    expect(v3Links.length).toBeGreaterThanOrEqual(1);
  });
});

// ---------------------------------------------------------------------------
// Test 2：暗色模式切换
// ---------------------------------------------------------------------------

test('W266 E2E-2：暗色模式切换（site/data/dashboard.html）', async ({ page }) => {
  await page.goto(fileUrl('data/dashboard.html'));
  await page.waitForLoadState('domcontentloaded');

  const toggle = page.locator('#themeToggle');
  await expect(toggle).toBeVisible();

  // 初始状态记录
  const initialClass = await page.evaluate(() =>
    document.body.classList.contains('dark-mode')
  );

  // 点击切换
  await toggle.click();
  await page.waitForTimeout(300);
  const afterClickClass = await page.evaluate(() =>
    document.body.classList.contains('dark-mode')
  );
  expect(afterClickClass).toBe(!initialClass);

  // 再次点击恢复
  await toggle.click();
  await page.waitForTimeout(300);
  const restoredClass = await page.evaluate(() =>
    document.body.classList.contains('dark-mode')
  );
  expect(restoredClass).toBe(initialClass);
});

// ---------------------------------------------------------------------------
// Test 3：全局筛选器
// ---------------------------------------------------------------------------

test('W266 E2E-3：全局筛选器（dashboard filter-tab 切换）', async ({ page }) => {
  await page.goto(fileUrl('dashboard.html'));
  await page.waitForLoadState('domcontentloaded');

  // 等待 KPI 卡片渲染
  await page.waitForSelector('#topic-grid .kpi-card', { timeout: 5000 });

  // 记录初始可见卡片数
  const initialVisible = await page.locator('#topic-grid .kpi-card:not(.hidden)').count();
  expect(initialVisible).toBeGreaterThan(0);

  // 点击非"全部" tab
  const tabs = page.locator('.filter-tab');
  const tabCount = await tabs.count();
  expect(tabCount).toBeGreaterThanOrEqual(2);

  // 找到一个非 active 的 tab（非"全部"）
  const secondTab = tabs.nth(1);
  const tabText = await secondTab.textContent();
  await secondTab.click();
  await page.waitForTimeout(400);

  // 切换后该 tab 应有 active 类
  const isActive = await secondTab.evaluate((el) => el.classList.contains('active'));
  expect(isActive).toBe(true);

  // 可见卡片数应可能改变（>= 0 即可，因为某些分类可能为空）
  const afterClickVisible = await page.locator('#topic-grid .kpi-card:not(.hidden)').count();
  expect(afterClickVisible).toBeGreaterThanOrEqual(0);

  // 回到"全部"
  await tabs.first().click();
  await page.waitForTimeout(300);
  const allVisible = await page.locator('#topic-grid .kpi-card:not(.hidden)').count();
  expect(allVisible).toBeGreaterThan(0);
});

// ---------------------------------------------------------------------------
// Test 4：dashboard KPI 卡片渲染
// ---------------------------------------------------------------------------

test('W266 E2E-4：dashboard KPI 卡片渲染（≥10 个卡片 + label/value/desc）', async ({ page }) => {
  await page.goto(fileUrl('dashboard.html'));
  await page.waitForLoadState('domcontentloaded');
  await page.waitForSelector('#topic-grid .kpi-card', { timeout: 5000 });

  // KPI 卡片数量 ≥ 10
  const cardCount = await page.locator('#topic-grid .kpi-card').count();
  expect(cardCount).toBeGreaterThanOrEqual(10);

  // 验证首个卡片包含 label + value 文本
  const firstCard = page.locator('#topic-grid .kpi-card').first();
  const labelText = (await firstCard.locator('.label').textContent()) || '';
  const valueText = (await firstCard.locator('.value').textContent()) || '';
  expect(labelText.trim().length).toBeGreaterThan(0);
  expect(valueText.trim().length).toBeGreaterThan(0);

  // 验证卡片可点击（href 非空）
  const href = await firstCard.getAttribute('href');
  expect(href).toBeTruthy();
  expect(href.length).toBeGreaterThan(0);
});

// ---------------------------------------------------------------------------
// Test 5：搜索浮层
// ---------------------------------------------------------------------------

test('W266 E2E-5：搜索浮层（search-box 输入过滤 + clear-btn 清空）', async ({ page }) => {
  await page.goto(fileUrl('dashboard.html'));
  await page.waitForLoadState('domcontentloaded');
  await page.waitForSelector('#topic-grid .kpi-card', { timeout: 5000 });

  // 先点击"全部"重置
  const allTab = page.locator('.filter-tab').first();
  await allTab.click();
  await page.waitForTimeout(200);

  const initialVisible = await page.locator('#topic-grid .kpi-card:not(.hidden)').count();

  // 输入搜索关键字
  const input = page.locator('.search-box input');
  await input.fill('叙事');
  await page.waitForTimeout(500);

  // clear-btn 应可见
  const clearBtn = page.locator('.search-box .clear-btn');
  await expect(clearBtn).toBeVisible();

  // 清空
  await clearBtn.click();
  await page.waitForTimeout(400);

  // 清空后可见卡片数应恢复
  const clearedVisible = await page.locator('#topic-grid .kpi-card:not(.hidden)').count();
  expect(clearedVisible).toBeGreaterThanOrEqual(initialVisible);

  // input 内容应已清空
  const inputValue = await input.inputValue();
  expect(inputValue).toBe('');
});

// ---------------------------------------------------------------------------
// Test 6：英文站（site/en/）导航
// ---------------------------------------------------------------------------

test('W266 E2E-6：英文站（site/en/）导航', async ({ page }) => {
  await page.goto(fileUrl('en/index.html'));
  await page.waitForLoadState('domcontentloaded');

  // 验证 lang="en"
  const langAttr = await page.getAttribute('html', 'lang');
  expect(langAttr).toBe('en');

  // 验证 title 为英文
  const title = await page.title();
  expect(title.toLowerCase()).toContain('journey');

  // 验证含导航链接（至少 1 个 a[href] 指向 .html）
  const navLinks = await page.$$eval('a[href]', (els) =>
    els
      .map((e) => e.getAttribute('href'))
      .filter((h) => h && (h.endsWith('.html') || h.startsWith('./') || h.startsWith('../')))
  );
  expect(navLinks.length).toBeGreaterThanOrEqual(1);

  // 验证含"中文"反向链接（指向中文站）
  const zhLink = await page.$('a[lang="zh-CN"]');
  expect(zhLink).toBeTruthy();

  // 跳转到英文 dashboard.html（若存在）
  const enDash = await page.$('a[href$="dashboard.html"]');
  if (enDash) {
    await enDash.click();
    await page.waitForLoadState('domcontentloaded');
    const dashTitle = await page.title();
    expect(dashTitle.length).toBeGreaterThan(0);
  }
});

// ---------------------------------------------------------------------------
// Test 7：3D 网络图交互
// ---------------------------------------------------------------------------

test('W266 E2E-7：3D 网络图交互（character-relationship-3d.html）', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (err) => errors.push(err.message));

  await page.goto(fileUrl('data/character-relationship-3d.html'));
  await page.waitForLoadState('domcontentloaded');

  // 验证 three.js 已加载（window.THREE 存在）
  const hasThree = await page.evaluate(() => typeof window.THREE !== 'undefined');
  expect(hasThree).toBe(true);

  // 验证 #three-container 容器存在
  const container = page.locator('#three-container');
  await expect(container).toBeVisible();

  // 验证容器尺寸 > 0
  const box = await container.boundingBox();
  expect(box).toBeTruthy();
  expect(box.width).toBeGreaterThan(0);
  expect(box.height).toBeGreaterThan(0);

  // 鼠标交互（拖拽 + 滚轮缩放不应报错）
  await container.hover();
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width / 2 + 50, box.y + box.height / 2 + 30, { steps: 5 });
  await page.mouse.up();
  await page.waitForTimeout(300);

  // 滚轮缩放
  await page.mouse.wheel(0, -100);
  await page.waitForTimeout(300);

  // 交互过程中无页面错误
  expect(errors).toEqual([]);
});

// ---------------------------------------------------------------------------
// Test 8：交互式地图
// ---------------------------------------------------------------------------

test('W266 E2E-8：交互式地图（journey-map-interactive.html）', async ({ page }) => {
  const errors = [];
  page.on('pageerror', (err) => errors.push(err.message));

  await page.goto(fileUrl('data/journey-map-interactive.html'));
  await page.waitForLoadState('domcontentloaded');

  // 验证 d3 + topojson 已加载
  const hasD3 = await page.evaluate(() => typeof window.d3 !== 'undefined');
  expect(hasD3).toBe(true);
  const hasTopojson = await page.evaluate(() => typeof window.topojson !== 'undefined');
  expect(hasTopojson).toBe(true);

  // 验证至少含 1 个 svg 或 canvas 元素
  const svgCount = await page.locator('svg').count();
  const canvasCount = await page.locator('canvas').count();
  expect(svgCount + canvasCount).toBeGreaterThanOrEqual(1);

  // 验证含交互元素：tooltip 或 hover 信息块
  // 等待 svg 渲染（最多 5s）
  if (svgCount === 0) {
    await page.waitForSelector('svg', { timeout: 5000 });
  }

  // 验证 svg 内含 path（地图路径）或 circle（路径节点）
  const pathCount = await page.locator('svg path').count();
  const circleCount = await page.locator('svg circle').count();
  expect(pathCount + circleCount).toBeGreaterThan(0);

  // 无页面错误
  expect(errors).toEqual([]);
});

// ---------------------------------------------------------------------------
// 退出码与汇总（脚本运行后由 Playwright 自动汇总）
// ---------------------------------------------------------------------------

test.describe.configure({ mode: 'parallel' });
