# 前向被引实查（OpenAlex）：Walters 2023 / Ping&Wang 2024 的被引 + 侯的 2022 题录查找
import json
import urllib.parse
import urllib.request

UA = {"User-Agent": "xiyouji-literature-map/1.0 (mailto:research@example.org)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def show_citing(doi, label):
    try:
        w = get("https://api.openalex.org/works/doi:%s?select=id,display_name,cited_by_count,publication_year" % doi)
    except Exception as e:
        print("%s: FETCH FAIL %s" % (label, e))
        return
    wid = w["id"].rsplit("/", 1)[-1]
    print("\n## %s | %s (%s) | 被引 %d" % (label, w["display_name"][:60], w["publication_year"], w["cited_by_count"]))
    try:
        c = get("https://api.openalex.org/works?filter=cites:%s&sort=publication_date:desc&per-page=12&select=display_name,publication_year,doi" % wid)
        for it in c.get("results", []):
            print("  %s | %s | %s" % (it["publication_year"], (it["display_name"] or "")[:88], it.get("doi") or "-"))
    except Exception as e:
        print("  citing FAIL:", e)


show_citing("10.1038/s41598-023-41032-5", "Walters&Wilder 2023")
show_citing("10.1093/llc/fqad085", "Ping&Wang 2024 DSH")

print("\n## 侯的 2022 题录查找（OpenAlex title search）")
try:
    q = urllib.parse.urlencode({"filter": "title.search:历史时期信息传播网络的重建 邮政网络", "per-page": 3,
                                "select": "display_name,publication_year,doi,primary_location"})
    r = get("https://api.openalex.org/works?" + q)
    if not r.get("results"):
        print("  0 hit（中文刊在 OpenAlex 覆盖外——被引链改走 CNKI）")
    for it in r["results"]:
        src = ((it.get("primary_location") or {}).get("source") or {}).get("display_name")
        print("  %s | %s | %s | %s" % (it["publication_year"], (it["display_name"] or "")[:60], src, it.get("doi")))
except Exception as e:
    print("  FAIL:", e)
