#!/usr/bin/env python3
"""inject_service_endpoint.py — 静态产物服务地址注入（部署期）· W1205 契约 C-8

机制（构建期占位符 + 部署期替换）：
  ① 构建期：产物里写占位符 __XIJ_SERVICE_BASE__（不出现任何真实地址）；
  ② 部署期：本脚本把占位符替换成部署方自己的服务地址；
  ③ 开发者本机专用构建（--profile developer-local）：地址限定回环，且脚本会在产物内
     写入**显式标记** xij-build-profile:developer-local endpoint=<地址>——
     守卫据此豁免，豁免可审计（产物内可见 + 清单落盘）。

硬约束（契约 C-8）：
  - 默认档（--profile default）**拒绝**回环/内网地址（fail-closed，不静默降级）；
  - 开发者本机档**必须**是回环地址（否则说明档位用错）；
  - 产物里的占位符若未被替换，--check 判红（部署完整性门禁）。

用法：
  py -3 scripts/inject_service_endpoint.py --endpoint https://rag.example.com
  py -3 scripts/inject_service_endpoint.py --endpoint https://rag.example.com --apply
  py -3 scripts/inject_service_endpoint.py --endpoint https://rag.example.com --out-dir build/site
  py -3 scripts/inject_service_endpoint.py --profile developer-local --endpoint http://127.0.0.1:8777 --apply
  py -3 scripts/inject_service_endpoint.py --check

退出码：0 = 成功；1 = 占位符残留；2 = 校验失败 / 用法错误。
"""

import argparse
import json
import os
import re
import sys
import time

#: 与守卫共用常量（单一事实源·避免两脚本漂移）。
#: 注：本脚本家目录是 scripts/，直接运行或被 tests 导入时 scripts/ 都在 sys.path 上。
import check_no_hardcoded_endpoint as guard

PLACEHOLDER = guard.PLACEHOLDER
DEV_LOCAL_MARKER = guard.DEV_LOCAL_MARKER

#: 地址形态：scheme + host（+ 可选端口），不带路径（CSP host-source 兼容）。
ENDPOINT_RE = re.compile(r"^(?P<scheme>https?)://(?P<host>[^/?#\s:]+)(?::(?P<port>\d{1,5}))?/?$")

#: 各文件类型的标记注释形态（JSON 不支持注释 ⇒ 另作拒绝处理）。
MARKER_TEMPLATE_HTML = "<!-- {marker} endpoint={endpoint} -->"
MARKER_TEMPLATE_CODE = "/* {marker} endpoint={endpoint} */"
MARKER_TEMPLATE_TEXT = "# {marker} endpoint={endpoint}"
HTML_EXTS = (".html", ".htm", ".xhtml", ".xml", ".md")
CODE_EXTS = (".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".css")


def classify_endpoint(endpoint):
    """校验地址形态并判定地址类别（loopback / private / public）。"""
    m = ENDPOINT_RE.match(endpoint.strip())
    if not m:
        raise ValueError("地址形态非法（须为 scheme://host[:port]·不带路径）：" + endpoint)
    host_class = guard.classify_host(m.group("host"))
    return {
        "endpoint": endpoint.strip().rstrip("/"),
        "host": m.group("host"),
        "port": m.group("port"),
        "class": host_class,
    }


def validate_profile(endpoint_info, profile):
    """按档位校验地址（fail-closed）。"""
    host_class = endpoint_info["class"]
    if profile == "default":
        if host_class in ("loopback", "private", "link_local"):
            raise ValueError(
                "默认构建禁止回环/内网地址（契约 C-8）：" + endpoint_info["endpoint"]
                + "；开发者本机专用请用 --profile developer-local")
    else:
        if host_class != "loopback":
            raise ValueError(
                "开发者本机专用构建必须使用回环地址（收到 " + host_class + "）："
                + endpoint_info["endpoint"])


def marker_template_for(path):
    """按文件类型给出标记注释模板；JSON 不支持注释 ⇒ 返回 None（调用方须拒绝）。"""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        return None
    if ext in HTML_EXTS:
        return MARKER_TEMPLATE_HTML
    if ext in CODE_EXTS:
        return MARKER_TEMPLATE_CODE
    return MARKER_TEMPLATE_TEXT


def insert_marker(text, marker_line, is_html):
    """把标记插到文件顶部（HTML 插在 DOCTYPE 之后·避免 doctype 前注释触发怪异模式）。"""
    if is_html:
        lines = text.split("\n")
        for idx, ln in enumerate(lines):
            if ln.strip().lower().startswith("<!doctype"):
                cut = sum(len(x) + 1 for x in lines[: idx + 1])
                return text[:cut] + "\n" + marker_line + text[cut:]
    if text.startswith("#!"):
        nl = text.find("\n")
        if nl >= 0:
            return text[: nl + 1] + marker_line + "\n" + text[nl + 1:]
    return marker_line + "\n" + text


def inject_text(text, endpoint, profile, is_html=False):
    """对单文件文本做注入，返回 (新文本, 替换处数, 标记行或 None)。"""
    count = text.count(PLACEHOLDER)
    if count == 0:
        return text, 0, None
    new_text = text.replace(PLACEHOLDER, endpoint)
    marker_line = None
    if profile == "developer-local":
        marker_line = MARKER_TEMPLATE_CODE.format(marker=DEV_LOCAL_MARKER, endpoint=endpoint)
        if marker_line not in new_text:
            new_text = insert_marker(new_text, marker_line, is_html)
    return new_text, count, marker_line


def inject_file(path, endpoint, profile):
    """对单个文件注入，返回状态记录（含新内容，调用方决定是否落盘）。"""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if PLACEHOLDER not in text:
        marker_endpoint, marker_line = guard.parse_dev_local_marker(text)
        if marker_endpoint:
            return {"file": path, "status": "already_injected", "replacements": 0,
                    "marker": marker_line, "endpoint": marker_endpoint, "content": text}
        return {"file": path, "status": "no_placeholder", "replacements": 0,
                "marker": None, "content": text}
    if profile == "developer-local":
        if marker_template_for(path) is None:
            raise ValueError(
                "JSON 文件不支持注释标记（无法留可审计豁免痕迹）：" + path
                + "；请改用非 JSON 载体或调整产物结构")
    is_html = os.path.splitext(path)[1].lower() in HTML_EXTS
    new_text, count, marker_line = inject_text(text, endpoint, profile, is_html)
    return {"file": path, "status": "injected", "replacements": count,
            "marker": marker_line, "content": new_text}


def collect_targets(root):
    """收集含占位符的文件。"""
    out = []
    for path, text in guard.iter_text_files(root):
        if PLACEHOLDER in text:
            out.append(path)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="inject_service_endpoint.py",
        description="静态产物服务地址注入（部署期·契约 C-8）",
    )
    parser.add_argument("--endpoint", default=None, help="部署方服务地址（scheme://host[:port]）")
    parser.add_argument("--root", default="site", help="产物根目录（默认 site）")
    parser.add_argument("--profile", default="default", choices=("default", "developer-local"),
                        help="构建档位：default（禁回环）/ developer-local（本机专用·带显式标记）")
    parser.add_argument("--apply", action="store_true", help="就地替换（默认干跑·只打印计划）")
    parser.add_argument("--out-dir", default=None, help="输出到新目录（复制并注入·不改源目录）")
    parser.add_argument("--check", action="store_true", help="只查占位符残留（部署完整性门禁）")
    parser.add_argument("--manifest", default=None, help="审计清单落盘路径（JSON）")
    args = parser.parse_args(argv)

    if args.check:
        remaining = collect_targets(args.root)
        print(json.dumps({"check": True, "root": args.root,
                          "placeholder_remaining": len(remaining),
                          "files": remaining}, ensure_ascii=False, indent=2))
        return 0 if not remaining else 1

    if not args.endpoint:
        print("缺 --endpoint（部署方服务地址）", file=sys.stderr)
        return 2

    try:
        endpoint_info = classify_endpoint(args.endpoint)
        validate_profile(endpoint_info, args.profile)
    except ValueError as exc:
        print("校验失败：" + str(exc), file=sys.stderr)
        return 2

    endpoint = endpoint_info["endpoint"]
    targets = collect_targets(args.root)
    records = []
    for path in targets:
        rel = os.path.relpath(path, args.root).replace("\\", "/")
        try:
            rec = inject_file(path, endpoint, args.profile)
        except ValueError as exc:
            print("注入失败：" + str(exc), file=sys.stderr)
            return 2
        content = rec.pop("content", None)
        rec["file"] = rel
        records.append(rec)
        if args.apply and content is not None:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
        if args.out_dir and content is not None:
            dest = os.path.join(args.out_dir, rel)
            parent = os.path.dirname(dest)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(dest, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)

    summary = {
        "profile": args.profile,
        "endpoint": endpoint,
        "endpoint_class": endpoint_info["class"],
        "root": args.root,
        "applied": bool(args.apply),
        "out_dir": args.out_dir,
        "target_count": len(targets),
        "injected_count": sum(1 for r in records if r["status"] == "injected"),
        "records": records,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    if args.manifest:
        with open(args.manifest, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
