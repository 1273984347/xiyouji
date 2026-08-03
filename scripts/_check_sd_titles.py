#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复查：每个 SD 切片的 标题主题 是否与 正文主题 一致（识别 SD001 式“标题≠正文”真 corruption）。
若 标题主题 == 正文主题，但二者都≠声明回号 → 仅是“对应回号”注释漂移（非内容错装）。
若 标题主题 != 正文主题 → 真 corruption 候选。"""
import os, re, glob
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHENDU = os.path.join(ROOT, "source", "原文", "shendu")

# 复用 v2 的术语表（节选关键项）
TERMS = [
    ("花果山",[1]),("水帘洞",[1,57]),("美猴王",[1]),("灵台方寸山",[1,2]),("菩提祖师",[1,2]),("须菩提",[1,2]),
    ("金箍棒",[3]),("弼马温",[4]),("齐天大圣",[4]),("蟠桃",[4,5]),("大闹天宫",[5]),("八卦炉",[5]),
    ("二郎神",[6]),("五行山",[7,14]),("两界山",[7,14]),
    ("观音禅院",[16]),("黑风山",[16,17]),("高老庄",[18,19]),("云栈洞",[18,19]),("猪八戒",[18,19]),
    ("黄风岭",[20,21]),("流沙河",[22]),("沙僧",[22]),
    ("四圣试禅心",[23]),("黎山老母",[23]),("撞天婚",[23]),
    ("五庄观",[24,25,26]),("镇元大仙",[24,25,26]),("人参果",[24,25,26]),
    ("白骨精",[27]),("尸魔",[27]),
    ("黄袍怪",[28,29,30,31]),("奎木狼",[28,29,30,31]),("宝象国",[29,30]),("百花羞",[30]),
    ("平顶山",[32,33,34,35]),("金角",[32,33,34,35]),("银角",[32,33,34,35]),("紫金红葫芦",[33,34,35]),("芭蕉扇",[33,34,35,59,60,61]),
    ("乌鸡国",[36,37,38,39]),("青狮",[37,38,39,74,75]),("文殊",[39]),
    ("红孩儿",[40,41,42]),("火云洞",[40,41,42]),("圣婴大王",[40,41,42]),("三昧真火",[41]),("善财童子",[42]),
    ("黑水河",[43]),("鼍龙",[43]),("西海龙王",[43]),
    ("车迟国",[44,45,46]),("虎力",[44,45,46]),("鹿力",[44,45,46]),("羊力",[44,45,46]),("三清",[44,45]),("求雨",[45]),
    ("通天河",[47,48,49]),("灵感大王",[47,48,49]),("陈家庄",[47,48]),
    ("金兜洞",[50,51,52]),("青牛精",[50,51,52]),("独角兕",[50,51,52]),
    ("女儿国",[53,54,55]),("子母河",[53,54]),("落胎泉",[53,54]),("蝎子精",[55]),("昴日星官",[55]),
    ("盗贼",[56]),("杀贼",[56]),("真假美猴王",[57,58]),("六耳猕猴",[57,58]),
    ("火焰山",[59,60,61]),("铁扇公主",[59,60,61]),("罗刹",[59,60,61]),("牛魔王",[60,61]),("三借芭蕉扇",[61]),
    ("祭赛国",[62,63]),("九头虫",[63]),
    ("荆棘岭",[64]),("树精",[64]),("杏仙",[64]),
    ("小雷音寺",[65,66]),("黄眉怪",[65,66]),("弥勒",[66]),
    ("七绝山",[67]),
    ("朱紫国",[68,69,70,71]),("金圣宫",[69,70,71]),("赛太岁",[70,71]),("金毛犼",[70,71]),
    ("盘丝洞",[72,73]),("蜘蛛精",[72,73]),("蜈蚣精",[73]),
    ("狮驼岭",[74,75,76,77]),("大鹏",[74,75,76,77]),("白象",[74,75,76,77]),
    ("比丘国",[78,79]),("白鹿",[78,79]),
    ("老鼠精",[80,81,82,83]),("无底洞",[81,82,83]),
    ("灭法国",[84]),("钦法国",[84]),
    ("隐雾山",[85,86]),("豹子精",[85,86]),
    ("凤仙郡",[87]),
    ("玉华州",[88,89,90]),("黄狮精",[88,89,90]),("九头狮",[90]),("九灵元圣",[90]),
    ("金平府",[91,92]),("犀牛精",[91,92]),
    ("天竺国",[93,94,95]),("玉兔精",[95]),
    ("寇员外",[96,97]),
    ("凌云渡",[98]),("老龟",[99]),("晒经石",[100]),
]


def read(p):
    return open(p, encoding="utf-8").read()


def parse_declared(body):
    m = re.search(r"推测对应原著回号:\s*第(\d+)(?:-(\d+))?回", body)
    if not m:
        return None
    a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
    return list(range(a, b + 1))


def extract_body(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"^#\s.*$", "", text, count=1, flags=re.MULTILINE)
    return text


def subject_of(text):
    """返回文本命中的回次 Counter（去重术语，每术语每回 +1）。"""
    c = Counter()
    for term, chs in TERMS:
        if term in text:
            for ch in chs:
                c[ch] += 1
    return c


def main():
    files = sorted(glob.glob(os.path.join(SHENDU, "SD*.md")))
    true_corrupt = []   # 标题≠正文
    drift = []          # 标题==正文，但都≠声明
    for p in files:
        base = os.path.basename(p)
        m = re.match(r"SD(\d+)\.md", base)
        if not m:
            continue
        num = int(m.group(1))
        txt = read(p)
        declared = parse_declared(txt)
        # 提取标题（第一个 # 行中 “·” 之后的部分）
        first = txt.splitlines()[0] if txt.splitlines() else ""
        title = first.split("·", 1)[1].strip() if "·" in first else first
        body = extract_body(txt)
        ts = subject_of(title)      # 标题主题
        bs = subject_of(body)       # 正文主题
        t_top = ts.most_common(1)[0][0] if ts else None
        b_top = bs.most_common(1)[0][0] if bs else None
        # 判定
        if t_top is not None and b_top is not None and t_top != b_top:
            true_corrupt.append((num, declared, title, t_top, b_top, ts.most_common(3), bs.most_common(3)))
        elif t_top is not None and b_top is not None and declared is not None and t_top not in declared and b_top not in declared:
            drift.append((num, declared, title, t_top, b_top))
    print(f"=== 真 corruption 候选（标题主题≠正文主题）: {len(true_corrupt)} ===")
    for num, dec, title, t, b, t3, b3 in true_corrupt:
        print(f"SD{num:03d} 声明{dec} 标题→第{t}回 正文→第{b}回 | 标题'{title}'")
        print(f"   标题命中{t3} | 正文命中{b3}")
    print(f"\n=== 注释漂移（标题==正文，但都≠声明回号）: {len(drift)} ===")
    for num, dec, title, t, b in drift:
        print(f"SD{num:03d} 声明{dec} 实际主题≈第{b}回 | 标题'{title}'")
    # 也打印正文无主题的切片（可能早期/综述类）
    print("\n=== 正文无锚点主题的切片（需人工看是否综述/过渡） ===")
    for p in files:
        num = int(re.match(r"SD(\d+)\.md", os.path.basename(p)).group(1))
        bs = subject_of(extract_body(read(p)))
        if not bs:
            dec = parse_declared(read(p))
            print(f"SD{num:03d} 声明{dec}")


if __name__ == "__main__":
    main()
