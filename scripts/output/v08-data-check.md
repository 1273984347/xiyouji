# v0.8 EMBEDDED_DATA 数据完整性验证

验证时间：2026-07-22
验证文件：scripts/output/v08-embedded-data.js

| 验证项 | 结果 | 证据 |
|--------|------|------|
| 名人档案字段完整性 | PASS | 10 条 celebrity_profiles，每条 8 字段齐全（id/name/era/role/quote/modern_translation/suitable_age/historical_detail） |
| 年龄段交叉一致 | PASS | 4 组 age_groups，suitable_age 与名人档案一致 |
| 穿越身份引用 | PASS | 6 个 celebrity_id 全在 celebrity_profiles 中存在（lu_xun/hu_shi/mao_zedong/qian_zhongshu/lin_yutang/chen_yinke） |
| 对话参与者 | PASS | triangle_dialogue 3 speaker + roundtable 3 speaker 全在名人档案中（李卓吾/胡适/毛泽东/鲁迅/林语堂） |
| 场景角色 | PASS | 2 个 character 全在名人档案中（鲁迅/钱钟书） |
