#!/usr/bin/env python3
"""一次性：按《数据核验与复现报告》（A 轨/C 轨·2026-09-28）处置项修订稿件。

A 轨 × 4 处（投稿版 + 匿名稿同改，均带断言）：
  A1 §5.1 半程计数：「第 51—100 回达 10 处（不含两端）」→「达 11 处」（复算 4+11=15 自洽）
  A2 §5.1「最长的空白出现在…」→「显著的空白出现在…」+「（宝象国之后至平顶山…）」→「（宝象国之后至乌鸡国之前…）」
  A3 表 2 车迟国行 46 回片段 → 连续逐字「用了宝印，便要递与唐僧，放行西路」（底本第 46 回 line 1）
  A4 §4.3「坐名告状」→「“坐名告你”」（加全角引号·第 97 回 line 31 逐字）
C 轨 × 4 点位（投稿版 + 匿名稿同改）+ 大纲：
  C1 中文摘要「存活三周」→「存活约七周」
  C2 英文摘要「survived three weeks」→「survived for about seven weeks」
  C3 案例一小节标题「三周存活」→「约七周存活」
  C4 正文「它存活了三周。…」→「它存活了约七周。…（索引自 2026 年 7 月 30 日起收录）…直到 2026 年 9 月 22 日…」
  G  大纲「存活三周」→「存活约七周」

用法：py scripts/_s4ac_data_fix.py [--check|--apply]（默认 --check 只读核查）
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
S4 = ROOT / "docs" / "S4-学术投稿"
A = S4 / "01-论文" / "明清小说方向-投稿版.md"
A_ANON = S4 / "01-论文" / "明清小说方向-匿名稿.md"
C = S4 / "01-论文" / "可验证性方向-投稿版.md"
C_ANON = S4 / "01-论文" / "可验证性方向-匿名稿.md"
G = S4 / "可验证性方向-论文三大纲.md"

# 注：两稿正文散引号为半角直引号（0x22）；C 轨「> 原文引文」行用全角引号（门禁要求）。

REPLACEMENTS = {
    A: [
        ("A1", "第 51—100 回达 10 处（不含两端）", "第 51—100 回达 11 处"),
        ("A2", "最长的空白出现在第 30—38 回（宝象国之后至平顶山，九回无驿传节点）",
               "显著的空白出现在第 30—38 回（宝象国之后至乌鸡国之前，九回无驿传节点）"),
        ("A3", "46 回 line 1 用了宝印，放行西路", "46 回 line 1 用了宝印，便要递与唐僧，放行西路"),
        ("A4", '官府缉捕、坐名告状（line 31）', '官府缉捕、"坐名告你"（line 31）'),
        ("A5", '（如车迟国"用了宝印，放行西路"）', '（如车迟国"用了宝印，便要递与唐僧，放行西路"）'),
    ],
    C: [
        ("C1", "存活三周", "存活约七周"),
        ("C2", "survived three weeks", "survived for about seven weeks"),
        ("C3", "三周存活", "约七周存活"),
        ("C4", '它存活了三周。先是它以"项目索引已收录"的形态获得了看似权威的出处，随后被论文写作当作真实文献转述、引用；直到审读质疑触发对抗性自查',
               '它存活了约七周。先是它以"项目索引已收录"的形态获得了看似权威的出处（索引自 2026 年 7 月 30 日起收录），随后被论文写作当作真实文献转述、引用；直到 2026 年 9 月 22 日审读质疑触发对抗性自查'),
    ],
    G: [
        ("G1", "存活三周", "存活约七周"),
    ],
}

MIRROR = {A: A_ANON, C: C_ANON}  # 匿名稿镜像同改


def check_file(path, reps, apply):
    text = path.read_text(encoding="utf-8")
    ok = True
    for tag, old, new in reps:
        n = text.count(old)
        flag = "OK " if n == 1 else "!! "
        if n != 1:
            ok = False
        print("  %s[%s] count=%d  old=%r" % (flag, tag, n, old[:48]))
        if n >= 1 and apply:
            text = text.replace(old, new)
    if apply and ok:
        path.write_text(text, encoding="utf-8")
        print("  -> 已写入 %s" % path.name)
    return ok


def main():
    apply = "--apply" in sys.argv
    print("== 模式：%s ==" % ("APPLY（写盘）" if apply else "CHECK（只读）"))
    all_ok = True
    for path, reps in REPLACEMENTS.items():
        print("#" * 20, path.name, "（+镜像）")
        all_ok &= check_file(path, reps, apply)
        mirror = MIRROR.get(path)
        if mirror:
            all_ok &= check_file(mirror, reps, apply)

    # 附加核对：A 文件「用了宝印」与「用了宝印，放行西路」全部落点上下文
    print("== 附加核对：A 稿『用了宝印』落点 ==")
    for p in (A, A_ANON):
        t = p.read_text(encoding="utf-8")
        i = 0
        while True:
            i = t.find("用了宝印", i)
            if i < 0:
                break
            print("  [%s] …%s…" % (p.name[:12], t[max(0, i - 40): i + 40].replace("\n", "⏎")))
            i += 1
        print("  [%s] 残留「用了宝印，放行西路」count=%d（预期：正文表外如有压缩引用需人工判读）"
              % (p.name[:12], t.count("用了宝印，放行西路")))
    print("== 残留扫描：C 稿『三周』/『three weeks』 ==")
    for p in (C, C_ANON, G):
        t = p.read_text(encoding="utf-8")
        print("  [%s] 三周=%d  three weeks=%d" % (p.name[:16], t.count("三周"), t.count("three weeks")))

    print("== 结果：%s ==" % ("全部断言通过" if all_ok else "存在计数不符（未写盘或部分未写）"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())