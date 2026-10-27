# -*- coding: utf-8 -*-
"""_w983_download.py — W983 出图原件下载（node_id → 本地 raw/round12/）

流程：
  1. 对每个 node_id 调 `mcode-tools get_asset_url <node_id>` 取短期下载 URL
  2. urllib 下载落盘（文件名取 output_file 的 base + .jpg——模型返回实为 JPEG）

与 `_w945_download.py` 的差异：本脚本自己调 get_asset_url（不必手工拼 urls.jsonl），
且**按 node_id ↔ 目标名映射**落盘（避免模型返回文件名与预期 stem 不一致时串图）。

用法：py -3 scripts/_w983_download.py <映射文件.json> [目标子目录]
映射文件格式：[{"node_id": "...", "file": "plate-line-13-jinjiaodawang.png"}, ...]
"""
import io
import json
import os
import shutil
import subprocess
import sys
import urllib.request

REPO = r"D:\xiyouji"
RAW_ROOT = os.path.join(REPO, "assets", "promo", "plate-set", "raw")

# mcode-tools 在本机是 `mcode-tools.cmd`（批处理）——Windows CreateProcess 不做 PATHEXT 扩展
# ⇒ subprocess 直接传 "mcode-tools" 会报 WinError 2（文件不存在）⇒ 必须显式解析 .cmd 路径。
MCODE = (shutil.which("mcode-tools.cmd") or shutil.which("mcode-tools")
         or os.path.join(os.path.dirname(sys.executable), "mcode-tools.cmd")
         or r"C:\Users\12739\.minimax\bin\mcode-tools.cmd")


def get_url(node_id: str) -> str:
    p = subprocess.run([MCODE, "get_asset_url", node_id],
                       capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        raise RuntimeError("get_asset_url 失败(%s): %s" % (p.returncode, p.stderr.strip()[:200]))
    data = json.loads(p.stdout)
    if not data.get("download_url"):
        raise RuntimeError("无 download_url: %s" % p.stdout[:200])
    return data["download_url"]


def main(argv):
    if len(argv) < 1 or len(argv) > 2:
        print("用法: py -3 scripts/_w983_download.py <映射文件.json> [目标子目录]")
        return 2
    raw = os.path.join(RAW_ROOT, argv[1]) if len(argv) == 2 else RAW_ROOT
    if not os.path.isdir(raw):
        os.makedirs(raw)
    items = json.load(io.open(argv[0], encoding="utf-8"))
    bad = 0
    for it in items:
        node_id = it["node_id"]
        base = os.path.splitext(os.path.basename(it["file"]))[0]
        dst = os.path.join(raw, base + ".jpg")
        try:
            url = get_url(node_id)
            req = urllib.request.Request(url, headers={"User-Agent": "xiyouji-w983/1.0"})
            with urllib.request.urlopen(req, timeout=300) as r:
                blob = r.read()
            if len(blob) < 4096:
                raise RuntimeError("下载内容过小(%d B)" % len(blob))
            io.open(dst, "wb").write(blob)
            print("OK   %-38s %8d B  <- %s" % (base + ".jpg", len(blob), node_id))
        except Exception as e:
            print("FAIL %-38s %s" % (base, e))
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
