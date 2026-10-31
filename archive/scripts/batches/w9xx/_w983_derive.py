# -*- coding: utf-8 -*-
"""_w983_derive.py — 从归档件**程序化派生** W983 施工脚本（避免手抄漏改硬编码）

背景（坑）：派生脚本时若只改 `BATCH` 常量、漏改 `main()` 里硬编码的 `--w 951`，
首跑就会把上一批已收官的台账行回填成本批内容（W952 实证）。
⇒ 本派生器用**替换表 + 残留断言**兜底：派生产物源码里若仍出现源批次号 / 源轮次目录，
   立即中止（fail-closed），不产出文件。

派生源（archive/scripts/batches/w9xx/）：
  _w974_prepare.py      → scripts/_w983_prepare.py      （母版/站点版派生·作用域 raw/round12）
  _w974_download.py     → scripts/_w983_download.py     （node_id → 原件下载）
  _w974_insert_plates.py→ scripts/_w983_insert_plates.py（接入 12 页·JOBS 整块替换）

用法：py -3 scripts/_w983_derive.py [--dry-run]
"""
import io
import os
import re
import sys

REPO = r"D:\xiyouji"
ARCH = os.path.join(REPO, "archive", "scripts", "batches", "w9xx")
SCRIPTS = os.path.join(REPO, "scripts")

# 本批 12 条接入清单（页面相对路径 · 图片文件名 · alt 文本）
JOBS_W983 = '''JOBS = [
    # —— people 人物 4 ——
    ("site/reader/people/如来.html", "plate-line-25-rulai.webp",
     "如来线描立像：头螺髻垂双耳，立于层叠莲花宝座，身披袈裟双手胸前结印"),
    ("site/reader/people/玉帝.html", "plate-line-26-yudi.webp",
     "玉皇大帝线描立像：头戴冕旒十二串珠，身着玄色宽袖帝服，双手平举白玉笏"),
    ("site/reader/people/百眼魔君.html", "plate-line-27-baiyan-mojun.webp",
     "百眼魔君线描立像：披发黄袍，额头正中张开一只内嵌数十小眼的千眼巨目，双手横持降妖杵"),
    ("site/reader/people/嫦娥外传.html", "plate-line-28-change.webp",
     "嫦娥线描立像：广袖长裙，右手抱玉兔，左手拈桂枝，身旁一轮满月"),
    # —— themes 主题 3 ——
    ("site/reader/themes/神学干预机制专题.html", "plate-line-29-shenxue-ganyu-topic.webp",
     "神学干预机制主题线描立像：如来左掌向下翻转压住五行山，右侧观音手持净瓶插柳枝"),
    ("site/reader/themes/取经路径地理符号学专题.html", "plate-line-30-lujing-ditu-topic.webp",
     "取经路径地理符号学主题线描立像：身披僧衣的行者双手平举展开的古代舆图，图上路线串起驿站圆点"),
    ("site/reader/themes/取经密码学专题.html", "plate-line-31-mima-pan-topic.webp",
     "取经密码学主题线描立像：道袍天机士左手托青铜密码转盘，右手边半卷竹简"),
    # —— essays / poetry / culture 跨学科 3 ——
    ("site/reader/essays/西游与民俗学.html", "plate-line-32-minsu-taofu-topic.webp",
     "西游与民俗学主题线描立像：披甲门神右手按剑、左手执桃符木牌，身侧散落爆竹"),
    ("site/reader/poetry/西游诗词意象谱系专题.html", "plate-line-33-yixiang-puxi-topic.webp",
     "西游诗词意象谱系主题线描立像：唐僧左手拈念珠仰首望月，右手边摊开一卷诗笺"),
    ("site/reader/culture/明代科举制度对照专题.html", "plate-line-34-keju-zhidu-topic.webp",
     "明代科举制度对照主题线描立像：青衫书生头戴儒巾，双手捧一卷考卷，身旁一方砚台"),
    # —— 回目页 2 ——
    ("site/reader/ch010.html", "plate-line-35-ch010-weizheng.webp",
     "第 010 回线描立像：魏征幞头绯色官服，双手横持长剑，身侧盘绕一条三爪之龙"),
    ("site/reader/ch004.html", "plate-line-36-ch004-bimawen.webp",
     "第 004 回线描立像：猴王头戴乌纱官帽、身着青色天庭官服，右手高举齐天大圣旗，左手托方官印"),
]'''

# 通用替换表：源批次号 / 源轮次目录 / UA 标识
COMMON = [
    ("_w974_", "_w983_"),
    ("w974", "w983"),
    ("W974", "W983"),
    ("round11", "round12"),
    ("xiyouji-w974/1.0", "xiyouji-w983/1.0"),
]

# 各产物的「残留禁词」：派生产物里若仍出现这些 ⇒ 硬编码漏改 ⇒ 中止
FORBIDDEN = {
    "_w983_prepare.py": ["974", "round11", "W974"],
    "_w983_download.py": ["974", "round11", "W974"],
    "_w983_insert_plates.py": ["974", "round11", "W974"],
}


def read_src(name):
    p = os.path.join(ARCH, name)
    return io.open(p, encoding="utf-8", newline="").read()


def derive_prepare():
    src = read_src("_w974_prepare.py")
    out = src
    for a, b in COMMON:
        out = out.replace(a, b)
    # 母版张数表述：52 → 64（拼图与输出行里的既有张数）
    out = out.replace("既有 40 张母版与站点版零改动", "既有 52 张母版与站点版零改动")
    out = out.replace("既有 40 + 本批 12", "既有 52 + 本批 12")
    out = out.replace("全目录 52 张", "全目录 64 张")
    out = out.replace("`raw/round11`", "`raw/round12`")
    return out


def derive_download():
    src = read_src("_w974_download.py")
    out = src
    for a, b in COMMON:
        out = out.replace(a, b)
    return out


def derive_insert():
    src = read_src("_w974_insert_plates.py")
    out = src
    for a, b in COMMON:
        out = out.replace(a, b)
    # JOBS 整块替换（锚点：JOBS = [ ... ]）
    m = re.search(r"^JOBS = \[.*?^\]$", out, re.S | re.M)
    if not m:
        print("ABORT  未匹配到 JOBS 块（归档件结构已变）")
        return None
    out = out[:m.start()] + JOBS_W983 + out[m.end():]
    # 题材说明段替换（旧批的 12 条落位说明）
    out = re.sub(r"题材 → 落位页的选择依据.*?\n\"\"\"",
                 "题材 → 落位页的选择依据（见执行前计划 T30 附录 A·12 条落位页已由 ST-03 先验脚本逐页实读确认存在且无题图）：\n"
                 "  · people 4 张 → people 库主页面（如来 / 玉帝 / 百眼魔君 / 嫦娥外传）\n"
                 "  · themes 3 张 → themes 库专题页（神学干预机制 / 取经路径地理符号学 / 取经密码学）\n"
                 "  · essays·poetry·culture 3 张 → 三库专题页（西游与民俗学 / 西游诗词意象谱系 / 明代科举制度对照）\n"
                 "  · 回目页 2 张 → 第 010 回 / 第 004 回\n\"\"\"",
                 out, flags=re.S)
    return out


def write_out(name, text, dry):
    if text is None:
        return False
    for bad in FORBIDDEN[name]:
        if bad in text:
            print("ABORT  %s 残留源批次硬编码「%s」⇒ 漏改·不产出" % (name, bad))
            return False
    p = os.path.join(SCRIPTS, name)
    if dry:
        print("DRY-RUN  %s（%d 字符）" % (name, len(text)))
        return True
    io.open(p, "w", encoding="utf-8", newline="\n").write(text)
    print("写出 %s（%d 字符）" % (name, len(text)))
    return True


def main() -> int:
    dry = "--dry-run" in sys.argv
    ok = True
    ok = write_out("_w983_prepare.py", derive_prepare(), dry) and ok
    ok = write_out("_w983_download.py", derive_download(), dry) and ok
    ok = write_out("_w983_insert_plates.py", derive_insert(), dry) and ok
    if not ok:
        return 2
    print("\n派生完成：3 件施工脚本（硬编码残留断言全过）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
