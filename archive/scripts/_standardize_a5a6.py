import os
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A5/A6 全量结构标准化 v2（统一 footer，不破坏已有交叉引用）。
对每个非 README 文件：
1) 轨标 元数据：缺则补（A5=教学讲解/诗词歌赋；A6=个人创作/跨学科随笔），已有则保留。
2) 末尾统一 footer 块：
   - 剥离原尾部所有 "> 导航" / "> 关联" 行，收集其链接；
   - 写标准 导航：[返回本辑](README.md) · [站点首页](../../site/index.html) [+ 原导航里的额外链接]；
   - 写 关联分析：A3 人物 + A1 逐回 链接 [+ 原关联里的额外链接]，去重。
全部幂等。DRY_RUN（不带 --apply）仅打印。
"""
import os, re, glob, sys

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A3 = os.path.join(ROOT, "docs", "02-人物深度分析")
A1 = os.path.join(ROOT, "docs", "01-全书逐回解读")
A5 = os.path.join(ROOT, "docs", "05-诗词歌赋")
A6 = os.path.join(ROOT, "docs", "06-个人随笔")
DRY_RUN = "--apply" not in sys.argv

ALIAS = {
    "悟空": "孙悟空", "孙猴子": "孙悟空", "美猴王": "孙悟空", "斗战胜佛": "孙悟空",
    "玄奘": "唐僧", "三藏": "唐僧", "唐僧": "唐僧",
    "八戒": "猪八戒", "猪八戒": "猪八戒", "老猪": "猪八戒",
    "沙僧": "沙僧", "沙和尚": "沙僧", "卷帘": "沙僧",
    "小白龙": "白龙马", "白龙马": "白龙马", "小龙": "白龙马",
    "菩提": "菩提祖师", "菩提祖师": "菩提祖师", "须菩提": "菩提祖师",
    "玉帝": "玉帝", "玉皇": "玉帝", "玉皇大帝": "玉帝",
    "如来": "如来", "佛祖": "如来", "如来佛祖": "如来",
    "观音": "观音", "菩萨": "观音", "观世音": "观音",
    "太上老君": "太上老君", "老君": "太上老君",
    "二郎神": "二郎神", "杨戬": "二郎神",
    "哪吒": "哪吒",
    "铁扇公主": "铁扇公主", "罗刹": "铁扇公主", "芭蕉扇": "铁扇公主",
    "牛魔王": "牛魔王",
    "红孩儿": "红孩儿", "圣婴": "红孩儿",
    "镇元大仙": "镇元大仙", "镇元子": "镇元大仙",
    "六耳猕猴": "六耳猕猴",
    "白骨精": "白骨精", "白骨夫人": "白骨精",
    "金箍棒": "孙悟空",
}
TERMS = [
    ("花果山",1),("水帘洞",1),("灵台方寸山",1),("菩提祖师",1),("须菩提",1),
    ("金箍棒",3),("定海神针",3),("傲来国",3),("四海龙王",3),
    ("弼马温",4),("齐天大圣",4),("蟠桃园",4),("蟠桃",4),("大闹天宫",5),("八卦炉",5),("兜率宫",5),
    ("二郎神",6),("灌江口",6),("梅山六圣",6),
    ("五行山",7),("两界山",7),("安天大会",7),
    ("观音禅院",16),("黑风山",16),("黑熊精",16),("金池",16),
    ("高老庄",18),("云栈洞",18),("猪八戒",18),
    ("黄风岭",20),("黄风怪",20),("灵吉",20),
    ("流沙河",22),("沙僧",22),
    ("四圣试禅心",23),("黎山老母",23),("撞天婚",23),
    ("五庄观",24),("镇元大仙",24),("人参果",24),
    ("白骨精",27),("尸魔",27),("三打白骨精",27),
    ("黄袍怪",28),("奎木狼",28),("宝象国",29),("百花羞",30),
    ("平顶山",32),("金角",32),("银角",32),("紫金红葫芦",33),("莲花洞",32),
    ("乌鸡国",36),("假国王",37),("青狮",37),("文殊",39),
    ("红孩儿",40),("火云洞",40),("三昧真火",41),("善财童子",42),
    ("黑水河",43),("鼍龙",43),("西海龙王",43),
    ("车迟国",44),("虎力",44),("鹿力",44),("羊力",44),("三清",44),("求雨",45),
    ("通天河",47),("灵感大王",47),("陈家庄",47),("鱼篮",49),("竹篮",49),
    ("金兜洞",50),("青牛精",50),("独角兕",50),("金刚琢",50),
    ("女儿国",53),("子母河",53),("落胎泉",53),("蝎子精",55),("昴日星官",55),
    ("真假美猴王",57),("六耳猕猴",57),
    ("火焰山",59),("铁扇公主",59),("牛魔王",60),("积雷山",60),("三借芭蕉扇",61),
    ("祭赛国",62),("金光寺",62),("九头虫",63),("舍利",62),
    ("荆棘岭",64),("树精",64),("杏仙",64),
    ("小雷音寺",65),("黄眉怪",65),("弥勒",66),
    ("七绝山",67),("红鳞大蟒",67),
    ("朱紫国",68),("金圣宫",68),("赛太岁",70),("金毛犼",70),("紫阳真人",71),
    ("盘丝洞",72),("蜘蛛精",72),("濯垢泉",72),("多目怪",73),("蜈蚣精",73),("毗蓝婆",73),
    ("狮驼岭",74),("大鹏",74),("白象",74),("阴阳二气瓶",75),
    ("比丘国",78),("国丈",78),("白鹿",78),("寿星",79),
    ("老鼠精",80),("无底洞",81),("地涌夫人",80),("托塔李天王",83),
    ("灭法国",84),("钦法国",84),
    ("隐雾山",85),("豹子精",85),
    ("凤仙郡",87),("米山",87),("面山",87),
    ("玉华州",88),("黄狮精",88),("九头狮",90),("九灵元圣",90),
    ("金平府",91),("犀牛精",91),("四木禽星",92),
    ("天竺国",93),("玉兔精",95),("太阴星君",95),
    ("寇员外",96),("铜台府",96),
    ("凌云渡",98),("老龟",99),("晒经石",100),("无字经",100),
]


def a3_links(body):
    out, seen = [], set()
    for alias, canon in ALIAS.items():
        if canon in seen:
            continue
        if alias in body:
            f = os.path.join(A3, canon + ".md")
            if os.path.exists(f):
                out.append((canon, f"../02-人物深度分析/{canon}.md"))
                seen.add(canon)
        if len(out) >= 5:
            break
    return out


def a1_links(body):
    cnt = {}
    for term, ch in TERMS:
        if term in body:
            cnt[ch] = cnt.get(ch, 0) + 1
    top = sorted(cnt.items(), key=lambda x: -x[1])[:3]
    out = []
    for ch, _ in top:
        ms = [os.path.basename(m) for m in glob.glob(os.path.join(A1, f"第{ch:03d}回-*.md"))]
        ms = [m for m in ms if m != "README.md"]
        if ms:
            out.append((f"第{ch}回", f"../01-全书逐回解读/{ms[0]}"))
    return out


def process(path, kind):
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    lines = txt.split("\n")

    # 收集并剥离原 footer（> 导航 / > 关联）
    old_nav, old_rel = [], []
    body_lines = []
    for l in lines:
        s = l.strip()
        if s.startswith("> 导航"):
            for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", s):
                old_nav.append((m.group(1), m.group(2)))
        elif s.startswith("> 关联"):
            for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", s):
                old_rel.append((m.group(1), m.group(2)))
        else:
            body_lines.append(l)
    while body_lines and body_lines[-1].strip() == "":
        body_lines.pop()

    # 轨标
    has_gui = any(l.strip().startswith("> 轨标") for l in body_lines[:6])
    if not has_gui:
        idx = next((i for i, l in enumerate(body_lines) if l.startswith("# ")), 0)
        block = (["> 轨标：教学讲解", "> 主题类别：诗词歌赋",
                  "> 数据来源：原著诗词（回前引诗·回中状物·回末收束诗）"] if kind == "A5"
                 else ["> 轨标：个人创作", "> 主题类别：跨学科随笔"])
        body_lines[idx+1:idx+1] = [""] + block

    # 计算新链接
    a3 = a3_links(txt)
    a1 = a1_links(txt)

    def dedupe(seq):
        seen, res = set(), []
        for t, u in seq:
            if u in seen:
                continue
            seen.add(u); res.append((t, u))
        return res

    # 导航：标准两项 + 原导航里的额外项（去重）
    nav = [("返回本辑", "README.md"), ("站点首页", "../../site/index.html")]
    for t, u in old_nav:
        if u not in ("README.md", "../../site/index.html"):
            nav.append((t, u))
    nav = dedupe(nav)

    # 关联分析：A3 + A1（新标准）+ 原关联额外项
    rel = [(t, u) for t, u in a3 + a1]
    for t, u in old_rel:
        if not u.startswith("../02-人物深度分析/") and not u.startswith("../01-全书逐回解读/"):
            rel.append((t, u))
    rel = dedupe(rel)

    nav_line = "> 导航：" + " · ".join(f"[{t}]({u})" for t, u in nav)
    rel_line = "> 关联分析：" + " · ".join(f"[{t}]({u})" for t, u in rel)

    new_txt = "\n".join(body_lines) + "\n\n" + nav_line + "\n" + rel_line + "\n"

    if new_txt != txt:
        if DRY_RUN:
            print(f"[DRY] {os.path.relpath(path, ROOT)} 导航{len(nav)} 关联{len(rel)} (原导航{len(old_nav)} 原关联{len(old_rel)})")
        else:
            with _w536_guard_open(path, "w", encoding="utf-8") as f:
                f.write(new_txt)
            print(f"[APPLY] {os.path.relpath(path, ROOT)} 导航{len(nav)} 关联{len(rel)}")
    else:
        print(f"[skip] {os.path.relpath(path, ROOT)}")


def main():
    for kind, d in (("A5", A5), ("A6", A6)):
        for p in sorted(glob.glob(os.path.join(d, "*.md"))):
            if os.path.basename(p) == "README.md":
                continue
            process(p, kind)
    print("\n模式:", "DRY_RUN" if DRY_RUN else "APPLY")


if __name__ == "__main__":
    main()
