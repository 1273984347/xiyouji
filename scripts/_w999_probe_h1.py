import re

for ch in ["ch001", "ch022", "ch089", "ch003", "ch066"]:
    p = "site/reader/%s.html" % ch
    s = open(p, encoding="utf-8").read()
    hs = [m.start() for m in re.finditer(r"</h1>", s)]
    h1o = [m.start() for m in re.finditer(r"<h1[^>]*>", s)]
    fig = s.find('<figure class="chapter-plate"')
    head = s.find("</head>")
    body = s.find("<body")
    print("%-8s </h1>x%d @%s | <h1> 位置 %s | head末=%d body首=%d | figure@%d %s"
          % (ch, len(hs), hs[:3], h1o[:3], head, body, fig,
             "<<< figure 在 head 内" if 0 <= fig < head else ""))
