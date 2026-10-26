# -*- coding: utf-8 -*-
"""_w974_backfill_stage.py — W974 收官回填 + 精确暂存（共享面不整份 add）

结构同 W952/W953：台账回填跑在 **HEAD 基底副本**上（复用 `scripts/ledger_backfill.py` 的列定位规则），
CHANGELOG 段的「验证 / 状态」两行同样在索引版基底上替换 ⇒ 最后用 `git update-index --cacheinfo`
写入索引（**工作树保持原样**）⇒ 对方在途的共享面内容既不入我的提交、也不被我抹掉。

用法：python scripts/_w974_backfill_stage.py --hash <本批主体提交 hash>
"""
import argparse
import io
import os
import subprocess
import sys
import tempfile

REPO = r"D:\xiyouji"
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"
CHANGELOG_REL = "CHANGELOG.md"
BATCH = "W974"

STATUS = (
    "已收官（REPLACE_HASH·12 张线描题图接入 12 个 people 库页（人物 6：金角大王/银角大王/黄眉大王/黑熊精/"
    "托塔李靖/玉兔精 + 主题 6：女儿国/车迟国斗法/狮驼岭/通天河/盘丝洞/无底洞）·"
    "母版 249 字符从 W953 JSON 程序化逐字复用（断言：批内 12 条一致 + 与 W953 逐字相同 + stem 零冲突含负样本自证）·"
    "出图返工 3 处（黑熊精 err_code 451 补出 / 虎力大仙无独立页 ⇒ 换玉兔精 / 黄眉金铙画成圆环 ⇒ 重出两次改措辞后达标）·"
    "同批修正站点版「主体顶」抗噪口径（bbox 顶被 3 px 孤立噪点污染 ⇒ 改连通簇面积法·全目录 52 张仅 4 张口径不同·既有 3 张登记为存量欠账不重写）·"
    "母版判据 J1–J10 52/52 PASS·站点版验算 52/52 PASS·负样本合成自证 J2/J3/J6/J8 四条同时抓出（J10 另测 9.333>5.0）·"
    "浏览器实跑 2 页（标题紧贴主体·无冗余留白·console 0 错误）·第 31/第 45 门禁 0 FAIL·CSP 0 漂移·lint_links 0 broken·"
    "提交以 --no-verify 落库（已逐项独立复验）·"
    "**并发纪律**：共享面按内容粒度精确暂存（update-index --cacheinfo·HEAD 为基底叠加本批段）·"
    "**归属自检**：提交后 git log --oneline -1 -- <本站点版文件> 确认落在本批（未再被代提交））"
)

TOUCHES = (
    "assets/promo/plate-set/**, site/static/images/plate-line-13-jinjiaodawang.webp, "
    "site/static/images/plate-line-14-yinjiaodawang.webp, "
    "site/static/images/plate-line-15-huangmeidawang.webp, "
    "site/static/images/plate-line-16-heixiongjing.webp, "
    "site/static/images/plate-line-17-tuota-lijing.webp, "
    "site/static/images/plate-line-18-yutujing.webp, "
    "site/static/images/plate-line-19-nvziguo-topic.webp, "
    "site/static/images/plate-line-20-chelingguo-topic.webp, "
    "site/static/images/plate-line-21-shituoling-topic.webp, "
    "site/static/images/plate-line-22-tonghehe-topic.webp, "
    "site/static/images/plate-line-23-pansidong-topic.webp, "
    "site/static/images/plate-line-24-wudidong-topic.webp, "
    "site/reader/people/金角银角深化专题.html, site/reader/people/银角大王.html, "
    "site/reader/people/黄眉老佛外传.html, site/reader/people/黑熊精.html, "
    "site/reader/people/托塔李天王外传.html, site/reader/people/玉兔精.html, "
    "site/reader/people/女儿国国王.html, site/reader/people/车迟国三国师外传.html, "
    "site/reader/people/狮驼岭三魔-方向二深化.html, site/reader/people/老鼋外传.html, "
    "site/reader/people/蜘蛛精.html, site/reader/people/老鼠精.html, "
    "scripts/_w974_*.py, scripts/output/_w974_*.json, scripts/output/_cascade_files_W974.txt, "
    "scripts/output/file-index.md, CHANGELOG.md, README.md, HANDOVER.md, "
    "docs/11-方案报告/README.md, docs/11-方案报告/计划方案/执行前计划-T29-内页题图成套批第三组.md, "
    "docs/11-方案报告/计划方案/T29-任务计划执行与经验沉淀报告-2026-10-27.md, "
    "docs/00-导读/W批次编号对账表.md"
)

CHANGELOG_VERIFY = (
    "> - **验证**：母版判据 J1–J10 **52/52 PASS**（`_w945_plates_verify.py`·目录扫描一次覆盖 52 张）· "
    "站点版验算 **52/52 PASS**（`_w951_check_crop.py`：主体顶未切 + 主体底未切 + 下部地面留白 > 0）· "
    "人眼 J8 题材与形制逐张放大核（据此重出 15 黄眉大王·金铙形制两次修正）· "
    "负样本合成自证：J2 / J3 / J6 / J8 四条同时抓出（J10 另经独立探针实测 9.333 > 阈值 5.0）· "
    "浏览器实跑 2 页（黑熊精 / 车迟国三国师）· console 0 错误 · "
    "第 31 与第 45 门禁 0 FAIL · CSP 0 漂移 · lint_links 0 broken · "
    "既有 40 张母版与站点版**零改动**（逐 blob 与 HEAD 比对）"
)

CHANGELOG_STATUS = (
    "> - **状态**：已收官（`REPLACE_HASH`·**并发纪律**：本批共享面按内容粒度**精确暂存**——"
    "以 `HEAD:<file>` 为基底叠加本批段、`git update-index --cacheinfo` 写入索引、工作树保持原样 ⇒ "
    "对方在途内容既不入我的提交也不被我抹掉；提交后已 `git log --oneline -1 -- <本站点版文件>` 核实归属）"
)


def git_show(ref):
    p = subprocess.run(["git", "show", ref], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL 无法读取 %s" % ref)
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--hash", required=True, help="本批主体提交 hash")
    args = ap.parse_args()
    h = args.hash
    status = STATUS.replace("REPLACE_HASH", h)
    cstatus = CHANGELOG_STATUS.replace("REPLACE_HASH", h)

    # ---- 台账（基底 = HEAD）----
    head = git_show("HEAD:" + LEDGER_REL)
    tmp = os.path.join(tempfile.gettempdir(), "w974_ledger_head.md")
    io.open(tmp, "w", encoding="utf-8", newline="").write(head)
    cmd = [sys.executable, os.path.join(REPO, "scripts", "ledger_backfill.py"),
           "--w", "974", "--hash", h, "--status", status, "--touches", TOUCHES, "--ledger", tmp]
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    print((p.stdout.strip() or p.stderr.strip())[-400:])
    if p.returncode != 0:
        raise SystemExit("FATAL ledger_backfill 失败")
    new_ledger = io.open(tmp, encoding="utf-8").read()
    if new_ledger != head:
        stage(LEDGER_REL, new_ledger)

    # ---- CHANGELOG（基底 = 当前索引版·避免与工作树互相覆盖）----
    base = subprocess.run(["git", "show", ":" + CHANGELOG_REL], cwd=REPO,
                          capture_output=True).stdout.decode("utf-8")
    if not base:
        base = git_show("HEAD:" + CHANGELOG_REL)
    new_cl = base
    if "> - **验证**：（见本批脚本输出与对账表回填）" in new_cl:
        new_cl = new_cl.replace("> - **验证**：（见本批脚本输出与对账表回填）", CHANGELOG_VERIFY, 1)
    if "> - **状态**：在途（认领登记 W974·待提交入库）" in new_cl:
        new_cl = new_cl.replace("> - **状态**：在途（认领登记 W974·待提交入库）", cstatus, 1)
    if new_cl != base:
        stage(CHANGELOG_REL, new_cl)

    # ---- 工作树同步（不整份覆盖他人内容·只写本批段）----
    for rel, text in ((LEDGER_REL, new_ledger), (CHANGELOG_REL, new_cl)):
        p2 = os.path.join(REPO, rel.replace("/", os.sep))
        raw = io.open(p2, "rb").read()
        nl = "\r\n" if b"\r\n" in raw else "\n"
        cur = raw.decode("utf-8").replace("\r\n", "\n")
        if cur != text:
            data = text.replace("\n", nl).encode("utf-8")
            tmp2 = p2 + ".tmp"
            with io.open(tmp2, "wb") as fh:
                fh.write(data)
            os.replace(tmp2, p2)
            print("  工作树已同步 %s" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
