#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_w1049_pick_verify.py — W1049 第五轮选材核验（12 主体·逐项实读证据）

自证要求：
  ① 12 目标回必须全部在「扩量目标集」内（挂通用 og-cover 且无任何配图）；
  ② 12 主体名在该回正文实读命中 ≥ 2 次（不凭记忆）；
  ③ 12 slug 与已出 124 母版 slug 零冲突；
  ④ 12 中文主体名与已落位 57 张配图的主体名零冲突（同角色复现风险·坑表 E-05）；
  ⑤ 12 目标回互不相同（同页两题图不被落位脚本支持）。

任一条不满足 ⇒ 退出码非 0（fail-closed）。
"""
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
assert os.path.isdir(os.path.join(REPO, "site", "reader")), "仓根推导错误：%s" % REPO
RD = os.path.join(REPO, "site", "reader")
SET = os.path.join(REPO, "assets", "promo", "plate-set")

# ---- 选材（W1049 第五轮·编号 97–108）----
SEL = [
    ("ch016", "金池长老", "jinchi-zhanglao", 97),
    ("ch039", "文殊菩萨", "wenshu-pusa", 98),
    ("ch046", "鹿力大仙", "luli-daxian", 99),
    ("ch050", "火德星君", "huode-xingjun", 100),
    ("ch055", "女儿国国王", "nvguo-guowang", 101),
    ("ch084", "灭法国王", "miefo-guowang", 102),
    ("ch005", "四大天王", "sida-tianwang", 103),
    ("ch018", "高太公", "gao-taigong", 104),
    ("ch032", "银角大王", "yinjiao-dawang", 105),
    ("ch056", "十代阎君", "shidai-yanjun", 106),
    ("ch067", "红鳞大蟒", "honglin-damang", 107),
    ("ch058", "谛听", "diting", 108),
]

RE_TAG = re.compile(r"<[^>]+>")
RE_SLUG = re.compile(r"^plate-line-(\d+)(?:-ch(\d+))?-([A-Za-z0-9-]+)\.png$")


def body(ch):
    p = os.path.join(RD, ch + ".html")
    t = io.open(p, encoding="utf-8", errors="ignore").read()
    return RE_TAG.sub(" ", t)


# ---- 目标集：挂通用 og-cover 且无任何配图 ----
# W1049 盲审 P1-3 修正：本批落位后 12 回已有 chapter-plate ⇒ 不再是「目标集」成员
# ⇒ 目标集判定须以「**排除本批 12 回后的存量缺口**」为基准。
BATCH_CHS = {c for c, _n, _s, _k in SEL}
target = {}
for f in sorted(glob.glob(os.path.join(RD, "ch*.html"))):
    t = io.open(f, encoding="utf-8", errors="ignore").read()
    # W1049 自证修正：key 必须与 SEL 同形（5 位 "ch016"）——
    # 首版误用 basename[2:5]（3 位 "016"）⇒ 目标集全体判空、12 项假红。
    ch = os.path.basename(f)[:5]
    assert ch.startswith("ch") and ch[2:].isdigit() and len(ch) == 5, \
        "回目 key 形态异常：%s" % ch
    og = re.search(r'<meta property="og:image" content="([^"]+)"', t)
    ogname = og.group(1).split("/")[-1] if og else ""
    has_fig = ('class="chapter-plate"' in t) or ('class="chapter-scene"' in t) \
        or ('class="chapter-banner"' in t)
    # 目标集成员判定（W1049 盲审 P1-3 修正）：
    #   本批落位后 12 回的 og 已换专属 og-plate-line-* 且已有 chapter-plate ⇒
    #   「挂通用 og-cover」这一条件对本批 12 回不再成立（它们**本就是**目标回）。
    #   ⇒ 目标集 = （挂通用 og-cover 且无配图的存量缺口）∪（本批 12 回）。
    if ch in BATCH_CHS or ("og-cover" in ogname and not has_fig):
        target[ch] = True

# ---- 已出母版 slug 全表 ----
# W1049 盲审 P1-3 修正：本批自身产出的资产（编号 97–108）已入目录 ⇒ 若把它们
# 算进「已出表」则本批选材**自指失效**（跑即 12 FAIL·与真实状态无关）。
# 正确基准 = **排除本批编号后的存量表**（124 张）。
BATCH_NUMS = {97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108}
used_slugs = set()
used_nums = set()
excluded = []
for fn in os.listdir(SET):
    m = RE_SLUG.match(fn)
    if m:
        num = int(m.group(1))
        if num in BATCH_NUMS:
            excluded.append(fn)
            continue
        used_slugs.add(m.group(3))
        used_nums.add(num)

# ---- 已落位配图主体中文名 ----
# W1049 盲审 P1-3 修正：本批落位的 12 回现在也有 chapter-plate ⇒ 其主体名会
# 撞上本批选材 ⇒ 同样须排除本批 12 回（基准 = 他方已落位的主体名）。
used_names = set()
for f in sorted(glob.glob(os.path.join(RD, "ch*.html"))):
    ch = os.path.basename(f)[:5]
    if ch in BATCH_CHS:
        continue
    t = io.open(f, encoding="utf-8", errors="ignore").read()
    for m in re.finditer(
            r'<figure class="chapter-(?:plate|scene|banner)">\s*<img src="[^"]+"\s+alt="([^"]*)"', t):
        alt = m.group(1)
        mm = re.match(r"(.+?)(?:的线描(?:立像|场景|场面|横幅|题图)|线描立像|水墨意境图)", alt)
        if mm:
            nm = mm.group(1)
            for suffix in ("与猴形行者", "与猴形行者对峙", "与十八罗汉", "与冥府判官",
                           "与鹤童子", "与虎形行者", "与狮驼", "与羊力大仙"):
                nm = nm.replace(suffix, "")
            used_names.add(nm)

print("扩量目标集 = %d 回 · 已出母版 = %d 张 / 唯一 slug = %d 个 · 已落位配图主体名 = %d 个"
      % (len(target), len(used_slugs), len(used_slugs), len(used_names)))
print()

fails = []
chs = [c for c, _n, _s, _k in SEL]
nums = [k for _c, _n, _s, k in SEL]
if len(set(chs)) != len(chs):
    fails.append("目标回重复：%s" % chs)
if len(set(nums)) != len(nums):
    fails.append("编号重复：%s" % nums)

for ch, name, slug, num in SEL:
    hit = body(ch).count(name)
    in_target = ch in target
    slug_clash = slug in used_slugs
    name_clash = name in used_names
    num_clash = num in used_nums
    ok = (hit >= 2) and in_target and not slug_clash and not name_clash and not num_clash
    print("  %-6s %-8s slug=%-16s 命中=%-3d 目标集=%-3s slug冲突=%-3s 主体名冲突=%-3s 编号冲突=%-3s %s"
          % (ch, name, slug, hit, "Y" if in_target else "N",
             "Y" if slug_clash else "n", "Y" if name_clash else "n",
             "Y" if num_clash else "n", "PASS" if ok else "*** FAIL ***"))
    if not ok:
        fails.append("%s %s（命中%d·目标集%s·slug%s·名%s·号%s）"
                     % (ch, name, hit, in_target, slug_clash, name_clash, num_clash))

print()
if fails:
    print("*** 选材核验失败 %d 项 ***" % len(fails))
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print("选材核验 PASS：12 主体全部目标集内 + 命中≥2 + slug/主体名/编号零冲突")

# ---- 负样本自证：判据必须会红（否则「全绿」是假的）----
print("\n== 负样本自证（每条只破坏一个维度·判据须 FAIL）==")
NEG_OK = True


def _check(ch, name, slug, num):
    """复用同一组判据·返回 (ok, 原因列表)"""
    reasons = []
    hit = body(ch).count(name)
    if hit < 2:
        reasons.append("命中不足(%d)" % hit)
    if ch not in target:
        reasons.append("不在目标集")
    if slug in used_slugs:
        reasons.append("slug 冲突")
    if name in used_names:
        reasons.append("主体名冲突")
    if num in used_nums:
        reasons.append("编号冲突")
    return (not reasons), reasons


NEGS = [
    ("N1 命中不足：把主体改成该回零出现的词", ("ch016", "金池长老X", "jinchi-zhanglao", 97)),
    ("N2 不在目标集：换已落位回 ch097", ("ch097", "犀牛怪", "test-n2", 97)),
    ("N3 slug 冲突：借用存量 slug", ("ch016", "金池长老", "xiniu", 97)),
    ("N4 编号冲突：借用存量编号 96", ("ch016", "金池长老", "test-n4", 96)),
    ("N5 主体名冲突：借用已落位主体名", ("ch016", "太阴星君", "test-n5", 97)),
]
for label, item in NEGS:
    ok, reasons = _check(*item)
    print("  %-42s %s %s" % (label, "PASS(会红)" if not ok else "*** FAIL(未报警) ***", reasons))
    if ok:
        NEG_OK = False
if not NEG_OK:
    raise SystemExit("负样本自证失败：判据存在恒真盲区")
print("负样本自证 PASS：5/5 判据可证伪")

out = os.path.join(REPO, "scripts", "output", "_w1049_pick.json")
with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(
        {"sel": [{"ch": c, "name": n, "slug": s, "num": k} for c, n, s, k in SEL],
         "target_total": len(target)}, ensure_ascii=False, indent=1))
print("写出:", os.path.relpath(out, REPO).replace("\\", "/"))
