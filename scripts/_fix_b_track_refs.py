#!/usr/bin/env python3
"""B 轨著录错误修复（2026-09-27 用户裁决执行）。

修两处经外部三源核验确认的错误：
  ① [2] 作者「蒲安迪」→「浦安迪」（Andrew H. Plaks 通行中文名）
  ② [4] 书名《设计学概论》→《艺术设计概论》（李砚祖 2009 湖北美术出版社实书名）
覆盖面：装饰投稿版/匿名稿 md×2 + Zotero 导出脚本（数据源，改后重导出 JSON）。
每处断言唯一命中；任一未命中原样报错退出。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    ROOT / "docs" / "S4-学术投稿" / "装饰投稿" / "学术论文B轨-新中式数字雅集-装饰投稿版.md": [
        ("蒲安迪", "浦安迪"),
        ("李砚祖：《设计学概论》", "李砚祖：《艺术设计概论》"),
    ],
    ROOT / "docs" / "S4-学术投稿" / "装饰投稿" / "学术论文B轨-新中式数字雅集-匿名稿.md": [
        ("蒲安迪", "浦安迪"),
        ("李砚祖：《设计学概论》", "李砚祖：《艺术设计概论》"),
    ],
    ROOT / "scripts" / "_w607_zotero_export.py": [
        ('"literal": "蒲安迪"', '"literal": "浦安迪"'),
        ('"title": "设计学概论"', '"title": "艺术设计概论"'),
    ],
}


def main() -> int:
    for path, pairs in FILES.items():
        t = path.read_text(encoding="utf-8")
        for old, new in pairs:
            n = t.count(old)
            assert n == 1, "%s: '%s' count=%d (expect 1)" % (path.name, old, n)
            t = t.replace(old, new)
        path.write_text(t, encoding="utf-8")
        print("ok:", path.name)
    # 验证输出
    for path in list(FILES)[:2]:
        t = path.read_text(encoding="utf-8")
        assert "蒲安迪" not in t and "设计学概论" not in t
        assert "浦安迪" in t and "艺术设计概论" in t
        print("verified:", path.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())