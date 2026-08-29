#!/usr/bin/env python3
"""仓库版 skills/ ↔ 全局安装版 ~/.qwenworkcn/skills/ 比对与同步工具（本地用，不入 CI）。

背景（W497 教训）：仓库版与全局安装版是独立副本，W478/W488 演进只进全局版、仓库 visual-batch
停 v1.0.0——两份真源无强制一致机制。本工具默认约定**仓库版为真源**，收尾时同步方向为 仓库 → 全局。

背景（W531 教训 · 方向反转）：agent-session-loop / deep-review-loop / mem-wrap-up / self-evolution
四个通用技能在 QwenWork 作品仓库与全局版做了「QwenWork 原生化」演进（v1.3.0-trae → v1.4.0-qwenwork-native），
本仓库副本停留在 8/24 旧版。此时 --check 仍按「仓库为真源」提示跑 --sync，**照做会把新版覆盖成旧版**
且事后 --check 显示一致——静默降级。故本工具新增三件事：

1. **降级保护**：漂移时按 frontmatter 版本号（顶层 version / metadata.version）判定方向；
   判定为「全局更新」的技能，--sync 默认跳过并报错，需 --force 才强行覆盖。
2. **反向回写**：--take-global 显式把全局版拉回仓库（全局 → 仓库），用于真源确在他处演进的场合。
3. **显式归属策略（W533）**：MIRROR_SKILLS 内的技能（四个通用会话流程 skill）以**全局安装版为唯一 master**，
   仓库副本是 git tracked 受控镜像（满足 W517「共享机制必须写入仓库内文件」），**永久禁止** --sync 覆盖 master，
   唯一合法同步路径是 --take-global；其余 xiyouji-* 技能仍以仓库为真源。
4. **行尾归一化比对**：本仓库 core.autocrlf=true，工作区存在 CRLF 副本（skills/ 内 3 个文件），
   旧的逐字节比对会把「仅行尾差异」误报成内容漂移。现比对时统一 CRLF→LF，落盘统一写 LF。

用法：
  python scripts/sync_skills.py --check              # 只比对 + 方向判定（exit 0=无漂移，1=有漂移/有降级）
  python scripts/sync_skills.py --sync               # 仓库 → 全局（跳过「全局更新」与全部镜像技能）
  python scripts/sync_skills.py --sync --force       # 无视方向判定强行仓库 → 全局
  python scripts/sync_skills.py --take-global NAME... # 全局 → 仓库 回写指定技能
  python scripts/sync_skills.py --self-test          # 内置负样本自检（临时目录，不碰真实技能）

与 check_skills_index.py 分工：后者是 CI 门禁（纯仓库内检查）；本工具比对仓库与全局，
依赖本机路径，仅本地跑。改任何 skill 后（含新增）收尾时运行 --sync。
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
GLOBAL_SKILLS = Path.home() / ".qwenworkcn" / "skills"

VER_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)")

# W533 归属策略：这四个通用会话流程 skill 以全局安装版为唯一 master，仓库副本为受控镜像。
# 依据：① 实际加载与触发只认全局目录；② 其 QwenWork 原生化演进发生在 QwenWork 语境；
# ③ 仓库副本必须存在是 W517 铁律（共享机制须 git tracked），但方向单向：只允许 全局 → 仓库。
MIRROR_SKILLS = {"agent-session-loop", "deep-review-loop", "mem-wrap-up", "self-evolution"}

VERDICT_MARK = {
    "global_newer": "[全局更新·禁 --sync]",
    "repo_newer": "[仓库更新→可 --sync]",
    "same_version": "[同版冲突·交人工]",
    "unknown": "[方向不可判·交人工]",
    "mirror": "[镜像技能·仅 --take-global]",
}


# ---------- 基础工具：行尾归一化读取 ----------


def read_norm(path: Path) -> bytes:
    """读文件并把 CRLF 归一为 LF——仓库 autocrlf=true，行尾差异不算内容漂移。"""
    return path.read_bytes().replace(b"\r\n", b"\n")


def write_norm(src: Path, dst: Path) -> None:
    """按 LF 落盘（与 git index 存储形态一致，避免下次 checkout 又长出 CRLF）。"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(read_norm(src))


def repo_skill_files(skill_dir: Path) -> dict[str, Path]:
    """返回相对路径 → 该目录下文件绝对路径 映射（含隐藏文件，如 .skill-metadata.yaml）。"""
    out: dict[str, Path] = {}
    for p in skill_dir.rglob("*"):
        if p.is_file():
            out[p.relative_to(skill_dir).as_posix()] = p
    return out


def collect(skills_dir: Path | None = None, global_skills: Path | None = None) -> list[tuple[str, dict[str, Path], Path | None, Path | None]]:
    """返回 [(skill 名, 仓库文件表, 全局目录或 None)]，覆盖仓库有/全局有两侧。参数可注入供自检。"""
    skills_dir = skills_dir or SKILLS_DIR
    global_skills = global_skills or GLOBAL_SKILLS
    items: list[tuple[str, dict[str, Path], Path | None, Path | None]] = []
    repo_dirs = {p.name: p for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists()}
    global_dirs = (
        {p.name: p for p in global_skills.iterdir() if p.is_dir() and (p / "SKILL.md").exists()} if global_skills.exists() else {}
    )

    for name in sorted(set(repo_dirs) | set(global_dirs)):
        # 只处理仓库 skill 与全局 xiyouji-*（QwenWork 内置/其他项目 skill 如 docx/pdf 不在同步范围）
        if name not in repo_dirs and not name.startswith("xiyouji-"):
            continue
        repo_files = repo_skill_files(repo_dirs[name]) if name in repo_dirs else {}
        items.append((name, repo_files, global_dirs.get(name), repo_dirs.get(name)))
    return items


def diff_file(global_path: Path, repo_path: Path) -> list[str]:
    gl = read_norm(global_path).decode("utf-8-sig").splitlines() if global_path.exists() else []
    rp = read_norm(repo_path).decode("utf-8-sig").splitlines()
    return list(difflib.unified_diff(gl, rp, fromfile=f"global:{global_path.name}", tofile=f"repo:{repo_path.name}", lineterm=""))


# ---------- 方向判定：谁才是更新的那一份 ----------


def frontmatter_version(skill_dir: Path) -> tuple[str | None, tuple[int, int, int] | None]:
    """从 SKILL.md frontmatter 抽版本号（顶层 version 优先，其次 metadata.version）。

    返回 (原始串, 可比较三元组)；抽不到返回 (None, None)。
    """
    sk = skill_dir / "SKILL.md"
    if not sk.exists():
        return None, None
    text = read_norm(sk).decode("utf-8-sig", errors="replace")
    head = text.split("---", 2)
    block = head[1] if len(head) >= 3 else ""
    raw: str | None = None
    for line in block.splitlines():
        stripped = line.strip()
        if not re.match(r"version\s*[:=]", stripped):
            continue  # 精确匹配 version 键，避免 version_note / versions 误判
        m = VER_RE.search(stripped)
        if m:
            raw = re.split(r"[:=]", stripped, maxsplit=1)[-1].strip().strip("\"'")
            break
    if raw is None:
        return None, None
    m = VER_RE.search(raw)
    return raw, (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def judge_direction(repo_dir: Path, global_dir: Path) -> tuple[str, str]:
    """判定漂移方向。返回 (结论码, 人类可读依据)。

    结论码：global_newer / repo_newer / same_version / unknown
    """
    rv, rvt = frontmatter_version(repo_dir)
    gv, gvt = frontmatter_version(global_dir)
    if rvt and gvt:
        if gvt > rvt:
            return "global_newer", f"版本 {rv} < 全局 {gv}"
        if rvt > gvt:
            return "repo_newer", f"版本 {rv} > 全局 {gv}"
        return "same_version", f"两侧同为 {rv} 但内容不同（真源分歧，需人工定夺）"
    if gvt and not rvt:
        return "global_newer", f"全局带版本 {gv}，仓库 SKILL.md 无版本号"
    if rvt and not gvt:
        return "repo_newer", f"仓库带版本 {rv}，全局 SKILL.md 无版本号"
    # 两侧都没版本号 → 用文件最新 mtime 作弱证据（copy2 保mtime，正常同步后两侧相等）
    rm = max((p.stat().st_mtime for p in repo_dir.rglob("*") if p.is_file()), default=0)
    gm = max((p.stat().st_mtime for p in global_dir.rglob("*") if p.is_file()), default=0)
    if gm > rm + 60:
        return "global_newer", f"两侧无版本号，全局最新 mtime 晚于仓库 {(gm - rm) / 3600:.1f}h"
    if rm > gm + 60:
        return "repo_newer", f"两侧无版本号，仓库最新 mtime 晚于全局 {(rm - gm) / 3600:.1f}h"
    return "unknown", "两侧无版本号且 mtime 相同，方向不可判"


def sync_blocked(name: str, verdict: str) -> bool:
    """该技能是否禁止 仓库→全局 覆盖。镜像技能无条件禁止（W533 归属策略），其余按方向判定。"""
    return name in MIRROR_SKILLS or verdict in ("global_newer", "same_version", "unknown")


def analyze(skills_dir: Path | None = None, global_skills: Path | None = None) -> list[dict]:
    """产出每个 skill 的漂移与方向结论。"""
    rows: list[dict] = []
    for name, repo_files, global_dir, repo_dir in collect(skills_dir, global_skills):
        if not repo_files:
            rows.append({"name": name, "kind": "orphan", "detail": "全局有、仓库无（QwenWork 内置或其他项目 skill，不动）"})
            continue
        if global_dir is None:
            rows.append({"name": name, "kind": "missing", "detail": "仓库有、全局无（--sync 将新建）"})
            continue
        drift: list[str] = []
        pairs: list[tuple[str, Path, Path]] = []
        for rel, repo_path in sorted(repo_files.items()):
            gpath = global_dir / rel
            if not gpath.exists():
                drift.append(f"{rel} 全局缺失")
                continue
            if read_norm(gpath) != read_norm(repo_path):
                drift.append(f"{rel} 内容不同")
                pairs.append((rel, repo_path, gpath))
        if not drift:
            rows.append({"name": name, "kind": "clean", "detail": ""})
            continue
        if name in MIRROR_SKILLS:
            verdict, why = "mirror", "全局为唯一 master（W533 归属策略），仓库副本是受控镜像"
        else:
            verdict, why = judge_direction(repo_dir, global_dir)
        rows.append({"name": name, "kind": "drift", "detail": "; ".join(drift), "verdict": verdict, "why": why, "pairs": pairs})
    return rows


# ---------- 三个动作 ----------


def do_check(skills_dir: Path | None = None, global_skills: Path | None = None) -> int:
    rows = analyze(skills_dir, global_skills)
    bad = [r for r in rows if r["kind"] != "clean"]
    regress = [r for r in bad if r.get("verdict") in ("global_newer", "mirror")]
    if not bad:
        print("仓库版与全局版完全一致，无漂移。")
        return 0
    print(f"检测到 {len(bad)} 个技能存在差异：")
    for r in bad:
        if r["kind"] == "drift":
            print(f"  {VERDICT_MARK[r['verdict']]} {r['name']} — {r['detail']}（依据：{r['why']}）")
            for rel, repo_path, gpath in r.get("pairs", [])[:3]:
                for line in diff_file(gpath, repo_path)[:8]:
                    print(f"      {rel} | {line}")
        else:
            print(f"  [{r['kind']}] {r['name']} — {r['detail']}")
    if regress:
        print(
            f"\n⚠ 其中 {len(regress)} 个技能全局版比仓库版更新——照旧跑 --sync 会静默降级（W531 教训）。"
            f"\n  以全局为真源回写仓库：python scripts/sync_skills.py --take-global "
            + " ".join(r["name"] for r in regress)
            + "\n  确要强行以仓库覆盖全局，再加 --force。"
        )
        return 1
    print("\n全部差异方向均为仓库更新，运行 `python scripts/sync_skills.py --sync` 同步到全局版。")
    return 1


def do_sync(force: bool) -> int:
    rows = analyze()
    blocked = {r["name"]: r for r in rows if r["kind"] == "drift" and sync_blocked(r["name"], r.get("verdict", ""))}
    synced = 0
    for name, repo_files, global_dir, _repo_dir in collect():
        if not repo_files:
            continue
        if name in blocked and (name in MIRROR_SKILLS or not force):
            tag = "镜像技能·永久禁 --sync" if name in MIRROR_SKILLS else "--sync 会降级"
            print(f"跳过 {name}/（{blocked[name]['why']}）——{tag}，请改用 --take-global" + ("" if name in MIRROR_SKILLS else " 或加 --force"))
            continue
        target = global_dir if global_dir is not None else GLOBAL_SKILLS / name
        for rel, repo_path in sorted(repo_files.items()):
            gpath = target / rel
            if not gpath.exists() or read_norm(gpath) != read_norm(repo_path):
                write_norm(repo_path, gpath)
                synced += 1
                print(f"同步 {name}/{rel}")
    print(f"\n同步完成：{synced} 个文件更新。" + (f" 有 {len(blocked)} 个技能被降级保护拦下。" if blocked and not force else ""))
    if force and blocked:
        print("（--force 已生效：方向判定被人为越过）")
    return 1 if (blocked and not force) else 0


def do_take_global(names: list[str]) -> int:
    """全局 → 仓库 回写指定技能（真源确在全局侧时使用）。"""
    global_dirs = {p.name: p for p in GLOBAL_SKILLS.iterdir() if p.is_dir()}
    done = 0
    for name in names:
        gdir = global_dirs.get(name)
        if gdir is None:
            print(f"✗ 全局无 {name}/，无法回写")
            return 2
        target = SKILLS_DIR / name
        for src in sorted(gdir.rglob("*")):
            if not src.is_file() or src.name == ".skill-metadata.yaml":
                continue  # 仓库侧元数据为真源，不被全局版抹掉
            write_norm(src, target / src.relative_to(gdir))
            done += 1
        print(f"回写 {name}/ ← 全局版（{frontmatter_version(gdir)[0] or '无版本号'}）")
    print(f"\n回写完成：{done} 个文件（LF 落盘，仓库 .skill-metadata.yaml 保留）。")
    return 0


# ---------- 内置自检：负样本验证 ----------


def do_self_test() -> int:
    """临时目录构造三类场景，断言方向判定与降级拦截都真的生效（先 assert 前提成立再验结论）。"""
    cases: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        repo, glob = root / "repo", root / "global"
        (repo / "xiyouji-demo").mkdir(parents=True)
        (glob / "xiyouji-demo").mkdir(parents=True)

        def put(base: Path, version_line: str, body: str) -> None:
            txt = f"---\nname: xiyouji-demo\n{version_line}---\n\n# demo\n{body}\n"
            (base / "xiyouji-demo" / "SKILL.md").write_text(txt, encoding="utf-8", newline="\n")

        # 场景 1：全局版本更高 → 必须判 global_newer 且 --check 返回降级告警
        put(repo, 'version: "1.3.0-trae-distilled"\n', "OLD")
        put(glob, 'version: "1.4.0-qwenwork-native"\n', "NEW")
        assert b"1.4.0" in (glob / "xiyouji-demo" / "SKILL.md").read_bytes(), "负样本前提未注入成功"
        assert b"1.3.0" in (repo / "xiyouji-demo" / "SKILL.md").read_bytes(), "负样本前提未注入成功"
        rows = analyze(repo, glob)
        drift = [r for r in rows if r["kind"] == "drift"]
        assert len(drift) == 1 and drift[0]["verdict"] == "global_newer", f"场景1 失败：{drift}"
        cases.append("✓ 场景1 全局版本更高 → 判 global_newer（--sync 会被拦）")

        # 场景 2：仓库版本更高 → 判 repo_newer
        put(repo, 'version: "1.5.0"\n', "NEW")
        put(glob, 'version: "1.4.0"\n', "OLD")
        rows = analyze(repo, glob)
        drift = [r for r in rows if r["kind"] == "drift"]
        assert len(drift) == 1 and drift[0]["verdict"] == "repo_newer", f"场景2 失败：{drift}"
        cases.append("✓ 场景2 仓库版本更高 → 判 repo_newer")

        # 场景 3：仅 CRLF/LF 行尾差异 → 不得报漂移（autocrlf 假漂移根因）
        put(repo, 'version: "1.5.0"\n', "SAME")
        put(glob, 'version: "1.5.0"\n', "SAME")
        p = repo / "xiyouji-demo" / "SKILL.md"
        p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
        assert b"\r\n" in p.read_bytes(), "CRLF 负样本前提未注入成功"
        rows = analyze(repo, glob)
        assert all(r["kind"] == "clean" for r in rows), f"场景3 失败（行尾差异被误报）：{rows}"
        cases.append("✓ 场景3 仅行尾差异 → 不报漂移（字节假漂移已修）")

        # 场景 4：同版本号但内容不同 → 判 same_version（冲突，仍需人工）
        put(repo, 'version: "1.5.0"\n', "A")
        put(glob, 'version: "1.5.0"\n', "B")
        rows = analyze(repo, glob)
        drift = [r for r in rows if r["kind"] == "drift"]
        assert len(drift) == 1 and drift[0]["verdict"] == "same_version", f"场景4 失败：{drift}"
        cases.append("✓ 场景4 同版不同内容 → 判 same_version 交人工")

    # 场景 5：MIRROR_SKILLS 内的技能，即便仓库版本号更高，也禁止 --sync 覆盖 master
    with tempfile.TemporaryDirectory() as td2:
        root2 = Path(td2)
        repo2, glob2 = root2 / "repo", root2 / "global"
        mname = sorted(MIRROR_SKILLS)[0]
        (repo2 / mname).mkdir(parents=True)
        (glob2 / mname).mkdir(parents=True)
        (repo2 / mname / "SKILL.md").write_text(
            f'---\nname: {mname}\nversion: "99.0.0"\n---\n\n# repo ahead\n', encoding="utf-8", newline="\n")
        (glob2 / mname / "SKILL.md").write_text(
            f'---\nname: {mname}\nversion: "1.0.0"\n---\n\n# master\n', encoding="utf-8", newline="\n")
        assert sync_blocked(mname, "repo_newer"), "场景5 失败：镜像技能被判定为可 --sync（会覆盖 master）"
        assert not sync_blocked("xiyouji-demo", "repo_newer"), "场景5 失败：普通技能的可同步性被误伤"
        cases.append("✓ 场景5 镜像技能即使仓库版本更高也禁 --sync（普通技能不受影响）")

    print(f"sync_skills.py --self-test {len(cases)}/{len(cases)} 通过：")
    for c in cases:
        print("  " + c)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="比对列漂移 + 方向判定")
    ap.add_argument("--sync", action="store_true", help="仓库→全局（降级保护默认生效）")
    ap.add_argument("--force", action="store_true", help="越过方向判定强行 --sync")
    ap.add_argument("--take-global", nargs="+", metavar="NAME", help="全局→仓库 回写指定技能")
    ap.add_argument("--self-test", action="store_true", help="内置负样本自检（临时目录）")
    args = ap.parse_args()
    if args.self_test:
        return do_self_test()
    if not GLOBAL_SKILLS.exists():
        print(f"全局 skills 目录不存在：{GLOBAL_SKILLS}")
        return 2
    if args.take_global:
        rc = do_take_global(args.take_global)
        return rc if rc else do_check()
    if args.sync:
        rc = do_sync(args.force)
        return rc if rc else do_check()
    if args.check:
        return do_check()
    ap.error("必须指定 --check / --sync / --take-global / --self-test")
    return 2


if __name__ == "__main__":
    sys.exit(main())
