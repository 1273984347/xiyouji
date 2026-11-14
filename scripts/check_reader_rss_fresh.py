#!/usr/bin/env python3
"""check_reader_rss_fresh.py — reader 站与 RSS 产物新鲜度门禁（W1232·审计登记「reader/rss 新鲜度」）

为什么（2026-11-06 基础设施审计登记项）：site/reader 623 页由 build_reader.py 从 docs 生成、
site/rss.xml 由 gen_rss.py 生成——docs 源变更后产物未重建即陈旧，此前零机器判据（靠人记得跑）。

判据（git 视角·CI-safe：CI fetch-depth 0 有全历史）：
  C1 reader：site/reader 最后一次提交时间 ≥ 其全部生成输入的最后变更时间
     （输入 = docs/01-06 内容板块 + source/ + build_reader.py 自身——生成器升级同样要求重生成）
  C2 rss：site/rss.xml 最后一次提交时间 ≥ 同源输入的最后变更时间 + gen_rss.py 自身
退出码：0 = 新鲜；1 = 陈旧（产物落后于输入）；2 = 判据未执行（git 不可用/浅克隆无历史·fail-closed）
用法：python scripts/check_reader_rss_fresh.py [--gate]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import UTC, datetime

HERE = "."
READER_DIR = "site/reader"
RSS_FILE = "site/rss.xml"
SOURCE_DIRS = [
    "docs/01-全书逐回解读",
    "docs/02-人物深度分析",
    "docs/03-主题与情节专题",
    "docs/04-文化与历史背景",
    "docs/05-诗词歌赋",
    "docs/06-个人随笔",
    "source",
]
GENERATORS = ["scripts/build_reader.py", "scripts/gen_rss.py"]


def _git(args):
    r = subprocess.run(["git"] + args, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=120)
    if r.returncode != 0:
        raise RuntimeError("git %s 失败：%s" % (" ".join(args[:2]), (r.stderr or "").strip()[:160]))
    return r.stdout.strip()


def _last_commit_epoch(path: str) -> int | None:
    """路径最后一次触及提交的 epoch；从未提交返回 None。"""
    out = _git(["log", "-1", "--format=%ct", "--", path])
    return int(out) if out else None


def _newest_mtime(path: str) -> int:
    """文件自身 mtime；目录形态取其下最新文件 mtime（目录自身 mtime 不随内容改写更新）。"""
    if not os.path.isdir(path):
        return int(os.path.getmtime(path))
    newest = 0
    for root, _dirs, files in os.walk(path):
        for fn in files:
            try:
                newest = max(newest, int(os.path.getmtime(os.path.join(root, fn))))
            except OSError:
                pass
    return newest


def _effective_epoch(path: str) -> int | None:
    """产物有效时间 = max(git 最后提交, 工作树 mtime)。

    为什么取 max（W1232）：重建发生在提交**前**（收官链内跑 build_reader/gen_rss），
    此时 git log 时间仍是旧提交 ⇒ 判据会把「已重建待提交」误判陈旧（鸡生蛋）。
    工作树 mtime 覆盖该窗口：刚重建的产物 mtime ≥ 输入最新提交时间即视为新鲜。
    """
    e = _last_commit_epoch(path)
    if not os.path.exists(path):
        return e
    mtime = _newest_mtime(path)
    return max(e or 0, mtime)


def _shallow() -> bool:
    out = _git(["rev-parse", "--is-shallow-repository"])
    return out == "true"


def main() -> int:
    ap = argparse.ArgumentParser(description="reader/RSS 产物新鲜度门禁（W1232）")
    ap.add_argument("--gate", action="store_true", help="门禁模式（汇总行 + 退出码）")
    args = ap.parse_args()

    try:
        if _shallow():
            print("FAIL 浅克隆无全历史——新鲜度判据未执行（fail-closed·exit 2）")
            return 2
        inputs = SOURCE_DIRS + GENERATORS
        newest_input = None
        newest_input_path = None
        for p in inputs:
            e = _last_commit_epoch(p)
            if e is not None and (newest_input is None or e > newest_input):
                newest_input = e
                newest_input_path = p
        reader_e = _effective_epoch(READER_DIR)
        rss_e = _effective_epoch(RSS_FILE)
    except RuntimeError as exc:
        print("FAIL 判据未执行：%s（fail-closed·exit 2）" % exc)
        return 2

    if newest_input is None:
        print("FAIL 输入面全部未提交（异常状态）")
        return 2
    fails = []

    def fmt(e):
        return datetime.fromtimestamp(e, tz=UTC).strftime("%Y-%m-%d %H:%M UTC")
    if reader_e is None:
        fails.append("site/reader 从未提交（产物缺失）")
    elif reader_e < newest_input:
        fails.append("site/reader 陈旧：最后生成 %s < 输入 %s（%s）→ 重跑 python scripts/build_reader.py"
                     % (fmt(reader_e), fmt(newest_input), newest_input_path))
    if rss_e is None:
        fails.append("site/rss.xml 从未提交（产物缺失）")
    elif rss_e < newest_input:
        fails.append("site/rss.xml 陈旧：最后生成 %s < 输入 %s（%s）→ 重跑 python scripts/gen_rss.py"
                     % (fmt(rss_e), fmt(newest_input), newest_input_path))

    if args.gate or True:
        print("---- reader/RSS 新鲜度：输入最新 %s（%s）· reader %s · rss %s ----"
              % (fmt(newest_input), newest_input_path,
                 fmt(reader_e) if reader_e else "无",
                 fmt(rss_e) if rss_e else "无"))
    if fails:
        for f in fails:
            print("FAIL", f)
        print("---- reader/RSS 新鲜度：%d FAIL ----" % len(fails))
        return 1
    print("OK reader/RSS 产物新鲜（reader %.1f 天前 · rss %.1f 天前 · 均晚于最新输入）"
          % ((max(0, newest_input - reader_e)) / 86400.0 if reader_e else -1,
             (max(0, newest_input - rss_e)) / 86400.0 if rss_e else -1))
    print("---- reader/RSS 新鲜度：0 FAIL ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
