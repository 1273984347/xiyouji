#!/usr/bin/env python3
"""W678 批次六数据修复总脚本（WP-6.2/6.3/6.6/6.7·部署副本层 15 文件 + 真源/生成器 2 件）。

原则（B-8 惯例）：机械/注记级直改；语义口径类只加注记不改正值；
生成器层先行（cave_estate/character_appearance 由生成器重建后 sync）。
每处替换带出现次数断言，任一失配即整体中止不落盘。
前置：_w678_fixes 假定生成器已重跑（由 run() 内嵌 subprocess 完成）。
"""
import json
import subprocess
import sys

GEN1 = "scripts/M_洞府房产/cave_estate.py"
GEN2 = "scripts/B_人物/character_appearance.py"


def tload(f):
    return open(f, encoding="utf-8", newline="").read()


def tsave(f, t):
    open(f, "w", encoding="utf-8", newline="").write(t)


def tsub(f, old, new, n=1):
    t = tload(f)
    nl = "\r\n" if "\r\n" in t else "\n"
    old, new = old.replace("\n", nl), new.replace("\n", nl)
    c = t.count(old)
    if c == 0 and t.count(new) >= n:
        print("SKIP 已应用 %s：%r" % (f.split("/")[-1], old[:30]))
        return
    assert c == n, "%s: %r 期望 %d 实得 %d" % (f, old[:40], n, c)
    tsave(f, t.replace(old, new))
    print("OK 字面 %s：%r x%d" % (f.split("/")[-1], old[:30], n))


def jedit(f, fn):
    """json 结构编辑：保持键序，indent 2，ensure_ascii False，尾换行保形；无变化/已完成态即跳过。"""
    raw = tload(f)
    trailing = raw.endswith("\n")
    nl = "\r\n" if "\r\n" in raw else "\n"
    d = json.loads(raw)
    before = json.dumps(d, ensure_ascii=False, sort_keys=True)
    try:
        fn(d)
    except AssertionError:
        print("SKIP 已应用(断言态) %s" % f.split("/")[-1])
        return
    if json.dumps(d, ensure_ascii=False, sort_keys=True) == before:
        print("SKIP 已应用 %s" % f.split("/")[-1])
        return
    out = json.dumps(d, ensure_ascii=False, indent=2).replace("\n", nl)
    if trailing:
        out += nl
    tsave(f, out)
    print("OK 结构 %s" % f.split("/")[-1])


def main():
    dry = "--dry" in sys.argv

    # ---------- 真源 + 生成器层 ----------
    tsub("dataset/cave-estate.json", "万圣公主遗物珠玉满堂", "万岁狐王遗物珠玉满堂")
    tsub(GEN1, '"name": "白虎洞"', '"name": "波月洞"')
    tsub(GEN1, '" mischief石碣、铁板桥、瀑布天帘"', '"石碣、铁板桥、瀑布天帘"')
    tsub(GEN1, "万圣公主遗物珠玉满堂", "万岁狐王遗物珠玉满堂")
    # character_appearance.py 已手工改（W678 覆盖表+appear 字段），此处只断言在位
    g2 = tload(GEN2)
    assert '"观音": 6' in g2 and '"appear_in_chapters": appear_in_chapters.get' in g2

    if not dry:
        r = subprocess.run([sys.executable, GEN1], capture_output=True, text=True)
        if r.returncode != 0:
            print("GEN FAIL", GEN1, r.stdout[-300:], r.stderr[-300:])
            sys.exit(1)
        print("GEN OK -> scripts/output/data/cave_estate.json")
        r = subprocess.run([sys.executable, "character_appearance.py", "--output", "../../scripts/output/data/character_appearance.json"],
                           capture_output=True, text=True, cwd="scripts/B_人物")
        if r.returncode != 0:
            print("GEN FAIL", GEN2, r.stdout[-300:], r.stderr[-300:])
            sys.exit(1)
        print("GEN OK -> scripts/output/data/character_appearance.json")

    # ---------- 部署副本：字面级 ----------
    D = "site/data/json/"
    tsub(D + "character_cards.json", "/demo 求助观音", "求助观音")
    tsub(D + "cave_by_owner_rank.json", "中将级", "妖将级")
    tsub(D + "monster_ipo.json", "STD：", "STD:", 5)
    tsub(D + "east_asia_amplification.json", "《悟空传》《大猿王》", "《悟空传》")
    tsub(D + "heart_sutra_sculpture.json", "灵山·成佛归零", "灵山·最终归零")
    tsub(D + "webnovel_adaptations.json", "却被如来一棒打死", "却被悟空一棒打杀·如来识破真身")
    tsub(D + "scent_map.json", "沙僧盘踞·水深仅 1m 但充满陷阱", "沙僧盘踞·弱水三千鹅毛不浮")
    tsub(D + "project_review.json", "5 人晋升佛位", "唐僧、悟空师徒二人成佛")
    tsub(D + "project_review.json", "贞观27年", "贞观27年（原著纪年）", 2)
    tsub(D + "narrative_cards.json", "一扇扇出八万四千里·但对火系无效",
         "一扇扇出八万四千里·专克火系（第 59-61 回扇灭火焰山）")
    tsub(D + "narrative_cards.json", "物理伤害×1.5·但对女性妖怪伤害-50%", "物理伤害×1.5")

    # ---------- 部署副本：结构级 ----------
    def fn_decon(d):
        if d["year_range"][0] == 1986 and "east_asia_receptions_detail" in d:
            raise AssertionError("done")
        assert d["year_range"][0] == 1979
        d["year_range"][0] = 1986
        d["east_asia_receptions_detail"] = "明细见同目录 east_asia_receptions.json（9 条，2026-10-09 W678 关联注记）"
    jedit(D + "deconstruction_summary.json", fn_decon)

    def fn_dial(d):
        d["avg_sentiment_note"] = "口径注记（W678）：avg_sentiment 为词典强度累加值（非归一化均值），个别条目可超出 [-1,1]，属口径特征非数据错误"
        d["other_speakers"] = 46
        d["chapter_coverage_note"] = "chapter_sentiment 缺第 9/10/11 回：归属管线在该三回 0 条带引号归属语（生成器重跑确定性复现），补提需扩归属算法，属作者裁决项（W678 登记）"
    jedit(D + "dialogue_sentiment.json", fn_dial)

    def fn_vn(d):
        for e in d:
            if e.get("year") == "1990s":
                del e["year"]
                e["year_start"] = 1990
                e["year_end"] = 1999
    jedit(D + "east_asia_receptions.json", fn_vn)

    def fn_geo(d):
        d["duration_note"] = "nodes[].duration 为两界节点间的回目停留跨度（非自然年），W678 注记"
    jedit(D + "journey_geo_3d.json", fn_geo)

    def fn_vil(d):
        fix = {"左上": ([7, 10], [7, 10], 1), "右上": ([0, 6], [7, 10], 7),
               "左下": ([0, 6], [0, 6], 6), "右下": ([7, 10], [0, 6], 1)}
        for q in d["quadrants"]:
            xr, yr, cnt = fix[q["quadrant"]]
            q["x_range"], q["y_range"], q["example_count"] = xr, yr, cnt
    jedit(D + "villain_matrix.json", fn_vil)

    def fn_roi(d):
        d["scoring_note"] = "roi_score 为主观综合评分（综合效率/消耗/成本/耗时/威望五因子人工裁定），非 formula 公式直算值；公式用于展示思维框架（W678 注记）"
    jedit(D + "rescue_roi.json", fn_roi)

    # 美猴王首现回（text-search 前置实证：第 1 回须有「美猴王」）
    ts = json.load(open("dataset/text-search.json", encoding="utf-8"))
    ch1 = next(c for c in ts["chapters"] if c["num"] == 1)["text"]
    assert "美猴王" in ch1, "text-search 第 1 回无美猴王，勿改"

    def fn_tb(d):
        cur = [e["chapter_first"] for e in d if e["chinese"] == "美猴王"]
        if cur == [1]:
            raise AssertionError("done")
        assert cur == [4], cur
        for e in d:
            if e["chinese"] == "美猴王":
                e["chapter_first"] = 1
    jedit(D + "translation_bias.json", fn_tb)

    # ---------- 生成器链同步 ----------
    if not dry:
        r = subprocess.run([sys.executable, "scripts/sync_data_json.py",
                            "--files", "cave_estate.json,character_appearance.json"],
                           capture_output=True, text=True)
        print(r.stdout.strip()[-300:])
        if r.returncode != 0:
            print(r.stderr[-300:])
            sys.exit(1)

    # ---------- 自检（方案机判口径） ----------
    checks = [
        ("site/data/json/cave_estate.json", "白虎洞", 0),
        ("site/data/json/cave_estate.json", "mischief", 0),
        ("site/data/json/cave_estate.json", "万圣公主遗物", 0),
        ("dataset/cave-estate.json", "万圣公主遗物", 0),
        ("site/data/json/character_cards.json", "/demo", 0),
        ("site/data/json/cave_by_owner_rank.json", "中将级", 0),
        ("site/data/json/monster_ipo.json", "：", 0),
        ("site/data/json/east_asia_amplification.json", "《大猿王》", 1),  # 日本条目代表作为专名保留
        ("site/data/json/heart_sutra_sculpture.json", "成佛归零", 0),
        ("site/data/json/project_review.json", "5 人晋升佛位", 0),
        ("site/data/json/narrative_cards.json", "对火系无效", 0),
        ("site/data/json/narrative_cards.json", "女性妖怪", 0),
        ("site/data/json/webnovel_adaptations.json", "如来一棒打死", 0),
        ("site/data/json/scent_map.json", "水深仅", 0),
    ]
    bad = 0
    for f, pat, want in checks:
        c = tload(f).count(pat)
        flag = "" if c == want else "  <-- FAIL"
        if c != want:
            bad += 1
        print("%s %r=%d（期望 %d）%s" % (f.split("/")[-1], pat[:24], c, want, flag))
    # 结构断言
    ca = json.load(open(D + "character_appearance.json", encoding="utf-8"))
    nonempty = sum(1 for c in ca["characters"] if c.get("appear_in_chapters"))
    guanyin = next(c for c in ca["characters"] if c["name"] == "观音")
    print("appear 非空率: %d/%d" % (nonempty, len(ca["characters"])))
    print("观音 first_chapter =", guanyin["first_chapter"])
    print("玉帝 first_chapter =", next(c["first_chapter"] for c in ca["characters"] if c["name"] == "玉帝"))
    if nonempty != len(ca["characters"]) or guanyin["first_chapter"] != 6:
        bad += 1
    print("OK 自检失败 %d%s" % (bad, "（dry）" if dry else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
