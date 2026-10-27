#!/usr/bin/env python3
"""_w988_plan.py — W988 落位定案表（单一事实源·供预检/接入/og派生三处共用）

落位口径（用户 2026-10-27 选区指定 + 问卷裁定）：
  · 13 张人物卡 → 角色页 / 回目页顶部「横幅」= `.chapter-banner`（派生 1200×500 宽幅）
  · 14 张场景卡 → 主题页「场景位」= `.chapter-scene`（1:1 原图·不裁）

字段说明：
  card     源图 stem（site/static/images/<card>.webp）
  target   落位页（相对仓根）
  slot     banner | scene
  where    banner: after-h1（h1 之后、题图之前）| scene: before-h2（正文首个 h2 之前）
  subject  画面题材（用于 alt 文本与落位理由）
  src      源图类别：card1（1:1 水墨卡）| plate34（3:4 线描母版·仅供 og 派生）
"""
from __future__ import annotations

# ---------- 13 张人物卡 → 顶部横幅 ----------
BANNERS = [
    {"card": "card-14-bajie-choupa", "target": "site/reader/people/猪八戒.html",
     "subject": "猪八戒正面立像·双手横持九齿钉耙",
     "why": "主角色页·八戒标准像·与既有线描题图（plate-line-03）上下分层"},
    {"card": "card-13-bajie-yuexia", "target": "site/reader/themes/猪八戒-不愿承认的自己.html",
     "subject": "猪八戒月下扛耙行走·身后一轮满月",
     "why": "主题页·「不愿承认的自己」的疲惫夜色·无题图不抢位"},
    {"card": "card-15-bajie-zuoxie", "target": "site/reader/people/猪八戒-方向二深化.html",
     "subject": "猪八戒坐歇·钉耙横置于身侧",
     "why": "角色页深化·「随时准备散伙」的歇脚姿态·无题图"},
    {"card": "card-16-bajie-yunzhong", "target": "site/reader/people/猪八戒深化专题.html",
     "subject": "猪八戒戴斗笠挑担行路·担上货箱",
     "why": "角色页专题·劳作形态的八戒·无题图"},
    {"card": "card-17-bajie-denggao", "target": "site/reader/ch019.html",
     "subject": "猪八戒登高远望·崖下远处一点朱红",
     "why": "回目页·第019回云栈洞收八戒·八戒初出场的远望姿态·该回无题图"},
    {"card": "card-18-bajie-daodan", "target": "site/reader/ch031.html",
     "subject": "猪八戒挑担走在山路·身后是开阔的群山",
     "why": "回目页·第031回八戒义激猴王·赶路形态·该回无题图"},
    {"card": "card-19-shaseng-dujiang", "target": "site/reader/people/沙僧.html",
     "subject": "沙僧立像·肩扛月牙刃降妖宝杖",
     "why": "主角色页·沙僧标准像·无题图"},
    {"card": "card-20-shaseng-zhenshui", "target": "site/reader/themes/沙僧-沉默者的智慧.html",
     "subject": "沙僧执杖立于水纹之上·周身水痕",
     "why": "主题页·「最沉默的人」的镇水定相·该页已有线描题图（plate-line-04）→ 横幅置 h1 后题图前"},
    {"card": "card-21-shaseng-shouye", "target": "site/reader/people/沙僧-方向二深化.html",
     "subject": "沙僧守夜·盘坐于灯前·身侧一盏灯火",
     "why": "角色页深化·「从不惹事的人」的守夜·无题图"},
    {"card": "card-22-shaseng-fuzhong", "target": "site/reader/people/沙僧外传.html",
     "subject": "沙僧背负大包袱行于山间石阶",
     "why": "角色页外传·负重前行的沙僧·无题图"},
    {"card": "card-26-wukong-jingu", "target": "site/reader/people/孙悟空.html",
     "subject": "悟空背影·手握金箍棒立于山崖",
     "why": "主角色页·悟空背影·无题图"},
    {"card": "card-23-shixiong-bingli", "target": "site/reader/themes/取经团队-凭什么走到西天.html",
     "subject": "师兄弟三人并立山路·悟空执棒在前",
     "why": "团队主题页·三人同框的团队图·无题图"},
    {"card": "card-24-shixiong-shanmen", "target": "site/reader/people/取经团队动力学深化专题.html",
     "subject": "师兄弟立于山门之前·背影远望",
     "why": "团队专题页·山门前的背影·无题图",
     # 裁切特例：原图上部 2/3 是山门巨石、下部才是三人 ⇒ 通用「主体顶−30」会把人物整段切掉。
     # 此处改为保人物的下带（山门取其下缘），使横幅主体仍是三个人。
     "banner_crop": [389, 889]},
]

# ---------- 14 张场景卡 → 主题页场景位 ----------
SCENES = [
    {"card": "card-01-huoshan", "target": "site/reader/people/火焰山土地外传.html",
     "subject": "火焰山远景·山口赤焰与熔岩河",
     "why": "「那场火不是我放的·但我守了一辈子」·火焰山实景页"},
    {"card": "card-02-tongtianhe", "target": "site/reader/themes/无字真经专题.html",
     "subject": "通天河渡口·冰裂纹水面与横舟",
     "why": "无字真经在通天河沉没·该页已有线描题图→场景图下沉到正文首个 h2 前"},
    {"card": "card-03-shituoling", "target": "site/reader/people/狮驼岭三魔-方向二深化.html",
     "subject": "狮驼岭峰顶三魔剪影·云海翻涌",
     "why": "三魔立像剪影·该页已有线描题图→场景图下沉"},
    {"card": "card-04-dushuangxuejiang", "target": "site/reader/poetry/原著景物诗赏析专题.html",
     "subject": "雪江独钓·一叶孤舟横于寒水",
     "why": "「独钓寒江雪」意境·景物诗赏析页·无题图"},
    {"card": "card-05-mingyuesongjian", "target": "site/reader/poetry/原著景物诗分类赏析专题.html",
     "subject": "明月松间·一轮赭金满月与松枝云气",
     "why": "景物诗分类赏析·该页已有题图→场景图下沉"},
    {"card": "card-06-yunshenzhibu", "target": "site/reader/themes/空间叙事学专题.html",
     "subject": "云深山远·层峦叠嶂间一条小径",
     "why": "空间纵深·空间叙事学主题页·无题图"},
    {"card": "card-07-baiyao", "target": "site/reader/themes/小妖生命史专题.html",
     "subject": "百妖列阵·虫豸狮象各据一方",
     "why": "小妖群像·小妖生命史主题页·无题图"},
    {"card": "card-08-zhuowuquan", "target": "site/reader/people/蜘蛛精.html",
     "subject": "濯垢泉·石拱洞内一道垂瀑",
     "why": "濯垢泉实景·该页已有题图（濯垢泉池）→场景图下沉"},
    {"card": "card-09-sanyao", "target": "site/reader/people/白鹿精-方向二深化.html",
     "subject": "三妖之一·白鹿立于旗与牌坊之下",
     "why": "「一千一百一十一个心洞」·角色页·无题图"},
    {"card": "card-10-gusichenzhong", "target": "site/reader/culture/西游与佛教禅宗专题.html",
     "subject": "古寺晨钟·苍松掩映的殿宇与石亭",
     "why": "古寺禅境·佛教禅宗专题页·无题图"},
    {"card": "card-11-songyunshitan", "target": "site/reader/themes/水帘洞-瀑布门的世界.html",
     "subject": "松云石坛·孤松倚石与云气回旋",
     "why": "水帘洞石景·水帘洞主题页·无题图"},
    {"card": "card-12-shuyuanxingtantan", "target": "site/reader/themes/取经教育学专题.html",
     "subject": "书院杏坛·杏花枝下的讲堂与讲席",
     "why": "讲学场景·取经教育学主题页·无题图"},
    {"card": "card-25-santiebaigujing", "target": "site/reader/people/白骨精外传.html",
     "subject": "洞中白骨堆与一条朱红蛇影",
     "why": "「那具白骨在遇见取经人之前」·角色页·无题图"},
    {"card": "card-27-rejiao-fenxi", "target": "site/reader/themes/佛学AI西游三维语义映射表.html",
     "subject": "点阵分布图·黑点矩阵中一簇朱红高亮",
     "why": "点阵即语义分布·与「三维语义映射表」页数据图形语言同构·无题图"},
]

ALL = BANNERS + SCENES

if __name__ == "__main__":
    print("横幅", len(BANNERS), "场景", len(SCENES), "合计", len(ALL))
    assert len({b["card"] for b in BANNERS}) == len(BANNERS), "横幅 card 重复"
    assert len({s["card"] for s in SCENES}) == len(SCENES), "场景 card 重复"
    assert len({b["target"] for b in BANNERS}) == len(BANNERS), "横幅目标页重复"
    assert len({s["target"] for s in SCENES}) == len(SCENES), "场景目标页重复"
    assert not ({b["target"] for b in BANNERS} & {s["target"] for s in SCENES}), "横幅/场景目标页交叉"
    print("自检：27 张唯一 · 27 个目标页唯一 · 横幅与场景目标页无交叉")
