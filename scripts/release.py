#!/usr/bin/env python3
"""release.py — 版本发布一致性助手

用途：
    版本 bump 时自动校验 6 文档文档一致性 + 推荐下一步动作清单。
    不直接修改文件（文档一致性由 check_doc_sync.py 校验·修改由批次级联/人工完成），仅做发布前体检。

使用方式：
    # 发布前体检
    python scripts/release.py
    # 指定目标版本号（默认从 CHANGELOG 提取最新）
    python scripts/release.py --target v2.2.16

设计要点：
    - 步骤 1：check_doc_sync 口径体检必须 PASS（否则报错并退出·W793 起替换已退役的 sync_docs）
    - 步骤 2：git 状态检查（未提交改动 / 未推送 commits）
    - 步骤 3：测试套件 pytest 必须通过（如 tests/ 存在）
    - 步骤 4：打印发布动作 checklist（tag / push / archive note）
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

# 常量
_STEP_SEPARATOR = "=" * 60
_REPO_SIZE_WARN_MB = 1024
_LOOSE_OBJECTS_WARN = 20000
_CHANGELOG_VERSION_RE = re.compile(r"^###\s+(v\d+\.\d+\.\d+)", re.MULTILINE)


# ============================================================
# 通用工具
# ============================================================

def run(cmd: list[str], cwd=ROOT, check=True) -> tuple[int, str]:
    """运行命令，返回 (returncode, output)。"""
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if check and r.returncode != 0:
        print(f"[FAIL] {' '.join(cmd)}")
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
    return r.returncode, (r.stdout + r.stderr).strip()


def _print_step_header(step: int, title: str) -> None:
    """打印单个步骤的标题块（统一分隔线格式）。"""
    print("\n" + _STEP_SEPARATOR)
    print(f"步骤 {step}/5: {title}")
    print(_STEP_SEPARATOR)


# ============================================================
# 步骤 1：文档一致性
# ============================================================

def step1_doc_sync() -> bool:
    """步骤 1：check_doc_sync.py 口径体检全 PASS（W793 起替换已退役的 sync_docs.py）。"""
    print(_STEP_SEPARATOR)
    print("步骤 1/5: 文档口径体检 (check_doc_sync.py)")
    print(_STEP_SEPARATOR)
    rc, _ = run([sys.executable, str(SCRIPTS / "check_doc_sync.py")], check=False)
    if rc != 0:
        print("\n[FAIL] check_doc_sync.py 检测到不一致——按输出逐条修复（与 verify_delivery 第 31 槽同源）")
        return False
    print("[OK] check_doc_sync.py 口径体检全 PASS")
    return True


# ============================================================
# 步骤 2：git 状态
# ============================================================

def _check_uncommitted() -> bool:
    """检查未提交改动；有则打印并返回 False。"""
    rc, out = run(["git", "status", "--porcelain"], check=False)
    if rc != 0:
        print("[WARN] git 命令失败（可能未初始化 git）")
        return True  # 非 git 仓库不阻断
    if out.strip():
        print("[FAIL] 工作区有未提交改动：")
        lines = out.splitlines()
        for line in lines[:10]:
            print(f"  {line}")
        if len(lines) > 10:
            print(f"  ...共 {len(lines)} 项")
        return False
    print("[OK] 工作区干净")
    return True


def _check_unpushed() -> None:
    """检查未推送 commit（仅告警·不阻断）。"""
    rc, out = run(["git", "log", "@{u}..HEAD", "--oneline"], check=False)
    if rc == 0 and out.strip():
        lines = out.splitlines()
        print(f"[WARN] 有 {len(lines)} 个未推送的 commit：")
        for line in lines[:5]:
            print(f"  {line}")


def step2_git_status() -> bool:
    """步骤 2：git 状态干净（无未提交改动）。"""
    _print_step_header(2, "git 状态检查")
    if not _check_uncommitted():
        return False
    _check_unpushed()
    return True


# ============================================================
# 步骤 3：仓库体量
# ============================================================

def _parse_count_objects(out: str) -> dict:
    """解析 `git count-objects -v` 输出为 dict。"""
    stats = {}
    for line in out.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            try:
                stats[k.strip()] = int(v.strip())
            except ValueError:
                pass
    return stats


def step3_repo_size() -> bool:
    """步骤 3：仓库体量体检（W698·P2-1：count-objects 监视 + 1GB 告警线）。

    背景：.git 体量曾达 427MB（其中 318MB 为未打包松散对象）；全站 sweep 批次
    （CSP 重生成等）每次把整站页面字节写入历史。监视不阻断日常提交，只在
    发布体检时对超线告警。处置红线：禁历史重写（裁决史以 SHA 锚定），
    超线时走「gc 回收 / 归档治理 / 大文件增量组装」路线。
    """
    _print_step_header(3, "仓库体量体检 (git count-objects)")
    rc, out = run(["git", "count-objects", "-v"], check=False)
    if rc != 0:
        print("[WARN] git 命令失败（可能未初始化 git），跳过体量体检")
        return True

    stats = _parse_count_objects(out)
    loose_mb = stats.get("size", 0) / 1024.0       # size 单位 KB
    pack_mb = stats.get("size-pack", 0) / 1024.0   # size-pack 单位 KB
    total_mb = loose_mb + pack_mb
    print("[INFO] 松散对象 %d 个 / %.0f MB；打包 %.0f MB；合计约 %.0f MB"
          % (stats.get("count", 0), loose_mb, pack_mb, total_mb))

    if stats.get("count", 0) > _LOOSE_OBJECTS_WARN:
        print("[INFO] 松散对象偏多，建议择机 git gc（打包后通常可缩 60%+）")
    if total_mb > _REPO_SIZE_WARN_MB:
        print("[FAIL] 仓库体量超过 1GB 告警线（%.0f MB）——走 gc/归档/增量组装路线，"
              "禁历史重写（裁决史 SHA 锚定）" % total_mb)
        return False
    print("[OK] 仓库体量在 1GB 告警线内")
    return True


# ============================================================
# 步骤 4：pytest
# ============================================================

def step4_pytest() -> bool:
    """步骤 4：pytest 测试通过。"""
    _print_step_header(4, "测试套件 (pytest)")
    tests_dir = ROOT / "tests"
    if not tests_dir.exists():
        print("[SKIP] tests/ 目录不存在")
        return True
    rc, _ = run([sys.executable, "-m", "pytest", "tests/", "-q"], check=False)
    if rc != 0:
        print("[FAIL] pytest 测试失败")
        return False
    print("[OK] pytest 全部通过")
    return True


# ============================================================
# 步骤 5：checklist
# ============================================================

def step5_checklist(target_version: str) -> None:
    """步骤 5：打印发布动作 checklist。"""
    _print_step_header(5, f"发布动作 checklist (目标版本: {target_version})")
    print(f"""
发布前最后动作（人工执行）：

  1. [ ] CHANGELOG.md 添加新版本段 `### {target_version}` + W### ID + 四件套字段
  2. [ ] file-index.md 追加新版本条目（反向索引）
  3. [ ] README.md / STRUCTURE.md / 项目说明.md / HANDOVER.md 头部版本号更新
         版本行由批次级联（batch_cascade）更新·一致性用 python scripts/check_doc_sync.py 校验
  4. [ ] git commit -m "release: {target_version}"
  5. [ ] git tag {target_version}
  6. [ ] git push && git push --tags
  7. [ ] （可选）更新 archive/docs/CHANGELOG-ARCHIVE.md（如旧版本归档）

可用命令：
  python scripts/check_doc_sync.py     # 文档口径体检（与 verify 第 31 槽同源）
  python scripts/stats.py --w <批号>   # 统计计数刷新（sync_docs 已退役·无 --fix 路径）
  python scripts/lint_links.py --all   # 链接校验
  python scripts/check_js_syntax.py --all  # JS 语法检查
""")


# ============================================================
# 主入口
# ============================================================

def _resolve_target_version(explicit: str) -> str:
    """解析目标版本号：显式 → CHANGELOG 首行 → "(未知)"。"""
    if explicit:
        return explicit
    cl = ROOT / "CHANGELOG.md"
    if cl.exists():
        m = _CHANGELOG_VERSION_RE.search(cl.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    return "(未知)"


def main():
    parser = argparse.ArgumentParser(description="版本发布一致性助手")
    parser.add_argument("--target", default="", help="目标版本号（如 v2.2.16，默认从 CHANGELOG 提取）")
    args = parser.parse_args()

    target = _resolve_target_version(args.target)

    ok = step1_doc_sync()
    if not ok:
        return 1
    ok = step2_git_status() and ok
    ok = step3_repo_size() and ok
    ok = step4_pytest() and ok
    step5_checklist(target)

    print("\n" + _STEP_SEPARATOR)
    if ok:
        print(f"[READY] 发布前体检通过，可执行上方 checklist 发布 {target}")
        return 0
    else:
        print("[BLOCK] 发布前体检未通过，请先修复上述问题")
        return 1


if __name__ == "__main__":
    sys.exit(main())
