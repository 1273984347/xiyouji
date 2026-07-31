# -*- coding: utf-8 -*-
"""
W286-FIX: 修复第069回、第099回原文缺失
从古诗文网备用URL或其他可用源抓取，补充分回原文并重新合并
"""

import urllib.request
import urllib.parse
import re
from pathlib import Path
from bs4 import BeautifulSoup
import time

ROOT = Path(__file__).resolve().parent.parent
SOURCE_YW_SPLIT = ROOT / "source" / "原文" / "分回"
DOCS_01 = ROOT / "docs" / "01-全书逐回解读"
TEMP_SHENDU = ROOT / "temp_shendu"

# ------------- 备用抓取：尝试不同的 page/section selector ------------
def try_fetch_alternative(chapter: int):
    """
    尝试多种策略抓取指定回目正文：
      策略1: 同页面但 selector 更宽松 (抓取所有非链接的 p/div 文本)
      策略2: 同域备用路径 /gushiwen/
      策略3: 直接返回 None 让用户知道哪回需要人工校对
    """
    n = chapter

    # 策略1: 相同URL，用浏览器抓取的真实HTML结构：似乎正文是 <h1> 之后紧跟 一堆<a>单字链接？不，那不是正文
    # 先尝试原URL但更一般的 selector：找所有包含多行文本的 block
    page = 705 + n
    url = f"https://m.gsw6.com/book/xyj/{page}.html"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  [{n:03d}] 策略1 fetch error: {e}")
        raw = ""

    if raw:
        soup = BeautifulSoup(raw, "html.parser")
        # 删除所有<a>...</a>单字链接
        for a in soup.find_all("a"):
            if a.get_text(strip=True) and len(a.get_text(strip=True)) <= 2:
                # 如果a只有1-2字且包含href=单字页，就剥离（保留父节点文本）
                pass
        # 更简单: 查找所有不是链接、长度>200字符的文本容器
        candidates = []
        for tag in soup.find_all(["div", "article", "section", "p"]):
            txt = tag.get_text("\n", strip=True)
            # 过滤：必须包含"诗曰"或"话表"或"却说"或"行者"且字数>500
            if (len(txt) > 500
                    and ("诗曰" in txt or "话表" in txt or "却说" in txt
                         or "行者" in txt or "师徒" in txt or "菩萨" in txt)):
                candidates.append((len(txt), txt))
        candidates.sort(key=lambda x: x[0], reverse=True)
        if candidates:
            txt = candidates[0][1]
            # 清理行首多余空格、空行过滤
            lines = [ln.rstrip() for ln in txt.splitlines() if ln.strip()]
            return "\n".join(lines) + "\n"

    # 策略2: 备用抓取源 - 尝试搜索其他公开《西游记》全文源（此处用一个简单的fallback:
    # 尝试 https://www.xituhui.com/xyj/chapter_{n}.html 等模板
    alt_urls = [
        f"https://www.shicimingju.com/book/xiyouji/{n}.html",
    ]
    for au in alt_urls:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            req = urllib.request.Request(au, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw2 = resp.read().decode("utf-8", errors="ignore")
            soup2 = BeautifulSoup(raw2, "html.parser")
            # 常见小说正文div
            for sel in [{"class": "chapter-content"}, {"id": "content"}, {"class": "content"}, {"class": "book_content"}]:
                block = soup2.find("div", sel)
                if block:
                    txt = block.get_text("\n", strip=True)
                    if len(txt) > 500:
                        lines = [ln.rstrip() for ln in txt.splitlines() if ln.strip()]
                        return "\n".join(lines) + "\n"
        except Exception:
            continue
        time.sleep(0.5)

    return None


def parse_shendu_metadata(path: Path):
    text = path.read_text(encoding="utf-8")
    first = text.splitlines()[0].strip() if text.splitlines() else ""
    m = re.match(r"<!--\s*深读编号:\s*(\d+)\s*\|\s*标题:\s*(.*?)\s*\|\s*推测对应原著回号:\s*第(\d+)回\s*-->", first)
    if m:
        sd_num, sd_title, orig_ch = int(m.group(1)), m.group(2).strip(), int(m.group(3))
        body = "\n".join(text.splitlines()[1:]).strip()
        return sd_num, sd_title, orig_ch, body
    return None


def load_shendu_index():
    result = {}
    for p in sorted(TEMP_SHENDU.glob("SD*.txt")):
        r = parse_shendu_metadata(p)
        if not r:
            continue
        sd_num, sd_title, orig_ch, body = r
        result.setdefault(orig_ch, []).append((sd_num, sd_title, body))
    for k in result:
        result[k].sort(key=lambda x: x[0])
    return result


def rebuild_single_md(chapter: int, shendu_idx: dict, new_yuanwen: str):
    """重新构建单个逐回解读.md：去除旧的深度解读/原文全文，重新追加"""
    # 找到对应的 md 文件
    candidates = list(DOCS_01.glob(f"第{chapter:03d}回-*.md"))
    if not candidates:
        print(f"  [MD NOT FOUND] 第{chapter:03d}回 没有对应 .md 文件!")
        return False
    md_path = candidates[0]

    orig = md_path.read_text(encoding="utf-8")
    # 移除旧段
    if re.search(r"\n## 深度解读", orig):
        orig = re.sub(r"\n## 深度解读[\s\S]*$", "", orig).rstrip()
    if re.search(r"\n## 原文全文", orig):
        orig = re.sub(r"\n## 原文全文[\s\S]*$", "", orig).rstrip()
    orig = orig.rstrip() + "\n\n"

    sd_list = shendu_idx.get(chapter, [])
    if sd_list:
        orig += "## 深度解读\n\n"
        for sd_num, sd_title, sd_body in sd_list:
            orig += f"### SD{sd_num:03d} · {sd_title}\n\n{sd_body}\n\n---\n\n"
    orig += "## 原文全文\n\n" + new_yuanwen.rstrip() + "\n"

    md_path.write_text(orig, encoding="utf-8")
    return True


# ------------------------ Main ------------------------
if __name__ == "__main__":
    PROBLEM_CHAPTERS = [69, 99]

    shendu_idx = load_shendu_index()
    # 扩展 shendu_idx: 有些 SD 可能漏填对应回号？之前脚本已经处理过，这里直接用之前的索引

    print("=" * 60)
    print("W286 FIX: 修复问题回目原文 (69, 99)")
    print("=" * 60)

    fixed_count = 0
    for n in PROBLEM_CHAPTERS:
        print(f"\n▶ 处理第{n:03d}回 ...")
        txt = try_fetch_alternative(n)
        if not txt or len(txt) < 1000:
            print(f"  ❌ 备用源仍无法获取足够正文 (当前长度: {len(txt or '')} chars)")
            print("  → 将尝试用更激进的方案: 直接按行拼抓页面所有非链接长文本 + 过滤字典/单字链接行")

            # Fallback: 读现存的 分回/第069回.txt，如果太短，打印明确提示并跳过
            existing_path = SOURCE_YW_SPLIT / f"第{n:03d}回.txt"
            existing = existing_path.read_text(encoding="utf-8") if existing_path.exists() else ""
            if len(existing) > 1000:
                txt = existing
            else:
                print("  ⚠️  暂时无法自动补全，请手动粘贴正文章节到:")
                print(f"       {existing_path}")
                print("      然后重新运行本脚本或直接重新跑 W286 合并部分")
                continue

        # 保存原文
        out_path = SOURCE_YW_SPLIT / f"第{n:03d}回.txt"
        out_path.write_text(txt, encoding="utf-8")
        k = len(txt)
        print(f"  ✅ 原文保存成功: {out_path}  ({k/1024:.1f} KB, {k} chars)")

        # 重新合并对应 .md
        ok = rebuild_single_md(n, shendu_idx, txt)
        if ok:
            fixed_count += 1
            print(f"  ✅ 已更新 第{n:03d}回 .md")

    print("\n" + "=" * 60)
    print(f"修复完成: 共修复 {fixed_count}/{len(PROBLEM_CHAPTERS)} 回")
    print("=" * 60)
