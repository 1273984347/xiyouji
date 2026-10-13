# scripts/_audit_agentweb_baseline.py — 方案 R（agent-web 重设计）基线审计（只读）
# 用途：docs/superpowers/plans/2026-09-17-agent-web-redesign-plan.md 的基线取证与执行批次对账。
# 运行：python scripts/_audit_agentweb_baseline.py   （输出 KEY=value 行）
import glob
import json
import os
import re
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AW = os.path.join(ROOT, 'xiyouji-agent-web')


def rd(p):
    with open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, '/')


# B01 文件与规模
ts_files = (glob.glob(os.path.join(AW, 'server', '**', '*.ts'), recursive=True)
            + glob.glob(os.path.join(AW, 'src', '**', '*.ts'), recursive=True)
            + glob.glob(os.path.join(AW, 'src', '**', '*.tsx'), recursive=True))
loc = sum(rd(f).count('\n') + 1 for f in ts_files)
print(f'B01_ts_files={len(ts_files)} loc={loc}')

# B02 端点清单
sv = rd(os.path.join(AW, 'server', 'index.ts'))
eps = re.findall(r'app\.(get|post|patch|delete|use)\(\s*"([^"]+)"', sv)
print('B02_endpoints=' + str([f'{m.upper()} {p}' for m, p in eps]))

# B03 关键依赖版本
pkg = json.load(open(os.path.join(AW, 'package.json'), encoding='utf-8'))
deps = pkg.get('dependencies', {})
keys = ['react', 'express', '@tencent-ai/agent-sdk', '@tdesign-react/chat',
        '@tdesign-react/aigc', 'better-sqlite3', 'dompurify', 'tdesign-react']
print('B03_deps=' + str({k: deps.get(k, 'ABSENT') for k in keys}))

# B04 markdown 渲染管线（TDesign Chat 的 ChatMarkdown + DOMPurify）
cm = re.findall(r'from\s+[\'"]([^\'"]*(?:chat|aigc)[^\'"]*)[\'"]', sv + ''.join(
    rd(f) for f in glob.glob(os.path.join(AW, 'src', '**', '*.tsx'), recursive=True)))
allsrc = ''.join(rd(f) for f in ts_files)
print(f'B04_markdown chat_imports={sorted(set(cm))} dompurify_uses={allsrc.count("DOMPurify.sanitize")}')

# B05 交互能力缺口（复制/重新生成/编辑）
print(f'B05_affordances clipboard={allsrc.lower().count("clipboard")} '
      f'regenerate={len(re.findall(r"重新生成|regenerate", allsrc, re.I))} '
      f'edit_message={len(re.findall(r"editMessage|编辑消息", allsrc, re.I))}')

# B06 可靠性键（与 D-H 方案 A01 同源）
uc = rd(os.path.join(AW, 'src', 'hooks', 'useChat.ts'))
err_n = len(re.findall(r'type\s*===?\s*["\']error["\']', uc))
ok_n = len(re.findall(r'\.ok\b', uc))
print(f'B06_reliability error_branch={err_n} '
      f'abortcontroller={uc.count("AbortController")} res_ok={ok_n} '
      f'setItem={uc.count("localStorage.setItem")}')

# B07 指标与统计
db = rd(os.path.join(AW, 'server', 'db.ts'))
print(f'B07_metrics db_duration_col={int("duration_ms" in db)} db_feedback_col={int("feedback" in db)} '
      f'stats_endpoint={sv.count("/api/stats")}')

# B08 反馈闭环
print(f'B08_feedback endpoint={sv.count("/api/feedback")} '
      f'ui={len(re.findall(r"点赞|点踩|thumbsUp|thumbsup|ThumbsupIcon", allsrc, re.I))}')

# B09 双源漂移存量
ua = rd(os.path.join(AW, 'src', 'hooks', 'useAgents.ts'))
envex = rd(os.path.join(AW, '.env.example')) if os.path.exists(os.path.join(AW, '.env.example')) else ''
print(f'B09_stale useagents_v239={ua.count("v2.3.9")} useagents_oldpath={ua.count("D:/1/xiyouji")} '
      f'envexample_oldpath={envex.count("D:/1/xiyouji")}')

# B10 rag 资产
rag_srv = os.path.join(ROOT, 'scripts', 'rag', 'rag_server.py')
rag_core = os.path.join(ROOT, 'scripts', 'rag', 'xiyouji_rag.py')
rs = rd(rag_srv) if os.path.exists(rag_srv) else ''
rc = rd(rag_core) if os.path.exists(rag_core) else ''
routes = re.findall(r'path\s*==\s*"([^"]+)"', rs)
corpus = re.findall(r'(\d+) 篇', rc)[:1]
print(f'B10_rag routes={routes} corpus_claim={corpus} '
      f'docs_dir_const={int("DOCS_DIR" in rc)} exclude_rules={len(re.findall(r"startswith|excluded|跳过", rc))}')

# B11 CI 覆盖
ci = [rel(p) for p in glob.glob(os.path.join(ROOT, '.github', 'workflows', '*.yml'))
      if 'agent-web' in rd(p)]
print(f'B11_ci_files={ci}')

# B12 chat.db 实况
try:
    con = sqlite3.connect(f'file:{os.path.join(AW, "data", "chat.db")}?mode=ro', uri=True)
    print(f'B12_chatdb sessions={con.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]} '
          f'messages={con.execute("SELECT COUNT(*) FROM messages").fetchone()[0]}')
    con.close()
except Exception as e:  # noqa: BLE001
    print(f'B12_chatdb_error={e}')

# B13 移动端与无障碍基线
tsx_all = ''.join(rd(f) for f in glob.glob(os.path.join(AW, 'src', '**', '*.tsx'), recursive=True))
print(f'B13_a11y reduced_motion={allsrc.count("prefers-reduced-motion")} '
      f'aria_labels={len(re.findall(r"aria-label", tsx_all))} '
      f'fixed_sidebar={int("w-[260px]" in tsx_all or "w-[260px]" in allsrc)}')

# B14 SDK 进程依赖线索（CLI 名）
sdk_dist = glob.glob(os.path.join(AW, 'node_modules', '@tencent-ai', 'agent-sdk', '**', '*.js'), recursive=True)
cli_hits = set()
for f in sdk_dist[:80]:
    for m in re.findall(r'[\'"](codebuddycli|codebud(?:dy)?|comate|claude)[\'"]', rd(f), re.I):
        cli_hits.add(m.lower())
print(f'B15_sdk_cli_hints={sorted(cli_hits)} sdk_dist_files={len(sdk_dist)}')

# B16 公网化件现状
print(f'B16_serve express_static={sv.count("express.static")} host_env={sv.count("AGENT_WEB_HOST")} '
      f'ratelimit={len(re.findall(r"rate[- ]?limit|429", sv, re.I))} '
      f'maxlength_server={int("invalid_message" in sv or "4000" in sv)}')

print('AUDIT_DONE')
