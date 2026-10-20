#!/usr/bin/env python3
"""gen_folder_docs.py — 为全仓目录补齐 index.md / README.md（W779 批·用户令「检查所有文件夹，添加 index.md REMADE.md STRUCTURE.md」）。

## 背景与范围（动工前实测 2026-10-18）

用户令「检查一下文件内所有文件夹，添加一下 index.md REMADE.md STRUCTURE.md」。三项裁决：

1. **REMADE.md = README.md 的误写**（用户确认·全仓 0 处先例）→ 本批补 README.md。
2. **STRUCTURE.md = 根级结构文档**：根目录已有 `STRUCTURE.md`（Reference 角色·目录树+说明表），
   按「单一事实源」原则（文档规范 §3）**不在每个子目录复制结构文档**；本脚本在每份生成文档中
   放一行指针指向根 STRUCTURE.md。目录级新增/约定变更仍只在根 STRUCTURE.md 登记（§11.5 骨架约束）。
3. **范围 = 245 个在管目录**（排除 node_modules/__pycache__/tmpe/_trash/构建产物/缓存等）。

## 定位分工（W779 重设计·消除 index/README 同文重复）

首版 406 个文件写完后 verify 全量暴露三处设计债，据此整改：

- **两文件定位不同**：`index.md` = 机器可读的**逐文件清单**（人/Agent 查「这里有什么文件」）；
  `README.md` = 人读的**目录导读**（这里装什么、怎么加新东西、约定是什么）。首版两者同文＝174 个
  目录纯重复，违反「单一事实源·禁止两处维护同一份清单」（文档规范 §3 判据）。
- **治理目录排除**：`docs/10-方法论沉淀/` 与 `docs/11-方案报告/` 由 check_index_health.py 第 17 门禁
  「方法论 README 双向覆盖」断言（目录 md ↔ README 索引链接差集 = 0）——它们的 README 是**治理档**，
  脚本生成会同时打破双向覆盖并把 `.md` 计数推高（report_docs 25→32·methodology_docs 24→25），
  引发第 31 门禁 C5d stats 漂移 FAIL。故这两棵树整体跳过（README 由治理流程人工维护·正是现状）。
- **docs/01-06 内容板块顶层跳过**（既有 README 是教学模板档·且三个门禁 iter 逻辑已按名排除顶层 README）。

## 内容形态（零链接门禁风险设计）

- **不放任何 Markdown 链接**（不含相对路径 []() 形态）——lint_links.py 第 6 门禁与 `--dir .`
  全仓口径都只校验链接；用反引号路径书写既无死链风险也满足「路径自解释」（文档规范 §4.1）。
- **不写会漂移的现役值**（文档规范 §4.9/§4.10·CLAUDE.md C4）——「生成时点实测 N 个文件」带
  时点限定，禁「当前共 N 篇」式裸聚合数字（第 31 门禁 C5c 形态）。
- **不触发第 18/19/20 门禁**：docs/01-06 顶层 README.md 被三个门禁按名排除；本脚本不向
  docs/01-06 顶层与 10/11 两棵治理树写任何文件。

## 用法

    python scripts/gen_folder_docs.py            # 写入缺失的 index.md / README.md
    python scripts/gen_folder_docs.py --dry-run  # 只报告将写哪些文件
    python scripts/gen_folder_docs.py --refresh  # 安全刷新陈旧生成物（「生成来源」标记判所有权·人工维护件自动跳过·W780）
    python scripts/gen_folder_docs.py --force    # 已存在的也按生成内容重写（含人工维护件·慎用）

退出码：0 成功；3 有目录写入失败（未中断整批）；2 参数/环境错误。
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 目录遍历排除（机器相关/不入库产物/缓存·按路径片段匹配·两侧均归一为 /frag/ 形态）
EXCLUDE_SUBSTR = (
    "node_modules",
    "__pycache__",
    ".pw-browsers",
    "_trash",
    "tmpe",
    ".cache",
    ".mimosa",
    ".pytest_cache",
    ".ruff_cache",
    ".review-tmp",
    "review-w760",
)
# 顶层目录排除（纯本地运行态·不入库也无内容导航价值）
EXCLUDE_TOP = set(EXCLUDE_SUBSTR) | {".git"}
# 构建/打包产物目录名（packaging/xiyouji-analysis/build · dist · *.egg-info·非源码面无导航价值）
EXCLUDE_SEGMENTS = {"build", "dist"}
EXCLUDE_SUFFIX = (".egg-info",)
# 建文档时跳过的文件名（自身/占位/.gitkeep）
SKIP_NAMES = {".gitkeep", "index.md", "INDEX.md", "README.md", "STRUCTURE.md"}
# 索引里列文件时的分类顺序（其余按扩展名归入「其他」）
EXT_GROUPS: list[tuple[str, set[str]]] = [
    ("Markdown 文档", {".md"}),
    ("HTML 页面", {".html", ".htm"}),
    ("Python 脚本", {".py"}),
    ("JavaScript / TypeScript", {".js", ".mjs", ".cjs", ".ts", ".tsx"}),
    ("数据与配置", {".json", ".jsonl", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".cff", ".txt", ".csv"}),
    ("样式与资源", {".css", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".otf", ".mp3", ".wav"}),
    ("文档产物", {".pdf", ".docx", ".xlsx", ".pptx"}),
]


def _is_excluded(abs_path: str) -> bool:
    rel = os.path.relpath(abs_path, ROOT).replace(os.sep, "/")
    top = rel.split("/", 1)[0]
    if top in EXCLUDE_TOP:
        return True
    # 按路径段匹配（防 "tmpe" 咬到无关词·只匹配完整目录名）
    parts = rel.split("/")
    if any(p in EXCLUDE_TOP for p in parts):
        return True
    # 构建产物段（build/ · dist/ · *.egg-info）
    if any(p in EXCLUDE_SEGMENTS or p.endswith(EXCLUDE_SUFFIX) for p in parts):
        return True
    # gitignored 目录（docs/S2-* · docs/_dev · scripts/screenshots 等）
    # —— 漏这层会让 index.md 被写进不入仓的目录（git add 也不会带上），
    # 且其清单会列名敏感路径（W779 首版实证 344 条）。
    if rel in _GITIGNORED_DIRS:
        return True
    return False


# 模块级缓存：gitignored 目录集合（scan_dirs 前算一次）
_GITIGNORED_DIRS: set[str] = set()


def _build_gitignored_dirs() -> set[str]:
    """用 `git status --porcelain --ignored` 之外的低成本途径：逐目录 check-ignore
    会慢（O(目录数) 次 subprocess），故用一次 `git ls-files --others --ignored
    --exclude-standard --directory` 拿**被忽略的目录**清单一轮算完。"""
    rels: set[str] = set()
    try:
        r = subprocess.run(
            ["git", "-c", "core.quotePath=false", "ls-files", "--others",
             "--ignored", "--exclude-standard", "--directory"],
            capture_output=True, timeout=120, cwd=ROOT,
        )
    except Exception:
        return set()
    if r.returncode != 0:
        return set()
    for ln in r.stdout.decode("utf-8", "replace").splitlines():
        s = ln.strip().strip('"').replace("\\", "/").rstrip("/")
        if s:
            rels.add(s)
    return rels


def scan_dirs() -> list[str]:
    """返回在管目录绝对路径（递归·排除见 EXCLUDE_*）。"""
    out = []
    for dirpath, dirnames, _filenames in os.walk(ROOT):
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in EXCLUDE_TOP and not _is_excluded(os.path.join(dirpath, d))
        )
        out.append(dirpath)
    return out


def list_files_raw_names(abs_dir: str) -> list[str]:
    """目录直属文件名（跳过占位/自身三类文档·不过滤 gitignored·供再过滤用）。"""
    try:
        names = os.listdir(abs_dir)
    except OSError:
        return []
    return [
        n for n in names
        if os.path.isfile(os.path.join(abs_dir, n)) and n not in SKIP_NAMES
    ]


def list_files(abs_dir: str) -> list[str]:
    """目录直属文件名（跳过占位/自身三类文档·跳过 gitignored 本地件）·排序稳定。

    gitignored 过滤是硬要求（W779 整改·首版实测 344 条）：`.gitignore` 排除的
    敏感/本地产物（S4 双盲件、`03-PRD-第28门禁…` 真名 PRD、`.env`、
    `SECURITY-AUDIT-*.password` 等）一旦被 index.md 列名并入库，等于把「不入仓」
    的路径本身公开——正是 W620/W650 两轮裁决要防的泄漏面。
    """
    names_all = list_files_raw_names(abs_dir)
    ignored = _gitignored_set(abs_dir, names_all)
    return [n for n in sorted(names_all) if n not in ignored]


def _kind_exists(abs_dir: str, kind: str) -> bool:
    """kind 是否已存在（大小写不敏感）——Windows 写 index.md 会覆盖已存在的 INDEX.md
    （实测 2026-10-18：NTFS 大小写不敏感·直接 open('w') 即整文件覆写），故必须判重，
    否则 S4-学术投稿 12 份 INDEX.md 与 docs/INDEX.md 会被幂等运行清空。"""
    return os.path.exists(os.path.join(abs_dir, kind)) or kind in list_files_raw(abs_dir)


def list_files_raw(abs_dir: str) -> set[str]:
    """目录直属文件名集合（含占位/自身三类·大小写判重专用）。"""
    try:
        names = os.listdir(abs_dir)
    except OSError:
        return set()
    return {n for n in names if os.path.isfile(os.path.join(abs_dir, n))}


def _gitignored_set(abs_dir: str, names: list[str], is_dir: bool = False) -> set[str]:
    """返回 names 中被 .gitignore 排除的名字集合（批查·git 不可用/异常 → 空集不阻断）。

    Windows 必须走 --stdin **字节流**（UTF-8）：text 模式 stdin 在 Windows 走 GBK，
    中文路径永不命中（scripts/lint_links.py filter_gitignored W699 同款踩坑修复）。

    两条实测口径修正（W779）：
    1. **目录判定必须带尾斜杠**——`git check-ignore` 对目录型规则要求路径以 `/` 结尾，
       `docs/S2-外部分享` rc=1（不命中）而 `docs/S2-外部分享/` rc=0（命中）。
    2. **stdout 行可能带 CRLF**——剥 `\r` 后再比对，否则集合永不命中。
    """
    if not names:
        return set()
    rel_dir = os.path.relpath(abs_dir, ROOT).replace(os.sep, "/")
    prefix = "" if rel_dir == "." else rel_dir + "/"
    # 目录查询带尾斜杠；文件查询不带
    rels = [(prefix + n + ("/" if is_dir else "")) for n in names]
    try:
        r = subprocess.run(
            ["git", "-c", "core.quotePath=false", "check-ignore", "--stdin"],
            input=("\n".join(rels) + "\n").encode("utf-8"),
            capture_output=True, timeout=60, cwd=ROOT,
        )
    except Exception:
        return set()
    if r.returncode not in (0, 1):  # 2=命令行错误·保守放行
        return set()
    ignored_rels: set[str] = set()
    for ln in r.stdout.decode("utf-8", "replace").splitlines():
        s = ln.strip().strip('"').replace("\\", "/").rstrip("/")
        s = re.sub(r"/{2,}", "/", s)
        if s:
            ignored_rels.add(s)
    # 归一化比对键（两侧都去尾斜杠）
    return {n for n in names if (prefix + n) in ignored_rels}


def _kind_exists(abs_dir: str, kind: str) -> bool:
    """kind 是否已存在（大小写不敏感）——Windows 写 index.md 会覆盖已存在的 INDEX.md
    （实测 2026-10-18：NTFS 大小写不敏感·直接 open('w') 即整文件覆写），故必须判重，
    否则 S4-学术投稿 12 份 INDEX.md 与 docs/INDEX.md 会被幂等运行清空。"""
    return os.path.exists(os.path.join(abs_dir, kind)) or kind in list_files_raw(abs_dir)


def list_subdirs(abs_dir: str) -> list[str]:
    """直属子目录名（排除：非目录 / EXCLUDE_TOP / gitignored 目录如 docs/S2-*）。"""
    try:
        names = os.listdir(abs_dir)
    except OSError:
        return []
    # 归一化比对：_gitignored_set 返回的是**名字**（去前缀），故用 n 直接判成员
    ignored_names = _gitignored_set(abs_dir, names, is_dir=True)
    out = [n for n in sorted(names)
           if os.path.isdir(os.path.join(abs_dir, n))
           and not _is_excluded(os.path.join(abs_dir, n))
           and n not in ignored_names]
    return out


def group_label(fname: str) -> str:
    ext = os.path.splitext(fname)[1].lower()
    for label, exts in EXT_GROUPS:
        if ext in exts:
            return label
    return "其他"


def rel_of(abs_dir: str) -> str:
    r = os.path.relpath(abs_dir, ROOT).replace(os.sep, "/")
    return "" if r == "." else r


# 治理目录整体跳过（含其下全部子目录）——生成器主循环与 check_folder_docs.py 新鲜度
# 门禁（第 45 槽）共用本判定（W780 自 main() 局部量提升模块级：单一事实源，两处维护即漂移）：
# - docs/10-方法论沉淀/：第 17 门禁「方法论 README 双向覆盖」断言（目录 md ↔ README 索引
#   链接差集=0）——脚本生成的 README 会同时打破双向覆盖并推高 methodology_docs 计数。
# - docs/11-方案报告/：同族·report_docs 是 stats 键（W737 建·该目录 README 是报告篇数
#   唯一权威）——W779 首版实证：脚本写入 3 个子目录 README/index 后 report_docs 25→32、
#   methodology_docs 24→25，第 31 门禁 C5d「stats 与磁盘实算漂移」当场 FAIL。
# - docs/01-06 内容板块顶层：既有 README 是教学模板档·且 check_frontmatter / check_glossary /
#   check_citations 的 iter 逻辑按名排除顶层 README（子目录不在三者扫描面）。
GOVERNED_SKIP = {
    "docs/10-方法论沉淀",
    "docs/11-方案报告",
    "docs/01-全书逐回解读",
    "docs/02-人物深度分析",
    "docs/03-主题与情节专题",
    "docs/04-文化与历史背景",
    "docs/05-诗词歌赋",
    "docs/06-个人随笔",
}


def in_scope(abs_dir: str) -> bool:
    """目录是否在生成器管辖内（治理树排除）。gen_folder_docs 主循环与
    check_folder_docs.py（第 45 槽）共用本判定——口径改动只改这一处。"""
    rel = rel_of(abs_dir)
    return not (rel in GOVERNED_SKIP or any(
        rel == g or rel.startswith(g + "/") for g in GOVERNED_SKIP
    ))


def case_collides(abs_dir: str) -> bool:
    """目录内已有 index/README 的大小写变体（如 INDEX.md/Readme.md）→ True。

    NTFS 大小写不敏感：open('index.md','w') 会整文件覆写已存在的 INDEX.md
    （W779 实测·S4 12 份 + docs/INDEX.md 差点被清空），故生成器**全模式**跳过
    此类目录；check_folder_docs 第 45 槽同口径豁免。按 os.listdir 真名小写比对
    （两平台同构·不依赖 fs 大小写语义）——否则 Windows 读到异构内容、Linux 报缺件，
    同一目录两平台两种红法（W780 首跑实证 docs/ 目录）。
    """
    try:
        names = os.listdir(abs_dir)
    except OSError:
        return False
    return any(n.lower() in ("index.md", "readme.md")
               and n not in ("index.md", "README.md") for n in names)


def build_index(abs_dir: str) -> str:
    """index.md：机器可读逐文件清单（定位=「这个目录里有什么」·不含叙述与约定）。"""
    rel = rel_of(abs_dir)
    title = os.path.basename(abs_dir) if rel else "仓库根目录"
    here = f"`{rel}/`" if rel else "仓库根目录"
    subdirs = list_subdirs(abs_dir)
    files = list_files(abs_dir)

    lines = [f"# 文件索引 · {title}", ""]
    lines.append(f"> 本文件逐条列出 {here} 的直属文件与子目录，供检索与盘点使用（自动生成·勿手改）。")
    lines.append("> 目录导读与维护约定见同目录 `README.md`；全仓目录用途见根目录 `STRUCTURE.md`。")
    lines.append("")

    lines.append("## 子目录（%d）" % len(subdirs))
    lines.append("")
    if subdirs:
        for d in subdirs:
            lines.append(f"- `{d}/`")
    else:
        lines.append("- （无）")
    lines.append("")

    lines.append("## 文件（%d）" % len(files))
    lines.append("")
    if files:
        groups: dict[str, list[str]] = {}
        for f in files:
            groups.setdefault(group_label(f), []).append(f)
        for label, _ in EXT_GROUPS:
            if label in groups:
                lines.append(f"### {label}")
                lines.append("")
                for f in groups[label]:
                    lines.append(f"- `{f}`")
                lines.append("")
        if "其他" in groups:
            lines.append("### 其他")
            lines.append("")
            for f in groups["其他"]:
                lines.append(f"- `{f}`")
            lines.append("")
    else:
        lines.append("- （无直属文件·纯容器或占位目录）")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("> 生成时点：2026-10-18 · 由 `python scripts/gen_folder_docs.py` 重跑刷新（文件数随磁盘变动·不作文档间同步口径）。")
    lines.append("")
    return "\n".join(lines)


def build_readme(abs_dir: str) -> str:
    """README.md：人读目录导读（定位=「这里装什么、怎么加东西」·不含逐文件清单）。"""
    rel = rel_of(abs_dir)
    title = os.path.basename(abs_dir) if rel else "仓库根目录"
    here = f"`{rel}/`" if rel else "仓库根目录"
    subdirs = list_subdirs(abs_dir)
    files = list_files(abs_dir)
    groups = {group_label(f) for f in files}

    lines = [f"# {title}", ""]
    lines.append(f"> 本文件说明 {here} 的用途、内容构成与维护约定。")
    lines.append("> 逐文件索引见同目录 `index.md`；全仓目录树与命名规范见根目录 `STRUCTURE.md`。")
    lines.append("")

    lines.append("## 这个目录装什么")
    lines.append("")
    lines.append(_describe(abs_dir, rel, subdirs, files, groups))
    lines.append("")

    if subdirs:
        lines.append("## 子目录")
        lines.append("")
        for d in subdirs:
            lines.append(f"- `{d}/`")
        lines.append("")

    lines.append("## 维护约定")
    lines.append("")
    lines.append("- 新增文件后同目录 `index.md` 不会自动更新；需要刷新时重跑 `python scripts/gen_folder_docs.py`。")
    lines.append("- 目录用途或命名约定变更时同步改根目录 `STRUCTURE.md`（单一事实源·本文件不放全仓结构叙述）。")
    lines.append("- 内容文档的写作格式与血缘元信息块按 `docs/00-导读/文档规范.md` 执行。")
    lines.append("")
    return "\n".join(lines)


def _describe(abs_dir: str, rel: str, subdirs: list[str], files: list[str], groups: set[str]) -> str:
    """一句话描述目录内容构成（基于实测构成推导·不写人工定性用途以免失真）。"""
    bits: list[str] = []
    if files:
        bits.append("生成时点含 %d 个直属文件" % len(files))
        if groups:
            bits.append("（%s）" % "、".join(sorted(groups)))
    else:
        bits.append("生成时点无直属文件")
    if subdirs:
        bits.append("；下辖 %d 个子目录" % len(subdirs))
    return "".join(bits) + "。详见同目录 `index.md` 的逐文件清单。"


def render(abs_dir: str, kind: str) -> str:
    """渲染目标文件：H1 标题 → 血缘元信息块 → 正文（§4.1：H1 须为首个非空行）。"""
    body = build_index(abs_dir) if kind == "index.md" else build_readme(abs_dir)
    role = ("逐文件索引（机器可读·与 README.md 分工：本文件列清单、README 讲用途约定）"
            if kind == "index.md" else
            "目录导读（人读·与 index.md 分工：本文件讲用途约定、index.md 列清单）")
    meta = (
        "> 生成来源：`scripts/gen_folder_docs.py`@W779\n"
        "> 生成日期：2026-10-18\n"
        "> 文件角色：%s\n" % role
    )
    lines = body.split("\n")
    # 插入点：H1（首个 '# ' 行）之后
    for i, ln in enumerate(lines):
        if ln.startswith("# "):
            head, tail = lines[: i + 1], lines[i + 1:]
            out = head + [""] + meta.rstrip("\n").split("\n")
            if tail and tail[0] != "":
                out.append("")
            return "\n".join(out + tail)
    return meta + body  # 无 H1 的异常路径：保持元信息在前


def main() -> int:
    ap = argparse.ArgumentParser(description="为在管目录补齐 index.md / README.md")
    ap.add_argument("--dry-run", action="store_true", help="只报告将写哪些文件，不落盘")
    ap.add_argument("--force", action="store_true", help="已存在的文件也按生成内容重写（含人工维护件·慎用）")
    ap.add_argument("--refresh", action="store_true",
                    help="安全刷新：仅重写「生成物所有」的既有文件（按「生成来源」标记判定所有权·人工维护件自动跳过）")
    args = ap.parse_args()

    global _GITIGNORED_DIRS
    _GITIGNORED_DIRS = _build_gitignored_dirs()
    dirs_all = scan_dirs()
    # 大小写冲突目录全模式跳过（INDEX.md 等变体在盘·NTFS 覆写守卫·见 case_collides）
    dirs = [d for d in dirs_all if not case_collides(d)]
    skipped_collision = len(dirs_all) - len(dirs)
    written, skipped_exist, skipped_readme, skipped_hand, failed = [], [], [], [], []

    for d in dirs:
        if not in_scope(d):
            continue

        for kind in ("index.md", "README.md"):
            exists_kind = _kind_exists(d, kind)
            if exists_kind and not (args.force or args.refresh):
                if kind == "README.md":
                    skipped_readme.append(os.path.relpath(os.path.join(d, kind), ROOT))
                else:
                    skipped_exist.append(os.path.relpath(os.path.join(d, kind), ROOT))
                continue
            target = os.path.join(d, kind)
            rel_target = os.path.relpath(target, ROOT).replace(os.sep, "/")
            if args.dry_run:
                written.append(rel_target)
                continue
            # 写前再校验一次（防 dry-run 与实际写之间并发产生 INDEX.md 被覆写）
            exists_kind = _kind_exists(d, kind)
            if exists_kind and not (args.force or args.refresh):
                skipped_exist.append(rel_target)
                continue
            if exists_kind and args.refresh and not args.force:
                # --refresh 所有权判定：带「生成来源：gen_folder_docs.py」元信息标记（或
                # 内容与当前渲染全等）→ 生成物所有·可安全刷新；否则视为人工维护/手改件
                # （所有权已转移）跳过——防 --force 式误轰根 README.md 等手工档（W780）
                try:
                    with open(target, encoding="utf-8") as f:
                        content = f.read()
                except OSError:
                    content = None
                owned = content is not None and (
                    "> 生成来源：`scripts/gen_folder_docs.py`@" in content
                    or content == render(d, kind))
                if not owned:
                    skipped_hand.append(rel_target)
                    continue
            try:
                with open(target, "w", encoding="utf-8", newline="\n") as f:
                    f.write(render(d, kind))
            except OSError as e:
                # 目录被沙盒/占用（.github 等）时不中断整批·如实登记
                failed.append((rel_target, type(e).__name__))
                continue
            written.append(rel_target)

    print("在管目录数：%d（大小写冲突跳过 %d）" % (len(dirs), skipped_collision))
    print("将写入/已写入文件数：%d（index.md %d · README.md %d）" % (
        len(written),
        sum(1 for w in written if w.lower().endswith("index.md")),
        sum(1 for w in written if w.lower().endswith("readme.md")),
    ))
    print("已存在跳过：index.md %d · README.md %d" % (len(skipped_exist), len(skipped_readme)))
    if skipped_hand:
        print("人工维护件跳过 %d 个（--refresh 所有权判定不等·未覆写）：" % len(skipped_hand))
        for rel_t in skipped_hand:
            print("  HAND  " + rel_t)
    if failed:
        print("写入失败 %d 个（目录被占用/沙盒拒绝·未中断整批）：" % len(failed))
        for rel_target, etype in failed:
            print("  FAIL  %s（%s）" % (rel_target, etype))
        return 3
    if args.dry_run:
        for w in written:
            print("  DRY  " + w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
