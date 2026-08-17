#!/usr/bin/env python3
"""
verify_delivery.py — 零依赖交付校验门禁（Senior Developer 设立）

解决两类工程顽疾：
  1) 「旧疾」：单文件连续多次 Edit 时描述段丢失 → 校验文档均含最新版本号 + W### 里程碑 token。
  2) 「范围漂移」：已评审/已记录 scope 之外又发生了改动（如 html 里出现 W334 标记但文档只记到 W333）
     → 校验 site/dukou-engine.html 中引用的所有 W### 是否都已在文档中记录。

降级六文档同步（W393）：
  - 核心 2 份（CHANGELOG.md / 交接文档.md）= 跨 session 连续性真载体，缺失 v/W 仍【阻断】。
  - 辅助 4 份（README.md / STRUCTURE.md / 项目说明.md / file-index.md）= 每次 W### 的纯手工税，
    缺失仅【WARN 不阻断】，里程碑时跑 scripts/bump_version.py 一键补齐。

零依赖：仅标准库。可直接运行：
  python scripts/verify_delivery.py            # 静态校验（提交前门禁）
  python scripts/verify_delivery.py --health   # 额外探测 RAG /health（环境项，仅告警不阻断）

退出码：核心 FAIL 1；仅辅助 WARN 0。可直接挂到 .git/hooks/pre-commit（辅助 WARN 不再阻断提交）。
"""

import json
import os
import re
import subprocess
import sys
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, ".."))  # scripts/.. = 项目根 xiyouji

# 降级六文档同步（W393）：核心 2 份硬门禁，辅助 4 份仅 WARN 不阻断
# W413 修正（2026-08-09）：严格审查后交接文档恢复入库（无敏感内容），恢复为核心硬门禁
CORE_DOCS = [
    "CHANGELOG.md",
    "交接文档.md",
]
AUX_DOCS = [
    "README.md",
    "STRUCTURE.md",
    os.path.join("docs", "00-导读", "项目说明.md"),
    os.path.join("scripts", "output", "file-index.md"),
]
DOCS = CORE_DOCS + AUX_DOCS
HTML = os.path.join(ROOT, "site", "dukou-engine.html")

# 四份含 A4 计数语义的文档（W413 修正：交接文档恢复入库，恢复 4 份检查）
A4_DOCS = ["README.md", "STRUCTURE.md",
           os.path.join("docs", "00-导读", "项目说明.md"), "交接文档.md"]
EXPECT_A4 = "209 篇"  # 真实计数（W342 199→201 起步，W400 后实际 209）

# 归档文件（W417 新增）：归档后旧 W### 仍纳入范围漂移可追溯扫描，避免误报
ARCHIVE_DOCS = [
    "CHANGELOG-ARCHIVE.md",
    os.path.join("scripts", "output", "file-index-archive.md"),
    "交接文档-archive.md",
]

# A1-A6 内容板块真实文件计数 vs README 声明（W417 新增，防计数声明失真）
A_AREAS = [
    ("A1 逐回解读", os.path.join("docs", "01-全书逐回解读")),
    ("A2 个人随笔", os.path.join("docs", "06-个人随笔")),
    ("A3 人物分析", os.path.join("docs", "02-人物深度分析")),
    ("A4 主题专题", os.path.join("docs", "03-主题与情节专题")),
    ("A5 文化背景", os.path.join("docs", "04-文化与历史背景")),
    ("A6 诗词歌赋", os.path.join("docs", "05-诗词歌赋")),
]


def _count_content_md(area_dir):
    """统计板块 .md 文件数，排除 README.md/.gitkeep 等非正文文件（各板块恰好 1 个 README.md）"""
    p = os.path.join(ROOT, area_dir)
    if not os.path.isdir(p):
        return -1
    return sum(1 for fn in os.listdir(p)
               if fn.endswith(".md") and fn.lower() != "readme.md")


def _read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def main():
    fails = 0
    warns = 0

    def fail(msg):
        nonlocal fails
        fails += 1
        print("FAIL  " + msg)

    def warn(msg):
        nonlocal warns
        warns += 1
        print("WARN  " + msg)

    def ok(msg):
        print("OK    " + msg)

    # ---- 读取 html，提取 footer 版本 + 扫描所有 W### ----
    html = _read(HTML)
    if not html:
        fail("找不到 %s（未生成或被忽略）" % HTML)
    m = re.search(r"v(\d+\.\d+\.\d+)\s+W(\d+)", html)
    ver = m.group(1) if m else None
    wnum = m.group(2) if m else None
    html_w = [int(x) for x in re.findall(r"W(\d{3})", html)]
    max_w_html = max(html_w) if html_w else 0

    if ver and wnum:
        ok("dukou-engine.html footer 版本 v%s W%s" % (ver, wnum))
    else:
        fail("dukou-engine.html footer 未解析出 vX.Y.Z W###")

    # ---- 降级六文档同步校验（W393）----
    # 核心 2 份（CHANGELOG/交接文档）缺失 v/W → 阻断；
    # 辅助 4 份（README/STRUCTURE/项目说明/file-index）缺失 → WARN 不阻断。
    doc_all = ""
    for d in DOCS:
        p = os.path.join(ROOT, d)
        c = _read(p)
        doc_all += c
        core = d in CORE_DOCS
        if not c:
            if core:
                fail("缺失核心文档: %s" % d)
            else:
                warn("缺失辅助文档（不阻断，可跑 scripts/bump_version.py）: %s" % d)
            continue
        if ver and ("v" + ver) not in c:
            if core:
                fail("%s 不含版本 v%s（旧疾风险·核心阻断）" % (d, ver))
            else:
                warn("%s 不含版本 v%s（辅助文档，跑 scripts/bump_version.py 同步，不阻断）" % (d, ver))
            continue
        if wnum and ("W" + wnum) not in c:
            if core:
                fail("%s 不含 W%s 里程碑 token（旧疾风险·核心阻断）" % (d, wnum))
            else:
                warn("%s 不含 W%s 里程碑 token（辅助文档，跑 scripts/bump_version.py 同步，不阻断）" % (d, wnum))
            continue
        ok("%s 含 v%s / W%s" % (d, ver, wnum))

    # ---- 范围漂移检测 ----
    doc_w = [int(x) for x in re.findall(r"W(\d{3})", doc_all)]
    # W417：归档文件纳入扫描——归档后旧 W### 仍可追溯，不因归档误报范围漂移
    for a in ARCHIVE_DOCS:
        doc_w += [int(x) for x in re.findall(r"W(\d{3})", _read(os.path.join(ROOT, a)))]
    max_w_doc = max(doc_w) if doc_w else 0
    if max_w_html > max_w_doc:
        fail("范围漂移：%s 引用到 W%d，但六文档+归档最高仅记到 W%d（疑似未记录的改动，需补记或回退）"
             % (os.path.basename(HTML), max_w_html, max_w_doc))
    else:
        ok("无范围漂移（html 最高 W%d ≤ 文档+归档最高 W%d）" % (max_w_html, max_w_doc))

    # ---- A4 计数一致性 ----
    miss = []
    for d in A4_DOCS:
        c = _read(os.path.join(ROOT, d))
        if EXPECT_A4 not in c:
            miss.append(d)
    if miss:
        fail("A4 计数不一致（缺 '%s'）：%s" % (EXPECT_A4, ", ".join(miss)))
    else:
        ok("A4 计数一致（四份文档均含 '%s'）" % EXPECT_A4)

    # ---- A1-A6 真实文件计数 vs README 声明（W417 新增，防计数声明失真）----
    readme_txt = _read(os.path.join(ROOT, "README.md"))
    m_cnt = re.search(r"共\s*(\d+)\s*篇", readme_txt)
    actual_total = 0
    for name, d in A_AREAS:
        n = _count_content_md(d)
        if n < 0:
            warn("%s 目录缺失: %s" % (name, d))
            continue
        actual_total += n
    if m_cnt:
        declared = int(m_cnt.group(1))
        if actual_total == declared:
            ok("A1-A6 真实文件计数 %d 篇 == README 声明 %d 篇（排除各板块 README.md）" % (actual_total, declared))
        else:
            fail("A1-A6 真实文件计数 %d 篇 != README 声明 %d 篇（计数漂移，需同步 README 声明）"
                 % (actual_total, declared))
    else:
        warn("README 未找到 '共 N 篇' 声明，跳过 A1-A6 计数校验")

    # ---- 学术研究 轨显式引用门禁（W452 新增：可核查引用硬性化）----
    acad_total = 0
    acad_missing = []
    for r, _, fns in os.walk(os.path.join(ROOT, "docs")):
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            c = _read(os.path.join(r, fn))
            m = re.search(r"^> 轨标：([^\r\n]+)", c, re.M)
            if not m or m.group(1).strip() != "学术研究":
                continue
            acad_total += 1
            if not re.search(r"^> 引用：.*学术论文索引", c, re.M):
                acad_missing.append(os.path.join(r, fn))
    if acad_total == 0:
        warn("未发现 学术研究 轨文档，跳过显式引用门禁")
    elif acad_missing:
        fail("学术研究 轨文档 %d 篇缺显式引用（缺 '> 引用：' 学术论文索引 链接）：%s"
             % (len(acad_missing), ", ".join(acad_missing[:5])))
    else:
        ok("学术研究 轨文档 %d 篇均含显式引用（> 引用：学术论文索引 链接）" % acad_total)

    # ---- A1 导航相邻性断言（W422 新增：W418 只保证"每回有导航行"不保证指向相邻回）----
    ch_dir = os.path.join(ROOT, "docs", "01-全书逐回解读")
    nav_fail = []
    if os.path.isdir(ch_dir):
        for fn in sorted(os.listdir(ch_dir)):
            m = re.match(r"^第(\d+)回-", fn)
            if not m or not fn.endswith(".md"):
                continue
            num = int(m.group(1))
            c = _read(os.path.join(ch_dir, fn))
            nm = re.search(r"(?m)^>\s*导航：.*$", c)
            if not nm:
                nav_fail.append("第%d回 无导航行" % num)
                continue
            line = nm.group(0)
            pm = re.search(r"\[上一回\]\(第(\d+)回", line)
            xm = re.search(r"\[下一回\]\(第(\d+)回", line)
            if num > 1:
                if not pm or int(pm.group(1)) != num - 1:
                    nav_fail.append("第%d回 上一回 -> %s（期望第%d回）" % (num, pm.group(1) if pm else "无", num - 1))
            elif pm:
                nav_fail.append("第1回 不应有上一回链接")
            if num < 100:
                if not xm or int(xm.group(1)) != num + 1:
                    nav_fail.append("第%d回 下一回 -> %s（期望第%d回）" % (num, xm.group(1) if xm else "无", num + 1))
            elif xm:
                nav_fail.append("第100回 不应有下一回链接")
    if nav_fail:
        fail("A1 导航相邻性异常 %d 处（示例：%s）" % (len(nav_fail), nav_fail[0]))
    else:
        ok("A1 导航相邻性 100/100（上一回=N-1·下一回=N+1·第1回无上/第100回全书完）")

    # ---- docs/01 链接校验（W422：W420 曾修复 66 死链，纳入门禁防回归）----
    try:
        r = subprocess.run(
            [sys.executable, os.path.join(_HERE, "lint_links.py"),
             "--dir", os.path.join(ROOT, "docs", "01-全书逐回解读")],
            capture_output=True, text=True, timeout=180)
        if r.returncode == 0:
            ok("docs/01 链接校验通过（lint_links 0 broken）")
        else:
            tail = (r.stdout.splitlines()[-3:] + r.stderr.splitlines()[-3:])
            fail("docs/01 存在 broken 链接（lint_links exit %d）：%s" % (r.returncode, " / ".join(tail)))
    except Exception as e:
        fail("docs/01 链接校验执行异常: %s" % e)

    # ---- sitemap 覆盖校验（W422：防新增页面漏收录，W417 曾手工补 69→154）----
    sm_txt = _read(os.path.join(ROOT, "site", "sitemap.xml"))
    site_dir = os.path.join(ROOT, "site")
    EXCLUDED_SM = {
        "rum-viewer.html",
        "visit-viewer.html",
        "_template.html",
        "data/81-hardships-view.html",
        "data/character-relationship-3d-view.html",
        "data/_shell.html",
    }
    if sm_txt and os.path.isdir(site_dir):
        locs = set()
        for m in re.finditer(r"<loc>([^<]+)</loc>", sm_txt):
            u = m.group(1).strip().rstrip("/")
            u = re.sub(r"^https?://[^/]+/", "", u)
            u = u[len("xiyouji/"):] if u.startswith("xiyouji/") else u
            locs.add(u if u else "index.html")
        actual = set()
        for root, _dirs, fnames in os.walk(site_dir):
            for fn in fnames:
                if fn.endswith(".html"):
                    rel = os.path.relpath(os.path.join(root, fn), site_dir).replace("\\", "/")
                    actual.add(rel)
        expected = {x for x in actual if x not in EXCLUDED_SM}
        miss = sorted(expected - locs)
        extra = sorted(locs - expected)
        if miss or extra:
            fail("sitemap 与 site 不一致：缺 %d 页（%s）、多余 %d 页（%s）"
                 % (len(miss), miss[:3], len(extra), extra[:3]))
        else:
            ok("sitemap 覆盖一致（%d 页，排除统计/预览页 %d 个）" % (len(locs), len(EXCLUDED_SM)))
    else:
        warn("sitemap.xml 或 site/ 缺失，跳过 sitemap 覆盖校验")

    # ---- site/data 内嵌回退模式静态检查（W422：file:// 铁律的自动验证）----
    data_dir = os.path.join(ROOT, "site", "data")
    EMB_RE = re.compile(r"EMBEDDED_DATA|const\s+EMBEDDED|FALLBACK|INLINE|MOCK_DATA|const\s+data\s*=|text-search-app")
    no_emb = []
    data_count = 0
    if os.path.isdir(data_dir):
        for fn in sorted(os.listdir(data_dir)):
            if fn.endswith(".html"):
                data_count += 1
                if not EMB_RE.search(_read(os.path.join(data_dir, fn))):
                    no_emb.append(fn)
    if no_emb:
        fail("site/data 有 %d/%d 页缺内嵌回退模式（file:// 直开风险）：%s"
             % (len(no_emb), data_count, ", ".join(no_emb[:5])))
    else:
        ok("site/data %d 页均含内嵌回退模式（EMBEDDED_DATA/EMBEDDED/FALLBACK/inline data）" % data_count)

    # ---- M2 双源漂移检查（W424：内嵌数据 vs scripts/output/data JSON 数组长度）----
    # 防"内嵌副本为空/过期、线上 fetch 404 后回退到错误数据"（81-hardships 先例）
    drift_js = os.path.join(ROOT, "scripts", "check_data_drift.js")
    try:
        r = subprocess.run(["node", drift_js], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("数据漂移检查通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("数据漂移检查失败（exit %d）：%s" % (r.returncode, " / ".join(tail)))
    except FileNotFoundError:
        warn("node 不可用，跳过数据漂移检查（W424 M2）")
    except Exception as e:
        warn("数据漂移检查执行异常（W424 M2）: %s" % e)

    # ---- CSP 漂移检查（W424：全站 CSP meta 必须与内联脚本哈希一致）----
    # 改任何内联脚本后未重跑 generate_csp.py 会在此拦截（页面脚本会被 CSP 拦死）
    csp_py = os.path.join(_HERE, "generate_csp.py")
    try:
        r = subprocess.run(
            [sys.executable, csp_py, "--check"],
            capture_output=True, text=True, timeout=180,
        )
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("CSP 校验通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("CSP 漂移（exit %d）：%s（改内联脚本后须重跑 python scripts/generate_csp.py）"
                 % (r.returncode, " / ".join(tail)))
    except Exception as e:
        warn("CSP 校验执行异常（W424）: %s" % e)

    # ---- 腐蚀/插件引用门禁（W424 复盘沉淀：EN 腐蚀第二波 + sankey 漏引防复发）----
    corr_py = os.path.join(_HERE, "check_corruption.py")
    try:
        r = subprocess.run([sys.executable, corr_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("腐蚀/插件引用门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("腐蚀/插件引用门禁失败（exit %d）：%s" % (r.returncode, " / ".join(tail)))
    except Exception as e:
        warn("腐蚀/插件引用门禁执行异常（W424 复盘沉淀）: %s" % e)

    # ---- 内联脚本语法门禁（W457：EN 引号/撇号/键名腐蚀致 SyntaxError 曾 7 页漏网）----
    js_syntax_js = os.path.join(_HERE, "check_js_syntax.js")
    try:
        r = subprocess.run(["node", js_syntax_js], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("内联脚本语法门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("内联脚本语法错误（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except FileNotFoundError:
        warn("node 不可用，跳过内联脚本语法门禁（W457）")
    except Exception as e:
        warn("内联脚本语法门禁执行异常（W457）: %s" % e)

    # ---- CSS 结构平衡门禁（W457：url() 缺右括号致整页 CSS 裸奔白屏，222 页先例）----
    struct_py = os.path.join(_HERE, "check_structure.py")
    try:
        r = subprocess.run([sys.executable, struct_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("CSS 结构平衡通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("CSS 结构异常（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("CSS 结构平衡门禁执行异常（W457）: %s" % e)

    # ---- 动态链接门禁（W459：lint_links 只扫静态 href，JS 拼接链接曾致 D2 回目跳转全 404 漏网）----
    dyn_links_py = os.path.join(_HERE, "check_dynamic_links.py")
    try:
        r = subprocess.run([sys.executable, dyn_links_py], capture_output=True, text=True, timeout=120)
        tail = (r.stdout.splitlines()[-2:] + r.stderr.splitlines()[-2:])
        if r.returncode == 0:
            ok("动态链接门禁通过（%s）" % (tail[0] if tail else "无输出"))
        else:
            fail("动态链接死链（exit %d）：%s" % (r.returncode, " / ".join(tail[:6])))
    except Exception as e:
        warn("动态链接门禁执行异常（W459）: %s" % e)

    # ---- 可选：RAG /health 探活（仅告警，不阻断）----
    if "--health" in sys.argv:
        try:
            r = urllib.request.urlopen("http://127.0.0.1:8777/health", timeout=5)
            body = json.loads(r.read().decode("utf-8"))
            ok("/health 存活：%s" % body)
        except Exception as e:
            print("WARN  /health 不可达（环境项，不阻断提交）：%s" % e)

    print("\n==== 交付校验汇总 ====")
    if fails == 0:
        print("核心全部通过 ✅" + ("（%d 项辅助 WARN，不阻断）" % warns if warns else ""))
        return 0
    print("%d 项核心 FAIL ❌（%d 项辅助 WARN）" % (fails, warns))
    return 1


if __name__ == "__main__":
    sys.exit(main())
