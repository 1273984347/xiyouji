"""W757 负样本验证器：逐条摘除接线，断言对应测试必红（真防线 vs 假防线）。

用法：py -3 scripts/_w757_negative_check.py
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # scripts/ 的上一级 = 仓库根
CI = ROOT / ".github" / "workflows" / "ci.yml"
BAK = CI.with_suffix(".yml.bak")

CASES = [
    (
        "N1 摘除 playwright 安装块",
        "      - name: Install scripts deps + Playwright (第 43 门禁运行条件·W757)\n"
        "        run: |\n"
        "          npm ci --prefix scripts\n"
        "          cd scripts\n"
        "          npx playwright install --with-deps chromium\n",
        "",
        "test_verify_delivery_job_installs_playwright",
    ),
    (
        "N2 摘除浏览器缓存步骤",
        "      - name: Cache Playwright browsers (W757·复用 W421 模式)\n"
        "        uses: actions/cache@55cc8345863c7cc4c66a329aec7e433d2d1c52a9 # v6\n"
        "        with:\n"
        "          path: ~/.cache/ms-playwright\n"
        "          key: playwright-${{ runner.os }}-${{ hashFiles('scripts/package-lock.json') }}\n",
        "",
        "test_verify_delivery_job_caches_playwright_browsers",
    ),
    (
        "N3 test:server 的 run 改 echo（步骤名仍含关键字）",
        "run: npm --prefix xiyouji-agent-web run test:server",
        "run: echo skipped",
        "test_agent_web_job_runs_server_tests",
    ),
    (
        "N4 第 43 门禁从 verify_delivery 摘除",
        None,  # 特殊：改另一个文件
        None,
        "test_gate43_still_mounted_in_verify_delivery",
    ),
]


def run_pytest(node: str) -> tuple[int, str]:
    r = subprocess.run(
        [sys.executable, "-m", "pytest", f"tests/unit/test_ci_wiring.py::{node}", "-q"],
        cwd=ROOT, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main():
    failures = []
    for name, old, new, node in CASES:
        shutil.copy(CI, BAK)
        verify = ROOT / "scripts" / "verify_delivery.py"
        vbak = verify.with_suffix(".py.bak")
        try:
            if old is None:  # N4：改 verify_delivery.py
                shutil.copy(verify, vbak)
                s = verify.read_text(encoding="utf-8")
                s2 = s.replace("check_chart_values.js", "REMOVED.js")
                assert s2 != s, "N4 替换未命中"
                verify.write_text(s2, encoding="utf-8")
            else:
                s = CI.read_text(encoding="utf-8")
                assert old in s, f"{name}: 目标片段未找到"
                CI.write_text(s.replace(old, new), encoding="utf-8")

            rc, out = run_pytest(node)
            status = "OK(红=真防线)" if rc != 0 else "BAD(仍绿=假防线)"
            if rc == 0:
                failures.append(name)
            print(f"{status}  {name}  ->  {node}")
        finally:
            shutil.copy(BAK, CI)
            if vbak.exists():
                shutil.copy(vbak, verify)
                vbak.unlink()
    BAK.unlink(missing_ok=True)
    print()
    print("=== 负样本汇总 ===")
    print("真防线 %d/%d" % (len(CASES) - len(failures), len(CASES)))
    if failures:
        print("假防线（必须修判据）:", failures)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
