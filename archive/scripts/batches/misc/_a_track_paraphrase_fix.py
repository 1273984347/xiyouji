# 一次性脚本：A 轨驿递稿转述句对抗性终扫处置（09-28 联网核验后·两稿同步·不入库门禁）
# 核验结论：魏丕信三联框架查无实据(软化)·花月痕核不到(删)·会通馆查无出处(改写)·
#           布罗代尔"准结构/所谓引文"去引号化(与§6延伸发现同族)·参考文献版本统一2006增订本
import re

F1 = '明清小说方向-投稿版.md'
F2 = '明清小说方向-匿名稿.md'

PAIRS = [
    # (旧, 新)
    ('则以"塘报—奏折—邸报"的多级信息通道', '则以塘报、奏折为主的文书奏报体系'),
    ('魏丕信的"塘报—奏折—邸报"给出"信息语法"', '魏丕信的文书奏报体系给出"信息语法"'),
    ('报官递解与"塘报—奏折—邸报"', '报官递解与文书奏报体系'),
    ('魏丕信所论"塘报—奏折—邸报"多级信息通道', '魏丕信所论的文书奏报体系'),
    ('缩小版的"塘报—奏折"循环', '缩小版的逐级奏报循环'),
    ('是地理与历史之间的"准结构"', '是地理与历史之间近乎结构性的存在'),
    ('恰对应布罗代尔所谓"交通网络的兴衰系于政治秩序的强弱"', '恰对应布罗代尔所揭示的交通网络与政治秩序的依存关系'),
    ('以会通馆文献与地方志互证', '以官修地志与商书的点校整理互证'),
    ('其后该作者又将这一视角延伸至《花月痕》——「交通线路与明清小说书写」已成为', '「交通线路与明清小说书写」已成为'),
    ('[2] 杨正泰. 明代驿站考[M]. 上海: 上海古籍出版社, 1994.',
     '[2] 杨正泰. 明代驿站考：附寰宇通衢、一统路程图记、士商类要：增订本[M]. 上海: 上海古籍出版社, 2006.'),
]

for fname in (F1, F2):
    text = open(fname, encoding='utf-8').read()
    report = []
    for old, new in PAIRS:
        n = text.count(old)
        if n == 1:
            text = text.replace(old, new)
            report.append('OK')
        elif n == 0:
            report.append('skip(0)')
        else:
            raise SystemExit(f'FATAL {fname}: 计数 {n} != 0/1: {old[:30]}')
    with open(fname, 'w', encoding='utf-8', newline='') as f:
        f.write(text)
    plain = re.sub(r'\s', '', re.sub(r'^>.*$|^#.*$|^---$|\|', '', text, flags=re.M))
    body = re.sub(r'\s', '', re.sub(r'(?m)^> .*$', '', re.sub(r'(?m)^#{1,6} .*$', '', text)))
    residual = [p for p, _ in PAIRS if p[:12] in text and '驿站考[M]' not in p]
    print(f'{fname}: 替换 {report.count("OK")}/10 · 跳过 {report.count("skip(0)")} · '
          f'正文字符(去空白含标题注)≈{len(body)} · 残留 {len(residual)}')
    for p in PAIRS:
        if p[0][:12] in text:
            print('   残留:', p[0][:40])
