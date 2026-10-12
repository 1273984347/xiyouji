#!/usr/bin/env python3
"""doc_areas.py — A1-A6 内容板块目录与计数口径的单一事实源（W728 重构提取）。

背景：verify_delivery.py（A1-A6 计数门禁）与 sync_docs.py（rule_stats 磁盘实数期望）
各自维护一份六板块目录表与 .md 计数函数——sync_docs 源码注释即自证「与
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
