"""S4 文献补全（fetch21）：ACM/TF 页面正文 → 清理 → HTML → PDF 转存（2026-10-05）。
命名：【页面转存版】；HTML 头部含来源/许可/完整性声明。
"""
import os
import re
import subprocess

TMPE = r"d:\xiyouji\tmpe"
DEST = r"d:\xiyouji\docs\S4-学术投稿\06-文献"

CONFIGS = [
    {
        "key": "ACM",
        "txt": os.path.join(TMPE, "acm_fulltext.txt"),
        "out_pdf": os.path.join(DEST, "2025_Chen-Xie-Yu_西游法宝交互可视化系统_VINCI【页面转存版】.pdf"),
        "title": "From Myth to Interface: An AI-Augmented Interactive Visual System for Exploring Artifact Interactions in Journey to the West",
        "source": "https://dl.acm.org/doi/10.1145/3769534.3769615",
        "venue": "VINCI '25 / ACM DL（Article 58, pp.1-8）",
        "license": "CC BY-NC-ND 4.0（ACM DL 页面声明：Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License）",
        "start": ("last-before", "Abstract", "We developed an AI-assisted"),
        "end": ("first", "Index Terms"),
        "noise_lines": [r"^Citation$", r"^\(Open in a new window\)$", r"^Google Scholar$", r"^Web of Science.*$", r"^Crossref.*$"],
    },
    {
        "key": "TF",
        "txt": os.path.join(TMPE, "tf_fulltext.txt"),
        "out_pdf": os.path.join(DEST, "2026_Rhee-Kim_Simdogihaeng行记空间化_JAABE【页面转存版】.pdf"),
        "title": "Spatializing Simdogihaeng travelogue (1906): place recognition and heritage authorization on Ganghwa Island",
        "source": "https://www.tandfonline.com/doi/full/10.1080/13467581.2026.2730906",
        "venue": "Journal of Asian Architecture and Building Engineering（T&F·Published online 22 Sep 2026）",
        "license": "CC BY-NC 4.0（Crossref 核实；期刊页标注 Open access）",
        "start": ("first-after", "ABSTRACT", 1400),
        "end": ("after-lines-before", "Xiaopeng Sun et al.", 2),
        "noise_lines": [r"^Citation$", r"^\(Open in a new window\)$", r"^Google Scholar$", r"^Web of Science.*$", r"^Crossref.*$", r"^Sign me up$", r"^×$",
                        r"^PubMed$", r"^Download PDF$", r"^Share$", r"^Related research$", r"^People also read$", r"^Recommended articles$", r"^Cited by.*$", r"^View more$"],
    },
]


def find_start(t, cfg):
    kind = cfg["start"][0]
    if kind == "first-after":
        marker, after = cfg["start"][1], cfg["start"][2]
        return t.find(marker, after)
    marker, rel = cfg["start"][1], cfg["start"][2]
    anchor = t.find(rel)
    return t.rfind(marker, max(0, anchor - 400), anchor)


def find_end(t, cfg, start):
    kind = cfg["end"][0]
    marker = cfg["end"][1]
    if kind == "after-lines-before":
        n = cfg["end"][2]
        anchor = t.find(marker, start)
        if anchor <= 0:
            return len(t)
        cut = anchor
        for _ in range(n):
            prev = t.rfind("\n", 0, cut)
            if prev <= 0:
                return cut
            cut = prev
        return cut
    i = t.find(marker, start)
    return i if i > 0 else len(t)


def clean(text, noise_lines):
    lines = [l.rstrip() for l in text.split("\n")]
    pats = [re.compile(p) for p in noise_lines]
    out = [l for l in lines if not any(p.match(l.strip()) for p in pats)]
    s = "\n".join(out)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


HTML_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: "Segoe UI", "Microsoft YaHei", serif; font-size: 10.5pt; line-height: 1.6; color: #1a1a1a; max-width: 720px; margin: 0 auto; padding: 0 6px; }}
  .prov {{ border: 1.2px solid #8b1f1f; background: #fbf7f3; padding: 10px 14px; font-size: 9pt; color: #333; margin-bottom: 20px; }}
  .prov b {{ color: #8b1f1f; }}
  h1 {{ font-size: 15.5pt; line-height: 1.35; margin: 0 0 4px; }}
  .venue {{ font-size: 9.5pt; color: #555; margin-bottom: 14px; }}
  pre {{ white-space: pre-wrap; word-wrap: break-word; font-family: inherit; margin: 0; }}
</style>
</head>
<body>
<div class="prov">
  <b>文本转存版（非出版社排版）</b><br>
  来源：{source}<br>
  刊载：{venue}<br>
  获取方式：2026-10-05 经 Edge 浏览器加载期刊页面后提取正文转存（PDF 二进制传输受网络限制，页面正文可用）<br>
  许可：{license}<br>
  完整性说明：正文、参考文献均含；页面导航/控件等杂质已尽力清理，版式与页码请以出版社原文为准。<br>
  S4 文献库·本地研究存档
</div>
<h1>{title}</h1>
<div class="venue">{venue}</div>
<pre>{body}</pre>
</body>
</html>"""


def main():
    for cfg in CONFIGS:
        t = open(cfg["txt"], encoding="utf-8").read()
        # 许可线索探测
        lic_hits = re.findall(r"(?i)(creative commons[^\n]{0,90}|CC[ -]BY[^\n]{0,50}|open access[^\n]{0,60})", t)
        if lic_hits:
            print("[%s] 许可线索: %s" % (cfg["key"], lic_hits[:3]))
        s = find_start(t, cfg)
        e = find_end(t, cfg, s if s > 0 else 0)
        if s < 0:
            print("[%s] 起始未找到，跳过" % cfg["key"])
            continue
        body = clean(t[s:e], cfg["noise_lines"])
        print("[%s] 裁剪 %d→%d | 清理后 %d 字符" % (cfg["key"], s, e, len(body)))
        print("[%s] 头 160: %s" % (cfg["key"], body[:160].replace("\n", " | ")))
        print("[%s] 尾 160: %s" % (cfg["key"], body[-160:].replace("\n", " | ")))
        html = HTML_TMPL.format(source=cfg["source"], venue=cfg["venue"], title=cfg["title"],
                                license=cfg["license"], body=body)
        hp = os.path.join(TMPE, "_s4_%s.html" % cfg["key"].lower())
        with open(hp, "w", encoding="utf-8") as f:
            f.write(html)
        print("[%s] HTML → %s" % (cfg["key"], hp))
        r = subprocess.run(["node", "scripts/_html2pdf.js", hp, cfg["out_pdf"]],
                           capture_output=True, text=True, cwd=r"d:\xiyouji")
        print("[%s] node: %s | %s" % (cfg["key"], (r.stdout or "").strip()[:120], (r.stderr or "").strip()[:160]))
    # 校验
    import pypdf
    for cfg in CONFIGS:
        p = cfg["out_pdf"]
        if os.path.exists(p):
            try:
                rd = pypdf.PdfReader(p)
                print("[%s] PDF OK %d pages %d bytes" % (cfg["key"], len(rd.pages), os.path.getsize(p)))
            except Exception as ex:
                print("[%s] PDF 读取失败: %s" % (cfg["key"], ex))
        else:
            print("[%s] PDF 未生成" % cfg["key"])


if __name__ == "__main__":
    main()
