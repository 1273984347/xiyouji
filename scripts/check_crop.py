"""check_crop.py — 验站点版「只裁上部留白」没有切坏主体

站点版做法：**只**裁掉主体上方的留白（cut = 该张主体顶 − 6 px），**保留下部空白**
（那是画师留的「地面留白」·裁掉会把人物从地面上「拔起来」⇒ 破坏构图关系·W951 实测教训）。

验三条不变量：
  ① 站点版宽 = 1200（母版宽未变）
  ② **主体顶没被切**：站点版墨迹包围盒顶 ≥ 1 px（主体完整进入画布）
  ③ **主体底没被切**：站点版墨迹包围盒底 < 站点版高（人物与地面留白都在）
另输出「下部留白高度」= 站点版高 − 主体底（画师的地面留白·应 > 0）。

用法：py -3 scripts/check_crop.py
（W983 批从 archive 恢复为现役·跨批通用判据·判据逻辑逐字未改；W1002 转正去 `_` 前缀，
 硬编码仓根改为 `dirname(dirname(__file__))`——原来写死 `D:/xiyouji` 换机即失效。）
"""
import glob
import os
import sys

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
SITE_IMG = os.path.join(REPO, "site", "static", "images")
PAPER = (250, 247, 240)
DARK_TOL = 26
SITE_W = 1200


def ink_bbox(im, tol=26):
    """**主体带**（连通簇法·W999 改口径）——不再用「全图墨迹 bbox」。

    改口径的实证（W999）：全图墨迹 bbox 会把**朱砂点睛与赭金装饰**算进主体
    ⇒ 实测 `plate-line-59-ch089-huangshi` 报「主体顶被切（bbox 顶 = 0 px）」，
    但主体簇法复核显示主体**完整**（192..1153 · 地面留白 118 px）⇒ **判据假红**
    （与 W974「bbox 顶 ≠ 主体顶」同族：孤立噪点/装饰色把 bbox 顶拉到画布边）。
    ⇒ 改用与 `scripts/subject_band.py` 同口径（W1004 由归档桶转正）：连通簇（面积 ≥ 200 px²）+ 排除朱砂（r−g ≥ 35）
    与赭金（luma ≥ 90）。**判据阈值与三条不变量一字未改**，只换「主体」的计算口径。
    （W999 批实测：全目录 88 张按新口径复算，仅满幅场景的 ch001 仍 FAIL ⇒ 未掩盖真缺陷。）
    """
    from subject_band import subject_band

    top, bottom, _ = subject_band(im)
    if top is None:
        return None
    return (0, top, im.width, bottom)


def main():
    rows = []
    for p in sorted(glob.glob(os.path.join(SET_DIR, "plate-line-*.png"))):
        stem = os.path.splitext(os.path.basename(p))[0]
        site_p = os.path.join(SITE_IMG, stem + ".webp")
        if not os.path.exists(site_p):
            print("FAIL  站点版缺失: " + stem)
            return 1
        site = Image.open(site_p).convert("RGB")
        sw, sh = site.size
        bbox = ink_bbox(site)
        fails = []
        if sw != SITE_W:
            fails.append("站点版宽=%d（应为 %d）" % (sw, SITE_W))
        if not bbox:
            fails.append("站点版无墨迹（异常）")
            top = bot = -1
            floor = -1
        else:
            top, bot = bbox[1], bbox[3]
            floor = sh - bot
            if top < 1:
                fails.append("主体顶被切（站点版 bbox 顶 = %d px）" % top)
            if bot >= sh:
                fails.append("主体底被切（bbox 底 = %d ≥ 画布 %d）" % (bot, sh))
            if floor <= 0:
                fails.append("下部地面留白被裁掉（floor = %d）⇒ 人物悬空" % floor)
        rows.append((stem, (sw, sh), top, bot, floor, fails))

    print("=== W951 站点版「只裁上部留白」验算 ===")
    print("%-30s %11s %7s %7s %8s  %s" % ("stem", "尺寸", "主体顶", "主体底", "地面留白", "判定"))
    n_fail = 0
    for stem, size, top, bot, floor, fails in rows:
        mark = "PASS" if not fails else "FAIL"
        if fails:
            n_fail += 1
        print("%-30s %11s %7d %7d %8d  %s" % (
            stem, "%dx%d" % size, top, bot, floor, mark))
        for f in fails:
            print("      -> " + f)
    print("\n合计：%d 张 · FAIL %d 张" % (len(rows), n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
