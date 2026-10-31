# -*- coding: utf-8 -*-
"""_w1043_download.py — W1043 出图原件下载（node_id → get_asset_url → raw/round17/）

口径沿用 W1018 批：下载器**幂等**（已存在且 ≥ MIN_BYTES ⇒ SKIP）⇒ 重出件必须先删旧件
（坑表 E-37）。每次下载后**立即**回读字节数与 PNG 头，避免拿到错误页/空文件。

用法：py -3 archive/scripts/batches/w10xx/_w1043_download.py
"""
import io
import json
import os
import subprocess
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
OUT = os.path.join(REPO, "scripts", "output")
DEST = os.path.join(REPO, "assets", "promo", "plate-set", "raw", "round17")
MIN_BYTES = 20000
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def _mcode_cmd():
    """定位 mcode-tools 可执行（Windows 下是 .cmd 包装器·须绝对路径 + shell=True）。

    W1044：删除 `~/.minimax/` 路径回退——铁律 16③ 禁用该目录任何内容；
    工具不在 PATH 时 fail-closed（由调用处报错），不改从用户 profile 里找。
    """
    import shutil
    p = shutil.which("mcode-tools")
    return [p] if p else ["mcode-tools"]


_MCODE_CMD = _mcode_cmd()


def _gen_files():
    for fn in sorted(os.listdir(OUT)):
        if fn.startswith("_w1043_gen") and fn.endswith(".json"):
            yield os.path.join(OUT, fn)


def main() -> int:
    os.makedirs(DEST, exist_ok=True)
    ok = skip = fail = 0
    for gp in _gen_files():
        try:
            d = json.load(io.open(gp, encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            print("FAIL  读取 %s 失败：%r" % (os.path.basename(gp), e))
            fail += 1
            continue
        items = d.get("success_items", []) or []
        for it in items:
            node_id = it.get("node_id")
            fname = it.get("file_name") or ""
            if not node_id or not fname:
                continue
            dest = os.path.join(DEST, fname)
            if os.path.exists(dest) and os.path.getsize(dest) >= MIN_BYTES:
                print("SKIP  %s（已存在 %d B）" % (fname, os.path.getsize(dest)))
                skip += 1
                continue
            try:
                # Windows：mcode-tools 是 .cmd 包装器 ⇒ subprocess 传裸名会 FileNotFoundError
                # （实测本批 12 件全失败）⇒ 用解析出的绝对路径 + shell=True。
                u = subprocess.run(_MCODE_CMD + ["get_asset_url", str(node_id)],
                                   capture_output=True, text=True, encoding="utf-8",
                                   errors="replace", timeout=120, shell=True)
                url = json.loads(u.stdout)["download_url"]
                with urllib.request.urlopen(url, timeout=180) as r:
                    data = r.read()
            except Exception as e:  # noqa: BLE001
                print("FAIL  %s 下载失败：%r" % (fname, e))
                fail += 1
                continue
            if len(data) < MIN_BYTES:
                print("FAIL  %s 过小（%d B）" % (fname, len(data)))
                fail += 1
                continue
            if not (data.startswith(PNG_MAGIC) or data.startswith(JPEG_MAGIC)):
                print("FAIL  %s 非 PNG/JPEG 头（前 8 字节 %r）" % (fname, data[:8]))
                fail += 1
                continue
            with io.open(dest, "wb") as fh:
                fh.write(data)
            print("OK    %s（%d B）" % (fname, len(data)))
            ok += 1
    print("下载完成：成功 %d · SKIP %d · 失败 %d · 目录 %s"
          % (ok, skip, fail, os.path.relpath(DEST, REPO).replace("\\", "/")))
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
