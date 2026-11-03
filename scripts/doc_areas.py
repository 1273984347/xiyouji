#!/usr/bin/env python3
"""doc_areas.py — A1-A6 内容板块目录与计数口径的单一事实源（W728 重构提取）。

背景：verify_delivery.py（A1-A6 计数门禁）与 sync_docs.py（rule_stats 磁盘实数期望）
各自维护一份六板块目录表与 .md 计数函数（sync_docs.py 已于 W793 退役·一致性职责由
check_doc_sync 承接·本段为 W728 提取时的历史背景）——sync_docs 源码注释即自证「与
verify_delivery._count_content_md 同口径」。双份手工表的漂移风险：任一侧改目录或
计数口径，另一侧静默失配（A1-A6 计数门禁/统计期望值同时失真且无机器防线）。

本模块收敛口径层（W728）：
  - AREA_DIRS：六板块相对目录（唯一事实源·顺序=A1..A6）
  - count_content_md()：板块顶层 .md 计数，排除 README.md（非正文）；目录缺失返回 -1
展示标签（「A1 逐回解读」/「A1」短键）属呈现层，由各消费方自行组合，不入本模块。

零依赖（仅标准库）。消费方以 `python scripts/xxx.py` 直跑时 sys.path[0]=scripts/
可自动导入；pytest 侧由 tests/conftest.py 注入 scripts/ 同保障。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # scripts/.. = 项目根

# 六板块相对目录（顺序恒定=A1..A6·与 docs/ 实际目录一一对应）
AREA_DIRS = (
    os.path.join("docs", "01-全书逐回解读"),    # A1 逐回解读
    os.path.join("docs", "06-个人随笔"),        # A2 个人随笔
    os.path.join("docs", "02-人物深度分析"),    # A3 人物分析
    os.path.join("docs", "03-主题与情节专题"),  # A4 主题专题
    os.path.join("docs", "04-文化与历史背景"),  # A5 文化背景
    os.path.join("docs", "05-诗词歌赋"),        # A6 诗词歌赋
)


# W1110（P-3 L2）：板块内容篇数的**异源复算**口径——单一事实源（C10 与 agent_start 共用）
#
# 背景：第 31 门禁 C10（W1105 立）用**独立实现**复算 7 个板块的内容篇数并与
# `stats.json` 对账（排除集按大小写不敏感）；W1104 批的 `agent_start.py` 四类告警里
# 留了「口径一致性待异源复算（C10）落地后接入」的挂账 ⇒ 本函数把 C10 的复算式
# **抽成共享单一事实源**，让 C10 与开局摘要**同源复用**（避免两处实现漂移）。
#
# 排除集口径（与 stats.py 的 `_sec` 同口径）：README.md / index.md（大小写不敏感）
# ——README 与 INDEX 皆为生成件，两种写法都排除。

#: (板块目录相对路径, stats.json 键) ——顺序与 C10 判据一致
BOARD_COUNT_SPEC = (
    ("docs/06-个人随笔", "a2_docs"),
    ("docs/02-人物深度分析", "a3_docs"),
    ("docs/04-文化与历史背景", "a5_docs"),
    ("docs/05-诗词歌赋", "a6_docs"),
    ("docs/07-学以致用", "learn_docs"),
    ("docs/08-提升认知", "cognition_docs"),
    ("docs/09-精神塑造", "spirit_docs"),
)

#: 排除的生成件名（小写形态·比较时统一 lower()）
BOARD_EXCLUDE = ("readme.md", "index.md")


#: stats 键 → 板块中文名（供判据消息可读性；不改 BOARD_COUNT_SPEC 结构·避免影响既有消费方）
BOARD_KEY_NAMES = {
    "a2_docs": "06-个人随笔",
    "a3_docs": "02-人物深度分析",
    "a5_docs": "04-文化与历史背景",
    "a6_docs": "05-诗词歌赋",
    "learn_docs": "07-学以致用",
    "cognition_docs": "08-提升认知",
    "spirit_docs": "09-精神塑造",
}


def count_board_content(board_dir):
    """板块**顶层**内容 .md 篇数（排除 README.md / index.md·大小写不敏感）。

    目录不存在返回 -1（与 count_content_md 的「缺失即 -1」口径一致）。
    这是 C10 与 agent_start L2 告警**共用**的复算式——两处必须同口径，
    否则同一份 stats.json 会在门禁与开局摘要给出不同结论。
    """
    p = os.path.join(ROOT, board_dir)
    if not os.path.isdir(p):
        return -1
    return sum(1 for fn in os.listdir(p)
               if fn.endswith(".md") and fn.lower() not in BOARD_EXCLUDE)


def recount_boards():
    """返回 {stats 键: 实算篇数}（仅含目录存在的板块）。"""
    out = {}
    for board_dir, key in BOARD_COUNT_SPEC:
        n = count_board_content(board_dir)
        if n >= 0:
            out[key] = n
    return out


def board_count_mismatches(stats):
    """返回 [(stats 键, 实算, 存值)] —— 异源复算与 stats.json 不一致的项。

    stats 非 dict 或键缺 value 时跳过（不可比项不判）。
    """
    out = []
    if not isinstance(stats, dict):
        return out
    real = recount_boards()
    for key, computed in sorted(real.items()):
        ent = stats.get(key)
        if not isinstance(ent, dict) or "value" not in ent:
            continue
        try:
            stored = int(ent["value"])
        except (TypeError, ValueError):
            continue
        if stored != computed:
            out.append((key, computed, stored))
    return out


def count_content_md(area_dir):
    """统计板块顶层 .md 文件数，排除 README.md（非正文）；目录缺失返回 -1。

    与重构前 verify_delivery._count_content_md / sync_docs._count_content_md
    逐字节同口径（两侧原实现一致·W728 收敛为本函数）。
    """
    p = os.path.join(ROOT, area_dir)
    if not os.path.isdir(p):
        return -1
    return sum(1 for fn in os.listdir(p)
               if fn.endswith(".md") and fn.lower() != "readme.md")
