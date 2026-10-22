#!/usr/bin/env python3
"""check_no_brand_refs.py — 品牌字面量零命中守卫（W836·N2「归档检测器复活到活面」）

为什么有这个东西（W812/W814 去品牌批留下的缺口）：

  W812/W814 两批把三枚品牌字面量从全仓清零，**验收方式是人工终扫**——仓内没有任何机器防线。
  与此同时，仓里唯一一处「品牌字面量扫描器」是归档件
  `archive/scripts/batches/misc/_audit_agentweb_baseline.py`：它在 W680 时被归档进
  `archive/scripts/batches/misc/`，而其 ROOT 仍按「脚本所在目录上溯两级」计算 ⇒ ROOT 落到
  `archive/scripts`（应为仓库根·上溯四级）⇒ 第 31 行读 `archive/scripts/xiyouji-agent-web/…`
  直接抛错，**第 110 行的品牌扫描段根本不可达**。
  于是「品牌回归」在仓库里既无扫描器、也无机器防线：**后写的文档又把字面量带回来也没人拦**。
  本文件即该检测能力的**活面承接**（归档件按文档规范 §11.2 不回溯修改）。

三条设计纪律：

  ① **字面量不在本文件明文出现**（base64 编码存储·运行时解码）——禁令要求的是
     「全仓明文 0 命中」，守卫自身若明文写出被禁字面量就等于自己违规；编码后明文扫描仍为 0，
     而守卫依旧能检出回归。
  ② **fail-closed 且分流退出码**：0=零命中 · 1=有命中 · 2=判据未执行（字面量解码失败 /
     扫描面为空 / git 不可用）——「判据未执行」与「判定为红」语义不同，故不同码（沿用
     W816 引文门禁的 1/2 分流口径）。
  ③ **扫描面 = git 已跟踪文件**（含 `archive/**`）：未跟踪文件（AI 会话运行态目录、
     本地临时产物）不进判定面——它们既不入库也不构成仓库内容。

用法：
    py -3 scripts/check_no_brand_refs.py            # 全仓扫描（退出码 0/1/2）
    py -3 scripts/check_no_brand_refs.py --self-test  # 判据自检（合成样本·不碰真实仓）

豁免（逐条写明·不豁免即等于漏检）：
    archive/scripts/batches/misc/_audit_agentweb_baseline.py
        ——归档件本身即历史检测器快照，其模式串是禁令对象的历史留痕；本批已按「活面承接」
          移除该段的模式串（见该文件内的移除说明），故不再需要路径豁免。
"""
import base64
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# 三枚被禁品牌字面量（base64 编码·明文不出现在仓库内容中）。
# 追加/调整须同步更新 docs/00-导读/W批次编号对账表.md 的 W836 行与本文档自检样本。
_B64_BRANDS = [
    "Y29kZWJ1ZGR5",          # 枚 1（其子串形态一并命中·子串匹配即命中）
    "d29ya2J1ZGR5",          # 枚 2
    "Y29tYXRl",               # 枚 3
]

# 扫描面排除的目录名（相对仓库根·顶层）与扩展名
_SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", "coverage",
    "__pycache__", ".pytest_cache", ".ruff_cache", ".tsbuild",
}
_SKIP_SUFFIX = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz",
                ".woff", ".woff2", ".ttf", ".eot", ".mp3", ".mp4", ".wasm", ".db", ".sqlite")


def brand_patterns():
    """解码被禁字面量 → 小写正则片段列表。解码失败即抛（调用方须转成退出码 2）。"""
    out = []
    for b64 in _B64_BRANDS:
        raw = base64.b64decode(b64.encode("ascii")).decode("utf-8")
        if not raw.strip():
            raise ValueError("空字面量")
        out.append(raw.lower())
    return out


def scan_text(text, patterns):
    """返回命中的 (pattern, 命中片段) 列表（大小写不敏感·子串匹配）。"""
    low = text.lower()
    hits = []
    for pat in patterns:
        idx = low.find(pat)
        if idx >= 0:
            hits.append((pat, text[max(0, idx - 30): idx + len(pat) + 30].replace("\n", "\\n")))
    return hits


def tracked_files(root=ROOT):
    """git ls-files 的结果（已跟踪文件=仓库内容面）。git 不可用即抛。"""
    r = subprocess.run(["git", "-C", root, "ls-files"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError("git ls-files 失败：%s" % (r.stderr or "").strip()[:200])
    files = []
    for line in r.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        rel = line.replace("\\", "/")
        parts = rel.split("/")
        if any(p in _SKIP_DIRS for p in parts[:-1]):
            continue
        if rel.lower().endswith(_SKIP_SUFFIX):
            continue
        files.append(rel)
    return files


def scan_repo(root=ROOT):
    """全仓扫描 → (命中清单, 扫描文件数)。命中清单元素为 (相对路径, 片段)。"""
    patterns = brand_patterns()
    files = tracked_files(root)
    if not files:
        raise RuntimeError("扫描面为空（无已跟踪文件）·判据未执行")
    hits = []
    for rel in files:
        path = os.path.join(root, rel.replace("/", os.sep))
        try:
            with open(path, encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except OSError:
            continue
        for pat, snippet in scan_text(text, patterns):
            hits.append((rel, pat, snippet))
    return hits, len(files)


def _self_test():
    """判据自检（合成样本·不读真实仓）：正例须命中、反例须零命中、退出码须分流。"""
    fails = 0
    cases = 0

    def check(cond, note):
        nonlocal fails, cases
        cases += 1
        if not cond:
            fails += 1
        print("%s  %s" % ("OK  " if cond else "FAIL", note))

    patterns = brand_patterns()
    check(len(patterns) == 3, "字面量解码出 3 枚（%d）" % len(patterns))
    check(all(p == p.lower() and p.isascii() for p in patterns), "解码结果为小写 ASCII 字面量")

    # 正例：每枚字面量的大小写形态与词内嵌形态都必须命中
    # 探针**由解码结果在运行时派生**——若在此处硬编码探针串，本文件自身就带着明文字面量，
    # 守卫入库后会把自己判红（自指违规）。
    for pat in patterns:
        for probe in (pat, pat.upper(), pat.capitalize(), "a %scli b" % pat, "x%s" % pat):
            hit = scan_text("prefix %s suffix" % probe, patterns)
            check(bool(hit), "正例应命中：%s 的大小写/内嵌形态" % pat)

    # 反例：形近但不同的字面量、允许品牌、允许的中性标识一律不得命中
    for probe in ["claude", "Claude-compat", "旧厂商 Agent 品牌", "并行 Agent 会话", "主会话",
                  "codebud", "buddy", "workbud", "comat", "mate", "", "c0debuddy"]:
        hit = scan_text("prefix %s suffix" % probe, patterns)
        check(not hit, "反例不应命中：%r" % probe)

    # 退出码分流：判定为红=1；判据未执行=2
    check(_exit_code_for_hits(3) == 1, "有命中 → 退出码 1")
    check(_exit_code_for_hits(0) == 0, "零命中 → 退出码 0")
    check(_exit_code_for_error() == 2, "判据未执行 → 退出码 2")

    print("self-test: %d/%d 通过" % (cases - fails, cases))
    return 1 if fails else 0


def _exit_code_for_hits(n):
    return 1 if n else 0


def _exit_code_for_error():
    return 2


def main(argv):
    if "--self-test" in argv[1:]:
        return _self_test()
    root = ROOT
    try:
        hits, scanned = scan_repo(root)
    except Exception as exc:  # noqa: BLE001 — 判据未执行统一转退出码 2
        print("ERROR 判据未执行：%s" % exc)
        return _exit_code_for_error()
    if hits:
        print("FAIL 品牌字面量命中 %d 处（扫描 %d 个已跟踪文件）：" % (len(hits), scanned))
        for rel, _pat, snippet in hits[:40]:
            print("  %s :: %s" % (rel, snippet))
        if len(hits) > 40:
            print("  ……另有 %d 处未列" % (len(hits) - 40))
        return _exit_code_for_hits(len(hits))
    print("OK 品牌字面量零命中（扫描 %d 个已跟踪文件·含 archive/）" % scanned)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
