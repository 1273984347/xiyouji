r"""W757 专项测试：CI 工作流接线完整性（门禁「建置即绿」的机器防线）

## 为什么测这个

项目 E36-E42 铁则②原文：「**门禁建置即绿**（不允许"从未运行/从未通过"的门禁存在）」。
但 W757 取证实测三条真实缺陷，全部属「门禁已声明、CI 里却跑不起来」：

  D1 第 43 门禁 CI 必红：`verify_delivery.py` 委托 `check_chart_values.js --gate`，
     该脚本硬依赖 `require('playwright')`；而 `ci.yml` 的 verify-delivery job 只装
     Python + Node，从未安装 Playwright（`scripts/node_modules` 被 `.gitignore:24` 忽略），
     缺失即 MODULE_NOT_FOUND → crash 分支打印「1 FAIL」→ `_StrictGate` 记 FAIL →
     整个 `verify_delivery.py` FAIL。**门禁建置即红**，且因本地 HEAD 领先公开 main 63
     提交（W728-W756 未推送）而长期未被 CI 暴露。
  D2 W752 安全单测未接线：`xiyouji-agent-web/package.json` 的 `test:server`
     （tools.test.ts 权限边界 / audit.test.ts 审计落盘 / citationGuard.test.ts 引文守卫）
     在全部 workflow 中零引用，CI 只做 build + golden-evals（结构校验）。
  D3 安全扫描盲区：`security_scan.py` 的 discover_files() roots 不含
     `xiyouji-agent-web/`、exts 不含 `.ts/.tsx/.mjs`（见 test_security_scan.py 的扩面断言）。

## 为什么必须用测试守（而不是靠文档纪律）

缺陷本质是「接线被摘除/遗漏时无人发现」——D1 就是一次真实的静默失效：门禁写好了、
本地有 Playwright 所以本地全绿，CI 无浏览器所以必红，两侧观察结果不一致且无人核对。
文档纪律（AGENTS 铁律 / checklist）在 E1 铁律 31 次复现中已被证伪，唯一机械防线是
让「接线存在性」本身成为可执行断言：删掉 CI 里的安装/测试步骤，本文件即红。

## 覆盖判据

  W1 verify-delivery job 具备 Playwright 运行条件（缓存 + 安装步骤）
  W2 agent-web-build job 调用 `test:server`（安全单测接线）
  W3 第 43 门禁仍挂在 verify_delivery（防「删门禁代替修门禁」的假修复）
  W4 三条接线各自可定位（失败时报出缺失项，不静默通过）
  W5 反自检：断言面对真实文件生效（文件不存在即 FAIL，不许静默跳过）
  W6 e2e-interaction job 实际执行 `node tests/e2e/` 套件 + 具备 Playwright
     运行条件（T-02/W773 缺陷①：8 个 JS E2E 套件零 workflow 接线——W674 遗留的
     K11 页面回归因此潜伏到本批接线首跑才暴露，见 ci.yml 内注释）
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
CI_YML = ROOT / ".github" / "workflows" / "ci.yml"
VERIFY_PY = ROOT / "scripts" / "verify_delivery.py"
CHART_JS = ROOT / "scripts" / "check_chart_values.js"
PLAYWRIGHT_UTILS_JS = ROOT / "scripts" / "lib" / "playwright_gate_utils.js"
AGENT_WEB_PKG = ROOT / "xiyouji-agent-web" / "package.json"


def _ci_text() -> str:
    return CI_YML.read_text(encoding="utf-8")


def _job_body(ci: str, job: str) -> str:
    """截取 `job:` 到下一个同级 job 定义之间的正文（缩进 2 空格的 key）。"""
    m = re.search(r"(?m)^  %s:\s*$" % re.escape(job), ci)
    if not m:
        pytest.fail("ci.yml 中找不到 job 定义：%s（接线被删除或改名）" % job)
    rest = ci[m.end():]
    nxt = re.search(r"(?m)^  [A-Za-z0-9_-]+:\s*$", rest)
    return rest[:nxt.start()] if nxt else rest


def _run_blocks(job_body: str) -> str:
    """提取 job 正文中所有 `run:` 步骤的**实际命令文本**（含 `run: |` 多行块）。

    只取命令体：`run: |` 之后的更深缩进行、以及 `run: <单行>`。步骤 `name:` 与注释
    一律排除——W757 负样本实测证明，仅做字符串存在性断言会被步骤名骗过
    （把 run 改成 `echo skipped` 后 `test:server` 仍在步骤名里 → 断言假绿）。
    """
    lines = job_body.splitlines()
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^(\s*)run:\s*(.*)$", ln)
        if m:
            indent = len(m.group(1))
            rest = m.group(2).strip()
            if rest.startswith("|"):  # `run: |` 多行块——收后续更深缩进行
                i += 1
                while i < len(lines):
                    nxt = lines[i]
                    if not nxt.strip():
                        i += 1
                        continue
                    if len(nxt) - len(nxt.lstrip()) <= indent:
                        break
                    out.append(nxt.strip())
                    i += 1
                continue
            out.append(rest)  # `run: <单行命令>`
        i += 1
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 前置：被测文件必须存在（fail-closed·防「文件被挪走所以断言静默空过」）
# ---------------------------------------------------------------------------

def test_wiring_targets_exist():
    """W5：断言对象真实存在——缺文件即 FAIL，不静默跳过。"""
    for p in (CI_YML, VERIFY_PY, CHART_JS, AGENT_WEB_PKG):
        assert p.exists(), "接线断言对象不存在：%s" % p


# ---------------------------------------------------------------------------
# W1：第 43 门禁在 CI 中的运行条件
# ---------------------------------------------------------------------------

def test_gate43_hard_depends_on_playwright():
    """前提事实：第 43 门禁（经 lib 公共模块）确实 require('playwright')（判据前提，非接线本身）。

    W775 重构后 playwright 依赖改为传递链：check_chart_values.js →
    scripts/lib/playwright_gate_utils.js（惰性 require·仅浏览器模式加载，
    --self-test/--judge 纯函数模式不加载浏览器）。本断言守护传递链两环——
    任一环断裂即红，提示同步复核 ci.yml 是否需要装浏览器：防「脚本不再需要
    浏览器，但 CI 仍装着」或反向的静默漂移。
    """
    gate_src = CHART_JS.read_text(encoding="utf-8")
    assert "playwright_gate_utils" in gate_src, (
        "check_chart_values.js 不再引用 lib/playwright_gate_utils——playwright 依赖链第一环断裂")
    assert PLAYWRIGHT_UTILS_JS.exists(), (
        "scripts/lib/playwright_gate_utils.js 缺失——playwright 依赖链第二环断裂（W5 同款 fail-closed）")
    utils_src = PLAYWRIGHT_UTILS_JS.read_text(encoding="utf-8")
    assert "require('playwright')" in utils_src or 'require("playwright")' in utils_src, (
        "playwright_gate_utils.js 不再硬依赖 playwright——请同步复核 ci.yml 是否需要装浏览器")


def test_verify_delivery_job_installs_playwright():
    """W1：verify-delivery job 必须**实际执行** Playwright 安装（否则第 43 门禁在 CI 必红）。

    判据锚在 `run:` 行（同 W2 理由）：字符串存在性会被步骤名/注释骗过。
    `playwright install` 与 `npm ci --prefix scripts` 可能写在多行 run 块内，
    故先按 run 块聚合再匹配。
    """
    body = _job_body(_ci_text(), "verify-delivery")
    cmds = _run_blocks(body)
    has_install = "playwright install" in cmds
    has_deps = "npm ci --prefix scripts" in cmds or "npm install" in cmds
    assert has_install, (
        "verify-delivery job 缺少 `npx playwright install` 步骤——"
        "第 43 门禁 check_chart_values.js 在 CI 中会 MODULE_NOT_FOUND 而必红（W757 D1）")
    assert has_deps, (
        "verify-delivery job 缺少 scripts/ 的 npm 依赖安装——"
        "playwright 包本身来自 scripts/package.json（W757 D1）")


def test_verify_delivery_job_caches_playwright_browsers():
    """W1 辅助：浏览器应有缓存（job 时长可控·复用 W421 模式）。"""
    body = _job_body(_ci_text(), "verify-delivery")
    assert "~/.cache/ms-playwright" in body, (
        "verify-delivery job 未缓存 Playwright 浏览器（每次 CI 全量下载·job 时长不可控）")


# ---------------------------------------------------------------------------
# W2：W752 安全单测接线
# ---------------------------------------------------------------------------

def test_agent_web_job_runs_server_tests():
    """W2：agent-web-build job 必须**实际执行** test:server（W752 安全单测接线）。

    判据必须锚在 `run:` 行上：仅断言 `test:server` 字符串存在会被步骤名/注释骗过
    （W757 负样本实测：把 `run:` 改成 `echo skipped` 后字符串仍在步骤名里，断言假绿）。
    """
    body = _job_body(_ci_text(), "agent-web-build")
    cmds = _run_blocks(body)
    assert "test:server" in cmds, (
        "agent-web-build job 未在 `run:` 中执行 `npm run test:server`——"
        "W752 的权限边界/审计/引文守卫单测在 CI 中不设防（W757 D2）")


def test_agent_web_package_declares_server_tests():
    """W2 前提：package.json 的 test:server 脚本存在且覆盖三个安全测试文件。"""
    import json

    pkg = json.loads(AGENT_WEB_PKG.read_text(encoding="utf-8"))
    script = pkg.get("scripts", {}).get("test:server")
    assert script, "xiyouji-agent-web/package.json 缺少 test:server 脚本（接线目标已消失）"
    for f in ("tools.test.ts", "audit.test.ts", "citationGuard.test.ts"):
        assert f in script, "test:server 未覆盖 %s（安全单测面收窄）" % f


# ---------------------------------------------------------------------------
# W6（T-02·W773）：JS E2E 套件接线（缺陷①——8 个套件零 workflow 调用）
# ---------------------------------------------------------------------------

def test_e2e_interaction_job_runs_js_suite():
    """W6：e2e-interaction job 必须**实际执行** `node tests/e2e/` 套件。

    判据锚 run: 块（同 W1/W2 理由）：字符串存在性会被步骤名/注释骗过。
    接受 `node ../tests/e2e/`（scripts/ cwd 形态）与 `node tests/e2e/`
    （仓库根 cwd 形态）两种写法。
    """
    body = _job_body(_ci_text(), "e2e-interaction")
    cmds = _run_blocks(body)
    assert re.search(r"node\s+(?:\.\./)?tests/e2e/", cmds), (
        "e2e-interaction job 未在 `run:` 中执行 node tests/e2e/ 套件——"
        "8 个 Playwright JS E2E 套件零接线缺陷复燃（T-02 缺陷①·W773）")


def test_e2e_interaction_job_has_playwright_runtime():
    """W6 辅助：该 job 必须具备 Playwright 运行条件（依赖安装 + 浏览器安装）。

    入口即使写对，缺依赖/缺浏览器仍会红（W757 D1 同族：第 43 门禁因 CI 未装
    Playwright 而「建置即红」）。
    """
    body = _job_body(_ci_text(), "e2e-interaction")
    cmds = _run_blocks(body)
    assert "npm ci --prefix scripts" in cmds or "npm install" in cmds, (
        "e2e-interaction job 缺少 scripts/ 的 npm 依赖安装——"
        "playwright 包来自 scripts/package.json（W757 D1 同族）")
    assert "playwright install" in cmds, (
        "e2e-interaction job 缺少 `npx playwright install`——无浏览器套件必红")


# ---------------------------------------------------------------------------
# W3：门禁不得被「删掉」冒充「修好」
# ---------------------------------------------------------------------------

def test_gate43_still_mounted_in_verify_delivery():
    """W3：第 43 门禁仍挂在 verify_delivery（防以删除门禁代替修复接线）。"""
    src = VERIFY_PY.read_text(encoding="utf-8")
    assert "check_chart_values.js" in src, "第 43 门禁已从 verify_delivery.py 摘除（假修复）"
    assert "---- 第 43 门禁 可视化数据断言：" in src, "第 43 门禁汇总行标记缺失（防静默跳过口径被删）"


def test_gate42_and_gate41_still_mounted():
    """W3 辅助：相邻两槽同样在位（防本批顺手摘除其它门禁）。"""
    src = VERIFY_PY.read_text(encoding="utf-8")
    assert "check_script_coverage.py" in src, "第 42 门禁已摘除"
    assert "第 41 门禁" in src or "AGENTS分层" in src, "第 41 门禁标记已摘除"


# ---------------------------------------------------------------------------
# W4：失败可定位（三条接线各自独立断言，不合并成一条笼统断言）
# ---------------------------------------------------------------------------

def test_ci_jobs_are_distinct_and_locatable():
    """W4：两个被测 job 都能被独立定位（失败信息可指到具体 job）。"""
    ci = _ci_text()
    assert re.search(r"(?m)^  verify-delivery:\s*$", ci), "verify-delivery job 不存在"
    assert re.search(r"(?m)^  agent-web-build:\s*$", ci), "agent-web-build job 不存在"
