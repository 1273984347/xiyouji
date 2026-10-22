#!/usr/bin/env python3
"""_w862_tokenize_spacing.py — W862 B1 间距值保留式令牌化（一次性迁移件）。

口径（W862 认领行）：只把 padding/margin 家族里**与 v4 间距刻度精确等值**的
字面量换成 var(--space-N)——不等值（6/10/14/16/18/22px 等）一律不动，
保证计算样式零变化（由 J2 探针对拍兜底验证）。

安全面：
- 跳过 `<!-- INLINED CSS` 标记到对应 `</style>` 的内联块（防把
  `--space-3: 8px` 定义自身改成 `var(--space-3)` 循环·也防改出与
  site/tokens.css 单一事实源的分裂）；
- 只认 padding/margin 家族属性声明（含 scroll-padding 等）；
- 多值简写逐值替换（`padding: 12px 24px` → `padding: var(--space-4) var(--space-6)`）；
- 内联 style 属性同样处理；
- 0px/auto/百分比/em/rem 不碰。

用法：
    py -3 scripts/_w862_tokenize_spacing.py --dry <file...>   # 只报不写
    py -3 scripts/_w862_tokenize_spacing.py <file...>         # 应用
"""

import re
import sys

# v4 间距刻度（site/tokens.css W851 落地）→ 令牌名
SCALE = {
    "2px": "--space-1",
    "4px": "--space-2",
    "8px": "--space-3",
    "12px": "--space-4",
    "20px": "--space-5",
    "24px": "--space-6",
    "32px": "--space-7",
    "40px": "--space-8",
    "48px": "--space-9",
    "64px": "--space-10",
    "80px": "--space-11",
    "96px": "--space-12",
}

_PROP_RE = re.compile(
    r"(?P<prop>(?:scroll-)?(?:padding|margin)(?:-(?:top|right|bottom|left|block"
    r"|inline(?:-start|-end)?))?)\s*:\s*(?P<val>[^;{}\"<>]*)")
_PX_RE = re.compile(r"(?<![\w.-])(\d+)px(?![\w])")
_INLINE_RE = re.compile(r'style\s*=\s*"([^"]*)"')
_INLINE_BLOCK_RE = re.compile(
    r"<!--\s*INLINED CSS.*?</style>", re.S | re.I)


def _tok_value(val):
    """值列表逐 px 替换；返回 (新值, 替换数)。非刻度值原样留。"""
    n = 0

    def sub(m):
        nonlocal n
        lit = m.group(0)
        tok = SCALE.get(lit)
        if tok is None:
            return lit
        n += 1
        return "var(%s)" % tok

    return _PX_RE.sub(sub, val), n


def _strip_inlined(text):
    """把 INLINED CSS 块替换为占位符（内容不参与替换·结束后还原）。"""
    blocks = []

    def keep(m):
        blocks.append(m.group(0))
        return "\x00INLINED%d\x00" % (len(blocks) - 1)

    masked = _INLINE_BLOCK_RE.sub(keep, text)
    return masked, blocks


def tokenize(text):
    """返回 (新文本, [(prop, 原值, 新值), ...])。"""
    masked, blocks = _strip_inlined(text)
    out = []
    for m in _PROP_RE.finditer(masked):
        new_val, n = _tok_value(m.group("val"))
        if n:
            out.append((m.group("prop"), m.group("val").strip(), new_val.strip()))
    # 重建：按匹配位置逐段替换（_PROP_RE 的 val 组即替换区）
    result = []
    last = 0
    for m in _PROP_RE.finditer(masked):
        new_val, n = _tok_value(m.group("val"))
        if not n:
            continue
        result.append(masked[last:m.start("val")])
        result.append(new_val)
        last = m.end("val")
    result.append(masked[last:])
    new_text = "".join(result)
    # 还原 INLINED 块（按占位序号·块内容原样）
    new_text = re.sub(r"\x00INLINED(\d+)\x00",
                      lambda m: blocks[int(m.group(1))], new_text)
    return new_text, out


def main(argv):
    dry = "--dry" in argv
    files = [a for a in argv[1:] if not a.startswith("--")]
    if not files:
        print("用法：--dry <file...> ｜ <file...>")
        return 2
    total = 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        new_text, hits = tokenize(text)
        total += len(hits)
        print("%s %s：%d 处" % ("[DRY]" if dry else "[APPLY]", path, len(hits)))
        for prop, old, new in hits:
            print("    %s: %s → %s" % (prop, old, new))
        if not dry and hits:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new_text)
    print("合计 %d 处%s" % (total, "（dry-run 未写盘）" if dry else "已写盘"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
