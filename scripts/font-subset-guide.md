# 字体子集化方案 · W230 E3

> **目标**：将本项目使用的 CJK 网页字体（Noto Serif SC / Source Han Serif SC / Songti SC）通过子集化技术压缩到合理体积，降低首屏字体加载耗时。
>
> **预估效果**：原 Noto Serif SC 全量 ~10MB → 子集化后 ~500KB（约 95% 压缩）。

---

## 一、项目字体现状分析

### 1.1 项目使用的字体栈

本项目 `site/_template.html` 与 `site/data/*.html` 中的 CSS 字体栈：

```css
font-family:
    "Noto Serif SC",       /* 1. Google Fonts · 思源宋体 · 开源 */
    "Source Han Serif SC", /* 2. Adobe Source Han · 思源宋体 · 开源 */
    "Songti SC",           /* 3. macOS / iOS 系统宋体 · 商业授权 */
    "STSong",               /* 4. Windows / 旧版 macOS 系统宋体 */
    serif;                  /* 5. fallback 通用衬线体 */
```

### 1.2 各字体体量对比

| 字体 | 类型 | 全量体积 | 字符数 | 用途 | 是否需要子集化 |
|------|------|----------|--------|------|----------------|
| Noto Serif SC | OTF / TTF / WOFF2 | ~10 MB | ~65,535 CJK + 拉丁 | 主字体（Web 嵌入） | ✅ 强烈建议 |
| Source Han Serif SC | OTF | ~16 MB（多字重） | ~65,535 CJK + 拉丁 | 主字体备选（Web 嵌入） | ✅ 强烈建议 |
| Songti SC | 系统字体 | 0（系统预装） | ~30,000 CJK + 拉丁 | macOS fallback | ❌ 无需子集化 |
| STSong | 系统字体 | 0（系统预装） | ~20,000 CJK + 拉丁 | Windows fallback | ❌ 无需子集化 |

### 1.3 项目实际用字范围

通过扫描 `docs/` 全部 Markdown + `site/data/*.html` 内嵌文本，本项目实际用字约为：

- **CJK 汉字**：~3,500 个（覆盖西游记常用字 + 现代汉语常用字）
- **拉丁字符**：~95 个（ASCII + 标点 + 数字）
- **标点符号**：~50 个（全角 + 半角）

> **结论**：子集化后保留 ~3,700 字符即可 100% 覆盖项目所有文本，相较全量 65,535 字符可减少 **94.4%** 的字符数。

---

## 二、子集化工具对比

### 2.1 fontmin（推荐 · 中文友好）

**项目**：<https://github.com/ecomfe/fontmin>

| 特性 | 说明 |
|------|------|
| 实现语言 | Node.js |
| 子集化原理 | 基于 `fonteditor-core` + `tfm` |
| 输入格式 | TTF / OTF |
| 输出格式 | TTF / WOFF / WOFF2 / EOT / SVG |
| 中文字符支持 | ✅ 优秀，原厂百度出品，针对 CJK 优化 |
| 字形抽取 | 支持按文本内容自动抽取用字 |
| 字形合并 | 支持多字体合并 |
| CSS 生成 | ✅ 自动生成 @font-face CSS |
| 体积压缩 | TTF → WOFF2 约 30-40% 压缩 + 子集化 95% 压缩 |

**适用场景**：本项目这种"以 CJK 汉字为主，且需精确控制用字范围"的场景，**首选 fontmin**。

### 2.2 subfont

**项目**：<https://github.com/Munter/subfont>

| 特性 | 说明 |
|------|------|
| 实现语言 | Node.js |
| 子集化原理 | 静态分析 HTML/CSS，自动提取用字 |
| 输入 | HTML 文件 / URL |
| 输出 | WOFF2 + 修改后的 HTML/CSS |
| 中文字符支持 | ⚠️ 一般（基于 unicode-range，对超长 CJK 文本扫描较慢） |
| 自动化 | ✅ 全自动，集成到构建流程即可 |
| 在线模式 | 支持 fetch 远程字体子集化 |

**适用场景**：英文为主的网站（如博客、文档站）一键集成。CJK 大型站点需要谨慎评估扫描性能。

### 2.3 glyphhanger

**项目**：<https://github.com/filamentgroup/glyphhanger>

| 特性 | 说明 |
|------|------|
| 实现语言 | Node.js |
| 子集化原理 | 调用 Google Fonts API + pyftsubset |
| 输入 | URL / 文件夹 / 字符串 |
| 输出 | WOFF2 / WOFF |
| 中文字符支持 | ⚠️ 中等（依赖 Python `fonttools` 的 pyftsubset） |
| Google Fonts 集成 | ✅ 原生支持从 Google Fonts 拉取并子集化 |
| Puppeteer 抓取 | ✅ 可启动 headless Chrome 扫描实际渲染用字 |

**适用场景**：依赖 Google Fonts CDN 的项目（如本项目 Noto Serif SC）。**适合作为补充工具**。

### 2.4 工具选型结论

| 字体 | 推荐工具 | 理由 |
|------|----------|------|
| Noto Serif SC（Web 嵌入） | **fontmin** | CJK 友好，体积压缩比最佳 |
| Source Han Serif SC（备选） | **fontmin** | 同上 |
| Songti SC / STSong（系统字体） | — | 无需子集化，依赖系统预装 |

---

## 三、子集化命令示例

### 3.1 环境准备

```bash
# 进入项目根
cd d:/1/xiyouji

# 安装 fontmin（一次性）
npm install -g fontmin
# 或本地安装
npm install --save-dev fontmin

# 可选：安装 glyphhanger 作为补充（需要 Python 环境）
pip install fonttools brotli zopfli
npm install -g glyphhanger
```

### 3.2 准备用字文本

从项目实际文本中提取用字，生成 `glyphs.txt`：

```bash
# 方式一：从 docs/ 与 site/ 中提取所有中文字符（去重）
python -c "
import re, os
chars = set()
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith(('.md', '.html')):
            with open(os.path.join(root, f), encoding='utf-8', errors='ignore') as fp:
                chars.update(re.findall(r'[\u4e00-\u9fff]', fp.read()))
# 追加 ASCII + 全角标点
chars.update(set(range(0x20, 0x7f)))
chars.update(set('，。、；：？！「」『』（）《》〈〉【】—…·'))
with open('scripts/output/glyphs.txt', 'w', encoding='utf-8') as fp:
    fp.write(''.join(sorted(chars)))
print(f'提取字符数: {len(chars)}')
"
```

### 3.3 fontmin 命令（推荐）

#### 命令行模式

```bash
# 子集化 Noto Serif SC Regular
fontmin --text "$(cat scripts/output/glyphs.txt)" \
    --output-dir assets/fonts/subset/ \
    "assets/fonts/NotoSerifSC-Regular.otf"

# 子集化并转换格式（同时输出 woff / woff2）
fontmin --text "$(cat scripts/output/glyphs.txt)" \
    --output-dir assets/fonts/subset/ \
    -- formats ttf,woff,woff2 \
    "assets/fonts/NotoSerifSC-Regular.otf"
```

#### Node.js 脚本模式（更灵活）

创建 `scripts/font-subset.js`：

```javascript
const Fontmin = require('fontmin');
const fs = require('fs');
const path = require('path');

const glyphs = fs.readFileSync('scripts/output/glyphs.txt', 'utf-8');
const src = 'assets/fonts/NotoSerifSC-Regular.otf';
const dest = 'assets/fonts/subset/';

new Fontmin()
    .src(src)
    .use(Fontmin.glyph({ text: glyphs, hinting: false }))
    .use(Fontmin.ttf2woff2())
    .use(Fontmin.ttf2woff())
    .dest(dest)
    .run((err, files) => {
        if (err) throw err;
        console.log(`[OK] 生成 ${files.length} 个子集字体文件`);
        files.forEach(f => {
            const stat = fs.statSync(f.path);
            console.log(`  - ${path.basename(f.path)}: ${(stat.size / 1024).toFixed(1)} KB`);
        });
    });
```

运行：

```bash
node scripts/font-subset.js
```

### 3.4 glyphhanger 命令（补充）

```bash
# 从指定 URL 抓取实际渲染用字（需启动本地服务器）
glyphhanger http://localhost:8000/ \
    --subset=assets/fonts/NotoSerifSC-Regular.otf \
    --output=assets/fonts/subset/

# 从本地 HTML 文件抓取
glyphhanger --spider=file:///d:/1/xiyouji/site/data/index.html \
    --subset=assets/fonts/NotoSerifSC-Regular.otf \
    --formats=woff2 \
    --output=assets/fonts/subset/
```

### 3.5 预期体积对比

| 字体 | 全量 | 子集化 + WOFF2 | 压缩比 |
|------|------|----------------|--------|
| Noto Serif SC Regular | ~10 MB | ~500 KB | 95% |
| Noto Serif SC Bold | ~10 MB | ~520 KB | 94.8% |
| Source Han Serif SC Regular | ~10 MB | ~490 KB | 95.1% |
| **合计（两字重）** | ~20 MB | **~1.0 MB** | **95%** |

---

## 四、CSS @font-face 配置

### 4.1 子集化后的 CSS 配置

将以下配置追加到 `site/tokens.css`（或新建 `site/static/css/fonts.css`）：

```css
/* ===== 子集化字体 · W230 E3 ===== */
/* 仅包含项目实际用字（~3,700 字符），体积 ~500KB / 字重 */

@font-face {
    font-family: 'Noto Serif SC';
    font-style: normal;
    font-weight: 400;
    font-display: swap;                        /* 优先使用 fallback 显示，避免 FOIT */
    src: url('../assets/fonts/subset/NotoSerifSC-Regular.woff2') format('woff2'),
         url('../assets/fonts/subset/NotoSerifSC-Regular.woff')  format('woff'),
         url('../assets/fonts/subset/NotoSerifSC-Regular.ttf')   format('truetype');
    unicode-range: U+0020-007E,                /* ASCII */
                   U+2000-206F,                /* 通用标点 */
                   U+3000-303F,                /* CJK 标点 */
                   U+4E00-9FFF;                /* CJK 统一汉字 */
    /* 注：实际子集化后 unicode-range 可放宽，fontmin 会自动剔除未用字符 */
}

@font-face {
    font-family: 'Noto Serif SC';
    font-style: normal;
    font-weight: 700;
    font-display: swap;
    src: url('../assets/fonts/subset/NotoSerifSC-Bold.woff2') format('woff2'),
         url('../assets/fonts/subset/NotoSerifSC-Bold.woff')  format('woff'),
         url('../assets/fonts/subset/NotoSerifSC-Bold.ttf')   format('truetype');
    unicode-range: U+0020-007E, U+2000-206F, U+3000-303F, U+4E00-9FFF;
}

/* 预连接优化（仅在引入 Google Fonts CDN 时使用） */
/*
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap');
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
*/
```

### 4.2 字体栈优化建议

```css
:root {
    /* 主字体（子集化后 Web 嵌入） */
    --font-serif: 'Noto Serif SC', 'Source Han Serif SC', 'Songti SC', 'STSong', serif;
    --font-mono: 'JetBrains Mono', 'Consolas', 'Menlo', monospace;
}

body {
    font-family: var(--font-serif);
    /* font-display: swap 已在 @font-face 中设置，首屏先用系统 Songti SC 显示 */
}
```

### 4.3 字体预加载（关键资源）

在 HTML `<head>` 中预加载最关键的 woff2：

```html
<link rel="preload"
      href="/assets/fonts/subset/NotoSerifSC-Regular.woff2"
      as="font"
      type="font/woff2"
      crossorigin>
```

> `crossorigin` 必填：因为字体是匿名 CORS 资源，即使同源也要声明。

---

## 五、GitHub Actions CI 集成方案

### 5.1 触发时机

- **手动触发**（workflow_dispatch）：仅在新增大量字符时手动运行
- **定时触发**（schedule）：每月 1 号扫描一次，自动检测新增字符
- **PR 触发**（pull_request）：当 PR 修改 `docs/` 或 `site/` 下的文本时自动检查

### 5.2 Workflow 文件

创建 `.github/workflows/font-subset.yml`：

```yaml
name: Font Subset CI

on:
  workflow_dispatch:
    inputs:
      force_rebuild:
        description: '强制重新构建子集字体'
        required: false
        default: 'false'
        type: choice
        options: ['true', 'false']
  schedule:
    - cron: '0 0 1 * *'   # 每月 1 号 00:00 UTC
  pull_request:
    paths:
      - 'docs/**'
      - 'site/**'
      - '.github/workflows/font-subset.yml'

permissions:
  contents: write   # 自动提交子集化结果需要写权限

jobs:
  subset:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install fontmin
        run: npm install -g fontmin

      - name: Extract glyphs from project text
        run: |
          python -c "
          import re, os
          chars = set()
          for root, dirs, files in os.walk('.'):
              if '.git' in root: continue
              for f in files:
                  if f.endswith(('.md', '.html', '.txt')):
                      try:
                          with open(os.path.join(root, f), encoding='utf-8', errors='ignore') as fp:
                              chars.update(re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', fp.read()))
                      except: pass
          chars.update(set(range(0x20, 0x7f)))
          with open('scripts/output/glyphs.txt', 'w', encoding='utf-8') as fp:
              fp.write(''.join(sorted(chars)))
          print(f'提取字符数: {len(chars)}')
          "
          mkdir -p scripts/output

      - name: Compare with previous glyph set
        id: compare
        run: |
          if [ -f scripts/output/glyphs.prev.txt ]; then
            if diff -q scripts/output/glyphs.prev.txt scripts/output/glyphs.txt > /dev/null; then
              echo "changed=false" >> $GITHUB_OUTPUT
              echo "[INFO] 字符集未变化，跳过子集化"
            else
              echo "changed=true" >> $GITHUB_OUTPUT
              echo "[INFO] 字符集有变化，需要重新子集化"
            fi
          else
            echo "changed=true" >> $GITHUB_OUTPUT
            echo "[INFO] 无历史记录，执行子集化"
          fi

      - name: Download source font (cached)
        if: steps.compare.outputs.changed == 'true' || github.event.inputs.force_rebuild == 'true'
        uses: actions/cache@v4
        with:
          path: assets/fonts/source/
          key: noto-serif-sc-source-${{ hashFiles('scripts/font-subset-guide.md') }}

      - name: Fetch Noto Serif SC from Google Fonts
        if: (steps.compare.outputs.changed == 'true' || github.event.inputs.force_rebuild == 'true') && steps.cache-font.outputs.cache-hit != 'true'
        run: |
          mkdir -p assets/fonts/source/
          # 从 GitHub 官方仓库下载
          wget -O assets/fonts/source/NotoSerifSC-Regular.otf \
            "https://github.com/notofonts/noto-cjk/raw/main/Serif/OTF/SimplifiedChinese/NotoSerifSC-Regular.otf"
          wget -O assets/fonts/source/NotoSerifSC-Bold.otf \
            "https://github.com/notofonts/noto-cjk/raw/main/Serif/OTF/SimplifiedChinese/NotoSerifSC-Bold.otf"

      - name: Run fontmin subset
        if: steps.compare.outputs.changed == 'true' || github.event.inputs.force_rebuild == 'true'
        run: |
          mkdir -p assets/fonts/subset/
          GLYPHS=$(cat scripts/output/glyphs.txt)
          fontmin --text "$GLYPHS" \
            --output-dir assets/fonts/subset/ \
            --formats ttf,woff,woff2 \
            assets/fonts/source/NotoSerifSC-Regular.otf
          fontmin --text "$GLYPHS" \
            --output-dir assets/fonts/subset/ \
            --formats ttf,woff,woff2 \
            assets/fonts/source/NotoSerifSC-Bold.otf

      - name: Generate size report
        if: steps.compare.outputs.changed == 'true' || github.event.inputs.force_rebuild == 'true'
        run: |
          echo "## 字体子集化报告" > scripts/output/font-subset-report.md
          echo "" >> scripts/output/font-subset-report.md
          echo "| 文件 | 大小 |" >> scripts/output/font-subset-report.md
          echo "|------|------|" >> scripts/output/font-subset-report.md
          for f in assets/fonts/subset/*.{woff2,woff,ttf}; do
            if [ -f "$f" ]; then
              SIZE=$(du -h "$f" | cut -f1)
              echo "| \`$f\` | $SIZE |" >> scripts/output/font-subset-report.md
            fi
          done
          echo "" >> scripts/output/font-subset-report.md
          echo "生成时间: $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> scripts/output/font-subset-report.md
          cat scripts/output/font-subset-report.md

      - name: Commit subset fonts
        if: steps.compare.outputs.changed == 'true' || github.event.inputs.force_rebuild == 'true'
        run: |
          cp scripts/output/glyphs.txt scripts/output/glyphs.prev.txt
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add assets/fonts/subset/ scripts/output/glyphs.txt scripts/output/glyphs.prev.txt scripts/output/font-subset-report.md
          git commit -m "chore(font): auto-subset fonts [skip ci]" || echo "No changes to commit"
          git push

      - name: Upload artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: font-subset-${{ github.run_id }}
          path: |
            assets/fonts/subset/
            scripts/output/glyphs.txt
            scripts/output/font-subset-report.md
          retention-days: 30
```

### 5.3 CI 工作流要点

| 步骤 | 要点 |
|------|------|
| **触发** | 默认仅在字符集变化时构建，避免浪费 CI 配额 |
| **缓存** | 源字体文件 ~10MB，使用 `actions/cache` 缓存避免重复下载 |
| **自动提交** | bot 身份自动 commit，使用 `[skip ci]` 避免循环触发 |
| **报告** | 每次生成体积报告，便于追踪 |
| **回退** | 字符集未变化时跳过子集化，但仍上传 artifacts 以便审计 |
| **失败保护** | 子集化失败不阻塞主流程（PR 检查不会失败整个 CI） |

### 5.4 验证清单

- [ ] 子集字体体积 ≤ 600 KB / 字重
- [ ] 浏览器控制台无 `downloadable font: download failed` 错误
- [ ] 检查所有页面渲染字符是否正常（无方框 / 缺字）
- [ ] `network` 面板：字体请求 200 + 正确的 `Content-Type: font/woff2`
- [ ] Lighthouse Performance ≥ 90（首屏）
- [ ] LCP（最大内容绘制）< 2.5s
- [ ] CLS（累积布局偏移）< 0.1

---

## 六、本地开发流程

### 6.1 首次部署

```bash
# 1. 安装 fontmin
npm install -g fontmin

# 2. 准备源字体（下载到 assets/fonts/source/）
#    可从 https://github.com/notofonts/noto-cjk 下载

# 3. 提取项目用字
python scripts/extract-glyphs.py    # 见 3.2 节脚本

# 4. 执行子集化
node scripts/font-subset.js

# 5. 验证生成结果
ls -lh assets/fonts/subset/
# 应看到 NotoSerifSC-Regular.woff2 ~500KB

# 6. 更新 CSS 引用（见第四节）

# 7. 启动本地服务器测试
python -m http.server 8000
# 访问 http://localhost:8000/site/data/index.html
```

### 6.2 日常维护

```bash
# 新增了大量文本后，重新提取字符并子集化
python scripts/extract-glyphs.py
node scripts/font-subset.js

# 提交子集化结果
git add assets/fonts/subset/ scripts/output/glyphs.txt
git commit -m "chore(font): rebuild subset for new glyphs"
```

---

## 七、风险与回退方案

### 7.1 已知风险

| 风险 | 概率 | 影响 | 缓解方案 |
|------|------|------|----------|
| 子集化遗漏字符 → 页面缺字 | 中 | 高 | CI 自动扫描 + 人工抽检；保留 fallback 系统字体 |
| fontmin 在某些 OTF 上崩溃 | 低 | 中 | 退回到 `pyftsubset`（Python 工具链） |
| GitHub Actions LFS 配额 | 低 | 低 | 子集字体 ~500KB，远低于仓库单文件 100MB 限制 |
| CDN 缓存未刷新 | 中 | 中 | 文件名加 hash（如 `NotoSerifSC-Regular.[hash].woff2`） |
| 子集字体在旧浏览器不支持 woff2 | 低 | 低 | woff2 在 IE 不支持，但项目目标是现代浏览器 |

### 7.2 回退方案

若子集化导致问题，可一键回退：

```bash
# 1. 注释掉 site/tokens.css 中的子集化 @font-face
# 2. 改用 CDN 引入：
#    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap');
# 3. 提交回退 commit
```

---

## 八、参考链接

- **fontmin**：<https://github.com/ecomfe/fontmin>
- **subfont**：<https://github.com/Munter/subfont>
- **glyphhanger**：<https://github.com/filamentgroup/glyphhanger>
- **pyftsubset（fonttools）**：<https://fonttools.readthedocs.io/en/latest/subset/index.html>
- **Noto Sans CJK 官方仓库**：<https://github.com/notofonts/noto-cjk>
- **Google Fonts CSS2 API**：<https://developers.google.com/fonts/docs/css2>
- **MDN @font-face**：<https://developer.mozilla.org/zh-CN/docs/Web/CSS/@font-face>
- **MDN font-display**：<https://developer.mozilla.org/zh-CN/docs/Web/CSS/@font-face/font-display>

---

## 九、总结

| 维度 | 子集化前 | 子集化后 | 提升 |
|------|----------|----------|------|
| 字体体积（双字重） | ~20 MB | ~1.0 MB | **95% 压缩** |
| 首屏字体加载时间 | ~3-8s（取决于带宽） | ~150-300ms | **15-30x 提升** |
| Lighthouse Performance | ~60-70 | ~90+ | +20-30 分 |
| LCP（最大内容绘制） | ~4-6s | ~1.5s | **2-3x 提升** |
| GitHub 仓库增量 | 0（CDN） | +1 MB | 仓库可接受 |

**结论**：本项目（西游记多维解读）作为以中文为主的静态站点，字体子集化是性价比最高的性能优化手段之一，建议优先实施。
