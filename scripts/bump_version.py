#!/usr/bin/env python3
"""
bump_version.py — 降级六文档同步（W393）的辅助同步工具

每次工程 W### 不再手工同步 README/STRUCTURE/项目说明/file-index 四份辅助文档
（它们已降级为 WARN 不阻断）。在发布里程碑（或页脚版本前进）时，跑一次本脚本
把辅助 4 份补齐到 site/dukou-engine.html 页脚当前的 v / W，消除 verify_delivery 的 WARN。

用法：
  python scripts/bump_version.py                 # 自动从 site/dukou-engine.html 读 v/W，note 取 W 号
  python scripts/bump_version.py --note "W393 降级六文档同步"
  python scripts/bump_version.py --version v2.3.18 --w W393 --note "发布说明"

零依赖：仅标准库。幂等：重复运行不产生重复条目。
"""

import argparse
import datetime
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, ".."))
HTML = os.path.join(ROOT, "site", "dukou-engine.html")
AUX_VERSION_DOCS = [
    "README.md",
    "STRUCTURE.md",
    os.path.join("docs", "00-导读", "项目说明.md"),
]
FILE_INDEX = os.path.join(ROOT, "scripts", "output", "file-index.md")


def _read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _write(p, c):
    with open(p, "w", encoding="utf-8") as f:
        f.write(c)


def parse_footer():
    html = _read(HTML)
    m = re.search(r"v(\d+\.\d+\.\d+)\s+W(\d+)", html)
    if not m:
        print("ERROR 无法从 %s 解析 vX.Y.Z W### 页脚" % HTML)
        sys.exit(2)
    return m.group(1), "W" + m.group(2)


def bump_version_line(c, old_ver, new_ver, w, note):
    """替换「当前版本」行中的版本号，并确保含 W token（缺失则追加）。"""
    def repl(mt):
        line = mt.group(0)
        line = line.replace("v" + old_ver, "v" + new_ver)
        if w not in line:
            line = line.rstrip() + " + " + w + ("（" + note + "）" if note else "") + "\n"
        return line

    return re.sub(
        r"^> \**当前版本[^\n]*v" + re.escape(old_ver) + r"[^\n]*\n",
        repl,
        c,
        flags=re.M,
    )


def main():
    ap = argparse.ArgumentParser(description="降级六文档同步：辅助 4 份一键补齐")
    ap.add_argument("--version", help="目标版本号，如 v2.3.18（缺省读页脚）")
    ap.add_argument("--w", help="目标 W 号，如 W393（缺省读页脚）")
    ap.add_argument("--note", default="", help="里程碑一句话说明")
    args = ap.parse_args()

    if args.version and args.w:
        new_ver = args.version.lstrip("v")
        w = args.w if args.w.startswith("W") else "W" + args.w
    else:
        new_ver, w = parse_footer()

    note = args.note or w
    today = datetime.date.today().isoformat()

    # 从某份辅助文档的「当前版本」行推断旧版本号
    old_ver = None
    for d in AUX_VERSION_DOCS:
        m = re.search(r"当前版本\s+v(\d+\.\d+\.\d+)", _read(os.path.join(ROOT, d)))
        if m:
            old_ver = m.group(1)
            break
    if not old_ver:
        print("ERROR 无法推断旧版本号（辅助文档缺少「当前版本 vX.Y.Z」）")
        sys.exit(2)

    changed = []

    # 1) 三份版本文档：更新版本行 + 补 W token
    for d in AUX_VERSION_DOCS:
        p = os.path.join(ROOT, d)
        c = _read(p)
        if not c:
            continue
        new_c = bump_version_line(c, old_ver, new_ver, w, note)
        if new_c != c:
            _write(p, new_c)
            changed.append(d)

    # 2) file-index.md：补版本说明 + 追加里程碑段（含 v + W，满足辅助门禁）
    fi = _read(FILE_INDEX)
    if ("v" + new_ver) not in fi:
        fi = fi.rstrip() + "\n\n> 当前版本 v%s（%s）\n" % (new_ver, today)
        changed.append(FILE_INDEX)
    header = "\n## %s %s（%s）\n\n| 文件 | W | 说明 |\n|---|---|---|\n" % (w, note, today)
    if ("## %s " % w) not in fi:
        fi = fi.rstrip() + "\n" + header
        _write(FILE_INDEX, fi)
        if FILE_INDEX not in changed:
            changed.append(FILE_INDEX)

    print("已同步辅助文档：")
    for f in changed:
        print("  - " + f)
    if not changed:
        print("  （辅助文档均已是最新 v%s %s，无改动）" % (new_ver, w))


if __name__ == "__main__":
    main()
