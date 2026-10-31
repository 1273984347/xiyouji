# -*- coding: utf-8 -*-
"""_w1049_faces_rest.py — 跑完剩余当前态面（footers + file-index）

背景：`backfill_changelog.py --refresh-current` 在 CITATION 面报「版本/日期行未变化」
⇒ 因为我已用 `_w1049_faces.py` 把 CITATION 手动改到 W1049 ⇒ 级联再跑就「无变化」⇒
其 fail-closed 断言拦下（该断言本意是防静默失配·此处属**已完成**情形）。
⇒ 本脚本直接调用 batch_cascade 的 `_face_footers` 与 `_face_file_index` 两个面函数
（跳过已完成的 CITATION 面）。

用法：py -3 archive/scripts/batches/w10xx/_w1049_faces_rest.py
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


def main() -> int:
    import json
    spec = json.load(io.open(SPEC, encoding="utf-8"))
    ctx = bc._Ctx(spec)
    print("ctx.batch=%s · desc=%s" % (ctx.batch, ctx.desc))
    for name in ("_face_footers", "_face_file_index"):
        fn = getattr(bc, name, None)
        assert fn is not None, "面函数不存在：%s" % name
        try:
            fn(ctx)
            print("OK    %s" % name)
        except AssertionError as e:
            print("FAIL  %s：%s" % (name, e))
            return 1
    # 落盘队列（面函数把内容放进 ctx.pend；nl 可能为 None ⇒ 按原文件行尾）
    for path, content, nl in ctx.pend:
        if nl is None:
            raw = open(path, "rb").read()
            nl = "\r\n" if b"\r\n" in raw else "\n"
        tmp = path + ".tmp"
        with open(tmp, "wb") as fh:
            fh.write(content.replace("\n", nl).encode("utf-8"))
        os.replace(tmp, path)
        print("  落盘：%s" % os.path.relpath(path, REPO).replace("\\", "/"))
    print("---- 剩余当前态面完成 ----")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
