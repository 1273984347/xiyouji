# 全站可视化审计报告 (site/data/)

生成时间: 2026-08-06T10:09:47.522Z
页面数: 84

## 概览
- 有 error 级问题页面: 4
- 有 warn 级问题页面: 45
- 无问题页面: 35

## 问题分类统计
- label-overlap: 36
- clipping: 19

## 逐页明细（按严重度排序）

### 🔴 cave-estate.html
- 截图: _audit_shots/cave-estate.html.png  | svg:4 text:161 circle:0 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"table-wrap","sw":1145,"cw":1145,"sh":1197,"ch":638}]
  - [error] **label-overlap**: SVG 内 33 处文字相互压盖
    - 样例: [{"a":"0","b":"1","ratio":0.45},{"a":"1","b":"2","ratio":0.45},{"a":"2","b":"3","ratio":0.45},{"a":"3","b":"4","ratio":0.45},{"a":"4","b":"5","ratio":0.45},{"a":"5","b":"6","ratio":0.45},{"a":"6","b":"7","ratio":0.45},{"a":"7","b":"8","ratio":0.45}]

### 🔴 monster-female-network.html
- 截图: _audit_shots/monster-female-network.html.png  | svg:4 text:91 circle:99 canvas:1
  - [error] **label-overlap**: SVG 内 49 处文字相互压盖
    - 样例: [{"a":"蜘蛛精二姐","b":"蜘蛛精三姐","ratio":0.48},{"a":"蜘蛛精二姐","b":"蜘蛛精四姐","ratio":0.48},{"a":"蜘蛛精四姐","b":"蜘蛛精五姐","ratio":0.74},{"a":"蜘蛛精五姐","b":"蜘蛛精六姐","ratio":0.48},{"a":"蜘蛛精六姐","b":"蜘蛛精七妹","ratio":0.48},{"a":"第59回","b":"第60回","ratio":0.56},{"a":"第72回","b":"第72回","ratio":1},{"a":"第72回","b":"第72回","ratio":1}

### 🔴 narratology-12d-network.html
- 截图: _audit_shots/narratology-12d-network.html.png  | svg:4 text:98 circle:75 canvas:1
  - [error] **label-overlap**: SVG 内 34 处文字相互压盖
    - 样例: [{"a":"时","b":"空","ratio":0.7},{"a":"空","b":"听","ratio":0.57},{"a":"听","b":"嗅","ratio":0.63},{"a":"触","b":"视","ratio":0.66},{"a":"触","b":"2025-04","ratio":0.52},{"a":"视","b":"味","ratio":0.57},{"a":"视","b":"六感","ratio":0.65},{"a":"视","b":"2025-04","ratio":0.52}]

### 🔴 narratology-13d-network.html
- 截图: _audit_shots/narratology-13d-network.html.png  | svg:4 text:132 circle:106 canvas:1
  - [error] **label-overlap**: SVG 内 176 处文字相互压盖
    - 样例: [{"a":"W161","b":"W162","ratio":0.99},{"a":"W161","b":"W170","ratio":0.49},{"a":"W161","b":"W171","ratio":0.47},{"a":"W161","b":"W172","ratio":0.45},{"a":"W162","b":"W170","ratio":0.5},{"a":"W162","b":"W171","ratio":0.48},{"a":"W162","b":"W172","ratio":0.47},{"a":"W164","b":"W165","ratio":0.8}]

### 🟡 81-hardships.html
- 截图: _audit_shots/81-hardships.html.png  | svg:4 text:15 circle:0 canvas:0
  - [warn] **label-overlap**: SVG 内 3 处文字相互压盖
    - 样例: [{"a":"81","b":"总计","ratio":0.5},{"a":"81","b":"总计","ratio":0.5},{"a":"81","b":"总计","ratio":0.5}]

### 🟡 aesthetics.html
- 截图: _audit_shots/aesthetics.html.png  | svg:2 text:32 circle:19 canvas:0
  - [warn] **label-overlap**: SVG 内 1 处文字相互压盖
    - 样例: [{"a":"唐僧","b":"白龙马","ratio":1}]

### 🟡 century-dialogue.html
- 截图: _audit_shots/century-dialogue.html.png  | svg:0 text:0 circle:0 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"triangle-stage","sw":1085,"cw":1085,"sh":501,"ch":480}]

### 🟡 character-relationship-3d-view.html
- 截图: _audit_shots/character-relationship-3d-view.html.png  | svg:0 text:0 circle:0 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"vt-tablewrap","sw":1406,"cw":1406,"sh":902,"ch":538}]

### 🟡 chart-design.html
- 截图: _audit_shots/chart-design.html.png  | svg:8 text:129 circle:22 canvas:0
  - [warn] **label-overlap**: SVG 内 3 处文字相互压盖
    - 样例: [{"a":"💀","b":"S2","ratio":0.69},{"a":"👂","b":"S3","ratio":1},{"a":"🪭","b":"S4","ratio":0.58}]

### 🟡 criticism-history.html
- 截图: _audit_shots/criticism-history.html.png  | svg:4 text:55 circle:32 canvas:0
  - [warn] **label-overlap**: SVG 内 2 处文字相互压盖
    - 样例: [{"a":"道","b":"陈士斌 · 内丹金丹","ratio":0.83},{"a":"释·文","b":"现代学者 · 文学本位","ratio":0.68}]

### 🟡 cross-time-danmaku.html
- 截图: _audit_shots/cross-time-danmaku.html.png  | svg:1 text:4 circle:4 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"world-map","sw":1083,"cw":1083,"sh":396,"ch":358}]

### 🟡 cultural-misreading.html
- 截图: _audit_shots/cultural-misreading.html.png  | svg:3 text:121 circle:0 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"table-wrap","sw":1145,"cw":1145,"sh":1110,"ch":718}]
  - [warn] **label-overlap**: SVG 内 1 处文字相互压盖
    - 样例: [{"a":"12","b":"总作品数","ratio":0.52}]

### 🟡 deconstruction.html
- 截图: _audit_shots/deconstruction.html.png  | svg:3 text:117 circle:37 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"table-wrap","sw":1145,"cw":1145,"sh":1051,"ch":618}]
  - [warn] **label-overlap**: SVG 内 5 处文字相互压盖
    - 样例: [{"a":"颠覆 · 严肃","b":"10","ratio":0.44},{"a":"颠覆 · 娱乐","b":"1","ratio":0.76},{"a":"龙珠（鸟山明）","b":"花游记（韩国电视剧）","ratio":0.54},{"a":"魔法千字文（韩国漫画）","b":"美猴王传奇（美国改编）","ratio":0.49},{"a":"16","b":"部作品","ratio":0.5}]

### 🟡 dialogue-sentiment.html
- 截图: _audit_shots/dialogue-sentiment.html.png  | svg:6 text:146 circle:60 canvas:0
  - [warn] **label-overlap**: SVG 内 1 处文字相互压盖
    - 样例: [{"a":"90","b":"avg_sentiment","ratio":0.45}]

### 🟡 ecology.html
- 截图: _audit_shots/ecology.html.png  | svg:7 text:203 circle:39 canvas:0
  - [warn] **label-overlap**: SVG 内 2 处文字相互压盖
    - 样例: [{"a":"10/10","b":"如来佛祖","ratio":0.43},{"a":"平顶山·莲…","b":"青龙山·玄…","ratio":0.95}]

### 🟡 emotional-heatmap.html
- 截图: _audit_shots/emotional-heatmap.html.png  | svg:2 text:64 circle:160 canvas:0
  - [warn] **label-overlap**: SVG 内 18 处文字相互压盖
    - 样例: [{"a":"李卓吾","b":"1 · 石猴出世","ratio":0.6},{"a":"5 · 大圣偷丹","b":"7 · 八卦炉中逃大圣","ratio":0.77},{"a":"8 · 佛祖定计","b":"12 · 玄奘现身","ratio":0.44},{"a":"22 · 收沙僧","b":"24 · 五庄观人参果","ratio":0.75},{"a":"24 · 五庄观人参果","b":"27 · 三打白骨精","ratio":0.48},{"a":"27 · 三打白骨精","b":"32 · 莲花洞金角银角","ratio":0.7},{"a":"32 · 莲花洞金角银角

### 🟡 ethics-consumption.html
- 截图: _audit_shots/ethics-consumption.html.png  | svg:2 text:53 circle:6 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"ipo-card biggest","sw":1172,"cw":1143,"sh":997,"ch":997}]

### 🟡 four-dimensional-research-network.html
- 截图: _audit_shots/four-dimensional-research-network.html.png  | svg:5 text:159 circle:76 canvas:1
  - [warn] **label-overlap**: SVG 内 9 处文字相互压盖
    - 样例: [{"a":"第100回","b":"L98","ratio":0.42},{"a":"第100回","b":"L100","ratio":1},{"a":"7.5","b":"弗洛伊德","ratio":0.56},{"a":"10.0","b":"王阳明","ratio":0.68},{"a":"权力政治","b":"马基雅维利","ratio":0.41},{"a":"福柯","b":"马基雅维利","ratio":1},{"a":"海德格尔","b":"热奈特","ratio":0.56},{"a":"海德格尔","b":"里柯尔","ratio":0.86}]

### 🟡 game-webnovel.html
- 截图: _audit_shots/game-webnovel.html.png  | svg:5 text:114 circle:10 canvas:0
  - [warn] **label-overlap**: SVG 内 3 处文字相互压盖
    - 样例: [{"a":"金刚琢","b":"紧箍咒","ratio":1},{"a":"芭蕉扇（阳…","b":"阴阳二气瓶","ratio":0.61},{"a":"紫金红葫芦","b":"阴阳二气瓶","ratio":0.41}]

### 🟡 global-pattern.html
- 截图: _audit_shots/global-pattern.html.png  | svg:2 text:33 circle:8 canvas:0
  - [warn] **label-overlap**: SVG 内 1 处文字相互压盖
    - 样例: [{"a":"西游记","b":"格列佛游记","ratio":0.82}]

### 🟡 graph-explorer.html
- 截图: _audit_shots/graph-explorer.html.png  | svg:1 text:40 circle:20 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"ASIDE","cls":"side","sw":239,"cw":239,"sh":1207,"ch":842}]
  - [warn] **label-overlap**: SVG 内 5 处文字相互压盖
    - 样例: [{"a":"系缚","b":"熏习","ratio":1},{"a":"系缚","b":"现行","ratio":0.77},{"a":"解脱","b":"转依","ratio":0.59},{"a":"熏习","b":"现行","ratio":0.77},{"a":"现行","b":"声尘","ratio":0.52}]

### 🟡 guanyin-six-roles-network.html
- 截图: _audit_shots/guanyin-six-roles-network.html.png  | svg:5 text:104 circle:80 canvas:1
  - [warn] **label-overlap**: SVG 内 1 处文字相互压盖
    - 样例: [{"a":"立项请缨","b":"10","ratio":0.46}]

### 🟡 hardship-difficulty-heatmap.html
- 截图: _audit_shots/hardship-difficulty-heatmap.html.png  | svg:5 text:64 circle:0 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"heatmap-wrap","sw":1147,"cw":1147,"sh":480,"ch":460}]
  - [warn] **label-overlap**: SVG 内 1 处文字相互压盖
    - 样例: [{"a":"第80难","b":"第81难","ratio":0.67}]

### 🟡 hardship-heatmap.html
- 截图: _audit_shots/hardship-heatmap.html.png  | svg:3 text:49 circle:0 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"heatmap-wrap","sw":1147,"cw":1147,"sh":436,"ch":420}]

### 🟡 intertextuality-network.html
- 截图: _audit_shots/intertextuality-network.html.png  | svg:5 text:115 circle:55 canvas:1
  - [warn] **label-overlap**: SVG 内 3 处文字相互压盖
    - 样例: [{"a":"公元前6-公元4世纪","b":"公元前5-公元3世纪","ratio":0.53},{"a":"公元前6-公元4世纪","b":"公元前500","ratio":0.51},{"a":"地理借用","b":"人物转化","ratio":0.53}]

### 🟡 journey-geo-semiotics.html
- 截图: _audit_shots/journey-geo-semiotics.html.png  | svg:1 text:7 circle:7 canvas:1
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"graph-wrap","sw":1145,"cw":1145,"sh":593,"ch":573}]

### 🟡 journey-route.html
- 截图: _audit_shots/journey-route.html.png  | svg:2 text:25 circle:5 canvas:0
  - [warn] **label-overlap**: SVG 内 9 处文字相互压盖
    - 样例: [{"a":"第20回","b":"第20回","ratio":1},{"a":"第30回","b":"第30回","ratio":1},{"a":"第40回","b":"第40回","ratio":1},{"a":"第50回","b":"第50回","ratio":1},{"a":"第60回","b":"第60回","ratio":1},{"a":"第70回","b":"第70回","ratio":1},{"a":"第80回","b":"第80回","ratio":1},{"a":"第90回","b":"第90回","ratio":1}]

### 🟡 journey-spacetime.html
- 截图: _audit_shots/journey-spacetime.html.png  | svg:1 text:47 circle:68 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":640,"ch":620}]

### 🟡 jurisprudence.html
- 截图: _audit_shots/jurisprudence.html.png  | svg:6 text:128 circle:18 canvas:0
  - [warn] **label-overlap**: SVG 内 1 处文字相互压盖
    - 样例: [{"a":"Δ=1","b":"刑罚严重度","ratio":0.98}]

### 🟡 magic-system.html
- 截图: _audit_shots/magic-system.html.png  | svg:5 text:27 circle:0 canvas:0
  - [warn] **label-overlap**: SVG 内 2 处文字相互压盖
    - 样例: [{"a":"8","b":"件","ratio":0.5},{"a":"8","b":"件","ratio":0.5}]

### 🟡 material-archaeology.html
- 截图: _audit_shots/material-archaeology.html.png  | svg:8 text:155 circle:27 canvas:0
  - [warn] **label-overlap**: SVG 内 8 处文字相互压盖
    - 样例: [{"a":"金刚琢","b":"九齿钉耙","ratio":0.45},{"a":"金箍棒","b":"九齿钉耙","ratio":0.65},{"a":"1","b":"妖/兽","ratio":0.99},{"a":"3","b":"民/赘婿","ratio":0.99},{"a":"4","b":"僧徒","ratio":0.99},{"a":"6","b":"高僧","ratio":0.99},{"a":"8","b":"王/将","ratio":0.99},{"a":"10","b":"佛","ratio":0.86}]

### 🟡 mbti-evolution.html
- 截图: _audit_shots/mbti-evolution.html.png  | svg:7 text:151 circle:124 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"heatmap-wrap","sw":1147,"cw":1147,"sh":530,"ch":514}]

### 🟡 methodology-matrix.html
- 截图: _audit_shots/methodology-matrix.html.png  | svg:2 text:72 circle:27 canvas:0
  - [warn] **clipping**: 4 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"quadrant-card","sw":294,"cw":274,"sh":242,"ch":242},{"tag":"DIV","cls":"quadrant-card","sw":294,"cw":274,"sh":242,"ch":242},{"tag":"DIV","cls":"quadrant-card","sw":294,"cw":274,"sh":242,"ch":242},{"tag":"DIV","cls":"quadrant-card","sw":294,"cw":274,"sh":242,"ch":242}]

### 🟡 ming-political-thought-comparison.html
- 截图: _audit_shots/ming-political-thought-comparison.html.png  | svg:5 text:70 circle:50 canvas:0
  - [warn] **clipping**: 5 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":440,"ch":420},{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":400,"ch":380},{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":400,"ch":380},{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":440,"ch":420},{"tag":"DIV","c

### 🟡 monster-capability-radar.html
- 截图: _audit_shots/monster-capability-radar.html.png  | svg:4 text:91 circle:16 canvas:0
  - [warn] **clipping**: 3 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":580,"ch":560},{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":440,"ch":420},{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":500,"ch":480}]
  - [warn] **label-overlap**: SVG 内 9 处文字相互压盖
    - 样例: [{"a":"智谋","b":"10","ratio":0.46},{"a":"法宝","b":"10","ratio":0.46},{"a":"背景","b":"10","ratio":0.45},{"a":"结局","b":"10","ratio":0.43},{"a":"红孩儿","b":"青狮精","ratio":1},{"a":"黑熊精","b":"铁扇公主","ratio":1},{"a":"黑熊精","b":"白象精","ratio":1},{"a":"牛魔王","b":"黄眉大王","ratio":1}]

### 🟡 monster-ecology-network.html
- 截图: _audit_shots/monster-ecology-network.html.png  | svg:4 text:110 circle:52 canvas:1
  - [warn] **label-overlap**: SVG 内 2 处文字相互压盖
    - 样例: [{"a":"大妖顶级捕食者","b":"20%","ratio":0.47},{"a":"取经团队","b":"15%","ratio":0.47}]

### 🟡 monster-victims-network.html
- 截图: _audit_shots/monster-victims-network.html.png  | svg:4 text:51 circle:44 canvas:1
  - [warn] **label-overlap**: SVG 内 4 处文字相互压盖
    - 样例: [{"a":"金角银角案 (32-35回)","b":"第35回","ratio":0.72},{"a":"通天河案 (47-49回)","b":"第50回","ratio":0.41},{"a":"朱紫国案 (70-71回)","b":"第70回","ratio":0.72},{"a":"8","b":"9","ratio":1}]

### 🟡 music-structure.html
- 截图: _audit_shots/music-structure.html.png  | svg:3 text:93 circle:97 canvas:0
  - [warn] **clipping**: 1 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"climax-wrap","sw":1145,"cw":1145,"sh":1810,"ch":458}]

### 🟡 narrative-experiment.html
- 截图: _audit_shots/narrative-experiment.html.png  | svg:2 text:31 circle:17 canvas:0
  - [warn] **label-overlap**: SVG 内 1 处文字相互压盖
    - 样例: [{"a":"张卡牌","b":"12 (因果) × 10 (法器) × 10","ratio":0.51}]

### 🟡 philosophy.html
- 截图: _audit_shots/philosophy.html.png  | svg:4 text:105 circle:30 canvas:0
  - [warn] **label-overlap**: SVG 内 2 处文字相互压盖
    - 样例: [{"a":"0","b":"0","ratio":1},{"a":"10","b":"10","ratio":1}]

### 🟡 pilgrim-team-psychology-arc.html
- 截图: _audit_shots/pilgrim-team-psychology-arc.html.png  | svg:5 text:146 circle:123 canvas:0
  - [warn] **clipping**: 5 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":540,"ch":520},{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":520,"ch":500},{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":440,"ch":420},{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":340,"ch":320},{"tag":"DIV","c

### 🟡 poetry-rhythm-analysis.html
- 截图: _audit_shots/poetry-rhythm-analysis.html.png  | svg:5 text:98 circle:0 canvas:0
  - [warn] **clipping**: 4 个容器 overflow 裁切内容
    - 样例: [{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":440,"ch":420},{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":380,"ch":360},{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":400,"ch":380},{"tag":"DIV","cls":"chart-wrap","sw":1147,"cw":1147,"sh":460,"ch":440}]
  - [warn] **label-overlap**: SVG 内 6 处文字相互压盖
    - 样例: [{"a":"西江月","b":"临江仙","ratio":0.82},{"a":"西江月","b":"满庭芳","ratio":0.64},{"a":"西江月","b":"开篇诗","ratio":0.46},{"a":"临江仙","b":"满庭芳","ratio":0.81},{"a":"临江仙","b":"开篇诗","ratio":0.62},{"a":"满庭芳","b":"开篇诗","ratio":0.8}]

### 🟡 power-resources.html
- 截图: _audit_shots/power-resources.html.png  | svg:4 text:105 circle:10 canvas:0
  - [warn] **label-overlap**: SVG 内 4 处文字相互压盖
    - 样例: [{"a":"蟠桃（9000…","b":"唐僧肉","ratio":1},{"a":"人参果","b":"太乙真人莲藕化身","ratio":0.77},{"a":"太上老君仙丹","b":"九转金丹","ratio":1},{"a":"总资源","b":"10","ratio":0.49}]

### 🟡 relationships.html
- 截图: _audit_shots/relationships.html.png  | svg:8 text:255 circle:833 canvas:3
  - [warn] **label-overlap**: SVG 内 2 处文字相互压盖
    - 样例: [{"a":"10","b":"首领：玉皇大帝","ratio":0.64},{"a":"10","b":"首领：如来佛祖","ratio":0.64}]

### 🟡 risk-project.html
- 截图: _audit_shots/risk-project.html.png  | svg:5 text:110 circle:51 canvas:0
  - [warn] **label-overlap**: SVG 内 2 处文字相互压盖
    - 样例: [{"a":"#3","b":"#7","ratio":1},{"a":"#4","b":"#6","ratio":1}]

### 🟡 text-evolution.html
- 截图: _audit_shots/text-evolution.html.png  | svg:4 text:111 circle:20 canvas:0
  - [warn] **label-overlap**: SVG 内 15 处文字相互压盖
    - 样例: [{"a":"1600","b":"层4·明万历翻刻·简本","ratio":0.65},{"a":"元末·已佚  ·  已佚  ·  平话","b":"《西游记杂剧》","ratio":0.67},{"a":"已佚·仅见于《永乐大典》残卷'魏徵斩龙'与韩","b":"元末明初·杨景贤  ·  24回  ·  杂","ratio":1},{"a":"世德堂本《西游记》","b":"朱鼎臣本《唐三藏西游释厄传》","ratio":0.5},{"a":"明万历20年·1592  ·  100回  ","b":"朱鼎臣本《唐三藏西游释厄传》","ratio":0.82},{"a":"明万历20年·1

### 🟡 timeline.html
- 截图: _audit_shots/timeline.html.png  | svg:1 text:63 circle:22 canvas:0
  - [warn] **label-overlap**: SVG 内 17 处文字相互压盖
    - 样例: [{"a":"玄奘西行","b":"大唐西域记","ratio":0.88},{"a":"亚东排印本","b":"人文社整理本","ratio":0.68},{"a":"人文社整理本","b":"新校注本","ratio":0.87},{"a":"新校注本","b":"数字化版本","ratio":0.53},{"a":"1927","b":"1941","ratio":0.56},{"a":"连环画普及","b":"铁扇公主动画","ratio":0.93},{"a":"铁扇公主动画","b":"央视西游记","ratio":0.55},{"a":"铁扇公主动画","b":"大话西游","r

### 🟡 visual-art.html
- 截图: _audit_shots/visual-art.html.png  | svg:2 text:54 circle:20 canvas:0
  - [warn] **label-overlap**: SVG 内 2 处文字相互压盖
    - 样例: [{"a":"No.5","b":"取经路径（按章节顺序）→ 灵山","ratio":0.5},{"a":"No.6","b":"取经路径（按章节顺序）→ 灵山","ratio":0.5}]

### ✅ 81-hardships-view.html
_无自动检测到的问题_

### ✅ ai-dialogue.html
_无自动检测到的问题_

### ✅ business-model.html
_无自动检测到的问题_

### ✅ chapter-stats.html
_无自动检测到的问题_

### ✅ chapter-structure-graph.html
_无自动检测到的问题_

### ✅ character-appearance.html
_无自动检测到的问题_

### ✅ character-dynamic-network.html
_无自动检测到的问题_

### ✅ character-presence-timeline.html
_无自动检测到的问题_

### ✅ character-relationship-3d.html
_无自动检测到的问题_

### ✅ character-semantic-network.html
_无自动检测到的问题_

### ✅ character-sentiment-arc.html
_无自动检测到的问题_

### ✅ cognitive-psychology.html
_无自动检测到的问题_

### ✅ concept-device.html
_无自动检测到的问题_

### ✅ counterfactual.html
_无自动检测到的问题_

### ✅ data-explorer.html
_无自动检测到的问题_

### ✅ famous-time-travel.html
_无自动检测到的问题_

### ✅ four-heavenly-kings-artifacts.html
_无自动检测到的问题_

### ✅ heaven-power-network.html
_无自动检测到的问题_

### ✅ journey-map-interactive.html
_无自动检测到的问题_

### ✅ karma-reincarnation.html
_无自动检测到的问题_

### ✅ language-style-radar.html
_无自动检测到的问题_

### ✅ linguistics.html
_无自动检测到的问题_

### ✅ monster-background.html
_无自动检测到的问题_

### ✅ monster-hierarchy-network.html
_无自动检测到的问题_

### ✅ monster-sociology.html
_无自动检测到的问题_

### ✅ narrative-rhythm-curve.html
_无自动检测到的问题_

### ✅ perf-canvas-rendering.html
_无自动检测到的问题_

### ✅ pilgrim-team-dynamic-network.html
_无自动检测到的问题_

### ✅ search.html
_无自动检测到的问题_

### ✅ six-senses-narratology-network.html
_无自动检测到的问题_

### ✅ social-media.html
_无自动检测到的问题_

### ✅ tag-cloud.html
_无自动检测到的问题_

### ✅ text-search.html
_无自动检测到的问题_

### ✅ theological-intervention-network.html
_无自动检测到的问题_

### ✅ underworld-power-network.html
_无自动检测到的问题_

### ✅ workplace.html
_无自动检测到的问题_

