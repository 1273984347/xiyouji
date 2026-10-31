# -*- coding: utf-8 -*-
"""_w984_retry.py — W984 单张重出修正器（通用·可复用）

用法：py -3 scripts/_w984_retry.py <stem> <batch号> "<旧文本>" "<新文本>" ...

流程：
  1. 在 scripts/_w984_make_prompts.py 中按**单行内短锚点**替换（字节级原子替换·断言命中数=1）
  2. 重跑 make_prompts（重建 3 个 batch json）
  3. 取出目标张的单条参数 → scripts/output/_w984_retry_<stem>.json
  4. 打印下一步命令（出图 / 下载 / 派生 / 判据）

纪律（来自 W952 教训）：
  · 锚点必须**逐字从原文复制**且取**单行内**片段——跨行 Python 字符串拼接会造成失配
  · 命中数 ≠ 1 ⇒ 立即中止且**不写盘**
  · 修正后必须重跑整批参数生成，避免新旧 prompt 混用
"""
import io
import json
import os
import subprocess
import sys

MK = os.path.join("scripts", "_w984_make_prompts.py")
OUT = os.path.join("scripts", "output")


def main(argv):
    if len(argv) < 4 or (len(argv) - 2) % 2 != 0:
        print("用法：py -3 scripts/_w984_retry.py <stem> <batch号1-3> <旧> <新> [<旧> <新> ...]")
        return 2
    stem = argv[0]
    batch_no = int(argv[1])
    pairs = [(argv[i], argv[i + 1]) for i in range(2, len(argv), 2)]

    raw = io.open(MK, "rb").read()
    for old, new in pairs:
        ob, nb = old.encode("utf-8"), new.encode("utf-8")
        n = raw.count(ob)
        if n != 1:
            print("ABORT  命中数 %d（期望 1）· 锚点：%s" % (n, old[:40]))
            return 2
        raw = raw.replace(ob, nb)
    tmp = MK + ".tmp"
    io.open(tmp, "wb").write(raw)
    os.replace(tmp, MK)
    print("make_prompts.py 已修正（%d 处）" % len(pairs))

    r = subprocess.run([sys.executable, MK], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print("ABORT  make_prompts 重跑失败 rc=%d\n%s" % (r.returncode, r.stderr[:400]))
        return 2
    print("参数重建：%s" % r.stdout.strip().splitlines()[0])

    bp = os.path.join(OUT, "_w984_batch%d.json" % batch_no)
    b = json.load(io.open(bp, encoding="utf-8"))
    target = "plate-line-%s.png" % stem
    hit = [it for it in b["requests"] if it["output_file"] == target]
    if len(hit) != 1:
        print("ABORT  batch%d 中未唯一命中 %s（命中 %d）" % (batch_no, target, len(hit)))
        return 2
    it = hit[0]
    for old, new in pairs:
        if new not in it["prompt"]:
            print("ABORT  修正点未进 prompt（%s）" % new[:30])
            return 2
    rp = os.path.join(OUT, "_w984_retry_%s.json" % stem)
    io.open(rp, "w", encoding="utf-8", newline="\n").write(
        json.dumps({"requests": [it]}, ensure_ascii=False, indent=2))
    print("单条重出参数：%s" % rp)
    print("\n下一步：")
    print("  mcode-tools connector call connector__matrix__generate_image --args-file %s" % rp)
    print("  （随后：写映射 → _w984_download.py → _w984_prepare.py → _w945_plates_verify.py）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
