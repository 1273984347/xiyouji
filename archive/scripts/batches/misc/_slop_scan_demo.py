# 一次性脚本：slop-scan TIER-1/TIER-2 规则表执行器（演示用·不入库门禁）
import re
import sys

TIER1 = [
    ('清嗓子开头', r'在当今(社会|时代)|随着[^，。]{2,12}的发展|在[^，。]{2,10}的大背景下'),
    ('模板总结', r'综上所述|总而言之|由此可见'),
    ('假停顿', r'值得注意的是|需要指出的是'),
    ('三连排比', r'不仅[^。]{1,20}更是[^。]{1,20}还是'),
    ('升华结尾', r'让我们一起|希望对你有所帮助|愿我们都能'),
    ('管理黑话', r'赋能|抓手|深耕|擘画|注入新动能|保驾护航|开启[^。]{0,8}新篇章|绘就[^。]{0,6}画卷'),
    ('伪直引假深刻', r'不是[^。，]{2,14}，?而是[^。，]{2,20}[。；]'),
]
TIER2 = [
    ('模糊归因', r'有(专家|学者)指出|研究表明(?![^。]{0,30}\[\d)|业内人士认为'),
    ('解释性废话', r'换句话说|简单来说|这意味着|从某种意义上讲'),
    ('报幕词', r'首先[^。]{1,30}其次|其次[^。]{1,40}最后'),
    ('弱化词堆叠', r'(可能|或许|在一定程度上|相对){1}[^。]*?(可能|或许|在一定程度上|相对)'),
]

def scan(path, label):
    t = open(path, encoding='utf-8').read()
    paras = [p for p in re.split(r'\n+', t) if p.strip()]
    print(f'\n## {label}（{len(t)} 字符）')
    t1_hits, t2_hits = [], []
    for name, pat in TIER1:
        for m in re.finditer(pat, t):
            s = max(0, m.start() - 20)
            t1_hits.append((name, t[s:m.end() + 25].replace('\n', ' ')))
    for name, pat in TIER2:
        for m in re.finditer(pat, t):
            s = max(0, m.start() - 15)
            t2_hits.append((name, t[s:m.end() + 20].replace('\n', ' ')))
    print(f'TIER-1 命中 {len(t1_hits)} 处')
    for name, ctx in t1_hits[:8]:
        print(f'  [{name}] …{ctx}…')
    print(f'TIER-2 命中 {len(t2_hits)} 处')
    for name, ctx in t2_hits[:5]:
        print(f'  [{name}] …{ctx}…')
    # 句长均匀度（TIER-2 节奏项·正文段抽样）
    body = re.sub(r'[>#|\-*\[\]()]', '', t)
    sents = [s for s in re.split(r'[。；！？]', body) if 8 < len(s) < 120]
    lens = [len(s) for s in sents]
    if len(lens) > 10:
        import statistics
        print(f'节奏抽样: {len(lens)} 句·均长 {statistics.mean(lens):.0f}·标准差 {statistics.stdev(lens):.0f}'
              f'·短句(<15字)占比 {sum(1 for x in lens if x < 15) / len(lens):.0%}')

scan(sys.argv[1], sys.argv[2])
