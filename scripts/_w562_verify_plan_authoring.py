# _w562_verify_plan_authoring.py — 校验 ZCode 用户级 plan-authoring 技能
import os
import re

base = os.path.join(os.path.expanduser('~'), '.zcode', 'skills', 'xiyouji-plan-authoring')
s = open(os.path.join(base, 'SKILL.md'), encoding='utf-8').read()
r = open(os.path.join(base, 'reference.md'), encoding='utf-8').read()

ok = True
def chk(name, cond):
    global ok
    print(('OK  ' if cond else 'FAIL'), name)
    if not cond:
        ok = False

fm = s.split('---')[1]
chk('frontmatter name 正确', 'name: xiyouji-plan-authoring' in fm)
chk('frontmatter version 1.3.0', 'version: 1.3.0' in fm)
chk('SKILL.md 无旧项目路径', 'D:\\1\\' not in s and '/d/1/' not in s)
chk('reference.md 无旧项目路径', 'D:\\1\\' not in r and '/d/1/' not in r)
chk('新项目路径在位', 'D:\\xiyouji' in s and '/d/xiyouji' in s)
chk('六步流程完整', all(k in s for k in ['第 1 步：读上游', '第 4 步：成文', '第 6 步：汇报']))
chk('去模糊化五标准在', '去模糊化成文标准' in s and '无测量命令的条款不得写入' in s)
chk('reference.md 四节齐全', all(k in r for k in ['方案文档骨架', '基线表示例', '取证命令速查', '汇报模板']))
chk('引用式表述示范在', '以 verify_delivery 输出为准' in s)
chk('W562 迁移注记在', 'W562 后从 qwenworkcn 优化迁移' in s)
print('总体:', 'PASS' if ok else 'FAIL')
