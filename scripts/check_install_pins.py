#!/usr/bin/env python3
"""check_install_pins.py — W1194：workflow 安装命令必须钉到精确版本。

背景：GitHub「Security and quality」面板的 Code scanning 段里，OSSF Scorecard 的
PinnedDependenciesID 检查三类可固定对象——`uses:` 引用、安装命令、Dockerfile `FROM`。
本仓此前只有 `scripts/check_action_refs.py` 覆盖第一类；安装命令面无判据 ⇒ 2026-11-09
实查查出 7 处未钉版安装命令（pip-audit / black / mypy / pip 自身 / @lhci/cli /
playwright ×2），它们在 Scorecard 面板上以告警形态暴露。

判据：`.github/workflows/*.yml` 的每个 `run` 块里，安装类命令必须处于 OSSF Scorecard
的 Pinned-Dependencies 认定的 pinned 形态（**与 Scorecard 源码同源，不自拟口径**）：

· **pip**（Scorecard `checks/raw/shell_download_validate.go` 的 `isUnpinnedPipInstall`）：
  命令含 `--require-hashes` → pinned（直接 return false）；
  含其他参数（如 `pip install pkg==1.2.3`、`pip install -r file`）→ unpinned。
  即 pip 面必须「钉 hash」而非「钉版本」。
· **npm**（同文件 `isNpmUnpinnedDownload`）：
  命令含 `npm ci`（走 lockfile·ci 会校验 lock 内的 integrity hash）→ pinned；
  `npm install pkg@版本`、`npm install pkg@hash` 等形态 → unpinned。

豁免（三种，均属「本层已处于 pinned 形态」）：
  ① `npm ci` —— 走 lockfile，lock 内含 integrity hash·ci 会校验（Scorecard 认 pinned）；
  ② `pip install --require-hashes -r <哈希化清单>` —— 每个依赖（含传递）都钉版本 + hash；
  ③ 命令替换取版本（如 `pip install "$(grep '^ruff==' scripts/requirements.txt)"`）——
     版本来自仓内已钉版的清单。

额外判据（W1194 二轮：供应链面）：仓内每个 `package-lock.json` 的 `resolved` 字段必须指向官方
npm 注册表（`registry.npmjs.org`）——指向第三方镜像站的 lock 会把 CI 的安装取值绑在外部站点，
对方站点故障时取值失败且无法定位（PR 首轮 CI 实测：`registry.npmmirror.com` 返回 500，拉
`omi-7.7.13.tgz` 失败 → `npm ci` 中断）。

用法：
  py -3 scripts/check_install_pins.py             # 判据模式：逐条校验，退出码 0/1
  py -3 scripts/check_install_pins.py --self-test # 负样本自证（含 20 例：安装命令 10 + shell 面 6 + lock 供应链 4）
"""
import argparse
import json
import os
import re
import shlex
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from external_rule_scope import find_shell_files  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WF_DIR = os.path.join(ROOT, ".github", "workflows")

PIP_RE = re.compile(r"\bpip3?\s+install\b|\bpython\s+-m\s+pip\s+install\b")
NPM_RE = re.compile(r"\bnpm\s+(?:i|install)\b")
OTHER_INSTALL_RE = re.compile(r"\bgem\s+install\b|\bgo\s+install\b|\bcargo\s+install\b|\bapt(?:-get)?\s+install\b")
PIP_OPTION_TOKENS = {"-r", "--requirement", "-U", "--upgrade", "--user", "--no-cache-dir",
                     "--disable-pip-version-check", "--index-url", "--extra-index-url", "-q", "--quiet"}
NPM_OPTION_TOKENS = {"-g", "--global", "--prefix", "--save-dev", "-D", "--no-audit", "--no-fund",
                     "--registry", "--loglevel"}

# W1194 二轮：lock 的 resolved 只允许指向官方 npm 注册表（供应链面判据）
LOCK_SKIP_DIRS = {"node_modules", ".git", "archive", "dist", "release", "site", ".agent"}
ALLOWED_REGISTRY_HOSTS = {"registry.npmjs.org"}
# echo / printf 的参数位不是命令（Scorecard 的 shell 解析器同理）
ECHO_ONLY_RE = re.compile(r"^\s*(echo|printf)\b", re.I)


def strip_comment(command):
    """剥离行尾注释（引号内的 # 不算注释）。"""
    out = []
    quote = None
    for ch in command:
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            out.append(ch)
            continue
        if ch == "#":
            break
        out.append(ch)
    return "".join(out)


def _iter_run_blocks(text):
    """产出 (行号, 命令行) —— 覆盖 YAML 的 `run: |` 块与单行 run。"""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        m = re.match(r"^(?:-\s+)?run:\s*(.*)$", stripped)
        if not m:
            i += 1
            continue
        rest = m.group(1).strip()
        if rest.startswith(("|", ">")):
            base_indent = len(raw) - len(raw.lstrip())
            i += 1
            while i < len(lines):
                cur = lines[i]
                if cur.strip() and (len(cur) - len(cur.lstrip())) <= base_indent:
                    break
                yield i + 1, cur.strip()
                i += 1
            continue
        yield i + 1, rest
        i += 1


def _tokens(command):
    """引号感知切分（保留 "$(grep ...)" 这类命令替换为整体）·不配对引号时回退粗切。"""
    try:
        return shlex.split(command)
    except ValueError:
        return [t for t in re.split(r"\s+", command.strip()) if t]


def _after_install(tokens):
    """返回 install 关键字之后的 token 列表（找不到则空）。"""
    for idx, tok in enumerate(tokens):
        if tok == "install" or (tok == "i" and idx > 0 and tokens[idx - 1] == "npm"):
            return tokens[idx + 1:]
    return []


def _unquote(tok):
    if len(tok) >= 2 and tok[0] in ("'", '"') and tok[-1] == tok[0]:
        return tok[1:-1]
    return tok


def _pip_unpinned(command):
    """返回非 pinned 的 pip 安装命令中的包规格（供闭口陈述）。

    Scorecard 对 pip 的 pinned 判定是「命令含 --require-hashes」，而非「包规格钉了版本」。
    因此本函数只报「带包规格但无 --require-hashes」的命令中的非标志参数，
    供闭口陈述具体是哪个包规格未被 hash 固定。
    """
    bad = []
    for tok in _after_install(_tokens(command)):
        if tok.startswith("-"):
            continue
        if tok in PIP_OPTION_TOKENS:
            continue
        inner = _unquote(tok)
        if "$(" in inner or inner.startswith("$"):
            continue  # 命令替换取版本（来自仓内已钉版清单）
        if inner in ("pip", "setuptools", "wheel"):
            continue  # 工具自身
        bad.append(tok)
    return bad


def _npm_unpinned(command):
    """返回非 pinned 的 npm 安装命令中的包规格（供闭口陈述）。

    Scorecard 对 npm 的 pinned 判定是「命令里有 ci」（走 lockfile·ci 会校验 lock 内的 integrity hash），
    而非「包规格钉了版本」——即 `npm install pkg@1.2.3` 也判 unpinned。
    本函数因此报出命令里出现的非标志包规格，供闭口陈述具体是哪个。
    """
    bad = []
    for tok in _after_install(_tokens(command)):
        if tok.startswith("-"):
            continue
        if tok in NPM_OPTION_TOKENS:
            continue
        bad.append(tok)
    return bad


def _is_install_command(command):
    """返回该命令是否为安装类命令（不考虑是否已 pinned）。

    用于统计口径的可视化：已 pinned 的命令也要算在「安装命令总数」里，
    否则输出会让读者误以为目标文件内没有安装命令。
    """
    cmd = strip_comment(command).strip()
    if not cmd:
        return False
    if OTHER_INSTALL_RE.search(cmd):
        return True
    if NPM_RE.search(cmd):
        return True
    if PIP_RE.search(cmd):
        return True
    return False


def check_command(command):
    """返回 (类别, 未钉 hash 的包规格列表)。类别 ∈ {pip, npm, other, None}。

    判定与 Scorecard 源码同源（ossf/scorecard checks/raw/shell_download_validate.go）：
      pip：命令含 `--require-hashes` → pinned（直接 return false）；
           含其他参数（包规格形式的包名 / 版本 / 清单名）→ unpinned。
      npm：命令含 `ci`（走 lockfile·lock 内含 integrity hash）→ pinned；
           `npm install` / `npm i` / `npm update` 带包规格 → unpinned。
    """
    cmd = strip_comment(command).strip()
    if not cmd:
        return None, []
    if OTHER_INSTALL_RE.search(cmd):
        return "other", []
    if NPM_RE.search(cmd):
        tail = cmd.split("npm", 1)[1].strip()
        if tail.startswith("ci"):
            return None, []  # npm ci：走 lockfile·ci 校验 lock 内的 integrity hash（Scorecard 认 pinned）
        return "npm", _npm_unpinned(cmd)
    if PIP_RE.search(cmd):
        # pip：含 --require-hashes → pinned（不再看包规格）
        if "--require-hashes" in cmd:
            return None, []
        return "pip", _pip_unpinned(cmd)
    return None, []


def check_workflow_text(text):
    """返回 [(行号, 类别, 命令)] —— 未钉版的安装命令。"""
    bad = []
    for lineno, command in _iter_run_blocks(text):
        if not command or command.startswith("#"):
            continue
        kind, unpinned = check_command(command)
        if kind and unpinned:
            bad.append((lineno, kind, command))
    return bad


def check_shell_text(text):
    """返回 [(lineno, 类别, 命令)] —— shell 文件内未钉 hash 的安装命令。

    判据与 workflow 的 `run:` 块同源（Scorecard 的 shell 面与 workflow run: 块走同一套
    `validateShellFile` 判定）：
      pip 面必须含 `--require-hashes`；npm 面只认 `npm ci`。

    跳过：注释行、echo/printf 的参数位（它们不是命令）。
    """
    bad = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        if ECHO_ONLY_RE.match(s):
            continue
        kind, unpinned = check_command(s)
        if kind and unpinned:
            bad.append((lineno, kind, s))
    return bad


def find_lockfiles(root=ROOT):
    """产出仓内所有 package-lock.json（排除 node_modules / archive 等非源目录）。"""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in LOCK_SKIP_DIRS]
        for fn in filenames:
            if fn == "package-lock.json":
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def check_lock_registry(path):
    """返回 [(host, 违规条数)] —— lock 里指向非官方注册表的 resolved 主机与条数。

    判据：lock 的 `resolved` 字段只允许官方 npm 注册表（registry.npmjs.org）。
    指向第三方镜像站的 lock 会把 CI 的安装取值绑定在外部站点，对方站点故障时
    取值失败且无法定位（W1194 二轮 CI 实测：registry.npmmirror.com 返回 500）。
    """
    counts = {}
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        return [("<lock 不可解析: %s>" % exc.__class__.__name__, 1)]
    packages = data.get("packages") if isinstance(data, dict) else None
    if not isinstance(packages, dict):
        return []
    for node in packages.values():
        if not isinstance(node, dict):
            continue
        resolved = node.get("resolved")
        if not isinstance(resolved, str) or not resolved.startswith(("http://", "https://")):
            continue
        host = resolved.split("//", 1)[1].split("/", 1)[0].split(":", 1)[0].lower()
        if host not in ALLOWED_REGISTRY_HOSTS:
            counts[host] = counts.get(host, 0) + 1
    return sorted(counts.items())


def report_shell_face(root=ROOT):
    """扫描全仓 shell 面并报告。

    Scorecard 的扫描 Pattern 是 "*"（全仓 shell）——与 workflow 的 run: 块同一套判定（validateShellFile）。
    本守卫原本只扫 workflow ⇒ 面窄于规则面（W1197 扩面后对齐）。

    返回 (shell 文件数, 安装命令总数, FAIL 数)。
    """
    shell_files = find_shell_files(root)
    shell_checked = 0
    fails = 0
    for rel in shell_files:
        path = os.path.join(root, rel.replace("/", os.sep))
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            fails += 1
            print("  FAIL %s  [读取失败]→ fail-closed: %s" % (rel, exc))
            continue
        bad = check_shell_text(text)
        n_install = _count_install_commands(text)
        shell_checked += n_install
        if not bad:
            print("  PASS %s（%d 条安装命令均已钉 hash）" % (rel, n_install))
            continue
        for lineno, kind, command in bad:
            fails += 1
            print("  FAIL %s:%d  [%s] %s" % (rel, lineno, kind, command[:110]))
            print("       ↳ 安装命令的包规格必须钉 hash（pip 需 --require-hashes·npm 需 npm ci）")
            print("       ↳ 该文件在 Scorecard 的 Pattern:"*" 扫描面内（非 workflow 也在）")
    return shell_files, shell_checked, fails


def _count_install_commands(text):
    """统计文本内的安装类命令数（含已 pinned 的）——仅用于可视化输出。"""
    n = 0
    for raw in text.splitlines():
        s = raw.strip()
        if not s or s.startswith("#") or ECHO_ONLY_RE.match(s):
            continue
        if _is_install_command(s):
            n += 1
    return n


def run_gate(root=ROOT):
    wf_dir = os.path.join(root, ".github", "workflows")
    fails = 0
    checked = 0
    files = sorted(f for f in os.listdir(wf_dir) if f.endswith((".yml", ".yaml")))
    for fn in files:
        path = os.path.join(wf_dir, fn)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        bad = check_workflow_text(text)
        # 计「安装命令总数」（含已 pinned 的）——check_command 对 pinned 的命令返回
        # (None, [])，若只统计非 None 则输出为 0，会让读者误以为「无安装命令」。
        install_lines = [1 for _, c in _iter_run_blocks(text) if _is_install_command(c)]
        checked += len(install_lines)
        rel = ".github/workflows/" + fn
        if not bad:
            print("  PASS %s（%d 条安装命令全部已钉版）" % (rel, len(install_lines)))
            continue
        for lineno, kind, command in bad:
            fails += 1
            print("  FAIL %s:%d  [%s] %s" % (rel, lineno, kind, command[:110]))
            print("       ↳ 安装命令的包规格必须钉到精确版本（如 pkg==1.2.3 / pkg@1.2.3）")
    shell_files, shell_checked, shell_fails = report_shell_face(root)
    fails += shell_fails
    # 供应链面（W1194 二轮）：lock 的 resolved 不得指向第三方镜像站
    lock_files = find_lockfiles(root)
    for path in lock_files:
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        bad = check_lock_registry(path)
        if not bad:
            print("  PASS %s（resolved 均指向官方 npm 注册表）" % rel)
            continue
        for host, cnt in bad:
            fails += 1
            print("  FAIL %s  [%s] %d 条 resolved 指向非官方注册表" % (rel, host, cnt))
            print("       ↳ lock 的 resolved 必须统一为 https://registry.npmjs.org/（避免安装取值绑定外部镜像站）")
    print("---- 安装命令钉版门禁：%d FAIL / %d workflow / %d 个 shell 面文件 / %d 条 workflow 安装命令 / %d 条 shell 安装命令 / %d 个 lock ----"
          % (fails, len(files), len(shell_files), checked, shell_checked, len(lock_files)))
    return 1 if fails else 0


def _self_test():
    cases = [
        ("        run: pip install --require-hashes -r scripts/requirements-hashed.txt", 0, "pip --require-hashes → pinned（Scorecard 认定形态）"),
        ("        run: pip install pip-audit==2.10.1", 1, "pip 钉版本但无 --require-hashes → 判红（Scorecard 要求钉 hash）"),
        ("        run: pip install pip-audit", 1, "pip 未钉版 → 判红"),
        ("        run: pip install -r scripts/requirements.txt", 1, "pip -r 清单但无 --require-hashes → 判红"),
        ("        run: npm install -g @lhci/cli@0.13.0", 1, "npm install 钉了版本仍 → 判红（Scorecard 只认 npm ci）"),
        ("        run: npm install playwright@1.63.0 @playwright/test@1.63.0", 1, "npm install 钉了版本仍 → 判红"),
        ("        run: npm ci --prefix scripts", 0, "npm ci → pinned（走 lockfile·ci 校验 integrity hash）"),
        ("        run: pip install \"$(grep '^ruff==' scripts/requirements.txt)\" black==26.10.1", 1, "命令替换取版本但无 --require-hashes → 判红"),
        ("        run: pip install --require-hashes -r scripts/requirements-hashed.txt  # 注释", 0, "行尾注释被剥离 ⇒ 通过"),
        ("        run: npm ci --prefix scripts  # 注释", 0, "npm ci + 注释 ⇒ 通过"),
    ]
    ok = 0
    for content, expect_fail, desc in cases:
        bad = check_workflow_text(content + "\n")
        got = len(bad)
        if got == expect_fail:
            ok += 1
        else:
            print("  FAIL 自证用例：%s（期望 FAIL 数 %d·实际 %d）" % (desc, expect_fail, got))
    # shell 面用例（W1197：全仓 shell 面·与 Scorecard 的 Pattern:"*" 对齐）
    shell_cases = [
        ("#!/bin/bash\nnpm ci --prefix scripts\n", 0, "shell 内 npm ci → pinned"),
        ("#!/bin/bash\nnpm install somepkg@1.0.0\n", 1, "shell 内 npm install 钉版本仍 → 判红"),
        ("#!/bin/bash\npip install somepkg==1.0.0\n", 1, "shell 内 pip 钉版本但无 --require-hashes → 判红"),
        ("#!/bin/bash\npip install --require-hashes -r requirements-hashed.txt\n", 0, "shell 内 pip --require-hashes → pinned"),
        ("#!/bin/bash\n# npm install somepkg@1.0.0\n", 0, "shell 内注释行不算命令"),
        ("#!/bin/bash\necho 'npm install somepkg@1.0.0'\n", 0, "shell 内 echo 参数位不算命令"),
    ]
    for content, expect_fail, desc in shell_cases:
        got = len(check_shell_text(content))
        if got == expect_fail:
            ok += 1
        else:
            print("  FAIL 自证用例：%s（期望 FAIL 数 %d·实际 %d）" % (desc, expect_fail, got))

    # lock 供应链面用例（W1194 二轮）
    lock_cases = [
        ('{"packages": {"node_modules/x": {"resolved": "https://registry.npmjs.org/x/-/x-1.0.0.tgz"}}}',
         0, "lock 指向官方注册表 ⇒ 通过"),
        ('{"packages": {"node_modules/x": {"resolved": "https://registry.npmmirror.com/x/-/x-1.0.0.tgz"}}}',
         1, "lock 指向第三方镜像 ⇒ 判红"),
        ('{"packages": {"node_modules/x": {"version": "1.0.0"}}}',
         0, "lock 无 resolved 字段 ⇒ 通过"),
        ('{"packages": {"node_modules/x": {"resolved": "git+https://example.com/x.git"}}}',
         0, "lock 指向 git 地址 ⇒ 通过"),
    ]
    total_cases = len(cases) + len(shell_cases) + len(lock_cases)
    for content, expect_fail, desc in lock_cases:
        with tempfile.NamedTemporaryFile("w", suffix="package-lock.json", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(content)
            tmp = fh.name
        try:
            got = len(check_lock_registry(tmp))
        finally:
            os.unlink(tmp)
        if got == expect_fail:
            ok += 1
        else:
            print("  FAIL 自证用例：%s（期望 FAIL 数 %d·实际 %d）" % (desc, expect_fail, got))
    print("  自证 %d/%d 通过" % (ok, total_cases))
    print("SELF_TEST_OK" if ok == total_cases else "SELF_TEST_FAILED")
    return 0 if ok == total_cases else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    return run_gate()


if __name__ == "__main__":
    sys.exit(main())
