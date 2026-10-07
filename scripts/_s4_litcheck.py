"""清单一致性核对（2026-10-04）：清单引用 vs 实际 PDF 文件。"""
import os
import re

folder = r"d:\xiyouji\docs\S4-学术投稿\06-文献"
md = open(os.path.join(folder, "00-文献清单.md"), encoding="utf-8").read()
refs = re.findall(r"`([^`/]+\.pdf)`", md)
actual = set(f for f in os.listdir(folder) if f.lower().endswith(".pdf"))
print("清单引用数:", len(refs), "| 实际文件数:", len(actual))
missing = [r for r in refs if r not in actual]
extra = [a for a in actual if a not in refs]
print("清单引用但文件缺失:", missing if missing else "无")
print("文件存在但清单未登记:", extra if extra else "无")
lines = [l for l in md.splitlines() if l.startswith("| `")]
nodoi = [l[:90] for l in lines if not any(k in l for k in ("DOI", "arXiv:", "无 DOI", "文章编号", "同上"))]
print("引用行缺 DOI/arXiv 标识:", nodoi if nodoi else "无")
