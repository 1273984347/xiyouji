#!/usr/bin/env python3
"""batch_spec.py — 级联 spec 的唯一解析入口（W1009·两处重复实现合并）

## 为什么要有这个模块

「本批应动哪些文件」被两次实现过：`safe_commit._spec_paths`（W1006）与
`check_commit_scope.spec_paths_for`（W1007）。W1007 自查时踩到 `cells[1]` 与 `cells[0]`
的分歧（spec 行形如 `| 路径 | W#### | 说明 |`，去壳后**第一格才是路径**）——
一处修好、另一处还错，是典型的「同一判据两处实现」风险。
本模块把它收敛成单一实现，两处改为调用。

## 口径

- spec 为 JSON，字段 `file_index_rows` 是 markdown 表行列表；
- 每行去首尾 `|` 后按 `|` 切格，**第 1 格 = 仓库相对路径**；
- 跳过表头（`文件`）、分隔行（`|---|---|`）、空行、空格；
- 路径统一 `/`，去重后排序返回（稳定顺序便于比对与单测）。
"""
from __future__ import annotations

import json
import re

HEADER_CELLS = {"文件", ""}
SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")   # markdown 表分隔行 |---|---|


def paths_from_rows(rows):
    """markdown 表行列表 → 路径列表（去重·排序）。纯函数。

    W1167：入口即校验路径非 git 八进制转义乱码（判据实现见 assert_clean_rows）——本函数是
    第 51 槽与 safe_commit 的共同取数面，乱码路径在此静默通过即等于「应动全集」失真。
    """
    assert_clean_rows(rows)
    out = set()
    for row in rows or []:
        cells = [c.strip() for c in str(row).strip().strip("|").split("|")]
        if not cells or cells[0] in HEADER_CELLS or SEPARATOR_RE.match(cells[0]):
            continue
        out.add(cells[0].replace("\\", "/"))
    return sorted(out)


# W1139 立式：目录分组行——「<目录>/（<N> 件）」第 1 格声明该目录子树为应动全集成员。
# 动因：巨批（616 页同族改动）逐文件行把 file-index 段顶破 256KiB 体积窗（W1139 实测
# 618 行 = +74KB），且逐行说明为零信息密度重复串。分组行由 spec 权威承载、
# cascade/rebuild 写段时原样透传（单一事实源不变），第 51 槽覆盖判定按子树展开。
_DIR_GROUP_RE = re.compile(r"^(.+)/（\d+ 件）$")


def groups_from_rows(rows):
    """markdown 表行列表 → 目录分组前缀列表（去重·排序）。纯函数。"""
    out = set()
    for row in rows or []:
        cells = [c.strip() for c in str(row).strip().strip("|").split("|")]
        if not cells or cells[0] in HEADER_CELLS or SEPARATOR_RE.match(cells[0]):
            continue
        m = _DIR_GROUP_RE.match(cells[0])
        if m:
            out.add(m.group(1).replace("\\", "/"))
    return sorted(set(out))


def covers(spec_rows, staged):
    """group-aware 覆盖判定：staged ⊆（精确路径 ∪ 分组目录子树）。纯函数。

    返回 (ok, extra)：extra = 未被任何精确路径或分组子树覆盖的 staged 路径（排序）。
    判据强度：分组只按**显式声明的目录前缀**覆盖子树（P2-2 语义声明：分组行 = **子树级
    声明**·含递归——故分组形态 spec 须由受信写入侧生成，禁手搓）；未声明路径一律进 extra。
    """
    exact = set(paths_from_rows(spec_rows))
    groups = groups_from_rows(spec_rows)
    extra = []
    for p in sorted({x.replace("\\", "/") for x in staged or []}):
        if p in exact:
            continue
        if any(p == g or p.startswith(g + "/") for g in groups):
            continue
        extra.append(p)
    return (not extra), sorted(extra)


def spec_paths_from_spec(spec):
    """spec dict → 路径列表。"""
    return paths_from_rows((spec or {}).get("file_index_rows") or [])


def load_spec(path):
    """读 spec JSON。抛 OSError / ValueError，由调用方决定 fail-closed 口径。"""
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def spec_paths(path):
    """路径 → 路径列表（读文件 + 解析）。"""
    return spec_paths_from_spec(load_spec(path))


# W1142 立式（体积矛盾根修·铁律 15）：登记面（file-index 段）与应动全集（spec）职责分工——
# spec 恒全量逐行（第 51 槽精确权威·不受体积窗管）；file-index 段由写入侧在行数超阈值时
# 自动转「目录分组行」（可导航性保留·每文件路径集由 spec 权威承载）。阈值取 200：
# W1139 实测 861 行段 ≈ +74KB（两巨段即顶破 256KiB），200 行 ≈ 17KB 为安全密度。
FI_SEGMENT_GROUP_THRESHOLD = 200

# W1167 实证坑（铁律 15 机制修法）：`git status --porcelain`（非 -z）对非 ASCII 路径输出
# 八进制转义，且 **加 core.quotePath=false 也照转**——取数面必须走 -z（仓内既有解法
# check_doc_sync._git_status_z）。转义路径一旦进 spec，级联会把「docs/00-/345/257/274/…」
# 这类乱码目录写进 file-index 登记面：目录不存在 ⇒ collect_paths 静默丢弃 ⇒ 第 51 槽
# 「应动全集」与登记面双双失真，且全程零红灯。故在唯一写入口 fail-closed，而不是靠人记得。
# 形态：git 的 `\346\211\271` 经 replace("\\","/") 后成 `/346/211/271`，UTF-8 续节字节
# 落在 0x80-0xBF（八进制 200-277），故**不能要求连号 3xx**——那正是首版守卫自己的漏判形态。
# 段数下限取 3（一个 CJK 字=3 字节=3 段）：取 2 会把 `photos/200/301/x.png` 这类
# 真数字目录误判为乱码，取 3 后此类路径放行（守卫误伤同样会让正常批卡死在收官链）。
MANGLED_PATH_RE = re.compile(r"(?:^|/)(?:[0-7]{3})(?:/[0-7]{3}){2,}(?:/|$)")


def assert_clean_rows(rows, where="file_index_rows"):
    """spec 行的路径格禁含八进制转义乱码；命中即抛（不静默降级为「少几行登记」）。"""
    bad = []
    for r in rows or []:
        cells = [c.strip() for c in str(r).strip().strip("|").split("|")]
        path = cells[0] if cells else ""
        if MANGLED_PATH_RE.search(path):
            bad.append(path)
    if bad:
        raise ValueError(
            "spec %s 有 %d 行路径是 git 八进制转义乱码（取数面未走 `git status --porcelain -z`），"
            "样例：%s" % (where, len(bad), bad[0][:80])
        )


def fi_group_rows(rows, batch):
    """巨批段行分组：行数 > 阈值 → 按目录分组行；阈值内原样返回。纯函数。

    分组行形态与手工压缩登记式一致（「<目录>/（<N> 件）」·covers 已 group-aware）；
    说明列取该目录内首行说明截断（登记面可导航即可·细节在 spec/CHANGELOG）。
    """
    rows = list(rows or [])
    assert_clean_rows(rows)
    if len(rows) <= FI_SEGMENT_GROUP_THRESHOLD:
        return rows
    from collections import Counter

    dirs = Counter()
    note = {}
    exact_no_slash = []  # W1142（P1-3 根修）：无斜杠根级文件不参与分组——「AGENTS.md/（1 件）」
    # 是文件伪装目录（os.walk 对文件零产出 → collect_paths 静默丢弃；covers 单文件获子树
    # 语义 → 代提防线失效）。保留为精确行。
    for r in rows:
        cells = [c.strip() for c in str(r).strip().strip("|").split("|")]
        path = cells[0] if cells else ""
        if "/" not in path:
            exact_no_slash.append(str(r).strip())
            continue
        d = path.rsplit("/", 1)[0]
        dirs[d] += 1
        note.setdefault(d, (cells[2] if len(cells) > 2 else "")[:40])
    grouped = ["| %s/（%d 件） | %s | %s |" % (d, c, batch, note[d])
               for d, c in sorted(dirs.items())]
    return grouped + exact_no_slash
