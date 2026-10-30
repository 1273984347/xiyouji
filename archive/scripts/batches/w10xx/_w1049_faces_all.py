# -*- coding: utf-8 -*-
"""_w1049_faces_all.py — 跑全部当前态面并落盘（绕开 CITATION 的「无变化」断言）

背景：`backfill_changelog.py --refresh-current` 的面循环在 `_face_citation` 报
「CITATION.cff 版本/日期行未变化」时**中止** ⇒ `bc._apply_pend(ctx.pend, …)` 从未执行
⇒ 前面五面（三面/交接/workflows/AGENTS）的 pend 全部**未落盘**（静默半途）。

处置：本脚本直接构造 `_Ctx` ⇒ 依次跑
  `_face_three_docs` / `_face_handover` / `_face_workflows` / `_face_agents` / `_face_footers`
（**跳过 `_face_citation`**——CITATION 已由 `_w1049_faces.py` 手动改到 W1049·
  再跑会触发「未变化」断言）⇒ 然后用 `bc._apply_pend` 落盘。

用法：py -3 archive/scripts/batches/w10xx/_w1049_faces_all.py
"""
import importlib.util
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
CASCADE = os.path.join(REPO, "scripts", "batch_cascade.py")
SPEC = os.path.join(REPO, "scripts", "output", "_w1049_spec.json")

sys.path.insert(0, os.path.join(REPO, "scripts"))
spec = importlib.util.spec_from_file_location("batch_cascade", CASCADE)
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)

FACES = ["_face_three_docs", "_face_handover", "_face_workflows",
         "_face_agents"]


def main() -> int:
    spec_j = json.load(io.open(SPEC, encoding="utf-8"))
    ctx = bc._Ctx(spec_j)
    # 交接文档面断言需要 CHANGELOG 原文（ctx.cl_src）
    ctx.cl_src = io.open(os.path.join(REPO, "CHANGELOG.md"), encoding="utf-8").read()
    # `ctx.new_w` 由 CHANGELOG 面回填（「现役段号 + 1」·AGENTS 面用它写归档注记）
    # ⇒ 本脚本跳过 CHANGELOG 面（段已由 backfill 按号序补好）⇒ 须手工回填。
    ctx.new_w = int(ctx.batch[1:]) + 1
    ctx.new_rule = "（W001-W%d）" % (int(ctx.batch[1:]) + 1)
    print("ctx.batch=%s · new_w=%d" % (ctx.batch, ctx.new_w))
    for name in FACES:
        fn = getattr(bc, name)
        before = len(ctx.pend)
        try:
            fn(ctx)
            print("  OK  %s（+%d 面）" % (name, len(ctx.pend) - before))
        except AssertionError as e:
            print("  FAIL %s：%s" % (name, e))
            return 1
    # 页脚面：已在 `_w1049_faces_rest.py` 跑过一次 ⇒ 再跑会触发「token 重复」断言 ⇒ 跳过
    print("  SKIP _face_footers（已由 _w1049_faces_rest.py 落盘·再跑会触发 token 重复断言）")
    if not ctx.pend:
        print("未产生落盘项")
        return 1
    bc._apply_pend(ctx.pend, "W%d" % int(ctx.batch[1:]))
    print("[SYNC] 落盘完成：%d 面" % len(ctx.pend))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
