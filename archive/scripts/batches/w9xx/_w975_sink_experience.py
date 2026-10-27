# -*- coding: utf-8 -*-
"""_w975_sink_experience.py — W975 跨 Agent 经验沉淀入仓（坑表 + 计数链 + 深篇登记 + 台账认领）

触发：用户 2026-10-27 纠正「你不能只沉淀进你自己的 Memory 文件，本项目是多 Agent 协作的项目
所以需要你同样沉淀进本项目内」——W974 批的经验只进了 Agent 私有 Memory，仓内其他 Agent 读不到。
⚠️ 这正是坑表既有条目「共享机制必须写入仓库内文件（git tracked）」的**复发实证** ⇒ 该条目补注本批复发。

本批沉淀面（全部以 HEAD 为基底 + 原子写 + 精确暂存）：
  ① docs/agent/pitfalls.md：6 条新条目（CSS/视觉渲染 +2 · git/提交/并发 +1 · 数据/内容可信度 +2 ·
     流程/协作/取证 +1）+ 4 处节标题条数 + 共享机制条目补 W974 复发实证
  ② AGENTS.md §4.3：阅读契约条数 / 主题视图 / 六主题目录行（含各主题条数与总条数）
  ③ HANDOVER.md：两处「57 条·六主题」指针
  ④ docs/10-方法论沉淀/：深篇《素材批处理与判据自证方法论.md》+ 其 README 目录索引登记（编号 26）
  ⑤ docs/00-导读/W批次编号对账表.md：W975 认领行

用法：py -3 scripts/_w975_sink_experience.py [--dry-run]
"""
import io
import os
import subprocess
import sys

REPO = r"D:\xiyouji"
PITFALLS = "docs/agent/pitfalls.md"
AGENTS = "AGENTS.md"
HANDOVER = "HANDOVER.md"
METH = "docs/10-方法论沉淀/README.md"
METH_FILE = "docs/10-方法论沉淀/素材批处理与判据自证方法论.md"
LEDGER = "docs/00-导读/W批次编号对账表.md"

# —— 6 条新坑位条目（每条一行·含根因与修法）——
NEW_CSS = [
    "- **素材出图 prompt 里器物的「形状类别」比「数量计数」更要紧**（W974 实证·E-07/D-10）：写「金铙」二字 ⇒ 模型画成**圆环**（读作手镯/环）——形状类别错会**误读成别的题材**（须重出）；改写成「**倒扣的金钵 · 半圆盘 · 钵面一圈回纹 · 绝不是圆环或手镯**」一次画对。⇒ 描述器物必须给**几何形状 + 排除项**（「是 A·不是 B」），禁只给器物名；数量级偏差（星点数/环数）不误读则记取舍不重出（承 W942 紧箍儿九倒刺、W948 芭蕉扇叶形两先例）。",
    "- **素材选题前先验「落位页存在且尚无题图」**（W974 实证·E-08）：原定「虎力大仙」在 people 库**无独立页面**（只有「车迟国三国师」这类合并页）⇒ 出图完成后才发现无处可放，浪费一次生成。⇒ 开工前做「题材 × 落位页」双向核对（存在 + 无题图）；同一 stem 只能对应一个母版，禁两套提示词。",
]
NEW_GIT = [
    "- **写既有文件必须「临时文件 + 原子替换」——`open(path,\"wb\")` 在 write 之前就截断原文件**（W974 实证·E-03）：本批把一份 28,936 B 的 README 写成 **0 字节**（TypeError 发生在 write 阶段）⇒ 靠 `git checkout HEAD -- <path>` 恢复。⇒ 批改既有文件一律 `io.open(p+\".tmp\",\"wb\")` 写完再 `os.replace(tmp, p)`；改完立刻 `git diff --numstat` 核对增删比（≠1:1 且非新增文件 ⇒ 立即查行尾）。",
]
NEW_DATA = [
    "- **图像裁切/对齐：「整图包围盒顶」≠「主体顶」——孤立噪点会把裁切线拉歪**（W974 实证·E-01/E-02）：实测一张图顶部第 18 行仅 **3 个孤立像素**（差值 41）就把 bbox 顶从 437 拉到 18 ⇒ 站点版几乎没裁、标题与主体间仍多留约 160 px 空白（肉眼像「图缺了一块」），而**机器判据全绿**（顶部留白墨量确实≈0）。⇒ 主体顶 = **面积 ≥ 200 px² 的墨迹连通簇的最小顶**（噪点被滤掉、真实稀疏顶部如冠尖属大簇不受影响）；反向坑：**按行内墨迹像素数设阈值过粗**，会切掉主体稀疏顶部 ⇒ 整目录复算差异清单留档，既有资产**人眼判定后再决定是否批量改**，禁自动化批量改。",
    "- **校验/自检代码必须自证：检查脚本可能恒真，负样本自检函数本身可能漏覆盖**（W974 实证·E-05/E-06）：① 本批 stem 冲突检查因**前缀不匹配**（裸 stem vs `plate-line-` 前缀）而**从未生效**，却每次打印「12/12 无冲突」⇒ 检查须带**负样本自证**（把本批 key 塞进假想既有集合，必须报冲突，否则 fail-closed 中止）；② 判据脚本的 `negative_check()` 只覆盖 J1/J2/J3/J4/J6/J8，**J5/J7/J9/J10 从未被自检** ⇒「自检通过」≠「其余判据可证伪」（J10 实测 9.333 > 阈值 5.0 完全可证伪，只是没被函数覆盖）⇒ 自合成多维负样本（实心黑块 + 贯穿暗框 + 纯白竖带 ⇒ 一次踩中多条判据）。",
]
NEW_FLOW = [
    "- **本地验收起服务：「端口被另一个进程占着」是假故障**（W974 实证·E-09）：`netstat` 显示 LISTENING + 大量 TIME_WAIT（说明确实连过），但 curl / Python urllib / 浏览器**全部失败或超时** ⇒ 根因 = 之前起的 `http.server` 没退干净、**两个进程抢同一端口**（Windows SO_REUSEADDR 允许）。⇒ 起步先 `Get-NetTCPConnection -LocalPort <port> -State Listen | % { Stop-Process -Id $_.OwningProcess -Force }` 清干净；起服务用 `Start-Process` 独立进程 + 重定向日志（**禁**在管道后接 `Select-Object -First N`，那会关掉 stdout 管道把服务打挂）。",
]

SECTION_COUNTS = [
    ("### CSS / 视觉渲染（10 条）", "### CSS / 视觉渲染（12 条）", NEW_CSS),
    ("### git / 提交 / 并发（18 条）", "### git / 提交 / 并发（19 条）", NEW_GIT),
    ("### 数据 / 内容可信度（6 条）", "### 数据 / 内容可信度（8 条）", NEW_DATA),
    ("### 流程 / 协作 / 取证（9 条）", "### 流程 / 协作 / 取证（10 条）", NEW_FLOW),
]

PROXY_NOTE = ("（W974 复发实证：W974 批的经验只沉淀进 Agent 私有 Memory 而未入仓 ⇒ 仓内其他 Agent 读不到，"
              "用户当场纠正「你不能只沉淀进你自己的 Memory 文件，本项目是多 Agent 协作的项目所以需要你同样沉淀进本项目内」"
              "⇒ 沉淀载体分工：规则类→AGENTS.md / 批次经验→HANDOVER「三」/ 深度篇→docs/10-方法论沉淀/ / 工具→scripts/。）")

METH_ROW = ("| 26 | 素材批处理与判据自证方法论 | [素材批处理与判据自证方法论.md](素材批处理与判据自证方法论.md) | "
            "成套素材的质量保证靠**构造**不靠拼凑——母版程序化复用 + 判据可证伪 + 人工关前置 + 落位页先验；"
            "且经验**必须入仓**（多 Agent 协作仓·私有记忆只有本会话读得到） |")

CLAIM_ROW = (
    "| W975 | 跨 Agent 经验沉淀入仓批（用户 2026-10-27 纠正「你不能只沉淀进你自己的 Memory 文件，本项目是多 Agent 协作的项目"
    "所以需要你同样沉淀进本项目内」·承接 W974 批）：① **问题定性**——W974 批的 9 条经验只写进 Agent 私有 Memory，"
    "仓内其他 Agent 读不到 ⇒ 正是坑表既有条目「共享机制必须写入仓库内文件（git tracked）」的**复发实证**（该条目本批补注复发）；"
    "② **入仓面**——坑表 `docs/agent/pitfalls.md` 6 条新条目（CSS/视觉渲染 +2「器物形状类别 > 数量计数」「落位页先验」·"
    "git/提交/并发 +1「写既有文件须临时文件 + 原子替换」·数据/内容可信度 +2「bbox 顶 ≠ 主体顶」「校验/自检代码必须自证」·"
    "流程/协作/取证 +1「端口占用是假故障」）+ 深度篇《素材批处理与判据自证方法论.md》（10-方法论沉淀 编号 26）+ "
    "AGENTS §4.3 主题视图/计数链 + HANDOVER 两处指针；③ **计数链同步**——坑表 57 → **63 条**、"
    "AGENTS §4.3 与 HANDOVER 的条数声明同批订正（门禁 N4 核对「AGENTS 声明 == pitfalls 实数」）| "
    "—（待回填） | —（待回填） | 在途（认领·未收官） | 主会话 2026-10-27（跨 Agent 经验沉淀入仓批） | "
    "`docs/agent/pitfalls.md` · `AGENTS.md` · `HANDOVER.md` · `docs/10-方法论沉淀/README.md` · "
    "`docs/10-方法论沉淀/素材批处理与判据自证方法论.md` · `docs/00-导读/W批次编号对账表.md`（本行） |"
)


def read(rel):
    raw = io.open(os.path.join(REPO, rel.replace("/", os.sep)), "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def write_atomic(rel, text, nl):
    p = os.path.join(REPO, rel.replace("/", os.sep))
    tmp = p + ".tmp"
    with io.open(tmp, "wb") as fh:
        fh.write(text.replace("\n", nl).encode("utf-8"))
    os.replace(tmp, p)


def git_show(rel):
    p = subprocess.run(["git", "show", "HEAD:" + rel], cwd=REPO, capture_output=True)
    return None if p.returncode != 0 else p.stdout.decode("utf-8").replace("\r\n", "\n")


def stage_exact(rel, text):
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO,
                          input=text.encode("utf-8"), capture_output=True)
    if blob.returncode != 0:
        raise SystemExit("FATAL hash-object 失败")
    b = blob.stdout.decode().strip()
    p = subprocess.run(["git", "update-index", "--cacheinfo", "100644," + b + "," + rel],
                       cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("FATAL update-index 失败: " + p.stderr.decode("utf-8", "replace")[:200])
    print("  精确暂存 %s（blob %s）" % (rel, b[:8]))


def t_pitfalls(text):
    """4 节插入新条目 + 节标题条数改写 + 共享机制条目补注"""
    lines = text.split("\n")
    for old_head, new_head, items in SECTION_COUNTS:
        if new_head.split("（")[0] + "（" in text and old_head not in text:
            raise SystemExit("FATAL 未找到节标题：%s" % old_head)
        # 定位节起止
        start = end = None
        for i, ln in enumerate(lines):
            if ln.startswith(old_head):
                start = i
            elif start is not None and (ln.startswith("### ") or ln.startswith("## ")):
                end = i
                break
        if start is None:
            raise SystemExit("FATAL 未找到节标题：%s" % old_head)
        if end is None:
            end = len(lines)
        # 在该节最后一条「- **」之后插入
        last = max([i for i in range(start, end) if lines[i].startswith("- **")] or [start])
        lines[last + 1:last + 1] = items
        for i in range(start, len(lines)):
            if lines[i] == old_head:
                lines[i] = new_head
                break
    text = "\n".join(lines)
    # 共享机制条目补注（W974 复发实证）
    anchor = "其他 Agent 在项目 session 读的是仓库版"
    idx = text.find(anchor)
    if idx < 0:
        raise SystemExit("FATAL 未找到共享机制条目")
    line_end = text.find("\n", idx)
    line = text[idx:line_end]
    if "W974 复发实证" not in line:
        text = text[:idx] + line + PROXY_NOTE + text[line_end:]
    return text


def t_agents(text):
    reps = [
        ("57 条坑位按六主题迁", "63 条坑位按六主题迁"),
        ("CSS/视觉渲染（10）· JS/CSP/运行时（6）· git/提交/并发（18）· 级联/CHANGELOG（8）· 数据/内容可信度（6）· 流程/协作/取证（9）",
         "CSS/视觉渲染（12）· JS/CSP/运行时（6）· git/提交/并发（19）· 级联/CHANGELOG（8）· 数据/内容可信度（8）· 流程/协作/取证（10）"),
        ("（现役 57 条·增量沿革见各条目自注与 CHANGELOG·W966 校）", "（现役 63 条·增量沿革见各条目自注与 CHANGELOG·W975 校）"),
        ("Windows 类=W509 BOM/W514 heredoc/W535 路径实参/W706 终端编码兜底。",
         "Windows 类=W509 BOM/W514 heredoc/W535 路径实参/W706 终端编码兜底；素材类=W974 bbox 顶≠主体顶（连通簇面积法）/出图器物形状类别>数量计数/落位页先验。"),
    ]
    for old, new in reps:
        if text.count(old) != 1:
            raise SystemExit("FATAL AGENTS 锚点命中 %d 次（期望 1）：%s" % (text.count(old), old[:50]))
        text = text.replace(old, new, 1)
    return text


def t_handover(text):
    n = text.count("（57 条·六主题")
    if n != 2:
        raise SystemExit("FATAL HANDOVER 指针命中 %d 次（期望 2）" % n)
    return text.replace("（57 条·六主题", "（63 条·六主题")


def t_meth(text):
    if "素材批处理与判据自证方法论.md" in text:
        return text
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("| 25 | 报告与复盘系列"):
            lines.insert(i + 1, METH_ROW)
            break
    else:
        raise SystemExit("FATAL 方法论目录索引未找到编号 25 行")
    return "\n".join(lines)


def t_ledger(text):
    if "| W975 |" in text:
        return text
    return text.rstrip("\n") + "\n" + CLAIM_ROW + "\n"


TARGETS = [(PITFALLS, t_pitfalls), (AGENTS, t_agents), (HANDOVER, t_handover),
           (METH, t_meth), (LEDGER, t_ledger)]


def main() -> int:
    dry = "--dry-run" in sys.argv
    for rel, fn in TARGETS:
        head = git_show(rel)
        if head is None:
            print("SKIP（HEAD 无此文件）：%s" % rel)
            continue
        try:
            new = fn(head)
        except SystemExit as e:
            print("FATAL %s：%s" % (rel, e))
            return 2
        if new == head:
            print("OK   无需改动：%s" % rel)
            continue
        if dry:
            print("DRY  %s：%d → %d 字符" % (rel, len(head), len(new)))
            continue
        cur, nl = read(rel)
        write_atomic(rel, new, nl)
        stage_exact(rel, new)
        print("OK   %s：已改写并精确暂存" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
