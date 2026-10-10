"""_w695_mount_csp.py — W695 两裁决落盘（一次性）：第 39 门禁挂载 + CSP 白名单收紧。

1) check_story_timeline_sync.py 加门禁汇总行（38 槽同款 marker 形态）
2) verify_delivery.py：VERIFY_SECTIONS 追加「时间线双源」+ 第 39 槽 wrapper 块（crash 即拦+防静默跳过）
3) generate_csp.py：EXTERNAL_SCRIPT_HOSTS 清空（W456 禁外域后零引用·grep 实证）+ docstring 同步
4) AGENTS §4.2 第 39 条目 + 文档规范 §8 引用式行对齐
全部替换带命中断言，零命中即中止。
"""
import sys

ROOT = r"D:\xiyouji"


def edit(rel, pairs):
    p = ROOT + "\\" + rel.replace("/", "\\")
    s = open(p, encoding="utf-8", newline="").read()
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, "expect 1 hit in %s for %r..., got %d" % (rel, old[:60], n)
        s = s.replace(old, new, 1)
    open(p, "w", encoding="utf-8", newline="").write(s)
    print("OK %s (%d edits)" % (rel, len(pairs)))


def main():
    # 1) 校验器汇总行
    edit("scripts/check_story_timeline_sync.py", [
        ('''    n = len(parse_py())
    print("OK 故事内时间线双源一致（KEY_EVENTS %d 条 == EMBEDDED_DATA %d 条·phase 区间全匹配）" % (n, n))
    return 0''',
         '''    n = len(parse_py())
    print("OK 故事内时间线双源一致（KEY_EVENTS %d 条 == EMBEDDED_DATA %d 条·phase 区间全匹配）" % (n, n))
    print("---- 第 39 门禁 故事内时间线双源同步：KEY_EVENTS %d 条 == EMBEDDED_DATA %d 条 · 失配 0 · phase 区间全匹配 ----" % (n, n))
    return 0'''),
        ('''        print("FAIL 故事内时间线双源失配 %d 项：" % len(issues))
        for s in issues[:10]:
            print("  -", s)
        return 1''',
         '''        print("FAIL 故事内时间线双源失配 %d 项：" % len(issues))
        for s in issues[:10]:
            print("  -", s)
        print("---- 第 39 门禁 故事内时间线双源同步：失配 %d 项 ----" % len(issues))
        return 1'''),
    ])

    # 2) verify_delivery.py：名单 + 第 39 槽块
    gate39_block = '''    section("时间线双源")
    # ---- 故事内时间线双源同步门禁（第 39 槽·W695 用户裁决：六轮外审 P1-4——
    # timeline.py KEY_EVENTS 与 story-timeline.html EMBEDDED_DATA 为人工同步，
    # 本门禁即机器防线：逐条比对 chapter/event/characters/顺序 + phase 区间映射。wrapper 同款）----
    ts_py = os.path.join(_HERE, "check_story_timeline_sync.py")
    try:
        r = subprocess.run([sys.executable, ts_py], capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail("时间线双源门禁执行异常（第 39 槽·crash 即拦）: %s" % e)
    else:
        tail = (r.stdout.splitlines()[-1:] + r.stderr.splitlines()[-2:])
        if r.returncode != 0:
            fail("时间线双源失配（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
        elif "---- 第 39 门禁 故事内时间线双源同步：" not in r.stdout:
            fail("时间线双源门禁输出缺汇总行（疑似未真正执行·防静默跳过）：%r" % r.stdout[-160:])
        else:
            ok("时间线双源门禁通过（%s）" % (r.stdout.splitlines()[-2] if len(r.stdout.splitlines()) >= 2 else "无输出"))


    # ---- 可选：RAG /health 探活（仅告警，不阻断）----'''
    edit("scripts/verify_delivery.py", [
        ('"声明分隔", "孤立选择", "kpi基类", "内嵌残留",',
         '"声明分隔", "孤立选择", "kpi基类", "内嵌残留", "时间线双源",'),
        ('''
    # ---- 可选：RAG /health 探活（仅告警，不阻断）----''',
         "\n" + gate39_block),
    ])

    # 3) generate_csp.py：白名单清空 + docstring
    edit("scripts/generate_csp.py", [
        ("  - script-src 'self' + d3js.org/cdnjs（外部脚本白名单，与 SRI 加固同源）",
         "  - script-src 'self'（W695 起外部脚本白名单移除——W456 禁外域 CDN 后全站零外域脚本加载，grep 实证无引用）"),
        ('EXTERNAL_SCRIPT_HOSTS = ["https://d3js.org", "https://cdnjs.cloudflare.com"]',
         'EXTERNAL_SCRIPT_HOSTS = []  # W695 收紧：W456 禁外域 CDN 后零引用（grep 实证），script-src 仅 self+哈希'),
    ])

    # 4) 文档规范 §8 引用式行
    edit("docs/00-导读/文档规范.md", [
        ("| `scripts/verify_delivery.py` | 门禁体系编号至第 38 门禁",
         "| `scripts/verify_delivery.py` | 门禁体系编号至第 39 门禁"),
        ("·页面内嵌残留标记（W693：check_embedded_stale_markers.py 第 38 门禁——json 副本修复批的 EMBEDDED 双路径回归·修复前旧值即标记·随批登记） | pre-commit（每次 commit） |",
         "·页面内嵌残留标记（W693：check_embedded_stale_markers.py 第 38 门禁——json 副本修复批的 EMBEDDED 双路径回归·修复前旧值即标记·随批登记）·故事内时间线双源同步（W695：check_story_timeline_sync.py 第 39 门禁——timeline.py KEY_EVENTS 与 story-timeline.html EMBEDDED_DATA 逐条比对+phase 区间映射） | pre-commit（每次 commit） |"),
    ])

    # 5) AGENTS §4.2 第 39 条目
    edit("AGENTS.md", [
        ("；--self-test 注入式负样本 2 例）",
         "；--self-test 注入式负样本 2 例）\n"
         "39. **故事内时间线双源同步**（check_story_timeline_sync.py --self-test 三负样本，W695 挂载·第 39 门禁：六轮外审 P1-4——timeline.py KEY_EVENTS 与 site/data/story-timeline.html EMBEDDED_DATA 为人工同步的机器防线：逐条比对 chapter/event/characters/顺序 + phase 区间映射；失配即 FAIL 阻断；改锚点须同批重灌页内嵌副本并重跑 generate_csp）"),
    ])

    print("ALL-MOUNTED")


if __name__ == "__main__":
    sys.exit(main())
