"""W756 人名用字语料纯度批：语料容器 `魏徵`→`魏征`（选项 3）。

范围（5 容器 · 10 处）：
  权威源：source/原文/分回/第068回.md（2）+ 第091回.md（1）+ source/原文/shendu/SD039.md（1）
  镜像容器：dataset/text-search.json（3·第 20 门禁语料保真检对拍源）
            site/static/js/text-search-app.js（3·页面内嵌副本·W691 三容器纪律）
不动：docs/02-04 散文、dataset 其它 json、site/data 页（展示面两态并存为既定口径）。
"""
import sys

TARGETS = {
    "source/原文/分回/第068回.md": 2,
    "source/原文/分回/第091回.md": 1,
    "source/原文/shendu/SD039.md": 1,
    "dataset/text-search.json": 3,
    "site/static/js/text-search-app.js": 3,
}
OLD, NEW = "魏徵", "魏征"
total = 0
for p, expect in TARGETS.items():
    t = open(p, encoding="utf-8", newline="").read()  # newline='' 保行尾
    n_old, n_new_before = t.count(OLD), t.count(NEW)
    assert n_old == expect, f"{p}: 预期 {expect} 处旧值，实测 {n_old} 处（拒绝盲改）"
    t2 = t.replace(OLD, NEW)
    assert t2.count(OLD) == 0, f"{p}: 替换后仍有旧值残留"
    assert t2.count(NEW) == n_new_before + n_old, f"{p}: 新值增量异常"
    open(p, "w", encoding="utf-8", newline="").write(t2)
    total += n_old
    print(f"{p}: 旧值 {n_old} → 0 · 新值 {n_new_before} → {t2.count(NEW)}")
print("合计改字:", total)
sys.exit(0)
