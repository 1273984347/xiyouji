"""w1167_analytics_inject.py — 第⑤步 双轨统计注入器（A 方案：GA4 海外面 + GoatCounter 大陆面）

配置驱动：scripts/output/_w1167_analytics.json
  {"ga4_measurement_id": "G-XXX|空=跳过GA4", "goatcounter_endpoint": "https://<acct>.goatcounter.com/count"}

形态（历史契约复活，W426 取证）：
  - GoatCounter：本地自托管 site/static/js/goatcounter.js（ISC·9213B）+ data-goatcounter 属性回传
  - GA4：async gtag.js + 内联 config（哈希由 generate_csp 自动覆盖）
  - file:// 场景：两轨均 async + 网络失败静默（脚本本地在、回传不可达即无声降级，
    页面渲染零依赖——G0-1 例外边界与 G0-3 口径的实现面）
幂等：MARK 存在即原位更新；--check 供批后门禁引用。
"""
import io
import json
import re
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 根路径按 __file__ 派生：硬编码盘符在 CI（Linux runner）上指向不存在目录，
# 会让消费方门禁「扫到 0 页」而假绿——本地绿≠CI 绿（W700 教训形态）。
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CONFIG = ROOT / "scripts/output/_w1167_analytics.json"
MARK = "<!-- ANALYTICS v2 w1168 -->"
# v1 的双轨 MARK 保留为**迁移锚点**：不认旧 MARK，重跑会把旧块留在页面里再插一块新块
# ⇒ 每页两份脚本双份上报（幂等性的真正考验是「跨版本」而不只是「同版本重跑」）。
LEGACY_MARKS = ("<!-- ANALYTICS-DUAL v1 w1167 -->",)
STATS_JS = "stats.js"
SKIP = {"_template.html"}
END_HEAD = re.compile(r"</head>", re.I)


def rel_static(rel_path: str, fname: str = "goatcounter.js") -> str:
    """按页面深度给 static/js 下的相对路径（file:// 直开要求相对而非站点根）。"""
    depth = len(Path(rel_path).parts) - 1
    return ("../" * depth) + "static/js/" + fname


def build_block(rel_path: str, cfg: dict) -> str:
    gc = cfg.get("goatcounter_endpoint", "")
    parts = [MARK]
    if gc:
        parts.append('<script data-goatcounter="%s" async src="%s"></script>' % (gc, rel_static(rel_path)))
        # 统计桥（W1168）：编程式事件的唯一入口；声明式 click 仍由 goatcounter 自身 bind_events 处理
        parts.append('<script defer src="%s"></script>' % rel_static(rel_path, STATS_JS))
    if not gc:
        # GA4 轨自 W1168 起退出（G0-1 的 GA4 半侧经用户决定退役：账号未建、大陆可达性差、
        # web vitals 与自定义事件改由自托管 GoatCounter 单轨承载）；
        # 配置里的 ga4_measurement_id 字段保留为**退役说明位**而非待填项——
        # 删字段会让历史配置读起来像「还没配好」，反而是失真。
        return ""
    return "\n" + "\n".join(parts) + "\n"


def _block_start(txt: str) -> int:
    """现行 MARK 或任一 LEGACY MARK 的位置（跨版本迁移用）。"""
    for m in (MARK,) + LEGACY_MARKS:
        if m in txt:
            return txt.index(m)
    return -1


def process(rel: str, txt: str, cfg: dict):
    block = build_block(rel, cfg)
    if not block.strip():
        return txt, "no-config"
    i = _block_start(txt)
    if i >= 0:
        # 幂等更新：MARK（含旧版本）到 </head> 前的注入区整段重建
        j = txt.lower().index("</head>", i)
        new = txt[:i] + block.strip() + "\n" + txt[j:]
        return new, "update"
    e = END_HEAD.search(txt)
    if not e:
        return txt, "no-head"
    return txt[:e.start()] + block + txt[e.start():], "insert"


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dry-run"
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    stats, changed = {}, []
    for f in sorted(SITE.rglob("*.html")):
        rel = f.relative_to(SITE).as_posix()
        if rel in SKIP:
            continue
        txt = f.read_text(encoding="utf-8", errors="replace")
        new, action = process(rel, txt, cfg)
        stats[action] = stats.get(action, 0) + 1
        if new != txt:
            changed.append(rel)
            if mode == "--apply":
                f.write_text(new, encoding="utf-8")
    gc_on = bool(cfg.get("goatcounter_endpoint"))
    print(f"mode={mode}  轨道: GoatCounter 单轨={'开' if gc_on else '关'}"
          f"  桥={'随发' if gc_on else '不发'}  GA4=已退役(W1168)")
    print(f"stats={stats}  改动={len(changed)}")
    if mode == "--check":
        missing = [f for f in sorted(SITE.rglob("*.html"))
                   if f.relative_to(SITE).as_posix() not in SKIP
                   and MARK not in f.read_text(encoding="utf-8", errors="replace")]
        print(f"CHECK {'FAIL 缺注入页=' + str(len(missing)) if gc_on and missing else 'PASS'}")
        sys.exit(1 if gc_on and missing else 0)


if __name__ == "__main__":
    main()
