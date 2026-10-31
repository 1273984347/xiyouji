# -*- coding: utf-8 -*-
"""_w1049_readme_register.py — 报告目录 §六（计划方案）登记本批执行前计划件

纪律：临时文件 + os.replace 原子替换；读入保留原换行；写回用原行尾。
用法：py -3 archive/scripts/batches/w10xx/_w1049_readme_register.py [--dry-run]
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
P = os.path.join(REPO, "docs", "11-方案报告", "README.md")

ROW = (
    "| 55 | 执行前计划-W1049-回次og-image全覆盖第五轮（2026-10-31·W1049） | "
    "[执行前计划-W1049-回次og-image全覆盖第五轮.md]"
    "(计划方案/执行前计划-W1049-回次og-image全覆盖第五轮.md) | "
    "用户令「剩余 42 回 og 扩量开始」＋规模裁决「12 张一批」："
    "**缺口实读 43 回**（用户口径 42 回·差 1 回系旧探针漏查 chapter-banner·两探针差集={019,031}）· "
    "12 主体逐项实读命中 2–16 次且与已出 124 slug / 49 个已落位主体名零冲突"
    "（选材判据五项全绿＋**负样本自证 5/5 可证伪**·并修判据自身 key 形态 bug）· "
    "母版段两变体（立像逐字 249 字符＋场面改 3 处）· "
    "**3 张重出**（97/103/107·103 铠甲鳞纹密排与 107 山石渲染笔触超 J3 墨量上限·"
    "97 二版因「稀疏留白」措辞与母版段「占幅五成」打架反使 J4 更低 ⇒ 三版删留白措辞改显式放大占幅）"
    "⇒ **全目录机器判据 136 张 FAIL 0** · 落位 12 回题图 ⇒ "
    "**配图覆盖 55→67 回·通用 og 缺口 43→31 回** · 坑表 +3 条（E-54~E-56）|"
)


def main() -> int:
    dry = "--dry-run" in sys.argv
    raw = io.open(P, "rb").read()
    text = raw.decode("utf-8")
    nl = "\r\n" if b"\r\n" in raw else "\n"

    assert ROW not in text, "登记行已存在（勿重复追加）"
    # 定位 §六 分区表格的末行（以 `| 54 |` 开头）
    lines = text.split("\n")
    idx = None
    for i, ln in enumerate(lines):
        if ln.startswith("| 54 |"):
            idx = i
    assert idx is not None, "未找到 §六 表格末行（| 54 |）"
    lines.insert(idx + 1, ROW)
    new = "\n".join(lines)

    if dry:
        print("DRY 将插入 §六 登记行（位置：第 %d 行后）" % (idx + 1))
        return 0
    data = new.replace("\n", nl).encode("utf-8")
    tmp = P + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, P)
    print("已追加 §六 登记行（| 55 |）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
