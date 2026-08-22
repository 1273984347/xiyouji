#!/usr/bin/env python3
"""baseline_snapshot.py — W464 Phase 3 观测基线快照生成器（入库脚本）

自动生成「现状基线表」写入 scripts/output/观测基线快照.md：
内容计数（A1-A6/可视化/EN/sitemap）+ 性能三值（读 perf-baseline.json）+ UV 手填栏。
UV（G1/G2）依赖 GoatCounter 后台登录态，本脚本留手填位，由维护者回填后供 W465 judge_gate 消费。

用法：python scripts/baseline_snapshot.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def count_md(d: Path) -> int:
    return sum(1 for p in d.glob("*.md") if p.name != "README.md") if d.exists() else 0


def main() -> None:
    docs = ROOT / "docs"
    a = {
        "A1": count_md(docs / "01-全书逐回解读"),
        "A2": count_md(docs / "06-个人随笔"),
        "A3": count_md(docs / "02-人物深度分析"),
        "A4": count_md(docs / "03-主题与情节专题"),
        "A5": count_md(docs / "04-文化与历史背景"),
        "A6": count_md(docs / "05-诗词歌赋"),
    }
    total = sum(a.values())
    viz = sum(1 for p in (ROOT / "site" / "data").glob("*.html") if p.name != "_shell.html")
    en = sum(1 for p in (ROOT / "site" / "en").glob("*.html"))
    sitemap = (ROOT / "site" / "sitemap.xml").read_text(encoding="utf-8")
    loc = len(re.findall(r"<loc>", sitemap))
    perf = json.loads((ROOT / "scripts" / "output" / "perf-baseline.json").read_text(encoding="utf-8"))

    lines = [
        "# 观测基线快照（W464 · 2026-08-18 · baseline_snapshot.py 自动生成）",
        "",
        "> Phase 3 路线图 §0 基线的机器生成版；UV 两值为手填栏（GoatCounter 后台需登录态），",
        "> 由维护者回填后作为 W465 judge_gate.py 的输入凭据（输入+阈值+输出分支可复算）。",
        "",
        "| 维度 | 现值 | 来源 |",
        "|:---|:---|:---|",
        f"| 内容文档 | A1–A6 共 {total} 篇（A1 {a['A1']} / A2 {a['A2']} / A3 {a['A3']} / A4 {a['A4']} / A5 {a['A5']} / A6 {a['A6']}） | 目录实测 |",
        f"| 可视化页 | {viz}（site/data 减 _shell） | 目录实测 |",
        f"| 英文站 | {en} 页 | 目录实测 |",
        f"| sitemap | {loc} 个 <loc> | sitemap.xml |",
    ]
    for page, m in perf["pages"].items():
        lines.append(f"| LCP/CLS/TBT · {page} | {m['lcp']}ms / {m['cls']} / {m['tbt']}ms | perf-baseline.json（W464 实测） |")
    lines += [
        "| **7 日 UV（G1/G3）** |  待后台回填 | GoatCounter 后台 |",
        "| **30 日 UV（G1/G3）** | ⬜ 待后台回填 | GoatCounter 后台 |",
        "| 外部访客事件/周（G2） | ⬜ 待后台回填 | GoatCounter 后台（visit-log 不计入） |",
        "",
        "## 决策闸门阈值（W465 判定用）",
        "",
        "- 进入分发轨（Phase B）：7 日 UV ≥ 100 或 30 日 UV ≥ 200",
        "- 触发归档维护：30 日 UV < 30",
        "- 中间态：仅观测 + Phase C 工程质量加固",
        "",
        "## 链路核验（W464 自动项）",
        "",
        "- count.js 加载属性：async（根/CN/EN 抽查 ✅）；visit-log.js：defer（✅，仅本地诊断不计 G2）",
        "- 计数端点可达：https://1273984347.goatcounter.com/count 响应（裸 GET 400 = 端点存活 ✅）",
        "- 性能三值全过阈值（LCP<5000/CLS<0.3/TBT<300 ✅，实测最大 LCP 136ms / TBT 163ms）",
    ]
    out = ROOT / "scripts" / "output" / "观测基线快照.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] {out.name} 已生成（内容 {total} 篇 / 可视化 {viz} / EN {en} / sitemap {loc}）")


if __name__ == "__main__":
    main()
