r"""
analyzer_base.py — 《西游记》分析脚本通用入口。

用途：
    消除 34 类分析脚本中重复的样板代码（argparse / 加载文本 / 写 JSON /
    打印进度）。新脚本只需实现 analyze_fn(chapters, args) -> dict，
    调用 run_analyzer 即可。

用法示例：

    # my_analyzer.py
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from utils.analyzer_base import run_analyzer

    def analyze(chapters, args=None):
        # chapters: list[tuple[str, str]]，每项为 (回目名, 文本)
        return {"total": len(chapters)}

    if __name__ == "__main__":
        run_analyzer(
            name="my_analyzer",
            analyze_fn=analyze,
            default_output="output/data/my_analyzer.json",
            extra_args=[("--top", {"type": int, "default": 100,
                                    "help": "前 N 个"})],
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

# 添加项目 scripts 目录到 sys.path（用于 import utils.text_loader）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.text_loader import load_all_chapters, load_text  # noqa: I001 禁 isort 重排·本 import 必须位于 sys.path.insert 之后（引导顺序）


# 项目根与默认分回目录（提为模块级常量·避免每次调用重复上溯）
_PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
_DEFAULT_CHAPTERS_DIR: Path = _PROJECT_ROOT / "source" / "原文" / "分回"


def _default_input_dir() -> Path:
    """返回项目标准分回目录：source/原文/分回/。"""
    return _DEFAULT_CHAPTERS_DIR


def _load_chapters(input_path: Path) -> list[tuple[str, str]]:
    """加载章节文本：目录走 load_all_chapters，单文件走 load_text。"""
    if input_path.is_dir():
        return load_all_chapters(input_path)
    return [(input_path.stem, load_text(input_path))]


def _build_arg_parser(
    name: str,
    default_output: str | None,
    extra_args: list | None,
) -> argparse.ArgumentParser:
    """构建统一命令行解析器。

    参数：
        name: 脚本名（用于描述与默认输出路径）
        default_output: 默认输出路径
        extra_args: 额外参数列表，[(flag, kwargs), ...]

    返回：
        配置完毕的 ArgumentParser。
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
    return parser


def _resolve_input_path(args, name: str) -> Path:
    """根据 --input 解析实际输入路径，缺失则回退到默认分回目录。

    参数：
        args: 已解析的 argparse 命名空间
        name: 脚本名（用于错误消息）

    返回：
        存在的输入路径。

    异常：
        路径不存在时打印错误并以退出码 1 结束进程（保持历史行为）。
    """
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(
                f"[ERROR] [{name}] 输入路径不存在：{input_path}",
                file=sys.stderr,
            )
            sys.exit(1)
        return input_path

    input_path = _default_input_dir()
    if not input_path.exists():
        print(
            f"[ERROR] [{name}] 默认分回目录不存在：{input_path}\n"
            f"        请通过 --input 指定路径",
            file=sys.stderr,
        )
        sys.exit(1)
    return input_path


def _invoke_analyze(analyze_fn, chapters, args):
    """调用 analyze_fn，自动兼容 1 参 / 2 参签名。

    若 analyze_fn 接受 >= 2 个参数，则传 (chapters, args)；
    否则仅传 chapters（向后兼容旧脚本）。
    """
    sig = inspect.signature(analyze_fn)
    if len(sig.parameters) >= 2:
        return analyze_fn(chapters, args)
    return analyze_fn(chapters)


def _write_json(result, output_path: Path) -> None:
    """将结果写为 UTF-8 JSON（ensure_ascii=False, indent=2）。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


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
                    例: [("--top", {"type": int, "default": 100,
                                    "help": "前 N 个"})]

    流程：
        1. argparse 解析 --input / --output / extra_args
        2. 加载文本（text_loader.load_all_chapters 或 load_text）
        3. 调用 analyze_fn 得到 dict
        4. 写 JSON（ensure_ascii=False, indent=2）
        5. 打印进度日志

    返回：
        analyze_fn 的返回值（dict）。
    """
    parser = _build_arg_parser(name, default_output, extra_args)
    args = parser.parse_args()

    input_path = _resolve_input_path(args, name)
    chapters = _load_chapters(input_path)
    print(f"[INFO] [{name}] 加载了 {len(chapters)} 个文件（来源：{input_path}）")

    result = _invoke_analyze(analyze_fn, chapters, args)

    output_path = Path(args.output)
    _write_json(result, output_path)
    print(f"[OK] [{name}] 结果已写入：{output_path}")

    return result
