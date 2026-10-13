# -*- coding: utf-8 -*-
"""W707 一次性：八份治理文件阅读契约头部（用户方案第十一条阶段 1·纯增量头部）。"""

import io

CONTRACTS = {
    "CHANGELOG.md": """> **📖 阅读契约（W707）**：查表型——判断「当前版本/最近批次」时只读**顶段 1 个版本段**；查历史段用 grep（`grep -A 30 "### vX"`）；完整通读非预期用法（历史细节在 docs/archive/CHANGELOG-ARCHIVE*.md·grep 单段查勿打开通读）。
""",
    "交接文档.md": """> **📖 阅读契约（W707）**：首段型+查表型——接手时只读「零、当前阻塞」+「一、当前进度」+ 文件末尾「最后更新」链；「三、方法论沉淀」「四、待办」按需查；历史批次细节在 CHANGELOG（grep 查）勿在本文件找。
""",
    "STRUCTURE.md": """> **📖 阅读契约（W707）**：索引型——找「东西在哪」时读顶层结构表+目标目录所在段；各板块下的建置沿革（v0.x W0xx 补齐…）是历史记录见 CHANGELOG，勿通读；计数与口径以磁盘实数与 [统计口径说明](docs/00-导读/统计口径说明.md) 为准。
""",
    "README.md": """> **📖 阅读契约（W707）**：分段型——普通读者通读「普通读者专区」；Agent/开发者**只读**「开发者/维护者专区」（技术栈/目录结构/测试/门禁）与「AI 生成说明」，读者导览段（emoji 列表）按需。
""",
    "AGENTS.md": None,  # 已单独 Edit
    "CLAUDE.md": """> **📖 阅读契约（W707）**：通读型——本文件 ≤60 行一屏读完即全部；正文唯一权威在指针目标。
""",
    "docs/archive/CHANGELOG-ARCHIVE.md": """> **📖 阅读契约（W707）**：禁读型——**永远不要通读**；查历史 W 号用 `grep -A 20 "### vX"` 单段取用。
""",
    "docs/archive/CHANGELOG-ARCHIVE-tier2.md": """> **📖 阅读契约（W707）**：禁读型——**永远不要通读**；查历史 W 号用 `grep -A 20 "### vX"` 单段取用。
""",
    "docs/archive/STRUCTURE-ARCHIVE.md": """> **📖 阅读契约（W707）**：禁读型——**永远不要通读**；查历史建置沿革用 grep 关键词单段取用。
""",
    "docs/archive/交接文档-ARCHIVE.md": """> **📖 阅读契约（W707）**：禁读型——**永远不要通读**；查历史批次进度用 grep 关键词单段取用。
""",
}

for path, contract in CONTRACTS.items():
    if contract is None:
        print("[SKIP] %s（已单独落）" % path)
        continue
    with io.open(path, encoding="utf-8", newline="") as f:
        s = f.read()
    if "阅读契约（W707）" in s:
        print("[SKIP] %s（已在位）" % path)
        continue
    lines = s.split("\n")
    # 插在 H1 与首个 blockquote 之间：找 H1 行后第一个空行位置
    i_h1 = next(i for i, l in enumerate(lines) if l.startswith("# "))
    j = i_h1 + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    lines.insert(j, "")
    lines.insert(j + 1, contract.rstrip("\n"))
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines))
    print("[OK] %s" % path)
print("DONE")
