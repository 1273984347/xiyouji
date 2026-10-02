"""_s4c_anon.py — S4 C 轨：AI 使用声明补入 + 匿名稿（双盲脱敏）生成（一次性）

1) 主稿：在「核验与复现」之后补「## AI 使用声明」（对齐 B 轨投稿包的声明实践）
2) 匿名稿 = 主稿镜像 - 脱敏面：
   - 头部两行改为匿名稿说明（不含 S4/目录自指）
   - [^15] 仓库表述补匿名延期说明（对齐 B 轨「项目信息随作者信息提供」口径）
   - 移除「## 关联文档」（内部导航链接）
   其余内容逐字镜像（diff 面仅限脱敏项）。
"""
import io
import sys

MAIN = r"D:\xiyouji\docs\S4-学术投稿\学术论文C轨-可验证性基础设施.md"
ANON = r"D:\xiyouji\docs\S4-学术投稿\学术论文C轨-可验证性基础设施-匿名稿.md"

AI_SECTION = """## AI 使用声明

本文的生产过程使用生成式 AI 工具（TraeCode agent·DeepSeek-V4.1-Flash）：线索整理、结构建议与文字草稿由 AI 辅助生成，研究设计、系统实现、核心论证与最终文字由作者逐条审定并承担责任。文中全部原著引文行均经引文校验脚本对公开底本电子文本逐字命中核验，外部文献题录均经 Crossref API 或官方页面复核（记录见文末「核验与复现」）；本文所报告的工具与方法即核验基础设施本身，其全部判定可由任何第三方以公开材料独立重跑。AI 工具未署名为作者，未参与判定标准的制定。

"""


def rep(s, old, new, n=1, label=""):
    c = s.count(old)
    assert c == n, "替换计数异常 [%s] 期望 %d 实得 %d :: %s" % (label, n, c, old[:50])
    return s.replace(old, new)


def main():
    text = io.open(MAIN, encoding="utf-8").read()

    # ---------- 1) 主稿补 AI 使用声明（置于 核验与复现 与 关联文档 之间）----------
    if "## AI 使用声明" not in text:
        text = rep(text, "\n---\n\n## 关联文档\n",
                   "\n---\n\n" + AI_SECTION + "---\n\n## 关联文档\n",
                   label="ai-section")
        io.open(MAIN, "w", encoding="utf-8", newline="\r\n").write(text)
        print("main updated: AI 使用声明 inserted")
    else:
        print("main: AI 使用声明 already present")

    # ---------- 2) 由主稿生成匿名稿 ----------
    anon = text
    anon = rep(anon,
               "> S4 学术投稿 · 论文三（C 轨） · 2026-09-28（脚注体例与配图版）\n"
               "> 生成来源：TraeCode agent 执笔（academic-writing skill 辅助·基于本目录 C 轨大纲与项目实证）",
               "> 匿名稿 · 投稿用 · 不含作者信息与项目自指\n"
               "> 双盲评审版（改编自同名稿 2026-09-28·脚注体例与配图同步）\n"
               "> 生成来源：TraeCode agent 执笔（academic-writing skill 辅助·基于项目实证）",
               label="anon-header")
    anon = rep(anon,
               "上述工具与底本语料、被核验内容同在项目公开仓库发布，版本以投稿时冻结的版本为准。",
               "上述工具与底本语料、被核验内容同在项目公开仓库发布（匿名：仓库地址与项目信息在评审通过后随作者信息一并提供），版本以投稿时冻结的版本为准。",
               label="anon-repo")
    i = anon.find("\n---\n\n## 关联文档\n")
    assert i > 0, "未定位到关联文档节"
    anon = anon[:i] + "\n"

    io.open(ANON, "w", encoding="utf-8", newline="\r\n").write(anon)
    print("anon written:", ANON)

    # ---------- 3) diff 面统计（应仅限脱敏项）----------
    a = text.split("\n")
    b = anon.split("\n")
    import difflib
    diff = [l for l in difflib.unified_diff(a, b, lineterm="", n=0)][2:]
    print("diff lines:", len(diff))
    for l in diff:
        print("  ", l)


if __name__ == "__main__":
    sys.exit(main())