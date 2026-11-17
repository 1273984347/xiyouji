#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_check_json_copies.py — 兼容入口（W563/A-3 旧名）→ 委托给 scripts/check_json_copies.py。

W1265 批一：第 81 槽（页面引用 → 已部署 闭合性）落地后，门禁挂载点须用 check_*.py
  命名（第 42/45 槽按 check_[a-z0-9_]+\.(py|js) 扫描挂载脚本·下划线前缀会被正则截断
  成 check_json_copies.py 而误判「引用不存在的门禁脚本」）。
  故：实现体在 scripts/check_json_copies.py；本文件保留为**向后兼容入口**
  （旧脚本清单/文档仍引用本名），行为完全一致。
用法：py -3 scripts/_check_json_copies.py [--closure-only|--strict|--report|--self-test]
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

TARGET = Path(__file__).resolve().parent / "check_json_copies.py"

if __name__ == "__main__":
    sys.argv[0] = str(TARGET)
    runpy.run_path(str(TARGET), run_name="__main__")
