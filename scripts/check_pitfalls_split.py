#!/usr/bin/env python3
"""check_pitfalls_split.py —— 坑表六主题拆分结构判据（W1290 拆分的结构守卫）。

病根：W1290 把坑表正本「单文件 419 条」拆成三层——
      ① 根索引壳 `pitfalls.md`（阅读契约 + 六主题正本表 + E-NN→主题反查表，**壳内零条目**）
      ② 六主题判据层正本 `docs/agent/pitfalls-topics/*.md`（每主题一份，含契约段 + 段头条数）
      ③ 叙事层归档 `archive/docs/pitfalls-detail-ARCHIVE.md`（`#### E-NN` 段 · 逐字全文）
    拆完后「一致性」从「一份大表内部自洽」变成「跨 8 个文件自洽」⇒ **任一面失配都不会
    自然报错**（每个文件单独看都合法、每处数字单看都对）⇒ 「零信息丢失 / 零重号 /
    零计数漂移」三句承诺若只靠人核，拆一次就漂一次（仓内先例：计数链五处手改长期无人核）。

本脚本判 7 项（逐项输出 PASS/FAIL 与实测数字；退出码 0=全过 / 1=有 FAIL）：
  C1 六主题文件存在且每份含契约段（正文含「何时读」）
  C2 每个主题文件：段头声明条数（剥 `<!--stats:...-->` 后匹配 `### <名>（N 条）`）
                   == 该文件内 `- **` 行实算数
  C3 索引壳：「六主题正本」表内声明条数 == 跨六文件聚合的实算条数；且壳内 `- **` 行数 == 0
  C4 索引壳的 E-NN→主题反查表：覆盖全部本体 E 号，**无遗漏、无多余**
  C5 双层镜像：判据层每条指针型条目在叙事层归档有对应段且内容同源（零信息丢失）
  C6 本体 E 号唯一：跨六文件聚合后无重复号
  C7 写窗：每个主题文件字节 <= MAX_DOC_BYTES（与全局同窗）；并输出各文件字节与合计

口径复用（**引用不复制**）：
  · 本体 E 号形态 → `scripts/check_pitfall_id_unique.py` 的 `RX_ENTRY`
    （「（W#### 实证·E-NN」且后跟 `·` 或 `）`；E 号位数不固定，如 `E-9`）
  · 主题名 → stats 键 → `scripts/check_doc_sync.py` 的 `PITFALL_THEME_KEYS`
  · 字节窗 → `scripts/utils/gate_common.py` 的 `MAX_DOC_BYTES`（W1315 下沉共享层·禁复制常量）

用法：python scripts/check_pitfalls_split.py [--root 目录]
本脚本**只读**：不修改任何文件、不做 git 写操作。
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(ROOT, "scripts") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT, "scripts"))

# ---- 口径引用（单一事实源·引用不复制）-------------------------------------
from check_pitfall_id_unique import RX_ENTRY  # noqa: E402  本体 E 号形态

# W1300（L-07 治本）：多批次锚**已在公共本体口径 RX_ENTRY 内支持**（见
#   check_pitfall_id_unique.RX_ENTRY·W1300 扩为允许并列批次号·取首个）⇒
#   镜像侧**不再需要**私有扩展正则（RX_ENTRY_MULTI 退役）⇒ 本体口径与镜像口径
#   **收敛为单一事实源**（引用不复制·避免两份正则各自漂移）。

try:
    from check_doc_sync import PITFALL_THEME_KEYS  # noqa: E402  主题名 → stats 键
except Exception as _e:  # pragma: no cover - fail-closed
    sys.stderr.write("FAIL  无法导入 check_doc_sync.PITFALL_THEME_KEYS（fail-closed）：%r\n" % (_e,))
    sys.exit(1)

from utils.gate_common import MAX_DOC_BYTES  # noqa: E402  全局字节窗（W1315 下沉；导入失败即抛错·禁兜底字面量）

# ---- 模块级常量表 --------------------------------------------------------
SHELL_REL = "pitfalls.md"
ARCHIVE_REL = os.path.join("archive", "docs", "pitfalls-detail-ARCHIVE.md")
TOPICS_DIR_REL = os.path.join("docs", "agent", "pitfalls-topics")

# 主题名 → 正本文件名（文件名同时由索引壳「六主题正本」表的路径列反查对拍·见 C3）
THEME_FILES = {
    "CSS / 视觉渲染": "css-visual.md",
    "JS / CSP / 运行时": "js-csp-runtime.md",
    "git / 提交 / 并发": "git-concurrency.md",
    "级联 / CHANGELOG": "cascade-changelog.md",
    "数据 / 内容可信度": "data-trust.md",
    "流程 / 协作 / 取证": "flow-collab.md",
}

RE_STAT_MARK = re.compile(r"<!--stats:[a-z_0-9]+-->")
RE_ENTRY_LINE = re.compile(r"^- \*\*")
RE_POINTER = re.compile(r"见归档")                       # 指针型条目（判据层 → 叙事层）
RE_ARCHIVE_SEG = re.compile(r"^#### (E-\d+)")             # 归档层段头
RE_SHELL_ROW = re.compile(
    r"^\|\s*(?P<name>[^|]+?)\s*\|\s*`(?P<path>[^`]+)`\s*\|\s*(?P<n>\d+)\s*\|")
RE_E_ID = re.compile(r"E-(\d+)")
RX_THEME_HEAD = re.compile(r"^### (?P<name>.+?)（(?P<n>\d+) 条）")

# 截断指针语（判据层把叙事全文换成指针）—— 镜像比对只取指针之前的正文
TRUNC_MARKERS = (
    "⇒ 要点与纪律详见归档",
    "⇒ 纪律要点详见归档",
    "；【全文详见归档",
    "⇒ 要点详见归档",
    "【全文详见归档",
    "详见归档",
    "见归档",
)

# 镜像比对用的「宽松归一」：抹掉层间合法的形态差异（E 号插入位、跨项目通用标、
# 空白与标点），只留语义主干 —— 判据层与叙事层的文字差异必须先过这一关才谈「逐字」。
_PUNCT_RE = re.compile(r"[，,、。；;：:「」『』\"'（）()【】\[\]—\-·…!！?？]")

# W1290（主会话裁决）：**不设豁免表**——新增白名单须用户批准（铁律 16⑦），
# 而本仓的镜像「偏差」并非缺陷：正本＝判据层·**截断+指针版**（叙事全文在归档段），
# 故「正本与归档全文逐字不同」是**设计形态**⇒ 降为观测统计（prefix_miss / verbatim_hits）。
# 镜像**硬判据只认真缺陷**：① 指针条目的归档段存在；② 归档段内有条目正文行。
MIRROR_EXEMPT = {}  # 保留结构（工具与单测引用）·**零生效豁免**

def note_only(_check, msg):
    """形态差异登记（**不判红**）：正本判据层为「截断+指针版」，与归档叙事全文非逐字同源
    是**设计形态**而非缺陷 ⇒ 只记录不阻断（硬判据见「段存在 + 段内有正文行」）。"""
    return None


CHECK_NAMES = {
    "C1": "六主题文件存在且含契约段",
    "C2": "主题文件段头声明条数 == 实算条数",
    "C3": "索引壳表内声明 == 跨文件聚合实算·壳内零条目",
    "C4": "反查表覆盖全部本体 E 号（无遗漏无多余）",
    "C5": "双层镜像（判据层 → 叙事层）零信息丢失",
    "C6": "本体 E 号唯一",
    "C7": "主题文件写窗（字节 <= MAX_DOC_BYTES）",
}


# ---- 基础工具（纯函数）---------------------------------------------------
def strip_stat_marks(text):
    """剥 `<!--stats:...-->` 实体标记（段头声明数比对前必做）。"""
    return RE_STAT_MARK.sub("", text)


def norm_eid(eid):
    """E 号归一（去前导零：`E-08` ≡ `E-8`），避免跨文件形态差异造伪偏差。"""
    m = RE_E_ID.search(eid or "")
    return "E-%d" % int(m.group(1)) if m else (eid or "")


def _normalize_exempt():
    """豁免表键归一（表内写 `E-04`·判据层取数得 `E-4` ⇒ 前导零差异不得造成漏豁免）。"""
    return {norm_eid(k): v for k, v in MIRROR_EXEMPT.items()}


def entry_lines(text):
    """取条目行（`- **` 开头）——判据层正本的条目本体。"""
    return [ln for ln in (text or "").splitlines() if RE_ENTRY_LINE.match(ln)]


def entry_title(line):
    """取条目标题（`- **` 与下一个 `**` 之间）。"""
    idx = line.find("**", 4)
    return line[4:idx] if idx > 4 else ""


def mirror_key(line):
    """取镜像比对键：截断指针之前的正文（尾标点归一）。"""
    idx = len(line)
    for marker in TRUNC_MARKERS:
        p = line.find(marker)
        if p != -1:
            idx = min(idx, p)
    return line[:idx].rstrip().rstrip("。").rstrip()


def norm_mirror(text):
    """镜像比对的宽松归一（抹层间合法形态差异·保留语义主干）。"""
    s = re.sub(r"·E-\d+", "", text or "")
    s = s.replace("·跨项目通用", "")
    s = re.sub(r"[\s\u3000]", "", s)
    s = _PUNCT_RE.sub("", s)
    return s


def parse_archive_segments(text):
    """解析归档层 `#### E-NN` 段 -> {归一 E 号: [段内行]}。"""
    segs = {}
    cur = None
    for line in (text or "").splitlines():
        m = RE_ARCHIVE_SEG.match(line)
        if m:
            cur = norm_eid(m.group(1))
            segs.setdefault(cur, [])
            continue
        if cur is not None:
            segs[cur].append(line)
    return segs


def shell_theme_table(shell_text):
    """解析索引壳「六主题正本」表 -> {主题名: {"path":…, "n": 声明条数}}。"""
    table = {}
    for line in strip_stat_marks(shell_text or "").splitlines():
        m = RE_SHELL_ROW.match(line.strip())
        if not m:
            continue
        name = m.group("name").strip()
        if name in PITFALL_THEME_KEYS:
            table[name] = {"path": m.group("path").strip(), "n": int(m.group("n"))}
    return table


def shell_reverse_table(shell_text):
    """解析索引壳「E-NN → 主题 反查表」段的 E 号 -> [归一 E 号]（保序·可计重）。"""
    lines = (shell_text or "").splitlines()
    start = None
    for i, ln in enumerate(lines):
        if "反查表" in ln:
            start = i
            break
    if start is None:
        return []
    ids = []
    for ln in lines[start:]:
        if ln.startswith("## ") and "反查表" not in ln:
            break
        for m in RE_E_ID.finditer(ln):
            ids.append(norm_eid(m.group(0)))
    return ids


# ---- 判据主体（可注入纯函数）---------------------------------------------
def _check_c1(topics, theme_names, bad, facts):
    """C1 六主题文件存在且含契约段。"""
    c1 = {}
    for name in theme_names:
        item = topics.get(name)
        text = (item or {}).get("text")
        if text is None:
            bad("C1", "主题文件缺失：%s（%s）" % (name, (item or {}).get("path", "?")))
            c1[name] = "缺失"
            continue
        if "何时读" not in text:
            bad("C1", "主题文件缺契约段（正文无「何时读」）：%s" % name)
            c1[name] = "缺契约段"
            continue
        c1[name] = "OK"
    facts["C1"] = {"per_theme": c1,
                   "present": sum(1 for v in c1.values() if v == "OK"),
                   "total": len(theme_names)}


def _check_c2(topics, theme_names, bad, facts):
    """C2 段头声明数 == 实算数；返回各主题实算条数（C3 聚合用）。"""
    c2 = {}
    declared_total = {}
    actual_total = {}
    for name in theme_names:
        item = topics.get(name) or {}
        text = item.get("text")
        if text is None:
            continue
        stripped = strip_stat_marks(text)
        declared = None
        for line in stripped.splitlines():
            m = RX_THEME_HEAD.match(line)
            if m and m.group("name").strip() == name:
                declared = int(m.group("n"))
                break
        actual = len(entry_lines(stripped))
        if declared is None:
            bad("C2", "主题文件缺段头条数声明（`### %s（N 条）`）：%s" % (name, name))
            c2[name] = {"declared": None, "actual": actual}
            continue
        if declared != actual:
            bad("C2", "主题「%s」段头声明 %d 条 ≠ 实算 %d 条"
                % (name, declared, actual))
        c2[name] = {"declared": declared, "actual": actual}
        declared_total[name] = declared
        actual_total[name] = actual
    facts["C2"] = {"per_theme": c2,
                   "declared_sum": sum(declared_total.values()),
                   "actual_sum": sum(actual_total.values())}
    return actual_total


def _check_c3(shell, theme_names, actual_total, bad, facts):
    """C3 索引壳表内声明 == 聚合实算·壳内零条目。"""
    table = shell_theme_table(shell)
    c3 = {}
    agg_actual = sum(actual_total.values())
    agg_declared_shell = 0
    for name in theme_names:
        row = table.get(name)
        if row is None:
            bad("C3", "索引壳「六主题正本」表缺主题行：%s" % name)
            c3[name] = None
            continue
        agg_declared_shell += row["n"]
        act = actual_total.get(name)
        if act is None:
            continue
        if row["n"] != act:
            bad("C3", "索引壳主题「%s」声明 %d 条 ≠ 六文件聚合实算 %d 条"
                % (name, row["n"], act))
        expected_path = os.path.join(TOPICS_DIR_REL, THEME_FILES[name]).replace("\\", "/")
        if row["path"].replace("\\", "/") != expected_path:
            bad("C3", "索引壳主题「%s」正本路径 %s ≠ 期望 %s"
                % (name, row["path"], expected_path))
        c3[name] = {"declared": row["n"], "actual": act}
    shell_entry_count = len(entry_lines(strip_stat_marks(shell)))
    if shell_entry_count != 0:
        bad("C3", "索引壳内含 %d 条 `- **` 条目行（壳不得承载条目）" % shell_entry_count)
    facts["C3"] = {"per_theme": c3,
                   "shell_declared_sum": agg_declared_shell,
                   "aggregate_actual": agg_actual,
                   "shell_entry_lines": shell_entry_count}


def _check_c4(topics, theme_names, shell, bad, facts):
    """C4 反查表覆盖全部本体 E 号；返回本体 E 号集合（C6 唯一性用）。"""
    theme_ids = []
    theme_id_files = {}
    for name in theme_names:
        text = (topics.get(name) or {}).get("text")
        if text is None:
            continue
        for line in entry_lines(strip_stat_marks(text)):
            m = RX_ENTRY.match(line)
            if not m:
                continue
            eid = norm_eid(m.group(2))
            theme_ids.append(eid)
            theme_id_files.setdefault(eid, []).append(name)
    theme_id_set = set(theme_ids)
    rev_ids = shell_reverse_table(shell)
    rev_set = set(rev_ids)
    missing = sorted(theme_id_set - rev_set)
    extra = sorted(rev_set - theme_id_set)
    for eid in missing:
        bad("C4", "反查表漏掉本体 E 号 %s（主题层有·反查表无）" % eid)
    for eid in extra:
        bad("C4", "反查表多余 E 号 %s（主题层无·反查表有）" % eid)
    multi = []
    for eid in sorted(theme_id_set):
        t_cnt = theme_ids.count(eid)
        r_cnt = rev_ids.count(eid)
        if t_cnt != r_cnt:
            multi.append((eid, t_cnt, r_cnt))
    facts["C4"] = {"theme_eids": len(theme_ids), "theme_unique": len(theme_id_set),
                   "reverse_entries": len(rev_ids), "reverse_unique": len(rev_set),
                   "missing": missing, "extra": extra, "multiplicity_diff": multi}
    return theme_ids, theme_id_files, theme_id_set


def _c5_check_pointer(eid, line, title, seg, exempt, bad, note_only, c5):
    """C5 指针型条目镜像硬判据；返回 False = 本条目提前结束（原 `continue` 语义）。"""
    c5["pointer"] += 1
    if not seg:
        if eid not in exempt:
            bad("C5", "镜像缺失：判据层条目 %s 指向归档段但归档无 `#### %s` 段"
                % (eid, eid))
        else:
            c5["exempt_used"].append(eid)
        c5["seg_missing"].append(eid)
        return False
    body_lines = [ln for ln in seg if RE_ENTRY_LINE.match(ln)]
    if not body_lines:
        if eid not in exempt:
            bad("C5", "镜像缺失：归档段 `#### %s` 内无条目正文行" % eid)
        else:
            c5["exempt_used"].append(eid)
        c5["seg_missing"].append(eid)
        return False
    if title and any(title in ln for ln in body_lines):
        c5["title_hits"] += 1
    key = norm_mirror(mirror_key(line))
    if key and not any(key in norm_mirror(ln) for ln in body_lines):
        if eid not in exempt:
            note_only("C5", "形态差异（不判红）：判据层条目 %s 的正文与归档段 `#### %s` 全文非逐字同源"
                % (eid, eid))
        else:
            c5["exempt_used"].append(eid)
        c5["prefix_miss"].append(eid)
    return True


def _check_c5(topics, theme_names, archive, exempt, bad, note_only, facts):
    """C5 双层镜像（判据层 → 叙事层）；硬判据 = 段存在 + 段内有正文行。"""
    segs = parse_archive_segments(archive)
    c5 = {"pointer": 0, "seg_missing": [], "prefix_miss": [], "verbatim_hits": 0,
          "title_hits": 0, "empty_body": [], "orphan_segments": [], "w_drift": [],
          "exempt_used": [], "exempt_stale": []}
    referenced = set()
    for name in theme_names:
        text = (topics.get(name) or {}).get("text")
        if text is None:
            continue
        for line in entry_lines(strip_stat_marks(text)):
            m = RX_ENTRY.match(line)
            if not m:
                continue
            eid = norm_eid(m.group(2))
            title = entry_title(line)
            if line in archive:
                c5["verbatim_hits"] += 1
            # W1299（L-04①·A 类口径修正）：`referenced` 口径改为「正本存在该 E 号条目即算」——
            #   原口径只在**指针型**条目分支里 add ⇒ 正本自带完整叙事的条目被判成「归档段无人指向」
            #   ⇒ 实测 11 段误报（E-185 / E-288~E-290 / E-292~E-297 / E-299）。
            #   孤儿段的正确语义＝「归档有段而**正本完全无对应条目**」⇒ 无条件记入。
            referenced.add(eid)
            if RE_POINTER.search(line):
                if not _c5_check_pointer(eid, line, title, segs.get(eid), exempt, bad, note_only, c5):
                    continue
            else:
                if title and title in archive:
                    c5["title_hits"] += 1
                if line.rstrip().endswith("："):
                    c5["empty_body"].append(eid)
            # 批次号漂移（观测）
            seg = segs.get(eid)
            if seg:
                aw = re.search(r"(W\d+)", seg[0])
                if aw and aw.group(1) != m.group(1):
                    c5["w_drift"].append((eid, m.group(1), aw.group(1)))
    c5["orphan_segments"] = sorted(set(segs) - referenced)
    for eid in sorted(exempt):
        if (eid not in c5["exempt_used"] and eid not in c5["seg_missing"]
                and eid not in c5["prefix_miss"]):
            c5["exempt_stale"].append(eid)
    facts["C5"] = c5


def _check_c6(theme_ids, theme_id_files, theme_id_set, bad, facts):
    """C6 本体 E 号唯一。"""
    dups = {}
    for eid in theme_ids:
        dups[eid] = dups.get(eid, 0) + 1
    dup_list = sorted((e for e, n in dups.items() if n > 1),
                      key=lambda e: int(e.split("-")[1]))
    for eid in dup_list:
        bad("C6", "本体 E 号重复：%s 出现 %d 次（主题：%s）"
            % (eid, dups[eid], "、".join(sorted(set(theme_id_files.get(eid, []))))))
    facts["C6"] = {"total": len(theme_ids), "unique": len(theme_id_set),
                   "duplicates": dup_list}


def _check_c7(topics, theme_names, max_bytes, bad, facts):
    """C7 主题文件写窗。"""
    c7 = {}
    total_bytes = 0
    for name in theme_names:
        item = topics.get(name) or {}
        size = item.get("bytes")
        if size is None:
            text = item.get("text")
            size = len(text.encode("utf-8")) if text is not None else 0
        total_bytes += size
        c7[name] = size
        if size > max_bytes:
            bad("C7", "主题文件超写窗：%s %d 字节 > %d" % (name, size, max_bytes))
    facts["C7"] = {"per_theme": c7, "total_bytes": total_bytes, "max_bytes": max_bytes}


def evaluate(inputs, max_bytes=MAX_DOC_BYTES):
    """跑全部 7 项判据，返回 {"problems": [...], "facts": {...}}。

    inputs（可注入·单测据此造坏输入而不必改仓库真实文件）：
      {"shell":   {"path": str, "text": str},
       "topics":  {主题名: {"path": str, "text": str|None, "bytes": int}},
       "archive": {"path": str, "text": str}}

    W1315：主体按 C1-C7 拆为独立判据函数（原单函数 232 行 ⇒ 认知负担）；
    本函数只做输入归一与顺序编排，判据文案与判定行为逐字不变。
    """
    problems = []
    facts = {}
    exempt = _normalize_exempt()

    def bad(check, message):
        problems.append({"check": check, "message": message})

    shell = (inputs.get("shell") or {}).get("text") or ""
    topics = inputs.get("topics") or {}
    archive = (inputs.get("archive") or {}).get("text") or ""

    theme_names = list(PITFALL_THEME_KEYS.keys())

    _check_c1(topics, theme_names, bad, facts)
    actual_total = _check_c2(topics, theme_names, bad, facts)
    _check_c3(shell, theme_names, actual_total, bad, facts)
    theme_ids, theme_id_files, theme_id_set = _check_c4(topics, theme_names, shell, bad, facts)
    _check_c5(topics, theme_names, archive, exempt, bad, note_only, facts)
    _check_c6(theme_ids, theme_id_files, theme_id_set, bad, facts)
    _check_c7(topics, theme_names, max_bytes, bad, facts)

    return {"problems": problems, "facts": facts}


# ---- 读盘入口 ------------------------------------------------------------
def load_inputs(root=ROOT):
    """从磁盘读齐 8 个面（根索引壳 + 六主题正本 + 叙事层归档）。"""
    def _read(rel):
        path = os.path.join(root, rel)
        try:
            with open(path, encoding="utf-8") as f:
                data = f.read()
            return data, len(data.encode("utf-8"))
        except OSError:
            return None, 0

    shell_text, _ = _read(SHELL_REL)
    archive_text, _ = _read(ARCHIVE_REL)
    topics = {}
    for name in PITFALL_THEME_KEYS:
        rel = os.path.join(TOPICS_DIR_REL, THEME_FILES[name])
        text, size = _read(rel)
        topics[name] = {"path": rel.replace("\\", "/"),
                        "text": text, "bytes": size}
    return {
        "shell": {"path": SHELL_REL, "text": shell_text},
        "topics": topics,
        "archive": {"path": ARCHIVE_REL.replace("\\", "/"), "text": archive_text},
    }


def render(result):
    """把判据结果渲染成逐项 PASS/FAIL + 实测数字的文本。"""
    facts = result["facts"]
    problems = result["problems"]
    lines = []

    def status(check):
        return "FAIL" if any(p["check"] == check for p in problems) else "PASS"

    c1 = facts["C1"]
    lines.append("%s C1 %s —— %d/%d 主题文件存在且含契约段「何时读」"
                 % (status("C1"), CHECK_NAMES["C1"], c1["present"], c1["total"]))
    c2 = facts["C2"]
    detail = "、".join("%s 声明 %s/实算 %s" % (k, v["declared"], v["actual"])
                       for k, v in c2["per_theme"].items() if v)
    lines.append("%s C2 %s —— 声明合计 %d / 实算合计 %d（%s）"
                 % (status("C2"), CHECK_NAMES["C2"], c2["declared_sum"],
                    c2["actual_sum"], detail))
    c3 = facts["C3"]
    lines.append("%s C3 %s —— 壳内声明合计 %d / 六文件聚合实算 %d · 壳内条目行 %d"
                 % (status("C3"), CHECK_NAMES["C3"], c3["shell_declared_sum"],
                    c3["aggregate_actual"], c3["shell_entry_lines"]))
    c4 = facts["C4"]
    lines.append("%s C4 %s —— 本体 E 号 %d 条/去重 %d · 反查表 %d 条/去重 %d · 遗漏 %d · 多余 %d"
                 % (status("C4"), CHECK_NAMES["C4"], c4["theme_eids"], c4["theme_unique"],
                    c4["reverse_entries"], c4["reverse_unique"],
                    len(c4["missing"]), len(c4["extra"])))
    c5 = facts["C5"]
    lines.append("%s C5 %s —— 指针型条目 %d · 逐字整行命中 %d · 标题同源 %d · 段缺失 %d · 前缀不匹配 %d · 豁免在案 %d · 孤儿归档段 %d"
                 % (status("C5"), CHECK_NAMES["C5"], c5["pointer"], c5["verbatim_hits"],
                    c5["title_hits"], len(c5["seg_missing"]), len(c5["prefix_miss"]),
                    len(set(c5["exempt_used"])), len(c5["orphan_segments"])))
    c6 = facts["C6"]
    lines.append("%s C6 %s —— 本体 E 号 %d 条 · 去重 %d · 重号 %d 个 %s"
                 % (status("C6"), CHECK_NAMES["C6"], c6["total"], c6["unique"],
                    len(c6["duplicates"]), c6["duplicates"] or ""))
    c7 = facts["C7"]
    bytes_detail = "、".join("%s %d" % (k, v) for k, v in c7["per_theme"].items())
    lines.append("%s C7 %s —— 上限 %d 字节/文件 · 合计 %d 字节（%s）"
                 % (status("C7"), CHECK_NAMES["C7"], c7["max_bytes"],
                    c7["total_bytes"], bytes_detail))
    return "\n".join(lines)


def main():
    root = ROOT
    if "--root" in sys.argv:
        root = sys.argv[sys.argv.index("--root") + 1]
    inputs = load_inputs(root)
    result = evaluate(inputs)
    print(render(result))
    problems = result["problems"]
    for p in problems:
        print("FAIL  %s  %s" % (p["check"], p["message"]))
    c5 = result["facts"]["C5"]
    if c5["exempt_used"]:
        print("NOTE  镜像存量偏差豁免在案 %d 项：%s"
              % (len(set(c5["exempt_used"])), "、".join(sorted(set(c5["exempt_used"])))))
    if c5["exempt_stale"]:
        print("NOTE  镜像豁免表已失效（条目已修复·可清理）：%s" % "、".join(c5["exempt_stale"]))
    if c5["w_drift"]:
        print("NOTE  判据层与叙事层批次号漂移 %d 项：%s"
              % (len(c5["w_drift"]),
                 "、".join("%s(判据 %s/归档 %s)" % t for t in c5["w_drift"])))
    if c5["empty_body"]:
        print("NOTE  判据层正文为空的条目 %d 项：%s"
              % (len(c5["empty_body"]), "、".join(c5["empty_body"])))
    if c5["orphan_segments"]:
        print("NOTE  归档层孤儿段 %d 段（判据层无对应条目·多批次锚形态不可判）：%s"
              % (len(c5["orphan_segments"]), "、".join(c5["orphan_segments"])))
    if result["facts"]["C4"]["multiplicity_diff"]:
        print("NOTE  反查表与本体 E 号出现次数不一致 %d 项：%s"
              % (len(result["facts"]["C4"]["multiplicity_diff"]),
                 "、".join("%s(主题 %d/反查 %d)" % t
                           for t in result["facts"]["C4"]["multiplicity_diff"])))
    if problems:
        print("---- 坑表六主题拆分判据：%d FAIL ----" % len(problems))
        return 1
    print("---- 坑表六主题拆分判据：0 FAIL ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
