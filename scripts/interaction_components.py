"""interaction_components.py — 全站开合组件清单（W1147 待办①·交互后态门禁覆盖的数据面）。

12 类开合组件 × 代表页 × 交互入口/关闭方式/开启态断言/关闭后残留断言。
探针 scripts/interaction_state_probe.py 按本清单驱动；组件增删须同步本表（单一事实源）。
"""

# 每行：(组件类, 代表页(相对 site/), 入口选择器, 开启态断言(选择器, 属性检查), 关闭后残留白名单)
COMPONENTS = [
    ("nav-drawer",      "index.html",                        ".nav-toggle",                 (".topnav nav.open", "nav-mask.open"),          ()),
    ("filter-tab",      "dashboard.html",                    ".filter-tab:nth-child(2)",    ("[data-filtered]", None),                       ()),
    ("search-clear",    "data/search.html",                  "input[type=search]",          ("#results", None),                              ()),
    ("chart-tooltip",   "data/chapter-stats.html",           "svg.vis rect",                (".chart-tooltip.visible", None),                (".chart-tooltip.visible",)),
    ("drill-layer",     "data/graph-explorer.html",          "tbody tr",                    (".vt-drill.open", None),                        (".vt-drill.open",)),
    ("ask-chip",        "index.html",                        ".ask-chip",                   ("#askInput", None),                             ()),
    ("theme-toggle",    "index.html",                        "#themeToggle, [data-theme-btn], .nav-actions button", ("html[data-theme]", None), ()),
    ("danmaku-hover",   "data/cross-time-danmaku.html",      ".danmaku-card",               (None, None),                                    ()),
    ("cite-copy",       "reader/ch001.html",                 ".cite-copy",                  (None, None),                                    ()),
    ("back-to-top",     "guide.html",                        None,                          (None, None),                                    ()),
    ("table-sticky",    "data/methodology-matrix.html",      None,                          (".table-wrap--sticky", None),                   ()),
    ("tag-cloud-hover", "data/tag-cloud.html",               ".tag-item, a",                (None, None),                                    ()),
]
