r"""
karma_reincarnation.py — 《西游记》命运与轮回

用途：
    1. 生死簿轮回流转图：8 个生死簿被篡改/特殊处理的案例·暴露地府治理漏洞与业力流转
    2. 因果报应定律：10 个因果案例·揭示西游世界"善有善报·恶有恶报"的业力法则
    3. 六道轮回系统：天道/人道/阿修罗道/畜生道/饿鬼道/地狱道 六道众生分类
    4. 整体统计：跨概念汇总命运与轮回的运作规律

    输出 JSON：
    - life_death_registry.json：生死簿轮回流转图
    - karma_law.json：因果报应定律
    - samsara_wheel.json：六道轮回系统
    - karma_reincarnation_summary.json：整体统计

使用方式：
    py K_命运与轮回/karma_reincarnation.py --output output/data/
"""

import argparse
import json
from pathlib import Path

# 1. 生死簿轮回流转图
# 8 个生死簿被篡改/特殊处理的案例：character/original_fate/actual_fate/modifier/cause/chapter
LIFE_DEATH_REGISTRY = {
    "concept_name": "生死簿轮回流转图",
    "english_name": "Life-Death Registry Reincarnation Flow",
    "definition": "地府生死簿是轮回系统中枢·但被多次篡改或特殊处理·暴露业力可被干预的'漏洞'机制·每项改动都对应一段因缘",
    "core_principle": "原著中生死簿并非不可改·改簿者有三类：自身强销（悟空）/ 判官私改（崔判官）/ 阎王特许（刘全/寇洪）·体现'业力大于簿籍'的暗规则",
    "cases": [
        {
            "n": 1,
            "character": "孙悟空",
            "identity": "花果山美猴王·无编制草根",
            "original_fate": "魂字一千三百五十号·该寿三百四十二岁·善终",
            "actual_fate": "强销死籍·自猴属之名一并勾销·不入轮回·延寿至取经后成佛",
            "modifier": "孙悟空（自勾·强销死籍）",
            "cause": "求长生·学道归来不满寿数·勾销自己与花果山猴属",
            "chapter": "第 3 回",
            "impact_severity": 10,
            "data_volume_affected": "猴属 47000 条记录",
            "long_term_consequence": "猴群亦脱离地府管辖·生死簿永久被改·无补救",
        },
        {
            "n": 2,
            "character": "李世民",
            "identity": "大唐太宗皇帝",
            "original_fate": "贞观十三年寿尽·该死于游地府时",
            "actual_fate": "崔判官私改贞观十三年为贞观三十三年·延寿 20 年·还魂返阳",
            "modifier": "崔判官（地府判官·内部编制·私改）",
            "cause": "魏征与崔判官旧交·托梦求情·李世民游地府见善魂积德",
            "chapter": "第 10-11 回",
            "impact_severity": 7,
            "data_volume_affected": "1 条记录（帝王命数）",
            "long_term_consequence": "李世民还魂办水陆大会·开启取经项目·是西游故事总引子",
        },
        {
            "n": 3,
            "character": "寇洪（寇员外）",
            "identity": "铜台府地灵县寇员外·斋僧万人",
            "original_fate": "寿数未尽·被强盗踢死·魂归地府",
            "actual_fate": "阎王特许还魂·延寿 12 年·为大唐添寿一纪",
            "modifier": "地藏王菩萨/阎王（特许）+ 悟空地府说情",
            "cause": "斋僧万人积德·被强盗误杀·冤魂告状",
            "chapter": "第 97 回",
            "impact_severity": 5,
            "data_volume_affected": "1 条记录",
            "long_term_consequence": "寇员外还魂·说明地府对'善人'有特许通道·业力可争取",
        },
        {
            "n": 4,
            "character": "刘全",
            "identity": "均州民刘全·因妻李翠莲施金钗于僧被疑而自缢",
            "original_fate": "以死进瓜·本应死于进瓜任务",
            "actual_fate": "阎王查勘·夫妻皆有登仙之寿·均赐还魂·李翠莲借尸还魂附李世民妹李玉英",
            "modifier": "阎王（特许·查勘业力）",
            "cause": "进瓜有功·夫妻死皆冤·阎王特许双还",
            "chapter": "第 11 回",
            "impact_severity": 4,
            "data_volume_affected": "2 条记录（夫妻双还）",
            "long_term_consequence": "夫妇团圆·说明地府有'特许还魂'通道·非系统化·按业力个案处理",
        },
        {
            "n": 5,
            "character": "泾河龙王",
            "identity": "长安城外泾河龙君·水族",
            "original_fate": "本不当死·享天年",
            "actual_fate": "违旨改雨时辰点数·被魏征梦斩于剐龙台·龙头坠长安街",
            "modifier": "魏征（监斩·人曹官·人神二职）",
            "cause": "与袁守诚赌赛·违玉帝改雨时辰点数旨意·犯天条",
            "chapter": "第 9-10 回",
            "impact_severity": 8,
            "data_volume_affected": "1 条记录（但引发后续唐王游地府）",
            "long_term_consequence": "龙王鬼魂缠李世民·致其游地府·是西游项目第二大引子",
        },
        {
            "n": 6,
            "character": "乌鸡国王",
            "identity": "乌鸡国主·三年前井中遇害",
            "original_fate": "本不当死·被推入八宝琉璃井冤死三年",
            "actual_fate": "井底三年受苦·悟空取还魂丹+井水起死回生·还魂复位",
            "modifier": "孙悟空（取还魂丹）+ 八戒（驮尸出井）+ 文殊菩萨（默许青毛狮子代行）",
            "cause": "三年前乌鸡国王曾将文殊菩萨化身淹死三天·遭同业等流报",
            "chapter": "第 37-39 回",
            "impact_severity": 6,
            "data_volume_affected": "1 条记录（井底三年占位）",
            "long_term_consequence": "还魂后皈依佛法·揭示冤报需'同业等流'偿还",
        },
        {
            "n": 7,
            "character": "灵感大王（金鱼精）",
            "identity": "观音菩萨莲花池中金鱼·每日浮头听经成精",
            "original_fate": "本为菩萨宠物·不入生死簿·不轮六道",
            "actual_fate": "自行下界通天河·化作灵感大王·要童男童女祭祀·9 年吃人无数",
            "modifier": "金鱼精自行下界（观音未授意）·观音编外收回归莲池",
            "cause": "听经悟道·成精下界·借祭祀为名行夺舍食人之实",
            "chapter": "第 47-49 回",
            "impact_severity": 7,
            "data_volume_affected": "陈家庄童男童女 9 年 18 条·按生死簿应轮回却被夺舍食尽",
            "long_term_consequence": "观音编篮收走·未入轮回系统·揭示'仙佛眷属'有法外之权",
        },
        {
            "n": 8,
            "character": "猪八戒·沙僧（合并案例）",
            "identity": "天蓬元帅·卷帘大将（天庭武职正神）",
            "original_fate": "本为天庭正神·享天禄·不入轮回",
            "actual_fate": "猪八戒调戏嫦娥贬下凡错投猪胎·沙僧打碎琉璃盏贬下凡七日一次飞剑穿胸",
            "modifier": "玉帝（贬谪令）",
            "cause": "八戒蟠桃会醉酒调戏嫦娥·沙僧蟠桃会失手打碎琉璃盏",
            "chapter": "第 8 回 / 第 22 回",
            "impact_severity": 6,
            "data_volume_affected": "2 条记录（两位正神贬凡）",
            "long_term_consequence": "二人为取经团队主力·揭示贬谪是'赎罪+历练'机制·非纯惩罚",
        },
    ],
    "registry_stats": {
        "total_cases": 8,
        "tampering_types": {
            "自改（强销）": 1,
            "判官私改": 1,
            "阎王特许": 2,
            "天庭执行（斩/贬）": 2,
            "坐骑下界（夺舍/篡位）": 1,
            "仙佛收编": 1,
        },
        "modifying_party": ["孙悟空", "崔判官", "阎王", "魏征", "文殊菩萨/青毛狮子", "金鱼精", "玉帝"],
        "common_pattern": "生死簿非不可改·改簿者必有'因缘'对应·业力大于簿籍",
        "governance_gap": "8 案中仅 1 案（泾河龙王）按簿执行·其余 7 案皆为'特例'·地府治理漏洞率 87.5%",
    },
    "registry_insights": [
        "生死簿在地府是'参考簿'·非'绝对簿'·业力因缘可优先于簿籍",
        "8 案中只有'泾河龙王'是按簿执行被斩·其余皆是'篡改/特例'·说明业力高于簿籍",
        "李世民改寿 20 年是西游故事总引子·无此改则无取经项目",
        "悟空强销死籍是首例'篡改'·为后续大闹天宫埋伏笔·是天庭治理崩盘起点",
        "寇洪/刘全还魂揭示地府有'善人特例通道'·非纯按簿执行",
        "金鱼精案例揭示'仙佛眷属'有法外之权·可绕过生死簿",
    ],
}


# 2. 因果报应定律
# 10 个因果案例：cause/effect/karma_type/rebirth_destination
KARMA_LAW = {
    "concept_name": "因果报应定律",
    "english_name": "Karma Law of Cause and Effect",
    "definition": "西游世界遵循'善有善报·恶有恶报·如是因如是果'的业力法则·因果类型可分为：违令受罚/冤报同业/善化/赎罪/轮回修行/色报/失误受罚/姻缘定数/劫数考验/归正 十类",
    "core_principle": "业力大于天命·玉帝旨意可被业力推翻（如泾河龙王被斩是业力所归）·业力大于簿籍（生死簿可改但业力不可逃）",
    "cases": [
        {
            "n": 1,
            "case_name": "泾河龙王抗旨被斩",
            "cause": "与袁守诚赌赛·违玉帝旨意·改雨时辰点数（'改时辰·减点数'）",
            "effect": "魏征梦斩于剐龙台·龙头坠长安街·鬼魂缠李世民致其游地府",
            "karma_type": "违令受罚（业力与天命冲突·业力优先）",
            "rebirth_destination": "龙族业报流转·入轮回·化为鬼魂暂留冥府",
            "chapter": "第 9-10 回",
            "karma_principle": "天命可改·业力不可逃·违令即受报",
        },
        {
            "n": 2,
            "case_name": "乌鸡国王 3 年井底",
            "cause": "三年前乌鸡国王将文殊菩萨化身（化僧）捆浸御水河中三天",
            "effect": "文殊菩萨坐骑青毛狮子推国王入八宝琉璃井·井底冤死三年",
            "karma_type": "同业等流（冤报·以彼之道还施彼身）",
            "rebirth_destination": "还魂复位·人道·皈依佛法",
            "chapter": "第 37-39 回",
            "karma_principle": "你浸我三天·我推你三年·冤报以同业等流偿还",
        },
        {
            "n": 3,
            "case_name": "红孩儿纵火被收",
            "cause": "三昧真火烧悟空·伤生无数·要吃唐僧肉",
            "effect": "观音用天罡刀化莲台收伏·收为善财童子·永不入轮回",
            "karma_type": "善化（恶业转善果·强制修行）",
            "rebirth_destination": "观音善财童子·菩萨眷属·不入六道轮回",
            "chapter": "第 41-42 回",
            "karma_principle": "恶业可由更高业力转化·收编即'恶业转善果'",
        },
        {
            "n": 4,
            "case_name": "悟空大闹被压 500 年",
            "cause": "大闹天宫·偷蟠桃盗仙丹搅乱蟠桃会·与天庭为敌",
            "effect": "如来五行山压 500 年·饥食铁丸渴饮铜汁",
            "karma_type": "惩罚赎罪（业力清偿）",
            "rebirth_destination": "皈依佛门·随唐僧取经·终封斗战胜佛",
            "chapter": "第 7 回 / 第 14 回",
            "karma_principle": "大恶需大赎·500 年清偿·赎后成正果",
        },
        {
            "n": 5,
            "case_name": "唐僧 9 世修行",
            "cause": "金蝉子轻慢佛法·被如来贬下凡尘",
            "effect": "前 9 世为僧修行皆遭流沙河沙僧所食·头骨挂沙僧颈上·第 10 世玄奘完成取经",
            "karma_type": "轮回修行（多世赎罪·终成正果）",
            "rebirth_destination": "第 10 世成佛·封旃檀功德佛",
            "chapter": "第 8 回 / 第 22 回 / 第 100 回",
            "karma_principle": "前世因果今生偿·9 世遭难为第 10 世成佛铺垫",
        },
        {
            "n": 6,
            "case_name": "八戒调戏被贬",
            "cause": "蟠桃会醉酒调戏嫦娥·色心起·拱倒斗牛宫",
            "effect": "玉帝贬下凡·错投猪胎·外貌丑陋·福陵山云栈洞为妖",
            "karma_type": "色报（色心感畜生道果报）",
            "rebirth_destination": "畜生道（错投猪胎）→取经成净坛使者",
            "chapter": "第 8 回 / 第 19 回 / 第 100 回",
            "karma_principle": "色心感色报·错投畜生道·赎后成正果",
        },
        {
            "n": 7,
            "case_name": "沙僧打碎琉璃盏被贬",
            "cause": "蟠桃会失手打碎琉璃盏·失仪之罪",
            "effect": "玉帝贬下凡·七日一次飞剑穿胸·流沙河为妖·吃过往行人",
            "karma_type": "失误受罚（过失亦受重报）",
            "rebirth_destination": "畜生道（流沙河水妖）→取经成金身罗汉",
            "chapter": "第 22 回 / 第 100 回",
            "karma_principle": "天庭仪轨森严·失手亦重罚·赎后成正果",
        },
        {
            "n": 8,
            "case_name": "黄袍怪 13 年",
            "cause": "奎木狼与披香殿玉女私通·双双下界为妖",
            "effect": "奎木狼贬下界为黄袍怪·与百花羞公主 13 年姻缘·吃人作恶",
            "karma_type": "姻缘定数（私通下界·业力纠缠）",
            "rebirth_destination": "奎木狼归天庭星宿·百花羞归人道",
            "chapter": "第 28-31 回",
            "karma_principle": "私通业力感 13 年姻缘定数·业报尽后各归本位",
        },
        {
            "n": 9,
            "case_name": "女儿国未成婚",
            "cause": "唐僧与女儿国王业缘未尽·但劫数考验在前·不可成婚",
            "effect": "唐僧假意成亲骗通关文牒·蝎子精掳走唐僧·女儿国王独守空闺",
            "karma_type": "劫数考验（情劫·定业不可改）",
            "rebirth_destination": "唐僧继续取经·终成佛·女儿国王归人道",
            "chapter": "第 53-55 回",
            "karma_principle": "取经人有情劫·但定业优先·劫数不可避但不可成",
        },
        {
            "n": 10,
            "case_name": "牛魔王归顺",
            "cause": "罗刹女家庭+与悟空斗法失败·诸神围剿·四面楚歌",
            "effect": "牛魔王现原身大白牛·被哪吒降伏·归顺天庭灵山",
            "karma_type": "归正（恶业由强力转化·非自愿归正）",
            "rebirth_destination": "归顺天庭灵山·不入轮回·为正神眷属",
            "chapter": "第 60-61 回",
            "karma_principle": "恶业深重者由强力降伏归正·非自愿但终归善果",
        },
    ],
    "karma_stats": {
        "total_cases": 10,
        "karma_type_distribution": {
            "违令受罚": 1,
            "冤报同业": 1,
            "善化": 1,
            "惩罚赎罪": 1,
            "轮回修行": 1,
            "色报": 1,
            "失误受罚": 1,
            "姻缘定数": 1,
            "劫数考验": 1,
            "归正": 1,
        },
        "rebirth_destinations": {
            "成佛": 3,
            "成正果（使者/罗汉）": 2,
            "菩萨眷属": 1,
            "归天庭星宿": 2,
            "还魂人道": 1,
            "归顺正神眷属": 1,
        },
        "common_pattern": "10 案中 7 案最终'成正果/归正'·说明西游业力观是'可转化'的·非定死",
        "karma_balance": "恶业可由'赎罪·收编·强力归正'转化·但定业（如女儿国情劫）不可改",
    },
    "karma_insights": [
        "西游业力观是'可转化'的·非'定死'·10 案中 7 案最终成正果",
        "业力大于天命·泾河龙王虽违玉帝旨意·但被斩是业力所归",
        "业力大于簿籍·生死簿可改但业力不可逃·唐僧 9 世仍需偿业",
        "冤报以同业等流偿还·乌鸡国王浸僧 3 天·被推井 3 年·比例 1:365",
        "色报最重·八戒调戏嫦娥错投畜生道·是色心感色报",
        "失误亦受重罚·沙僧打碎琉璃盏贬凡·说明天庭仪轨森严",
        "劫数不可改但可避·女儿国未成婚是劫数考验·非定业",
    ],
}


# 3. 六道轮回系统
# 6 道：天道/人道/阿修罗道/畜生道/饿鬼道/地狱道
SAMSARA_WHEEL = {
    "concept_name": "六道轮回系统",
    "english_name": "Six Realms Samsara Wheel",
    "definition": "佛教六道轮回：天道/人道/阿修罗道/畜生道/饿鬼道/地狱道·众生随业力流转·西游世界以此为基础·但'仙佛眷属'与'取经成正果者'可跳出轮回",
    "core_principle": "六道中以天道/人道为善道·阿修罗道为半善道·畜生/饿鬼/地狱为三恶道·业力决定去向·修行可超脱",
    "realms": [
        {
            "n": 1,
            "name": "天道",
            "english_name": "Deva Realm",
            "population": "诸天神佛·天人无数",
            "entry_criteria": "上品十善业·或修行圆满·或正神归位",
            "exit_criteria": "福报尽时堕落·或天寿终了·随业流转",
            "duration": "一劫或多劫·极长久",
            "notable_cases": ["玉帝", "太上老君", "如来佛祖", "天庭仙官", "观音菩萨"],
            "characteristics": "天人福报大·但仍在轮回中·非究竟解脱",
            "in_pilgrim_team": 0,
        },
        {
            "n": 2,
            "name": "人道",
            "english_name": "Human Realm",
            "population": "凡界众生·四大部洲人类",
            "entry_criteria": "中品善业·持五戒·或天人福报尽转生",
            "exit_criteria": "业力流转·随业受生·或修行超脱",
            "duration": "一生数十百年·短促",
            "notable_cases": ["李世民", "唐僧 9 世", "陈光蕊", "殷温娇", "寇员外", "刘全"],
            "characteristics": "人道苦乐参半·最易修行·是成佛的必要条件",
            "in_pilgrim_team": 1,
        },
        {
            "n": 3,
            "name": "阿修罗道",
            "english_name": "Asura Realm",
            "population": "阿修罗众·有天福无天德",
            "entry_criteria": "善业中有嗔心·或修行有成但脾气未化",
            "exit_criteria": "嗔心转善可升天·嗔心重者堕恶道",
            "duration": "长寿·但福报有尽",
            "notable_cases": ["大鹏金翅雕（佛母孔雀菩萨眷属）", "部分妖怪源流"],
            "characteristics": "阿修罗好斗·常与天争·是有福无德之界",
            "in_pilgrim_team": 0,
        },
        {
            "n": 4,
            "name": "畜生道",
            "english_name": "Animal Realm",
            "population": "飞禽走兽水族昆虫·各路妖精",
            "entry_criteria": "下品恶业·愚痴·或色心感色报·或失误受重罚",
            "exit_criteria": "业报尽可转生·或被收编归正",
            "duration": "不定·随业力长短",
            "notable_cases": ["猪八戒错投猪胎", "沙僧流沙河水妖", "白龙马", "各路妖精", "泾河龙王业报流转"],
            "characteristics": "畜生道愚痴·常被驱使·是赎罪的好场所",
            "in_pilgrim_team": 3,
        },
        {
            "n": 5,
            "name": "饿鬼道",
            "english_name": "Preta Realm",
            "population": "饿鬼众·腹大咽细·常受饥渴",
            "entry_criteria": "中品恶业·贪悭不舍·或生前贪欲重",
            "exit_criteria": "业报尽可转生·或得超度",
            "duration": "长久·常受饥渴",
            "notable_cases": ["孟婆汤后忘前生·黄泉路上孤魂野鬼"],
            "characteristics": "饿鬼道贪悭·常求不得·是贪欲的果报",
            "in_pilgrim_team": 0,
        },
        {
            "n": 6,
            "name": "地狱道",
            "english_name": "Hell Realm",
            "population": "受苦众生·随罪业轻重受诸苦",
            "entry_criteria": "上品恶业·五逆十恶·或犯天条重罪",
            "exit_criteria": "业报尽可出·或地藏王菩萨超度",
            "duration": "长久·按劫数计·最久",
            "notable_cases": ["十八层地狱", "铜柱铁床", "刀山火海", "刀锯地狱"],
            "characteristics": "地狱道最苦·业报尽方可出·是恶业的终极果报",
            "in_pilgrim_team": 0,
        },
    ],
    "samsara_stats": {
        "total_realms": 6,
        "good_realms": ["天道", "人道"],
        "neutral_realm": ["阿修罗道"],
        "evil_realms": ["畜生道", "饿鬼道", "地狱道"],
        "pilgrim_team_distribution": {
            "天道": 0,
            "人道": 1,
            "阿修罗道": 0,
            "畜生道": 3,
            "饿鬼道": 0,
            "地狱道": 0,
            "超越轮回（成正果）": 5,
        },
        "escape_paths": ["取经成正果", "菩萨收编眷属", "皈依佛门", "强力归正"],
        "common_pattern": "取经团队 5 人中有 4 人原为天道正神贬下凡（畜生道/水妖）·最终全部超越轮回",
    },
    "samsara_insights": [
        "取经团队是'跳出轮回'的特例·5 人最终全部成佛/成正果·超越六道",
        "畜生道是赎罪的好场所·八戒/沙僧/白龙马皆由畜生道超脱",
        "人道是修行的最佳场所·唐僧 10 世皆为人道·方成佛",
        "天道非究竟·天人福报尽仍堕落·需修行超脱",
        "阿修罗道是'有福无德'之界·对应部分妖怪源流",
        "饿鬼道/地狱道是恶业终极果报·但业报尽可出·非永罚",
    ],
}


# 整体统计
SUMMARY = {
    "concept_name": "命运与轮回整体统计",
    "total_concepts": 4,
    "concept_list": ["生死簿轮回流转图", "因果报应定律", "六道轮回系统", "整体统计"],
    "total_data_points": (
        len(LIFE_DEATH_REGISTRY["cases"])
        + len(KARMA_LAW["cases"])
        + len(SAMSARA_WHEEL["realms"])
    ),
    "key_findings": [
        "8 个生死簿篡改案例·仅 1 案（泾河龙王）按簿执行·地府治理漏洞率 87.5%",
        "10 个因果案例·7 案最终成正果·说明业力观是'可转化'的",
        "6 道轮回中·取经团队 5 人最终全部超越轮回·成佛成正果",
        "业力大于天命·业力大于簿籍·是西游世界观的暗规则",
    ],
    "cross_concept_insight": "命运与轮回揭示西游是'业力可转化'的故事·非'命定不可改'·但转化需付出代价（赎罪·收编·归正·修行）",
    "key_numbers": {
        "life_death_cases": 8,
        "karma_cases": 10,
        "samsara_realms": 6,
        "wukong_age_at_death": 342,
        "li_shimin_extended_years": 20,
        "wukong_mountain_years": 500,
        "tang_monk_incarnations": 10,
        "wujing_flying_sword_cycle_days": 7,
        "baoxiang_kingdom_years": 13,
        "child_sacrifices_per_year_tongtian_river": 2,
    },
    "thematic_summary": {
        "命运观": "业力大于天命·业力大于簿籍·但业力可由修行/收编/归正转化",
        "轮回观": "六道轮回是基础架构·但'仙佛眷属'与'取经成正果者'可跳出轮回",
        "报应观": "善有善报·恶有恶报·如是因如是果·但恶业可由赎罪转化",
        "修行观": "人道是修行的最佳场所·取经是赎罪+历练+成正果的复合机制",
    },
}


def main():
    parser = argparse.ArgumentParser(description="生成《西游记》命运与轮回 JSON 数据")
    parser.add_argument(
        "--output",
        default="output/data/",
        help="输出目录",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "karma_life_death_registry.json": LIFE_DEATH_REGISTRY,
        "karma_law.json": KARMA_LAW,
        "samsara_wheel.json": SAMSARA_WHEEL,
        "karma_reincarnation_summary.json": SUMMARY,
    }

    for filename, data in outputs.items():
        filepath = output_dir / filename
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {filepath}")


if __name__ == "__main__":
    main()
