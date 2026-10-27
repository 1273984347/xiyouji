# -*- coding: utf-8 -*-
"""_w974_merge_retry.py — 合并「补出件 + 未出批次」为一个 json，一次调用出图

背景（W974 实际发生）：
  · batch1 index 4（黑熊精）首轮 err_code 451「The result is unavailable」⇒ 需补出
  · batch2 index 2 原为「虎力大仙」⇒ 该角色在 people 库无独立页面（只有「车迟国三国师」页）
    ⇒ 选题调整为「玉兔精」（people/玉兔精.html 存在且尚无题图），原图弃用（不下载）
  · batch3（4 张）尚未出图
⇒ 把 2 条补出 + 4 条 batch3 合成一个 6 条 json，一次调用完成（省一次远程调用往返）。

母版一致性：两条补出件的母版段直接从已生成的 batch json 中原样取出（**一字不改**）
⇒ 母版仍与 W953 母版逐字相同。

用法：py -3 scripts/_w974_merge_retry.py
输出：scripts/output/_w974_batch34.json（6 条）
"""
import io
import json
import os
import sys

REPO = r"D:\xiyouji"
OUT = os.path.join(REPO, "scripts", "output")

# (源 batch json, 1-based index, 说明)
PICKS = [
    ("_w974_batch1.json", 4, "补出：黑熊精（首轮 err_code 451）"),
    ("_w974_batch2.json", 2, "替换：虎力大仙 → 玉兔精（people 库无虎力大仙独立页）"),
]
EXTRA = "_w974_batch3.json"          # 整批并入（狮驼岭 / 通天河 / 盘丝洞 / 无底洞）


def main() -> int:
    reqs = []
    for fn, idx, note in PICKS:
        p = os.path.join(OUT, fn)
        data = json.load(io.open(p, encoding="utf-8"))
        r = data["requests"][idx - 1]
        masters = {x["prompt"].split("主体：")[0] for x in data["requests"]}
        if len(masters) != 1:
            print("FATAL %s 母版不一致" % fn)
            return 2
        master = data["requests"][0]["prompt"].split("主体：")[0]
        if r["prompt"].split("主体：")[0] != master:
            print("FATAL %s index %d 母版与其余条目不一致" % (fn, idx))
            return 2
        reqs.append(r)
        print("并入：%-38s ← %s index %d（%s）" % (r["output_file"], fn, idx, note))

    p3 = os.path.join(OUT, EXTRA)
    data3 = json.load(io.open(p3, encoding="utf-8"))
    for r in data3["requests"]:
        reqs.append(r)
        print("并入：%-38s ← %s" % (r["output_file"], EXTRA))

    # 断言：批内母版逐字一致 + 与 W953 母版逐字相同
    masters = {r["prompt"].split("主体：")[0] for r in reqs}
    if len(masters) != 1:
        print("FATAL 合并批母版不一致")
        return 2
    ref = json.load(io.open(os.path.join(OUT, "_w953_batch1.json"), encoding="utf-8"))
    w953 = ref["requests"][0]["prompt"].split("主体：")[0]
    if list(masters)[0] != w953:
        print("FATAL 合并批母版与 W953 不逐字相同")
        return 2
    # 断言：输出文件互不重复
    names = [r["output_file"] for r in reqs]
    if len(set(names)) != len(names):
        print("FATAL 输出文件名重复")
        return 2

    dst = os.path.join(OUT, "_w974_batch34.json")
    io.open(dst, "w", encoding="utf-8", newline="\n").write(
        json.dumps({"requests": reqs}, ensure_ascii=False, indent=2))
    print("\n写出 %s（%d 条）· 母版 %d 字符与 W953 逐字相同" % (
        os.path.basename(dst), len(reqs), len(w953)))
    for r in reqs:
        print("  - " + r["output_file"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
