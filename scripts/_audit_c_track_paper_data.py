#!/usr/bin/env python3
"""一次性：C 轨可验证性基础设施稿《数据核验与复现》审计（2026-09-28）。

只读审计（不改动任何源文件）：逐项核验
docs/S4-学术投稿/01-论文/可验证性方向-投稿版.md（投稿版 + 匿名稿）
的全部量化断言，对照：
- 引文门禁 scripts/check_citations.py（--dir docs 全量实跑 ×3 + 计时；--self-test）
- 锚点定位 scripts/audit/line_check.py（四条引文锚点 + --self-test）
- 语料 dataset/text-search.json（100 回 / 708,441 字）与内容文档计数（A1-A6=615）
- 门禁基线（frontmatter 611 / glossary 383 / content-consistency 9）
- 门禁编号与案例记录（CHANGELOG / AGENTS / 脚本头注）
- 图表文件（图表/ C-图1~C-图4）
- 幻觉条目生存期（git 提交史取证：索引初始提交 / A 稿 W386 快照 / W605 清除）
结果落盘 tmpe/audit_c_track_paper_data.json；控制台输出逐项判定与差异项。
"""
import json
import re
import statistics  # noqa: F401  (保留：后续复算扩展用)
import struct
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
S4 = ROOT / "docs" / "S4-学术投稿"
MD = S4 / "01-论文" / "可验证性方向-投稿版.md"
MD_ANON = S4 / "01-论文" / "可验证性方向-匿名稿.md"
FIGDIR = S4 / "07-图表"
OUT = ROOT / "tmpe" / "audit_c_track_paper_data.json"
CHANGELOG = ROOT / "CHANGELOG.md"
AGENTS = ROOT / "AGENTS.md"

INDEX = "source/引用与网络解读/学术论文索引.md"
A_TRACK = "docs/S4-学术投稿/01-论文/明清小说方向-投稿版.md"


def run(cmd, cwd=ROOT):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", cwd=str(cwd))
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def count_md(area):
    p = ROOT / "docs" / area
    return sum(1 for fn in p.iterdir() if fn.suffix == ".md" and fn.name.lower() != "readme.md")


def main():
    res = {"generated": "2026-09-28"}

    # ---- 1. 引文门禁全量 ×3 + 计时 ----
    runs = []
    for _ in range(3):
        t0 = time.perf_counter()
        code, out = run([sys.executable, str(ROOT / "scripts" / "check_citations.py"), "--dir", "docs"])
        dt = time.perf_counter() - t0
        m = re.search(r"共 (\d+) 条引文行 · 命中率 (\d+)%（(\d+) 个文件扫描）", out)
        runs.append({
            "seconds": round(dt, 2), "exit": code,
            "lines": int(m.group(1)) if m else None,
            "rate": int(m.group(2)) if m else None,
            "files": int(m.group(3)) if m else None,
        })
    code, st = run([sys.executable, str(ROOT / "scripts" / "check_citations.py"), "--self-test"])
    res["citation_gate"] = {"runs": runs, "self_test": st.strip(), "self_test_exit": code}

    # ---- 2. 锚点定位四条 + self-test ----
    anchors = [(98, "白本者，乃无字真经，倒也是好的。", 43), (2, "此山叫做灵台方寸山，山中有座斜月三星洞。", 9),
               (13, "心生，种种魔生；心灭，种种魔灭。", 1), (7, "皇帝轮流做", 45)]
    anchor_res = []
    for ch, frag, expect in anchors:
        _, out = run([sys.executable, str(ROOT / "scripts" / "audit" / "line_check.py"), str(ch), frag])
        got = out.strip()
        anchor_res.append({"chapter": ch, "expect": expect, "got": got, "ok": got == str(expect)})
    _, lc_st = run([sys.executable, str(ROOT / "scripts" / "audit" / "line_check.py"), "--self-test"])
    res["anchors"] = {"items": anchor_res, "self_test": lc_st.strip(),
                      "all_ok": all(a["ok"] for a in anchor_res)}

    # ---- 3. 计数：615 / 105 / 语料 100 回 708441 字 ----
    areas = ["01-全书逐回解读", "06-个人随笔", "02-人物深度分析", "03-主题与情节专题", "04-文化与历史背景", "05-诗词歌赋"]
    per_area = {a: count_md(a) for a in areas}
    acad, acad_missing = 0, 0
    import os
    for r, _, fns in os.walk(ROOT / "docs"):
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            c = (Path(r) / fn).read_text(encoding="utf-8", errors="replace")
            m = re.search(r"^> 轨标：([^\r\n]+)", c, re.M)
            if m and m.group(1).strip() == "学术研究":
                acad += 1
                if not re.search(r"^> 引用：.*学术论文索引", c, re.M):
                    acad_missing += 1
    d = json.loads((ROOT / "dataset" / "text-search.json").read_text(encoding="utf-8"))
    corpus = {"chapters": len(d["chapters"]),
              "chars_raw": sum(len(c["text"]) for c in d["chapters"])}
    res["counts"] = {"content_docs": {"per_area": per_area, "total": sum(per_area.values())},
                     "academic_track": {"total": acad, "missing_explicit_cite": acad_missing},
                     "corpus": corpus}

    # ---- 4. 门禁基线 ----
    def baseline_count(p):
        lines = [x for x in (ROOT / p).read_text(encoding="utf-8").splitlines()
                 if x.strip() and not x.strip().startswith("#")]
        return len(lines)

    res["baselines"] = {
        "frontmatter_611": baseline_count("scripts/output/frontmatter-baseline.txt"),
        "glossary_383": baseline_count("scripts/output/glossary-baseline.txt"),
        "content_consistency_9": baseline_count("scripts/content-consistency-baseline.txt"),
    }

    # ---- 5. 门禁编号与案例记录（字符串取证） ----
    cl = CHANGELOG.read_text(encoding="utf-8")
    ag = AGENTS.read_text(encoding="utf-8")
    fd = (ROOT / "scripts" / "check_frontmatter.py").read_text(encoding="utf-8")
    gl = (ROOT / "scripts" / "check_glossary.py").read_text(encoding="utf-8")
    ci = (ROOT / "scripts" / "check_citations.py").read_text(encoding="utf-8")
    ic = (ROOT / "scripts" / "check_inlined_css.py").read_text(encoding="utf-8")
    cc = (ROOT / "scripts" / "check_content_consistency.py").read_text(encoding="utf-8")
    vd = (ROOT / "scripts" / "verify_delivery.py").read_text(encoding="utf-8")
    sr = (ROOT / "docs" / "archive" / "w550-shot-review" / "shot-review-report.md").read_text(encoding="utf-8")
    spec = (ROOT / "docs" / "00-导读" / "文档规范.md").read_text(encoding="utf-8")

    def missing_subs(s, *subs):
        return [x for x in subs if x not in s]

    gates = {
        "gate16_retired": missing_subs(cl, "第16门禁/sync_skills同步退役", "门禁计数 25→24"),
        "gate18_20_refs": missing_subs(fd + gl + ci + spec + ag, "第 18 门禁", "第 19 门禁", "第 20 门禁"),
        "gate15_20kb": missing_subs(ic + cl, "20000"),
        "gate25_ref": missing_subs(ag + cc, "第 25 门禁"),
        "case1_7cleared": missing_subs(cl, "全仓清除 7 处", "循环核验", "外部权威源"),
        "case2_224pages": missing_subs(cl, "224 个 data+EN 页", "14 门禁无一拦截"),
        "case2_gate15_turned": missing_subs(cl, "第 15 门禁"),
        "case_extra_w457_7p": missing_subs(vd, "W457", "7 页漏网"),
        "case_extra_w550_10p": missing_subs(cl, "10 页补 d3-sankey.min.js 引用"),
        "case_extra_w550_4groups": missing_subs(sr, "4 组全部 yes"),
        "case_extra_consistency3": missing_subs(cc, "W550 实证三类同页数字矛盾"),
        "silent_skip_hardening": missing_subs(ci, "防静默跳过", "疑似引文行未采用规范语法"),
    }
    res["gates_and_cases"] = {k: {"ok": v == [], "missing": v} for k, v in gates.items()}

    # ---- 6. 两稿：引文条数 / 字数 / 脚注 / diff ----
    def cite_lines(p):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_citations.py"), "--file", str(p)],
                           capture_output=True, text=True, encoding="utf-8")
        m = re.search(r"共 (\d+) 条引文行", r.stdout)
        return int(m.group(1)) if m else None

    def words(p):
        t = p.read_text(encoding="utf-8")
        i, j = t.find("## 一、"), t.find("## 注释")
        body = re.sub(r"\s+", "", t[i:j]) if i >= 0 and j >= 0 else ""
        return {"total_nows": len(re.sub(r"\s+", "", t)), "body_nows": len(body)}

    main_t = MD.read_text(encoding="utf-8")
    anon_t = MD_ANON.read_text(encoding="utf-8")
    footnotes = len(re.findall(r"^\[\^(\d+)\]:", main_t, re.M))
    import difflib
    dl = list(difflib.unified_diff(main_t.splitlines(), anon_t.splitlines(), lineterm=""))
    diff = sum(1 for x in dl if x[:1] in "+-" and not x.startswith(("+++", "---")))
    diff_hunks = sum(1 for x in dl if x.startswith("@@"))
    res["manuscripts"] = {
        "main": {"citations": cite_lines(MD), "words": words(MD), "footnotes": footnotes},
        "anon": {"citations": cite_lines(MD_ANON), "words": words(MD_ANON)},
        "line_diff_count": diff, "diff_hunks": diff_hunks,
    }

    # ---- 7. 图表 ----
    def png_dims(p):
        with open(p, "rb") as f:
            h = f.read(33)
        w, hh = struct.unpack(">II", h[16:24])
        return {"w": w, "h": hh}

    figs = {}
    for name in ("C-图1-三层体系", "C-图2-锚点查询实测", "C-图3-校验输出实测", "C-图4-门禁运行实测"):
        svg = (FIGDIR / (name + ".svg")).read_text(encoding="utf-8")
        figs[name] = {
            "svg": True, "png": png_dims(FIGDIR / (name + ".png")),
            "svg_has": [k for k in ("437", "842", "100%", "line 9", "line 45", "第 2 回", "阻断", "FAIL", "门禁") if k in svg],
        }
    res["figures"] = figs

    # ---- 8. 幻觉条目生存期（git 取证） ----
    g = {}
    code, out = run(["git", "log", "--format=%h %ad", "--date=short", "-S", "竺洪波, 张培恒", "--", INDEX])
    g["index_string_changes"] = out.strip().splitlines()
    code, out = run(["git", "show", "156643f:" + INDEX])
    g["in_initial_commit"] = "竺洪波, 张培恒" in out
    code, out = run(["git", "log", "--reverse", "--format=%h %ad", "--date=short", "-S", "张培恒", "--", A_TRACK])
    g["a_track_first_change"] = (out.strip().splitlines() or [""])[0]
    code, out = run(["git", "log", "--format=%h %ad %s", "--date=short", "-S", "全仓清除 7 处", "--", "CHANGELOG.md"])
    g["clear_commit"] = (out.strip().splitlines() or [""])[0][:80]
    res["hallucination_lifespan"] = g

    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- 控制台摘要 ----
    print("== 引文门禁 ==", [(r["seconds"], r["lines"], r["files"], r["rate"]) for r in runs])
    print("   self-test:", st.strip().splitlines()[-1])
    print("== 锚点 ==", [(a["chapter"], a["got"], a["ok"]) for a in anchor_res], "| all_ok =", res["anchors"]["all_ok"])
    print("== 计数 ==", res["counts"])
    print("== 基线 ==", res["baselines"])
    bad = {k: v for k, v in res["gates_and_cases"].items() if not v["ok"]}
    print("== 门禁/案例取证 ==  异常:", bad if bad else "无")
    print("== 两稿 ==", json.dumps(res["manuscripts"], ensure_ascii=False))
    print("== 图表 ==", json.dumps(res["figures"], ensure_ascii=False))
    print("== 幻觉生存期取证 ==", json.dumps(g, ensure_ascii=False, indent=1))
    print("written:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())