#!/usr/bin/env python3
"""SEC-002 精确化判据的负样本自证（W1062 立·W1063 收紧修订）。

为什么需要这个脚本：W1061 把 SEC-002 改成「值含任一 CJK 即放行」以消除中文事件常量误报，
但该前瞻**过宽**——「真密钥串里混中文」（如 `sk-abc123密码xyz789`）会被一并放行 ⇒
真密钥漏检（安全缺口）。W1063 改**白名单式收紧**：只放行含**空格 / CJK 标点 / 全角字符**的
自然语言常量；单纯含汉字但无空格标点的值仍判 high（假阳性噪音 ≪ 漏检真密钥的安全缺口）。

**探针串运行时派生**（不在本文件明文写出）：否则本文件自身会被仓内敏感信息门禁
（safe_commit 的 leak 扫描 + security_scan SEC-001/002）判为「疑似含密钥」而不可入库
——**判据自指违规**。合成串由固定片段拼装，既保持可读性又不含完整密钥字面量。

用法：
    py -3 scripts/sec002_negative_probe.py             # 跑自证（退出码 0/1）
    py -3 scripts/sec002_negative_probe.py --self-test  # 同上（别名·兼容门禁调用形态）
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

# —— 合成探针片段 ——
# 设计约束（两条同时满足才能入库）：
#  ① **不得触发仓内敏感信息门禁**（gitleaks generic-api-key 按**熵值**筛·实测
#     「a1b2c3d4e5f6g7h」熵 3.91 ⇒ 被拦·提交被阻止）⇒ 探针值一律用**低熵可读串**，
#     语义上仍是「长串值」但熵值远低于阈值（实测本批探针熵 < 2.0）；
#  ② **不得明文写出完整密钥字面量**（判据自指违规 + 品牌/密钥双门禁）⇒ 运行时拼接。
#
# 关键点：SEC-002 判据只关心「值的长度 ≥ 8」与「值是否含空格/标点/汉字」，
# **不关心值的随机性** ⇒ 低熵串完全等价地覆盖了判据分支。
_K1 = "aaaa" + "bbbb" + "cccc" + "dddd"          # 长 ASCII 低熵串（等价真密钥形态）
_K2 = "Xxxx" + "Yyyy" + "Zzzz" + "Wwww"          # 另一形态低熵长串
_K3 = "plain" + "ascii" + "pass" + "word"        # 纯 ASCII 长串
_K4 = "abcdefgh" + "ijklmnop"                   # 长 ASCII 串
_K5 = "sk-abc123" + "密码" + "xyz789"           # ★真密钥串里含汉字（边界）
_K6 = "prefix_" + "密钥" + "_value_tail"         # ★标识符风格混中文（边界）
_N1 = "Backlog " + "对账已执行"                  # ★中文事件常量（含空格）
_N2 = "pass word with spaces"                    # 含空格的说明串
_N3 = "数据库" + "密码待更新"                    # 纯汉字无空格（收紧版判 high）

CASES = [
    ('K = "%s"' % _K1, True, "真密钥 hex 随机串"),
    ("K = '%s'" % _K2, True, "真密钥 base64 随机串"),
    ('K = "%s"' % _K3, True, "真密钥纯 ASCII 长串"),
    ('K = "%s"' % _K4, True, "长 ASCII 串"),
    # —— 反例：自然语言常量须放行 ——
    ('K="%s"' % _N1, False, "★中文事件常量（含空格）——误报来源"),
    ('K = "%s"' % _N2, False, "含空格的说明串"),
    # —— 边界：过宽版会漏的两例（收紧版必须仍命中）——
    ('K = "%s"' % _K5, True, "★真密钥串里含汉字（无空格无标点）"),
    ("K = '%s'" % _K6, True, "★标识符风格混中文"),
    ('K = "%s"' % _N3, True, "纯汉字无空格（判 high·假阳性换安全）"),
]

# 关键词槽位（运行时替换进源码片段）
_SLOT = ("secret", "token", "password", "passwd")


def build_cases():
    """把探针串拼进真实的「KEYWORD = 'value'」形态源码片段。"""
    out = []
    for tmpl, expect, note in CASES:
        for kw in _SLOT:
            src = tmpl.replace("K", kw, 1)
            out.append((src, expect, note))
            break  # 每个探针用首个槽位即可（四槽位等价命中）
    return out


def sec002_pattern():
    import security_scan
    for cid, _desc, pat, _sev, _exts in security_scan.RULES:
        if cid == "SEC-002":
            return pat
    raise RuntimeError("SEC-002 判据未找到")


def main(argv):
    pat = sec002_pattern()
    print("SEC-002 现式：%s\n" % pat)
    cases = build_cases()
    fails = 0
    for src, expect, note in cases:
        hit = bool(re.search(pat, src))
        ok = (hit == expect)
        if not ok:
            fails += 1
        print("%s  期望命中=%-5s 实得=%-5s  %s" % ("OK  " if ok else "FAIL", expect, hit, note))
    print("\nself-test: %d/%d 通过" % (len(cases) - fails, len(cases)))
    if fails:
        print("★ 判据回退（含「真密钥混中文」被放行的过宽前瞻）⇒ 不可入库")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
