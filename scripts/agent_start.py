#!/usr/bin/env python3
"""Agent 开局状态摘要 agent_start（W705·用户方案第三阶段第 2 步）——把「读文档的负担」转移到系统。

会话开始时运行 `python scripts/agent_start.py`：现读磁盘输出一份当前事实摘要
（现役三元组/近 3 批次/stats 全键/对账表现势/门禁实况/关键铁律指针）——全部值来自
磁盘实时读取，无缓存无硬编码，保证 Agent 开局拿到的是当前值而非训练记忆。
`--json` 供程序化消费（宿主/MCP 注入用）。

设计边界：本脚本不做「强制注入」（宿主 system message 是宿主侧能力）——项目侧最强形态是
CLAUDE.md 接手导航首行指令 + AGENTS §7 第 0 步：宿主自动加载 CLAUDE.md → Agent 看到指令 →
开局先跑本脚本 → 记忆刷新为当前事实。
"""

import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台 GBK 默认编码兜底

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RE_TOP = re.compile(r"^###\s+(v[\d.]+)（([^）]+)）：(W\d+)\s*([^\n]*)", re.M)
RE_RECENT = re.compile(r"^###\s+(v[\d.]+)（([^）]+)）：(W\d+)[^\n]*", re.M)
RE_LEDGER_NOW = re.compile(r"现势：下一自由号 = \*\*(W\d+)\*\*")
RE_CLAUDE_RULE = re.compile(r"^\d+\. \*\*(.+?)→", re.M)


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def gather():
    changelog = read("CHANGELOG.md")
    top = RE_TOP.search(changelog)
    recent = RE_RECENT.findall(changelog)[:3]
    stats = {}
    try:
        with open(os.path.join(HERE, "output", "stats.json"), encoding="utf-8") as f:
            stats = json.load(f)
    except (OSError, ValueError):
        pass
    ledger = read(os.path.join("docs", "00-导读", "W批次编号对账表.md"))
    m_now = RE_LEDGER_NOW.search(ledger)
    jiaojie = read("交接文档.md")
    i = jiaojie.find("零、当前阻塞")
    blockers = []
    if i != -1:
        for ln in jiaojie[i:].splitlines()[1:]:
            ln = ln.strip().lstrip("- ").strip()
            if ln and not ln.startswith(("#", ">", "|")):
                blockers.append(ln[:90])
            if len(blockers) >= 2:
                break
    claude = read("CLAUDE.md")
    rules = ["「" + r.strip().rstrip("→ ") + "」等 → 详见 CLAUDE.md" for r in RE_CLAUDE_RULE.findall(claude)[:3]]
    return {
        "version": top.group(1) if top else None,
        "date": top.group(2) if top else None,
        "head_w": top.group(3) if top else None,
        "head_desc": (top.group(4).strip() if top else None),
        "recent_batches": [{"v": v, "date": d, "w": w} for v, d, w in recent],
        "stats": {k: (e.get("value") if isinstance(e, dict) else e) for k, e in stats.items() if not k.startswith("_")},
        "ledger_next_free": m_now.group(1) if m_now else None,
        "blockers": blockers,
        "claude_md": "CLAUDE.md 已由宿主自动加载（速查层·指针化）；必守规则入口=" + (rules[0] if rules else "CLAUDE.md"),
    }


def render(d):
    out = []
    out.append("=" * 24 + " 当前项目状态（agent_start 实读磁盘·%s）" % d["date"] + " " + "=" * 24)
    out.append("现役版本：%s（%s）%s——%s" % (d["version"], d["date"], d["head_w"], d["head_desc"]))
    out.append("近 3 批次：" + " / ".join("%s（%s）" % (b["w"], b["v"]) for b in d["recent_batches"]))
    out.append("对账表现势：下一自由号 %s（动工前先在该表登记认领）" % d["ledger_next_free"])
    st = d["stats"]
    if st:
        out.append(
            "规模口径：HTML %s（data %s/en %s/根 %s/reader %s）·可视化页 %s·CSP %s·门禁 %s 槽"
            % (st.get("html_total"), st.get("site_data_html"), st.get("site_en_html"), st.get("site_root_html"),
               st.get("site_reader_html"), st.get("visualization_pages"), st.get("csp_covered"), st.get("gate_count"))
        )
        out.append(
            "内容口径：A1-A6 %s 篇·方法论 %s 篇·scripts %s 类·data json %s 个（全部实读 stats.json·勿用记忆值）"
            % (st.get("a1_a6_docs"), st.get("methodology_docs"), st.get("script_classes"), st.get("json_count"))
        )
    if d["blockers"]:
        out.append("当前阻塞（交接「零」段）：" + "；".join(d["blockers"]))
    out.append("开局三查：① git log --oneline -5 + gh run list 识别并行增量 ② 动手前 verify_delivery 全绿基线 ③ " + d["claude_md"])
    out.append("收尾纪律：七步清单（AGENTS §4.3）+ 级联 batch_cascade + 对账表登记；改口径批次须同批 stats.py --w 刷新。")
    out.append("=" * 78)
    return "\n".join(out)


def main():
    d = gather()
    if "--json" in sys.argv:
        print(json.dumps(d, ensure_ascii=False, indent=2))
    else:
        print(render(d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
