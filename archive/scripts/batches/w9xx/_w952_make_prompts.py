# -*- coding: utf-8 -*-
"""_w952_make_prompts.py — W952 出图参数生成（风格段从上批母版程序化复用·只换构图句）

做法：
  1. 读上批 `_w945_batch1.json` 的母版（252 字符）
  2. **只替换构图句**：「画面上方 28% 保持完全空白的纯纸面…用于叠放标题文字」⇒
     「画面主体上方只保留约一成的纯纸面呼吸空间，不设专用标题区（页面标题在图外）」
     ⇒ 风格段（宣纸底 / 墨线 / 色板 / 点睛 / 禁项 / 全身立像构图）**逐字未动**
  3. 拼本批 12 条 SUBJECT 段 ⇒ 写 3 个 batch json（各 4 条）
  4. 自带断言：① 本批 12 条母版逐字一致 ② 本批母版去掉构图句后与上批母版**逐字一致**（风格同族）

输出：scripts/output/_w952_batch1.json / _w952_batch2.json / _w952_batch3.json
"""
import io
import json
import os
import sys

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")
SRC = os.path.join(OUT, "_w945_batch1.json")

OLD_COMPOSE = "画面上方 28% 保持完全空白的纯纸面（不得有任何笔触或色彩），用于叠放标题文字；"
NEW_COMPOSE = "画面主体上方只保留约一成的纯纸面呼吸空间，不设专用标题区（页面标题在图外）；"

# (序号 stem, 主体, SUBJECT 段)
SUBJECTS = [
    # —— 人物 8 ——
    ("01-bailongma", "白龙马",
     "小白龙的完整全身立像，一位白衣龙君，头戴金冠、身着素色道袍、肩披浅色氅衣，双手横持一杆三叉戟；"
     "身后隐约浮起一条白龙龙影（龙身弯曲、鳞纹可辨、不喧宾夺主），面容俊朗沉静，双腿直立站姿。"),
    ("02-dujiao-shengwang", "独角兕大王",
     "青牛精的完整全身立像，一个牛首独角（额心一只竖直长角）、阔口獠牙的青牛妖王，身披乌金铠甲，"
     "双手横持一杆方头钢叉（叉身有环），身形魁梧，双腿直立站姿。"),
    ("03-linggan", "灵感大王",
     "金鱼精的完整全身立像，一位头戴王冠、身着龙袍的鱼王，下身是覆满鳞片的鱼尾（尾鳍分叉展开），"
     "双手托着一只盛水的玉钵，颈挂佛珠，神态倨傲，双腿直立站姿。"),
    ("04-huangfengguai", "黄风怪",
     "黄毛貂鼠精的完整全身立像，一个尖嘴圆耳的黄鼠狼身妖王（毛色金黄），头戴毗卢帽、身披僧式黄袍，"
     "双手持一把大芭蕉扇（叶形长卵扇面、中脉与细脉清晰、柄端缠绳），身侧卷起三道风纹，双腿直立站姿。"),
    ("05-saitaisui", "赛太岁",
     "赛太岁的完整全身立像，一只人面兽身的金毛犼（人面、狮身、金黄鬃毛），身披红色法衣、头戴金冠，"
     "颈挂一枚硕大的紫金铃（铃身有云纹与铃舌），凶相毕露，双腿直立站姿。"),
    ("06-jiuLingyuansheng", "九灵元圣",
     "九灵元圣的完整全身立像，一只九头狮王的真身（狮身雄健，颈部同时生出九个狮头、其中三个正面可见、"
     "其余侧向或背向，鬃毛层叠），四足稳稳立住地面，双腿直立站姿。"),
    ("07-nezha", "哪吒",
     "哪吒的完整全身立像，一位少年神将，双髻束发、身披红色战袍，颈挂乾坤圈（项圈形金圈），"
     "一手持火尖枪（枪尖燃着赤焰）、一手持混天绫（红绫向侧后飘展），脚下踩着一对风火轮，双腿直立站姿。"),
    ("08-angrixingguan", "昴日星官",
     "昴日星官的完整全身立像，一位头戴星冠、身着羽衣的神将，面部化作一只大公鸡的形貌"
     "（鸡冠高耸、喙锐利、颈羽层层），一手持长鞭（鞭梢系着金色铃），威风凛凛，双腿直立站姿。"),
    # —— 主题 4 ——
    ("09-jingu-topic", "紧箍咒专题",
     "紧箍咒主题的完整全身立像：悟空身披锁子甲、头戴金圈紧箍（金圈内缘一圈九个倒刺钩，钩尖清晰可辨），"
     "额前系着朱砂红绦（红绦绕过头顶垂向脑后），双手紧握金箍棒、身形微弓似在忍痛，神情凝重。"),
    ("10-jindouyun-topic", "筋斗云专题",
     "筋斗云主题：悟空的完整全身立像端坐于祥云之上（云是层叠的涡卷云团、拖尾向右上方卷出，"
     "云气用淡赭金线勾出），悟空头戴凤翅紫金冠、身着锁子甲，一手前指、衣袂向后飞扬，双腿屈于云上。"),
    ("11-fabao-topic", "法宝系统主题",
     "法宝系统主题：一名完整全身立像的道装仙人（头戴道冠、身着宽袖道袍）双手托举一排悬浮的法宝——"
     "紫金红葫芦、白瓷玉净瓶、芭蕉扇、乾坤圈、金钢琢，依次排开呈弧形、每件用细墨线勾出并以淡赭金描边，"
     "人物神情自得。"),
    ("12-wuzi-jing-topic", "无字真经专题",
     "无字真经主题：一名完整全身立像的比丘僧人（头戴毗卢帽、眉眼低垂）双手捧着一卷完全空白的经卷"
     "（卷面只有淡赭金的横向纹理、没有任何文字与字迹），卷轴两端垂下丝带，身前浮着一圈极淡的光晕线条，神情虔敬。"),
]


def main() -> int:
    src = json.load(io.open(SRC, encoding="utf-8"))
    old_master = src["requests"][0]["prompt"].split("主体：")[0]
    if OLD_COMPOSE not in old_master:
        print("FATAL 上批母版中未找到构图句（母版已变？）：%s" % old_master[-160:])
        return 2
    new_master = old_master.replace(OLD_COMPOSE, NEW_COMPOSE, 1)

    # 断言① 风格段一致：两批母版去掉各自构图句后逐字相同
    old_style = old_master.replace(OLD_COMPOSE, "", 1)
    new_style = new_master.replace(NEW_COMPOSE, "", 1)
    if old_style != new_style:
        print("FATAL 风格段与上批不一致（母版改动了构图句以外的内容）")
        for a, b in zip(old_style.split("。"), new_style.split("。")):
            if a != b:
                print("  差异句：上批「%s」 vs 本批「%s」" % (a[:70], b[:70]))
                break
        return 2
    print("风格段与上批逐字一致（%d 字符）· 构图句已换为「留一成呼吸空间」" % len(new_style))

    for bi in (1, 2, 3):
        items = SUBJECTS[(bi - 1) * 4: bi * 4]
        reqs = []
        for stem, _name, subject in items:
            reqs.append({
                "aspect_ratio": "3:4",
                "resolution": "2K",
                "output_file": "plate-line-%s.png" % stem,
                "prompt": new_master + "主体：" + subject,
            })
        # 断言② 批内母版逐字一致
        masters = {r["prompt"].split("主体：")[0] for r in reqs}
        if len(masters) != 1:
            print("FATAL batch%d 母版不一致" % bi)
            return 2
        p = os.path.join(OUT, "_w952_batch%d.json" % bi)
        io.open(p, "w", encoding="utf-8").write(
            json.dumps({"requests": reqs}, ensure_ascii=False, indent=2))
        print("写出 %s（%d 条）" % (os.path.basename(p), len(reqs)))

    print("\n本批母版全文：\n%s" % new_master)
    return 0


if __name__ == "__main__":
    sys.exit(main())
