# -*- coding: utf-8 -*-
"""_w974_register_report.py — 报告目录 README §六 登记 T29 两件 + 精确暂存

共享面（`docs/11-方案报告/README.md`）**不整份 add**：以 `HEAD:<file>` 为基底叠加本批登记行
→ `git update-index --cacheinfo` 写入索引 ⇒ 并行会话在途内容既不入本批提交、也不被抹掉。

用法：py -3 scripts/_w974_register_report.py [--dry-run]
"""
import io
import os
import subprocess
import sys

REPO = r"D:\xiyouji"
REL = "docs/11-方案报告/README.md"
ABS = os.path.join(REPO, REL.replace("/", os.sep))

ROW_PLAN = (
    "| 35 | T-29《执行前计划》— 内页题图成套批·第三组（W974：12 张 3:4 竖版线描墨稿·人物 6 + 主题 6·2026-10-27·V1.0） | "
    "[执行前计划-T29-内页题图成套批第三组.md](计划方案/执行前计划-T29-内页题图成套批第三组.md) | "
    "框架第二十九次执行：用户 2026-10-27 令「帮我做几张素材图…成套出图保证风格一致」并明文要求「开始前先问我：素材用在哪里、需要几张、有没有参考风格」→ "
    "四问裁定 = **内页题图 3:4 竖版 1200×1600** / **12 张** / **沿用 plate-set 线描墨稿母版逐字复用** / **人物 + 主题各半**；"
    "含 12 条 AC + 11 步 ST + 12 项 V 指标 + 8 条风险 + **8 条决策** + 10 项自包含检查 + **8 条不完成定义**；"
    "核心设计 = **母版跨批逐字复用**（读 W953 的 249 字符母版）+ **目录扫描判据** + **资产层裁切** + **共享面精确暂存** |"
)

ROW_REPORT = (
    "| 36 | T-29《任务计划执行与经验沉淀报告》— 内页题图成套批·第三组（2026-10-27·V1.0·W974） | "
    "[T29-任务计划执行与经验沉淀报告-2026-10-27.md](计划方案/T29-任务计划执行与经验沉淀报告-2026-10-27.md) | "
    "框架第二十九次执行的终稿报告：① **12 张新题图**（人物 6：金角大王/银角大王/黄眉大王/黑熊精/托塔李靖/玉兔精 + "
    "主题 6：女儿国/车迟国斗法/狮驼岭/通天河/盘丝洞/无底洞）接入 12 个 people 库页 ⇒ 站内线描题图累计 **52 张**、"
    "reader 有题图页 **51→63**；② **母版 249 字符从 W953 JSON 逐字复用**（断言：批内 12 条一致 + 与 W953 逐字相同 + stem 零冲突含负样本自证）；"
    "③ **出图返工 3 个位**（黑熊精 err_code 451 补出 / 虎力大仙无落位页 ⇒ 换玉兔精 / 黄眉金铙画成圆环 ⇒ 重出两次改措辞后达标）；"
    "④ **同批修正站点版「主体顶」抗噪口径**（bbox 顶会被 3 px 孤立噪点污染 ⇒ 改连通簇面积法·全目录 52 张仅 4 张口径不同·既有 3 张登记为存量欠账不重写）；"
    "⑤ **判据可证伪性**：合成多维负样本 ⇒ J2/J3/J6/J8 四条同时抓出（J10 另测 9.333>5.0）；⑥ **浏览器实跑 2 页**（标题紧贴主体·无冗余留白·console 0 错误）；"
    "含 12 条 AC 验收 + **9 条经验 E-01~E-09** + 6 条风险与偏差留档 + **5 项未验证项显式声明** |"
)


def read(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def write_atomic(p, t, nl):
    data = t.replace("\n", nl).encode("utf-8")
    tmp = p + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, p)


def add_rows(text):
    """在 §六 表格末尾（`| 34 |` 行之后）插入两行登记"""
    if "T-29《执行前计划》" in text:
        return text
    lines = text.split("\n")
    anchor = None
    for i, ln in enumerate(lines):
        if ln.startswith("| 34 |"):
            anchor = i
            break
    if anchor is None:
        raise SystemExit("FATAL 未找到 §六 表格末行（| 34 |）")
    lines.insert(anchor + 1, ROW_REPORT)
    lines.insert(anchor + 1, ROW_PLAN)
    return "\n".join(lines)


def stage_exact(text):
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=text.encode("utf-8"), capture_output=True)
    if blob.returncode != 0:
        raise SystemExit("FATAL hash-object 失败")
    b = blob.stdout.decode().strip()
    p = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + REL],
                       cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL update-index 失败: " + p.stderr.decode("utf-8", "replace")[:200])
    print("  精确暂存 %s（blob %s·HEAD 基底 + 本批登记行）" % (REL, b[:8]))


def main() -> int:
    dry = "--dry-run" in sys.argv
    t, nl = read(ABS)
    new = add_rows(t)
    if new == t:
        print("工作树无变化（登记行已存在）")
    else:
        if not dry:
            write_atomic(ABS, new, nl)
        print("工作树已更新  %s（+2 行登记）" % REL)
    if dry:
        return 0
    head = subprocess.run(["git", "show", "HEAD:" + REL], cwd=REPO, capture_output=True)
    if head.returncode != 0:
        print("  跳过（HEAD 无此文件）")
        return 0
    head_new = add_rows(head.stdout.decode("utf-8").replace("\r\n", "\n"))
    if head_new == head.stdout.decode("utf-8").replace("\r\n", "\n"):
        print("  HEAD 基底下无新增 → 跳过暂存")
    else:
        stage_exact(head_new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
