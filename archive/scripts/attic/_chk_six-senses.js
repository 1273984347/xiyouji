
// ============================================================
// EMBEDDED DATA —— 六感叙事学数据（W168）
// ============================================================
const EMBEDDED_DATA = {
  sixSenses: {
    // 七感官主节点
    senses: [
      { id: "time", name: "时间叙事学", sense: "时间", color: "#8B4513", 专题: "W161", 理论家数: 4, 术语数: 28, 案例数: 5, 引用度: 85, 理论年代: "公元4世纪-20世纪" },
      { id: "space", name: "空间叙事学", sense: "空间", color: "#A0522D", 专题: "W162", 理论家数: 4, 术语数: 28, 案例数: 5, 引用度: 88, 理论年代: "1974-1996" },
      { id: "auditory", name: "听觉叙事学", sense: "听觉", color: "#CD853F", 专题: "W163", 理论家数: 4, 术语数: 28, 案例数: 5, 引用度: 82, 理论年代: "1972-1998" },
      { id: "olfactory", name: "嗅觉叙事学", sense: "嗅觉", color: "#DAA520", 专题: "W164", 理论家数: 4, 术语数: 28, 案例数: 5, 引用度: 78, 理论年代: "1798-2002" },
      { id: "tactile", name: "触觉叙事学", sense: "触觉", color: "#B8860B", 专题: "W165", 理论家数: 4, 术语数: 28, 案例数: 5, 引用度: 80, 理论年代: "1945-2008" },
      { id: "visual", name: "视觉叙事学", sense: "视觉", color: "#D2691E", 专题: "W166", 理论家数: 4, 术语数: 28, 案例数: 5, 引用度: 90, 理论年代: "1972-1994" },
      { id: "gustatory", name: "味觉叙事学", sense: "味觉", color: "#BC8F8F", 专题: "W167", 理论家数: 4, 术语数: 28, 案例数: 5, 引用度: 75, 理论年代: "1999-2012" }
    ],
    nodes: [
      // 7 个感官主节点
      { id: "time", name: "时间叙事学", sense: "时间", color: "#8B4513", 专题: "W161", 理论家数: 4, 术语数: 28, 案例数: 5 },
      { id: "space", name: "空间叙事学", sense: "空间", color: "#A0522D", 专题: "W162", 理论家数: 4, 术语数: 28, 案例数: 5 },
      { id: "auditory", name: "听觉叙事学", sense: "听觉", color: "#CD853F", 专题: "W163", 理论家数: 4, 术语数: 28, 案例数: 5 },
      { id: "olfactory", name: "嗅觉叙事学", sense: "嗅觉", color: "#DAA520", 专题: "W164", 理论家数: 4, 术语数: 28, 案例数: 5 },
      { id: "tactile", name: "触觉叙事学", sense: "触觉", color: "#B8860B", 专题: "W165", 理论家数: 4, 术语数: 28, 案例数: 5 },
      { id: "visual", name: "视觉叙事学", sense: "视觉", color: "#D2691E", 专题: "W166", 理论家数: 4, 术语数: 28, 案例数: 5 },
      { id: "gustatory", name: "味觉叙事学", sense: "味觉", color: "#BC8F8F", 专题: "W167", 理论家数: 4, 术语数: 28, 案例数: 5 },
      // 理论家节点（每个感官 4 个，共 28 个）
      // 时间叙事学理论家
      { id: "t1", name: "奥古斯丁", parent: "time", type: "theorist" },
      { id: "t2", name: "海德格尔", parent: "time", type: "theorist" },
      { id: "t3", name: "保罗·利科", parent: "time", type: "theorist" },
      { id: "t4", name: "巴赫金", parent: "time", type: "theorist" },
      // 空间叙事学理论家
      { id: "s1", name: "列斐伏尔", parent: "space", type: "theorist" },
      { id: "s2", name: "福柯", parent: "space", type: "theorist" },
      { id: "s3", name: "大卫·哈维", parent: "space", type: "theorist" },
      { id: "s4", name: "索雅", parent: "space", type: "theorist" },
      // 听觉叙事学理论家
      { id: "a1", name: "肖恩·洛克本", parent: "auditory", type: "theorist" },
      { id: "a2", name: "唐纳德·霍顿", parent: "auditory", type: "theorist" },
      { id: "a3", name: "罗兰·巴特", parent: "auditory", type: "theorist" },
      { id: "a4", name: "雷蒙德·默里·谢弗", parent: "auditory", type: "theorist" },
      // 嗅觉叙事学理论家
      { id: "o1", name: "康德", parent: "olfactory", type: "theorist" },
      { id: "o2", name: "大卫·豪斯", parent: "olfactory", type: "theorist" },
      { id: "o3", name: "吉姆·德罗布尼克", parent: "olfactory", type: "theorist" },
      { id: "o4", name: "雷切尔·赫尔兹", parent: "olfactory", type: "theorist" },
      // 触觉叙事学理论家
      { id: "ta1", name: "梅洛-庞蒂", parent: "tactile", type: "theorist" },
      { id: "ta2", name: "马塞尔·莫斯", parent: "tactile", type: "theorist" },
      { id: "ta3", name: "让-吕克·南希", parent: "tactile", type: "theorist" },
      { id: "ta4", name: "阿德里安·帕坦", parent: "tactile", type: "theorist" },
      // 视觉叙事学理论家
      { id: "v1", name: "约翰·伯格", parent: "visual", type: "theorist" },
      { id: "v2", name: "劳拉·穆尔维", parent: "visual", type: "theorist" },
      { id: "v3", name: "W.J.T.米歇尔", parent: "visual", type: "theorist" },
      { id: "v4", name: "马丁·杰伊", parent: "visual", type: "theorist" },
      // 味觉叙事学理论家
      { id: "g1", name: "卡罗尔·库恩卡斯", parent: "gustatory", type: "theorist" },
      { id: "g2", name: "巴里·史密斯", parent: "gustatory", type: "theorist" },
      { id: "g3", name: "戈登·谢泼德", parent: "gustatory", type: "theorist" },
      { id: "g4", name: "大卫·萨顿", parent: "gustatory", type: "theorist" }
    ],
    links: [
      // 感官内部连接（形成六感结构环）
      { source: "time", target: "space", type: "结构" },
      { source: "space", target: "auditory", type: "结构" },
      { source: "auditory", target: "olfactory", type: "结构" },
      { source: "olfactory", target: "tactile", type: "结构" },
      { source: "tactile", target: "visual", type: "结构" },
      { source: "visual", target: "gustatory", type: "结构" },
      // 感官到理论家连接（每个感官 4 个）
      { source: "time", target: "t1" }, { source: "time", target: "t2" }, { source: "time", target: "t3" }, { source: "time", target: "t4" },
      { source: "space", target: "s1" }, { source: "space", target: "s2" }, { source: "space", target: "s3" }, { source: "space", target: "s4" },
      { source: "auditory", target: "a1" }, { source: "auditory", target: "a2" }, { source: "auditory", target: "a3" }, { source: "auditory", target: "a4" },
      { source: "olfactory", target: "o1" }, { source: "olfactory", target: "o2" }, { source: "olfactory", target: "o3" }, { source: "olfactory", target: "o4" },
      { source: "tactile", target: "ta1" }, { source: "tactile", target: "ta2" }, { source: "tactile", target: "ta3" }, { source: "tactile", target: "ta4" },
      { source: "visual", target: "v1" }, { source: "visual", target: "v2" }, { source: "visual", target: "v3" }, { source: "visual", target: "v4" },
      { source: "gustatory", target: "g1" }, { source: "gustatory", target: "g2" }, { source: "gustatory", target: "g3" }, { source: "gustatory", target: "g4" }
    ],
    radar: [
      { sense: "时间", 术语数: 28, 案例数: 5, 理论家数: 4, 引用度: 85 },
      { sense: "空间", 术语数: 28, 案例数: 5, 理论家数: 4, 引用度: 88 },
      { sense: "听觉", 术语数: 28, 案例数: 5, 理论家数: 4, 引用度: 82 },
      { sense: "嗅觉", 术语数: 28, 案例数: 5, 理论家数: 4, 引用度: 78 },
      { sense: "触觉", 术语数: 28, 案例数: 5, 理论家数: 4, 引用度: 80 },
      { sense: "视觉", 术语数: 28, 案例数: 5, 理论家数: 4, 引用度: 90 },
      { sense: "味觉", 术语数: 28, 案例数: 5, 理论家数: 4, 引用度: 75 }
    ],
    sankey: [
      // 感官 → 四层结构
      { source: "时间", target: "循环结构", value: 4 },
      { source: "时间", target: "线性结构", value: 3 },
      { source: "时间", target: "永恒结构", value: 2 },
      { source: "时间", target: "瞬间结构", value: 2 },
      { source: "空间", target: "垂直结构", value: 4 },
      { source: "空间", target: "水平结构", value: 3 },
      { source: "空间", target: "封闭结构", value: 3 },
      { source: "空间", target: "开放结构", value: 2 },
      { source: "听觉", target: "天籁", value: 3 },
      { source: "听觉", target: "神谕", value: 3 },
      { source: "听觉", target: "人声", value: 3 },
      { source: "听觉", target: "妖音", value: 3 },
      { source: "嗅觉", target: "仙气", value: 3 },
      { source: "嗅觉", target: "妖风", value: 3 },
      { source: "嗅觉", target: "烟火", value: 3 },
      { source: "嗅觉", target: "药香", value: 3 },
      { source: "触觉", target: "金箍", value: 3 },
      { source: "触觉", target: "兵器", value: 3 },
      { source: "触觉", target: "肌肤", value: 3 },
      { source: "触觉", target: "法器", value: 3 },
      { source: "视觉", target: "法相", value: 3 },
      { source: "视觉", target: "幻象", value: 3 },
      { source: "视觉", target: "凝视", value: 3 },
      { source: "视觉", target: "显现", value: 3 },
      { source: "味觉", target: "仙丹", value: 3 },
      { source: "味觉", target: "人参果", value: 3 },
      { source: "味觉", target: "素斋", value: 3 },
      { source: "味觉", target: "妖食", value: 3 },
      // 四层结构 → 案例
      { source: "天籁", target: "花果山", value: 2 },
      { source: "神谕", target: "雷音寺", value: 2 },
      { source: "人声", target: "师徒对话", value: 2 },
      { source: "妖音", target: "妖怪呼啸", value: 2 },
      { source: "幻象", target: "白骨精三变", value: 2 },
      { source: "凝视", target: "女儿国", value: 2 },
      { source: "法相", target: "佛祖五指山", value: 2 },
      { source: "显现", target: "真经显现", value: 2 },
      { source: "仙丹", target: "蟠桃宴", value: 2 },
      { source: "人参果", target: "镇元大仙", value: 2 },
      { source: "素斋", target: "日常修行", value: 2 },
      { source: "妖食", target: "唐僧肉", value: 2 }
    ],
    timeline: [
      { 专题: "W161", 感官: "时间", 理论家: "奥古斯丁/海德格尔/利科/巴赫金", 创建: "2026-07-28", 理论年代: "公元4世纪-20世纪", 年代起点: 4, 年代终点: 1990 },
      { 专题: "W162", 感官: "空间", 理论家: "列斐伏尔/福柯/哈维/索雅", 创建: "2026-07-28", 理论年代: "1974-1996", 年代起点: 1974, 年代终点: 1996 },
      { 专题: "W163", 感官: "听觉", 理论家: "洛克本/霍顿/巴特/谢弗", 创建: "2026-07-28", 理论年代: "1972-1998", 年代起点: 1972, 年代终点: 1998 },
      { 专题: "W164", 感官: "嗅觉", 理论家: "康德/豪斯/德罗布尼克/赫尔兹", 创建: "2026-07-28", 理论年代: "1798-2007", 年代起点: 1798, 年代终点: 2007 },
      { 专题: "W165", 感官: "触觉", 理论家: "梅洛-庞蒂/莫斯/南希/帕坦", 创建: "2026-07-28", 理论年代: "1945-2008", 年代起点: 1945, 年代终点: 2008 },
      { 专题: "W166", 感官: "视觉", 理论家: "伯格/穆尔维/米歇尔/杰伊", 创建: "2026-07-28", 理论年代: "1972-1994", 年代起点: 1972, 年代终点: 1994 },
      { 专题: "W167", 感官: "味觉", 理论家: "库恩卡斯/史密斯/谢泼德/萨顿", 创建: "2026-07-28", 理论年代: "1999-2012", 年代起点: 1999, 年代终点: 2012 }
    ]
  }
};

// ============================================================
// F6 skeleton: fetchJson → loadData → main → renderXxx × N → cache → resize
// ============================================================
const fetchStatus = { anyFetched: false };

async function fetchJson(path, fallbackKey) {
  try {
    const response = await fetch(path);
    if (!response.ok) throw new Error('fetch failed: ' + path);
    fetchStatus.anyFetched = true;
    return await response.json();
  } catch (e) {
    console.warn('[W168] 使用嵌入数据 (' + fallbackKey + ')：', e.message);
    return EMBEDDED_DATA[fallbackKey];
  }
}

async function loadData() {
  const base = '../../scripts/output/data/';
  const sixSenses = await fetchJson(base + 'six-senses-narratology.json', 'sixSenses');
  const ss = sixSenses.sixSenses || sixSenses;
  return {
    senses: ss.senses || EMBEDDED_DATA.sixSenses.senses,
    network: ss.nodes ? { nodes: ss.nodes, links: ss.links } : { nodes: EMBEDDED_DATA.sixSenses.nodes, links: EMBEDDED_DATA.sixSenses.links },
    radar: ss.radar || EMBEDDED_DATA.sixSenses.radar,
    sankey: ss.sankey || EMBEDDED_DATA.sixSenses.sankey,
    timeline: ss.timeline || EMBEDDED_DATA.sixSenses.timeline
  };
}

// 感官配色查表
function senseColorMap(senses) {
  const m = {};
  (senses || EMBEDDED_DATA.sixSenses.senses).forEach(s => { m[s.sense] = s.color; m[s.id] = s.color; });
  return m;
}

// ============================================================
// Section 1: 概览卡片
// ============================================================
function renderOverview(senses) {
  const grid = d3.select('#senses-grid');
  grid.html('');
  if (!senses || senses.length === 0) {
    grid.append('div').attr('class', 'empty-state').text('暂无数据');
    return;
  }
  const card = grid.selectAll('.sense-card')
    .data(senses)
    .enter()
    .append('div')
    .attr('class', 'sense-card')
    .attr('role', 'button')
    .attr('tabindex', '0')
    .attr('aria-label', d => d.name + ' · ' + d.专题)
    .each(function(d) { d3.select(this).style('border-top', '4px solid ' + d.color); });

  card.append('div').attr('class', 'sense-name').text(d => d.sense);
  card.append('div').attr('class', 'swatch-bar').each(function(d) { d3.select(this).style('background', d.color); });
  card.append('div').attr('class', 'sense-tag').text(d => d.name + ' · ' + d.专题);
  card.append('div').attr('class', 'sense-stats').text(d => '术语 ' + d.术语数 + ' · 理论家 ' + d.理论家数 + ' · 案例 ' + d.案例数 + ' · 引用 ' + d.引用度);

  // 键盘 a11y
  card.on('keydown', function(e, d) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      showSenseTooltip(e, d);
    }
  });
  card.on('click', function(e, d) { showSenseTooltip(e, d); });
}

function showSenseTooltip(event, d) {
  let tip = d3.select('.tooltip');
  if (tip.empty()) {
    tip = d3.select('body').append('div').attr('class', 'tooltip');
  }
  tip.html('')
    .style('opacity', 0.95)
    .style('left', (event.pageX + 10) + 'px')
    .style('top', (event.pageY - 28) + 'px');
  tip.append('div').html('<strong>' + d.sense + ' · ' + d.name + '</strong>');
  tip.append('div').text('专题：' + d.专题);
  tip.append('div').text('术语数：' + d.术语数);
  tip.append('div').text('理论家数：' + d.理论家数);
  tip.append('div').text('案例数：' + d.案例数);
  tip.append('div').text('引用度：' + d.引用度);
  tip.append('div').text('理论年代：' + d.理论年代);
  setTimeout(() => tip.transition().duration(400).style('opacity', 0), 3000);
}

// ============================================================
// Section 2: 力导向图
// ============================================================
function renderForce(networkData) {
  const svg = d3.select('#chart-force');
  svg.selectAll('*').remove();
  if (!networkData || !networkData.nodes || networkData.nodes.length === 0) {
    svg.append('text').attr('x', 200).attr('y', 310).attr('fill', '#8a7a5a').text('暂无数据');
    return;
  }

  const width = +svg.node().clientWidth || 800;
  const height = 620;
  svg.attr('viewBox', `0 0 ${width} ${height}`);

  const senseColors = senseColorMap(EMBEDDED_DATA.sixSenses.senses);
  const senseNames = {};
  EMBEDDED_DATA.sixSenses.senses.forEach(s => { senseNames[s.id] = s.sense; });

  // 深拷贝节点避免 mutation
  const nodes = networkData.nodes.map(d => ({ ...d }));
  const links = networkData.links.map(d => ({ ...d }));

  function nodeRadius(d) {
    if (d.type === 'theorist') return 7;
    return 18; // 感官主节点
  }
  function nodeFill(d) {
    if (d.type === 'theorist') {
      const parent = nodes.find(n => n.id === d.parent);
      return parent ? parent.color : '#8a7a5a';
    }
    return d.color || '#8b4513';
  }

  const tooltip = d3.select('body').selectAll('.tooltip').empty()
    ? d3.select('body').append('div').attr('class', 'tooltip').style('opacity', 0)
    : d3.select('.tooltip');

  const sim = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id)
      .distance(d => d.type === '结构' ? 140 : 60)
      .strength(d => d.type === '结构' ? 0.25 : 0.5))
    .force('charge', d3.forceManyBody().strength(d => d.type === 'theorist' ? -120 : -520))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collide', d3.forceCollide().radius(d => nodeRadius(d) + 8))
    .alphaDecay(0.08).velocityDecay(0.5);  // 性能：更快收敛，减少无谓 tick

  // 结构链（感官间）
  const structLink = svg.append('g').selectAll('.struct-link')
    .data(links.filter(l => l.type === '结构'))
    .enter().append('line')
    .attr('class', 'struct-link')
    .attr('stroke', '#8b4513')
    .attr('stroke-width', 2)
    .attr('stroke-opacity', 0.5)
    .attr('stroke-dasharray', '6,3');

  // 理论家连接
  const theoristLink = svg.append('g').selectAll('.t-link')
    .data(links.filter(l => l.type !== '结构'))
    .enter().append('line')
    .attr('class', 't-link')
    .attr('stroke', '#d4c5a9')
    .attr('stroke-width', 1.2)
    .attr('stroke-opacity', 0.55);

  // 性能优化：节点 + 标签合并为 <g class="node">，用 transform 定位
  // （GPU 合成，避免逐帧对 cx/cy/x/y 四次属性写入并触发重排）
  const nodeG = svg.append('g').attr('class', 'nodes')
    .selectAll('g.node')
    .data(nodes)
    .enter().append('g')
    .attr('class', 'node');

  nodeG.append('circle')
    .attr('class', 'node-circle')
    .attr('r', nodeRadius)
    .attr('fill', nodeFill)
    .attr('stroke', '#fff')
    .attr('stroke-width', 2)
    .on('mouseover', function(e, d) {
      d3.select(this).attr('stroke', '#8b4513').attr('stroke-width', 3);
      tooltip.transition().duration(200).style('opacity', 0.95);
      tooltip.html('');
      if (d.type === 'theorist') {
        const parent = nodes.find(n => n.id === d.parent);
        const parentSense = parent ? parent.sense : '';
        tooltip.append('div').html('<strong>' + d.name + '</strong>');
        tooltip.append('div').text('类型：理论家');
        tooltip.append('div').text('归属：' + parentSense + '叙事学');
      } else {
        tooltip.append('div').html('<strong>' + d.sense + ' · ' + d.name + '</strong>');
        tooltip.append('div').text('专题：' + d.专题);
        tooltip.append('div').text('术语数：' + d.术语数);
        tooltip.append('div').text('理论家数：' + d.理论家数);
        tooltip.append('div').text('案例数：' + d.案例数);
      }
      const connected = links.filter(l =>
        (l.source.id || l.source) === d.id || (l.target.id || l.target) === d.id
      );
      tooltip.append('div').text('关联边数：' + connected.length);
    })
    .on('mousemove', function(e) {
      tooltip.style('left', (e.pageX + 12) + 'px').style('top', (e.pageY - 28) + 'px');
    })
    .on('mouseout', function() {
      d3.select(this).attr('stroke', '#fff').attr('stroke-width', 2);
      tooltip.transition().duration(400).style('opacity', 0);
    });

  nodeG.append('text')
    .attr('class', 'node-label')
    .attr('text-anchor', 'middle')
    .attr('dy', d => d.type === 'theorist' ? -14 : 4)
    .attr('font-weight', d => d.type === 'theorist' ? 400 : 700)
    .attr('font-size', d => d.type === 'theorist' ? 10 : 13)
    .attr('fill', d => d.type === 'theorist' ? '#5a3828' : '#1a1410')
    .text(d => d.type === 'theorist' ? d.name : d.sense);

  // 拖拽
  nodeG.call(d3.drag()
    .on('start', (e, d) => { if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; })
    .on('end', (e, d) => { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; })
  );

  sim.on('tick', () => {
    structLink.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
    theoristLink.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x).attr('y2', d.target.y);
    nodeG.attr('transform', d => `translate(${d.x},${d.y})`);
  });

  // 图例
  const legend = d3.select('#force-legend');
  legend.html('');
  const legendItems = [
    { label: '七感官主节点', color: '#8b4513' },
    { label: '感官结构链（虚线）', color: '#8b4513', dashed: true },
    { label: '理论家节点', color: '#d4c5a9' }
  ];
  legendItems.forEach(item => {
    const li = legend.append('div').attr('class', 'legend-item');
    li.append('div').attr('class', 'legend-swatch')
      .each(function() { d3.select(this).style('background', item.color).style('border', item.dashed ? '2px dashed #8b4513' : 'none'); });
    li.append('span').text(item.label);
  });
}

// ============================================================
// Section 3: 雷达图（7 感官 × 4 维度）
// ============================================================
function renderRadar(radarData) {
  const svg = d3.select('#chart-radar');
  svg.selectAll('*').remove();
  if (!radarData || radarData.length === 0) {
    svg.append('text').attr('x', 200).attr('y', 270).attr('fill', '#8a7a5a').text('暂无数据');
    return;
  }

  const width = +svg.node().clientWidth || 800;
  const height = 540;
  svg.attr('viewBox', `0 0 ${width} ${height}`);

  const dimensions = ['术语数', '案例数', '理论家数', '引用度'];
  const senseColors = senseColorMap(EMBEDDED_DATA.sixSenses.senses);

  // 归一化：每维度映射到 0-10
  const maxes = {};
  dimensions.forEach(dim => {
    maxes[dim] = d3.max(radarData, d => d[dim]) || 1;
  });

  const cx = width / 2;
  const cy = height / 2 + 10;
  const radius = Math.min(width, height) / 2 - 90;
  const levels = 5;

  const gBg = svg.append('g').attr('transform', `translate(${cx},${cy})`);

  // 背景同心多边形
  for (let lvl = 1; lvl <= levels; lvl++) {
    const r = radius * lvl / levels;
    const points = dimensions.map((dim, i) => {
      const angle = (i / dimensions.length) * 2 * Math.PI - Math.PI / 2;
      return [Math.cos(angle) * r, Math.sin(angle) * r];
    });
    gBg.append('polygon')
      .attr('points', points.map(p => p.join(',')).join(' '))
      .attr('fill', 'none')
      .attr('stroke', '#d4c5a9')
      .attr('stroke-width', 1)
      .attr('stroke-dasharray', lvl === levels ? '0' : '3,3');
  }

  // 轴线 + 标签
  dimensions.forEach((dim, i) => {
    const angle = (i / dimensions.length) * 2 * Math.PI - Math.PI / 2;
    gBg.append('line')
      .attr('x1', 0).attr('y1', 0)
      .attr('x2', Math.cos(angle) * radius)
      .attr('y2', Math.sin(angle) * radius)
      .attr('stroke', '#d4c5a9')
      .attr('stroke-width', 1);
    const labelR = radius + 28;
    gBg.append('text')
      .attr('x', Math.cos(angle) * labelR)
      .attr('y', Math.sin(angle) * labelR)
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('font-size', '13px')
      .attr('font-weight', '600')
      .attr('fill', '#1a1410')
      .text(dim);
  });

  // 数值刻度
  for (let lvl = 1; lvl <= levels; lvl++) {
    const r = radius * lvl / levels;
    gBg.append('text')
      .attr('x', -6).attr('y', -r)
      .attr('text-anchor', 'end')
      .attr('font-size', '10px')
      .attr('fill', '#8a7a5a')
      .text(lvl * 2);
  }

  const tooltip = d3.select('body').selectAll('.tooltip').empty()
    ? d3.select('body').append('div').attr('class', 'tooltip').style('opacity', 0)
    : d3.select('.tooltip');

  // 每个感官一个多边形
  radarData.forEach(role => {
    const points = dimensions.map((dim, i) => {
      const angle = (i / dimensions.length) * 2 * Math.PI - Math.PI / 2;
      // 归一化到 0-10 后映射半径
      const normalized = (role[dim] / maxes[dim]) * 10;
      const rr = radius * (normalized / 10);
      return [Math.cos(angle) * rr, Math.sin(angle) * rr];
    });
    const color = senseColors[role.sense] || '#8b4513';

    gBg.append('polygon')
      .attr('points', points.map(p => p.join(',')).join(' '))
      .attr('fill', color)
      .attr('fill-opacity', 0.12)
      .attr('stroke', color)
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .on('mouseover', function(e) {
        d3.select(this).attr('fill-opacity', 0.35);
        tooltip.transition().duration(200).style('opacity', 0.95);
        tooltip.html('');
        tooltip.append('div').html('<strong>' + role.sense + '叙事学</strong>');
        dimensions.forEach(dim => {
          tooltip.append('div').text(dim + '：' + role[dim]);
        });
      })
      .on('mousemove', function(e) {
        tooltip.style('left', (e.pageX + 12) + 'px').style('top', (e.pageY - 28) + 'px');
      })
      .on('mouseout', function() {
        d3.select(this).attr('fill-opacity', 0.12);
        tooltip.transition().duration(400).style('opacity', 0);
      });

    // 顶点圆
    points.forEach((p) => {
      gBg.append('circle')
        .attr('cx', p[0]).attr('cy', p[1])
        .attr('r', 3.5)
        .attr('fill', color)
        .attr('stroke', '#fff')
        .attr('stroke-width', 1);
    });
  });

  // 图例
  const legend = d3.select('#radar-legend');
  legend.html('');
  radarData.forEach(role => {
    const item = legend.append('div').attr('class', 'legend-item');
    item.append('div').attr('class', 'legend-swatch').each(function() { d3.select(this).style('background', senseColors[role.sense] || '#8b4513'); });
    item.append('span').text(role.sense);
  });
}

// ============================================================
// Section 4: 桑基图（感官 → 结构 → 案例）
// ============================================================
function buildSankeyGraph(linkData) {
  // 从 links 提取节点，分三层：感官(0) / 结构(1) / 案例(2)
  const senseNames = EMBEDDED_DATA.sixSenses.senses.map(s => s.sense);
  const nodeMap = new Map();
  // 判断每个节点层级：作为 source 但从不是 target → 感官；既是 target 又是 source → 结构；只是 target → 案例
  const sources = new Set(linkData.map(l => l.source));
  const targets = new Set(linkData.map(l => l.target));

  linkData.forEach(l => {
    if (!nodeMap.has(l.source)) {
      const cat = senseNames.includes(l.source) ? 0 : 1;
      nodeMap.set(l.source, { name: l.source, cat });
    }
    if (!nodeMap.has(l.target)) {
      const cat = sources.has(l.target) ? 1 : 2;
      nodeMap.set(l.target, { name: l.target, cat });
    }
  });
  return {
    nodes: Array.from(nodeMap.values()),
    links: linkData.map(l => ({ source: l.source, target: l.target, value: l.value }))
  };
}

function renderSankey(sankeyLinkData) {
  const svg = d3.select('#chart-sankey');
  svg.selectAll('*').remove();
  if (!sankeyLinkData || sankeyLinkData.length === 0) {
    svg.append('text').attr('x', 200).attr('y', 290).attr('fill', '#8a7a5a').text('暂无数据');
    return;
  }
  if (typeof d3.sankey === 'undefined') {
    svg.append('text').attr('x', 200).attr('y', 290).attr('fill', '#8b4513')
      .text('d3-sankey 未加载，请检查 ../static/js/d3-sankey.min.js');
    return;
  }

  const width = +svg.node().clientWidth || 800;
  const height = 580;
  svg.attr('viewBox', `0 0 ${width} ${height}`);

  const margin = { top: 20, right: 20, bottom: 20, left: 20 };

  const senseColors = senseColorMap(EMBEDDED_DATA.sixSenses.senses);
  const catColors = ['#8b4513', '#6b4226', '#8a7a5a'];

  const graphData = buildSankeyGraph(sankeyLinkData);
  // 深拷贝避免 mutation
  const nodes = graphData.nodes.map(d => ({ ...d }));
  const links = graphData.links.map(d => ({ ...d }));

  const sankeyGen = d3.sankey()
    .nodeId(d => d.name)
    .nodeWidth(16)
    .nodePadding(8)
    .extent([[margin.left, margin.top], [width - margin.right, height - margin.bottom]]);

  const graph = sankeyGen({ nodes, links });

  const tooltip = d3.select('body').selectAll('.tooltip').empty()
    ? d3.select('body').append('div').attr('class', 'tooltip').style('opacity', 0)
    : d3.select('.tooltip');

  // 链接
  svg.append('g').selectAll('path')
    .data(graph.links)
    .enter().append('path')
    .attr('d', d3.sankeyLinkHorizontal())
    .attr('fill', 'none')
    .attr('stroke', d => {
      if (d.source.cat === 0) return senseColors[d.source.name] || catColors[0];
      return catColors[d.source.cat] || '#8a7a5a';
    })
    .attr('stroke-width', d => Math.max(1, d.width))
    .attr('stroke-opacity', 0.4)
    .style('cursor', 'pointer')
    .on('mouseover', function(e, d) {
      d3.select(this).attr('stroke-opacity', 0.75);
      tooltip.transition().duration(200).style('opacity', 0.95);
      tooltip.html('');
      tooltip.append('div').html('<strong>' + d.source.name + ' → ' + d.target.name + '</strong>');
      tooltip.append('div').text('流量权重：' + d.value);
    })
    .on('mousemove', function(e) {
      tooltip.style('left', (e.pageX + 12) + 'px').style('top', (e.pageY - 28) + 'px');
    })
    .on('mouseout', function() {
      d3.select(this).attr('stroke-opacity', 0.4);
      tooltip.transition().duration(400).style('opacity', 0);
    });

  // 节点
  const node = svg.append('g').selectAll('g')
    .data(graph.nodes)
    .enter().append('g')
    .style('cursor', 'pointer');

  node.append('rect')
    .attr('x', d => d.x0)
    .attr('y', d => d.y0)
    .attr('width', d => Math.max(1, d.x1 - d.x0))
    .attr('height', d => Math.max(1, d.y1 - d.y0))
    .attr('fill', d => {
      if (d.cat === 0) return senseColors[d.name] || catColors[0];
      return catColors[d.cat] || '#8a7a5a';
    })
    .attr('stroke', '#fff')
    .attr('stroke-width', 1)
    .on('mouseover', function(e, d) {
      d3.select(this).attr('stroke', '#8b4513').attr('stroke-width', 2);
      tooltip.transition().duration(200).style('opacity', 0.95);
      tooltip.html('');
      tooltip.append('div').html('<strong>' + d.name + '</strong>');
      const catLabel = ['感官', '四层结构', '西游案例'][d.cat] || '';
      tooltip.append('div').text('层级：' + catLabel);
      tooltip.append('div').text('流入：' + (d.targetLinks || []).length + ' · 流出：' + (d.sourceLinks || []).length);
      tooltip.append('div').text('总流量：' + d.value);
    })
    .on('mousemove', function(e) {
      tooltip.style('left', (e.pageX + 12) + 'px').style('top', (e.pageY - 28) + 'px');
    })
    .on('mouseout', function() {
      d3.select(this).attr('stroke', '#fff').attr('stroke-width', 1);
      tooltip.transition().duration(400).style('opacity', 0);
    });

  // 节点标签
  node.append('text')
    .attr('x', d => d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6)
    .attr('y', d => (d.y0 + d.y1) / 2)
    .attr('dy', '0.35em')
    .attr('text-anchor', d => d.x0 < width / 2 ? 'start' : 'end')
    .attr('font-size', '11px')
    .attr('fill', '#1a1410')
    .text(d => d.name);

  // 图例
  const legend = d3.select('#sankey-legend');
  legend.html('');
  const layers = ['感官维度', '四层结构', '西游案例'];
  layers.forEach((layer, i) => {
    const item = legend.append('div').attr('class', 'legend-item');
    item.append('div').attr('class', 'legend-swatch').each(function() { d3.select(this).style('background', catColors[i]); });
    item.append('span').text(layer);
  });
}

// ============================================================
// Section 5: 时间线（W161-W167 + 理论家年代）
// ============================================================
function renderTimeline(timelineData) {
  const svg = d3.select('#chart-timeline');
  svg.selectAll('*').remove();
  if (!timelineData || timelineData.length === 0) {
    svg.append('text').attr('x', 200).attr('y', 230).attr('fill', '#8a7a5a').text('暂无数据');
    return;
  }

  const width = +svg.node().clientWidth || 800;
  const height = 460;
  svg.attr('viewBox', `0 0 ${width} ${height}`);

  const senseColors = senseColorMap(EMBEDDED_DATA.sixSenses.senses);
  const margin = { top: 50, right: 40, bottom: 90, left: 60 };
  const innerW = width - margin.left - margin.right;
  const innerH = height - margin.top - margin.bottom;

  const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);

  // X 轴：W161-W167 专题序（等距分布）
  const topics = timelineData.map((d, i) => ({ ...d, idx: i }));
  const xScale = d3.scaleLinear()
    .domain([0, topics.length - 1])
    .range([0, innerW]);

  // Y 轴：理论家年代跨度（用年代起点-终点做横向条带）
  const yearMin = d3.min(topics, d => d.年代起点);
  const yearMax = d3.max(topics, d => d.年代终点);
  const yScale = d3.scaleLinear()
    .domain([yearMin - 50, yearMax + 50])
    .range([innerH, 0]);

  const tooltip = d3.select('body').selectAll('.tooltip').empty()
    ? d3.select('body').append('div').attr('class', 'tooltip').style('opacity', 0)
    : d3.select('.tooltip');

  // 背景网格
  g.append('g')
    .attr('class', 'grid')
    .call(d3.axisLeft(yScale).tickSize(-innerW).tickFormat('').ticks(6))
    .selectAll('line').attr('stroke', '#d4c5a9').attr('stroke-dasharray', '3,3').attr('opacity', 0.4);
  g.select('.grid .domain').attr('stroke', 'none');

  // 理论家年代跨度条（垂直）
  topics.forEach(d => {
    const cx = xScale(d.idx);
    const y1 = yScale(d.年代起点);
    const y2 = yScale(d.年代终点);
    g.append('line')
      .attr('x1', cx).attr('y1', y1)
      .attr('x2', cx).attr('y2', y2)
      .attr('stroke', senseColors[d.感官] || '#8b4513')
      .attr('stroke-width', 8)
      .attr('stroke-opacity', 0.35)
      .attr('stroke-linecap', 'round');
  });

  // 主时间线（水平）
  g.append('line')
    .attr('x1', 0).attr('y1', innerH)
    .attr('x2', innerW).attr('y2', innerH)
    .attr('stroke', '#8b4513')
    .attr('stroke-width', 2);

  // 专题节点
  g.selectAll('.topic-node')
    .data(topics)
    .enter()
    .append('circle')
    .attr('class', 'topic-node')
    .attr('cx', d => xScale(d.idx))
    .attr('cy', innerH)
    .attr('r', 12)
    .attr('fill', d => senseColors[d.感官] || '#8b4513')
    .attr('stroke', '#fff')
    .attr('stroke-width', 2.5)
    .style('cursor', 'pointer')
    .on('mouseover', function(e, d) {
      d3.select(this).attr('r', 15);
      tooltip.transition().duration(200).style('opacity', 0.95);
      tooltip.html('');
      tooltip.append('div').html('<strong>' + d.专题 + ' · ' + d.感官 + '叙事学</strong>');
      tooltip.append('div').text('创建：' + d.创建);
      tooltip.append('div').text('理论家：' + d.理论家);
      tooltip.append('div').text('理论年代：' + d.理论年代);
    })
    .on('mousemove', function(e) {
      tooltip.style('left', (e.pageX + 12) + 'px').style('top', (e.pageY - 28) + 'px');
    })
    .on('mouseout', function() {
      d3.select(this).attr('r', 12);
      tooltip.transition().duration(400).style('opacity', 0);
    });

  // 专题标签（X 轴下方）
  g.selectAll('.topic-label')
    .data(topics)
    .enter()
    .append('text')
    .attr('class', 'topic-label')
    .attr('x', d => xScale(d.idx))
    .attr('y', innerH + 24)
    .attr('text-anchor', 'middle')
    .attr('font-size', '11px')
    .attr('font-weight', '600')
    .attr('fill', d => senseColors[d.感官] || '#8b4513')
    .text(d => d.专题);

  // 感官标签（X 轴下方第二行）
  g.selectAll('.sense-label')
    .data(topics)
    .enter()
    .append('text')
    .attr('class', 'sense-label')
    .attr('x', d => xScale(d.idx))
    .attr('y', innerH + 40)
    .attr('text-anchor', 'middle')
    .attr('font-size', '10px')
    .attr('fill', '#5a3828')
    .text(d => d.感官);

  // 理论年代标注（顶部）
  g.selectAll('.era-label')
    .data(topics)
    .enter()
    .append('text')
    .attr('class', 'era-label')
    .attr('x', d => xScale(d.idx))
    .attr('y', d => yScale(d.年代终点) - 8)
    .attr('text-anchor', 'middle')
    .attr('font-size', '9px')
    .attr('fill', '#8a7a5a')
    .text(d => d.理论年代);

  // Y 轴
  g.append('g')
    .call(d3.axisLeft(yScale).ticks(6).tickFormat(d => d + '年'))
    .selectAll('text').attr('font-size', '10px');

  // 轴标题
  g.append('text')
    .attr('x', innerW / 2).attr('y', innerH + 65)
    .attr('text-anchor', 'middle')
    .attr('font-size', '12px')
    .attr('fill', '#8a7a5a')
    .text('专题序（W161-W167）');
  g.append('text')
    .attr('transform', 'rotate(-90)')
    .attr('x', -innerH / 2).attr('y', -45)
    .attr('text-anchor', 'middle')
    .attr('font-size', '12px')
    .attr('fill', '#8a7a5a')
    .text('理论家活跃年代');

  // 图例
  const legend = d3.select('#timeline-legend');
  legend.html('');
  EMBEDDED_DATA.sixSenses.senses.forEach(s => {
    const item = legend.append('div').attr('class', 'legend-item');
    item.append('div').attr('class', 'legend-swatch').each(function() { d3.select(this).style('background', s.color); });
    item.append('span').text(s.专题 + ' ' + s.sense);
  });
}

// ============================================================
// Section 6: 汇总表 + 理论家清单
// ============================================================
function renderSummary(senses, networkData) {
  const wrap = d3.select('#summary-table-wrap');
  wrap.html('');
  if (!senses || senses.length === 0) {
    wrap.append('div').attr('class', 'empty-state').text('暂无数据');
    return;
  }

  // 汇总表
  const table = wrap.append('table').attr('class', 'summary-table');
  const thead = table.append('thead').append('tr');
  ['感官', '专题', '理论家数', '术语数', '案例数', '引用度', '理论年代'].forEach(h => {
    thead.append('th').text(h);
  });
  const tbody = table.append('tbody');
  const rows = tbody.selectAll('tr')
    .data(senses)
    .enter()
    .append('tr')
    .attr('role', 'row')
    .attr('tabindex', '0');

  rows.each(function(d) {
    const tr = d3.select(this);
    const td1 = tr.append('td');
    td1.append('span').attr('class', 'sense-dot').each(function() { d3.select(this).style('background', d.color); });
    td1.append('span').text(d.sense + '叙事学');
    tr.append('td').text(d.专题);
    tr.append('td').text(d.理论家数);
    tr.append('td').text(d.术语数);
    tr.append('td').text(d.案例数);
    tr.append('td').text(d.引用度);
    tr.append('td').text(d.理论年代);
  });

  // 理论家清单
  const theoristList = d3.select('#theorist-list');
  theoristList.html('');
  const theorists = (networkData.nodes || []).filter(n => n.type === 'theorist');
  if (theorists.length === 0) {
    theoristList.append('div').attr('class', 'empty-state').text('暂无理论家数据');
    return;
  }
  const senseColors = senseColorMap(senses);
  const items = theoristList.selectAll('.theorist-item')
    .data(theorists)
    .enter()
    .append('div')
    .attr('class', 'theorist-item')
    .each(function(d) {
      const parent = (networkData.nodes || []).find(n => n.id === d.parent);
      const senseName = parent ? parent.sense : '';
      const color = parent ? parent.color : '#d4c5a9';
      d3.select(this).style('border-left-color', color);
      d3.select(this).append('div').attr('class', 't-name').text(d.name);
      d3.select(this).append('div').attr('class', 't-sense').text(senseName + '叙事学');
    });
}

// ============================================================
// main：调度所有渲染函数
// ============================================================
async function main() {
  const data = await loadData();
  window.__lastData = data;

  if (fetchStatus.anyFetched) {
    document.getElementById('dataSource').innerHTML =
      '数据源：实时加载自 <code>scripts/output/data/</code>（http server 模式）';
  }

  renderOverview(data.senses);
  renderForce(data.network);
  renderRadar(data.radar);
  renderSankey(data.sankey);
  renderTimeline(data.timeline);
  renderSummary(data.senses, data.network);
}

// 响应式重绘（debounce 250ms）
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    if (window.__lastData) {
      const data = window.__lastData;
      renderOverview(data.senses);
      renderForce(data.network);
      renderRadar(data.radar);
      renderSankey(data.sankey);
      renderTimeline(data.timeline);
      renderSummary(data.senses, data.network);
    }
  }, 250);
});

// 启动
main();
