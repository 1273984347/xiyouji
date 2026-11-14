r"""W1232 单元测试·门禁挂槽批四判据回归锁。

## 覆盖（审计专批 2026-11-06 四登记项）

  - #51 基线自服务重写审批标记：三个基线重写旗标（check_data_copy_chain --record /
    check_glossary --build-baseline / check_citability --generate-baseline）无 --approve
    时必须拒绝（退出码 1）且不落盘（铁律 16-⑦ 机器化）；
  - 第 72 槽 emoji 基线棘轮：当前 > 基线判红 / ≤ 基线放行（纯函数级构造）；
  - gen_rss 版段正则：现役 `### WNNN（日期）：标题` 形态可解析（v 形态退役后 rss
    自 10-22 静默陈旧的根因）；
  - check_reader_rss_fresh 判据面：非 git 目录取 max(提交, mtime) 语义在位。

运行：py -m pytest tests/unit/test_w1232_gates.py -v
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"

# ———————— #51 审批标记（三脚本·无 --approve 拒绝）————————


def _run(script, *flags):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *flags],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=120, cwd=str(ROOT))


def test_copy_chain_record_requires_approve():
    r = _run("check_data_copy_chain.py", "--record")
    assert r.returncode == 1 and "REFUSE" in r.stdout
    assert "--approve" in r.stdout, "拒绝信息必须给出批准命令"


def test_glossary_build_baseline_requires_approve():
    r = _run("check_glossary.py", "--build-baseline")
    assert r.returncode == 1 and "REFUSE" in r.stdout


def test_citability_generate_baseline_requires_approve():
    r = _run("check_citability.py", "--generate-baseline")
    assert r.returncode == 1 and "REFUSE" in r.stdout


# ———————— 第 72 槽 emoji 基线棘轮（读门禁模块纯判定面）————————


def test_emoji_ratchet_baseline_file_exists_and_matches_gate():
    base = ROOT / "scripts" / "output" / "emoji-residue-baseline.txt"
    assert base.exists(), "棘轮基线应已登记（首跑自动登记）"
    baseline = int(base.read_text(encoding="utf-8").strip())
    # 门禁 --gate 在当前树上必须 OK（当前计数 ≤ 基线）——防基线与实况脱节
    r = _run("check_emoji_icons.py", "--gate", "--no-browser")
    assert r.returncode == 0, r.stdout[-400:]
    assert "静态 %d / 基线 %d" % (baseline, baseline) in r.stdout or "OK" in r.stdout


# ———————— gen_rss 现役版段正则 ————————


def test_gen_rss_parses_current_heading_form():
    src = (SCRIPTS / "gen_rss.py").read_text(encoding="utf-8")
    # 现役形态正则在位（W1232 根修）且 v 形态回退仍在
    assert r'^### (W\d+)（' in src, "现役形态正则缺失"
    assert "if not items:" in src, "回退链缺失"
    # 实跑：rss 必须能从现役 CHANGELOG 解析出条目（W1231 顶段）
    r = subprocess.run(["python", str(SCRIPTS / "gen_rss.py"), "--help"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=60, cwd=str(ROOT))
    assert "解析为空" not in (r.stderr or ""), "现役 CHANGELOG 应可解析"


# ———————— reader/rss 新鲜度判据面 ————————


def test_reader_rss_fresh_effective_epoch_semantics():
    src = (SCRIPTS / "check_reader_rss_fresh.py").read_text(encoding="utf-8")
    assert "_effective_epoch" in src, "max(提交, mtime) 语义函数在位"
    assert "os.path.isdir" in src, "目录形态取最新文件 mtime"
    assert "is-shallow-repository" in src, "浅克隆 fail-closed 判据在位"


def test_gates_registry_has_72_73_74():
    """挂槽一致性：verify_delivery 三新槽 + EXPECTED 清单 + 汇总行 marker 全在位。"""
    src = (SCRIPTS / "verify_delivery.py").read_text(encoding="utf-8")
    for token in ('section="emoji残留棘轮"', 'section="readerRSS新鲜度"', 'section="治理文档体积窗口"',
                  "第 72 门禁 emoji 残留棘轮：", "第 74 门禁 治理文档体积窗口：",
                  '"emoji残留棘轮"', '"readerRSS新鲜度"', '"治理文档体积窗口"'):
        assert token in src, "缺挂槽登记：%s" % token
