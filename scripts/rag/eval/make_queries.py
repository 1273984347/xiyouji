#!/usr/bin/env python3
"""make_queries.py — RAG 检索评测题集生成器（W844 · Q4「评测集入仓」）。

背景（为什么要这个脚本）：
    30 题冻结集与全部评测脚本原先只存在于本地工地（`tmpe/_inbox/hf-poc/`），
    既不可复算也不可审计——题集是「手工件」，一旦失传，recall 数字就再也没法复现。
    本脚本把题集的**生成规则**固化下来：人工题（30 条冻结集）原样保留，
    机械题（70 条）由「文档标题锚点」派生，gold 由脚本解析，可随时重生成。

两类题的定位差异（写死以免混淆）：
    - `origin=frozen`：人工撰写，接近真实提问（口语、间接、概念性），是**主指标**；
    - `origin=anchor`：标题派生，问句由模板生成、gold 是标题含该锚点的文档集合。
      这类题偏易（BM25 命中标题即中），**只能用来看「标题面覆盖」，不可与人工题合并解读**。

用法：
    python scripts/rag/eval/make_queries.py --write          # 重生 queries_100q.jsonl
    python scripts/rag/eval/make_queries.py --check          # 只校验现有文件与规则一致
    python scripts/rag/eval/make_queries.py --list-missing   # 列出解析不到 gold 的锚点
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAG_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(RAG_DIR))

FROZEN_FILE = os.path.join(HERE, "queries_30q_frozen.jsonl")
OUT_FILE = os.path.join(HERE, "queries_100q.jsonl")

# 机械题：70 条（qid 从 Q31 起，避免与冻结集 Q01-Q30 撞号）。
# 每条 = (qid 后缀号, type, 问句, 标题锚点)。锚点须是**文档基名**的子串；
# 生成时只保留「已在 BM25 索引内」的文档，故 gold 一定可被检索到（不会因未索引入题而假降）。
ANCHOR_CASES = [
    # ---- person（人物关系 / 人物专题）22 条 ----
    ("person", "白骨精这个角色到底想表达什么", "白骨精"),
    ("person", "铁扇公主和牛魔王的关系怎么看", "铁扇公主"),
    ("person", "牛魔王为什么不肯借扇", "牛魔王"),
    ("person", "红孩儿和牛魔王是什么关系", "红孩儿"),
    ("person", "二郎神和孙悟空谁更自由", "二郎神"),
    ("person", "哪吒的出身和剔骨还父怎么理解", "哪吒"),
    ("person", "六耳猕猴是不是孙悟空的另一面", "六耳猕猴"),
    ("person", "黄袍怪下界为妖的缘由", "黄袍怪"),
    ("person", "奎木狼为什么不负前情", "奎木狼"),
    ("person", "太上老君在取经里扮演什么角色", "太上老君"),
    ("person", "太白金星为什么总来招安", "太白金星"),
    ("person", "观音菩萨的安排有什么用意", "观音"),
    ("person", "唐僧的软弱是不是一种坚持", "唐僧"),
    ("person", "猪八戒的贪欲有什么功能", "猪八戒"),
    ("person", "沙僧为什么几乎没有台词", "沙僧"),
    ("person", "女儿国国王的抉择", "女儿国国王"),
    ("person", "乌鸡国国王的遭遇说明了什么", "乌鸡国国王"),
    ("person", "大鹏金翅雕的背景有多硬", "大鹏金翅雕"),
    ("person", "九头虫的战力设定", "九头虫"),
    ("person", "万圣公主偷灵芝的动机", "万圣公主"),
    ("person", "土地公在各地怎么出场", "土地公"),
    ("person", "取经五众之间的关系网络", "取经五众"),
    # ---- theme（主题归类 / 学科视角）24 条 ----
    ("theme", "八十一难的整体结构怎么划分", "八十一难结构"),
    ("theme", "八十一难的风险管理视角", "八十一难风险管理"),
    ("theme", "取经团队的动力学如何演变", "取经团队动力学"),
    ("theme", "取经地理学讲了什么", "取经地理学"),
    ("theme", "取经伦理学的核心争点", "取经伦理学"),
    ("theme", "取经团队心理学怎么分析", "取经团队心理学"),
    ("theme", "时间叙事在原著里怎么用", "时间叙事"),
    ("theme", "空间叙事与取经路线的关系", "空间叙事"),
    ("theme", "身体政治学怎么看妖魔变形", "身体政治"),
    ("theme", "权力在西游世界如何分布", "权力"),
    ("theme", "西游与死亡研究专题讲了什么", "西游与死亡"),
    ("theme", "声音政治学怎么切入取经", "声音政治"),
    ("theme", "不可靠叙述在原著中的表现", "不可靠叙述"),
    ("theme", "元叙事学怎么解读西游记", "元叙事"),
    ("theme", "互文性叙事学的分析路径", "互文性"),
    ("theme", "创伤叙事学能解释谁", "创伤叙事"),
    ("theme", "动物研究视角下的妖怪", "动物研究"),
    ("theme", "历史叙事学与玄奘取经", "历史叙事"),
    ("theme", "取经生态学的关切点", "取经生态"),
    ("theme", "取经气候学的切入点", "取经气候"),
    ("theme", "取经拓扑学的空间模型", "取经拓扑"),
    ("theme", "取经密码学在讲什么", "取经密码"),
    ("theme", "媒介考古学怎么看取经传播", "媒介考古"),
    ("theme", "取经数字人文专题的方法", "取经数字人文"),
    # ---- hardship（八十一难 / 情节母题）12 条 ----
    ("hardship", "五次蜕变分别指什么", "五次蜕变"),
    ("hardship", "大闹天宫是英雄还是悲剧", "大闹天宫"),
    ("hardship", "真假美猴王到底死了谁", "真假美猴王"),
    ("hardship", "火焰山这一难的结构作用", "火焰山"),
    ("hardship", "人参果与欲望的关系", "人参果"),
    ("hardship", "紧箍儿为什么是内侧的", "紧箍儿"),
    ("hardship", "三借芭蕉扇的叙事节奏", "芭蕉扇"),
    ("hardship", "盘丝洞的性别隐喻", "盘丝洞"),
    ("hardship", "车迟国斗法的政治含义", "车迟国"),
    ("hardship", "狮驼岭为什么最恐怖", "狮驼岭"),
    ("hardship", "八十一难专题的总论", "八十一难专题"),
    ("hardship", "取经路上地府体系的呈现", "地府体系"),
    # ---- chapter（回目引用 / 单回细读）12 条 ----
    ("chapter", "第五十九回唐三藏路阻火焰山讲了什么", "第059回"),
    ("chapter", "第二十七回尸魔三戏唐三藏怎么读", "第027回"),
    ("chapter", "第一回灵根育孕源流出", "第001回"),
    ("chapter", "第一百回径回东土五圣成真", "第100回"),
    ("chapter", "第七回八卦炉中逃大圣", "第007回"),
    ("chapter", "第十四回心猿归正六贼无踪", "第014回"),
    ("chapter", "第四十二回大圣殷勤拜南海", "第042回"),
    ("chapter", "第七十二回盘丝洞七情迷本", "第072回"),
    ("chapter", "第九十八回猿熟马驯方脱壳", "第098回"),
    ("chapter", "第十六回观音院僧谋宝贝", "第016回"),
    ("chapter", "第三十三回外道迷真性元神助本心", "第033回"),
    ("chapter", "第八十一回镇海寺心猿知怪", "第081回"),
]


def load_frozen():
    """读冻结集（**逐行原样**保留，不改写字段与分隔符）。"""
    out = []
    with open(FROZEN_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def indexed_docs():
    """BM25 索引内的文档路径集合（posix 形态）。

    只认索引内文档作 gold，是为了让 recall 的分母与检索面一致——
    未入索引的文档无论检索器多好都不可能命中，把它算进 gold 等于凭空压低分数。
    """
    if RAG_DIR not in sys.path:
        sys.path.insert(0, RAG_DIR)
    import xiyouji_rag  # noqa: E402  仅在需要索引时导入（--check 也要）

    index = xiyouji_rag.build_index()
    return [d["path"].replace("\\", "/") for d in index["docs"]]


def build_cases(docs):
    """按锚点解析 gold；返回 (cases, missing)。"""
    cases, missing = [], []
    for i, (typ, query, anchor) in enumerate(ANCHOR_CASES):
        gold = sorted(p for p in docs if anchor in os.path.basename(p)[:-3])
        if not gold:
            missing.append((typ, query, anchor))
            continue
        cases.append(
            {
                "qid": "Q%02d" % (31 + i),
                "query": query,
                "type": typ,
                "gold": gold,
                "origin": "anchor",
                "anchor": anchor,
            }
        )
    return cases, missing


def render(frozen, generated):
    """拼装 100 题文本：冻结集在前（逐行原样），机械题在后。"""
    lines = []
    with open(FROZEN_FILE, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                lines.append(line.rstrip("\r\n"))
    for c in generated:
        lines.append(json.dumps(c, ensure_ascii=False))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="RAG 检索评测题集生成（W844）")
    ap.add_argument("--write", action="store_true", help="重生 queries_100q.jsonl")
    ap.add_argument("--check", action="store_true", help="只校验现有文件与生成规则一致")
    ap.add_argument("--list-missing", action="store_true", help="列出解析不到 gold 的锚点")
    args = ap.parse_args()
    if not (args.write or args.check or args.list_missing):
        ap.error("需指定 --write / --check / --list-missing 之一")

    frozen = load_frozen()
    if len(frozen) != 30:
        print("[FAIL] 冻结集应为 30 条，实际 %d 条" % len(frozen))
        return 1
    if len(ANCHOR_CASES) != 70:
        print("[FAIL] 机械题应为 70 条，实际 %d 条（改锚点表后请同步总数断言）" % len(ANCHOR_CASES))
        return 1

    docs = indexed_docs()
    generated, missing = build_cases(docs)

    if args.list_missing:
        if not missing:
            print("[OK] 全部 70 个锚点均解析到 gold")
            return 0
        print("[MISS] %d 个锚点解析不到 gold：" % len(missing))
        for typ, q, a in missing:
            print("  %-9s %-24s 锚点=%s" % (typ, q[:24], a))
        return 1

    if missing:
        print("[FAIL] %d 个锚点解析不到 gold（索引内无标题含该锚点的文档）——先修正锚点表" % len(missing))
        for typ, _q, a in missing:
            print("  %-9s 锚点=%s" % (typ, a))
        return 1

    text = render(frozen, generated)

    if args.check:
        if not os.path.exists(OUT_FILE):
            print("[FAIL] 缺少 %s（先跑 --write）" % os.path.relpath(OUT_FILE, ROOT))
            return 1
        cur = open(OUT_FILE, encoding="utf-8", newline="").read()
        if cur.replace("\r\n", "\n") != text:
            print("[FAIL] queries_100q.jsonl 与生成规则不一致（跑 --write 重生）")
            return 1
        print("[OK] 100 题与生成规则一致（30 冻结 + 70 机械）")
        return 0

    with open(OUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("[WRITE] %s：%d 条（冻结 %d + 机械 %d）"
          % (os.path.relpath(OUT_FILE, ROOT), len(frozen) + len(generated), len(frozen), len(generated)))
    by_type = {}
    for c in generated:
        by_type[c["type"]] = by_type.get(c["type"], 0) + 1
    print("        机械题类型分布：" + " · ".join("%s=%d" % kv for kv in sorted(by_type.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
