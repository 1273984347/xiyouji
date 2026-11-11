#!/usr/bin/env python3
"""check_lfs_text_purity.py — 文本文件不得被 LFS 托管（W1214 立·PR #171 CI 红灯根因判据）

为什么存在（W1214 实证）
--------------------------
W1209 做 LFS 迁移时给 assets/promo/** 写了 filter=lfs 规则，migrate 自动追加的
「**/*.md !text -filter -merge -diff」排除行被同批**整行删除**（理由：!text 压制 W993 立的
LF 规范化、-diff 让 md 被当二进制）⇒ **filter/merge 的排除语义随之消失** ⇒ 此后凡被
git add 的 assets/promo 下文本文件都走 LFS clean filter ⇒ 落成 LFS 指针（实测 8 md + 2 html）。

后果链条（本地绿 / CI 红）：
  CI 的 actions/checkout 默认**不拉 LFS 真身** ⇒ 工作树是指针文本
  ⇒ 第 45 槽 parse_index(指针) = None
  ⇒ C2「INDEX.md 结构不合生成器模板」× 6 目录
  ⇒ Delivery Gate 红 ⇒ required check 未过 ⇒ PR 硬拦。
  本地不红是因为 git lfs checkout 已把工作树恢复成真身 ⇒ 读磁盘永远读不到指针。

判据口径（**索引 blob**，不是工作树文件）
----------------------------------------
实算对象取 Git 索引里的 blob：索引 = 已跟踪 + 已暂存新增 = 将要入库的内容 = CI 干净检出的
内容。若读工作树文件，本地恒读真身 ⇒ 判据本地恒绿 ⇒ 抓不到「已入库的指针」⇒ 只能等 CI 报红。
⇒ 本判据**本地即可提前发现**。

用法：
    python scripts/check_lfs_text_purity.py --gate      # 门禁模式（默认）
    python scripts/check_lfs_text_purity.py --self-test  # 注入式自测（合成 git 仓·不触真仓）

退出码：0 全过；1 有 FAIL；2 参数/环境错误（git 不可用 ⇒ fail-closed）。

挂载位（W1214 定·不改动管控脚本 verify_delivery.py）：
  ① 第 45 槽 C5 子项（scripts/check_folder_docs.py）—— 目录文档层，Delivery Gate 必跑 ⇒ 拦合并；
  ② scripts/ci_sim.py GATES —— 全仓层，CI Sim job 必跑（不拦合并，但留 CI 证据）；
  ③ 挂第 72 槽（verify_delivery.py 注册表）须用户批准（规则 10）⇒ 本批不做，登记待办。
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MARKER = "---- LFS 文本纯净性："

# LFS 指针文件的签名行（git-lfs 规范固定首行）
POINTER_SIGNATURE = b"version https://git-lfs.github.com/spec/v1"

# 指针文件恒为小体量（实测 130 B）；超过此值的不可能是指针 ⇒ 批量读内容前先按体量筛
POINTER_MAX_BYTES = 512

# 文本类扩展名白名单：这些扩展名的文件**必须**是可直接读的普通 blob（审计面依赖内容 diff，
# 门禁依赖内容解析，CI 无 LFS 真身时指针内容不可用）。二进制媒体（png/jpg/webp/pdf/zip…）
# 留在 LFS 是**正确**用法，不在本判据范围。
TEXT_EXTS = frozenset(
    {
        ".md", ".markdown", ".mdx",
        ".html", ".htm", ".xml", ".svg",
        ".txt", ".csv", ".tsv",
        ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
        ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
        ".css", ".scss", ".less",
        ".sh", ".bash", ".ps1", ".bat", ".cmd",
        ".sql", ".rst", ".tex",
    }
)


def is_pointer_bytes(data: bytes) -> bool:
    """是否 LFS 指针内容（首行即签名）。纯函数·单测直接钉住。"""
    return data.startswith(POINTER_SIGNATURE)


def is_text_path(path: str) -> bool:
    """路径是否属文本类扩展名。纯函数·单测直接钉住。"""
    return os.path.splitext(path)[1].lower() in TEXT_EXTS


def _git_bytes(root: str, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", root, *args],
        capture_output=True,
        check=False,
    ).stdout


def index_entries(root: str) -> list[tuple[str, str]]:
    """索引条目 → [(blob_oid, rel_path)]（POSIX 分隔·相对仓根）。"""
    raw = _git_bytes(root, "ls-files", "-s", "-z")
    out: list[tuple[str, str]] = []
    for rec in raw.split(b"\0"):
        if not rec:
            continue
        head, _, path = rec.partition(b"\t")
        parts = head.split()
        if len(parts) < 2:
            continue
        out.append((parts[1].decode("ascii"), path.decode("utf-8", errors="replace")))
    return out


def _blob_sizes(root: str, oids: list[str]) -> dict[str, int]:
    """批量取 blob 体量（一次 --batch-check）。"""
    if not oids:
        return {}
    payload = ("\n".join(oids) + "\n").encode("ascii")
    proc = subprocess.run(
        ["git", "-C", root, "cat-file", "--batch-check"],
        input=payload,
        capture_output=True,
        check=False,
    )
    sizes: dict[str, int] = {}
    for line in proc.stdout.decode("utf-8", errors="replace").splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[1] == "blob":
            try:
                sizes[parts[0]] = int(parts[2])
            except ValueError:
                continue
    return sizes


def _blob_batch(root: str, oids: list[str]) -> dict[str, bytes]:
    """一次 --batch 读多个 blob。

    逐个起子进程（git cat-file blob <oid>）会把第 45 槽拖到 30 s+（实测 32.6 s）
    ⇒ 必须批量：一次 --batch-check 取体量筛小件，再一次 --batch 取内容。
    """
    if not oids:
        return {}
    payload = ("\n".join(oids) + "\n").encode("ascii")
    proc = subprocess.run(
        ["git", "-C", root, "cat-file", "--batch"],
        input=payload,
        capture_output=True,
        check=False,
    )
    out = proc.stdout
    res: dict[str, bytes] = {}
    pos = 0
    for _ in oids:
        nl = out.find(b"\n", pos)
        if nl < 0:
            break
        header = out[pos:nl].decode("ascii", errors="replace").split()
        pos = nl + 1
        if len(header) < 3:
            continue
        try:
            size = int(header[2])
        except ValueError:
            continue
        if header[1] != "blob":
            pos += size + 1
            continue
        res[header[0]] = out[pos:pos + size]
        pos += size + 1
    return res


def scan_index_text_pointers(root: str | None = None) -> tuple[int, list[str]]:
    """扫描索引里被 LFS 托管的文本文件。

    返回 (文本文件总数, 指针文件相对路径列表·已排序)。
    git 不可用时抛 RuntimeError（调用方须 fail-closed⇒ exit 2，不得 fail-open）。
    """
    base = root or ROOT
    entries = index_entries(base)
    if not entries:
        proc = subprocess.run(["git", "-C", base, "ls-files"], capture_output=True, check=False)
        if proc.returncode != 0:
            raise RuntimeError("git 不可用（ls-files rc=%d）" % proc.returncode)
    text_entries = [(oid, path) for oid, path in entries if is_text_path(path)]
    sizes = _blob_sizes(base, [oid for oid, _ in text_entries])
    small = [(oid, path) for oid, path in text_entries
             if sizes.get(oid) is not None and sizes[oid] <= POINTER_MAX_BYTES]
    contents = _blob_batch(base, [oid for oid, _ in small])
    bad = [path for oid, path in small if is_pointer_bytes(contents.get(oid, b""))]
    return len(text_entries), sorted(bad)


def summary_line(n_fail: int, n_text: int, bad: list[str]) -> str:
    """门禁汇总行（失败项并入本行·W1212 口径：CI 侧只看得见 marker 行）。"""
    detail = ""
    if bad:
        detail = "· 失败项：%s" % (" ｜ ".join(bad[:5]))
        if len(bad) > 5:
            detail += "（共 %d 条·余 %d 条见 stdout）" % (len(bad), len(bad) - 5)
    return "%s%d FAIL / %d 文本文件%s----" % (MARKER, n_fail, n_text, detail)


def run_gate() -> int:
    try:
        n_text, bad = scan_index_text_pointers()
    except RuntimeError as e:
        print("FAIL git 不可用（LFS 文本纯净性判据不可执行·fail-closed）：%s" % e)
        return 2
    for p in bad:
        print("FAIL 被 LFS 托管的文本文件（CI 无 LFS 真身时不可读）：%s" % p)
    print(summary_line(len(bad), n_text, bad))
    return 1 if bad else 0


def _self_test() -> int:
    """注入式自测：合成 git 仓（1 普通 md + 1 指针形态 md）⇒ 判据须只命中指针那个。"""
    import shutil
    import tempfile

    base = tempfile.mkdtemp(prefix="lfs_txt_selftest_")
    ok = False
    try:
        subprocess.run(["git", "init", "-q"], cwd=base, check=True)
        with open(os.path.join(base, "plain.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write("# 普通文本\n")
        with open(os.path.join(base, "pointer.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write(POINTER_SIGNATURE.decode("ascii") + "\noid sha256:" + "0" * 64 + "\nsize 42\n")
        with open(os.path.join(base, "pic.png"), "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")
        subprocess.run(["git", "-C", base, "add", "-A"], check=True)
        subprocess.run(
            ["git", "-C", base, "-c", "user.name=t", "-c", "user.email=t@example.com",
             "commit", "-q", "-m", "synth"],
            check=True,
        )
        n_text, bad = scan_index_text_pointers(base)
        ok = (bad == ["pointer.md"]) and n_text == 2
        print("合成仓扫描：文本文件 %d 个·命中 %r ⇒ %s" % (n_text, bad, "PASS" if ok else "FAIL"))
    except Exception as e:  # pragma: no cover - 自测环境异常
        print("self-test 异常：%r" % (e,))
        ok = False
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print("%sself-test：%s ----" % (MARKER, "全过" if ok else "有红"))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="LFS 文本纯净性门禁（W1214）")
    ap.add_argument("--gate", action="store_true", help="门禁模式（默认）")
    ap.add_argument("--self-test", action="store_true", help="注入式自测（合成 git 仓）")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    return run_gate()


if __name__ == "__main__":
    sys.exit(main())
