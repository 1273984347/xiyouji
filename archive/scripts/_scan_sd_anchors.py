#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SD 切片错位（张冠李戴）扫描器 v2 —— 专有名词锚点法。

原理：
- 维护一份《西游记》专有名词 → 所属回次 的词典（仅收录各回“最具辨识度”的地名/人名/法宝/事件，
  排除孙悟空/唐僧/观音/如来等全书通用词，避免噪声）。
- 对每个 SD 切片，解析头部声明回次（支持单回与“第X-Y回”区间），统计正文命中的锚点并按回次归集。
- 若正文“完全由其他回次锚点主导、本回锚点为 0”（strong），或“其他回次锚点远多于本回”（likely），
  则判定疑似错位。
- 配套：输出每个切片的 top5 回次命中，便于人工审计。

相比 v1（余弦）：避开“现代评论 vs 古文原文”词表错位与模板 boilerplate 带来的假阳性，
专有名词在评论中会被原样复用，信号更稳。
"""
import os
import re
import glob
from collections import Counter

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHENDU = os.path.join(ROOT, "source", "原文", "shendu")
REPORT = os.path.join(ROOT, ".workbuddy", "sd_scan_v2.md")

# term -> [chapters]
TERMS = [
    # 1-22 早期
    ("花果山", [1]), ("水帘洞", [1, 57]), ("美猴王", [1]), ("灵台方寸山", [1, 2]),
    ("斜月三星洞", [1, 2]), ("菩提祖师", [1, 2]), ("须菩提", [1, 2]), ("樵夫", [1]),
    ("七十二变", [2]), ("筋斗云", [2]),
    ("傲来国", [3]), ("金箍棒", [3]), ("定海神针", [3]), ("四海龙王", [3]), ("阎王", [3]),
    ("弼马温", [4]), ("御马监", [4]), ("齐天大圣", [4]), ("蟠桃园", [4]), ("蟠桃", [4, 5]),
    ("大闹天宫", [5]), ("蟠桃会", [5]), ("兜率宫", [5]), ("金丹", [5]), ("炼丹炉", [5]), ("八卦炉", [5]),
    ("二郎神", [6]), ("梅山六圣", [6]), ("灌江口", [6]), ("金刚琢", [6, 50, 51, 52]), ("哮天犬", [6]),
    ("五行山", [7, 14]), ("两界山", [7, 14]), ("安天大会", [7]),
    ("观音奉旨", [8]), ("福陵山", [8, 18, 19]), ("袁守诚", [9]), ("泾河龙王", [9]), ("魏征", [9, 10]),
    ("唐太宗", [9, 10, 11, 12]), ("地府", [9, 10]), ("判官", [9, 10]), ("刘全", [11]),
    ("水陆大会", [12]), ("陈玄奘", [12]), ("袈裟", [12, 16]), ("锡杖", [12]),
    ("双叉岭", [13]), ("寅将军", [13]), ("太白金星", [13]), ("刘伯钦", [13]),
    ("六贼", [14]), ("紧箍咒", [14]),
    ("鹰愁涧", [15]), ("白龙马", [15]), ("小白龙", [15]), ("敖闰", [15]),
    ("观音禅院", [16]), ("金池长老", [16]), ("黑风山", [16, 17]), ("黑熊精", [16, 17]),
    ("高老庄", [18, 19]), ("高翠兰", [18, 19]), ("云栈洞", [18, 19]), ("猪八戒", [18, 19]), ("钉耙", [19]),
    ("黄风岭", [20, 21]), ("黄风怪", [20, 21]), ("灵吉菩萨", [20, 21]), ("三昧神风", [21]),
    ("流沙河", [22]), ("沙僧", [22]), ("卷帘大将", [22]), ("葫芦", [22, 33]),
    # 23 四圣试禅心
    ("四圣试禅心", [23]), ("黎山老母", [23]), ("撞天婚", [23]), ("真真爱爱怜怜", [23]),
    # 24-26 人参果
    ("万寿山", [24, 25, 26]), ("五庄观", [24, 25, 26]), ("镇元大仙", [24, 25, 26]),
    ("镇元子", [24, 25, 26]), ("人参果", [24, 25, 26]), ("草还丹", [24, 25, 26]),
    ("推倒人参果树", [25]), ("观音救活", [26]),
    # 27 白骨精
    ("三打白骨精", [27]), ("白骨夫人", [27]), ("尸魔", [27]), ("白骨精", [27]),
    # 28-31 黄袍怪
    ("黄袍怪", [28, 29, 30, 31]), ("奎木狼", [28, 29, 30, 31]), ("宝象国", [29, 30]),
    ("百花羞", [30]), ("碗子山", [28, 29]),
    # 32-35 金角银角
    ("平顶山", [32, 33, 34, 35]), ("金角", [32, 33, 34, 35]), ("银角", [32, 33, 34, 35]),
    ("莲花洞", [32, 33]), ("紫金红葫芦", [33, 34, 35]), ("芭蕉扇", [33, 34, 35, 59, 60, 61]),
    ("羊脂玉净瓶", [33]),
    # 36-39 乌鸡国
    ("宝林寺", [36, 37]), ("乌鸡国", [36, 37, 38, 39]), ("井龙王", [36, 38]),
    ("假国王", [37, 38]), ("青狮", [37, 38, 39, 74, 75]), ("文殊", [39]),
    # 40-42 红孩儿
    ("红孩儿", [40, 41, 42]), ("火云洞", [40, 41, 42]), ("圣婴大王", [40, 41, 42]),
    ("三昧真火", [41]), ("善财童子", [42]), ("金箍", [42]),
    # 43 黑水河
    ("黑水河", [43]), ("鼍龙", [43]), ("西海龙王", [43]),
    # 44-46 车迟国
    ("车迟国", [44, 45, 46]), ("虎力", [44, 45, 46]), ("鹿力", [44, 45, 46]),
    ("羊力", [44, 45, 46]), ("三清", [44, 45]), ("求雨", [45]),
    # 47-49 通天河
    ("通天河", [47, 48, 49]), ("灵感大王", [47, 48, 49]), ("陈家庄", [47, 48]),
    ("鱼篮", [49]), ("竹篮", [49]),
    # 50-52 金兜洞
    ("金兜洞", [50, 51, 52]), ("青牛精", [50, 51, 52]), ("独角兕", [50, 51, 52]),
    # 53-55 女儿国
    ("女儿国", [53, 54, 55]), ("子母河", [53, 54]), ("落胎泉", [53, 54]),
    ("蝎子精", [55]), ("琵琶精", [55]), ("昴日星官", [55]),
    # 56-58
    ("盗贼", [56]), ("杀贼", [56]), ("真假美猴王", [57, 58]), ("六耳猕猴", [57, 58]),
    # 59-61 火焰山
    ("火焰山", [59, 60, 61]), ("铁扇公主", [59, 60, 61]), ("罗刹", [59, 60, 61]),
    ("牛魔王", [60, 61]), ("积雷山", [60, 61]), ("玉面狐狸", [60, 61]), ("三借芭蕉扇", [61]),
    # 62-63 祭赛国
    ("祭赛国", [62, 63]), ("金光寺", [62, 63]), ("舍利", [62, 63]),
    ("九头虫", [63]), ("万圣龙王", [63]), ("碧波潭", [63]),
    # 64 荆棘岭
    ("荆棘岭", [64]), ("树精", [64]), ("杏仙", [64]), ("木耳", [64]),
    # 65-66 小雷音寺
    ("小雷音寺", [65, 66]), ("黄眉怪", [65, 66]), ("金铙", [65]), ("弥勒", [66]), ("人种袋", [66]),
    # 67 七绝山
    ("七绝山", [67]), ("红鳞大蟒", [67]), ("稀柿衕", [67]),
    # 68-71 朱紫国
    ("朱紫国", [68, 69, 70, 71]), ("金圣宫", [69, 70, 71]), ("赛太岁", [70, 71]),
    ("金毛犼", [70, 71]), ("紫阳真人", [71]), ("悬丝诊脉", [69]),
    # 72-73 盘丝洞
    ("盘丝洞", [72, 73]), ("蜘蛛精", [72, 73]), ("濯垢泉", [72]), ("多目怪", [73]),
    ("蜈蚣精", [73]), ("毗蓝婆", [73]),
    # 74-77 狮驼岭
    ("狮驼岭", [74, 75, 76, 77]), ("大大王", [74, 75, 76, 77]), ("二大王", [74, 75, 76, 77]),
    ("三大王", [74, 75, 76, 77]), ("白象", [74, 75, 76, 77]), ("大鹏", [74, 75, 76, 77]),
    ("阴阳二气瓶", [75]), ("狮驼国", [77]),
    # 78-79 比丘国
    ("比丘国", [78, 79]), ("国丈", [78, 79]), ("小儿心肝", [78]), ("白鹿", [78, 79]), ("寿星", [79]),
    # 80-83 老鼠精
    ("镇海寺", [80, 81]), ("老鼠精", [80, 81, 82, 83]), ("地涌夫人", [80, 81, 82, 83]),
    ("无底洞", [81, 82, 83]), ("托塔李天王", [83]),
    # 84 灭法国
    ("灭法国", [84]), ("钦法国", [84]), ("杀和尚", [84]),
    # 85-86 隐雾山
    ("隐雾山", [85, 86]), ("折岳连环洞", [85, 86]), ("豹子精", [85, 86]), ("艾叶花皮豹", [86]),
    # 87 凤仙郡
    ("凤仙郡", [87]), ("米山", [87]), ("面山", [87]), ("金锁", [87]), ("劝善施霖", [87]),
    # 88-90 玉华州
    ("玉华州", [88, 89, 90]), ("黄狮精", [88, 89, 90]), ("钉耙会", [89]),
    ("九头狮", [90]), ("九灵元圣", [90]), ("太乙救苦天尊", [90]),
    # 91-92 金平府
    ("金平府", [91, 92]), ("青龙山", [91, 92]), ("犀牛精", [91, 92]), ("四木禽星", [92]),
    # 93-95 天竺国
    ("天竺国", [93, 94, 95]), ("假公主", [93, 95]), ("真公主", [94]), ("玉兔精", [95]),
    ("太阴星君", [95]), ("布金禅寺", [94]),
    # 96-97 寇员外
    ("寇员外", [96, 97]), ("铜台府", [96, 97]), ("斋僧", [96]),
    # 98 凌云渡
    ("凌云渡", [98]), ("接引佛祖", [98]), ("无底船", [98]),
    # 99-100
    ("老龟", [99]), ("晒经石", [100]), ("无字经", [100]),
]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_declared(body):
    """解析声明回次，支持 第X回 / 第X-Y回。返回 int 列表；无法解析返回 None。"""
    m = re.search(r"推测对应原著回号:\s*第(\d+)(?:-(\d+))?回", body)
    if not m:
        return None
    a = int(m.group(1))
    b = int(m.group(2)) if m.group(2) else a
    return list(range(a, b + 1))


def extract_body(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"^#\s.*$", "", text, count=1, flags=re.MULTILINE)
    return text


def main():
    sd_files = sorted(glob.glob(os.path.join(SHENDU, "SD*.md")))
    results = []
    for p in sd_files:
        base = os.path.basename(p)
        m = re.match(r"SD(\d+)\.md", base)
        if not m:
            continue
        num = int(m.group(1))
        txt = read(p)
        declared = parse_declared(txt)
        body = extract_body(txt)
        # 统计命中
        tally = Counter()
        hits = {}  # chapter -> list of terms
        for term, chs in TERMS:
            if term in body:
                for c in chs:
                    tally[c] += 1
                    hits.setdefault(c, []).append(term)
        declared_set = set(declared) if declared else set()
        declared_total = sum(tally[c] for c in declared_set)
        others = [(c, tally[c]) for c in tally if c not in declared_set]
        others.sort(key=lambda x: -x[1])
        best_other = others[0] if others else (None, 0)
        # 判定
        issues = []
        sev = None
        if declared is None:
            issues.append("无声明回号(解析失败)")
            sev = "check"
        else:
            if declared_total == 0 and best_other[1] >= 3:
                issues.append(f"本回锚点=0，完全由其他回主导(最佳第{best_other[0]}回×{best_other[1]})")
                sev = "strong"
            elif best_other[1] > declared_total and best_other[1] >= 3 and declared_total < best_other[1] * 0.5:
                issues.append(f"其他回主导: 第{best_other[0]}回×{best_other[1]} > 本回×{declared_total}")
                sev = "likely"
            elif best_other[1] >= 3 and declared_total == best_other[1]:
                issues.append(f"本回×{declared_total} 与其他回第{best_other[0]}回×{best_other[1]}持平(需人工看)")
                sev = "check"
        top5 = tally.most_common(5)
        results.append({
            "sd": num, "declared": declared, "declared_total": declared_total,
            "best_other": best_other, "issues": issues, "sev": sev,
            "top5": top5, "hits_other": hits.get(best_other[0], []) if best_other[0] else [],
        })

    flagged = [r for r in results if r["sev"] in ("strong", "likely", "check") and r["issues"]]
    strong = [r for r in results if r["sev"] == "strong"]
    likely = [r for r in results if r["sev"] == "likely"]
    check = [r for r in results if r["sev"] == "check"]

    lines = []
    lines.append("# SD 切片错位扫描报告 v2（专有名词锚点法）\n")
    lines.append(f"- 扫描切片：{len(results)}")
    lines.append(f"- **strong（完全错位）**：{len(strong)}")
    lines.append(f"- **likely（高度疑似）**：{len(likely)}")
    lines.append(f"- **check（需人工看）**：{len(check)}\n")

    def dump(title, items):
        lines.append(f"## {title}\n")
        for r in sorted(items, key=lambda x: -x["best_other"][1]):
            lines.append(f"### SD{r['sd']:03d} 声明{r['declared']}")
            lines.append(f"- {r['issues']}")
            lines.append(f"- 本回锚点={r['declared_total']}；最佳异回=第{r['best_other'][0]}回×{r['best_other'][1]}"
                         + (f"（命中：{r['hits_other'][:6]}）" if r['hits_other'] else ""))
            lines.append(f"- top5：{' | '.join(f'第{c}回×{n}' for c, n in r['top5'])}")
            lines.append("")

    dump("STRONG —— 完全错位（本回锚点=0，由其他回主导）", strong)
    dump("LIKELY —— 高度疑似（其他回锚点远多于本回）", likely)
    dump("CHECK —— 需人工复核", check)
    lines.append("## 全部切片 top5 锚点（审计留痕）\n")
    for r in results:
        lines.append(f"- SD{r['sd']:03d} 声明{r['declared']} 本回={r['declared_total']} | "
                     + " ".join(f"第{c}={n}" for c, n in r["top5"]))

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with _w536_guard_open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"切片:{len(results)} | strong:{len(strong)} | likely:{len(likely)} | check:{len(check)}")
    print("=== STRONG ===")
    for r in sorted(strong, key=lambda x: -x["best_other"][1]):
        print(f"SD{r['sd']:03d} 声明{r['declared']} 本回={r['declared_total']} 异回第{r['best_other'][0]}×{r['best_other'][1]} | {r['hits_other'][:6]}")
    print("=== LIKELY ===")
    for r in sorted(likely, key=lambda x: -x["best_other"][1]):
        print(f"SD{r['sd']:03d} 声明{r['declared']} 本回={r['declared_total']} 异回第{r['best_other'][0]}×{r['best_other'][1]} | top5={' '.join(f'第{c}={n}' for c,n in r['top5'])}")
    print(f"\n报告: {REPORT}")


if __name__ == "__main__":
    main()
