#!/usr/bin/env python3
"""check_placeholder_hash_carrier.py — 构建期占位符不得落在 CSP 哈希载体上（第 71 槽 · W1210）

病根（坑表 E-225 已立正解，但只有人工一次性实测，无常驻机器判据）：
  静态产物用「构建期占位符 + 部署期替换」承载服务地址（契约 C-8）。若占位符落在
  **内联 <script> 块**内，部署期替换会改变该块字节 ⇒ `script-src 'sha256-…'` 哈希失配
  ⇒ **整段内联脚本被浏览器拒执行**（页面照常渲染、功能全废；静态审查看不出来——
  哈希由 generate_csp.py 算，注入脚本与生成器两侧代码各自「正确」）。
  同族第二形态：占位符落在 `<script src="…">` 属性值上 ⇒ 替换后成外域 URL ⇒
  CSP `script-src 'self' + sha256` 不含该域 ⇒ 外链脚本被拒（同族断链·静态同样看不出）。

判据（本槽四项）：
  C1 内联 <script> 块正文出现构建期占位符 ⇒ 判红（载体角色 inline_script）
  C2 <script src> 属性值出现构建期占位符 ⇒ 判红（载体角色 script_src）
  C3 产物面扫不到任何内联 <script> 块 ⇒ 判红（扫描面失效·防静默假绿·E-223 族）
  C4 其余载体（<meta> / 外部 JS / 内联 style / 其它文本）⇒ 登记不判红

口径同源（引用不复制纪律·W1120）：内联块的提取与哈希**直接 import generate_csp**
（`SCRIPT_RE` + `inline_script_hashes`），不复制正则字面量——第 56 槽是复制式
（注释写「必须逐字一致」），本槽改引用式以从根上杜绝两处正则分叉。

用法：
  py -3 scripts/check_placeholder_hash_carrier.py                    # 扫 site/
  py -3 scripts/check_placeholder_hash_carrier.py --root site --json out.json
  py -3 scripts/check_placeholder_hash_carrier.py --report           # 只报不判红
  py -3 scripts/check_placeholder_hash_carrier.py --self-test         # 负样本自证
  py -3 scripts/check_placeholder_hash_carrier.py --gate              # 门禁汇总行（第 71 槽）

退出码：0 = 无违规；1 = 有违规；2 = 自测失败 / 用法错误。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

# 口径单一事实源：内联 <script> 的提取与哈希由 generate_csp 定义（CSP 生成器）。
import generate_csp  # noqa: E402
from check_no_hardcoded_endpoint import PLACEHOLDER as SERVICE_BASE_PLACEHOLDER  # noqa: E402

#: 构建期占位符 token 集合：
#: ① 服务地址占位符取守卫脚本的单一事实源（check_no_hardcoded_endpoint.PLACEHOLDER）；
#: ② 通用形态 __XIJ_XXX__ —— 覆盖未来新增的构建期占位符（不必再改本判据）。
PLACEHOLDER_RE = re.compile(r"__XIJ_[A-Z0-9_]+__")

#: <script …> 起始标签（用于取 src 属性）。
SCRIPT_TAG_RE = re.compile(r"<script\b[^>]*>", re.IGNORECASE)

#: src 属性值（双引号 / 单引号 / 无引号三形态）。
SRC_ATTR_RE = re.compile(
    r"\bsrc\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))",
    re.IGNORECASE,
)

#: 文本扩展名（其余按二进制跳过·避免把图片当文本扫）。
TEXT_EXTS = frozenset({".html", ".htm", ".xhtml", ".js", ".mjs", ".cjs", ".css"})

#: 扫描时跳过的目录。
SKIP_DIRS = frozenset({".git", "node_modules", ".venv", "__pycache__", ".cache"})

#: 载体角色取值（登记用·C4 不判红）。
ROLE_INLINE_SCRIPT = "inline_script"
ROLE_SCRIPT_SRC = "script_src"
ROLE_META = "meta"
ROLE_CSP_META = "csp_meta"
ROLE_EXTERNAL_JS = "external_js"
ROLE_STYLE = "style"
ROLE_OTHER = "other"

#: 判红的角色（C1/C2）。
RED_ROLES = frozenset({ROLE_INLINE_SCRIPT, ROLE_SCRIPT_SRC})


def _norm_token(token: str) -> str:
    """占位符 token 归一（去空白·便于报告）。"""
    return token.strip()


def find_placeholders(text: str) -> list[str]:
    """返回文本中出现的构建期占位符 token 列表（按出现顺序·去重保序）。"""
    seen = []
    for m in PLACEHOLDER_RE.finditer(text):
        tok = _norm_token(m.group(0))
        if tok not in seen:
            seen.append(tok)
    return seen


def inline_blocks(html: str) -> list[tuple[int, str]]:
    """返回该页内联 <script> 块 [(起始偏移, 正文)]（口径同 generate_csp·纯空白块跳过）。

    块正文与 generate_csp.inline_script_hashes 的哈希输入**逐字相同**——
    块序与该函数返回的哈希列表一一对应（第 i 块 ↔ hashes[i]）。
    """
    out = []
    for m in generate_csp.SCRIPT_RE.finditer(html):
        body = m.group(1)
        if not body.strip(" \t\r\n"):
            continue
        out.append((m.start(), body))
    return out


def _line_of(text: str, offset: int) -> int:
    """偏移量所在行号（1 起）。"""
    return text.count("\n", 0, offset) + 1


def _script_src_hits(text: str) -> list[tuple[int, str]]:
    """返回 [(偏移, 命中 token)] —— <script src> 属性值内的占位符。"""
    out = []
    for m in SCRIPT_TAG_RE.finditer(text):
        tag = m.group(0)
        if "src" not in tag.lower():
            continue
        sm = SRC_ATTR_RE.search(tag)
        if not sm:
            continue
        value = next((g for g in sm.groups() if g is not None), "")
        for tok in find_placeholders(value):
            out.append((m.start(), tok))
    return out


def _meta_hits(text: str) -> list[tuple[int, str, str]]:
    """返回 [(偏移, 角色, 命中 token)] —— <meta …> 标签内的占位符（合法载体·登记用）。

    CSP 声明面（<meta http-equiv="Content-Security-Policy">）单独归类为 csp_meta：
    它**不参与** sha256 计算（它就是哈希的来源），替换后 connect-src 仍合法 ⇒ 合法载体；
    但与「旁挂 meta（如 <meta name="xij-service-base">）」性质不同，须分开登记，
    以免将来被误当违规加豁免、或被误判为哈希载体。
    """
    out = []
    for m in re.finditer(r"<meta\b[^>]*>", text, re.IGNORECASE):
        tag = m.group(0)
        role = ROLE_CSP_META if "content-security-policy" in tag.lower() else ROLE_META
        for tok in find_placeholders(tag):
            out.append((m.start(), role, tok))
    return out


def scan_html(rel_path: str, text: str) -> tuple[list[dict], list[dict], int]:
    """扫描单页 HTML ⇒ (违规, 登记, 内联块数)。"""
    violations = []
    registry = []
    blocks = inline_blocks(text)
    hashes = generate_csp.inline_script_hashes(text)

    # C1：内联 <script> 块正文内的占位符（哈希载体·替换即失配）
    for idx, (offset, body) in enumerate(blocks):
        toks = find_placeholders(body)
        if not toks:
            continue
        digest = ""
        if idx < len(hashes):
            digest = hashes[idx].replace("'sha256-", "")[:12]
        for tok in toks:
            violations.append({
                "file": rel_path,
                "line": _line_of(text, offset),
                "role": ROLE_INLINE_SCRIPT,
                "token": tok,
                "block_index": idx + 1,
                "block_hash12": digest,
                "reason": "占位符落在内联 <script> 块内（sha256 哈希载体）·部署期替换即哈希失配⇒整块脚本被浏览器拒执行",
            })

    # C2：<script src> 属性值内的占位符（外链载体·替换后成外域⇒script-src 不含该域）
    for offset, tok in _script_src_hits(text):
        violations.append({
            "file": rel_path,
            "line": _line_of(text, offset),
            "role": ROLE_SCRIPT_SRC,
            "token": tok,
            "block_index": 0,
            "block_hash12": "",
            "reason": "占位符落在 <script src> 属性值上·替换后成外域 URL⇒CSP script-src 不含该域⇒外链脚本被拒",
        })

    # C4：其余载体登记（<meta> / CSP 声明面等非哈希载体·合法）
    for offset, role, tok in _meta_hits(text):
        registry.append({
            "file": rel_path,
            "line": _line_of(text, offset),
            "role": role,
            "token": tok,
            "note": ("CSP 声明面·不参与 sha256 计算·替换后仍合法"
                     if role == ROLE_CSP_META
                     else "meta 载体·不受 CSP 哈希约束·合法"),
        })
    return violations, registry, len(blocks)


def scan_code(rel_path: str, text: str) -> list[dict]:
    """扫描非 HTML 文本件（外部 JS / 内联 style 等）⇒ 登记（不判红）。"""
    out = []
    role = ROLE_EXTERNAL_JS if rel_path.endswith((".js", ".mjs", ".cjs")) else ROLE_STYLE
    for m in PLACEHOLDER_RE.finditer(text):
        out.append({
            "file": rel_path,
            "line": _line_of(text, m.start()),
            "role": role,
            "token": _norm_token(m.group(0)),
            "note": "非哈希载体·合法（外部脚本不受 sha256 约束）",
        })
    return out


def iter_text_files(root: str):
    """遍历 root 下可读文本文件（跳过二进制扩展名与隐藏目录）。"""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(filenames):
            ext = os.path.splitext(fn)[1].lower()
            if ext not in TEXT_EXTS:
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, encoding="utf-8") as f:
                    yield path, f.read()
            except (OSError, UnicodeDecodeError):
                continue


def scan_roots(roots: list[str]) -> dict:
    """扫描多个 root，汇总结果。"""
    violations = []
    registry = []
    scanned = 0
    inline_total = 0
    html_pages = 0
    for root in roots:
        if not os.path.isdir(root):
            continue
        for path, text in iter_text_files(root):
            scanned += 1
            try:
                rel = os.path.relpath(path, os.getcwd())
            except ValueError:
                rel = path
            rel = rel.replace("\\", "/")
            if rel.endswith((".html", ".htm", ".xhtml")):
                v, r, nb = scan_html(rel, text)
                violations.extend(v)
                registry.extend(r)
                inline_total += nb
                html_pages += 1
            else:
                registry.extend(scan_code(rel, text))
    return {
        "scanned_files": scanned,
        "html_pages": html_pages,
        "inline_blocks": inline_total,
        "violations": violations,
        "registry": registry,
    }


def evaluate(roots: list[str]) -> dict:
    """主判定：C1 + C2 + C3 兜底。"""
    result = scan_roots(roots)
    issues = list(result["violations"])
    if result["inline_blocks"] == 0:
        issues.append({
            "file": "-",
            "line": 0,
            "role": "scan_surface",
            "token": "-",
            "block_index": 0,
            "block_hash12": "",
            "reason": "产物面扫不到任何内联 <script> 块⇒判据扫描面失效或产物形态变更（fail-closed·不得静默放行）",
        })
    return {
        "ok": not issues,
        "roots": roots,
        "scanned_files": result["scanned_files"],
        "html_pages": result["html_pages"],
        "inline_blocks": result["inline_blocks"],
        "violation_count": len(issues),
        "violations": issues,
        "registry_count": len(result["registry"]),
        "registry": result["registry"],
    }


def self_test() -> int:
    """负样本自证：违例必红 / 合法形态必绿 / 扫描面失效必红 / 口径同源。"""
    import tempfile

    cases = []
    tmpdir = tempfile.mkdtemp(prefix="xij_phc_guard_")
    try:
        def write(name, content):
            p = os.path.join(tmpdir, name)
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
            return p

        ph = SERVICE_BASE_PLACEHOLDER
        write("violation.html",
              "<html><head><script>const B='%s'; fetch(B);</script></head></html>" % ph)
        write("src_violation.html",
              "<html><head><script src=\"%s/app.js\"></script></head></html>" % ph)
        write("meta_ok.html",
              "<html><head><meta name=\"xij-service-base\" content=\"%s\"></head>"
              "<body>x</body></html>" % ph)
        write("external_ok.js", "const B = '%s';\n" % ph)

        def run(names):
            res = evaluate([tmpdir])
            return [v for v in res["violations"]
                    if os.path.basename(v.get("file", "")) in names]

        checks = [
            ("T1 内联 <script> 内占位符必红", len(run({"violation.html"})) == 1),
            ("T2 <script src> 属性占位符必红", len(run({"src_violation.html"})) == 1),
            ("T3 <meta> 载体占位符必绿", len(run({"meta_ok.html"})) == 0),
            ("T4 外部 JS 占位符必绿", len(run({"external_ok.js"})) == 0),
        ]

        # T5 扫描面兜底：必须**独占目录**测（同目录若另有内联块则 inline_blocks>0·不触发兜底）；
        # 兜底违规的 file 恒为 "-"（非文件名）⇒ 不能走按文件名的过滤路径。
        empty_dir = tempfile.mkdtemp(prefix="xij_phc_empty_")
        try:
            with open(os.path.join(empty_dir, "no_inline.html"), "w", encoding="utf-8") as f:
                f.write("<html><head><script src=\"static/js/app.js\"></script></head>"
                        "<body>x</body></html>")
            res_empty = evaluate([empty_dir])
            t5 = (len([v for v in res_empty["violations"]
                       if v.get("role") == "scan_surface"]) == 1)
        finally:
            for fn in os.listdir(empty_dir):
                try:
                    os.remove(os.path.join(empty_dir, fn))
                except OSError:
                    pass
            try:
                os.rmdir(empty_dir)
            except OSError:
                pass
        checks.append(("T5 无内联块时扫描面兜底必红", t5))

        # T6 口径同源：块正文与 generate_csp 逐字一致 ⇒ 哈希一致
        sample = "<html><body><script>\n  const a = 1;\n</script></body></html>"
        blocks = inline_blocks(sample)
        hashes = generate_csp.inline_script_hashes(sample)
        ok_same = (len(blocks) == len(hashes) == 1
                   and generate_csp.inline_script_hashes("<script>%s</script>" % blocks[0][1]) == hashes)
        checks.append(("T6 内联块口径与 generate_csp 同源", ok_same))

        # T7 正样本：合法页全绿
        ok_dir = tempfile.mkdtemp(prefix="xij_phc_ok_")
        try:
            with open(os.path.join(ok_dir, "ok.html"), "w", encoding="utf-8") as f:
                f.write("<html><head><meta name=\"xij-service-base\" content=\"%s\"></head>"
                        "<body><script>var x=1;</script></body></html>" % ph)
            ok_res = evaluate([ok_dir])
            checks.append(("T7 合法页整体通过（违规 0）", ok_res["ok"] and ok_res["violation_count"] == 0))
        finally:
            for fn in os.listdir(ok_dir):
                try:
                    os.remove(os.path.join(ok_dir, fn))
                except OSError:
                    pass
            try:
                os.rmdir(ok_dir)
            except OSError:
                pass

        for name, ok in checks:
            cases.append((name, ok))
            print(("PASS  " if ok else "FAIL  ") + name)
        failed = [n for n, ok in cases if not ok]
        if failed:
            print("自测结论：失败 %d 例：%s" % (len(failed), "、".join(failed)))
        else:
            print("自测结论：全部通过（%d/%d）" % (len(cases), len(cases)))
        return 0 if not failed else 2
    finally:
        for fn in os.listdir(tmpdir):
            try:
                os.remove(os.path.join(tmpdir, fn))
            except OSError:
                pass
        try:
            os.rmdir(tmpdir)
        except OSError:
            pass


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_placeholder_hash_carrier.py",
        description="构建期占位符不得落在 CSP 哈希载体上（第 71 槽 · W1210）",
    )
    parser.add_argument("--root", action="append", default=None,
                        help="扫描根目录（可多次·默认 site）")
    parser.add_argument("--json", default=None, help="结果 JSON 落盘路径")
    parser.add_argument("--report", action="store_true", help="只报不判红（退出码恒 0）")
    parser.add_argument("--self-test", action="store_true", help="负样本自证（造临时件·跑完即删）")
    parser.add_argument("--gate", action="store_true",
                        help="门禁模式：输出汇总行（第 71 槽挂载用）")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    roots = args.root or ["site"]
    report = evaluate(roots)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    print("扫描根：%s · 文本文件 %d 个 · HTML %d 页 · 内联脚本块 %d 个"
          % (", ".join(roots), report["scanned_files"], report["html_pages"],
             report["inline_blocks"]))
    print("违规 %d · 非哈希载体登记 %d" % (report["violation_count"], report["registry_count"]))
    for v in report["violations"]:
        print("  [违规] %s:%d  %s  token=%s%s  %s"
              % (v["file"], v["line"], v["role"], v["token"],
                 ("  块#%d 哈希 %s" % (v["block_index"], v["block_hash12"]))
                 if v["block_index"] else "",
                 v["reason"]))
    for r in report["registry"]:
        print("  [登记] %s:%d  %s  token=%s  %s"
              % (r["file"], r["line"], r["role"], r["token"], r.get("note", "")))
    if args.gate:
        print("---- 第 71 门禁 占位符哈希载体：违规 %d · %s ----"
              % (report["violation_count"], "OK" if report["ok"] else "FAIL"))
    if args.report:
        return 0
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
