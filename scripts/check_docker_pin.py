#!/usr/bin/env python3
"""check_docker_pin.py — W1194：Dockerfile 基础镜像必须钉到不可变 digest。

背景：GitHub「Security and quality」面板的 Code scanning 段共 20 条告警，其中 14 条为
OSSF Scorecard 的 PinnedDependenciesID。该规则检查三类对象：workflow 的 `uses:` 引用、
安装命令（pip install / npm install 等）是否钉版、Dockerfile 的 `FROM` 是否钉 digest。
W1191/W1192 只核对了 `uses:` 面（90 个引用全钉 40-hex SHA）⇒ 核对面窄于告警面，
安装命令面与 Dockerfile 面被漏掉。本守卫把后两面收进机器判据。

判据：仓内（排除 archive/ 与 node_modules/）每个 Dockerfile 的每条 `FROM` 指令必须写成
`image@sha256:<64 位十六进制>`；`FROM image AS stage` 形式允许保留 AS 别名。

用法：
  py -3 scripts/check_docker_pin.py             # 判据模式：逐条 FROM 校验，退出码 0/1
  py -3 scripts/check_docker_pin.py --self-test # 负样本自证（4 例：已钉/未钉/别名/非 hex）
"""
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"archive", "node_modules", ".git", "site", "dist", "release"}
FROM_RE = re.compile(r"^\s*FROM\s+(\S+)(.*)$", re.IGNORECASE)
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def find_dockerfiles(root=ROOT):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.lower() == "dockerfile" or fn.lower().startswith("dockerfile."):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def check_dockerfile(path):
    """返回 (problems, total)：problems 为 [(行号, 原始 FROM 行)]。"""
    problems = []
    total = 0
    with open(path, encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            m = FROM_RE.match(line)
            if not m:
                continue
            total += 1
            spec = m.group(1)
            if "@" not in spec:
                problems.append((lineno, stripped))
                continue
            image, _, digest = spec.partition("@")
            if not image or not DIGEST_RE.match(digest):
                problems.append((lineno, stripped))
    return problems, total


def run_gate(root=ROOT):
    files = find_dockerfiles(root)
    fails = 0
    checked = 0
    for path in files:
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        problems, total = check_dockerfile(path)
        checked += total
        if not total:
            print("  PASS %s（无 FROM 指令）" % rel)
            continue
        if problems:
            fails += len(problems)
            for lineno, text in problems:
                print("  FAIL %s:%d  %s" % (rel, lineno, text))
                print("       ↳ FROM 必须写成 image@sha256:<64 位十六进制>（不可变引用）")
        else:
            print("  PASS %s（%d 条 FROM 全部已钉 digest）" % (rel, total))
    print("---- Docker 基础镜像钉版门禁：%d FAIL / %d 文件 / %d 条 FROM ----"
          % (fails, len(files), checked))
    return 1 if fails else 0


def _self_test():
    cases = [
        ("FROM node:22-alpine@sha256:" + "a" * 64 + "\n", 0, "已钉 digest ⇒ 通过"),
        ("FROM node:22-alpine\n", 1, "未钉 digest ⇒ 判红"),
        ("FROM node:22-alpine@sha256:" + "a" * 64 + " AS build\n", 0, "多阶段别名 ⇒ 通过"),
        ("FROM node:22-alpine@sha256:deadbeef\n", 1, "非 64 位 hex ⇒ 判红"),
        ("# FROM node:22-alpine\nRUN echo ok\n", 0, "注释行不计入"),
    ]
    ok = 0
    for content, expect_fail, desc in cases:
        with tempfile.NamedTemporaryFile("w", suffix="Dockerfile", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(content)
            tmp = fh.name
        try:
            problems, total = check_dockerfile(tmp)
        finally:
            os.unlink(tmp)
        got_fail = len(problems)
        if got_fail == expect_fail:
            ok += 1
        else:
            print("  FAIL 自证用例：%s（期望 FAIL 数 %d·实际 %d）" % (desc, expect_fail, got_fail))
    print("  自证 %d/%d 通过" % (ok, len(cases)))
    print("SELF_TEST_OK" if ok == len(cases) else "SELF_TEST_FAILED")
    return 0 if ok == len(cases) else 1


def main():
    if "--self-test" in sys.argv:
        return _self_test()
    return run_gate()


if __name__ == "__main__":
    sys.exit(main())
