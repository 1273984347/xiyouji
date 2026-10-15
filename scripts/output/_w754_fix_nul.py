"""W754 一次性修复：CHANGELOG.md 与 scripts/output/file-index.md 的 NUL 转义残留 + 行尾归一。

背景：W736 批 spec 的 file_index_rows 含 JSON 转义 `\\u0000`，落盘时被写成**真 NUL 字节**
（CHANGELOG W736 段、file-index W736 段各 1 处），使两文件被编辑器判为二进制、且静默污染文本。
本脚本把真 NUL 还原为字面 `\\u0000` 两字符序列的转义写法，并保证文件为纯 CRLF（与两文件 HEAD blob 一致）。
幂等：重复执行无副作用。
"""
import sys

TARGETS = ["CHANGELOG.md", "scripts/output/file-index.md"]
fail = 0
for P in TARGETS:
    b = open(P, "rb").read()
    n_nul = b.count(b"\x00")
    if n_nul:
        b = b.replace(b"\x00", b"\\u0000")
    # 兜底：修正曾被 shell 转义放大成双反斜杠的写法
    t = b.decode("utf-8").replace("\\\\u0000", "\\u0000")
    assert "\x00" not in t
    assert "\n" not in t.replace("\r\n", ""), P + " 存在裸 LF（须先归一再级联）"
    open(P, "w", encoding="utf-8", newline="").write(t)
    b2 = open(P, "rb").read()
    print(f"{P}: NUL 修复 {n_nul} 处 · CRLF={b2.count(chr(13).encode()+chr(10).encode())} · bareLF=0")
    fail += n_nul
print("合计修复 NUL:", fail)
sys.exit(0)
