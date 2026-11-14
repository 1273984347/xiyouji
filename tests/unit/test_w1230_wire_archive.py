r"""W1230 单元测试·跨批复用图像判据的实质执行面（check_crop / plates_verify / subject_band）。

## 为什么（W1230 批·审计专批裁决）

三件是 W983 定式「跨批复用判据不归档，转正留顶层」的转正件（W988/W1002/W1004），
但自转正起只有 import 冒烟、无任何实质执行面（2026-11-06 基础设施审计 §2.1 P2 实证）。
本批给三件各补一组合成图像判据测试：判据逻辑真实执行 + 正反样本可证伪。

  - check_crop.judge_og：og 卡顶边切墨判据（纯纸判绿 / 顶墨判红 / 体积超限判红）；
  - subject_band：连通簇主体检测（200px² 噪点过滤 / 朱砂排除 / 纯朱砂图返回空）；
  - plates_verify：负样本端到端（`--negative` 已知坏样本必须被抓出 = 判据可证伪）
    + 正样本判据原语（顶部留白 / 下部主体 / 整图墨量 / 朱砂点检）。

运行：py -m pytest tests/unit/test_w1230_wire_archive.py -v
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import check_crop
import plates_verify
import subject_band

PAPER = (250, 247, 240)
INK = (35, 32, 26)
VERM = (200, 70, 58)


def _paper_image(size):
    return Image.new("RGB", size, PAPER)


# ———————— check_crop ————————


def test_check_crop_judge_og_clean_paper_passes():
    """纯纸 og：无违例（判据判定面真实执行）。"""
    assert check_crop.judge_og(_paper_image(check_crop.OG_SIZE)) == []


def test_check_crop_judge_og_top_ink_caught():
    """顶部 20px 墨块（> 容忍 12px）⇒ 必须判红（W1044 判据可证伪）。"""
    im = _paper_image(check_crop.OG_SIZE)
    for x in range(10, 30):
        im.putpixel((x, 0), INK)
    fails = check_crop.judge_og(im)
    assert any("顶边切墨" in f for f in fails), fails


def test_check_crop_judge_og_wrong_size_and_bytes():
    """尺寸不符与体积超限两条独立违例都要被抓出。"""
    im = _paper_image((600, 400))
    fails = check_crop.judge_og(im, size_bytes=check_crop.OG_MAX_BYTES + 1)
    assert any("og 尺寸" in f for f in fails)
    assert any("体积" in f for f in fails)


def test_check_crop_self_test_via_cli():
    """CLI --self-test 真跑（负样本自证路径走 subprocess 全链）。"""
    r = subprocess.run([sys.executable, str(SCRIPTS / "check_crop.py"), "--self-test"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=120, cwd=str(ROOT))
    assert r.returncode == 0, r.stdout + r.stderr


# ———————— subject_band ————————


def _strip_with_noise():
    """300×400 纸面：顶部 1 个 5px 孤立墨点（<200px² 噪点）+ y=250 起 220px² 大墨簇。"""
    im = _paper_image((300, 400))
    px = im.load()
    for dx in range(2):          # 2×2=4px 噪点（远小于 MIN_CLUSTER_AREA=200）
        for dy in range(2):
            px[50 + dx, 30 + dy] = INK
    for yy in range(250, 340):   # 90×80=7200px 大簇
        for xx in range(100, 180):
            px[xx, yy] = INK
    return im


def test_subject_band_filters_small_noise_cluster():
    """连通簇法：顶部孤立噪点不得把主体顶拉到噪点处（W974 教训判据）。"""
    top, bottom, n = subject_band.subject_band(_strip_with_noise())
    assert top is not None and n >= subject_band.MIN_CLUSTER_AREA
    assert top >= 200, "主体顶 %s 被噪点拉歪（应 ≥200=大簇上缘）" % top
    assert top <= 260, "主体顶 %s 漏检大簇（应 ≈250）" % top
    assert bottom > top


def test_subject_band_excludes_vermilion():
    """朱砂属点睛非主体：纯朱砂大簇 ⇒ body_mask 空 ⇒ 返回 (None, None, 0)。"""
    im = _paper_image((300, 400))
    px = im.load()
    for yy in range(100, 300):
        for xx in range(100, 200):
            px[xx, yy] = VERM
    top, bottom, n = subject_band.subject_band(im)
    assert (top, bottom, n) == (None, None, 0)


def test_subject_band_empty_paper():
    assert subject_band.subject_band(_paper_image((100, 100))) == (None, None, 0)


# ———————— plates_verify ————————


def _synthetic_plate():
    """1200×1600 合成题图：顶部纯纸 / 下部 220×220 墨簇 / 朱砂点睛——按 J1-J5 规格取值。"""
    im = _paper_image(plates_verify.TARGET)
    px = im.load()
    for yy in range(800, 1020):          # 下部 72% 主体区（h*0.28=448 之后）
        for xx in range(400, 620):
            px[xx, yy] = INK
    for yy in range(900, 904):
        for xx in range(700, 704):
            px[xx, yy] = VERM            # J5 朱砂点（>0 即可）
    return im


def test_plates_verify_positive_primitives():
    """正样本判据原语：顶部留白≈0 / 下部墨量 ≥ J4_MIN / 整图墨量 ∈ [J3_LO, J3_HI] / 朱砂 > 0。"""
    im = _synthetic_plate()
    w, h = im.size
    top = plates_verify.ink_ratio(im, (0, 0, w, int(h * 0.10)))
    lower = plates_verify.ink_ratio(im, (0, int(h * 0.28), w, h))
    whole = plates_verify.ink_ratio(im)
    verm = plates_verify.near_px(im, plates_verify.VERM, plates_verify.VERM_TOL)
    assert top <= plates_verify.J2_MAX, "顶部留白 %s" % top
    assert lower >= plates_verify.J4_MIN, "下部主体墨量 %s" % lower
    assert plates_verify.J3_LO <= whole <= plates_verify.J3_HI, "整图墨量 %s" % whole
    assert verm > 0, "朱砂点缺失"


def test_plates_verify_negative_check_catches_bad_sample(tmp_path):
    """负样本端到端：16:9 浓墨图走 `--negative` 必须被判据抓出（可证伪性·rc=0=抓出）。"""
    bad = _paper_image((800, 450))
    px = bad.load()
    for yy in range(0, 450, 2):
        for xx in range(0, 800, 2):
            px[xx, yy] = INK             # 16:9 + 半屏浓墨：J1/J3/J6 多重违例
    p = tmp_path / "bad-sample.png"
    bad.save(p)
    r = subprocess.run([sys.executable, str(SCRIPTS / "plates_verify.py"),
                        "--negative", str(p)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=120, cwd=str(ROOT))
    assert r.returncode == 0, "坏样本未被任何判据抓出（判据恒真）:\n%s%s" % (
        r.stdout[-500:], r.stderr[-200:])
    assert "判据可证伪" in r.stdout


def test_plates_verify_constants_contract():
    """判据常量契约钉：画幅 1200×1600（3:4）·阈值常量在位（防规格漂移静默改判据）。"""
    assert plates_verify.TARGET == (1200, 1600)
    assert plates_verify.PAPER == (250, 247, 240)
    assert plates_verify.VERM == (200, 70, 58)
    assert 0 < plates_verify.J2_MAX < plates_verify.J3_LO
