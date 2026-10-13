# _w553_jiacheck.py — batch_cascade 落盘字节级核查（W555 口径）
import re

def rd(f):
    return open(f, 'rb').read().decode('utf-8')

ok = True
def chk(name, cond, detail=''):
    global ok
    print(('OK  ' if cond else 'FAIL'), name, detail)
    if not cond: ok = False

# 0) 行尾翻倍检查（全部级联文件）
for f in ['README.md', 'STRUCTURE.md', '交接文档.md', 'CHANGELOG.md', 'docs/00-导读/项目说明.md', 'scripts/output/file-index.md', 'AGENTS.md']:
    s = rd(f)
    chk(f + ' 无 CRCR', '\r\r' not in s)

# 1) CHANGELOG
cl = rd('CHANGELOG.md')
chk('CHANGELOG W555 段存在', '### v2.3.155（2026-09-06）：W555' in cl)
chk('CHANGELOG 编号上限 W555', 'W001-W555' in cl)
chk('CHANGELOG W553 段仍在', '### v2.3.153' in cl)
chk('CHANGELOG 版段倒序', cl.find('v2.3.155') < cl.find('v2.3.153'))

# 2) 交接文档
j = rd('交接文档.md')
head_line = j.split('\r\n')[6]
chk('交接头链 W555×1', head_line.count('W555') == 1, f"实际 {head_line.count('W555')}")
tail = j[j.rfind('最后更新：'):]
chk('交接尾链 W555×1', tail.count('W555') == 1 and tail.count('2026-') == 3)
chk('交接里程碑块 W555', '- **v2.3.155 W555' in j)
chk('交接 HEAD 句 W555', '当前 HEAD = v2.3.155 W555' in j)
chk('交接九、使用说明段在', '## 九、使用说明' in j)

# 3) 版本行
for f in ['README.md', 'STRUCTURE.md', 'docs/00-导读/项目说明.md']:
    chk(f + ' 版本行 v2.3.155', 'v2.3.155' in rd(f))

# 4) AGENTS 脚注
ag = rd('AGENTS.md')
chk('AGENTS 脚注 W555', '2026-09-06（v2.3.155 W555）' in ag)
chk('AGENTS 尾锚唯一', ag.count('。如与上述权威文档冲突，以权威文档为准。*') == 1)

# 5) workflows README
wf = rd('.github/workflows/README.md')
chk('workflows 头部 W555', 'v2.3.155 W555' in wf and 'W450-W555' in wf)

# 6) file-index
fi = rd('scripts/output/file-index.md')
chk('file-index W555 段', '## W555 ' in fi)
chk('file-index 段倒序', fi.find('## W555 ') < fi.find('## W553 '))

# 7) 四页脚
for f in ['site/index.html', 'site/data/cross-time-danmaku.html', 'site/data/tag-cloud.html', 'site/dukou-engine.html']:
    chk(f + ' 页脚 W555', 'W555' in rd(f))

print('\n总体:', 'PASS' if ok else 'FAIL')
