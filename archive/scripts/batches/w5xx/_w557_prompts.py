# _w557_prompts.py — 生成 98 组 judge 提示文件（组号/页表/切片绝对路径）
import json
from pathlib import Path

ROOT = Path('.')
plan = json.loads((ROOT / 'scripts/output/review-pass3/group-plan.json').read_text(encoding='utf-8'))
outdir = ROOT / 'scripts/output/review-pass3/prompts'
outdir.mkdir(parents=True, exist_ok=True)
for g in plan:
    lines = [f"GROUP {g['group']}/98", f"PAGES: {json.dumps(g['pages'], ensure_ascii=False)}", "SLICES:"]
    for p in g['paths']:
        lines.append('D:\\xiyouji\\.review-tmp\\slices\\' + p.split('\\')[-1])
    (outdir / f"group-{g['group']:02d}.txt").write_text('\n'.join(lines), encoding='utf-8')
print('prompts written:', len(plan))
