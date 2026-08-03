/*!
 * vis-tools.js — 《详解西游记》可视化交互增强工具库（零依赖·原生 JS）
 *
 * 提供「筛选 / 钻取 / 导出」三类可复用能力，供 site/data/*.html 调用：
 *   - exportCSV(rows, filename)        表格对象数组 → CSV（带 BOM，Excel 不乱码）
 *   - exportJSON(obj, filename)        任意对象 → .json 下载
 *   - exportSVG(svgEl, filename)       SVG 元素 → PNG（序列化后绘到 canvas）
 *   - makeFilterableTable(opts)        渲染带搜索框的可排序表格，返回控制句柄
 *   - openDrill(title, html) / closeDrill()   右侧滑入式钻取详情面板
 *
 * 不依赖任何框架；file:// 下亦可工作（导出用 Blob + a[download]，无需服务器）。
 * 设计语言沿用 tokens.css：朱砂 #c8463a / 靛青 #3a6b8c / 宣纸 #faf7f2。
 */
(function (global) {
  "use strict";

  function downloadBlob(blob, filename) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function csvCell(v) {
    if (v === null || v === undefined) v = "";
    v = String(v);
    if (/[",\n]/.test(v)) v = '"' + v.replace(/"/g, '""') + '"';
    return v;
  }

  function exportCSV(rows, filename) {
    if (!rows || !rows.length) { alert("没有可导出的数据"); return; }
    var cols = [];
    rows.forEach(function (r) {
      Object.keys(r).forEach(function (k) { if (cols.indexOf(k) < 0) cols.push(k); });
    });
    var lines = [cols.join(",")];
    rows.forEach(function (r) {
      lines.push(cols.map(function (k) { return csvCell(r[k]); }).join(","));
    });
    // BOM 让 Excel 正确识别 UTF-8
    var blob = new Blob(["\uFEFF" + lines.join("\n")], { type: "text/csv;charset=utf-8" });
    downloadBlob(blob, filename || "export.csv");
  }

  function exportJSON(obj, filename) {
    var blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json;charset=utf-8" });
    downloadBlob(blob, filename || "export.json");
  }

  function exportSVG(svgEl, filename) {
    if (!svgEl) { alert("没有可导出的图表"); return; }
    var clone = svgEl.cloneNode(true);
    clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    var xml = new XMLSerializer().serializeToString(clone);
    var svgBlob = new Blob([xml], { type: "image/svg+xml;charset=utf-8" });
    var url = URL.createObjectURL(svgBlob);
    var img = new Image();
    img.onload = function () {
      var vb = (svgEl.getAttribute("viewBox") || "0 0 600 400").split(/\s+/).map(Number);
      var w = vb[2] || svgEl.clientWidth || 600;
      var h = vb[3] || svgEl.clientHeight || 400;
      var scale = 2;
      var canvas = document.createElement("canvas");
      canvas.width = w * scale; canvas.height = h * scale;
      var ctx = canvas.getContext("2d");
      ctx.fillStyle = "#faf7f2";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.scale(scale, scale);
      ctx.drawImage(img, 0, 0);
      URL.revokeObjectURL(url);
      canvas.toBlob(function (b) { downloadBlob(b, filename || "chart.png"); });
    };
    img.onerror = function () { URL.revokeObjectURL(url); alert("SVG 导出失败（可能含跨域字体）"); };
    img.src = url;
  }

  // ---- 可筛选可排序表格 ----
  // opts: { container, columns:[{key,label,sortable}], rows:[{}], searchKeys:[], onRowClick(row) }
  function makeFilterableTable(opts) {
    var container = typeof opts.container === "string"
      ? document.querySelector(opts.container) : opts.container;
    var columns = opts.columns || [];
    var rows = opts.rows || [];
    var searchKeys = opts.searchKeys || columns.map(function (c) { return c.key; });
    var onRowClick = opts.onRowClick || null;
    var sortKey = null, sortDir = 1;

    container.innerHTML = "";
    var toolbar = document.createElement("div");
    toolbar.className = "vt-toolbar";
    toolbar.innerHTML =
      '<input class="vt-search" type="search" placeholder="筛选 / 搜索…" aria-label="筛选表格">' +
      '<span class="vt-count"></span>' +
      '<button class="vt-btn" data-act="csv">导出 CSV</button>' +
      '<button class="vt-btn" data-act="json">导出 JSON</button>';
    container.appendChild(toolbar);

    var tableWrap = document.createElement("div");
    tableWrap.className = "vt-tablewrap";
    container.appendChild(tableWrap);

    function current() { return rows.slice(); }

    function render() {
      var q = (toolbar.querySelector(".vt-search").value || "").trim().toLowerCase();
      var data = current();
      if (q) {
        data = data.filter(function (r) {
          return searchKeys.some(function (k) {
            return String(r[k] === undefined ? "" : r[k]).toLowerCase().indexOf(q) >= 0;
          });
        });
      }
      if (sortKey) {
        data.sort(function (a, b) {
          var x = a[sortKey], y = b[sortKey];
          if (typeof x === "number" && typeof y === "number") return (x - y) * sortDir;
          return String(x).localeCompare(String(y), "zh") * sortDir;
        });
      }
      var html = "<table class=\"vt-table\"><thead><tr>";
      columns.forEach(function (c) {
        var arrow = sortKey === c.key ? (sortDir > 0 ? " ▲" : " ▼") : "";
        html += '<th data-key="' + c.key + '"' + (c.sortable === false ? "" : " class=\"vt-sortable\"") +
          ">" + (c.label || c.key) + arrow + "</th>";
      });
      html += "</tr></thead><tbody>";
      if (!data.length) {
        html += "<tr><td class=\"vt-empty\" colspan=\"" + columns.length + "\">无匹配数据</td></tr>";
      } else {
        data.forEach(function (r, i) {
          html += "<tr data-i=\"" + i + "\">";
          columns.forEach(function (c) { html += "<td>" + escapeHtml(r[c.key]) + "</td>"; });
          html += "</tr>";
        });
      }
      html += "</tbody></table>";
      tableWrap.innerHTML = html;
      toolbar.querySelector(".vt-count").textContent = "共 " + data.length + " 行";
      tableWrap._data = data;
    }

    toolbar.querySelector(".vt-search").addEventListener("input", render);
    toolbar.querySelector('[data-act="csv"]').addEventListener("click", function () {
      exportCSV(tableWrap._data || [], "xiyouji-export.csv");
    });
    toolbar.querySelector('[data-act="json"]').addEventListener("click", function () {
      exportJSON(tableWrap._data || [], "xiyouji-export.json");
    });
    tableWrap.addEventListener("click", function (e) {
      var th = e.target.closest("th.vt-sortable");
      if (th) {
        var k = th.getAttribute("data-key");
        if (sortKey === k) sortDir = -sortDir; else { sortKey = k; sortDir = 1; }
        render(); return;
      }
      var tr = e.target.closest("tr[data-i]");
      if (tr && onRowClick) {
        var i = +tr.getAttribute("data-i");
        onRowClick((tableWrap._data || [])[i], i);
      }
    });

    function setData(newRows) { rows = newRows || []; render(); }
    function setRows(newRows) { rows = newRows || []; render(); }
    render();
    return { render: render, setData: setData, setRows: setRows, getData: function () { return tableWrap._data || []; } };
  }

  function escapeHtml(s) {
    return String(s === undefined ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // ---- 钻取详情面板（右侧滑入） ----
  function ensureDrillRoot() {
    var root = document.getElementById("vt-drill");
    if (!root) {
      root = document.createElement("div");
      root.id = "vt-drill";
      root.className = "vt-drill";
      root.innerHTML = "<div class=\"vt-drill-mask\"></div>" +
        "<aside class=\"vt-drill-panel\" role=\"dialog\" aria-modal=\"true\">" +
        "<header><span class=\"vt-drill-title\"></span>" +
        "<button class=\"vt-drill-close\" aria-label=\"关闭\">×</button></header>" +
        "<div class=\"vt-drill-body\"></div></aside>";
      document.body.appendChild(root);
      root.querySelector(".vt-drill-mask").addEventListener("click", closeDrill);
      root.querySelector(".vt-drill-close").addEventListener("click", closeDrill);
    }
    return root;
  }

  function openDrill(title, html) {
    var root = ensureDrillRoot();
    root.querySelector(".vt-drill-title").textContent = title || "";
    root.querySelector(".vt-drill-body").innerHTML = html || "";
    root.classList.add("open");
  }
  function closeDrill() {
    var root = document.getElementById("vt-drill");
    if (root) root.classList.remove("open");
  }

  // ---- 样式注入（仅一次） ----
  if (!document.getElementById("vt-style")) {
    var s = document.createElement("style");
    s.id = "vt-style";
    s.textContent =
      ".vt-toolbar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:10px}" +
      ".vt-search{flex:1;min-width:160px;padding:8px 10px;border:1px solid var(--line,#d9cdb8);" +
      "border-radius:8px;font-size:14px;background:var(--paper,#fff)}" +
      ".vt-count{color:var(--ink-soft,#6B6455);font-size:13px}" +
      ".vt-btn{padding:7px 12px;border:1px solid var(--accent,#c8463a);background:var(--accent,#c8463a);" +
      "color:#fff;border-radius:8px;cursor:pointer;font-size:13px}" +
      ".vt-btn:hover{opacity:.88}" +
      ".vt-tablewrap{max-height:60vh;overflow:auto;border:1px solid var(--line,#d9cdb8);border-radius:8px}" +
      ".vt-table{width:100%;border-collapse:collapse;font-size:14px}" +
      ".vt-table th,.vt-table td{padding:8px 10px;border-bottom:1px solid var(--line,#d9cdb8);text-align:left;vertical-align:top}" +
      ".vt-table thead th{position:sticky;top:0;background:var(--bg,#faf7f2);z-index:1}" +
      ".vt-table th.vt-sortable{cursor:pointer;user-select:none}" +
      ".vt-table tbody tr{cursor:pointer}" +
      ".vt-table tbody tr:hover{background:rgba(200,70,58,.06)}" +
      ".vt-empty{text-align:center;color:var(--ink-soft,#6B6455);padding:20px}" +
      ".vt-drill{position:fixed;inset:0;z-index:9999;display:none}" +
      ".vt-drill.open{display:block}" +
      ".vt-drill-mask{position:absolute;inset:0;background:rgba(35,32,26,.4)}" +
      ".vt-drill-panel{position:absolute;top:0;right:0;height:100%;width:min(460px,92vw);" +
      "background:var(--paper,#fff);box-shadow:-8px 0 30px rgba(0,0,0,.2);display:flex;flex-direction:column;" +
      "transform:translateX(100%);transition:transform .25s ease;font-family:inherit}" +
      ".vt-drill.open .vt-drill-panel{transform:translateX(0)}" +
      ".vt-drill-panel header{display:flex;align-items:center;justify-content:space-between;" +
      "padding:14px 16px;border-bottom:1px solid var(--line,#d9cdb8)}" +
      ".vt-drill-title{font-weight:600;color:var(--accent,#c8463a)}" +
      ".vt-drill-close{border:none;background:none;font-size:24px;cursor:pointer;color:var(--ink-soft,#6B6455)}" +
      ".vt-drill-body{padding:16px;overflow:auto;line-height:1.7}" +
      ".vt-drill-body table{width:100%;border-collapse:collapse;margin:8px 0}" +
      ".vt-drill-body th,.vt-drill-body td{border:1px solid var(--line,#d9cdb8);padding:6px 8px;font-size:13px;text-align:left}";
    document.head.appendChild(s);
  }

  global.VisTools = {
    exportCSV: exportCSV,
    exportJSON: exportJSON,
    exportSVG: exportSVG,
    makeFilterableTable: makeFilterableTable,
    openDrill: openDrill,
    closeDrill: closeDrill,
  };
})(window);
