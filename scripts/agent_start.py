#!/usr/bin/env python3
"""Agent 开局状态摘要 agent_start（W705 建·W707 加 --task）——把「读文档的负担」转移到系统。

会话开始时运行 `python scripts/agent_start.py`：现读磁盘输出一份当前事实摘要
（现役三元组/近 3 批次/stats 全键/对账表现势/门禁实况/关键铁律指针）——全部值来自
磁盘实时读取，无缓存无硬编码，保证 Agent 开局拿到的是当前值而非训练记忆。
`--task`：按 git status 改动路径分类输出「本次任务相关」必读清单（W707·按需读取入口）。
`--json` 供程序化消费（宿主/MCP 注入用）。

设计边界：本脚本不做「强制注入」（宿主 system message 是宿主侧能力）——项目侧最强形态是
CLAUDE.md 接手导航首行指令 + AGENTS §7 第 0 步：宿主自动加载 CLAUDE.md → Agent 看到指令 →
开局先跑本脚本 → 记忆刷新为当前事实。
"""

import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台 GBK 默认编码兜底

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RE_SEG_HIST = re.compile(r"^###\s+v([\d.]+)（([^）]+)）：(W\d+)\s*([^\n]*)", re.M)
RE_SEG_NEW = re.compile(r"^###\s+(W\d+)（([^）]+)）：\s*([^\n]*)", re.M)  # W711 方案 D 新形态（W713 兼容·历史段不匹配）
RE_LEDGER_NOW = re.compile(r"现势：下一自由号 = \*\*(W\d+)\*\*")
RE_CLAUDE_RULE = re.compile(r"^\d+\. \*\*(.+?)→", re.M)

TASK_MAP = [  # (路径模式, 必读提示) —— W713 更新：BL-24 已收官（W709），指针改 L2 主题文件
    (r"^site/|\.(css|js|html)$", "docs/agent/gates.md（改 site 必读门禁）+ docs/agent/pitfalls.md §CSS/视觉渲染"),
    (r"^scripts/check_|verify_delivery", "docs/agent/gates.md 对应槽位 + verify 段自洽锁（改门禁必读）"),
    (r"\.py$", "AGENTS §4.3 工具链要点 + docs/agent/pitfalls.md §流程/协作/取证 + ruff/pytest 计数钉纪律"),
    (r"^dataset/|scripts/output/data", "docs/agent/pitfalls.md §数据/内容可信度（计数钉/旧值标记扫描/双源门禁第 39/40）"),
    (r"^docs/|^交接文档|^CHANGELOG|^README|^STRUCTURE", "docs/00-导读/文档规范.md §4.9-4.11 + 第 31 门禁 C5 对账"),
    (r"^xiyouji-agent-web/", "docs/agent/agent-web.md（W680 引擎层）"),
    (r"^\.github/", "AGENTS §4.3 CI 类（workflow 触发条件/quotePath/SHA 钉）"),
]


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def _segments(changelog):
    """CHANGELOG 段解析（W713 双形态）：历史段 vX.Y.Z（date）：W### 标题 / 新段 W###（date）：标题。
    返回按出现序的 [{"v", "date", "w", "desc"}]（新段 v=None·方案 D 批次键唯一）。"""
    segs = []
    for m in RE_SEG_HIST.finditer(changelog):
        segs.append((m.start(), {"v": m.group(1), "date": m.group(2), "w": m.group(3), "desc": m.group(4).strip()}))
    for m in RE_SEG_NEW.finditer(changelog):
        segs.append((m.start(), {"v": None, "date": m.group(2), "w": m.group(1), "desc": m.group(3).strip()}))
    segs.sort(key=lambda t: t[0])
    return [d for _, d in segs]


def gather():
    changelog = read("CHANGELOG.md")
    segs = _segments(changelog)
    top = segs[0] if segs else None
    recent = segs[1:4]
    stats = {}
    try:
        with open(os.path.join(HERE, "output", "stats.json"), encoding="utf-8") as f:
            stats = json.load(f)
    except (OSError, ValueError):
        pass
    ledger = read(os.path.join("docs", "00-导读", "W批次编号对账表.md"))
    m_now = RE_LEDGER_NOW.search(ledger)
    jiaojie = read("交接文档.md")
    i = jiaojie.find("零、当前阻塞（接手必读）")  # W713：锚段标题（原锚「零、当前阻塞」命中阅读契约引述·取不到正文）
    blockers = []
    if i != -1:
        for ln in jiaojie[i:].splitlines()[1:]:
            ls = ln.strip()
            if ls.startswith("#"):
                break  # W713：段标题即「零」段终点——防把「一、当前进度」里程碑 bullet 当阻塞输出（实证）
            ln = ls.lstrip("- ").strip()
            if ln and not ln.startswith((">", "|")):
                blockers.append(ln[:90])
            if len(blockers) >= 2:
                break
    claude = read("CLAUDE.md")
    rules = ["「" + r.strip().rstrip("→ ") + "」等 → 详见 CLAUDE.md" for r in RE_CLAUDE_RULE.findall(claude)[:3]]
    return {
        "version": top["v"] if top else None,
        "date": top["date"] if top else None,
        "head_w": top["w"] if top else None,
        "head_desc": (top["desc"] if top else None),
        "recent_batches": recent,
        "stats": {k: (e.get("value") if isinstance(e, dict) else e) for k, e in stats.items() if not k.startswith("_")},
        "ledger_next_free": m_now.group(1) if m_now else None,
        "blockers": blockers,
        "claude_md": "CLAUDE.md 已由宿主自动加载（速查层·指针化）；必守规则入口=" + (rules[0] if rules else "CLAUDE.md"),
    }


def render(d):
    out = []
    out.append("=" * 24 + " 当前项目状态（agent_start 实读磁盘·%s）" % d["date"] + " " + "=" * 24)
    if d["version"]:
        out.append("现役版本：v%s（%s）%s——%s" % (d["version"], d["date"], d["head_w"], d["head_desc"]))
    else:
        out.append("现役批次：%s（%s）——%s" % (d["head_w"], d["date"], d["head_desc"]))
    out.append("近 3 批次：" + " / ".join("%s（%s）" % (b["w"], b["v"] or "批次键") for b in d["recent_batches"]))
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


def changed_paths():
    r = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return [ln[3:].strip().strip('"') for ln in r.stdout.splitlines() if ln.strip()]


def render_task():
    paths = changed_paths()
    hits = []
    for pat, tip in TASK_MAP:
        matched = [x for x in paths if re.search(pat, x)]
        if matched:
            joined = "、".join(matched[:3])
            hits.append("* " + tip + "\n      例：" + joined)
    out = ["===== 本次任务相关（按改动路径分类·agent_start --task）====="]
    if not paths:
        out.append("（工作树干净——无未提交改动；按任务性质自行选择节）")
    out.extend(hits if hits else ["（改动未命中已知分类——按 AGENTS §7 快速上手路径走）"])
    out.append("通用必读：CLAUDE.md（宿主已加载）→ 交接「零、当前阻塞」→ 动手前 verify_delivery 全绿。")
    out.append("=" * 60)
    return "\n".join(out)


def main():
    if "--task" in sys.argv:
        print(render_task())
        return 0
    d = gather()
    if "--json" in sys.argv:
        print(json.dumps(d, ensure_ascii=False, indent=2))
    else:
        print(render(d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
