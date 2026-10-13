import re
with open('site/data/hardship-heatmap.html', 'r', encoding='utf-8') as f:
    content = f.read()
scores = [int(s) for s in re.findall(r'score:(\d+)', content)]
print(f'总数: {len(scores)}')
print(f'平均难度: {sum(scores)/len(scores):.2f}')
print(f'最高: {max(scores)}, 最低: {min(scores)}')
print(f'极难数(9-10): {sum(1 for s in scores if s>=9)}')
print(f'极难回目列表: 见 HTML')
stages = re.findall(r'stage:"(\w+)"', content)
from collections import Counter
print(f'阶段分布: {dict(Counter(stages))}')
for s in ['pre','early','mid','late','end']:
    idx = [i for i,st in enumerate(stages) if st==s]
    if idx:
        print(f'{s} 阶段: {len(idx)} 难, 均分 {sum(scores[i] for i in idx)/len(idx):.2f}')
