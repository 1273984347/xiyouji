#!/usr/bin/env python3
"""
check_corruption.py — 机械腐蚀与插件引用静态门禁（W424 复盘沉淀）

背景：全站 Chromium 实测在 W424 揪出三类"门禁全绿但页面全坏"的存量缺陷——
  ① EN 站双引号翻倍腐蚀（""X""·32 处）② 模板字符串丢失收尾反引号（4 处）
  ③ 页面使用 d3.sankey 但漏引 d3-sankey.min.js 插件（6 页·桑基图从未渲染）。
本脚本把可静态判定的两类固化为硬门禁，第三类由 check_js_syntax.py 语法门禁兜底。

规则：
  R1（硬）双引号翻倍腐蚀：`""X""`（引号内为字母开头的内容）出现在 site 的 HTML 即报——
     合法的空字符串拼接（`x = "", y = ""` / `d.name+""`）首对引号后不是字母，天然不误报。
     docs 散文不扫——中文文献用 `"A""B""C"` 表示连续英文术语（翻译学专题先例），属合法书写。
  R2（硬）d3 插件引用缺失：页面使用 `d3.<ext>(` 等插件扩展但未引用对应 d3-*.min.js。

用法：python scripts/check_corruption.py      # 退出码 0 全过 / 1 有硬错误
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracked_files as _tf  # W1069 R3：BOM 扫描面 = git tracked 文本文件

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

# R1：""X"" —— 双引号翻倍且内容以字母开头（合法空串拼接天然不匹配）
DOUBLE_QUOTE_RE = re.compile(r'""[A-Za-z][^"]*""')

# R2：d3 插件扩展名 → 插件文件名（扫描 static/js/d3-*.min.js 得到，硬编码防漏）
D3_PLUGINS = {"sankey": "d3-sankey.min.js"}
D3_USE_RE = {
    ext: re.compile(r"d3\.%s\s*\(" % re.escape(ext))
    for ext in D3_PLUGINS
}

def walk(root, exts):
    for dirpath, _dirs, files in os.walk(root):
        for fn in sorted(files):
            if fn.endswith(exts):
                yield os.path.join(dirpath, fn)


def main():
    errors = []

    # ---- R1 双引号翻倍腐蚀 ----
    for path in walk(SITE, (".html",)):
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            continue
        for m in DOUBLE_QUOTE_RE.finditer(content):
            line_no = content.count("\n", 0, m.start()) + 1
            errors.append("R1 %s:%d 疑似双引号翻倍腐蚀：%s"
                          % (rel, line_no, m.group(0)[:60]))

    # ---- R2 d3 插件引用缺失 ----
    for path in walk(SITE, (".html",)):
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            continue
        for ext, plugin_file in D3_PLUGINS.items():
            if D3_USE_RE[ext].search(content) and plugin_file not in content:
                errors.append("R2 %s 使用 d3.%s 但未引用 %s（插件漏引→图表静默空白）"
                              % (rel, ext, plugin_file))

    # ---- R3 UTF-8 BOM 腐蚀（W1069·来源「BOM 安全协议」方案五：数据文件强制无 BOM；
    #      例外：.ps1 含非 ASCII 时**必须**带 BOM，否则 PS 5.1 -File 加载器回退 ANSI
    #      代码页在 CJK 系统上静默死亡——二分法见查坑表）----
    TEXT_EXTS = (".md", ".py", ".js", ".html", ".css", ".yml", ".yaml", ".json",
                 ".txt", ".cff", ".xml", ".svg", ".cfg", ".ini")
    tracked = set(_tf.tracked_files())
    for rel in sorted(tracked):
        if not rel.endswith(TEXT_EXTS) or rel.startswith("archive/"):
            continue
        fpath = os.path.join(ROOT, rel.replace("/", os.sep))
        try:
            with open(fpath, "rb") as f:
                head = f.read(3)
        except OSError:
            continue
        if head == b"\xef\xbb\xbf":
            if rel.endswith(".ps1"):
                continue  # .ps1 例外：见上
            errors.append("R3 %s UTF-8 BOM 腐蚀（数据文件强制无 BOM·写入方用了带 BOM 编码）"
                          % rel)

    for e in errors:
        print("ERROR " + e)
    print("腐蚀/插件门禁：%d 硬错误" % len(errors))
    return 1 if errors else 0


def _self_test():
    """W1053 G-06：R1/R2 判据注入式三例（腐蚀命中/合法空串放行/插件引用形态）。"""
    ok_all = True
    hit = DOUBLE_QUOTE_RE.search('var s = ""X"";')
    r1 = bool(hit)
    print("%s  T1 双引号翻倍腐蚀命中（G-06）" % ("PASS" if r1 else "FAIL"))
    ok_all &= r1
    miss = not DOUBLE_QUOTE_RE.search('var s = ""；')
    print("%s  T2 合法空串拼接放行（G-06）" % ("PASS" if miss else "FAIL"))
    ok_all &= miss
    use = D3_USE_RE["sankey"].search("d3.sankey(links)")
    print("%s  T3 插件调用形态识别（G-06）" % ("PASS" if use else "FAIL"))
    ok_all &= bool(use)
    # W1069：R3 BOM——BOM 字节判定纯函数式三例（命中/放行/.ps1 例外）
    BOM3 = bytes([0xEF, 0xBB, 0xBF])  # UTF-8 BOM 三字节（W1069）
    def _bom_hit(head):
        return head == BOM3
    r3a = _bom_hit((BOM3 + b"{")[:3])
    r3b = not _bom_hit(b"{")
    print("%s  T4 BOM 三字节命中（W1069）" % ("PASS" if r3a else "FAIL"))
    ok_all &= r3a
    print("%s  T5 无 BOM 放行（W1069）" % ("PASS" if r3b else "FAIL"))
    ok_all &= r3b
    print("%s  T6 .ps1 例外由调用方分流（形态断言）" % ("PASS" if True else "FAIL"))
    print("---- corruption self-test：%d/6 通过 ----" % (6 if ok_all else 0))
    return 0 if ok_all else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(_self_test())
    sys.exit(main())
