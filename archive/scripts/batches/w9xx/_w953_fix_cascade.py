# -*- coding: utf-8 -*-
"""_w953_fix_cascade.py — 补 W953 cascade 的文件清单与文案（重出批次 + 辅助脚本）"""
import io
import os
import sys

P = os.path.join(r"D:\xiyouji", "scripts", "_w953_cascade.py")


def read_norm(p):
    raw = io.open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def main():
    t, nl = read_norm(P)
    n = 0
    pairs = [
        ('BATCH_JSONS = ["scripts/output/_w953_batch%d.json" % i for i in (1, 2, 3)]',
         'BATCH_JSONS = ["scripts/output/_w953_batch%d.json" % i for i in (1, 2, 3, 4, 5)]'),
        ('"scripts/_w953_cascade.py", "scripts/_w945_prepare.py", "scripts/_w945_plates_verify.py",',
         '"scripts/_w953_cascade.py", "scripts/_w953_prep_raws.py", "scripts/_w953_prep_raws2.py",\n'
         '    "scripts/_w953_prep_raws3.py", "scripts/_w953_update_readme.py", "scripts/_w945_prepare.py",\n'
         '    "scripts/_w945_plates_verify.py",'),
        ('"⑤ **防画中画**——并列型题材（混世四猴/兵器/四值功曹/五方揭谛/六丁六甲/器物传记）统一带"',
         '"⑤ **重出 6 张**——首轮机器判据抓出 06（兵器挤在左上角·顶满画面）与 10（六将画得过密），'
         '人眼另抓出 04（石帘被涂成黑色实心条）与 08（四值功曹被画成四张猴脸·题材误读）；'
         '二次重出时 06 画得过稀（墨量 0.0137 低于下限）、10 画成黑框密图 ⇒ 再调（兵器放大 + 六将改一字横排）后收敛；"\n'
         '        "⑥ **防画中画**——并列型题材（混世四猴/兵器/四值功曹/五方揭谛/六丁六甲/器物传记）统一带"'),
        ('"⑥ **接入**——按 `chapter-plate` 范式插入 12 个 themes 专题页（幂等脚本 `_w953_insert_plates.py`）；"\n'
         '        "⑦ **前置**——preflight 取号 W953（max=W952+1·撞号检测无同号多行） | "',
         '"⑦ **接入**——按 `chapter-plate` 范式插入 12 个 themes 专题页（幂等脚本 `_w953_insert_plates.py`）；"\n'
         '        "⑧ **前置**——preflight 取号 W953（max=W952+1·撞号检测无同号多行） | "'),
        ('"**防画中画**：并列型题材（混世四猴 / 兵器 / 四值功曹 / 五方揭谛 / 六丁六甲 / 器物传记）统一带「四周不得有任何边框、格子、展板或深色底板」措辞——W952 的 11-法宝系统正是栽在「展柜」上，重出后有效的措辞。',
         '"**重出 6 张**：机器判据抓出 06 兵器（挤在左上角·顶满画面·J2/J10 判红）与 10 六丁六甲（过密·J3=0.1251 超阈）；'
         '人眼另抓出 04 石帘被涂成黑色实心条、08 四值功曹被画成四张猴脸（题材误读）。'
         '二次重出时 06 画得过稀（墨量 0.0137 低于下限）、10 画成黑框密图 ⇒ 再调（兵器放大 + 六将改一字横排）后收敛。\\n\\n'
         '**防画中画**：并列型题材（混世四猴 / 兵器 / 四值功曹 / 五方揭谛 / 六丁六甲 / 器物传记）统一带「四周不得有任何边框、格子、展板或深色底板」措辞——W952 的 11-法宝系统正是栽在「展柜」上，重出后有效的措辞。'),
    ]
    for old, new in pairs:
        if old in t:
            t = t.replace(old, new, 1)
            n += 1
        else:
            print("WARN 未命中：%s" % old[:60].replace("\n", " "))
    io.open(P, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))
    print("cascade 已修 %d/%d 处" % (n, len(pairs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
