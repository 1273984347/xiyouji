#!/usr/bin/env python3
"""release.py — 版本发布一致性助手

用途：
    版本 bump 时自动校验 6 文件文档一致性 + 推荐下一步动作清单。
    不直接修改文件（修改仍由人工/sync_docs.py --fix 完成），仅做发布前体检。

使用方式：
    # 发布前体检
    python scripts/release.py
    # 指定目标版本号（默认从 CHANGELOG 提取最新）
    python scripts/release.py --target v2.2.16

设计要点：
    - 步骤 1：sync_docs 全部 4 规则必须 PASS（否则报错并退出）
    - 步骤 2：git 状态检查（未提交改动 / 未推送 commits）
    - 步骤 3：测试套件 pytest 必须通过（如 tests/ 存在）
    - 步骤 4：打印发布动作 checklist（tag / push / archive note）
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def run(cmd: list[str], cwd=ROOT, check=True) -> tuple[int, str]:
    """运行命令，返回 (returncode, output)。"""
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if check and r.returncode != 0:
        print(f"[FAIL] {' '.join(cmd)}")
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
    return r.returncode, (r.stdout + r.stderr).strip()


def step1_sync_docs() -> bool:
    """步骤 1：sync_docs.py 4 规则全 PASS。"""
    print("=" * 60)
    print("步骤 1/4: 文档一致性校验 (sync_docs.py)")
    print("=" * 60)
    rc, _ = run([sys.executable, str(SCRIPTS / "sync_docs.py")], check=False)
    if rc != 0:
        print("\n[FAIL] sync_docs.py 检测到不一致，请先修复或运行：")
        print("       python scripts/sync_docs.py --fix")
        return False
    print("[OK] sync_docs.py 4 规则全 PASS")
    return True


def step2_git_status() -> bool:
    """步骤 2：git 状态干净（无未提交改动）。"""
    print("\n" + "=" * 60)
    print("步骤 2/4: git 状态检查")
    print("=" * 60)
    rc, out = run(["git", "status", "--porcelain"], check=False)
    if rc != 0:
        print("[WARN] git 命令失败（可能未初始化 git）")
        return True  # 非 git 仓库不阻断
    if out.strip():
        print("[FAIL] 工作区有未提交改动：")
        for line in out.splitlines()[:10]:
            print(f"  {line}")
        if len(out.splitlines()) > 10:
            print(f"  ...共 {len(out.splitlines())} 项")
        return False
    print("[OK] 工作区干净")

    # 检查是否有未推送 commits
    rc, out = run(["git", "log", "@{u}..HEAD", "--oneline"], check=False)
    if rc == 0 and out.strip():
        print(f"[WARN] 有 {len(out.splitlines())} 个未推送的 commit：")
        for line in out.splitlines()[:5]:
            print(f"  {line}")
    return True


def step3_pytest() -> bool:
    """步骤 3：pytest 测试通过。"""
    print("\n" + "=" * 60)
    print("步骤 3/4: 测试套件 (pytest)")
    print("=" * 60)
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


def step4_checklist(target_version: str) -> None:
    """步骤 4：打印发布动作 checklist。"""
    print("\n" + "=" * 60)
    print(f"步骤 4/4: 发布动作 checklist (目标版本: {target_version})")
    print("=" * 60)
    print(f"""
发布前最后动作（人工执行）：

  1. [ ] CHANGELOG.md 添加新版本段 `### {target_version}` + W### ID + 四件套字段
  2. [ ] file-index.md 追加新版本条目（反向索引）
  3. [ ] README.md / STRUCTURE.md / 项目说明.md / 交接文档.md 头部版本号更新
         可运行：python scripts/sync_docs.py --fix
  4. [ ] git commit -m "release: {target_version}"
  5. [ ] git tag {target_version}
  6. [ ] git push && git push --tags
  7. [ ] （可选）更新 CHANGELOG-ARCHIVE.md（如旧版本归档）

可用命令：
  python scripts/sync_docs.py          # 一致性校验
  python scripts/sync_docs.py --fix    # 自动修复版本号 + 统计
  python scripts/lint_links.py --all   # 链接校验
  python scripts/check_js_syntax.py --all  # JS 语法检查
""")


def main():
    parser = argparse.ArgumentParser(description="版本发布一致性助手")
    parser.add_argument("--target", default="", help="目标版本号（如 v2.2.16，默认从 CHANGELOG 提取）")
    args = parser.parse_args()

    target = args.target
    if not target:
        # 从 CHANGELOG 提取最新版本号
        cl = ROOT / "CHANGELOG.md"
        if cl.exists():
            import re
            m = re.search(r"^###\s+(v\d+\.\d+\.\d+)", cl.read_text(encoding="utf-8"), re.MULTILINE)
            if m:
                target = m.group(1)
    if not target:
        target = "(未知)"

    ok = step1_sync_docs()
    if not ok:
        return 1
    ok = step2_git_status() and ok
    ok = step3_pytest() and ok
    step4_checklist(target)

    print("\n" + "=" * 60)
    if ok:
        print(f"[READY] 发布前体检通过，可执行上方 checklist 发布 {target}")
        return 0
    else:
        print("[BLOCK] 发布前体检未通过，请先修复上述问题")
        return 1


if __name__ == "__main__":
    sys.exit(main())
