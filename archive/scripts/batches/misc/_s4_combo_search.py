# _s4_combo_search.py — 三方向组合检索式机跑（OpenAlex/arXiv·2026-10-07）
# 已知 DOI 集用于去重：命中分「新发现」与「已覆盖」
import json
import urllib.parse
import urllib.request

UA = {"User-Agent": "xiyouji-literature-map/1.0 (mailto:research@example.org)"}

KNOWN = {
    "10.1038/s41598-023-41032-5", "10.48550/arXiv.2605.07723", "10.48550/arXiv.2607.09774",
    "10.48550/arXiv.2607.00738", "10.48550/arXiv.2607.22693", "10.48550/arXiv.2602.23452",
    "10.48550/arXiv.2602.06718", "10.48550/arXiv.2604.26835", "10.48550/arXiv.2601.18724",
    "10.1080/08989621.2026.2645390", "10.3897/ese.2025.e153973", "10.1007/s10676-026-09921-1",
    "10.24069/sep.2026.11.48", "10.1371/journal.pone.0347253", "10.1371/journal.pone.0351327",
    "10.1093/llc/fqad085", "10.1080/13467581.2026.2730906",
}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def openalex(label, search, since="2025-06-01", n=10):
    q = urllib.parse.urlencode({
        "search": search, "filter": "from_publication_date:%s" % since,
        "sort": "publication_date:desc", "per-page": n,
        "select": "display_name,publication_date,doi,primary_location"})
    try:
        r = get("https://api.openalex.org/works?" + q)
    except Exception as e:
        print("\n## %s | FAIL %s" % (label, e))
        return
    print("\n## %s | 命中 %d（显示前 %d）" % (label, r.get("meta", {}).get("count", 0), len(r.get("results", []))))
    for it in r.get("results", []):
        doi = (it.get("doi") or "-").replace("https://doi.org/", "")
        tag = "已知" if doi in KNOWN else "新?"
        src = ((it.get("primary_location") or {}).get("source") or {}).get("display_name") or "-"
        print("  [%s] %s | %s | %s | %s" % (tag, it.get("publication_date"), (it["display_name"] or "")[:78], src[:36], doi))


def arxiv(label, q, n=10):
    q = urllib.parse.urlencode({"search_query": q, "sortBy": "submittedDate",
                                "sortOrder": "descending", "max_results": n})
    try:
        req = urllib.request.Request("http://export.arxiv.org/api/query?" + q, headers=UA)
        import re
        with urllib.request.urlopen(req, timeout=30) as r:
            xml = r.read().decode("utf-8", "ignore")
        entries = re.findall(r"<entry>(.*?)</entry>", xml, re.S)
    except Exception as e:
        print("\n## %s | FAIL %s" % (label, e))
        return
    print("\n## %s | 命中 %d（显示前 %d）" % (label, len(entries), len(entries)))
    for e in entries:
        title = re.sub(r"\s+", " ", (re.search(r"<title>(.*?)</title>", e, re.S).group(1))).strip()
        eid = re.search(r"<id>http://arxiv.org/abs/(.*?)</id>", e).group(1)
        date = re.search(r"<published>(\d{4}-\d{2})", e).group(1)
        doi = "10.48550/arXiv." + eid.split("v")[0]
        tag = "已知" if doi in KNOWN else "新?"
        print("  [%s] %s | %s | arXiv:%s" % (tag, date, title[:82], eid))


# C 可验证性方向
openalex("C-组合式（OpenAlex·2025H2 起）",
         "hallucinated citations OR phantom references OR fabricated references large language models")
arxiv("C-组合式（arXiv·最新）",
      'all:"hallucinated citations" OR all:"phantom references" OR all:"fabricated references"')
# A 明清小说方向（英文层）
openalex("A-英文层（GIS×行记/驿路·中国）",
         '"post road" OR "postal network" OR "travelogue" GIS China historical reconstruction', n=8)
# 翻译传播（储-1）
openalex("翻译传播（西游记英译×计量/接受）",
         '"Journey to the West" translation OR retranslation OR stylometry OR reception', n=10)
# 跨媒介游戏（储-2）
openalex("跨媒介游戏（黑神话×传播/接受）",
         '"Black Myth" Wukong transmedia OR reception OR cultural', n=8)
