# -*- coding: utf-8 -*-
"""_w1049_handover.py — HANDOVER 头链与里程碑更新（交接面）

C2 判据（check_doc_sync.py）：交接文档头链链首 ≡ CHANGELOG 顶段。
本批提交后 CHANGELOG 顶段 = W1049（工作树含 W1050 段但已从我的提交剔除）
⇒ 头链须指向 W1049。

改动三处（结构性·符合 HANDOVER 维护契约「最后更新行只写最新 1–3 批」）：
  ① `## 一、当前进度（W…）` 标题的 W 号与摘要
  ② 文件头「最后更新：…」链（第 1 处）
  ③ 文件尾「最后更新：…；；；」链（第 2 处）
另加本批里程碑条目到「一、当前进度」列表首。

写法：临时文件 + os.replace 原子替换；保留原换行。
用法：py -3 archive/scripts/batches/w10xx/_w1049_handover.py [--dry-run]
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
P = os.path.join(REPO, "HANDOVER.md")

BATCH = "W1049"
SUMMARY = "回次 og:image 全覆盖批·第五轮（12 张线描立像/场面）"

MILESTONE = (
    "- **W1049 回次 og:image 全覆盖批·第五轮**（12 张线描立像/场面）：\n"
    "  - 缺口实读 43 回通用 og（用户口径 42 回·差 1 回系旧探针漏查 chapter-banner）· "
    "已出母版 124 张 / 唯一 slug 124 个 · 12 主体逐项实读命中 2–16 次 + 全表避重（负样本自证 5/5 可证伪）\n"
    "  - 母版段两变体：立像段逐字 249 字符（6 张）+ 场面段仅改 3 处（6 张）\n"
    "  - 12 主体：金池长老/文殊菩萨/鹿力大仙/火德星君/女儿国国王/灭法国王 + "
    "四大天王/高太公/银角大王/十代阎君/红鳞大蟒/谛听\n"
    "  - 3 张重出（97/103/107·鳞纹密排与渲染笔触超墨量上限）⇒ 全目录机器判据 136 张 FAIL 0\n"
    "  - 落位 12 回题图 ⇒ 配图覆盖 55 → 67 回 · 通用 og 缺口 43 → 31 回 · 坑表 +3 条（E-54~E-56）\n"
)


def main() -> int:
    dry = "--dry-run" in sys.argv
    raw = io.open(P, "rb").read()
    text = raw.decode("utf-8")
    nl = "\r\n" if b"\r\n" in raw else "\n"

    # ① §一 标题
    # 形态须与 batch_cascade._face_handover 的锚点正则一致：
    #   `## 一、当前进度（(?:v[\d.]+ )?W\d+ [^；]*；更早批次详见 CHANGELOG\.md）`
    # ⇒ **W 号后须有空格 + desc**（我首版写成「W1049：回次…」缺空格 ⇒ 级联锚点失配）。
    idx = text.find("## 一、当前进度（")
    assert idx >= 0, "未找到 §一 标题"
    end = text.find("\n", idx)
    old_title = text[idx:end]
    new_title = "## 一、当前进度（%s %s；更早批次详见 CHANGELOG.md）" % (BATCH, SUMMARY)
    text = text[:idx] + new_title + text[end:]
    print("① §一 标题：%s" % old_title[:60])
    print("           → %s" % new_title[:80])

    # ②③ 两处「最后更新」链：把 W1048 条替换为 W1049 条（保留 W1047/W1045 两批）
    head_old = ("最后更新：2026-10-31（W1048 P2 治理与孤儿批收编）·2026-10-31（W1047 图表判据剥标签根修）")
    head_new = ("最后更新：2026-10-31（W1049 回次 og:image 全覆盖第五轮 12 张）·"
                 "2026-10-31（W1048 P2 治理与孤儿批收编）·2026-10-31（W1047 图表判据剥标签根修）")
    tail_old = ("最后更新：2026-10-31（W1048 P2 治理与孤儿批收编）；2026-10-31（W1047 图表判据剥标签根修）；")
    tail_new = ("最后更新：2026-10-31（W1049 回次 og:image 全覆盖第五轮 12 张）；"
                 "2026-10-31（W1048 P2 治理与孤儿批收编）；2026-10-31（W1047 图表判据剥标签根修）；")
    assert head_old in text, "未找到头部最后更新链"
    assert tail_old in text, "未找到尾部最后更新链"
    text = text.replace(head_old, head_new).replace(tail_old, tail_new)
    print("②③ 两处「最后更新」链已更新（W1049 置首）")

    # 里程碑：插到「一、当前进度」列表首（W1048 条之前）
    m = text.find("- **W1048 P2 治理与孤儿批收编**：")
    assert m >= 0, "未找到 W1048 里程碑条目"
    text = text[:m] + MILESTONE + text[m:]
    print("④ 本批里程碑已插入「一、当前进度」列表首")

    if dry:
        print("DRY 未落盘")
        return 0
    data = text.replace("\n", nl).encode("utf-8")
    tmp = P + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, P)
    print("已落盘 HANDOVER.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
