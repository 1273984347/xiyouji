"""xiyouji_analysis — 《详解西游记》分析方法工具包（B-7 · W658）

将可视化站点 scripts/ 下的 A-H 类目分析脚本以 pip 包形式分发给研究者，
用于对任意《西游记》文本语料复现同一套分析（词频/共现/情感/术语 NLP 等）。

脚本来源：仓库 scripts/A-H 类目（单一事实源），由 scripts/package_analysis_sync.py
同步进 analyses/ 目录（保留类目结构·非 _ 前缀脚本）。同步时点见 SYNC_MANIFEST。
"""

from __future__ import annotations

from pathlib import Path

__version__ = "0.1.0"


def analyses_root() -> str:
    """返回 analyses 数据目录的文件系统路径（subprocess 执行用）。"""
    return str(Path(__file__).resolve().parent / "analyses")
