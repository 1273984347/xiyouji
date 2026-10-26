# -*- coding: utf-8 -*-
"""_w974_make_retry.py — 按失败 index 从已生成的 batch json 抽出重出件

用法：py -3 scripts/_w974_make_retry.py <batchN> <index1based> [out.json]

背景：W974 batch1 首轮 3/4 成功·index 3（黑熊精）返回 err_code 451「The result is unavailable」
⇒ 从已生成的 batch json 中原样抽出该条（母版与 SUBJECT 段**一字不改**·只重试生成）
⇒ 重出件的母版仍与 W953 逐字相同（母版一致性不受重出影响）。
"""
import io
import json
import os
import sys

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")


def main(argv):
    if len(argv) < 2:
        print("用法: py -3 scripts/_w974_make_retry.py <batchN> <index1based> [out.json]")
        return 2
    batch = int(argv[0])
    idx = int(argv[1]) - 1
    src = os.path.join(OUT, "_w974_batch%d.json" % batch)
    dst = os.path.join(OUT, argv[2]) if len(argv) > 2 else os.path.join(
        OUT, "_w974_retry_b%d_i%d.json" % (batch, idx + 1))
    data = json.load(io.open(src, encoding="utf-8"))
    reqs = data["requests"]
    if idx < 0 or idx >= len(reqs):
        print("FATAL index 越界：%d（该批共 %d 条）" % (idx + 1, len(reqs)))
        return 2
    one = {"requests": [reqs[idx]]}
    io.open(dst, "w", encoding="utf-8", newline="\n").write(
        json.dumps(one, ensure_ascii=False, indent=2))
    print("抽出重出件：%s ← batch%d index %d（%s）" % (
        os.path.basename(dst), batch, idx + 1, reqs[idx]["output_file"]))
    print("母版段长度 = %d 字符（与 W953 母版同源）" % len(
        reqs[idx]["prompt"].split("主体：")[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
