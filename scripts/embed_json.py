"""embed_json.py — 通用 JSON 嵌入工具

用途：
  将外部 JSON 数据嵌入到 HTML 文件中的 EMBEDDED JavaScript 对象，使其在
  file:// 协议下可被直接访问（无需 fetch 外部 JSON，绕过浏览器对本地文件
  fetch 的安全限制）。用于替代 w102_embed_timeline.py / w102_embed_safe.py /
  w102_reembed.py 三份临时脚本。

参数：
  --html <path>       目标 HTML 文件路径
  --json <path>       数据 JSON 文件路径
  --key <name>        嵌入到 EMBEDDED 对象的键名
  --mode <mode>       insert（默认，新增键）或 replace（替换已有键）
  --no-backup         不备份原文件到 .bak（默认会备份）

示例：
  # 新增键
  python embed_json.py --html site/data/relationships.html \
                       --json scripts/output/data/cooccurrence_timeline.json \
                       --key cooccurrence_timeline

  # 替换已有键
  python embed_json.py --html site/data/relationships.html \
                       --json scripts/output/data/cooccurrence.json \
                       --key cooccurrence --mode replace

  # 不备份
  python embed_json.py --html site/data/relationships.html \
                       --json scripts/output/data/x.json --key x --no-backup

设计要点：
  - 纯标准库实现（argparse / json / re / pathlib / shutil）
  - 用括号深度计数精确定位 EMBEDDED 对象边界，避免正则贪婪匹配截断后续内容
    （吸取 w102_embed_timeline.py 失败教训，沿用 w102_embed_safe.py 思路）
  - EMBEDDED 对象不存在时自动注入空 EMBEDDED 声明（兼容 const/let/var/window.）
  - insert 模式下若键已存在则报错，避免重复插入；replace 模式下键不存在则报错
  - JSON 解析失败时明确报错并退出码 2
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

# 匹配 const/let/var/window.EMBEDDED = {
EMBEDDED_PATTERN = re.compile(
    r'(?:const|let|var)\s+EMBEDDED\s*=\s*\{|window\.EMBEDDED\s*=\s*\{'
)


def find_embedded_bounds(html: str):
    """定位 EMBEDDED 对象的 { 与匹配 } 索引（含括号）。

    返回 (start_brace_index, end_brace_index)；未找到返回 None。
    """
    m = EMBEDDED_PATTERN.search(html)
    if not m:
        return None
    brace_start = m.end() - 1  # 指向 {
    depth = 0
    for i in range(brace_start, len(html)):
        c = html[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return brace_start, i
    return None


def find_field_bounds(html: str, brace_start: int, brace_end: int, key: str):
    """在 EMBEDDED 对象 [brace_start, brace_end] 内查找 `<key>: { ... }` 字段。

    返回字段值对象字面量的 { } 索引（含括号）；未找到返回 None。
    沿用 w102_reembed.py 的简单正则思路：EMBEDDED 顶层 key 名冲突概率极低。
    """
    field_pattern = re.compile(r'\b' + re.escape(key) + r'\s*:\s*\{')
    m = field_pattern.search(html, brace_start, brace_end)
    if not m:
        return None
    val_start = m.end() - 1  # 指向 {
    depth = 0
    for i in range(val_start, brace_end + 1):
        c = html[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return val_start, i
    return None


def ensure_embedded_exists(html: str) -> str:
    """若 EMBEDDED 对象不存在，注入空 EMBEDDED 声明。

    注入位置优先级：`</head>` 前 > `</body>` 前 > 文件末尾。
    """
    if EMBEDDED_PATTERN.search(html):
        return html
    inject = (
        '    <script>\n'
        '        const EMBEDDED = {};\n'
        '    </script>\n'
    )
    head_close = html.find('</head>')
    if head_close != -1:
        return html[:head_close] + inject + html[head_close:]
    body_close = html.find('</body>')
    if body_close != -1:
        return html[:body_close] + inject + html[body_close:]
    return html + '\n' + inject


def insert_key(html: str, brace_start: int, brace_end: int, key: str, json_str: str) -> str:
    """在 EMBEDDED 对象末尾插入 `<key>: <json_str>`。"""
    inner = html[brace_start + 1: brace_end].strip()
    is_empty = (inner == '')

    # 找闭合 } 之前最后一个非空白字符
    j = brace_end - 1
    while j > brace_start and html[j] in ' \t\n\r':
        j -= 1
    last_char = html[j]

    if is_empty or last_char == ',':
        insert_text = f'\n        {key}: {json_str}\n    '
    else:
        insert_text = f',\n        {key}: {json_str}\n    '

    return html[:brace_end] + insert_text + html[brace_end:]


def replace_key(html: str, brace_start: int, brace_end: int, key: str, json_str: str) -> str:
    """替换 EMBEDDED 对象中已有 `<key>: { ... }` 字段的值。"""
    field_bounds = find_field_bounds(html, brace_start, brace_end, key)
    if field_bounds is None:
        raise KeyError(
            f'字段 "{key}" 未在 EMBEDDED 对象中找到，无法替换。'
            f'请改用 --mode insert 新增。'
        )
    val_start, val_end = field_bounds
    return html[:val_start] + json_str + html[val_end:]


def main():
    parser = argparse.ArgumentParser(
        description='将 JSON 数据嵌入到 HTML 的 EMBEDDED JavaScript 对象（file:// 协议友好）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            '示例:\n'
            '  python embed_json.py --html site/data/relationships.html \\\n'
            '       --json scripts/output/data/cooccurrence_timeline.json \\\n'
            '       --key cooccurrence_timeline\n'
            '\n'
            '  python embed_json.py --html site/data/relationships.html \\\n'
            '       --json scripts/output/data/cooccurrence.json \\\n'
            '       --key cooccurrence --mode replace\n'
        ),
    )
    parser.add_argument('--html', required=True, help='目标 HTML 文件路径')
    parser.add_argument('--json', required=True, help='数据 JSON 文件路径')
    parser.add_argument('--key', required=True, help='嵌入到 EMBEDDED 对象的键名')
    parser.add_argument(
        '--mode', choices=['insert', 'replace'], default='insert',
        help='insert（默认）新增键；replace 替换已有键',
    )
    parser.add_argument(
        '--no-backup', action='store_true',
        help='不备份原文件到 .bak（默认会备份）',
    )
    args = parser.parse_args()

    html_path = Path(args.html)
    json_path = Path(args.json)

    if not html_path.exists():
        print(f'[ERROR] HTML 文件不存在: {html_path}', file=sys.stderr)
        sys.exit(1)
    if not json_path.exists():
        print(f'[ERROR] JSON 文件不存在: {json_path}', file=sys.stderr)
        sys.exit(1)

    # 读取 & 解析 JSON
    try:
        raw_json = json_path.read_text(encoding='utf-8')
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        print(f'[ERROR] JSON 解析失败 ({json_path}): {e}', file=sys.stderr)
        sys.exit(2)
    except OSError as e:
        print(f'[ERROR] 读取 JSON 失败 ({json_path}): {e}', file=sys.stderr)
        sys.exit(2)
    json_str = json.dumps(data, ensure_ascii=False)

    # 读取 HTML
    try:
        html = html_path.read_text(encoding='utf-8')
    except OSError as e:
        print(f'[ERROR] 读取 HTML 失败 ({html_path}): {e}', file=sys.stderr)
        sys.exit(2)
    original_size = len(html)

    # 自动创建 EMBEDDED 声明（若不存在）
    html = ensure_embedded_exists(html)

    # 定位 EMBEDDED 对象边界
    bounds = find_embedded_bounds(html)
    if bounds is None:
        print('[ERROR] 无法定位 EMBEDDED 对象边界', file=sys.stderr)
        sys.exit(3)
    brace_start, brace_end = bounds

    # 模式校验：insert 模式下键不应已存在；replace 模式下键应已存在
    if args.mode == 'insert' and find_field_bounds(html, brace_start, brace_end, args.key) is not None:
        print(
            f'[ERROR] 键 "{args.key}" 已存在于 EMBEDDED 对象中，'
            f'请改用 --mode replace 或换一个键名',
            file=sys.stderr,
        )
        sys.exit(4)

    # 执行嵌入
    try:
        if args.mode == 'insert':
            new_html = insert_key(html, brace_start, brace_end, args.key, json_str)
        else:
            new_html = replace_key(html, brace_start, brace_end, args.key, json_str)
    except KeyError as e:
        print(f'[ERROR] {e}', file=sys.stderr)
        sys.exit(4)

    # 备份原文件
    if not args.no_backup:
        bak_path = html_path.with_suffix(html_path.suffix + '.bak')
        try:
            shutil.copy2(html_path, bak_path)
            print(f'[INFO] 备份原文件到 {bak_path}')
        except OSError as e:
            print(f'[WARN] 备份失败: {e}', file=sys.stderr)

    # 写回
    try:
        html_path.write_text(new_html, encoding='utf-8')
    except OSError as e:
        print(f'[ERROR] 写入 HTML 失败 ({html_path}): {e}', file=sys.stderr)
        sys.exit(5)

    delta = len(new_html) - original_size
    print(f'[OK] EMBEDDED.{args.key} 已以 {args.mode} 模式嵌入到 {html_path}')
    print(f'[OK] 文件大小: {original_size} -> {len(new_html)} bytes ({delta:+d})')


if __name__ == '__main__':
    main()
