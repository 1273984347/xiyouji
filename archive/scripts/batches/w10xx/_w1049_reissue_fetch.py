# -*- coding: utf-8 -*-
"""_w1049_reissue_fetch.py — 下载已成功的重出件（按 node_id 逐件·幂等跳过）"""
import io, json, os, subprocess, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
DEST = os.path.join(REPO, "assets", "promo", "plate-set", "raw", "round18")
MIN_BYTES = 20000
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def mcode_cmd():
    import shutil
    p = shutil.which("mcode-tools")
    return [p] if p else ["mcode-tools"]


def fetch(items):
    ok = 0
    for it in items:
        node_id = it.get("node_id")
        fname = it.get("file_name") or ""
        dest = os.path.join(DEST, fname)
        if os.path.exists(dest) and os.path.getsize(dest) >= MIN_BYTES:
            print("SKIP  %s（已存在 %d B）" % (fname, os.path.getsize(dest)))
            ok += 1
            continue
        u = subprocess.run(mcode_cmd() + ["get_asset_url", str(node_id)],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=120, shell=True)
        url = json.loads(u.stdout)["download_url"]
        with urllib.request.urlopen(url, timeout=180) as rr:
            data = rr.read()
        if len(data) < MIN_BYTES or not (data.startswith(PNG_MAGIC) or data.startswith(JPEG_MAGIC)):
            print("FAIL  %s 非法（%d B）" % (fname, len(data)))
            continue
        with io.open(dest, "wb") as fh:
            fh.write(data)
        print("OK    %s（%d B）" % (fname, len(data)))
        ok += 1
    return ok


if __name__ == "__main__":
    items = json.loads(sys.argv[1])
    raise SystemExit(0 if fetch(items) == len(items) else 1)
