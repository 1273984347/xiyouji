#!/usr/bin/env python3
"""check_fallback_fidelity.py — 第 79 门禁 · 回退块保真度（W1265 批一·判据补盲 1-8）。

背景（《全站网页可视化图表审查报告 2026-11-16 · W1259》P1-2）：
  AGENTS.md L101 铁律要求所有 site/data 可视化页内嵌 EMBEDDED 回退，"fetch 失败时仍可渲染
  （file:// 双击可用）"。但部分页面的「回退块」实为 **mock 假数据**：
    journey-route        真值 total_places=53 / places 53 条 → 回退 mock 仅 5 个地点（-90%）
    character-appearance 真值 characters 40 人            → 回退 mock 仅 15 人（-62.5%）
    chapter-stats        真值 per_chapter 100 条          → 回退 mock 仅 10 回示例
  ⇒ "有 EMBEDDED" 只满足形式检查项，实质违反铁律：离线双击（站点明示支持的场景）拿到的数据
  比在线更差，且同页 KPI 与文案自相矛盾。

判据（方向：回退块必须是**真值快照**，不得是 mock；条目数须与真值相等）：
  F1  回退块变量名含 MOCK（EMBEDDED_MOCK / MOCK_CHARACTERS / MOCK_DATA）→ 违例
  F1b 回退块**内容**含强 mock 声明标记（mock 数据 / mock data / fallback mock /
      embedded mock / 内嵌 mock / 回退 mock / 示例数据 / 演示数据）→ 违例
      ※ 只用**强标记**：「离线示例 / 内置示例」属 live-API 页的合法离线降级（徽标正本
        STATUS_TEXT.live 已声明"服务未启动时自动回退到发布快照"）⇒ 不判红。
      ※ 不用泛化的 \b(fake|sample|demo)\b 扫块内容：W1265 实测假阳性两例——
        en/social-media 的数据文案 "photo 2 is fake"、en/character-relationship-3d 的
        角色名 "Fake Wukong" 都会被误判 ⇒ 判据只认「身份标识 + 强声明标记」。
  F2  回退块条目数须等于真值 → 违例
      口径：把回退块解析成结构（路径→数组长度 / 路径→数值标量），与该页 fetch 目标对应的
            **真值 JSON**（site/data/json/ 或 site/en/json/ 或 scripts/output/data/）对拍：
              · 同路径数组长度不等 → 违例（真值 53 处 → 回退 5 处）
              · 同路径数值标量不等 → 违例
              · 形状不同（回退是根数组·真值是对象）→ 取「回退最大数组长度 vs 真值最大数组
                长度」对比（真值 40 人 → 回退 15 人）
            无可确定真值的页（不 fetch）只判 F1/F1b。

存量基线：审查报告实测 3 页（journey-route / character-appearance / chapter-stats·含 EN 对应页
  = 6 页）。门禁默认「基线冻结」形态：基线内记「存量基线」不计 FAIL；基线外新增照样 FAIL；
  零容忍：--strict（基线不参与判定·全部违例计 FAIL）。

用法：
  py -3 scripts/check_fallback_fidelity.py
  py -3 scripts/check_fallback_fidelity.py --strict
  py -3 scripts/check_fallback_fidelity.py --report
  py -3 scripts/check_fallback_fidelity.py --generate-baseline
  py -3 scripts/check_fallback_fidelity.py --self-test
退出码：0 通过 / 1 违例或基线缺失（fail-closed）/ 2 自测失败
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from lib import freeze_gate, json_refs  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MARKER = "---- 第 79 门禁 回退块保真度："
BASELINE = ROOT / "scripts" / "output" / "fallback-fidelity-baseline.txt"
SITE_DIRS = ("site/data", "site/en")
SKIP_STEMS = ("_shell", "_template")

RE_BLOCK_VAR = re.compile(r"(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*([\[{])")
RE_MOCK_NAME = re.compile(r"(?i)mock")
RE_STRONG_MARKERS = (
    "mock 数据",
    "mock data",
    "fallback mock",
    "mock fallback",
    "embedded mock",
    "内嵌 mock",
    "回退 mock",
    "mock 回退",
    "示例数据",
    "演示数据",
)
RE_STRONG = re.compile("|".join(re.escape(m) for m in RE_STRONG_MARKERS), re.I)
RE_TRAILING_COMMA = re.compile(r",(\s*[}\]])")
RE_BARE_KEY = re.compile(r"([{,]\s*)([A-Za-z_$][\w$]*)(\s*:)")
RE_SINGLE_QUOTE = re.compile(r"'([^'\"\\]*)'")


def _balanced_literal(src: str, open_idx: int) -> str | None:
    """取 '[' / '{' 起的字面量正文（配平扫描·跳过字符串）。"""
    depth = 0
    in_str = ""
    esc = False
    for i in range(open_idx, len(src)):
        ch = src[i]
        if in_str:
            if esc:
                esc = False
                continue
            if ch == "\\":
                esc = True
                continue
            if ch == in_str:
                in_str = ""
            continue
        if ch in "'\"":
            in_str = ch
            continue
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
            if depth == 0:
                return src[open_idx : i + 1]
    return None


def loose_json(text: str):
    """JS 字面量 → Python 对象（宽松预处理）。

    站内 EMBEDDED 常带无引号键与尾逗号（审查报告《探针法教训》第 3 条）⇒ 直接 json.loads 必失败。
    """
    out = RE_TRAILING_COMMA.sub(r"\1", text)
    out = RE_BARE_KEY.sub(r'\1"\2"\3', out)
    out = RE_SINGLE_QUOTE.sub(r'"\1"', out)
    try:
        return json.loads(out)
    except (ValueError, TypeError):
        return None


def structure(obj, prefix: str = "$") -> tuple[dict, dict, dict]:
    """对象 → (数组路径→长度, 标量路径→值, 数组路径→首元素键集)。

    键集用于「形状不同」时的同族判定（回退是根数组·真值是对象 ⇒ 按元素键集找同族数组）。
    """
    arrays: dict[str, int] = {}
    scalars: dict[str, object] = {}
    elem_keys: dict[str, frozenset] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = "%s.%s" % (prefix, k)
            if isinstance(v, (list, dict)):
                sub_a, sub_s, sub_k = structure(v, path)
                arrays.update(sub_a)
                scalars.update(sub_s)
                elem_keys.update(sub_k)
            else:
                scalars[path] = v
    elif isinstance(obj, list):
        arrays[prefix] = len(obj)
        for v in obj[:1]:
            if isinstance(v, dict):
                elem_keys[prefix] = frozenset(v.keys())
        for i, v in enumerate(obj[:3]):
            if isinstance(v, (list, dict)):
                sub_a, sub_s, sub_k = structure(v, "%s[%d]" % (prefix, i))
                arrays.update(sub_a)
                scalars.update(sub_s)
                elem_keys.update(sub_k)
    return arrays, scalars, elem_keys


def find_fallback_blocks(html: str) -> list[tuple[str, str]]:
    """找回退块 → [(变量名, 字面量源码)]。变量名须含 EMBEDDED/MOCK/FALLBACK/SAMPLE/DEMO。"""
    out: list[tuple[str, str]] = []
    src = json_refs.strip_comments(html)
    for m in RE_BLOCK_VAR.finditer(src):
        name = m.group(1)
        if not re.search(r"(?i)(EMBEDDED|MOCK|FALLBACK|SAMPLE|DEMO)", name):
            continue
        lit = _balanced_literal(src, m.end() - 1)
        if lit:
            out.append((name, lit))
    return out


def truth_candidates(page_rel: str, targets) -> list[Path]:
    """该页可用的真值 JSON 候选（fetch 目标解析后存在的文件）。"""
    out: list[Path] = []
    for target, _rule in targets:
        resolved = json_refs.norm_path(json_refs.resolve_http_path(page_rel, target))
        cand = ROOT / resolved
        if cand.is_file() and cand.suffix == ".json" and cand not in out:
            out.append(cand)
    return out


def _truth_structures(paths) -> tuple[dict, dict, dict]:
    arrays: dict[str, int] = {}
    scalars: dict[str, object] = {}
    elem_keys: dict[str, frozenset] = {}
    for t in paths:
        try:
            obj = json.loads(t.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        a, s, k = structure(obj)
        arrays.update(a)
        scalars.update(s)
        elem_keys.update(k)
    return arrays, scalars, elem_keys


_PARSE_FAILS: list[str] = []   # W1271 P2-2：宽松解析失败的回退块（main 末尾 NOTE 计数·防静默豁免面）


def _f2_violations(page_rel: str, name: str, lit: str, truth_arr: dict, truth_sca: dict, truth_keys=None) -> list[str]:
    """F2：回退块条目数/值 ≠ 真值。解析失败不计 F2 但记入 _PARSE_FAILS（可见性）。"""
    viol: list[str] = []
    obj = loose_json(lit)
    if obj is None:
        _PARSE_FAILS.append("%s|%s" % (page_rel, name))
        return viol
    arr, sca, fb_keys = structure(obj)
    truth_keys = truth_keys or {}
    matched = False
    for path, ln in sorted(arr.items()):
        tv = truth_arr.get(path)
        if tv is None:
            continue
        matched = True
        if tv != ln:
            viol.append("%s|F2|回退块 %s 路径 %s 条目数 %d ≠ 真值 %d" % (page_rel, name, path, ln, tv))
    for path, val in sorted(sca.items()):
        tv = truth_sca.get(path)
        if isinstance(val, (int, float)) and isinstance(tv, (int, float)) and abs(val - tv) > 1e-9:
            matched = True
            viol.append("%s|F2|回退块 %s 路径 %s 值 %s ≠ 真值 %s" % (page_rel, name, path, val, tv))
    if not matched and arr and truth_arr:
        # 形状不同（回退是根数组 / 真值是对象）⇒ 按**元素键集同族**找真值数组再比长度
        fb_root_keys = fb_keys.get("$", frozenset())
        peers = []
        if fb_root_keys:
            for p, ks in truth_keys.items():
                if ks and len(ks & fb_root_keys) >= 2:
                    peers.append((p, truth_arr[p]))
        if peers:
            tv_path, tv_len = max(peers, key=lambda x: x[1])
            fb_len = arr.get("$", max(arr.values()))
            if fb_len < tv_len:
                viol.append("%s|F2|回退块 %s 条目数 %d ≠ 真值 %s %d（元素键集同族）"
                            % (page_rel, name, fb_len, tv_path, tv_len))
        else:
            fb_max = max(arr.values())
            tv_max = max(truth_arr.values())
            if fb_max < tv_max:
                viol.append("%s|F2|回退块 %s 最大条目数 %d ≠ 真值 %d" % (page_rel, name, fb_max, tv_max))
    return viol


def scan_page(page_rel: str, html: str, truth_paths=None, truth=None) -> list[str]:
    """扫描一页 → 违例键列表。

    truth_paths 为 None 时从页面 fetch 目标推导真值；truth=(arr, sca, keys) 时直接注入
    内存真值（W1271 对抗审查 P2-3 修：自测此前经手工重拼绕过 scan_page 真实管线，
    「从 fetch 目标推导真值」路径零自测覆盖——注入形参让自测真跑主管线）。"""
    viol: list[str] = []
    blocks = find_fallback_blocks(html)
    if not blocks:
        return viol
    if truth_paths is None:
        targets, _ = json_refs.extract_targets(html)
        truth_paths = truth_candidates(page_rel, targets)
    if truth is not None:
        truth_arr, truth_sca, truth_keys = truth
    else:
        truth_arr, truth_sca, truth_keys = _truth_structures(truth_paths)
    for name, lit in blocks:
        if RE_MOCK_NAME.search(name):
            viol.append("%s|F1|回退块 %s 变量名含 MOCK（不得以示例数据充当回退）" % (page_rel, name))
        m = RE_STRONG.search(lit)
        if m:
            viol.append("%s|F1b|回退块 %s 含 mock 声明「%s」" % (page_rel, name, m.group(0)))
        if truth_arr or truth_sca:
            viol.extend(_f2_violations(page_rel, name, lit, truth_arr, truth_sca, truth_keys))
    return viol


def scan_site() -> tuple[list[str], dict[str, list[str]]]:
    viol: list[str] = []
    per_page: dict[str, list[str]] = {}
    for d in SITE_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for f in sorted(base.glob("*.html")):
            if f.stem in SKIP_STEMS:
                continue
            page_rel = d + "/" + f.name
            html = f.read_text(encoding="utf-8", errors="ignore")
            v = scan_page(page_rel, html)
            if v:
                viol.extend(v)
                per_page[page_rel] = v
    return viol, per_page


def self_test() -> int:
    """负样本自测：违例必红·正常必绿·基线语义正确。"""
    truth = {"total_places": 53, "places": [{"n": i} for i in range(53)], "characters": [{"n": i} for i in range(40)]}
    cases = [
        ("正样本-回退块与真值一致", '{"total_places": 53}', "EMBEDDED_DATA", 0),
        ("负样本-F1 变量名含 MOCK", '{"total_places": 53}', "EMBEDDED_MOCK", 1),
        ("负样本-F1b 块内含强 mock 声明", '{"total_places": 53, "note": "嵌入 mock 数据"}', "EMBEDDED_DATA", 1),
        ("负样本-F2 数组条目数少于真值", '{"places": [{"n": 0}]}', "EMBEDDED_DATA", 1),
        ("负样本-F2 标量值不等于真值", '{"total_places": 5}', "EMBEDDED_DATA", 1),
        ("负样本-F2 形状不同（根数组 15 vs 真值 40）", '[{"n": 1}]', "EMBEDDED_CHARACTERS", 1),
        ("正样本-数据文案含 fake 不判红", '{"desc": "photo 2 is fake"}', "EMBEDDED_DATA", 0),
        ("正样本-角色名 Fake Wukong 不判红", '{"desc": "Fake Wukong; indistinguishable"}', "EMBEDDED_DATA", 0),
        ("正样本-仅离线示例字样不判红", '{"note": "离线示例 · 内置示例"}', "EMBEDDED_DATA", 0),
    ]
    bad = 0
    for name, lit, var, expect in cases:
        html = "<script>const %s = %s;</script>" % (var, lit)
        # W1271 P2-3 修：内存真值经 truth 注入直通 scan_page 主管线（fetch 推导路径另有用例）
        t_arr, t_sca, t_keys = structure(truth)
        viol = scan_page("site/en/_selftest.html", html, truth=(t_arr, t_sca, t_keys))
        ok = len(viol) == expect
        print("%s %s：期望 %d 条违例·实得 %d 条 %s" % ("OK  " if ok else "FAIL", name, expect, len(viol), viol))
        bad += 0 if ok else 1
    print("自测 %d/%d 通过" % (len(cases) - bad, len(cases)))
    return 0 if bad == 0 else 2


def main() -> int:
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return self_test()

    strict = "--strict" in argv
    report_only = "--report" in argv
    baseline_path = BASELINE
    if "--baseline" in argv:
        i = argv.index("--baseline")
        if i + 1 < len(argv):
            baseline_path = Path(argv[i + 1])
            if not baseline_path.is_absolute():
                baseline_path = ROOT / baseline_path

    viol, per_page = scan_site()
    if "--generate-baseline" in argv:
        n = freeze_gate.write_baseline(
            baseline_path,
            viol,
            [
                "# 第 79 门禁 · 回退块保真度基线（W1265 建立·存量违例冻结）",
                "# 生成命令：py -3 scripts/check_fallback_fidelity.py --generate-baseline",
                "# 格式：<页面>|<F1|F1b|F2>|<细节>；F1=变量名含 MOCK·F1b=含强 mock 声明·F2=条目数≠真值",
                "# 语义：基线内违例记「存量基线」不计 FAIL；基线外新增 = FAIL；零容忍：--strict",
            ],
        )
        print("基线已写入 %s（%d 条）" % (baseline_path, n))
        return 0

    baseline, problems = freeze_gate.read_baseline(baseline_path)
    if problems:
        if report_only:
            for p in problems:
                print("NOTE " + p + "（报告档不判红）")
            baseline = set()
        else:
            for p in problems:
                print("FAIL " + p)
            print("%s 基线缺失/不可读·fail-closed·拒绝通过 ----" % MARKER)
            return 1

    res = freeze_gate.evaluate(viol, baseline, strict=strict)
    by_code = {"F1": 0, "F1b": 0, "F2": 0}
    for v in viol:
        code = v.split("|")[1]
        by_code[code] = by_code.get(code, 0) + 1
    print("扫描 site/data + site/en · F1 变量名含 MOCK %d 条 · F1b 强 mock 声明 %d 条 · F2 条目数≠真值 %d 条 · 违例页 %d 页"
          % (by_code.get("F1", 0), by_code.get("F1b", 0), by_code.get("F2", 0), len(per_page)))
    for p in sorted(per_page):
        print("  · %s：%s" % (p, " / ".join(v.split("|")[1] + " " + v.split("|")[2][:70] for v in per_page[p])))
    freeze_gate.print_eval(res, MARKER, strict=strict)
    print("%s ----" % MARKER)
    if report_only:
        return 0
    return 1 if res["new_fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
