#!/usr/bin/env python3
"""Agent 开局状态摘要 agent_start（W705 建·W707 加 --task）——把「读文档的负担」转移到系统。

会话开始时运行 `python scripts/agent_start.py`：现读磁盘输出一份当前事实摘要
（现役三元组/近 3 批次/stats 全键/对账表现势/门禁实况/关键铁律指针）——全部值来自
磁盘实时读取，无缓存无硬编码，保证 Agent 开局拿到的是当前值而非训练记忆。
`--task`：按 git status 改动路径分类输出「本次任务相关」必读清单（W707·按需读取入口），
并附「变更类型 → 必跑清单」（W1179·命令可直接粘贴）。
`--checklist <类型|all>`：工作树干净时也能在**动手前**查某类变更该跑什么（清单最有用的时刻）。
`--checklist-selftest`：四类命中与命令完整性自测。
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
    # W1154：「现势：下一自由号」块已碑化；权威规则＝台账认领行 max(W)+1（W1179 起与
    # next_batch_w 共用单一实现，避免 gather 与 --checklist 出现两套批号口径）。
    ledger_next = next_batch_w()
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


def changed_entries():
    """git status → [(状态码, 路径)]。W1179：清单需区分「新增 A/??」与「修改 M」——
    原 changed_paths 丢掉状态码，无法识别「新增页 / 新增槽」这类**按动作**分类的变更类型。

    状态码取 XY 的首位（索引态优先；工作树新增为 ??）；重命名取箭头右侧的新路径。
    """
    r = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True,
                       text=True, encoding="utf-8", errors="ignore")
    out = []
    for ln in r.stdout.splitlines():
        if not ln.strip():
            continue
        code = ln[:2].strip() or "??"
        path = ln[3:].strip().strip('"')
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip().strip('"')
        out.append((code, path))
    return out


def changed_paths():
    """兼容原接口：返回路径列表（TASK_MAP / minimal_rules 依赖）。"""
    return [p for _, p in changed_entries()]


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


# W1179：变更类型 → 必跑清单。
# 立项依据：W1176 新增页返工四轮、W1177 把新增页清单化、W1178 新增槽又漏改
# EXPECTED_SECTION_NAMES —— 三者是同一缺口的三种形态：**清单只存在于上一轮的记忆里**。
# 设计约束：
#   ① 每条必带「依据」锚（坑表 E-NN / 门禁槽号 / W 批次），清单与源漂移时可检索核对；
#   ② 命令必须可直接粘贴——批号取台账下一自由号、页名取改动路径，禁省略号与占位符猜测；
#   ③ 与 agent_start 的设计边界一致：只提示不阻断（开局摘要不是门禁）；
#   ④ 工作树干净时可用 --checklist 主动查，覆盖「动手前」这一最需要清单的时刻。
CHANGE_CHECKLISTS = (
    {
        "key": "new-page",
        "name": "新增页（site/data|en|reader 新增 HTML）",
        "basis": "W1176 四轮返工 / W1177 --post / 第 28·30·26·45·46·64·69 槽",
        "pattern": r"^site/(data|en|reader)/.*\.html$|^site/[^/]+\.html$",
        "items": (
            ("note", "生成阶段优先用 new_page.py --post（已含徽标/导航/SEO/sitemap/索引/CSP/色盲基线/第 69 槽自检）；"
                     "若页已手写生成，逐条跑下列命令"),
            ("cmd", "py -3 scripts/w1167_badge_inject.py --apply"),
            ("cmd", "py -3 scripts/w1167_nav_inject.py --apply"),
            ("cmd", "py -3 scripts/inject_seo_head.py"),
            ("cmd", "py -3 scripts/gen_sitemap.py"),
            ("cmd", "py -3 scripts/_gen_search_index.py"),
            ("cmd", "py -3 scripts/generate_csp.py"),
            ("cmd", "py -3 scripts/stats.py --w {W}"),
            ("cmd", "py -3 scripts/check_chart_colorblind.py --generate-baseline"),
            ("cmd", "py -3 scripts/check_template_contract.py --target {target}"),
            ("note", "同步 CHANGELOG「全站页数口径」块七个数字 + AGENTS 可视化页计数（第 31 槽 C5/C5b）"),
            ("note", "先 git add 再跑 gen_folder_docs.py --refresh（第 45 槽按 Git 索引收集，refresh 先于 add 必漏新件）"),
            ("cmd", "py -3 scripts/gen_folder_docs.py --refresh"),
        ),
    },
    {
        "key": "new-gate",
        "name": "新增门禁槽 / 新增 check_*.py",
        "basis": "坑表 E-98（五处同改·W1105）/ W1178 实证（漏改 EXPECTED_SECTION_NAMES 被启动期断言抓出）",
        "pattern": r"^scripts/check_.*\.py$|^scripts/verify_delivery\.py$",
        "items": (
            ("note", "触发条件：新增 check_*.py，或 verify_delivery.py 新增/移动门禁段"
                     "（仅改注释、文案时可跳过本类；拿不准用 --checklist new-gate 复核）"),
            ("note", "E-98 五处接线：verify_delivery.py 门禁元组 → EXPECTED_SECTION_NAMES → 恒跑段登记 _SCOPE_CORE"
                     "（读页面且非恒跑则登记 SCOPE_SITE_SECTIONS，二选一）→ AGENTS §4.2 摘要 + 槽数三处"
                     " → gates.md 有序列表条目 + 标题槽数；漏一处第 41 槽启动期即拦"),
            ("cmd", "py -3 scripts/check_agents_layers.py"),
            ("cmd", "py -3 scripts/check_script_coverage.py"),
            ("cmd", "py -3 scripts/stats.py --w {W}"),
            ("note", "四面引用：verify_delivery.py / AGENTS.md / gates.md / 被挂脚本自身 docstring（第 42 槽 C1）"),
            ("cmd", "py -3 scripts/_gen_search_index.py"),
            ("cmd", "py -3 scripts/generate_csp.py"),
        ),
    },
    {
        "key": "shared-css",
        "name": "改共享 CSS（site/system.css / site/tokens.css）",
        "basis": "坑表 E-90（改动半径＝851 页内联副本）/ W1172·W1173 双视口实证",
        "pattern": r"^site/(system|tokens)\.css$",
        "items": (
            ("cmd", "py -3 scripts/inline_css.py --force"),
            ("cmd", "py -3 scripts/generate_csp.py"),
            ("cmd", "py -3 scripts/mobile_viewport_probe.py --scope all --reader-sample 20 "
                    "--width 375 --height 667 --out scripts/output/mobile_viewport_report.json"),
            ("cmd", "py -3 scripts/mobile_viewport_probe.py --scope all --reader-sample 20 "
                    "--width 320 --height 640 --out scripts/output/mobile_viewport_report_320.json"),
            ("cmd", "py -3 scripts/check_chart_colorblind.py --gate"),
            ("cmd", "py -3 scripts/stats.py --w {W}"),
            ("note", "第 12 槽 token 覆盖率 / 第 15 槽 INLINED 完整性 / 第 36 槽孤立选择器 / 第 37 槽 kpi-card 基类"),
        ),
    },
    {
        "key": "stats-scope",
        "name": "改口径块 / 统计 / 计数链",
        "basis": "第 31 槽 C5·C5b·C5d·C5e / 第 41·45·46·54 槽 / W1178 提交失败第二轮（索引陈旧）",
        "pattern": r"^(CHANGELOG\.md|HANDOVER\.md|AGENTS\.md|pitfalls\.md|STRUCTURE\.md|README\.md|"
                   r"scripts/output/stats\.json|\.agent/skills/puti-shouye/SKILL\.md)$",
        "items": (
            ("cmd", "py -3 scripts/stats.py --w {W}"),
            ("cmd", "py -3 scripts/check_doc_sync.py"),
            ("cmd", "py -3 scripts/check_pitfall_id_unique.py"),
            ("cmd", "py -3 scripts/check_agents_layers.py"),
            ("cmd", "git add -A -- . ':(exclude).gitignore'"),
            ("cmd", "py -3 scripts/gen_folder_docs.py --refresh"),
            ("cmd", "py -3 scripts/_gen_search_index.py"),
            ("cmd", "py -3 scripts/generate_csp.py"),
            ("note", "五处计数链同步：AGENTS §4.3 摘要 / HANDOVER 三件套 / puti-shouye SKILL / pitfalls 段头 /"
                     " CHANGELOG 口径块；文档改动必令第 46 槽索引失配（W1178 实证）"),
        ),
    },
)

_CHECKLIST_TAIL = (
    ("cmd", "py -3 scripts/verify_delivery.py --scope auto"),
    ("note", "提交前复核：py -3 scripts/check_commit_scope.py（第 51 槽）· git ls-files --eol 检 w/crlf 应为 0（E-11）"),
)


def _ledger_max_w():
    """台账最新认领行编号（W1154 权威规则：现势块已碑化，只认认领行）。"""
    ledger = read(os.path.join("docs", "00-导读", "W批次编号对账表.md"))
    ws = [int(w) for w in re.findall(r"^\|\s*W?(\d{3,4})\s*\|", ledger, re.M)]
    return max(ws) if ws else None


def current_batch_w():
    """本批号＝台账最新认领行（项目纪律：动工前先登记认领，故 max 即本批）。
    W1179 实证：清单初版误用「下一自由号」max+1，`stats.py --w` 会指向尚未开工的下一批。
    """
    m = _ledger_max_w()
    return "W%d" % m if m else None


def next_batch_w():
    """下一自由号＝max(W)+1 —— 供 gather 显示「动工前先登记认领」用。"""
    m = _ledger_max_w()
    return "W%d" % (m + 1) if m else None


def _is_new(code):
    return code.startswith("A") or code == "??"


def checklist_hits(entries):
    """改动条目 → 命中的清单 key 列表 + 每类匹配路径。"""
    hits, matched = [], {}
    for spec in CHANGE_CHECKLISTS:
        pat = re.compile(spec["pattern"])
        ms = [(c, p) for c, p in entries if pat.search(p)]
        if spec["key"] == "new-page":
            ms = [(c, p) for c, p in ms if _is_new(c)]
        if spec["key"] == "new-gate":
            ms = [(c, p) for c, p in ms
                  if (_is_new(c) and p.startswith("scripts/check_")) or p == "scripts/verify_delivery.py"]
        if ms:
            hits.append(spec["key"])
            matched[spec["key"]] = [p for _, p in ms]
    return hits, matched


def _checklist_vars(entries, matched):
    """命令变量全部从实况推导，输出即可粘贴。"""
    w = current_batch_w() or "W0000"
    pages = matched.get("new-page", [])
    target = pages[0] if pages else "site/_template.html"
    return {"W": w, "target": target}


def render_checklist(keys, entries, matched=None):
    """渲染「变更类型 → 必跑清单」。命令去重保序，避免多类命中重复输出。"""
    matched = matched or {}
    by_key = {s["key"]: s for s in CHANGE_CHECKLISTS}
    keys = [k for k in (keys or []) if k in by_key]
    if not keys:
        return "（未命中任何变更类型清单——按 AGENTS §7 快速上手路径走）"
    v = _checklist_vars(entries, matched)
    out = ["===== 本次必跑清单（变更类型 → 动作·W1179）=====",
           "本批号 %s（台账最新认领行·动工前先登记）· 命令可直接粘贴" % v["W"]]
    if matched.get("new-page"):
        out.append("新增页目标：%s" % v["target"])
    seen = set()
    for k in keys:
        spec = by_key[k]
        out.append("")
        out.append("【%s】依据：%s" % (spec["name"], spec["basis"]))
        for kind, text in spec["items"]:
            line = text.format(**v)
            if line in seen:
                continue
            seen.add(line)
            out.append(("  $ " if kind == "cmd" else "  · ") + line)
    out.append("")
    out.append("【收尾·各类共用】")
    for kind, text in _CHECKLIST_TAIL:
        line = text.format(**v)
        if line in seen:
            continue
        seen.add(line)
        out.append(("  $ " if kind == "cmd" else "  · ") + line)
    out.append("依据锚可用 Grep 在 pitfalls.md / AGENTS.md / CHANGELOG.md 中检索，防清单与源漂移。")
    out.append("=" * 60)
    return "\n".join(out)


def checklist_selftest():
    """四类命中 + 命令完整性自测（不含省略号 / 占位符 / 假批号）。"""
    cases = [
        ("new-page", [("A", "site/data/probe.html")]),
        ("new-gate", [("A", "scripts/check_probe.py"), ("M", "scripts/verify_delivery.py")]),
        ("shared-css", [("M", "site/system.css")]),
        ("stats-scope", [("M", "CHANGELOG.md"), ("M", "scripts/output/stats.json")]),
    ]
    w, n = current_batch_w(), next_batch_w()
    ok = 0
    for want, entries in cases:
        hits, matched = checklist_hits(entries)
        text = render_checklist(hits, entries, matched)
        bad = [t for t in ("...", "…", "（同路径）", "{W}", "{target}", "W0000") if t in text]
        # W1179 根因守卫：命令里的 --w 必须是本批号，不得出现「下一自由号」
        if n and n in text:
            bad.append("误用下一自由号 " + n)
        passed = want in hits and not bad and "py -3 scripts/verify_delivery.py --scope auto" in text
        print("%s  %-12s  命中=%s  禁忌残留=%s" % ("OK  " if passed else "FAIL", want, hits, bad))
        ok += int(passed)
    clean = checklist_hits([])[0] == []
    print("%s  干净工作树不误报 = %s" % ("OK  " if clean else "FAIL", clean))
    ok += int(clean)
    sep = bool(w and n and int(n[1:]) == int(w[1:]) + 1)
    print("%s  批号口径分离：本批 %s / 下一自由号 %s" % ("OK  " if sep else "FAIL", w, n))
    ok += int(sep)
    total = len(cases) + 2
    print("自测 %d/%d 通过" % (ok, total))
    return 0 if ok == total else 1


def render_task():
    entries = changed_entries()
    paths = [p for _, p in entries]
    hits = []
    for pat, tip in TASK_MAP:
        matched = [x for x in paths if re.search(pat, x)]
        if matched:
            joined = "、".join(matched[:3])
            hits.append("* " + tip + "\n      例：" + joined)
    out = ["===== 本次任务相关（按改动路径分类·agent_start --task）====="]
    if not paths:
        out.append("（工作树干净——无未提交改动；动手前可用 --checklist <类型|all> 主动查必跑清单）")
    out.extend(hits if hits else ["（改动未命中已知分类——按 AGENTS §7 快速上手路径走）"])
    out.append("通用必读：CLAUDE.md（宿主已加载）→ 交接「零、当前阻塞」→ 动手前 verify_delivery 全绿。")
    # W1179：变更类型 → 必跑清单（按改动路径自动分类；干净时提示手动查）
    ck_keys, ck_matched = checklist_hits(entries)
    out.append("")
    if ck_keys:
        out.append(render_checklist(ck_keys, entries, ck_matched))
    else:
        out.append("本次必跑清单：未命中四类变更；如需动手前查，用 --checklist <new-page|new-gate|"
                   "shared-css|stats-scope|all>")
    # W1148 b 方案：最小铁律集注入（恒真 ∪ 路径敏感·抽整条原文带回指锚）
    rules = minimal_rules(paths)
    if rules:
        out.append("")
        out.append("===== 最小铁律集（恒真 + 按 touches 敏感·共 %d 条·全文见 AGENTS §6）=====" % len(rules))
        out.extend(rules)
    out.append("=" * 60)
    return "\n".join(out)


def main():
    if "--checklist-selftest" in sys.argv:
        return checklist_selftest()
    if "--checklist" in sys.argv:
        i = sys.argv.index("--checklist")
        want = sys.argv[i + 1] if i + 1 < len(sys.argv) else "all"
        keys = [s["key"] for s in CHANGE_CHECKLISTS] if want == "all" else [want]
        print(render_checklist(keys, changed_entries()))
        return 0
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
