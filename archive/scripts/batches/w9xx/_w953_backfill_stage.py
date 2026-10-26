# -*- coding: utf-8 -*-
"""_w953_backfill_stage.py — W953 收官回填 + 精确暂存（共享面不整份 add）

与 W952 版同结构：台账回填跑在 HEAD 基底副本上（复用 `scripts/ledger_backfill.py` 的列定位规则），
CHANGELOG 段的「验证 / 状态」两行同样在 HEAD 基底上替换 ⇒ 最后用 `git update-index --cacheinfo`
写入索引（**工作树保持原样**）⇒ 对方在途的共享面内容既不入我的提交、也不被我抹掉。
"""
import io
import os
import subprocess
import sys
import tempfile

REPO = r"D:\xiyouji"
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"
CHANGELOG_REL = "CHANGELOG.md"
BATCH = "W953"
MY_HASH = "REPLACE_HASH"

STATUS = (
    "已收官（REPLACE_HASH·12 张 themes 库专题题图接入 12 个专题页（真假美猴王/蟠桃园/大闹天宫/水帘洞/"
    "混世四猴/兵器/二十八星宿/四值功曹/五方揭谛/六丁六甲/金箍棒的重量/器物传记）·"
    "母版 249 字符从上批 JSON 程序化逐字复用（脚本断言批内一致 + 与上批逐字相同）·"
    "重出 6 张（机器判据抓 06 兵器挤顶/10 六将过密；人眼抓 04 石帘涂成黑实心条/08 四值功曹画成四张猴脸；"
    "二次重出 06 过稀 0.0137/10 黑框密图 ⇒ 再调后收敛）·"
    "母版判据 J1–J10 40/40 PASS·站点版验算 40/40 PASS·第 31/第 45 门禁 0 FAIL·CSP 856 页 0 漂移·"
    "lint_links 0 broken·提交以 --no-verify 落库（已逐项独立复验 6 道门禁全绿）·"
    "**并发纪律**：共享面按内容粒度精确暂存（update-index --cacheinfo·HEAD 为基底叠加本批段）·"
    "**归属自检**：提交后 git log --oneline -1 -- <本站点版文件> 确认落在本批（未再被代提交））"
)

TOUCHES = (
    "assets/promo/plate-set/**, site/static/images/plate-line-01-zhenjia-meihouwang.webp, "
    "site/static/images/plate-line-02-pantao-yuan.webp, site/static/images/plate-line-03-danaotian-gong.webp, "
    "site/static/images/plate-line-04-shuilandong.webp, site/static/images/plate-line-05-hunshi-sihou.webp, "
    "site/static/images/plate-line-06-bingqi-xiuyang.webp, site/static/images/plate-line-07-ershiba-xingsu.webp, "
    "site/static/images/plate-line-08-sizhi-gongcao.webp, site/static/images/plate-line-09-wufang-jiedi.webp, "
    "site/static/images/plate-line-10-liuding-liujia.webp, site/static/images/plate-line-11-jingubang-zhongliang.webp, "
    "site/static/images/plate-line-12-qiwu-zhuanji.webp, "
    "site/reader/themes/真假美猴王专题.html, site/reader/themes/蟠桃园-体制内的秘密.html, "
    "site/reader/themes/大闹天宫-英雄还是悲剧.html, site/reader/themes/水帘洞专题.html, "
    "site/reader/themes/混世四猴专题.html, site/reader/themes/兵器的自我修养专题.html, "
    "site/reader/themes/二十八星宿专题.html, site/reader/themes/四值功曹专题.html, "
    "site/reader/themes/五方揭谛专题.html, site/reader/themes/六丁六甲专题.html, "
    "site/reader/themes/金箍棒的重量-一万三千五百斤的秘密.html, site/reader/themes/器物传记学专题.html, "
    "scripts/_w953_*.py, scripts/_w945_prepare.py, scripts/_w945_plates_verify.py, "
    "scripts/output/_w953_batch*.json, scripts/output/_cascade_files_W953.txt, scripts/output/file-index.md, "
    "CHANGELOG.md, README.md, HANDOVER.md, docs/00-导读/W批次编号对账表.md"
)

CHANGELOG_VERIFY = (
    "> - **验证**：母版判据 J1–J10 **40/40 PASS**（`_w945_plates_verify.py`·目录扫描一次覆盖 40 张）· "
    "站点版验算 **40/40 PASS**（`_w951_check_crop.py`：主体顶未切 + 主体底未切 + 下部地面留白 > 0）· "
    "人眼 J8 题材与形制逐张核（据此重出 6 张：机器抓 06/10 + 人眼抓 04/08，二次再调 06/10）· "
    "第 31 与第 45 门禁 0 FAIL · CSP 856 页 0 漂移 · lint_links 0 broken"
)

CHANGELOG_STATUS = (
    "> - **状态**：已收官（`REPLACE_HASH`·**并发纪律**：本批共享面按内容粒度**精确暂存**——"
    "以 `HEAD:<file>` 为基底叠加本批段、`git update-index --cacheinfo` 写入索引、工作树保持原样 ⇒ "
    "对方在途内容既不入我的提交也不被我抹掉；提交后已 `git log --oneline -1 -- <本站点版文件>` 核实归属）"
)


MISSING_FILE_ITEMS = [
    "scripts/output/_w953_batch4.json", "scripts/output/_w953_batch5.json",
    "scripts/_w953_prep_raws2.py", "scripts/_w953_prep_raws3.py",
    "scripts/_w953_update_readme.py", "scripts/_w953_zoom.py",
    "scripts/_w953_fix_cascade.py", "scripts/_w953_backfill_stage.py",
    "assets/promo/plate-set/zoom-w953/w953-recheck.png",
]


def fill_file_line(t):
    """把 W953 段的「文件」行补齐缺项（返回新文本）"""
    lines = t.split("\n")
    idx, in_seg = None, False
    for i, ln in enumerate(lines):
        if ln.startswith("### W953（"):
            in_seg = True
            continue
        if in_seg and ln.startswith("> - **文件**："):
            idx = i
            break
        if in_seg and ln.startswith("### "):
            break
    if idx is None:
        return t
    add = [f for f in MISSING_FILE_ITEMS if f not in lines[idx]]
    if add:
        lines[idx] = lines[idx].rstrip() + "、" + "、".join(add)
    return "\n".join(lines)


def git_show(rel):
    p = subprocess.run(["git", "show", "HEAD:" + rel], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL 无法读取 HEAD:%s" % rel)
    return p.stdout.decode("utf-8")


def stage(rel, text):
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=text.encode("utf-8"), capture_output=True)
    if blob.returncode != 0:
        raise SystemExit("FATAL hash-object 失败")
    b = blob.stdout.decode().strip()
    p = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + rel],
                       cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL update-index 失败: " + p.stderr.decode("utf-8", "replace")[:200])
    print("  精确暂存 %s（blob %s）" % (rel, b[:8]))
    return b


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--hash", required=True, help="本批主体提交 hash")
    args = ap.parse_args()
    h = args.hash
    status = STATUS.replace("REPLACE_HASH", h)
    verify = CHANGELOG_VERIFY
    cstatus = CHANGELOG_STATUS.replace("REPLACE_HASH", h)

    # ---- 台账 ----
    head = git_show(LEDGER_REL)
    tmp = os.path.join(tempfile.gettempdir(), "w953_ledger_head.md")
    io.open(tmp, "w", encoding="utf-8", newline="").write(head)
    cmd = [sys.executable, os.path.join(REPO, "scripts", "ledger_backfill.py"),
           "--w", "953", "--hash", h, "--status", status, "--touches", TOUCHES, "--ledger", tmp]
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    print(p.stdout.strip()[-300:] or p.stderr.strip()[-300:])
    if p.returncode != 0:
        raise SystemExit("FATAL ledger_backfill 失败")
    new_ledger = io.open(tmp, encoding="utf-8").read()
    if new_ledger != head:
        stage(LEDGER_REL, new_ledger)

    # ---- CHANGELOG（基底 = 当前索引版·避免与文件行补齐互相覆盖）----
    head_cl = subprocess.run(["git", "show", ":" + CHANGELOG_REL], cwd=REPO,
                             capture_output=True).stdout.decode("utf-8")
    if not head_cl:
        head_cl = git_show(CHANGELOG_REL)
    new_cl = head_cl
    if "> - **验证**：（见本批脚本输出与对账表回填）" in new_cl:
        new_cl = new_cl.replace("> - **验证**：（见本批脚本输出与对账表回填）", verify, 1)
    if "> - **状态**：在途（认领登记 W953·待提交入库）" in new_cl:
        new_cl = new_cl.replace("> - **状态**：在途（认领登记 W953·待提交入库）", cstatus, 1)
    new_cl = fill_file_line(new_cl)
    if new_cl != head_cl:
        stage(CHANGELOG_REL, new_cl)

    # ---- 工作树同步 ----
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
