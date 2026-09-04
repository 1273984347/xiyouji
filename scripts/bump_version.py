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
  python scripts/bump_version.py --desc "W417 文档健康治理"   # 同时替换版本行主描述（W417 增强）

零依赖：仅标准库。幂等：重复运行不产生重复条目。

W417 增强（修复 W413/W414/W415 三次同模式踩坑）：
  1) --desc 替换版本行主描述（此前只改版本号+追加 W，主描述仍是旧 W，需手动补）
  2) 全文件 W001-W### 范围替换（README 开发者区/双索引等深处残留一次性清零）
  3) 页脚 3 个简单页脚（index/cross-time-danmaku/tag-cloud）自动同步
"""

import argparse
import datetime
import os
import re
import sys

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, ".."))
HTML = os.path.join(ROOT, "site", "dukou-engine.html")
AUX_VERSION_DOCS = [
    "README.md",
    "STRUCTURE.md",
    os.path.join("docs", "00-导读", "项目说明.md"),
]
FILE_INDEX = os.path.join(ROOT, "scripts", "output", "file-index.md")

# W417 增强：W 范围替换 + 页脚 3 个简单页脚同步
SYNC_DOCS = AUX_VERSION_DOCS + [FILE_INDEX,
                                os.path.join(ROOT, "交接文档.md"),
                                os.path.join(ROOT, "CHANGELOG.md"),
                                os.path.join(ROOT, "site", "index.html"),
                                os.path.join(ROOT, "site", "data", "cross-time-danmaku.html"),
                                os.path.join(ROOT, "site", "data", "tag-cloud.html")]


def _read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _write(p, c):
    with _w536_guard_open(p, "w", encoding="utf-8") as f:
        f.write(c)


def parse_footer():
    html = _read(HTML)
    m = re.search(r"v(\d+\.\d+\.\d+)\s+W(\d+)", html)
    if not m:
        print("ERROR 无法从 %s 解析 vX.Y.Z W### 页脚" % HTML)
        sys.exit(2)
    return m.group(1), "W" + m.group(2)


def bump_version_line(c, old_ver, new_ver, w, note, desc=None):
    """替换「当前版本」行：版本号 + 主描述（--desc）+ 确保含 W token。

    W500 增强：同时覆盖 "- **当前版本**："（项目说明次级版本行）——该行历史格式
    仅含版本号、无 W 后缀，故次级行只替换版本号，不追加 W token（防格式漂移）。
    """
    def repl(mt):
        line = mt.group(0)
        is_secondary = line.lstrip().startswith("- **")
        line = line.replace("v" + old_ver, "v" + new_ver)
        # 主描述替换（W417 增强）：把行首 "：W### 旧描述（…）" 换成新 W + desc（剥离 desc 的 W 前缀防重复）。
        # 仅匹配首个括号（[^）\n] 禁跨括号嵌套），且不带 \s*· 后缀——避免吞掉 "）— A1-A6 共 611 篇（…201 篇）·" 等后续内容（W417 实测修复）
        if desc and w not in line and not is_secondary:
            desc_clean = re.sub(r"^W\d{3}\s*", "", desc).strip()
            line = re.sub(
                r"([：:])\s*W\d{3}[^\n]*?（[^）\n]*?）",
                lambda m2: m2.group(1) + " " + w + " " + desc_clean,
                line,
                count=1,
            )
        if w not in line and not is_secondary:
            line = line.rstrip() + " + " + w + ("（" + note + "）" if note else "") + "\n"
        return line

    pat = r"^(?:> \**当前版本|-\s*\*\*当前版本\*\*)[^\n]*v" + re.escape(old_ver) + r"[^\n]*\n"
    return re.sub(pat, repl, c, flags=re.M)


def main():
    ap = argparse.ArgumentParser(description="降级六文档同步：辅助 4 份一键补齐")
    ap.add_argument("--version", help="目标版本号，如 v2.3.18（缺省读页脚）")
    ap.add_argument("--w", help="目标 W 号，如 W393（缺省读页脚）")
    ap.add_argument("--note", default="", help="里程碑一句话说明")
    ap.add_argument("--desc", default="", help="W417 增强：新版本行主描述（如 'W417 文档健康治理'）")
    args = ap.parse_args()

    if args.version and args.w:
        new_ver = args.version.lstrip("v")
        w = args.w if args.w.startswith("W") else "W" + args.w
    else:
        new_ver, w = parse_footer()

    note = args.note or w
    desc = args.desc or note
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

    old_w = str(int(w[1:]) - 1).zfill(3)
    changed = []

    # 0) W417 增强：全文件 W001-W### 范围替换 + 页脚 3 个 v/W 替换
    for p in SYNC_DOCS:
        c = _read(p)
        if not c:
            continue
        c2 = c
        # W001-W### 现役范围声明替换（W417 增强）：仅命中精确现役锚点，
        # 绝不触碰历史描述（"W001-W087 已归档"/"W001-W099 对应"/W414 段内旧范围）
        c2 = re.sub(r"W### ID（W001-W\d{3}）", "W### ID（W001-" + w + "）", c2)      # CHANGELOG 编号规则 + README 双索引
        c2 = re.sub(r"# 更新日志（W001-W\d{3}）", "# 更新日志（W001-" + w + "）", c2)  # README 目录树
        c2 = re.sub(r"正向时间线，W001-W\d{3}；", "正向时间线，W001-" + w + "；", c2)  # 交接文档 CHANGELOG 范围
        # 页脚简单格式（index/cross-time-danmaku/tag-cloud）：v2.3.30 · W415
        c2 = re.sub(r"v" + re.escape(old_ver) + r"\s*·\s*W" + old_w,
                    "v" + new_ver + " · " + w, c2)
        if c2 != c:
            _write(p, c2)
            changed.append(p)

    # 1) 三份版本文档：更新版本行 + 补 W token + 主描述（--desc）
    for d in AUX_VERSION_DOCS:
        p = os.path.join(ROOT, d)
        c = _read(p)
        if not c:
            continue
        new_c = bump_version_line(c, old_ver, new_ver, w, note, desc)
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
    print("提示（W417）：")
    print("  - site/dukou-engine.html 页脚为长链格式，需人工在头部插入 v%s %s 段" % (new_ver, w))
    print("  - 交接文档「Git HEAD」/版本号列表/接续编号（当前 W%s·下一 W%d）需人工核对" % (old_w, int(w[1:]) + 1))


if __name__ == "__main__":
    main()
