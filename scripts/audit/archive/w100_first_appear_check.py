"""验证 first_appear 早现的合理性"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ts_html = (ROOT / "site" / "data" / "text-search.html").read_text(encoding="utf-8")

# 验证唐僧/猪八戒/沙僧/白龙马 在第7回和第8回的提及
targets = {
    "唐僧": ["唐僧", "玄奘", "三藏", "唐三藏", "旃檀功德佛", "圣僧", "唐长老", "御弟"],
    "猪八戒": ["猪八戒", "八戒", "天蓬元帅", "净坛使者", "呆子", "猪悟能", "木母"],
    "沙僧": ["沙僧", "沙悟净", "卷帘大将", "金身罗汉", "沙和尚", "黄婆"],
    "白龙马": ["白龙马", "敖烈", "八部天龙", "玉龙", "白马"],
}

for ch_num in [7, 8]:
    print(f"\n=== 第{ch_num}回 ===")
    pattern = rf'num:\s*{ch_num},\s*\n\s*title:\s*"([^"]+)".*?text:\s*`([^`]+)`'
    m = re.search(pattern, ts_html, re.DOTALL)
    if not m:
        print(f"  第{ch_num}回未找到")
        continue
    title = m.group(1)
    text = m.group(2)
    print(f"  回目: {title}")
    for char, aliases in targets.items():
        hits = []
        for alias in aliases:
            for am in re.finditer(re.escape(alias), text):
                start = max(0, am.start() - 30)
                end = min(len(text), am.end() + 30)
                ctx = text[start:end].replace("\n", " ")
                hits.append((alias, am.start(), ctx))
        if hits:
            print(f"  {char}: {len(hits)} 处提及")
            for alias, pos, ctx in hits[:2]:
                print(f"    alias='{alias}' @{pos}: ...{ctx}...")
