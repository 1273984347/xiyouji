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
MARK = "<!-- ANALYTICS-DUAL v1 w1167 -->"
SKIP = {"_template.html"}
END_HEAD = re.compile(r"</head>", re.I)


def rel_static(rel_path: str) -> str:
    depth = len(Path(rel_path).parts) - 1
    return ("../" * depth) + "static/js/goatcounter.js"


def build_block(rel_path: str, cfg: dict) -> str:
    gc = cfg.get("goatcounter_endpoint", "")
    ga4 = cfg.get("ga4_measurement_id", "")
    parts = [MARK]
    if gc:
        parts.append('<script data-goatcounter="%s" async src="%s"></script>' % (gc, rel_static(rel_path)))
    if ga4:
        # SRI 取舍：gtag.js 由 Google 高频轮换内容且官方不提供稳定摘要，钉 SRI 会在数日内
        # 静默打断统计——不可行。防线为 CSP script-src host 白名单（G0-1 具名例外）；
        # W424 的 SRI 先例适用面是稳定库（d3 等），形态不同不套用。大陆面走自托管 GoatCounter 零此风险。
        parts.append('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>' % ga4)
        parts.append(
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}"
            "gtag('js',new Date());gtag('config','%s');</script>" % ga4
        )
    if not gc and not ga4:
        return ""
    return "\n" + "\n".join(parts) + "\n"


def process(rel: str, txt: str, cfg: dict):
    block = build_block(rel, cfg)
    if not block.strip():
        return txt, "no-config"
    if MARK in txt:
        # 幂等更新：MARK 到 </head> 前的注入区整段重建
        i = txt.index(MARK)
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
    ga4_on = bool(cfg.get("ga4_measurement_id"))
    print(f"mode={mode}  轨道: GoatCounter={'开' if gc_on else '关'} GA4={'开' if ga4_on else '关(ID未配置)'}")
    print(f"stats={stats}  改动={len(changed)}")
    if mode == "--check":
        missing = [f for f in sorted(SITE.rglob("*.html"))
                   if f.relative_to(SITE).as_posix() not in SKIP
                   and MARK not in f.read_text(encoding="utf-8", errors="replace")]
        print(f"CHECK {'FAIL 缺注入页=' + str(len(missing)) if (gc_on or ga4_on) and missing else 'PASS'}")
        sys.exit(1 if (gc_on or ga4_on) and missing else 0)


if __name__ == "__main__":
    main()
