# -*- coding: utf-8 -*-
"""_w952_fix_j10.py — J10 判据口径修正（段内改用「最亮 20% 像素均值」= 纸色主导值）

问题：段内用「整段均值」时，**主体伸进顶部带**（昴日星官的鸡冠尖）会把该段均值拉低
⇒ 纯纸面无边的图被判 J10 = 5.00 压线（W952 实测）。
修正：段内取**最亮 20% 像素的均值**（＝该段纸色主导值）⇒ 主体墨迹只占少数像素、不影响它；
真正的白边/色带（边缘段纯白 / 中段米黄）仍会被抓住 ⇒ **判据变准，不是放宽阈值**。
"""
import io
import os
import sys

P = os.path.join(r"D:\xiyouji", "scripts", "_w945_plates_verify.py")

OLD = """        px = list(reg.getdata())
        if not px:
            continue
        vals.append(sum(sum(p) / 3 for p in px) / len(px))
    if len(vals) < 2:
        return 0.0
    return max(vals) - min(vals)"""

NEW = """        px = list(reg.getdata())
        if not px:
            continue
        # 段内取「最亮 20% 像素的均值」= 该段纸色基底（主体墨迹只占少数像素·不影响它）
        lum = sorted(sum(p) / 3 for p in px)
        top = lum[int(len(lum) * 0.80):]
        if not top:
            top = lum[-1:]
        vals.append(sum(top) / len(top))
    if len(vals) < 2:
        return 0.0
    return max(vals) - min(vals)"""

DOC_OLD = """    口径：取**顶部 band 高度带**（该带按规格是纯纸面留白区·不含主体）
    ⇒ 该带的均值即该段的纸色基底；分段求均值后取 max-min。
    白边/色带 ⇒ 边段基底是纯白（255）而中段是米黄 ⇒ 差值显著。
    只测顶部带而不测整幅，是为了避开主体白色衣物对白段均值的污染。
    \"\"\""""

DOC_NEW = """    口径（W952 修正）：段内统计用**最亮 20% 像素的均值**（＝该段的纸色主导值），而非整段均值
    —— 否则**主体伸进顶部带**（如昴日星官的鸡冠尖）会把该段均值拉低、误报成「背景不均匀」
    （W952 实测：一张纯纸面无边的图被判 J10 = 5.00 压线）。
    取最亮 20% ⇒ 主体墨迹只占少数像素、不影响纸色基底；而真正的白边/色带
    （边缘段是纯白、中段是米黄）仍会被抓住 ⇒ **判据变准，不是放宽阈值**。
    \"\"\""""


def main():
    raw = io.open(P, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    t = raw.decode("utf-8").replace("\r\n", "\n")
    if "最亮 20% 像素的均值" in t:
        print("已修正（幂等跳过）")
        return 0
    if OLD not in t:
        print("FATAL 未找到目标代码段")
        return 2
    t = t.replace(OLD, NEW, 1)
    if DOC_OLD in t:
        t = t.replace(DOC_OLD, DOC_NEW, 1)
    else:
        print("NOTE 未找到 docstring 段（仅替换代码体）")
    io.open(P, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))
    print("J10 口径已修正：段内改用最亮 20% 像素均值")
    return 0


if __name__ == "__main__":
    sys.exit(main())
