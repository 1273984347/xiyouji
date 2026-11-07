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
RE_CLAUDE_RULE = re.compile(r"^\d+\. \*\*(.+?)→", re.M)

TASK_MAP = [  # (路径模式, 必读提示) —— W713 更新：BL-24 已收官（W709），指针改 L2 主题文件
    (r"^site/|\.(css|js|html)$", "docs/agent/gates.md（改 site 必读门禁）+ pitfalls.md §CSS/视觉渲染"),
    (r"^scripts/check_|verify_delivery", "docs/agent/gates.md 对应槽位 + verify 段自洽锁（改门禁必读）"),
    (r"\.py$", "AGENTS §4.3 工具链要点 + pitfalls.md §流程/协作/取证 + ruff/pytest 计数钉纪律"),
    (r"^dataset/|scripts/output/data", "pitfalls.md §数据/内容可信度（计数钉/旧值标记扫描/双源门禁第 39/40）"),
    (r"^docs/|^HANDOVER|^CHANGELOG|^README|^STRUCTURE", "docs/00-导读/文档规范.md §4.9-4.11 + 第 31 门禁 C5 对账"),
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


def _stats_consistency_warnings(stats):
    """stats.json 的**口径一致性**告警（P-3 L2·W1110 落地·复用 C10 同一复算式）。

    W1104 批（P-3 L1）落地四类告警（缺失 / 损坏 / 空 / 陈旧）时，把「口径一致性」
    挂账为「待异源复算（C10）落地后接入」⇒ 本函数是那次挂账的清偿：
    用**与第 31 门禁 C10 完全同一复算式**（`doc_areas.board_count_mismatches`·
    共享单一事实源）独立复算各板块内容篇数，与 stats.json 对账 ⇒ 不一致即告警。

    为何要独立复算（同源自检的盲区）：C5d 用 `stats.py --check`（**同一实现**）实算 ⇒
    实算与存值自洽 ⇒ 口径写错时**门禁不红**（W1096 实证：排除集写死小写 ⇒
    07/08/09 三板块对外篇数各虚增 1 而全链无红灯）。故开局摘要必须用**独立复算**
    才能发现口径漂移。

    告警**不阻断**（工具层告警与门禁阻断分层·与 L1 同族纪律）。
    """
    warnings = []
    try:
        from doc_areas import board_count_mismatches
    except ImportError:  # pragma: no cover — 直跑时 sys.path[0]=scripts/ 应可导入
        warnings.append("stats 口径一致性未核验（复算模块不可导入·跳过）")
        return warnings
    try:
        mismatches = board_count_mismatches(stats)
    except Exception as exc:  # noqa: BLE001 — 告警层不因复算异常而崩开局摘要
        warnings.append("stats 口径一致性未核验（复算异常：%s）" % exc)
        return warnings
    for key, computed, stored in mismatches:
        warnings.append(
            "stats.json 口径漂移：%s 实算 %d ≠ 存值 %d（排除集口径漂移或未刷新 stats）"
            "·请跑 py -3 scripts/stats.py --w <批号> 刷新" % (key, computed, stored))
    return warnings


def load_stats_with_warnings(stats_path, changelog_path, stale_tolerance=2.0):
    """读 stats.json 并返回 (stats, warnings)。

    W1104（P-3 L1）：开局事实摘要原先把 stats.json 当**事实源**直读——读失败静默
    pass（stats 变空字典且无任何提示）、陈旧也照单全收 ⇒ 属**静默降级**：Agent 拿到
    过期或缺失的规模口径却以为是真的。本函数改为**三类显式告警**：

      ① 缺失（FileNotFoundError）② 不可读/损坏（非合法 JSON）③ 内容为空或非对象
      ④ 陈旧（mtime 早于事实源 CHANGELOG.md——链序：级联写 CHANGELOG → … → stats.py --w）

    告警只提示不阻断（开局摘要不是门禁），但必须**显形**而非静默。
    陈旧判据用 mtime 比较并留 stale_tolerance 容差（写盘粒度与链序执行间隔）。
    """
    warnings = []
    stats = {}
    try:
        with open(stats_path, encoding="utf-8") as f:
            stats = json.load(f)
    except FileNotFoundError:
        warnings.append("stats.json 缺失（%s）·规模口径不可用·"
                        "请跑 py -3 scripts/stats.py --w <批号> 重建" % stats_path)
        return stats, warnings
    except (OSError, ValueError) as exc:
        warnings.append("stats.json 不可读或损坏（%s：%s）·规模口径不可用·"
                        "请跑 py -3 scripts/stats.py --w <批号> 重建"
                        % (stats_path, exc))
        return stats, warnings
    if not isinstance(stats, dict) or not stats:
        warnings.append("stats.json 为空或非对象（%s）·规模口径不可用·"
                        "请跑 py -3 scripts/stats.py --w <批号> 重建" % stats_path)
        return stats, warnings
    try:
        s_mtime = os.path.getmtime(stats_path)
        c_mtime = os.path.getmtime(changelog_path)
    except OSError:
        return stats, warnings
    if s_mtime + stale_tolerance < c_mtime:
        warnings.append("stats.json 陈旧（早于 CHANGELOG.md 的最新改动）·"
                        "规模口径可能过期·请跑 py -3 scripts/stats.py --w <批号> 刷新")
    # P-3 L2（W1110）：口径一致性（异源复算·复用 C10 同一复算式）——清偿 W1104 的挂账
    warnings.extend(_stats_consistency_warnings(stats))
    return stats, warnings


def gather():
    changelog = read("CHANGELOG.md")
    segs = _segments(changelog)
    top = segs[0] if segs else None
    recent = segs[1:4]
    stats, stats_warnings = load_stats_with_warnings(
        os.path.join(HERE, "output", "stats.json"),
        os.path.join(ROOT, "CHANGELOG.md"))
    ledger = read(os.path.join("docs", "00-导读", "W批次编号对账表.md"))
    # W1154（基础设施审计 §3.5.2-5）：「现势：下一自由号」块 W737 起已碑化（台账第 8 行明示
    # 停止维护）⇒ 原读数恒 None；权威规则 = 台账认领行 max(W)+1（与 reserve_w 同源口径）。
    _ledger_ws = [int(w) for w in re.findall(r"^\|\s*W?(\d{3,4})\s*\|", ledger, re.M)]
    ledger_next = "W%d" % (max(_ledger_ws) + 1) if _ledger_ws else None
    jiaojie = read("HANDOVER.md")
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
        "stats_warnings": stats_warnings,
        "ledger_next_free": ledger_next,
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
            "内容口径：A1-A6 %s 篇·方法论 %s 篇·scripts %s 类（全部实读 stats.json·勿用记忆值）"
            % (st.get("a1_a6_docs"), st.get("methodology_docs"), st.get("script_classes"))
        )
    for w in d.get("stats_warnings") or []:
        out.append("⚠ stats 状态告警：" + w)
    if d["blockers"]:
        out.append("当前阻塞（交接「零」段）：" + "；".join(d["blockers"]))
    out.append("开局三查：① git log --oneline -5 + gh run list 识别并行增量 ② 动手前 verify_delivery 全绿基线 ③ " + d["claude_md"])
    out.append("收尾纪律：七步清单（AGENTS §4.3）+ 级联 batch_cascade + 对账表登记；改口径批次须同批 stats.py --w 刷新。")
    out.append("=" * 78)
    return "\n".join(out)


def changed_paths():
    r = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return [ln[3:].strip().strip('"') for ln in r.stdout.splitlines() if ln.strip()]


# W1148 b 方案（治懒读）：touches 路径 → 最小铁律集。恒真高频条目（任何任务都适用）
# 与路径敏感条目（按 touches 分类）→ 从 AGENTS §6 抽**整条原文**注入会话头——
# 「精准喂」取代「全读靠自觉」。每条带「AGENTS 铁律 N」回指锚（防注入件与源漂移失联）。
ALWAYS_RULES = (1, 2, 5, 8, 17, 18, 21)  # 恒真：声明≠落地/纯设计/先取证/禁擅改/预约/三问/CI节奏
RULE_PATH_MAP = [  # (路径模式, 铁律号)
    (r"^site/|\.(css|js|html)$", (12, 6)),      # 动效契约 / file:// 铁律
    (r"\.py$", (20, 23)),                        # Python 结构检查 / 异常分类
    (r"^scripts/(batch_cascade|backfill|rebuild)", (24, 16)),  # 并行隔离 / 协作约束
    (r"^docs/|^HANDOVER|^CHANGELOG", (6, 1)),    # 文档同步 / 六文档
    (r"^dataset/", (13, 14)),                    # 可信度 / 修实例必修根
]


def minimal_rules(paths):
    """touches → 最小铁律集（恒真 ∪ 路径敏感·抽整条原文·带回指锚）。"""
    src = read("AGENTS.md")
    r0 = src.find("## 6. 必须遵守的铁律")
    r1 = src.find("## 7.", r0)
    seg = src[r0:r1] if r0 != -1 and r1 != -1 else ""
    blocks = re.split(r"(?=^\d+\. \*\*)", seg, flags=re.M)
    by_num = {}
    for b in blocks:
        m = re.match(r"^(\d+)\. ", b)
        if m:
            by_num[int(m.group(1))] = b.strip()
    want = set(ALWAYS_RULES)
    for pat, nums in RULE_PATH_MAP:
        if any(re.search(pat, x) for x in paths):
            want.update(nums)
    out = []
    for n in sorted(want):
        body = by_num.get(n)
        if not body:
            continue
        # 单条超 400 字符截断（细节归原文·回指锚保联）
        if len(body) > 400:
            body = body[:400] + "…（全文见 AGENTS.md §6）"
        out.append("【AGENTS 铁律 %d】%s" % (n, body))
    return out


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
    # W1148 b 方案：最小铁律集注入（恒真 ∪ 路径敏感·抽整条原文带回指锚）
    rules = minimal_rules(paths)
    if rules:
        out.append("")
        out.append("===== 最小铁律集（恒真 + 按 touches 敏感·共 %d 条·全文见 AGENTS §6）=====" % len(rules))
        out.extend(rules)
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
