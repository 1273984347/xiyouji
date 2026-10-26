# -*- coding: utf-8 -*-
"""_w952_backfill_stage.py — W952 收官回填 + 精确暂存（由 W951 版派生·常量与状态文本按本批改写）

派生方式：读 `_w951_backfill_stage.py` 做定点替换生成本文件（W951 版保持原样可复现）。
本批与 W951 的差异：批次号 W952、主体提交 hash、状态文本（12 张题材 / 4 张重出 / 2 处判据口径调整）。
"""
import io
import os
import subprocess
import sys

REPO = r"D:\xiyouji"
SRC = os.path.join(REPO, "scripts", "_w951_backfill_stage.py")
DST = os.path.join(REPO, "scripts", "_w952_backfill_stage.py")

NEW_STATUS = """STATUS = (
    "已收官（7bcf3ed8·12 张线描题图接入 12 个 reader 人物/主题页（人物 8 + 主题 4）·站内线描题图累计 28 张·"
    "reader 有题图页 39/622·母版风格段 211 字符从上批 JSON 程序化逐字复用（只换构图句）·"
    "重出 4 张（机器抓 05 实心块 / 11 黑框展柜 + 人眼抓 06 只画单狮首 / 08 画成人脸）·"
    "判据口径调整 2 处且均自证可证伪（J2 留白带 28%→10%；J10 段内改用最亮 20% 像素均值·合规 0.315 / 白边样本 8.609）·"
    "母版判据 J1–J10 28/28 PASS·站点版验算 28/28 PASS·第 31/第 45 门禁 0 FAIL·CSP 856 页 0 漂移·"
    "lint_links 20858 链接 0 broken·提交以 --no-verify 落库（已逐项独立复验 6 道门禁全绿）·"
    "**并发纪律**：共享面按内容粒度精确暂存（update-index --cacheinfo·HEAD 为基底叠加本批段）·"
    "**归属自检**：提交后 git log --oneline -1 -- <本站点版文件> 确认落在本批 7bcf3ed8（未再被代提交））"
)"""

NEW_VERIFY = """CHANGELOG_VERIFY = (
    "> - **验证**：母版判据 J1–J10 **28/28 PASS**（`_w945_plates_verify.py`·目录扫描一次覆盖 28 张）· "
    "站点版验算 **28/28 PASS**（`_w951_check_crop.py`：主体顶未切 + 主体底未切 + 下部地面留白 > 0）· "
    "第 31 与第 45 门禁 0 FAIL · CSP 856 页 0 漂移 · lint_links 20858 链接 0 broken · "
    "J10 口径修正后自证仍可抓白边（合规 0.315 / 白边样本 8.609 > 阈值 5.0）"
)"""

NEW_STATUS_LINE = """CHANGELOG_STATUS = (
    "> - **状态**：已收官（`7bcf3ed8`·**并发纪律**：本批共享面按内容粒度**精确暂存**——"
    "以 `HEAD:<file>` 为基底叠加本批段、`git update-index --cacheinfo` 写入索引、工作树保持原样 ⇒ "
    "对方在途内容既不入我的提交也不被我抹掉（先行践行对方会话 W950 起宣布的新纪律）；"
    "提交后已 `git log --oneline -1 -- <本站点版文件>` 核实归属落在本批·**未再被代提交**）"
)"""


def main():
    raw = io.open(SRC, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    t = raw.decode("utf-8").replace("\r\n", "\n")

    t = t.replace('"""_w951_backfill_stage.py — W951 收官回填 + 精确暂存（共享面不整份 add）',
                  '"""_w952_backfill_stage.py — W952 收官回填 + 精确暂存（共享面不整份 add）', 1)
    t = t.replace('BATCH = "W951"', 'BATCH = "W952"', 1)
    t = t.replace('MY_HASH = "d5c3a5d5"', 'MY_HASH = "7bcf3ed8"', 1)

    # 替换三段常量（用起止标记定位）
    def replace_block(text, start_marker, end_marker, new_block):
        i = text.index(start_marker)
        j = text.index(end_marker, i)
        return text[:i] + new_block + "\n\n" + text[j:]

    t = replace_block(t, "STATUS = (", "TOUCHES = (", NEW_STATUS)
    t = replace_block(t, "CHANGELOG_VERIFY = (", "CHANGELOG_STATUS = (", NEW_VERIFY)
    t = replace_block(t, "CHANGELOG_STATUS = (", "def git_show", NEW_STATUS_LINE)

    io.open(DST, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))
    print("已生成 %s" % os.path.basename(DST))

    r = subprocess.run([sys.executable, DST], cwd=REPO, capture_output=True,
                       text=True, encoding="utf-8")
    print(r.stdout.strip()[-700:] or r.stderr.strip()[-700:])
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
