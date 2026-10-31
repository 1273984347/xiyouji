# -*- coding: utf-8 -*-
"""_w1049_reissue_og.py — 重出件的 og 版强制重新派生

陷阱（W1049 实测）：落位脚本的 og 派生是**幂等 SKIP**（文件已存在且尺寸合规即跳过）
⇒ 重出母版后 og 版仍指向**旧图**（页面 og:image 不变、肉眼可见的是新母版但社交卡是旧图）。

修法：重出后必须**显式删除该 3 张 og 版**再重跑落位脚本 ⇒ og 由新母版重新派生。
本脚本只删本批 3 张重出件对应的 og 版（白名单·不碰其余 133 张）。

用法：py -3 archive/scripts/batches/w10xx/_w1049_reissue_og.py [--dry-run]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
IMG = os.path.join(REPO, "site", "static", "images")

# 重出过的 3 张（仅这 3 张的 og 需重新派生）
REISSUED = [
    "plate-line-97-ch016-jinchi-zhanglao",
    "plate-line-103-ch005-sida-tianwang",
    "plate-line-107-ch067-honglin-damang",
]


def main() -> int:
    dry = "--dry-run" in sys.argv
    for stem in REISSUED:
        p = os.path.join(IMG, "og-%s.webp" % stem)
        if not os.path.exists(p):
            print("SKIP  og-%s.webp 不存在（无需删除）" % stem)
            continue
        size = os.path.getsize(p)
        if dry:
            print("DRY  将删 og-%s.webp（%d B）⇒ 下次落位由新母版重新派生" % (stem, size))
            continue
        os.remove(p)
        print("已删 og-%s.webp（%d B）" % (stem, size))
    print("---- 重出件 og 版清退完成（白名单 %d 张）----" % len(REISSUED))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
