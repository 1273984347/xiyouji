# CSS 包含块退化与交互后态机检范式

> **定位（W1147 建）**：把「CSS 特性悄悄改变定位锚点」与「交互后态零门禁覆盖」两件事的方法固化。
> **谁该读**：要写 fixed/sticky 浮层（抽屉/tooltip/弹层）、要给 CSS 加 transform/backdrop-filter 类效果、或设计「交互后状态」的自动化检查的人。
> **一句话**：**`backdrop-filter`/`transform` 等特性会悄悄把祖先变成 fixed 后代的包含块；一条运行时判定（offsetParent）比一百条静态正则可靠；交互后态必须有自己的探针——干净加载测不出一切「点开之后」的世界。**

---

## 一、包含块退化：一条运行时判定压过全部静态正则

### 1.1 病理

按 CSS 规范，元素具有以下任一**非 none**特性时，即成为其 `position:fixed` / `absolute` 后代的**包含块**（后代不再相对视口定位）：

| 特性 | 常见来源 | 危险度 |
|:---|:---|:---|
| `backdrop-filter` / `filter` | 顶条毛玻璃、暗色补偿、图片滤镜 | **最高**——磨砂效果常给 sticky 顶条（恰是浮层的父级） |
| `transform` | hover 上浮、滑入动画、reveal-in | 高——`:hover` 瞬态也会在悬停期间退化 |
| `will-change: transform` 等 | 动画性能优化提示 | 高——常驻 |
| `perspective` / `contain: layout\|paint\|strict` | 3D 卡片、绘制隔离 | 中 |

**本项目实证**（745px 窄视口用户实报）：顶条磨砂（W335）+ 抽屉滑出（W492）两个各自正常的特性组合 → 抽屉面板被压进 144px 高的顶条、其余链接裸浮页外——**潜伏 600+ 批无人发现**。

### 1.2 机检范式（唯一推荐）

```js
// 枚举全部 fixed 元素，断言包含块未退化——一条判定覆盖全部祖先特性组合
for (const el of document.querySelectorAll('*')) {
    if (getComputedStyle(el).position === 'fixed') {
        const op = el.offsetParent;
        // 正常：null（视口锚定）；退化：某祖先元素（backdrop-filter/transform 等所致）
        assert(op === null || op === document.body);
    }
}
```

为什么**不推荐静态正则交叉分析**：扫描「含块特性规则 × fixed 规则」得到 100 × 23 的组合面，其中大量是
`:hover` 瞬态、误匹配（script 片段）、自身 transform（不影响自身定位）——噪声比信号高一个量级。
运行时判定由浏览器引擎自己回答「这个 fixed 元素此刻锚定在哪」，零误报。

固化探针：`scripts/fixed_ancestor_probe.py`（页面 × 视口参数化）· `scripts/containment_block_scan.py`（静态面辅助参考）。

### 1.3 修复选择序

发现退化后按序选：① **祖先特性移除或限定断点**（本项目实证：≤768 抽屉态关顶条磨砂——磨砂在窄视口的视觉增益本就不可感）；② 浮层 DOM 移出退化祖先（`document.body.appendChild`）；③ 浮层改 absolute + JS 定位（最后手段）。

---

## 二、交互后态：干净加载测不出的世界

### 2.1 盲区本体

全站既有验证（门禁/J2 视觉回归/截图审查/交互探针首版）全部是**干净加载**——没有任何一环检查「用户点开菜单之后」「关闭之后有没有残留」。抽屉塌陷正是纯交互态缺陷：页面初始加载一切正常，第一次点开汉堡菜单才崩。

### 2.2 清单驱动探针

`scripts/interaction_state_probe.py` + `scripts/interaction_components.py`（**12 类开合组件单一事实源**）：
每个组件执行「入口交互 → 开启态断言（fixed 退化 + 开启选择器在位）→ 关闭 → 残留断言（白名单外 `.open` 残留即 FAIL）」。
组件增删必须同步清单——探针是引擎，清单是案件表。

### 2.3 边界与诚实记录

部分组件的入口选择器与页面实际结构存在偏差（基线报告 `acted=false` 如实记录）——探针的两条主断言
（退化/残留）不依赖交互成功与否（页面全元素枚举），但「开启态在位」断言依赖交互成功——选择器校准是持续项。

---

## 三、断点缝隙：1440/375 之间的世界

截图审查双视口 1440/375 之间的 520-768（平板窄/小桌面窗）是形态断点密集区（≤768 抽屉、≤640 图例纵排、≤520 窄屏）。
**745 档已入运行时锁**（横向溢出断言 + 抽屉全高）——新增断点形态时同步扩探针视口集，而非等用户撞。

---

## 四、检查清单（动手前 30 秒）

- [ ] 给任何元素加 `backdrop-filter`/`transform`/`filter` 前：它有没有 fixed/absolute 后代？
- [ ] 新增 fixed/sticky 浮层后：跑 `fixed_ancestor_probe.py`（全视口）
- [ ] 新增开合交互后：`interaction_components.py` 清单加一行 + 跑 `interaction_state_probe.py`
- [ ] 新增形态断点后：探针视口集同步加该档 + 溢出断言
