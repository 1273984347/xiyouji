#!/usr/bin/env python3
"""batch_cascade.py — W 批次文档级联常驻脚本（W542 新建·AGENTS §4.3 三新规④配套）。

用法：
  python scripts/batch_cascade.py --spec <spec.json>             # dry-run：全部断言跑通但不写盘
  python scripts/batch_cascade.py --spec <spec.json> --apply     # 断言全过后统一落盘

两阶段设计：第一阶段在内存中对全部 10 个面做断言与改写（W628 起 +CITATION.cff），任何锚点失配立即中止（零落盘）；
第二阶段仅在 --apply 时统一写入。写入后自检交接文档无 `））；` 双括号。--apply 落盘后输出级联文件清单
（scripts/output/_cascade_files_<批号>.txt，W649 起——防 partial commit 漏级联面：提交时按清单 git add）。

spec 字段见文末说明（JSON）。
"""
import argparse
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_root = os.path.realpath(ROOT)



def load(path):
    _real = os.path.realpath(os.path.join(ROOT, path))
    if not (_real == _root or _real.startswith(_root + os.sep)):
        raise SystemExit("path escapes project root: %s" % path)
    s = open(_real, encoding="utf-8", newline="").read()
    # W706 结构防线：混行尾文件下按单一 nl 操作会错位吞段（「一、当前进度」标题被吞实证）——fail-closed
    _crlf = "\r\n" in s
    _lf_bare = re.search(r"(?<!\r)\n", s) is not None
    _cr_bare = re.search(r"\r(?!\n)", s) is not None
    if (_crlf and (_lf_bare or _cr_bare)) or (_lf_bare and _cr_bare):
        raise AssertionError(
            "混合行尾文件（CRLF/CR/LF 并存）——级联按单一 nl 操作会错位吞段（W706 实证）：先归一行尾再级联"
        )
    return s, ("\r\n" if "\r\n" in s else "\n")


def drop_block(s, bm_start, nl):
    """淘汰一个里程碑块：标题行 + 其后连续 bullet 行（W624 提取·整块删除）。

    bullet 行=「  - 」前缀（spec milestone_block 唯一形状）；其余任何行
    （空行/新组标题/章节标题/引用行/非 bullet 正文）即消费终点——有界于块自身，
    不越过分隔空行、不吞正文。单块滚动制下每批整块移除最老块。
    """
    seg = s[bm_start:].split(nl)
    j = 1  # seg[0] = 标题行
    while j < len(seg) and seg[j].startswith("  - "):
        j += 1
    return s[:bm_start] + s[bm_start + len(nl.join(seg[:j]) + nl):]


def precheck(spec):
    """spec 预校验（W667/S-01）：字段级分隔符黑名单 + title 领衔断言——在 dry-run 断言之前拦截
    「能落盘但会破坏下一批锚点正则」的 spec（W664 实证：W663 desc 含「·」致 README/项目说明锚点失配）。
    分隔符按字段分治：desc 写入版本行（锚点 ·A1-A6 / —A1-A6 / ；详见）→ 禁 ·；—；head_sentence 进入
    HEAD 句（锚点 ；详见）→ 禁 ；—（· 已实证无害·全角括号由既有断言管）。返回违例清单。"""
    issues = []
    for field, banned in (("desc", ("·", "；", "—")), ("head_sentence", ("；", "—"))):
        for sep in banned:
            if sep in spec.get(field, ""):
                issues.append("spec.%s 含分隔符 %r（写入版本行/HEAD 句后将使下一批锚点正则失配）"
                              % (field, sep))
    if not str(spec.get("title", "")).startswith(str(spec.get("batch", ""))):
        issues.append("spec.title 未以 batch 号领衔（现役段解析取标题首个 W###·合并段场景必须显式领衔）")
    if "**文件**：" not in str(spec.get("changelog_body", "")):
        issues.append("spec.changelog_body 缺「**文件**」行（四件套必填·W723 起第 31 门禁 C4-f 据其对账手工件入库·"
                      "路径须写 repo 相对路径·见 pitfalls git 类）")
    # W964 定形契约：脚注条目头必须是「阿拉伯日期（W###）」——中文数字日期形态对滚动切分器
    # 不可见（实证 52 条二〇二六形态条目黏成 67.1KB 巨段使「保留 5 条」契约名存实亡·AGENTS.md
    # 被撑到 110KB）；条目是索引不是摘要，长度一并封顶。
    _note = str(spec.get("agents_note", ""))
    if not re.match(r"^20\d{2}-\d{2}-\d{2}（W\d{3,4}）", _note):
        issues.append("spec.agents_note 未以「阿拉伯日期（W###）」条目头开场（W964 定形契约·"
                      "中文数字日期会让滚动器失明）：%r" % _note[:40])
    if len(_note) > 120:
        issues.append("spec.agents_note 长 %d 字 > 120 上限（W964 定形·W989 收紧·脚注是索引不是摘要·"
                      "细节归 CHANGELOG）" % len(_note))
    return issues


def _assert_status_wnum(spec, batch):
    """段内「状态」字段的认领登记 W 号必须等于本段号（W956 建 · E-28 段状态串行错位防线）。

    病根（W954 复盘报告实例 4）：收官回填按写顺序推进时，W941 段的状态字段曾写成
    「在途（认领登记 W940·待提交入库）」——段号与状态所述批次错位（后已被订正）。
    凡**写入段内状态字段**的动作（正常级联 _face_changelog 与递延补段 backfill_changelog
    两个写入点共用本断言），断言状态文本里「认领登记 W###」这一自我指称形态所指的
    W 号 == 本段号；状态文本引用别批（承接 / 让号最终落点 / 回填锚注等）不受限——
    只锁「认领登记」形态，防错位不防合法引用。
    """
    m = re.search(r"认领登记\s*W(\d+)", str(spec.get("changelog_body", "")))
    if m:
        assert int(m.group(1)) == int(str(batch)[1:]), (
            "spec.changelog_body 状态字段写「认领登记 W%s」≠ 本段号 %s——E-28 段状态串行错位"
            "（段号与状态所述批次必须同批·W956/P-43-05 防线）" % (m.group(1), batch)
        )


class _Ctx:
    """级联上下文：spec 字段 + 派生量 + 落盘队列（W731 提取）。"""

    def __init__(self, spec):
        self.spec = spec
        self.batch, self.date = spec["batch"], spec["date"]  # W711：ver 字段弃用（方案 D 批次键唯一·spec.version 仅存档）
        self.desc = spec["desc"]
        self.entry = spec["head_entry"]
        self.new_w = None     # CHANGELOG 面回填：现役段号 + 1
        self.new_rule = None  # CHANGELOG 面回填：编号规则段新形态
        self.pend = []        # (path, content, nl) 落盘队列
        self.cl_src = ""      # CHANGELOG 原文（交接文档面 W534 断言用）


def _face_changelog(ctx):
    """CHANGELOG 面：插入新段并推进编号规则（回填 ctx.new_w/new_rule/cl_src）。"""
    # ---------- CHANGELOG ----------
    p = "CHANGELOG.md"
    s, nl = load(p)
    ctx.cl_src = s  # W713：保留 CHANGELOG 原文，供交接里程碑淘汰前断言（W534 承诺）
    # W711 方案 D 双形态：历史段 ### vX.Y.Z（date）：W### / 新段 ### W###（date）：标题
    m = re.search(r"^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（[^）]*）：)", s, re.M)
    assert m, "CHANGELOG 未找到现役段"
    cur_anchor = m.group(0)
    cur_w = int(m.group(1) or m.group(2))
    # W895：显式缺口许可（并行在途批的现实）——--allow-gap 列出的 W 号须在台账有认领行、
    # 且在 CHANGELOG 尚无段（其落段自理：晚到者用 backfill_changelog.py 按号序补）。
    gaps = getattr(ctx, "allow_gap", [])
    if gaps:
        ledger = open(os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md"), encoding="utf-8").read()
        for g in gaps:
            assert re.search(rf"^\| {re.escape(g)} ", ledger, re.M), f"缺口 {g} 在台账无认领行"
            assert f"### {g}" not in s, f"缺口 {g} 已有段（无需允许）"
        print("  缺口许可：%s（在途·台账已有认领行）" % "、".join(gaps))
    new_w = cur_w + 1 + len(gaps)
    ctx.new_w = new_w
    assert ctx.batch == "W" + str(new_w), f"批次号应为 W{new_w}" + (f"（含缺口 {gaps}）" if gaps else "")
    assert ("### " + ctx.batch) not in s, ctx.batch + " 段已存在"
    old_rule, new_rule = f"（W001-W{cur_w}）", f"（W001-W{new_w}）"
    ctx.new_rule = new_rule
    # W712：cur_anchor 改行首锚定——段 body 内的形态示例引用（反引号内·非行首）不再使计数爆炸
    assert s.count(old_rule) == 1, "编号规则段锚点异常"
    _anchor_hits = len(re.findall(rf"^{re.escape(cur_anchor)}", s, re.M))
    assert _anchor_hits == 1, f"现役段标题行首命中 {_anchor_hits}（应为 1·body 自指内容须避开行首同形）"
    # W713：precheck 强制 title 以批次号领衔（历史段 ：W### 解析依赖），新形态段标题由模板自带 batch——
    # 模板侧清洗 title 领衔号，防「### W713（date）：W713 标题」双写（W711/W712 实证·file-index 同根）
    title_body = re.sub(r"^W\d+\s+", "", ctx.spec["title"]).strip()
    new_title = f"### {ctx.batch}（{ctx.date}）：{title_body}"
    _ins = new_title + ctx.spec["changelog_body"].replace("\n", nl) + nl + cur_anchor
    out = re.sub(rf"^{re.escape(cur_anchor)}", lambda m: _ins, s, count=1, flags=re.M)  # W717：lambda 字面替换——replacement 串语义会把 body 中的 \d 等当转义（bad escape·本批实证）
    # re.sub 行首锚定插入（W712：防 body 自指·replace 全文计数会误伤）
    out = out.replace(old_rule, new_rule, 1)
    assert out.count(new_title) == 1 and out.count(new_rule) == 1
    ctx.pend.append((p, out, nl))


def _face_three_docs(ctx):
    """README / STRUCTURE / 项目说明 三文档批头版本行。

    W1005 行锚定化（根因修复·本批实证）：四个正则的 desc 匹配段原为 `[^·]*` / `[^—]*`。
    Python 字符类 `[^X]` **匹配换行符** ⇒ 匹配区间可跨行；而 re.sub 替换的是**整个匹配区间**，
    跨行匹配即等于静默删掉中间行的内容。

    实证（W1005）：项目说明.md「当前版本」列表行的正则**无尾锚点** ⇒ 旧 desc 行内无「·」时
    `[^·]*` 一路吞到下一处「·」之前，匹配区间 1143..1342 跨 1 行，re.sub 后该文件 103 行→102 行，
    第 49 行「当前阶段」行首（87 页可视化 + Phase 7 逐回解读…）被静默删掉。

    反直觉点（值得单独记住）：旧 desc **含**「·」时反而**安全**——`[^·]*` 止于行内；
    而 desc **无**「·」（正是 C6 判据 W841 要求的形态）才触发跨行吞并。
    ⇒ C6 与本面旧正则在列表行上互为镜像：一个把「·」清掉，另一个靠「·」才不越界。

    修法（本批）：① 四个 desc 匹配段一律行锚定（`[^\\n\\r·]` / `[^\\n\\r—]` / `[^\\n\\r]`）；
    ② 空白量一律 `[ \\t]`（`\\s` 亦匹配换行）；③ 每个改写面补「替换前后行数不变」断言
    ——吞并一旦复发当场 FAIL，而非静默落盘；④ 列表行由 `[^·]*` 改 `[^\n\r]*`（整行替换）
    ⇒ 顺带根治「旧 desc 尾部残留」（历史实证：旧 desc 含「·」时匹配止于「·」，其尾部残留行尾）。

    只读面（`[^*]*` / `[^；]*` 等）跨行匹配只会导致断言 FAIL（fail-closed 误报），不产生破坏，
    故本批不动——同族风险只锁定「改写面」。
    """
    # ---------- README / STRUCTURE / 项目说明 ----------
    p = "README.md"
    s, nl = load(p)
    out = re.sub(r"> \*\*当前(?:版本 v[\d.]+|批次 W\d+)（[^）]*）\*\*：[ \t]*(?:v[\d.]+[ \t]+)?(?:W\d+[ \t]+)?[^\n\r·]*·A1-A6",
                 f"> **当前批次 {ctx.batch}（{ctx.date}）**：{ctx.desc}·A1-A6", s, count=1)  # W711 方案 D 新抬头·W712 锚点兼容 desc 直连形态·W1005 行锚定化
    assert out != s, "README 版本行未变化"
    assert out.count("\n") == s.count("\n"), "README 版本行替换吞行（行锚定失效·W1005 跨行吞并防线）"
    ctx.pend.append((p, out, nl))

    p = "STRUCTURE.md"
    s, nl = load(p)
    out = re.sub(r"> 当前(?:版本：v[\d.]+|批次：W\d+)（[^）]*）—[ \t]*(?:v[\d.]+[ \t]+)?(?:W\d+[ \t]+)?[^\n\r—]*—[ \t]*A1-A6",
                 f"> 当前批次：{ctx.batch}（{ctx.date}）— {ctx.desc}—A1-A6", s, count=1)  # W712 锚点兼容 desc 直连·W1005 行锚定化
    assert out != s, "STRUCTURE 版本行未变化"
    assert out.count("\n") == s.count("\n"), "STRUCTURE 版本行替换吞行（行锚定失效·W1005 跨行吞并防线）"
    ctx.pend.append((p, out, nl))

    p = "docs/00-导读/项目说明.md"
    s, nl = load(p)
    out = re.sub(r"> 当前(?:版本 v[\d.]+|批次 W\d+)（[^）]*）：[ \t]*(?:v[\d.]+[ \t]+)?(?:W\d+[ \t]+)?[^\n\r·]*·详细变更见",
                 f"> 当前批次 {ctx.batch}（{ctx.date}）：{ctx.desc}·详细变更见", s, count=1)  # W712 锚点兼容 desc 直连·W1005 行锚定化
    assert out != s, "项目说明头部版本行未变化"
    assert out.count("\n") == s.count("\n"), "项目说明头部版本行替换吞行（行锚定失效·W1005 跨行吞并防线）"
    out2 = re.sub(r"(\*\*当前(?:版本|批次)\*\*：)(?:v[\d.]+|W\d+)（[^）]*）—[ \t]*(?:v[\d.]+[ \t]+)?(?:W\d+[ \t]+)?[^\n\r]*",
                  rf"\g<1>{ctx.batch}（{ctx.date}）— {ctx.desc}", out, count=1)
    assert out2 != out, "项目说明「当前版本」列表行未变化（正则失配·fail-closed——W711 起 desc 直连形态实证·W713 补断言）"
    assert out2.count("\n") == out.count("\n"), "项目说明「当前版本」列表行替换吞行（W1005 跨行吞并防线）"
    ctx.pend.append((p, out2, nl))


def _handover_rotate_oldest(s, ctx, nl, h1pos):
    """交接文档：滚动淘汰最老里程碑块并同步「历史概要」指针（W534/W624/W713 语义）。"""
    pm = re.search(r"> 历史概要（W(\d+) 及更早）的详细记录见", s)
    assert pm, "未找到历史概要指针"
    oldest_w = pm.group(1)
    # W713 双形态 + 窗口限定进度段内（防后文待办/方法论区 bullet 误入旋转窗）
    blocks_all = [b for b in re.finditer(r"- \*\*(?:v[\d.]+ )?(W\d+)[^*]*\*+[^\r\n:*]{0,30}：", s) if b.start() > h1pos]
    # W913：窗口不足 2 块不滚动（契约「只留最近 5 版」——不足时无盈可滚；原无条件滚动在
    # 单块窗口必致空窗异常·阻断后续一切级联·W912/W913 两批连续实证）
    if len(blocks_all) < 2:
        return s
    tgt = [b for b in blocks_all if b.group(1) == "W" + oldest_w]
    if not tgt:
        raise AssertionError(f"未找到最老里程碑块 W{oldest_w}；现存块 {[b.group(1) for b in blocks_all]}")
    assert int(tgt[0].group(1)[1:]) == min(int(b.group(1)[1:]) for b in blocks_all), (
        "淘汰目标非窗口最老块——「历史概要」指针漂移（W712 手工段实证 pm=最新块形态）："
        "先手工把指针归位到最老可见块再级联（W713 旋转语义防线）"
    )
    bm_start = tgt[0].start()
    assert bm_start > h1pos, (
        f"最老里程碑块 W{oldest_w} 不在「一、当前进度」段内（W705 教训：跨段整块淘汰会吞掉段标题）"
    )
    eidx = s.find(f"> 历史概要（W{oldest_w} 及更早）的详细记录见", bm_start)
    assert eidx != -1
    # W534 承诺恢复（W713）：淘汰前断言该批详细记录已入 CHANGELOG 段（信息零丢失）
    assert re.search(rf"^### (?:v[\d.]+（[^）]*）：W{oldest_w}\b|W{oldest_w}（[^）]*）：)", ctx.cl_src, re.M), (
        f"CHANGELOG 无 W{oldest_w} 段（W534 契约：删前逐批断言 CHANGELOG 有段）"
    )
    # W624 修复：整块淘汰 = 标题行 + 其后连续 bullet 行（至空行/新组/标题/引用行止）。
    # W557 版候选表里的裸 "\n" 命中标题行自身行尾 → 每批只删标题行文本，bullets 留成
    # 无标题组、残留换行累积成空行串（W623 实证 33 组孤儿 + 14 行 debris，_w624 批清债）。
    # W557 前的旧实现从块起点整段删到指针，块区漂移时会连正文吞掉（W557 dry-run 实证）——
    # 本实现消费终点有界于块自身行，两个历史缺陷闭合。
    s = drop_block(s, bm_start, nl)
    # W713 旋转语义修正：pm ← 淘汰后窗口剩余最老块（W534 滚动窗口意图——原实现 pm←new_w
    # 使下一批淘汰上批最新块、更老块永不滚动，W710→W711 实证行为）
    _win = s[h1pos:s.find("> 历史概要（W")]
    _remain = [int(x[1:]) for x in re.findall(r"- \*\*(?:v[\d.]+ )?(W\d+)[^*]*\*+[^\r\n:*]{0,30}：", _win)]
    assert _remain, "淘汰后里程碑窗口为空（异常）"
    s = s.replace(f"> 历史概要（W{oldest_w} 及更早）的详细记录见",
                  f"> 历史概要（W{min(_remain)} 及更早）的详细记录见", 1)
    return s


def _face_handover(ctx):
    """交接文档面：头尾链/进度标题/里程碑块/HEAD 句全量改写与结构断言。"""
    # ---------- 交接文档 ----------
    p = "HANDOVER.md"
    s, nl = load(p)
    assert s.count("））；") == 0, "基线已存在双括号，先人工处理"
    s = s.replace("> 最后更新：", "> 最后更新：" + ctx.entry + "·", 1)
    h0 = s.find("> 最后更新：")
    h1 = s.find(nl, h0)
    head_line = s[h0:h1]
    entries = re.findall(r"·20\d{2}-\d{2}-\d{2}（", head_line)
    while len(entries) + 1 > 3:
        note_idx = head_line.find("·（W")
        assert note_idx != -1, "未找到历史注记锚点"
        oldest = head_line.rfind("·20", 0, note_idx)
        assert oldest != -1
        head_line = head_line[:oldest] + head_line[note_idx:]
        entries = re.findall(r"·20\d{2}-\d{2}-\d{2}（", head_line)
    s = s[:h0] + head_line + s[h1:]
    s = re.sub(r"；(?:v[\d.]+ W\d+|W\d+) 起生效）", f"；{ctx.batch} 起生效）", s, count=1)  # W713 双形态（该行现不存在=静默无操作·防未来回加时失配）
    # W705 教训：标题锚点与替换串形态必须恒定——旧替换串丢 ver 前缀致下一批锚点静默失配（re.sub 0 替换不报错），
    # 里程碑块遂在头部错位堆积、drop_block 跨段淘汰吞掉「一、当前进度」标题。此处改双形态锚点 + count 断言 fail-closed。
    _prog = re.compile(r"## 一、当前进度（(?:v[\d.]+ )?W\d+ [^；]*；更早批次详见 CHANGELOG\.md）")
    assert len(_prog.findall(s)) == 1, "「一、当前进度」标题锚点失配（W705 教训：静默失配后逐批漂移·先修复交接文档结构再级联）"
    s = _prog.sub(f"## 一、当前进度（{ctx.batch} {ctx.desc}；更早批次详见 CHANGELOG.md）", s, count=1)
    fb = re.search(r"- \*\*(?:v[\d.]+ )?W\d+", s)  # W713 双形态（W711 起新块无 v 前缀）
    h1pos = s.find("## 一、当前进度")
    assert fb and h1pos != -1 and fb.start() > h1pos, (
        "里程碑首块必须位于「一、当前进度」段内（W705 教训：文件头错位块链自我强化·先修复交接文档结构再级联）"
    )
    # W727 根修：rfind(nl)+1 在双字符 nl（CRLF 工作树·autocrlf=true）下少进 1 字节——
    # 标题行尾 \r\n 被撕成裸 \r（里程碑块插到 \r 与 \n 之间）+ 块尾多出裸 \n，交接文档混行尾
    # （W706 防线在下批 dry-run 正确拦截·fail-closed 实证）。LF 工作树 nl 单字符故 +1 恒正确，
    # 此前批次均运行于 LF 工作树所以未暴露。+len(nl) 双形态恒公。
    at = s.rfind(nl, 0, fb.start()) + len(nl)
    s = s[:at] + ctx.spec["milestone_block"].replace("\n", nl) + nl + s[at:]
    s = _handover_rotate_oldest(s, ctx, nl, h1pos)
    hs = re.search(r"当前 HEAD = (?:v[\d.]+ )?W\d+（[^）]*；详见 CHANGELOG）", s)
    assert hs, "未找到当前 HEAD 句"
    s = s[:hs.start()] + "当前 HEAD = {}（{}；详见 CHANGELOG）".format(ctx.batch, ctx.spec["head_sentence"]) + s[hs.end():]
    # W560 修复：尾链 prepend 必须锚定文末行（旧实现 s.replace("最后更新：", ..., 1) 命中的是
    # 头链首处 → 头链 entry 双写「E；E·」，W556/W557/W558 三批实证）。改用 rfind 定位文末行。
    tail_idx = s.rfind("最后更新：")
    assert tail_idx != -1, "未找到文末「最后更新」历史链"
    if ctx.entry + "；" not in s[tail_idx : tail_idx + len(ctx.entry) + 2]:
        s = s[:tail_idx] + "最后更新：" + ctx.entry + "；" + s[tail_idx + len("最后更新："):]
    # W560: 尾链维持 ≤3 条（交接文档维护契约②）
    tline_end = s.find(nl, tail_idx)
    tline = s[tail_idx:tline_end]
    tparts = re.split("；(?=20\\d{2}-)", tline)
    if len(tparts) > 3:
        s = s[:tail_idx] + "；".join(tparts[:3]) + s[tline_end:]
    assert s.count("））；") == 0, "写入后出现双括号 ））；"
    # W708 review：结构断言前置到落盘前（原仅写后 selfcheck WARN——脏盘已落才报告违 fail-closed 意图；写后断言保留双保险）
    _m = s.find("# 交接文档")
    assert _m != -1 and not s[:_m].strip(), "交接文档主标题前存在错位内容（结构断言·落盘前拦截）"
    _z, _y, _e = (s.find("## ⚠️ 零、当前阻塞"), s.find("## 一、当前进度"), s.find("## 二、下一步方向候选清单"))
    assert -1 < _z < _y < _e, f"交接文档段序破坏（零={_z} 一={_y} 二={_e}）——段标题被吞（结构断言·落盘前拦截）"
    assert re.search(r"> 历史概要（W\d+ 及更早）的详细记录见", s), "交接文档历史概要指针缺失（结构断言·落盘前拦截）"
    ctx.pend.append((p, s, nl))


def _face_workflows(ctx):
    """workflows README 头部区间与里程碑尾标记。"""
    # ---------- workflows README ----------
    p = ".github/workflows/README.md"
    s, nl = load(p)
    BS = chr(92)
    winpath = "`D:" + BS + "xiyouji`"  # W596：旧值为已不存在的双副本路径，曾每批续写进 workflows README
    pat_wf = re.compile(r"→ W450-W\d+\*\* — 西游记解读项目（" + re.escape(winpath) + r"，(?:v[\d.]+\s+)?W\d+）的 GitHub Actions 工作流层。")  # W711 双形态（ver 可选）
    repl_wf = f"→ W450-W{ctx.new_w}** — 西游记解读项目（{winpath}，{ctx.batch}）的 GitHub Actions 工作流层。"
    out = pat_wf.sub(lambda m: repl_wf, s, count=1)
    assert out != s, "workflows 头部未变化"
    out = re.sub(r"> \*\*W450-W\d+\*\*：verify 门禁体系扩展",
                 f"> **W450-W{ctx.new_w}**：verify 门禁体系扩展", out, count=1)
    marker = "无 workflow 结构改动）。"
    assert out.count(marker) == 1, f"里程碑尾标记出现 {out.count(marker)} 次"
    out = out.replace(marker, f"无 workflow 结构改动）+ W{ctx.new_w} {ctx.desc}·无 workflow 结构改动）。", 1)
    ctx.pend.append((p, out, nl))


# ---------- 四页脚（W717 锚定·W724 双重缺陷根修+链长治理）：
# 缺陷一=W717 版回写 mm.group(0) 而 s[at:] 已含该段 → 每批整链复制一遍（W705 错位链自强化页脚版·
# 六批后 index 重复 182 token/dukou 216·用户浏览器实见）；缺陷二=800 字符窗口截断 mm 致插入点
# 落 token 中间（「v2.3.28W722」粘连实证）。根修=完整 footer 节点内定位首 token·纯前插不回写·
# 插入后批次段裁剪至 12 条+尾注（链长治理落地·历史权威在 CHANGELOG 零信息损失）·去重断言。
_FOOT_RE = re.compile(r"<footer[^>]*>")
_FOOT_TOKEN = re.compile(r"(?:v[\d.]+(?:\s*·\s*)?)?W\d{3,4}")
_FOOT_MAX = 12

def _foot_insert(s_html, new_token):
    f = _FOOT_RE.search(s_html)
    assert f, "未找到 <footer>"
    f_close = s_html.find("</footer>", f.end())
    node_e = f_close if f_close != -1 else len(s_html)
    mm = _FOOT_TOKEN.search(s_html, f.end(), node_e)
    assert mm, "页脚链头 token 未命中（footer 节点全宽）"
    # 链文本节点=token 所在节点（dukou=footer 直后·index 等=footer-meta 内），全程插入前坐标
    n_start = s_html.rfind(">", 0, mm.start()) + 1  # W724 修正：dukou footer 开标签>在 f.end() 前·rfind 须全文件回溯
    n_end = s_html.find("<", mm.start())
    node = s_html[n_start:n_end]
    parts = node.split(" · ")
    first = next(i for i, seg in enumerate(parts) if re.search(r"W\d{3,4}", seg))
    batch = [new_token] + parts[first:]
    if len(batch) > _FOOT_MAX:
        batch = batch[:_FOOT_MAX] + ["…更早批次详见 CHANGELOG.md"]
    elif len(batch) == _FOOT_MAX:
        batch = batch + ["…更早批次详见 CHANGELOG.md"]
    new_node = " · ".join(parts[:first] + batch)
    _wns = re.findall(r"W\d{3,4}", new_node)
    assert len(_wns) == len(set(_wns)), "页脚链 token 重复（W724 防线）"
    return s_html[:n_start] + new_node + s_html[n_start + len(node):]


def _face_footers(ctx):
    """四页脚批次链插入（W717 锚定·W724 双重缺陷根修+链长治理·W781 防御性剥离前导批次号）。"""
    # W781 R-2：desc 以 W### 开头会叠成「W779 W779…」双 token（W779 四页实证·存量缺陷
    # 由 W780 顺修）——插入前无条件剥离，与 release_prep 的 spec 时点校验构成双防线。
    desc = re.sub(r"^W\d{3,4}\s*", "", ctx.desc)
    for p in ["site/index.html", "site/data/cross-time-danmaku.html", "site/data/tag-cloud.html"]:
        s, _ = load(p)
        ctx.pend.append((p, _foot_insert(s, f"{ctx.batch} {desc}"), None))
    p = "site/dukou-engine.html"
    s, _ = load(p)
    head_short = ctx.spec["head_sentence"].split("——")[0]
    ctx.pend.append((p, _foot_insert(s, f"{ctx.batch} {desc}（{head_short}）"), None))


def _agents_entry_wn(part):
    """解析脚注条目批次号（W### 形态）·W721 滚动切分用。"""
    m = re.search(r"（(?:v[\d.]+ )?W(\d{3,4})）", part)
    assert m, "脚注条目批次号解析失败: " + part[:40]
    return int(m.group(1))


def _face_agents(ctx):
    """AGENTS 脚注批次注记 + >5 条滚动迁 ARCHIVE（W721 内建机制）。"""
    # ---------- AGENTS 脚注 ----------
    p = "AGENTS.md"
    s, nl = load(p)
    tail = "。如与上述权威文档冲突，以权威文档为准。*"
    assert s.count(tail) == 1, "AGENTS 脚注尾锚点异常"
    _sep = "" if s[: s.index(tail)].rstrip().endswith("；") else "；"
    s = s.replace(tail, _sep + "{}。如与上述权威文档冲突，以权威文档为准。*".format(ctx.spec["agents_note"].rstrip("。")), 1)  # W972 修：尾句号不剥会拼出「。。」
    # W721 根修（S-29·FAM-14 闭环·W719 R1 制度破约教训）：脚注滚动内建——条目 >5 时最老条迁
    # ARCHIVE 尾块（第 12 面），指针上界同步；制度自此有执行机制，不再依赖手工 trim（W713/W719 两度）。
    _fs = s.find("*本文件由")
    _fline = s[_fs:].split(nl, 1)[0]
    # W964：切分器双日期形态——阿拉伯（20\d\d-\d\d-\d\d）与中文数字（二〇二六年十月二十日）。
    # 病根实证：仅认阿拉伯形态时，52 条中文日期条目黏进相邻条目成 67.1KB 巨段，
    # 切分器恒报 5 条 ⇒ 滚动永不触发（5 不大于 5）⇒「保留最近 5 条」名存实亡。
    _segs = re.split(
        r"；(?=(?:20\d{2}-\d{2}-\d{2}|二〇[一二三四五六七八九〇零十廿卅]+年[一二三四五六七八九〇零十廿卅]+月[一二三四五六七八九〇零十廿卅]+日)[（])",
        _fline)
    assert _fline.rstrip().endswith(tail) and len(_segs) >= 3, "脚注段解析异常（head/pointer/条目）"
    _entries = list(_segs[1:])
    _entries[-1] = _entries[-1][: -len(tail)]
    if len(_entries) > 5:
        _nums = [_agents_entry_wn(x) for x in _entries]
        assert _nums == sorted(_nums), "脚注条目乱序: %s" % _nums
        _overflow = len(_entries) - 5
        _move, _keep = _entries[:_overflow], _entries[_overflow:]
        _lo, _hi = _nums[0], _nums[_overflow - 1]
        # W759 根修：编号空洞（W750 作废·W752/753 由 W751 并行单写）系永久历史，
        # 「+1 连续」断言对每次真实滚动必假阳性（W758 实证）——放松为严格递增：
        # 前序 sorted 断言仍守乱序，本断言拦切分边界重复号（负样本 _w759_negative_check 实测仍红）。
        assert _agents_entry_wn(_keep[0]) > _hi, "滚动切分乱序（_keep 首条未严格大于 _hi——边界重复号或序错）"
        _arc = "archive/docs/AGENTS-ARCHIVE.md"
        _as, _anl = load(_arc)
        if not _as.endswith(_anl):
            _as += _anl
        _as += (
            "以下为 AGENTS.md 版本脚注早期条目（W%d-W%d）段的原文"
            "（单行沿革链·W%d 起级联自动滚动迁入·grep 查勿通读）：%s%s```text%s%s%s```%s"
            % (_lo, _hi, ctx.new_w, _anl, _anl, _anl, "；".join(_move), _anl, _anl)
        )
        ctx.pend.append((_arc, _as, _anl))
        _newline = "；".join([_segs[0].split("；")[0], _segs[0].split("；", 1)[1], *_keep]) + tail
        # 指针上界刷新（W725 单段化·W759 根修：区间注记就地正则替换——旧实现 strip 后按字面锚
        # 「W719 续迁 W708-W714·」回插，而现役脚注前缀已漂移为 W713 形态→回插静默失新；
        # 就地替换 token 保持「仅留最新区间」语义，无 token 时锚「脚注保留最近 5 条」前插）
        _note = "W%d-W%d 级联自动滚动·" % (_lo, _hi)
        if re.search(r"W\d{3,4}-W\d{3,4} 级联自动滚动·", _newline):
            _newline = re.sub(r"(?:W\d{3,4}-W\d{3,4} 级联自动滚动·)+", _note, _newline, count=1)
        else:
            assert "脚注保留最近 5 条" in _newline, "指针注记缺位且无插入锚点"
            _newline = _newline.replace("脚注保留最近 5 条", _note + "脚注保留最近 5 条", 1)
        assert _newline.endswith(tail) and "；".join(_keep) in _newline
        s = s[:_fs] + _newline + s[_fs + len(_fline):]
    ctx.pend.append((p, s, nl))


def _face_citation(ctx):
    """CITATION.cff 版本/日期同步（第 10 面）。"""
    # ---------- CITATION.cff（W628 起第 10 面：version/date-released 随批同步——第 27 门禁 R2 面） ----------
    p = "CITATION.cff"
    s, nl = load(p)
    out = re.sub(r'(?m)^version:\s*"[^"]+"', f'version: "{ctx.batch}"', s, count=1)
    out = re.sub(r'(?m)^date-released:\s*"[^"]+"', f'date-released: "{ctx.date}"', out, count=1)
    assert out != s, "CITATION.cff 版本/日期行未变化"
    ctx.pend.append((p, out, nl))


def _face_file_index(ctx):
    """file-index 最新段插入。"""
    # ---------- file-index ----------
    p = "scripts/output/file-index.md"
    s, nl = load(p)
    mm = re.search(r"## (W\d+) ", s)
    assert mm, "file-index 未找到最新段"
    rows = nl.join(["## {} {}（{}）".format(ctx.batch, re.sub(r"^W\d+\s+", "", ctx.spec["title"].split(" — ")[0].split("（")[0]).strip(), ctx.date),
                    "", "| 文件 | W | 说明 |", "|---|---|---|"] + ctx.spec["file_index_rows"] + ["", ""])
    ctx.pend.append((p, s.replace(mm.group(0), rows + mm.group(0), 1), nl))


def _apply_pend(pend, batch):
    """apply 阶段：统一落盘 + 写级联清单（W560 newline 坑规避）。"""
    # W560 修复：newline 恒为 ""——旧实现对 CRLF 文件传 newline=nl，io 层把 content 中
    # 既有 \r\n 的每个 \n 再翻译一次 → \r 翻倍（实测累计至 4×CR，全页视觉损毁）。
    for path, content, _nl in pend:
        _real = os.path.realpath(os.path.join(ROOT, path))
        if not (_real == _root or _real.startswith(_root + os.sep)):
            raise SystemExit("path escapes project root: %s" % path)
        with open(_real, "w", encoding="utf-8", newline="") as f:
            f.write(content)

    # ---------- 级联落盘清单（W649 防复发：W595/W632/W647 三次 partial commit 漏级联面——
    # 提交时按本清单逐面 git add，杜绝「级联落盘了但没进提交」的检出树≠工作树脱节） ----------
    manifest = f"scripts/output/_cascade_files_{batch}.txt"
    _real_m = os.path.realpath(os.path.join(ROOT, manifest))
    if not (_real_m == _root or _real_m.startswith(_root + os.sep)):
        raise SystemExit("path escapes project root: %s" % manifest)
    with open(_real_m, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(p for p, _, _ in pend) + "\n")
    print(f"[MANIFEST] 级联落盘清单 {len(pend)} 个文件 → {manifest}（提交时按清单 git add；清单本身随批入库）")


def _post_check(pend, batch):
    """写后自检（W560 并入 jiacheck 要点）：CR 串/交接文档结构/头尾链；返回问题清单。"""
    # ---------- 写后自检 + 自愈（W560：并入 _cascade_fix.py 与 jiacheck 要点） ----------
    selfcheck = []
    for path, _, _nl in pend:
        _real = os.path.realpath(os.path.join(ROOT, path))
        data = open(_real, "rb").read()
        if b"\r\r" in data:
            out = []
            for line in data.split(b"\n"):
                out.append(line.rstrip(b"\r") + b"\r" if line else b"")
            data = b"\n".join(out)
            with open(_real, "wb") as f:
                f.write(data)
            selfcheck.append(f"{path}: CR 串已收敛（自愈）")
        if path == "HANDOVER.md":
            txt = data.decode("utf-8")
            sep = "\r\n" if "\r\n" in txt else "\n"
            # W706 结构断言（用户挑刺 P0 实证：头部错位块链+段标题被吞·写后即拦不落脏盘）
            _main = txt.find("# 交接文档")
            if _main == -1 or txt[:_main].strip():
                selfcheck.append("交接文档: 主标题前存在错位内容（结构断言）")
            _z, _y, _e = (txt.find("## ⚠️ 零、当前阻塞"), txt.find("## 一、当前进度"), txt.find("## 二、下一步方向候选清单"))
            if not (-1 < _z < _y < _e):
                selfcheck.append(f"交接文档: 段序破坏（零={_z} 一={_y} 二={_e}）——段标题被吞（结构断言）")
            if not re.search(r"> 历史概要（W\d+ 及更早）的详细记录见", txt):
                selfcheck.append("交接文档: 历史概要指针缺失（结构断言）")
            hl0 = txt.find("> 最后更新：")  # W665 修复：里程碑块置顶后「最后更新」行不再固定在 index 6
            head_line = txt[hl0:txt.find(sep, hl0)] if hl0 != -1 else ""
            head_entries = re.findall(r"(?:v[\d.]+\s+)?(W\d+)", head_line)  # W711 双形态
            if not head_entries or head_entries[0] != batch:
                selfcheck.append(f"交接文档: 头链首条非 {batch}（{head_entries[:3]}）——需人工核查")
            tail_txt = txt[txt.rfind("最后更新："):]
            tail_entries = re.findall(r"(?:v[\d.]+\s+)?(W\d+)", tail_txt)  # W711 双形态
            if tail_txt.count("2026-") > 3 or not tail_entries or tail_entries[0] != batch:
                selfcheck.append(f"交接文档: 尾链异常（{tail_entries[:3]}）——需人工核查")
            if "## 九、使用说明" not in txt:
                selfcheck.append("交接文档: 「九、使用说明」段缺失——需人工核查")
    for line in selfcheck:
        print("[SELF-CHECK]", line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--allow-gap", default="",
                    help="允许的在途缺口 W 号（逗号分隔·须台账有认领行且 CHANGELOG 无段·W895 新增）")
    args = ap.parse_args()
    spec = json.load(open(args.spec, encoding="utf-8"))
    pre_issues = precheck(spec)
    if pre_issues:
        for it in pre_issues:
            print("[PRECHECK-FAIL] " + it)
        print("[PRECHECK] %d 项违例——修正 spec 后重跑（参照 AGENTS §4.3 desc 分隔符规则）" % len(pre_issues))
        return 1
    ctx = _Ctx(spec)
    ctx.allow_gap = [x.strip() for x in args.allow_gap.split(",") if x.strip()]
    assert ctx.entry.endswith("）"), "head_entry 必须以闭合括号结尾"
    assert "（" not in ctx.spec["head_sentence"] and "）" not in ctx.spec["head_sentence"], (
        "head_sentence 禁含全角括号——会破坏下一批「当前 HEAD 句」断言的 [^）]* 匹配（W649 实证：W648 嵌套括号致本批断言 FAIL，交接文档已手工修复）"
    )
    _assert_status_wnum(spec, ctx.batch)  # W956/P-43-05：段状态认领登记 W 号 == 本段号（E-28 防线）
    _face_changelog(ctx)
    _face_three_docs(ctx)
    _face_handover(ctx)
    _face_workflows(ctx)
    _face_footers(ctx)
    _face_agents(ctx)
    _face_citation(ctx)
    _face_file_index(ctx)
    # ---------- 落盘 ----------
    if not args.apply:
        print(f"[DRY-RUN] 10 个面断言与改写全部通过：{ctx.batch}（规则 {ctx.new_rule}）。加 --apply 落盘。")
        return 0
    import cascade_lock  # W991：级联运行锁（①层重启·防并行读中态——W971-W989 混行尾假红族根治）

    _lock_ok, _lock_info = cascade_lock.acquire(ctx.batch, holder="batch_cascade")
    if not _lock_ok:
        import time as _t

        raise AssertionError(
            "级联运行锁被 %s@%s 持有（%.0f 秒）——等级联完成或 scripts/cascade_lock.py --force"
            % (_lock_info.get("holder"), _lock_info.get("batch"),
               _t.time() - _lock_info.get("ts", 0)))
    try:
        _apply_pend(ctx.pend, ctx.batch)
        selfcheck = _post_check(ctx.pend, ctx.batch)
        window_ok = _refresh_window()
        stats_ok = _refresh_stats(ctx.batch)
        _close_hints()
        print(f"[APPLY] 级联完成：{ctx.batch} / {ctx.new_rule}，共 {len(ctx.pend)} 个文件；"
              f"写后自检 {'发现 %d 项' % len(selfcheck) if selfcheck else '全部通过'}；"
              f"回窗 {'OK' if window_ok else 'FAIL'}；stats {'已刷新' if stats_ok else '刷新失败'}")
    finally:
        cascade_lock.release(pid=os.getpid())  # W999 P2-1：pid 匹配才删·防 TTL 夺锁后误删他方新鲜锁
        print("[LOCK] 已释放")
    if not window_ok:
        print("[APPLY] 回窗失败——先修 archive_segments/archive_ledger_rows 再重跑"
              "（否则下一批 preflight 体积窗口必红·开不了工）")
        return 2
    if not stats_ok:
        print("[APPLY] stats 刷新失败——先修 stats.py 再重跑级联（否则 verify 第 31 槽 C5d 必红）")
        return 2
    return 0


# 体积窗口（文档规范 §8·W960 立窗）：CHANGELOG / file-index 各 110 段、台账 60 行。
WIN_SEGMENTS = 110
WIN_LEDGER = 60
_WINDOW_RUNNER = lambda cmd: __import__("subprocess").run(  # noqa: E731 — 单测注入点
    cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def _refresh_window():
    """W1010：级联收尾自动回窗（段滚动归档 + 台账行归档）。

    为什么必须机器做：每批插入一段/一行，正本必然 +1 越过窗口，然后 **下一批开工前**
    才被 preflight 判红拦下——W1008/W1009 两批都是「先超窗、再手工回窗」。人手记的那一步
    迟早漏，且漏了表现为「下一个人开不了工」。级联是唯一知道「段已插入」的时点。
    """
    here = os.path.dirname(os.path.abspath(__file__))
    steps = [
        ("segments", [sys.executable, os.path.join(here, "archive_segments.py"),
                      "--target", "both", "--keep", str(WIN_SEGMENTS), "--apply"]),
        ("ledger", [sys.executable, os.path.join(here, "archive_ledger_rows.py"),
                    "--keep", str(WIN_LEDGER), "--apply"]),
    ]
    ok = True
    for label, cmd in steps:
        r = _WINDOW_RUNNER(cmd)
        tail = [x for x in ((r.stdout or "") + (r.stderr or "")).splitlines() if x.strip()][-1:]
        good = r.returncode == 0
        ok = ok and good
        print("[WINDOW] %-8s %s（%s）" % (label, "OK" if good else "FAIL", " / ".join(tail)))
    return ok


_STATS_RUNNER = lambda cmd: __import__("subprocess").run(  # noqa: E731 — 单测注入点
    cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def _refresh_stats(batch):
    """W1009：级联收尾自动刷 stats（`stats.py --w <num>`）。

    为什么要机器做：C5d（stats 与磁盘实算漂移）在 W1006/W1007/W1008 三批各假红一次，
    每次都要人记得先跑 `stats.py --w ####`——「记得做」迟早漏，且漏了要到 verify 才暴露。
    级联是唯一知道「本批号 + 已落盘」的时点，就在这儿刷。

    失败不静默：打印 FAIL + 末两行输出，并让 main 返回非 0（会话能立刻看到）。
    """
    import subprocess
    num = str(batch).lstrip("W")
    r = _STATS_RUNNER([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "stats.py"),
                       "--w", num])
    tail = [x for x in ((r.stdout or "") + (r.stderr or "")).splitlines() if x.strip()][-2:]
    ok = r.returncode == 0
    print("[STATS] %s（%s）" % ("OK" if ok else "FAIL", " / ".join(tail)))
    return ok


def _close_hints():
    """收官提示位集合（W960 建·W979 扩展·全部只输出不改判定与退出码——W822 语义）。

    - [SIZE]    治理文档体积窗口（判据本体 check_doc_size_budget·开工面硬判据）
                + 超窗提示行（P-44-01：级联每批插入一段·回窗是每批常态动作而非异常）
    - [TMPE]    tmpe 批次桶计数 + _shot/_inbox TTL 超龄报数（P-44-02：删除须主人确认+回收站）
    - [SCRIPTS] scripts 顶层 `_` 件跟踪态计数（P-44-03：>20 提示退役扫描·W977 先例）
    """
    try:
        import check_doc_size_budget as _dsb

        _dsb_counts, _dsb_lines, _dsb_extra = _dsb.collect()
        for _line in _dsb_lines:
            print("[SIZE]", _line)
        _fails = _dsb.evaluate(_dsb_counts)
        if _fails:
            print("[SIZE] 超窗 %d 项——级联每批插入一段属常态·按上行 FAIL 行内指引跑"
                  "对应归档工具回窗（段式=archive_segments.py·台账行=archive_ledger_rows.py）" % len(_fails))
    except Exception as _exc:  # noqa: BLE001 — 提示位故障留痕不阻断
        print(f"[SIZE] 体积提示位不可用（{_exc}）")
    # W976：tmpe 临时区处置提示位（每批收官报一次·防「只进不出」复发——清理闭环
    # 自 W738 建制到 W976 只运转过一次，批次桶 699MB 堆积实证）。判据与工具本体在 tmpe_tidy。
    try:
        import tmpe_tidy as _tt

        _wbuckets = [d for d in os.listdir(_tt.TMPE)
                     if os.path.isdir(os.path.join(_tt.TMPE, d)) and re.match(r"^w\d{3,4}$", d)]
        print("[TMPE] 批次桶 %d 个在 tmpe（政策=批收官经主人确认整桶清·删走回收站）·"
              "沉淀扫描=py -3 scripts/tmpe_tidy.py --tool-candidates" % len(_wbuckets))
        _stale = []
        for _bucket in ("_shot", "_inbox"):
            _ttl = _tt.load_policy().get("ttl_days", {}).get(_bucket)
            if not _ttl:
                continue
            _n = _mb = 0
            for _dp, _dn, _fn in os.walk(os.path.join(_tt.TMPE, _bucket)):
                for _f in _fn:
                    try:
                        _st = os.stat(os.path.join(_dp, _f))
                    except OSError:
                        continue
                    if time.time() - _st.st_mtime > _ttl * 86400:
                        _n += 1
                        _mb += _st.st_size
            _stale.append("%s 超龄 %d 件 %.0fMB(TTL%dd)" % (_bucket, _n, _mb / 1048576, _ttl))
        if _stale:
            print("[TMPE] " + "·".join(_stale) + "——到期列清单经主人确认走回收站"
                  "（tmpe_tidy.py --plan --older N）")
    except Exception as _exc:  # noqa: BLE001 — 提示位故障留痕不阻断
        print(f"[TMPE] 提示位不可用（{_exc}）")
    # P-44-03：scripts 顶层 `_` 件防再积（W977 先例 286 件入库·跟踪态阈值 20）
    try:
        import subprocess as _sp

        _r = _sp.run(["git", "ls-files", "scripts/_*"], capture_output=True, text=True,
                     encoding="utf-8", errors="replace", cwd=ROOT)
        _tracked = len([x for x in _r.stdout.splitlines() if "/" not in x.replace("scripts/", "", 1)])
        _on_disk = len([f for f in os.listdir(os.path.join(ROOT, "scripts"))
                        if f.startswith("_") and os.path.isfile(os.path.join(ROOT, "scripts", f))])
        # W992 口径校准：跟踪数含近批证据锚（CHANGELOG 110 段窗内被引用·合法驻留），
        # 裸计数恒超 20 变常驻噪声——改报「零引用退役候选数」（可行动数）作阈值判据。
        _zero_ref = 0
        try:
            _corpus = ["CHANGELOG.md"]
            for _d in ("tests", "docs/agent", "docs/00-导读"):
                _rr = _sp.run(["git", "-c", "core.quotePath=false", "ls-files", _d],
                              capture_output=True, text=True,
                              encoding="utf-8", errors="replace", cwd=ROOT)
                _corpus.extend(x for x in _rr.stdout.splitlines() if x.strip())
            _texts = {}
            for _c in _corpus:
                try:
                    _texts[_c] = open(os.path.join(ROOT, _c.replace("/", os.sep)),
                                      encoding="utf-8", errors="ignore").read()
                except OSError:
                    pass
            _cl_tail = _texts.get("CHANGELOG.md", "")[-200000:]
            for _f in _r.stdout.splitlines():
                _name = _f.replace("scripts/", "", 1)
                if not _name.startswith("_"):
                    continue
                if _name in _cl_tail or any(_name in _tx for _tx in _texts.values()):
                    continue
                _zero_ref += 1
        except Exception:
            _zero_ref = -1
        _msg = "[SCRIPTS] 顶层 `_` 件跟踪态 %d 个（盘上 %d）·零引用退役候选 %s 个" % (
            _tracked, _on_disk, _zero_ref)
        if _zero_ref > 20:
            _msg += "——超阈值 20：跑退役扫描（archive_file.py 语料级引用剔除·W977/W992 先例）"
        print(_msg)
    except Exception as _exc:  # noqa: BLE001 — 提示位故障留痕不阻断
        print(f"[SCRIPTS] 提示位不可用（{_exc}）")
    # W995：归档健康提示位（check_archive_health T1-T4·独立尾部块——与 W992 校准块最小碰撞面）
    try:
        import check_archive_health as _cah

        _cah.run(strict=False, prefix="[ARCHIVE] ")
    except Exception as _exc:  # noqa: BLE001 — 提示位故障留痕不阻断
        print(f"[ARCHIVE] 提示位不可用（{_exc}）")
    # W995：tmpe 上次清理活动日期（.journal 最新落笔——清理节奏可见性，建制 13 天才首清的教训）
    try:
        import datetime as _dt

        _jdir = os.path.join(_tt.TMPE, ".journal")
        _journals = [os.path.join(_jdir, f) for f in os.listdir(_jdir)] if os.path.isdir(_jdir) else []
        if _journals:
            _last = max(os.path.getmtime(j) for j in _journals)
            print("[TMPE] 上次清理活动 %s（%.0f 天前·journal %d 份）"
                  % (_dt.date.fromtimestamp(_last), (time.time() - _last) / 86400, len(_journals)))
    except Exception as _exc:  # noqa: BLE001 — 提示位故障留痕不阻断
        print(f"[TMPE] 日期提示不可用（{_exc}）")


if __name__ == "__main__":
    sys.exit(main())

# spec 字段说明：
# batch/version/date/title/desc/head_entry/head_sentence/changelog_body/milestone_block/agents_note/file_index_rows
# 注意：head_entry 为交接文档头尾链条目全文（以 ） 结尾，不带分隔符）；
#       changelog_body 以两个换行开头；milestone_block 多行以 \n 分隔（脚本会按文件行尾归一）。
