"""_w616_zhuangshi_folder.py — W616 《装饰》投稿包独立文件夹迁移的链接与路径修复（一次性·可重复执行）

背景：用户裁决把《装饰》投稿包（B 轨全套）从 docs/S4-学术投稿/ 迁入 docs/S4-学术投稿/装饰投稿/
（12 文件 + 图表/图1-5 浅暗 9 PNG；A 轨 3 灰度图留守原 图表/）。git mv 已先行完成，本脚本修：
  1. 包内 md 的上行导航链接（../S4-学术投稿/ → ../）与指向 S4 根留存文件的链接（补 ../ 前缀）
  2. 9 个历史脚本的路径常量（docs/S4-学术投稿/<名> → docs/S4-学术投稿/装饰投稿/<名>·仅 B 轨面）
  3. 政策核查第 5 项图表路径与陈旧计数（9 图/图 1/2/6 → 5 图）
断言：包内全部 md 相对链接 100% 可解析；脚本层 B 轨旧路径零残留（E1 铁律）。
"""
import os
import re
import sys

ROOT = r"D:\xiyouji"
NEWDIR = os.path.join(ROOT, "docs", "S4-学术投稿", "装饰投稿")

MOVED_MD = [
    "学术论文B轨-新中式数字雅集.md",
    "学术论文B轨-新中式数字雅集-大纲.md",
    "学术论文B轨-新中式数字雅集-匿名稿.md",
    "学术论文B轨-新中式数字雅集-装饰投稿版.md",
    "装饰投稿政策核查-2026-09.md",
    "B轨投稿辅助-确认邮件与投稿信.md",
    "同方向文献调研-B轨-古典文学可视化本土美学.md",
    "论文写法调研-B轨-设计类期刊写作范式.md",
    "图表_清单.md",
]

SCRIPTS = [
    "_w606_prose_polish.py",
    "_w606_paper_figures.py",
    "_w607_zotero_export.py",
    "_w608_crop_fig5.py",
    "_w612_remove_user_study.py",
    "_w612b_finish.py",
    "_w614_notes_polish.py",
    "_w615_official_format.py",
    "_w607_md2docx.js",
]

SCRIPT_RULES = [
    ("S4-学术投稿/学术论文B轨", "S4-学术投稿/装饰投稿/学术论文B轨"),
    ("S4-学术投稿\\学术论文B轨", "S4-学术投稿\\装饰投稿\\学术论文B轨"),
    ("S4-学术投稿/B轨", "S4-学术投稿/装饰投稿/B轨"),
    ("S4-学术投稿\\B轨", "S4-学术投稿\\装饰投稿\\B轨"),
    ("S4-学术投稿/装饰投稿政策核查", "S4-学术投稿/装饰投稿/装饰投稿政策核查"),
    ("S4-学术投稿\\装饰投稿政策核查", "S4-学术投稿\\装饰投稿\\装饰投稿政策核查"),
    ("S4-学术投稿/图表_清单", "S4-学术投稿/装饰投稿/图表_清单"),
    ("S4-学术投稿\\图表_清单", "S4-学术投稿\\装饰投稿\\图表_清单"),
    ("S4-学术投稿/同方向文献调研-B轨", "S4-学术投稿/装饰投稿/同方向文献调研-B轨"),
    ("S4-学术投稿\\同方向文献调研-B轨", "S4-学术投稿\\装饰投稿\\同方向文献调研-B轨"),
    ("S4-学术投稿/论文写法调研-B轨", "S4-学术投稿/装饰投稿/论文写法调研-B轨"),
    ("S4-学术投稿\\论文写法调研-B轨", "S4-学术投稿\\装饰投稿\\论文写法调研-B轨"),
    ("S4-学术投稿/图表/图", "S4-学术投稿/装饰投稿/图表/图"),
    ("S4-学术投稿\\图表\\图", "S4-学术投稿\\装饰投稿\\图表\\图"),
    ("/docs/S4-学术投稿/图表\"", "/docs/S4-学术投稿/装饰投稿/图表\""),  # _w607_md2docx.js FIGDIR
]

OLD_FRAGMENTS = [
    "S4-学术投稿/学术论文B轨", "S4-学术投稿\\学术论文B轨",
    "S4-学术投稿/B轨论文", "S4-学术投稿\\B轨论文",
    "S4-学术投稿/装饰投稿政策核查", "S4-学术投稿\\装饰投稿政策核查",
    "S4-学术投稿/图表_清单", "S4-学术投稿\\图表_清单",
]


def fix_md(name):
    p = os.path.join(NEWDIR, name)
    t = open(p, encoding="utf-8", newline="").read()
    orig = t
    d = os.path.dirname(p)

    def repl(m):
        target = m.group(1)
        if target.startswith(("http", "#", "mailto:")):
            return m.group(0)
        if target.startswith("../S4-学术投稿/"):
            target = "../" + target[len("../S4-学术投稿/"):]
        else:
            base = os.path.basename(target)
            sibling = os.path.join(d, target)
            upstairs = os.path.join(d, "..", base)
            if not target.startswith("../") and not os.path.exists(sibling) and os.path.exists(upstairs):
                target = "../" + target
        # 下移一层通用加深：../X 型未解析而 ../../X 可解析 → 补一层 ../（S2/source 等外部目录链接）
        if target.startswith("../") and not os.path.exists(os.path.normpath(os.path.join(d, target))):
            deeper = "../" + target
            if os.path.exists(os.path.normpath(os.path.join(d, deeper))):
                target = deeper
        return "](" + target + ")"

    t = re.sub(r"\]\(([^)\s]+)\)", repl, t)
    if name == "装饰投稿政策核查-2026-09.md":
        old5 = ("5. **图表**：9 图已生成于 `docs/S4-学术投稿/图表/`"
                "（图 1/2/6 自绘示意，图 3-5 印刷态浅/暗各 2×）；投稿时按刊图版要求（2× 视网膜、≤210mm 宽）整理。")
        new5 = ("5. **图表**：配套 5 图已随包迁至 `docs/S4-学术投稿/装饰投稿/图表/`"
                "（图 1/2 自绘示意，图 3-5 印刷态浅/暗各 2×；A 轨灰度图仍在 `../图表/`）；"
                "投稿时按刊图版要求（2× 视网膜、≤210mm 宽）整理。")
        if old5 in t:
            t = t.replace(old5, new5)
    if t != orig:
        open(p, "w", encoding="utf-8", newline="").write(t)
        print("FIX", name)


def check_links():
    bad = []
    for name in MOVED_MD:
        p = os.path.join(NEWDIR, name)
        t = open(p, encoding="utf-8").read()
        d = os.path.dirname(p)
        for target in re.findall(r"\]\(([^)\s]+)\)", t):
            if target.startswith(("http", "#", "mailto:")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(d, target))):
                bad.append((name, target))
    assert not bad, f"断链: {bad}"
    print(f"LINK-CHECK OK（{len(MOVED_MD)} 个包内 md 相对链接全部可解析）")


def fix_scripts():
    for s in SCRIPTS:
        p = os.path.join(ROOT, "scripts", s)
        t = open(p, encoding="utf-8", newline="").read()
        orig = t
        for old, new in SCRIPT_RULES:
            if old in t:
                t = t.replace(old, new)
        # 幂等性由规则天然保证（替换后旧串不再出现）；残留检查见 fix_scripts 尾部 OLD_FRAGMENTS
        if t != orig:
            open(p, "w", encoding="utf-8", newline="").write(t)
            print("FIX", s)
    for s in SCRIPTS:
        t = open(os.path.join(ROOT, "scripts", s), encoding="utf-8").read()
        for frag in OLD_FRAGMENTS:
            assert frag not in t, (s, frag)
        if s == "_w607_md2docx.js":
            assert '"/docs/S4-学术投稿/装饰投稿/图表"' in t, "FIGDIR 未更新"
    print("SCRIPT-CHECK OK（9 脚本无旧路径残留·FIGDIR 已指新目录）")


if __name__ == "__main__":
    for name in MOVED_MD:
        fix_md(name)
    check_links()
    fix_scripts()
    print("ALL OK")
    sys.exit(0)
