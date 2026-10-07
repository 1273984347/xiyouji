# _s4_reorg_links.py — S4 分类整理断链检查/修复（一次性·--check 只报 | --fix 断言修复）
import os
import re
import sys

ROOT = r"D:\xiyouji\docs\S4-学术投稿"
LINK = re.compile(r"\]\(([^)#\s]+\.(?:md|docx))\)")

MOVES = {
    # 00-决策导航
    "稿件决策清单-2026-10-07.md": "00-决策导航/稿件决策清单-2026-10-07.md",
    "投稿渠道矩阵-2026-10-07.md": "00-决策导航/投稿渠道矩阵-2026-10-07.md",
    "投稿夹装填清单-2026-10-07.md": "00-决策导航/投稿夹装填清单-2026-10-07.md",
    # 01-论文
    "明清小说方向-投稿版.md": "01-论文/明清小说方向-投稿版.md",
    "明清小说方向-匿名稿.md": "01-论文/明清小说方向-匿名稿.md",
    "可验证性方向-投稿版.md": "01-论文/可验证性方向-投稿版.md",
    "可验证性方向-匿名稿.md": "01-论文/可验证性方向-匿名稿.md",
    "可验证性方向-投稿版.docx": "01-论文/可验证性方向-投稿版.docx",
    "可验证性方向-英文short-paper.md": "01-论文/可验证性方向-英文short-paper.md",
    "心学方向-投稿版.md": "01-论文/心学方向-投稿版.md",
    "心学方向-匿名稿.md": "01-论文/心学方向-匿名稿.md",
    # 02-大纲与规划
    "可验证性方向-论文三大纲.md": "02-大纲与规划/可验证性方向-论文三大纲.md",
    "艺术学论文四大纲-2026-10-07.md": "02-大纲与规划/艺术学论文四大纲-2026-10-07.md",
    "学术投稿规划-三路线论文选题大纲与目标刊分级.md": "02-大纲与规划/学术投稿规划-三路线论文选题大纲与目标刊分级.md",
    "明清小说方向-体例改造方案与样例-2026-10-06.md": "02-大纲与规划/明清小说方向-体例改造方案与样例-2026-10-06.md",
    # 03-审查与核验
    "审查报告-明清小说方向-2026-09-26.md": "03-审查与核验/审查报告-明清小说方向-2026-09-26.md",
    "审查报告-可验证性方向-2026-10-06.md": "03-审查与核验/审查报告-可验证性方向-2026-10-06.md",
    "审查报告-全目录有据可依复核-2026-10-06.md": "03-审查与核验/审查报告-全目录有据可依复核-2026-10-06.md",
    "引用核验报告-PaperCheck-明清小说方向-2026-10-06.md": "03-审查与核验/引用核验报告-PaperCheck-明清小说方向-2026-10-06.md",
    "引用核验报告-PaperCheck-可验证性方向-2026-10-06.md": "03-审查与核验/引用核验报告-PaperCheck-可验证性方向-2026-10-06.md",
    "数据核验与复现报告-明清小说方向-2026-09-28.md": "03-审查与核验/数据核验与复现报告-明清小说方向-2026-09-28.md",
    "数据核验与复现报告-可验证性方向-2026-09-28.md": "03-审查与核验/数据核验与复现报告-可验证性方向-2026-09-28.md",
    "数据核验与复现报告-全方向复核-2026-10-06.md": "03-审查与核验/数据核验与复现报告-全方向复核-2026-10-06.md",
    # 04-文献研究
    "艺术学四类文献-参考与借鉴工作稿.md": "04-文献研究/艺术学四类文献-参考与借鉴工作稿.md",
    "同行文献库-三方向检索存档.md": "04-文献研究/同行文献库-三方向检索存档.md",
    "文献库计量分析报告-2026-10-06.md": "04-文献研究/文献库计量分析报告-2026-10-06.md",
    "文献综述地图-2026-10-07.md": "04-文献研究/文献综述地图-2026-10-07.md",
}


def all_docs():
    out = []
    for dp, _dn, fn in os.walk(ROOT):
        for f in fn:
            if f.lower().endswith((".md", ".docx")):
                out.append(os.path.join(dp, f))
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    docs = all_docs()
    basenames = {}
    for p in docs:
        basenames.setdefault(os.path.basename(p), []).append(p)
    broken = []
    for p in docs:
        try:
            text = open(p, encoding="utf-8").read()
        except Exception:
            continue  # docx binary
        for m in LINK.finditer(text):
            L = m.group(1)
            if L.startswith(("http", "file:")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), L))):
                broken.append((p, L))
    print("broken links:", len(broken))
    if mode != "--fix":
        for p, L in broken:
            print("  %s  ->  %s" % (os.path.relpath(p, ROOT), L))
        return 0

    def solve(p, L):
        """R1: basename 在 S4 内唯一定位；R2: S4 外目标逐级 ../ 试探。返回新相对串或 None"""
        base = os.path.basename(L)
        cands = list(basenames.get(base, []))
        if "/" in L:
            seg = L.split("/")[0]
            f = [c for c in cands if seg in c.replace("\\", "/").split("/")]
            cands = f or cands
        if len(cands) > 1:
            f = [c for c in cands if not re.search(r"[\/][^\/]*投稿[\/]", c)]
            cands = f or cands
        if len(cands) > 1:
            f = [c for c in cands if os.path.relpath(c, ROOT).replace("\\", "/") in set(MOVES.values())]
            cands = f or cands
        if len(cands) == 1:
            return os.path.relpath(cands[0], os.path.dirname(p)).replace("\\", "/"), "R1"
        for k in (1, 2, 3, 4):
            trial = ("../" * k) + L
            if os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), trial))):
                return trial, "R2"
        return None, None

    byfile = {}
    for p, L in broken:
        byfile.setdefault(p, []).append(L)
    r1 = r2 = 0
    leftovers = []
    touched = set()
    for p, links in sorted(byfile.items()):
        text = open(p, encoding="utf-8").read()
        changed = False
        for L in dict.fromkeys(links):
            newrel, rule = solve(p, L)
            if newrel is None:
                leftovers.append((p, L))
                continue
            old = "](%s)" % L
            n = text.count(old)
            assert n >= 1, "未找到待替换串: %s in %s" % (L, p)
            text = text.replace(old, newrel)
            changed = True
            if rule == "R1":
                r1 += n
            else:
                r2 += n
        if changed:
            open(p, "w", encoding="utf-8", newline="").write(text)
            touched.add(os.path.relpath(p, ROOT))
    print("fixed:", r1 + r2, "(R1=%d R2=%d)" % (r1, r2), "| files:", len(touched), "| leftover:", len(leftovers))
    for p, L in leftovers:
        print("  LEFT %s -> %s" % (os.path.relpath(p, ROOT), L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
