# -*- coding: utf-8 -*-
"""_w1005_heroes.py — W1005：两张 hero 水墨图重出（人数修正为「4 人形 + 1 匹白马」）

用户 2026-10-29 指出：`site/static/images/ink-mountains-hero.webp`「内容不符合西游记·为什么有七个人」
⇒ 查档：W852 批的 hero-01 档案明写「山脊云海+**七人单行**」⇒ **W852 批就画错了人数**；
而 W879 批原地替换的 ink-mountains-hero 沿用了同一错误 ⇒ 本批一并修两张。

用户裁定（2026-10-29 问卷）：
  · 人物口径 = **取经五人组：4 人形 + 1 匹白马**（唐僧·悟空·八戒·沙僧 + 白龙马）
  · 范围 = 两张一并修

规格（原地替换·同文件名同尺寸 ⇒ 848 页零页面改动）：
  A `ink-mountains-hero.webp`  1792×1024  .hero 深底 soft-light 合成底图
      ⇒ 必须「**浅/亮底 + 浓墨近黑山影**」（W879 批结论：源越暗越显影·源越亮越隐形）
  B `hero-01-xihai-yunhai.webp` 2560×1440  宣传单页配图（浅底直显）

输出：scripts/output/_w1005_batch.json（出图批次）+ scripts/output/_w1005_heroes.json（判据报告）
用法：py -3 scripts/_w1005_heroes.py [--stage batch|prepare|report]
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
RAW = os.path.join(REPO, "assets", "promo", "hero-set", "raw", "round-w1005")
IMG = os.path.join(REPO, "site", "static", "images")
PY = sys.executable

TEAM = ("队伍剪影**恰好四个**：最前一名披袈裟的僧人、其后一名持长棍的猴形、一个猪首僧挑着担子、"
        "最后一名卷发僧挑着行李；**这四人身后跟着一匹白马**。"
        "画面中**只有这四名人影与一匹白马**——不得出现第五个人影、不得出现第二匹马、不得出现其他动物。"
        "剪影极小如米粒、只作点缀，不可放大成主体。")

# 队伍落位限定：`.hero` 背景用 `background-position: center 70%` ⇒ 队伍若贴在画面下缘会被裁出
# ⇒ 队伍须落在山脊中部（垂直 45%–60%），裁切后仍完整可见。
TEAM_POS = ("队伍整体位于画面右侧山脊的中部（垂直方向约 45%–60% 处），不可贴近画面下边缘，"
            "合成裁切后须仍完整可见。")


PROMPT_A = (
    "浅米白宣纸底（暖白 #F8F3E9 至 #FBF3EA 一族），大片留白。"
    "画面中下部与左侧是一道**浓墨近黑**的横向连绵山影（湿染枯笔、深黑成片，不要淡灰），"
    "山间有云雾白气自下向上漫过山腰；一条**赭金色**细窄小径自左下蜿蜒通向右侧山脊；"
    + TEAM + " " + TEAM_POS +
    "无文字、无落款、无印章、无水印、无边框。"
)

PROMPT_B = (
    "浅米白宣纸底（#F8F3E9 至 #FBF3EA 一族），大片淡墨云海翻涌，远山以淡墨勾形、"
    "右上方山头染赭金色；一条细窄曲径自左下蜿蜒盘上主脊；"
    + TEAM +
    "画面**下方约四成完全空白**（不画地面、不画草木、不画文字）；"
    "无文字、无落款、无印章、无水印、无边框。"
)

JOBS = [
    {"key": "ink-mountains-hero", "size": (1792, 1024), "prompt": PROMPT_A},
    {"key": "hero-01-xihai-yunhai", "size": (2560, 1440), "prompt": PROMPT_B},
]


def write_batch():
    os.makedirs(RAW, exist_ok=True)
    reqs = []
    for j in JOBS:
        reqs.append({"prompt": j["prompt"], "aspect_ratio": "16:9", "resolution": "2K",
                     "output_file": "assets/promo/hero-set/raw/round-w1005/%s.png" % j["key"]})
    p = os.path.join(OUT, "_w1005_batch.json")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"requests": reqs}, ensure_ascii=False, indent=1))
    print("出图批次写出:", os.path.basename(p), "·", len(reqs), "条")
    for r in reqs:
        print("   ", r["output_file"].split("/")[-1], "| prompt %d 字" % len(r["prompt"]))


def download(mapping):
    MCODE = None
    for cand in ("mcode-tools.cmd", "mcode-tools"):
        r = subprocess.run(["where", cand], capture_output=True, text=True, shell=True)
        if r.returncode == 0 and r.stdout.strip():
            MCODE = r.stdout.strip().splitlines()[0]
            break
    if not MCODE:
        print("FAIL  找不到 mcode-tools")
        return 1
    os.makedirs(RAW, exist_ok=True)
    for node_id, name in mapping:
        p = subprocess.run([MCODE, "get_asset_url", node_id], capture_output=True, text=True, timeout=180)
        if p.returncode != 0:
            print("FAIL  get_asset_url", node_id, p.stderr[:120])
            continue
        url = json.loads(p.stdout)["download_url"]
        import urllib.request
        dst = os.path.join(RAW, name + ".jpg")
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "xiyouji/1.0"}),
                                   timeout=300) as r2:
            blob = r2.read()
        with open(dst, "wb") as fh:
            fh.write(blob)
        print("OK   %-42s %8d B" % (name + ".jpg", len(blob)))
    return 0


def crop_to(im, size):
    """裁到精确比例（不拉伸）+ 缩放到目标尺寸。"""
    tw, th = size
    want = tw / th
    w, h = im.size
    cur = w / h
    if cur > want:
        nw = int(round(h * want))
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(round(w / want))
        im = im.crop((0, 0, w, nh))
    return im.resize(size, Image.LANCZOS)


def softlight_span(im, board=(0x22, 0x1D, 0x16)):
    """soft-light 合成到深底后的亮度跨度（显影度）—— W879 批口径：≥0.07 即显影。"""
    from PIL import ImageChops
    bg = Image.new("RGB", im.size, board)
    out = ImageChops.blend(bg, im, 0.0)          # 占位，真正的 soft-light 手工算
    a = [v / 255.0 for v in board]
    px = im.convert("RGB").load()
    vals = []
    for y in range(0, im.height, 3):
        for x in range(0, im.width, 3):
            s = [px[x, y][i] / 255.0 for i in range(3)]
            o = []
            for i in range(3):
                b, sv = a[i], s[i]
                if sv <= 0.5:
                    r = b - (1 - 2 * sv) * b * (1 - b)
                else:
                    d = min(b, 1 - b)
                    r = b + (2 * (sv - 0.5) * d)
                o.append(r)
            vals.append(0.299 * o[0] + 0.587 * o[1] + 0.114 * o[2])
    return max(vals) - min(vals)


def dark_cluster_count(im, tol=40, min_area=12):
    """山脊带内「深墨小簇」计数（人形剪影的机器上限检查：期望 ≤5，>5 判红）。"""
    import numpy as np
    from scipy import ndimage
    a = np.asarray(im.convert("L"), dtype=np.int16)
    m = a < tol
    if not m.any():
        return 0
    labels, n = ndimage.label(m, structure=np.ones((3, 3), dtype=int))
    sizes = ndimage.sum(m, labels, index=np.arange(1, n + 1))
    # 只数「小簇」（人形剪影尺度）——大块山影不计入
    small = [i + 1 for i, s in enumerate(sizes) if min_area <= s <= 900]
    return len(small)


def prepare(mapping):
    """裁切到目标尺寸 + 存站点版（webp）+ 出判据报告。"""
    report = []
    for node_id, name in mapping:
        src = os.path.join(RAW, name + ".jpg")
        if not os.path.exists(src):
            print("FAIL  原件缺失:", src)
            continue
        im = Image.open(src).convert("RGB")
        job = next(j for j in JOBS if j["key"] == name)
        out = crop_to(im, job["size"])
        dst = os.path.join(IMG, name + ".webp")
        tmp = dst + ".tmp"
        out.save(tmp, "WEBP", quality=88, method=6)
        os.replace(tmp, dst)
        span = softlight_span(out)
        clusters = dark_cluster_count(out)
        kb = os.path.getsize(dst) / 1024.0
        report.append({"key": name, "size": list(job["size"]), "kb": round(kb, 1),
                       "softlight_span": round(span, 4), "dark_small_clusters": clusters})
        print("OK   %-26s %s · %.1f KB · 显影跨度 %.4f · 深墨小簇 %d"
              % (name, job["size"], kb, span, clusters))
    with open(os.path.join(OUT, "_w1005_heroes.json"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(report, ensure_ascii=False, indent=1))
    return 0


def main() -> int:
    stage = "batch"
    for a in sys.argv[1:]:
        if a.startswith("--stage="):
            stage = a.split("=", 1)[1]
    if stage == "batch":
        write_batch()
    elif stage in ("download", "prepare"):
        mp = os.path.join(OUT, "_w1005_map.json")
        mapping = [(m["node_id"], m["key"]) for m in json.load(open(mp, encoding="utf-8"))]
        if stage == "download":
            return download(mapping)
        return prepare(mapping)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
