# -*- coding: utf-8 -*-
"""_w987_family_scan.py — W987 水墨意境卡族盘点 + 回目页插入点实测

盘点三件事（供登记与验收用）：
  ① 族成员：`site/static/images/card-*.webp` + `chap-*.webp`（数量 / 尺寸分布 / 画风族）
  ② 引用现状：这些文件在全站 HTML 中的被引用次数
  ③ 插入点：6 个目标回目页的「首个 <h2>」行号（唯一性校验）

输出：scripts/output/_w987_family_scan.json
用法：py -3 scripts/_w987_family_scan.py
"""
import io
import json
import os
import re
import sys

REPO = r"D:\xiyouji"
IMG = os.path.join(REPO, "site", "static", "images")
OUT = os.path.join(REPO, "scripts", "output", "_w987_family_scan.json")

TARGETS = ["ch007", "ch014", "ch015", "ch023", "ch027", "ch030"]
RE_H2 = re.compile(r"^\s*<h2>", re.M)
RE_SCENE = re.compile(r'class="chapter-scene"')


def main() -> int:
    members = []
    for fn in sorted(os.listdir(IMG)):
        if re.match(r"^(card|chap)-.*\.webp$", fn):
            members.append(fn)

    # 引用扫描（全站 HTML）
    refs = {}
    html_root = os.path.join(REPO, "site")
    for dirpath, _dirs, files in os.walk(html_root):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(dirpath, f)
            try:
                t = io.open(p, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for m in set(re.findall(r"(?:card|chap)-[0-9a-z-]+\.webp", t)):
                refs.setdefault(m, []).append(os.path.relpath(p, REPO).replace("\\", "/"))

    # 尺寸分布（用文件头字节读 PNG/WEBP 尺寸：直接用 PIL）
    try:
        from PIL import Image
        sizes = {}
        for fn in members:
            s = Image.open(os.path.join(IMG, fn)).size
            sizes["%dx%d" % s] = sizes.get("%dx%d" % s, 0) + 1
    except Exception as e:  # pragma: no cover
        sizes = {"<PIL 不可用：%s>" % e: len(members)}

    # 插入点实测
    points = []
    for t in TARGETS:
        p = os.path.join(REPO, "site", "reader", "%s.html" % t)
        lines = io.open(p, encoding="utf-8", newline="").read().split("\n")
        h2 = [i for i, l in enumerate(lines, 1) if re.match(r"^\s*<h2>", l)]
        h1 = [i for i, l in enumerate(lines, 1) if "<h1>" in l]
        plate = [i for i, l in enumerate(lines, 1) if 'class="chapter-plate"' in l]
        scene = [i for i, l in enumerate(lines, 1) if RE_SCENE.search(l)]
        points.append({
            "page": t, "h1": h1[:1], "chapter_plate": plate[:1], "chapter_scene": scene,
            "first_h2": h2[:1], "h2_count": len(h2),
            "insert_before_line": (h2[0] if h2 else None),
        })

    data = {
        "family": {
            "card_count": len([m for m in members if m.startswith("card-")]),
            "chap_count": len([m for m in members if m.startswith("chap-")]),
            "total": len(members),
            "size_distribution": sizes,
            "referenced_files": len(refs),
            "referenced_count": sum(len(v) for v in refs.values()),
        },
        "members": members,
        "references": {k: v[:3] for k, v in sorted(refs.items())},
        "insert_points": points,
    }
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(
        json.dumps(data, ensure_ascii=False, indent=2))

    fam = data["family"]
    print("族成员：card-* %d 张 + chap-* %d 张 = %d 张" % (fam["card_count"], fam["chap_count"], fam["total"]))
    print("尺寸分布：%s" % fam["size_distribution"])
    print("引用现状：被引用的文件 %d 个 · 引用点 %d 处" % (fam["referenced_files"], fam["referenced_count"]))
    for p in points:
        print("  %-7s h1=%s 题图=%s 首个h2=%s（唯一=%s） 已有场景图=%s" % (
            p["page"], p["h1"], p["chapter_plate"], p["first_h2"],
            p["h2_count"] == 1, len(p["chapter_scene"])))
    print("报告：%s" % OUT)
    bad = [p["page"] for p in points if not p["first_h2"]]
    if bad:
        print("WARN  未找到 <h2> 的页：%s" % ", ".join(bad))
    else:
        print("插入点就绪：6/6 页首个 <h2> 均可定位（页面 h2 总数分别为 %s）" %
              ", ".join("%s=%d" % (p["page"], p["h2_count"]) for p in points))
    return 0


if __name__ == "__main__":
    sys.exit(main())
