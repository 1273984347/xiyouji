# -*- coding: utf-8 -*-
"""_w1049_reissue.py — W1049 重出 3 张（机器判据 J3/J4 判红 + 目视取证确认）

判红与目视结论（证据）：
  97  金池长老   J4 下部主体墨量 0.0298 < 0.03（擦线 0.0002）·目视：老僧立像主体在位、
                  构图合规·但墨量擦线 ⇒ 同批重出（避免单张例外口径分叉）
  103 四大天王   J3 整图墨量 0.1861 > 0.12（超限 55%）·目视：四副铠甲「鳞纹密排线」
                  ⇒ 真实缺陷（墨线过密）·重出时约束鳞纹只勾少数几片
  107 红鳞大蟒   J3 整图墨量 0.2026 > 0.12（超限 69%）·目视：山石用「渲染笔触」而非纯墨线
                  + 蟒身鳞片密排 ⇒ 真实缺陷（渲染阴影违反母版段 + 墨量过载）·重出时强化约束

重出纪律（坑表 E-37）：下载器幂等 ⇒ **重出件必须先删旧件**，否则会复活旧图。
用法：py -3 archive/scripts/batches/w10xx/_w1049_reissue.py
"""
import io
import json
import os
import subprocess
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
OUT = os.path.join(REPO, "scripts", "output")
DEST = os.path.join(REPO, "assets", "promo", "plate-set", "raw", "round18")
MIN_BYTES = 20000
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"

# 强化约束后的 3 条 prompt（母版段沿用同一 249 字符基底·只改主体段）
src = json.load(io.open(os.path.join(OUT, "_w1049_batch.json"), encoding="utf-8"))
BASE = src["requests"][0]["prompt"]
i = BASE.find("主体：")
MASTER = BASE[:i]
assert len(MASTER) == 249, "母版段长度变了：%d" % len(MASTER)

REPL = [
    ("无实心色块填充、无渐变、无阴影、无光效、无背景场景、无边框",
     "无实心色块填充、无渐变、无阴影、无光效、无边框；远景仅以淡墨山形与水面暗示环境，不画建筑、树木与器物细节"),
    ("主体为完整全身立像、居画面中下部、占画面高度约五成、完整入框不被裁切",
     "主体为二至十九人的群像或对峙场面、前后景分明、占画面高度约七成、完整入框不被裁切"),
    ("画面中仅有一处朱砂红 #C8463A 点睛，位于主体右侧",
     "画面中仅有一处朱砂红 #C8463A 点睛，位于主体群右侧"),
]
SCENE = MASTER
for old, new in REPL:
    assert old in SCENE, "母版段锚点失配：" + old[:20]
    SCENE = SCENE.replace(old, new, 1)

CLOTH = "衣物只用墨线勾出衣纹，通体不涂任何实心色块。"
FOOT = "主体完整入框不入画，画面底部须留出约一成的纯纸面空白，不画地面、不裁切衣摆。"
DOT = "画面中那处朱砂红仅为一枚指甲盖大小的圆点，不得画成火焰、块状物、条状物或竖椭圆。"

# 墨量约束：显式要求「线条稀疏·留白充分」+「禁密排纹理·禁渲染笔触」
SPARSE = ("全图线条须稀疏舒展、大量留白，不得用密集排线、细密网纹或鳞片阵列铺满衣甲与躯体；"
          "不得用灰擦渲染、阴影渐层或水墨渲染笔触表现体积，所有形体只以稀疏的墨线轮廓勾出。")

JOBS = [
    ("ch016", "jinchi-zhanglao", "plate-line-97-ch016-jinchi-zhanglao",
     "金池长老：年迈僧人形象，头戴毗卢帽（帽面平整洁净），身着宽袖僧衣（"
     + CLOTH + "），双手合十于胸前，身姿恭谨。僧衣上只勾三五道衣纹，其余大面积留白。"
     + SPARSE + FOOT + DOT + "不画黑熊精、不画孙悟空、不画唐僧、不画观音。"),
    ("ch005", "sida-tianwang", "plate-line-103-ch005-sida-tianwang",
     "四名天将并肩分立：四人皆头戴战盔（盔顶有翎）、身着宽袖重甲（甲面完全留白·只勾甲片分界线·"
     + CLOTH + "），各执一柄形如长柄的兵器（兵器形制各异·一为琵琶形、一为剑、一为伞、一为蛇形长杆）；"
     "四人前后错落站位。画面中只有这四名人物。"
     + SPARSE + FOOT + DOT + "不画孙悟空、不画唐僧、不画玉皇大帝、不画太上老君。"),
    ("ch067", "honglin-damang", "plate-line-107-ch067-honglin-damang",
     "一条巨大的蟒蛇与一名猴形行者隔岭对峙：蟒蛇通体只以稀疏墨线勾出轮廓，"
     "蛇身表面完全不画鳞片阵列、不画细密网纹（只勾五六道蛇身弧线表示转折），"
     "蛇身粗大弯卷、蛇首高昂并张口；对面站着一名猴形行者（手执长铁棒·棒身笔直·毛色淡墨）；"
     "画面中只有蟒蛇与行者两方。远景山石只以几笔稀疏淡墨轮廓勾出，不得渲染。"
     + SPARSE + FOOT + DOT + "不画猪八戒、不画唐僧、不画沙僧、不画灵感大王、不画孙悟空。"),
]


def mcode_cmd():
    import shutil
    p = shutil.which("mcode-tools")
    return [p] if p else ["mcode-tools"]


def main() -> int:
    reqs = []
    for ch, slug, stem, desc in JOBS:
        base = MASTER if ch in ("ch016",) else SCENE
        reqs.append({
            "aspect_ratio": "3:4",
            "resolution": "2K",
            "output_file": stem,
            "prompt": base + "主体：" + desc,
        })
    argf = os.path.join(OUT, "_w1049_reissue.json")
    io.open(argf, "w", encoding="utf-8", newline="\n").write(
        json.dumps({"requests": reqs}, ensure_ascii=False, indent=1))
    print("重出请求 %d 条 -> %s" % (len(reqs), argf))

    # 先删旧件（下载器幂等·不删会复活旧图）
    for _ch, _slug, stem, _d in JOBS:
        for ext in (".png", ".jpg", ".jpeg"):
            old = os.path.join(DEST, stem + ext)
            if os.path.exists(old):
                os.remove(old)
                print("已删旧件:", os.path.basename(old))

    # 出图
    r = subprocess.run(mcode_cmd() + ["connector", "call", "connector__matrix__generate_image",
                                      "--args-file", argf],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=600, shell=True)
    print("出图 exit=%d" % r.returncode)
    print((r.stdout or "")[:2000])
    if r.returncode != 0:
        print((r.stderr or "")[:1000])
        return 1

    try:
        d = json.loads(r.stdout)
    except ValueError:
        return 1
    items = d.get("success_items") or []
    print("成功 %d / 请求 %d" % (len(items), len(reqs)))
    if len(items) != len(reqs):
        return 1

    # 下载
    ok = 0
    for it in items:
        node_id = it.get("node_id")
        fname = it.get("file_name") or ""
        u = subprocess.run(mcode_cmd() + ["get_asset_url", str(node_id)],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=120, shell=True)
        url = json.loads(u.stdout)["download_url"]
        with urllib.request.urlopen(url, timeout=180) as rr:
            data = rr.read()
        if len(data) < MIN_BYTES or not (data.startswith(PNG_MAGIC) or data.startswith(JPEG_MAGIC)):
            print("FAIL  %s 非法（%d B）" % (fname, len(data)))
            continue
        with io.open(os.path.join(DEST, fname), "wb") as fh:
            fh.write(data)
        print("OK    %s（%d B）" % (fname, len(data)))
        ok += 1
    return 0 if ok == len(items) else 1


if __name__ == "__main__":
    raise SystemExit(main())
