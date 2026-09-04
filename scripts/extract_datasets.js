/**
 * extract_datasets.js — 从 site/data/*.html 提取 EMBEDDED_DATA 为 dataset/*.json
 * 
 * 用法：node scripts/extract_datasets.js
 * 输出：dataset/ 目录（每页一个 JSON）+ dataset/README.md 索引
 */
const fs = require('fs');
const path = require('path');

const SITE_DATA = path.join(path.dirname(__dirname), 'site', 'data');
const OUT_DIR = path.join(path.dirname(__dirname), 'dataset');

// 确保输出目录存在
if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

const files = fs.readdirSync(SITE_DATA).filter(f => f.endsWith('.html') && f !== '_shell.html');
const index = [];
let extracted = 0, skipped = 0;

for (const file of files) {
  const html = fs.readFileSync(path.join(SITE_DATA, file), 'utf-8');
  
  // 查找 EMBEDDED_DATA 定义
  const patterns = [
    /const\s+EMBEDDED_DATA\s*=\s*(\{[\s\S]*?\});\s*\n/,
    /EMBEDDED_DATA\s*=\s*(\{[\s\S]*?\});\s*\n/,
    /const\s+EMBEDDED_FALLBACK\s*=\s*(\{[\s\S]*?\});\s*\n/,
  ];
  
  let dataStr = null;
  for (const pat of patterns) {
    const m = html.match(pat);
    if (m) { dataStr = m[1]; break; }
  }
  
  if (!dataStr) {
    skipped++;
    continue;
  }
  
  // JSON 解析数据字面量（尾逗号自动修复；不再动态执行代码）
  let data;
  try {
    data = JSON.parse(dataStr);
  } catch (e) {
    // 尝试修复常见问题：尾逗号
    try {
      const fixed = dataStr.replace(/,\s*([}\]])/g, '$1');
      data = JSON.parse(fixed);
    } catch (e2) {
      console.log(`  PARSE_ERROR: ${file} — ${e2.message.slice(0, 60)}`);
      skipped++;
      continue;
    }
  }
  
  if (!data || typeof data !== 'object' || Object.keys(data).length === 0) {
    skipped++;
    continue;
  }
  
  const outName = file.replace('.html', '.json');
  if (!/^[A-Za-z0-9._-]+\.json$/.test(outName)) { skipped++; continue; }
  const outPath = path.join(OUT_DIR, outName);
  if (!path.resolve(outPath).startsWith(OUT_DIR + path.sep)) { skipped++; continue; }
  fs.writeFileSync(outPath, JSON.stringify(data, null, 2), 'utf-8');
  
  const keys = Object.keys(data);
  const sizeKB = (Buffer.byteLength(JSON.stringify(data)) / 1024).toFixed(1);
  index.push({ file: outName, keys: keys.length, sizeKB, topKeys: keys.slice(0, 5) });
  extracted++;
  console.log(`  OK: ${outName} (${keys.length} keys, ${sizeKB} KB)`);
}

// 生成 README.md
const readme = `# dataset/ — 详解西游记结构化数据

> 从 site/data/*.html 的 EMBEDDED_DATA 中提取的结构化数据集。
> 提取时间：${new Date().toISOString().slice(0, 10)}
> 提取脚本：scripts/extract_datasets.js

## 概览

- 提取页面：${extracted} / ${files.length}
- 跳过页面：${skipped}（无 EMBEDDED_DATA 或解析失败）
- 格式：JSON（UTF-8，2 空格缩进）

## 数据索引

| 文件 | 数据键数 | 大小 | 主要键 |
|------|---------|------|--------|
${index.map(r => `| ${r.file} | ${r.keys} | ${r.sizeKB} KB | ${r.topKeys.join(', ')} |`).join('\n')}

## 使用方式

\`\`\`python
import json
with open('dataset/81-hardships.json', encoding='utf-8') as f:
    data = json.load(f)
print(data['hardships'])  # 八十一难完整数据
\`\`\`

\`\`\`javascript
const data = await fetch('dataset/philosophy.json').then(r => r.json());
\`\`\`

## 许可

MIT License · 数据来源于《西游记》原著（公共版权）+ 项目原创分析标注。
`;

fs.writeFileSync(path.join(OUT_DIR, 'README.md'), readme, 'utf-8');
console.log(`\n完成：${extracted} 个数据集提取至 dataset/，README.md 已生成。`);
