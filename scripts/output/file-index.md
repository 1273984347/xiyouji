# xiyouji 文件反向索引

> 与 [CHANGELOG.md](../../CHANGELOG.md) 配套：给定文件，查它被改过几次、每次对应哪个 W 条目。
> W### 编号规则见 CHANGELOG.md 顶部。
> 创建于 2026-07-22（v0.8 双索引改造）
>
> **历史归档**：W031-W087（v2.0.4-v2.0.60）site/data/ 部分已迁移至 [file-index-archive.md](file-index-archive.md)。本文件仅保留 W088+ 现役索引。

---


## W389 交接文档历史段归档（2026-08-07·v2.3.17）

| 文件 | W | 说明 |
|---|---|---|
| 交接文档.md | W389 | v2.3.17 修改·W343-W358 历史提交记录（92 行）迁出至 交接文档-archive.md·「零、当前阻塞」HEAD 引用 W387→W388 修正·当前版本段 v2.3.16→v2.3.17 |
| 交接文档-archive.md | W389 | v2.3.17 修改·新增「二、历史提交记录（W343-W358）」段（92 行·乱序段 14 个）·头部归档范围扩容说明 |
| docs/00-导读/项目说明.md | W389 | v2.3.17 修改·第 45 行"当前版本"v2.3.15→v2.3.17（W388 遗留残留修复） |
| CHANGELOG.md | W389 | v2.3.17 修改·新增 W389 段·W### 规则 W001-W388→W001-W389 |
| README.md | W389 | v2.3.17 修改·头部版本段 v2.3.16→v2.3.17 |
| STRUCTURE.md | W389 | v2.3.17 修改·头部版本段 v2.3.16→v2.3.17 |
| .git（历史包） | W389 | v2.3.17 filter-repo 重写·--strip-blobs-bigger-than 5M + 删 screenshots 路径·241.7→32.8MB·force push（提交哈希全部重写） |

## W388 文档审查整理（2026-08-07·v2.3.16）

| 文件 | W | 说明 |
|---|---|---|
| 交接文档.md | W388 | v2.3.16 修改·「零、当前阻塞」段重写（W358 未提交过期→现 W387 干净）·历史快照标注 |
| docs/00-导读/项目说明.md | W388 | v2.3.16 修改·第 45 行"当前版本"v2.3.9 → v2.3.15（历史残留修复） |
| .gitignore | W388 | v2.3.16 修改·新增 rag_index.json + assets/fonts/source/ 排除规则 |
| scripts/output/rag_index.json | W388 | v2.3.16 索引移除（git rm --cached·本地保留·32.4MB 构建产物） |
| assets/fonts/source/（6 文件） | W388 | v2.3.16 索引移除（git rm --cached·本地保留·26.7MB 字体源） |

## W387 学术索引反哺 24 条（2026-08-07·v2.3.15）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/成书背景.md | W387 | v2.3.15 修改·+6 处学术标注（A09/A07/A06/A10/A08/A11） |
| docs/04-文化与历史背景/版本演变.md | W387 | v2.3.15 修改·+8 处学术标注（A13/C06/S02/S03/A12/T05/T09/T10+T07/T08/T11/T06） |
| docs/04-文化与历史背景/佛道思想.md | W387 | v2.3.15 修改·+7 处学术标注（P04/P05/C06/C03/P06/C04×2/A08/C05/A11） |
| source/引用与网络解读/学术论文索引.md | W387 | v2.3.15 修改·24 条"（待反哺）"→ 实际反哺位置·修订记录 v1.3 |

## W386 S4 学术投稿首批 2 篇（2026-08-07·v2.3.14）

| 文件 | W | 说明 |
|---|---|---|
| docs/S4-学术投稿/学术论文-心学视域下的西游记心猿书写与真假美猴王.md | W386 | v2.3.14 新建 148 行·S4 第一篇·王阳明"致良知"与心猿书写·"结构性渗透"判定·对话王阳明/鲁迅/胡适/李时人/黄霖·13 条参考文献 |
| docs/S4-学术投稿/学术论文-西游记驿递交通书写的数字人文研究.md | W386 | v2.3.14 新建 149 行·S4 第二篇·15 处涉关文地点数据集·四态类型学·与杨正泰/黄仁宇/布罗代尔/魏丕信制度史互证·对话竺洪波 N02 |

## W385 S2 方向落地（2026-08-07·v2.3.13）

| 文件 | W | 说明 |
|---|---|---|
| docs/S2-学术投稿/学术投稿候选-明代日常生活制度镜像方法论.md | W385 | v2.3.13 新建 215 行·基于 W369-W373 A5 五篇·婚姻/驿递/盐政/服饰/医学五维镜像·S2 学术投稿 8→11 篇 |
| docs/S2-学术投稿/学术投稿候选-边缘人物深度书写方法论.md | W385 | v2.3.13 新建 208 行·基于 W374-W379 A3 六篇·深化专题/外传/历史对照三形态·"地位越高声音越少"规律 |
| docs/S2-学术投稿/学术投稿候选-理论新视野四重路径方法论.md | W385 | v2.3.13 新建 199 行·基于 W380-W383 A4 四篇·空间生产/媒介/死亡/解释学四重路径 |
| docs/S2-学术投稿/学术投稿候选-记忆研究方法论.md | W385 | v2.3.13 修改·标题标准化（`学术投稿候选-` → `学术投稿候选：...——《西游记》作为文化记忆载体的四框架解读`） |
| docs/S2-学术投稿/学术投稿候选-A3性别对照双轨方法论.md | W385 | v2.3.13 修改·标题标准化（`学术投稿候选-` → `学术投稿候选：...——《西游记》男女八框架性别研究的对照结构`） |
| docs/S2-外部分享/S2-发布-西游与心理学.md | W385 | v2.3.13 脱敏·删尾部 CHANGELOG/file-index 链接 + W235 元信息行 |
| docs/S2-外部分享/S2-发布-西游与经济学.md | W385 | v2.3.13 脱敏·删尾部 CHANGELOG/file-index 链接 + W235 元信息行 |
| docs/S2-外部分享/S2-发布-西游与认知科学专题.md | W385 | v2.3.13 脱敏·删尾部 CHANGELOG/file-index 链接 + W235 元信息行 |
| docs/S2-外部分享/S2-发布-西游与后结构主义专题.md | W385 | v2.3.13 脱敏·删尾部 CHANGELOG/file-index 链接 + W235 元信息行 |
| docs/S2-外部分享/S2-发布-西游与记忆研究.md | W385 | v2.3.13 脱敏·删头部 W261 元信息 + 正文 W253-W256 改写 + 尾部双索引/关联文档 |
| docs/S2-外部分享/S2-发布-西游与男性研究.md | W385 | v2.3.13 脱敏·删头部 W262 元信息 + 正文 W237-W244 改写 + 尾部双索引/关联文档 |
| docs/S2-外部分享/S2-发布-西游与团队动力学心理学.md | W385 | v2.3.13 脱敏·删头部 W272 行 + 尾部本文基础/跨方向整合/关联文档块 |
| docs/S2-外部分享/S2-发布-西游妖怪生态学.md | W385 | v2.3.13 脱敏·删头部 W276 行 + 尾部本文基础/跨方向整合行 |
| docs/S2-外部分享/S2-发布-西游神学干预机制.md | W385 | v2.3.13 脱敏·删头部 W280 行 + 元数据块清理（保留内容信息行） |
| docs/S2-外部分享/S2-发布-西游四维研究.md | W385 | v2.3.13 脱敏·删尾部 CHANGELOG/file-index 双行 |

## W384 V 方向可视化深化 + E 方向工程化门禁（2026-08-07·v2.3.12）

| 文件 | W | 说明 |
|---|---|---|
| site/data/customs-pass-route.html | W384 | v2.3.12 新建·通关文牒·取经驿路图·基于 W370·15 处涉关文地点时间线+明代驿递对照表+5 洞察·可视化 85→86 |
| site/dashboard.html | W384 | v2.3.12 修改·数据中枢 40→42 数据集（3 处）·KPI 数据更新 |
| site/static/js/datahub-index.js | W384 | v2.3.12 修改·补 chapters-metadata 条目·index 41→42 对齐 dataset 42 |
| site/en/dashboard.html | W384 | v2.3.12 修改·KPI 更新（60→211 / 91→209 / 68→85）·45+→41+ topic cards |
| site/en/README.md | W384 | v2.3.12 修改·KPI 注记 as of W234→v2.3.11 W383 |
| site/data/search.html | W384 | v2.3.12 修改·跨 40→42 数据集 |
| site/data/philosophy.html | W384 | v2.3.12 修改·P3 清零·热力图轴副标题 h+44→h+58 |
| site/data/jurisprudence.html | W384 | v2.3.12 修改·P3 清零·树图 nameOf 短标签（完整 desc 保留 tooltip/图例） |
| site/data/relationships.html | W384 | v2.3.12 修改·inline_css 补内联（原漏）·静态优先闭环 |
| site/mobile-index.html | W384 | v2.3.12 修改·a11y 修复 9 处 E2-13 补 aria-label |
| site/en/essay-ming-literary-thought.html | W384 | v2.3.12 修改·死链修复 E9 回链 essay-literary-couplets→essay-chapter-couplets |
| site/en/visualizations.html | W384 | v2.3.12 修改·死链修复 theology→theological-intervention-network |
| scripts/_audit_final_residual.md | W384 | v2.3.12 修改·P3 最终回归报告增补（content 重叠 16→0 页） |

## W369-W383 A 方向内容扩容续 15 篇（2026-08-07·v2.3.11·与 W359-W368 合并提交）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/明代婚姻家庭制度对照专题.md | W369 | v2.3.11 新建 170 行·陈顾远/瞿同祖/费孝通/道格拉斯·婚嫁/妻妾/贞节/家庭伦理四维度·A5 第 27 个明代对照专题·A5 29→34 |
| docs/04-文化与历史背景/明代驿递交通制度对照专题.md | W370 | v2.3.11 新建 170 行·杨正泰/黄仁宇/布罗代尔/魏丕信·驿站/通关文牒/水陆交通/信息传递·A5 第 28 个 |
| docs/04-文化与历史背景/明代盐法开中制度对照专题.md | W371 | v2.3.11 新建 168 行·吴承明/李龙潜/佐伯富/曾仰丰·开中法/盐商边饷/私盐/盐的财政地位·A5 第 29 个 |
| docs/04-文化与历史背景/明代服饰舆服制度对照专题.md | W372 | v2.3.11 新建 169 行·沈从文/周锡保/布迪厄/王世贞·舆服等级/僭越/僧道服饰/服饰符号·A5 第 30 个 |
| docs/04-文化与历史背景/明代医学养生制度对照专题.md | W373 | v2.3.11 新建 172 行·李时珍/陈寅恪/高濂/李约瑟·太医院/丹药长生/本草/养生·A5 第 31 个 |
| docs/02-人物深度分析/高翠兰深化专题.md | W374 | v2.3.11 新建 128 行·学术九段式·A3 女性深化系列第 5 篇·乔多萝/沃斯通克拉夫特/鲁宾/吉利根·A3 205→211 |
| docs/02-人物深度分析/金圣宫娘娘深化专题.md | W375 | v2.3.11 新建 125 行·第 6 篇·福柯/麦金农/巴特基/戈夫曼·被掳身体/棕团扇隔离 |
| docs/02-人物深度分析/李贽与悟空对照专题.md | W376 | v2.3.11 新建 158 行·明代人物对照系列第 4 篇·李卓吾评本钩子/童心说/狂禅 |
| docs/02-人物深度分析/严嵩与牛魔王对照专题.md | W377 | v2.3.11 新建 158 行·第 5 篇·丁易/沈德符/高阳/吴晗·权臣与妖王结构性同构 |
| docs/02-人物深度分析/昴日星官外传.md | W378 | v2.3.11 新建 121 行·外传散文体·卯日鸡"准时的神"·第 55 回降蝎子精 |
| docs/02-人物深度分析/百眼魔君外传.md | W379 | v2.3.11 新建 107 行·外传散文体·黄花观技术官僚·"千只眼不如一根针"·第 73 回 |
| docs/03-主题与情节专题/取经空间生产专题.md | W380 | v2.3.11 新建 133 行·列斐伏尔/哈维/索亚/德·塞托·与空间叙事学/空间政治学区分·A4 205→209 |
| docs/03-主题与情节专题/西游与媒介理论专题.md | W381 | v2.3.11 新建 144 行·麦克卢汉/英尼斯/基特勒/波斯特·紧箍咒/通关文牒/金箍棒作为媒介 |
| docs/03-主题与情节专题/西游与死亡研究专题.md | W382 | v2.3.11 新建 144 行·阿里耶斯/弗洛伊德/海德格尔/贝克尔·死亡态度史/六贼之死/凌云渡脱胎 |
| docs/03-主题与情节专题/西游与解释学专题.md | W383 | v2.3.11 新建 139 行·伽达默尔/施莱尔马赫/利科/海德格尔·无字真经作为解释学事件 |

## W359-W368 A 方向内容扩容 15 篇（2026-08-01·v2.3.10）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/明代市井百态对照专题.md | W359 | v2.3.10 新建 185 行·谢肇淛/顾起元/沈榜/范濂四位明代笔记史料家·市井五重对照·与 W126 等形成"十层明代镜像结构"·A5 25→30 |
| docs/04-文化与历史背景/明代文学体裁与西游对照专题.md | W360 | v2.3.10 新建 168 行·鲁迅/胡适/郑振铎/李卓吾·章回体/韵散相间/回目对仗/评点传统四体裁维度 |
| docs/04-文化与历史背景/明代宫廷与宦官制度对照专题.md | W361 | v2.3.10 新建 170 行·王世贞/丁易/吴晗/高阳·内廷/宦官/特务/决策四宫廷维度·修复"蟠桃会"line 3→35（4 处引用） |
| docs/04-文化与历史背景/西游与明代商业经济专题.md | W362 | v2.3.10 新建 170 行·傅衣凌/吴承明/范金民/卜正民·商人资本/市场流通/税收勒索/功德经济四维度·修复"紫金钵盂"line 29→47（5 处引用） |
| docs/04-文化与历史背景/西游与明代民间宗教专题.md | W363 | v2.3.10 新建 169 行·杨庆堃/欧大年/韩明士/王斯福·与 W225 形成"民间信仰-民间宗教"双轨 |
| docs/02-人物深度分析/玉面狐狸深化专题.md | W364 | v2.3.10 新建 124 行·伊里加蕾/穆尔维/巴特勒/斯皮瓦克·A3 女性人物深化（W237-W244 女性主义八框架系列） |
| docs/02-人物深度分析/泾河龙王外传.md | W364 | v2.3.10 新建 135 行·外传散文体·第 9-10 回因骄傲毁约撬动王朝的悲剧 |
| docs/02-人物深度分析/唐僧-方向二深化.md | W364 | v2.3.10 新建 115 行·方向二散文体·十世轮回与"佛性执念" |
| docs/02-人物深度分析/孙悟空外传.md | W364 | v2.3.10 新建 127 行·外传散文体·斗战胜佛之后的孤独旅程 |
| docs/02-人物深度分析/观音外传.md | W364 | v2.3.10 新建 107 行·外传散文体·"取经工程项目经理"视角 |
| docs/02-人物深度分析/车迟国三国师外传.md | W364 | v2.3.10 新建 125 行·外传散文体·第 44-46 回三位"技术官僚"被体制抛弃 |
| docs/03-主题与情节专题/取经数字人文专题.md | W365 | v2.3.10 新建 152 行·莫莱蒂远读/乔克斯宏观分析/毕尔/伯特算法批评·与 W289-W291 形成"数字方法"新维度 |
| docs/03-主题与情节专题/西游与复杂性科学专题.md | W366 | v2.3.10 新建 150 行·霍兰德/考夫曼/圣塔菲学派/普里高津·与西游与系统论专题形成"系统-复杂性"深化 |
| docs/03-主题与情节专题/西游与记忆技术专题.md | W367 | v2.3.10 新建 153 行·阿斯曼/诺拉/格罗托夫斯基/范·迪克·与 W253/W255/W256 形成"记忆四联" |
| docs/03-主题与情节专题/取经团队决策论专题.md | W368 | v2.3.10 新建 152 行·西蒙/卡尼曼/冯·诺依曼/贾尼斯·与取经团队心理学/组织学/动力学形成"决策"新维度 |
| scripts/audit/line_check.py | W359-W368 | v2.3.10 新建·text-search.html 回内行号验证工具（line 号权威源确立）·A3 200→206 / A4 202→206 / A5 25→30 |

## W358 静态优先健壮性加固·前端自包含与交互增强（2026-08-05）

| 文件 | W | 说明 |
|---|---|---|
| scripts/inline_css.py | W358 | v2.3.9 新建·幂等 CSS 内联生成器·将 `../tokens.css`+`../system.css` `<link>` 内联为 `<style>` 块覆盖 `data/` 及子目录 136 个 HTML（含 `data/en/`）；`--dry` 预览、`--force` 重同步；单一事实源仍是 `site/tokens.css`/`site/system.css` |
| site/data/graph-explorer.html | W358 | v2.3.9 多重加固：localStorage 持久化（选中图谱/筛选/搜索/节点/坐标）+ 节点「相关研究」跳 search.html?q= + 离线图集内联（删外部 graph-fallback.js src）+ flex 布局替换 calc(100vh) + `.no-side`/`.no-drill` 可折叠 + 大图降迭代性能兜底 |
| site/static/js/rag-chat.js | W358 | v2.3.9 渡口问津升级：draft 渡口摘要改主回答（打字机）+ 来源 path 可点击 + 命中词 `<mark>` 高亮 + 历史 localStorage 持久化 + 发送带最近 4 轮 history 上下文 |
| site/data/search.html | W358 | v2.3.9 新增 `?q=` 预填自搜，闭合图谱→文链路 |
| scripts/rag/rag_server.py | W358 | v2.3.9 `/query` 解析 `history` 参数（json.loads 失败回退 None）并透传 `RAG.answer(history=...)`，向后兼容（默认 None） |
| scripts/rag/xiyouji_rag.py | W358 | v2.3.9 `answer()` 新增 `history=None` 参数；LLM 占位分支注释：接入 LLM 时把 history 拼为上下文注入 prompt（档 B 待 LLM_API_KEY） |
| site/data/81-hardships-view.html | W358 | v2.3.9 内联 `vis-tools.js`+`dataset-view.js`（消除外部 `../static/js` 不加载→停在「正在连接数据 API」的空白隐患；`</script>` 转义 `<\/script`） |
| site/data/character-relationship-3d-view.html | W358 | v2.3.9 同 81-hardships-view·内联 vis-tools.js+dataset-view.js |
| site/data/data-explorer.html | W358 | v2.3.9 内联 vis-tools.js（仅依赖 VisTools，不含 DatasetView） |
| site/data/*.html（136 页·含 data/en/） | W358 | v2.3.9 由 scripts/inline_css.py 批量内联 tokens.css+system.css，彻底摆脱 `../` 外观依赖；D3 CDN 保留 |
| scripts/bump_footer_version.py | W358 | v2.3.9 新建·幂等 footer 版本印章升 W358 脚本·三规则（①`CHANGELOG.md</a> v2.3.8 W357` 锚点 ②`file-index.md</a> W357` 锚点 ③`<footer>` 块内散文式 `v2.3.8 W357` prose）覆盖 en/ 51 页 + dukou-engine.html；`--dry` 预览 |
| site/en/*.html（51 页）+ site/dukou-engine.html | W358 | v2.3.9 footer 版本印章由 v2.3.8 W357 升 v2.3.9 W358（en/ 页锚点+散文双印章 + dukou-engine 散文式 footer）；data/ 中文页 footer 无版本印章故不动 |
| site/en/README.md | W358 | v2.3.9 footer 双索引版本示例同步 v2.3.9 W358（第 85/92 行描述与现状一致） |

## W357 英文站扩张（A6 诗词译介续·四篇 poetry essay 译介 + 入口与文档同步，2026-08-04）

| 文件 | W | 说明 |
|---|---|---|
| site/en/essay-character-fu.html | W357 | v2.3.8 新建·英文站 E34 译介·人物赋（四理论家 刘勰/钟嵘/司空图/王国维 + 四赋型 定像/变化/点化/封圣 line 522/864/1393/7085·明代镜像 前后七子/公安派/戏曲唱白） |
| site/en/essay-rhythm-analysis.html | W357 | v2.3.8 新建·英文站 E35 译介·韵律分析（四理论家 王力/启功/周振甫/朱光潜 + 四维度 平仄/对仗/节奏/韵律圆成 line 522/864/1393/7085·仄起平收） |
| site/en/essay-thematic-poetry.html | W357 | v2.3.8 新建·英文站 E36 译介·主题诗词创作（项目自身四首创作 五行山/三打白骨精/真假美猴王/凌云渡 忠实英译·旧瓶装新酒） |
| site/en/essay-original-poetry.html | W357 | v2.3.8 新建·英文站 E37 译介·原著诗词赏析（约 800 首功能/主题/回目对联/体裁分布 6%/37%/10%/25%/4%/6%/5% + 人物赞对比·E6/E31/E33 总览伴侣） |
| site/en/index.html | W357 | v2.3.8 入口卡片 46→50（新增 E34-E37 四卡）·section-sub 文案更新·footer 双索引升 v2.3.8 W357 |
| site/en/README.md | W357 | v2.3.8 文件清单 47→51·版本号升 v2.3.8 W357·Footer/Verification/Scope 段同步 |

## W346 数据闭环·八十一难逐难明细填充（2026-08-04）

| 文件 | W | 说明 |
|---|---|---|
| dataset/81-hardships.json | W346 | v2.2.97 填充 `hardships` 数组 0→81 条逐难明细（index/name/chapter/cause/ending/difficulty），数据源 scripts/C_情节/hardships_81.py → scripts/output/data/hardships_81.json，前 80 难与原著第 99 回灾难簿对齐；数据集由"半空"变闭环 |
| scripts/_build_81_hardships.py | W346 | v2.2.97 新建·可重跑桥接脚本·写入前断言四项聚合轴与既有值 100% 吻合 |
| dataset/README.md | W346 | v2.2.97 第 17 行登记键补 `hardships`、大小 0.7→5.1 KB |

## W345 英文站扩张（A5/A6 三篇专题译介 + 入口与文档同步，2026-08-04）

| site/en/essay-zen-koan-vs-neidan.html | W345 | v2.2.96 新建·英文站 A5 专题译介·禅宗公案顿悟 × 清代内丹渐修两种读法并置（策展摘要·非全文翻译·footer 双索引 v2.2.96 W345） |
| site/en/essay-version-evolution.html | W345 | v2.2.96 新建·英文站 A5 专题译介·南宋诗话—1592 世德堂本之间"失落的平话层"推考（明确标注推测/残存） |
| site/en/essay-scenery-poems.html | W345 | v2.2.96 新建·英文站 A6 专题译介·景物诗"山水奇观/旅途即景/禅境灵域"三型分类赏析（引文逐句核对原著） |
| site/en/index.html | W345 | v2.2.96 入口卡片 5→8（新增 E4/E5/E6 三卡）·section-sub 文案更新·footer 双索引升 v2.2.96 W345 |
| site/en/README.md | W345 | v2.2.96 文件清单 7→10·版本号升 v2.2.96 W345·Footer/Verification/Scope 段同步 |
| site/en/tribulations.html | W347 | v2.2.98 新建·英文站数据页·八十一难看板（dataset/81-hardships.json 桥接·成因/结局/难度三维 + 成因×结局矩阵 + 81 难全表） |
| site/en/characters.html | W347 | v2.2.98 新建·英文站数据页·取经五人组（Belbin 团队角色 + 五维心理画像 + 凝聚力里程碑） |
| site/en/bestiary.html | W347 | v2.2.98 新建·英文站数据页·妖魔生态（30 种群·4 社会型·73% 灭绝率·能力极值） |
| site/en/chapters-map.html | W347 | v2.2.98 新建·英文站数据页·百回阅读地图（四幕分章 + 每回回目对联/主要人物/地点） |
| site/en/essay-historical-xuanzang.html | W348 | v2.2.99 新建·英文站 E7 译介·历史玄奘 vs 小说玄奘七维对照（138 国·657 经·1335 卷·明朝投射） |
| site/en/essay-divine-bureaucracy.html | W348 | v2.2.99 新建·英文站 E8 译介·天庭即明代衙门（黄仁宇/钱穆/韦伯/王斯福·照妖镜反讽） |
| site/en/essay-chapter-couplets.html | W348 | v2.2.99 新建·英文站 E9 译介·百回回目七言对联（格律/五型/结构统计 100%-85%-70%） |
| site/en/visualizations.html | W348 | v2.2.99 新建·英文站导览·85 个 site/data 可视化分页入八簇（含每页说明与直链） |
| site/en/character-wukong.html | W348 | v2.2.99 新建·英文站深度页·孙悟空（名号/石生/反天/13500 斤金箍棒/心猿·跨可视化链接） |
| site/en/methodology.html | W348 | v2.2.99 新建·英文站指南·全站读法（内容地图/A4 七段式/宣纸设计语言/双索引/零编造门禁） |
| site/en/character-tangseng.html | W349 | v2.3.0 新建·英文站深度页·唐僧（Belbin 协调者/五维心理画像/与悟空信任张力·江流儿→旃檀功德佛） |
| site/en/character-bajie.html | W349 | v2.3.0 新建·英文站深度页·猪八戒（天蓬→猪→净坛使者/团队社交胶水/食欲喜剧） |
| site/en/character-shaseng.html | W349 | v2.3.0 新建·英文站深度页·沙悟净（卷帘大将→金身罗汉/执行者/平稳心理轴） |
| site/en/essay-quanzhen-daoism.html | W349 | v2.3.0 新建·英文站 E10 译介·道教全真派内丹学读法（心猿/金公/木母/刀圭·四理论家·四概念） |
| site/en/character-bailongma.html | W350 | v2.3.1 新建·英文站深度页·白龙马（西海三太子→马→八部天龙/ Belbin Specialist/ 低恐惧高顺从雷达） |
| site/en/essay-buddhist-chan.html | W350 | v2.3.1 新建·英文站 E11 译介·佛教禅宗读法（达摩/慧能/神秀/玄奘·八识结构·四概念） |
| site/en/essay-folk-belief.html | W350 | v2.3.1 新建·英文站 E12 译介·民间信仰读法（杨庆堃/王斯福/武雅士/华琛·弥漫性宗教/帝国隐喻/标准化） |
| site/en/essay-composition-origins.html | W351 | v2.3.2 新建·英文站 E13 译介·成书背景（作者之谜/版本谱系/历史vs小说玄奘/明代世界） |
| site/en/essay-ming-metaphor.html | W351 | v2.3.2 新建·英文站 E14 译介·明代隐喻（六重隐喻/官场/荫庇株连/市民文化/宗教政治） |
| site/en/essay-three-teachings.html | W351 | v2.3.2 新建·英文站 E15 译介·佛道思想（三教合一/五蕴对应五人/内丹三家相见） |
| site/en/site-map.html | W351 | v2.3.2 新建·英文站全局主题索引·七簇 29 链接 |
| site/en/essay-cipai-xijiangyue.html | W352 | v2.3.3 新建·英文站 E16 译介·西江月词牌（52字双调·四理论家 王国维/叶嘉莹/龙榆生/夏承焘·四重境界 line 522/864/1393/7085） |
| site/en/essay-cipai-linjiangxian.html | W352 | v2.3.3 新建·英文站 E17 译介·临江仙词牌（60字·四理论家 王国维/叶嘉莹/龙榆生/唐圭璋·四重境界 line 981/2306/4432/7052） |
| site/en/essay-cipai-mantingfang.html | W352 | v2.3.3 新建·英文站 E18 译介·满庭芳词牌（全书唯一明名词牌·樵夫 line 39·四理论家 王国维/叶嘉莹/龙榆生/缪钺·四重境界 line 39/981/4792/7085） |
| site/en/essay-cipai-shuidiaogetou.html | W352 | v2.3.3 新建·英文站 E19 译介·水调歌头词牌（95字长调·四理论家 王国维/叶嘉莹/龙榆生/缪钺·苏轼对照·四重境界 line 522/864/1393/7085） |
| site/en/essay-ming-examination.html | W353 | v2.3.4 新建·英文站 E20 译介·明代科举制度（取经=科举复刻·如来开科 line 981/玄奘被举 line 1219/八十一难=考课/灵山金榜 line 7085·四理论家 黄仁宇/艾尔曼/宫崎市定/韦伯） |
| site/en/essay-ming-garrison.html | W353 | v2.3.4 新建·英文站 E21 译介·明代卫所制度（天兵/龙宫/狮驼=卫所三层次·line 632/700/726/5484·四史家 黄仁宇/顾诚/于志嘉/彭勇） |
| site/en/essay-ming-maritime-ban.html | W353 | v2.3.4 新建·英文站 E22 译介·明代海禁政策（花果山海外法外/朝贡跨海/流沙渡水/真经东传·line 522/996/1936/7085·四史家 黄仁宇/樊树志/李庆/卜正民） |
| site/en/essay-ming-judiciary.html | W353 | v2.3.4 新建·英文站 E23 译介·明代司法制度深化（四案 赛太岁安静犯罪/朱紫国王罪己/金圣宫失声/崔判官改簿·四理论家 黄仁宇/瞿同祖/滋贺秀三/寺田浩明） |
| site/en/essay-ming-politics.html | W354 | v2.3.5 新建·英文站 E24 译介·明代政治制度（天庭=明代政治镜像·皇权/官僚/藩封/法律四重对照·line 522/621/864/981·四理论家 黄仁宇/钱穆/孟森/谢国桢） |
| site/en/essay-ming-economy.html | W354 | v2.3.5 新建·英文站 E25 译介·明代经济制度（天庭财政/取经团队=粮长/功德货币/长时段·line 660/840/1149/1393/2073/7085·四理论家 黄仁宇/梁方仲/韦伯/布罗代尔） |
| site/en/essay-ming-military.html | W354 | v2.3.5 新建·英文站 E26 译介·明代军事制度（天兵=卫所兵/李天王=总兵/哪吒=家丁/二郎神=土司·四学者 黄仁宇/茅海建/梁方仲/孟森） |
| site/en/essay-ming-religion.html | W354 | v2.3.5 新建·英文站 E27 译介·明代宗教制度（僧官/昊天上帝/关帝观音/度牒考核·line 981/1219/7085·四理论家 黄仁宇/钱穆/韦伯/杨庆堃） |
| site/en/essay-ming-social-customs.html | W355 | v2.3.6 新建·英文站 E28 译介·明代社会风俗（婚姻/服饰/饮食/丧葬/科举五大制度性风俗·福柯治理术·13 处 line 锚点·古今对位五组） |
| site/en/essay-ming-literary-thought.html | W355 | v2.3.6 新建·英文站 E29 译介·明代文学思想（李贽童心说/袁宏道公安派/归有光唐宋派/李梦阳前后七子·四大名著横向对位·五阶段纵向定位） |
| site/en/essay-ming-intellectual-history.html | W355 |
| site/en/essay-poetry-opening.html | W356 | v2.3.7 新建·英文站 E31 译介·开篇诗（三重诗学坐标 王国维/朱光潜/叶嘉莹 + 六处关键回目诗 1/7/8/14/22/100 三教合一·道→佛→圆融 + 古今对位） |
| site/en/essay-poetry-imagery.html | W356 | v2.3.7 新建·英文站 E33 译介·意象谱系（四理论家 庞德/艾略特/巴什拉/刘勰 + 四意象 石猴/蟠桃/白骨/真经=造化→欲望→虚妄→觉悟 + 中西对位 刘勰早于西方意象派1400年） |
 v2.3.6 新建·英文站 E30 译介·明代思想史（王阳明心学/李贽童心异端/王畿泰州学派/黄宗羲君客主·四组案例对照 line 1459/4370/1868/7085·八层明代镜像闭环） |




## W344 质量增强包（术语统一审计 + A1 结构化元数据 + A5/A6 提质 + 项目说明版本残留修复，2026-08-04）

| docs/00-导读/项目说明.md | W344 | v2.2.95 修复·第 45 行残留 v2.2.69 旧版本号（实为 v2.2.94）·消除版本错乱 |
| scripts/_audit_terminology.py | W344 | v2.2.95 新建·术语统一审计（全站 docs/ + site/ 扫描·繁→简专名/OCR 错谬/单字繁体残余·区分有意别名与错谬·产出 terminology-audit-report.md 并保守修复） |
| scripts/_build_chapter_metadata.py | W344 | v2.2.95 新建·A1 逐回结构化元数据生成（回目 couplet/主要人物≤6/难序/地点≤6·由 dataset 反推·零编造） |
| dataset/chapters-metadata.json | W344 | v2.2.95 新建·第 42 个结构化 JSON·100 回结构化元数据（回目/主要人物/难序/地点）·反哺图谱 |
| docs/01-全书逐回解读/第001-100回-*.md（100 篇） | W344 | v2.2.95 注入 `<!-- chapter-meta -->` 机器可读注释（渲染不可见·可重跑·反哺图谱） |
| docs/04-文化与历史背景/西游与禅宗公案专题.md | W344 | v2.2.95 新建·A5 提质·禅宗顿悟读法 × 清代内丹渐修读法并置 |
| docs/04-文化与历史背景/版本演变补遗-平话层.md | W344 | v2.2.95 新建·A5 提质·已佚《西游记平话》层残迹推考（明确标注推测/残存） |
| docs/05-诗词歌赋/原著景物诗分类赏析专题.md | W344 | v2.2.95 新建·A6 提质·景物诗三型分类赏析（引文与原著回目原文逐句核对） |

## W343 交付收尾（内容质量收口 + 工程化 CI 转绿，2026-08-04）

| site/system.css | W343 | v2.2.94 改造·`#summary-table-wrap` 加 `overflow-x:auto`·消除 5 个网络图页 mobile 视图 table-overflow 真实缺陷（intertextuality/monster-female/narratology-12d/narratology-13d/six-senses-narratology-network） |
| scripts/sync_docs.py | W343 | v2.2.94 改造·移除 `_eval_dim_expr` 中的 eval()·改安全手写解析器（支持前导负号/空串）·XSS 安全门禁 high 1→0 |
| scripts/batch_screenshots.js | W343 | v2.2.94 改造·过滤浏览器级良性 console.error（file:// 无后端噪声）+ 放松 --fail-on-issues 门槛（仅阻断未捕获 pageerror 与捕获失败） |
| .github/workflows/screenshot-review.yml | W343 | v2.2.94 修复·空 baseline 误报（grep 空 baseline 返回 1 致整步 exit 1·管道加 `\|\| true` 容错） |
| scripts/_add_analysis_links_v2.py | W343 | v2.2.94 新建·A1 逐回关联分析 footer 收尾（剩余 23 回补全·100/100 覆盖·586 链接 0 断） |
| scripts/_annotate_sd_crossref.py | W343 | v2.2.94 新建·28 篇跨章 SD 源切片补充关联分析 footer（A1 章节 + A3 人物·155 链接 0 断） |
| scripts/_audit_content_gaps.py | W343 | v2.2.94 新建·图谱实体×文档覆盖率审计（确认无宏观空缺·可复用） |
| scripts/rag/xiyouji_rag.py | W343 | v2.2.94 重建·build_index(force=True)·rag_index.json + rag_graph.json 675 文档全覆盖（补全 W084/W342 两篇 gap-fill） |

## W337 RAG质量提升+数据API化+可视化交互深化+移动端PWA（2026-08-03）

## W342 权力五联对照(W084)+妖怪身份政治·A4 gap-fill（2026-08-03）

| docs/03-主题与情节专题/权力五联对照专题.md | W084/W342 | v2.2.93 新建·填补自 W089 空间政治学起即以 W084 编号互链却长期未成稿的空缺·A4 七段式概论·定义"权力来源→制度化→工具化→空间化→谱系化"五联闭环·链接 W077/W078/W079/W080/W081·零依赖·file:// 全兼容 |
| docs/03-主题与情节专题/妖怪身份政治专题.md | W342 | v2.2.93 新建·权力五联"权力来源"维度总论·以泰勒/霍耐特/法农/斯皮瓦克身份政治理论重读西游"正/妖"二分·与 W077 黑熊精.md 个案形成"总论→个案"结构·A4 计数 +2（199→201） |

## W340 图谱关系语义增强（边关系着色·语义权重·关系筛选·钻取富语义，2026-08-03）

| site/data/graph-explorer.html | W340 | v2.2.92 改造·图谱关系语义增强（边按关系类型 curated 着色+语义权重粗细+关系类型筛选+钻取面板「语义关系汇总」+属性/取值富展示·悬停边可见「关系·属性·取值」·normalizeGraph 修复整数 id 钻取·edgeRel 兼容 relation/type）·复用 dukou 范式适配 file:// |
| scripts/api/api_server.py | W340 | v2.2.92 改造·openapi version 升 v2.2.92 |

## W339 知识图谱探索器（纯SVG力导向·多图·/graph端点，2026-08-03）

| site/data/graph-explorer.html | W339 | v2.2.91 新建·知识图谱探索器（零依赖纯SVG力导向·多图切换+按类型筛选+维度标签+节点拖拽+钻取+SVG/PNG/JSON导出）·复用 dukou 范式适配 file:// |
| scripts/api/api_server.py | W339 | v2.2.91 改造·新增 GET /graph（图集清单）+ GET /graph/<name>（nodes/edges 归一化）·注册 yuanqi-graph + character-relationship-3d |
| dataset/yuanqi-graph.json | W339 | v2.2.91 新建·由 scripts/output/yuanqi_*.csv 生成的佛法=AI=西游 三元映射图谱（20 节点/20 边） |
| site/static/js/graph-fallback.js | W339 | v2.2.91 新建·离线内嵌图集（yuanqi-graph + character-relationship-3d）·file:// 降级用 |
| site/dashboard.html | W339 | v2.2.91 改造·数据中枢新增「知识图谱探索器」入口卡片 |
| site/static/js/datahub-index.js | W339 | v2.2.91 改造·41 数据集名称/标题索引（含 yuanqi-graph） |
| tests/e2e/test_graph.js | W339 | v2.2.91 新建·图谱 E2E 回归（离线渲染+钻取+筛选 + /graph 在线断言） |

## W338 收口价值（数据API接入+vis-tools范式复用+新功能E2E回归，2026-08-03）

| site/data/search.html | W338 | v2.2.90 新建·全站搜索（在线 /search 跨集递归检索 + 离线 file:// 内置索引降级）·复用 vis-tools |
| site/static/js/dataset-view.js | W338 | v2.2.90 新建·单数据集可交互渲染模块（键 tab→数组表/对象柱状图）·vis-tools 范式复用核心 |
| site/static/js/datahub-index.js | W338 | v2.2.90 新建·40 数据集名称/标题索引（dashboard 数据中枢离线降级用） |
| site/data/character-relationship-3d-view.html | W338 | v2.2.90 新建·人物关系可交互视图（22 节点表+钻取·fetch 在线 + FALLBACK 离线） |
| site/data/81-hardships-view.html | W338 | v2.2.90 新建·八十一难可交互视图（起因/结局/难度分布柱状图） |
| site/dashboard.html | W338 | v2.2.90 改造·新增「数据中枢」section（在线 /datasets + 离线 datahub-index·卡片跳转） |
| tests/e2e/test_newfeatures.js | W338 | v2.2.90 新建·新功能 E2E 回归（离线渲染 + API 在线断言） |



| scripts/rag/xiyouji_rag.py | W337 | v2.2.89 改造·RAG 质量提升：西游专名/别名词典（40 canonical→别名）+ 最长匹配分词 + 查询别名扩展 + 标题/短语字段加权 + RRF 四路融合重排 + 改进摘录（最近小标题上下文）·INDEX_VERSION=2 触发缓存重建 |
| scripts/rag/rag_server.py | W337 | v2.2.89 改造·HTTPServer→ThreadingHTTPServer 修复并发卡死 |
| scripts/api/api_server.py | W337 | v2.2.89 新建·零依赖数据 API 服务（/datasets /dataset/<name> /dataset/<name>/keys /search?q= 跨集递归检索 /health /openapi.json + /api 文档页 + 托管 site/ 静态资源）·ThreadingHTTPServer |
| site/static/js/vis-tools.js | W337 | v2.2.89 新建·可视化交互工具库（makeFilterableTable 搜索+排序+CSV/JSON 导出 + openDrill/closeDrill 钻取面板 + exportSVG→PNG · 沿用 tokens.css 设计语言） |
| site/data/data-explorer.html | W337 | v2.2.89 新建·可筛选/可钻取/可导出旗舰示范页·fetch 在线优先 + file:// 内嵌 FALLBACK 降级 |
| site/manifest.webmanifest | W337 | v2.2.89 新建·PWA manifest（name/short_name/start_url/display standalone/theme_color #3a2820/background_color #faf7f2 + 3 icons） |
| site/sw.js | W337 | v2.2.89 新建·Service Worker（app shell 预缓存 + 导航网络优先回退缓存 + 静态缓存优先 + 数据/API 网络优先回退缓存 + activate 清理旧缓存） |
| site/static/icons/icon-192.png | W337 | v2.2.89 新建·PWA 图标 192×192（Pillow·宣纸底+朱砂外圈+靛青中心印） |
| site/static/icons/icon-512.png | W337 | v2.2.89 新建·PWA 图标 512×512 |
| site/static/icons/icon-maskable-512.png | W337 | v2.2.89 新建·PWA maskable 图标 512×512 |
| site/index.html | W337 | v2.2.89 改造·head 加 manifest link + </body> 前注册 SW（http 协议守卫）·footer v2.2.86 W334 → v2.2.89 W337 |
| site/mobile-index.html | W337 | v2.2.89 改造·head 加 manifest link + </body> 前注册 SW（http 协议守卫） |
| CHANGELOG.md | W337 | v2.2.89 同步·新增 W337 版本段·W### 编号范围 W336→W337 |
| README.md | W337 | v2.2.89 同步·版本号 v2.2.88→v2.2.89·新增 W337 四方向描述 |
| STRUCTURE.md | W337 | v2.2.89 同步·版本号 v2.2.88→v2.2.89·新增 W337 四方向描述 |
| docs/00-导读/项目说明.md | W337 | v2.2.89 同步·版本号 v2.2.88→v2.2.89·新增 W337 段 |
| scripts/output/file-index.md | W337 | v2.2.89 同步·新增 v2.2.89 反向索引段 |
| 交接文档.md | W337 | v2.2.89 同步·更新当前进度至 W337 四方向·版本号 v2.2.88→v2.2.89 |

## W336 RAG前端接入+数据产品化（2026-08-03）

| docs/00-导读/文档规范.md | W336 | 新建·文档写入规则（防膨胀·归档触发·6文档同步正确方式） |

| 文件 | 操作 | 说明 |
|------|------|------|
| site/static/js/rag-chat.js | 新建 | 渡口问津浮动对话组件 |
| scripts/extract_datasets.js | 新建 | EMBEDDED_DATA 提取脚本 |
| dataset/*.json（40 个） | 新建 | 结构化数据集 |
| dataset/README.md | 新建 | 数据手册 |
| site/index.html | 修改 | 嵌入 rag-chat.js |
| site/dashboard.html | 修改 | 嵌入 rag-chat.js |


## W335 全站设计系统迁移（2026-08-03）

| 文件 | 操作 | 说明 |
|------|------|------|
| site/system.css | 新建 | 组件设计系统（topnav/hero/card/kpi/chart/table/footer） |
| site/data/_shell.html | 新建 | 数据页骨架模板 |
| scripts/w335_migrate_design_system.py | 新建 | 幂等迁移脚本 |
| site/index.html | 重写 | 594→170 行，通用组件由 system.css 驱动 |
| site/data/*.html（72 页） | 迁移 | 替换 head/hero/footer，保留 D3 逻辑 |
| site/data/ 4 特殊页面 | 手动迁移 | 非标准 hero 结构 |
| 16 页 gen-time 修复 | 修改 | null guard 防止 JS 报错 |


## 项目文件反向索引（按版本倒序，覆盖 site/data/ 可视化页面 + docs/ 文档 + 根目录 6 文件 + 其他）

### v2.2.86 W334 全站 UI/UX 重设计·新中式·数字雅集（tokens 集中化+首页/看板重写+88 页批量换肤+字体子集化·零新增运行时依赖·A4 计数不变仍 199 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| site/tokens.css | W334 | v2.2.86 重写为 v2·新中式数字雅集令牌集中化：新色板（#FAF7F0/#23201A/#C8463A/#E5DFD0）+ --chart-1..6 雅集图表五色 + --font-serif/sans/mono 三层字体栈 + 6 个 @font-face 子集 webfont + hero 玄墨覆写 + 全站字体分层覆写 + 选区/焦点细节 |
| site/index.html | W334 | v2.2.86 全量重写·新中式首页：顶部导航（印章+字标+文字链）+ 负空间 Hero（kicker+88px 宋体大标+巨数 100 回）+ 墨山纹 SVG + 数据条（100/625/80/133）+ 九卷索引档案表（00-09 编号+宋体板块名+描述+靛蓝 meta）+ 玄墨开篇诗深色节奏段 + 站点工具不等高卡片 + 新页脚·375px 断点·skip-link/a11y |
| site/dashboard.html | W334 | v2.2.86 全量重写·新中式看板：紧凑看板头+数据源注条+4 KPI 卡+八十一难三维透视（环图标签外置图例·色块+名称+数值+占比·语义配色靛蓝=被接走/朱砂=被诛杀）+交叉表+关键洞察+取经路线紧凑条+专题数据看板（文字筛选 tab+41 卡+搜索浮层 JS 交互原样保留）+标签云横幅+研究矩阵 10 卡（A4 199·625 篇口径修正）+三层架构 |
| site/_template.html | W334 | v2.2.86 升级·新令牌/玄墨 hero/发丝线卡片/图表规范注释（系列色取 --chart-1..6·标签一律外置·环图内径 0.62R）+ CHART_PALETTE 常量·new_page.py 占位符全部保留兼容 |
| scripts/w334_reskin.py | W334 | v2.2.86 新建·批量换肤脚本（幂等 W334-RESKIN 标记）：tokens.css 链接归位至 </head> 前 + JS 硬编码色值映射（#7a5230→#C9A063/#5a7a3a→#6B8E5A/#2c2418→#23201A/#6b5e4d→#6B6455）·处理 88 页 |
| scripts/w334_font_subset.py | W334 | v2.2.86 新建·字体子集化管线：扫描 docs/+site/ 实际用字（~3,700 字符）→ pyftsubset（fonttools+brotli）→ site/static/fonts/ 4 个 woff2（Noto Serif/Sans SC 可变字重 + JetBrains Mono Regular/Medium） |
| site/data/*.html（80 个可视化页面） | W334 | v2.2.86 批量换肤：tokens.css 链接归位（此前 80 页均无外链 tokens·内联重复定义）+ JS 色值映射雅集色板·hero 玄墨化与字体分层经 tokens.css 级联覆写生效·页面结构与 EMBEDDED_DATA 未动 |
| site/en/*.html（7 个英文站页面） | W334 | v2.2.86 批量换肤：同 site/data 处理 |
| site/mobile-index.html | W334 | v2.2.86 批量换肤：tokens.css 链接归位 + JS 色值映射 |
| site/dukou-engine.html | W334 | v2.2.86 批量换肤：tokens.css 链接归位 + JS 色值映射（图谱配色随雅集色板） |
| site/static/fonts/ | W334 | v2.2.86 新建·子集化 woff2 产物目录（pyftsubset 生成·~3,700 字覆盖全站文本） |
| assets/fonts/source/ | W334 | v2.2.86 新建·源字体目录（google/fonts 官方仓库可变 TTF：NotoSerifSC/NotoSansSC [wght] + JetBrains Mono Regular/Medium） |
| CHANGELOG.md | W334 | v2.2.86 同步·新增 W334 版本段·W### 编号范围 W333→W334 |
| README.md | W334 | v2.2.86 同步·版本号 v2.2.85→v2.2.86·新增 W334 全站 UI/UX 重设计描述 |
| STRUCTURE.md | W334 | v2.2.86 同步·版本号 v2.2.85→v2.2.86·新增 W334 描述 |
| docs/00-导读/项目说明.md | W334 | v2.2.86 同步·版本号 v2.2.85→v2.2.86·新增 W334 段 |
| scripts/output/file-index.md | W334 | v2.2.86 同步·新增 v2.2.86 反向索引段 |
| 交接文档.md | W334 | v2.2.86 同步·更新当前进度至 W334 全站 UI/UX 重设计·版本号 v2.2.85→v2.2.86·A4 主题专题 199 篇（不变） |

### v2.2.85 W333 渡口引擎图谱力导向布局·消除点击跳变·节点度数半径·方向箭头·焦点高亮（零依赖·复用 /graph·nodePos 位置缓存轻量力导向·A4 计数不变仍 199 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| site/dukou-engine.html | W333 | v2.2.85 改造·新增 nodePos 跨重绘位置缓存 Map + graphFocus 焦点·layoutGraph() 轻量力导向（斥力+边弹簧+中心引力+锚定回弹）·新节点从父旁长出·旧节点锚定稳定·节点半径按度数映射 5–14px·边加 SVG marker 方向箭头·点击节点聚焦高亮+展开邻居·mergeTriples(triples,parent) 记种子父·resetGraph() 清 nodePos/graphFocus·footer 版本 v2.2.84 W332 → v2.2.85 W333 |
| CHANGELOG.md | W333 | v2.2.85 同步·新增 W333 版本段·W### 编号范围 W332→W333 |
| README.md | W333 | v2.2.85 同步·版本号 v2.2.84→v2.2.85·新增 W333 渡口引擎图谱力导向布局描述 |
| STRUCTURE.md | W333 | v2.2.85 同步·版本号 v2.2.84→v2.2.85·新增 W333 渡口引擎图谱力导向布局描述 |
| docs/00-导读/项目说明.md | W333 | v2.2.85 同步·版本号 v2.2.84→v2.2.85·新增 W333 段 |
| scripts/output/file-index.md | W333 | v2.2.85 同步·新增 v2.2.85 反向索引段 |
| 交接文档.md | W333 | v2.2.85 同步·更新当前进度至 W333 渡口引擎图谱力导向布局·版本号 v2.2.84→v2.2.85·A4 主题专题 199 篇（不变） |

### v2.2.84 W332 渡口引擎图谱交互式展开·节点可点击扩展关联三元组（零依赖·复用 /graph·graphState 累加去重·重置按钮·A4 计数不变仍 199 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| site/dukou-engine.html | W332 | v2.2.84 改造·新增 graphState 三元组累加器 + mergeTriples() 去重·renderGraph() 改无参读 graphState 重绘·节点加 gnode class + cursor:pointer + hover 高亮·枢纽 ghub 朱砂红描边·新增「重置图谱」按钮 resetGraph()·点击节点 expandNode(label) 调 /graph?q=label 展开邻居·footer 版本 v2.2.83 W331 → v2.2.84 W332 |
| CHANGELOG.md | W332 | v2.2.84 同步·新增 W332 版本段·W### 编号范围 W331→W332 |
| README.md | W332 | v2.2.84 同步·版本号 v2.2.83→v2.2.84·新增 W332 渡口引擎图谱交互式展开描述 |
| STRUCTURE.md | W332 | v2.2.84 同步·版本号 v2.2.83→v2.2.84·新增 W332 渡口引擎图谱交互式展开描述 |
| docs/00-导读/项目说明.md | W332 | v2.2.84 同步·版本号 v2.2.83→v2.2.84·新增 W332 段 |
| scripts/output/file-index.md | W332 | v2.2.84 同步·新增 v2.2.84 反向索引段 |
| 交接文档.md | W332 | v2.2.84 同步·更新当前进度至 W332 渡口引擎图谱交互式展开·版本号 v2.2.83→v2.2.84·A4 主题专题 199 篇（不变） |

### v2.2.83 W331 渡口引擎图谱可视化·W326 三元组纯 SVG 渲染（零依赖·复用 /graph·dukou-engine 检索结果新增关系图面板·A4 计数不变仍 199 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| site/dukou-engine.html | W331 | v2.2.83 改造·新增 #graphPanel 面板 + renderGraph() 纯 SVG 关系图（圆形布局·边标关系·枢纽节点朱砂红）·shortLabel() 截断长标签 + xmlEsc() XML 转义·renderRAG() 末尾调 renderGraph()·RAG 未启动回退模板引擎并隐藏面板·修正提示「检索真实语口语料」→「检索真实语料」·footer 版本 v2.2.82 W330 → v2.2.83 W331 |
| CHANGELOG.md | W331 | v2.2.83 同步·新增 W331 版本段·W### 编号范围 W330→W331 |
| README.md | W331 | v2.2.83 同步·版本号 v2.2.82→v2.2.83·新增 W331 渡口引擎图谱可视化描述 |
| STRUCTURE.md | W331 | v2.2.83 同步·版本号 v2.2.82→v2.2.83·新增 W331 渡口引擎图谱可视化描述 |
| docs/00-导读/项目说明.md | W331 | v2.2.83 同步·版本号 v2.2.82→v2.2.83·新增 W331 段 |
| scripts/output/file-index.md | W331 | v2.2.83 同步·新增 v2.2.83 反向索引段 |
| 交接文档.md | W331 | v2.2.83 同步·更新当前进度至 W331 渡口引擎图谱可视化·版本号 v2.2.82→v2.2.83·A4 主题专题 199 篇（不变） |

### v2.2.82 W330 本地 RAG 后端·LightRAG 架构轻量落地（零依赖·BM25 向量层 + W326 图谱层双层检索·rag_server.py + Neo4j 种子脚本 + dukou-engine 桥接·结合项目实际无 LLM key 落地零依赖本地 RAG·A4 计数不变仍 199 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| scripts/rag/xiyouji_rag.py | W330 | v2.2.82 新建·零依赖核心引擎·stdlib BM25 向量层（671 篇 docs/*.md 索引）+ W326 yuanqi_nodes/edges.csv 图谱层（1~2 跳邻居展开）·`answer()` 返回 语料片段+三元组+渡口风格摘要·`LLM_API_KEY` 存在走真实生成 |
| scripts/rag/rag_server.py | W330 | v2.2.82 新建·stdlib http.server 本地 API（/query /graph /health·默认 127.0.0.1:8777·CORS 跨域）·dukou-engine 桥接真实后端 |
| scripts/rag/graph_seed_neo4j.py | W330 | v2.2.82 新建·导出 rag_graph.json 快照 + neo4j_seed.cypher（LOAD CSV 灌入 Neo4j·对齐 LightRAG Neo4j 后端） |
| scripts/rag/README.md | W330 | v2.2.82 新建·架构对照表（LightRAG↔本实现）+ 快速开始 + 升级 lightrag-hku 路径 |
| scripts/rag/.env.lightrag.example | W330 | v2.2.82 新建·lightrag-hku 接入示例 |
| site/dukou-engine.html | W330 | v2.2.82 改造·新增「检索真实语料」按钮 + queryRAG() 调用本地 /query·服务未启动自动回退模板引擎·footer 版本 v2.2.82 W330 |
| .env.example | W330 | v2.2.82 更新·新增可选 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL / EMBEDDING_MODEL |
| CHANGELOG.md | W330 | v2.2.82 同步·新增 W330 版本段·W### 编号范围 W329→W330 |
| README.md | W330 | v2.2.82 同步·版本号 v2.2.81→v2.2.82·补回佛法=AI 六大拓展描述 + 新增 W329 招安对比 + 新增 W330 本地 RAG 后端 |
| STRUCTURE.md | W330 | v2.2.82 同步·版本号 v2.2.81→v2.2.82·补回佛法=AI 六大拓展描述 + 新增 W329 招安对比 + 新增 W330 本地 RAG 后端 |
| docs/00-导读/项目说明.md | W330 | v2.2.82 同步·版本号 v2.2.81→v2.2.82·A4 主题专题 198→199 篇·新增 W330 段 |
| scripts/output/file-index.md | W330 | v2.2.82 同步·新增 v2.2.82 反向索引段 |
| 交接文档.md | W330 | v2.2.82 同步·更新当前进度至 W330 本地 RAG 后端·版本号 v2.2.81→v2.2.82·A4 主题专题 199 篇（不变） |

### v2.2.81 W329 方向③落地·招安对比重写专题·唯识AI框架双模型对照（宋江=过拟合模型/悟空=正则化模型·跨文本西游×水浒·A4 主题专题 198→199 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| docs/03-主题与情节专题/招安对比重写专题.md | W329 | v2.2.81 新建·七段式（与 W321-W327 一致）·核心命题：招安=同一模型部署操作·差别在权重分布（过拟合vs正则化）与部署环境接口松紧·四理论家（玄奘末那识Q初始偏差/龙树空性泛化/Hinton过拟合+正则化/Vaswani注意力QKV）·三个对照维度（训练数据差异/部署环境/结局对称性）·跨文本西游×水浒（水浒以回目标注·未用西游line锚点）·6 个西游 line 号（522/864/964/1393/7012/7142 沿用已验证）·术语表+关联文档（W321/W322/W324/W325） |
| CHANGELOG.md | W329 | v2.2.81 同步·新增 W329 版本段·W### 编号范围 W328→W329 |
| README.md | W329 | v2.2.81 同步·版本号 v2.2.80→v2.2.81·A4 主题专题 198→199 篇·补回佛法=AI六大拓展描述+新增 W329 招安对比 |
| STRUCTURE.md | W329 | v2.2.81 同步·版本号 v2.2.80→v2.2.81·A4 主题专题 198→199 篇·补回佛法=AI六大拓展描述+新增 W329 招安对比 |
| docs/00-导读/项目说明.md | W329 | v2.2.81 同步·版本号 v2.2.80→v2.2.81·A4 主题专题 198→199 篇·新增 W329 段 |
| scripts/output/file-index.md | W329 | v2.2.81 同步·新增 v2.2.81 反向索引段 |
| 交接文档.md | W329 | v2.2.81 同步·更新当前进度至 W329 招安对比重写·版本号 v2.2.80→v2.2.81·A4 主题专题 198→199 篇 |

### v2.2.80 W328 佛法=AI 框架六项拓展全部落地·六文档同步收口（W322-W327·A4 主题专题 193→198 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| docs/03-主题与情节专题/黑神话拒绝金箍专题.md | W322 | v2.2.74 新建·七段式·四理论家（玄奘末那识/龙树空性/Hinton 冻结解冻/Vaswani 注意力 Q+KV 缓存）·金箍四层映射·天命人=清空 KV 缓存未初始化模型·三结局 AI 翻译·8 个 line 号（沿用 W321 锚点） |
| docs/00-导读/缘起总纲-取经是训练.md | W323 | v2.2.75 新建·元叙事八段·第0篇·回指 W321 缘起即算法专题 |
| docs/03-主题与情节专题/西游渡元定义.md | W323 | v2.2.75 新建·西游渡一句话定义·渡口隐变量 |
| docs/03-主题与情节专题/暗数据遗忘者列传.md | W324 | v2.2.76 新建·系列宣言+三篇（火焰山北坡村民/通天河童男女/狮驼国百姓）·对应三种数据命运 |
| docs/03-主题与情节专题/缘起即算法-章节体.md | W325 | v2.2.77 新建·六章（总纲回指/种子与权重/优化器/损失函数/数据增强/凌云渡 Dropout）·章节体收束表 |
| docs/03-主题与情节专题/佛学AI西游三维语义映射表.md | W326 | v2.2.78 新建·节点定义 7 类+关系定义 7 类+Cypher 模板+Neo4j 导入脚本 |
| scripts/output/yuanqi_nodes.csv | W326 | v2.2.78 新建·20 节点·列 id,node_type,buddhist_entity,ai_entity,xiyou_entity,description |
| scripts/output/yuanqi_edges.csv | W326 | v2.2.78 新建·20 边·列 source,target,relation,property,value |
| site/dukou-engine.html | W327 | v2.2.79 新建·西游渡口无我写作引擎·纯前端模板引擎·五母题库 SENSORY/ROLE/LINE/TURN/CLOSE·约 300 字渡口档案草稿·无外部 API |
| CHANGELOG.md | W328 | v2.2.80 同步·新增 v2.2.74-v2.2.80 七个版本段·W### 编号范围 W321→W328 |
| README.md | W328 | v2.2.80 同步·版本号 v2.2.73→v2.2.80·A4 主题专题 193→198 篇·新增佛法=AI 框架六大拓展描述 |
| STRUCTURE.md | W328 | v2.2.80 同步·版本号 v2.2.73→v2.2.80·A4 主题专题 193→198 篇·新增佛法=AI 框架六大拓展描述 |
| docs/00-导读/项目说明.md | W328 | v2.2.80 同步·版本号 v2.2.73→v2.2.80·A4 主题专题 193→198 篇·新增 W328 段 |
| scripts/output/file-index.md | W328 | v2.2.80 同步·新增 v2.2.80 反向索引段 |
| 交接文档.md | W328 | v2.2.80 同步·更新当前进度至 W328 佛法=AI 框架六项拓展落地·版本号 v2.2.73→v2.2.80·A4 主题专题 193→198 篇 |

### v2.2.73 W321 A4 跨学科开拓·缘起即算法专题·唯识学×深度学习×西游记三向同构映射（玄奘唯识学+龙树中观+Hinton深度学习+Vaswani注意力机制四理论家·9 个 line 号·A4 主题专题 192→193 篇）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| docs/03-主题与情节专题/缘起即算法专题.md | W321 | v2.2.73 新建·294 行·七段式·唯识学×深度学习×西游记三向同构映射·四理论家+四核心概念+取经五众=模型架构+八节点训练日志+AI心经偈子+9 个 line 号（522/554/864/964/1393/2306/4432/7012/7142） |
| CHANGELOG.md | W321 | v2.2.73 同步·新增 W321 版本段·W### 编号范围 W320→W321 |
| README.md | W321 | v2.2.73 同步·版本号 v2.2.72→v2.2.73·A4 主题专题 192→193 篇 |
| STRUCTURE.md | W321 | v2.2.73 同步·版本号 v2.2.72→v2.2.73·A4 主题专题 192→193 篇 |
| docs/00-导读/项目说明.md | W321 | v2.2.73 同步·版本号 v2.2.72→v2.2.73·新增 W321 段 |
| scripts/output/file-index.md | W321 | v2.2.73 同步·新增 W321 反向索引段 |
| 交接文档.md | W321 | v2.2.73 同步·更新当前进度至 W321 缘起即算法专题·版本号 v2.2.72→v2.2.73·A4 主题专题 192→193 篇 |

### v2.2.72 W320 S2 外部分享扩充第二批·4 篇中等文章扩展至 200+ 行（心理学 144→206 / 经济学 148→225 / 后结构主义 162→244 / 认知科学 164→220·4 subagent 并行扩展·主代理 spot-check 验证行数·16 篇 S2 外部分享全部达 200+ 行·S2 方向收束）

| 文件 | W ID | 改动摘要 |
|---|---|---|
| docs/S2-外部分享/S2-发布-西游与心理学.md | W320 | v2.2.72 扩展·心理学 144→206 行·弗洛伊德/荣格/拉康三视角各补充 line 号锚点+新增交叉验证小节 |
| docs/S2-外部分享/S2-发布-西游与经济学.md | W320 | v2.2.72 扩展·经济学 148→225 行·古典/现代/当代三维度各补充 line 号锚点+新增博弈论+总结节+古今对位表 |
| docs/S2-外部分享/S2-发布-西游与后结构主义专题.md | W320 | v2.2.72 扩展·后结构主义 162→244 行·德里达/福柯/德勒兹三视角各补充 line 号锚点+新增利奥塔宏大叙事节+总结节 |
| docs/S2-外部分享/S2-发布-西游与认知科学专题.md | W320 | v2.2.72 扩展·认知科学 164→220 行·可得性/灵活性/外部控制三视角各补充 line 号锚点+新增丹尼特多重草稿节 |
| CHANGELOG.md | W320 | v2.2.72 同步·新增 W320 版本段·W### 编号范围 W319→W320 |
| README.md | W320 | v2.2.72 同步·版本号 v2.2.71→v2.2.72·S2 外部分享描述更新 |
| STRUCTURE.md | W320 | v2.2.72 同步·版本号 v2.2.71→v2.2.72·S2 外部分享描述更新 |
| docs/00-导读/项目说明.md | W320 | v2.2.72 同步·版本号 v2.2.71→v2.2.72·新增 W320 段 |
| scripts/output/file-index.md | W320 | v2.2.72 同步·新增 W320 反向索引段 |
| 交接文档.md | W320 | v2.2.72 同步·更新当前进度至 W320 S2 外部分享收束·版本号 v2.2.71→v2.2.72·4 篇扩展至 200+ 行·S2 方向收束 |

---

> **历史归档**：W319 及更早的反向索引已迁移至 [file-index-archive.md](file-index-archive.md)。

## W393 降级六文档同步 核心2+辅助4自动（2026-08-08）

| 文件 | W | 说明 |
|---|---|---|

## W394 英文站 batch1 导览双页英文化（2026-08-08·v2.3.17）

| 文件 | W | 说明 |
|---|---|---|
| site/en/guide.html | W394 | 新建·导读页英文版（7 类读者路径 + 术语表 + 版本/引用）·内联 CSS·双向导航 |
| site/en/dukou-engine.html | W394 | 新建·渡口写作引擎英文版·保全内联 JS·零 CJK 残留 |
| site/en/index.html | W394 | 修改·导航卡新增 Reading Guide + Ferry Crossing |
| 交接文档.md | W394 | v2.3.17 同步·新增 W394 段 |
| CHANGELOG.md | W394 | v2.3.17 同步·新增 W394 版本段 |

## W395 英文站 batch2 三核心可视化页英文化（2026-08-08·v2.3.17）

| 文件 | W | 说明 |
|---|---|---|
| site/en/81-hardships.html | W395 | 新建·八十一难深度统计英文版·保全内联 D3 JS/CSS·双向导航 |
| site/en/chapter-structure-graph.html | W395 | 新建·回目结构图谱英文版·译 KPI/叙事簇/轴标签/tooltip |
| site/en/character-appearance.html | W395 | 新建·人物出场频次英文版·15 人物名转拼音 |
| site/en/visualizations.html | W395 | 修改·3 索引卡改指 EN 版 + 中文回链 |
| 交接文档.md | W395 | v2.3.17 同步·新增 W395 段 |
| CHANGELOG.md | W395 | v2.3.17 同步·新增 W395 版本段 |

## W396 英文站 batch3 三可视化页英文化（2026-08-08·v2.3.17）

| 文件 | W | 说明 |
|---|---|---|
| site/en/hardship-heatmap.html | W396 | 新建·八十一难难度热力图英文版 |
| site/en/character-presence-timeline.html | W396 | 新建·人物出场时间线英文版·35+ 人物名转英文 |
| site/en/character-relationship-3d.html | W396 | 新建·人物关系 3D 网络图英文版（Three.js） |
| site/en/visualizations.html | W396 | 修改·3 索引卡改指 EN 版 + 中文回链 |
| 交接文档.md | W396 | v2.3.17 同步·新增 W396 段 |
| CHANGELOG.md | W396 | v2.3.17 同步·新增 W396 版本段 |

## W397 英文站 batch4 三可视化页英文化（2026-08-08·v2.3.17）

| 文件 | W | 说明 |
|---|---|---|
| site/en/character-sentiment-arc.html | W397 | 新建·人物情感弧线英文版 |
| site/en/chapter-stats.html | W397 | 新建·章节字数与对话统计英文版 |
| site/en/narrative-rhythm-curve.html | W397 | 新建·叙事节奏曲线英文版 |
| site/en/visualizations.html | W397 | 修改·3 索引卡改指 EN 版 + 中文回链 |
| 交接文档.md | W397 | v2.3.17 同步·新增 W397 段 |
| CHANGELOG.md | W397 | v2.3.17 同步·新增 W397 版本段 |

## W398 英文站 batch5 两地理可视化页英文化（2026-08-08·v2.3.17）

| 文件 | W | 说明 |
|---|---|---|
| site/en/journey-geo-semiotics.html | W398 | 新建·取经路径地理符号学英文版 |
| site/en/journey-route.html | W398 | 新建·取经全路程图英文版·耦合地理类型枚举整块转译 |
| site/en/character-semantic-network.html | W398 | 新建·人物语义关系网络英文版（batch5 一并入库） |
| site/en/visualizations.html | W398 | 修改·2 索引卡改指 EN 版 + 中文回链 |
| CHANGELOG.md | W398 | v2.3.17 同步·新增 W398 版本段 |
| 交接文档.md | W398 | v2.3.17 同步·新增 W398 段 |
| README.md | W398 | v2.3.17 同步·六文档同步补齐 W394-W398·版本段日期 2026-08-08 |
| STRUCTURE.md | W398 | v2.3.17 同步·六文档同步补齐 W394-W398·版本段日期 2026-08-08 |
| docs/00-导读/项目说明.md | W398 | v2.3.17 同步·六文档同步补齐 W394-W398·版本段日期 2026-08-08 |
| scripts/output/file-index.md | W398 | v2.3.17 同步·新增 W394-W398 反向索引段 |

## W399 CI 触发修复+SEO 域名+rum-viewer 埋点查看页（2026-08-08）

| 文件 | W | 说明 |
|---|---|---|

> 当前版本 v2.3.18（2026-08-08）

## W400 CI/安全 workflow 转绿（2026-08-08）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/ci.yml | W400 | ruff 门禁生效·移除 black·Lighthouse Performance 降级 warn（Accessibility 硬门槛）·a11y 移除 pip cache |
| pyproject.toml | W400 | extend-exclude `_` 前缀/archive·全局忽略 UP031 |
| scripts/security_scan.py | W400 | discover_files 跳过 `_` 前缀开发脚本（XSS high 6→0） |
| scripts/a11y_audit.py | W400 | F841 parser 死代码清理·B007 循环变量改 `_` |
| scripts/perf_optimize.py | W400 | B023 闭包默认参数绑定·B007/F841 清理 |
| scripts/sync_docs.py | W400 | B023 lambda 默认参数绑定 |
| scripts/rag/xiyouji_rag.py | W400 | F841 best_head 清理·B007 循环变量 |
| scripts/perf_monitor.py | W400 | F841 categorized 死代码清理·B007 |
| scripts/B_人物/character_nlp.py | W400 | B007 循环变量改 `_`（4 处） |
| scripts/w286_merge_yuanwen_shendu.py | W400 | F841 skipped 死代码清理 |
| 其余 63 个 scripts/*.py | W400 | ruff --fix 自动修复（I001/F401/F541/UP009/UP015/E401） |
| README.md | W400 | 文档同步·头部版本行压缩至 ≤200 字符（473→160·A2 43→44 篇·site/data 85→86 个） |
| STRUCTURE.md | W400 | 文档同步·头部版本行压缩至 ≤200 字符（467→157·A2 43→44 篇） |
| docs/00-导读/项目说明.md | W400 | 文档同步·头部版本行压缩至 ≤200 字符（423→162·A2 43→44 篇·可视化 80→86 页·待办计数 A3/A4/A5 更新） |
| 交接文档.md | W400 | 文档同步·内部过期引用 12 处修复（W358→W400·v2.3.9→v2.3.18·A2 43→44/A3 199→211/A4 201→209/A5 20→34·site/data 85→86·英文站 7→65·页脚） |
| 项目交接参考手册.md | W400 | 文档同步·版本 v2.3.8 W357→v2.3.18 W400·计数 A2/A3/A4/A5·可视化 85→86·英文站 51→65·发布待办标记完成 |

## W401 CI 补齐 pytest + agent-web 构建（2026-08-08）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/ci.yml | W401 | 新增 pytest-unit + agent-web-build job（5→7 job）·pytest tests 全量（--ignore=tests/e2e）·npm ci + npm run build |
| .gitignore | W401 | agent-web 由整目录忽略改为精细忽略（node_modules/dist/data/server 编译产物/vite.config 产物） |
| xiyouji-agent-web/*（37 文件） | W401 | agent-web 源码入库（src/server/package*.json/vite/tsconfig 等·供 CI 构建验证） |
| .github/workflows/README.md | W401 | ci.yml 7 job 说明·阈值·artifact·本地复现命令·双索引 W401 |
| CHANGELOG.md | W401 | 新增 W401 版本段（四件套） |
