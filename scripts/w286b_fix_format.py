"""
W286b 格式修复脚本：
1. source/原文/分回/第NNN回.txt → 第NNN回.md（添加 # 标题头）
2. source/原文/temp_shendu/SDxxx.txt → source/原文/shendu/SDxxx.md（去 temp_ 前缀 + .md）
3. 删除旧的 .txt 文件和 temp_shendu 目录
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FENHUI_DIR = ROOT / "source" / "原文" / "分回"
OLD_SHENDU_DIR = ROOT / "source" / "原文" / "temp_shendu"
NEW_SHENDU_DIR = ROOT / "source" / "原文" / "shendu"
MD_DIR = ROOT / "docs" / "01-全书逐回解读"


def get_chapter_title(n: int) -> str:
    """从 docs/01-全书逐回解读/第NNN回-*.md 提取回目标题"""
    pattern = f"第{n:03d}回-*.md"
    matches = list(MD_DIR.glob(pattern))
    if not matches:
        return f"第{n:03d}回"
    md_file = matches[0]
    # 文件名格式：第NNN回-回目摘要.md
    name = md_file.stem  # 第NNN回-回目摘要
    # 提取回目摘要部分
    parts = name.split("-", 1)
    if len(parts) > 1:
        return f"第{n:03d}回 {parts[1]}"
    return f"第{n:03d}回"


def convert_fenhui():
    """分回 .txt → .md，添加标题头"""
    count = 0
    for txt_file in sorted(FENHUI_DIR.glob("第*回.txt")):
        # 提取回号
        m = re.match(r"第(\d+)回", txt_file.stem)
        if not m:
            continue
        n = int(m.group(1))
        title = get_chapter_title(n)

        # 读取原文
        content = txt_file.read_text(encoding="utf-8").strip()

        # 生成 .md 内容：标题头 + 原文
        md_content = f"# {title}\n\n{content}\n"

        # 写入 .md
        md_file = txt_file.with_suffix(".md")
        md_file.write_text(md_content, encoding="utf-8")

        # 删除 .txt
        txt_file.unlink()
        count += 1

    print(f"[分回] 转换 {count} 个 .txt → .md")
    return count


def convert_shendu():
    """temp_shendu/SDxxx.txt → shendu/SDxxx.md"""
    if not OLD_SHENDU_DIR.exists():
        print("[shendu] temp_shendu 目录不存在，跳过")
        return 0

    # 创建新目录
    NEW_SHENDU_DIR.mkdir(parents=True, exist_ok=True)

    count = 0
    for txt_file in sorted(OLD_SHENDU_DIR.glob("SD*.txt")):
        # 读取内容
        content = txt_file.read_text(encoding="utf-8").strip()

        # 提取 SD 编号和标题（从元数据注释中）
        # 格式: <!-- 深读编号: 1 | 标题: xxx | 推测对应原著回号: ... -->
        sd_num = txt_file.stem  # SD001
        title_match = re.search(r"标题:\s*(.+?)(?:\s*\|)", content)
        title = title_match.group(1).strip() if title_match else sd_num

        # 生成 .md 内容：标题头 + 原内容
        md_content = f"# {sd_num} · {title}\n\n{content}\n"

        # 写入新目录的 .md
        md_file = NEW_SHENDU_DIR / f"{sd_num}.md"
        md_file.write_text(md_content, encoding="utf-8")

        # 删除旧 .txt
        txt_file.unlink()
        count += 1

    # 删除旧的 temp_shendu 目录
    try:
        OLD_SHENDU_DIR.rmdir()
        print(f"[shendu] 已删除 temp_shendu 目录")
    except OSError:
        print(f"[shendu] temp_shendu 目录非空，未删除")

    print(f"[shendu] 转换 {count} 个 .txt → .md（temp_shendu → shendu）")
    return count


if __name__ == "__main__":
    c1 = convert_fenhui()
    c2 = convert_shendu()
    print(f"\n完成：共转换 {c1 + c2} 个文件")
