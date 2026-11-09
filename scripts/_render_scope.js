// scripts/_render_scope.js — W1192：渲染审计「采集面」口径单一来源
//
// 为什么单独成模块（口径两处实现 ⇒ 必然漂移）：
//   ① scripts/_audit_render_states.js —— CI 分片采集端：--scope charts = 全站含 <svg 的 .html 页
//   ② scripts/check_dark_state_gate.js —— 暗色门禁比对端：需要知道「本次采集本应覆盖哪些页」
//   端侧采集按「含 <svg」挑页、比对侧却拿全基线（charts + reader 两个面）做缺失/萎缩断言
//   ⇒ reader 面 621 页与已下线页被误判「基线页缺失」，门禁恒红 625 项（W1192 实证）。
//   两端共用本模块 ⇒ 采集面口径只有一处实现，缺失断言只在同面内成立。
//
// 口径定义（与 W579 建门禁时的机判口径一致·单点来源）：
//   charts 面 = site 根下以 .html 结尾、文件名不以 _ 开头、且**文件内容含 <svg** 的页面；
//   不含 . 开头目录与 node_modules；结果按页面相对路径升序。
//
// 用法：
//   const { listPages, chartsPages } = require('./_render_scope.js');
//   listPages(siteDir)    // 全部候选页
//   chartsPages(siteDir)  // charts 面页集合
const fs = require('fs');
const path = require('path');

/** site 根下的候选页集合（.html · 非 _ 前缀 · 跳过 . 目录与 node_modules）·按相对路径升序。 */
function listPages(siteDir) {
  const out = [];
  const walk = (d) => {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) {
        if (!e.name.startsWith('.') && e.name !== 'node_modules') walk(p);
      } else if (e.name.endsWith('.html') && !e.name.startsWith('_')) {
        out.push(path.relative(siteDir, p).split(path.sep).join('/'));
      }
    }
  };
  walk(siteDir);
  return out.sort();
}

/** charts 面页集合：候选页中**文件内容含 <svg** 者（缺文件按不含处理·读失败不抛）。 */
function chartsPages(siteDir) {
  return listPages(siteDir).filter((rel) => {
    try {
      return fs.readFileSync(path.join(siteDir, rel), 'utf8').includes('<svg');
    } catch (e) {
      return false;
    }
  });
}

module.exports = { listPages, chartsPages };
