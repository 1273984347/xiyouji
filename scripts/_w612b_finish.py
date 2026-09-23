"""_w612b_finish.py — W612 用户研究删除收尾（投稿版/匿名稿/大纲/清单）

完整稿已在先前轮次完成；本脚本处理因 CRLF 空行断言未落盘的剩余四文件。
"""
import io

SUB = "docs/S4-学术投稿/装饰投稿/学术论文B轨-新中式数字雅集-装饰投稿版.md"
ANON = "docs/S4-学术投稿/装饰投稿/学术论文B轨-新中式数字雅集-匿名稿.md"
OUTLINE = "docs/S4-学术投稿/装饰投稿/学术论文B轨-新中式数字雅集-大纲.md"
LIST = "docs/S4-学术投稿/装饰投稿/图表_清单.md"


def load(p):
    return io.open(p, encoding="utf-8").read().split("\n")


def save(p, sl):
    io.open(p, "w", encoding="utf-8", newline="").write("\n".join(sl))


def find(sl, prefix, start=0):
    for i in range(start, len(sl)):
        if prefix in sl[i]:
            return i
    raise AssertionError("未找到前缀: " + prefix)


# ---------- 投稿版 / 匿名稿 ----------
pairs_body = [
    ("**用户研究**（独立验证·设计已定稿，尚未执行）：", None),  # 整行删除
    ("（正常文本 4.5:1、大文本/非文本 UI 3:1）⑯在令牌定义阶段即满足",
     "（正常文本 4.5:1、大文本/非文本 UI 3:1）⑮在令牌定义阶段即满足"),
    ("局限亦须诚实交代：其一，用户研究尚未执行，审美偏好仍是预期而非结果，论文主张的实证支撑有待样本数据补强；其二，86 页规模虽大",
     "局限亦须诚实交代：其一，86 页规模虽大"),
    ("；其三，暗色治理的经验数据来自单一项目", "；其二，暗色治理的经验数据来自单一项目"),
    ("⑯ W3C.", "⑮ W3C."),
    ("执行用户研究回填图 6 正式数据；", ""),
]
for path in [SUB, ANON]:
    sl = load(path)
    for old, new in pairs_body:
        try:
            j = find(sl, old)
        except AssertionError:
            continue  # 幂等：上一轮已应用
        if new is None:
            assert sl[j - 1].strip() == "", (path, j)
            del sl[j - 1 : j + 1]
        else:
            sl[j] = sl[j].replace(old, new)
    j = find(sl, "⑮ Chen Z, Xie A, Liu Y")
    del sl[j : j + 1]
    save(path, sl)
    t = "\n".join(sl)
    assert t.count("用户研究") == 0 and t.count("图 6") == 0 and t.count("Chen") == 0 and t.count("⑯") == 0, path
    print("OK", path.split("/")[-1][-16:])

# ---------- 大纲 ----------
sl = load(OUTLINE)
j = find(sl, "4.4 用户研究")
del sl[j : j + 5]  # 标题 + 3 bullet + 尾随空行
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
assert t.count("图 6") == 0 and t.count("用户研究协议") == 0 and t.count("结果示意") == 0, LIST
resid = [(i + 1, l.strip()[:80]) for i, l in enumerate(sl) if "用户研究" in l]
print("OK 图表清单；用户研究残留行:", resid if resid else 0)
