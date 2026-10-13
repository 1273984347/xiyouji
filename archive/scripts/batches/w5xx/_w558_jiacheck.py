# _w558_jiacheck.py — batch_cascade 落盘核查（W558 口径；条目按 v/W 编号正则计数）
import re

def rd(f):
    return open(f, 'rb').read().decode('utf-8')

ok = True
def chk(name, cond, detail=''):
    global ok
    print(('OK  ' if cond else 'FAIL'), name, detail)
    if not cond: ok = False

for f in ['README.md', 'STRUCTURE.md', '交接文档.md', 'CHANGELOG.md', 'docs/00-导读/项目说明.md', 'scripts/output/file-index.md', 'AGENTS.md']:
    chk(f + ' 无 CRCR', '\r\r' not in rd(f))

cl = rd('CHANGELOG.md')
chk('CHANGELOG W558 段存在', '### v2.3.158（2026-09-07）：W558' in cl)
chk('CHANGELOG 编号上限 W558', 'W001-W558' in cl)
chk('CHANGELOG W557 段仍在', '### v2.3.157' in cl)
chk('CHANGELOG 版段倒序', 0 <= cl.find('v2.3.158') < cl.find('v2.3.157'))

j = rd('交接文档.md')
head_entries = re.findall(r'v2\.3\.1\d\d (W\d+)', j.split('\r\n')[6])
chk('交接头链条目 = W558/W557/W556', head_entries == ['W558', 'W557', 'W556'], str(head_entries))
tail = j[j.rfind('最后更新：'):]
tail_entries = re.findall(r'v2\.3\.1\d\d (W\d+)', tail)
chk('交接尾链 3 条且含 W558', tail.count('2026-') == 3 and tail_entries[:1] == ['W558'], str(tail_entries[:3]))
chk('交接里程碑块 W558', '- **v2.3.158 W558' in j)
chk('交接 HEAD 句 W558', '当前 HEAD = v2.3.158 W558' in j)
chk('交接九、使用说明段在', '## 九、使用说明' in j)

for f in ['README.md', 'STRUCTURE.md', 'docs/00-导读/项目说明.md']:
    chk(f + ' 版本行 v2.3.158', 'v2.3.158' in rd(f))

ag = rd('AGENTS.md')
chk('AGENTS 脚注 W558', '2026-09-07（v2.3.158 W558）' in ag)
chk('AGENTS 缺分号条目在', 'CSS 缺分号 = 整条声明静默丢弃' in ag)
chk('AGENTS 尾锚唯一', ag.count('。如与上述权威文档冲突，以权威文档为准。*') == 1)

wf = rd('.github/workflows/README.md')
chk('workflows 头部 W558', 'v2.3.158 W558' in wf and 'W450-W558' in wf)

fi = rd('scripts/output/file-index.md')
chk('file-index W558 段', '## W558 ' in fi)
chk('file-index 段倒序', fi.find('## W558 ') < fi.find('## W557 '))

for f in ['site/index.html', 'site/data/cross-time-danmaku.html', 'site/data/tag-cloud.html', 'site/dukou-engine.html']:
    chk(f + ' 页脚 W558', 'W558' in rd(f))

print('\n总体:', 'PASS' if ok else 'FAIL')
