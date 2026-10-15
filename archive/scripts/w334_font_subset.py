#!/usr/bin/env python3
"""w334_font_subset.py — W334 字体子集化管线（零依赖运行时 · 本地托管）

流程：
  1. 扫描 docs/ + site/ 全部 .md/.html 文本，提取实际用字（CJK + ASCII + 全角标点）
  2. 用 pyftsubset 将源字体子集化为 woff2，输出到 site/static/fonts/

源字体（assets/fonts/source/）：
  - NotoSerifSC-var.ttf      思源宋体可变字重（google/fonts 官方仓库）
  - NotoSansSC-var.ttf       思源黑体可变字重
  - JetBrainsMono-Regular.ttf / JetBrainsMono-Medium.ttf

产物（site/static/fonts/）：
  - NotoSerifSC-VF.woff2     （可变字重 200-900，site/tokens.css 引用）
  - NotoSansSC-VF.woff2
  - JetBrainsMono-Regular.woff2 / JetBrainsMono-Medium.woff2

用法：
    python scripts/w334_font_subset.py
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "fonts" / "source"
OUT = ROOT / "site" / "static" / "fonts"
GLYPHS_TXT = ROOT / "scripts" / "output" / "glyphs.txt"

VENV_PY = Path(r"C:\Users\12739\.workbuddy\binaries\python\envs\default\Scripts\python.exe")
PY = str(VENV_PY if VENV_PY.exists() else Path(sys.executable))

FONTS = [
    ("NotoSerifSC-var.ttf", "NotoSerifSC-VF.woff2"),
    ("NotoSansSC-Regular.woff2", "NotoSansSC-Regular.woff2"),
    ("NotoSansSC-Medium.woff2", "NotoSansSC-Medium.woff2"),
    ("JetBrainsMono-Regular.ttf", "JetBrainsMono-Regular.woff2"),
    ("JetBrainsMono-Medium.ttf", "JetBrainsMono-Medium.woff2"),
]


def extract_glyphs() -> str:
    chars: set[str] = set()
    scan_dirs = [ROOT / "docs", ROOT / "site"]
    for base in scan_dirs:
        for p in base.rglob("*"):
            if p.suffix.lower() not in (".md", ".html"):
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            chars.update(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf]", text))
    # ASCII 可见字符 + 常用全角标点 + 项目符号
    chars.update(chr(c) for c in range(0x20, 0x7F))
    chars.update("，。、；：？！「」『』（）《》〈〉【】—…·×→←“”‘’％℃")
    glyphs = "".join(sorted(chars))
    GLYPHS_TXT.parent.mkdir(parents=True, exist_ok=True)
    GLYPHS_TXT.write_text(glyphs, encoding="utf-8")
    return glyphs


def subset_one(src: Path, dst: Path, glyphs: str) -> bool:
    cmd = [
        PY, "-m", "fontTools.subset",
        str(src),
        f"--text={glyphs}",
        "--flavor=woff2",
        f"--output-file={dst}",
        "--layout-features=*",
        "--name-IDs=*",
        "--notdef-outline",
        "--recalc-bounds",
        "--drop-tables+=FFTM",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [FAIL] {src.name}: {result.stderr.strip()[:400]}")
        return False
    size_kb = dst.stat().st_size / 1024
    print(f"  [OK] {dst.name}: {size_kb:.0f} KB")
    return True


def main() -> None:
    print("[INFO] 提取项目实际用字 ...")
    glyphs = extract_glyphs()
    print(f"[INFO] 字符数 {len(glyphs)}（含 ASCII 与全角标点）")

    OUT.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    for src_name, dst_name in FONTS:
        src, dst = SRC / src_name, OUT / dst_name
        if not src.exists():
            print(f"  [MISS] {src} 不存在，跳过")
            fail += 1
            continue
        print(f"[INFO] 子集化 {src_name} → {dst_name}")
        if subset_one(src, dst, glyphs):
            ok += 1
        else:
            fail += 1
    print(f"[DONE] 成功 {ok} / 失败 {fail}")
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
