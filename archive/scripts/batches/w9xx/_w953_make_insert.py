# -*- coding: utf-8 -*-
"""_w953_make_insert.py — 派生 W953 接入脚本（读 W952 版替换 JOBS 块）

⚠️ 派生纪律（W952 教训）：替换后**必须打印产物核对**（JOBS 条数 / 页面路径 / 图名），
   并断言「无 W952 残留路径」。
"""
import io
import os
import sys

REPO = r"D:\xiyouji"
SRC = os.path.join(REPO, "scripts", "_w952_insert_plates.py")
DST = os.path.join(REPO, "scripts", "_w953_insert_plates.py")

JOBS = '''JOBS = [
    ("site/reader/themes/真假美猴王专题.html", "plate-line-01-zhenjia-meihouwang.webp",
     "真假美猴王主题线描立像：两个一模一样的猴王并排，各持一根相同的如意金箍棒，右侧一面照妖镜"),
    ("site/reader/themes/蟠桃园-体制内的秘密.html", "plate-line-02-pantao-yuan.webp",
     "蟠桃园主题线描立像：守园仙童双手前托浅盘，盘中三枚蟠桃，身后一株蟠桃树枝叶"),
    ("site/reader/themes/大闹天宫-英雄还是悲剧.html", "plate-line-03-danaotian-gong.webp",
     "大闹天宫主题线描立像：悟空头戴凤翅紫金冠、双手横持如意金箍棒，左肩扛杏黄旗杆，身后蟠桃枝叶"),
    ("site/reader/themes/水帘洞专题.html", "plate-line-04-shuilandong.webp",
     "水帘洞主题线描立像：石猴双手前伸作拨开帘幕之姿，身前垂落石帘，身后洞口与飞瀑"),
    ("site/reader/themes/混世四猴专题.html", "plate-line-05-hunshi-sihou.webp",
     "混世四猴主题线描立像：四只猴王一字排开——灵明石猴、赤尻马猴、通臂猿猴、六耳猕猴"),
    ("site/reader/themes/兵器的自我修养专题.html", "plate-line-06-bingqi-xiuyang.webp",
     "兵器专题线描立像：如意金箍棒、九齿钉耙、月牙铲、火尖枪四件悬浮排开，下方一位武僧抱拳而立"),
    ("site/reader/themes/二十八星宿专题.html", "plate-line-07-ershiba-xingsu.webp",
     "二十八星宿主题线描立像：星宿神将头戴星冠、身着星辰纹战袍，身后一轮星盘，一手持星形拂尘"),
    ("site/reader/themes/四值功曹专题.html", "plate-line-08-sizhi-gongcao.webp",
     "四值功曹主题线描立像：值年执玉板、值月执铜镜、值日执日轮、值时执漏刻，四位神将一字排开"),
    ("site/reader/themes/五方揭谛专题.html", "plate-line-09-wufang-jiedi.webp",
     "五方揭谛主题线描立像：五位护法神僧一字排开，各持金刚杵、铜铃、念珠、九环锡杖、玉如意"),
    ("site/reader/themes/六丁六甲专题.html", "plate-line-10-liuding-liujia.webp",
     "六丁六甲主题线描立像：六位甲胄神将结成一圈围向中央正面的一位，各执戟斧枪刀锤鞭"),
    ("site/reader/themes/金箍棒的重量-一万三千五百斤的秘密.html", "plate-line-11-jingubang-zhongliang.webp",
     "金箍棒重量主题线描立像：如意金箍棒横置，下方一杆大秤、秤砣是一只金箍环，旁边猴王侧身托起秤杆"),
    ("site/reader/themes/器物传记学专题.html", "plate-line-12-qiwu-zhuanji.webp",
     "器物传记主题线描立像：牛首妖王持混铁棍与白衣龙君托玉净瓶并立，两人之间悬着一只紫金红葫芦"),
]'''


def main():
    raw = io.open(SRC, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    t = raw.decode("utf-8").replace("\r\n", "\n")

    i = t.index("JOBS = [")
    j = t.index("\n]\n", i) + 3
    t = t[:i] + JOBS + "\n" + t[j:]
    t = t.replace('"""W952：把 12 张线描题图按站内既有 chapter-plate 范式插入 12 个 reader 人物/主题页',
                  '"""W953：把 12 张线描题图按站内既有 chapter-plate 范式插入 12 个 reader 专题页')
    t = t.replace("/* W952：专题题图（线描人物/主题立像", "/* W953：专题题图（线描主题立像")
    io.open(DST, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))

    # ---- 核对产物（派生纪律）----
    chk = io.open(DST, encoding="utf-8").read()
    n_jobs = chk.count('("site/reader/themes/')
    print("产物：%s" % os.path.basename(DST))
    print("  JOBS 条数 = %d（应为 12）" % n_jobs)
    assert n_jobs == 12, "JOBS 条数不对"
    assert "W952" not in chk.replace("_w952", ""), "仍有 W952 残留"
    for line in chk.split("\n"):
        s = line.strip()
        if s.startswith('("site/reader/themes/'):
            print("  " + s[:96])
    print("  CSS 注释含 W953: %s" % ("W953" in chk))
    return 0


if __name__ == "__main__":
    sys.exit(main())
