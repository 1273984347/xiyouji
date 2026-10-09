"""W691 BL-19 下游修复：第 1/2 回引文从节选本措辞迁回真本（35 行 / 31 文件 / 14 句）。

映射为人工策展终表（每句已经 corpus.count>=1 子串验证）；应用后由 check_citations 复验。
"""
import re
import sys

# norm 前缀（去空白后的旧引文前 16 字）→ (新回目, 新引文体)
MAP = [
    ("此山叫做灵台方寸山，山中有座斜月三星洞", 1, "此山叫做灵台方寸山。山中有座斜月三星洞。"),
    ("那洞中有一个神仙，称名须菩提祖师", 1, "那洞中有一个神仙，称名须菩提祖师。"),
    ("见那菩提祖师端坐在台上，两边有三十个小仙侍立", 1, "见那菩提祖师端坐在台上，两边有三十个小仙侍立台下。"),
    ("只见正当中有一石碣，碣上有一行楷书大字", 1, "只见正当中有一石碣。碣上有一行楷书大字，镌着“花果山福地，水帘洞洞天。”"),
    ("你们才说有本事进得来、出得去、不伤身体者", 1, "你们才说有本事进得来，出得去，不伤身体者，就拜他为王。"),
    ("海外有一国土，名曰傲来国。国近大海，海中有一座名山", 1, "海外有一国土，名曰傲来国。国近大海，海中有一座山，唤为花果山。"),
    ("猴王闻之，满心欢喜道", 1, "我明日就辞汝等下山，云游海角，远涉天 涯，务必访此三者，学一个不老长生，常躲过阎君之难。”"),
    ("自此，石猿高登王位，将", 1, "众猴听说，即拱伏无违。一个个序齿排班，朝上礼拜，都称“千岁大王”。"),
    ("众猴听得，个个欢喜，遂都随了石猴进去", 1, "众猴听得，个个欢喜，都道：“你还先走，带我们进去，进去！”"),
    ("毕竟不知向何方去访，且听下回分解", 2, "毕竟不知怎生结果，居此界终始如何，且听下回分解。"),
    ("此山乃十洲之祖脉，三岛之来龙", 1, "此山乃十洲之祖脉，三岛之来龙，自开清浊而立，鸿 蒙判后而成。"),
    ("那座山正当顶上，有一块仙石", 1, "那座山，正当顶上，有一块仙 石。"),
    ("与你起法名叫做", 1, "与你起个法名叫做‘孙悟空’好么？”"),
    ("自今就叫做孙悟空也", 1, "自今就叫做孙悟空也！"),
]


def norm(s):
    return re.sub(r"\s+", "", s)


def main():
    dry = "--dry" in sys.argv
    import subprocess
    r = subprocess.run(["python", "scripts/check_citations.py", "--dir", "docs"],
                       capture_output=True, text=True)
    items = re.findall(r"FAIL (docs/[^\s]+):(\d+) 第(\d+)回未命中", r.stdout)
    assert items, "无失配项（可能已修复）"
    targets = {}
    for f, ln, ch in items:
        targets.setdefault(f, []).append(int(ln))
    print("待修文件", len(targets), "行", len(items))
    fixed = 0
    caches = {}
    for f, lns in targets.items():
        t = open(f, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in t else "\n"
        lines = t.split(nl)
        for ln in lns:
            m = re.match(r"^> 原文引文（第(\d+)回）：(.*)$", lines[ln - 1])
            assert m, f + ":" + str(ln) + " 非规范引文行"
            old_body = norm(m.group(2).strip().strip("“”"))
            hit = None
            for prefix, new_ch, new_body in MAP:
                if old_body.startswith(norm(prefix)[:16]):
                    hit = (new_ch, new_body)
                    break
            assert hit, f + ":" + str(ln) + " 无映射（旧: " + old_body[:30] + "）"
            lines[ln - 1] = "> 原文引文（第%d回）：“%s”" % (hit[0], hit[1])
            fixed += 1
        caches[f] = nl.join(lines)
    if dry:
        print("[DRY] 将修复", fixed, "行")
        return 0
    for f, t in caches.items():
        open(f, "w", encoding="utf-8", newline="").write(t)
    print("已修复", fixed, "行 /", len(caches), "文件")
    r2 = subprocess.run(["python", "scripts/check_citations.py", "--dir", "docs"],
                        capture_output=True, text=True)
    tail = r2.stdout.strip().splitlines()[-1]
    print("复验:", tail)
    if r2.returncode != 0:
        for line in r2.stdout.splitlines():
            if "FAIL" in line:
                print("  残留", line)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
