r"""
analyzer_base.py — 《西游记》分析脚本通用入口

用途：
    消除 34 类分析脚本中重复的样板代码（argparse / 加载文本 / 写 JSON / 打印进度）。
    新脚本只需实现 analyze_fn(chapters, args) -> dict，调用 run_analyzer 即可。

用法示例：

    # my_analyzer.py
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from utils.analyzer_base import run_analyzer

    def analyze(chapters, args=None):
        # chapters: list[tuple[str, str]]，每项为 (回目名, 文本)
        return {"total": len(chapters)}

    if __name__ == "__main__":
        run_analyzer(
            name="my_analyzer",
            analyze_fn=analyze,
            default_output="output/data/my_analyzer.json",
            extra_args=[("--top", {"type": int, "default": 100, "help": "前 N 个"})],
        )

    # CLI: python my_analyzer.py [--input PATH] [--output PATH] [--top N]

设计要点：
    - --input 可选：默认使用项目标准分回目录 source/原文/分回/
      支持传入目录（load_all_chapters）或单文件（load_text）
    - --output 可选：默认 output/data/<name>.json
    - extra_args：额外 argparse 参数，[(flag, kwargs), ...]
    - analyze_fn 签名：analyze_fn(chapters, args=None) -> dict
      若函数只接受一个参数，则仅传 chapters（向后兼容）
    - chapters 类型：list[tuple[str, str]]，与 text_loader.load_all_chapters 一致
"""

import argparse
import inspect
import json
import sys
from pathlib import Path

# 添加项目 scripts 目录到 sys.path（用于 import text_loader）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.text_loader import load_text, load_all_chapters


def _default_input_dir() -> Path:
    """返回项目标准分回目录：source/原文/分回/。"""
    project_root = Path(__file__).resolve().parent.parent.parent
    return project_root / "source" / "原文" / "分回"


def _load_chapters(input_path: Path) -> list[tuple[str, str]]:
    """加载章节文本：目录走 load_all_chapters，单文件走 load_text。"""
    if input_path.is_dir():
        return load_all_chapters(input_path)
    return [(input_path.stem, load_text(input_path))]


def run_analyzer(
    name: str,
    analyze_fn,
    *,
    default_output: str = None,
    extra_args: list = None,
):
    """通用分析脚本入口。

    参数：
        name: 脚本名（用于日志与默认输出文件名）
        analyze_fn: 分析函数，签名 analyze_fn(chapters, args=None) -> dict
                    若只接受 1 个参数，则仅传 chapters
        default_output: 默认输出路径（默认 output/data/<name>.json）
        extra_args: 额外 argparse 参数，形如 [(flag, kwargs), ...]
                    例: [("--top", {"type": int, "default": 100, "help": "前 N 个"})]

    流程：
        1. argparse 解析 --input / --output / extra_args
        2. 加载文本（text_loader.load_all_chapters 或 load_text）
        3. 调用 analyze_fn 得到 dict
        4. 写 JSON（ensure_ascii=False, indent=2）
        5. 打印进度日志
    """
    parser = argparse.ArgumentParser(description=f"《西游记》{name} 分析")
    parser.add_argument(
        "--input",
        default=None,
        help="输入路径：分回目录或单文件（默认 source/原文/分回/）",
    )
    parser.add_argument(
        "--output",
        default=default_output or f"output/data/{name}.json",
        help="输出 JSON 路径",
    )
    if extra_args:
        for flag, kwargs in extra_args:
            parser.add_argument(flag, **kwargs)
    args = parser.parse_args()

    # 解析输入路径
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"[ERROR] [{name}] 输入路径不存在：{input_path}", file=sys.stderr)
            sys.exit(1)
    else:
        input_path = _default_input_dir()
        if not input_path.exists():
            print(
                f"[ERROR] [{name}] 默认分回目录不存在：{input_path}\n"
                f"        请通过 --input 指定路径",
                file=sys.stderr,
            )
            sys.exit(1)

    # 加载文本
    chapters = _load_chapters(input_path)
    print(f"[INFO] [{name}] 加载了 {len(chapters)} 个文件（来源：{input_path}）")

    # 调用分析函数（兼容 1 参 / 2 参签名）
    sig = inspect.signature(analyze_fn)
    if len(sig.parameters) >= 2:
        result = analyze_fn(chapters, args)
    else:
        result = analyze_fn(chapters)

    # 写 JSON
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] [{name}] 结果已写入：{output_path}")

    return result
