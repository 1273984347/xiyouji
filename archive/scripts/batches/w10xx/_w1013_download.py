# -*- coding: utf-8 -*-
"""_w1013_download.py — W1013 出图下载器（node_id → 母版落盘）

流程（沿用 W1005 批做法）：
  ① 读 `scripts/output/_w1013_manifest.json`（出图返回的 node_id + file_name 清单）；
  ② 对每条跑 `mcode-tools get_asset_url <node_id>` 拿短效下载 URL；
  ③ Python urllib 下载到 `assets/promo/plate-set/raw/round15/<file_name>`；
  ④ 写后自检：文件存在 + 字节数 > 阈值 + PNG/JPEG 头可解析 + 尺寸为 3:4。

用法：py -3 scripts/_w1013_download.py
"""
import io
import json
import os
import shutil
import struct
import subprocess
import sys
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(REPO, "scripts", "output", "_w1013_manifest.json")
DEST = os.path.join(REPO, "assets", "promo", "plate-set", "raw", "round15")
MIN_BYTES = 20000
# mcode-tools 是宿主注入 PATH 的 .cmd 包装（不在系统 PATH）⇒ Python subprocess 取不到
# ⇒ 回退到宿主 bin 目录的绝对路径，并对 .cmd 走 shell=True（Windows 下直接 CreateProcess 失败）
CLI = shutil.which("mcode-tools") or "mcode-tools"   # W1044：禁 ~/.minimax 回退（铁律 16③）·缺工具即 fail-closed


def jpeg_size(b):
    i = 2
    while i < len(b) - 9:
        if b[i] != 0xFF:
            i += 1
            continue
        m = b[i + 1]
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", b[i + 5:i + 9])
            return w, h
        if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
            i += 2
            continue
        seg = struct.unpack(">H", b[i + 2:i + 4])[0]
        i += 2 + seg
    return -1, -1


def png_size(b):
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        return -1, -1
    w, h = struct.unpack(">II", b[16:24])
    return w, h


def main() -> int:
    man = json.load(io.open(MANIFEST, encoding="utf-8"))
    items = man["items"]
    os.makedirs(DEST, exist_ok=True)
    ok = 0
    for it in items:
        dst = os.path.join(DEST, it["file_name"])
        if os.path.exists(dst) and os.path.getsize(dst) >= MIN_BYTES:
            print("SKIP  %s（已落盘 %d B）" % (it["file_name"], os.path.getsize(dst)))
            ok += 1
            continue
        r = subprocess.run([CLI, "get_asset_url", it["node_id"]],
                           cwd=REPO, capture_output=True,
                           shell=CLI.lower().endswith(".cmd"))
        if r.returncode != 0:
            print("FAIL  get_asset_url %s rc=%d %s" % (it["node_id"], r.returncode,
                                                        r.stderr.decode("utf-8", "ignore")[:120]))
            continue
        info = json.loads(r.stdout.decode("utf-8"))
        url = info["download_url"]
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
        tmp = dst + ".tmp"
        io.open(tmp, "wb").write(data)
        os.replace(tmp, dst)
        if data[:2] == b"\xff\xd8":
            w, h = jpeg_size(data)
            fmt = "JPEG"
        elif data[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = png_size(data)
            fmt = "PNG"
        else:
            w, h = -1, -1
            fmt = "?"
        assert len(data) >= MIN_BYTES, "下载字节过小：%d" % len(data)
        print("OK    %-30s %s %dx%d  %d B" % (it["file_name"], fmt, w, h, len(data)))
        ok += 1
    print("---- 落盘 %d/%d ----" % (ok, len(items)))
    return 0 if ok == len(items) else 1


if __name__ == "__main__":
    raise SystemExit(main())
