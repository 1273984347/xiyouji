"""_s4_biblio_analysis.py — S4 学术投稿文献库计量分析（一次性·只读）

用途：解析 docs/S4-学术投稿/06-文献/00-文献清单.md 的「已存资料」表，
      结合同目录实际 PDF 清单，输出年份/渠道/方向/语种/许可 五维分布。
只读：不修改任何源文件；结果打印到 stdout 并写入 tmpe/s4_biblio_stats.json。
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(r"d:\xiyouji")
LIST_MD = ROOT / "docs" / "S4-学术投稿" / "06-文献" / "00-文献清单.md"
PDF_DIR = ROOT / "docs" / "S4-学术投稿" / "06-文献"
OUT = ROOT / "tmpe" / "s4_biblio_stats.json"

CJK = re.compile(r"[\u4e00-\u9fff]")


def split_row(line: str) -> list[str]:
    """Markdown 表格行 -> 单元格列表（去首尾空单元）。"""
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def parse_rows(md: str) -> list[dict]:
    rows: list[dict] = []
    current_headers: list[str] = []
    for line in md.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = split_row(s)
        if all(set(c) <= set("-: ") for c in cells if c):
            continue  # 分隔行
        if cells and cells[0] == "文件":  # 表头
            current_headers = cells
            continue
        if not cells or "`" not in cells[0]:
            continue
        m = re.search(r"`([^`]+\.pdf)`", cells[0])
        if not m:
            continue
        fname = m.group(1)
        rec = {"file": fname}
        for i, c in enumerate(cells):
            key = current_headers[i] if i < len(current_headers) else f"col{i}"
            rec[key] = c
        rows.append(rec)
    return rows


def venue_from_filename(fname: str) -> str:
    stem = re.sub(r"\.pdf$", "", fname)
    stem = re.sub(r"【[^】]*】", "", stem)
    parts = stem.split("_")
    if len(parts) < 3:
        return "未标注"
    seg = parts[-1]
    if re.fullmatch(r"[_\-]?e?\d[\d\-\.]*", seg) and len(parts) >= 4:
        seg = parts[-2]  # 末段为纯文章号（如 PLoSONE_e0347253 拆出的 e0347253）
    seg = re.sub(r"[_\-]?e\d{4,}$", "", seg)          # 去掉形如 -e153973 的文章号
    seg = re.sub(r"\d[\d\-\.]*$", "", seg)            # 去掉尾部卷期/页码/编号
    seg = seg.strip(" -_")
    return seg or "未标注"


def bucket_direction(d: str) -> str:
    if "C 轨" in d:
        return "C 轨（可验证性）"
    if "A 轨" in d:
        return "A 轨（驿递交通）"
    if "B 轨" in d:
        return "B 轨（古典文学可视化）"
    if "西游 DH" in d:
        return "西游数字人文（同赛道）"
    for k, name in (
        ("美术学", "艺术学·美术学"),
        ("设计学", "艺术学·设计学"),
        ("综合艺术", "艺术学·综合艺术"),
        ("艺术学理论", "艺术学·艺术学理论"),
        ("①", "艺术学·设计理论与历史"),
        ("②", "艺术学·艺术史论评"),
        ("③", "艺术学·现当代"),
        ("④", "艺术学·西南区域"),
        ("跨文化", "艺术学·跨文化图像"),
        ("画论", "艺术学·画论"),
        ("交互设计理论", "艺术学·交互设计"),
        ("研究范式", "艺术学·研究范式"),
    ):
        if k in d:
            return name
    return "其他"


VENUE_MAP = {
    "DSH": "Digital Scholarship in the Humanities",
    "SciRep": "Scientific Reports",
    "PLoSONE": "PLOS ONE",
    "MTI": "Multimodal Technologies and Interaction",
    "DHQ": "Digital Humanities Quarterly",
    "ESE": "European Science Editing",
    "AccountabilityInResearch": "Accountability in Research",
    "npjHeritageScience": "npj Heritage Science",
    "HeritageScience": "Heritage Science",
    "VCIA": "Visual Computing for Industry, Biomedicine, and Art",
    "AUT设计学硕士论文": "Auckland University of Technology (thesis)",
    "风景园林": "风景园林",
    "燕山大学学报哲社版": "燕山大学学报（哲社版）",
    "电子科技大学学报社科版": "电子科技大学学报（社科版）",
    "西南交大学报社科版": "西南交通大学学报（社科版）",
    "ArchitectureImageStudies": "Architecture & Image Studies",
    "FrontiersPsychology": "Frontiers in Psychology",
    "L10N": "L10N Journal",
    "VINCI": "VINCI (ACM Conference)",
    "CHI": "CHI (ACM Conference)",
    "JAABE": "Journal of Asian Architecture and Building Engineering",
    "艺术发展研究": "艺术发展研究",
    "知识管理论坛": "知识管理论坛",
    "首都师范大学学报": "首都师范大学学报（社科版）",
    "中国比较文学": "中国比较文学",
    "科技与出版": "科技与出版",
    "arXiv": "arXiv (preprint)",
}


def norm_venue(v: str) -> str:
    if v in VENUE_MAP:
        return VENUE_MAP[v]
    if v.startswith("arXiv"):
        return VENUE_MAP["arXiv"]
    if v.startswith("数字人文研究"):
        return "数字人文研究"
    if v.startswith("艺术设计研究"):
        return "艺术设计研究"
    return v


def main() -> None:
    md = LIST_MD.read_text(encoding="utf-8")
    rows = parse_rows(md)
    disk = sorted(p.name for p in PDF_DIR.glob("*.pdf"))

    years = Counter()
    venues = Counter()
    langs = Counter()
    licenses = Counter()
    directions = Counter()
    for r in rows:
        fname = r["file"]
        years[fname[:4]] += 1
        venue = norm_venue(venue_from_filename(fname))
        venues[venue] += 1
        langs["中文" if CJK.search(venue) else "英文"] += 1
        src = r.get("来源/许可", "")
        if "arXiv" in src:
            lic = "arXiv 常规授权"
        elif "CC" in src:
            lic = "CC 开放许可"
        elif "页面转存" in src or "正文提取" in src or "转存" in src:
            lic = "页面转存（非出版社排版）"
        elif "网络首发" in src:
            lic = "网络首发（第三方收录）"
        elif "许可未标示" in src or "未标示" in src:
            lic = "许可未标示"
        else:
            lic = "官方端点·公开可读（许可未标示或未逐条标注）"
        licenses[lic] += 1
        directions[bucket_direction(r.get("方向") or r.get("类别") or "未标注")] += 1

    lic_files: dict[str, list[str]] = {}
    for r in rows:
        src = r.get("来源/许可", "")
        if "arXiv" in src:
            key = "arXiv 常规授权"
        elif "CC" in src:
            key = "CC 开放许可"
        elif "页面转存" in src or "正文提取" in src or "转存" in src:
            key = "页面转存（非出版社排版）"
        elif "网络首发" in src:
            key = "网络首发（第三方收录）"
        elif "许可未标示" in src or "未标示" in src:
            key = "许可未标示"
        else:
            key = "官方端点·公开可读（许可未标示或未逐条标注）"
        lic_files.setdefault(key, []).append(r["file"])

    stats = {
        "清单条目数": len(rows),
        "磁盘 PDF 文件数": len(disk),
        "差额说明": "多出 1 件为 Ping & Wang DSH 同文【出版社版副本】",
        "年份分布": dict(sorted(years.items())),
        "语种分布": dict(langs),
        "英文文件": [r["file"] for r in rows if not CJK.search(norm_venue(venue_from_filename(r["file"])))],
        "许可/可达性分布": dict(licenses.most_common()),
        "许可明细": {k: v for k, v in lic_files.items()},
        "渠道 Top": venues.most_common(20),
        "渠道总数": len(venues),
        "未标注渠道文件": [r["file"] for r in rows if norm_venue(venue_from_filename(r["file"])) == "未标注"],
        "方向分布": directions.most_common(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"清单条目 {len(rows)} / 磁盘 PDF {len(disk)}")
    print("年份:", stats["年份分布"])
    print("语种:", stats["语种分布"])
    print("许可:", stats["许可/可达性分布"])
    print("渠道数:", len(venues))
    for v, n in venues.most_common(20):
        print(f"   {n:>3}  {v}")
    print("方向:")
    for d, n in directions.most_common():
        print(f"   {n:>3}  {d}")
    print("written:", OUT)


if __name__ == "__main__":
    main()
