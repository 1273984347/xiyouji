#!/usr/bin/env python3
"""
inline_css.py — 将数据页的外部 ../tokens.css + ../system.css <link> 标签
内联为 <style> 块，使页面自包含、彻底摆脱预览/部署环境下的 ../ 相对路径依赖。

设计要点（对齐项目"静态优先 / EMBEDDED_DATA fallback"哲学）：
- 仅替换精确的 <link rel="stylesheet" href="../tokens.css|../system.css"> 标签；
  sw.js / tokens.css 等非 <link> 字符串引用不会被误伤。
- 单一事实源仍是 site/tokens.css + site/system.css；CSS 有改动时重跑本脚本
  （或加 --force）即可把所有页面重新同步，不会 85× 手工维护。
- 内联副本剥离块注释（strip_comments）：源文件带注释供维护与 W 号追溯，传播到每页时
  去掉注释字节——DESIGN.md §4A.8 的预算针对「每页内联体积」，注释对渲染零贡献。
- 不内联 D3 CDN（<script src="https://d3js.org/...">），那是项目唯一 sanctioned 外部依赖。
- 幂等：已内联（带 INLINED CSS 标记）的页面默认跳过；--force 重新同步。

用法：
    python scripts/inline_css.py                 # 内联所有未处理的页面
    python scripts/inline_css.py --force         # 强制重新同步**已内联页**（不再顺带把外链页转内联）
    python scripts/inline_css.py --force --inline-links  # 显式把外链页也转为内联（大动作·W895 护栏）
    python scripts/inline_css.py --dry           # 仅统计，不写文件
"""
import os
import re
import sys

# W550：守卫根=项目根而非 scripts/（否则写 site/ 页面被误拒·W536 后 --force 实证）·W761 收敛至 utils/path_guard
from utils.path_guard import PROJECT_ROOT, make_guard

_w536_guard_open = make_guard(PROJECT_ROOT)

SITE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
TOKENS = os.path.join(SITE_DIR, "tokens.css")
SYSTEM = os.path.join(SITE_DIR, "system.css")

LINK_TOKENS = '<link rel="stylesheet" href="../tokens.css">'
LINK_SYSTEM = '<link rel="stylesheet" href="../system.css">'
MARKER = "INLINED CSS"

# 防御：CSS 内若含 </style 转义，避免提前闭合
def safe(css):
    return css.replace("</style", "<\\/style")


# 块注释（非嵌套·CSS 无嵌套注释语法）
_CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


def strip_comments(css):
    """内联副本剥离块注释（源 site/*.css 不动，注释仍在源文件里供维护与追溯）。

    依据 DESIGN.md §4A.8：体积预算的实质是「每页内联体积」（每 +1KB = 全站 +225KB），
    而注释对渲染零贡献 ⇒ 只在传播环节剥离，既真正压住每页字节，又不损失源的可读性
    与 W 号追溯。实测：源 28.4KB 中注释约 5.6KB，330 个内联页合计省约 1.85MB。

    注意：副本的**识别**不依赖注释内容——门禁按 `<!-- INLINED CSS … -->` 标记与紧随
    `<style>` 的配对判定副本（见 `utils/gate_common.iter_private_style_blocks`）。若哪天
    有人改成靠块内注释文本识别，剥注释会让它静默失效（W1019 实证·228 页误判）。
    """
    return re.sub(r"\n{3,}", "\n\n", _CSS_COMMENT_RE.sub("", css)).strip()


def process(path, force, dry, inline_links=False):
    with open(path, encoding="utf-8") as f:
        html = f.read()

    # W875：深度感知——reader 子目录页用 ../../ 前缀（原固定 ../ 永远同步不到）
    _rel = os.path.relpath(path, SITE_DIR)
    _depth = _rel.count(os.sep)
    _prefix = "../" * _depth
    link_tokens = '<link rel="stylesheet" href="%stokens.css">' % _prefix
    link_system = '<link rel="stylesheet" href="%ssystem.css">' % _prefix

    has_tokens_link = link_tokens in html
    has_system_link = link_system in html
    already = MARKER in html

    # BL-33 附伤：原「depth==0 无条件早退」把根级**已内联**页（dukou-engine /
    # _template）的重同步路径一并堵死（W876 只能手工靶向修）⇒ 早退撤除，改由本判据
    # 接管：已内联页（含根级）一律放行 --force 重同步；外链页仍受 W895 护栏保护。
    if not (has_tokens_link or has_system_link) and not already:
        return "skip-no-link"   # 根级页面用 tokens.css（无 ../ 且无标记），无需处理
    if already and not force:
        return "skip-inlined"
    # W895 护栏（BL-33）：--force 只重同步已内联页；外链页转内联会把整站样式的
    # 维护形态从「外链」换成「内联」（W875/W895 两次实证 66 万行格式抖动），
    # 必须显式加 --inline-links 才做，避免通扫误伤 520+ 外链 reader 页。
    if force and not already and not inline_links:
        return "skip-external"
    if already and force:
        # 移除旧内联块（从标记注释到对应 </style>）
        html = re.sub(r"<!-- %s.*?-->\s*<style>.*?</style>\s*" % re.escape(MARKER),
                      "", html, flags=re.S)

    with open(TOKENS, encoding="utf-8") as f:
        tokens = strip_comments(safe(f.read().strip()))
    with open(SYSTEM, encoding="utf-8") as f:
        system = strip_comments(safe(f.read().strip()))

    inlined = (
        '    <!-- %s (tokens.css + system.css) · 单一事实源: site/tokens.css, site/system.css · 重同步: python scripts/inline_css.py -->\n'
        '    <style>\n%s\n\n%s\n    </style>\n' % (MARKER, tokens, system)
    )

    # B-0（W563）：内联块的相对 url 以文档为基解析（无 <base>），子目录页的
    # url('static/…') 会解析到 site/data/static/、site/en/static/ 等不存在路径。
    # 按页面相对 site/ 的深度补 ../ 前缀；tokens.css / system.css 源文件不动
    # （对根级 <link> 页与根级 INLINED 页本就正确）。
    _depth = os.path.relpath(path, SITE_DIR).count(os.sep)
    if _depth:
        _prefix = "../" * _depth
        inlined = inlined.replace("url('static/", "url('%sstatic/" % _prefix)
        inlined = inlined.replace('url("static/', 'url("%sstatic/' % _prefix)

    html = html.replace(link_tokens, "")
    html = html.replace(link_system, "")

    if "<style" in html:
        html = html.replace("<style", inlined + "<style", 1)
    else:
        html = html.replace("</head>", inlined + "</head>", 1)

    if not dry:
        with _w536_guard_open(path, "w", encoding="utf-8") as f:
            f.write(html)
    return "inlined" if not already else "re-synced"


def main():
    force = "--force" in sys.argv
    dry = "--dry" in sys.argv
    inline_links = "--inline-links" in sys.argv   # W895 护栏：外链页转内联须显式
    count = {"inlined": 0, "re-synced": 0, "skip-no-link": 0, "skip-inlined": 0, "skip-external": 0}
    processed = []

    for root, _, files in os.walk(SITE_DIR):
        # 跳过构建缓存/隐藏目录
        if any(seg.startswith(".") for seg in root.split(os.sep)):
            continue
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(root, fn)
            try:
                r = process(p, force, dry, inline_links)
            except Exception as e:
                print("ERR  %s -> %s" % (p, e))
                continue
            count[r] = count.get(r, 0) + 1
            if r in ("inlined", "re-synced"):
                processed.append(os.path.relpath(p, SITE_DIR))

    print("=== 结果 ===")
    for k, v in count.items():
        print("  %-14s %d" % (k, v))
    if processed:
        print("--- 受影响页面（%d）---" % len(processed))
        for p in processed[:10]:
            print("  " + p)
        if len(processed) > 10:
            print("  ... 共 %d 个" % len(processed))


if __name__ == "__main__":
    main()
