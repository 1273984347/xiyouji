# -*- coding: utf-8 -*-
"""_w1049_reissue_97.py — 97 号第三次出图（修正「稀疏约束」与「占幅五成」的冲突）

两轮实测：
  首版  J4=0.0298（差阈值 0.0002·目视合规·主体占幅偏小）
  二版  J4=0.0258（更差）—— 根因：二版加的「僧衣只勾三五道衣纹·其余大面积留白」
        +「线条须稀疏·大量留白」把模型推向「画得更小更空」，
        与母版段「主体占画面高度约五成」直接冲突。

三版修法：**删掉所有「留白/稀疏」措辞**，改为显式要求主体**放大占幅**：
  「主体须显著高大·占画面高度约七成·头部接近画面中线·双脚接近画面底部」
  + 僧衣上**勾十余道**衣纹（给足墨量）+ 保持「不涂实心色块」。

只改这一张，不碰其余 11 张。
用法：py -3 archive/scripts/batches/w10xx/_w1049_reissue_97.py
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
STEM = "plate-line-97-ch016-jinchi-zhanglao"

src = json.load(io.open(os.path.join(OUT, "_w1049_batch.json"), encoding="utf-8"))
BASE = src["requests"][0]["prompt"]
MASTER = BASE[:BASE.find("主体：")]
assert len(MASTER) == 249, "母版段长度变了：%d" % len(MASTER)

CLOTH = "衣物只用墨线勾出衣纹，通体不涂任何实心色块。"
FOOT = "主体完整入框不入画，画面底部须留出约一成的纯纸面空白，不画地面、不裁切衣摆。"
DOT = "画面中那处朱砂红仅为一枚指甲盖大小的圆点，不得画成火焰、块状物、条状物或竖椭圆。"

DESC = (
    "金池长老：年迈僧人形象，头戴毗卢帽（帽面平整洁净），身着宽袖僧衣（"
    + CLOTH + "），僧衣上用墨线勾出十余道衣纹与褶皱。双手合十于胸前，身姿恭谨。"
    "主体须显著高大、占画面高度约七成，头部位于画面中线附近、双脚接近画面底部，"
    "人物在画面中醒目突出。"
    + FOOT + DOT + "不画黑熊精、不画孙悟空、不画唐僧、不画观音。"
)


def mcode_cmd():
    import shutil
    p = shutil.which("mcode-tools")
    return [p] if p else ["mcode-tools"]


def main() -> int:
    argf = os.path.join(OUT, "_w1049_reissue_97.json")
    io.open(argf, "w", encoding="utf-8", newline="\n").write(json.dumps(
        {"requests": [{
            "aspect_ratio": "3:4", "resolution": "2K",
            "output_file": STEM,
            "prompt": MASTER + "主体：" + DESC,
        }]}, ensure_ascii=False, indent=1))
    print("97 三版出图请求 ->", argf)

    # 先删旧件（下载器幂等·不删会复活旧图）
    for ext in (".png", ".jpg", ".jpeg"):
        old = os.path.join(DEST, STEM + ext)
        if os.path.exists(old):
            os.remove(old)
            print("已删旧件:", os.path.basename(old))

    r = subprocess.run(mcode_cmd() + ["connector", "call", "connector__matrix__generate_image",
                                      "--args-file", argf],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=600, shell=True)
    print("出图 exit=%d" % r.returncode)
    print((r.stdout or "")[:1500])
    if r.returncode != 0:
        print((r.stderr or "")[:800])
        return 1
    d = json.loads(r.stdout)
    items = d.get("success_items") or []
    if len(items) != 1:
        print("出图未全成功：%s" % d.get("failed_items"))
        return 1
    it = items[0]
    u = subprocess.run(mcode_cmd() + ["get_asset_url", str(it["node_id"])],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=120, shell=True)
    url = json.loads(u.stdout)["download_url"]
    with urllib.request.urlopen(url, timeout=180) as rr:
        data = rr.read()
    if len(data) < MIN_BYTES or not (data.startswith(PNG_MAGIC) or data.startswith(JPEG_MAGIC)):
        print("FAIL 非法原件（%d B）" % len(data))
        return 1
    with io.open(os.path.join(DEST, it["file_name"]), "wb") as fh:
        fh.write(data)
    print("OK    %s（%d B）" % (it["file_name"], len(data)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
