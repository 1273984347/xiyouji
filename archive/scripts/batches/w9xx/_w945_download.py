# -*- coding: utf-8 -*-
"""_w945_download.py — 下载 W945 出图原件到 assets/promo/plate-set/raw/

用法：
    py -3 scripts/_w945_download.py <urls.jsonl> [目标子目录]

urls.jsonl = 每行一个 get_asset_url 返回的 JSON（含 node_id / download_url / file_name）。
保存名 = file_name 的 basename 改扩展名为 .png（统一容器格式，便于裁切与判据）。
目标子目录默认 raw/；第二轮出图用 raw/round2/。
"""
import io
import json
import os
import sys
import urllib.request

REPO = r"D:\xiyouji"
RAW_ROOT = os.path.join(REPO, "assets", "promo", "plate-set", "raw")


def main(argv):
    if len(argv) < 1 or len(argv) > 2:
        print("用法: py -3 scripts/_w945_download.py <urls.jsonl> [目标子目录]")
        return 2
    RAW = os.path.join(RAW_ROOT, argv[1]) if len(argv) == 2 else RAW_ROOT
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    bad = 0
    for line in io.open(argv[0], encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except Exception as e:
            print("BAD  JSON 解析失败: %s" % e)
            bad += 1
            continue
        url = data.get("download_url")
        node_id = data.get("node_id", "?")
        fname = data.get("file_name") or ("%s.png" % node_id)
        # 模型返回的字节实为 JPEG ⇒ 统一按 .jpg 存（避免「名为 png 实为 jpeg」）
        name = os.path.splitext(os.path.basename(fname))[0] + ".jpg"
        if not url:
            print("FAIL %-34s 无 download_url" % name)
            bad += 1
            continue
        dst = os.path.join(RAW, name)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "xiyouji-w945/1.0"})
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
            if len(data) < 4096:
                raise RuntimeError("下载内容过小(%d B)" % len(data))
            io.open(dst, "wb").write(data)
            print("OK   %-34s %8d B  <- %s" % (name, len(data), node_id))
        except Exception as e:
            print("FAIL %-34s %s" % (name, e))
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
