"""_w612_remove_user_study.py — W612 用户研究整体删除手术（一次性）

范围：
1. 投稿版/匿名稿：删除 §5 用户研究段+图 6 引用、⑮Chen 注释项、⑯→⑮ 重排、§8 局限其一删除、页脚待办清理
2. 完整稿：删除 4.6 节（用户研究）、[15] Chen 条目、[16]→[15]、局限其一删除、行 224/357 尾句清理
3. 大纲：删除 4.4 用户研究小节与图 6 行
4. 图表清单：删除图 6 行与状态说明、标题 9→8 张
最终断言：三稿+清单中 用户研究/图 6/⑮Chen/协议链接 残留为 0。
"""
import io

SUB = "docs/S4-学术投稿/学术论文B轨-新中式数字雅集-装饰投稿版.md"
ANON = "docs/S4-学术投稿/学术论文B轨-新中式数字雅集-匿名稿.md"
FULL = "docs/S4-学术投稿/学术论文B轨-新中式数字雅集.md"
OUTLINE = "docs/S4-学术投稿/学术论文B轨-新中式数字雅集-大纲.md"
LIST = "docs/S4-学术投稿/图表_清单.md"


def load(p):
    return io.open(p, encoding="utf-8").read().split("\n")


def save(p, sl):
    io.open(p, "w", encoding="utf-8", newline="").write("\n".join(sl))


def find_sub(sl, needle, start=0):
    for i in range(start, len(sl)):
        if needle in sl[i]:
            return i
    raise AssertionError("未找到子串: " + needle)


def find(sl, prefix, start=0):
    for i in range(start, len(sl)):
        if sl[i].startswith(prefix):
            return i
    raise AssertionError("未找到前缀: " + prefix)


# ---------- 投稿版 / 匿名稿 ----------
for path in []:
    sl = load(path)
    # 1) 删除 §5 用户研究段（含前导空行）
    i = find(sl, "**用户研究**（独立验证")
    assert sl[i - 1].strip() == "", path + " 段前非空行"
    del sl[i - 1 : i + 1]
    # 2) §6 ⑯→⑮
    j = find(sl, "**对比度内建令牌**：WCAG 2.2 AA 阈值")
    assert "⑯" in sl[j]
    sl[j] = sl[j].replace("⑯", "⑮")
    # 3) §8 局限其一删除、其二其三前移
    j = find(sl, "局限亦须诚实交代：其一，用户研究尚未执行")
    sl[j] = sl[j].replace(
        "局限亦须诚实交代：其一，用户研究尚未执行，审美偏好仍是预期而非结果，论文主张的实证支撑有待样本数据补强；其二，86 页规模虽大",
        "局限亦须诚实交代：其一，86 页规模虽大",
    ).replace("；其三，暗色治理的经验数据", "；其二，暗色治理的经验数据")
    assert "用户研究" not in sl[j]
    # 4) 注释 ⑮ Chen 删除、⑯ W3C → ⑮
    j = find(sl, "⑮ Chen Z, Xie A, Liu Y")
    assert sl[j - 1].strip() == ""
    del sl[j - 1 : j + 1]
    j = find(sl, "⑯ W3C.")
    sl[j] = sl[j].replace("⑯", "⑮")
    # 5) 页脚待办清理
    j = find(sl, "> 待办：投稿前 48 小时")
    sl[j] = sl[j].replace("执行用户研究回填图 6 正式数据；", "")
    save(path, sl)
    t = "\n".join(sl)
    assert t.count("用户研究") == 0 and t.count("图 6") == 0 and t.count("Chen") == 0 and t.count("⑯") == 0, path
    print("OK", path.split("/")[-1][-16:])

# ---------- 完整稿 ----------
sl = load(FULL)
# 4) 案例章末尾句删除（指向已删节）
j = find(sl, "三个案例分别证明了系统的一个侧面")
assert "下一节给出小样本用户研究的设计与预期" in sl[j]
sl[j] = sl[j].replace("但\"可复制\"最终还需要人的检验：下一节给出小样本用户研究的设计与预期。", "")
# 1) 删除 4.6 节（### 六、用户研究 → 第五章 前）
i1 = find(sl, "### 六、用户研究")
i5 = find(sl, "## 第五章 可及性")
del sl[i1 : i5 - 2]  # 连同节尾空行；保留 ---
assert "用户研究" not in "\n".join(sl[i1 - 2 : i1 + 3])
# 2) [16] → [15]（正文锚点）
j = find_sub(sl, "（SC 1.4.3/1.4.11）[16]")
sl[j] = sl[j].replace("[16]", "[15]")
# 3) §8 局限其一删除
j = find(sl, "本文的局限同样需要诚实交代：其一，4.6 的用户研究尚未执行")
sl[j] = sl[j].replace(
    "其一，4.6 的用户研究尚未执行，审美偏好的实证支撑仍是预期而非结果；其二，部分参考文献",
    "其一，部分参考文献",
).replace("；其三，86 页的规模虽大", "；其二，86 页的规模虽大")
# 4.5) §8 路线图句去用户研究项
j = find_sub(sl, "这三条局限构成下一步工作的路线图：执行用户研究、补全文献、以一部新的古典名著验证迁移。")
sl[j] = sl[j].replace(
    "这三条局限构成下一步工作的路线图：执行用户研究、补全文献、以一部新的古典名著验证迁移。",
    "这三条局限构成下一步工作的路线图：补全文献、以一部新的古典名著验证迁移。")
# 5) 参考文献 [15] Chen 删除、[16] W3C → [15]
j = find(sl, "[15] CHEN Z, XIE A, LIU Y")
assert sl[j - 1].strip() == ""
del sl[j - 1 : j + 1]
j = find(sl, "[16] W3C.")
sl[j] = sl[j].replace("[16]", "[15]")
# 6) 页脚待办清理
j = find(sl, "> 待办：4.6 用户研究协议待执行")
sl[j] = sl[j].replace("4.6 用户研究协议待执行；", "").replace("图1/图2/图6 及印刷态截图", "印刷态截图")
save(FULL, sl)
t = "\n".join(sl)
assert t.count("用户研究") == 0 and t.count("[15] CHEN") == 0 and t.count("[16]") == 0 and t.count("图6") == 0, FULL
print("OK 完整稿")

# ---------- 大纲 ----------
sl = load(OUTLINE)
i1 = find(sl, "4.4 用户研究")
del sl[i1 : i1 + 5]  # 4.4 标题+3 条 bullet+尾随空行
j = find(sl, "| 图6 | 用户研究结果图")
del sl[j : j + 1]
save(OUTLINE, sl)
t = "\n".join(sl)
assert t.count("用户研究") == 0 and t.count("图6") == 0 and t.count("Chen") == 0, OUTLINE
print("OK 大纲")

# ---------- 图表清单 ----------
sl = load(LIST)
j = find(sl, "# 图表清单（B 轨论文 · 9 张）")
sl[j] = sl[j].replace("9 张", "8 张")
j = find(sl, "| 图 6 | 用户研究设计示意")
del sl[j : j + 1]
j = find(sl, "- **图 6 状态**")
del sl[j : j + 1]
save(LIST, sl)
t = "\n".join(sl)
assert t.count("图 6") == 0 and t.count("用户研究") == 0 and t.count("用户研究协议") == 0, LIST
print("OK 图表清单")
