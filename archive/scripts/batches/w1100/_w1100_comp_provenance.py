# -*- coding: utf-8 -*-
"""W1100 关键验证：补偿规则是否各页同源（同模板复制）？⇒ 决定「按令牌匹配」
能否从共享层/生成链一次根治（而非逐页改 20130 条）。"""
import collections
import io
import os
import pathlib
import re

ROOT = pathlib.Path(r"D:\xiyouji")
SITE = ROOT / "site"
RX = re.compile(r"^\s*([^\n{]*\[fill[^\n{]*)\{([^}]*)\}\s*$", re.M)


def main():
    per_page = {}
    for dirpath, _d, files in os.walk(SITE):
        if any(p.startswith(".") for p in dirpath.split(os.path.sep)):
            continue
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = pathlib.Path(dirpath) / fn
            rel = str(p.relative_to(SITE)).replace("\\", "/")
            txt = p.read_text(encoding="utf-8", errors="ignore")
            styles = "\n".join(m.group(1) for m in
                               re.finditer(r"<style\b[^>]*>(.*?)</style>", txt, re.S))
            rules = []
            for m in RX.finditer(styles):
                sel = " ".join(m.group(1).split())
                if "[fill" in sel:
                    rules.append((sel, " ".join(m.group(2).split())))
            if rules:
                per_page[rel] = rules

    print("含 [fill... 补偿规则的页数：%d" % len(per_page))
    sigs = collections.Counter()
    for rel, rules in per_page.items():
        sigs[tuple(sorted(rules))] += 1
    print("不同规则集合（指纹）数量：%d" % len(sigs))
    for sig, n in sigs.most_common(5):
        print("   指纹命中 %4d 页 · 规则数 %d" % (n, len(sig)))
    # 最常见指纹的样子
    sig, n = sigs.most_common(1)[0]
    print("\n=== 最常见指纹（前 8 条 · 命中 %d 页）===" % n)
    for sel, body in list(sig)[:8]:
        print("   %s { %s }" % (sel[:96], body[:60]))
    # 第二指纹差异（看是否只有个别色不同）
    if len(sigs) > 1:
        s2 = sigs.most_common(2)[1][0]
        print("\n=== 次常见指纹（命中 %d 页）与首指纹的差异条数 ===" % sigs.most_common(2)[1][1])
        a = set(sig)
        b = set(s2)
        print("   仅首指纹有：%d 条 · 仅次指纹有：%d 条 · 共有：%d 条"
              % (len(a - b), len(b - a), len(a & b)))
        for x in list(a - b)[:3]:
            print("     -", x[0][:90])
        for x in list(b - a)[:3]:
            print("     +", x[0][:90])
    # 规则写在页内 <style> 还是外部文件？
    ext = []
    for dirpath, _d, files in os.walk(SITE):
        for fn in files:
            if fn.endswith(".css"):
                p = pathlib.Path(dirpath) / fn
                txt = p.read_text(encoding="utf-8", errors="ignore")
                if "[fill" in txt:
                    ext.append((str(p.relative_to(SITE)).replace("\\", "/"),
                                len(re.findall(r"\[fill", txt))))
    print("\n=== 外部 CSS 中的 [fill 规则（%d 个文件）===" % len(ext))
    for x in ext[:10]:
        print("   %-46s %d 处" % x)


if __name__ == "__main__":
    main()
