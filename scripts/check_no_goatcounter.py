#!/usr/bin/env python3
"""check_no_goatcounter.py — GoatCounter 退役防回退守卫（W806 建立·CI 侧接线）。

背景（W806 裁决）：GoatCounter 站点代码 1273984347 已失效（`fetch_gate_stats.py`
实测 HTTP 404「not found」，2026-09-30 断链至今未恢复），页面上的埋点脚本采不到
任何数据，却仍在每页加载并产生一次无效外域请求。W806 裁决「彻底退役」：
移除 234 页埋点标签、清 CSP connect-src 外域放行、退役注入器与自托管 count.js。
退役后若无机器防线，任何一次「顺手加回埋点」都会静默恢复一条外域链——本守卫
把该回退面关进笼子。

检查项（全过 exit 0，任一 FAIL exit 1）：
C1 页面无埋点标签：site/**/*.html 不含 `data-goatcounter`（注入器写入的形态）
C2 页面无外域放行：site/**/*.html 不含 `goatcounter.com`（含 CSP connect-src 残留）
C3 站点无追踪脚本：site/ 下不得存在文件名含 `goatcounter` 的文件（如自托管 count.js）
C4 工具无注入器：scripts/ 下不得存在文件名含 `goatcounter` 的脚本（如 inject_/remove_ 类）

口径说明：
- 扫描范围限「运行时面」（site/ + scripts/ 文件名），**不扫 docs/ 与 CHANGELOG**——
  历史记录与退役说明文档本就应保留对 GoatCounter 的文字引用，扫它们会把「记录事实」
  误判成「回退」。
- 判定用**具体形态**（`data-goatcounter` / `goatcounter.com`）而非裸词 `goatcounter`：
  退役口径的注释与说明（rum.js / visit-log.js 等）提到 GoatCounter 是合法且必要的。

跨平台断言纪律（pitfalls「latent 三问 + 双平台断言禁例」）：全部比对基于文件名字符串
与文件内容子串（大小写不敏感），零 os.name/盘符/大小写语义断言；负样本用系统临时
目录注入（合成树两平台同构·不触仓库），真实执行位=CI（Linux）与本地（Windows）同断言。

用法：
    python scripts/check_no_goatcounter.py             # 门禁模式
    python scripts/check_no_goatcounter.py --self-test # 注入式自测（1 正 4 负·不触仓库）

退出码：0 全过；1 有 FAIL；2 参数/环境错误。
"""

from __future__ import annotations

import argparse
import os
import sys

MARKER = "---- W806 守卫 GoatCounter 退役防回退："

# 判定用具体形态（大小写不敏感）：裸词 goatcounter 会误伤退役口径的注释说明
TAG_PATTERN = "data-goatcounter"
DOMAIN_PATTERN = "goatcounter.com"
# 文件名级判定：注入器 / 追踪脚本的命名共性词
FILENAME_PATTERN = "goatcounter"


def _iter_html(site_dir: str):
    for root, _dirs, files in os.walk(site_dir):
        for fn in sorted(files):
            if fn.lower().endswith(".html"):
                yield os.path.join(root, fn)


def _iter_files(base_dir: str):
    for root, _dirs, files in os.walk(base_dir):
        for fn in sorted(files):
            yield os.path.join(root, fn)


def _is_ignored(path: str) -> bool:
    """守卫自身与 Python 字节码产物不参与判定。

    - 自身：本守卫文件名含 `goatcounter`（守卫对象即该词），须排除，否则自指误报。
      按**文件名**排除而非仅 realpath——同名副本（如测试合成树里的拷贝）同属守卫
      形态，不该被判成注入器。
    - `__pycache__/*.pyc`：已删脚本的编译残留（gitignore 内），非源码实体。
    """
    if os.path.basename(path) == os.path.basename(__file__):
        return True
    if os.path.realpath(path) == os.path.realpath(__file__):
        return True
    return "__pycache__" in os.path.normpath(path).split(os.sep)


def scan(site_dir: str, scripts_dir: str) -> list[str]:
    """返回 FAIL 明细列表（空列表 = 全过）。纯函数形态：--self-test 复用同一判据。"""
    fails: list[str] = []

    # C1 / C2：页面内容（埋点标签 + 外域放行，含 CSP connect-src 残留）
    for path in _iter_html(site_dir):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                content = f.read().lower()
        except OSError as exc:
            fails.append("C1 页面读取失败：%s（%s）" % (path, exc))
            continue
        if TAG_PATTERN in content:
            fails.append("C1 页面仍含埋点标签（%s）：%s" % (TAG_PATTERN, path))
        if DOMAIN_PATTERN in content:
            fails.append("C2 页面仍放行外域（%s）：%s" % (DOMAIN_PATTERN, path))

    # C3：site/ 下不得残留追踪脚本文件
    for path in _iter_files(site_dir):
        if _is_ignored(path):
            continue
        if FILENAME_PATTERN in os.path.basename(path).lower():
            fails.append("C3 站点残留追踪脚本：%s" % path)

    # C4：scripts/ 下不得残留注入器
    for path in _iter_files(scripts_dir):
        if _is_ignored(path):
            continue
        if FILENAME_PATTERN in os.path.basename(path).lower():
            fails.append("C4 工具残留注入器：%s" % path)

    return fails


def _self_test() -> int:
    """注入式自测：1 正 4 负，合成树用系统临时目录，不触仓库。"""
    import shutil
    import tempfile

    tmp = tempfile.mkdtemp(prefix="no_goatcounter_selftest_")
    ok = True
    try:
        site = os.path.join(tmp, "site")
        scripts = os.path.join(tmp, "scripts")
        os.makedirs(os.path.join(site, "static", "js"))
        os.makedirs(scripts)
        page = os.path.join(site, "index.html")
        with open(page, "w", encoding="utf-8", newline="\n") as f:
            f.write("<html><head></head><body>ok</body></html>\n")

        def case(label: str, expect: list[str]) -> None:
            nonlocal ok
            got = scan(site, scripts)
            hit = [g for g in got if g.startswith(tuple(expect))] if expect else []
            passed = (not got) if not expect else bool(hit)
            print("  %s %s" % ("PASS" if passed else "FAIL", label))
            if not passed:
                ok = False
                print("    期望命中前缀 %r·实得 %r" % (expect, got))

        # 正样本：干净树 → 无 FAIL
        case("clean-tree-must-pass", [])
        # 负样本 1：埋点标签
        with open(page, "a", encoding="utf-8", newline="\n") as f:
            f.write('<script data-goatcounter="https://x.goatcounter.com/count" async '
                    'src="static/js/goatcounter.js"></script>\n')
        case("tag-must-fail-C1", ["C1"])
        # 负样本 2：外域放行残留（CSP connect-src）
        with open(page, "w", encoding="utf-8", newline="\n") as f:
            f.write("<meta http-equiv=\"Content-Security-Policy\" "
                    "content=\"connect-src 'self' https://1273984347.goatcounter.com\">\n")
        case("domain-must-fail-C2", ["C2"])
        # 负样本 3：站点残留追踪脚本文件
        with open(page, "w", encoding="utf-8", newline="\n") as f:
            f.write("<html></html>\n")
        with open(os.path.join(site, "static", "js", "goatcounter.js"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write("// tracker\n")
        case("tracker-file-must-fail-C3", ["C3"])
        os.remove(os.path.join(site, "static", "js", "goatcounter.js"))
        # 负样本 4：工具残留注入器
        with open(os.path.join(scripts, "inject_goatcounter.py"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write("# injector\n")
        case("injector-must-fail-C4", ["C4"])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if ok:
        print("SELF_TEST_OK")
        return 0
    print("SELF_TEST_FAIL")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description="GoatCounter 退役防回退守卫（W806）")
    ap.add_argument("--self-test", action="store_true", help="注入式自测（不触仓库）")
    args = ap.parse_args()

    if args.self_test:
        return _self_test()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    site_dir = os.path.join(root, "site")
    scripts_dir = os.path.join(root, "scripts")
    if not os.path.isdir(site_dir) or not os.path.isdir(scripts_dir):
        print("环境错误：未找到 site/ 或 scripts/ 目录", file=sys.stderr)
        return 2

    fails = scan(site_dir, scripts_dir)
    print(MARKER + ("%d FAIL" % len(fails) if fails else "0 FAIL（全站零 GoatCounter 引用）"))
    for msg in fails[:20]:
        print("  FAIL", msg)
    if len(fails) > 20:
        print("  ...（其余 %d 条略）" % (len(fails) - 20))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
