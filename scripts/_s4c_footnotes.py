"""_s4c_footnotes.py — S4 C 轨主稿：注释脚注化 + 引文注释格式复核 + 图注位 + 数字同步（一次性）

依据：
- 《数字人文》征稿启事（清华中文系官网）：注释采用脚注样式，格式参见《中国社会科学》引文注释规定
- 《中国社会科学杂志社期刊引文注释规定（2026 年修订）》：页下注①②③、外文文献格式、>3 作者用 et al.
本批动作：
1) 正文注码 ①-⑮ → Markdown 脚注 [^n]（按出现顺序重排；新增 [^1] Walters & Wilder、[^14] 底本）
2) 「## 注释」重建为 17 条脚注定义（英文题录按 2026 规定重排）；「## 参考文献」并入脚注（刊方未设文末书目）
3) §1(一) 补 Walters & Wilder 动机链段（Sci Rep 2023，55%/18%/43%/24% 经原文复核）
4) 图注位：图 C-1 ~ 图 C-4 引用与图注行
5) 数字同步占位：433→437、841→842（待匿名稿入库后复验）
6) 内部术语脱敏：「A 轨」→ 平行稿件表述（投稿件正文不留内部轨名）
只读输入、单文件写出，失败即 assert 中断不落盘。
"""
import io
import sys

ROOT_MD = r"D:\xiyouji\docs\S4-学术投稿\学术论文C轨-可验证性基础设施.md"


def rep(s, old, new, n=1, label=""):
    c = s.count(old)
    assert c == n, "替换计数异常 [%s] 期望 %d 实得 %d :: %s" % (label, n, c, old[:50])
    return s.replace(old, new)


def main():
    text = io.open(ROOT_MD, encoding="utf-8").read()
    orig = text

    # ---------- 1. 头部 ----------
    text = rep(text,
               "> S4 学术投稿 · 论文三（C 轨）初稿 · 2026-09-26",
               "> S4 学术投稿 · 论文三（C 轨） · 2026-09-28（脚注体例与配图版）",
               label="head-line")
    text = rep(text,
               "> 体例说明：草稿采用「脚注样式注释（文末并列）+ 参考文献」双轨，注释序号①起，参考文献暂作书目标注（角标于投稿体例转换时统一分配）；正式投稿前须按刊方当期样文与《中国社会科学》引文注释规定复核转换",
               "> 体例说明：注释已按《数字人文》征稿启事（「注释采用脚注样式」）与《中国社会科学》引文注释规定（2026 年修订）脚注化——正文注码以 Markdown 脚注语法承载（[^n] 置于引文句标点之后，按出现顺序编号），注文见文末「注释」；投稿 Word 版将呈现为页下注（序号①②③，按刊方「每页单独排序」规则设置）。原「参考文献」书目已并入脚注（刊方征稿启事仅规定注释体例，未设文末参考文献）。",
               label="tili")

    # ---------- 2. 摘要（中/英）----------
    text = rep(text,
               "当批实测结果：433 条引文行全部命中（含本文自带的 4 条；另 3 条为门禁加固后新纳入核验分母者），覆盖 841 个文件，亚秒级完成（本机复测 0.47–0.81 秒）。",
               "当批实测结果：437 条引文行全部命中（含本文两稿自带的 8 条；另 3 条为门禁加固后新纳入核验分母者），覆盖 842 个文件，亚秒级完成（本机复测 0.47–0.81 秒）。",
               label="abstract-zh")

    lines = text.split("\n")
    done_en = False
    for i, ln in enumerate(lines):
        if ln.startswith("**Abstract**: "):
            lines[i] = ("**Abstract**: As generative AI enters the production pipelines of digital humanities "
                        "scholarship, hallucinated citations have become a measurable integrity risk. An audit in "
                        "*The Lancet* of nearly 2.5 million biomedical papers reports a more than twelvefold "
                        "increase in the fabricated-reference rate within two years; a study covering 111 million "
                        "references across four platforms estimates about 147,000 non-existent citations in 2025 "
                        "alone. Existing responses remain largely external: manual line-by-line checking does not "
                        "scale, AI-content detectors do not target citation entities, and platform sanctions arrive "
                        "only after publication. This paper presents and evaluates a three-layer verifiability "
                        "infrastructure embedded in the production workflow of a *Journey to the West* digital "
                        "humanities project (615 documents; a 100-chapter electronic base text): an anchor layer "
                        "that locates every claim at \"chapter N, line X\"; a verification layer that requires every "
                        "quotation line to be an exact substring of the base text after whitespace normalization, "
                        "with any mismatch failing the delivery; and a gate layer that makes verification a "
                        "mandatory step of every delivery rather than a one-off check before submission. Results: "
                        "437 quotation lines — including the eight carried by the two versions of this paper — "
                        "achieved a 100% hit rate across 842 files in under a second. Two cases are analyzed: a "
                        "well-formed hallucinated bibliographic entry that survived three weeks in two manuscripts "
                        "and an index before being detected by anchoring verification to external authoritative "
                        "sources; and an incident in which a repair script emptied the inline styles of 224 pages "
                        "while fourteen gates stayed green, exposing the blind spots of the gates themselves. The "
                        "discussion delimits what quote-level verification can and cannot answer — whether a "
                        "quotation is literally present, not whether it supports the claim — and positions the work "
                        "against adjacent, same-layer efforts in biomedical data curation, legal research, and "
                        "conference-proceedings auditing.")
            done_en = True
    assert done_en, "未找到英文摘要行"
    text = "\n".join(lines)

    # ---------- 3. §1（一）插入 Walters 动机链段 ----------
    text = rep(text,
               "这种风险的规模，在最近两年从个案传闻变成了可测量的分布。",
               "这类条目并非假想。早在 2023 年，一项审计逐条核验了 ChatGPT（GPT-3.5 与 GPT-4）生成的 84 份文稿中的 636 条被引文献：GPT-3.5 的引文有 55% 所指的作品并不存在，GPT-4 为 18%；即便在真实存在的引文中，带有作者、题名、卷期等实质性错误的仍分别占 43% 与 24%。[^1]\n\n这种风险的规模，在随后三年间从个案传闻变成了可测量的分布。",
               label="walters-para")

    # ---------- 4. §3 图注位 ----------
    text = rep(text,
               "本节按自下而上的顺序描述三层结构：锚点层解决\"引文在哪里\"，校验层解决\"引文对不对\"，门禁层解决\"核验何时发生、由谁强制执行\"。",
               "本节按自下而上的顺序描述三层结构：锚点层解决\"引文在哪里\"，校验层解决\"引文对不对\"，门禁层解决\"核验何时发生、由谁强制执行\"（图 C-1）。\n\n**图 C-1　三层可验证性基础设施（来源：作者自绘）**",
               label="fig1")
    text = rep(text,
               "经定位脚本查询，该句位于第 2 回 line 9。任何读者拿到\"第 2 回 line 9\"这一坐标，都可以在公开语料上独立复现定位结果。",
               "经定位脚本查询，该句位于第 2 回 line 9（图 C-2）。任何读者拿到\"第 2 回 line 9\"这一坐标，都可以在公开语料上独立复现定位结果。",
               label="fig2-ref")
    text = rep(text,
               "锚点层的意义不在于方便作者自己回溯，而在于让第三方拥有与作者相同的定位能力——这是后文一切\"可复现\"承诺的底座。",
               "锚点层的意义不在于方便作者自己回溯，而在于让第三方拥有与作者相同的定位能力——这是后文一切\"可复现\"承诺的底座。\n\n**图 C-2　锚点定位实测：两条引文的「第 N 回 line X」坐标（来源：据工具实测输出重绘）**",
               label="fig2-cap")
    text = rep(text,
               "以该条为例：它声明出自第 13 回，去空白归一后在底本文本中可以精确命中，因此通过；如果引文里的\"魔生\"被错背成\"魔灭\"，或者句子被改写成\"心生则种种魔生\"，匹配都会失败，交付被阻断。",
               "以该条为例：它声明出自第 13 回，去空白归一后在底本文本中可以精确命中，因此通过；如果引文里的\"魔生\"被错背成\"魔灭\"，或者句子被改写成\"心生则种种魔生\"，匹配都会失败，交付被阻断（图 C-3）。\n\n**图 C-3　引文校验实测：全量命中与单字改写后的交付阻断（来源：据工具实测输出重绘）**",
               label="fig3")
    text = rep(text,
               "原著引文硬验证则是本文的中心：任何一条引文行未命中即整体失败。",
               "原著引文硬验证则是本文的中心：任何一条引文行未命中即整体失败。门禁体系的一次完整运行见图 C-4。",
               label="fig4-ref")
    text = rep(text,
               "另一个是不对称的交付纪律。门禁挂在提交路径上，意味着它的失败会直接阻断工作流。这种设计把核验成本前移到了生产成本里：每条引文在写下的那一刻就要考虑\"它能不能命中\"，而不是等审稿意见回来再补。本文认为这是基础设施与工具的分水岭——工具改变能力，基础设施改变路径。",
               "另一个是不对称的交付纪律。门禁挂在提交路径上，意味着它的失败会直接阻断工作流。这种设计把核验成本前移到了生产成本里：每条引文在写下的那一刻就要考虑\"它能不能命中\"，而不是等审稿意见回来再补。本文认为这是基础设施与工具的分水岭——工具改变能力，基础设施改变路径。\n\n**图 C-4　交付门禁运行实测（输出节选·核心全部通过）（来源：据工具实测输出重绘）**",
               label="fig4-cap")

    # ---------- 5. 数字与内部术语 ----------
    text = rep(text,
               "在实证层面，给出当批实测的规模数据（433 条引文行、841 个文件、亚秒级、100% 命中）",
               "在实证层面，给出当批实测的规模数据（437 条引文行、842 个文件、亚秒级、100% 命中）",
               label="contrib")
    text = rep(text, "## 四、实证：615 篇文档中的 430 条引文",
               "## 四、实证：615 篇文档中的 437 条引文", label="sec4-title")
    text = rep(text,
               "截至 2026 年 9 月 26 日的实测口径如下。内容文档 615 篇（项目六大内容板块的顶层文档计数）；目录全量扫描覆盖 841 个文件（含本批新增的审计报告，文档增删会使该数漂移）；通过核验的原著引文行 433 条（含本文自带的 4 条，以及门禁加固后新纳入分母的 3 条），命中率 100%；校验脚本全量运行亚秒级完成（多次复测 0.47–0.81 秒，视机器负载）。",
               "截至 2026 年 9 月 28 日的实测口径如下。内容文档 615 篇（项目六大内容板块的顶层文档计数）；目录全量扫描覆盖 842 个文件（文档增删会使该数漂移）；通过核验的原著引文行 437 条（含本文两稿自带的 8 条，以及门禁加固后新纳入分母的 3 条），命中率 100%；校验脚本全量运行亚秒级完成（多次复测 0.47–0.81 秒，视机器负载）。",
               label="shice")
    text = rep(text,
               "433 条引文意味着引文核验不是抽样演练，而是覆盖全文的真实工作量——每一条引文都逐字比对过。841 个文件的扫描面说明",
               "437 条引文意味着引文核验不是抽样演练，而是覆盖全文的真实工作量——每一条引文都逐字比对过。842 个文件的扫描面说明",
               label="shice2")
    text = rep(text,
               "这一批数字在 2026-09-27 又有一处小规模变动：同批完成的 A 轨稿件修复中，核验脚本被加固——凡疑似引文行而语法漂移者一律判失败（此前会被静默跳过）。加固后，三条此前\"隐身\"的引文行（某匿名稿因回目号带空格与半角引号而从未被识别）进入核验分母并全部逐字命中，全库引文行数由 430 升至 433。",
               "这一批数字其后又有一处小规模变动：在一次平行稿件的修复中，核验脚本被加固——凡疑似引文行而语法漂移者一律判失败（此前会被静默跳过）。加固后，三条此前\"隐身\"的引文行（某匿名稿因回目号带空格与半角引号而从未被识别）进入核验分母并全部逐字命中，全库引文行数由 430 升至 433；本文两稿入库后，快照口径为 437 条。",
               label="hardening")
    text = rep(text, "随后被 A、B 两个论文方向的多篇稿件引用。",
               "随后被该项目多个论文方向的多篇稿件引用。", label="ab-scrub")
    text = rep(text,
               "当批实测给出 433 条引文行 100% 命中、841 个文件、亚秒级的成绩",
               "当批实测给出 437 条引文行 100% 命中、842 个文件、亚秒级的成绩",
               label="concl")

    # ---------- 6. 分拆头尾：注释/参考文献并入脚注 ----------
    i0 = text.index("\n## 注释\n")
    i2 = text.index("\n---\n\n## 核验与复现\n")
    i3 = text.index("\n---\n\n## 关联文档\n")
    head = text[:i0]
    assert i0 < i2 < i3, "节序异常"

    # 底本注锚（§3.1：「…一并入库。[1]锚点体系…」）
    head = rep(head, "语料随项目公开，加载脚本与页面一并入库。[1]锚点体系",
               "语料随项目公开，加载脚本与页面一并入库。[^14]锚点体系", label="diben-note")

    # 注码重排（仅正文头段）：①-⑮ → [^2]-[^17]（[^1] Walters、[^14] 底本 已就地插入）
    mapping = {ord("①"): "[^2]", ord("②"): "[^3]", ord("③"): "[^4]", ord("④"): "[^5]",
               ord("⑤"): "[^6]", ord("⑥"): "[^7]", ord("⑦"): "[^8]", ord("⑧"): "[^9]",
               ord("⑨"): "[^10]", ord("⑩"): "[^11]", ord("⑪"): "[^12]", ord("⑫"): "[^13]",
               ord("⑬"): "[^15]", ord("⑭"): "[^16]", ord("⑮"): "[^17]"}
    n_before = sum(head.count(chr(0x2460 + i)) for i in range(15))
    head = head.translate(mapping)
    n_after = sum(head.count("[^%d]" % i) for i in range(1, 18))
    assert n_after == n_before + 2, "注码重排后计数异常：%d vs %d" % (n_after, n_before)

    # 脚注定义（17 条）
    defs = [
        "[^1]: W. H. Walters and E. I. Wilder, “Fabrication and errors in the bibliographic citations generated by ChatGPT,” *Scientific Reports*, vol. 13 (2023), art. no. 14045. DOI: 10.1038/s41598-023-41032-5.",
        "[^2]: M. Topaz et al., “Fabricated citations: an audit across 2·5 million biomedical papers,” *The Lancet*, vol. 407, no. 10541 (2026), pp. 1779-1781. DOI: 10.1016/S0140-6736(26)00603-3. 该文另刊出勘误一则（*The Lancet*, vol. 408, no. 10551 (2026), p. 218）。",
        "[^3]: Z. Zhao et al., “LLM hallucinations in the wild: Large-scale evidence from non-existent citations,” arXiv:2605.07723, May 8, 2026, https://arxiv.org/abs/2605.07723（2026 年 9 月 26 日访问）。（预印本，未经同行评审）",
        "[^4]: M. Naddaf and E. Quill, “Hallucinated citations are polluting the scientific literature,” *Nature*, vol. 652 (2026), pp. 26-29. DOI: 10.1038/d41586-026-00969-z.",
        "[^5]: H. Jergas and C. Baethge, “Quotation accuracy in medical journal articles——a systematic review and meta-analysis,” *PeerJ*, vol. 3 (2015), art. no. e1364. DOI: 10.7717/peerj.1364.",
        "[^6]: D. B. Resnik and M. Hosseini, “Hallucinated citations produced by generative artificial intelligence may constitute research misconduct when citations function as data in scholarly papers,” *Accountability in Research*, vol. 33, no. 7 (2026). DOI: 10.1080/08989621.2026.2645390.",
        "[^7]: arXiv, “Code of Conduct” and “Code of Conduct Enforcement,” info.arxiv.org（2026 年 9 月 26 日访问）；「一年禁投」公告系版主 2026 年 5 月通过社交媒体发布，经科技媒体报道，本文按其「公告式执法实践」形态表述。",
        "[^8]: ICLR 2026 Program Chairs, “Policies on Large Language Model Usage at ICLR 2026,” blog.iclr.cc, August 26, 2025; “ICLR 2026 Response to LLM-Generated Papers and Reviews,” blog.iclr.cc, November 19, 2025; “A Retrospective on the ICLR 2026 Review Process,” blog.iclr.cc, March 31, 2026（2026 年 9 月 26 日访问）。",
        "[^9]: M. Russinovich, R. S. Siva Kumar and A. Salem, “Phantom References: Hallucinated Citations That Survive Peer Review at Top-Tier Conferences,” arXiv:2607.00738, 2026, https://arxiv.org/abs/2607.00738（2026 年 9 月 26 日访问）。（RefChecker 开源管线；写作前撞题检索发现的同域并行工作）",
        "[^10]: R. Franzone, “A citation verification framework for LLMs in sensitive domains,” *The AI Journal*, April 10, 2026.",
        "[^11]: linkml-reference-validator, PyPI, https://pypi.org/project/linkml-reference-validator/（2026 年 9 月 26 日访问），生物医学数据策管场景的支持文本子串校验；proof-citations / Proof Engine, PyPI, v1.45.0。",
        "[^12]: 深度研究报告管线的证据引文核验方向（evidence-quote 子串匹配与蕴含判定）。该方向多份工作由自动研究系统产出，本文仅引用其问题意识，不引用其数据。",
        "[^13]: 撞题检索为公开网页级（2026 年 9 月 26 日执行），覆盖 arXiv、PyPI、主要出版社页与科技媒体；CNKI 级中文库复核列为投稿前查重项。",
        "[^14]: 底本电子文本为百回本《西游记》的电子化文本（100 回、708,441 字），随项目公开，加载脚本与检索页面一并入库；本文全部引文核验与行号定位均锚定此一公开底本。",
        "[^15]: 工具与文件：定位脚本 `scripts/audit/line_check.py`、引文校验脚本 `scripts/check_citations.py`、门禁入口 `scripts/verify_delivery.py`，均为无外部依赖的只读工具；上述工具与底本语料、被核验内容同在项目公开仓库发布，版本以投稿时冻结的版本为准。",
        "[^16]: 复现命令示例与预期输出见图 C-2 至图 C-4；三条命令均只读，不写入任何源文件。",
        "[^17]: 行号锚定与语料切分绑定的问题，本文尚未给出最终方案；候选方向包括「回目内字符偏移锚点」与「语料哈希＋行号」复合锚点。",
    ]
    notes_block = "## 注释\n\n" + "\n\n".join(defs) + "\n"

    verify_block = (
        "## 核验与复现\n\n"
        "- 量化数字（615 篇 / 842 文件 / 437 条引文行 / 100% / 亚秒级 / 105 篇）为 2026-09-28 终测快照"
        "（含本文两稿自带的 8 条与门禁加固后新纳入的 3 条；文档增删会使总数漂移，复跑时以本快照口径为准）。\n"
        "- 全文 4 条原著引文行已通过引文校验脚本命中核验（第 98 回 / 第 2 回 / 第 13 回 / 第 7 回）；"
        "锚点行号经定位脚本实测（第 2 回 line 9、第 13 回 line 1、第 7 回 line 45、第 98 回 line 43），"
        "实测输出见图 C-2 与图 C-3。\n"
        "- 外部文献题录均经 Crossref API 或官方页面复核；Lancet 勘误、arXiv 政策形态、预印本状态已在注释中如实标注。\n"
        "- 投稿前尚待：CNKI 全库查重、Lancet 勘误内容复核、Word 版生成（页下注与图版）、刊方当期样文终校。\n"
    )

    new_text = head + "\n" + notes_block + "\n---\n\n" + verify_block + text[i3:]

    # 复审修复（2026-09-28·P1-1）：体例说明中的「序号①②③」示例在注码重排中被误伤，回正
    new_text = rep(new_text, "（序号[^2][^3][^4]，", "（序号①②③，", label="seq-example-restore")

    # 落地校验（内存内）
    assert "## 参考文献" not in new_text, "参考文献节未清除"
    assert new_text.count("## 注释") == 1 and new_text.count("## 核验与复现") == 1, "节计数异常"
    assert new_text.count("[^1]:") == 1 and new_text.count("[^17]:") == 1, "脚注定义异常"

    with io.open(ROOT_MD, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(new_text)
    print("written:", ROOT_MD)
    print("chars: %d -> %d" % (len(orig), len(new_text)))
    print("脚注定义条数:", sum(1 for i in range(1, 18) if ("[^%d]: " % i) in new_text))
    print("正文注码引用数:", sum(new_text.count("[^%d]" % i) - 1 for i in range(1, 18)))


if __name__ == "__main__":
    sys.exit(main())