#!/usr/bin/env python3
"""站点交互流程全量复核扫描器（只读·不改任何页面）

维度（对齐用户指令四项）：
  A 跳转路径 —— 死链 / 锚点失效 / 不可达页 / 孤儿页 / .md 直链 / 外域新窗口安全
  B 按钮与状态反馈 —— 可点击元素清单 / 键盘可达 / type 缺失 / 状态信号（aria-live/disabled/loading）
  C 表单填写与出错提示 —— 控件 label 关联 / required / 错误提示容器 / 空提交反馈
  D 空状态与异常分支 —— fetch 失败是否可见 / 空态文案 / 脚本异常兜底

用法：py -3 scripts/_w926_ia_audit.py [--out <json 路径>]
输出：scripts/output/_w926_ia_audit.json（含逐页明细与全量聚合）
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DEFAULT_OUT = ROOT / "scripts" / "output" / "_w926_ia_audit.json"

# ---------- 文本信号（用户可见） ----------
EMPTY_STATE_RE = re.compile(
    r"(暂无|没有.{0,6}(数据|内容|结果|记录)|无.{0,4}(数据|结果|内容)|空空如也|加载中|敬请期待|未找到|0\s*条|空空|无匹配|no data|not found|no results)"
)
USER_VISIBLE_ERR_RE = re.compile(
    r"(出错了|失败|错误|请稍后|重试|无法|不可用|已停止|超时|异常|不支持|请检查|重新加载|error|failed|retry|timeout)"
)
FETCH_RE = re.compile(r"\bfetch\s*\(")
CATCH_RE = re.compile(r"\.catch\s*\(|try\s*\{")
ALERT_RE = re.compile(r"\balert\s*\(")
CONSOLE_ONLY_RE = re.compile(r"console\.(warn|error|log)\s*\(")
EMPTY_TEXT_RE = re.compile(r"if\s*\(\s*!\s*[A-Za-z_$][\w.$]*\s*\)\s*(return|continue)\s*;?\s*\}?\s*$", re.M)


class PageParser(HTMLParser):
    """逐页抽取交互结构。script/style 内容按 CDATA 交给 handle_data，不当 HTML 解析。"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[dict] = []
        self.buttons: list[dict] = []
        self.controls: list[dict] = []
        self.forms: list[dict] = []
        self.inline_scripts: list[str] = []
        self.ext_scripts: list[str] = []
        self.imgs_no_alt = 0
        self.has_viewport = False
        self.lang = None
        self.title = None
        self.aria_live_nodes = 0
        self.role_alert_nodes = 0
        self.role_status_nodes = 0
        self.loading_tokens = 0
        self.disabled_attrs = 0
        self._form_depth = 0
        self._in_script = False
        self._in_style = False
        self._in_title = False
        self._buf: list[str] = []
        self._btn_stack: list[dict] = []
        self._click_stack: list[dict] = []
        # 判据修正（W926·五）：可点击元素计数用**计数器**而非栈长度——
        # 栈会被任意 </div> 提前弹出，导致总数被记成 0（盲审实测全站应为 12）
        self.n_clickable = 0

    # -- helpers --
    @staticmethod
    def _attrs_dict(attrs) -> dict:
        # 判据修正（W926·六）：HTML 规范规定**重复属性取第一个**（后者被忽略）——
        # 原实现用 dict 构造让后者覆盖前者，导致 `<span role="button" role="listitem">`
        # 被读成 listitem → 首页 4 个快捷词被漏计（盲审实测全站应为 12，修复前测得 8）
        d: dict = {}
        for k, v in attrs:
            k = k.lower()
            if k not in d:
                d[k] = (v if v is not None else "")
        return d

    def handle_starttag(self, tag, attrs):
        a = self._attrs_dict(attrs)
        if "id" in a and a["id"]:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "meta" and a.get("name", "").lower() == "viewport":
            self.has_viewport = True
        if tag == "title":
            self._in_title = True
        if tag == "script":
            self._in_script = True
            self._buf = []
            if a.get("src"):
                self.ext_scripts.append(a["src"])
        if tag == "style":
            self._in_style = True
        if tag == "form":
            self._form_depth += 1
            self.forms.append({"id": a.get("id", ""), "method": a.get("method", "get").lower(),
                               "action": a.get("action", ""), "has_submit": False})
        if tag == "button":
            rec = {"tag": "button", "id": a.get("id", ""), "cls": a.get("class", ""),
                   "type": a.get("type", ""), "in_form": self._form_depth > 0,
                   "disabled": "disabled" in a, "text": "", "has_aria": bool(a.get("aria-label") or a.get("aria-labelledby"))}
            self.buttons.append(rec)
            self._btn_stack.append(rec)
        elif tag in ("input", "select", "textarea"):
            if tag == "input" and a.get("type", "").lower() == "hidden":
                pass
            else:
                rec = {"tag": tag, "id": a.get("id", ""), "name": a.get("name", ""),
                       "type": a.get("type", ""), "required": "required" in a,
                       "has_label": self._has_label_for(a.get("id", "")), "has_aria": bool(a.get("aria-label") or a.get("aria-labelledby")),
                       "placeholder": bool(a.get("placeholder")), "in_form": self._form_depth > 0}
                self.controls.append(rec)
        if tag == "a":
            self.links.append({"href": a.get("href", ""), "target": a.get("target", ""),
                                "rel": a.get("rel", ""), "id": a.get("id", ""),
                                "cls": a.get("class", "")})
        if tag == "img" and "alt" not in a:
            self.imgs_no_alt += 1
        if a.get("role") == "alert":
            self.role_alert_nodes += 1
        if a.get("role") == "status":
            self.role_status_nodes += 1
        if "aria-live" in a:
            self.aria_live_nodes += 1
        if "disabled" in a:
            self.disabled_attrs += 1
        interactive_roles = ("button", "link", "tab", "menuitem", "switch", "option", "checkbox", "radio")
        if tag in ("div", "span", "li", "p", "td") and (
                "onclick" in a or a.get("role", "") in interactive_roles or "tabindex" in a):
            self.n_clickable += 1
            self._click_stack.append({"tag": tag, "id": a.get("id", ""), "cls": a.get("class", ""),
                                       "onclick": "onclick" in a, "role": a.get("role", ""),
                                       "tabindex": a.get("tabindex", ""), "type": ""})
        if tag == "input" and a.get("type", "").lower() in ("submit", "image", "button"):
            if self.forms:
                self.forms[-1]["has_submit"] = True
        # 判据修正（W926·二）：<button type="submit"> 也是提交控件——原判据只认 input[submit]
        # ⇒ 曾把 index.html 的 #askForm 误判为「表单无提交」
        if tag == "button" and a.get("type", "").lower() == "submit":
            if self.forms:
                self.forms[-1]["has_submit"] = True

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_script = False
            code = "".join(self._buf)
            if code.strip():
                self.inline_scripts.append(code)
            self._buf = []
        if tag == "style":
            self._in_style = False
        if tag == "title":
            self._in_title = False
        if tag == "form" and self._form_depth > 0:
            self._form_depth -= 1
        if tag == "button" and self._btn_stack:
            self._btn_stack.pop()
        if tag in ("div", "span", "li", "p", "td") and self._click_stack:
            self._click_stack.pop()

    def handle_data(self, data):
        if self._in_script or self._in_style:
            self._buf.append(data)
            return
        if self._in_title and self.title is None:
            self.title = data.strip()
        if self._btn_stack:
            self._btn_stack[-1]["text"] += data

    def _has_label_for(self, elem_id: str) -> bool:
        return bool(elem_id) and elem_id in self._labels

    # 提前扫描 label for
    _labels: set = set()


def collect_labels(html: str) -> set:
    return set(re.findall(r"<label[^>]*\bfor\s*=\s*[\"']?([A-Za-z0-9_\-:.]+)[\"']?", html, re.I))


def classify(rel: str) -> str:
    p = Path(rel)
    if rel.startswith("reader/") and (p.name == "index.html" or "themes" in rel or "poetry" in rel or "essays" in rel):
        return "reader-hub"
    if rel.startswith("reader/"):
        return "reader-chapter"
    if rel.startswith("data/"):
        return "data-viz"
    if rel.startswith("en/"):
        return "en"
    return "root"


def main() -> int:
    out_path = DEFAULT_OUT
    if "--out" in sys.argv:
        out_path = Path(sys.argv[sys.argv.index("--out") + 1])

    files = sorted(SITE.rglob("*.html"))
    pages: dict[str, dict] = {}
    id_map: dict[str, set] = {}
    code_map: dict[str, str] = {}
    link_index: list[tuple[str, dict]] = []

    for f in files:
        rel = f.relative_to(SITE).as_posix()
        html = f.read_text(encoding="utf-8", errors="replace")
        p = PageParser()
        p._labels = collect_labels(html)
        try:
            p.feed(html)
        except Exception as exc:  # 单页解析失败不中断全量
            print(f"WARN parse fail {rel}: {exc}", file=sys.stderr)
        pages[rel] = {
            "bytes": len(html.encode("utf-8")),
            "kind": classify(rel),
            "lang": p.lang,
            "title": p.title,
            "has_viewport": p.has_viewport,
            "n_links": len(p.links),
            "n_buttons": len(p.buttons),
            "n_controls": len(p.controls),
            "n_forms": len(p.forms),
            "n_inline_scripts": len(p.inline_scripts),
            "n_ext_scripts": len(p.ext_scripts),
            "aria_live": p.aria_live_nodes,
            "role_alert": p.role_alert_nodes,
            "role_status": p.role_status_nodes,
            "disabled_attrs": p.disabled_attrs,
            "imgs_no_alt": p.imgs_no_alt,
            "click_stack": p._click_stack,
            "n_clickable": p.n_clickable,
        }
        id_map[rel] = p.ids
        for lnk in p.links:
            link_index.append((rel, lnk))
        code = "\n".join(p.inline_scripts)
        code_map[rel] = code
        pages[rel].update({
            "n_fetch": len(FETCH_RE.findall(code)),
            "n_catch": len(CATCH_RE.findall(code)),
            "n_alert": len(ALERT_RE.findall(code)),
            "n_console_only": len(CONSOLE_ONLY_RE.findall(code)),
            "has_user_visible_err": bool(USER_VISIBLE_ERR_RE.search(code)),
            "has_empty_state_text": bool(EMPTY_STATE_RE.search(html)),
            "has_loading_token": bool(re.search(r"loading|spinner|加载中|aria-busy", code, re.I)),
        })

    # ---------- A 跳转路径 ----------
    existing = set(pages.keys())
    # 判据修正（W926）：链接目标可能是 json/css/js 等非 HTML 资源——existing 必须含全部文件，
    # 否则会把 19 条 data/json/*.json 下载链接误判为死链（先质疑判据再质疑结论）
    all_files = {p.relative_to(SITE).as_posix() for p in SITE.rglob("*") if p.is_file()}
    broken, anchor_miss, md_links, ext_unsafe, ext_total = [], [], [], [], 0
    html_only_false_dead: list[dict] = []
    inbound: dict[str, int] = defaultdict(int)
    for src, lnk in link_index:
        href = (lnk.get("href") or "").strip()
        if not href or href.startswith("#") or href.startswith(("javascript:", "mailto:", "tel:", "data:")):
            if href.startswith("#") and len(href) > 1:
                if href[1:] not in id_map.get(src, set()):
                    anchor_miss.append({"page": src, "href": href})
            continue
        if href.startswith(("http://", "https://", "//")):
            ext_total += 1
            if lnk.get("target") == "_blank" and "noopener" not in (lnk.get("rel") or ""):
                ext_unsafe.append({"page": src, "href": href})
            continue
        target = href.split("#")[0].split("?")[0]
        if not target:
            continue
        try:
            resolved = (SITE / src).parent.joinpath(target).resolve()
            rel_res = resolved.relative_to(SITE.resolve()).as_posix()
        except Exception:
            continue
        if rel_res in existing or rel_res in all_files:
            inbound[rel_res] += 1
            # 判据对照（W926）：目标存在但不是 .html（json/css/js 等）⇒ 首轮「只比 *.html」判据会误判为死链。
            # 此处显式计数，使首轮口径与修正口径**同时可复算**（避免证据被覆盖后数字失链）
            if rel_res not in existing:
                html_only_false_dead.append({"page": src, "href": href, "resolved": rel_res})
        else:
            if target.lower().endswith(".md"):
                md_links.append({"page": src, "href": href})
            elif target.lower().endswith((".html", "/")) or "." in Path(target).name:
                broken.append({"page": src, "href": href})
            else:
                broken.append({"page": src, "href": href})

    # 可达性：从 site/index.html 广度遍历站内 html 链接
    adj: dict[str, list[str]] = defaultdict(list)
    for src, lnk in link_index:
        href = (lnk.get("href") or "").strip()
        if not href or href.startswith(("http://", "https://", "//", "#", "mailto:", "javascript:", "data:")):
            continue
        target = href.split("#")[0].split("?")[0]
        if not target:
            continue
        try:
            resolved = (SITE / src).parent.joinpath(target).resolve()
            rel_res = resolved.relative_to(SITE.resolve()).as_posix()
        except Exception:
            continue
        if rel_res in existing:
            adj[src].append(rel_res)
    seen, queue = {"index.html"}, ["index.html"]
    while queue:
        cur = queue.pop()
        for nxt in adj.get(cur, ()):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    unreachable = sorted(existing - seen)
    orphans = sorted(p for p in existing if inbound.get(p, 0) == 0 and p not in ("index.html",))

    # ---------- B/C/D 聚合 ----------
    clickable_total = sum(v.get("n_clickable", 0) for v in pages.values())
    clickables_nonrole = [
        {"page": r, **c} for r, v in pages.items() for c in v["click_stack"]
        if c["onclick"] and c["tag"] in ("div", "span", "li", "p", "td")
        and c["role"] not in ("button", "link", "tab", "menuitem", "switch")
        and not c["tabindex"]
    ]
    # 缺 role 或 tabindex 的可点击 div/span（真实 a11y 缺口）
    clickables_missing_a11y = [
        {"page": r, **c} for r, v in pages.items() for c in v["click_stack"]
        if c["tag"] in ("div", "span", "li", "p", "td")
        and not (c["role"] in ("button", "link", "tab", "menuitem", "switch") and c["tabindex"])
    ]
    # ---- B 维度明细：二次解析取按钮/控件/表单细节（首轮只存计数，避免内存翻倍） ----
    btn_detail: dict[str, list] = {}
    ctrl_detail: dict[str, list] = {}
    for f in files:
        rel = f.relative_to(SITE).as_posix()
        html = f.read_text(encoding="utf-8", errors="replace")
        p = PageParser()
        p._labels = collect_labels(html)
        try:
            p.feed(html)
        except Exception:
            continue
        btn_detail[rel] = p.buttons
        ctrl_detail[rel] = p.controls

    buttons_no_type_in_form = [
        {"page": rel, "id": b["id"], "cls": b["cls"], "text": (b["text"] or "").strip()[:40]}
        for rel, bl in btn_detail.items() for b in bl
        if b["in_form"] and not b["type"]
    ]
    buttons_no_feedback = [
        {"page": rel, "id": b["id"], "cls": b["cls"], "text": (b["text"] or "").strip()[:40]}
        for rel, bl in btn_detail.items() for b in bl
        if not b["disabled"] and not b["has_aria"]
    ]
    controls_no_label = [
        {"page": rel, "tag": c["tag"], "id": c["id"], "type": c["type"]}
        for rel, cl in ctrl_detail.items() for c in cl
        if not c["has_label"] and not c["has_aria"]
    ]
    # C 维度明细：二次解析取表单明细（首轮只存计数）
    fm_detail: dict[str, list] = {}
    for f in files:
        rel = f.relative_to(SITE).as_posix()
        html = f.read_text(encoding="utf-8", errors="replace")
        p = PageParser()
        p._labels = collect_labels(html)
        try:
            p.feed(html)
        except Exception:
            continue
        fm_detail[rel] = p.forms
    forms_no_submit = [
        {"page": rel, "id": fm["id"], "method": fm["method"], "action": fm["action"]}
        for rel, fl in fm_detail.items() for fm in fl
        if not fm["has_submit"]
    ]

    fetch_pages = {r: v for r, v in pages.items() if v["n_fetch"] > 0}
    # 判据修正（W926·三）：「fetch 页无可见错误文案」原判据 = 整页无错误关键词 → 过粗
    # （catch 里写了内联兜底文案也算「有」，但正文别处的错误词会污染）
    # 改为逐 catch 块判定：块内是否写 DOM（innerHTML/textContent/appendChild/样式切换）
    VISIBLE_IN_CATCH = re.compile(
        r"(innerHTML|textContent|appendChild|insertAdjacentHTML|\.style\.|classList\.|"
        r"setAttribute\(\s*['\"](?:aria|class)|\.append\(|\.text\(|\.html\(|\.classed\(|\.transition\(|"
        r"showError|renderError|setStatus|showMsg)")
    fetch_no_visible_err = []
    for rel, v in fetch_pages.items():
        code = code_map.get(rel, "")
        # 判据修正（W926·四）：用「位置法」而非正则配平——.catch 后取 800 字符窗口
        # （原正则被 `function (e)` 的右括号截断 → 116/118 假红）
        ok = False
        for m in re.finditer(r"\.catch\b", code):
            seg = code[m.end(): m.end() + 800]
            if VISIBLE_IN_CATCH.search(seg):
                ok = True
                break
        if not ok:
            fetch_no_visible_err.append({"page": rel, "n_fetch": v["n_fetch"], "n_catch": v["n_catch"],
                                        "n_console_only": v["n_console_only"]})
    fetch_no_catch = [
        {"page": r, "n_fetch": v["n_fetch"]} for r, v in fetch_pages.items() if v["n_catch"] == 0
    ]
    pages_with_scripts_no_error_signal = [
        {"page": r, "n_scripts": v["n_inline_scripts"], "n_catch": v["n_catch"], "n_console_only": v["n_console_only"]}
        for r, v in pages.items()
        if v["n_inline_scripts"] > 0 and v["n_catch"] == 0 and v["n_console_only"] > 0
    ]

    by_kind: dict[str, int] = defaultdict(int)
    for v in pages.values():
        by_kind[v["kind"]] += 1

    result = {
        "meta": {
            "pages_total": len(pages),
            "pages_with_controls": sum(1 for v in pages.values() if v["n_buttons"] + v["n_controls"] > 0),
            "controls_total": sum(v["n_buttons"] + v["n_controls"] for v in pages.values()),
            "buttons_total": sum(v["n_buttons"] for v in pages.values()),
            "form_controls_total": sum(v["n_controls"] for v in pages.values()),
            "forms_total": sum(v["n_forms"] for v in pages.values()),
            "inline_scripts_total": sum(v["n_inline_scripts"] for v in pages.values()),
            "links_total": sum(v["n_links"] for v in pages.values()),
            "fetch_pages": len(fetch_pages),
            "fetch_calls_total": sum(v["n_fetch"] for v in pages.values()),
            "by_kind": dict(by_kind),
            "bytes_total": sum(v["bytes"] for v in pages.values()),
        },
        "A_paths": {
            "broken_links": broken,
            "broken_count": len(broken),
            "html_only_false_dead": html_only_false_dead,
            "html_only_false_dead_count": len(html_only_false_dead),
            "anchor_miss": anchor_miss,
            "anchor_miss_count": len(anchor_miss),
            "md_links": md_links,
            "md_links_count": len(md_links),
            "external_total": ext_total,
            "external_blank_no_noopener": ext_unsafe,
            "unreachable_from_index": unreachable,
            "unreachable_count": len(unreachable),
            "orphans_no_inbound": orphans,
            "orphans_count": len(orphans),
            "inbound_zero_pages": sorted(p for p in existing if inbound.get(p, 0) == 0),
        },
        "B_buttons": {
            "clickable_div_span": clickable_total,
            "clickables_missing_role_or_tabindex": clickables_missing_a11y,
            "clickables_missing_role_or_tabindex_count": len(clickables_missing_a11y),
            "clickables_without_role_or_tabindex": clickables_nonrole,
            "buttons_no_type_in_form": buttons_no_type_in_form,
            "buttons_no_type_in_form_count": len(buttons_no_type_in_form),
            "buttons_without_aria_or_disabled": buttons_no_feedback,
            "buttons_without_aria_or_disabled_count": len(buttons_no_feedback),
            "pages_with_aria_live": sum(1 for v in pages.values() if v["aria_live"] > 0),
            "pages_with_role_alert": sum(1 for v in pages.values() if v["role_alert"] > 0),
            "pages_with_role_status": sum(1 for v in pages.values() if v["role_status"] > 0),
        },
        "C_forms": {
            "forms_total": sum(v["n_forms"] for v in pages.values()),
            "forms_no_submit": forms_no_submit,
            "forms_no_submit_count": len(forms_no_submit),
            "controls_without_label": controls_no_label,
            "controls_without_label_count": len(controls_no_label),
        },
        "D_states": {
            "fetch_pages_count": len(fetch_pages),
            "fetch_no_visible_err": fetch_no_visible_err,
            "fetch_no_catch": fetch_no_catch,
            "pages_with_scripts_console_only": pages_with_scripts_no_error_signal,
            "pages_with_empty_state_text": sum(1 for v in pages.values() if v["has_empty_state_text"]),
            "pages_without_viewport": [r for r, v in pages.items() if not v["has_viewport"]],
            "imgs_no_alt_total": sum(v["imgs_no_alt"] for v in pages.values()),
        },
        "per_page": pages,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

    m = result["meta"]
    print(f"[扫描完成] {out_path}")
    print(f"  页数 {m['pages_total']}（{m['by_kind']}）· 控件 {m['controls_total']}· 按钮 {m['buttons_total']}· 表单控件 {m['form_controls_total']}")
    print(f"  A 死链 {len(broken)}· 锚点失效 {len(anchor_miss)}· .md 直链 {len(md_links)}· 首页不可达 {len(unreachable)}· 无入链 {len(orphans)}")
    print(f"  B div/span 可点击 {clickable_total}· 无 role/tabindex {len(clickables_nonrole)}· form 内 button 缺 type {len(buttons_no_type_in_form)}")
    print(f"  C 控件无 label {len(controls_no_label)}· 表单无提交 {len(forms_no_submit)}")
    print(f"  D fetch 页 {len(fetch_pages)}· 无可见错误文案 {len(fetch_no_visible_err)}· 无 catch {len(fetch_no_catch)}")
    print(f"  汇总 → {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
