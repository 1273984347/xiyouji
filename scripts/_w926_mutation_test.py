import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
TMP = Path(os.environ["TEMP"])
BASE = TMP / "w926_mut_base"
MUT = TMP / "w926_mut"
REPORT_REL = "docs/11-方案报告/审查与评审/站点交互流程审查复核报告-2026-10-25.md"
PAGES = ("cross-time-danmaku.html", "graph-explorer.html",
         "journey-map-interactive.html", "narrative-rhythm-curve.html")


def build_base():
    if BASE.exists():
        shutil.rmtree(BASE)
    (BASE / "scripts" / "output").mkdir(parents=True)
    (BASE / REPORT_REL).parent.mkdir(parents=True)
    shutil.copy(SRC / "scripts" / "_w926_verify_numbers.py", BASE / "scripts" / "_w926_verify_numbers.py")
    for j in ("_w926_ia_audit.json", "_w926_ia_evidence.json", "_w926_visible_leak.json"):
        shutil.copy(SRC / "scripts" / "output" / j, BASE / "scripts" / "output" / j)
    shutil.copy(SRC / REPORT_REL, BASE / REPORT_REL)
    (BASE / "site" / "data" / "json").mkdir(parents=True)
    (BASE / "site" / "en").mkdir(parents=True)
    for f in ("rum-viewer.html", "visit-viewer.html", "sitemap.xml"):
        shutil.copy(SRC / "site" / f, BASE / "site" / f)
    for d in ("data", "en"):
        for p in PAGES:
            shutil.copy(SRC / "site" / d / p, BASE / "site" / d / p)
    for j in (SRC / "site" / "data" / "json").glob("*.json"):
        shutil.copy(j, BASE / "site" / "data" / "json" / j.name)


def rep_text(root):
    return (root / REPORT_REL).read_text(encoding="utf-8")


def rep_write(root, s):
    (root / REPORT_REL).write_text(s, encoding="utf-8")


def audit_load(root):
    return json.loads((root / "scripts" / "output" / "_w926_ia_audit.json").read_text(encoding="utf-8"))


def audit_write(root, d):
    (root / "scripts" / "output" / "_w926_ia_audit.json").write_text(
        json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


# ---- 突变定义：(名称, 期望 FAIL 的断言编号, 变换函数) ----
def m_json(fn):
    def go(root):
        d = audit_load(root)
        fn(d)
        audit_write(root, d)
    return go


def m_pages_total_85(root):
    m_json(lambda d: d["meta"].__setitem__("pages_total", 85))(root)


def m_false_dead_7(root):
    m_json(lambda d: d["A_paths"].__setitem__("html_only_false_dead_count", 7))(root)


def m_zero_inbound_drop(root):
    m_json(lambda d: d["A_paths"].__setitem__("inbound_zero_pages", d["A_paths"]["inbound_zero_pages"][:8]))(root)


def m_report_sub(old, new):
    def go(root):
        s = rep_text(root)
        if old not in s:
            raise SystemExit("MUT 目标串不存在：%r" % old[:60])
        mutated = s.replace(old, new, 1)
        if old in mutated:
            raise SystemExit("MUT 未生效：替换后原串仍在（可能命中多处）")
        if mutated == s:
            raise SystemExit("MUT 未生效：内容无变化")
        rep_write(root, mutated)
    return go


def m_section_sub(start, end, old, new):
    """只在 [start, end) 段内替换 —— 防止同名串在别处先命中导致变异没打到目标点。"""
    def go(root):
        s = rep_text(root)
        if start not in s or end not in s:
            raise SystemExit("MUT 段落边界不存在")
        head, tail = s.split(start, 1)
        body, rest = tail.split(end, 1)
        if old not in body:
            raise SystemExit("MUT 段内目标串不存在：%r" % old[:60])
        mutated_body = body.replace(old, new, 1)
        if old in mutated_body or mutated_body == body:
            raise SystemExit("MUT 段内替换未生效")
        rep_write(root, head + start + mutated_body + end + rest)
    return go


CASES = [
    ("M1 证据 pages_total 857→85（子串型假通过点）", "N-01", m_pages_total_85),
    ("M2 证据 false_dead_count 17→7（子串型假通过点）", "N-09", m_false_dead_7),
    ("M3 报告 §2.2 标题去掉 R-05 标识", "S-05",
     m_report_sub("### 2.2 R-02（P0）/ R-05（P1）", "### 2.2 R-02（P0）")),
    ("M4 报告 §2.9 篡改 1 个 json 文件名", "S-09",
     m_report_sub("json/board_game.json", "json/board_game_TYPO.json")),
    ("M5 报告 §2.9 篡改 R-09 工具页路径", "S-10",
     m_report_sub("`site/rum-viewer.html`", "`site/rum-viewerX.html`")),
    ("M6 给 user-message 控件加 aria-label（真缺陷应消失）", "S-13", None),
    ("M7 报告 §0.3 B3 行去掉 R-10", "S-07",
     m_report_sub("R-03 R-04 R-07 R-08 R-09 R-10 R-11 R-12", "R-03 R-04 R-07 R-08 R-09 R-11 R-12")),
    ("M8 报告 §1.3 节头「四条」→「五条」", "S-06",
     m_report_sub("### 1.3 判据自纠四条", "### 1.3 判据自纠五条")),
    ("M9 证据零入链清单 9→8 页", "S-12", m_zero_inbound_drop),
    ("M10 报告 §0.4 的 P1 行去掉 R-05（低成本项被埋回大批）", "S-15",
     m_section_sub("### 0.4 执行序重排", "## 1. 审查范围", "| R-05 |", "| — |")),
    ("M11 报告 §0.4 的 P0 行去掉 R-01（阻断项被降级）", "S-15",
     m_section_sub("### 0.4 执行序重排", "## 1. 审查范围", "| R-01 R-06 |", "| R-06 |")),
]


def m_add_aria(root):
    f = root / "site" / "data" / "cross-time-danmaku.html"
    s = f.read_text(encoding="utf-8")
    if 'id="user-message"' not in s:
        raise SystemExit("M6 目标控件不存在")
    s = s.replace('id="user-message"', 'id="user-message" aria-label="留言"', 1)
    f.write_text(s, encoding="utf-8")


CASES[5] = (CASES[5][0], CASES[5][1], m_add_aria)

build_base()
print("baseline 构建完成：%s\n" % BASE)

# baseline 必须全绿
out = subprocess.run([sys.executable, str(BASE / "scripts" / "_w926_verify_numbers.py")],
                     capture_output=True, text=True, encoding="utf-8")
if out.returncode != 0:
    print("FAIL baseline 非绿，突变测试无意义：\n", out.stdout[-1500:], out.stderr[-800:])
    raise SystemExit(1)
print("baseline 绿 ✅\n")

bad = []
for name, expect, fn in CASES:
    if MUT.exists():
        shutil.rmtree(MUT)
    shutil.copytree(BASE, MUT)
    fn(MUT)
    r = subprocess.run([sys.executable, str(MUT / "scripts" / "_w926_verify_numbers.py")],
                       capture_output=True, text=True, encoding="utf-8")
    hit = ("FAIL " + expect) in r.stdout
    if r.returncode != 0 and hit:
        print("OK   %-52s → %s 红 ✅" % (name, expect))
    else:
        bad.append((name, expect, r.returncode, r.stdout[-400:]))
        print("FAIL %-52s → 期望 %s 红，实得 exit=%s" % (name, expect, r.returncode))

if MUT.exists():
    shutil.rmtree(MUT)
print()
if bad:
    print("突变测试：%d/%d 未按预期失败" % (len(bad), len(CASES)))
    for b in bad:
        print("   ", b[0], "->", b[3][:300])
    raise SystemExit(1)
print("突变测试：%d/%d 组全部按预期失败（断言可证伪 ✅）" % (len(CASES), len(CASES)))
