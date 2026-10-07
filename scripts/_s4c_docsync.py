"""_s4c_docsync.py — S4 C 轨：大纲与规划档状态同步（2026-09-28 投稿前打磨批次）"""
import io
import re
import sys

MAIN = r"D:\xiyouji\docs\S4-学术投稿\可验证性方向-投稿版.md"
OUT = r"D:\xiyouji\docs\S4-学术投稿\可验证性方向-论文三大纲.md"
PLAN = r"D:\xiyouji\docs\S4-学术投稿\学术投稿规划-三路线论文选题大纲与目标刊分级.md"


def load(p):
    return io.open(p, encoding="utf-8").read()


def save(p, s):
    io.open(p, "w", encoding="utf-8", newline="\r\n").write(s)


def rep(s, old, new, n=1, label=""):
    c = s.count(old)
    assert c == n, "[%s] 计数 %d != %d" % (label, c, n)
    return s.replace(old, new)


def main():
    body = load(MAIN)
    # 正文字符数（去空白·去元信息头与文末内部节外的口径提示：仅统计报数供规划档引用）
    n_chars = len(re.sub(r"\s+", "", body))
    print("main chars (no-ws):", n_chars)

    out = load(OUT)
    out = rep(out,
              "> 增补：2026-09-26 前置核查完成（待办 1/2）——动机链逐条 Crossref/官方页核验、撞题终判修订「quote 级缺位」表述（详见 [同行文献库](同行文献库-三方向检索存档.md) 第三节 3.3/3.4）；全文初稿另出（[可验证性方向-投稿版.md](可验证性方向-投稿版.md)）",
              "> 增补：2026-09-26 前置核查完成（待办 1/2）——动机链逐条 Crossref/官方页核验、撞题终判修订「quote 级缺位」表述（详见 [同行文献库](同行文献库-三方向检索存档.md) 第三节 3.3/3.4）；全文初稿另出（[可验证性方向-投稿版.md](可验证性方向-投稿版.md)）\n"
              "> 增补：2026-09-28 投稿前打磨——注释脚注化（《中国社会科学》2026 年修订格式·Markdown 脚注承载）+ 英文摘要润色 + 系统配图 4 幅（图表/ C-图1~C-图4·实测输出重绘）+ 匿名稿产出 + 快照数同步（437/842）",
              label="outline-add")
    out = rep(out,
              "| 引文核验实证 | **433 条引文行 100% 命中（2026-09-27 终测快照·841 文件·含本文自带 4 条与门禁加固新纳入 3 条）** | 已复测 |",
              "| 引文核验实证 | **437 条引文行 100% 命中（2026-09-28 终测快照·842 文件·含本文两稿自带 8 条与门禁加固新纳入 3 条）** | 已复测 |\n"
              "| 系统配图 4 幅（体系图/锚点查询/校验输出/门禁运行） | [图表/](图表/) C-图1~C-图4（SVG 源 + PNG 2×·实测输出重绘） | 已出（2026-09-28） |",
              label="outline-material")
    out = rep(out,
              "4. 匿名稿与英文 short paper 版本；投稿前：CNKI 查重 + 《数字人文》当期体例复核（注释脚注化）",
              "4. 匿名稿与英文 short paper 版本——**匿名稿已出（`可验证性方向-匿名稿.md`·2026-09-28·双盲脱敏面 = 头部两行 / [^15] 仓库表述 / 关联文档节）**；英文 short paper 待后续批次\n"
              "5. 投稿前（待办）：CNKI 全库查重 + Word 版生成（页下注与图版）+ Lancet 勘误内容复核 + 刊方当期样文终校",
              label="outline-todo")
    save(OUT, out)
    print("outline updated")

    plan = load(PLAN)
    plan = rep(plan,
               "## 六、论文三（C 轨）：DH 可验证性基础设施（全新撰写·独特性最高）\n\n**建议选题**",
               "## 六、论文三（C 轨）：DH 可验证性基础设施（全新撰写·独特性最高）\n\n"
               "> **2026-09-28 投稿前打磨完毕**：全文稿与匿名稿双稿（`可验证性方向-投稿版.md` / `-匿名稿.md`）+ 4 幅系统配图（图表/ C-图1~C-图4）+ 注释脚注化（《中国社会科学》2026 年修订格式）与英文摘要润色；余 CNKI 查重、Word 版生成、刊方样文终校留待投稿前执行。\n\n"
               "**建议选题**",
               label="plan-c3")
    save(PLAN, plan)
    print("plan updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())