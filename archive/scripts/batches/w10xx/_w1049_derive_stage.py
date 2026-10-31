# -*- coding: utf-8 -*-
"""_w1049_stage.py — W1049 落位：12 个回目页接入题图 + 换专属 og:image

由 W1043 批落位脚本**程序化派生**（派生纪律：程序化派生 + 残留断言·禁手抄改常量）。
替换方式：定位 JOBS 列表块 → 用本批 JOBS_DATA 整块替换 → 断言源批次号零残留。

本批 12 回**全部为「新增题图」**（W1043 的 ch086「已有旧题图只换 og」例外在本批不存在
—— 12 个目标回实读均无任何配图·见 `_w1049_pick_verify.py` 第 ① 项判据）
⇒ PREEXISTING = 空集。

用法：py -3 archive/scripts/batches/w10xx/_w1049_stage.py [--dry-run]
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "_w1043_stage.py")
DST = os.path.join(HERE, "_w1049_stage.py")

# 本批 12 回的站点版文件名 + alt 文本（alt 形态沿用前四轮口径）
JOBS_DATA = [
    ("ch016", "plate-line-97-ch016-jinchi-zhanglao.webp",
     "金池长老的线描立像：毗卢帽、宽袖僧衣，双手合十于胸前"),
    ("ch039", "plate-line-98-ch039-wenshu-pusa.webp",
     "文殊菩萨的线描立像：五佛冠、广袖法衣，左手托莲瓣座莲台，右手作说法印"),
    ("ch046", "plate-line-99-ch046-luli-daxian.webp",
     "鹿力大仙的线描立像：莲花冠、宽袖道袍，双手拢于袖中"),
    ("ch050", "plate-line-100-ch050-huode-xingjun.webp",
     "火德星君的线描立像：窄尖高冠、宽袖帝君袍，双手托一只三足圆鼎"),
    ("ch055", "plate-line-101-ch055-nvguo-guowang.webp",
     "女儿国国王的线描立像：高挽发髻插素簪，广袖长裙、双手交握于身前"),
    ("ch084", "plate-line-102-ch084-miefo-guowang.webp",
     "灭法国国王的线描立像：平直王冠、宽袖王袍，双手拱于身前相迎"),
    ("ch005", "plate-line-103-ch005-sida-tianwang.webp",
     "四大天王的线描场面：四名戴盔天将前后错落分立，各执长柄兵器"),
    ("ch018", "plate-line-104-ch018-gao-taigong.webp",
     "高太公与猴形行者的线描场面：戴方巾的老翁双手作揖，与执棒行者相对"),
    ("ch032", "plate-line-105-ch032-yinjiao-dawang.webp",
     "银角大王与猴形行者的线描场面：戴高窄紫金冠的妖王持七星剑，与执棒行者隔阵对峙"),
    ("ch056", "plate-line-106-ch056-shidai-yanjun.webp",
     "十代阎君的线描场面：十名戴獬豸冠的冥府判官排成两列，各持留白长方牌"),
    ("ch067", "plate-line-107-ch067-honglin-damang.webp",
     "红鳞大蟒与猴形行者的线描场面：粗大蟒身弯卷高昂，与执棒行者隔岭对峙"),
    ("ch058", "plate-line-108-ch058-diting.webp",
     "谛听与猴形行者的线描场面：狮首麒麟状神兽四足伏地，与执棒行者相对"),
]


def _jobs_block() -> str:
    lines = ["JOBS = ["]
    for ch, site_name, alt in JOBS_DATA:
        lines.append('    (%r, %r,' % (ch, site_name))
        lines.append('     %r),' % alt)
    lines.append("]")
    return "\n".join(lines)


def derive() -> str:
    src = open(SRC, encoding="utf-8").read()
    out = src

    # ① 替换 JOBS 块（从 "JOBS = [" 到该块的 "]")
    m = re.search(r"^JOBS = \[.*?^\]$", out, re.S | re.M)
    if not m:
        raise SystemExit("派生锚点失配：未找到 JOBS 块")
    out = out[:m.start()] + _jobs_block() + out[m.end():]

    # ② 本批无「已有旧题图」例外
    out = out.replace(
        'PREEXISTING = {"ch086"}',
        "PREEXISTING = set()  # W1049：本批 12 回实读均无任何配图⇒无例外回")

    # ③ 标题/注释/用法里的源批次号
    out = out.replace("_w1043_stage.py — W1016 落位", "_w1049_stage.py — W1049 落位")
    out = out.replace("用法：py -3 scripts/_w1043_stage.py [--dry-run]",
                      "用法：py -3 archive/scripts/batches/w10xx/_w1049_stage.py [--dry-run]")
    # W1049 盲审 P1-2 修正：源文件实为「其余 **68** 个」（本版原写成 88 ⇒ str.replace
    # 零替换且无报错 ⇒ 静默 no-op·产物仍留 68）。⇒ 锚点逐字取自源文件。
    out = out.replace("只碰本批 12 个页面 ⇒ 其余 68 个无配图回目页的 og:image 零改动。",
                      "只碰本批 12 个页面 ⇒ 其余 88 个已配图/未配图回目页的 og:image 零改动。")

    # ④ CSS 常量里的源批次号（W1049 盲审 P1-2：残留断言补 "W1043" 后必须
    #    同步改写 CSS 常量注释，否则断言必然拦下 ⇒ 派生脚本自带「改写+断言」闭环）
    out = out.replace("/* W1043：回目题图（线描族·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */",
                      "/* W1049：回目题图（线描族·沿用章回页 chapter-plate 范式·浅底宣纸图暗色模式隐藏） */")

    # 残留断言：源批次号/例外回/存量编号不得残留（补 "W1043" 与 "68 个" 两项·
    # 盲审实测：原断言列表漏 "W1043" ⇒ 产物 CSS 常量仍带 `/* W1043：回目题图 */`）
    for bad in ("_w1043", "W1043", "ch086", "plate-line-85", "plate-line-96",
                "其余 68 个", "W1016"):
        if bad in out:
            raise SystemExit("残留断言失败：产物仍含 %r" % bad)
    return out


def main() -> int:
    if not os.path.exists(DST):
        text = derive()
        tmp = DST + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        os.replace(tmp, DST)
        print("派生写出：%s" % os.path.relpath(DST, os.getcwd()))
    else:
        print("已存在，跳过派生：%s" % os.path.relpath(DST, os.getcwd()))

    ns = {"__name__": "__main__", "__file__": DST}
    sys.argv = [DST] + sys.argv[1:]
    try:
        exec(compile(open(DST, encoding="utf-8").read(), DST, "exec"), ns)
    except SystemExit as e:
        return e.code or 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
