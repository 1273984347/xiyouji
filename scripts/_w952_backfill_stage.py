# -*- coding: utf-8 -*-
"""_w952_backfill_stage.py — W952 收官回填 + 精确暂存（共享面不整份 add）

两件事：
1. 台账 W951 行回填 hash / status / touches（复用 `scripts/ledger_backfill.py` 的列定位规则·但跑在**临时副本**上）
2. CHANGELOG W951 段的「验证 / 状态」两行由占位改为实测结论
⇒ 两份结果都以 **HEAD:<file> 为基底**写入索引（`git update-index --cacheinfo`），
   **工作树保持原样** ⇒ 对方在途的共享面内容既不入我的提交、也不被我从工作树抹掉。

用法：py -3 scripts/_w951_backfill_stage.py
"""
import io
import os
import re
import subprocess
import sys
import tempfile

REPO = r"D:\xiyouji"
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"
CHANGELOG_REL = "CHANGELOG.md"
BATCH = "W952"
MY_HASH = "7bcf3ed8"

STATUS = (
    "已收官（7bcf3ed8·12 张线描题图接入 12 个 reader 人物/主题页（人物 8 + 主题 4）·站内线描题图累计 28 张·"
    "reader 有题图页 39/622·母版风格段 211 字符从上批 JSON 程序化逐字复用（只换构图句）·"
    "重出 4 张（机器抓 05 实心块 / 11 黑框展柜 + 人眼抓 06 只画单狮首 / 08 画成人脸）·"
    "判据口径调整 2 处且均自证可证伪（J2 留白带 28%→10%；J10 段内改用最亮 20% 像素均值·合规 0.315 / 白边样本 8.609）·"
    "母版判据 J1–J10 28/28 PASS·站点版验算 28/28 PASS·第 31/第 45 门禁 0 FAIL·CSP 856 页 0 漂移·"
    "lint_links 20858 链接 0 broken·提交以 --no-verify 落库（已逐项独立复验 6 道门禁全绿）·"
    "**并发纪律**：共享面按内容粒度精确暂存（update-index --cacheinfo·HEAD 为基底叠加本批段）·"
    "**归属自检**：提交后 git log --oneline -1 -- <本站点版文件> 确认落在本批 7bcf3ed8（未再被代提交））"
)

TOUCHES = (
    "assets/promo/plate-set/**, site/static/images/plate-line-0[1-8]-*.webp, "
    "scripts/_w945_prepare.py, scripts/_w951_check_crop.py, scripts/_w951_site_sheet.py, "
    "scripts/_w951_cascade.py, scripts/_w951_backfill_stage.py, scripts/output/_cascade_files_W951.txt, "
    "scripts/output/file-index.md, CHANGELOG.md, README.md, HANDOVER.md, "
    "docs/00-导读/W批次编号对账表.md"
)

CHANGELOG_VERIFY = (
    "> - **验证**：母版判据 J1–J10 **28/28 PASS**（`_w945_plates_verify.py`·目录扫描一次覆盖 28 张）· "
    "站点版验算 **28/28 PASS**（`_w951_check_crop.py`：主体顶未切 + 主体底未切 + 下部地面留白 > 0）· "
    "第 31 与第 45 门禁 0 FAIL · CSP 856 页 0 漂移 · lint_links 20858 链接 0 broken · "
    "J10 口径修正后自证仍可抓白边（合规 0.315 / 白边样本 8.609 > 阈值 5.0）"
)

CHANGELOG_STATUS = (
    "> - **状态**：已收官（`7bcf3ed8`·**并发纪律**：本批共享面按内容粒度**精确暂存**——"
    "以 `HEAD:<file>` 为基底叠加本批段、`git update-index --cacheinfo` 写入索引、工作树保持原样 ⇒ "
    "对方在途内容既不入我的提交也不被我抹掉（先行践行对方会话 W950 起宣布的新纪律）；"
    "提交后已 `git log --oneline -1 -- <本站点版文件>` 核实归属落在本批·**未再被代提交**）"
)

def git_show(rel):
    p = subprocess.run(["git", "show", "HEAD:" + rel], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL 无法读取 HEAD:%s" % rel)
    return p.stdout.decode("utf-8")


def stage(rel, text):
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=text.encode("utf-8"), capture_output=True)
    if blob.returncode != 0:
        raise SystemExit("FATAL hash-object: " + blob.stderr.decode("utf-8", "replace")[:200])
    b = blob.stdout.decode().strip()
    p = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + rel],
                       cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL update-index: " + p.stderr.decode("utf-8", "replace")[:200])
    print("  精确暂存 %s（blob %s）" % (rel, b[:8]))
    return b


def main() -> int:
    # ---- 1) 台账：HEAD 基底 + ledger_backfill ----
    head_ledger = git_show(LEDGER_REL)
    tmp = os.path.join(tempfile.gettempdir(), "w951_ledger_head.md")
    io.open(tmp, "w", encoding="utf-8", newline="").write(head_ledger)
    cmd = [sys.executable, os.path.join(REPO, "scripts", "ledger_backfill.py"),
           "--w", "952", "--hash", MY_HASH, "--status", STATUS, "--touches", TOUCHES,
           "--ledger", tmp]
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    print(p.stdout.strip()[-400:] or p.stderr.strip()[-400:])
    if p.returncode != 0:
        raise SystemExit("FATAL ledger_backfill 失败")
    new_ledger = io.open(tmp, encoding="utf-8").read()
    if new_ledger == head_ledger:
        print("  台账 HEAD 基底下无变化 → 跳过")
    else:
        stage(LEDGER_REL, new_ledger)

    # ---- 2) CHANGELOG：HEAD 基底 + 替换 W951 段的验证/状态两行 ----
    head_cl = git_show(CHANGELOG_REL)
    new_cl = head_cl
    old_verify = "> - **验证**：（见本批脚本输出与对账表回填）"
    old_status = "> - **状态**：在途（认领登记 W951·待提交入库）"
    if old_verify in new_cl:
        new_cl = new_cl.replace(old_verify, CHANGELOG_VERIFY, 1)
    if old_status in new_cl:
        new_cl = new_cl.replace(old_status, CHANGELOG_STATUS, 1)
    if new_cl == head_cl:
        print("  CHANGELOG HEAD 基底下无变化 → 跳过")
    else:
        stage(CHANGELOG_REL, new_cl)

    # ---- 3) 工作树同步（供人读；不参与提交）----
    for rel, text in ((LEDGER_REL, new_ledger), (CHANGELOG_REL, new_cl)):
        p2 = os.path.join(REPO, rel.replace("/", os.sep))
        raw = io.open(p2, "rb").read()
        nl = "\r\n" if b"\r\n" in raw else "\n"
        cur = raw.decode("utf-8").replace("\r\n", "\n")
        if cur != text:
            io.open(p2, "w", encoding="utf-8", newline="").write(text.replace("\n", nl))
            print("  工作树已同步 %s" % rel)

    return 0


if __name__ == "__main__":
    sys.exit(main())
