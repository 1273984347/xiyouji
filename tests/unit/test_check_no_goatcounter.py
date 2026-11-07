r"""统计具名例外面对账守卫专项测试（W806 建 · W1167 判据重指向）

## 为什么测这个脚本

W806 的守卫形态是「GoatCounter 存在即红」。W1167 用户拍板 G0-1 把统计改为双轨具名例外
（GoatCounter 大陆面 + GA4 海外面），旧裁决被推翻——**但被推翻的是裁决，不是防线**：
现在真的存在外域统计面，失控风险比退役期更大。守卫因此从「不得存在」重指向
「必须等于具名例外全集」（判据定义见脚本头注 C1-C5）。

本测试的存在意义随之变为两条，缺一即失守：
① 越界形态必须命中对应 C 码（原防回退面）；
② **规范形态必须放行**（新增的正向证据——否则重指向只是换了个误报器，
   铁律 23「每条保护逻辑要配一条它真的生效的正向证据」）。

守卫自身若判据失效（模式写宽/写窄、忽略规则放水），该防线会静默归零——
项目 W663/W709 教训：门禁自身漂移要靠点检抓。W1167 实证形态：初版沿用
`data-goatcounter` 前缀子串，把导航正本的事件属性 `data-goatcounter-click` 误判成追踪标签，
现网直接 1 FAIL——两形态用途不同，必须分形态定义（G3 已锁住两种形态都拦）。

## 覆盖判据

  G1 现网实跑 0 FAIL（例外面 == 具名全集）
  G2 自检：`--self-test` 8/8（2 正 6 负）且退出码 0
  G3 判据单元：规范形态放行 + C1 无 MARK / C2 他人端点 / C3 影子脚本 /
     C4 第二写入口（标签与事件两形态）/ C5 双源分叉
  G4 忽略规则：守卫自身与 `__pycache__` 字节码不参与判定（自指误报防线）
  G5 CLI 退出码语义：现网实跑与自检形态均退出码 0

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
    """G2 自检：8/8（2 正 + 6 负）且退出码 0。"""
    res = _run("--self-test")
    assert res.returncode == 0, res.stdout + res.stderr
    assert res.stdout.count("PASS") == 8, res.stdout
    assert "SELF_TEST_OK" in res.stdout


def test_g3_judgements(tmp_path):
    """G3 判据单元：具名例外面越界分别命中 C1-C5，规范形态必须放行。"""
    site, scripts = _tree(tmp_path)
    truth = guard._load_truth()
    assert guard.scan(str(site), str(scripts), truth) == []

    # 正样本：规范形态（MARK + 正本端点 + 正本脚本路径）必须零 FAIL
    # ——W1167 重指向判据的核心正向证据：改造后的守卫不是「换了个误报器」
    (site / "static" / "js" / "goatcounter.js").write_text("// tracker\n", encoding="utf-8")
    (site / "a.html").write_text(
        '%s\n<script data-goatcounter="%s" async src="static/js/goatcounter.js"></script>\n'
        % (truth["mark"], truth["endpoint"]), encoding="utf-8")
    assert guard.scan(str(site), str(scripts), truth) == [], "规范形态被误判"

    # C1：有追踪标签、无 MARK（手工散落埋点）
    (site / "a.html").write_text(
        '<script data-goatcounter="%s" async src="static/js/goatcounter.js"></script>\n'
        % truth["endpoint"], encoding="utf-8")
    assert any(f.startswith("C1") for f in guard.scan(str(site), str(scripts), truth))

    # C2：端点被换成他人账号（例外面扩散）
    (site / "a.html").write_text(
        '%s\n<script data-goatcounter="https://someone-else.goatcounter.com/count" '
        'async src="static/js/goatcounter.js"></script>\n' % truth["mark"], encoding="utf-8")
    assert any(f.startswith("C2") for f in guard.scan(str(site), str(scripts), truth))

    # C3：第二份追踪脚本（影子文件；正本路径自身不算越界，上面正样本已证）
    (site / "a.html").unlink()
    (site / "static" / "js" / "goatcounter.js").unlink()
    (site / "static" / "js" / "goatcounter-legacy.js").write_text("// second\n", encoding="utf-8")
    assert any(f.startswith("C3") for f in guard.scan(str(site), str(scripts), truth))

    # C4：第二个写入口——标签形态与事件属性形态都要拦（W1167 实证前缀子串判据会混这两态）
    (site / "static" / "js" / "goatcounter-legacy.js").unlink()
    (scripts / "ad_hoc_inject.py").write_text('X = "data-goatcounter=\\"https://x\\""\n',
                                              encoding="utf-8")
    assert any(f.startswith("C4") for f in guard.scan(str(site), str(scripts), truth))
    (scripts / "ad_hoc_inject.py").write_text('X = \'data-goatcounter-click="nav-hacked"\'\n',
                                              encoding="utf-8")
    assert any(f.startswith("C4") for f in guard.scan(str(site), str(scripts), truth))
    (scripts / "ad_hoc_inject.py").unlink()

    # C5：配置端点与 CSP 白名单分叉
    desync = dict(truth)
    desync["csp_hosts"] = {"other.goatcounter.com"}
    assert any(f.startswith("C5") for f in guard.scan(str(site), str(scripts), desync))


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
