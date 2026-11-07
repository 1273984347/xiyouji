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

import cascade_idempotence as ci  # W1122：级联插入型面的幂等原语（单一事实源）
import version_surface  # W1114：版本面字面量的共享单一事实源（只引用不复制）

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
    # W1019 硬守卫：段正文必须以空行开场。病根：级联把标题行与 changelog_body 直接拼接，
    # body 若无前导空行 ⇒ 新段标题行与「> **来源**」挤在同一行（与既有段形态不符·只能
    # 段内定向订正，级联不可重跑 E-17）。W1018 spec 实测以 \n\n\n\n 开场，本批漏写即粘连。
    if not str(spec.get("changelog_body", "")).startswith("\n\n"):
        issues.append("spec.changelog_body 未以空行（\\n\\n）开场（级联会把段标题行与正文粘成同一行·"
                      "W1019 实证·首元素前必须留空行）")
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
    # W1137 口径对齐根修（铁律 15）：写入侧 AGENTS 条目 = note + 「。」+ 固定尾句家具，而体积门禁
    # check_doc_size_budget.check_footnote_shape 量的是**剥家具后含尾句「。」拼装**的条目本体
    # ——W1137 实证 note=119 过本守卫、拼装后 139 过不了门禁（本地绿 CI 红）。预检改与门禁
    # 同源计量（单一事实源·只引用不复制），note 预算随拼装开销自动收紧。
    try:
        from check_doc_size_budget import check_footnote_shape
        _probe = _note.rstrip("。") + "。" + _AGENTS_TAIL.lstrip("。")
        _bad = check_footnote_shape("；2026-11-05（W0000）占位；" + _probe)
        if _bad:
            issues.append("spec.agents_note 拼装后 %s（门禁 check_footnote_shape 同源计量·"
                          "预算 = 120 − 固定尾句家具与尾句号开销）" % _bad[0])
    except ImportError:
        pass  # 判据模块缺失时退回上行 len 守卫（不静默放行超长·上守卫仍在）
    # W1016 硬守卫：desc / head_sentence 禁裸聚合数字（`N 项/篇/页/个/类`）。
    # 病根：两字段逐字写入 README/STRUCTURE/项目说明的**版本抬头行**，而第 31 门禁 C5c
    # 对抬头行也查裸聚合数字（`<!--doc-sync:exempt-->` 在行尾、不紧跟命中 ⇒ 后置豁免不命中）
    # ⇒ 落盘后必然 C5c 判红，只能段内定向订正（级联不可重跑·E-17）。W1014 实测连撞 4 次
    # （「15 项真缺陷」四处抬头行全红）。前置拦截成本≈0，故升硬守卫。
    for field in ("desc", "head_sentence"):
        _hit = re.findall(r"\d+\s*(?:项|篇|页|个|类)", str(spec.get(field, "")))
        if _hit:
            issues.append("spec.%s 含裸聚合数字 %s（会写入版本抬头行 ⇒ 第 31 门禁 C5c 必红·"
                          "改无量词表达如「一批真缺陷」或加实体标记）" % (field, _hit))
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
        # W1114：head_sentence 提升为 ctx 字段（不再让面函数直接摸 ctx.spec）——
        # 判据 scripts/check_cascade_line_anchor.py 的 _Ctx 替身只带最小字段集，
        # 面函数若新增对 ctx.spec 的直读 ⇒ 替身缺 spec ⇒ AttributeError ⇒ 判据整体失效。
        self.head_sentence = spec.get("head_sentence", "")
        self.new_w = None     # CHANGELOG 面回填：现役段号 + 1
        self.new_rule = None  # CHANGELOG 面回填：编号规则段新形态
        self.pend = []        # (path, content, nl) 落盘队列
        self.cl_src = ""      # CHANGELOG 原文（交接文档面 W534 断言用）


def _locate_cl_section(s, batch):
    """定位 CHANGELOG 里本批号已立段的区间（起点=段标题行首·终点=下一段标题行首）。

    W1122（根修 W1117 R-01）：级联插入型面的幂等定位器。
    """
    m = re.search(r"^### %s（[^\n]*" % re.escape(batch), s, re.M)
    if not m:
        return None
    start = m.start()
    nxt = re.search(r"^### ", s[m.end():], re.M)
    end = m.end() + nxt.start() if nxt else len(s)
    return start, end


def _handover_progress_bounds(s):
    """交接文档「一、当前进度」段的区间（起点=段标题行首·终点=下一 '## ' 章节标题行首）。

    W1122（根修 W1117 R-02）：块区间必须**有界于进度段**——原实现对链尾块返回
    end=len(s) ⇒ 「不一致替换」会把进度段之后的全部文档内容吞掉。
    """
    h = s.find("## 一、当前进度")
    if h == -1:
        return None
    nxt = re.search(r"^## ", s[h + 1:], re.M)
    end = h + 1 + nxt.start() if nxt else len(s)
    return h, end


def _handover_milestone_blocks(s):
    """交接文档「一、当前进度」段内的里程碑块链（文档序·区间有界）。

    W1122（根修 W1117 R-02）：里程碑块链是**按批号降序**（最新在前）的有序面，
    低号批落段不得占链首（第 31 门禁 C2「交接头链链首 ≡ CHANGELOG 顶段」判红）。
    返回 [(批号:int, 起点:int, 终点:int), ...]：
      · 块终点 = 下一块起点；
      · 链尾块终点 = 进度段内「历史概要」指针行首（若有）或进度段末（**不越段**）。
    """
    bounds = _handover_progress_bounds(s)
    if bounds is None:
        return []
    h, end = bounds
    seg = s[h:end]
    heads = list(re.finditer(r"^- \*\*(?:v[\d.]+ )?(W\d+)\b", seg, re.M))
    blocks = []
    for i, m in enumerate(heads):
        st = h + m.start()
        if i + 1 < len(heads):
            en = h + heads[i + 1].start()
        else:
            pm = re.search(r"^> 历史概要（W\d+ 及更早）的详细记录见", seg[m.end():], re.M)
            en = h + m.end() + pm.start() if pm else end
        blocks.append((int(m.group(1)[1:]), st, en))
    return blocks


def _locate_handover_milestone(s, batch):
    """定位交接文档「一、当前进度」段内本批号里程碑块的区间（有界）。

    W1122（根修 W1117 R-01 + R-02）：级联插入型面的幂等定位器；
    区间**有界于进度段**（原实现对链尾块返回 end=len(s) ⇒ 替换时会吞掉后文）。
    """
    bn = int(re.sub(r"\D", "", batch))
    for num, st, en in _handover_milestone_blocks(s):
        if num == bn:
            return st, en
    return None


def _face_changelog(ctx):
    """CHANGELOG 面：插入新段并推进编号规则（回填 ctx.new_w/new_rule/cl_src）。"""
    # ---------- CHANGELOG ----------
    p = "CHANGELOG.md"
    s, nl = load(p)
    ctx.cl_src = s  # W713：保留 CHANGELOG 原文，供交接里程碑淘汰前断言（W534 承诺）
    # W1122：记录 CHANGELOG **现役顶段号**（低号批落段时交接面不得回退现役单点·现役面只指最高号批）
    ctx.cur_w = None  # 由下方 cur_w 解析后回填
    # W711 方案 D 双形态：历史段 ### vX.Y.Z（date）：W### / 新段 ### W###（date）：标题
    m = re.search(r"^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（[^）]*）：)", s, re.M)
    assert m, "CHANGELOG 未找到现役段"
    cur_anchor = m.group(0)
    cur_w = int(m.group(1) or m.group(2))
    ctx.cur_w = cur_w  # W1122：现役顶段号（低号批守卫用）
    # W895：显式缺口许可（并行在途批的现实）——--allow-gap 列出的 W 号须在台账有认领行、
    # 且在 CHANGELOG 尚无段（其落段自理：晚到者用 backfill_changelog.py 按号序补）。
    gaps = getattr(ctx, "allow_gap", [])
    if gaps:
        ledger = open(os.path.join(ROOT, "docs", "00-导读", "W批次编号对账表.md"), encoding="utf-8").read()
        for g in gaps:
            # W1047 修：台账登记行的实际形态是 `| W1046 |`（**带 W 前缀**），
            # 原断言查 `| 1046 ` ⇒ 缺口许可机制**从未真正可用过**（每次都断言失败）。
            # ⇒ 改为兼容两种形态：`| 1046 ` 或 `| W1046 `。
            assert re.search(rf"^\|\s*W?{re.escape(g)}\s", ledger, re.M), (
                f"缺口 {g} 在台账无认领行（台账登记行形态应为「| W{g} |」）")
            assert f"### {g}" not in s, f"缺口 {g} 已有段（无需允许）"
        print("  缺口许可：%s（在途·台账已有认领行）" % "、".join(gaps))
    # W1122（根修 W1117 R-01「段插入仍非幂等」）：本批段**已存在** ⇒ 不重复插入。
    # 原语义是「段已存在即断言失败」⇒ 落段后无法重跑级联；且「批次号=顶段+1」的强断言
    # 在**降序位补段**（我方 W1120 的形态）下必然失败 ⇒ 本批已立段时走幂等分支。
    # 内容不一致 ⇒ fail-closed 并指引用 scripts/rebuild_section.py 重建（与 file-index 面同策略）。
    _cspan = _locate_cl_section(s, ctx.batch)
    if _cspan is not None:
        _title_body = re.sub(r"^W\d+\s+", "", ctx.spec["title"]).strip()
        _new_title = f"### {ctx.batch}（{ctx.date}）：{_title_body}"
        _expected = _new_title + ctx.spec["changelog_body"].replace("\n", nl) + nl
        _old = s[_cspan[0]:_cspan[1]]
        if _old.replace("\r\n", "\n").strip() != _expected.replace("\r\n", "\n").strip():
            raise AssertionError(
                "CHANGELOG 已存在 %s 段但内容与 spec 不一致 ⇒ 拒绝重复插入"
                "（防同号双段·不静默留 stale）——修法=跑 py -3 scripts/rebuild_section.py"
                " --batch %s --spec <spec 路径> --apply 重建该段" % (ctx.batch, ctx.batch))
        ctx.new_w = int(str(ctx.batch).lstrip("Ww"))
        ctx.new_rule = "（W001-W%d）" % ctx.new_w
        out, _rule_changed = version_surface.advance_changelog_rule(s, ctx.batch)
        ctx.pend.append((p, out, nl))
        print("[CHANGELOG] %s 段已存在且内容一致 ⇒ 幂等跳过插入（不产生同号双段）" % ctx.batch)
        return
    new_w = cur_w + 1 + len(gaps)
    ctx.new_w = new_w
    assert ctx.batch == "W" + str(new_w), f"批次号应为 W{new_w}" + (f"（含缺口 {gaps}）" if gaps else "")
    assert ("### " + ctx.batch) not in s, ctx.batch + " 段已存在"
    old_rule, new_rule = f"（W001-W{cur_w}）", f"（W001-W{new_w}）"
    ctx.new_rule = new_rule
    # W712：cur_anchor 改行首锚定——段 body 内的形态示例引用（反引号内·非行首）不再使计数爆炸
    # W1137 续跑容忍：收官链 versions 步同为幂等版本面——乱序（先 closeout 后 cascade）时规则行
    # 已被提前推进到本批号 ⇒ old 0 次 / new 恰 1 次，跳过锚点断言继续（尾部 advance 幂等归零）；
    # 其余形态（old≠1 或 new 重复）仍 fail-closed，断言强度不降。
    if not (s.count(old_rule) == 0 and s.count(new_rule) == 1):
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
    # 规则段上限属**版本面字面量**（W1117：跨文件字面量面）⇒ 改调共享模块
    # （单一事实源·只引用不复制·幂等）——原先在此处就地 replace 属段面耦合。
    out, _rule_changed = version_surface.advance_changelog_rule(out, ctx.batch)
    assert out.count(new_title) == 1 and out.count(new_rule) == 1
    ctx.pend.append((p, out, nl))


def _face_three_docs(ctx):
    """README / STRUCTURE / 项目说明 三文档批头版本行。

    **W1114 改为调用共享模块 scripts/version_surface.py**（只引用不复制·避免两份实现漂移）：
    版本面字面量推进由 version_surface 承担（幂等·已是目标态则零变化·锚点缺失 fail-closed）。
    """
    # ---------- README / STRUCTURE / 项目说明 ----------
    for rel in ("README.md", "STRUCTURE.md", "docs/00-导读/项目说明.md"):
        # 用**本模块的 load** 读文件 + 把文本交给 version_surface 的纯函数 advance_text：
        # 判据 check_cascade_line_anchor.py 才能 monkeypatch 本模块 load 注入合成样本
        # （若版本面模块自己读盘，判据会读到磁盘真实文件 ⇒ 合成样本驱动失效）。
        s, nl = load(rel)
        out, _changed = version_surface.advance_text(
            s, rel, ctx.batch, ctx.date, ctx.desc, ctx.head_sentence)
        ctx.pend.append((rel, out, nl))


def _handover_rotate_oldest(s, ctx, nl, h1pos):
    """交接文档：滚动淘汰最老里程碑块并同步「历史概要」指针（W534/W624/W713 语义）。

    W1124（T74 R-C）：**滚动幂等守卫下沉到函数内**——病根是守卫此前只在调用点
    （插入路径）生效 ⇒ 若单独重跑滚动逻辑，仍会再淘汰一块（指针指向的块被淘汰后
    指针移到新最老块 ⇒ 再跑一次就再淘汰一块 ⇒ 信息丢失·零红灯）。
    ⇒ 本版：本批块**已存在于链上** ⇒ 视为本批已滚动过 ⇒ 直接返回（零变化）。
    """
    if _locate_handover_milestone(s, ctx.batch) is not None:
        # W1144 根修（P1-1 复发真根因·W1142/W1144 两批连续实证 7>6）：W1124 幂等守卫与
        # 插入路径 rotate 序列自相矛盾——本批块刚被 upsert 进链，locate 恒命中 ⇒ rotate
        # 恒零变化 ⇒ 概要块只增不减。守卫改为「本批在链上 **且** 窗口未超限（≤6）」：
        # 超限 = 本批插入后未滚（补救路径·继续往下滚）；未超限的重跑场景维持零变化
        # （W1124 防「单独重跑再淘汰一块」语义保留）。
        _win_blocks = [b for b in re.finditer(r"- \*\*(?:v[\d.]+ )?(W\d+)[^*]*\*+[^\r\n:*]{0,30}：", s)
                       if h1pos < b.start() < s.find("## 二、", h1pos)]
        if len(_win_blocks) <= 6:
            return s
    pm = re.search(r"> 历史概要（W(\d+) 及更早）的详细记录见", s)
    assert pm, "未找到历史概要指针"
    # W1144 根修：淘汰目标 = 进度段有界窗口内 **min 批号块**——块形态用与门禁 C7 同口径
    # 的严格正则（`**：` 尾约束·_handover_milestone_blocks 是宽松定位器会把进度段内
    # 非 milestone bullet 一并计入（实测 19 vs 7）→ min 漂移误拦）；不再按指针号全文匹配。
    # 指针在淘汰后统一改指新最老（W713 旋转语义·自愈式归位）。
    _bounds = _handover_progress_bounds(s)
    assert _bounds, "未找到「一、当前进度」段"
    _seg = s[_bounds[0]:_bounds[1]]
    _mb = [(int(m.group(1)), _bounds[0] + m.start()) for m in
           re.finditer(r"^- \*\*(?:v[\d.]+ )?W(\d+)[^*]*\*+[^\r\n:*]{0,30}：", _seg, re.M)]
    assert len(_mb) >= 2, "里程碑窗口不足 2 块（W913：无盈可滚）"
    _min_num = min(x[0] for x in _mb)
    oldest_w = "W%d" % _min_num
    tgt = [st for num, st in _mb if num == _min_num]
    blocks_all = _mb
    # W913：窗口不足 2 块不滚动（契约「只留最近 5 版」——不足时无盈可滚；原无条件滚动在
    # 单块窗口必致空窗异常·阻断后续一切级联·W912/W913 两批连续实证）
    if len(blocks_all) < 2:
        return s
    bm_start = tgt[0]
    # W1144：tgt 取自有界窗口（_handover_milestone_blocks·恒在进度段内），跨段断言随之
    # 保留为双保险（W705 教训：跨段整块淘汰会吞掉段标题）。
    assert bm_start > h1pos, (
        f"最老里程碑块 {oldest_w} 不在「一、当前进度」段内（W705 教训：跨段整块淘汰会吞掉段标题）"
    )
    eidx = s.find(f"> 历史概要（W{_min_num} 及更早）的详细记录见", bm_start)
    assert eidx != -1, (
        "W1144 自愈语义：指针未指窗口最老块（旧指针 W%s）——淘汰后 replace 需旧行在位；"
        "此形态说明指针曾指向更老已滚块，先归位指针再级联" % pm.group(1)
    )
    # W534 承诺恢复（W713）：淘汰前断言该批详细记录已入 CHANGELOG 段（信息零丢失）
    # W1144：oldest_w 已是 "W1127" 带前缀形态——rf 内不再重复加 W（双 W 曾使断言恒假）
    assert re.search(rf"^### (?:v[\d.]+（[^）]*）：{oldest_w}\b|{oldest_w}（[^）]*）：)", ctx.cl_src, re.M), (
        f"CHANGELOG 无 {oldest_w} 段（W534 契约：删前逐批断言 CHANGELOG 有段）"
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
    # W1144 修：捕获组移到 W 之后（原 (W\d+) 使 int('W1144') 炸——rotate 恒早退从未触达的潜伏炸点）
    _remain = [int(x) for x in re.findall(r"- \*\*(?:v[\d.]+ )?W(\d+)[^*]*\*+[^\r\n:*]{0,30}：", _win)]
    assert _remain, "淘汰后里程碑窗口为空（异常）"
    # W1144：oldest_w 已含 W 前缀——f 串不再重复加 W（双 W 曾使 replace 恒不命中·指针不随淘汰同步）
    s = s.replace(f"> 历史概要（{oldest_w} 及更早）的详细记录见",
                  f"> 历史概要（W{min(_remain)} 及更早）的详细记录见", 1)
    return s


def _upsert_chain_entry(chain, entry, batch, sep):
    """「最后更新」链**内容**（不含锚点）的幂等 upsert（最新在前·按批号序）。

    W1122（根修 W1117 R-01 + 低号批落段）：链式面此前**各自判定「已存在」**且判定方式错误
    （尾链切窗少算了锚点长度 ⇒ 恒判「不存在」⇒ 每次重跑都前置一条 ⇒ 重复累积且占链首）。
    本函数为头链与尾链的**单一事实源**：
      · 本批 entry 不存在 ⇒ 按批号序插入（链首批次 > 本批 ⇒ 插到链首之后）
      · 已存在且内容一致 ⇒ 零变化；若**占链首而链首更新** ⇒ 重排到按序位
      · 已存在但内容不一致 ⇒ 替换
    返回 (新链内容, 状态)；状态 ∈ inserted / unchanged / moved / replaced
    """
    bn = int(re.sub(r"\D", "", batch))
    nums = [int(m.group(1)) for m in re.finditer(r"（(?:v[\d.]+ )?W(\d{3,4})[^）]*）", chain)]
    first_num = nums[0] if nums else None
    first_re = re.compile(r"20\d{2}-\d{2}-\d{2}（(?:v[\d.]+ )?W(\d{3,4})[^）]*）")
    mi = re.search(re.escape(entry), chain)
    if mi is not None:
        if chain[mi.start():mi.end()].strip() != entry.strip():
            return chain[:mi.start()] + entry + chain[mi.end():], "replaced"
        fe = first_re.search(chain)
        # 位置校正：本批 entry 占链首、而链上存在**更高号批次** ⇒ 移到按序位
        _higher = [x for x in nums if x > bn]
        if fe is not None and _higher and mi.start() <= fe.start():
            e = mi.group(0)
            rest = (chain[:mi.start()] + chain[mi.end():]).replace(sep + sep, sep)
            fe2 = first_re.search(rest)
            if fe2 is None:
                return chain, "unchanged"
            pos = fe2.end()
            return rest[:pos] + sep + e + rest[pos:], "moved"
        return chain, "unchanged"
    fe = first_re.search(chain)
    if first_num is not None and first_num > bn and fe is not None:
        pos = fe.end()
        return chain[:pos] + sep + entry + chain[pos:], "inserted"
    return entry + sep + chain, "inserted"


def _upsert_handover_milestone(s, build, batch, nl):
    """交接文档「一、当前进度」里程碑块的幂等 upsert（按批号序·最新在前）。

    W1122（根修 W1117 R-02 + 低号批落段）：里程碑块此前**无条件插到链首** ⇒
    低号批（W1122 < 现役 W1123）占据链首 ⇒ 第 31 门禁 C2
    「交接文档头链链首 ≡ CHANGELOG 顶段」判红（本地与 CI 同红·真红非分歧）。
    本函数为里程碑块的**单一事实源**（与头尾链 _upsert_chain_entry 同族语义）：
      · 不存在 ⇒ 按批号序插入（插到链上第一个更小号块之前；无更小号 ⇒ 插到链尾）
      · 已存在且一致 ⇒ 零变化；占链首而链上有更高号 ⇒ 移到按序位（moved）
      · 已存在但不一致 ⇒ 替换（区间有界于进度段·不吞后文）
    返回 (新 s, 状态)；状态取值 inserted / unchanged / moved / replaced。
    """
    bn = int(re.sub(r"\D", "", batch))
    blocks = _handover_milestone_blocks(s)
    mspan = _locate_handover_milestone(s, batch)
    if mspan is None:
        lower = [b for b in blocks if b[0] < bn]
        if lower:
            pos = lower[0][1]
        else:
            bounds = _handover_progress_bounds(s)
            pos = blocks[-1][2] if blocks else (bounds[1] if bounds else len(s))
            if pos > 0 and not s[:pos].endswith(nl):
                s = s[:pos] + nl + s[pos:]
                pos += len(nl)
        return s[:pos] + build + s[pos:], "inserted"
    cur = s[mspan[0]:mspan[1]]
    if cur.strip() != build.strip():
        return s[:mspan[0]] + build + s[mspan[1]:], "replaced"
    others = [b for b in blocks if b[0] != bn]
    higher = [b for b in others if b[0] > bn]
    if blocks and blocks[0][0] == bn and higher:
        rest = s[:mspan[0]] + s[mspan[1]:]
        blocks2 = _handover_milestone_blocks(rest)
        lower2 = [b for b in blocks2 if b[0] < bn]
        if lower2:
            pos = lower2[0][1]
        else:
            pos = blocks2[-1][2] if blocks2 else mspan[0]
        return rest[:pos] + cur + rest[pos:], "moved"
    return s, "unchanged"


def _face_handover(ctx):
    """交接文档面：头尾链/进度标题/里程碑块/HEAD 句全量改写与结构断言。"""
    # ---------- 交接文档 ----------
    p = "HANDOVER.md"
    s, nl = load(p)
    assert s.count("））；") == 0, "基线已存在双括号，先人工处理"
    # W1122（根修 W1117 R-01 + 低号批落段）：头链 entry 此前**无条件 prepend** ⇒ 重跑级联静默重复；
    # 且低号批会占据链首（登记面一致性闸要求「链首 ≡ CHANGELOG 现役段」）⇒ 改为统一幂等 upsert
    # （_upsert_chain_entry 为头链与尾链的单一事实源·含位置校正）。
    _hanchor = "> 最后更新："
    _h0x = s.find(_hanchor)
    _h1x = s.find(nl, _h0x) if _h0x != -1 else -1
    assert _h0x != -1 and _h1x != -1, "未找到交接文档头链行"
    _hchain, _hst = _upsert_chain_entry(s[_h0x + len(_hanchor):_h1x], ctx.entry, ctx.batch, "·")
    if _hst != "unchanged":
        print("[HANDOVER] 头链 entry：%s" % _hst)
    s = s[:_h0x + len(_hanchor)] + _hchain + s[_h1x:]
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
    # W1122：**低号批不得回退现役单点**（历史版本面不可回退）——现役面只指最高号批。
    _cur_w = getattr(ctx, "cur_w", None)
    _is_current = (_cur_w is None) or (int(str(ctx.batch).lstrip("Ww")) >= int(_cur_w))
    if _is_current:
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
    # W1122（根修 W1117 R-02）：不再以「链首块行首」为插入点——低号批落段会占据链首
    # （第 31 门禁 C2「交接文档头链链首 ≡ CHANGELOG 顶段」判红·本地与 CI 同红）；
    # 插入位改由 _upsert_handover_milestone 按批号序判定（含位置校正）。
    # W1122（根修 W1117 R-01）：里程碑块此前**无条件插入** ⇒ 重跑级联静默重复插块；
    # 且里程碑滚动（淘汰最老块）是**有状态**的 ⇒ 重跑会再淘汰一块（信息丢失）。
    # 本版：本批块已存在 ⇒ 只做「一致则零变化·不一致则替换」；**跳过滚动**（滚动已在首次执行时完成）。
    # W1122（根修 W1117 R-01 + R-02）：里程碑块此前**无条件插入** ⇒ 重跑级联静默重复插块；
    # 且里程碑滚动（淘汰最老块）是**有状态**的 ⇒ 重跑会再淘汰一块（信息丢失）。
    # 本版：统一走单一事实源 _upsert_handover_milestone（按批号序·含位置校正）；
    # **仅首次插入**才执行滚动（滚动已在首次执行时完成）。
    _mbuild = ctx.spec["milestone_block"].replace("\n", nl) + nl
    s, _mst = _upsert_handover_milestone(s, _mbuild, ctx.batch, nl)
    if _mst != "unchanged":
        print("[HANDOVER] 里程碑块：%s" % _mst)
    if _mst == "inserted":
        s = _handover_rotate_oldest(s, ctx, nl, h1pos)
    hs = re.search(r"当前 HEAD = (?:v[\d.]+ )?W\d+（[^）]*；详见 CHANGELOG）", s)
    assert hs, "未找到当前 HEAD 句"
    if _is_current:  # W1122：低号批不改现役 HEAD 句（现役面只指最高号批）
        s = s[:hs.start()] + "当前 HEAD = {}（{}；详见 CHANGELOG）".format(ctx.batch, ctx.spec["head_sentence"]) + s[hs.end():]
    # W560 修复：尾链 prepend 必须锚定文末行（旧实现 s.replace("最后更新：", ..., 1) 命中的是
    # 头链首处 → 头链 entry 双写「E；E·」，W556/W557/W558 三批实证）。改用 rfind 定位文末行。
    tail_idx = s.rfind("最后更新：")
    assert tail_idx != -1, "未找到文末「最后更新」历史链"
    # W1122：尾链的「已存在」判定此前切窗少算锚点长度 ⇒ 恒判「不存在」⇒ 每次重跑都前置一条
    # ⇒ 重复累积且占链首。改走同一幂等 upsert 原语（单一事实源）。
    _tanchor = "最后更新："
    _tline_end = s.find(nl, tail_idx)
    _tchain, _tst = _upsert_chain_entry(s[tail_idx + len(_tanchor):_tline_end], ctx.entry, ctx.batch, "；")
    if _tst != "unchanged":
        print("[HANDOVER] 尾链 entry：%s" % _tst)
    s = s[:tail_idx + len(_tanchor)] + _tchain + s[_tline_end:]
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
    """workflows README 头部区间与里程碑尾标记。

    **W1114**：头部区间（两处「W450-W####」）改由共享模块 version_surface 推进（幂等）；
    里程碑尾标记是**追加型**内容（每批加一条），仍由本面负责（不属版本面字面量）。
    **W1157 有界化根修**：里程碑尾标记原追加在 README 门禁体系区间行尾 ⇒ 单行无限累计
    （实测 27KB 撑爆文件体积，本批已把累计历史拆往归档件）。改为双面——README 保留
    **有界区间行**（区间号仍由 version_surface 推进·锚点不变故 test_w1114/w1117 语义
    零变化），逐批明细行改追加 `archive/docs/workflows-readme-history.md`（归档件
    只增不删·语义合规·台账已登记）。
    """
    # ---------- workflows README（有界区间行） ----------
    p = ".github/workflows/README.md"
    s, nl = load(p)
    out, _changed = version_surface.advance_text(
        s, p, ctx.batch, ctx.date, ctx.desc, ctx.head_sentence)
    ctx.pend.append((p, out, nl))
    # ---------- 逐批明细追加面（归档件·行制） ----------
    ap = "archive/docs/workflows-readme-history.md"
    s_arch, nl_arch = load(ap)
    _line = f"+ W{ctx.new_w} {ctx.desc}·无 workflow 结构改动）。"
    lines = s_arch.splitlines(keepends=True)
    idx = next((i for i, ln in enumerate(lines)
                if ln.strip().startswith(f"+ W{ctx.new_w} ")), None)
    if idx is not None:
        # W1122 同款幂等：已存在本批行 ⇒ 内容一致则零变化·不一致则替换
        if lines[idx].strip() != _line.strip():
            lines[idx] = _line + ("\n" if lines[idx].endswith("\n") else "")
    else:
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        lines.append(_line + "\n")
    s_arch = "".join(lines)
    ctx.pend.append((ap, s_arch, nl_arch))


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


def _foot_upsert(s_html, new_token, batch):
    """页脚批次链插入的**幂等版**（W1122 · 根修 W1117 R-01）。

    原 _foot_insert 无条件前插 ⇒ 重跑级联会插出**同号双 token**（被 W724 去重断言拦下·fail-closed）。
    本版：链节点内已有本批号 token ⇒ 内容一致则**零变化**·不一致则**替换该段**。
    """
    f = _FOOT_RE.search(s_html)
    assert f, "未找到 <footer>"
    f_close = s_html.find("</footer>", f.end())
    node_e = f_close if f_close != -1 else len(s_html)
    mm = _FOOT_TOKEN.search(s_html, f.end(), node_e)
    assert mm, "页脚链头 token 未命中（footer 节点全宽）"
    n_start = s_html.rfind(">", 0, mm.start()) + 1
    n_end = s_html.find("<", mm.start())
    node = s_html[n_start:n_end]
    parts = node.split(" · ")
    _bnum = int(re.sub(r"\D", "", batch))
    for i, seg in enumerate(parts):
        if re.search(r"\bW%d\b" % _bnum, seg):
            new_parts = list(parts)
            new_parts[i] = new_token
            new_node = " · ".join(new_parts)
            _wns = re.findall(r"W\d{3,4}", new_node)
            assert len(_wns) == len(set(_wns)), "页脚链 token 重复（W724 防线）"
            if new_node == node:
                return s_html
            return s_html[:n_start] + new_node + s_html[n_start + len(node):]
    return _foot_insert(s_html, new_token)


def _face_footers(ctx):
    """四页脚批次链插入（W717 锚定·W724 双重缺陷根修+链长治理·W1137 短令牌根修）。

    W1137（R-02 访客页脚去工程化·用户 2026-11-05 批准）：页脚链只写 W 号短令牌——
    批次描述的访客可见面曾达 ~1650 字/页（W926 R-02 P0「信任损失」），
    权威载体恒为 CHANGELOG，desc/head_sentence 不再进页脚。
    本批随附一次性存量清理（index/danmaku/tag-cloud/dukou 四页链段裁剪为纯令牌）。
    """
    for p in ["site/index.html", "site/data/cross-time-danmaku.html", "site/data/tag-cloud.html",
              "site/dukou-engine.html"]:
        s, _ = load(p)
        ctx.pend.append((p, _foot_upsert(s, ctx.batch, ctx.batch), None))


_AGENTS_TAIL = "。如与上述权威文档冲突，以权威文档为准。*"


_AGENTS_ENTRY_TOKEN_RE = re.compile(
    r"(?:20\d{2}-\d{2}-\d{2}|二〇[一二三四五六七八九〇零十廿卅]+年"
    r"[一二三四五六七八九〇零十廿卅]+月[一二三四五六七八九〇零十廿卅]+日)"
    r"（(?:v[\d.]+ )?W(\d{3,4})）"
)


def _locate_agents_note(s, batch):
    """定位 AGENTS 脚注行内**本批号条目**的区间（列表·按出现顺序）。

    W1122（根修 W1117 R-01 + R-03）：
      · 原实现按**全文首个** `（W###）` 定位 ⇒ 正文提及批号时会误定位到非脚注位置。
      · 原实现用「下一个『；』」界定条目终点 ⇒ **条目正文本身含分号时区间被截断**
        （实证 W1122 条目含「只补真缺的那一面；顺带回填…」⇒ 终点落在内部分号）
        ⇒ 每次重跑判定「内容不一致」⇒ 替换 ⇒ 残留尾巴 ⇒ **同号条目无限累积**
        （PR #130 实测脚注里累积到 4 份）。
      · 本版：限定在脚注行（`*本文件由` 之后）内查找；按**下一个条目 token** 定界
        （条目正文可含任意分号）；返回**全部**同号副本（供去重）。
    返回 [(start, end), ...]；无则 []。
    """
    _fs = s.find("*本文件由")
    if _fs == -1:
        return []
    _bnum = str(batch).lstrip("Ww")
    _toks = list(_AGENTS_ENTRY_TOKEN_RE.finditer(s, _fs))
    spans = []
    for i, t in enumerate(_toks):
        if t.group(1) != _bnum:
            continue
        start = t.start()
        if i + 1 < len(_toks):
            end = _toks[i + 1].start()
            while end > t.end() and s[end - 1] == "；":
                end -= 1
        else:
            _tail_i = s.find(_AGENTS_TAIL)
            end = (_tail_i + 1) if _tail_i != -1 else len(s)
        spans.append((start, end))
    return spans


def _locate_handover_head_entry(s, entry):
    """定位交接文档**头链**内本批 entry 的区间（起点=分隔「·」·终点=entry 文本末尾）。

    W1122（根修 W1117 R-01）：头链 entry 此前无条件 prepend ⇒ 重跑级联静默重复。
    """
    h0 = s.find("> 最后更新：")
    if h0 == -1:
        return None
    h1 = s.find("\n", h0)
    if h1 == -1:
        h1 = len(s)
    span = ci.locate_entry(s[h0:h1], re.escape(entry), r"·")
    if span is None:
        return None
    return h0 + span[0], h0 + span[1]


def _locate_workflows_marker(s, batch_w, desc):
    """定位 workflows README 里本批里程碑尾标记的区间。

    W1122（根修 W1117 R-01）：尾标记此前无条件包裹 ⇒ 重跑级联层层累积。
    """
    return ci.locate_entry(s, r"\+ W%s %s·无 workflow 结构改动）。"
                          % (re.escape(str(batch_w)), re.escape(desc)))


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
    tail = _AGENTS_TAIL
    assert s.count(tail) == 1, "AGENTS 脚注尾锚点异常"
    _sep = "" if s[: s.index(tail)].rstrip().endswith("；") else "；"
    _note_text = ctx.spec["agents_note"].rstrip("。")  # W972 修：尾句号不剥会拼出「。。」
    # W1122（根修 W1117 R-01）：脚注条目此前**无条件追加** ⇒ 重跑级联静默重复插同号条目。
    # 本版：已存在本批条目 ⇒ 内容一致则零变化·不一致则替换（可重跑级联修正）。
    _spans = _locate_agents_note(s, ctx.batch)
    if _spans:
        # W1122（根修 W1117 R-03）：先删**同号重复副本**（从后往前删·区间稳定），
        # 再校准首个副本内容（重复副本源于旧实现的分号截断缺陷·本版一并订正）。
        for _st2, _en2 in reversed(_spans[1:]):
            _cut = _st2
            _semi = s.rfind("；", 0, _st2)
            if _semi != -1:
                _cut = _semi
            s = s[:_cut] + s[_en2:]
        _spans = _locate_agents_note(s, ctx.batch)
        _st, _en = _spans[0]
        _entry_new = _note_text + "。"
        if s[_st:_en].strip() != _entry_new.strip():
            s = s[:_st] + _entry_new + s[_en:]
    else:
        # W1122：按批号**升序**插入（脚注条目断言 _nums == sorted(_nums)）——
        # 原实现恒插在末尾 ⇒ 低号批（并行让号后的常见形态）落段即触发「脚注条目乱序」断言。
        _fs0 = s.find("*本文件由")
        assert _fs0 != -1, "AGENTS 脚注起点锚点缺失"
        _bn = int(str(ctx.batch).lstrip("Ww"))
        _target = None
        for _m2 in re.finditer(
                r"(?:20\d{2}-\d{2}-\d{2}|二〇[一二三四五六七八九〇零十廿卅]+年"
                r"[一二三四五六七八九〇零十廿卅]+月[一二三四五六七八九〇零十廿卅]+日)"
                r"（(?:v[\d.]+ )?W(\d{3,4})）", s[_fs0:]):
            if int(_m2.group(1)) > _bn:
                _target = _fs0 + _m2.start()
                break
        if _target is not None:
            s = s[:_target] + _note_text + "；" + s[_target:]
        else:
            s = s.replace(tail, _sep + _note_text + tail, 1)
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
    """CITATION.cff 版本/日期同步（第 10 面）。

    **W1114**：改由共享模块 version_surface 推进（幂等·单一事实源）。
    """
    p = "CITATION.cff"
    s, nl = load(p)
    out, _changed = version_surface.advance_text(
        s, p, ctx.batch, ctx.date, ctx.desc, ctx.head_sentence)
    if out == s:
        # W1122：低号批落段 ⇒ 版本面**单调守卫**（只升不降）⇒ 本批号 ≤ 现役批号 ⇒ 零变化是正确结果。
        # 原断言「必须有变化」会把单调守卫的正当零变化误判为推进失效 ⇒ 改为零变化时校验
        # 「现役批号 ≥ 本批号」⇒ 判据强度不降（该改却没改仍判红）。
        _cur = re.search(r"W(\d{3,4})", s)
        _cur_w = int(_cur.group(1)) if _cur else None
        _mine = int(str(ctx.batch).lstrip("Ww"))
        assert _cur_w is not None and _cur_w >= _mine, (
            "CITATION.cff 版本/日期行未变化且现役批号 %s < 本批 W%d ⇒ 版本面推进失效"
            % (_cur_w, _mine))
        print("[CITATION] 现役批号 W%d ≥ 本批 W%d ⇒ 单调守卫零变化（低号批落段的正确结果）"
              % (_cur_w, _mine))
    ctx.pend.append((p, out, nl))


def _face_file_index(ctx):
    """file-index 最新段插入（**幂等**：本批号已立段则不再追加·W1120 根修）。

    W1120 根修（对方 W1121 批实证转交我方）：本面此前**无条件**在「最新段」之前插入
    ⇒ 当本批号已由补段工具（backfill_changelog）立过段时，会插出**同号双段**
    （CHANGELOG 面有「batch == 顶段+1」断言挡住 ⇒ 只有 file-index 面漏判）。
    ⇒ 本批号已立段时：**内容一致 ⇒ 零变化不追加**（幂等）；
      **内容不一致 ⇒ fail-closed** 并指引用 scripts/rebuild_section.py 重建该段
      （不静默留 stale 段·不制造同号双段）。
    """
    # ---------- file-index ----------
    p = "scripts/output/file-index.md"
    s, nl = load(p)
    batch_w = int(str(ctx.batch).lstrip("Ww"))
    head = "## {} {}（{}）".format(
        ctx.batch, re.sub(r"^W\d+\s+", "", ctx.spec["title"].split(" — ")[0].split("（")[0]).strip(), ctx.date)
    # W1142 立式：行数超阈值自动分组（与 backfill_changelog.file_index_block 同口径·
    # 单一原语 batch_spec.fi_group_rows——spec 恒全量·登记面压缩）
    import batch_spec as _bs
    seg_lines = [head, "", "| 文件 | W | 说明 |", "|---|---|---|"] + _bs.fi_group_rows(ctx.spec["file_index_rows"], ctx.batch) + ["", ""]
    rows = nl.join(seg_lines)          # 原生行尾（落盘用）
    rows_lf = "\n".join(seg_lines)      # 归一形态（与 load() 读出的内存形态一致·供内容判等）
    # W1120 幂等判定：本批号是否已立段
    m_exist = None
    for _m in re.finditer(r"^## (W\d+) ", s, re.M):
        if int(_m.group(1)[1:]) == batch_w:
            m_exist = _m
            break
    if m_exist is not None:
        _nxt = re.search(r"^## (W\d+) ", s[m_exist.end():], re.M)
        _end = m_exist.end() + (_nxt.start() if _nxt else len(s) - m_exist.end())
        _old = s[m_exist.start():_end]
        if _old.strip() == rows_lf.strip():
            print("[FILE-INDEX] W%d 段已存在且内容一致 ⇒ 幂等跳过（不追加·防同号双段）" % batch_w)
            return
        raise AssertionError(
            "file-index 已存在 W%d 段但内容与 spec 不一致 ⇒ 拒绝追加（防同号双段·不静默留 stale）"
            "——修法=跑 py -3 scripts/rebuild_section.py --batch W%d --spec <spec 路径> --apply 重建该段"
            % (batch_w, batch_w))
    mm = re.search(r"## (W\d+) ", s)
    assert mm, "file-index 未找到最新段"
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


def _rotate_only(ctx, apply):
    """独立滚动入口（W1127·T74 R-C）：只跑交接文档的「里程碑滚动淘汰」这一个动作。

    病根：此前滚动只能作为「本批块插入」的副动作发生 ⇒ 若某批只想滚动（或需重跑滚动），
    没有独立入口 ⇒ 只能手工改文档；且「重跑会再淘汰一块」的隐患只靠调用点守卫。
    W1124 已把守卫**下沉到 _handover_rotate_oldest 内部**（本批块已在链上 ⇒ 零变化），
    本步提供独立入口 ⇒ 独立重跑同样零变化（零红灯·不丢信息）。

    用法：py -3 scripts/batch_cascade.py --spec <spec> --rotate-only [--apply]
    """
    p = "HANDOVER.md"
    s, nl = load(p)
    ctx.cl_src = open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8").read()
    h1pos = s.find("## 一、当前进度")
    assert h1pos != -1, "未找到交接文档「一、当前进度」段"
    out = _handover_rotate_oldest(s, ctx, nl, h1pos)
    if out == s:
        print("[ROTATE] 本批块已在链上 ⇒ 视为本批已滚动过 ⇒ 零变化（幂等）")
        return 0
    if not apply:
        print("[ROTATE] 需滚动最老里程碑块（dry-run·未落盘）·加 --apply 落盘")
        return 0
    _apply_pend([(p, out, nl)], ctx.batch)
    print("[ROTATE] 已落盘：滚动淘汰最老里程碑块并同步历史概要指针")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--rotate-only", action="store_true",
                    help="只执行「交接文档里程碑滚动淘汰」一个动作（W1127·T74 R-C 独立入口）："
                         "幂等——本批块已在链上 ⇒ 零变化并直接退出")
    ap.add_argument("--allow-gap", default="",
                    help="允许的在途缺口 W 号（逗号分隔·须台账有认领行且 CHANGELOG 无段·W895 新增）")
    ap.add_argument("--skip-changelog", action="store_true",
                    help="跳过 CHANGELOG 面（段改由 backfill_changelog.py 按号序补·"
                         "用于「并行批次占号未立段」的号段缺口；此时 --allow-gap 的号"
                         "**不要求**台账有认领行·只要求 CHANGELOG 无该段）")
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
    if args.rotate_only:
        return _rotate_only(ctx, args.apply)
    assert ctx.entry.endswith("）"), "head_entry 必须以闭合括号结尾"
    assert "（" not in ctx.spec["head_sentence"] and "）" not in ctx.spec["head_sentence"], (
        "head_sentence 禁含全角括号——会破坏下一批「当前 HEAD 句」断言的 [^）]* 匹配（W649 实证：W648 嵌套括号致本批断言 FAIL，交接文档已手工修复）"
    )
    _assert_status_wnum(spec, ctx.batch)  # W956/P-43-05：段状态认领登记 W 号 == 本段号（E-28 防线）
    if args.skip_changelog:
        # 跳过 CHANGELOG 面（W1045 新增）：段由 `backfill_changelog.py --only <W号>` 按号序补
        # （场景：并行批次占号未立段 ⇒ 号段出现缺口·正常级联的「段号必须 == 顶段+1」断言
        #  无法通过）。此处仍需算出 new_w/new_rule 供其余 9 个「当前态」面使用。
        _cs = open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8").read()
        _cm = re.search(r"^### (?:v[\d.]+（[^）]*）：W(\d+)|W(\d+)（[^）]*）：)", _cs, re.M)
        assert _cm, "CHANGELOG 未找到现役段"
        _cur_w = int(_cm.group(1) or _cm.group(2))
        ctx.cl_src = _cs
        ctx.new_w = _cur_w + 1 + len(ctx.allow_gap)
        ctx.new_rule = "（W001-W%d）" % ctx.new_w
        assert ctx.batch == "W" + str(ctx.new_w), (
            "批次号应为 W%d（现役段 W%d + 在途缺口 %s）" % (ctx.new_w, _cur_w, ctx.allow_gap))
        for _g in ctx.allow_gap:
            assert "### " + _g not in _cs, "缺口 %s 已有段（无需允许）" % _g
        print("[SKIP-CHANGELOG] 段由 backfill 补·new_w=W%d（在途缺口 %s）"
              % (ctx.new_w, "、".join(ctx.allow_gap) or "无"))
    else:
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
    num = str(batch).lstrip("W")
    r = _STATS_RUNNER([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "stats.py"),
                       "--w", num])
    tail = [x for x in ((r.stdout or "") + (r.stderr or "")).splitlines() if x.strip()][-2:]
    ok = r.returncode == 0
    print("[STATS] %s（%s）" % ("OK" if ok else "FAIL", " / ".join(tail)))
    return ok


def _hint_size():
    """[SIZE] 治理文档体积窗口提示位（判据本体 check_doc_size_budget）。"""
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


def _tmpe_stale_one(tmpe_dir, bucket, ttl):
    """统计单个 tmpe 桶里超龄件数与体积（W1114 结构档拆分·抽函数降嵌套）。"""
    _n = _mb = 0
    for _dp, _dn, _fn in os.walk(os.path.join(tmpe_dir, bucket)):
        for _f in _fn:
            try:
                _st = os.stat(os.path.join(_dp, _f))
            except OSError:
                continue
            if time.time() - _st.st_mtime > ttl * 86400:
                _n += 1
                _mb += _st.st_size
    return "%s 超龄 %d 件 %.0fMB(TTL%dd)" % (bucket, _n, _mb / 1048576, ttl)


def _hint_tmpe_buckets():
    """[TMPE] tmpe 批次桶计数 + _shot/_inbox TTL 超龄报数（W976 段）。"""
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
            _stale.append(_tmpe_stale_one(_tt.TMPE, _bucket, _ttl))
        if _stale:
            print("[TMPE] " + "·".join(_stale) + "——到期列清单经主人确认走回收站"
                  "（tmpe_tidy.py --plan --older N）")
    except Exception as _exc:  # noqa: BLE001 — 提示位故障留痕不阻断
        print(f"[TMPE] 提示位不可用（{_exc}）")


def _zero_ref_candidates(tracked_out):
    """统计 scripts 顶层下划线前缀件里「语料零引用」的退役候选数（W992 口径）。

    返回 -1 表示统计不可用（异常留痕·不阻断）。
    """
    import subprocess as _sp

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
        _zero_ref = 0
        for _f in tracked_out.splitlines():
            _name = _f.replace("scripts/", "", 1)
            if not _name.startswith("_"):
                continue
            if _name in _cl_tail or any(_name in _tx for _tx in _texts.values()):
                continue
            _zero_ref += 1
        return _zero_ref
    except Exception:
        return -1


def _hint_scripts():
    """[SCRIPTS] scripts 顶层下划线前缀件跟踪态计数 + 零引用退役候选（P-44-03·W992 口径）。"""
    try:
        import subprocess as _sp

        _r = _sp.run(["git", "ls-files", "scripts/_*"], capture_output=True, text=True,
                     encoding="utf-8", errors="replace", cwd=ROOT)
        _tracked = len([x for x in _r.stdout.splitlines() if "/" not in x.replace("scripts/", "", 1)])
        _on_disk = len([f for f in os.listdir(os.path.join(ROOT, "scripts"))
                        if f.startswith("_") and os.path.isfile(os.path.join(ROOT, "scripts", f))])
        _zero_ref = _zero_ref_candidates(_r.stdout)
        _msg = "[SCRIPTS] 顶层下划线件跟踪态 %d 个（盘上 %d）·零引用退役候选 %s 个" % (
            _tracked, _on_disk, _zero_ref)
        if _zero_ref > 20:
            _msg += "——超阈值 20：跑退役扫描（archive_file.py 语料级引用剔除·W977/W992 先例）"
        print(_msg)
    except Exception as _exc:  # noqa: BLE001 — 提示位故障留痕不阻断
        print(f"[SCRIPTS] 提示位不可用（{_exc}）")


def _hint_archive():
    """[ARCHIVE] 归档健康提示位（check_archive_health T1-T4·W995）。"""
    try:
        import check_archive_health as _cah

        _cah.run(strict=False, prefix="[ARCHIVE] ")
    except Exception as _exc:  # noqa: BLE001 — 提示位故障留痕不阻断
        print(f"[ARCHIVE] 提示位不可用（{_exc}）")


def _hint_hygiene():
    """[HYGIENE] 三支报告型探针接入收尾浮出（W1014 接线升格·不硬挂 verify 槽）。"""
    try:
        import subprocess as _sp2

        for _tag, _probe in (("卫生", "check_content_hygiene.py"),
                             ("双源", "check_dual_source_scan.py"),
                             ("锚点", "check_parser_anchor_coverage.py")):
            _pr = _sp2.run([sys.executable, os.path.join(ROOT, "scripts", _probe)],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", cwd=ROOT, timeout=180)
            _tail = next((ln for ln in reversed(_pr.stdout.splitlines()) if ln.strip()), "")
            print(f"[HYGIENE] {_tag} {_probe} → {_tail.strip()[:80]}")
    except Exception as _exc:  # noqa: BLE001 — 提示位故障留痕不阻断
        print(f"[HYGIENE] 提示位不可用（{_exc}）")


def _hint_tmpe_journal():
    """[TMPE] 上次清理活动日期（.journal 最新落笔·W995）。"""
    try:
        import datetime as _dt

        import tmpe_tidy as _tt

        _jdir = os.path.join(_tt.TMPE, ".journal")
        _journals = [os.path.join(_jdir, f) for f in os.listdir(_jdir)] if os.path.isdir(_jdir) else []
        if _journals:
            _last = max(os.path.getmtime(j) for j in _journals)
            print("[TMPE] 上次清理活动 %s（%.0f 天前·journal %d 份）"
                  % (_dt.date.fromtimestamp(_last), (time.time() - _last) / 86400, len(_journals)))
    except Exception as _exc:  # noqa: BLE001 — 提示位故障留痕不阻断
        print(f"[TMPE] 日期提示不可用（{_exc}）")


def _close_hints():
    """收官提示位集合（W960 建·W979 扩展·全部只输出不改判定与退出码——W822 语义）。

    - [SIZE]    治理文档体积窗口（判据本体 check_doc_size_budget·开工面硬判据）
                + 超窗提示行（P-44-01：级联每批插入一段·回窗是每批常态动作而非异常）
    - [TMPE]    tmpe 批次桶计数 + _shot/_inbox TTL 超龄报数（P-44-02：删除须主人确认+回收站）
    - [SCRIPTS] scripts 顶层下划线件跟踪态计数（P-44-03：>20 提示退役扫描·W977 先例）

    **W1114 拆分为多个子函数**：原实现单函数 82 语句 / 复杂度 26 / 分支 25 / 嵌套 5，
    超 ruff 结构档阈值（≤80 语句 · ≤15 复杂度 · ≤16 分支 · ≤4 嵌套）⇒ 本批首次改动
    该文件即被结构档拦下 ⇒ 按结构档判据做根因拆分（行为不变·仅函数边界）。
    """
    _hint_size()
    _hint_tmpe_buckets()
    _hint_scripts()
    _hint_archive()
    _hint_hygiene()
    _hint_tmpe_journal()

if __name__ == "__main__":
    sys.exit(main())

# spec 字段说明：
# batch/version/date/title/desc/head_entry/head_sentence/changelog_body/milestone_block/agents_note/file_index_rows
# 注意：head_entry 为交接文档头尾链条目全文（以 ） 结尾，不带分隔符）；
#       changelog_body 以两个换行开头；milestone_block 多行以 \n 分隔（脚本会按文件行尾归一）。
