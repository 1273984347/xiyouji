/*!
 * dataset-view.js — 《详解西游记》单数据集可交互视图（零依赖·原生 JS）
 *
 * 把 data-explorer.html 的渲染逻辑抽成可复用模块，证明 vis-tools 范式
 * 可逐项实例化：给定数据集名 + 离线 fallback，即可渲染
 *   「键 tab → 数组表(可筛选/排序/导出/钻取) / 对象柱状图」两类视图。
 *
 * 用法（页面中）：
 *   <script src="../static/js/vis-tools.js"></script>
 *   <script src="../static/js/dataset-view.js"></script>
 *   <script>
 *     DatasetView.mount({
 *       name: "character-relationship-3d",
 *       fallback: window.CHAR_FB,            // file:// 下的离线示例
 *       bannerId: "banner", metaId: "meta",
 *       keytabsId: "keytabs", chartTitleId: "chartTitle",
 *       chartHostId: "chartHost", tableHostId: "tableHost"
 *     });
 *   </script>
 *
 * file:// 下 fetch 失败自动走 fallback；http(s) 下同源命中数据 API。
 */
(function (global) {
  "use strict";

  function apiFetch(path) {
    return fetch(path, { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    });
  }

  function setBanner(id, html, offline) {
    var b = document.getElementById(id);
    if (!b) return;
    b.innerHTML = html;
    b.className = "banner" + (offline ? " offline" : "");
  }

  function pickColumns(rows) {
    var cols = [];
    rows.slice(0, 50).forEach(function (r) {
      Object.keys(r).forEach(function (k) { if (cols.indexOf(k) < 0) cols.push(k); });
    });
    return cols.slice(0, 7).map(function (k) { return { key: k, label: k }; });
  }

  function openRowDrill(key, row) {
    var html = "<p><b>所属键：</b>" + key + "</p><table><tbody>";
    Object.keys(row).forEach(function (k) {
      var v = row[k];
      if (v && typeof v === "object") v = JSON.stringify(v);
      html += "<tr><th>" + k + "</th><td>" + String(v) + "</td></tr>";
    });
    html += "</tbody></table>";
    global.VisTools.openDrill((row.name || row.label || key), html);
  }

  function renderArrayTable(key, rows, tableHostId) {
    global.VisTools.makeFilterableTable({
      container: "#" + tableHostId,
      columns: pickColumns(rows),
      rows: rows,
      searchKeys: pickColumns(rows).map(function (c) { return c.key; }),
      onRowClick: function (row) { openRowDrill(key, row); }
    });
  }

  function renderObjectView(key, obj, ids) {
    var entries = Object.keys(obj).map(function (k) { return { label: k, value: obj[k] }; });
    var max = Math.max.apply(null, entries.map(function (e) { return +e.value || 0; })) || 1;
    var colors = ["#c8463a", "#3a6b8c", "#C9A063", "#6B8E5A", "#8c2a2a", "#b07a3a"];
    var svg = '<svg id="chart" viewBox="0 0 520 ' + (entries.length * 34 + 10) + '" width="100%" style="max-width:560px">';
    entries.forEach(function (e, i) {
      var w = Math.round(((+e.value || 0) / max) * 360);
      svg += '<text x="0" y="' + (i * 34 + 18) + '" font-size="12" fill="#23201A">' + e.label + "</text>";
      svg += '<rect x="120" y="' + (i * 34 + 6) + '" width="' + w + '" height="18" rx="3" fill="' + colors[i % colors.length] + '"/>';
      svg += '<text x="' + (124 + w) + '" y="' + (i * 34 + 19) + '" font-size="11" fill="#6B6455">' + e.value + "</text>";
    });
    svg += "</svg>";
    document.getElementById(ids.chartTitleId).textContent = "分布：" + key;
    document.getElementById(ids.chartHostId).innerHTML = svg;
    document.getElementById(ids.chartHostId).parentNode.style.display = "block";
    global.VisTools.makeFilterableTable({
      container: "#" + ids.tableHostId,
      columns: [{ key: "label", label: "项" }, { key: "value", label: "值" }],
      rows: entries,
      onRowClick: function (row) { openRowDrill(key, row); }
    });
  }

  function renderKey(key, value, ids) {
    document.getElementById(ids.chartHostId).parentNode.style.display = "none";
    var host = document.getElementById(ids.tableHostId);
    if (Array.isArray(value) && value.length && typeof value[0] === "object") {
      renderArrayTable(key, value, ids.tableHostId);
    } else if (value && typeof value === "object") {
      renderObjectView(key, value, ids);
    } else if (Array.isArray(value)) {
      renderArrayTable(key, value.map(function (v, i) { return { "#": i + 1, value: v }; }), ids.tableHostId);
    } else {
      host.innerHTML = "<p class='meta'>" + key + "：<b>" + String(value) + "</b></p>";
    }
  }

  function renderKeyTabs(data, ids) {
    var tabs = document.getElementById(ids.keytabsId);
    tabs.innerHTML = "";
    var keys = Object.keys(data).filter(function (k) { return k !== "meta"; });
    if (!keys.length) { document.getElementById(ids.tableHostId).textContent = "（无表格数据）"; return; }
    function choose(k) {
      document.querySelectorAll("#" + ids.keytabsId + " .keytab").forEach(function (n) { n.classList.remove("active"); });
      Array.prototype.slice.call(tabs.children).find(function (c) { return c.dataset.k === k; }).classList.add("active");
      renderKey(k, data[k], ids);
    }
    keys.forEach(function (k) {
      var t = document.createElement("span");
      t.className = "keytab"; t.dataset.k = k; t.textContent = k;
      t.addEventListener("click", function () { choose(k); });
      tabs.appendChild(t);
    });
    choose(keys[0]);
  }

  var DatasetView = {
    mount: function (opts) {
      var ids = {
        bannerId: opts.bannerId, metaId: opts.metaId, keytabsId: opts.keytabsId,
        chartTitleId: opts.chartTitleId, chartHostId: opts.chartHostId, tableHostId: opts.tableHostId
      };
      var name = opts.name, fallback = opts.fallback || null;
      var online = false;

      function show(data) {
        if (!data) { document.getElementById(ids.metaId).textContent = "（该数据集需启动 API 才能获取）"; return; }
        var title = (data.meta && data.meta.title) || name;
        document.getElementById(ids.metaId).textContent =
          "数据集：" + name + (data.meta && data.meta.note ? " · " + data.meta.note : "");
        renderKeyTabs(data, ids);
      }

      apiFetch("/dataset/" + name).then(function (data) {
        online = true;
        setBanner(ids.bannerId, "已连接数据 API · 数据集 " + name + " 已加载。", false);
        show(data);
      }).catch(function () {
        if (fallback) {
          setBanner(ids.bannerId, "离线模式（file://）：展示内置示例。启动 <code>python scripts/api/api_server.py</code> 后通过 http://127.0.0.1:8787/data/" + name + "-view.html 访问可得完整数据。", true);
          show(fallback);
        } else {
          setBanner(ids.bannerId, "离线且无内置示例：请启动数据 API 后通过 http 访问。", true);
        }
      });
    }
  };

  global.DatasetView = DatasetView;
})(window);
