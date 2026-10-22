# 对拍模板（duipai）

> W778 固化（tmpe 工地层）· **W798 转正入库**（现役模板位·随仓版本化）· 方法论出处：第 41 篇复盘 §2 E-09 / docs/10-方法论沉淀/批次交付流水线.md §八。
> 场景：门禁/检查器类脚本的重构、拆分、替换——**先快照旧版、再落新版、最后对拍**。
> 本目录已入库（`docs/_templates/duipai/`·随仓版本化）；tmpe 下的同名副本为工地遗留，可删。方法论条文在流水线文档（durable）。

## 快速用法

```bash
# 旧版在位时（例：重构 check_x.js 之前）
python docs/_templates/duipai/duipai.py snapshot --tag x_old_selftest -- node scripts/check_x.js --self-test
python docs/_templates/duipai/duipai.py snapshot --tag x_old_gate3   -- node scripts/check_x.js --gate --pages a,b,c

# 新版落地后
python docs/_templates/duipai/duipai.py snapshot --tag x_new_selftest -- node scripts/check_x.js --self-test
python docs/_templates/duipai/duipai.py compare x_old_selftest x_new_selftest
python docs/_templates/duipai/duipai.py compare x_old_gate3 x_new_gate3 --sort   # 并发输出序不定时
```

## 归一化与判定

- 自动归一：ISO 时间戳 / `done in Ns` / `· N.Ns ·` / `ms=N` / 裸 `N.Ns`。
- **契约面零容忍**：退出码、消息文本、汇总末行、字段名；**抖动面归一**：计时、像素计数、并发序。
- 覆盖集合变化（可比页数/扫描页数）必须追根因：修复型变化（更多对象被纳入）显式记录后保留，不得为「逐字节一致」回滚修复本身。

## 快照目录

`snapshots/<tag>/{stdout.txt,stderr.txt,exit.txt,meta.json}`——快照可复用于回归基线；用后按 tmpe 纪律清理（不长期堆积）。
