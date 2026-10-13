# scripts/_audit_service_experience.py — 「体验与服务」方向基线审计（只读，不改任何文件）
# 用途：docs/superpowers/plans/2026-09-09-service-experience-and-agent-ops-plans.md 的基线取证
#       与执行批次验收对账。全部输出为 KEY=value 行，可直接粘贴进方案/CHANGELOG。
# 运行：python scripts/_audit_service_experience.py
import glob
import os
import re
import sqlite3
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
AW = os.path.join(ROOT, 'xiyouji-agent-web')


def rd(p):
    with open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


htmls = sorted(glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True))
SC = {p: rd(p) for p in htmls}  # 页面内容缓存，全脚本共用一次读盘
def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, '/')

# ---------- 站点侧 ----------

print(f'S01_site_html_total={len(htmls)}')

# S02/S03/S04：锚链接可达性（部署根 = site/）
oob, missing, legacy = [], [], []
href_re = re.compile(r'<a\b[^>]*?href=("([^"]*)"|\'([^\']*)\')', re.I)
skip = ('http://', 'https://', '//', 'mailto:', 'javascript:', 'data:', '#', 'tel:')
for p in htmls:
    for m in href_re.finditer(SC[p]):
        h = (m.group(2) if m.group(2) is not None else m.group(3) or '').strip()
        if not h or h.startswith(skip):
            continue
        hp = h.split('#')[0].split('?')[0]
        if not hp:
            continue
        tgt = os.path.normpath(os.path.join(os.path.dirname(p), hp))
        if not (tgt == SITE or tgt.startswith(SITE + os.sep)):
            oob.append((rel(p), h, rel(tgt)))
        elif not os.path.exists(tgt):
            missing.append((rel(p), h))
        else:
            head = os.path.relpath(tgt, SITE).replace(os.sep, '/').split('/')[0]
            if head in ('chapters', 'characters', 'themes'):
                legacy.append((rel(p), h))


def brief(rows, n=6):
    files = sorted(set(r[0] for r in rows))
    return f'n={len(rows)} files={len(files)} samples={rows[:n]}'


bk = Counter()
for _, _, t in oob:
    seg = t.split('/')
    bk['/'.join(seg[:2]) if len(seg) > 1 else seg[0]] += 1
print('S02_oob_anchors ' + brief(oob))
print('S02b_oob_breakdown ' + str(dict(bk.most_common(8))))
print('S03_missing_internal ' + brief(missing))
print('S04_legacy_dir_anchors ' + brief(legacy, 4))

# S05：自定义 404 页
p404 = glob.glob(os.path.join(SITE, '**', '404*.html'), recursive=True)
print(f'S05_custom_404={len(p404)} paths={[rel(x) for x in p404]}')

# S06：反馈渠道（穷举同义变体）
pats = ['giscus', 'utterances', 'disqus', 'mailto:', '/issues',
        'github.com/1273984347/xiyouji/issues', '意见反馈', '联系我们']
cnt = Counter()
for p in htmls:
    low = SC[p].lower()
    for k in pats:
        if k in low:
            cnt[k] += 1
print('S06_feedback_channels ' + str(dict(cnt)))

# S07：GoatCounter 覆盖
gc = [p for p in htmls if 'data-goatcounter' in SC[p]]
print(f'S07_goatcounter_pages={len(gc)}/{len(htmls)}')

# S08：RUM 上报目标与协议闸门
rum = glob.glob(os.path.join(SITE, '**', 'rum.js'), recursive=True)
if rum:
    r = rd(rum[0])
    m = re.search(r'fetch\(\s*[\'"`]([^\'"`]+)[\'"`]', r)
    gate = ('location.protocol' in r) or ('location.hostname' in r)
    print(f'S08_rum_post_target={m.group(1) if m else "NONE"} protocol_gate={gate} path={rel(rum[0])}')
else:
    print('S08_rum_post_target=NO_FILE')

# S09：Service Worker 缓存名与注册页
swp = os.path.join(SITE, 'sw.js')
if os.path.exists(swp):
    c = re.search(r'const CACHE\s*=\s*["\']([^"\']+)["\']', rd(swp))
    reg = [p for p in htmls if 'serviceWorker.register' in SC[p]]
    print(f'S09_sw_cache={c.group(1) if c else "?"} register_pages={len(reg)} pages={[rel(x) for x in reg]}')

# S10：viewport meta 缺失页
novp = [rel(p) for p in htmls if 'name="viewport"' not in SC[p]]
print(f'S10_viewport_missing={len(novp)} {novp[:5]}')

# S11：index.html 页脚版本串
idx_path = os.path.join(SITE, 'index.html')
idx = SC.get(idx_path, '')
vers = re.findall(r'v\d+\.\d+\.\d+', idx)
wtok = re.findall(r'W\d{3}', idx)
print(f'S11_index_footer_version_tokens={len(vers)} w_tokens={len(wtok)} '
      f'has_lastupdated={"最后更新" in idx} distinct_tail={sorted(set(vers))[-3:]}')

# S12：data/ 页页脚版本分布（构建期快照陈旧度）
foot = Counter()
stale_pages = 0
vers_tuple = []
for p in [x for x in htmls if os.sep + 'data' + os.sep in x and '_shell' not in x]:
    m = re.search(r'v(\d+)\.(\d+)\.(\d+) · (W\d+)', SC[p])
    if m:
        key = f'v{m.group(1)}.{m.group(2)}.{m.group(3)}·{m.group(4)}'
        foot[key] += 1
        vers_tuple.append((tuple(int(x) for x in m.groups()[:3]), p))
if vers_tuple:
    maxv = max(v for v, _ in vers_tuple)
    stale_pages = sum(1 for v, _ in vers_tuple if v != maxv)
print(f'S12_data_footer_versions={dict(foot.most_common(5))} stale_pages={stale_pages}')

# S13：search 页面向终端用户暴露的开发者指引
for tag, cand in (('zh', os.path.join(SITE, 'data', 'search.html')),
                  ('en', os.path.join(SITE, 'en', 'search.html'))):
    if os.path.exists(cand):
        s = SC[cand]
        print(f'S13_search_devcopy_{tag}=api_server:{s.count("api_server")} '
              f'offline_banner:{s.count("离线Mode") + s.count("离线模式")} '
              f'has_offline_render:{int("renderOffline" in s or "render-offline" in s)}')

# S14：首页→mobile-index 入口
mob_n = len(re.findall(r'href="[^"]*mobile-index', idx))
print(f'S14_index_to_mobile_links={mob_n}')

# S15：data/ 可视化页 tooltip 触屏适配现状
mo = mo_notouch = 0
data_pages = [x for x in htmls if os.sep + 'data' + os.sep in x and '_shell' not in x
              and '_template' not in x]
for p in data_pages:
    s = SC[p]
    if "'mouseover'" in s or '"mouseover"' in s:
        mo += 1
        if 'touchstart' not in s and 'touchend' not in s:
            mo_notouch += 1
print(f'S15_tooltip_data_pages={len(data_pages)} with_mouseover={mo} mouseover_no_touch={mo_notouch}')

# S16：dashboard 的 AI 入口
dash = SC.get(os.path.join(SITE, 'dashboard.html'), '')
print('S16_dashboard_ai_entry_n='
      + str(len(re.findall(r'href="[^"]*(?:dukou|rag|agent)[^"]*"', dash, re.I))))

# S17：首页 ASK 提交去向
m17 = re.search(r"location\.href\s*=\s*['\"]([^'\"]*)['\"]", idx)
print(f'S17_ask_redirect={m17.group(1) if m17 else "NONE"}')

# S18：部署态指向本机服务的页面（127.0.0.1 / localhost）
loose = []
for p in htmls:
    n = SC[p].count('127.0.0.1') + SC[p].count('localhost')
    if n:
        loose.append((rel(p), n))
print(f'S18_localhost_ref_pages={len(loose)} total_refs={sum(n for _, n in loose)} '
      f'top={sorted(loose, key=lambda x: -x[1])[:5]}')

# S19：curated 外链先例（D-1 改写风格参照）
cur = SC.get(os.path.join(SITE, 'curated.html'), '')
tb = cur.count('target="_blank"')
print(f'S19_curated_blob_links={cur.count("github.com/1273984347/xiyouji/blob/main/")} '
      f'target_blank={tb}')

# S20：GitHub issue 模板（反馈入口目标）
tpl = sorted(glob.glob(os.path.join(ROOT, '.github', 'ISSUE_TEMPLATE', '*')))
print(f'S20_issue_templates={[os.path.basename(x) for x in tpl]}')

# S21/S22：检索资产
print(f'S21_rag_server_exists={int(os.path.exists(os.path.join(ROOT, "scripts", "rag", "rag_server.py")))} '
      f'docs_md_total={len(glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True))}')
print(f'S22_docs_index_py={int(os.path.exists(os.path.join(ROOT, "scripts", "docs_index.py")))} '
      f'INDEX_md={int(os.path.exists(os.path.join(ROOT, "docs", "INDEX.md")))}')
tsa = os.path.join(SITE, 'static', 'js', 'text-search-app.js')
if os.path.exists(tsa):
    print(f'S24_textsearch_corpus_bytes={os.path.getsize(tsa)}')

# S23：第 21 门禁（动态链接）断言根是仓库而非部署根
cdl = os.path.join(ROOT, 'scripts', 'check_dynamic_links.py')
if os.path.exists(cdl):
    hits = [ln.strip() for ln in rd(cdl).splitlines() if 'site' in ln.lower()][:3]
    print('S23_dynamic_gate_site_mentions=' + str(hits))

# ---------- agent-web 侧 ----------

uc_p = os.path.join(AW, 'src', 'hooks', 'useChat.ts')
uc = rd(uc_p) if os.path.exists(uc_p) else ''
err_n = len(re.findall(r'type\s*===?\s*["\']error["\']', uc))
ok_n = len(re.findall(r'\.ok\b', uc))
print(f'A01_usechat_error_branch={err_n} '
      f'abortcontroller={uc.count("AbortController")} res_ok={ok_n} '
      f'setItem={uc.count("localStorage.setItem")} addEventListener_abort={uc.count("abort")}')

sv_p = os.path.join(AW, 'server', 'index.ts')
sv = rd(sv_p) if os.path.exists(sv_p) else ''
err_emit = len(re.findall(r'type:\s*"error"', sv))
done_line = re.search(r'type:\s*"done"[^\n]*', sv)
mproper = re.search(r'listen\(([^)]*)\)', sv)
la = mproper.group(1) if mproper else '?'
print(f'A05_server_error_emit={err_emit} '
      f'done_has_metrics={int(bool(done_line and "duration" in done_line.group(0) and "cost" in done_line.group(0)))} '
      f'uncaughtexception={sv.count("uncaughtException")} express_static={sv.count("express.static")} '
      f'ratelimit={len(re.findall(r"rate[- ]?limit|429", sv, re.I))} '
      f'listen_args="{la}"')

db_p = os.path.join(AW, 'server', 'db.ts')
db = rd(db_p) if os.path.exists(db_p) else ''
mt = re.search(r'CREATE TABLE IF NOT EXISTS messages\s*\(([^)]*)\)', db, re.S)
cols = [c.strip().split()[0] for c in mt.group(1).split(',') if c.strip()] if mt else []
print(f'A11_db_message_columns={cols}')

ua_p = os.path.join(AW, 'src', 'hooks', 'useAgents.ts')
ua = rd(ua_p) if os.path.exists(ua_p) else ''
mv = re.findall(r'v\d+\.\d+\.\d+', ua)
print(f'A12_useagents_version_literals={mv}')

pkg = rd(os.path.join(AW, 'package.json'))
mv2 = re.search(r'"react":\s*"([^"]+)"', pkg)
rdme = rd(os.path.join(AW, 'README.md')) if os.path.exists(os.path.join(AW, 'README.md')) else ''
print(f'A13_react_dep={mv2.group(1) if mv2 else "?"} readme_react18={int("React 18" in rdme)}')

comp = glob.glob(os.path.join(AW, 'src', 'components', '*.tsx'))
allsrc = ''.join(rd(f) for f in glob.glob(os.path.join(AW, 'src', '**', '*.tsx'), recursive=True)
                 + glob.glob(os.path.join(AW, 'src', '**', '*.ts'), recursive=True))
dead = []
for c in comp:
    name = os.path.splitext(os.path.basename(c))[0]
    uses = len(re.findall(r'from\s+[\'"][^\'"]*' + re.escape(name) + r'[\'"]', allsrc))
    if uses == 0:
        dead.append(name)
print(f'A15_dead_components={dead}')

dbfile = os.path.join(AW, 'data', 'chat.db')
try:
    con = sqlite3.connect(f'file:{dbfile}?mode=ro', uri=True)
    n_sess = con.execute('SELECT COUNT(*) FROM sessions').fetchone()[0]
    n_msg = con.execute('SELECT COUNT(*) FROM messages').fetchone()[0]
    roles = con.execute('SELECT role, COUNT(*) FROM messages GROUP BY role').fetchall()
    con.close()
    print(f'A16_chatdb_sessions={n_sess} messages={n_msg} roles={roles}')
except Exception as e:  # noqa: BLE001 — 审计脚本容忍库缺失
    print(f'A16_chatdb_error={e}')

print(f'A17_stats_endpoint={sv.count("/api/stats")} '
      f'maxlength_frontend={len(re.findall(r"maxLength", "".join(rd(f) for f in glob.glob(os.path.join(AW, "src", "**", "*.tsx"), recursive=True))))}')

print('AUDIT_DONE')
