# audit/archive/ — 历史一次性验证脚本归档

本目录保存与特定 W### 工作项绑定的一次性验证脚本，已完成历史使命，保留以备追溯。

| 脚本 | 关联工作项 | 用途 |
|:---|:---|:---|
| `w051_kpi_verify.py` | W051 | dashboard 45 KPI 卡片一致性验证 |
| `w051_r3_verify.py` | W051 | DRL R3 收敛验证 |
| `w053_fix_placeholders.py` | W053 | 占位符批量修复 |
| `w053_verify_links.py` | W053 | 链接验证（已被根级 `lint_links.py` 取代） |
| `w100_drl_r1b_spotcheck.py` | W100 | DRL R1b spot-check |
| `w100_first_appear_check.py` | W100 | 人物首现回目检查 |
| `w100_preflight_check.py` | W100 | Preflight 三轨验证 |
| `w102_check_ch7.py` | W102 | 第 7 章数据校验 |
| `w102_check_sanzang.py` | W102 | "三藏共"模式检查 |

> **规则**：新的一次性验证脚本应放在 `audit/` 根目录并在文件名中带 W### 前缀；
> 工作项收尾后归档至 `audit/archive/`。根目录 `audit/` 仅保留当前活跃工作项的脚本。
