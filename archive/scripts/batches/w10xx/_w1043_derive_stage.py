# -*- coding: utf-8 -*-
"""_w1043_derive_stage.py — 由归档的 _w1018_stage.py **程序化派生** W1043 落位脚本

派生纪律（坑表 E-37）：程序化派生 + 残留断言；JOBS 为**内容**（非常量）⇒ 显式替换整块，
替换后断言条目数 = 12 且回号互不重复（同页两题图不被落位脚本支持 ⇒ 必须互斥）。
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
SRC = os.path.join(REPO, "archive", "scripts", "batches", "w10xx", "_w1018_stage.py")
DST = os.path.join(REPO, "archive", "scripts", "batches", "w10xx", "_w1043_stage.py")

REPO_EXPR = ("REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(\n"
             "    os.path.dirname(os.path.abspath(__file__))))))")

JOBS = '''JOBS = [
    ("ch053", "plate-line-85-ch053-ruyizhenxian.webp",
     "如意真仙的线描立像：七瓣莲花冠、宽袖道袍，双手捧一枚圆润果实"),
    ("ch033", "plate-line-86-ch033-chuikouxian.webp",
     "吹口仙的线描立像：斗笠宽檐、宽袖短褂，双手交叠腹前作吹哨之姿"),
    ("ch094", "plate-line-87-ch094-taiyinxingjun.webp",
     "太阴星君的线描立像：高挽发髻插一支素簪，广袖长裙、双手拢于袖中"),
    ("ch073", "plate-line-88-ch073-duomuguai.webp",
     "多目怪的线描立像：素色冠帽、宽袖长袍，额面与两颊散布数枚圆形小眼"),
    ("ch069", "plate-line-89-ch069-ziyangzhenren.webp",
     "紫阳真人的线描立像：莲花冠、宽袖道袍，双手捧一只扁圆形葫芦"),
    ("ch090", "plate-line-90-ch090-yijiukutianzun.webp",
     "乙救苦天尊的线描立像：莲瓣冠、宽袖帝君袍，双手结印于胸前"),
    ("ch071", "plate-line-91-ch071-jiuling-shiba.webp",
     "九灵元圣与十八罗汉的线描场面：独角仙人与两列罗汉同框"),
    ("ch086", "plate-line-92-ch086-bihan-bishu.webp",
     "辟寒大王与辟暑大王的线描场面：冰棱角冠与薄片角冠两名妖王相对而立"),
    ("ch095", "plate-line-93-ch095-yumian.webp",
     "玉面狐狸与猴形行者的线描场面：白面狐妖拈诀，与执棒行者相对"),
    ("ch029", "plate-line-94-ch029-bengpo-baboren.webp",
     "奔波儿灞与灞波儿奔的线描场面：水纹帽两名巡海小妖并肩而行"),
    ("ch085", "plate-line-95-ch085-diyongfuren.webp",
     "地涌夫人与猴形行者的线描场面：白鼻鼠妖作拈诀之姿，与执棒行者隔洞对峙"),
    ("ch097", "plate-line-96-ch097-xiniu.webp",
     "犀牛怪与猴形行者的线描场面：额生粗短独角的犀牛妖，与执棒行者隔山对峙"),
]'''

text = io.open(SRC, encoding="utf-8").read()
text = text.replace(
    'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))', REPO_EXPR)
text = text.replace("W1016：回目题图", "W1043：回目题图")
text = text.replace("_w1018_stage.py", "_w1043_stage.py")
# 归档面缺 subject_band 模块 ⇒ sys.path 需并入 scripts/（W1043 补）
text = text.replace(
    'sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))',
    'sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n'
    'sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(\n'
    '    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))), "scripts"))')

# JOBS 整块替换
m = re.search(r"JOBS = \[.*?\n\]", text, re.S)
if not m:
    print("FAIL  源脚本未找到 JOBS 块")
    raise SystemExit(1)
text = text[:m.start()] + JOBS + text[m.end():]

# 残留断言（路径/文件名常量）
for bad in ("_w1018", "huxianfeng", "qingfeng"):
    if bad in text:
        print("FAIL  派生产物残留源常量：%s" % bad)
        raise SystemExit(1)

# 断言：条目 12 + 回号互不重复
ch_list = re.findall(r'\("(ch\d{3})",', text)
if len(ch_list) != 12 or len(set(ch_list)) != 12:
    print("FAIL  JOBS 回号异常：%d 条·唯一 %d" % (len(ch_list), len(set(ch_list))))
    raise SystemExit(1)

io.open(DST, "w", encoding="utf-8", newline="\n").write(text)
print("OK    派生 %s（%d 字符·JOBS 12 条·回号唯一）"
      % (os.path.relpath(DST, REPO).replace("\\", "/"), len(text)))
