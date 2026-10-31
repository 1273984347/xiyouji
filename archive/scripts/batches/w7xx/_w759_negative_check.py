"""W759 负样本：脚注滚动切分断言防回归验证。

判据锚定真实命令体（W757 教训：只做存在性断言会假绿）——
变异真实 AGENTS.md 脚注制造「切分边界重复号」夹具，跑 batch_cascade dry-run，
断言其以「滚动切分乱序」失败；随后字节级恢复原状并断言恢复无损。
阳性对照：未变异 dry-run 必须十面全过（exit 0）。

运行：python scripts/output/_w759_negative_check.py
"""
import subprocess
import sys

AGENTS = "AGENTS.md"
SPEC = "scripts/output/_w759_spec.json"
orig = open(AGENTS, "rb").read()


def run_cascade():
    return subprocess.run(
        [sys.executable, "scripts/batch_cascade.py", "--spec", SPEC],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


fails = []
try:
    # ---- 负样本 1：切分边界重复号（W754→W751 造有序重复 [751,751,755,756,758]）----
    text = orig.decode("utf-8")
    # 仅变异脚注行内的条目号（该形态在脚注行内唯一——「2026-10-16（W754）」条目头）
    bad = text.replace("；2026-10-16（W754）", "；2026-10-16（W751）", 1)
    assert bad != text, "夹具注入失败：未找到 W754 条目锚"
    open(AGENTS, "wb").write(bad.encode("utf-8"))
    r = run_cascade()
    combined = (r.stdout or "") + (r.stderr or "")
    if r.returncode == 0:
        fails.append("负样本1：重复号夹具下 cascade 意外通过（防线假绿）")
    elif "滚动切分乱序" not in combined:
        fails.append("负样本1：失败但非目标断言拦截——%s" % combined[-300:])
    else:
        print("OK  负样本1：切分边界重复号 → 滚动切分乱序（exit %d）" % r.returncode)

    # ---- 阳性对照：恢复原状后 dry-run 必须全过 ----
    open(AGENTS, "wb").write(orig)
    r2 = run_cascade()
    if r2.returncode != 0:
        fails.append("阳性对照：未变异 dry-run 失败——%s" % ((r2.stdout or "") + (r2.stderr or ""))[-300:])
    else:
        print("OK  阳性对照：未变异 dry-run 十面全过（修复代码真路径就绪）")
finally:
    # ---- 字节级恢复（无论成败）----
    open(AGENTS, "wb").write(orig)

if open(AGENTS, "rb").read() != orig:
    fails.append("恢复断言失败：AGENTS.md 字节级不等于原状")

if fails:
    for f in fails:
        print("FAIL " + f)
    sys.exit(1)
print("OK  恢复断言：AGENTS.md 字节级原状")
print("==== W759 负样本 真防线 1/1 + 阳性对照 1/1 + 恢复无损 ====")
