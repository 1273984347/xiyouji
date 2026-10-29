"""gate_common.py — 门禁脚本公共骨架（W803 建 · 行为保持收敛）。

## 为什么有这个模块（W803 取证）

`scripts/check_*.py` 一族门禁脚本（第 32-37 槽等）在历史演进中各自内联了同一套骨架，
2026-10-19 实测重复形态：

  · `HERE = os.path.dirname(os.path.abspath(__file__))` + `ROOT = os.path.dirname(HERE)`
    —— 19 个根级脚本各写一遍；
  · 站点页面清单 `sorted(glob(site/data/*.html) + glob(site/*.html) + glob(site/en/*.html))`
    —— CSS/head 门禁各写一遍（其中 2 个是「data + en」二源变体）；
  · `open(f, encoding="utf-8", errors="replace").read()` —— 同上；
  · `<style>…</style>` 提取 + 「块起始行号 = `src[:m.start(1)].count("\\n") + 1`」
    —— CSS 门禁三件各写一遍；
  · 注入式自测的 fails 计数 + 逐例行 + `"---- 第 NN 门禁 self-test：%d/%d 通过 ----"`
    收尾行 + `return 1 if fails else 0` —— 多份逐字相同。

本模块即上述骨架的单一实现。设计红线（与 W761 `path_guard.py` 收敛 14 份内联守卫同款）：

  **只收敛重复，不改写任何既有语义** —— 所有输出的文案、字段、退出码属对外契约，
  收敛前后必须逐字节一致（对拍口径见 `docs/_templates/duipai/duipai.py`）。

## 公共 API

    ROOT / SCRIPTS_DIR / UTILS_DIR   仓库根、scripts/、scripts/utils/（绝对路径）
    read_text(path)                  UTF-8 容错读取（errors="replace"·扫描型门禁）
    read_text_strict(path)           UTF-8 严格读取（治理档门禁·编码异常即抛）
    relpath(path)                    仓库相对路径（历史 os.path.relpath(p, ROOT) 同义）
    site_pages(**sources)            站点页面清单（三源/二源可选·全局排序）
    iter_style_blocks(src)           [(style 块正文, 块起始行号)]（行号算法逐字保留）
    run_case_batch(...)              注入式自测跑批（统一逐例格式 + 收尾行 + 退出码）
    SelfTestTally                    逐例格式自定族复用的计数/收尾/退出码
    cli_main(check, selftest)        统一 CLI 分发（--self-test 走自测，否则只读校验）

## 使用形态

    from utils.gate_common import ROOT, read_text, relpath, site_pages

`python scripts/xxx.py` 直跑时 `sys.path[0]` 即 `scripts/`，故 `utils` 包可直接 import
（与 `scripts/utils/path_guard.py` 既有消费形态一致）。
"""
from __future__ import annotations

import glob
import os
import re
import sys
from collections.abc import Callable, Sequence
from typing import Any

# ---------------------------------------------------------------------------
# 路径常量
# ---------------------------------------------------------------------------
# 三级上溯：本文件 → scripts/utils/ → scripts/ → 仓库根。
# 用 abspath（不用 realpath）以与门禁历史内联写法逐字同义——含软链的机器上二者会分叉，
# 收敛不得夹带这层语义变化。

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(UTILS_DIR)
ROOT = os.path.dirname(SCRIPTS_DIR)

#: `<style …>…</style>` 提取口径（与各门禁历史内联正则逐字一致）
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
# INLINED 副本：由 inline_css.py 写入的标记注释与紧随其后的 <style> 配对。
# 这是识别「共享 CSS 副本」的**稳定契约**——判据不得依赖块内注释文本（如 "tokens.css —"）：
# 那类文本会被任何「剥离 CSS 注释」的动作静默抹掉（W1019 实证：剥注释后 228 页副本被
# 误判为页面私有块，token 覆盖率与动效门禁同时误报）。
INLINED_STYLE_RE = re.compile(
    r"<!--\s*INLINED CSS.*?-->\s*<style[^>]*>(.*?)</style>", re.S | re.I
)


# ---------------------------------------------------------------------------
# 读取与路径
# ---------------------------------------------------------------------------

def read_text(path: str) -> str:
    """按 UTF-8 容错读取文件（`errors="replace"`，与门禁历史内联写法一致）。

    容错而非抛错是刻意的：门禁要扫全站 800+ 页，单页编码异常不应中断整批扫描，
    而应以替换字符呈现、在判定阶段自然暴露。

    适用面：**扫描型**门禁（CSS/head 族——对象是站点产物，求「扫得完」）。
    治理档门禁（AGENTS/CLAUDE 族）读的是仓库自有 UTF-8 文件，编码异常应当立刻炸出来，
    请用 `read_text_strict()`——两种读取口径不可互替（W803 裁决）。
    """
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def read_text_strict(path: str) -> str:
    """按 UTF-8 严格读取文件（编码异常即抛 `UnicodeDecodeError`）。

    适用面：**治理档门禁**——读 `AGENTS.md` / `CLAUDE.md` / `verify_delivery.py` 这类
    仓库自有文件。这些文件若编码坏了，是必须立刻暴露的仓库事故，容错读取会把事故
    降级成「某个中文词没匹配上」的静默误判。
    """
    with open(path, encoding="utf-8") as f:
        return f.read()


def relpath(path: str) -> str:
    """返回相对仓库根的路径（历史 `os.path.relpath(p, ROOT)` 同义）。"""
    return os.path.relpath(path, ROOT)


# ---------------------------------------------------------------------------
# 站点页面清单
# ---------------------------------------------------------------------------

def site_pages(*, data: bool = True, root: bool = True, en: bool = True) -> list[str]:
    """收集站点页面清单，全局排序。

    与历史写法 `sorted(glob(A) + glob(B) + glob(C))` **同序**：`sorted()` 作用于拼接后的
    整体，故此处同样先拼接再整体排序。**不可**改成「逐源排序后拼接」——那会改变跨目录的
    相对顺序（如 `site/data/x.html` 与 `site/en/a.html` 的先后）。

    参数（按需取源；全 False 时返回空表）：
        data: 是否含 `site/data/*.html`（可视化页）
        root: 是否含 `site/*.html`（站点根页）
        en:   是否含 `site/en/*.html`（英文站）
    """
    parts: list[str] = []
    if data:
        parts += glob.glob(os.path.join(ROOT, "site", "data", "*.html"))
    if root:
        parts += glob.glob(os.path.join(ROOT, "site", "*.html"))
    if en:
        parts += glob.glob(os.path.join(ROOT, "site", "en", "*.html"))
    return sorted(parts)


def iter_style_blocks(src: str) -> list[tuple[str, int]]:
    """提取 `<style>` 块正文与块起始行号。

    行号算法与历史内联写法逐字一致：`src[:m.start(1)].count("\\n") + 1`，即块正文首行
    在全文件中的 1 基行号（各门禁据此打印 `文件:行号` 定位）。

    返回：
        [(块正文, 起始行号), …]，按出现顺序。
    """
    return [
        (m.group(1), src[: m.start(1)].count("\n") + 1)
        for m in STYLE_BLOCK_RE.finditer(src)
    ]


def iter_private_style_blocks(src: str) -> list[tuple[str, int]]:
    """页面**私有** `<style>` 块（跳过 INLINED tokens/system 副本），返回同 `iter_style_blocks`。

    判据取 `inline_css.py` 写入的 `<!-- INLINED CSS … -->` 标记与紧随 `<style>` 的配对，
    而非块内注释文本——后者会被「剥离 CSS 注释」静默破坏（见 INLINED_STYLE_RE 注释）。
    """
    inlined = {m.start(1) for m in INLINED_STYLE_RE.finditer(src)}
    return [
        (m.group(1), src[: m.start(1)].count("\n") + 1)
        for m in STYLE_BLOCK_RE.finditer(src)
        if m.start(1) not in inlined
    ]


# ---------------------------------------------------------------------------
# 注入式自测跑批
# ---------------------------------------------------------------------------

def run_case_batch(
    cases: Sequence[Any],
    evaluate: Callable[[Any], tuple[Any, Any]],
    label: str,
    *,
    got_text: Callable[[Any], str] = str,
    want_text: Callable[[Any], str] = str,
    line_format: str = "  %s %s（期望 %s）",
) -> int:
    """跑一批注入式自测用例，返回退出码（0 全过 / 1 有失败）。

    参数：
        cases:       用例序列，元素原样交给 `evaluate`（形态由各门禁自定）
        evaluate:    `(case) -> (got, want)`；`got == want` 即该例 PASS
        label:       收尾行标签，输出 `---- {label} self-test：{通过}/{总数} 通过 ----`
        got_text:    `got` 的渲染函数（默认 `str`；逐例行只打印期望值时用不到）
        want_text:   `want` 的渲染函数——各门禁期望值文案不同
                     （`"2 处"` / `"无违例"` / `"exit 0"` / `"missing=True"`），故由调用方提供
        line_format: 逐例输出格式，默认 `"  %s %s（期望 %s）"` = 状态、用例名、期望值

    说明：失败明细由各门禁自行追加打印——「明细行长什么样」属各门禁自有文案，
    不塞进公共层；本函数只负责计数、逐例状态行、收尾行与退出码。
    """
    fails = 0
    for case in cases:
        got, want = evaluate(case)
        ok = got == want
        if not ok:
            fails += 1
        print(line_format % ("PASS" if ok else "FAIL", case[0], want_text(want)))
    print("---- %s self-test：%d/%d 通过 ----" % (label, len(cases) - fails, len(cases)))
    return 1 if fails else 0


class SelfTestTally:
    """自测计数与收尾行（供逐例输出格式自定的门禁族复用）。

    适用形态：各门禁的判定函数签名与逐例输出差异较大（如需打印失败明细，或逐例只输出
    「状态 + 用例名」），无法套用 `run_case_batch` 的统一格式时，至少把「计数 → 收尾行 →
    退出码」这段逐字相同的逻辑收敛到此处。

        tally = SelfTestTally("第 41 门禁 AGENTS 分层完整性")
        for …:
            if not tally.add(ok):
                …  # 打印本门禁自有明细
        return tally.report()
    """

    def __init__(self, label: str) -> None:
        self.label = label
        self.total = 0
        self.fails = 0

    def add(self, ok: bool) -> bool:
        """登记一例结果，原样回传 `ok`。"""
        self.total += 1
        if not ok:
            self.fails += 1
        return ok

    @property
    def passed(self) -> int:
        return self.total - self.fails

    def report(self) -> int:
        """打印收尾行并返回退出码（0 全过 / 1 有失败）。"""
        print("---- %s self-test：%d/%d 通过 ----" % (self.label, self.passed, self.total))
        return 1 if self.fails else 0


# ---------------------------------------------------------------------------
# CLI 分发
# ---------------------------------------------------------------------------

def cli_main(run_check: Callable[[], int], run_self_test: Callable[[], int]) -> int:
    """门禁脚本统一的 CLI 分发：`--self-test` 走自测，否则走只读校验。

    这是门禁族用了最久、复制得最多的一段（`main()` 两分支 + `sys.exit(main())`），
    收敛在此以统一「CLI 形态」：**无参 = 只读校验，`--self-test` = 注入式自测**，
    其余参数一律忽略（与各门禁历史行为一致——它们只看 `sys.argv` 里有没有这个标记）。

    参数：
        run_check:      默认分支（无 `--self-test` 时调用）
        run_self_test:  `--self-test` 分支
    返回：
        两个分支各自的退出码，由调用方 `sys.exit(...)` 透传。
    """
    if "--self-test" in sys.argv:
        return run_self_test()
    return run_check()


__all__ = [
    "ROOT",
    "SCRIPTS_DIR",
    "INLINED_STYLE_RE",
    "STYLE_BLOCK_RE",
    "UTILS_DIR",
    "SelfTestTally",
    "cli_main",
    "iter_private_style_blocks",
    "iter_style_blocks",
    "read_text",
    "read_text_strict",
    "relpath",
    "run_case_batch",
    "site_pages",
]
