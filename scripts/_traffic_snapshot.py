#!/usr/bin/env python3
"""_traffic_snapshot.py — GitHub Traffic API 快照落盘（一次性/周期工具·W651）

背景（读者数据复盘 第零·二 三源同采法）：Traffic API 仅保留滚动 14 日窗，过期不可回溯——
须定期快照落盘方能形成时间序列。clones uniques 由 CI/dependabot 拉取主导，
不可换算为读者数（2026-10-02 实测 clones 225 vs views 3）；views 与 popular/referrers 才是弱信号。

用法：
  py -3 scripts/_traffic_snapshot.py                 # 快照写入 scripts/output/traffic-snapshots/
  py -3 scripts/_traffic_snapshot.py --out DIR       # 自定义输出目录

依赖：gh CLI 已登录（read:org 不需要，public 仓库 traffic 端点须 push 权限——本仓 owner 即用户）。
输出：traffic-snapshot-YYYY-MM-DD.json（views/clones/popular_paths/popular_referrers 四端点原样 + 采集时点）。
"""

import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

REPO = "1273984347/xiyouji"
ENDPOINTS = [
    "traffic/views",
    "traffic/clones",
    "traffic/popular/paths",
    "traffic/popular/referrers",
]


def gh_get(endpoint: str) -> object:
    r = subprocess.run(
        ["gh", "api", f"repos/{REPO}/{endpoint}"],
        capture_output=True, text=True, timeout=60,
    )
    if r.returncode != 0:
        raise RuntimeError(f"gh api {endpoint} 失败：{r.stderr.strip()[:200]}")
    return json.loads(r.stdout)


def main() -> int:
    out_dir = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else \
        Path(__file__).resolve().parent / "output" / "traffic-snapshots"
    out_dir.mkdir(parents=True, exist_ok=True)
    snap = {
        "captured_at": datetime.now().isoformat(timespec="seconds"),
        "capture_date": date.today().isoformat(),
        "window_note": "GitHub Traffic API 固定滚动 14 日窗·过期不可回溯",
        "caveat": "clones uniques 由 CI/dependabot 拉取主导，不可换算为读者数（W649 复盘第零·二）",
    }
    for ep in ENDPOINTS:
        try:
            snap[ep.split("/", 1)[1]] = gh_get(ep)
        except Exception as e:  # noqa: BLE001
            snap[ep.split("/", 1)[1]] = {"error": str(e)}
    out = out_dir / f"traffic-snapshot-{date.today().isoformat()}.json"
    out.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")
    v = snap.get("views", {})
    c = snap.get("clones", {})
    print(f"快照已写出：{out}")
    print(f"  views: count={v.get('count')} uniques={v.get('uniques')} · clones: count={c.get('count')} uniques={c.get('uniques')}")
    refs = snap.get("referrers") or []
    if isinstance(refs, list) and refs:
        print("  referrers: " + " · ".join(f"{r.get('referrer')}={r.get('count')}" for r in refs[:5]))
    else:
        print("  referrers: Nothing to display（与后台一致）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
