// v0.8 弹幕博物馆 EMBEDDED_DATA 数据源
// 数据来源：CHANGELOG.md v0.8 规划（2026-07-21）
// 用途：供 B2/B3/B4 HTML 页面复制内嵌到 <script> 中

const EMBEDDED_DATA = {
    // 页面 1 用
    celebrity_profiles: [
        { id: "li_zhuowu", name: "李卓吾", era: "明清", role: "明代思想家·头号解读UP主",
          quote: "读《西游记》者，不知作者宗旨，定作戏论。",
          modern_translation: "看不懂深层意思的人·只配当乐子人",
          suitable_age: "高中+",
          historical_detail: "明代思想家李贽（1527-1602），号卓吾。首位将《西游记》提升到哲学高度的批评家，提出'释厄'即心性修行解脱密码。" },
        { id: "jin_shengtan", name: "金圣叹", era: "清初", role: "清代评点家·毒舌一星差评",
          quote: "（对西游评价不及水浒）",
          modern_translation: "连差评区顶流都忍不住要评·说明西游火到绕不开",
          suitable_age: "初中+",
          historical_detail: "金圣叹（1608-1661），清初文学批评家。以评点水浒、西厢闻名，对西游评价不高但绕不开，侧面证明西游影响力。" },
        { id: "lu_xun", name: "鲁迅", era: "民国", role: "神魔小说鼻祖·神魔皆有人情",
          quote: "神魔皆有人情·精魅亦通世故",
          modern_translation: "妖怪也懂人情世故",
          suitable_age: "小学+",
          historical_detail: "鲁迅《中国小说史略》将《西游记》定位为'神魔小说'，剥离金丹大道宗教附会，完成祛魅手术。提出'神魔皆有人情'经典论断。" },
        { id: "hu_shi", name: "胡适", era: "民国", role: "高级童话派·反对过度解读",
          quote: "至多不过是一部很有趣味的滑稽小说……并没有什么微妙的意思",
          modern_translation: "就是个好玩的故事",
          suitable_age: "初中+",
          historical_detail: "胡适《西游记考证》花大力气考证作者与版本源流，怀疑作者非吴承恩，开启作者悬疑推理。但认为西游'并无微妙意思'，反对过度解读。" },
        { id: "chen_yinke", name: "陈寅恪", era: "民国", role: "考据派·追溯悟空形象源流",
          quote: "《西游记玄奘弟子故事之演变》",
          modern_translation: "孙悟空的形象是怎么一步步演变来的",
          suitable_age: "高中+",
          historical_detail: "陈寅恪（1890-1969），国学大师。撰《西游记玄奘弟子故事之演变》，考据悟空形象源自印度史诗《罗摩衍那》哈奴曼传说。" },
        { id: "zheng_zhenduo", name: "郑振铎", era: "民国", role: "考据派·梳理故事演化层叠",
          quote: "《西游记的演化》",
          modern_translation: "西游故事是一层一层叠上去的",
          suitable_age: "高中+",
          historical_detail: "郑振铎（1898-1958），文学史家。撰《西游记的演化》，梳理西游故事从民间传说到成书的层叠演化过程。" },
        { id: "mao_zedong", name: "毛泽东", era: "现代", role: "西游十级学者+野生代言人",
          quote: "唐僧百折不回·悟空反权威·八戒艰苦奋斗·白龙马任劳任怨",
          modern_translation: "项目经理天花板+整顿职场先驱+务实打工人+最强后勤",
          suitable_age: "高中+",
          historical_detail: "毛泽东熟读《西游记》，1945年重庆谈判时与民主党派人士聊一小时西游，大赞悟空'反权威'，表面说猴哥实际针砭蒋介石独裁——'用文化暗号谈政治'顶级案例。" },
        { id: "lin_yutang", name: "林语堂", era: "现代", role: "人性解剖师",
          quote: "悟空=叛逆少年·八戒=真实打工人·用荣格原型对读",
          modern_translation: "猴哥是青春期·猪哥是打工人",
          suitable_age: "大学+",
          historical_detail: "林语堂（1895-1976），作家、学者。用荣格心理学原型理论对读西游角色，将悟空视为叛逆少年原型，八戒视为真实打工人原型。" },
        { id: "qian_zhongshu", name: "钱钟书", era: "现代", role: "细节狂魔+纠错达人",
          quote: "一口钟是无袖长衣非铜钟",
          modern_translation: "读书仔细·连电视剧都骗不了你",
          suitable_age: "小学+",
          historical_detail: "钱钟书（1910-1998），学者、作家。1980年代致信央视杨洁导演指出'一口钟'应为无袖长外衣（明清俗语·类似斗篷）非庙堂之钟，导演收信后专门重拍。" },
        { id: "guo_moruo", name: "郭沫若", era: "现代", role: "分类学家+对联高手",
          quote: "迎风逐浪吹长叹·斩尽魔头万事休",
          modern_translation: "将西游归为神魔小说·还题了副对联",
          suitable_age: "全年龄",
          historical_detail: "郭沫若（1892-1978），诗人、史学家。将《西游记》归类为'神魔小说'，题联'迎风逐浪吹长叹·斩尽魔头万事休'。" }
    ],
    // content[] 统一结构 {name, quote, modern_translation, age_tag}
    age_groups: [
        { age_group: "幼儿/小学", title: "名人一句话", form: "表情包墙",
          content: [
              { name: "鲁迅", quote: "神魔皆有人情·精魅亦通世故", modern_translation: "妖怪也懂人情世故", age_tag: "幼儿/小学" },
              { name: "胡适", quote: "至多不过是一部很有趣味的滑稽小说", modern_translation: "就是个好玩的故事", age_tag: "幼儿/小学" },
              { name: "毛泽东", quote: "悟空反权威·八戒艰苦奋斗", modern_translation: "猴哥敢造反·猪哥肯吃苦", age_tag: "幼儿/小学" },
              { name: "钱钟书", quote: "一口钟是无袖长衣非铜钟", modern_translation: "读书仔细·连电视剧都骗不了你", age_tag: "幼儿/小学" }
          ] },
        { age_group: "初中", title: "观点PK赛", form: "辩题",
          content: [
              { name: "鲁迅+李卓吾", quote: "深度寓言·神魔皆有人情", modern_translation: "甲方：西游有深意", age_tag: "初中" },
              { name: "胡适", quote: "滑稽小说·并无微妙意思", modern_translation: "乙方：西游就是好玩", age_tag: "初中" },
              { name: "裁判（读者）", quote: "你站哪边？", modern_translation: "自己判断", age_tag: "初中" }
          ] },
        { age_group: "高中", title: "政治隐喻解码器", form: "修辞训练",
          content: [
              { name: "毛泽东·1945重庆谈判", quote: "大赞悟空反权威·表面说猴哥实际针砭蒋介石独裁", modern_translation: "用文化暗号谈政治的顶级案例", age_tag: "高中" },
              { name: "大闹天宫", quote: "类比反帝反封建", modern_translation: "借古讽今修辞训练素材", age_tag: "高中" }
          ] },
        { age_group: "大学", title: "学术谱系图", form: "谱系",
          content: [
              { name: "明代·李卓吾", quote: "释厄密码", modern_translation: "心性修行的密码本", age_tag: "大学" },
              { name: "清代·证道书", quote: "内丹修炼指南", modern_translation: "道家修行手册", age_tag: "大学" },
              { name: "民国·胡适+鲁迅", quote: "考证+定型", modern_translation: "作者悬疑+神魔小说定位", age_tag: "大学" },
              { name: "现代·毛泽东/林语堂/钱钟书", quote: "政治/人文/细读", modern_translation: "三路并行解读", age_tag: "大学" },
              { name: "当代·跨文化研究", quote: "比较文学视野", modern_translation: "走向世界文学", age_tag: "大学" }
          ] }
    ],
    mouthpiece_quotes: [
        { character: "金圣叹", role: "反内卷先锋",
          quote: "一部《西游》·不过教人安心做个'弼马温'·何苦非要闹天宫·争那斗战胜佛的虚名？",
          modern_translation: "别卷了·安稳打工不香吗" },
        { character: "猪八戒", role: "人间清醒代言人",
          quote: "取经路远·记得先吃饱·团队散伙是常态·保住高老庄的退路才是王道。",
          modern_translation: "保命要紧·退路第一" }
    ],
    // 页面 2 用
    triangle_dialogue: [
        { speaker: "李卓吾", position: "释厄密码", argument: "《西游记》表面写取经降妖，实则写心性修行。'释厄'二字是全书密码——解脱苦难即是修心。九九八十一难，每一难都是心魔的外化。",
          quote: "读《西游记》者，不知作者宗旨，定作戏论。", era: "明代" },
        { speaker: "胡适", position: "滑稽神话", argument: "《西游记》至多不过是一部很有趣味的滑稽小说，并没有什么微妙的意思。不必过度解读，好玩本身就是价值。",
          quote: "至多不过是一部很有趣味的滑稽小说……并没有什么微妙的意思", era: "民国" },
        { speaker: "毛泽东", position: "被压迫者反抗战歌", argument: "孙悟空大闹天宫是被压迫者反抗统治阶级的战歌。唐僧百折不回、悟空反权威、八戒艰苦奋斗——取经团队就是革命队伍的缩影。",
          quote: "唐僧百折不回·悟空反权威·八戒艰苦奋斗·白龙马任劳任怨", era: "现代" }
    ],
    roundtable_topics: [
        { topic: "如何评价猪八戒",
          participants: ["鲁迅", "林语堂", "毛泽东"],
          views: [
              { speaker: "鲁迅", view: "人情味——八戒身上的贪吃好色正是神魔皆有人情的最好注脚" },
              { speaker: "林语堂", view: "人欲原型——八戒是荣格心理学中的阴影原型，真实打工人的缩影" },
              { speaker: "毛泽东", view: "艰苦奋斗务实——八戒虽有缺点但始终走完取经路，是务实打工人的典范" }
          ] }
    ],
    // 页面 3 用（celebrity_id 用于与名人档案 join，celebrity_name 用于卡片正面直接显示）
    travel_identities: [
        { celebrity_id: "lu_xun", celebrity_name: "鲁迅", original_role: "神魔小说鼻祖",
          travel_role: "花果山史官", would_do: "写《妖界见闻录》揭露天庭黑幕" },
        { celebrity_id: "hu_shi", celebrity_name: "胡适", original_role: "高级童话派",
          travel_role: "取经团队顾问", would_do: "别解读了·先赶路！" },
        { celebrity_id: "mao_zedong", celebrity_name: "毛泽东", original_role: "西游十级学者",
          travel_role: "悟空的政委", would_do: "我们要建立自己的根据地！" },
        { celebrity_id: "qian_zhongshu", celebrity_name: "钱钟书", original_role: "细节狂魔",
          travel_role: "车迟国裁判", would_do: "纠正一口钟的常识错误" },
        { celebrity_id: "lin_yutang", celebrity_name: "林语堂", original_role: "人性解剖师",
          travel_role: "高老庄心理师", would_do: "给八戒做欲望管理咨询" },
        { celebrity_id: "chen_yinke", celebrity_name: "陈寅恪", original_role: "考据派",
          travel_role: "灵山档案馆员", would_do: "考证书真经的梵文原典" }
    ],
    scene_illustrations: [
        { scene_id: "luxun_underworld", character: "鲁迅", setting: "地府改革观察员",
          judgment: "我翻开这生死簿一查·歪歪斜斜的每页上都写着'天命注定'四个字·我横竖睡不着·仔细看了半夜·才从字缝里看出字来·满本都写着两个字是'吃人'！",
          svg_description: "鲁迅站在阎罗殿中横眉冷对生死簿的线稿" },
        { scene_id: "qian_postcard", character: "钱钟书", setting: "三界考据纠察官",
          judgment: "写信给吴承恩纠正妖王宴上宋代官窑瓷瓶形制在唐朝尚未出现·又给央视杨洁导演写信画图示意「一口钟」——两张幽默「纠错信」明信片。",
          svg_description: "两张幽默纠错信明信片" }
    ]
};

// 导出（供 Node.js 验证用，HTML 内嵌时此行可删除）
if (typeof module !== 'undefined' && module.exports) module.exports = EMBEDDED_DATA;
