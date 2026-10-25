#!/usr/bin/env python
"""release_prep.py — 批次发布预检器（S-31 落地 · W736 建 · 复盘第 38 篇 §3）。

把「能落盘但会让门禁红」的问题全部前置拦下——镜像三处机器房的判据：
  · batch_cascade.precheck   字段级分隔符黑名单 + title 领衔 + 四件套文件行
  · check_doc_sync C4        消息/文本 W### 形态须已登记（台账/CHANGELOG/归档）
  · check_doc_sync C4-f      文件行路径须在库或 staged 且未被 gitignore

三种用法：
    python scripts/release_prep.py --check-spec scripts/output/_w###_spec.json
    python scripts/release_prep.py --check-message tmpe/msg.txt
    python scripts/release_prep.py --init W### --title "W### 示例批" --out scripts/output/_w###_spec.json

退出码：0=全过；1=有违例（逐条输出定位）；2=参数/读取错误。
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_FILES = [
    "CHANGELOG.md",
    os.path.join("archive", "docs", "CHANGELOG-ARCHIVE.md"),
    os.path.join("archive", "docs", "CHANGELOG-ARCHIVE-tier2.md"),
    os.path.join("docs", "00-导读", "W批次编号对账表.md"),
]
REQUIRED_FIELDS = ("batch", "date", "title", "desc", "head_entry", "head_sentence",
                   "changelog_body", "milestone_block", "agents_note", "file_index_rows")
RE_W_FORM = re.compile(r"(?<![A-Za-z0-9])[Ww]\d{3,4}(?!\d)")
RE_PATH_TOKEN = re.compile(
    r"[A-Za-z0-9_\-./\u4e00-\u9fff]+\.(?:py|js|mjs|md|json|html|cff|yml|yaml|txt|toml|css)$")
BANNED = {"desc": ("·", "；", "—"), "head_sentence": ("；", "—", "（", "）")}
RE_PYTEST_ARABIC = re.compile(r"pytest (\d+) passed")
RE_PYTEST_ZH = re.compile(r"pytest ([零一二三四五六七八九十百千万]+)")
ZH_DIGIT = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
ZH_UNIT = {"十": 10, "百": 100, "千": 1000, "万": 10000}


def zh_num_to_int(s):
    """中文数字 → int（覆盖 零~九 + 十百千万 组合·PRE-25 双形态）。

    支持：三百一十三=313 / 十五=15（段首「十」兜底）/ 二千零五十=2050（零占位不累加）/ 一万零二十四=10024。
    非法字符或空串抛 ValueError。
    """
    if not s:
        raise ValueError("空串")
    total = section = digit = 0
    for ch in s:
        if ch in ZH_DIGIT:
            digit = ZH_DIGIT[ch]
        elif ch in ZH_UNIT:
            if ch == "万":
                total = (total + section + digit) * ZH_UNIT[ch]
                section = digit = 0
            else:
                if digit == 0 and section == 0:
                    digit = 1  # 段首「十三/百/千」形态兜底（零后跟单位不触发·保 0 占位）
                section += digit * ZH_UNIT[ch]
                digit = 0
        else:
            raise ValueError(f"非法中文数字字符：{ch!r}")
    return total + section + digit


def check_pytest_count(spec, expect):
    """PRE-25 第四检：spec 验证行 pytest 计数 vs 实跑对账（阿拉伯+中文双形态·W742）。

    对账面：changelog_body 的「pytest N passed」与 agents_note 的「pytest 中文数字」
    须双写一致且等于实跑数 expect（P-01/P-11 实证：单写/沿抄/双写失步三类失真）。
    changelog_body 无 pytest 计数形态 → 返回 ([], skip=True)（纯文档批无此声明）。
    返回 (issues, skipped)。
    """
    body = str(spec.get("changelog_body", ""))
    note = str(spec.get("agents_note", ""))
    s1 = sorted({int(m.group(1)) for m in RE_PYTEST_ARABIC.finditer(body)})
    issues = []
    if not s1:
        return issues, True  # spec 未声明 pytest 计数（纯文档批）——跳过
    s2_raw = [m.group(1) for m in RE_PYTEST_ZH.finditer(note)]
    s2 = []
    for raw in s2_raw:
        try:
            s2.append(zh_num_to_int(raw))
        except ValueError as exc:
            issues.append(f"spec.agents_note 中文计数解析失败：{raw!r}（{exc}）")
    if len(s1) != 1:
        issues.append(f"spec.changelog_body 的 pytest 计数形态不唯一：{s1}（应恰好 1 个「pytest N passed」）")
    if s1 and s2 and set(s1) != set(s2):
        issues.append(f"spec 双写失步（P-11）：changelog_body={s1} vs agents_note={s2}")
    if s1 and not s2:
        issues.append(f"spec.agents_note 缺中文计数双写（changelog_body={s1}·两处须一致——P-11 实证）")
    if expect is not None and s1 and s1[0] != expect:
        issues.append(f"spec 计数与实跑不符（P-01）：spec={s1[0]} vs 实跑 pytest={expect}"
                      f"（W737 实证：沿抄旧计数致 fix×2 返工）")
    return issues, False


def run_git(*args, cwd=None):
    return subprocess.run(["git"] + list(args), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", cwd=cwd or ROOT)


def load_registry(root):
    """已登记 W 号集合：CHANGELOG 现役 + 两归档 + 对账表（C4 同源四件）。"""
    reg = set()
    for rel in REGISTRY_FILES:
        try:
            text = open(os.path.join(root, rel), encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        reg.update(int(x) for x in re.findall(r"[Ww](\d{3,4})", text))
    return reg


def find_unregistered(text, registry):
    """扫描 W### 形态并返回未登记项 [(原文, 数字, 上下文)]。"""
    out = []
    for m in re.finditer(RE_W_FORM, text):
        num = int(m.group(0)[1:])
        if num not in registry:
            ctx = text[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")
            out.append((m.group(0), num, ctx))
    return out


def check_fields(spec):
    """镜像 batch_cascade.precheck 的字段级判据（分隔符/领衔/四件套）。"""
    issues = []
    for field in REQUIRED_FIELDS:
        if field not in spec:
            issues.append(f"spec 缺必填字段：{field}")
    if issues:
        return issues
    for field, banned in BANNED.items():
        for sep in banned:
            if sep in str(spec.get(field, "")):
                issues.append(f"spec.{field} 含禁用分隔符 {sep!r}（会使下一批锚点正则失配）")
    if not str(spec.get("title", "")).startswith(str(spec.get("batch", ""))):
        issues.append("spec.title 未以 batch 号领衔（现役段解析取标题首个 W###）")
    if not re.fullmatch(r"W\d{3,4}", str(spec.get("batch", ""))):
        issues.append(f"spec.batch 形态非法：{spec.get('batch')!r}（应 W+三位数字）")
    for field in ("desc", "head_sentence"):
        if re.match(r"^W\d{3,4}", str(spec.get(field, ""))):
            issues.append(
                f"spec.{field} 以批次号开头（页脚 token 形态为「batch + desc」·W779 实证叠成"
                f"「W779 W779…」双 token 且 W724 防线只能下一批拦截——防线前移到 spec 时点·W781 R-2）")
    body = str(spec.get("changelog_body", ""))
    if "**文件**：" not in body:
        issues.append("spec.changelog_body 缺「**文件**：」行（C4-f 据其对账手工件入库）")
    rows = spec.get("file_index_rows")
    if not isinstance(rows, list) or not rows or not all(str(r).startswith("| ") for r in rows):
        issues.append("spec.file_index_rows 缺失或行形态非法（应非空且每行以 '| ' 开头）")
    return issues


def extract_file_line_paths(body):
    """从 changelog_body 的「文件」行抽取待核对路径 token（带已知后缀者）。"""
    m = re.search(r"\*\*文件\*\*：(.+)", body)
    if not m:
        return []
    paths = []
    for tok in re.split(r"[、，,;]", m.group(1)):
        tok = tok.strip().strip("`\"'（）()。 ")
        if "（" in tok:
            tok = tok.split("（")[0]
        if RE_PATH_TOKEN.fullmatch(tok):
            paths.append(tok)
    return paths


def check_paths(paths, root=ROOT):
    """镜像 C4-f：在库或 staged + 未 gitignore。"""
    issues = []
    for p in paths:
        r = run_git("ls-files", "--error-unmatch", "--", p, cwd=root)
        if r.returncode != 0:
            issues.append(f"文件行路径 {p} 未在库/staged（先 git add·C4-f 会拦）")
            continue
        r2 = run_git("check-ignore", "-q", "--", p, cwd=root)
        if r2.returncode == 0:
            issues.append(f"文件行路径 {p} 命中 .gitignore（禁列·W734 实证）")
    return issues


def report(section, issues):
    print(f"-- {section}：{'OK' if not issues else f'{len(issues)} 项违例'}")
    for it in issues:
        print("   FAIL  " + it)
    return len(issues)


def check_message(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    registry = load_registry(ROOT)
    unreg = find_unregistered(text, registry)
    print(f"== 消息 W### 形态登记核验（{path}）==")
    n = report("未登记形态", [f"{w}（上下文：…{ctx}…）" for w, _num, ctx in unreg])
    print("PASS  全部 W### 形态均已登记" if not n else f"FAIL  {n} 处未登记（C4 会拦）")
    return n


def check_spec(path, pytest_count=None):
    total = 0
    try:
        raw = open(path, encoding="utf-8", errors="replace").read()
        spec = json.loads(raw)
    except (OSError, ValueError) as exc:
        print(f"FAIL  spec 读取/解析失败：{exc}")
        return 1
    print(f"== spec 预检（{path}）==")
    total += report("①字段/分隔符/领衔", check_fields(spec))
    cnt_issues, cnt_skip = check_pytest_count(spec, pytest_count)
    if cnt_skip:
        print("-- ②验证行计数对账（PRE-25）：SKIP（spec 未声明 pytest 计数·纯文档批）")
    else:
        total += report("②验证行计数对账（PRE-25·双形态）", cnt_issues)
        if not cnt_issues:
            got = sorted({int(m.group(1)) for m in RE_PYTEST_ARABIC.finditer(str(spec.get("changelog_body", "")))})
            print(f"   PASS  阿拉伯+中文双写一致{f' 且等于实跑 {pytest_count}' if pytest_count is not None else '（未传 --pytest-count·建议传入实跑数）'}：{got[0]}")
    if spec.get("changelog_body") is not None:
        total += report("③文件行路径（C4-f 镜像）",
                        check_paths(extract_file_line_paths(str(spec.get("changelog_body", "")))))
    registry = load_registry(ROOT)
    unreg = find_unregistered(raw, registry)
    total += report("④W### 形态登记（C4 镜像）",
                    [f"{w}（上下文：…{ctx}…）" for w, _num, ctx in unreg])
    print("PASS  spec 预检全过——可进入 dry-run" if not total else
          f"FAIL  {total} 项违例——修正后重跑")
    return 1 if total else 0


def init_spec(batch, title, out_path):
    today = datetime.date.today().isoformat()
    spec = {
        "batch": batch,
        "date": today,
        "title": title,
        "desc": "",
        "head_entry": f"{today}（{title}）",
        "head_sentence": "",
        "changelog_body": ("\n\n> **来源**：\n> - **T1**：\n"
                           "> - **验证（全绿）**：\n"
                           "> - **状态**：已落地（级联+提交后以 gh run list 为准）。\n"
                           "> - **文件**：\n"),
        "milestone_block": f"- **{title}**：\n",
        "agents_note": "",
        "file_index_rows": [],
    }
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        json.dump(spec, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK    spec 模板已生成：{out_path}")
    print("      填写后自检：python scripts/release_prep.py --check-spec " + out_path)
    return 0


def main():
    ap = argparse.ArgumentParser(description="批次发布预检（S-31）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check-spec", metavar="FILE", help="spec JSON 全量四检（含 PRE-25 计数对账·配 --pytest-count）")
    g.add_argument("--check-message", metavar="FILE", help="消息/文本 W### 形态登记核验")
    g.add_argument("--init", metavar="BATCH", help="生成 spec 模板（配合 --title/--out）")
    ap.add_argument("--title", help="--init 用批次标题")
    ap.add_argument("--out", help="--init 输出路径")
    ap.add_argument("--pytest-count", type=int, default=None,
                    help="--check-spec 用：实跑 pytest 通过数（PRE-25 第四检对账基准·建议必传）")
    args = ap.parse_args()
    if args.check_spec:
        return check_spec(args.check_spec, args.pytest_count)
    if args.check_message:
        return check_message(args.check_message)
    if not args.title or not args.out:
        print("FAIL  --init 需同时给 --title 与 --out")
        return 2
    return init_spec(args.init, args.title, args.out)


if __name__ == "__main__":
    sys.exit(main())
