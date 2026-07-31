"""
W286c 审查修复脚本：
1. 清除 source/原文/分回/第069回.md 和 第099回.md 的网页垃圾内容
2. 同步修复 docs/01-全书逐回解读/第069回.md 和 第099回.md 的原文全文
3. 第099回.md 追加缺失的 ## 深度解读 章节（SD075）
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 垃圾内容模式（shicimingju.com 网页导航广告）
JUNK_PATTERN = r"你的每一分钱.*?西游记\r?\n"


def clean_fenhui(chapter: int):
    """清除分回 .md 的网页垃圾"""
    fenhui = ROOT / "source" / "原文" / "分回" / f"第{chapter:03d}回.md"
    content = fenhui.read_text(encoding="utf-8")

    # 移除垃圾内容块（从"你的每一分钱"到"西游记\n"）
    cleaned = re.sub(JUNK_PATTERN, "", content, flags=re.DOTALL)

    if cleaned != content:
        fenhui.write_text(cleaned, encoding="utf-8")
        print(f"[分回] 第{chapter:03d}回.md 清除垃圾内容 ✓")
        return cleaned
    else:
        print(f"[分回] 第{chapter:03d}回.md 未发现垃圾内容")
        return None


def clean_and_fix_doc01(chapter: int, shendu_dir: Path):
    """修复 docs/01 的原文全文 + 第099回追加深度解读"""
    md_dir = ROOT / "docs" / "01-全书逐回解读"
    matches = list(md_dir.glob(f"第{chapter:03d}回-*.md"))
    if not matches:
        print(f"[docs/01] 第{chapter:03d}回.md 未找到")
        return
    md_file = matches[0]
    content = md_file.read_text(encoding="utf-8")

    # 1. 清除原文全文中的垃圾内容
    # 替换垃圾内容块为空
    cleaned = re.sub(JUNK_PATTERN, "", content, flags=re.DOTALL)

    # 2. 第099回追加深度解读（在 ## 原文全文 之前插入）
    if chapter == 99:
        # 读取 SD075 深读切片
        sd075 = shendu_dir / "SD075.md"
        if sd075.exists():
            sd_content = sd075.read_text(encoding="utf-8")
            # 提取 SD075 正文（去掉标题行和元数据注释）
            sd_body = sd_content
            # 去掉第一行标题（# SD075 · ...）
            lines = sd_body.split("\n")
            # 找到正文开始位置（跳过标题行和空行和注释行）
            body_start = 0
            for i, line in enumerate(lines):
                if line.startswith("# SD075"):
                    body_start = i + 1
                    continue
                if body_start > 0 and line.startswith("<!--") and line.endswith("-->"):
                    body_start = i + 1
                    continue
                if body_start > 0 and line.strip() == "":
                    body_start = i + 1
                    continue
                if body_start > 0:
                    break

            sd_body = "\n".join(lines[body_start:]).strip()

            # 提取标题
            sd_title_match = re.search(r"# SD075 · (.+)", sd_content)
            sd_title = sd_title_match.group(1).strip() if sd_title_match else "通天河——当取经人回到原来的渡口"

            # 构建深度解读章节
            shendu_section = f"## 深度解读\n\n### SD075 · {sd_title}\n\n{sd_body}\n\n---\n\n"

            # 在 ## 原文全文 之前插入
            cleaned = cleaned.replace("## 原文全文", shendu_section + "## 原文全文")
            print(f"[docs/01] 第099回.md 追加深度解读 SD075 ✓")

    if cleaned != content:
        md_file.write_text(cleaned, encoding="utf-8")
        print(f"[docs/01] 第{chapter:03d}回.md 修复完成 ✓")
    else:
        print(f"[docs/01] 第{chapter:03d}回.md 无需修复")


if __name__ == "__main__":
    shendu_dir = ROOT / "source" / "原文" / "shendu"

    # P1: 清除分回垃圾内容
    print("=== P1: 清除分回垃圾内容 ===")
    clean_fenhui(69)
    clean_fenhui(99)

    # P1+P2: 同步修复 docs/01
    print("\n=== P1+P2: 修复 docs/01 ===")
    clean_and_fix_doc01(69, shendu_dir)
    clean_and_fix_doc01(99, shendu_dir)

    print("\n修复完成")
