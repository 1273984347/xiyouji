# -*- coding: utf-8 -*-
"""_w952_fix_c6.py — 修 W952 两处门禁红项后重跑级联

① **C6**：README 版本行 desc 含「·」⇒ 会让下一批级联锚点正则失配（W826 实证）⇒ 换成「、」
② **C4-f**：CHANGELOG W952 段的「文件」行写了通配符（`scripts/_w952_*.py` / `scripts/output/_w952_batch*.json`）
   ⇒ 门禁按「字面路径 token ∈ 提交树」核对 ⇒ 通配符不是路径 ⇒ 判红 ⇒ 改成**具体文件列表**

做法：改 cascade 脚本常量 → 丢弃工作树里已落的 W952 段 → 重跑 cascade（写工作树 + 精确暂存）。
"""
import io
import os
import subprocess
import sys

REPO = r"D:\xiyouji"
CASCADE = os.path.join(REPO, "scripts", "_w952_cascade.py")

OLD_README = '"> **当前批次 W952（2026-10-25）**：内页人物题图续批第二组（十二张线描题图·人物 + 主题混合，累计 28 张）"'
NEW_README = '"> **当前批次 W952（2026-10-25）**：内页人物题图续批第二组（十二张线描题图，人物 + 主题混合，累计 28 张）"'

OLD_FILES = (
    "> - **文件**：site/static/images/plate-line-01-bailongma.webp 等 12 张、assets/promo/plate-set/**、12 个 reader 页、"
    "CHANGELOG.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/_w952_*.py、"
    "scripts/_w945_plates_verify.py、scripts/output/_w952_batch*.json"
)
NEW_FILES = (
    "> - **文件**：site/static/images/plate-line-01-bailongma.webp、site/static/images/plate-line-02-dujiao-shengwang.webp、"
    "site/static/images/plate-line-03-linggan.webp、site/static/images/plate-line-04-huangfengguai.webp、"
    "site/static/images/plate-line-05-saitaisui.webp、site/static/images/plate-line-06-jiuLingyuansheng.webp、"
    "site/static/images/plate-line-07-nezha.webp、site/static/images/plate-line-08-angrixingguan.webp、"
    "site/static/images/plate-line-09-jingu-topic.webp、site/static/images/plate-line-10-jindouyun-topic.webp、"
    "site/static/images/plate-line-11-fabao-topic.webp、site/static/images/plate-line-12-wuzi-jing-topic.webp、"
    "assets/promo/plate-set/README.md、assets/promo/plate-set/preview-contact-sheet.png、"
    "assets/promo/plate-set/preview-site-sheet.png、site/reader/people/白龙马.html、"
    "site/reader/people/独角兕大王.html、site/reader/people/灵感大王.html、site/reader/people/黄风怪外传.html、"
    "site/reader/people/赛太岁.html、site/reader/people/九灵元圣-方向二深化.html、site/reader/people/哪吒.html、"
    "site/reader/people/昴日星官.html、site/reader/themes/紧箍咒专题.html、site/reader/themes/筋斗云专题.html、"
    "site/reader/themes/法宝系统专题.html、site/reader/themes/无字真经专题.html、scripts/_w952_make_prompts.py、"
    "scripts/_w952_insert_plates.py、scripts/_w952_cascade.py、scripts/_w952_check_crop_helper.py、"
    "scripts/_w952_fix_j10.py、scripts/_w952_make_edge_sample.py、scripts/_w952_update_readme.py、"
    "scripts/_w952_zoom.py、scripts/_w945_prepare.py、scripts/_w945_plates_verify.py、scripts/_w945_detail_sheet.py、"
    "scripts/output/_w952_batch1.json、scripts/output/_w952_batch2.json、scripts/output/_w952_batch3.json、"
    "scripts/output/_w952_batch4.json、scripts/output/_w952_batch5.json、scripts/output/_cascade_files_W952.txt、"
    "scripts/output/file-index.md、CHANGELOG.md、README.md、HANDOVER.md、docs/00-导读/W批次编号对账表.md"
)

SHARED = [
    "docs/00-导读/W批次编号对账表.md",
    "CHANGELOG.md",
    "scripts/output/file-index.md",
    "README.md",
    "HANDOVER.md",
]


def main():
    raw = io.open(CASCADE, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    t = raw.decode("utf-8").replace("\r\n", "\n")
    n = 0
    for old, new in ((OLD_README, NEW_README), (OLD_FILES, NEW_FILES)):
        if old in t:
            t = t.replace(old, new, 1)
            n += 1
        else:
            print("WARN 未命中：%s" % old[:50])
    io.open(CASCADE, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))
    print("cascade 常量已修 %d/2 处" % n)

    # 丢弃工作树里已落的 W952 段（我方改动）⇒ 重跑级联
    p = subprocess.run(["git", "checkout", "--"] + SHARED, cwd=REPO, capture_output=True, text=True)
    if p.returncode != 0:
        print("FATAL checkout 失败: " + p.stderr[:200])
        return 2
    print("工作树共享面已回退至 HEAD（待重跑级联）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
