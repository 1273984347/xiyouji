"""check_chapter_stats_sync.py — chapter_stats 双源同步校验（S-24 家族化首对·W699）。

模板：check_story_timeline_sync.py（W695）。
原理：chapter_stats.py 为纯 regex 确定性分析（无随机/无 jieba）——重跑生成器得
当前真值，与 site/data/chapter-stats.html 的 EMBEDDED_DATA（JSON 直嵌）全量比对。
gitignored 的 scripts/output/data/chapter_stats.json 不作为比对基准（CI 无此文件），
以「重跑产物」为真值使校验器在 CI 可复现。

  python scripts/check_chapter_stats_sync.py             # 校验（exit 1=漂移）
  python scripts/check_chapter_stats_sync.py --self-test # 负样本自检
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / "scripts" / "A_文本基础" / "chapter_stats.py"
HTML = ROOT / "site" / "data" / "chapter-stats.html"


def fresh_output():
    """重跑生成器得当前真值（确定性）。"""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp = Path(f.name)
    r = subprocess.run([sys.executable, str(GEN), "--output", str(tmp)],
                       capture_output=True, text=True, timeout=300, cwd=str(ROOT / "scripts"))
    if r.returncode != 0:
        raise RuntimeError("chapter_stats.py 重跑失败：" + (r.stderr or r.stdout)[-300:])
    return json.loads(tmp.read_text(encoding="utf-8"))


def page_embedded():
    """抽取页面 EMBEDDED_DATA（const 声明后首个平衡大括号块·纯 JSON 直嵌）。"""
    text = HTML.read_text(encoding="utf-8")
    m = re.search(r"const\s+EMBEDDED_DATA\s*=\s*", text)
    assert m, "页面未找到 EMBEDDED_DATA 声明"
    start = text.index("{", m.end())
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise AssertionError("EMBEDDED_DATA 块未闭合")


def flat_check(fresh, page):
    issues = []
    for k, v in fresh.items():
        if k not in page:
            issues.append("页面缺键 %s" % k)
            continue
        if isinstance(v, list):
            if len(v) != len(page[k]):
                issues.append("per_chapter 长度 %d != %d" % (len(v), len(page[k])))
            else:
                for a, b in zip(v, page[k], strict=False):
                    if a != b:
                        issues.append("%s 条目漂移：%s != %s" % (k, json.dumps(a, ensure_ascii=False), json.dumps(b, ensure_ascii=False)))
                        break
        elif page[k] != v:
            issues.append("标量 %s 漂移：%r != %r" % (k, v, page[k]))
    for k in page:
        if k not in fresh:
            issues.append("页面多键 %s" % k)
    return issues


def main():
    if "--self-test" in sys.argv:
        fresh = {"total_chapters": 100, "total_chars": 740093, "avg_chars_per_chapter": 7400.9,
                 "per_chapter": [{"chapter": "第001回", "total_chars": 7288}]}
        page_ok = dict(fresh)
        page_ok["avg_chars_per_chapter"] = 7400.9
        assert flat_check(fresh, page_ok) == [], "正样本误报"
        drift = dict(fresh, total_chars=1)
        assert flat_check(fresh, drift), "标量漂移负样本未捕获"
        drift2 = dict(fresh, per_chapter=[{"chapter": "第001回", "total_chars": 1}])
        assert flat_check(fresh, drift2), "条目漂移负样本未捕获"
        print("SELF-TEST PASS：正样本零误报 + 标量/条目两负样本全捕获")
        return 0
    fresh = fresh_output()
    page = page_embedded()
    issues = flat_check(fresh, page)
    if issues:
        print("FAIL chapter_stats 双源漂移 %d 项（以重跑产物为真值）：" % len(issues))
        for s in issues[:10]:
            print("  -", s)
        print("处置：按 W691 规则重灌页面 EMBEDDED（修复前旧值登记第 38 门禁标记）并重跑 generate_csp")
        print("---- 第 40 门禁 chapter_stats 双源同步：漂移 %d 项 ----" % len(issues))
        return 1
    print("OK chapter_stats 双源一致（重跑产物 == 页面 EMBEDDED·%d 回全量比对）" % len(page.get("per_chapter", [])))
    print("---- 第 40 门禁 chapter_stats 双源同步：重跑真值 == EMBEDDED · %d 回全量 · 漂移 0 ----" % len(page.get("per_chapter", [])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
