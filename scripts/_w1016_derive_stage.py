# -*- coding: utf-8 -*-
"""_w1016_derive_stage.py — 由归档 `w10xx/_w1013_stage.py` **程序化派生** W1016 落位脚本

派生点（3 类）：
  ① 批号/文件名：_w1013_stage.py → _w1016_stage.py
  ② JOBS 块：换成本批 12 个回目页 + 站点版名 + alt（逐条替换整块，其余逻辑逐字继承）
  ③ 文档字符串：W1013 → W1016

残留断言：产物里不得出现 `w1013`（源批次痕迹）。
输出：scripts/_w1016_stage.py
"""
import io
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "archive", "scripts", "batches", "w10xx", "_w1013_stage.py")
DST = os.path.join(REPO, "scripts", "_w1016_stage.py")

JOBS_NEW = '''JOBS = [
    ("ch020", "plate-line-73-ch020-huxianfeng.webp",
     "虎先锋线描立像：虎首人身、宽袖战袍，双手横持一柄九齿钯"),
    ("ch024", "plate-line-74-ch024-qingfeng.webp",
     "清风童子的线描立像：双髻道童衣，双手捧一只木托盘，盘中两枚人参果"),
    ("ch034", "plate-line-75-ch034-bashanhu.webp",
     "巴山虎与倚海龙的线描场面：虎首与龙首两名小妖并肩，各执朴刀与长枪"),
    ("ch043", "plate-line-76-ch043-tuolong.webp",
     "鼍龙与摩昂的线描场面：龙母托三棱简、龙子按钢叉，对面猴形行者相对"),
    ("ch044", "plate-line-77-ch044-yangli.webp",
     "羊力大仙与猴形行者的线描场面：道冠妖道持拂尘，与执棒行者隔案相持"),
    ("ch049", "plate-line-78-ch049-laoyuan.webp",
     "老鼋的线描立像：龟首人身、白须垂胸，背负玄色甲壳伏于水中"),
    ("ch051", "plate-line-79-ch051-qingniu.webp",
     "青牛精与猴形行者的线描场面：额生独角的妖王左手套金圈，与执棒行者对峙"),
    ("ch064", "plate-line-80-ch064-xingxian.webp",
     "杏仙的线描立像：鬓发如云、宽袖长裙，右手执一柄素面折扇"),
    ("ch074", "plate-line-81-ch074-qingshi.webp",
     "青狮与白象的线描场面：狮首与象首两名魔头并肩，各执长柄兵器怒视猴形行者"),
    ("ch091", "plate-line-82-ch091-bidun.webp",
     "辟尘大王与猴形行者的线描场面：双角冠妖王双手握藤缠长柄兵器，与执棒行者对峙"),
    ("ch096", "plate-line-83-ch096-kouyuanwai.webp",
     "寇员外的线描立像：头戴方巾、宽袖锦袍，双手拱于身前相迎"),
    ("ch008", "plate-line-84-ch008-jinding.webp",
     "金顶大仙的线描立像：莲花冠、白须及胸，双手捧一柄拂尘端立"),
]'''

s = io.open(SRC, encoding="utf-8").read()
orig_len = len(s)

# ② JOBS 整块替换
s2, n = re.subn(r"JOBS = \[.*?\n\]", JOBS_NEW, s, count=1, flags=re.S)
assert n == 1, "未定位到 JOBS 块（派生中止）"
s = s2
# ① 批号/文件名
s = s.replace("_w1013_stage.py", "_w1016_stage.py").replace("W1013", "W1016")
s = s.replace("W1013 批", "W1016 批")
# 文档字符串首行
s = s.replace('"""_w1013_stage.py', '"""_w1016_stage.py')

# ---------- 残留断言 ----------
for bad in ("_w1013_", "W1013"):
    if bad in s:
        raise SystemExit("派生残留断言失败：产物仍含 %r" % bad)
assert "plate-line-84-ch008-jinding.webp" in s, "JOBS 替换未生效"

io.open(DST, "w", encoding="utf-8", newline="\n").write(s)
print("派生完成：%s（%d → %d 字符）· JOBS 12 条已换" % (os.path.basename(DST), orig_len, len(s)))
print("  残留断言 2/2 通过 ✓")
