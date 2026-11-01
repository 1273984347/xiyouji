#!/usr/bin/env python3
"""_w1076_make_spec.py — 生成 W1076 批次 spec（scripts/output/_w1076_spec.json）。

## 为什么用脚本生成

`file_index_rows` 必须**覆盖索引全集**（宁多勿少）——手写清单必漏（refresh 产物、
级联面、一次性脚本归档两端、J2 快照）。本脚本口径：

1. **策展清单**（本批应动的面·人工给定）＋
2. **索引态全集**（`git diff --cached --name-only` ＋ 未跟踪件）取并集；
3. 一次性脚本的**新旧两路径**都登记（git mv 后旧路径仍在 spec·第 51 槽口径）。

用法：
    python scripts/_w1076_make_spec.py            # 打印/写 spec
"""
import json
import os
import subprocess
import sys

def _repo_root():
    """向上找仓库根（带 .git 的目录）——脚本归档到 archive/scripts/batches/w1076/ 后仍可用。"""
    cur = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("未找到仓库根（.git）")
        cur = parent


ROOT = _repo_root()
OUT = os.path.join(ROOT, "scripts", "output", "_w1076_spec.json")
BATCH = "W1076"

# 本批策展清单（人工给定·与施工面对应）
CURATED = [
    # 站页面（施工）
    "site/index.html", "site/guide.html", "site/curated.html", "site/dashboard.html",
    "site/dukou-engine.html", "site/rum-viewer.html", "site/404.html", "site/system.css",
    # 站页面（级联页脚面）
    "site/data/cross-time-danmaku.html", "site/data/tag-cloud.html",
    # 工具件（本批新增·批后归档到 archive/scripts/batches/w1076/·两端都登记）
    "scripts/_w1076_make_spec.py", "scripts/_w1076_space_tokens.py",
    "scripts/_w1076_cjk_value_marks.py",
    "archive/scripts/batches/w1076/_w1076_make_spec.py",
    "archive/scripts/batches/w1076/_w1076_space_tokens.py",
    "archive/scripts/batches/w1076/_w1076_cjk_value_marks.py",
    # 工具产物（J2 快照·before/after 证明面）
    "scripts/output/_w1076_spec.json", "scripts/output/_w1076_j2_before",
    "scripts/output/_w1076_j2_before_root3.json", "scripts/output/_w1076_j2_after",
    # 目录文档 refresh 产物
    "scripts/output/README.md", "scripts/output/index.md", "scripts/output/tools-inventory.md",
    # 治理面
    "CHANGELOG.md", "HANDOVER.md", "README.md", "STRUCTURE.md", "AGENTS.md",
    "docs/00-导读/项目说明.md", "docs/00-导读/W批次编号对账表.md",
    "docs/11-方案报告/README.md",
    "docs/11-方案报告/计划方案/T42-任务计划执行与经验沉淀报告-2026-11-02.md",
]

CATEGORY = {
    "site/data/": "页面（v4 令牌消费）",
    "site/": "页面（v4 令牌消费）",
    "scripts/output/_w1076_j2": "本批工具/产物",
    "scripts/output/_w1076_spec.json": "本批工具/产物",
    "scripts/output/": "本批工具/产物",
    "scripts/": "本批工具/产物",
    "archive/": "本批工具/产物",
    "docs/": "治理文档",
}


def _cat(p):
    for k in ("site/data/", "site/", "scripts/output/_w1076_j2", "scripts/output/_w1076_spec.json",
              "scripts/output/", "scripts/", "archive/", "docs/"):
        if p.startswith(k):
            return CATEGORY[k]
    return "治理文档"


def _git(*args):
    # core.quotepath=false：中文路径直出 UTF-8（默认形态是 \346 八进制转义·会让 spec 行与真实路径失配）
    r = subprocess.run(["git", "-c", "core.quotepath=false"] + list(args),
                       cwd=ROOT, capture_output=True, text=True)
    return r.stdout.splitlines()


def staged_set():
    files = set(_git("diff", "--cached", "--name-only"))
    for ln in _git("status", "--porcelain"):
        ln = ln.strip()
        if not ln:
            continue
        path = ln[3:].strip()
        if " -> " in path:
            path = path.split(" -> ")[-1].strip()
        path = path.strip('"')
        if path and not path.endswith("/"):   # 空目录（git 不跟踪）不入清单
            files.add(path)
    return files


def main():
    _apply = '--apply' in sys.argv

    spec_path = OUT
    spec = json.load(open(spec_path, encoding="utf-8")) if os.path.exists(spec_path) else {}
    paths = set(CURATED) | staged_set()
    rows = ["| %s | %s | %s |" % (p, BATCH, _cat(p)) for p in sorted(paths)]
    spec["file_index_rows"] = rows
    if _apply:
        with open(spec_path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(spec, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        print("spec file_index_rows：%d 行 → %s（已写盘）" % (len(rows), spec_path))
    else:
        print("spec file_index_rows：%d 行 → %s（dry-run·须 --apply 才写盘）" % (len(rows), spec_path))
    for r in rows:
        print("  " + r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
