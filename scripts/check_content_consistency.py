#!/usr/bin/env python3
"""check_content_consistency.py — W555 方案 C 数据内容一致性检查（L1 站内自洽 / L2 站-dataset 对账）。

来源：plans/2026-09-06-w552-three-optional-batches-plans.md 方案 C。W550 实证三类同页数字矛盾
（relationships 89 回 vs 图例 88；narratology-13d 13/16/17 维度混用；six-senses 声明 5 vs 桑基 4），
本脚本把「同实体+不同值」矛盾规则化为机器判据。是否挂载 verify_delivery 第 25 门禁**须经用户确认**，
本脚本默认只跑批出清单（不阻断）。

用法：
  python scripts/check_content_consistency.py                 # L1 全站扫描（site/*.html）
  python scripts/check_content_consistency.py --self-test     # 负样本回放自检（W550 三案例 + 好样本）
  python scripts/check_content_consistency.py --dataset       # L2 EMBEDDED_DATA vs dataset/<同名>.json
  python scripts/check_content_consistency.py --json OUT      # 机器可读输出

退出码：发现矛盾（FAIL 级）= 1，否则 0。--self-test 断言失败 = 2。

已知口径限制：L1 为报告型启发式（轴标签/代码示例文本可能产生少量误报，逐条人工裁决）；
EMBEDDED_DATA 解析容忍 JS 无引号键与尾逗号（机器生成的内嵌数据形态）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DS_DIR = ROOT / "dataset"
BASELINE = ROOT / "scripts" / "content-consistency-baseline.txt"

# 计数词（中英）
COUNTER = r"(?:回|次|条|个|篇|维|层|类|项|种|页|座|位|名|nodes?|links?|edges?|dimensions?|cases?|chapters?|works?|types?)"
# 实体对：A与B / A和B / A-B / A×B（两侧懒匹配，保证同名实体对提取键稳定）
PAIR = r"([0-9A-Za-z一-鿿·]{1,14}?)[与和×xX\-—–]([0-9A-Za-z一-鿿·]{1,14}?)"
# 主语截断词（功能词/动词边界）
SUBJ_CUT = r"的|构建|覆盖|呈现|展现|展示|组成|构成|形成|分为|包括|描述|分析|讨论|围绕|讲述|其中"


class _TextExtract(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip and data.strip():
            self.parts.append(data)


def visible_text(html: str) -> str:
    p = _TextExtract()
    p.feed(html)
    return "".join(p.parts)


def js_of(html: str) -> str:
    return "\n".join(re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.S | re.I))


def arrays_in_js(js: str) -> list[list[dict]]:
    """提取 JS 中「对象数组字面量」（[...]; 赋值形态，键名引号归一后 JSON 解析）。"""
    out = []
    for m in re.finditer(r"=\s*(\[\s*\{.*?\}\s*\])\s*;", js, re.S):
        blob = re.sub(r",(\s*[}\]])", r"\1", m.group(1))
        blob = re.sub(r"([{,\n]\s*)([A-Za-z_][A-Za-z0-9_$]*)(\s*):", r'\1"\2"\3:', blob)
        try:
            data = json.loads(blob)
            if isinstance(data, list) and data and all(isinstance(x, dict) for x in data):
                out.append(data)
        except Exception:  # noqa: BLE001
            continue
    return out


def extract_embedded(html: str) -> dict | None:
    """提取 EMBEDDED_DATA = {...}（花括号配平；JS 键名引号归一；尾逗号容忍）。"""
    m = re.search(r"EMBEDDED_DATA\s*=\s*\{", html)
    if not m:
        return None
    start = m.end() - 1
    depth = 0
    in_str = ""
    i = start
    while i < len(html):
        ch = html[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == in_str:
                in_str = ""
            i += 1
            continue
        if ch in ('"', "'", "`"):
            in_str = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                blob = html[start : i + 1]
                blob = re.sub(r",(\s*[}\]])", r"\1", blob)
                blob = re.sub(r"([{,\n]\s*)([A-Za-z_][A-Za-z0-9_$]*)(\s*):", r'\1"\2"\3:', blob)
                try:
                    return json.loads(blob)
                except Exception:  # noqa: BLE001
                    return None
        i += 1
    return None


def claims(text: str) -> list[tuple[int, str, str, str]]:
    """提取 (数字, 计数词, 后置主语, 上下文)——「13 个维度」→ (13, 个, 维度)。"""
    out = []
    for m in re.finditer(r"(\d{1,5})\s*(" + COUNTER + r")\s*([0-9A-Za-z一-鿿]{0,8})", text):
        if int(m.group(1)) >= 1000 and not m.group(2).endswith("年"):
            continue  # 年份/ID 类大数非计数声明
        subj = re.split(SUBJ_CUT, m.group(3), maxsplit=1)[0]
        if subj.isascii() and (len(subj) > 8 or subj[:1].isupper()):
            continue  # visible_text 拼接伪影
        s_ = max(0, m.start() - 20)
        ctx = text[s_ : m.end()].replace("\n", " ")
        out.append((int(m.group(1)), m.group(2), subj, ctx))
    return out


def pair_claims(text: str) -> list[tuple[str, int, str]]:
    """提取（实体对, 数字, 计数形态）——窗口 40 字符内的「数字+计数词」或裸括号数字 (88)。

    实体对键做最短子串规范化：同页互为子串的匹配归并到最短键，保证同实体归组稳定。
    """
    raw = []
    for m in re.finditer(PAIR, text):
        if any(ch.isdigit() for ch in m.group(0)):
            continue  # 数字区间/轴标签（如「1-1」「第3-7」）非实体对
        window = text[m.end() : m.end() + 40]
        nm = re.search(r"(\d{1,5})\s*(" + COUNTER + r")", window)
        pm = re.search(r"[（(](\d{1,5})[)）]", window)
        if nm:
            raw.append((m.group(0), int(nm.group(1)), nm.group(2)))
        elif pm:
            raw.append((m.group(0), int(pm.group(1)), "(裸)"))
    keys = sorted({p for p, _n, _c in raw}, key=len)
    out = []
    for pair, num, cnt in raw:
        key = next((k for k in keys if k != pair and k in pair), pair)
        out.append((key, num, cnt))
    return out


def check_page(path: Path) -> list[str]:
    """L1：单页规则检查，返回 FAIL 描述列表。"""
    html = path.read_text(encoding="utf-8", errors="replace")
    text = visible_text(html)
    js = js_of(html)
    fails: list[str] = []

    arrays = arrays_in_js(js)
    node_arrays = [a for a in arrays if a and all(("id" in x or "name" in x) for x in a)]
    link_arrays = [a for a in arrays if a and all(("source" in x and "target" in x) for x in a)]

    # 规则 1：网络图注 节点数/边数 vs 数组字面长度（页面仅一组 nodes/links 数组时才判）
    if len(node_arrays) == 1 and len(link_arrays) == 1:
        n_nodes, n_links = len(node_arrays[0]), len(link_arrays[0])
        for num, cnt, subj, ctx in claims(text):
            key = cnt + subj
            if ("节点" in key or re.fullmatch(r"nodes?", key)) and num != n_nodes:
                fails.append(f"规则1 节点数矛盾：文案 {num} vs nodes 数组 {n_nodes}（…{ctx}…）")
            if ("边" in key or re.fullmatch(r"(links?|edges?)", key)) and num != n_links:
                fails.append(f"规则1 边数矛盾：文案 {num} vs links 数组 {n_links}（…{ctx}…）")

    # 规则 2：桑基图注 节点数 vs links 去重节点数
    if "d3.sankey(" in js and len(link_arrays) == 1:
        dedupe = set()
        for x in link_arrays[0]:
            dedupe.add(str(x.get("source")))
            dedupe.add(str(x.get("target")))
        for num, cnt, subj, ctx in claims(text):
            if ("节点" in cnt + subj or re.fullmatch(r"nodes?", cnt + subj)) and num != len(dedupe):
                fails.append(f"规则2 桑基节点数矛盾：文案 {num} vs links 去重 {len(dedupe)}（…{ctx}…）")

    # 规则 3a：同页同主语（计数词后置名词）出现 ≥2 个不同数字
    subj_vals: dict[str, set[int]] = {}
    for num, cnt, subj, _ctx in claims(text):
        if len(subj) >= 2:
            key = cnt + subj
            if key.isascii() and len(key) > 10:
                continue  # ASCII 粘连伪影
            if re.fullmatch(r"[一-鿿]", cnt) and subj.isascii():
                continue  # CJK 计数词 + 纯 ASCII 主语 = 代码/轴文本粘连
            subj_vals.setdefault(key, set()).add(num)
    for key, nums in subj_vals.items():
        if len(nums) >= 2:
            fails.append(f"规则3 同主语计数矛盾：「{key}」出现多个值 {sorted(nums)}")

    # 规则 3b：同页同实体对出现 ≥2 个不同数字（计数词或裸括号数字）
    pair_vals: dict[str, set[int]] = {}
    for pair, num, _cnt in pair_claims(text):
        pair_vals.setdefault(pair, set()).add(num)
    for pair, nums in pair_vals.items():
        if len(nums) >= 2:
            fails.append(f"规则3 实体对计数矛盾：「{pair}」出现多个值 {sorted(nums)}")

    # 规则 4：单 links 数组页，案例/流程类声明数 vs 实际边数
    if len(link_arrays) == 1:
        n_links = len(link_arrays[0])
        for num, _cnt, subj, ctx in claims(text):
            if subj in ("案例", "流程", "链路", "分支", "flows", "cases", "scene", "scenes") and num != n_links:
                fails.append(f"规则4 案例数矛盾：文案 {num} vs links 数组 {n_links}（…{ctx}…）")
    return fails


# ---------------- self-test 固定样本（W550 三案例复刻 + 好样本） ----------------
BAD_RELATIONSHIPS = """
<div class="chart-title">人物关系网络</div>
<p>唐僧-孙悟空两人之间 89 回共现，为全书第一。</p>
<script>var links=[{"source":"唐僧","target":"孙悟空","value":88}];</script>
<span>唐僧-孙悟空 (88)</span>
"""
BAD_13D = """
<p>全书共 13 个维度构建叙事网络。</p>
<p>扩展口径覆盖 16 个维度，含 17 个维度的完整版。</p>
"""
BAD_SIXSENSES = """
<p>本图呈现 5 个案例。</p>
<script>var links=[{"source":"眼","target":"色","value":1},{"source":"耳","target":"声","value":1},{"source":"鼻","target":"香","value":1},{"source":"舌","target":"味","value":1}];svg.call(d3.sankey());</script>
"""
GOOD_SAMPLE = """
<div class="chart-title">人物关系网络（2 个节点 · 1 条边）</div>
<p>唐僧-孙悟空 89 回共现，为全书第一。</p>
<script>var nodes=[{"id":"唐僧"},{"id":"孙悟空"}];var links=[{"source":"唐僧","target":"孙悟空","value":88}];</script>
"""


def self_test() -> int:
    tmp = ROOT / ".review-tmp" / "selftest"
    tmp.mkdir(parents=True, exist_ok=True)
    cases = [
        ("bad_relationships.html", BAD_RELATIONSHIPS, True),
        ("bad_13d.html", BAD_13D, True),
        ("bad_sixsenses.html", BAD_SIXSENSES, True),
        ("good_sample.html", GOOD_SAMPLE, False),
    ]
    rc = 0
    for name, html, expect_hit in cases:
        f = tmp / name
        f.write_text(html, encoding="utf-8")
        fails = check_page(f)
        hit = bool(fails)
        status = "OK " if hit == expect_hit else "FAIL"
        if hit != expect_hit:
            rc = 2
        print(f"{status} {name}: expect_hit={expect_hit} hit={hit} {fails if fails else ''}")
    print("self-test", "PASS" if rc == 0 else "FAIL")
    return rc


def load_baseline() -> set[str]:
    """基线冻结名单：`page::message`（页相对路径 / 归一）。存量误报冻结豁免，只拦新增。"""
    if not BASELINE.exists():
        return set()
    out = set()
    for line in BASELINE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.add(line)
    return out


def l1(gate: bool = False) -> int:
    pages = sorted(SITE.rglob("*.html"))
    # _template/_shell 模板壳；dukou-engine 为 Agent 控制台元页面（全文是开发术语，非内容声明页）
    pages = [p for p in pages if p.stem not in ("_template", "_shell", "dukou-engine")]
    baseline = load_baseline() if gate else set()
    frozen = []
    all_fails = {}
    for p in pages:
        try:
            fails = check_page(p)
        except Exception as e:  # noqa: BLE001
            fails = [f"解析异常: {e}"]
        if fails:
            all_fails[str(p.relative_to(ROOT))[:60]] = fails
    n_new = 0
    for page, fails in all_fails.items():
        key_norm = page.replace("\\", "/")
        for f in fails:
            full = f"{key_norm} :: {f}"
            if gate and full in baseline:
                frozen.append(full)
                continue
            n_new += 1
            print(f"FAIL {page} :: {f}")
    for line in frozen:
        print(f"FROZEN（基线冻结存量误报，豁免）{line.split(' :: ', 1)[-1][:0]}{line}")
    print(f"---- L1 扫描 {len(pages)} 页 · 矛盾 {n_new + len(frozen)} 条 · 新增 {n_new} · 基线冻结 {len(frozen)} ----")
    if gate:
        return 1 if n_new else 0
    return 1 if (n_new + len(frozen)) else 0


def l2() -> int:
    """L2 站-dataset 对账：site/data/<X>.html 的 EMBEDDED_DATA vs dataset/<X>.json 同名同源。

    比对：同名顶层键——list 对长度，dict/list 元素抽样逐字段相等（每页每键最多 8 项）。
    """
    drift = []
    n_pages = 0
    for hp in sorted((SITE / "data").glob("*.html")):
        src = DS_DIR / (hp.stem + ".json")
        if not src.exists():
            continue
        html = hp.read_text(encoding="utf-8", errors="replace")
        embedded = extract_embedded(html)
        if embedded is None:
            continue
        try:
            source = json.loads(src.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            drift.append(f"{hp.name}: JSON 解析失败 {e}")
            continue
        n_pages += 1
        mism = []
        checked = 0
        for key, ev in embedded.items():
            if key not in source or checked >= 8:
                continue
            sv = source[key]
            if isinstance(ev, list) and isinstance(sv, list):
                if len(ev) != len(sv):
                    mism.append(f"{key}: 页 {len(ev)} 项 vs dataset {len(sv)} 项")
                    checked += 1
                    continue
                for i, (a, b) in enumerate(zip(ev, sv, strict=False)):
                    if isinstance(a, dict) and isinstance(b, dict):
                        for k in list(a)[:6]:
                            if k in b and a[k] != b[k]:
                                mism.append(f"{key}[{i}].{k}: 页 {a[k]!r} vs dataset {b[k]!r}")
                                break
                    elif a != b:
                        mism.append(f"{key}[{i}]: 页 {a!r} vs dataset {b!r}")
                    checked += 1
                    if checked >= 8:
                        break
            elif isinstance(ev, dict) and isinstance(sv, dict):
                for k in list(ev)[:6]:
                    if k in sv and ev[k] != sv[k]:
                        mism.append(f"{key}.{k}: 页 {ev[k]!r} vs dataset {sv[k]!r}")
                        break
                checked += 1
        if mism:
            drift.append(f"{hp.name}: " + "；".join(mism[:4]))
    for d in drift:
        print("DRIFT", d)
    print(f"---- L2 对账 {n_pages} 页（EMBEDDED ∩ dataset 同名） · 漂移 {len(drift)} 页 ----")
    return 1 if drift else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--dataset", action="store_true", help="L2 站-dataset 对账模式")
    ap.add_argument("--gate", action="store_true", help="门禁模式（W555 第 25 门禁：基线冻结存量、只拦新增）")
    ap.add_argument("--json", dest="json_out", help="机器可读输出路径")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.dataset:
        return l2()
    return l1(gate=args.gate)


if __name__ == "__main__":
    sys.exit(main())
