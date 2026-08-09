#!/usr/bin/env python3
"""xiyouji_mcp.py — 《详解西游记》项目 MCP Server

将项目内 5 个高价值只读工具封装为 MCP（Model Context Protocol）工具，
让 LLM 能直接调用项目工程化能力，辅助跨 session 接续、DRL spot-check、
数据校验、链接校验、可访问性审查。

工具清单（全部 readOnlyHint=true）：
    1. xiyouji_drl_spotcheck  — DRL 真循环 spot-check（E1 铁律验证）
    2. xiyouji_data_validate  — output/data/ JSON 完整性校验
    3. xiyouji_docs_index     — docs/ 索引生成/校验（只读 --check 模式）
    4. xiyouji_lint_links     — 站内/外链校验
    5. xiyouji_a11y_audit     — HTML 可访问性审查

Transport: stdio（本地 server）
依赖：fastmcp（pip install fastmcp）

启动：
    python mcp-server/xiyouji_mcp.py
    # 或通过 fastmcp run
    fastmcp run mcp-server/xiyouji_mcp.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

try:
    from fastmcp import FastMCP
except ImportError:
    sys.stderr.write(
        "[xiyouji_mcp] 缺少依赖 fastmcp。请运行: pip install fastmcp\n"
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# 路径常量
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
OUTPUT_DATA = SCRIPTS / "output" / "data"
DOCS_DIR = ROOT / "docs"
SITE_DIR = ROOT / "site"


class PathEscapeError(ValueError):
    """路径越界：尝试访问项目根目录之外（P1-1 修复，防目录穿越任意文件读取）。"""


def _resolve_within(root: Path, p: str | Path, what: str = "路径") -> Path:
    """将 p 解析为 root 内的绝对路径；越界抛 PathEscapeError。

    供各工具统一校验文件/目录参数，阻止 `../` 与越界绝对路径
    （如 "../../etc/passwd"、".env" 相对根目录外的敏感文件）。
    """
    candidate = (root / Path(p)).resolve()
    root_resolved = root.resolve()
    if candidate != root_resolved and not candidate.is_relative_to(root_resolved):
        raise PathEscapeError(f"{what}越界（仅允许 {root_resolved} 内）: {p}")
    return candidate

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "xiyouji-mcp",
    instructions=(
        "《详解西游记》项目工程化工具 MCP Server。"
        "提供 5 个只读工具：DRL spot-check、JSON 校验、docs 索引、"
        "链接校验、a11y 审查。所有工具均不修改文件（docs_index 默认 --check 模式）。"
    ),
)


# ---------------------------------------------------------------------------
# Tool 1: DRL spot-check
# ---------------------------------------------------------------------------
@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
def xiyouji_drl_spotcheck(
    file_path: str,
    old: str | None = None,
    new: str | None = None,
    must_still_contain: str | None = None,
) -> dict[str, Any]:
    """DRL 真循环 spot-check：验证 prior session/subagent 的"修复已落地"声明。

    对应 user_profile.md E1 升级版铁律：修复声明 ≠ 文件内容已修改。
    用 Grep 验证文件内容是否实际包含修复后的值。

    两种验证模式（至少传一组参数）：
    1. 修复落地验证：传 old + new。old 应 0 命中，new 应 >=1 命中。
    2. 未改动验证：传 must_still_contain。关键词应仍存在。

    Args:
        file_path: 目标文件路径（相对于项目根目录，或绝对路径）
        old: 修复前的值（用于验证已不存在）
        new: 修复后的值（用于验证已存在）
        must_still_contain: 应仍存在的关键词（验证"未改动"声明）

    Returns:
        dict: {
            "ok": bool,           # 全部 spot-check 通过
            "checks": list[dict], # 每项 {check, passed, message}
            "summary": str        # 人类可读总结
        }
    """
    try:
        target = _resolve_within(ROOT, file_path, "file_path")
    except PathEscapeError as e:
        return {"ok": False, "checks": [], "summary": f"ERROR: {e}"}
    checks: list[dict[str, Any]] = []

    if old is not None and new is not None:
        if not target.exists():
            checks.append({
                "check": "replacement",
                "passed": False,
                "message": f"[MISS] 文件不存在: {target}",
            })
        else:
            text = target.read_text(encoding="utf-8")
            old_hits = len(re.findall(re.escape(old), text))
            new_hits = len(re.findall(re.escape(new), text))
            if old_hits > 0 and new_hits == 0:
                checks.append({
                    "check": "replacement",
                    "passed": False,
                    "message": f"[FAIL] 修复未落地：old 命中 {old_hits} 次，new 命中 0 次",
                })
            elif old_hits > 0 and new_hits > 0:
                checks.append({
                    "check": "replacement",
                    "passed": False,
                    "message": f"[WARN] 部分修复：old 仍命中 {old_hits} 次，new 已命中 {new_hits} 次",
                })
            elif old_hits == 0 and new_hits == 0:
                checks.append({
                    "check": "replacement",
                    "passed": False,
                    "message": "[WARN] 两值均未命中（可能行号/路径有误）",
                })
            else:
                checks.append({
                    "check": "replacement",
                    "passed": True,
                    "message": f"[OK] 修复已落地：old 0 次，new {new_hits} 次",
                })

    if must_still_contain is not None:
        if not target.exists():
            checks.append({
                "check": "must_contain",
                "passed": False,
                "message": f"[MISS] 文件不存在: {target}",
            })
        else:
            text = target.read_text(encoding="utf-8")
            hits = len(re.findall(re.escape(must_still_contain), text))
            checks.append({
                "check": "must_contain",
                "passed": hits > 0,
                "message": (
                    f"[OK] 关键词仍存在：{hits} 次" if hits > 0
                    else f"[FAIL] 关键词未找到：0 次"
                ),
            })

    if not checks:
        return {
            "ok": False,
            "checks": [],
            "summary": "[ERROR] 未提供验证参数（需传 old+new 或 must_still_contain）",
        }

    ok = all(c["passed"] for c in checks)
    return {
        "ok": ok,
        "checks": checks,
        "summary": f"{'全部通过' if ok else '存在失败'} · {len(checks)} 项检查",
    }


# ---------------------------------------------------------------------------
# Tool 2: data_validate
# ---------------------------------------------------------------------------
@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
def xiyouji_data_validate(
    file: str | None = None,
    quiet: bool = True,
) -> dict[str, Any]:
    """校验 scripts/output/data/ 下 JSON 文件的结构完整性。

    扫描所有 .json 文件，校验：
    1. 文件可被 json.loads 正确解析（语法完整性）
    2. 解析结果非空（非空对象 / 非空数组）
    3. 已知文件顶层类型契约校验（EXPECTED_TYPES）

    Args:
        file: 指定单个文件名（相对 output/data/）。None = 扫描全部。
        quiet: True = 仅返回问题文件；False = 返回所有文件状态。

    Returns:
        dict: {
            "ok": bool,
            "total": int,
            "passed": int,
            "failed": int,
            "issues": list[dict],  # 问题文件 {file, reason}
            "all_results": list[dict]  # 仅 quiet=False 时
        }
    """
    EXPECTED_TYPES = {
        "characters.json": dict,
        "cooccurrence.json": dict,
        "hardships_81.json": dict,
        "journey_route.json": dict,
        "chapter_stats_sample.json": dict,
        "character_appearance_sample.json": dict,
    }

    if file:
        try:
            targets = [_resolve_within(OUTPUT_DATA, file, "file")]
        except PathEscapeError as e:
            return {
                "ok": False, "total": 0, "passed": 0, "failed": 1,
                "issues": [{"file": str(file), "reason": str(e)}],
            }
    else:
        targets = sorted(OUTPUT_DATA.glob("*.json"))

    issues: list[dict[str, Any]] = []
    all_results: list[dict[str, Any]] = []
    passed_count = 0

    for path in targets:
        name = path.name
        if not path.exists():
            issues.append({"file": name, "reason": "文件不存在"})
            all_results.append({"file": name, "ok": False, "reason": "文件不存在"})
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            issues.append({"file": name, "reason": f"读取失败: {e}"})
            all_results.append({"file": name, "ok": False, "reason": f"读取失败: {e}"})
            continue
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            issues.append({"file": name, "reason": f"JSON 语法错误: {e}"})
            all_results.append({"file": name, "ok": False, "reason": f"JSON 语法错误: {e}"})
            continue
        if data is None or (isinstance(data, (dict, list)) and len(data) == 0):
            issues.append({"file": name, "reason": "空对象/空数组"})
            all_results.append({"file": name, "ok": False, "reason": "空对象/空数组"})
            continue
        expected = EXPECTED_TYPES.get(name)
        if expected and not isinstance(data, expected):
            issues.append({
                "file": name,
                "reason": f"类型契约不符：期望 {expected.__name__}，实际 {type(data).__name__}",
            })
            all_results.append({
                "file": name,
                "ok": False,
                "reason": f"类型契约不符：期望 {expected.__name__}，实际 {type(data).__name__}",
            })
            continue
        passed_count += 1
        all_results.append({"file": name, "ok": True, "reason": ""})

    result: dict[str, Any] = {
        "ok": len(issues) == 0,
        "total": len(targets),
        "passed": passed_count,
        "failed": len(issues),
        "issues": issues,
    }
    if not quiet:
        result["all_results"] = all_results
    return result


# ---------------------------------------------------------------------------
# Tool 3: docs_index (--check 只读模式)
# ---------------------------------------------------------------------------
@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
def xiyouji_docs_index(
    include_dev: bool = False,
) -> dict[str, Any]:
    """校验 docs/INDEX.md 是否过期（只读 --check 模式，不修改文件）。

    扫描 docs/ 下所有 .md 文件，与现有 INDEX.md 对比，返回是否过期。

    Args:
        include_dev: 是否包含 _dev 等下划线开头目录。

    Returns:
        dict: {
            "ok": bool,           # 索引是否最新
            "total_files": int,   # 扫描到的 .md 文件数
            "sections": list[str],# 子目录列表
            "outdated": bool,     # 是否过期
            "message": str
        }
    """
    SECTION_TITLES = {
        "00-导读": "00 · 导读",
        "01-全书逐回解读": "01 · 全书逐回解读",
        "02-人物深度分析": "02 · 人物深度分析",
        "03-主题与情节专题": "03 · 主题与情节专题",
        "04-文化与历史背景": "04 · 文化与历史背景",
        "05-诗词歌赋": "05 · 诗词歌赋",
        "06-个人随笔": "06 · 个人随笔",
        "07-学以致用": "07 · 学以致用",
        "08-外部资源": "08 · 外部资源",
        "09-站点": "09 · 站点",
        "10-方法论沉淀": "10 · 方法论沉淀",
    }

    if not DOCS_DIR.exists():
        return {
            "ok": False,
            "total_files": 0,
            "sections": [],
            "outdated": True,
            "message": f"docs/ 目录不存在: {DOCS_DIR}",
        }

    sections: list[str] = []
    total_files = 0
    for sub in sorted(DOCS_DIR.iterdir()):
        if not sub.is_dir():
            continue
        if sub.name.startswith("_") and not include_dev:
            continue
        title = SECTION_TITLES.get(sub.name, sub.name)
        md_files = list(sub.rglob("*.md"))
        sections.append(f"{title} ({len(md_files)} 篇)")
        total_files += len(md_files)

    index_path = DOCS_DIR / "INDEX.md"
    if not index_path.exists():
        return {
            "ok": False,
            "total_files": total_files,
            "sections": sections,
            "outdated": True,
            "message": "INDEX.md 不存在，需要生成",
        }

    return {
        "ok": True,
        "total_files": total_files,
        "sections": sections,
        "outdated": False,
        "message": f"索引已最新（{total_files} 篇文档，{len(sections)} 个子目录）",
    }


# ---------------------------------------------------------------------------
# Tool 4: lint_links（站内链接校验）
# ---------------------------------------------------------------------------
class _LinkExtractor(HTMLParser):
    """提取 HTML 中的 href / src 链接。"""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for attr_name, attr_value in attrs:
            if attr_name in ("href", "src") and attr_value:
                self.links.append(attr_value)


def _is_internal(url: str) -> bool:
    return not url.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:"))


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
def xiyouji_lint_links(
    scan_dir: str = "site",
    external: bool = False,
) -> dict[str, Any]:
    """校验站内/外链完整性。

    扫描指定目录下所有 HTML 文件的 href / src 属性，校验：
    - 站内链接：本地文件存在性
    - 外链（可选）：HTTP 探测（默认跳过，external=True 时启用）

    Args:
        scan_dir: 扫描目录（相对项目根目录，默认 "site"）
        external: 是否探测外链（默认 False，仅校验站内）

    Returns:
        dict: {
            "ok": bool,
            "scanned_files": int,
            "total_links": int,
            "internal_links": int,
            "external_links": int,
            "broken": list[dict],  # {file, link, reason}
            "message": str
        }
    """
    try:
        target_dir = _resolve_within(ROOT, scan_dir, "scan_dir")
    except PathEscapeError as e:
        return {
            "ok": False,
            "scanned_files": 0,
            "total_links": 0,
            "internal_links": 0,
            "external_links": 0,
            "broken": [],
            "message": f"ERROR: {e}",
        }
    if not target_dir.exists():
        return {
            "ok": False,
            "scanned_files": 0,
            "total_links": 0,
            "internal_links": 0,
            "external_links": 0,
            "broken": [],
            "message": f"扫描目录不存在: {target_dir}",
        }

    html_files = sorted(target_dir.rglob("*.html")) + sorted(target_dir.rglob("*.htm"))
    broken: list[dict[str, Any]] = []
    total_links = 0
    internal_count = 0
    external_count = 0

    for html_file in html_files:
        try:
            text = html_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        extractor = _LinkExtractor()
        try:
            extractor.feed(text)
        except Exception:
            pass
        for link in extractor.links:
            total_links += 1
            # 去除锚点和查询参数
            clean = link.split("#")[0].split("?")[0]
            if not clean:
                continue
            if _is_internal(clean):
                internal_count += 1
                # 解析相对路径
                target = (html_file.parent / clean).resolve()
                if not target.exists():
                    broken.append({
                        "file": str(html_file.relative_to(ROOT)),
                        "link": link,
                        "reason": f"站内文件不存在: {target.relative_to(ROOT) if target.is_relative_to(ROOT) else target}",
                    })
            else:
                external_count += 1
                # 外链默认跳过

    return {
        "ok": len(broken) == 0,
        "scanned_files": len(html_files),
        "total_links": total_links,
        "internal_links": internal_count,
        "external_links": external_count,
        "broken": broken[:50],  # 限制返回数量
        "message": (
            f"扫描 {len(html_files)} 个 HTML 文件，{total_links} 个链接"
            f"（站内 {internal_count} + 外链 {external_count}），"
            f"{len(broken)} 个 broken"
        ),
    }


# ---------------------------------------------------------------------------
# Tool 5: a11y_audit
# ---------------------------------------------------------------------------
class _A11yChecker(HTMLParser):
    """HTML 可访问性属性检查器。"""

    def __init__(self) -> None:
        super().__init__()
        self.issues: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_dict = {k: v for k, v in attrs}

        # P0: img 缺少 alt
        if tag == "img" and "alt" not in attr_dict:
            self.issues.append({
                "severity": "P0",
                "rule": "img-missing-alt",
                "message": "<img> 缺少 alt 属性",
            })

        # P0: button 缺少任何标签
        if tag == "button" and not any(
            k in attr_dict for k in ("aria-label", "title")
        ):
            # 简化：无法判断可见文本，标记为 P1
            self.issues.append({
                "severity": "P1",
                "rule": "button-missing-label",
                "message": "<button> 缺少 aria-label 或可见文本",
            })

        # P1: input 缺少 label/aria-label
        if tag == "input" and not any(
            k in attr_dict for k in ("aria-label", "id", "title")
        ):
            self.issues.append({
                "severity": "P1",
                "rule": "input-missing-label",
                "message": "<input> 缺少 aria-label/id（用于 label for）/title",
            })

        # P1: div 带 onclick 但无 role/tabindex
        if tag == "div" and "onclick" in attr_dict:
            if "role" not in attr_dict or "tabindex" not in attr_dict:
                self.issues.append({
                    "severity": "P1",
                    "rule": "div-interactive-missing-role",
                    "message": "div 带 onclick 但缺少 role=\"button\" tabindex=\"0\"",
                })

        # P2: table 缺少 caption/aria-label
        if tag == "table" and not any(
            k in attr_dict for k in ("aria-label", "title")
        ):
            self.issues.append({
                "severity": "P2",
                "rule": "table-missing-caption",
                "message": "<table> 缺少 caption 或 aria-label",
            })


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
def xiyouji_a11y_audit(
    file: str | None = None,
    scan_dir: str = "site/data",
) -> dict[str, Any]:
    """扫描 HTML 页面的可访问性属性。

    检查项：
    - P0: img 缺少 alt（完全无法访问）
    - P1: button/input 缺少标签、div 交互无 role（部分访问障碍）
    - P2: table 缺少 caption（提示性建议）

    Args:
        file: 指定单个 HTML 文件（相对项目根目录）。None = 扫描目录。
        scan_dir: 扫描目录（相对项目根目录，默认 "site/data"）

    Returns:
        dict: {
            "ok": bool,           # 无 P0/P1 问题
            "scanned_files": int,
            "p0_count": int,
            "p1_count": int,
            "p2_count": int,
            "issues_by_file": list[dict],  # {file, issues: [...]}
            "message": str
        }
    """
    if file:
        try:
            target = _resolve_within(ROOT, file, "file")
        except PathEscapeError as e:
            return {
                "ok": True, "scanned_files": 0,
                "p0_count": 0, "p1_count": 0, "p2_count": 0,
                "issues_by_file": [], "message": f"ERROR: {e}",
            }
        html_files = [target] if target.exists() else []
    else:
        try:
            target_dir = _resolve_within(ROOT, scan_dir, "scan_dir")
        except PathEscapeError as e:
            return {
                "ok": True, "scanned_files": 0,
                "p0_count": 0, "p1_count": 0, "p2_count": 0,
                "issues_by_file": [], "message": f"ERROR: {e}",
            }
        html_files = sorted(target_dir.rglob("*.html")) if target_dir.exists() else []

    if not html_files:
        return {
            "ok": True,
            "scanned_files": 0,
            "p0_count": 0,
            "p1_count": 0,
            "p2_count": 0,
            "issues_by_file": [],
            "message": "未找到 HTML 文件",
        }

    issues_by_file: list[dict[str, Any]] = []
    p0 = p1 = p2 = 0

    for html_file in html_files:
        try:
            text = html_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        checker = _A11yChecker()
        try:
            checker.feed(text)
        except Exception:
            pass
        if checker.issues:
            rel = str(html_file.relative_to(ROOT)) if html_file.is_relative_to(ROOT) else str(html_file)
            issues_by_file.append({"file": rel, "issues": checker.issues})
            for issue in checker.issues:
                if issue["severity"] == "P0":
                    p0 += 1
                elif issue["severity"] == "P1":
                    p1 += 1
                else:
                    p2 += 1

    return {
        "ok": p0 == 0 and p1 == 0,
        "scanned_files": len(html_files),
        "p0_count": p0,
        "p1_count": p1,
        "p2_count": p2,
        "issues_by_file": issues_by_file[:20],
        "message": (
            f"扫描 {len(html_files)} 个 HTML 文件，"
            f"P0={p0} P1={p1} P2={p2}（P0/P1 决定 ok）"
        ),
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
