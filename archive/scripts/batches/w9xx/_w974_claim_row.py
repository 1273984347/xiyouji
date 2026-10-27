# -*- coding: utf-8 -*-
"""_w974_claim_row.py — W974 台账认领行登记（字节级追加·保原行尾）

为什么用字节级而不是 Edit 工具：
  Edit 类工具在 CRLF 文件上按 \n 切分、写回时引入额外换行 ⇒ 行数翻倍、内容看似无损（W955 实证）。
  本脚本 open(p,'rb') → bytes.replace / bytes += → open(p,'wb')，行尾原样保留。

断言（fail-closed）：
  ① 文件以换行结尾（才能安全追加一行）
  ② 台账中不得已存在 W974 行（防重复登记）
  ③ 追加后行数 +1（防换行膨胀）

用法：py -3 scripts/_w974_claim_row.py [--dry-run]
"""
import io
import os
import sys

REPO = r"D:\xiyouji"
LEDGER = os.path.join(REPO, "docs", "00-导读", "W批次编号对账表.md")
LEDGER_REL = "docs/00-导读/W批次编号对账表.md"   # git 路径（相对·斜杠）

ROW = (
    "| W974 | 内页题图成套批·第三组（用户 2026-10-27 令「帮我做几张素材图：用途与画幅、风格与配色统一、主体清晰、"
    "留好放文字的空间都考虑到，成套出图保证风格一致」+ 明文要求「开始前先问我：素材用在哪里、需要几张、有没有参考风格」；"
    "问卷答复 = **内页题图 3:4 竖版 1200×1600** · **12 张（人物 6 + 主题 6）** · **沿用 plate-set 线描墨稿母版逐字复用**）："
    "① **母版跨批逐字复用**——直接读 W953 母版（249 字符）拼本批 SUBJECT 段，脚本内断言「批内 12 条母版逐字一致」"
    "+「与 W953 母版逐字相同」⇒ 跨三批（W945/W952/W953）风格同族由**构造**保证而非事后拼凑；"
    "② **编号段 13–24**（既有 01–12 已被 W945/W952/W953 三批复用·slug 唯一即可·新编号段零冲突）；"
    "③ **题材零重复**——人物 6（金角大王·紫金红葫芦+羊脂玉净瓶 / 银角大王·七星剑+幌金绳 / 黄眉大王·人种袋+金铙 / "
    "黑熊精·熊身人相+金箍棒 / 托塔李靖·玲珑七层宝塔+宝剑 / 虎力大仙·虎头人相+金冠+长棍）"
    "+ 主题 6（女儿国·琵琶+子母河 / 车迟国斗法·三修+油锅+仙丹 / 狮驼岭·青狮头+白象+大鹏 / 通天河·老鼋驮经 / "
    "盘丝洞·濯垢泉+蛛网 / 无底洞·金鼻白毛鼠精+地洞）——每张一件独占标志物 / 一个具象核心物，保证人眼形制可核；"
    "④ **本批专用 prep 脚本**（只处理 raw/round11 的 12 张·**不重跑全目录 prepare** ⇒ 既有 40 张母版与站点版零改动）；"
    "⑤ **站点版沿用 W951 裁切规则**（只裁上部留白·裁切线 = 主体顶 − 6 px·保留下部地面留白）；"
    "⑥ **判据复用既有 J1–J10**（目录扫描 52 张）+ 站点版裁切验算 52 张 + 负样本自证判据可证伪 | "
    "—（待回填） | —（待回填） | 在途（认领·未收官） | 主会话 2026-10-27（内页题图成套批·第三组） | "
    "`docs/11-方案报告/计划方案/执行前计划-T29-内页题图成套批第三组.md` · `assets/promo/plate-set/**` · "
    "`site/static/images/plate-line-1[3-9]-*.webp` · `site/static/images/plate-line-2[0-4]-*.webp` · "
    "`site/reader/people/**` · `site/reader/themes/**` · `scripts/_w974_*.py` · `scripts/output/_w974_*.json` · "
    "`CHANGELOG.md` · `docs/11-方案报告/README.md` · `docs/00-导读/W批次编号对账表.md`（本行） |"
)


def stage_head_exact():
    """以 **HEAD 基底** + 本批认领行精确暂存（共享面不整份 add）

    并发纪律：共享面文件（台账）**不整份 add**——若并行会话此刻正在改台账，
    整份 add 会把对方在途内容一并带进本批提交。
    ⇒ 以 `HEAD:<file>` 为基底 + 叠加本批认领行 → `git update-index --cacheinfo` 写入索引，
    工作树保持原样（对方在途内容既不入我的提交、也不被我抹掉）。
    """
    import subprocess
    head = subprocess.run(["git", "show", "HEAD:" + LEDGER_REL], cwd=REPO, capture_output=True)
    if head.returncode != 0:
        print("FATAL 无法读取 HEAD 台账")
        return 2
    text = head.stdout.decode("utf-8").replace("\r\n", "\n")
    if "| W974 |" in text:
        print("HEAD 基底已含 W974 行 → 跳过精确暂存")
        return 0
    nl = "\r\n" if b"\r\n" in head.stdout else b"\n"
    if not text.endswith("\n"):
        text += "\n"
    new_text = text + ROW + "\n"
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=new_text.encode("utf-8"), capture_output=True)
    if blob.returncode != 0:
        print("FATAL hash-object 失败")
        return 2
    b = blob.stdout.decode().strip()
    p = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + LEDGER_REL],
                       cwd=REPO, capture_output=True)
    if p.returncode != 0:
        print("FATAL update-index 失败: " + p.stderr.decode("utf-8", "replace")[:200])
        return 2
    print("精确暂存台账（blob %s·HEAD 基底 + 本批认领行·工作树保持原样）" % b[:8])
    return 0


def main() -> int:
    if "--stage-head" in sys.argv:
        return stage_head_exact()
    dry = "--dry-run" in sys.argv
    raw = io.open(LEDGER, "rb").read()
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    before_lines = raw.count(b"\n")
    print("行尾 = %s · 换行数 = %d · 字节 = %d" % (
        "CRLF" if nl == b"\r\n" else "LF", before_lines, len(raw)))

    if not raw.endswith(nl):
        print("FATAL 文件未以换行结尾，无法安全追加")
        return 2
    if b"| W974 |" in raw:
        print("FATAL 台账已存在 W974 行（防重复登记）")
        return 2
    if dry:
        print("DRY-RUN 拟追加行长度 = %d 字节" % len(ROW.encode("utf-8")))
        return 0

    data = raw + ROW.encode("utf-8") + nl
    io.open(LEDGER, "wb").write(data)

    after = io.open(LEDGER, "rb").read()
    after_lines = after.count(b"\n")
    if after_lines != before_lines + 1:
        print("FATAL 行数变化异常：%d → %d（应为 +1）" % (before_lines, after_lines))
        return 2
    if b"| W974 |" not in after:
        print("FATAL 追加后未找到 W974 行")
        return 2
    print("OK 认领行已追加 · 行数 %d → %d · 字节 %d → %d" % (
        before_lines, after_lines, len(raw), len(after)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
