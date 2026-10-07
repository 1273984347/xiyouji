"""补充批 6 件直取（跨文化图像/画论/交互理论·2026-10-06·一次性）。"""
import json
import logging
import os
import re
import ssl
import urllib.request

logging.disable(logging.CRITICAL)
from pypdf import PdfReader

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
B = "https://yssjyj.bift.edu.cn/api/api/Web/"
DEST = r"d:\xiyouji\docs\S4-学术投稿\06-文献"

PICKS = [
    ("意大利纺织图册", "2025_Li-Chen_意大利纺织图册早期时尚传播_艺术设计研究2025-6.pdf"),
    ("西渐", "2025_Xi-Yan-Zhang_丝路视域中国时尚文化西渐_艺术设计研究2025-6.pdf"),
    ("超越符号", "2025_Liang-Dong_服饰形象跨文化传播文明统一性_艺术设计研究2025-6.pdf"),
    ("集古树石画稿", "2026_Yang_集古树石画稿与南北宗论双重建构_艺术设计研究2026-1.pdf"),
    ("可穿戴健康交互设计", "2026_Han-Yao-Qiu_可穿戴健康交互器物到界面转向_艺术设计研究2026-4.pdf"),
    ("范式分野", "2026_Hu_中西方时尚理论研究范式分野_艺术设计研究2026-1.pdf"),
]


def get(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://yssjyj.bift.edu.cn/"})
    return urllib.request.urlopen(req, timeout=timeout, context=ctx).read()


items = json.load(open(r"d:\xiyouji\scripts\_s4_bift_all400.json", encoding="utf-8"))
meta = []
for k, fname in PICKS:
    hit = next((a for a in items if k in re.sub(r"<br\s*/?>", " ", a.get("Title") or "")), None)
    if not hit:
        print("[未找到]", k); continue
    path = os.path.join(DEST, fname)
    if not os.path.exists(path):
        d = get(B + "OpenArticleFilebyGuidNew?Id=%s" % hit.get("PDFFileNameUrlGUID"))
        if d[:4] != b"%PDF":
            print("[非PDF]", k); continue
        open(path, "wb").write(d)
    n = len(PdfReader(path).pages)
    au = re.sub(r"\s+", " ", hit.get("AuthorsList") or "")
    t = re.sub(r"\s+|<br\s*/?>", " ", hit.get("Title") or "").strip()
    print("[OK] %2d 页 %8d B | %s | %s | %s | %s-%s" % (n, os.path.getsize(path), fname[:50], au, hit.get("YearIssue_No"), hit.get("Page_Num"), hit.get("Page_NumEnd")))
    meta.append({"file": fname, "title": t, "authors": au, "issue": hit.get("YearIssue_No"),
                 "pages": "%s-%s" % (hit.get("Page_Num"), hit.get("Page_NumEnd")), "size": os.path.getsize(path)})
json.dump(meta, open(r"d:\xiyouji\scripts\_s4_final_picks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n完成 %d/6" % len(meta))
