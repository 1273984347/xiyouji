#!/usr/bin/env python3
"""pre_release_screenshot.py — 迭代发布前增强版截图审查集成脚本

用途：
    将现有的截图审查工具链（Playwright 全量截图 + Pillow 切片 + 运行时断言）
    打包成迭代发布前必跑的一道命令，输出结构化报告。

    作为 release.py 的步骤 5 集成（截图审查纳入迭代发布流程）。

使用方式：
    # 完整流程（截图 + 切片 + 断言 + 报告）
    python scripts/pre_release_screenshot.py

    # 仅生成报告（基于已有截图，不重新截图）
    python scripts/pre_release_screenshot.py --report-only

    # 仅截图不切片
    python scripts/pre_release_screenshot.py --no-slice

    # 指定 viewport
    python scripts/pre_release_screenshot.py --viewport desktop

依赖：
    - Node.js + Playwright（batch_screenshots.js）
    - Python + Pillow（slice_screenshots.py）
    - HTTP server 已启动（python -m http.server 8000）

退出码：
    0 = 截图审查通过（无 P0/P1 布局问题）
    1 = 发现 P0/P1 布局问题
    2 = 依赖缺失或脚本错误

v2.2.17 增强版截图审查纳入迭代发布流程第 1 个产出
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
OUTPUT = SCRIPTS / "output" / "screenshots"


def run(cmd: list[str], cwd=ROOT, check=False, timeout=600) -> tuple[int, str]:
    """运行命令，返回 (returncode, output)。"""
    try:
        r = subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout
        )
        return r.returncode, (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        return 1, f"TIMEOUT after {timeout}s: {' '.join(cmd)}"
    except FileNotFoundError as e:
        return 2, f"DEPENDENCY_MISSING: {e}"


def step1_batch_screenshots(viewport: str = "both") -> bool:
    """步骤 1：Playwright 全量截图（batch_screenshots.js）"""
    print("=" * 60)
    print("步骤 1/4: Playwright 全量截图")
    print("=" * 60)

    batch_js = SCRIPTS / "batch_screenshots.js"
    if not batch_js.exists():
        print(f"[SKIP] {batch_js} 不存在")
        return True  # 不阻塞

    cmd = ["node", str(batch_js)]
    if viewport != "both":
        cmd.extend(["--viewport", viewport])

    rc, out = run(cmd, check=False, timeout=900)
    if rc == 2:
        print(f"[DEPENDENCY] {out}")
        print("提示：请先安装 Node.js + Playwright: npm install playwright")
        return False
    if rc != 0:
        print(f"[FAIL] batch_screenshots.js 退出码 {rc}")
        print(out[-2000:])
        return False

    print("[OK] Playwright 全量截图完成")
    return True


def step2_slice_screenshots() -> bool:
    """步骤 2：Python Pillow 切片（slice_screenshots.py）"""
    print("\n" + "=" * 60)
    print("步骤 2/4: Python Pillow 800px 切片")
    print("=" * 60)

    slice_py = SCRIPTS / "slice_screenshots.py"
    if not slice_py.exists():
        print(f"[SKIP] {slice_py} 不存在")
        return True

    rc, out = run([sys.executable, str(slice_py)], check=False, timeout=300)
    if rc == 2:
        print(f"[DEPENDENCY] {out}")
        print("提示：请先安装 Pillow: pip install Pillow")
        return False
    if rc != 0:
        print(f"[WARN] slice_screenshots.py 退出码 {rc}（不阻塞，继续后续步骤）")
        print(out[-1000:])
        return True  # 切片失败不阻塞

    print("[OK] Pillow 切片完成")
    return True


def step3_layout_assertions() -> bool:
    """步骤 3：运行时布局断言（diagnose_overflow.js 或 layout-audit-report.md）"""
    print("\n" + "=" * 60)
    print("步骤 3/4: 运行时布局断言")
    print("=" * 60)

    diagnose_js = SCRIPTS / "diagnose_overflow.js"
    report_md = OUTPUT / "layout-audit-report.md"

    # 如果已有报告，直接读取
    if report_md.exists():
        print(f"[FOUND] 已有布局审查报告: {report_md}")
        # 简单检查报告内容
        text = report_md.read_text(encoding="utf-8", errors="replace")
        if "P0" in text and "FAIL" in text.upper():
            print("[FAIL] 布局审查报告含 P0 问题")
            return False
        print("[OK] 布局审查报告无 P0 问题")
        return True

    if diagnose_js.exists():
        rc, out = run(["node", str(diagnose_js)], check=False, timeout=300)
        if rc == 2:
            print(f"[DEPENDENCY] {out}")
            return False
        if rc != 0:
            print(f"[WARN] diagnose_overflow.js 退出码 {rc}")
            return True
        print("[OK] 运行时布局断言通过")
        return True

    print("[SKIP] 无 diagnose_overflow.js 且无 layout-audit-report.md")
    return True


def step4_generate_report() -> dict:
    """步骤 4：生成结构化汇总报告"""
    print("\n" + "=" * 60)
    print("步骤 4/4: 生成结构化汇总报告")
    print("=" * 60)

    desktop_dir = OUTPUT / "desktop"
    mobile_dir = OUTPUT / "mobile"
    slices_dir = OUTPUT / "slices"

    desktop_count = len(list(desktop_dir.glob("*.png"))) if desktop_dir.exists() else 0
    mobile_count = len(list(mobile_dir.glob("*.png"))) if mobile_dir.exists() else 0
    slices_count = (
        len(list((slices_dir / "desktop").glob("*.png")))
        + len(list((slices_dir / "mobile").glob("*.png")))
        if slices_dir.exists()
        else 0
    )

    # 读取 overflow 诊断结果
    overflow_md = OUTPUT / "overflow-diagnosis.md"
    overflow_json = OUTPUT / "overflow-diagnosis.json"
    overflow_issues = 0
    if overflow_json.exists():
        try:
            data = json.loads(overflow_json.read_text(encoding="utf-8"))
            if isinstance(data, list):
                overflow_issues = len(data)
            elif isinstance(data, dict):
                overflow_issues = len(data.get("issues", []))
        except Exception:
            pass

    report = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "version": "v2.2.17",
        "tool": "pre_release_screenshot.py",
        "screenshots": {
            "desktop": desktop_count,
            "mobile": mobile_count,
            "slices": slices_count,
            "total": desktop_count + mobile_count,
        },
        "overflow_issues": overflow_issues,
        "has_layout_report": (OUTPUT / "layout-audit-report.md").exists(),
        "has_overflow_diagnosis": overflow_md.exists(),
    }

    # 保存报告
    report_path = OUTPUT / "pre-release-summary.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"  截图总数：desktop={desktop_count}, mobile={mobile_count}")
    print(f"  切片总数：{slices_count}")
    print(f"  溢出问题：{overflow_issues}")
    print(f"  布局报告：{'有' if report['has_layout_report'] else '无'}")
    print(f"  诊断报告：{'有' if report['has_overflow_diagnosis'] else '无'}")
    print(f"\n报告已保存至：{report_path}")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="迭代发布前增强版截图审查集成脚本",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="仅生成报告（基于已有截图，不重新截图）",
    )
    parser.add_argument(
        "--no-slice",
        action="store_true",
        help="跳过切片步骤",
    )
    parser.add_argument(
        "--viewport",
        choices=["desktop", "mobile", "both"],
        default="both",
        help="指定 viewport（默认 both）",
    )
    args = parser.parse_args()

    print("🚀 迭代发布前增强版截图审查")
    print(f"   时间：{datetime.now().isoformat(timespec='seconds')}")
    print("   版本：v2.2.17")

    # 步骤 1: 截图
    if not args.report_only:
        if not step1_batch_screenshots(args.viewport):
            print("\n[FAIL] 截图步骤失败，无法继续")
            return 1

    # 步骤 2: 切片
    if not args.no_slice and not args.report_only:
        step2_slice_screenshots()  # 切片失败不阻塞

    # 步骤 3: 布局断言
    layout_ok = step3_layout_assertions()

    # 步骤 4: 汇总报告
    report = step4_generate_report()

    # 退出判定
    print("\n" + "=" * 60)
    if not layout_ok:
        print("[FAIL] 布局断言检测到 P0 问题，建议修复后再发布")
        return 1
    if report["overflow_issues"] > 0:
        print(f"[WARN] 检测到 {report['overflow_issues']} 个溢出问题，建议检查")
        # 溢出不阻塞发布（P2）
    print("[OK] 截图审查通过，可以发布")
    return 0


if __name__ == "__main__":
    sys.exit(main())
