/**
 * _render_arch_png.mjs — 架构图 HTML → PNG 导出（W925·一次性施工脚本）
 *
 * 目的：把《系统架构方案v2-架构图-2026-10-25.html》的六张图渲染为 PNG，
 *      供 PPT / 文档 / 对外分享使用（用户 2026-10-25 交付要求三形态：HTML + Mermaid + PNG）。
 *
 * 关键纪律（承接 W821 铁律 2「产物不得反向成为事实源」）：
 *   ① PNG 由 HTML 实测渲染产出（Playwright + Chromium），**非手工绘制** ⇒ 图与页一致；
 *   ② 图意事实源是方案正文 Mermaid 代码块——若 PNG 与正文不符，改正文，不改本脚本；
 *   ③ 本脚本只做「渲染 + 落盘」，不修改 HTML 任何内容。
 *
 * 用法：
 *   node scripts/_render_arch_png.mjs
 *   node scripts/_render_arch_png.mjs --check     # 只校验产物存在且非空，不重渲染
 *
 * 产物：docs/11-方案报告/设计与架构方案/系统架构方案v2-架构图/*.png（6 张）
 *
 * 依赖：playwright（已装于 scripts/node_modules）+ chromium（已装于 %LOCALAPPDATA%\ms-playwright）
 * 本机环境注记：PowerShell 侧 `python` 是应用执行存根；Node 侧 `node` 可直呼。
 */
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const HTML_REL = path.join('docs', '11-方案报告', '设计与架构方案', '系统架构方案v2-架构图-2026-10-25.html');
const HTML_ABS = path.join(ROOT, HTML_REL);
const OUT_DIR = path.join(ROOT, path.dirname(HTML_REL), '系统架构方案v2-架构图');

// 图号 → 文件名（与 HTML 中 <span class="fig-no"> 的显示文本一一对应，注意原文含空格「图 1」）
const FIGS = [
  { no: '图 1', name: '01-整体分层图' },
  { no: '图 4', name: '04-模块依赖图' },
  { no: '图 2', name: '02-数据流图' },
  { no: '图 5', name: '05-存储演进路线图' },
  { no: '图 6', name: '06-故障域降级拓扑图' },
  { no: '图 3', name: '03-私有化部署拓扑图' },
];

function parseArgs() {
  const args = process.argv.slice(2);
  return { check: args.includes('--check') };
}

/** --check 模式：校验六张 PNG 均存在且非空（不做渲染） */
function checkOnly() {
  let ok = true;
  for (const f of FIGS) {
    const p = path.join(OUT_DIR, `${f.name}.png`);
    if (!fs.existsSync(p)) {
      console.error(`  FAIL 缺失：${f.name}.png`);
      ok = false;
      continue;
    }
    const size = fs.statSync(p).size;
    if (size < 1024) {
      console.error(`  FAIL 过小（${size} B）：${f.name}.png`);
      ok = false;
      continue;
    }
    console.log(`  PASS ${f.name}.png（${(size / 1024).toFixed(1)} KB）`);
  }
  console.log(ok ? 'CHECK_OK（6/6 产物存在且非空）' : 'CHECK_FAIL');
  return ok ? 0 : 1;
}

async function main() {
  const { check } = parseArgs();
  if (check) return checkOnly();

  if (!fs.existsSync(HTML_ABS)) {
    console.error(`  FAIL 源 HTML 不存在：${HTML_ABS}`);
    return 1;
  }
  fs.mkdirSync(OUT_DIR, { recursive: true });

  let browser;
  try {
    browser = await chromium.launch({ headless: true });
  } catch (err) {
    console.error('  FAIL 无法启动 Chromium。执行：npx playwright install chromium');
    console.error(`  原因：${err && err.message ? err.message : String(err)}`);
    return 1;
  }

  let fails = 0;
  try {
    const context = await browser.newContext({
      viewport: { width: 1600, height: 1200 },
      deviceScaleFactor: 2, // 2× 像素密度 ⇒ PNG 清晰度足够放大查看
    });
    const page = await context.newPage();
    // file:// 直开（与站点 file:// 铁律同源——本页零外域，故 file:// 下样式完整生效）
    await page.goto(pathToFileURL(HTML_ABS).href, { waitUntil: 'load' });
    await page.waitForTimeout(300);

    // 零外域自检：页面不得发起任何 http(s) 请求（用户硬约束「禁外域依赖」）
    const external = [];
    page.on('request', (req) => {
      const u = req.url();
      if (/^https?:/i.test(u)) external.push(u);
    });
    await page.reload({ waitUntil: 'load' });
    await page.waitForTimeout(300);
    if (external.length) {
      console.error(`  FAIL 检测到 ${external.length} 个外域请求：${external.slice(0, 5).join(' | ')}`);
      fails += 1;
    } else {
      console.log('  PASS 零外域请求（file:// 加载期间无 http/https 请求）');
    }

    for (const f of FIGS) {
      // 精确定位：figure 内 .fig-no 元素文本严格等于该图号（避免「图 1」误配到「图 10」）
      const fig = page.locator('figure').filter({
        has: page.locator('.fig-no').filter({ hasText: new RegExp(`^${f.no.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`) }),
      }).first();
      const count = await fig.count();
      if (!count) {
        console.error(`  FAIL 未找到图件：${f.no}`);
        fails += 1;
        continue;
      }
      const out = path.join(OUT_DIR, `${f.name}.png`);
      try {
        await fig.screenshot({ path: out });
        const size = fs.statSync(out).size;
        if (size < 1024) {
          console.error(`  FAIL ${f.no} 产物过小（${size} B）`);
          fails += 1;
        } else {
          console.log(`  PASS ${f.no} → ${f.name}.png（${(size / 1024).toFixed(1)} KB）`);
        }
      } catch (err) {
        console.error(`  FAIL ${f.no} 渲染异常：${err && err.message ? err.message : String(err)}`);
        fails += 1;
      }
    }
    await context.close();
  } finally {
    await browser.close();
  }

  console.log(fails === 0 ? 'RENDER_OK（6/6 导出成功·零外域）' : `RENDER_FAIL（${fails} 项失败）`);
  return fails === 0 ? 0 : 1;
}

main().then((code) => process.exit(code)).catch((err) => {
  console.error(`  FAIL 未捕获异常：${err && err.stack ? err.stack : String(err)}`);
  process.exit(1);
});
