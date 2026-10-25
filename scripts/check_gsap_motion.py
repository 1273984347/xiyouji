#!/usr/bin/env python3
"""check_gsap_motion.py — GSAP 动效写法机检门禁（W957·**独立脚本·不改管控文件**）。

背景：《执行前计划-T28》Q-01「是否把 GSAP 写法判据挂成常驻门禁槽」尚待用户批准；
      在获批前，本脚本以**独立脚本**形态提供同等判据（不改 `check_motion_ban.py`
      与 `verify_delivery.py` 等管控件）。获批后可直接挂载为 verify_delivery 第 49 槽。

判据（8 项，全部可机器判定）：
  J1 载体存在且 JS 语法可解析（括号/引号平衡 + node --check 可用时以 node 为准）
  J2 禁用字面量零命中（视差 / 无限循环 / 大角度旋转 / 回弹类缓动 / 线性缓动 / 无缓动）
  J3 动画时长 ≤ 0.6 s（DESIGN §5.1 入场档）
  J4 缓动取值 ∈ 白名单 {power1.out, power2.out, power3.out, power2.inOut}（DESIGN §5.2）
  J5 reduced-motion 双守卫存在（prefers-reduced-motion 字面量 + matchMedia）
  J6 fail-open 证据存在（try/catch + 终态兜底 clearProps）
  J7 不动布局属性（GSAP vars 中禁 width/height/top/left/margin/padding）
  J8 接入页三件套齐全 + 相对路径可解析到真实文件 + data-gsap 标记存在

用法：
  py -3 scripts/check_gsap_motion.py            # 门禁模式（退出码 0/1）
  py -3 scripts/check_gsap_motion.py --self-test # 负样本自证（正样本 1 + 负样本 6）
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARRIER = ROOT / "site" / "static" / "js" / "motion-gsap.js"

# 允许接入动效的试点页（机检只覆盖本批接入面；推广批再扩清单）
WIRED_PAGES = [
    "site/index.html",
    "site/reader/ch007.html",
    "site/reader/themes/西游与死亡研究专题.html",
    "site/reader/people/黄风怪外传.html",
    "site/reader/people/白骨精.html",
]

EASE_WHITELIST = {"power1.out", "power2.out", "power3.out", "power2.inOut"}

# J2 禁用字面量（与 scripts/check_motion_ban.py 的 BAN 同源 + GSAP 特有的缓动禁项）
BANNED_LITERALS = [
    (r"parallax", "视差（DESIGN §5 禁止清单）"),
    (r"infinite", "无限循环"),
    (r"repeat\s*:\s*-1", "无限循环（repeat:-1）"),
    (r"rotate\(3\d\d", "大角度旋转"),
    (r"rotation\s*:\s*(3[6-9]\d|[4-9]\d\d)", "大角度旋转"),
    (r"back\.(out|in|inOut)", "回弹类缓动"),
    (r"elastic\.", "回弹类缓动"),
    (r"['\"]linear['\"]", "线性缓动（DESIGN §5.2 禁）"),
    (r"ease\s*:\s*['\"]none['\"]", "无缓动（DESIGN §5.2 禁）"),
    (r"cubic-bezier\([^)]*-\d", "cubic-bezier 负值（回弹）"),
]

# J7 禁动的布局属性（GSAP vars 键位）
LAYOUT_KEYS = ["width", "height", "top", "left", "margin", "marginTop", "padding", "fontSize"]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def check_carrier() -> list[str]:
    """返回问题清单（空 = 全过）。"""
    issues: list[str] = []
    if not CARRIER.exists():
        return ["J1 载体缺失：site/static/js/motion-gsap.js"]

    text = _read(CARRIER)

    # J1 语法：node --check 优先（node 缺失则退化为括号/引号平衡粗检）
    node = None
    for cand in ("node", "node.exe"):
        try:
            r = subprocess.run([cand, "--check", str(CARRIER)], capture_output=True,
                               text=True, timeout=60)
            node = r
            break
        except (FileNotFoundError, OSError):
            continue
    if node is not None:
        if node.returncode != 0:
            issues.append("J1 载体 JS 语法错误：%s" % (node.stderr or node.stdout).strip()[:200])
    else:
        if text.count("{") != text.count("}"):
            issues.append("J1 载体花括号不平衡（node 不可用·粗检）")
        if text.count("(") != text.count(")"):
            issues.append("J1 载体圆括号不平衡（node 不可用·粗检）")

    # J2 禁用字面量
    for pat, desc in BANNED_LITERALS:
        hits = re.findall(pat, text, flags=re.I)
        if hits:
            issues.append("J2 禁用字面量命中 %d 处：%s" % (len(hits), desc))

    # J3 时长上限（两形态：① 直接 duration 字面量 ② 时长常量表内的字面量）
    #   自证实证：初版只扫 ① ⇒ 时长表 `{ enter: 1.2 }` 形态越限不被抓（负样本 case5 未被抓住）
    for m in re.finditer(r"duration\s*:\s*([0-9]*\.?[0-9]+)", text):
        v = float(m.group(1))
        if v > 0.6:
            issues.append("J3 动画时长 %s s 超 0.6 s 上限" % v)
    for m in re.finditer(r"\b(?:DUR|TIMING|DURATION)\w*\s*=\s*\{([^}]*)\}", text):
        for num in re.finditer(r":\s*([0-9]*\.?[0-9]+)", m.group(1)):
            v = float(num.group(1))
            if v > 0.6:
                issues.append("J3 时长常量表内 %s s 超 0.6 s 上限" % v)

    # J4 缓动白名单（两形态：① 直接 ease 字面量 ② 缓动常量表内的字面量）
    #   自证实证：初版只扫 ① ⇒ 常量表形态的越权缓动不被抓（负样本 case8 未被抓住）
    for m in re.finditer(r"ease\s*:\s*['\"]([^'\"]+)['\"]", text):
        if m.group(1) not in EASE_WHITELIST:
            issues.append("J4 缓动 '%s' 不在白名单 %s" % (m.group(1), sorted(EASE_WHITELIST)))
    for m in re.finditer(r"\b(?:EASE|EASING)\w*\s*=\s*\{([^}]*)\}", text):
        for e in re.finditer(r":\s*['\"]([^'\"]+)['\"]", m.group(1)):
            if e.group(1) not in EASE_WHITELIST:
                issues.append("J4 缓动常量表内 '%s' 不在白名单 %s"
                              % (e.group(1), sorted(EASE_WHITELIST)))

    # J5 RM 双守卫
    if "prefers-reduced-motion" not in text:
        issues.append("J5 缺 reduced-motion 守卫（无 prefers-reduced-motion 字面量）")
    if "matchMedia" not in text:
        issues.append("J5 缺 reduced-motion 守卫（无 matchMedia）")

    # J6 fail-open 证据
    if "try" not in text or "catch" not in text:
        issues.append("J6 缺 fail-open 证据（无 try/catch）")
    if "clearProps" not in text:
        issues.append("J6 缺 fail-open 终态兜底（无 clearProps）")

    # J7 布局属性
    for k in LAYOUT_KEYS:
        if re.search(r"[\{,]\s*%s\s*:" % re.escape(k), text):
            issues.append("J7 出现布局属性键位 '%s'（DESIGN §5.8 只动 transform/opacity）" % k)

    return issues


def check_wiring() -> list[str]:
    issues: list[str] = []
    for rel in WIRED_PAGES:
        p = ROOT / rel
        if not p.exists():
            issues.append("J8 试点页缺失：%s" % rel)
            continue
        text = _read(p)
        for token in ("gsap.min.js", "ScrollTrigger.min.js", "motion-gsap.js"):
            if token not in text:
                issues.append("J8 %s 未引入 %s" % (rel, token))
        if "data-gsap=" not in text:
            issues.append("J8 %s 缺 data-gsap 标记" % rel)
        # 相对路径可解析性：以引用页所在目录为基准
        for m in re.finditer(r'src="((?:\.\./|\./)?[^"]*static/js/(?:gsap|ScrollTrigger|motion-gsap)\.min?\.js|motion-gsap\.js)"', text):
            target = (p.parent / m.group(1)).resolve()
            if not target.exists():
                issues.append("J8 %s 的外链不可解析到真实文件：%s" % (rel, m.group(1)))
    return issues


def run_gate() -> int:
    issues = check_carrier() + check_wiring()
    if issues:
        print("GSAP 动效写法门禁：%d 项 FAIL" % len(issues))
        for it in issues:
            print("  FAIL %s" % it)
        return 1
    print("GSAP 动效写法门禁通过：载体 8 项判据 + %d 个接入页接线检查全绿" % len(WIRED_PAGES))
    return 0


# ---------------- 负样本自证（判据必须可证伪） ----------------
GOOD = """(function () {
  'use strict';
  var GSAP = window.gsap;
  if (!GSAP) { return; }
  var DUR = { enter: 0.5 };
  var EASE = { enter: 'power3.out' };
  var mm = GSAP.matchMedia();
  mm.add({ full: '(prefers-reduced-motion: no-preference)' }, function (ctx) {
    if (!ctx.conditions.full) { return; }
    try {
      GSAP.set('.x', { autoAlpha: 0 });
      GSAP.to('.x', { autoAlpha: 1, y: 8, duration: DUR.enter, ease: EASE.enter });
      GSAP.set('.x', { autoAlpha: 1, clearProps: 'opacity,transform,visibility' });
    } catch (e) { }
  });
})();
"""

BAD_CASES = [
    ("J2 视差字面量", GOOD.replace("var DUR", "var parallax = 1; var DUR")),
    ("J2 无限循环", GOOD.replace("repeat: -1", "x").replace("var DUR", "var o = { repeat: -1 }; var DUR")),
    ("J2 回弹缓动", GOOD.replace("'power3.out'", "'back.out(1.7)'")),
    ("J3 时长越限", GOOD.replace("enter: 0.5", "enter: 1.2")),
    ("J5 缺 RM 守卫", GOOD.replace("prefers-reduced-motion: no-preference", "all")),
    ("J7 布局属性", GOOD.replace("y: 8", "y: 8, height: 200")),
    ("J4 缓动不在白名单（sine 不触 J2·只有 J4 能抓）",
     GOOD.replace("'power3.out'", "'sine.inOut'")),
]


def self_test() -> int:
    import tempfile
    fails = 0
    cases = 0
    with tempfile.TemporaryDirectory() as td:
        good = Path(td) / "good.js"
        good.write_text(GOOD, encoding="utf-8")
        global CARRIER
        orig = CARRIER
        CARRIER = good
        try:
            issues = check_carrier()
            cases += 1
            ok = not issues
            print("  %s case1 正样本应全过%s" % ("PASS" if ok else "FAIL",
                                            "" if ok else "：%s" % issues[:2]))
            fails += 0 if ok else 1
            for i, (name, text) in enumerate(BAD_CASES, start=2):
                bad = Path(td) / ("bad%d.js" % i)
                bad.write_text(text, encoding="utf-8")
                CARRIER = bad
                iss = check_carrier()
                caught = bool(iss)
                cases += 1
                print("  %s case%d 负样本应被抓：%s%s" % ("PASS" if caught else "FAIL", i, name,
                                                          "" if caught else "（未被抓住）"))
                fails += 0 if caught else 1
        finally:
            CARRIER = orig
    print("self-test: %d/%d 通过" % (cases - fails, cases))
    return 1 if fails else 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    return run_gate()


if __name__ == "__main__":
    sys.exit(main())
