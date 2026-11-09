#!/usr/bin/env python3
"""check_install_pins.py — W1194：workflow 安装命令必须钉到精确版本。

背景：GitHub「Security and quality」面板的 Code scanning 段里，OSSF Scorecard 的
PinnedDependenciesID 检查三类可固定对象——`uses:` 引用、安装命令、Dockerfile `FROM`。
本仓此前只有 `scripts/check_action_refs.py` 覆盖第一类；安装命令面无判据 ⇒ 2026-11-09
实查查出 7 处未钉版安装命令（pip-audit / black / mypy / pip 自身 / @lhci/cli /
playwright ×2），它们在 Scorecard 面板上以告警形态暴露。

判据：`.github/workflows/*.yml` 的每个 `run` 块里，安装类命令的每个包规格必须钉到精确版本。

豁免（三种，均属「已由另一处钉版」而非「未钉版」）：
  ① `npm ci` —— 按 lockfile 安装，版本由 package-lock.json 钉定；
  ② `pip install -r <清单>` —— 版本由该清单钉定（本仓清单逐行 `==` 钉版）；
  ③ 命令替换取版本（如 `pip install "$(grep '^ruff==' scripts/requirements.txt)"`）——
     版本来自仓内已钉版的清单。

用法：
  py -3 scripts/check_install_pins.py             # 判据模式：逐条校验，退出码 0/1
  py -3 scripts/check_install_pins.py --self-test # 负样本自证（含 8 例）
"""
import argparse
import os
import re
import shlex
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WF_DIR = os.path.join(ROOT, ".github", "workflows")

PIP_RE = re.compile(r"\bpip3?\s+install\b|\bpython\s+-m\s+pip\s+install\b")
NPM_RE = re.compile(r"\bnpm\s+(?:i|install)\b")
OTHER_INSTALL_RE = re.compile(r"\bgem\s+install\b|\bgo\s+install\b|\bcargo\s+install\b|\bapt(?:-get)?\s+install\b")
PIP_OPTION_TOKENS = {"-r", "--requirement", "-U", "--upgrade", "--user", "--no-cache-dir",
                     "--disable-pip-version-check", "--index-url", "--extra-index-url", "-q", "--quiet"}
NPM_OPTION_TOKENS = {"-g", "--global", "--prefix", "--save-dev", "-D", "--no-audit", "--no-fund",
                     "--registry", "--loglevel"}


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
    bad = []
    for tok in _after_install(_tokens(command)):
        if tok.startswith("-"):
            continue
        if tok in PIP_OPTION_TOKENS:
            continue
        inner = _unquote(tok)
        if "$(" in inner or inner.startswith("$"):
            continue  # 命令替换取版本（来自仓内已钉版清单）
        if "==" in inner:
            continue
        if inner in ("pip", "setuptools", "wheel"):
            continue  # 工具自身
        bad.append(tok)
    return bad


def _npm_unpinned(command):
    bad = []
    for tok in _after_install(_tokens(command)):
        if tok.startswith("-"):
            continue
        if tok in NPM_OPTION_TOKENS:
            continue
        if tok.count("@") >= 1 and tok.rsplit("@", 1)[1]:
            continue  # pkg@version 或 @scope/name@version
        bad.append(tok)
    return bad


def check_command(command):
    """返回 (类别, 未钉版包列表)。类别 ∈ {pip, npm, other, None}。"""
    cmd = strip_comment(command).strip()
    if not cmd:
        return None, []
    if OTHER_INSTALL_RE.search(cmd):
        return "other", []
    if NPM_RE.search(cmd):
        tail = cmd.split("npm", 1)[1].strip()
        if tail.startswith("ci"):
            return None, []  # npm ci：按 lockfile 安装（豁免）
        return "npm", _npm_unpinned(cmd)
    if PIP_RE.search(cmd):
        tail = cmd.split("install", 1)[1].strip()
        if tail.startswith(("-r", "--requirement")):
            return None, []  # -r 清单：版本由清单钉定（豁免）
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
        install_lines = [1 for _, c in _iter_run_blocks(text) if check_command(c)[0]]
        checked += len(install_lines)
        rel = ".github/workflows/" + fn
        if not bad:
            print("  PASS %s（%d 条安装命令全部已钉版）" % (rel, len(install_lines)))
            continue
        for lineno, kind, command in bad:
            fails += 1
            print("  FAIL %s:%d  [%s] %s" % (rel, lineno, kind, command[:110]))
            print("       ↳ 安装命令的包规格必须钉到精确版本（如 pkg==1.2.3 / pkg@1.2.3）")
    print("---- 安装命令钉版门禁：%d FAIL / %d 文件 / %d 条安装命令 ----" % (fails, len(files), checked))
    return 1 if fails else 0


def _self_test():
    cases = [
        ("        run: pip install pip-audit==2.10.1", 0, "pip 已钉版 ⇒ 通过"),
        ("        run: pip install pip-audit", 1, "pip 未钉版 ⇒ 判红"),
        ("        run: pip install -r scripts/requirements.txt", 0, "pip -r 清单 ⇒ 豁免"),
        ("        run: npm install -g @lhci/cli@0.13.0", 0, "npm scope 包已钉版 ⇒ 通过"),
        ("        run: npm install playwright @playwright/test", 1, "npm 未钉版 ⇒ 判红"),
        ("        run: npm ci --prefix scripts", 0, "npm ci ⇒ 豁免"),
        ("        run: pip install \"$(grep '^ruff==' scripts/requirements.txt)\" black==26.10.1", 0, "命令替换取版本 ⇒ 豁免"),
        ("        run: pip install pip-audit==2.10.1  # 钉版注释不应被当包名", 0, "行尾注释被剥离 ⇒ 通过"),
        ("        run: npm install playwright@1.63.0 @playwright/test@1.63.0  # 注释", 0, "scope 包带版本 + 注释 ⇒ 通过"),
    ]
    ok = 0
    for content, expect_fail, desc in cases:
        bad = check_workflow_text(content + "\n")
        got = len(bad)
        if got == expect_fail:
            ok += 1
        else:
            print("  FAIL 自证用例：%s（期望 FAIL 数 %d·实际 %d）" % (desc, expect_fail, got))
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
