#!/usr/bin/env python3
"""_w880_og_image_split.py — 全站 og:image 分语言接线（一次性批处理脚本·W880）。

背景：W879 把共享 `site/static/img/og-cover.png` 原地换成水墨图，URL 未变 ⇒ 社交平台按 URL
缓存 og:image，新图生效滞后于缓存过期；且 og-cover.png 是 `gen_og_cover.py` 的**生成物**，
手改会被下一次生成冲掉。本脚本把 855 页的 og:image 改指**新 URL**（缓存即刻失效）：

  中文站（除 en/ 外全部页面）→ static/img/og-cover-ink-zh.jpg（取 og-09 山口关隘）
  英文站（en/ 前缀）         → static/img/og-cover-ink-en.jpg（取 og-03 白龙马）

**生成端同步**（否则下次重建即被抹）：
  - scripts/build_reader.py（reader 生成器·仅产出中文页）
  - scripts/inject_seo_head.py（全站 SEO 注入器·按 is_en 分流）
**判据端同步**（管控件·用户 2026-10-22 批准）：
  - scripts/check_seo_head.py（R1 逐页期望值改分语言·R4 改校两张现役图）

替换口径：页内**全部**出现处的旧 URL 串（og:image meta 与内联 JSON-LD 的 image 字段一并换，
避免同一页两处指向不同图）；行尾原样保留（读写均 newline=""）。

用法：python scripts/_w880_og_image_split.py [--dry-run]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BASE = "https://1273984347.github.io/xiyouji/"

OLD = BASE + "static/img/og-cover.png"
NEW_ZH = BASE + "static/img/og-cover-ink-zh.jpg"
NEW_EN = BASE + "static/img/og-cover-ink-en.jpg"


def target_for(rel: str) -> str:
    """按页面相对路径判定目标图：en/ 前缀为英文站，其余为中文站。"""
    return NEW_EN if rel.replace("\\", "/").startswith("en/") else NEW_ZH


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    changed = 0
    occurrences = 0
    zh = en = 0
    for path in sorted(SITE.rglob("*.html")):
        rel = path.relative_to(SITE).as_posix()
        with path.open(encoding="utf-8", newline="") as f:
            s = f.read()
        if OLD not in s:
            continue
        n = s.count(OLD)
        out = s.replace(OLD, target_for(rel))
        occurrences += n
        if rel.startswith("en/"):
            en += 1
        else:
            zh += 1
        changed += 1
        if not args.dry_run:
            with path.open("w", encoding="utf-8", newline="") as f:
                f.write(out)

    print("[%s] 改写 %d 页（中文 %d · 英文 %d）· 共替换旧 URL %d 处"
          % ("DRY-RUN" if args.dry_run else "APPLY", changed, zh, en, occurrences))
    print("  中文站 → %s" % NEW_ZH)
    print("  英文站 → %s" % NEW_EN)
    return 0


if __name__ == "__main__":
    sys.exit(main())
