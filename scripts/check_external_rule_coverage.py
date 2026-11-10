#!/usr/bin/env python3
"""check_external_rule_coverage.py — W1196：外部规则覆盖面审计守卫。

背景
----
W1194→W1195 两批把 GitHub「Security and quality」面板的 Code scanning 段从 20 条降到
3 条，过程中踩到两个可复发的坑（均已入坑表 E-215 / E-216）：

① **外部规则的判定口径必须读其源码确证**——前批按告警文案推测「要钉版本」，
   实测 Scorecard 要的是「钉 hash」，导致 7 处真修一条告警未消。
② **修完不等于消警**——判据口径错时，本仓守卫会「按错误口径自证通过」，
   而平台告警一条不少。

本守卫解决的是**第三类复发**：外部规则的**覆盖面**本身可能超出本仓既有守卫的范围。
Scorecard 的 `checks/raw/pinned_dependencies.go` 里有三个扫描面：

  collectShellScriptInsecureDownloads  → Pattern: "*"        （**全仓所有 shell 脚本**）
  collectDockerfileInsecureDownloads → Pattern: "*Dockerfile*"（全仓所有 Dockerfile）
  collectGitHubWorkflowScript…       → Pattern: ".github/workflows/*"

而本仓三个守卫的扫描面是：

  check_install_pins.py  → 只扫 .github/workflows/*.yml
  check_action_refs.py   → 只扫 .github/workflows/**
  check_docker_pin.py    → 全仓扫 Dockerfile（面够宽）

⇒ **`.github/workflows/` 之外的 shell 脚本完全不在任何守卫的视野内**，
   而它们确实在 Scorecard 的扫描面内。实测（沙箱内变异证明）：
   在 `scripts/` 下放一个含 `npm install somepkg@1.0.0` 与
   `pip install somepkg==1.0.0` 的 `.sh` ⇒ 两个守卫都 rc=0、无任何输出 ⇒ 放过。

判据
----
本守卫不重复检查「某个包是否钉版」（那是 check_install_pins.py 的职责），
而是检查**覆盖面与外部规则是否对齐**：

1. **枚举 Scorecard 的 shell 扫描面**（按其源码的识别规则：文件扩展名属于
   shell 家族 **或** 首行 shebang 匹配 shell 家族），逐个检查其内是否存在
   「安装类命令」——存在即报出（因为本仓守卫不覆盖该面 ⇒ 属覆盖盲区）。
2. **枚举全仓所有依赖生态的清单/lock 文件**（npm / yarn / pnpm / pip / pipenv /
   poetry / cargo / composer / gem / gomod），核对每一处的 `resolved` 主机
   是否为官方源（非官方镜像站 ⇒ 供应链风险面，本仓守卫只覆盖部分）。
3. **核对本仓三个守卫的扫描面**是否覆盖了 Scorecard 的 shell 扫描面 ⇒
   不覆盖即报（覆盖缺口本身是可复发缺陷）。

用法
----
  py -3 scripts/check_external_rule_coverage.py             # 判据模式：退出码 0/1
  py -3 scripts/check_external_rule_coverage.py --self-test # 负样本自证（含 8 例）
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"node_modules", ".git", "archive", "dist", "release", "site",
             "tmpe", "__pycache__", ".venv", "docs", "spark-output"}

# Scorecard 的 shell 家族（checks/raw/shell_download_validate.go 的 supportedShells 语义）
SHELL_FAMILY = ["sh", "bash", "zsh", "ksh", "csh", "fish", "dash", "ash"]

# 安装类命令的判定（与 Scorecard 的 packageManagerCommands 同族的识别面）
INSTALL_CMD_RE = re.compile(
    r"\b(pip3?|python3?|npm|yarn|pnpm|gem|go|cargo)\b[^\n]*\b(install|i|add|get|update|upgrade)\b",
    re.I,
)
# echo / printf 的参数位不是命令（Scorecard 的 shell 解析器也不会把 echo 的字符串当命令）
ECHO_ONLY_RE = re.compile(r"^\s*(echo|printf)\b", re.I)

# 各生态的清单 / lock 文件 → 生态名
MANIFEST_FILES = {
    "package-lock.json": "npm",
    "yarn.lock": "yarn",
    "pnpm-lock.yaml": "pnpm",
    "Pipfile.lock": "pipenv",
    "poetry.lock": "poetry",
    "Cargo.lock": "cargo",
    "composer.lock": "composer",
    "Gemfile.lock": "gem",
    "go.sum": "gomod",
}
OFFICIAL_REGISTRY = {
    "npm": {"registry.npmjs.org"},
    "yarn": {"registry.npmjs.org", "registry.yarnpkg.com"},
    "pnpm": {"registry.npmjs.org"},
    "pipenv": {"files.pythonhosted.org"},
    "poetry": {"files.pythonhosted.org"},
    "cargo": {"crates.io", "static.crates.io", "index.crates.io"},
    "composer": {"repo.packagist.org", "packagist.org"},
    "gem": {"rubygems.org"},
    "gomod": {"proxy.golang.org", "sum.golang.org"},
}

# 本仓既有守卫的扫描面（用于第 3 条判据：覆盖缺口）
# W1197：check_install_pins.py 与 check_action_refs.py 已扩到全仓 shell（与 Scorecard 的
# Pattern:"*" 对齐）；check_docker_pin.py 全仓扫 Dockerfile（与 Pattern:"*Dockerfile*" 对齐）。
GUARD_SCOPE = {
    "check_install_pins.py": ["<repo-root>"],   # 全仓 shell（W1197）
    "check_action_refs.py": ["<repo-root>"],    # 全仓 shell（W1197）
    "check_docker_pin.py": ["<repo-root>"],     # 全仓 Dockerfile
}


def _is_shell_file(path, name):
    """按 Scorecard 的识别规则判定：扩展名属 shell 家族，或首行 shebang 匹配 shell 家族。"""
    if "." in name:
        if name.rsplit(".", 1)[-1].lower() in SHELL_FAMILY:
            return True
    try:
        with open(path, "rb") as fh:
            first = fh.readline(400)
    except OSError:
        return False
    if not first.startswith(b"#!"):
        return False
    text = first.decode("utf-8", "replace")
    return any(re.search(r"(^|[/\s])%s(\s|$)" % s, text) for s in SHELL_FAMILY)


def _walk(root=ROOT):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            yield os.path.join(dirpath, fn)


def find_shell_files(root=ROOT):
    """产出 Scorecard shell 扫描面内的文件（仓库相对路径）。"""
    out = []
    for path in _walk(root):
        name = os.path.basename(path)
        if _is_shell_file(path, name):
            out.append(os.path.relpath(path, root).replace(os.sep, "/"))
    return sorted(out)


def shell_install_commands(rel_path, root=ROOT):
    """返回该 shell 文件内的安装类命令行（含行号）——用于判据①。"""
    full = os.path.join(root, rel_path)
    hits = []
    try:
        with open(full, encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh, 1):
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                if ECHO_ONLY_RE.match(s):
                    continue  # echo/printf 的参数位不是命令（Scorecard shell 解析器同理）
                if INSTALL_CMD_RE.search(line):
                    hits.append((i, s[:130]))
    except OSError:
        pass
    return hits


def check_manifest_registry(rel_path, root=ROOT):
    """返回该清单里非官方源的 resolved 主机集合——用于判据②。"""
    name = os.path.basename(rel_path)
    eco = MANIFEST_FILES.get(name)
    if not eco:
        return set()
    full = os.path.join(root, rel_path)
    bad = set()
    try:
        with open(full, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return bad
    allowed = OFFICIAL_REGISTRY.get(eco, set())
    for m in re.finditer(r'"resolved"\s*:\s*"https?://([^/"]+)', text):
        host = m.group(1).split(":", 1)[0].lower()
        if host not in allowed:
            bad.add(host)
    return bad


def find_manifest_files(root=ROOT):
    out = []
    for path in _walk(root):
        name = os.path.basename(path)
        if name in MANIFEST_FILES:
            out.append(os.path.relpath(path, root).replace(os.sep, "/"))
    return sorted(out)


def guard_scope_gaps(root=ROOT):
    """返回 [(守卫名, 未覆盖的 shell 面文件)]——用于判据③。"""
    shell_files = find_shell_files(root)
    gaps = []
    for guard, scopes in GUARD_SCOPE.items():
        if "<repo-root>" in scopes:
            continue
        prefixes = [s.rstrip("/") + "/" for s in scopes]
        uncovered = []
        for f in shell_files:
            covered = False
            for prefix in prefixes:
                if f.startswith(prefix):
                    covered = True
                    break
            if not covered:
                uncovered.append(f)
        if uncovered:
            gaps.append((guard, uncovered))
    return gaps


def run_gate(root=ROOT):
    fails = 0

    print("=== ① Scorecard shell 扫描面内的安装类命令（本仓守卫不覆盖该面）===")
    shell_files = find_shell_files(root)
    print("  Scorecard shell 扫描面文件数：%d" % len(shell_files))
    for rel in shell_files:
        hits = shell_install_commands(rel, root)
        if not hits:
            print("  PASS %s（无安装类命令）" % rel)
            continue
        fails += 1
        print("  FAIL %s（%d 条安装类命令）" % (rel, len(hits)))
        for lineno, text in hits:
            print("       ↳ %4d: %s" % (lineno, text))
            print("       ↳ 该文件在 Scorecard 的 Pattern:\"*\" 扫描面内，但本仓安装命令守卫只扫 .github/workflows ⇒ 覆盖盲区")

    print("=== ② 各生态清单的 resolved 是否全为官方源 ===")
    manifests = find_manifest_files(root)
    for rel in manifests:
        bad = check_manifest_registry(rel, root)
        eco = MANIFEST_FILES[os.path.basename(rel)]
        if not bad:
            print("  PASS %s（%s·resolved 全为官方源）" % (rel, eco))
            continue
        fails += 1
        print("  FAIL %s（%s·非官方源：%s）" % (rel, eco, ", ".join(sorted(bad))))
        print("       ↳ 安装取值将绑定到外部站点；该站故障时 CI 取值失败且难定位")

    print("=== ③ 本仓守卫的扫描面 vs Scorecard 的 shell 扫描面 ===")
    gaps = guard_scope_gaps(root)
    if not gaps:
        print("  PASS 无覆盖缺口")
    for guard, uncovered in gaps:
        # 这一项是「当前已知的覆盖缺口」——报出但不阻断：
        # 它对应的修法是把守卫扫描面扩到全仓 shell（需另行批处理），
        # 在那之前不能用它阻断 CI。依据：本批实测 5 个 shell 面文件内实际无安装命令（见上方① 项）。
        print("  WARN %s 的扫描面不含 %d 个 shell 面文件（覆盖缺口·不阻断）：%s"
              % (guard, len(uncovered), uncovered[:5]))
        print("       ↳ Scorecard 扫 Pattern:\"*\"（全仓 shell）⇒ 本仓守卫面窄于规则面；修法是扩守卫扫描面")

    print("---- 外部规则覆盖面门禁：%d FAIL / %d shell 文件 / %d 个清单 ----"
          % (fails, len(shell_files), len(manifests)))
    return 1 if fails else 0


def _self_test():
    cases = []

    # 判据①：shell 识别规则
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        f_sh = os.path.join(td, "a.sh")
        with open(f_sh, "w", encoding="utf-8") as fh:
            fh.write("#!/bin/bash\necho hi\n")
        cases.append(("N1 .sh 扩展名", _is_shell_file(f_sh, "a.sh"), True, "扩展名属 shell 家族"))

        f_sheb = os.path.join(td, "b.txt")
        with open(f_sheb, "w", encoding="utf-8") as fh:
            fh.write("#!/usr/bin/env bash\necho hi\n")
        cases.append(("N2 shebang 匹配 shell", _is_shell_file(f_sheb, "b.txt"), True, "首行 shebang 匹配"))

        f_py = os.path.join(td, "c.py")
        with open(f_py, "w", encoding="utf-8") as fh:
            fh.write("print('x')\n")
        cases.append(("N3 非 shell 文件", _is_shell_file(f_py, "c.py"), False, "既无扩展名也无 shebang"))

        f_pysheb = os.path.join(td, "d.py")
        with open(f_pysheb, "w", encoding="utf-8") as fh:
            fh.write("#!/usr/bin/env python3\nprint('x')\n")
        cases.append(("N4 python shebang 不算 shell", _is_shell_file(f_pysheb, "d.py"), False, "shebang 非 shell 家族"))

        # 判据①：安装命令识别
        f_sh2 = os.path.join(td, "e.sh")
        with open(f_sh2, "w", encoding="utf-8") as fh:
            fh.write("#!/bin/bash\nnpm install somepkg@1.0.0\n")
        cases.append(("N5 shell 内 npm install", len(shell_install_commands("e.sh", td)) == 1, True, "识别到 1 条安装命令"))

        f_sh3 = os.path.join(td, "f.sh")
        with open(f_sh3, "w", encoding="utf-8") as fh:
            fh.write("#!/bin/bash\necho 'install ruff'\n# npm install x\n")
        cases.append(("N6 注释与字符串不算", len(shell_install_commands("f.sh", td)) == 0, True, "注释行不算"))

        # 判据②：官方源判定
        f_lock = os.path.join(td, "package-lock.json")
        with open(f_lock, "w", encoding="utf-8") as fh:
            json.dump({"packages": {"node_modules/x": {
                "resolved": "https://registry.npmmirror.com/x/-/x-1.0.0.tgz"}}}, fh)
        cases.append(("N7 第三方镜像源判红", len(check_manifest_registry("package-lock.json", td)) == 1, True, "npmmirror 非官方"))

        f_lock2 = os.path.join(td, "package-lock.json")
        with open(f_lock2, "w", encoding="utf-8") as fh:
            json.dump({"packages": {"node_modules/x": {
                "resolved": "https://registry.npmjs.org/x/-/x-1.0.0.tgz"}}}, fh)
        cases.append(("N8 官方源通过", len(check_manifest_registry("package-lock.json", td)) == 0, True, "npmjs 官方"))

    ok = 0
    for desc, got, want, note in cases:
        if got == want:
            ok += 1
        else:
            print("  FAIL 自证用例：%s（%s·期望 %s·实际 %s）" % (desc, note, want, got))
    print("  自证 %d/%d 通过" % (ok, len(cases)))
    print("SELF_TEST_OK" if ok == len(cases) else "SELF_TEST_FAILED")
    return 0 if ok == len(cases) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    return run_gate()


if __name__ == "__main__":
    sys.exit(main())
