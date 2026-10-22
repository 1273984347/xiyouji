#!/usr/bin/env python3
"""_w851_j1_name_audit.py — J1 命名冲突审计（W851·设计迁移阶段 1 验收件）

## 为什么需要它

W826 细化规格 §4 的「v4 令牌终稿」自称**纯加法**，但稿内 4 组名字与现役变量撞名：
`--chart-1..6`（现役已定义·其中 `--chart-3` 还要从 #C9A063 改值）、`--accent-soft`
（现役已定义）、暗色组 `--accent`（现役 #E0604F·稿中改 #E46250）、暗色 `--chart-3/5`
（暗色组新增即改变量回退值）。规格 §7 的 J1 口径：「同名即语义改变 → 破坏纯加法保证」。

本审计把「将要落地的名字」与「现役已存在的名字」做机器对拍，面含三处：
① `site/tokens.css` ② `site/system.css` ③ 全页面内联 <style> 与 style 属性
（页面内联抢先定义会因 tokens.css 后置加载而覆盖令牌·同归冲突面）。
另扫全站 `var()` 引用面——零消费是纯加法前提，有引用即落地会改渲染。

**W851 的落地集 = 稿中剔掉撞名项后的 34 个零消费新名 / 35 处定义**（暗色组
`--accent-text` 为同名第二处·裁决 4 双主题平级）；撞名项（图表色板改值 /
暗色朱砂改值）显式 defer 到迁移批，随批用 J2 探针逐页 proof。

## 历史坑（本批实证）

首版 `_DEF_RE` 捕获组漏了 `--` 前缀而 `LANDING_NAMES` 带前缀，导致交集/落地
两个方向全部空转（假绿）。凡「集合对拍」必先做一次**双向可失败**自证：
pre-flight 对「已知撞名的 defer 组」必须报撞（defer 复证），verify-landed 对
「已落地名」必须报在。单向永绿的检查等于没有检查。

## 用法

    py -3 scripts/_w851_j1_name_audit.py                  # 落地前：新名 ∩ 现役 == ∅ 且 var() 消费为 0
    py -3 scripts/_w851_j1_name_audit.py --verify-landed  # 落地后：新名 ⊆ tokens.css（含暗色组同名处）
    py -3 scripts/_w851_j1_name_audit.py --tokens PATH    # 指定 tokens.css 副本（如 git show 出的落地前版本）

退出码：0 过 / 1 有冲突或复验不齐。
"""

import glob
import json
import os
import re
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
TOKENS = os.path.join(SITE, "tokens.css")
SYSTEM = os.path.join(SITE, "system.css")
OUT = os.path.join(ROOT, "scripts", "output", "_w851_j1_name_audit.json")

# W851 实际落地集（34 个零消费新名）：W826 §4 稿剔撞名项后
LANDING_NAMES = (
    # 间距刻度（4px 基准 + 2/10 半格）13
    "--space-0", "--space-1", "--space-2", "--space-3", "--space-4", "--space-5",
    "--space-6", "--space-7", "--space-8", "--space-9", "--space-10", "--space-11",
    "--space-12",
    # 间距语义档 6
    "--gap-tight", "--gap-base", "--gap-loose", "--gap-block", "--gap-section",
    "--gap-hero",
    # 容器三档 3
    "--container-read", "--container-content", "--container-wide",
    # 栅格 2
    "--grid-columns", "--grid-gutter",
    # 排版角色 9
    "--type-display", "--type-title", "--type-subtitle", "--type-lead",
    "--type-body", "--type-label", "--type-caption", "--type-eyebrow",
    "--type-number",
    # 色彩补充 1（朱砂文字落 --bg 专用档·裁决 1 修法）
    "--accent-text",
)

# 暗色组须同名再定义一次的名字（裁决 4：双主题平级·与浅色取值不同）
# 故名计数 34、定义处计数 35——J1 判名（交集 0），体积与传播按处计
DARK_ONLY_DEFS = ("--accent-text",)

# W826 §4 稿中显式 defer 的撞名项（记账用·不落地）
# names 为涉及的现役变量名；pre-flight 机检复证「确已撞名」才许 defer
DEFERRED_ITEMS = (
    {"label": "--chart-1..6（浅色组重述）",
     "names": ("--chart-1", "--chart-2", "--chart-3", "--chart-4",
               "--chart-5", "--chart-6"),
     "reason": "现役名；--chart-3 改值命中 42 消费页"},
    {"label": "--accent-soft（重述同值）",
     "names": ("--accent-soft",),
     "reason": "现役名；332 消费页；同值重述空转且破 J1"},
    {"label": "暗色 --accent #E0604F→#E46250",
     "names": ("--accent",),
     "reason": "现役名改值；全站暗色视觉变化"},
    {"label": "暗色 --chart-3/5 新增",
     "names": ("--chart-3", "--chart-5"),
     "reason": "改暗色回退值；42 消费页暗色观感变化"},
)

# defer 持有复验（verify-landed）：撞名项落地后必须原样未动
# W890：W876 批已把浅色 --chart-3（#C9A063→#B38F58）与暗色 --accent
# （#E0604F→#E46250）两项「落地值」改掉——「原值未动」契约对这两项已不适用，
# 继续断言等于用过期期望判红（W889 CI 实证：pytest 2 failed 中的一项即此）。
# 保留项 = 尚未改值的撞名项（浅色 --accent-soft 仍为 #E9B885·实测 site/tokens.css）。
DEFER_HOLD_CHECKS = (
    ("浅色 --accent-soft 未改值", r"--accent-soft:\s*#E9B885"),
)
# defer 持有复验：暗色组不得偷新增这些名（新增即改变暗色回退值）
DEFER_HOLD_DARK_SNEAK = ("--chart-3", "--chart-5")

_DEF_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:")
_STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
_STYLE_ATTR_RE = re.compile(r'style\s*=\s*"([^"]*)"', re.I)
_DARK_BLOCK_RE = re.compile(r'html\[data-theme="dark"\]\s*\{([^}]*)\}', re.S)
_VAR_REF_RE = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)")


def _names_in_css(text):
    """CSS 文本内定义的变量名集合（含 -- 前缀·与 LANDING_NAMES 同形）。"""
    return {m.group(1) for m in _DEF_RE.finditer(text)}


def _iter_site_files():
    """全页面 (rel, text) 迭代（读失败跳过·内联定义与引用两面共用）。"""
    for p in sorted(glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                yield rel, f.read()
        except OSError:
            continue


def _page_inline_names():
    """全页面内联 <style> 块 + style 属性里定义的变量名 → {name: [页面...]}。"""
    found = {}
    for rel, t in _iter_site_files():
        css_text = "\n".join(_STYLE_BLOCK_RE.findall(t))
        css_text += "\n" + "\n".join(_STYLE_ATTR_RE.findall(t))
        for n in _names_in_css(css_text):
            found.setdefault(n, []).append(rel)
    return found


def _dark_block_names(tokens_txt):
    """所有 html[data-theme="dark"] 块内定义的变量名集合（块可多处）。"""
    names = set()
    for m in _DARK_BLOCK_RE.finditer(tokens_txt):
        names |= _names_in_css(m.group(1))
    return names


def _var_consumers(landing, files):
    """files 内 var(--新名) 引用面 → {name: [文件...]}。

    落地前须为 0：零消费是「纯加法不改变渲染」的前提；有引用即该名非零消费，
    落地会改变该页渲染（J2 全量面风险），该名须 defer。
    """
    want = set(landing)
    hits = {}
    for rel, text in files:
        for m in _VAR_REF_RE.finditer(text):
            n = m.group(1)
            if n in want:
                hits.setdefault(n, []).append(rel)
    return hits


def _parse_args(argv):
    verify_landed = "--verify-landed" in argv
    tokens_path = TOKENS
    if "--tokens" in argv:
        i = argv.index("--tokens")
        if i + 1 >= len(argv):
            raise SystemExit("--tokens 需要路径参数") from None
        tokens_path = argv[i + 1]
    return verify_landed, tokens_path


def _preflight_verdict(existing, consumed):
    """预检判定（纯函数·便于单测双向锁死）。

    返回 (ok, {clash, consumed, defer_unproven})。**双向可失败**：
    落地名撞现役 → FAIL；defer 组名没撞现役 → FAIL（理由不成立·须重裁）——
    单向永绿的检查等于没有检查（首版前缀 bug 的教训）。
    """
    clash = sorted(n for n in LANDING_NAMES if n in existing)
    defer_unproven = {}
    for item in DEFERRED_ITEMS:
        miss = [n for n in item["names"] if n not in existing]
        if miss:
            defer_unproven[item["label"]] = miss
    ok = not clash and not consumed and not defer_unproven
    return ok, {"clash": clash, "consumed": consumed,
                "defer_unproven": defer_unproven}


def main(argv):
    verify_landed, tokens_path = _parse_args(argv)
    with open(tokens_path, encoding="utf-8") as f:
        tokens_txt = f.read()
    with open(SYSTEM, encoding="utf-8") as f:
        system_txt = f.read()
    tokens_names = _names_in_css(tokens_txt)
    system_names = _names_in_css(system_txt)
    page_names = _page_inline_names()
    site_files = list(_iter_site_files()) + [("site/system.css", system_txt)]

    art = {
        "schema": 2,
        "batch": "W851",
        "captured_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "mode": "verify-landed" if verify_landed else "pre-flight",
        "tokens_source": os.path.relpath(tokens_path, ROOT).replace(os.sep, "/"),
        "landing_count": len(LANDING_NAMES),
        "landing_sites": len(LANDING_NAMES) + len(DARK_ONLY_DEFS),
        "existing_counts": {"tokens_css": len(tokens_names),
                            "system_css": len(system_names),
                            "page_inline_distinct": len(page_names)},
        "deferred": [dict(x) for x in DEFERRED_ITEMS],
        "checks": {},
    }

    if verify_landed:
        missing = [n for n in LANDING_NAMES if n not in tokens_names]
        dark_names = _dark_block_names(tokens_txt)
        dark_missing = [n for n in DARK_ONLY_DEFS if n not in dark_names]
        hold_fail = [label for label, pat in DEFER_HOLD_CHECKS
                     if not re.search(pat, tokens_txt)]
        dark_sneak = sorted(n for n in DEFER_HOLD_DARK_SNEAK
                            if n in dark_names)
        art["checks"]["landing_complete"] = {
            "missing": missing, "dark_block_missing": dark_missing,
            "definition_sites": len(LANDING_NAMES) + len(DARK_ONLY_DEFS)}
        art["checks"]["defer_hold"] = {
            "value_checks_failed": hold_fail,
            "dark_block_sneaked_new": dark_sneak}
        ok = (not missing and not dark_missing and not hold_fail
              and not dark_sneak)
        if ok:
            print("J1 复验 PASS：%d 个新名 / %d 处定义全部落地（含暗色组 %d 处同名再定义）"
                  % (len(LANDING_NAMES), len(LANDING_NAMES) + len(DARK_ONLY_DEFS),
                     len(DARK_ONLY_DEFS)))
            print("   defer 持有：%d 组撞名项原样未动（%s · 暗色组无 %s 新增）"
                  % (len(DEFER_HOLD_CHECKS),
                     " · ".join(lbl.replace(" 未改值", " 值未改") for lbl, _ in DEFER_HOLD_CHECKS),
                     "/".join(DEFER_HOLD_DARK_SNEAK)))
        else:
            if missing:
                print("J1 复验 FAIL：落地不完整，缺 %s" % "、".join(missing))
            if dark_missing:
                print("J1 复验 FAIL：暗色组缺同名再定义 %s"
                      % "、".join(dark_missing))
            if hold_fail:
                print("J1 复验 FAIL：defer 项被改动（%s）" % "、".join(hold_fail))
            if dark_sneak:
                print("J1 复验 FAIL：暗色组偷新增 %s（defer 破裂）"
                      % "、".join(dark_sneak))
    else:
        consumed = _var_consumers(LANDING_NAMES, site_files)
        ok, verdict = _preflight_verdict(
            tokens_names | system_names | set(page_names), consumed)
        clash = verdict["clash"]
        where = {}
        for n in clash:
            w = []
            if n in tokens_names:
                w.append("tokens.css")
            if n in system_names:
                w.append("system.css")
            if n in page_names:
                w.append("页面内联 ×%d" % len(page_names[n]))
            where[n] = w
        defer_unproven = verdict["defer_unproven"]
        art["checks"]["intersection"] = {"clash": clash, "where": where}
        art["checks"]["page_inline_scan"] = {
            "pages_scanned": len(site_files) - 1,
            "landing_names_predefined_in_pages": sorted(
                n for n in LANDING_NAMES if n in page_names)}
        art["checks"]["consumption"] = {
            "scope": "全页面内联 + system.css 的 var() 引用（tokens.css 自身引用不计）",
            "landing_names_referenced": consumed}
        art["checks"]["deferred_clash_confirmed"] = {
            "unproven_groups": defer_unproven}
        ok = not clash and not consumed and not defer_unproven
        if clash:
            print("J1 FAIL：%d 个新名撞现役名：" % len(clash))
            for n in clash:
                print("   %s ← %s" % (n, "、".join(where[n])))
        if consumed:
            print("J1 FAIL：%d 个新名存在 var() 消费（非零消费·落地会改渲染）："
                  % len(consumed))
            for n, files in sorted(consumed.items()):
                print("   %s ← %s" % (n, "、".join(files[:5])))
        if defer_unproven:
            print("J1 FAIL：defer 组有名字未撞现役（理由不成立·须重裁）：")
            for label, miss in defer_unproven.items():
                print("   %s ← 缺 %s" % (label, "、".join(miss)))
        if ok:
            print("J1 PASS：%d 个新名 / %d 处定义（浅 %d + 暗色组 %d）与现役"
                  "（tokens.css %d · system.css %d · 页面内联 %d 名）零交集"
                  % (len(LANDING_NAMES), len(LANDING_NAMES) + len(DARK_ONLY_DEFS),
                     len(LANDING_NAMES), len(DARK_ONLY_DEFS),
                     len(tokens_names), len(system_names), len(page_names)))
            print("   页面内联抢先定义：0（无级联覆盖风险）")
            print("   var() 消费面：0 引用（零消费·纯加法前提成立）")
            print("   defer 复证：4 组撞名项全部实证命中现役名")

    art["ok"] = ok
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(art, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("审计产物 → %s" % os.path.relpath(OUT, ROOT))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
