"""S4 全目录有据可依复核①：清单内全部 DOI/arXiv 外部库逐条比对（2026-10-06·一次性）。"""
import json
import re
import ssl
import time
import urllib.request

ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TraeAudit/1.0"
S4 = r"d:\xiyouji\docs\S4-学术投稿"
FILES = [S4 + r"\文献\00-文献清单.md", S4 + r"\同行文献库-三方向检索存档.md", S4 + r"\艺术学四类文献-参考与借鉴工作稿.md"]

text = ""
for f in FILES:
    text += open(f, encoding="utf-8").read() + "\n"

dois = sorted(set(re.findall(r"10\.\d{4,9}/[A-Za-z0-9._;()/:+<>-]+", text)))
dois = [d.rstrip(".。，,;；)）]").rstrip(")") for d in dois]
arxiv = sorted(set(re.findall(r"arXiv:(\d{4}\.\d{4,5})", text)))
print("DOI 共 %d 个 | arXiv 共 %d 个\n" % (len(dois), len(arxiv)))


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout, context=ctx).read().decode("utf-8", "ignore")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())[:60]


for d in dois:
    try:
        j = json.loads(get("https://api.crossref.org/works/" + urllib.request.quote(d)))
        t = (j["message"].get("title") or [""])[0]
        print("[OK ] %s | %s" % (d[:56], t[:60]))
    except Exception as ex:
        code = getattr(ex, "code", "")
        print("[%s] %s" % ("404" if code == 404 else "ERR", d[:70]))
    time.sleep(0.4)

print()
for a in arxiv:
    try:
        x = get("http://export.arxiv.org/api/query?id_list=" + a)
        m = re.search(r"<entry>.*?<title>(.*?)</title>", x, re.S)
        ok = m and "Error" not in x and m.group(1).strip() != ""
        print("[%s] arXiv:%s | %s" % ("OK " if ok else "MIS", a, re.sub(r"\s+", " ", (m.group(1) if m else "")).strip()[:70]))
    except Exception as ex:
        print("[ERR] arXiv:%s %s" % (a, repr(ex)[:50]))
    time.sleep(0.4)
