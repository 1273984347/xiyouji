#!/usr/bin/env python3
"""check_screenshot_scope.py — 截图审查 scope 判定（单一事实源·W1126 建）

背景（诊断实证·PR #130）：
  收官链每批必改 `site/en/search.html`（版本面推进 + 搜索索引刷新），
  而该文件在原 workflow 内联 case 的判定顺序里：
    · 不在页脚版本号免审名单（site/index.html / site/dukou-engine.html /
      site/data/cross-time-danmaku.html / site/data/tag-cloud.html）
    · `site/*`（bash case 的 `*` 跨 `/`）在 `site/data/*` 之后命中 ⇒ 掉进 full 分支
    ⇒ 掉进「未知路径 ⇒ 保守全量」兜底 ⇒ **为 2 行零视觉改动付全站 88 页截图代价**

本脚本把原 case 顺序逐条翻译为 Python 单一事实源，并落实两条修法：
  · **B**：新增 `site/en/*` ⇒ targeted（截该页 + 入口页·保留该页视觉审查强度·只削范围）
  · **C**：内容级免审判据——变更行集合 ⊆ {CSP 哈希行, 内嵌索引数据行} ⇒ 免审
    （白名单式最保守：任一未识别行变化即不 skip ⇒ 判据强度不降）

判定三态（与 workflow 的 GITHUB_OUTPUT 键一一对应）：
  needed     bool  —— 是否需要跑审查
  scope      str   —— skip / targeted / full
  only_pages str   —— targeted 时的截页清单（file:dir 逗号分隔）
  changed_names str —— targeted 时的变更页文件名清单（供 chart-gates --only）

用法：
  py -3 scripts/check_screenshot_scope.py --files-from "<git diff 输出>"
  py -3 scripts/check_screenshot_scope.py --changed-lines "<file>=<行号,行号,...>"
  py -3 scripts/check_screenshot_scope.py --self-test
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- 原 workflow case 顺序的 Python 翻译（* 不跨 /）----
FOOTER_EXEMPT = (
    "site/dukou-engine.html",
    "site/index.html",
    "site/data/cross-time-danmaku.html",
    "site/data/tag-cloud.html",
)
NONVISUAL_PREFIXES = (
    "scripts/", "docs/", "source/", "dataset/", "references/", "timeline/",
    "tools/", "mcp-server/", "xiyouji-agent-web/", "tests/",
    ".github/",
)
NONVISUAL_NAMES = (
    "Makefile", "CITATION.cff", "CONTRIBUTING.md", "pyproject.toml",
    "pytest.ini", "mypy.ini", ".gitignore", ".pre-commit-config.yaml",
    ".eslintrc.json", "eslint.config.mjs", ".env.example",
)
FULL_EXACT = (
    "scripts/batch_screenshots.js",
    "scripts/slice_screenshots.py",
    "scripts/detect_unwrapped_tables.py",
    ".github/workflows/screenshot-review.yml",
)

# 搜索页：内容级免审白名单行特征
CSP_RE = re.compile(r'http-equiv="Content-Security-Policy"')
INDEX_RE = re.compile(r"^const\s+SITE_SEARCH_INDEX_(ZH|EN)\s*=")


def _under(path, prefix):
    """等价于 bash case 的 `prefix/*`。

    **bash 的 case glob 中 `*` 匹配任意串（含 `/`）**——实测确认：
    `site/data/*` 命中 `site/data/x/y.html`、`site/*` 命中 `site/en/search.html`。
    ⇒ 本函数按「前缀 + 至少一个字符」判定，**不排除中间斜杠**。
    """
    if not path.startswith(prefix):
        return False
    rest = path[len(prefix):]
    return bool(rest)


def scope_of(path):
    """返回 ('skip'|'targeted'|'full', extra) —— extra 为 targeted 时的 dir 片段。"""
    if path in FOOTER_EXEMPT:
        return "skip", None
    if _under(path, "site/data/json"):
        return "skip", None
    if _under(path, "site/data"):
        return "targeted", "site/data"
    # B 修法：EN 子目录定向（原会掉进下方 site/* 的 full 兜底）
    if _under(path, "site/en"):
        return "targeted", "site/en"
    if _under(path, "site") or _under(path, "assets"):
        return "full", None
    if path in FULL_EXACT:
        return "full", None
    if path.endswith(".md") or path.startswith(NONVISUAL_PREFIXES) or path in NONVISUAL_NAMES:
        return "skip", None
    return "full", None


def is_search_page(path):
    return path in ("site/data/search.html", "site/en/search.html")


def content_only_search_change(path, changed_lines):
    """C 修法：变更行是否全部落在 {CSP 哈希行, 内嵌索引数据行} 内。

    changed_lines: 该文件被改动的行号集合（1-based）。
    任一不在白名单行集合内 ⇒ False（不豁免）。
    """
    if not is_search_page(path):
        return False
    try:
        with open(os.path.join(ROOT, path), encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return False
    allowed = set()
    for i, ln in enumerate(lines, start=1):
        if CSP_RE.search(ln) or INDEX_RE.match(ln):
            allowed.add(i)
    if not changed_lines:
        return False
    return set(changed_lines).issubset(allowed)


def _csp_index_lines(path):
    """动态定位搜索页的 CSP 哈希行与内嵌索引行行号（自测/单测夹具专用）。

    W1137 根修：夹具此前硬编码 [5, 1275]/[5, 1291]——任何 head 行数变化都会平移行号
    （favicon 三行注入实证断一次·判据脆弱特征）；改由与判据同源的正则动态定位，
    夹具语义不变（正例 = 变更行恰为 CSP+索引行）。第三返回值 = 非 CSP/索引的稳定
    内容行（title 行）·供「未识别行」负样本使用。
    """
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        lines = f.read().splitlines()
    csp = next(i for i, ln in enumerate(lines, 1) if CSP_RE.search(ln))
    idx = next(i for i, ln in enumerate(lines, 1) if INDEX_RE.match(ln))
    other = next(i for i, ln in enumerate(lines, 1)
                 if ln.lstrip().startswith("<title>") and i not in (csp, idx))
    return csp, idx, other


def decide(files, changed_map=None):
    """files: 改动文件列表；changed_map: {path: [行号]}（可选·用于 C 修法）。

    返回 (needed, scope, only_pages, changed_names)。
    """
    changed_map = changed_map or {}
    needed = False
    scope = "skip"
    only = ["index.html:site", "dashboard.html:site"]
    names = set()

    for f in files:
        # C 修法（优先级最高）：搜索页仅内容级变更（内嵌索引数据行 / CSP 哈希行）
        # ⇒ 无论该路径在 scope 判定里是 targeted 还是 full，一律免审。
        if content_only_search_change(f, changed_map.get(f, [])):
            continue
        sc, extra = scope_of(f)
        if sc == "skip":
            continue
        needed = True
        if sc == "full":
            scope = "full"
        else:  # targeted
            if scope != "full":
                scope = "targeted"
                only.append("%s:%s" % (os.path.basename(f), extra))
            m = re.match(r"^site/.*\.html$", f)
            if m:
                names.add(os.path.basename(f))

    if not needed:
        return False, "skip", "", ""
    return True, scope, ",".join(only), ",".join(sorted(names))


def _self_test():
    ok = True

    def check(label, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("%s  %s" % ("PASS" if good else "FAIL", label))

    # 现状语义（改造前应保持不变）
    check("页脚免审页 ⇒ skip", scope_of("site/index.html")[0], "skip")
    check("部署数据副本 ⇒ skip", scope_of("site/data/json/x.json")[0], "skip")
    check("data 页面（非页脚）⇒ targeted", scope_of("site/data/search.html")[0], "targeted")
    check("data 目录下的页脚页 ⇒ skip（页脚名单优先）", scope_of("site/data/cross-time-danmaku.html")[0], "skip")
    check("未知路径 ⇒ full（兜底不弱化）", scope_of("weird/thing.bin")[0], "full")
    check("非可视化 ⇒ skip", scope_of("docs/00-导读/x.md")[0], "skip")
    check("审查脚本自身 ⇒ full", scope_of("scripts/batch_screenshots.js")[0], "full")

    # B 修法
    check("EN 搜索页 ⇒ targeted（B 修法）", scope_of("site/en/search.html")[0], "targeted")
    check("EN 其他页 ⇒ targeted（B 修法）", scope_of("site/en/other.html")[0], "targeted")

    # 整体判定
    n1, s1, _, _ = decide(["docs/00-导读/W批次编号对账表.md"])
    check("纯文档改动 ⇒ skip", (n1, s1), (False, "skip"))
    n2, s2, o2, _ = decide(["site/en/search.html"])
    check("EN 搜索页单独改 ⇒ targeted", (n2, s2), (True, "targeted"))
    n3, s3, _, _ = decide(["site/index.html", "site/dukou-engine.html"])
    check("页脚页单独改 ⇒ skip", (n3, s3), (False, "skip"))
    n4, s4, _, _ = decide(["site/other.html"])
    check("site 顶层页 ⇒ full", (n4, s4), (True, "full"))
    n5, s5, _, _ = decide(["assets/x.png"])
    check("assets ⇒ full", (n5, s5), (True, "full"))

    # C 修法（正例 + 负例）——行号由 _csp_index_lines 动态定位（W1137 根修：硬编码行号被
    # favicon head 注入平移断过一次·夹具改与判据同源正则取行）
    csp_en, idx_en, other_en = _csp_index_lines("site/en/search.html")
    csp_zh, idx_zh, _ = _csp_index_lines("site/data/search.html")
    c_ok = content_only_search_change("site/en/search.html", [csp_en, idx_en])
    check("搜索页仅 CSP + 索引行变更 ⇒ 豁免（正例）", c_ok, True)
    c_bad = content_only_search_change("site/en/search.html", [csp_en, idx_en, other_en])
    check("搜索页含未识别行变更 ⇒ 不豁免（负样本）", c_bad, False)
    c_bad2 = content_only_search_change("site/en/search.html", [other_en])
    check("搜索页仅布局行变更 ⇒ 不豁免（负样本）", c_bad2, False)
    c_non = content_only_search_change("site/en/other.html", [csp_en])
    check("非搜索页不适用内容级豁免（负样本）", c_non, False)
    n6, s6, _, _ = decide(["site/en/search.html"], {"site/en/search.html": [csp_en, idx_en]})
    check("EN 搜索页内容级豁免后 ⇒ 免审（正例）", (n6, s6), (False, "skip"))
    n6b, s6b, _, _ = decide(["site/data/search.html"], {"site/data/search.html": [csp_zh, idx_zh]})
    check("ZH 搜索页内容级豁免后 ⇒ 免审（正例·对称）", (n6b, s6b), (False, "skip"))
    n7, s7, _, _ = decide(["site/en/search.html"], {"site/en/search.html": [csp_en, idx_en, other_en]})
    check("含未识别行 ⇒ 降级 targeted（负样本）", (n7, s7), (True, "targeted"))

    print("---- scope 判据自测：%s ----" % ("全过" if ok else "存在失败"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="截图审查 scope 判定（单一事实源）")
    ap.add_argument("--files-from", help="改动文件列表（每行一个）")
    ap.add_argument("--changed-lines", help="path=行号,行号,...（用于内容级豁免）")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return _self_test()

    files = []
    if args.files_from:
        if os.path.isfile(args.files_from):
            with open(args.files_from, encoding="utf-8") as f:
                files = [x.strip() for x in f if x.strip()]
        else:
            files = [x.strip() for x in args.files_from.splitlines() if x.strip()]

    changed_map = {}
    if args.changed_lines:
        for item in args.changed_lines.split(";"):
            if "=" not in item:
                continue
            path, nums = item.split("=", 1)
            changed_map[path.strip()] = [int(x) for x in nums.split(",") if x.strip().isdigit()]

    needed, scope, only, names = decide(files, changed_map)
    print("needed=%s" % ("true" if needed else "false"))
    print("scope=%s" % scope)
    if only:
        print("only_pages=%s" % only)
    if names:
        print("changed_names=%s" % names)
    return 0


if __name__ == "__main__":
    sys.exit(main())
