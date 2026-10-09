"""W691 七小项落地：BL-7C 卡池借扇注记 / BL-8B counterfactual 性质注记 / BL-9B domino 时点注记
/ BL-11A 稀柿同→衕（md 源头+text-search 重建）/ BL-14A 到达回口径统一 / BL-15B 阶段口径注记
/ BL-16B alert_level 格式统一。幂等：已应用态跳过。"""
import json
import re
import sys

D = "site/data/json/"


def jload(f):
    return json.load(open(D + f, encoding="utf-8"))


def jsave(f, d):
    raw = open(D + f, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    out = json.dumps(d, ensure_ascii=False, indent=2)
    if raw.endswith("\n"):
        out += nl
    open(D + f, "w", encoding="utf-8", newline="").write(out.replace("\n", nl) if nl != "\n" else out)
    print("OK", f)


def main():
    # ---------- BL-7C：牛魔王卡芭蕉扇·借 机制注记 ----------
    cc = jload("character_cards.json")
    niu = next(c for c in cc if c.get("character") == "牛魔王")
    if "lore_note" not in niu:
        niu["lore_note"] = ("「芭蕉扇·借」机制原型为原著第 59-61 回三借芭蕉扇（一借得假扇、二借强索、"
                            "三借众神助阵），卡面为简化口径（W691 BL-7 注记）")
        jsave("character_cards.json", cc)
    else:
        print("SKIP character_cards（已有 lore_note）")

    # ---------- BL-8B：counterfactual_summary 性质注记 ----------
    cs = jload("counterfactual_summary.json")
    if "nature_note" not in cs:
        cs["nature_note"] = ("性质注记（W691 BL-8）：本文件及 counterfactual_scenarios.json 为架空推演"
                             "（counterfactual），允许与原著细节出入（如意真仙归类、青狮白象归属表述等以推演逻辑为先），"
                             "原著事实以 text-search 语料与人物条目为准（B-C 级趣味数据惯例·W668）")
        jsave("counterfactual_summary.json", cs)
    else:
        print("SKIP counterfactual_summary")

    # ---------- BL-9B：domino 时点口径注记 ----------
    dm = jload("domino_causality.json")
    if "timing_note" not in dm:
        dm["timing_note"] = ("时点口径注记（W691 BL-9）：domino 链为叙事因果的简化建模，"
                             "个别链条时点（如紧箍咒线）按回目叙事顺序而非严格编年，跨链联动为设计推演")
        jsave("domino_causality.json", dm)
    else:
        print("SKIP domino_causality")

    # ---------- BL-11A：稀柿同→衕（md 源头）+ text-search 第 67 回重建 ----------
    md = "source/原文/分回/第067回.md"
    t = open(md, encoding="utf-8", newline="").read()
    if "稀柿同" in t:
        assert t.count("稀柿同") == 1
        t = t.replace("稀柿同", "稀柿衕")
        open(md, "w", encoding="utf-8", newline="").write(t)
        print("OK md 第067回 稀柿同→衕")
    else:
        print("SKIP md（无稀柿同）")
    tsp = "dataset/text-search.json"
    raw = open(tsp, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    d = json.loads(raw)
    c67 = next(c for c in d["chapters"] if c["num"] == 67)
    body = re.sub(r"^# 第\d+回[^\n]*\n+", "",
                  open(md, encoding="utf-8").read().split("单字解释：")[0]).strip()
    if c67["text"] != body:
        c67["text"] = body
        out = json.dumps(d, ensure_ascii=False, indent=2)
        if raw.endswith("\n"):
            out += nl
        open(tsp, "w", encoding="utf-8", newline="").write(out.replace("\n", nl) if nl != "\n" else out)
        print("OK text-search 第67回重建（衕 归一）")
    else:
        print("SKIP text-search 第67回")

    # ---------- BL-14A：geo_3d + route 统一到达回 ----------
    g3p = D + "journey_geo_3d.json"
    g3raw = open(g3p, encoding="utf-8", newline="").read()
    g3nl = "\r\n" if "\r\n" in g3raw else "\n"
    g3 = json.loads(g3raw)
    changed = False
    for n in g3["nodes"]:
        if n.get("name") == "两界山" and n.get("chapter") == "第14回":
            n["chapter"] = "第13回"
            changed = True
        if n.get("name") == "号山" and n.get("chapter") == "第40-42回":
            n["chapter"] = "第39回"
            changed = True
    if "chapter_note" not in g3:
        g3["chapter_note"] = ("chapter 口径=取经队抵达该地之回目（到达回·W691 BL-14 裁决统一）；"
                              "事件跨度见 event/正文叙述")
        changed = True
    if changed:
        out = json.dumps(g3, ensure_ascii=False, indent=2)
        if g3raw.endswith("\n"):
            out += g3nl
        open(g3p, "w", encoding="utf-8", newline="").write(out.replace("\n", g3nl) if g3nl != "\n" else out)
        print("OK journey_geo_3d（两界山13/号山39/口径注记）")
    else:
        print("SKIP journey_geo_3d")
    jrp = D + "journey_route.json"
    jrraw = open(jrp, encoding="utf-8", newline="").read()
    jrnl = "\r\n" if "\r\n" in jrraw else "\n"
    jr = json.loads(jrraw)
    jchanged = False
    for p in jr["places"]:
        if p.get("place") == "浮屠山" and p.get("chapter") == 20:
            p["chapter"] = 19
            jchanged = True
    for sg in jr.get("segments", []):
        if sg.get("to_place") == "浮屠山" and sg.get("to_chapter") == 20:
            sg["to_chapter"] = 19
            jchanged = True
        if sg.get("from_place") == "浮屠山" and sg.get("from_chapter") == 20:
            sg["from_chapter"] = 19
            jchanged = True
    if "chapter_note" not in jr:
        jr["chapter_note"] = "chapter 口径=取经队抵达该地之回目（到达回·W691 BL-14 裁决统一）"
        jchanged = True
    if jchanged:
        out = json.dumps(jr, ensure_ascii=False, indent=2)
        if jrraw.endswith("\n"):
            out += jrnl
        open(jrp, "w", encoding="utf-8", newline="").write(out.replace("\n", jrnl) if jrnl != "\n" else out)
        print("OK journey_route（浮屠山19/口径注记）")
    else:
        print("SKIP journey_route")

    # ---------- BL-15B：spiral / team 阶段口径注记 ----------
    sp = jload("spiral_progress.json")
    if "stage_scope_note" not in sp:
        sp["stage_scope_note"] = ("阶段口径注记（W691 BL-15）：本文件阶段划分为心性成长维度，"
                                  "与 team_effectiveness.json 的团队效能阶段非同一口径——边界差异系维度本质，非数据矛盾")
        jsave("spiral_progress.json", sp)
    else:
        print("SKIP spiral_progress")
    te = jload("team_effectiveness.json")
    if "stage_scope_note" not in te:
        te["stage_scope_note"] = ("阶段口径注记（W691 BL-15）：本文件阶段划分为团队效能维度，"
                                  "与 spiral_progress.json 的心性成长阶段非同一口径——边界差异系维度本质，非数据矛盾")
        jsave("team_effectiveness.json", te)
    else:
        print("SKIP team_effectiveness")

    # ---------- BL-16B：trip alert_level 统一「色·标签」 ----------
    LABELS = {"双叉岭": "黄·虎狼之厄", "观音禅院·黑风山": "橙·禅院失火", "黑风洞": "橙·黑风盗宝",
              "白虎岭": "红·白骨三变", "金兜山": "红·青牛套宝", "陷空山": "红·无底洞陷师",
              "青龙山": "橙·犀牛劫"}
    trp = D + "trip_report.json"
    trraw = open(trp, encoding="utf-8", newline="").read()
    trnl = "\r\n" if "\r\n" in trraw else "\n"
    tr = json.loads(trraw)
    tchanged = False
    for e in tr:
        loc = e.get("location")
        al = e.get("alert_level")
        if loc in LABELS and al != LABELS[loc]:
            e["alert_level"] = LABELS[loc]
            tchanged = True
    if tchanged:
        out = json.dumps(tr, ensure_ascii=False, indent=2)
        if trraw.endswith("\n"):
            out += trnl
        open(trp, "w", encoding="utf-8", newline="").write(out.replace("\n", trnl) if trnl != "\n" else out)
        print("OK trip_report（alert_level 7 处统一）")
    else:
        print("SKIP trip_report")

    # ---------- 自检 ----------
    bad = 0
    if "稀柿同" in open(md, encoding="utf-8").read():
        print("FAIL md 仍有稀柿同"); bad += 1
    if "稀柿同" in open(tsp, encoding="utf-8").read():
        print("FAIL text-search 仍有稀柿同"); bad += 1
    g3 = jload("journey_geo_3d.json")
    zz = next(n for n in g3["nodes"] if n.get("name") == "两界山")
    hs = next(n for n in g3["nodes"] if n.get("name") == "号山")
    if zz["chapter"] != "第13回" or hs["chapter"] != "第39回":
        print("FAIL geo_3d 口径", zz["chapter"], hs["chapter"]); bad += 1
    jr = jload("journey_route.json")
    ft = next(p for p in jr["places"] if p.get("place") == "浮屠山")
    if ft["chapter"] != 19:
        print("FAIL route 浮屠山", ft["chapter"]); bad += 1
    tr = jload("trip_report.json")
    bare = [e["alert_level"] for e in tr if e.get("alert_level") in ("橙", "红", "黄")]
    if bare:
        print("FAIL trip 裸色残留", bare); bad += 1
    print("七小项自检失败", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
