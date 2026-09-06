# _w553_jiacheck.py v2 — W553 级联产物全面核验
import re

def rd(f):
    return open(f, 'rb').read().decode('utf-8')

ok = True
def chk(name, cond, detail=''):
    global ok
    print(('OK  ' if cond else 'FAIL'), name, detail)
    if not cond: ok = False

# 1) CHANGELOG：W553 段 + 编号上限 + 上一段完整
cl = rd('CHANGELOG.md')
chk('CHANGELOG W553 段存在', '### v2.3.153（2026-09-06）：W553' in cl)
chk('CHANGELOG 编号规则上限 W553', bool(re.search(r'W001-W553', cl)))
chk('CHANGELOG W552 段仍存在', '### v2.3.152' in cl)
chk('CHANGELOG 版段倒序（553 在 552 前）', cl.find('v2.3.153') < cl.find('v2.3.152') and cl.find('v2.3.152') > 0)
chk('CHANGELOG 无 CRCR', '\r\r' not in cl)

# 2) 交接文档
j = rd('交接文档.md')
head_line = j.split('\r\n')[6]
chk('交接头链 W553×1', head_line.count('W553') == 1)
tail = j[j.rfind('最后更新：'):]
chk('交接尾链 W553×1', tail.count('W553') == 1 and tail.count('2026-') == 3)
chk('交接里程碑块 W553', '- **v2.3.153 W553' in j)
chk('交接 HEAD 句', '当前 HEAD = v2.3.153 W553' in j)
chk('交接无 CRCR', '\r\r' not in j)
chk('交接九、使用说明段在', '## 九、使用说明' in j)

# 3) README / STRUCTURE / 项目说明
for f in ['README.md', 'STRUCTURE.md', 'docs/00-导读/项目说明.md']:
    s = rd(f)
    chk(f + ' 版本行 v2.3.153', 'v2.3.153' in s)
    chk(f + ' 无 CRCR', '\r\r' not in s)

# 4) AGENTS 脚注
ag = rd('AGENTS.md')
chk('AGENTS 脚注 W553', '2026-09-06（v2.3.153 W553）' in ag)
chk('AGENTS 尾锚唯一', ag.count('。如与上述权威文档冲突，以权威文档为准。*') == 1)

# 5) workflows README
wf = rd('.github/workflows/README.md')
chk('workflows 头部 W553', 'v2.3.153 W553' in wf and 'W450-W553' in wf)

# 6) file-index
fi = rd('scripts/output/file-index.md')
chk('file-index W553 段', '## W553 ' in fi)
chk('file-index 段倒序', fi.find('## W553 ') < fi.find('## W552 '))

# 7) 四页脚
for f in ['site/index.html', 'site/data/cross-time-danmaku.html', 'site/data/tag-cloud.html', 'site/dukou-engine.html']:
    s = rd(f)
    chk(f + ' 页脚 W553', 'W553' in s)

print('\n总体:', 'PASS' if ok else 'FAIL')
