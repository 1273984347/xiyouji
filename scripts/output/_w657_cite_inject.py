#!/usr/bin/env python3
"""W657 临时脚本：B-6 第二步——86 页注入可引用性静态块（cite-block）

每页块内容（真实信息·零编造）：
  数据源：<fetch 页=json/xxx.json 路径列表 | EMBEDDED 页=页面内嵌 EMBEDDED 数据>（快照 <今日>）
         ·由 scripts/run_all.py 批量生成（口径与参数见 dataset 同名 JSON 与生成脚本源）
  引用格式（details 折叠·默认收起·视觉零扰动）：APA + BibTeX（title/canonical 从页面提取）
  下载：<fetch 页 a[download]>（EMBEDDED 页无——C4 由 EMBEDDED 声明判据通过）
插入位置：已有 <div id="dataSource"> → 其闭合前；无 → noscript/数据注释后新建 dataSource div。
输出触达清单 scripts/output/_cascade_files_W657_pages.txt。--check 只报告不写盘。
"""
import html as html_mod
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(".").resolve()
SITE_DATA = ROOT / "site" / "data"
SKIP = {"_shell", "_template"}
TODAY = date.today().isoformat()
SITE_BASE = "https://1273984347.github.io/xiyouji/data/{stem}.html"

RE_JSON = re.compile(r'["\']((?:json/|\./json/)[\w/-]+\.json)["\']')
RE_TITLE = re.compile(r"<title>([^<]+)</title>")
RE_CANON = re.compile(r'<link rel="canonical" href="([^"]+)"')
RE_DS_DIV = re.compile(r'(<div[^>]*id="dataSource"[^>]*>)')


def page_facts(p: Path) -> dict:
    h = p.read_text(encoding="utf-8", errors="ignore")
    title = (RE_TITLE.search(h).group(1) if RE_TITLE.search(h) else p.stem).strip()
    title = re.sub(r"\s*[|·]\s*详解西游记.*$", "", title).strip()
    url = SITE_BASE.format(stem=p.stem)
    jsons = sorted(set(RE_JSON.findall(h)))
    embedded = "EMBEDDED" in h
    return {"h": h, "title": title, "url": url, "jsons": jsons, "embedded": embedded}


def build_block(f: dict) -> str:
    if f["jsons"]:
        src_line = "数据源：" + "、".join(f"<code>{j}</code>" for j in f["jsons"]) + f"（快照 {TODAY}）"
        dl = "".join(
            f'<a href="{j}" download="{j.split("/")[-1]}">下载数据 JSON</a>' for j in f["jsons"][:1]
        )
    else:
        src_line = f"数据源：页面内嵌 EMBEDDED 数据（run_all 批量生成 JSON 快照于构建时嵌入·快照 {TODAY}）"
        dl = ""
    gen = "由 <code>scripts/run_all.py</code> 批量生成（口径与参数见 dataset 同名 JSON 与生成脚本源）。"
    apa = f"《详解西游记》项目. ({2026}). {f['title']}. 详解西游记可视化站点. {f['url']}（访问日期 {TODAY}）"
    bib = (
        "@misc{xiyouji_" + re.sub(r"[^\w]", "_", p_stem(f)) + ",\n"
        "  title       = {" + f["title"] + "},\n"
        "  author      = {{《详解西游记》项目}},\n"
        "  year        = {2026},\n"
        "  howpublished = {\\url{" + f["url"] + "}},\n"
        "  note        = {可视化数据可视化解读页, 访问日期 " + TODAY + "}\n"
        "}"
    )
    lines = [
        '<div class="cite-block" id="citeBox">',
        "  " + src_line + " " + gen,
        '  <details class="cite-details">',
        "  <summary>引用格式</summary>",
        '  <div class="cite-item"><span>APA</span><pre class="cite-text">' + html_mod.escape(apa) + "</pre>" + '<button type="button" class="cite-copy" data-cite-target="next">复制</button></div>',
        '  <div class="cite-item"><span>BibTeX</span><pre class="cite-text">' + html_mod.escape(bib) + "</pre>" + '<button type="button" class="cite-copy" data-cite-target="next">复制</button></div>',
        "  </details>",
        ("  " + dl if dl else ""),
        "</div>",
    ]
    return "\n".join(ln for ln in lines if ln)


def p_stem(f):
    return f["url"].rsplit("/", 1)[-1].replace(".html", "")


def inject(p: Path) -> str:
    """返回动作描述。"""
    f = page_facts(p)
    h = f["h"]
    if 'id="citeBox"' in h:
        return "skip: 已有 citeBox"
    block = build_block(f)
    m = RE_DS_DIV.search(h)
    if m:
        # 找 dataSource div 的闭合（首个 </div> 之后——dataSource 区无嵌套 div·W657 已核形态）
        close = h.find("</div>", m.end())
        assert close != -1, p.name
        s2 = h[:close] + block + "\n      " + h[close:]
        act = "append-to-dataSource"
    else:
        anchor = re.search(r"(<noscript>[\s\S]*?</noscript>)", h)
        if not anchor:
            return "skip: 无 dataSource 且无 noscript 锚"
        s2 = h[: anchor.end()] + '\n    <div id="dataSource" class="notice">' + block + "</div>" + h[anchor.end():]
        act = "new-dataSource"
    p.write_text(s2, encoding="utf-8", newline="")
    return act


check_only = "--check" in sys.argv
pages = [p for p in sorted(SITE_DATA.glob("*.html")) if p.stem not in SKIP]
touched, actions = [], {}
for p in pages:
    act = inject(p) if not check_only else "check-only"
    actions[act] = actions.get(act, 0) + 1
    if not act.startswith("skip") and not check_only:
        touched.append(str(p.relative_to(ROOT)).replace("\\", "/"))
for k, v in sorted(actions.items()):
    print(f"{k}: {v}")
if not check_only:
    manifest = ROOT / "scripts" / "output" / "_cascade_files_W657_pages.txt"
    manifest.write_text("\n".join(touched) + "\n", encoding="utf-8")
    print(f"--- {len(touched)} 页注入 · 清单 → {manifest.relative_to(ROOT)}")
