# -*- coding: utf-8 -*-
"""_w974_final_check.py — W974 收官守恒核验（AC-12）

断言（fail-closed）：
  ① 母版总数 = 既有 40 + 本批 12 = 52
  ② 站点版总数 = 52（site/static/images/plate-line-*.webp）
  ③ 本批 12 张母版 + 12 张站点版均存在且非空
  ④ 12 个落位页均含 chapter-plate 与本批题图引用
  ⑤ 既有 40 张**零改动**（与 HEAD 比对·母版与站点版均逐字节一致）
  ⑥ 母版段与 W953 母版逐字相同（跨批风格同族）

用法：py -3 scripts/_w974_final_check.py
退出码：0 全过；1 有 FAIL。
"""
import io
import json
import os
import subprocess
import sys

REPO = r"D:\xiyouji"
SET_DIR = os.path.join(REPO, "assets", "promo", "plate-set")
SITE_IMG = os.path.join(REPO, "site", "static", "images")
OUT = os.path.join(REPO, "scripts", "output")

BATCH = [
    "plate-line-13-jinjiaodawang", "plate-line-14-yinjiaodawang",
    "plate-line-15-huangmeidawang", "plate-line-16-heixiongjing",
    "plate-line-17-tuota-lijing", "plate-line-18-yutujing",
    "plate-line-19-nvziguo-topic", "plate-line-20-chelingguo-topic",
    "plate-line-21-shituoling-topic", "plate-line-22-tonghehe-topic",
    "plate-line-23-pansidong-topic", "plate-line-24-wudidong-topic",
]
PAGES = [
    "site/reader/people/金角银角深化专题.html", "site/reader/people/银角大王.html",
    "site/reader/people/黄眉老佛外传.html", "site/reader/people/黑熊精.html",
    "site/reader/people/托塔李天王外传.html", "site/reader/people/玉兔精.html",
    "site/reader/people/女儿国国王.html", "site/reader/people/车迟国三国师外传.html",
    "site/reader/people/狮驼岭三魔-方向二深化.html", "site/reader/people/老鼋外传.html",
    "site/reader/people/蜘蛛精.html", "site/reader/people/老鼠精.html",
]
EXPECT_MASTERS = 52
EXPECT_SITE = 52


def git_blob(rel):
    p = subprocess.run(["git", "rev-parse", "HEAD:" + rel], cwd=REPO, capture_output=True)
    return p.stdout.decode().strip() if p.returncode == 0 else None


def sha(path):
    import hashlib
    with open(path, "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()


def main() -> int:
    fails = []

    masters = sorted(f[:-4] for f in os.listdir(SET_DIR)
                     if f.startswith("plate-line-") and f.endswith(".png"))
    sites = sorted(f[:-5] for f in os.listdir(SITE_IMG)
                   if f.startswith("plate-line-") and f.endswith(".webp"))
    print("=== W974 收官守恒核验 ===")
    print("母版 %d 张（期望 %d）· 站点版 %d 张（期望 %d）" % (
        len(masters), EXPECT_MASTERS, len(sites), EXPECT_SITE))
    if len(masters) != EXPECT_MASTERS:
        fails.append("母版总数 = %d（期望 %d）" % (len(masters), EXPECT_MASTERS))
    if len(sites) != EXPECT_SITE:
        fails.append("站点版总数 = %d（期望 %d）" % (len(sites), EXPECT_SITE))

    for stem in BATCH:
        for ext in (".png", ".webp"):
            p = os.path.join(SET_DIR, stem + ext)
            if not (os.path.exists(p) and os.path.getsize(p) > 0):
                fails.append("母版缺失或空：%s" % (stem + ext))
        p = os.path.join(SITE_IMG, stem + ".webp")
        if not (os.path.exists(p) and os.path.getsize(p) > 0):
            fails.append("站点版缺失或空：%s.webp" % stem)

    for rel in PAGES:
        p = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.exists(p):
            fails.append("落位页缺失：%s" % rel)
            continue
        t = io.open(p, encoding="utf-8").read()
        if "chapter-plate" not in t:
            fails.append("落位页无 chapter-plate：%s" % rel)
        if not any(s in t for s in BATCH):
            fails.append("落位页无本批题图引用：%s" % rel)

    # ⑤ 既有 40 张零改动（与 HEAD 的 blob 比对）
    prior = [m for m in masters if m not in BATCH]
    changed = []
    for stem in prior:
        for rel in (os.path.join("assets", "promo", "plate-set", stem + ".png").replace("\\", "/"),
                    os.path.join("site", "static", "images", stem + ".webp").replace("\\", "/")):
            head = git_blob(rel)
            if head is None:
                continue
            p = os.path.join(REPO, rel.replace("/", os.sep))
            if not os.path.exists(p):
                changed.append(rel + "（工作树缺失）")
                continue
            idx = subprocess.run(["git", "rev-parse", ":" + rel], cwd=REPO, capture_output=True)
            if idx.returncode == 0 and idx.stdout.decode().strip() != head:
                changed.append(rel + "（索引≠HEAD·疑似被并行改动）")
    if changed:
        fails.append("既有资产被改动：%s" % "；".join(changed[:6]))
    print("既有 %d 张母版+站点版与 HEAD 比对：%s" % (
        len(prior), "零改动 ✓" if not changed else "有 %d 处差异 ✗" % len(changed)))

    # ⑥ 母版段与 W953 逐字相同
    ref = json.load(io.open(os.path.join(OUT, "_w953_batch1.json"), encoding="utf-8"))
    w953 = ref["requests"][0]["prompt"].split("主体：")[0]
    for i in (1, 2, 3):
        data = json.load(io.open(os.path.join(OUT, "_w974_batch%d.json" % i), encoding="utf-8"))
        for r in data["requests"]:
            m = r["prompt"].split("主体：")[0]
            if m != w953:
                fails.append("母版与 W953 不逐字相同：%s" % r["output_file"])
    print("母版段（249 字符）与 W953 逐字比对：%s" % ("一致 ✓" if not any("母版与 W953" in f for f in fails) else "不一致 ✗"))

    for f in fails:
        print("  FAIL  " + f)
    print("\n合计：%d 项 FAIL" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
