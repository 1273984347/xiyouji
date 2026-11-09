"""check_orchestration_refs.py —— 编排面引用存在性门禁（W1154 新建·基础设施审计 §6 建议）。

背景：W1014 sync_docs 死钩子、W1154 实证 drl-contracts 休眠钩子失效——「编排面
（Makefile / .pre-commit-config.yaml / workflow）指向的 scripts/ 路径」此前无任何
门禁校验存在性，同类问题以「休眠配置」形态潜伏。

判据（方向与第 42 槽相反：42 判「脚本有没有入口」，本件判「入口指向的文件还在不在」）：
  ① Makefile 命令行中的 scripts/... 路径必须存在（注释行不计）；
  ② .pre-commit-config.yaml 每个 entry: 的 scripts/ 路径必须存在；
  ③ .github/workflows/*.yml 中调用的 scripts/... 路径必须存在（注释行不计）。

用法：python scripts/check_orchestration_refs.py [--self-test]
退出码：0 = 通过 / 1 = 判红。
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# 双边界（W1154 实测三轮假阳性修正）：左边界排除 archive/scripts/ 等前缀路径的子串咬入；
# 右边界排除 .json/.shard 扩展前缀咬入（package.json / chart-gates.json / x.shard1.jsonl）。
REF_RE = re.compile(r"(?<![\w./-])scripts[/\\][\w\-./\\]+\.(?:py|js|mjs|sh|ps1|yaml|yml)(?![\w.])")


def _exists(rel):
    p = os.path.join(ROOT, rel.replace("\\", "/"))
    return os.path.isfile(p)


def _check_text(text, label, fails):
    """共同判据体：逐行（跳过 # 注释行）抽 scripts/ 引用·不存在即 FAIL。"""
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.lstrip().startswith("#"):
            continue
        for m in REF_RE.finditer(ln):
            rel = m.group(0).replace("\\", "/")
            if not _exists(rel):
                fails.append(f"{label}:{i} 引用不存在脚本：{rel}")


def check_makefile(fails, path=None):
    path = path or os.path.join(ROOT, "Makefile")
    if os.path.isfile(path):
        _check_text(open(path, encoding="utf-8").read(), "Makefile", fails)


def check_precommit(fails, path=None):
    path = path or os.path.join(ROOT, ".pre-commit-config.yaml")
    if not os.path.isfile(path):
        return
    for i, ln in enumerate(open(path, encoding="utf-8"), 1):
        st = ln.strip()
        if st.startswith("entry:"):
            _check_text(st, f".pre-commit-config.yaml:{i}", fails)


def check_workflows(fails, workflows_dir=None):
    d = workflows_dir or os.path.join(ROOT, ".github", "workflows")
    if not os.path.isdir(d):
        return
    for name in sorted(os.listdir(d)):
        if not name.endswith((".yml", ".yaml")):
            continue
        _check_text(open(os.path.join(d, name), encoding="utf-8").read(),
                    f".github/workflows/{name}", fails)


def run():
    fails = []
    check_makefile(fails)
    check_precommit(fails)
    check_workflows(fails)
    for f in fails:
        print("FAIL  " + f)
    print("---- 编排面引用存在性（W1154）：%d FAIL ----" % len(fails))
    return 1 if fails else 0


def _self_test():
    """① 负样本：注入含不存在引用的文本必红；② 正样本：现役编排面 0 FAIL。"""
    fails = []
    _check_text("ci:\n\tpython scripts/_not_exist_w1154.py\n", "Makefile", fails)
    assert any("_not_exist_w1154" in f for f in fails), "负样本未判红"
    fails.clear()
    _check_text("ci:\n\tpython scripts/check_structure.py\n", "Makefile", fails)
    assert not fails, "正样本误报"
    return 0


def main():
    ap = argparse.ArgumentParser(description="编排面引用存在性门禁（W1154）")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return _self_test()
    return run()


if __name__ == "__main__":
    sys.exit(main())
