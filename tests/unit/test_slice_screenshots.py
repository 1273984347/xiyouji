r"""W751 专项测试：scripts/slice_screenshots.py（整页截图切片 + 切片索引）

## 为什么测这个脚本（缺口取证）

W751 四面引用普查实测 slice_screenshots.py 属「无任何引用」清单——它只被
`pre_release_screenshot.py` 步骤 2 以「失败不阻塞」的方式调起，因此**自身坏了会静默**：
截图审查（人工/机器看切片）看到的是上一次的残留切片，而报告里写着「本次已切片」。
它同时是 W536 路径守卫的少数落地样本之一（`_w536_guard_open`），守卫语义也需要回归钉死。

## 覆盖判据（每条对应一个真实失效模式）

  S1 切片几何       → 高度不整除时最后一片被截断/丢尾（页脚内容丢失=审查盲区）
  S2 命名与顺序     → `_000/_001…` 编号错位会让审查者把两屏内容当成一屏
  S3 返回契约       → 相对路径必须是 posix 风格（Windows 反斜杠混进 md 表格）
  S4 clean_dir 精确 → 只删 png、只删目标目录（误删=截图全灭）
  S5 守卫语义       → scripts/ 外写入必须抛 SystemExit（W536 守卫回归）
  S6 索引报告结构   → desktop/mobile 两段 + 表头 + 每页一行（索引与切片同源）
  S7 重跑幂等       → 第二次运行不留旧编号残留（clean_dir 先于切片）

## 手法

图片一律现场生成（PIL，小尺寸）落 tmp_path；纯函数用例 monkeypatch `ss.ROOT`（它只决定
报告里的 posix 相对路径基准），CLI 端到端用例必须落在 scripts/ 内（W536 守卫语义：
`--output-dir` 不是逃逸口），用唯一命名子目录 scripts/output/_w751_slice_probe/ 并自清。

> **跨盘约束（实测发现·如实钉住）**：`slice_image` 用 `os.path.relpath(dst, ROOT)` 生成报告路径，
> Windows 下当 ROOT 在 D: 而输出目录在 C: 时 `relpath` 直接 `ValueError: path is on mount 'C:'`。
> 生产路径（脚本在 D:\xiyouji、输出默认 scripts/output/）同盘故不受影响；这条约束由 T_cross 用例
> 显式钉死，避免以后有人把输出目录挪到别的盘还以为是报告生成失败。
"""

import os
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import slice_screenshots as ss  # noqa: E402


def make_png(path, size, color=(200, 30, 30)):
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, color).save(path)


@pytest.fixture()
def shots(tmp_path):
    """构造 desktop/ + mobile/ 各两张图的截图目录（纯函数用例用·tmp_path 即可）。"""
    out = tmp_path / "screenshots"
    make_png(out / "desktop" / "index.png", (120, 2000))
    make_png(out / "desktop" / "dashboard.png", (120, 900))
    make_png(out / "mobile" / "index.png", (80, 1600))
    make_png(out / "mobile" / "dashboard.png", (80, 300))
    return out


def _probe_shot_dir():
    """main() 端到端用例必须落在 scripts/ 内（W536 守卫语义：--output-dir 不是逃逸口）。

    返回真实仓库 scripts/output/_w751_slice_probe/ —— 唯一命名，用例结束自清。
    """
    return Path(ss._W536_ROOT) / "output" / "_w751_slice_probe"


def _run_main_on_probe(slice_height=800, extra=()):
    out = _probe_shot_dir()
    if out.exists():
        import shutil

        shutil.rmtree(out)
    make_png(out / "desktop" / "index.png", (120, 2000))
    make_png(out / "desktop" / "dashboard.png", (120, 900))
    make_png(out / "mobile" / "index.png", (80, 1600))
    make_png(out / "mobile" / "dashboard.png", (80, 300))
    argv = ["slice_screenshots.py", "--output-dir", str(out), "--slice-height", str(slice_height), *extra]
    return out, argv


# ------------------------------------------------------------------- S1 切片几何
def test_s1_slice_count_and_last_chunk_height(tmp_path, monkeypatch):
    monkeypatch.setattr(ss, "ROOT", str(tmp_path))
    src = tmp_path / "page.png"
    make_png(src, (100, 2000))
    dst = tmp_path / "dst"
    dst.mkdir()
    chunks, (w, h), count = ss.slice_image(str(src), str(dst), 800)
    assert (w, h) == (100, 2000)
    assert count == 3, "2000/800 应为 3 片（800+800+400）"
    assert [Image.open(dst / f"page_{i:03d}.png").size for i in range(3)] == [(100, 800), (100, 800), (100, 400)]
    assert len(chunks) == 3, "最后一片必须落在 chunks 里（丢尾=页脚盲区）"


def test_s1b_slice_height_larger_than_image(tmp_path, monkeypatch):
    monkeypatch.setattr(ss, "ROOT", str(tmp_path))
    src = tmp_path / "small.png"
    make_png(src, (60, 200))
    dst = tmp_path / "dst"
    dst.mkdir()
    _chunks, _size, count = ss.slice_image(str(src), str(dst), 800)
    assert count == 1
    assert Image.open(dst / "small_000.png").size == (60, 200)


def test_s1c_content_positions_are_distinct_slices(tmp_path, monkeypatch):
    """条纹图逐片取中行色：证明切片边界按 y 递进而非重复同一块。"""
    monkeypatch.setattr(ss, "ROOT", str(tmp_path))
    src = tmp_path / "stripe.png"
    img = Image.new("RGB", (10, 40))
    for y in range(40):
        img.putpixel((5, y), (y * 6 % 256, 0, 0))
    img.save(src)
    dst = tmp_path / "dst"
    dst.mkdir()
    ss.slice_image(str(src), str(dst), 10)
    mids = [Image.open(dst / f"stripe_{i:03d}.png").getpixel((5, 5))[0] for i in range(4)]
    assert mids == [30, 90, 150, 210], "切片未按 y 递进（内容错位）"


def test_cross_drive_relpath_is_a_known_windows_constraint(tmp_path):
    """钉住跨盘约束：ROOT 与输出目录不同盘 → relpath ValueError（生产同盘不受影响）。"""
    src = tmp_path / "x.png"
    make_png(src, (10, 10))
    dst = tmp_path / "dst"
    dst.mkdir()
    root_drive = os.path.splitdrive(os.path.abspath(ss.ROOT))[0].upper()
    tmp_drive = os.path.splitdrive(os.path.abspath(str(tmp_path)))[0].upper()
    if root_drive == tmp_drive:
        pytest.skip("本机仓库与 tmp 同盘（%s），跨盘约束无法复现" % root_drive)
    with pytest.raises(ValueError) as ei:
        ss.slice_image(str(src), str(dst), 800)
    assert "mount" in str(ei.value)


# --------------------------------------------------------------- S2/S3 命名与返回契约
def test_s2_s3_naming_order_and_posix_relpath(tmp_path, monkeypatch):
    monkeypatch.setattr(ss, "ROOT", str(tmp_path))
    src = tmp_path / "src" / "p.png"
    make_png(src, (10, 25))
    dst = tmp_path / "out" / "slices"
    dst.mkdir(parents=True)
    chunks, _size, count = ss.slice_image(str(src), str(dst), 10)
    assert count == 3
    assert [os.path.basename(c) for c in chunks] == ["p_000.png", "p_001.png", "p_002.png"]
    assert all("\\" not in c for c in chunks), "反斜杠混进报告路径"
    assert all(c.startswith("out/slices/") for c in chunks)


# --------------------------------------------------------------------- S4 clean_dir
def test_s4_clean_dir_removes_only_png(tmp_path):
    dst = tmp_path / "d"
    dst.mkdir()
    make_png(dst / "a_000.png", (4, 4))
    make_png(dst / "a_001.png", (4, 4))
    (dst / "keep.txt").write_text("keep", encoding="utf-8")
    (dst / "sub").mkdir()
    make_png(dst / "sub" / "nested.png", (4, 4))
    ss.clean_dir(str(dst))
    assert not (dst / "a_000.png").exists() and not (dst / "a_001.png").exists()
    assert (dst / "keep.txt").exists(), "非 png 被误删"
    assert (dst / "sub" / "nested.png").exists(), "clean_dir 不得递归进子目录"


def test_s4b_clean_dir_missing_dir_is_noop(tmp_path):
    ss.clean_dir(str(tmp_path / "not-there"))  # 不抛异常即通过


# --------------------------------------------------------------------- S5 守卫语义
def test_s5_guard_blocks_outside_scripts_root(tmp_path):
    outside = tmp_path / "evil.txt"
    with pytest.raises(SystemExit) as ei:
        ss._w536_guard_open(str(outside), "w", encoding="utf-8")
    assert "W536 guard" in str(ei.value)
    assert not outside.exists(), "守卫必须拒绝且不落盘"


def test_s5b_guard_allows_inside_scripts_root():
    """在 scripts/ 下建唯一命名临时子目录，验证守卫放行 + 真实写入，用例自清。"""
    probe_dir = Path(ss._W536_ROOT) / "_w751_guard_probe"
    probe_dir.mkdir(exist_ok=True)
    probe = probe_dir / "ok.txt"
    try:
        with ss._w536_guard_open(str(probe), "w", encoding="utf-8") as f:
            f.write("ok")
        assert probe.read_text(encoding="utf-8") == "ok"
    finally:
        if probe.exists():
            probe.unlink()
        try:
            probe_dir.rmdir()
        except OSError:
            pass


# ----------------------------------------------------------------- S6 索引报告结构
def test_s6_index_report_two_viewports(monkeypatch):
    out, argv = _run_main_on_probe()
    try:
        monkeypatch.setattr(sys, "argv", argv)
        ss.main()
        index = (out / "slice-index.md").read_text(encoding="utf-8")
        assert index.startswith("# Screenshot Slice Index")
        assert "切片高度：800px" in index
        assert "## desktop" in index and "## mobile" in index
        assert index.count("| 页面 | 原始尺寸 | 切片数 | 切片路径 |") == 2, "两视口各一张表"
        for page, size, count in [("index", "120x2000", 3), ("dashboard", "120x900", 2)]:
            assert "| %s | %s | %d |" % (page, size, count) in index
        assert "| index | 80x1600 | 2 |" in index and "| dashboard | 80x300 | 1 |" in index
        assert (out / "slices" / "desktop" / "index_002.png").exists()
        assert (out / "slices" / "mobile" / "dashboard_000.png").exists()
        assert not (out / "slices" / "mobile" / "dashboard_001.png").exists(), "多切了一片"
    finally:
        import shutil

        shutil.rmtree(out, ignore_errors=True)


def test_s6b_main_refuses_output_dir_outside_scripts(tmp_path, monkeypatch):
    """--output-dir 指向 scripts/ 外时必须被拒绝（不许静默写仓外）。

    同盘 → W536 守卫 SystemExit；跨盘（tmp 在 C: 而仓在 D:）→ 更早的 relpath ValueError。
    两种都算拒绝，但**都必须不产出仓外索引文件**（判据取「拒绝且零落盘」，不锁死异常类型）。
    """
    outside = tmp_path / "shots"
    make_png(outside / "desktop" / "index.png", (10, 20))
    monkeypatch.setattr(sys, "argv", ["slice_screenshots.py", "--output-dir", str(outside)])
    with pytest.raises((SystemExit, ValueError)):
        ss.main()
    assert not (outside / "slice-index.md").exists()


# --------------------------------------------------------------------- S7 重跑幂等
def test_s7_rerun_leaves_no_stale_slices(monkeypatch):
    out, argv = _run_main_on_probe()
    try:
        monkeypatch.setattr(sys, "argv", argv)
        ss.main()
        stale = out / "slices" / "mobile" / "dashboard_009.png"
        make_png(stale, (80, 100))
        ss.main()
        assert not stale.exists(), "重跑必须清掉上一轮残留切片"
        assert len(list((out / "slices" / "mobile").glob("*.png"))) == 3, "残留导致切片数虚高"
    finally:
        import shutil

        shutil.rmtree(out, ignore_errors=True)
