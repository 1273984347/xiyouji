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
# W1231：站点页面实际用 `const EMBEDDED_DATA = {`（EMBEDDED_DATA 与 EMBEDDED 两名并存）
# ——原模式只认 EMBEDDED 名 ⇒ 对 EMBEDDED_DATA 页找不到嵌入点（实测 46 页用 EMBEDDED_DATA / 26 页用 EMBEDDED·W1231 实测）。
EMBEDDED_PATTERN = re.compile(
    r'(?:const|let|var)\s+(?:EMBEDDED_DATA|EMBEDDED)\s*=\s*\{|window\.EMBEDDED(?:_DATA)?\s*=\s*\{'
)


def _member_line_re(key: str):
    """成员行正则：行首缩进 + `<key>:` + 值开头（对象/数组双形态）。"""
    return re.compile(r'^(\s*)' + re.escape(key) + r'\s*:\s*([\[{])')


def _scan_balanced(text: str, start: int, end: int, open_ch: str, close_ch: str):
    """字符串感知的括号配对扫描（W1231 回退路径·仅空对象/单行形态使用）。

    字符串字面量（' " ` 三种引号·含反斜杠转义）内不计数。巨长文案页在深嵌套下
    可能失步（W1231 实证 17 页）——那类页面恒由行锚定路径接管，本扫描只是
    空对象 `const EMBEDDED = {};` / 单行形态的兜底（test_e3/e4/e9 夹具形态）。
    返回配对闭合字符的索引；未闭合返回 None。
    """
    depth = 0
    quote = None
    i = start
    while i <= end:
        c = text[i]
        if quote is not None:
            if c == '\\':
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in ('\'', '"', '`'):
            quote = c
        elif c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return None


def _line_anchored_bounds(html: str, key: str):
    """W1231 根修：行锚定成员定位（取代逐字符括号扫描）。

    为什么改算法：EMBEDDED 块里字符串值/注释可能含 `{}`/`[]`（relationships 页实测：
    洞察文案含引号+括号混排，逐字符扫描（含字符串感知版）在多页上边界失步 ⇒
    replace 把值写进错误 span、整页脚本语法损坏 17 页）。而本仓页面成员统一为
    embed_json insert 的既定行格式——`\\n        key: <值>` 行首对齐、块尾 `\\n    };`
    ⇒ 成员边界用**行锚定**判定：成员行 = 匹配 `^\\s*key\\s*:\\s*[\\[{]` 的行；
    值 span = 该行值首字符到「下一成员行或块尾行」之前最后一个闭合括号字符。
    返回 (val_start, val_end)（含括号）；未找到返回 None。
    """
    m = EMBEDDED_PATTERN.search(html)
    if not m:
        return None
    end_block_re = re.compile(r'^\s*\};\s*$', re.M)
    block_end = end_block_re.search(html, m.end())
    if not block_end:
        return None
    # 成员行集合（声明行到块尾之间·缩进须与首个成员行一致——嵌套行缩进不同·防误切）
    seg_start = m.end()
    seg = html[seg_start:block_end.start()]
    raw_members = []
    for lm in re.finditer(r'^(\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:\s*([\[{])', seg, re.M):
        raw_members.append((seg_start + lm.start(), lm.group(2), lm.group(1)))
    if not raw_members:
        return None
    # 缩进归一化：首成员的 ^(\s*) 捕获含前置换行（re.M 在段首匹配）——剥离 CR/LF 后比较
    def _norm(ind):
        return ind.replace('\r', '').replace('\n', '')
    root_indent = _norm(raw_members[0][2])
    member_positions = [(pos, k) for pos, k, ind in raw_members if _norm(ind) == root_indent]
    target = None
    for pos, k in member_positions:
        if k == key:
            target = pos
            break
    if target is None:
        return None
    target_idx = member_positions.index((target, key))
    next_pos = member_positions[target_idx + 1][0] if target_idx + 1 < len(member_positions) else block_end.start()
    # 值起点：成员行上 key: 之后的 { 或 [
    line_re = re.compile(_member_line_re(key).pattern, re.M)
    lm = line_re.search(html, target, next_pos)
    if not lm:
        return None
    val_start = lm.end() - 1
    # 值终点：next_pos 之前最后一个闭合括号字符（} 或 ]——成员值的外层闭合）
    region = html[val_start:next_pos]
    close_candidates = [i for i, ch in enumerate(region) if ch in '}]']
    if not close_candidates:
        return None
    val_end = val_start + close_candidates[-1]
    return val_start, val_end


def find_embedded_bounds(html: str):
    """定位 EMBEDDED 对象的 { 与匹配 } 索引（W1231 行锚定优先·字符串感知扫描回退）。

    返回 (start_brace_index, end_brace_index)；未找到返回 None。
    ① 多行形态：块尾 = 声明后第一个行首 `};`（embed_json insert 的既定块格式）；
    ② 回退（空对象 `const EMBEDDED = {};` / 单行形态·ensure 注入与 V8 重写产物）：
       行锚定块尾不存在 ⇒ 字符串感知括号扫描（_scan_balanced）——空对象/短字面量
       上边界精确；巨长文案页才会失步，而它们恒走 ①。
    """
    m = EMBEDDED_PATTERN.search(html)
    if not m:
        return None
    brace_start = m.end() - 1  # 指向 {
    end_block_re = re.compile(r'^\s*\};\s*$', re.M)
    block_end = end_block_re.search(html, m.end())
    if block_end:
        # 块尾行的 `}` 位置 = 该行首个 `}`
        brace_end = html.index('}', block_end.start())
        return brace_start, brace_end
    brace_end = _scan_balanced(html, brace_start, len(html) - 1, '{', '}')
    if brace_end is None:
        return None
    return brace_start, brace_end


def find_field_bounds(html: str, brace_start: int, brace_end: int, key: str):
    """在 EMBEDDED 对象内查找 `<key>: {...}` 或 `<key>: [...]` 字段（W1231 行锚定）。

    返回字段值字面量的起止索引（含括号）；未找到返回 None。
    历史：W102 系逐字符括号深度计数（含 W1231 中途版的字符串感知变体）在
    「洞察文案含引号/括号混排」的多页上边界失步 ⇒ 17 页 replace 后语法损坏
    （relationships/aesthetics/text-evolution 等实测）。行锚定以 embed_json 自己
    的 insert 行格式为准，成员边界不再依赖括号配对。
    """
    bounds = _line_anchored_bounds(html, key)
    if not bounds:
        return None
    return bounds


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
    """替换 EMBEDDED 对象中已有 `<key>: { ... }` / `<key>: [...]` 字段的值。

    W1231 根修（off-by-one）：find_field_bounds 返回的 val_end 是**含闭合括号**的索引，
    原实现 `html[val_end:]` 把旧闭合括号再拼一次 ⇒ 每次 replace 都产出 `}}`/`]]`
    ⇒ 页面脚本语法损坏。这正是「JSON 改稿后页面 EMBEDDED 从未重灌」的结构性根因
    （旧工具一重灌就坏页 ⇒ 快照永远停在旧版·476 条隐性值漂移即由此累积）。
    修法 = 值 span 闭区间替换：`html[val_end + 1:]`。
    """
    field_bounds = find_field_bounds(html, brace_start, brace_end, key)
    if field_bounds is None:
        raise KeyError(
            f'字段 "{key}" 未在 EMBEDDED 对象中找到，无法替换。'
            f'请改用 --mode insert 新增。'
        )
    val_start, val_end = field_bounds
    return html[:val_start] + json_str + html[val_end + 1:]


def _parse_args():
    """CLI 参数解析（W733 从 main 提取）。"""
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
    return parser.parse_args()


def _load_inputs(html_path, json_path):
    """读取并解析 JSON + HTML；错误路径打印 stderr 并以对应退出码终止（W733 提取）。"""
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
    return html, json_str


def _embed_key(html, args, json_str):
    """ensure 声明 + 定位边界 + 模式校验 + 执行嵌入；错误路径终止（W733 提取）。"""
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
            return insert_key(html, brace_start, brace_end, args.key, json_str)
        return replace_key(html, brace_start, brace_end, args.key, json_str)
    except KeyError as e:
        print(f'[ERROR] {e}', file=sys.stderr)
        sys.exit(4)


def _write_with_backup(html_path, new_html, no_backup):
    """备份原文件（可选 .bak）+ 写回；写失败终止（W733 提取）。"""
    # 备份原文件
    if not no_backup:
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


def main():
    args = _parse_args()

    html_path = Path(args.html)
    json_path = Path(args.json)

    html, json_str = _load_inputs(html_path, json_path)
    original_size = len(html)

    new_html = _embed_key(html, args, json_str)
    _write_with_backup(html_path, new_html, args.no_backup)

    delta = len(new_html) - original_size
    print(f'[OK] EMBEDDED.{args.key} 已以 {args.mode} 模式嵌入到 {html_path}')
    print(f'[OK] 文件大小: {original_size} -> {len(new_html)} bytes ({delta:+d})')


if __name__ == '__main__':
    main()
