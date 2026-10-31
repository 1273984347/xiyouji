# -*- coding: utf-8 -*-
"""_w988_fix_gates.py — W988 门禁两项 FAIL 的定向修复

FAIL 1 · SEO head 门禁（`scripts/check_seo_head.py` 的 og:image 白名单）
  根因：白名单是**硬编码 12 张**（W922 口径）⇒ 本批 102 页换的专属 og:image 全部不在白名单。
  修法：白名单改为**目录派生式**——`site/static/images/og-*.webp` 全部入白名单
        （W988 依用户指令「分回次 og:image」授权改管控件·W922「用户裁决批准改管控件」先例），
        en 页仍维持单值（英文封面）。目录派生 ⇒ 后续新增专属分享图不必再改门禁。

FAIL 2 · 第 31 门禁 C5c 裸聚合数字
  根因：级联把 spec 的 `desc` 写进 README/STRUCTURE/项目说明 共 4 处当前批次句，
        其中「102 页」被 C5c 判为裸聚合数字（未实体化）。
  修法：措辞改为「另给有配图的页换上专属 1200×630 og:image」（去掉裸计数），
        并同步改 spec 的 desc ⇒ 后续派生不再复现。

用法：py -3 scripts/_w988_fix_gates.py [--dry-run]
"""
import io
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
OLD_DESC_PART = "另给 102 页换上专属 1200×630 og:image"
NEW_DESC_PART = "另给有配图的页换上专属 1200×630 og:image"

SEO = os.path.join(REPO, "scripts", "check_seo_head.py")
SEO_OLD = """OG_ZH_ALLOWED = {OG_IMAGE_ZH} | {
    BASE + "static/images/og-%02d-%s.webp" % (i, kw)
    for i, kw in enumerate(
        ["kongkong", "tangseng", "bailongma", "jingubang", "bajiaoshan", "jingping",
         "qujingchuanshan", "hequshiqiao", "shankouguanai", "canjuan", "gudeng", "tongjing"], 1)
}"""
SEO_NEW = """OG_ZH_ALLOWED = {OG_IMAGE_ZH} | {
    BASE + "static/images/og-%02d-%s.webp" % (i, kw)
    for i, kw in enumerate(
        ["kongkong", "tangseng", "bailongma", "jingubang", "bajiaoshan", "jingping",
         "qujingchuanshan", "hequshiqiao", "shankouguanai", "canjuan", "gudeng", "tongjing"], 1)
} | {
    # W988（依用户 2026-10-27 指令「分回次 og:image」授权改管控件·W922「用户裁决批准改管控件」先例）：
    # og:image 分章化后，中文站页的 og:image 取「该页首屏第一张配图」的专属裁切版
    # （site/static/images/og-*.webp）⇒ 白名单改为**目录派生式**，后续新增专属分享图不必再改门禁。
    # en 页维持单值（英文封面·见 og_image_ok）。
    BASE + "static/images/" + p.name
    for p in (SITE / "static" / "images").glob("og-*.webp")
}"""

TARGETS = [
    "README.md",
    "STRUCTURE.md",
    "docs/00-导读/项目说明.md",
]


def read(p):
    raw = io.open(p, "rb").read()
    return raw.decode("utf-8"), ("\r\n" if b"\r\n" in raw else "\n")


def write(p, text, nl):
    tmp = p + ".tmp"
    io.open(tmp, "wb").write(text.replace("\r\n", "\n").replace("\n", nl).encode("utf-8"))
    os.replace(tmp, p)


def main() -> int:
    dry = "--dry-run" in os.sys.argv

    # ① SEO head 白名单
    t, n = read(SEO)
    if "目录派生式" in t:
        print("SKIP  SEO head 白名单已是目录派生式")
    else:
        # 逐行定位 `OG_ZH_ALLOWED = {OG_IMAGE_ZH} | {` … 结束的 `}`（不依赖行尾形态）
        lines = t.split("\n")
        start = None
        for i, ln in enumerate(lines):
            if "OG_ZH_ALLOWED = {OG_IMAGE_ZH}" in ln:
                start = i
                break
        assert start is not None, "未找到 OG_ZH_ALLOWED 定义"
        end = None
        for j in range(start + 1, len(lines)):
            if lines[j].strip() == "}":
                end = j
                break
        assert end is not None, "未找到 OG_ZH_ALLOWED 定义结束"
        block = [
            "} | {",
            "    # W988（依用户 2026-10-27 指令「分回次 og:image」授权改管控件·W922「用户裁决批准改管控件」先例）：",
            "    # og:image 分章化后，中文站页的 og:image 取「该页首屏第一张配图」的专属裁切版",
            "    # （site/static/images/og-*.webp）⇒ 白名单改为**目录派生式**，后续新增专属分享图不必再改门禁。",
            "    # en 页维持单值（英文封面·见 og_image_ok）。",
            '    BASE + "static/images/" + p.name',
            '    for p in (SITE / "static" / "images").glob("og-*.webp")',
            "}",
        ]
        lines[end:end + 1] = block
        t2 = "\n".join(lines)
        if dry:
            print("DRY  SEO head 白名单 → 目录派生式")
        else:
            write(SEO, t2, n)
            print("OK   SEO head 白名单已改目录派生式")

    # ② spec desc 措辞
    sp = os.path.join(OUT, "_w988_spec.json")
    with open(sp, encoding="utf-8") as fh:
        spec = json.load(fh)
    if OLD_DESC_PART in spec["desc"]:
        spec["desc"] = spec["desc"].replace(OLD_DESC_PART, NEW_DESC_PART)
        spec["head_sentence"] = spec["head_sentence"].replace(OLD_DESC_PART, NEW_DESC_PART)
        if dry:
            print("DRY  spec desc 措辞已改")
        else:
            io.open(sp, "w", encoding="utf-8", newline="\n").write(
                json.dumps(spec, ensure_ascii=False, indent=1))
            print("OK   spec desc / head_sentence 措辞已改")

    # ③ 4 处级联生成面的裸数字
    hits = 0
    for rel in TARGETS:
        p = os.path.join(REPO, rel.replace("/", os.sep))
        t, n = read(p)
        c = t.count(OLD_DESC_PART)
        if not c:
            continue
        hits += c
        if dry:
            print("DRY  %s：%d 处「102 页」" % (rel, c))
        else:
            write(p, t.replace(OLD_DESC_PART, NEW_DESC_PART), n)
            print("OK   %s：%d 处「102 页」已改措辞" % (rel, c))
    print("合计订正 %d 处" % hits)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
