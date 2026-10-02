#!/usr/bin/env python3
"""第 28 门禁 · 可视化可引用性检查（check_citability.py）

来源：B-6「可视化可引用性」第一步——W636（缺口发现）/ W637（门禁升级路径）/ W638（出处四字段收编）
三份外部分析裁决定稿，2026-10-02 经用户裁决批准开工（反转 B-6 三次「登记不开工」裁决·registry 已记账）。

四项检查（D2 裁决：任一锚点即过·报告分 L0-L3 级呈现）：
  C1 数据文件路径 + 版本标识
  C2 生成脚本 + 参数/口径说明（排除构建工具引用——v1.0 假阳性源）
  C3 引用格式呈现（<cite> / 引用区块 / 扫描区内站 URL）
  C4 下载入口（a[download] / 扫描区内 .json 链接 / EMBEDDED 内嵌声明）

扫描区 = <div id="dataSource"> 内容 ∪ 全文含「数据源：」的字符串字面量（fetch/EMBEDDED 两态都收）。
排除区 = 构建工具引用（inline_css.py / w334_font_subset.py·86/86 页命中·属内联 CSS 头注释）。

形态（D4 裁决）：WARN + 基线冻结·违规集合单调不增——
  基线内 missing → 冻结豁免（WARN）；基线外 missing → FAIL 阻断；
  基线 missing 已修复 → 提示可收紧（删除该行）；基线文件缺失 → 拒绝通过（fail-closed·W631 教训）。

用法：
  python scripts/check_citability.py --generate-baseline   # 首跑冻结存量
  python scripts/check_citability.py --gate                # 门禁模式（verify_delivery 调用）
  python scripts/check_citability.py --self-test           # 6 例自检：4 负样本 + 1 正样本 + 1 构建工具回归
  python scripts/check_citability.py                       # 报告模式（不判退出码）

退出码：0=通过 / 1=存在基线外违规（或报告模式下存在违规）/ 2=self-test 断言失败
范围（D1 裁决）：仅 site/data 86 页（不含 _shell/_template 模板壳·不含 site/en 镜像）。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DATA = ROOT / "site" / "data"
BASELINE = ROOT / "scripts" / "output" / "citability-baseline.txt"
DEFAULT_REPORT = ROOT / "scripts" / "output" / "citability-report.json"

ITEMS = ("C1", "C2", "C3", "C4")
# 构建工具引用排除表：这两者出现在 86/86 页的内联 CSS 头注释中，与数据出处无关（v1.0 假阳性源）
BUILD_TOOLS = ("inline_css.py", "w334_font_subset.py")
SKIP_STEMS = ("_shell", "_template")

RE_ANCHOR_DIV = re.compile(r'<div[^>]*id=["\']dataSource["\'][^>]*>(.*?)</div>', re.S | re.I)
RE_SRC_TEXT = re.compile(r"数据源[：:][^'\"\n]{0,240}")  # 允许内联标签：路径常写在 <code>json/x.json</code> 内
RE_TAG = re.compile(r"<[^>]{0,80}>")
RE_JSON_PATH = re.compile(r"[A-Za-z0-9_./\u4e00-\u9fff-]+\.json")
RE_SCRIPT_PATH = re.compile(r"scripts/[A-Za-z0-9_./\u4e00-\u9fff-]+\.py")
RE_VERSION = re.compile(r"\d{4}-\d{2}-\d{2}|\bW\d{3}\b|\b[0-9a-f]{40}\b|版本[：:]|快照")
RE_PARAM_HINT = re.compile(r"生成|参数|口径|run_all|阈值|样本|语料|模型|权重|归一")
RE_EMBEDDED = re.compile(r"嵌入式数据|嵌入数据|内嵌数据|嵌入式版本|EMBEDDED")
RE_SITE_URL = re.compile(r"1273984347\.github\.io/xiyouji|github\.com/1273984347/xiyouji")
RE_CITE_BLOCK = re.compile(r"<cite[\s>]|Citation|引用格式|如何引用|引文格式", re.I)
RE_EXEMPT = re.compile(r"<!--\s*citability-exempt\s*:\s*(C[1-4])\s+(.{2,80}?)\s*-->")
RE_EXEMPT_BAD = re.compile(r"<!--\s*citability-exempt\s*:\s*(.*?)-->", re.I)


def scan_pages() -> list[Path]:
    """D1 裁决：仅 site/data 86 页，排除模板壳。"""
    pages = [p for p in sorted(SITE_DATA.glob("*.html")) if p.stem not in SKIP_STEMS]
    return pages


def region_of(html: str) -> tuple[str, bool]:
    """出处扫描区：dataSource div 内容 ∪ 全文「数据源：」字符串字面量。返回 (区文本, 是否有主锚点)。"""
    parts: list[str] = []
    has_anchor = False
    for m in RE_ANCHOR_DIV.finditer(html):
        has_anchor = True
        parts.append(m.group(1))
    parts.extend(m.group(0) for m in RE_SRC_TEXT.finditer(html))
    return "\n".join(parts), has_anchor


def resolve_json(rel: str, page: Path) -> str | None:
    """把扫描区里的 .json 路径解析到磁盘。返回 'deployed'（site 内部署副本·读者可取）
    / 'generated'（仅存在于 gitignore 生成物区 scripts/output/data·读者不可取）/ None。"""
    rel = rel.lstrip("./")
    base = page.parent
    deployed = [
        base / rel,
        base.parent / rel,
        SITE_DATA / rel,
        SITE_DATA / "json" / Path(rel).name,
        ROOT / "site" / rel,
    ]
    if any(c.exists() for c in deployed):
        return "deployed"
    if (ROOT / "scripts" / "output" / "data" / Path(rel).name).exists():
        return "generated"
    return None


def check_page(page: Path) -> dict[str, tuple[str, str]]:
    """返回 {item: (status, reason_code)}，status ∈ ok|missing|exempt。"""
    html = page.read_text(encoding="utf-8")
    region, has_anchor = region_of(html)

    exempted = {m.group(1).upper() for m in RE_EXEMPT.finditer(html)}
    result: dict[str, tuple[str, str]] = {}

    # ---- C1 路径 + 版本 ----
    paths = [p for p in RE_JSON_PATH.findall(region) if not re.match(r"^(res|r|response|data)\.json$", p)]
    embedded_declared = bool(RE_EMBEDDED.search(region))
    locs = [resolve_json(p, page) for p in paths]
    deployed = any(loc == "deployed" for loc in locs)
    generated_only = bool(paths) and not deployed and any(loc == "generated" for loc in locs)
    path_ok = deployed or embedded_declared
    version_ok = bool(RE_VERSION.search(region))
    if path_ok and version_ok:
        c1 = ("ok", "")
    elif not paths and not embedded_declared:
        c1 = ("missing", "no-path" if region.strip() else "no-region")
    elif generated_only and not embedded_declared:
        c1 = ("missing", "gitignore-target")
    elif not path_ok and not embedded_declared:
        c1 = ("missing", "ghost-path")
    elif not version_ok:
        c1 = ("missing", "no-version")
    else:
        c1 = ("ok", "")

    # ---- C2 生成脚本 + 参数（排除构建工具；W650 收紧：路径含子目录不再视为「有参数/口径说明」，
    # 须命中参数提示词——否则仅写裸脚本路径的页会假通过）----
    scripts = [s for s in RE_SCRIPT_PATH.findall(region) if not s.endswith(BUILD_TOOLS)]
    if scripts:
        c2 = ("ok", "") if RE_PARAM_HINT.search(region) else ("missing", "no-params")
    elif RE_SCRIPT_PATH.search(region):
        c2 = ("missing", "build-tool-only")
    else:
        c2 = ("missing", "no-script")

    # ---- C3 引用格式呈现（任一锚点即过·D2 裁决）----
    has_cite_el = bool(RE_CITE_BLOCK.search(html))
    url_in_region = bool(RE_SITE_URL.search(region))
    if has_cite_el or url_in_region:
        c3 = ("ok", "")
    else:
        c3 = ("missing", "no-cite")

    # ---- C4 下载入口 ----
    has_download_attr = "download=" in html
    link_to_json = bool(re.search(r"href=[\"'][^\"']*\.json", region, re.I))
    if has_download_attr or link_to_json or embedded_declared:
        c4 = ("ok", "")
    else:
        c4 = ("missing", "no-download")

    for item, val in zip(ITEMS, (c1, c2, c3, c4), strict=True):
        result[item] = ("exempt", "exempt") if item in exempted else val
    return result


def cite_grade(html: str) -> str:
    """C3 分级（仅报告用·不参与门禁判定）：L3 结构化引用 > L2 <cite>/引用区块 > L1 站 URL > L0 无。"""
    region, _ = region_of(html)
    if re.search(r"BibTeX|APA|MLA", html, re.I):
        return "L3"
    if RE_CITE_BLOCK.search(html):
        return "L2"
    if RE_SITE_URL.search(region):
        return "L1"
    return "L0"


def rel_key(page: Path) -> str:
    return str(page.relative_to(ROOT)).replace("\\", "/")


def disp(p: Path) -> str:
    """路径展示：仓库内用相对路径，仓库外（如自检临时目录）退回绝对路径——
    避免错误消息本身抛异常，把「明确拒绝」变成「崩溃」。"""
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def evaluate(pages: list[Path]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for p in pages:
        try:
            res = check_page(p)
        except Exception as e:  # noqa: BLE001
            res = {i: ("missing", f"parse-error:{type(e).__name__}") for i in ITEMS}
        out[rel_key(p)] = {i: f"{st}|{rc}" for i, (st, rc) in res.items()}
    return out


# ---------------- 基线 ----------------

def baseline_path() -> Path:
    """基线位置守卫（fail-closed 前置）。"""
    return BASELINE


def parse_baseline() -> dict[str, dict[str, str]]:
    """基线文件：`page|item|status|snapshot` 每行一条。返回 {page: {item: status}}。"""
    data: dict[str, dict[str, str]] = {}
    for line in baseline_path().read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        bits = line.split("|")
        if len(bits) < 3:
            continue
        page, item, status = bits[0], bits[1], bits[2]
        data.setdefault(page, {})[item] = status
    return data


def generate_baseline(pages: list[Path], snapshot: str) -> int:
    results = evaluate(pages)
    lines = [
        "# 第 28 门禁 · 可视化可引用性基线（B-6 第一步）",
        f"# 生成：{snapshot} · 页数 {len(pages)} · 每页四项 = {len(pages) * 4} 行",
        "# 语义：违规集合单调不增——本文件内 missing 为冻结存量（WARN 豁免）；",
        "#       基线外 missing = FAIL 阻断；missing 项修复后应删除本行（收紧）。",
        "# 格式：page|item|status|snapshot   status ∈ ok | missing:reason | exempt",
    ]
    n_missing = 0
    for page in sorted(results):
        for item in ITEMS:
            st, rc = results[page][item].split("|", 1)
            status = "ok" if st == "ok" else ("exempt" if st == "exempt" else f"missing:{rc}")
            if st == "missing":
                n_missing += 1
            lines.append(f"{page}|{item}|{status}|{snapshot}")
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    baseline_path().write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"基线已生成：{disp(baseline_path())} · {len(results)} 页 · {len(results) * 4} 行 · missing {n_missing}")
    for item in ITEMS:
        ok_n = sum(1 for p in results for i, v in results[p].items() if i == item and v.startswith("ok"))
        print(f"  {item} 通过 {ok_n}/{len(results)}")
    return 0


def gate(pages: list[Path]) -> int:
    if not baseline_path().exists():
        print(f"FAIL 基线缺失：{disp(baseline_path())} — refuse to pass（先跑 --generate-baseline）")
        return 1
    try:
        base = parse_baseline()
    except Exception as e:  # noqa: BLE001
        print(f"FAIL 基线不可解析：{e}")
        return 1
    results = evaluate(pages)
    new_v, frozen, tighten, exempt_n = [], [], [], 0
    for page, items in results.items():
        for item, val in items.items():
            st, rc = val.split("|", 1)
            if st == "exempt":
                exempt_n += 1
                continue
            if st == "ok":
                if base.get(page, {}).get(item, "ok").startswith("missing"):
                    tighten.append(f"{page}|{item}")
                continue
            prev = base.get(page, {}).get(item)
            if prev is None:
                new_v.append(f"{page} :: {item} {rc}（页/项未入基线·新增面）")
            elif prev.startswith("missing"):
                frozen.append(f"{page} :: {item} {rc}")
            else:
                new_v.append(f"{page} :: {item} {rc}（基线原为 {prev}·回归）")
    for line in new_v:
        print(f"FAIL {line}")
    for line in tighten:
        print(f"TIGHTEN 已修复可收紧基线行：{line}")
    print(
        f"---- 第 28 门禁：扫描 {len(pages)} 页 · 基线外违规 {len(new_v)} · 冻结存量 {len(frozen)} · "
        f"可收紧 {len(tighten)} · 豁免 {exempt_n} ----"
    )
    if frozen:
        print(f"WARN 存量缺口 {len(frozen)} 项已冻结豁免（D4：收敛至阈值以下再转 FAIL·详见报告）")
    return 1 if new_v else 0


def report(pages: list[Path], out_path: Path) -> int:
    results = evaluate(pages)
    payload = {
        "scan_date": date.today().isoformat(),
        "scope": "site/data (D1: 不含 EN 镜像)",
        "pages": len(pages),
        "items": ITEMS,
        "pass_rate": {},
        "detail": {},
    }
    for item in ITEMS:
        ok_n = sum(1 for p in results for i, v in results[p].items() if i == item and v.startswith(("ok", "exempt")))
        payload["pass_rate"][item] = f"{ok_n}/{len(pages)}"
    for p in sorted(pages):
        key = rel_key(p)
        html = p.read_text(encoding="utf-8")
        payload["detail"][key] = {
            "items": {i: dict(zip(("status", "reason"), results[key][i].split("|", 1), strict=True)) for i in ITEMS},
            "cite_grade": cite_grade(html),
            "has_anchor": bool(RE_ANCHOR_DIV.search(html)),
        }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print("通过率：" + " · ".join(f"{k} {v}" for k, v in payload["pass_rate"].items()))
    print(f"报告已写出：{disp(out_path)}")
    return 0


# ---------------- 自检 ----------------

GOOD_PAGE = """<html><body>
<div class="notice" id="dataSource">
  数据源：实时加载自 <code>json/hardships_81.json</code>，由 scripts/AA_劫难分析/hardships_81.py 生成（口径：八十一难五级分类·样本 100 回·快照 2026-09-30）
  详见 https://1273984347.github.io/xiyouji/data/81-hardships.html
</div><a href="json/hardships_81.json" download="x.json">下载</a></body></html>"""

BAD_C1 = GOOD_PAGE.replace("快照 2026-09-30", "")  # 去版本 → C1 missing:no-version
BAD_C2 = GOOD_PAGE.replace("scripts/AA_劫难分析/hardships_81.py 生成（口径：八十一难五级分类·样本 100 回·", "")
BAD_C3 = GOOD_PAGE.replace("https://1273984347.github.io/xiyouji/data/81-hardships.html", "")
BAD_C4 = GOOD_PAGE.replace('<a href="json/hardships_81.json" download="x.json">下载</a>', "")


def self_test() -> int:
    tmp = ROOT / ".review-tmp" / "citability-selftest"
    tmp.mkdir(parents=True, exist_ok=True)
    cases = [
        ("good.html", GOOD_PAGE, None),
        ("bad_c1.html", BAD_C1, "C1"),
        ("bad_c2.html", BAD_C2, "C2"),
        ("bad_c3.html", BAD_C3, "C3"),
        ("bad_c4.html", BAD_C4, "C4"),
    ]
    rc = 0
    for name, html, want_bad in cases:
        f = tmp / name
        f.write_text(html, encoding="utf-8")
        res = check_page(f)
        bad = {i for i, (st, _) in res.items() if st == "missing"}
        if want_bad is None:
            ok = not bad
            detail = f"期望全通过 · 实际 missing={sorted(bad) or '无'}"
        else:
            ok = want_bad in bad and len(bad) == 1
            detail = f"期望仅 {want_bad} 失败 · 实际 missing={sorted(bad)}"
        rc = rc if ok else 2
        print(f"{'OK  ' if ok else 'FAIL'} {name}: {detail}")
    # 构建工具排除回归：仅有 inline_css.py 引用的页，C2 必须判 build-tool-only 而非通过
    f = tmp / "buildtool.html"
    f.write_text(
        '<div id="dataSource">数据源：见 scripts/inline_css.py 与 scripts/w334_font_subset.py（2026-09-30 快照）'
        '<a href="json/x.json" download>下载</a></div>',
        encoding="utf-8",
    )
    res = check_page(f)
    ok = res["C2"][0] == "missing" and res["C2"][1] == "build-tool-only"
    rc = rc if ok else 2
    print(f"{'OK  ' if ok else 'FAIL'} buildtool.html: C2 应为 build-tool-only（v1.0 假阳性回归）· 实际 {res['C2']}")
    print("self-test", "PASS" if rc == 0 else "FAIL")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser(description="第 28 门禁 · 可视化可引用性检查")
    ap.add_argument("--generate-baseline", action="store_true", help="首跑冻结存量基线")
    ap.add_argument("--gate", action="store_true", help="门禁模式：基线外违规=FAIL（verify_delivery 调用）")
    ap.add_argument("--self-test", action="store_true", help="负样本自检")
    ap.add_argument("--json", dest="json_out", help="报告输出路径（默认 scripts/output/citability-report.json）")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    pages = scan_pages()
    if not pages:
        print(f"FAIL 未扫到页面：{SITE_DATA}")
        return 1
    if args.generate_baseline:
        return generate_baseline(pages, date.today().isoformat())
    if args.gate:
        return gate(pages)
    return report(pages, Path(args.json_out) if args.json_out else DEFAULT_REPORT)


if __name__ == "__main__":
    sys.exit(main())
