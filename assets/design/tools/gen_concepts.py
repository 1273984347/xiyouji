#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_concepts.py — 分批调用生成模型出概念稿，并下载归一。

单次请求上限 10 条 → 自动按 10 条分批，逐批调用后合并。
用法：py gen_concepts.py <args.json> [下载目录名]
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import urllib.request

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
BATCH = 10


def call(batch, tag):
    args_file = os.path.join(HERE, f"_batch_{tag}.json")
    with open(args_file, "w", encoding="utf-8") as f:
        json.dump({"requests": batch}, f, ensure_ascii=False)
    cmd = (f'mcode-tools connector call connector__matrix__generate_image '
           f'--args-file "{args_file}"')
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=900)
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        print(f"[{tag}] 解析失败：{r.stdout[:400]} {r.stderr[:300]}")
        return {"success_items": []}


def main() -> int:
    if len(sys.argv) < 2:
        print("用法：py gen_concepts.py <args.json> [子目录名]")
        return 2
    args_path = sys.argv[1]
    sub = sys.argv[2] if len(sys.argv) > 2 else "concepts"
    out_dir = os.path.join(BASE, "assets", sub)
    os.makedirs(out_dir, exist_ok=True)

    with open(args_path, encoding="utf-8") as f:
        reqs = json.load(f)["requests"]

    items = []
    for i in range(0, len(reqs), BATCH):
        tag = f"{i // BATCH + 1}"
        print(f"--- 第 {tag} 批（{len(reqs[i:i + BATCH])} 张）---")
        res = call(reqs[i:i + BATCH], tag)
        ok = res.get("success_items", [])
        print(f"    成功 {len(ok)}/{len(res.get('success_items', [])) + len(res.get('failed_items', []))}")
        items += ok

    # node_id + 文件名 → 下载
    saved = 0
    for it in items:
        node_id = it.get("node_id")
        fname = it.get("file_name", "x.png")
        base = os.path.splitext(fname)[0]
        try:
            r = subprocess.run(f"mcode-tools get_asset_url {node_id}", shell=True,
                               capture_output=True, text=True, timeout=120)
            url = json.loads(r.stdout)["download_url"]
            with urllib.request.urlopen(url, timeout=120) as resp:
                data = resp.read()
            im = Image.open(io.BytesIO(data)).convert("RGB")
            w, h = im.size
            s = min(w, h)
            im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
            im = im.resize((640, 640), Image.LANCZOS)
            path = os.path.join(out_dir, f"{base}.png")
            im.save(path)
            print(f"    OK {base}.png")
            saved += 1
        except Exception as e:  # noqa: BLE001
            print(f"    FAIL {base}: {e}")
    print(f"完成：生成 {len(items)} 张，落盘 {saved} 张 → {out_dir}")
    return 0 if saved == len(items) else 1


if __name__ == "__main__":
    sys.exit(main())
