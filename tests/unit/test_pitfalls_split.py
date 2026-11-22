"""tests/unit/test_pitfalls_split.py —— 坑表六主题拆分判据的单测（W1290）。

门禁接线：本脚本**不**挂进 `scripts/verify_delivery.py`（门禁本体·禁改清单）⇒ 它的门禁
效果来自 **CI 的 pytest job**（会跑 tests/unit）⇒ 判据的**正负两面**都必须有单测锁住：
  · 正面：真实仓态 7 项判据 0 问题（不得误报，否则 CI 长期带病跑）
  · 反面：六类坏输入必红（不得漏报，否则判据形同虚设）

坏输入一律用 `tmp_path` 造：把真实 8 个面（根索引壳 + 六主题正本 + 叙事层归档）复制到
**临时目录**后，在临时目录里注入坏数据再判 ⇒ **绝不修改仓库真实文件**（多 Agent 并发
仓内改别人的正本＝污染他人施工面）。
"""

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS = os.path.join(ROOT, "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import check_pitfalls_split as cps  # noqa: E402
from check_pitfalls_split import evaluate, load_inputs  # noqa: E402

# 门禁口径（第 42 槽·根级脚本覆盖）：新增脚本须有「模块 import + 执行标记」实质引用
# ⇒ 本文件同时给出 from-import 形态与脚本相对路径常量（覆盖判据 E3/E1 形态）。
SCRIPT_REL = "scripts/check_pitfalls_split.py"


# ---- 夹具 ---------------------------------------------------------------
def real_inputs():
    """读真实仓态的 8 个面（只读）。"""
    return cps.load_inputs(ROOT)


def materialize(tmp_path, inputs):
    """把 inputs 落成临时仓库并回读（⇒ 坏数据只存在于临时目录）。"""
    repo = tmp_path / "repo"
    (repo / "docs" / "agent" / "pitfalls-topics").mkdir(parents=True, exist_ok=True)
    (repo / "archive" / "docs").mkdir(parents=True, exist_ok=True)
    (repo / "pitfalls.md").write_text(inputs["shell"]["text"] or "",
                                      encoding="utf-8", newline="\n")
    for name, item in inputs["topics"].items():
        rel = os.path.join("docs", "agent", "pitfalls-topics",
                           os.path.basename(item["path"]))
        (repo / rel).write_text(item["text"] or "", encoding="utf-8", newline="\n")
    (repo / "archive" / "docs" / "pitfalls-detail-ARCHIVE.md").write_text(
        inputs["archive"]["text"] or "", encoding="utf-8", newline="\n")
    return str(repo)


def declared_count(text):
    """取主题文件段头声明数（**当前值**·不硬编码）。"""
    m = re.search(r"（(\d+)(?:<!--stats:[a-z_0-9]+-->)? 条）", text)
    assert m, "段头声明未命中：无法解析当前声明数"
    return int(m.group(1))


def bump_declared(text, old=None, new=None):
    """把段头声明数改成新值（兼容 `<!--stats:xxx-->` 标记形态）。

    W1299 根治：原实现要求调用方**硬编码**当前声明数（如 90）⇒ 数据一变
    （E-283 进正本⇒90→91）既有负例单测即整体失效（5 例红）⇒ 改为**自动取当前值**：
    old 缺省 ⇒ 从段头解析当前声明数；new 缺省 ⇒ old + 1。
    参数名与个数不变（old/new 增默认值）⇒ 不构成破坏性签名变更。
    """
    if old is None:
        old = declared_count(text)
    if new is None:
        new = old + 1
    pat = re.compile(r"（%d(?:<!--stats:[a-z_0-9]+-->)? 条）" % old)
    out, cnt = pat.subn("（%d 条）" % new, text, count=1)
    assert cnt == 1, "段头声明未命中：%s" % old
    return out


def checks_of(result):
    """返回结果里出现的判据编号集合。"""
    return {p["check"] for p in result["problems"]}


def messages_of(result, check):
    return [p["message"] for p in result["problems"] if p["check"] == check]


# ---- 正面 ---------------------------------------------------------------
def test_real_repo_state_has_zero_problems():
    """正例：真实仓态下 ①~⑦ 全过（脚本返回 0 个问题）。"""
    result = cps.evaluate(real_inputs())
    assert result["problems"] == [], "真实仓态不应有 FAIL：%s" % (
        result["problems"],)
    assert result["facts"]["C6"]["duplicates"] == []
    assert result["facts"]["C3"]["shell_entry_lines"] == 0
    assert result["facts"]["C4"]["missing"] == []
    assert result["facts"]["C4"]["extra"] == []


def test_real_repo_mirror_has_no_hard_defect():
    """正例守护：真实仓态的镜像**硬判据**零缺陷（指针条目均有归档段且段内有正文行）。

    W1290 裁决：形态差异（正本截断+指针版 vs 归档全文）**不是缺陷**⇒ 不判红、也不进白名单；
    硬判据只认「段缺失」与「空段」两类真缺陷 ⇒ 真实仓态必须零命中。
    """
    result = cps.evaluate(real_inputs())
    c5 = result["facts"]["C5"]
    assert result["facts"]["C5"]["pointer"] > 0
    assert not c5.get("seg_missing"), "存在归档段缺失（真缺陷）：%s" % c5.get("seg_missing")
    assert not cps._normalize_exempt(), "豁免表须为空（新增白名单须用户批准·铁律 16⑦）"


# ---- 反面 ---------------------------------------------------------------
def test_c2_declared_count_mismatch_is_red():
    """负例：主题文件段头声明数与实算不符 ⇒ 判红。"""
    inputs = real_inputs()
    item = inputs["topics"]["CSS / 视觉渲染"]
    cur = declared_count(item["text"])
    item["text"] = bump_declared(item["text"])
    result = cps.evaluate(inputs)
    assert "C2" in checks_of(result)
    assert any("声明 %d 条" % (cur + 1) in m for m in messages_of(result, "C2"))


def test_c3_shell_carrying_entry_line_is_red():
    """负例：索引壳里多出一条 `- **` 条目行 ⇒ 判红（壳不得承载条目）。"""
    inputs = real_inputs()
    inputs["shell"]["text"] += "\n- **壳内伪造条目**（W9999 实证·E-999）：壳不该带条目\n"
    result = cps.evaluate(inputs)
    assert "C3" in checks_of(result)
    assert any("壳不得承载条目" in m for m in messages_of(result, "C3"))


def test_c3_shell_declared_count_mismatch_is_red():
    """负例：索引壳表内声明条数 ≠ 六文件聚合实算 ⇒ 判红。"""
    inputs = real_inputs()
    shell_txt = inputs["shell"]["text"]
    m = re.search(r"\| (\d+)<!--stats:pitfalls_css--> \|", shell_txt)
    assert m, "壳内 CSS 声明应带 stats 标记"
    inputs["shell"]["text"] = shell_txt.replace(
        m.group(0), "| %d<!--stats:pitfalls_css--> |" % (int(m.group(1)) + 1), 1)
    result = cps.evaluate(inputs)
    assert "C3" in checks_of(result)
    assert any("聚合实算" in m for m in messages_of(result, "C3"))


def test_c4_reverse_table_missing_eid_is_red():
    """负例：反查表漏掉一个本体 E 号 ⇒ 判红。"""
    inputs = real_inputs()
    shell = inputs["shell"]["text"]
    # W1299：反查表按「每行 10 个 E 号」排布 ⇒ 删整行会连带删多个号；须挑一个
    #   **只出现一次**的本体 E 号（否则其余号在别的主题小节仍有 ⇒ 仍被覆盖 ⇒ 不判遗漏）。
    counts = {}
    for mm in re.finditer(r"E-\d+", shell):
        counts[mm.group(0)] = counts.get(mm.group(0), 0) + 1
    victim_eid = next((e for e, c in sorted(counts.items()) if c == 1), None)
    assert victim_eid, "应能找到只出现一次的本体 E 号"
    victim = next((ln for ln in shell.splitlines() if victim_eid in ln), None)
    assert victim, "反查表应含该 E 号所在行"
    inputs["shell"]["text"] = shell.replace(victim + "\n", "", 1)
    result = cps.evaluate(inputs)
    assert "C4" in checks_of(result)
    assert any("漏掉本体 E 号" in m for m in messages_of(result, "C4"))


def test_c5_missing_archive_segment_is_red(tmp_path):
    """负例：删掉某指针条目对应的归档段 ⇒ 段缺失（真缺陷）⇒ 判红。"""
    inputs = real_inputs()
    repo = materialize(tmp_path, inputs)
    topic = os.path.join(repo, "docs", "agent", "pitfalls-topics", "css-visual.md")
    with open(topic, encoding="utf-8") as f:
        text = f.read()
    archive = inputs["archive"]["text"] or ""
    target = None
    for line in text.splitlines():
        m = cps.RX_ENTRY.match(line)
        if not m or not cps.RE_POINTER.search(line):
            continue
        eid = cps.norm_eid(m.group(2))
        if re.search(r"(?m)^#### %s\b" % re.escape(eid), archive):
            target = (line, eid)
            break
    assert target, "应能找到一条有归档段的指针型条目"
    line, eid = target
    broken_archive = re.sub(r"(?ms)^#### %s\b.*?(?=^#### |\Z)" % re.escape(eid), "", archive)
    with open(os.path.join(repo, "archive", "docs", "pitfalls-detail-ARCHIVE.md"),
              "w", encoding="utf-8", newline="\n") as f:
        f.write(broken_archive)
    result = cps.evaluate(cps.load_inputs(repo))
    assert "C5" in checks_of(result), "归档段缺失未判红：%s" % (result["problems"],)
    assert any(eid in msg for msg in messages_of(result, "C5"))


def test_c6_duplicate_eid_is_red():
    """负例：出现重复本体 E 号 ⇒ 判红。"""
    inputs = real_inputs()
    item = inputs["topics"]["CSS / 视觉渲染"]
    lines = item["text"].splitlines()
    dup = None
    for line in lines:
        m = cps.RX_ENTRY.match(line)
        if m and not cps.RE_POINTER.search(line):
            dup = line
            break
    assert dup, "应能找到一条可复制的条目"
    item["text"] = item["text"].replace(dup, dup + "\n" + dup, 1)
    item["text"] = bump_declared(item["text"])
    result = cps.evaluate(inputs)
    assert "C6" in checks_of(result)
    assert any("本体 E 号重复" in m for m in messages_of(result, "C6"))


def test_c7_topic_over_size_window_is_red(tmp_path):
    """负例：某主题文件超过字节窗 ⇒ 判红。"""
    inputs = real_inputs()
    repo = materialize(tmp_path, inputs)
    topic = os.path.join(repo, "docs", "agent", "pitfalls-topics", "css-visual.md")
    with open(topic, "w", encoding="utf-8", newline="\n") as f:
        f.write("x" * (cps.MAX_DOC_BYTES + 1))
    result = cps.evaluate(cps.load_inputs(repo))
    assert "C7" in checks_of(result)
    assert any("超写窗" in m for m in messages_of(result, "C7"))


def test_c1_missing_topic_file_is_red():
    """负例：某主题文件缺失 ⇒ 判红。"""
    inputs = real_inputs()
    inputs["topics"]["流程 / 协作 / 取证"]["text"] = None
    inputs["topics"]["流程 / 协作 / 取证"]["bytes"] = 0
    result = cps.evaluate(inputs)
    assert "C1" in checks_of(result)
    assert any("主题文件缺失" in m for m in messages_of(result, "C1"))


# ---- 端到端（退出码）----------------------------------------------------
def test_cli_exit_code_zero_on_real_repo():
    """端到端：真实仓态跑脚本 ⇒ 退出码 0。"""
    proc = subprocess.run([sys.executable, SCRIPT_REL],
                          cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_cli_exit_code_one_on_broken_repo(tmp_path):
    """端到端：临时仓里注入坏数据 ⇒ 退出码 1（门禁效果来自 pytest job·须真的会红）。"""
    inputs = real_inputs()
    repo = materialize(tmp_path, inputs)
    topic = os.path.join(repo, "docs", "agent", "pitfalls-topics", "css-visual.md")
    with open(topic, encoding="utf-8") as f:
        text = f.read()
    with open(topic, "w", encoding="utf-8", newline="\n") as f:
        f.write(bump_declared(text, None, 77))
    proc = subprocess.run(
        [sys.executable, SCRIPT_REL, "--root", repo],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "FAIL" in proc.stdout


def test_rx_entry_multi_recognizes_parallel_batch_anchor():
    """B 类回归锁（W1299 立·W1300 治本）：并列多批次锚须被**公共本体口径**识别。

    W1299：公共口径只认单批次 ⇒ 镜像侧另立扩展正则 RX_ENTRY_MULTI（口径双份）
    ⇒ 本体 E 号集合少 1（275 vs 条目行实测 276）⇒ 两套「坑位身份」口径不一致。
    W1300（L-07 治本）：公共 RX_ENTRY 已扩为支持并列锚（取**首个**批次号·与归档段头同序）
    ⇒ 镜像侧私有扩展正则**退役**（单一事实源·防两份正则各自漂移）⇒ 本例改断言「公共口径认该形态」。

    **函数名沿用旧名**：guardrails 的 api_diff 判据把 tests/ 下的 test 函数也当「公开 API」
    ⇒ 改名即被判「破坏性删除」而阻断提交（仓内实测）。名实不符之处以本 docstring 说明。
    """
    line = "- **某条目**（W1284/W1285 实证·E-291·跨项目通用）：正文"
    m = cps.RX_ENTRY.match(line)
    assert m is not None, "公共本体口径须识别并列多批次锚"
    assert m.group(1) == "W1284", m.group(1)
    assert m.group(2) == "E-291", m.group(2)
    assert not hasattr(cps, "RX_ENTRY_MULTI"), "镜像侧私有扩展正则应退役（口径单一事实源）"


def test_c5_non_pointer_entry_segment_is_not_orphan():
    """A 类回归锁（W1299）：正本自带完整叙事（非指针型）的条目 ⇒ 其归档段不得被判「孤儿段」。

    原口径只在**指针型**条目分支把 E 号计入 referenced ⇒ 正本完整叙事型条目的归档段
    被误判成「无人指向的孤儿段」（实测 11 段误报）。⇒ 孤儿语义应为「正本完全无对应条目」。
    """
    inputs = real_inputs()
    item = inputs["topics"]["CSS / 视觉渲染"]
    eid = "E-9001"
    line = "- **合成条目：判据层自带完整叙事**（W9999 实证·%s·跨项目通用）：正文" % eid
    item["text"] = item["text"] + "\n" + line
    seg = "\n#### %s（合成）\n\n%s\n" % (eid, line)
    inputs["archive"]["text"] = (inputs["archive"]["text"] or "") + seg
    result = cps.evaluate(inputs)
    assert eid not in result["facts"]["C5"]["orphan_segments"], (
        "正本存在该 E 号条目却被判孤儿段：%s" % (result["facts"]["C5"]["orphan_segments"],))


def test_e283_canonical_entry_exists():
    """C 类回归锁（W1299）：E-283 判据层条目须存在（归档有段·正本不得缺）。"""
    inputs = real_inputs()
    eids = set()
    for _name, item in inputs["topics"].items():
        for line in (item["text"] or "").splitlines():
            m = cps.RX_ENTRY.match(line)
            if m:
                eids.add(cps.norm_eid(m.group(2)))
    assert "E-283" in eids, "E-283 判据层条目缺失（归档有段·正本须补齐）"
