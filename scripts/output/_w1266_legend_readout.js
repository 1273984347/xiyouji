() => {
  const cls = (el) => (el.getAttribute ? (el.getAttribute('class') || '') : '');
  const vis = (el) => {
    const st = getComputedStyle(el);
    if (st.display === 'none' || st.visibility === 'hidden') return false;
    if (parseFloat(st.opacity || '1') === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const MARK_SEL = 'rect,circle,ellipse,polyline,polygon,path,line';
  const ITEM_SEL = '[class*="legend-item"],[class*="legend-cell"],[class*="legend-label"],[class*="legend-swatch"],[class*="legend-key"],[class*="legend-entry"]';
  const ITEMRE = /legend-(item|cell|label|swatch|key|entry)/i;
  const svgs = [];
  for (const s of document.querySelectorAll('svg')) {
    if (!vis(s)) continue;
    const r = s.getBoundingClientRect();
    const w = Math.round(r.width), h = Math.round(r.height);
    let marks = 0;
    const fills = new Set(), strokes = new Set();
    const byX = new Map();
    for (const el of s.querySelectorAll(MARK_SEL)) {
      if (!vis(el)) continue;
      const b = el.getBoundingClientRect();
      const st = getComputedStyle(el);
      const f = st.fill || '', st2 = st.stroke || '';
      if (f === 'none' && st2 === 'none') continue;
      marks += 1;
      if (f !== 'none') fills.add(f);
      if (st2 !== 'none') strokes.add(st2);
      if (el.tagName === 'rect') {
        const k = Math.round(b.x);
        byX.set(k, (byX.get(k) || 0) + 1);
      }
    }
    let stackMax = 0;
    for (const v of byX.values()) { if (v > stackMax) stackMax = v; }
    let texts = 0;
    for (const t of s.querySelectorAll('text')) { if (vis(t) && (t.textContent || '').trim()) texts += 1; }
    svgs.push({cls: cls(s), id: s.getAttribute('id') || '', w: w, h: h, marks: marks,
               texts: texts, titles: s.querySelectorAll('title').length,
               fills: Array.from(fills).slice(0, 8), strokes: Array.from(strokes).slice(0, 8),
               stackMax: stackMax});
  }
  let legendItems = 0, vlegend = false;
  for (const c of document.querySelectorAll('[class*="legend"],[id*="legend"],[id*="Legend"]')) {
    if (ITEMRE.test(cls(c))) continue;
    const its = Array.from(c.querySelectorAll(ITEM_SEL)).filter(vis);
    if (!its.length) continue;
    if (vis(c)) { vlegend = true; legendItems += its.length; }
  }
  return {svgs: svgs, legendItems: legendItems, visibleLegend: vlegend};
}