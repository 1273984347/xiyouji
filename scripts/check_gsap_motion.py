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

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARRIER = ROOT / "site" / "static" / "js" / "motion-gsap.js"  # 主载体（J8 接线判据仍指向它）

# W1053 G-04（W1046 方案）：J1-J4/J7 扫描域从单文件扩至 site/static/js 全部自有 js
# （排除 *.min.js 第三方库）——堵「越规动画写进另一个文件即整体逃逸」。
# 影子实测（W1053）：10 个自有 js 以现行规则全扫零违例 ⇒ 直接升格，无历史清偿负担。
# J5/J6（RM 双守卫 / fail-open）仍只对动效载体（含 gsap 引用）生效——非动效件无此义务。
MIN_LIB_SUFFIX = ".min.js"


def carriers():
    js_dir = CARRIER.parent
    return sorted(p for p in js_dir.glob("*.js") if not p.name.endswith(MIN_LIB_SUFFIX))


def _strip_js_comments(text: str) -> str:
    """J2 扫描前剥注释：块注释 /* */ 全剥；行注释仅剥「行首空白后的 //」（保 URL 的 //）。"""
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    return re.sub(r"(?m)^(\s*)//.*$", r"\1", text)

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


# 显式豁免机制（W960·用户批准挂槽时附带）：
#   在被检文件内写 `gsap-motion: waive J3 J4` ⇒ 对应规则对该文件跳过；
#   · **J2（禁止类：视差 / 无限循环 / 大角度旋转 / 回弹 / 线性 / 无缓动）不可豁免**——它是宪法级红线，
#     请求豁免 J2 一律判红（防止「用豁免绕过宪法」）；
#   · 豁免**不静默**：门禁输出逐条打印豁免项（规则号 + 文件名 + 原文行），可被台账复核。
WAIVE_RE = re.compile(r"gsap-motion:\s*waive\s+([A-Z0-9 ]+)")
NON_WAIVABLE = {"J2"}


def _waivers(text: str):
    """返回 (可豁免规则集合, 非法豁免列表, 豁免原文行列表)。"""
    ok, bad, lines = set(), [], []
    for m in WAIVE_RE.finditer(text):
        for rule in m.group(1).split():
            rule = rule.strip().upper()
            if not rule:
                continue
            if rule in NON_WAIVABLE:
                bad.append(rule)
            else:
                ok.add(rule)
        lines.append(m.group(0).strip())
    return ok, bad, lines


def check_carrier_text(name: str, text: str, node_result=None) -> list[str]:
    """单文件判定（纯函数·W1053 G-04 可测化）：J1-J7 对自有 js 全适用，J5/J6 仅动效载体。

    node_result：调用方注入的 node --check 结果（None=node 不可用 ⇒ 粗检）——node 检查
    需要真实文件路径，留在编排层（check_carrier_all），纯函数不再引用全局 CARRIER 路径。
    """
    issues: list[str] = []
    is_motion_carrier = "gsap" in text  # 动效载体判据：引用了 gsap
    waived, bad_waive, waive_lines = _waivers(text)
    for rule in bad_waive:
        issues.append("J2 宪法级规则不可豁免：%s 请求 waive（豁免仅对 J3/J4/J7 开放）" % rule)
    for rule in sorted(waived - {"J3", "J4", "J7"}):
        issues.append("豁免规则号不存在的规则：%s（可豁免范围 J3 / J4 / J7）" % rule)

    # J1 语法：node --check 结果由调用方注入；None=node 不可用 ⇒ 粗检兜底
    if not is_motion_carrier:
        # 非动效件：只查语法（J1）与禁词（J2·全适用）——J3-J7 语义不适用
        if node_result is None:
            if text.count("{") != text.count("}"):
                issues.append("J1 %s 花括号不平衡（node 不可用·粗检）" % name)
            if text.count("(") != text.count(")"):
                issues.append("J1 %s 圆括号不平衡（node 不可用·粗检）" % name)
        elif node_result.returncode != 0:
            issues.append("J1 %s JS 语法错误：%s"
                          % (name, (node_result.stderr or node_result.stdout).strip()[:200]))
        stripped = _strip_js_comments(text)
        for pat, desc in BANNED_LITERALS:
            hits = re.findall(pat, stripped, flags=re.I)
            if hits:
                issues.append("J2 %s 禁用字面量命中 %d 处：%s" % (name, len(hits), desc))
        return issues

    if node_result is not None:
        if node_result.returncode != 0:
            issues.append("J1 载体 JS 语法错误：%s" % (node_result.stderr or node_result.stdout).strip()[:200])
    else:
        if text.count("{") != text.count("}"):
            issues.append("J1 载体花括号不平衡（node 不可用·粗检）")
        if text.count("(") != text.count(")"):
            issues.append("J1 载体圆括号不平衡（node 不可用·粗检）")

    # J2 禁用字面量（W1053 G-04：扫描前剥注释——堵「写注释里再拼出来」与注释误伤）
    stripped2 = _strip_js_comments(text)
    for pat, desc in BANNED_LITERALS:
        hits = re.findall(pat, stripped2, flags=re.I)
        if hits:
            issues.append("J2 禁用字面量命中 %d 处：%s" % (len(hits), desc))

    # J3 时长上限（两形态：① 直接 duration 字面量 ② 时长常量表内的字面量）
    #   自证实证：初版只扫 ① ⇒ 时长表 `{ enter: 1.2 }` 形态越限不被抓（负样本 case5 未被抓住）
    if "J3" not in waived:
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
    if "J4" not in waived:
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


def wired_pages() -> list[str]:
    """J8 接线清单 glob 派生（W1053 G-04）：扫全站 html 引用 motion-gsap.js 的页面，免手维护。"""
    out = []
    for p in (ROOT / "site").rglob("*.html"):
        try:
            if "motion-gsap.js" in p.read_text(encoding="utf-8", errors="ignore"):
                out.append(p.relative_to(ROOT).as_posix())
        except OSError:
            continue
    return sorted(out)


def _node_check(p: Path):
    """node --check 单文件（node 缺失返回 None ⇒ 粗检兜底）。"""
    for cand in ("node", "node.exe"):
        try:
            return subprocess.run([cand, "--check", str(p)], capture_output=True,
                                  text=True, timeout=60)
        except (FileNotFoundError, OSError):
            continue
    return None


def check_carrier_all() -> list[str]:
    """W1053 G-04：对全部自有 js 跑判据（node --check 全件适用·非动效件也走真实语法门）。"""
    issues: list[str] = []
    for p in carriers():
        issues.extend(check_carrier_text(p.name, _read(p), node_result=_node_check(p)))
    return issues


def check_wiring() -> list[str]:
    issues: list[str] = []
    for rel in wired_pages():
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
    issues = check_carrier_all() + check_wiring()
    # 豁免不静默：逐条打印（规则号 + 原文行），供台账/评审复核
    for p in carriers():
        _ok, _bad, waive_lines = _waivers(_read(p))
        for ln in waive_lines:
            print("  WAIVE %s：%s" % (p.name, ln))
    print("---- 第 50 门禁 GSAP 写法：%s" % ("FAIL" if issues else "PASS"))
    if issues:
        print("GSAP 动效写法门禁：%d 项 FAIL" % len(issues))
        for it in issues:
            print("  FAIL %s" % it)
        return 1
    print("GSAP 动效写法门禁通过：自有 js %d 件全判据 + %d 个接入页（glob 派生）接线检查全绿"
          % (len(carriers()), len(wired_pages())))
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
    fails = 0
    cases = 0
    # W1053 G-04：改走纯函数 check_carrier_text（无需 monkeypatch 临时文件）
    issues = check_carrier_text("good.js", GOOD)
    cases += 1
    ok = not issues
    print("  %s case1 正样本应全过%s" % ("PASS" if ok else "FAIL",
                                    "" if ok else "：%s" % issues[:2]))
    fails += 0 if ok else 1
    for i, (name, text) in enumerate(BAD_CASES, start=2):
        iss = check_carrier_text("bad%d.js" % i, text)
        caught = bool(iss)
        cases += 1
        print("  %s case%d 负样本应被抓：%s%s" % ("PASS" if caught else "FAIL", i, name,
                                                  "" if caught else "（未被抓住）"))
        fails += 0 if caught else 1
    # G-04 新增：剥注释防线两向断言——注释内禁词不误伤 + 代码区禁词仍命中
    cases += 1
    ok_a = not any("J2" in it for it in check_carrier_text("hidden.js", "/* parallax 在注释 */\nvar x = 1;\n"))
    print("  %s case8a 注释内禁词不误伤（剥注释防线）" % ("PASS" if ok_a else "FAIL"))
    fails += 0 if ok_a else 1
    cases += 1
    ok_b = any("J2" in it for it in check_carrier_text("code.js", "var parallax = 1;\n"))
    print("  %s case8b 代码区禁词仍命中" % ("PASS" if ok_b else "FAIL"))
    fails += 0 if ok_b else 1
    cases += 1
    ok = not any(it.startswith(("J3", "J4", "J5", "J6", "J7"))
                 for it in check_carrier_text("plain.js", "var util = 1;\n"))
    print("  %s case9 非动效件只受 J1/J2 约束（J5/J6 不适用）" % ("PASS" if ok else "FAIL"))
    fails += 0 if ok else 1
    print("self-test: %d/%d 通过" % (cases - fails, cases))
    return 1 if fails else 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    return run_gate()


if __name__ == "__main__":
    sys.exit(main())
