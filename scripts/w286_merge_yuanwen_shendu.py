"""
W286 任务脚本：
1. 批量抓取古诗文网《西游记》100回完整原文，保存到 source/原文/分回/
2. 读取 temp_shendu/ 下100篇深读，按元数据中的"推测对应原著回号"合并到 docs/01-全书逐回解读/第NNN回-*.md
   在每个 .md 文件末尾追加两个 section：
   - ## 深度解读（所有覆盖该原著回的深读按SD编号顺序拼接）
   - ## 原文全文（从网上抓取的完整原著文本）
"""

import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

WORKSPACE = Path(r"d:\1\xiyouji")
YUANWEN_DIR = WORKSPACE / "source" / "原文"
FENHUI_DIR = YUANWEN_DIR / "分回"
TEMP_SHENDU_DIR = YUANWEN_DIR / "temp_shendu"
ZHUIHUI_DIR = WORKSPACE / "docs" / "01-全书逐回解读"

# URL pattern from browser mapping: chapter N (1-based) -> page 705+N
BASE_URL = "https://m.gsw6.com/book/xyj/{page}.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

FENHUI_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Part 1: Scrape 100 chapters raw text
# ============================================================
def fetch_chapter(n: int) -> str:
    """Fetch chapter N (1-based) and return clean plain text (with line breaks)."""
    page = 705 + n
    url = BASE_URL.format(page=page)
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    soup = BeautifulSoup(raw, "html.parser")
    # 古诗文手机端小说正文一般在多个 <p> 标签里，找正文容器
    # Try common selectors, fallback to all p in body
    container = (
        soup.select_one("div.contson")
        or soup.select_one("div.content")
        or soup.select_one("div.bookcontent")
        or soup.select_one("article")
        or soup.select_one("#content")
        or soup.body
    )
    ps = container.find_all("p") if container else soup.find_all("p")
    lines = []
    for p in ps:
        text = p.get_text("\n", strip=True)
        if not text:
            continue
        # 去掉广告或无关段落
        if any(kw in text for kw in ["扫码下载", "APP下载", "古诗文网", "手机版", "下一篇", "上一篇", "分享", "收藏", "纠错"]):
            continue
        lines.append(text)
    if not lines:
        # 再尝试整个页面的纯文本
        all_text = soup.get_text("\n", strip=True)
        lines = [ln.strip() for ln in all_text.splitlines() if ln.strip() and len(ln.strip()) > 20]
    return "\n\n".join(lines)


def save_all_chapters():
    """Scrape all 100 chapters, save as 第NNN回.txt. Skip if exists."""
    print("=" * 60)
    print("Part 1: Fetching 100 chapters of 《西游记》原文")
    print("=" * 60)
    missing = []
    for n in range(1, 101):
        out = FENHUI_DIR / f"第{n:03d}回.txt"
        if out.exists() and out.stat().st_size > 1000:
            continue
        try:
            text = fetch_chapter(n)
            out.write_text(text, encoding="utf-8")
            size_kb = out.stat().st_size / 1024
            print(f"  第{n:03d}回 OK  {size_kb:.1f} KB  ({len(text)} chars)")
        except Exception as e:
            missing.append(n)
            print(f"  第{n:03d}回 FAIL: {e}")
        time.sleep(0.3)  # gentle crawl
    if missing:
        print(f"\n⚠️  失败回号（共{len(missing)}）: {missing}")
        # retry once after pause
        print("重试失败的回号...")
        time.sleep(3)
        still_missing = []
        for n in missing:
            out = FENHUI_DIR / f"第{n:03d}回.txt"
            try:
                text = fetch_chapter(n)
                out.write_text(text, encoding="utf-8")
                print(f"  第{n:03d}回 OK")
            except Exception as e:
                still_missing.append(n)
                print(f"  第{n:03d}回 仍然失败: {e}")
            time.sleep(1)
        if still_missing:
            print(f"\n❌ 仍然失败: {still_missing}")
            return False
    print("\n✅ 100回原文全部抓取保存完毕\n")
    return True


# ============================================================
# Part 2: Merge shendu + 原文 into 逐回解读 .md files
# ============================================================
def parse_shendu_metadata(path: Path):
    """Parse SDxxx.txt first line HTML comment:
    <!-- 深读编号: N | 标题: XXX | 推测对应原著回号: 第X回 / 第X-Y回 -->
    Returns (sd_num, title, list of chapter_nums)
    """
    first = path.read_text(encoding="utf-8").splitlines()[0] if path.exists() else ""
    m = re.search(r"深读编号:\s*(\d+).*?标题:\s*(.*?)\s*[|\n].*?推测对应原著回号:\s*第?\s*(\d+)\s*回?\s*[-~—]?\s*(\d+)?", first)
    sd_num = 0
    title = path.stem
    chapters = []
    if m:
        sd_num = int(m.group(1))
        title = m.group(2).strip()
        c1 = int(m.group(3))
        c2 = int(m.group(4)) if m.group(4) else c1
        chapters = list(range(c1, min(c2, 100) + 1))
    else:
        # fallback: just put to a single chapter based on filename SDxxx → chapter xxx if reasonable
        m2 = re.match(r"SD(\d+)", path.stem)
        if m2:
            n = int(m2.group(1))
            sd_num = n
            if 1 <= n <= 100:
                chapters = [n]
    return sd_num, title, chapters


def load_shendu_index():
    """Scan temp_shendu/*.txt → {chapter_num: [(sd_num, title, body_path)]}"""
    idx = {}
    if not TEMP_SHENDU_DIR.exists():
        print(f"⚠️  目录不存在: {TEMP_SHENDU_DIR}")
        return idx
    for f in sorted(TEMP_SHENDU_DIR.glob("SD*.txt")):
        sd_num, title, chs = parse_shendu_metadata(f)
        body_text = f.read_text(encoding="utf-8")
        # 去掉第一行的元数据注释
        body_text = re.sub(r"^<!--.*?-->\s*\n?", "", body_text, count=1)
        body_text = body_text.strip()
        for ch in chs:
            idx.setdefault(ch, []).append((sd_num, title, body_text))
    print(f"✅ 深读索引建立完成，共覆盖 {len(idx)} 个原著回号\n")
    return idx


def merge_into_md_files(shendu_idx: dict):
    """For each 第NNN回-*.md in ZHUIHUI_DIR:
    append ## 深度解读 (if any shendu covers this chapter) + ## 原文全文
    Skip if already has both markers (idempotent).
    """
    print("=" * 60)
    print("Part 2: 合并深度解读 + 原文全文到逐回解读 .md")
    print("=" * 60)
    md_files = sorted(ZHUIHUI_DIR.glob("第*.md"))
    updated = 0
    no_yuanwen = []
    for md in md_files:
        # extract chapter number from filename 第NNN回-xxx.md
        m = re.match(r"第(\d+)回", md.name)
        if not m:
            continue
        ch = int(m.group(1))
        orig = md.read_text(encoding="utf-8")
        # Check idempotency
        has_shendu_sec = "## 深度解读" in orig
        has_yuanwen_sec = "## 原文全文" in orig
        # Remove old sections if any to allow re-run
        if has_shendu_sec:
            orig = re.sub(r"\n## 深度解读[\s\S]*$", "", orig).rstrip()
        if has_yuanwen_sec:
            orig = re.sub(r"\n## 原文全文[\s\S]*$", "", orig).rstrip()
        orig = orig.rstrip() + "\n\n"

        # --- Section 1: 深度解读 ---
        sd_list = shendu_idx.get(ch, [])
        if sd_list:
            sd_list.sort(key=lambda x: x[0])
            orig += "## 深度解读\n\n"
            for sd_num, sd_title, sd_body in sd_list:
                orig += f"### SD{sd_num:03d} · {sd_title}\n\n"
                orig += sd_body.rstrip() + "\n\n---\n\n"
            orig = orig.rstrip() + "\n\n"

        # --- Section 2: 原文全文 ---
        yw_path = FENHUI_DIR / f"第{ch:03d}回.txt"
        if yw_path.exists() and yw_path.stat().st_size > 200:
            yw_text = yw_path.read_text(encoding="utf-8").strip()
            orig += "## 原文全文\n\n"
            orig += yw_text + "\n"
        else:
            no_yuanwen.append(ch)
            orig += "## 原文全文\n\n"
            orig += "> ⚠️ 原文暂缺（待补）\n"

        md.write_text(orig.rstrip() + "\n", encoding="utf-8")
        updated += 1

    print(f"✅ 已更新 {updated} 个逐回解读 .md 文件")
    if no_yuanwen:
        print(f"⚠️  原文暂缺 {len(no_yuanwen)} 回: {no_yuanwen}")
    else:
        print("✅ 100回原文全部就位")
    return True


def main():
    ok = save_all_chapters()
    idx = load_shendu_index()
    merge_into_md_files(idx)
    # Summary
    yw_count = len(list(FENHUI_DIR.glob("第*回.txt")))
    sd_count = len(list(TEMP_SHENDU_DIR.glob("SD*.txt"))) if TEMP_SHENDU_DIR.exists() else 0
    md_count = len(list(ZHUIHUI_DIR.glob("第*.md")))
    print("\n" + "=" * 60)
    print("📊 W286 任务完成统计")
    print("=" * 60)
    print(f"  原著分回原文: {yw_count}/100")
    print(f"  深读切片数:    {sd_count}/100")
    print(f"  逐回解读.md:   {md_count}")
    print("=" * 60)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
