"""W1167② 三态数据徽标分发生成器（正本=本文件；文案与 spark-output 链路 STATUS_* 对齐）。

三态判定（机制规则，人工可维护集合）：
  live     = 调用本地问答服务接口的页（LIVE_SET，可随接口演进调整）
  sample   = 演示数据页（DEMO_SET，显式人工清单——不靠猜）
  snapshot = 其余全部（发布时生成的内嵌快照，默认态）

用法：--dry-run / --apply / --check（第 66 槽判据内核）
替换策略：优先整元素替换旧「数据源：」行（消除 11 种口径与 EMBEDDED 行话）；
无旧行页插入 h1 之后。幂等：已有徽标 MARK 的页原位更新。
"""
import io
import re
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 根路径按 __file__ 派生：硬编码盘符在 CI（Linux runner）上指向不存在目录，
# 会让消费方门禁「扫到 0 页」而假绿——本地绿≠CI 绿（W700 教训形态）。
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "site/data"
MARK = "<!-- DATA-STATUS-BADGE v1 w1167 -->"

# LIVE_SET：证据=页面内联 JS 调本地服务接口（grep localhost:3000|/api/ 实测命中，非猜测）
LIVE_SET = {"81-hardships-view.html", "character-relationship-3d-view.html", "data-explorer.html"}
# DEMO_SET：需人工证据才可入列（business-model/graph-explorer 经查证为真实分析页，不虚构分类）
DEMO_SET = set()

STATUS_TEXT = {
    "live": ("实时数据", "本页数据来自本地问答服务接口；服务未启动时自动回退到发布快照，徽标会如实变化。"),
    "snapshot": ("内嵌快照", "本页数字为发布时生成的快照，离线双击也能看，不随接口更新。"),
    "sample": ("示例数据 · 仅演示", "本页为演示数据，只用于交互展示，不代表真实统计。"),
}

OLD_LINE = re.compile(
    r'<(p|div|small|span|li)\b[^>]*>(?:(?!</?\1\b).)*?数据源[:：](?:(?!</?\1\b).)*?</\1>',
    re.S,
)
MARKED = re.compile(re.escape(MARK) + r'\s*<div\b[^>]*data-status[^>]*>.*?</div>', re.S)
H1 = re.compile(r"<h1\b[^>]*>.*?</h1>", re.S)


def classify(name: str) -> str:
    if name in LIVE_SET:
        return "live"
    if name in DEMO_SET:
        return "sample"
    return "snapshot"


def build_badge(status: str) -> str:
    label, note = STATUS_TEXT[status]
    return (
        f'{MARK}\n'
        f'<div class="data-status-badge" data-status="{status}">'
        f'<span class="ds-dot" aria-hidden="true"></span>'
        f'<span class="ds-label">{label}</span>'
        f'<span class="ds-note">{note}</span>'
        f'</div>'
    )


def process(rel_name: str, txt: str):
    status = classify(rel_name)
    badge = build_badge(status)
    if MARK in txt:
        m = MARKED.search(txt)
        if m:
            return txt[:m.start()] + badge + txt[m.end():], "update"
        return txt, "mark-broken"
    # 不动 #dataSource（39 页内联 JS 运行时槽 + chart-a11y 依赖）与 cite-block（引文溯源块）——
    # 徽标作为规范静态表态插在其前；旧行话统一已登记批后清偿（CHANGELOG 后续项）。
    h = H1.search(txt)
    if h:
        return txt[:h.end()] + "\n" + badge + txt[h.end():], "insert-after-h1"
    return txt, "no-anchor"


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dry-run"
    stats = {}
    changed = []
    files = [f for f in sorted(DATA.glob("*.html")) if f.name != "_shell.html"]
    for f in files:
        txt = f.read_text(encoding="utf-8", errors="replace")
        new, action = process(f.name, txt)
        stats[action] = stats.get(action, 0) + 1
        if new != txt:
            changed.append(f.name)
            if mode == "--apply":
                f.write_text(new, encoding="utf-8")
    print(f"mode={mode}  pages={len(files)}  stats={stats}  改动={len(changed)}")
    bad = {k: v for k, v in stats.items() if k in ("no-anchor", "mark-broken")}
    if bad:
        print("WARN 异常:", bad)
    if mode == "--check":
        missing = [f.name for f in files if MARK not in f.read_text(encoding="utf-8", errors="replace")]
        print(f"CHECK {'FAIL 缺徽标页=' + str(len(missing)) + missing[:10] if missing else 'PASS 88/88 徽标齐'}")
        sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
