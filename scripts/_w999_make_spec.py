# -*- coding: utf-8 -*-
"""_w999_make_spec.py — W999 级联 spec 生成

「文件」行取**本批实际改动**（git 视角）：
  新增 = `git status --porcelain` 的 `??` 项
  修改 = `git diff --name-only HEAD` 的项
（**必须在 git add 之前生成**——新增判定基于 HEAD 树，add 后会把本批新文件误判为既有·W988 批踩过）

排除：提交信息临时文件 / 本地服务日志。
输出：scripts/output/_w999_spec.json
"""
import json
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "scripts", "output")
EXCLUDE_SUFFIX = ("_commit_msg", "_commit_msg2", "_commit_msg3", "_serve.log", "_serve.err")

STEMS = ["49-ch001-xianshi", "50-ch003-aoguang", "51-ch009-yuanshoucheng", "52-ch011-xiaoyu",
         "53-ch022-liushahe", "54-ch028-qunyao", "55-ch047-tongtianhe", "56-ch063-jiutou",
         "57-ch066-mile", "58-ch079-nanpo", "59-ch089-huangshi", "60-ch093-geigu"]
CHS = ["ch001", "ch003", "ch009", "ch011", "ch022", "ch028", "ch047", "ch063",
       "ch066", "ch079", "ch089", "ch093"]


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True, text=True, cwd=REPO).stdout


def main():
    new = set()
    for ln in git("status", "--porcelain").splitlines():
        st = ln[:2]
        path = ln[3:].strip().strip('"')
        if st == "??":
            new.add(path.replace("\\", "/"))
    mod = set(x.strip() for x in git("diff", "--name-only", "HEAD").splitlines() if x.strip())

    files = sorted(new | mod)
    files = [f for f in files if not any(f.endswith(s) or s in f for s in EXCLUDE_SUFFIX)]
    # 去掉本批明确不提交的中间产物（一次性诊断脚本）
    drop = {"scripts/_w999_probe.py", "scripts/_w999_probe_h1.py", "scripts/_w999_diag.py",
            "scripts/_w999_crop_recheck.py", "scripts/_w999_fix_t35.py",
            "scripts/_w999_register.py", "scripts/_w999_sync_counts.py"}
    files = [f for f in files if f not in drop]

    title = "W999 回次 og:image 全覆盖批·第一轮试点（12 张线描立像/场面）"
    body = (
        "\n\n\n\n> **来源**：用户 2026-10-27 选区指定下一批建议（100 回全覆盖 og:image）→ 2026-10-28 令「开始」"
        "→ 问卷裁定三处口径（线描立像族·沿用 plate-set 母版段 / 按题材定主体·战斗回场面·其余立像 / 先出 12 张试点）。\n"
        ">\n"
        "> **让号留痕**：拟用 W990，但 preflight 实测台账 max=W998 ⇒ W990–W998 已被并行批次占用（**先落地者保留**）⇒ 让号 **W999**。\n"
        ">\n"
        "> - **文件**：" + "、".join(files) + "。\n\n"
        "**本批要点**：① **缺口实读修正**——100 个回目页中**仅 8 回有配图**，真实缺口 **80 回**"
        "（初查 92 系盘点正则过严所致·已按宽松匹配复核）；② **母版段派两个变体**——立像段**逐字复用 249 字符**，"
        "场面段**仅改 3 处**（环境暗示 / 主体体例 / 点睛主语）⇒ 同族一致由构造保证（母版段原含「无背景场景」，与场面型直接冲突）；"
        "③ **12 张试点**（6 立像 + 6 场面）主体**全部避开 plate-set 已出的 34 个角色**（敖广/袁守诚/萧瑀/弥勒/南极仙翁/给孤独长者 + 流沙河对峙/群妖聚义/通天河护童/龙宫夺珠/钉钯宴）；"
        "④ **12 页接入**（题图位 + 专属 1200×630 og:image）⇒ 回目页覆盖 8 → 20 回；"
        "⑤ **5 张重出**（1 张判据红 + 4 张人眼抓）· ⑥ **裁切判据改口径**——全图墨迹 bbox 会把朱砂/赭金装饰算成主体"
        "⇒ 假红（ch089 报「主体顶被切」但主体完整）⇒ 改用连通簇（阈值与三条不变量一字未改）。\n\n"
        "**验证**：母版判据 J1–J10 **88/88 PASS** · 裁切验算 **88/88 PASS**（新口径）· 负样本自证 3/3 各自命中 · "
        "接入验收判据 V1–V6 **全 PASS**（含「未覆盖页 78 个零回归」）· 幂等复跑 12/12 SKIP · "
        "12 页 + 12 母版 + 12 og 全 HTTP 200 · 浏览器实跑渲染正常（ch001 仙石 / ch022 流沙河对峙）· "
        "第 48 门禁 0 FAIL · 全量门禁 55/55 段全绿。\n\n"
        "> - **状态**：已收官（12 张试点落地·母版族 76 → 88 张·既有 76 张母版与站点版零改动·"
        "其余 78 个无配图回目页的 og:image 仍为通用图·未误改）\n"
    )
    rows = []
    for f in files:
        note = "本批新增/修改"
        if f.startswith("site/reader/ch"):
            note = "回目页接入题图 + 换专属 1200×630 og:image"
        elif f.startswith("site/static/images/og-"):
            note = "新增专属 og:image（1200×630·由母版裁切）"
        elif f.startswith("site/static/images/plate-line-"):
            note = "新增站点版（母版裁切·只裁上部留白）"
        elif f.startswith("assets/promo/plate-set/raw/"):
            note = "出图原件（本批 12 张·含 5 张重出）"
        elif f.startswith("assets/promo/plate-set/plate-line-"):
            note = "新增母版（1200×1600·含上部留白）"
        elif f.startswith("scripts/"):
            note = "本批工具/产物"
        elif f.startswith("docs/"):
            note = "登记面（报告/坑表/计数链/方法论/台账）"
        rows.append("| %s | W999 | %s |" % (f, note))

    spec = {
        "batch": "W999",
        "date": "2026-10-28",
        "title": "W999 " + title,
        "desc": "回次 og:image 全覆盖批·第一轮试点：12 张线描立像/场面（6 立像 + 6 场面）接入 12 个回目页并换专属 1200×630 og:image",
        "head_entry": "2026-10-28（W999 回次 og:image 全覆盖批·第一轮试点 12 张）",
        "head_sentence": "回次 og:image 全覆盖首轮试点：12 张线描立像/场面接入 12 个回目页并换专属 og:image",
        "changelog_body": body,
        "milestone_block": ("- **W999 回次 og:image 全覆盖批·第一轮试点**（12 张线描立像/场面）：\n"
                            "  - 缺口实读修正：80 回（初查 92 系盘点正则过严）· 回目覆盖 8 → 20 回\n"
                            "  - 母版段两变体：立像段逐字 249 字符 + 场面段仅改 3 处\n"
                            "  - 12 张主体全部避开已出的 34 个角色 · 5 张重出（1 张判据红 + 4 张人眼抓）\n"
                            "  - 裁切判据改主体口径（连通簇）消除假红 · 坑表 +4 条（87 → 91·并发后实算 94）"),
        "agents_note": ("2026-10-28（W999）给 100 个回目页补 og:image，出了 12 张试点。三件事记下来："
                        "一是「同一角色同一范式的第二张图观感必然重复」，所以扩量前先扫已出的 76 张主体清单，"
                        "12 张的主体全挑没出现过的角色或新场面；二是母版段里的「无背景场景」和场面型打架，"
                        "于是只改三处派生出场面变体，色板笔触一个字不动；三是自己写的裁切判据也会假红——"
                        "它把朱砂点睛和赭金装饰当成了主体，明明主体好好的却报「主体顶被切」。"
                        "最后一条最要紧：判据不是裁判，是也需要被复核的一方。"),
        "file_index_rows": rows,
    }
    p = os.path.join(OUT, "_w999_spec.json")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(spec, ensure_ascii=False, indent=1))
    print("spec 写出 · 文件清单 %d 项 · file_index %d 行" % (len(files), len(rows)))
    for f in files[:14]:
        print("   ", f)
    if len(files) > 14:
        print("    ... 共 %d 项" % len(files))
