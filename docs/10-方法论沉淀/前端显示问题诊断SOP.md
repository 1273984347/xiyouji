# 前端显示问题诊断 SOP（先取证，再假设）

> 轨标：方法论沉淀
> 更新时间：2026-08-16（W457 复盘沉淀）
> 适用：站点页面「显示异常 / 白屏 / 空白 / 样式丢失」类问题的诊断与修复。

---

## 一、铁律：先取证，再假设

**禁止**在拿到直接证据前自行假设根因（W456–W457 曾因「先假设后取证」两轮偏航：误判 CDN 阻断 → 误判浏览器缓存 → 靠用户截图才锁定真因）。

诊断第一步必须向用户（或从环境）索取三项证据，缺一不可：

1. **截图**（整页，能看清背景色、导航、字体、图表区）
2. **DevTools Console 输出**（F12 → Console，红色报错全文；若有 Network 失败也一并截）
3. **复现条件**（访问方式：file:// 双击 / http 本地服务 / 线上 URL；浏览器与版本；是否有扩展）

---

## 二、白屏/显示异常三类症状识别

| 症状 | 关键判据 | 常见根因 | 对应门禁 |
|---|---|---|---|
| **A. 图表区白、文字正常** | 文字有样式、导航正常，仅 SVG/canvas 区域空 | 图表 JS 未执行（脚本语法错误、CDN/库加载失败、数据 fetch 失败且无回退） | `check_js_syntax.js`、`_smoke_batch.js` |
| **B. 整页 CSS 裸奔** | 背景纯白、链接蓝色默认、字体 Times、无卡片/间距（文字本身正常） | 内联 CSS 结构破坏（url 缺括号致 bad-url 吞块）、CSP 拦 style | `check_structure.py`、`_p1_viz_audit.js` style-broken |
| **C. 无报错但内容空白** | 无 pageerror、`window.__data` 未设置、dataSource 停留初始文案 | **CSP 哈希失配**——改内联脚本后未重跑 generate_csp，整脚本被拒执行 | `verify_delivery.py` CSP 漂移检查 |

**识别技巧**：判断是否「整页 CSS 裸奔」（B 类），在 Console 执行：
```js
getComputedStyle(document.body).backgroundColor  // 若为 rgba(0,0,0,0) 即样式未生效
document.querySelector('style').sheet.cssRules.length  // 若 ≤1 即内联 CSS 整块被吞
```

---

## 三、标准排查路径

1. **取证**（见第一节三项证据）。
2. **分类**（见第二节症状表，对照截图 + Console 报错）。
3. **静态门禁先跑**（秒级、无需浏览器）：
   ```bash
   python scripts/check_structure.py      # CSS 结构平衡（B 类）
   node scripts/check_js_syntax.js        # 内联脚本语法（A/C 类）
   python scripts/generate_csp.py --check # CSP 哈希漂移（C 类）
   ```
4. **运行时复现**（有浏览器时）：`node scripts/_diag_style_assert.js` 全量断言样式生效 + pageerror；`_smoke_batch.js` 单页冒烟。
5. **定位到文件/行**：语法错误用 `node -e` 的 vm.Script 编译拿行号；CSS 断点用 `python scripts/_find_css_breaks.py <file>`。
6. **修复 + 复验**：修复后重跑对应门禁 + 浏览器复测渲染，留痕截图。

---

## 四、门禁对照表（哪类问题已被机器拦截）

| 门禁 | 挂载点 | 拦截的错误类别 |
|---|---|---|
| `check_structure.py` | verify_delivery（pre-commit） | CSS 括号/引号/url 结构破坏（W457 B 类） |
| `check_js_syntax.js` | verify_delivery（pre-commit） | 内联脚本 SyntaxError（W457 EN 腐蚀 A 类） |
| `generate_csp.py --check` | verify_delivery（pre-commit） | CSP 哈希失配（C 类） |
| `check_corruption.py` | verify_delivery（pre-commit） | 双引号翻倍腐蚀、d3 插件漏引 |
| `_diag_style_assert.js` / `_p1_viz_audit.js` / `_smoke_batch.js` | 运行时（CI/手动） | 样式裸奔、零渲染、零尺寸 canvas、横向溢出 |

---

## 五、修复后的留痕要求（沿用项目铁律）

改完页面**必须留痕审查证据再汇报**，严禁「改完直接报完成」：
- 静态语法检查 + 运行时冒烟（Playwright）+ 性能/渲染 before-after（重改必有基准）。
- 门禁复跑全绿 + 修复前后截图对比。
