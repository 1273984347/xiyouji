import os
#!/usr/bin/env python3
"""P1 聚类推广(第二批)：narratology-13d-network + six-senses-narratology-network。
按节点分组字段(通用 parent||id||category||type)做社区聚类锚点，复用试点范式。
narratology 的 collide 是 sim 末力(以;结尾) -> 注入后补; ；six-senses 的 collide 后接 .alphaDecay -> 不补;。
"""
import io, sys, re

_W536_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _w536_guard_open(path, *a, **k):
    _real = os.path.realpath(path)
    if not (_real == _W536_ROOT or _real.startswith(_W536_ROOT + os.sep)):
        raise SystemExit("W536 guard: path escapes project root: %s" % path)
    return open(_real, *a, **k)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILES = {
    "site/data/narratology-13d-network.html": True,   # collide 行以 ; 结尾（语句结束）
    "site/data/six-senses-narratology-network.html": False,  # collide 后接 .alphaDecay（链式）
}

CLUSTER_BODY = """            // [P1聚类] 按分组字段(parent||id||category||type)做社区聚类锚点
            .force('cluster-x', d3.forceX(d => {
                const key = (d.parent || d.id || d.category || d.type || '');
                if (!window.__clusterOrder) {
                    window.__clusterOrder = Array.from(new Set(nodes.map(n => (n.parent || n.id || n.category || n.type || '')).filter(Boolean)));
                }
                const idx = window.__clusterOrder.indexOf(key);
                return (width / (window.__clusterOrder.length + 1)) * (idx + 1);
            }).strength(0.16))
            .force('cluster-y', d3.forceY(height / 2).strength(0.06))"""

for f, ends_semicolon in FILES.items():
    s = open(f, encoding='utf-8').read()
    if '[P1聚类]' in s:
        print(f"· 跳过(已注入): {f}")
        continue
    # 匹配整行 collide 力（容忍嵌套括号、首尾空白、可选;）
    pat = re.compile(r"^\s*\.force\('collide'.*?\)\s*;?\s*$", re.MULTILINE)
    m = pat.search(s)
    if not m:
        print(f"!! 未匹配 collide 行: {f}")
        continue
    collide_line = m.group(0)
    suffix = ";" if ends_semicolon else ""
    new = collide_line + "\n" + CLUSTER_BODY + suffix
    s = s[:m.start()] + new + s[m.end():]
    _w536_guard_open(f, 'w', encoding='utf-8').write(s)
    print(f"✓ 注入聚类: {f} (末力补;={ends_semicolon})")
print("完成。")
