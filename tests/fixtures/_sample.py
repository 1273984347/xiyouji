"""_sample.py — agent-guardrails 自测用「故意违规」样板。

只用于验证 lint 档位确实能报出四类结构问题，不参与项目构建；
文件名 _ 前缀命中 ruff exclude（**/_*.py），日常扫描不会碰到它。

预期违规（实测见 ../README.md「真实输出证据」）：
  1. deep_six_levels   嵌套 6 层            → ruff PLR1702（阈值 >4）
  2. nested_comprehension 双层列表推导式    → scripts/check_nested_comprehension.py
  3. once_helper      只被调用 1 处         → scripts/once_call.py
  4. long_elif_chain  16 个 elif 分支       → ruff C90（阈值 >15）
"""


def deep_six_levels(matrix):
    total = 0
    for row in matrix:               # 1
        for cell in row:             # 2
            if cell > 0:             # 3
                for digit in str(cell):  # 4
                    if digit != "0":     # 5
                        while total < 3:  # 6
                            total += 1
    return total


def nested_comprehension(rows):
    # 双层列表推导式：外层推导里再套一个推导。
    return [[value * 2 for value in row if value] for row in rows]


def once_helper(value):
    # 故意只在一个地方调用，模拟「一次性逻辑被抽成辅助函数」。
    return value * 3


def long_elif_chain(code):
    # 16 个 elif 分支：C90 复杂度 = 17 > 阈值 15。
    if code == 0:
        return "zero"
    elif code == 1:
        return "one"
    elif code == 2:
        return "two"
    elif code == 3:
        return "three"
    elif code == 4:
        return "four"
    elif code == 5:
        return "five"
    elif code == 6:
        return "six"
    elif code == 7:
        return "seven"
    elif code == 8:
        return "eight"
    elif code == 9:
        return "nine"
    elif code == 10:
        return "ten"
    elif code == 11:
        return "eleven"
    elif code == 12:
        return "twelve"
    elif code == 13:
        return "thirteen"
    elif code == 14:
        return "fourteen"
    elif code == 15:
        return "fifteen"
    return "unknown"


def run():
    print(once_helper(2), deep_six_levels([[1, 2]]), nested_comprehension([["1"]]), long_elif_chain(3))


if __name__ == "__main__":
    run()
