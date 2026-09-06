# _w557_jiacheck.py — batch_cascade 落盘字节级核查（W557 口径）
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
chk('CHANGELOG W557 段存在', '### v2.3.157（2026-09-06）：W557' in cl)
chk('CHANGELOG 编号上限 W557', 'W001-W557' in cl)
chk('CHANGELOG W556 段仍在', '### v2.3.156' in cl)
chk('CHANGELOG 版段倒序', cl.find('v2.3.157') < cl.find('v2.3.156'))

j = rd('交接文档.md')
head_line = j.split('\r\n')[6]
chk('交接头链 W557×1', head_line.count('W557') == 1, f"实际 {head_line.count('W557')}")
tail = j[j.rfind('最后更新：'):]
chk('交接尾链 W557×1 且 3 条', tail.count('W557') == 1 and tail.count('2026-') == 3, f"实际 {tail.count('W557')}/{tail.count('2026-')}")
chk('交接里程碑块 W557', '- **v2.3.157 W557' in j)
chk('交接 HEAD 句 W557', '当前 HEAD = v2.3.157 W557' in j)
chk('交接 HEAD 句唯一', j.count('当前 HEAD = v2.3.1') == 1)
chk('交接九、使用说明段在', '## 九、使用说明' in j)
chk('交接零、当前阻塞段在', '当前阻塞' in j)

for f in ['README.md', 'STRUCTURE.md', 'docs/00-导读/项目说明.md']:
    chk(f + ' 版本行 v2.3.157', 'v2.3.157' in rd(f))

ag = rd('AGENTS.md')
chk('AGENTS 脚注 W557', '2026-09-06（v2.3.157 W557）' in ag)
chk('AGENTS 尾锚唯一', ag.count('。如与上述权威文档冲突，以权威文档为准。*') == 1)

wf = rd('.github/workflows/README.md')
chk('workflows 头部 W557', 'v2.3.157 W557' in wf and 'W450-W557' in wf)

fi = rd('scripts/output/file-index.md')
chk('file-index W557 段', '## W557 ' in fi)
chk('file-index 段倒序', fi.find('## W557 ') < fi.find('## W556 '))

for f in ['site/index.html', 'site/data/cross-time-danmaku.html', 'site/data/tag-cloud.html', 'site/dukou-engine.html']:
    chk(f + ' 页脚 W557', 'W557' in rd(f))

print('\n总体:', 'PASS' if ok else 'FAIL')
