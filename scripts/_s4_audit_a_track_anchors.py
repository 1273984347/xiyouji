#!/usr/bin/env python3
"""一次性：A 轨驿递稿 line 号锚点声明逐条核验（2026-09-26 审计）。

从 site/static/js/text-search-app.js 取底本语料，对稿中表 1/表 2 与正文声明的
（回目, 声称 line 号, 文本片段）逐条定位：OK=行号一致 / MISMATCH=行号不符 /
NOT_FOUND=片段未定位（含降级子串尝试）。结果落盘 tmpe/a_track_anchor_audit.json。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TS_JS = ROOT / "site" / "static" / "js" / "text-search-app.js"
OUT = ROOT / "tmpe" / "a_track_anchor_audit.json"

# (来源, 回目, 声称行号, 片段)
CLAIMS = [
    # ---- 表 1 关文节点（15 处）----
    ("表1-12回-发牒", 12, 51, "写了取经文牒"),
    ("表1-29回-宝象国", 29, 19, "倒换文牒，乞为转奏"),
    ("表1-39回-乌鸡国", 39, 31, "倒换关文"),
    ("表1-45回-车迟国", 45, 69, "国王教回銮，倒换关文"),
    ("表1-54回-女儿国", 54, 17, "迎阳馆驿丞，有事见驾"),
    ("表1-62回-祭赛国", 62, 21, "我欲面君倒换关文"),
    ("表1-68回-朱紫国", 68, 21, "你若要倒换关文，趁此急去"),
    ("表1-74回-狮驼国a", 74, 19, "八百里狮驼岭"),
    ("表1-74回-狮驼国b", 74, 19, "三个魔头"),
    ("表1-78回-比丘国", 78, 3, "西邸王位，须要倒换关文"),
    ("表1-84回-灭法国a", 84, 3, "灭法国"),
    ("表1-84回-灭法国b", 84, 63, "一个个也没了头发"),
    ("表1-88回-玉华县", 88, 15, "拿了关文，径至王府前"),
    ("表1-91回-金平府", 91, 7, "金平府是也"),
    ("表1-93回-天竺国", 93, 41, "若欲倒换关文，趁此时好"),
    ("表1-96回-铜台府a", 96, 5, "寇员外家"),
    ("表1-97回-铜台府b", 97, 31, "报官"),
    ("表1-97回-铜台府c", 97, 75, "解状递上"),
    ("表1-98回-灵山a", 98, 43, "无字真经"),
    ("表1-100回-灵山b", 100, 19, "将通关文牒取上来，对主公缴纳"),
    # ---- 表 2 驿传补充集（15 处）----
    ("表2-30回-金亭馆驿（修正后）", 30, 27, "乱传乱嚷，嚷到金亭馆驿"),
    ("表2-29回-牒文本文", 29, 21, "倘到西邦诸国，不灭善缘，照牒放行"),
    ("表2-40回-辞行倒换", 40, 7, "只是倒换关文"),
    ("表2-45回-验牒放行", 45, 21, "召来验牒放行"),
    ("表2-46回-用印放行", 46, 1, "用了宝印，放行西路"),
    ("表2-54回-迎阳驿", 54, 9, "上书迎阳驿三字"),
    ("表2-54回-印关文", 54, 73, "今日即印关文，打发他去也"),
    ("表2-62回-奏对倒换", 62, 33, "我与悟空入朝，倒换关文去来"),
    ("表2-68回-会同馆", 68, 19, "那馆中有两个馆使，乃是一正一副"),
    ("表2-69回-约期倒换", 69, 7, "病痊酬谢，倒换关文"),
    ("表2-78回-金亭馆驿", 78, 13, "忽转街见一衙门，乃金亭馆驿"),
    ("表2-85回-夜借宿", 85, 9, "夜至宝方饭店里借宿"),
    ("表2-87回-关牒上天", 87, 37, "将僧道两家的文牒，送至通明殿"),
    ("表2-93回-会同馆驿", 93, 39, "有一个会同馆驿，三藏等径入驿内"),
    ("表2-94回-驿中饯别", 94, 39, "走至驿中。驿丞接入，看茶摆饭"),
    ("表2-98回-如来阅牒", 98, 29, "将通关文牒奉上，如来一一看了"),
    # ---- 正文内声明 ----
    ("正文4.1-54回-迎阳驿对话", 54, 13, "请他们都进驿内，正厅坐下，即唤看茶"),
    ("正文4.1-54回-启奏倒换", 54, 13, "进城启奏我王，倒换关文"),
    ("正文4.2-68回-王位言论", 68, 3, "朱紫国必是西邦王位"),
    ("正文4.2-78回-王位府州县", 78, 3, "若是西邸王位，须要倒换关文"),
    ("正文4.2-46回-用了宝印", 46, 1, "即将关文用了宝印"),
    ("正文4.3-97回-投递解状", 97, 67, "投递解状"),
    ("正文5.3-87回-直符使者", 87, None, "直符使者"),
]


def load_chapters():
    js = TS_JS.read_text(encoding="utf-8")
    out = {}
    for num in range(1, 101):
        pat = re.compile(
            r"num:\s*" + str(num) + r",\s*\n\s*title:\s*\"[^\"]*\",\s*\n\s*fullTitle:\s*\"[^\"]*\",\s*\n\s*text:\s*`([^`]*)`",
            re.DOTALL,
        )
        m = pat.search(js)
        if m:
            out[num] = m.group(1)
    return out


def line_of(text: str, frag: str) -> int | None:
    idx = text.find(frag)
    if idx < 0:
        return None
    return text.count("\n", 0, idx) + 1


def locate(text: str, frag: str) -> tuple[int | None, str]:
    """先整段精确定位；失败则按标点切分降级，返回 (行号, 实际命中片段)。"""
    line = line_of(text, frag)
    if line:
        return line, frag
    for part in re.split(r"[，。；、·]", frag):
        part = part.strip()
        if len(part) >= 3:
            line = line_of(text, part)
            if line:
                return line, part
    return None, ""


def main() -> int:
    chapters = load_chapters()
    results = []
    ok = mismatch = notfound = 0
    for src, num, claimed, frag in CLAIMS:
        text = chapters.get(num, "")
        line, hit = locate(text, frag)
        if line is None:
            status = "NOT_FOUND"
            notfound += 1
        elif claimed is None:
            status = "OK~" if True else ""
            ok += 1
        elif line == claimed:
            status = "OK"
            ok += 1
        else:
            status = "MISMATCH"
            mismatch += 1
        results.append(
            {"source": src, "chapter": num, "claimed_line": claimed,
             "snippet": frag, "actual_line": line, "hit": hit, "status": status}
        )
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print("total:", len(CLAIMS), "| OK:", ok, "| MISMATCH:", mismatch, "| NOT_FOUND:", notfound)
    for r in results:
        if r["status"] != "OK":
            print(json.dumps(r, ensure_ascii=False))

    # ---- 逐条 NOT_FOUND 的降级诊断：候选子串实际落点 ----
    diag = {
        74: ["八百里狮驼岭", "三魔头", "三个魔头", "狮驼"],
        100: ["通关文牒", "取上来", "缴纳", "缴"],
        29: ["金亭馆驿", "乱传乱嚷", "嚷到"],
    }
    for num, frags in diag.items():
        text = chapters.get(num, "")
        print("== ch", num, "| len:", len(text))
        for f in frags:
            positions, i = [], 0
            while True:
                i = text.find(f, i)
                if i < 0 or len(positions) >= 3:
                    break
                positions.append(text.count("\n", 0, i) + 1)
                i += 1
            print("   ", f, "->", positions or "NOT FOUND")

    # ---- 全库扫描关键串（定位「金亭馆驿」等实际出现位置）----
    for f in ["金亭馆驿", "乱传乱嚷", "宝象国", "馆驿"]:
        hits = []
        for num, text in sorted(chapters.items()):
            i = 0
            while True:
                i = text.find(f, i)
                if i < 0 or len(hits) >= 12:
                    break
                hits.append((num, text.count("\n", 0, i) + 1))
                i += 1
        print("全库扫描:", f, "->", hits or "全库无")
    print("written:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())