#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""W941 · UI 图标位 emoji → 内联 SVG 图标 批量替换器

机制（两支，图形源唯一 = site/static/icons/ui/*.svg）：
  ① HTML 结构位 → 内联 <svg class="ico"> 元素（file:// / CSP img-src 'self' / 多层目录 三重安全）
  ② CSS content 位 → mask-image（同源 SVG 文件·'self' 允许·color: currentColor 随主题）

判据纪律：每条规则带**独立预期命中数**（取自 scripts/_w939_scan_targets.py 的基准扫描），
实际不符即抛错退出（防「声明≠落地」假收敛）。幂等：已替换的形态不再命中。

用法：
    py -3 scripts/_w939_emoji_to_svg.py --dry     # 只统计不写
    py -3 scripts/_w939_emoji_to_svg.py --apply   # 执行替换
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ICON_DIR = pathlib.Path("site/static/icons/ui")
TARGETS = pathlib.Path("scripts/output/_w939_targets.json")
REPORT = pathlib.Path("scripts/output/_w939_replacements.json")

# CSS content 位 → mask 规则模板（相对路径依赖页面深度 1：site/data/ 与 site/en/ 均成立）
MASK_RULES = {
    # (选择器, 原 content 字面量, 图标名, 是否尾随文字→需 ::after 承接)
    (".radio-out .caption::before", '"📻 "', "radio", False),
    (".detective-banner::before", '"🔍 "', "search", False),
    (".suspect-card::before", '"📌"', "pin", False),
    (".suspect-card .evi.for::before", '"✓ "', "check", False),
    (".suspect-card .evi.against::before", '"✗ "', "cross", False),
    (".hu-card::before", '"🔍"', "search", False),
    (".warn-item::before", '"⚠"', "warn", False),
    (".cc-acq::before", '"📜 "', "scroll", False),
    (".nc-quote::before", '"❝ "', "quote", False),
    (".search-box::before", '"🔍"', "search", False),
    (".idea-card .id-innovation::before", '"★ 创新 · "', "star", True),
}

SCAN_ROOTS = ["site", "xiyouji-agent-web/src", "xiyouji-desktop/src", "assets/promo"]
SRC_SUFFIX = {".html", ".htm", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".vue", ".css"}


def load_icons() -> dict[str, tuple[str, str]]:
    """读图标资产 → {name: (path_d, transform)}"""
    out = {}
    for f in sorted(ICON_DIR.glob("*.svg")):
        body = re.search(r"<path ([^/]+)/>", f.read_text(encoding="utf-8")).group(1)
        d = re.search(r'd="([^"]+)"', body).group(1)
        tr = re.search(r'transform="([^"]+)"', body)
        out[f.stem] = (d, tr.group(1) if tr else "")
    return out


def svg_tag(icons: dict, name: str, gap: bool = False) -> str:
    """内联 SVG 图标标记。

    width/height 属性是**降级兜底**：520 个阅读页走外链 CSS（site/system.css），
    若 CSS 未加载，SVG 无尺寸时会退化成 300×150 的巨图；属性兜底保证只影响观感不破坏版面。
    """
    d, tr = icons[name]
    tr_attr = f' transform="{tr}"' if tr else ""
    fill_attr = ' fill="currentColor"' if name.endswith("-solid") else ""
    cls = "ico ico-t" if gap else "ico"
    return (f'<svg class="{cls}" width="1em" height="1em" viewBox="0 0 24 24" aria-hidden="true">'
            f'<path d="{d}"{tr_attr}{fill_attr}/></svg>')


def mask_decl(icon: str, rel: str = "../static/icons/ui") -> str:
    url = f'url("{rel}/{icon}.svg")'
    return ('content: ""; display: inline-block; width: 1em; height: 1em; '
            'vertical-align: -0.14em; margin-right: 0.3em; background-color: currentColor; '
            f'-webkit-mask: {url} center / contain no-repeat; '
            f'mask: {url} center / contain no-repeat;')


# ---------------------------------------------------------------- 规则表
# (rule_id, 说明, 期望命中数, 查找串, 替换串生成器)
def build_rules(icons: dict):
    R = []

    # —— ① 阅读页三处主形态（615 页 × 3）——
    R.append((
        "reader-bookmark", "阅读页收藏按钮 ☆ → 星标图标", 615,
        'data-act="bookmark" aria-pressed="false">☆ 收藏本页</button>',
        lambda: ('data-act="bookmark" aria-pressed="false">'
                 + svg_tag(icons, "star", gap=True) + '收藏本页</button>'),
    ))
    R.append((
        "reader-thumb-up", "阅读页反馈「有帮助」👍 → 拇指图标", 615,
        'rel="noopener">👍 有帮助</a>',
        lambda: 'rel="noopener">' + svg_tag(icons, "thumb-up", gap=True) + '有帮助</a>',
    ))
    R.append((
        "reader-thumb-down", "阅读页反馈「待改进」👎 → 拇指图标", 615,
        'rel="noopener">👎 待改进</a>',
        lambda: 'rel="noopener">' + svg_tag(icons, "thumb-down", gap=True) + '待改进</a>',
    ))

    # —— ② JS 内联 HTML 串里的判定图标 ——
    R.append((
        "js-icon-wrong-plain", "icon-wrong 空图标（JS 串）", 4,
        '<span class="icon-wrong">✗</span>',
        lambda: '<span class="icon-wrong">' + svg_tag(icons, "cross") + '</span>',
    ))
    R.append((
        "js-icon-correct-plain", "icon-correct 空图标（JS 串）", 2,
        '<span class="icon-correct">✓</span>',
        lambda: '<span class="icon-correct">' + svg_tag(icons, "check") + '</span>',
    ))
    R.append((
        "html-icon-wrong-text", "icon-wrong 带文字（怪物结局）", 8,
        None,  # 正则规则，见下
        lambda: None,
    ))

    # —— ③ 空态与卡片图标槽 ——
    R.append((
        "es-icon-book", "空态书本图标 📖（含 text-search-app.js）", 3,
        '<span class="es-icon">📖</span>',
        lambda: '<span class="es-icon">' + svg_tag(icons, "book-open") + '</span>',
    ))
    R.append((
        "es-icon-search", "空态检索图标 🔍（text-search-app.js）", 1,
        '<span class="es-icon">🔍</span>',
        lambda: '<span class="es-icon">' + svg_tag(icons, "search") + '</span>',
    ))
    R.append((
        "pc-emoji-guide", "英文指南卡片图标槽（7 枚各一）", 7,
        None,
        lambda: None,
    ))

    # —— ④ 年龄段页签 ——
    R.append((
        "age-tab", "弹幕墙年龄段页签 4 枚 × 2 页", 8,
        None,
        lambda: None,
    ))

    # —— ⑤ 界面控件按钮（语言无关正则见 REGEX_RULES）——
    R.append((
        "btn-play", "播放按钮 ▶", 4,
        None,
        lambda: None,
    ))

    # —— ⑥ 图标链接前缀 ——
    R.append((
        "alias-search-link", "关联检索链接前缀 🔍（中文 JS 串）", 1,
        '>🔍 站内检索「',
        lambda: '>' + svg_tag(icons, "search", gap=True) + '站内检索「',
    ))
    R.append((
        "alias-search-link-en", "关联检索链接前缀 🔍（英文 JS 串）", 1,
        '>🔍 Site search for “',
        lambda: '>' + svg_tag(icons, "search", gap=True) + 'Site search for “',
    ))

    # —— ⑦ 运行时重建按钮的 JS（收藏态切换：用 DOM 克隆图标·不硬编码路径）——
    R.append((
        "reader-mark-js", "收藏按钮 JS 状态切换（★/☆ → 图标）", 1,
        "markBtn.textContent = on ? '★ 已收藏' : '☆ 收藏本页';",
        lambda: (
            "var baseIcon = markBtn.querySelector('svg');\n"
            "markBtn.innerHTML = (baseIcon ? baseIcon.outerHTML : '') + (on ? '已收藏' : '收藏本页');\n"
            "var mkPath = markBtn.querySelector('svg path');\n"
            "    if (mkPath) { if (on) { mkPath.setAttribute('fill', 'currentColor'); }"
            " else { mkPath.removeAttribute('fill'); } }"
        ),
    ))
    R.append((
        "verdict-inspect-js", "侦探卡结论标签前缀 🔎", 2,
        'text("🔎 " + c.verdict)',
        lambda: 'text(' + "'" + svg_tag(icons, "inspect", gap=True) + "' + c.verdict)",
    ))

    # —— ⑧ 外部 JS 标签前缀（rag-chat）——
    R.append((
        "rag-src-icon", "检索来源标签前缀 📖", 1,
        "'📖 来源：'",
        lambda: "'" + svg_tag(icons, "book-open", gap=True) + " 来源：'",
    ))
    R.append((
        "rag-snippet-icon", "相关语料标签前缀 📚", 1,
        "'📚 相关语料：'",
        lambda: "'" + svg_tag(icons, "book", gap=True) + " 相关语料：'",
    ))

    # —— ⑨ 正文段首提示标记 ——
    R.append((
        "criticism-pin", "批驳史段首提示标记 📌", 2,
        '📌 <strong>',
        lambda: svg_tag(icons, "pin", gap=True) + '<strong>',
    ))
    return R


REGEX_RULES = [
    # (rule_id, 说明, 期望命中数, 正则, 替换函数（接收 match）)
    ("html-icon-wrong-text", "icon-wrong 带文字（怪物结局）", 8,
     re.compile(r'<span class="icon-wrong">(✗)([^<]*)</span>'),
     lambda m, ic: f'<span class="icon-wrong">{svg_tag(ic, "cross", gap=True)}{m.group(2)}</span>'),
    ("pc-emoji-guide", "英文指南卡片图标槽", 7,
     re.compile(r'<span class="pc-emoji" aria-hidden="true">([^<]+)</span>'),
     None),  # 需按字符查图标名 → 运行时处理
    ("age-tab", "弹幕墙年龄段页签", 8,
     re.compile(r'(<div class="age-tab[^>]*>)([👶🎒📚🎓])\s*'),
     None),
    ("btn-play", "播放按钮 ▶", 4,
     re.compile(r'(id="btnPlay">)(▶)\s*'),
     None),
    ("btn-menu", "侧栏折叠按钮 ☰（中英各一）", 2,
     re.compile(r'(title="[^"]*")>(☰)</button>'),
     None),
    ("btn-close", "抽屉关闭按钮 ✕（中英各一·JS 串）", 2,
     re.compile(r'(aria-label="[^"]*")>(✕)</button>'),
     None),
    ("btn-pause", "暂停按钮 ⏸（中英各二）", 4,
     re.compile(r'(id="btnPause">)(⏸)\s*'),
     None),
    ("btn-textcontent-play-zh", "JS 按钮文本 ▶ 播放", 12,
     re.compile(r'btn\.textContent = "▶ (播放)";'),
     None),
    ("btn-textcontent-play-en", "JS 按钮文本 ▶ Play", 12,
     re.compile(r'btn\.textContent = "▶ (Play)";'),
     None),
    ("btn-textcontent-pause-zh", "JS 按钮文本 ⏸ 暂停", 3,
     re.compile(r'btn\.textContent = "⏸ (暂停)";'),
     None),
    ("btn-textcontent-pause-en", "JS 按钮文本 ⏸ Pause", 3,
     re.compile(r'btn\.textContent = "⏸ (Pause)";'),
     None),
    ("btn-play-static", "静态播放按钮 ▶（中英各三）", 6,
     re.compile(r'(<button class="ctrl-btn play" id="play-btn"[^>]*>)(▶)\s*'),
     None),
]

AGE_ICON = {"👶": "child", "🎒": "schoolbag", "📚": "book", "🎓": "cap"}
PC_ICON = {"🌱": "sprout", "🜂": "alchemy", "📜": "scroll", "📚": "book",
            "✒": "pen", "📊": "chart", "🌐": "globe"}


def iter_files(roots):
    for root in roots:
        p = pathlib.Path(root)
        if not p.exists():
            continue
        for f in sorted(p.rglob("*")):
            if f.is_file() and f.suffix.lower() in SRC_SUFFIX:
                yield f


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if not (args.dry or args.apply):
        ap.error("需指定 --dry 或 --apply")

    icons = load_icons()
    print(f"图标资产: {len(icons)} 枚 ← {ICON_DIR}")
    baseline = json.loads(TARGETS.read_text(encoding="utf-8"))
    print(f"基准扫描: reader_main {len(baseline['reader_main']['files'])} 文件 / "
          f"{baseline['reader_main']['total_hits']} 命中 · scattered {len(baseline['scattered'])} 条")

    # ---------- 收集所有源文件内容 ----------
    files = {str(f).replace("\\", "/"): f for f in iter_files(SCAN_ROOTS)}
    contents = {}
    for k, f in files.items():
        try:
            contents[k] = f.read_text(encoding="utf-8")
        except Exception:
            continue

    stats = []
    violations = []

    # ---------- 规则 1：字面串替换 ----------
    for rid, desc, expect, needle, gen in build_rules(icons):
        if needle is None:
            continue
        repl = gen()
        hits = 0
        already = 0
        touched = []
        for k, text in contents.items():
            n = text.count(needle)
            if n:
                hits += n
                contents[k] = text.replace(needle, repl)
                touched.append(k)
            elif rid in ("reader-bookmark", "reader-thumb-up", "reader-thumb-down") \
                    and 'data-act="bookmark"' in text and 'class="ico ico-t"' in text:
                # 已治理页（未跟踪的新阅读页·git restore 不适用）⇒ 幂等跳过并计入守恒
                already += 1
        total = hits + already
        stats.append({"rule": rid, "desc": desc, "expected": expect, "actual": total,
                      "new_hits": hits, "already_done": already,
                      "files": len(touched), "kind": "literal"})
        if total != expect:
            violations.append(f"{rid}: 期望 {expect} 实际 {total}（本次替换 {hits} + 已治理 {already}）")

    # ---------- 规则 2：正则替换 ----------
    for rid, desc, expect, rx, fn in REGEX_RULES:
        hits = 0
        touched = []
        for k, text in contents.items():
            def repl(m):
                nonlocal hits
                hits += 1
                if fn is not None:
                    return fn(m, icons)
                if rid == "pc-emoji-guide":
                    ch = m.group(1).strip().replace("\ufe0f", "")
                    name = PC_ICON.get(ch)
                    if name is None:
                        raise SystemExit(f"pc-emoji 未登记图标: {ch!r}")
                    return f'<span class="pc-emoji">{svg_tag(icons, name)}</span>'
                if rid == "age-tab":
                    ch = m.group(2)
                    return m.group(1) + svg_tag(icons, AGE_ICON[ch], gap=True)
                if rid == "btn-play":
                    return m.group(1) + svg_tag(icons, "play", gap=True)
                if rid == "btn-menu":
                    return m.group(1) + ">" + svg_tag(icons, "menu") + "</button>"
                if rid == "btn-close":
                    return m.group(1) + ">" + svg_tag(icons, "close") + "</button>"
                if rid == "btn-pause":
                    return m.group(1) + svg_tag(icons, "pause", gap=True)
                if rid.startswith("btn-textcontent-play"):
                    label = m.group(1)
                    return ('btn.innerHTML = ' + "'" + svg_tag(icons, "play", gap=True)
                            + label + "';")
                if rid.startswith("btn-textcontent-pause"):
                    label = m.group(1)
                    return ('btn.innerHTML = ' + "'" + svg_tag(icons, "pause", gap=True)
                            + label + "';")
                if rid == "btn-play-static":
                    return m.group(1) + svg_tag(icons, "play", gap=True)
                raise SystemExit(f"未实现的正则规则: {rid}")
            new = rx.sub(repl, text)
            if new != text:
                contents[k] = new
                touched.append(k)
        stats.append({"rule": rid, "desc": desc, "expected": expect, "actual": hits,
                      "files": len(touched), "kind": "regex"})
        if hits != expect:
            violations.append(f"{rid}: 期望 {expect} 实际 {hits}")

    # ---------- 规则 3：CSS content 位 → mask ----------
    css_stats = []
    for selector, literal, icon, has_text in MASK_RULES:
        expect = 2  # 中文页 + 英文页各一
        decl = mask_decl(icon)
        hits = 0
        touched = []
        for k, text in contents.items():
            if literal not in text:
                continue
            # 仅替换属于该选择器的那一条声明
            pat = re.compile(
                re.escape(selector) + r"\s*\{([^}]*?)content:\s*" + re.escape(literal) + r"\s*;")
            def repl(m):
                nonlocal hits
                hits += 1
                body = m.group(1)
                extra = ""
                if has_text:
                    extra = (f'\n    }}\n{selector}::after {{ content: " 创新 · "; '
                             'font-style: normal; font-weight: 600; font-size: 0.72rem; '
                             'color: var(--accent-3);')
                return f"{selector} {{{body}{decl}{extra}"
            new = pat.sub(repl, text)
            if new != text:
                contents[k] = new
                touched.append(k)
        css_stats.append({"selector": selector, "literal": literal, "icon": icon,
                          "expected": expect, "actual": hits, "files": len(touched)})
        if hits != expect:
            violations.append(f"css-content[{selector}]: 期望 {expect} 实际 {hits}")

    # ---------- 汇总 ----------
    print("\n=== 规则命中统计 ===")
    for s in stats + css_stats:
        key = s.get("rule") or s.get("selector")
        flag = "OK " if s["expected"] == s["actual"] else "!! "
        print(f"  {flag}{key:26s} 期望 {s['expected']:4d} 实际 {s['actual']:4d}  "
              f"文件 {s['files']}")

    total_expected = sum(s["expected"] for s in stats) + sum(s["expected"] for s in css_stats)
    total_actual = sum(s["actual"] for s in stats) + sum(s["actual"] for s in css_stats)
    print(f"\n合计: 期望 {total_expected} 实际 {total_actual}")

    if violations:
        print("\n!! 命中数不符（假收敛防护）:")
        for v in violations:
            print("   -", v)
        return 2

    if args.dry:
        print("\n[DRY] 未写盘")
        return 0

    changed = 0
    for k, text in contents.items():
        p = files[k]
        old = p.read_text(encoding="utf-8")
        if old != text:
            p.write_text(text, encoding="utf-8")
            changed += 1

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(
        {"stats": stats, "css": css_stats, "files_changed": changed,
         "total_expected": total_expected, "total_actual": total_actual},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n[APPLY] 改写 {changed} 个文件 → {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
