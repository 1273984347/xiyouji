"""按川大三方向直取北服 10 件（2026-10-06·一次性）。"""
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
    ("设计口述史", "2025_Cheng-Song_设计口述史当代设计史研究路径_艺术设计研究2025-5.pdf"),
    ("存在论转向", "2025_Mo_从造物到设计物观念存在论转向_艺术设计研究2025-5.pdf"),
    ("罗兰 · 巴特", "2026_Peng_罗兰巴特设计批评另类模式_艺术设计研究2026-4.pdf"),
    ("设计师身份的变迁", "2025_Hong-Luo_生成式AI时代设计师身份变迁_艺术设计研究2025-6.pdf"),
    ("持扇肖像画", "2026_Li-Tian_跨文化艺术史欧洲女性持扇肖像_艺术设计研究2026-4.pdf"),
    ("图画与屏幕", "2025_Lu_实物图画与屏幕美术史观看对象_艺术设计研究2025-4.pdf"),
    ("撒马尔罕", "2026_Cheng_撒马尔罕大使厅北壁壁画重考_艺术设计研究2026-4.pdf"),
    ("研究范式建构", "2026_Song_新时代中国设计研究范式建构_艺术设计研究2026-3.pdf"),
    ("卫生宣传画", "2025_Gan-Fang-Huang_新中国十七年卫生宣传画_艺术设计研究2025-6.pdf"),
    ("石器时代的设计学", "2025_Li-Luo_石器时代的设计学AI反思_艺术设计研究2025-5.pdf"),
]


def get(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://yssjyj.bift.edu.cn/"})
    return urllib.request.urlopen(req, timeout=timeout, context=ctx).read()


items = json.load(open(r"d:\xiyouji\scripts\_s4_bift_all400.json", encoding="utf-8"))
meta = []
for k, fname in PICKS:
    hit = next((a for a in items if k in re.sub(r"<br\s*/?>", "", a.get("Title") or "")), None)
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
    t = re.sub(r"\s+|<br\s*/?>", " ", hit.get("Title") or "")
    print("[OK] %2d 页 %7d B | %s | %s | %s | %s-%s" % (n, os.path.getsize(path), fname[:52], au, hit.get("YearIssue_No"), hit.get("Page_Num"), hit.get("Page_NumEnd")))
    meta.append({"file": fname, "title": t.strip(), "authors": au, "issue": hit.get("YearIssue_No"),
                 "pages": "%s-%s" % (hit.get("Page_Num"), hit.get("Page_NumEnd")), "size": os.path.getsize(path)})
json.dump(meta, open(r"d:\xiyouji\scripts\_s4_dir_picks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n完成 %d/10" % len(meta))
