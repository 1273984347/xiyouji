r"""W806 专项测试：scripts/check_no_goatcounter.py（GoatCounter 退役防回退守卫）

## 为什么测这个脚本

W806 裁决「彻底退役 GoatCounter」后，防回退面只剩这一道机器防线：页面若被重新
注入埋点标签、或 CSP 又放行该外域，**没有其他门禁会红**（CSP 漂移门禁只校验
「meta 与生成器输出一致」，不校验「该不该放行这个域」；脚本覆盖门禁只管脚本存废）。
守卫自身若判据失效（模式写宽/写窄、忽略规则放水），该防线会静默归零——
项目 W663/W709 教训：门禁自身漂移要靠点检抓。

## 覆盖判据

  G1 现网实跑 0 FAIL（当前仓库真实状态·退役已落地）
  G2 自检：`--self-test` 5/5（1 正 4 负）且退出码 0
  G3 判据单元：scan() 对四类回退（埋点标签 / 外域放行 / 追踪脚本文件 / 注入器文件）
     必须给出对应 C1-C4 码
  G4 忽略规则：守卫自身与 `__pycache__` 字节码不参与判定（自指误报防线）
  G5 CLI 退出码语义：现网实跑退出码 0（自检形态退出码亦为 0）

## 手法

判据用 scan() 注入构造（系统临时目录合成树·两平台同构·不触仓库）；CLI 面走
subprocess（真实入口，含退出码语义）。
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_no_goatcounter as guard  # noqa: E402

GATE = SCRIPTS / "check_no_goatcounter.py"


def _run(*args, timeout=180):
    return subprocess.run(
        [sys.executable, str(GATE), *args],
        capture_output=True, text=True, timeout=timeout, cwd=str(ROOT),
    )


def _tree(tmp_path):
    """构造合成树：site/ 与 scripts/ 各建一棵，返回 (site, scripts)。"""
    site = tmp_path / "site"
    scripts = tmp_path / "scripts"
    (site / "static" / "js").mkdir(parents=True)
    scripts.mkdir(parents=True)
    (site / "index.html").write_text("<html><head></head><body>ok</body></html>\n",
                                     encoding="utf-8")
    return site, scripts


def test_g1_repo_clean():
    """G1 现网实跑：0 FAIL（退役已落地）。"""
    res = _run()
    assert res.returncode == 0, res.stdout + res.stderr
    assert "0 FAIL" in res.stdout


def test_g2_self_test():
    """G2 自检：5/5 且退出码 0。"""
    res = _run("--self-test")
    assert res.returncode == 0, res.stdout + res.stderr
    assert res.stdout.count("PASS") == 5, res.stdout
    assert "SELF_TEST_OK" in res.stdout


def test_g3_judgements(tmp_path):
    """G3 判据单元：四类回退分别命中 C1-C4。"""
    site, scripts = _tree(tmp_path)
    assert guard.scan(str(site), str(scripts)) == []

    # C1 埋点标签
    (site / "a.html").write_text(
        '<script data-goatcounter="https://x.goatcounter.com/count" async '
        'src="../static/js/goatcounter.js"></script>\n', encoding="utf-8")
    assert any(f.startswith("C1") for f in guard.scan(str(site), str(scripts)))

    # C2 外域放行残留（CSP connect-src）
    (site / "a.html").write_text(
        '<meta http-equiv="Content-Security-Policy" '
        'content="connect-src \'self\' https://1273984347.goatcounter.com">\n',
        encoding="utf-8")
    assert any(f.startswith("C2") for f in guard.scan(str(site), str(scripts)))

    # C3 站点残留追踪脚本
    (site / "a.html").unlink()
    (site / "static" / "js" / "goatcounter.js").write_text("// tracker\n", encoding="utf-8")
    assert any(f.startswith("C3") for f in guard.scan(str(site), str(scripts)))

    # C4 工具残留注入器
    (site / "static" / "js" / "goatcounter.js").unlink()
    (scripts / "inject_goatcounter.py").write_text("# injector\n", encoding="utf-8")
    assert any(f.startswith("C4") for f in guard.scan(str(site), str(scripts)))


def test_g4_ignore_rules(tmp_path):
    """G4 忽略规则：守卫自身与 __pycache__ 字节码不参与判定（自指误报防线）。"""
    site, scripts = _tree(tmp_path)
    # 合成树内放一个同名守卫 → 仍不应被判 C4
    (scripts / "check_no_goatcounter.py").write_text("# copy\n", encoding="utf-8")
    # 字节码产物 → 不应被判 C4
    pyc_dir = scripts / "__pycache__"
    pyc_dir.mkdir()
    (pyc_dir / "inject_goatcounter.cpython-312.pyc").write_bytes(b"\x00")
    fails = guard.scan(str(site), str(scripts))
    assert fails == [], fails


def test_g5_cli_exit_codes():
    """G5 CLI 退出码语义：现网与自检形态均 0。"""
    assert _run().returncode == 0
    assert _run("--self-test").returncode == 0
