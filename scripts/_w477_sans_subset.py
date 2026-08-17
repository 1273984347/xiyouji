#!/usr/bin/env python3
"""W477 Noto Sans SC 子集化（一次性诊断脚本，不入门禁/CI）

复用 W334 管线口径（scripts/archive/w334_font_subset.py）：
扫 docs/ + site/ 全部 .md/.html 实际用字（CJK + ASCII + 全角标点），
将 assets/fonts/source/ 的 NotoSansSC 全量源子集化后覆写 site/static/fonts/ 同名文件。
文件名不变，tokens.css @font-face 无需改动。

用法：python scripts/_w477_sans_subset.py
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "fonts" / "source"
OUT = ROOT / "site" / "static" / "fonts"
GLYPHS_TXT = ROOT / "scripts" / "output" / "glyphs.txt"

FONTS = [
    ("NotoSansSC-Regular.woff2", "NotoSansSC-Regular.woff2"),
    ("NotoSansSC-Medium.woff2", "NotoSansSC-Medium.woff2"),
]


def extract_glyphs() -> str:
    chars = set()
    for base in (ROOT / "docs", ROOT / "site"):
        for p in base.rglob("*"):
            if p.suffix.lower() not in (".md", ".html"):
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            chars.update(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf]", text))
    chars.update(chr(c) for c in range(0x20, 0x7F))
    chars.update("，。、；：？！「」『』（）《》〈〉【】—…·×→←“”‘’％℃～")
    glyphs = "".join(sorted(chars))
    GLYPHS_TXT.parent.mkdir(parents=True, exist_ok=True)
    GLYPHS_TXT.write_text(glyphs, encoding="utf-8")
    return glyphs


def subset_one(src: Path, dst: Path, glyphs: str) -> bool:
    cmd = [
        sys.executable, "-m", "fontTools.subset",
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
    print(f"  [OK] {dst.name}: {dst.stat().st_size / 1024:.0f} KB")
    return True


def main() -> None:
    glyphs = extract_glyphs()
    print(f"[INFO] 字符数 {len(glyphs)}（含 ASCII 与全角标点）")
    ok = fail = 0
    for src_name, dst_name in FONTS:
        src, dst = SRC / src_name, OUT / dst_name
        if not src.exists():
            print(f"  [MISS] {src} 不存在，跳过")
            fail += 1
            continue
        print(f"[INFO] 子集化 {src_name} → site/static/fonts/{dst_name}")
        if subset_one(src, dst, glyphs):
            ok += 1
        else:
            fail += 1
    print(f"[DONE] 成功 {ok} / 失败 {fail}")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
