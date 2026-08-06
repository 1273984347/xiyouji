
    // ===== 嵌入式 fallback 数据（fetch 失败时使用）=====
    const EMBEDDED = {
        project_review: {
            project_name: "大唐文化传播集团·西天取经战略项目",
            project_code: "TANG-XIYOU-14Y",
            duration_years: 14,
            sponsor: "唐太宗李世民",
            pm: "唐三藏（项目经理）",
            tech_lead: "孙悟空（技术负责人）",
            team_size: 5,
            deliverables: "大乘真经 5048 卷",
            milestones: [
                { phase: "立项", year: "贞观13年", event: "水陆大会·唐僧受命", kpi: "项目立项" },
                { phase: "组建团队", year: "贞观13-14年", event: "收悟空·白龙·八戒·沙僧", kpi: "团队 5 人齐" },
                { phase: "执行", year: "贞观14-26年", event: "九九八十一难", kpi: "难度 81/81" },
                { phase: "交付", year: "贞观27年", event: "灵山取经·凌云渡脱胎", kpi: "真经 5048 卷" },
                { phase: "结项", year: "贞观27年", event: "径回东土·五圣成真", kpi: "5 人晋升佛位" }
            ],
            final_review: { rating: "A+", comment: "项目圆满交付·5 人晋升·真经入长安·功德圆满" }
        },
        team_effectiveness: {
            phases: [
                { phase: "Forming·初建期", chapter_range: "12-22", effectiveness: 5, feature: "组建团队·各成员带病入伙·磨合中" },
                { phase: "Storming·风暴期", chapter_range: "23-58", effectiveness: 4, feature: "三打白骨精·悟空被逐·真假美猴王·团队信任危机" },
                { phase: "Norming·规范期", chapter_range: "59-90", effectiveness: 8, feature: "火焰山·小雷音·狮驼岭·团队协作成熟化" },
                { phase: "Performing·表现期", chapter_range: "91-100", effectiveness: 10, feature: "青龙山·天竺·凌云渡·五圣成真" }
            ],
            spike_points: [
                { chapter: 30, event: "悟空回救·唐僧化虎", spike: 2, note: "Storming 后的首次回归·信任重建" },
                { chapter: 58, event: "真假美猴王辨明", spike: 3, note: "Storming 结束·进入 Norming" },
                { chapter: 77, event: "狮驼岭·如来亲降", spike: 5, note: "Performing 入门·团队默契顶峰" },
                { chapter: 98, event: "凌云渡·脱胎换骨", spike: 10, note: "Performing 顶峰·五圣成真" }
            ]
        },
        trip_report: [
            { n: 5, hardship: "出城逢虎", location: "双叉岭", alert_level: "黄", weather: "山林·虎啸", remark: "建议发放山林补贴", delay_days: 1 },
            { n: 11, hardship: "失却袈裟", location: "观音禅院·黑风山", alert_level: "橙", weather: "夜火·妖气", remark: "设备（袈裟）遗失，建议购买保险", delay_days: 3 },
            { n: 17, hardship: "黑熊精阻路", location: "黑风洞", alert_level: "橙", weather: "黑气弥漫", remark: "需观音姐姐亲临协调", delay_days: 2 },
            { n: 27, hardship: "三打白骨精", location: "白虎岭", alert_level: "红", weather: "白骨阴气", remark: "团队内讧·执行器被驱逐", delay_days: 7 },
            { n: 41, hardship: "红孩儿·三昧真火", location: "号山火云洞", alert_level: "红·极端高温", weather: "极端高温红色预警", remark: "建议发放高温补贴", delay_days: 5 },
            { n: 47, hardship: "通天河·金鱼精", location: "通天河", alert_level: "红·洪水", weather: "冰面行走·后遇洪水", remark: "遭遇不可抗力（洪水），行程延误", delay_days: 4 },
            { n: 50, hardship: "金兜洞·金刚琢", location: "金兜山", alert_level: "红", weather: "金光万道", remark: "诸神兵器被套·需老君亲降", delay_days: 6 },
            { n: 59, hardship: "三借芭蕉扇", location: "火焰山·芭蕉洞", alert_level: "红·极端高温", weather: "八百里火焰山", remark: "极端高温·建议发放高温补贴+防暑用品", delay_days: 8 },
            { n: 65, hardship: "小雷音寺·黄眉怪", location: "小西天", alert_level: "红·伪佛", weather: "伪佛光", remark: "诸神皆入人种袋·需弥勒亲降", delay_days: 7 },
            { n: 74, hardship: "狮驼岭三魔王", location: "狮驼岭·狮驼国", alert_level: "SSS·全城紧急", weather: "骷髅若岭", remark: "全城进入紧急状态·警报级别 SSS 级·如来亲降", delay_days: 12 },
            { n: 82, hardship: "无底洞·老鼠精", location: "陷空山", alert_level: "红", weather: "黑气漫山", remark: "李天王义女·需父女牌位协调", delay_days: 4 },
            { n: 91, hardship: "青龙山·三犀牛", location: "青龙山", alert_level: "橙", weather: "寒光凛凛", remark: "偷香油 5 万斤·需四星收服", delay_days: 5 }
        ],
        wukong_resume: {
            basic_info: {
                name: "孙悟空", alias: "齐天大圣·斗战胜佛",
                birthplace: "东胜神洲·花果山",
                education: "灵台方寸山·斜月三星洞（菩提祖师学院）",
                major: "地煞七十二变·筋斗云",
                phone: "金箍棒呼叫（一万三千五百斤直拨）"
            },
            work_experience: [
                { company: "天庭集团", position: "弼马温（御马监正堂）", duration: "半月", achievements: "管理天马千匹·建立标准化饲养流程", reason_for_leave: "岗位与个人能力不匹配·寻求更大挑战" },
                { company: "天庭集团·齐天大圣府", position: "齐天大圣（无具体职责·带俸留任）", duration: "数月", achievements: "策划并执行了一场针对大型跨国集团（天庭）的颠覆性压力测试，成功推动其安保系统与组织架构全面升级", reason_for_leave: "压力测试后·被五行山项目'冻结'500年" },
                { company: "大唐文化传播集团·西天取经项目", position: "技术负责人（大师兄）", duration: "14年", achievements: "主导解决九九八十一难中的 60+ 项技术难题·搬救兵 30+ 次·保项目交付", reason_for_leave: "项目结项·晋升斗战胜佛" }
            ],
            skills: [
                { skill: "地煞七十二变", level: "专家", note: "可避三灾·变化万千" },
                { skill: "筋斗云", level: "专家", note: "一筋斗十万八千里·跨洲位移" },
                { skill: "火眼金睛", level: "高级", note: "识破妖物本相·但怕烟熏" },
                { skill: "搬救兵", level: "大师", note: "天庭/灵山/南海·全域资源调度" },
                { skill: "金箍棒", level: "专家", note: "一万三千五百斤·大小如意" }
            ],
            stress_interview: [
                { question: "你曾因与直属领导（唐僧）管理理念不合而离职（三打白骨精后回花果山），请问你如何保证在新岗位能处理好上下级关系？", wukong_answer: "那次离职是必要的反思期。后来我意识到，领导的'不杀'基准值与我的'除恶'执行器之间存在执行边界问题。经过真假美猴王事件，我学会了在执行前先与领导'对齐'目标，避免误判。同时紧箍咒作为外部执行控制机制，也帮助我抑制冲动。", emoji_note: "戴紧箍咒的苦涩微笑" },
                { question: "你在天庭的'压力测试'（大闹天宫）造成严重后果，如何解释这次'试错'？", wukong_answer: "那次是个人价值与体系认可的错位需求。我当时未意识到天庭的科层制无法容纳'自封齐天大圣'的非编制身份。这次试错让我认识到，体系内的价值实现需要通过合规路径，而非暴力对抗。", emoji_note: "挠头尴尬笑" },
                { question: "你经常'搬救兵'，如何评估你的独立解决问题能力？", wukong_answer: "搬救兵是资源调度的成熟表现。前期我倾向'先打再说'，后期学会精确计算搬救兵的 ROI：解决问题效率×人情消耗/耗时×威望折损。能独立解决的（如白骨精·车池国三仙）我独立解决；有背景妖怪（如红孩儿·金兜洞）必须搬救兵，这是组织行为学的合理选择。", emoji_note: "托腮认真分析" }
            ]
        },
        internet_buzzwords: [
            { buzzword: "对齐", chinese_meaning: "对准·同步", xiyou_usage: "唐僧召集徒弟们开会：'我们今日须得在山头对齐一下，这山有妖气。'", category: "会议用语" },
            { buzzword: "赋能", chinese_meaning: "赋予能力", xiyou_usage: "观音给悟空三根救命毫毛：'我特来为你赋能。'", category: "资源支持" },
            { buzzword: "底层逻辑", chinese_meaning: "根本原理", xiyou_usage: "如来对悟空解释：'你大闹天宫的底层逻辑，其实是对个人价值与体系认可的错位需求。'", category: "方法论" },
            { buzzword: "颗粒度", chinese_meaning: "细致程度", xiyou_usage: "悟空汇报：'狮驼岭的妖怪颗粒度太粗，三个魔头抓了全城百姓。'", category: "汇报用语" },
            { buzzword: "抓手", chinese_meaning: "着力点", xiyou_usage: "悟空对八戒：'你这耙子就是抓手，别丢！'", category: "执行用语" },
            { buzzword: "闭环", chinese_meaning: "完整循环", xiyou_usage: "如来：'取经项目必须形成闭环·九九八十一缺一不可。'", category: "方法论" },
            { buzzword: "打法", chinese_meaning: "策略方法", xiyou_usage: "悟空：'这妖怪的打法是变化+硬打，不行就搬救兵。'", category: "执行用语" },
            { buzzword: "沉淀", chinese_meaning: "积累", xiyou_usage: "唐僧：'14年取经·我们要沉淀出真经5048卷。'", category: "方法论" },
            { buzzword: "心智模型", chinese_meaning: "认知结构", xiyou_usage: "如来：'心猿意马，即心智模型未归正·需紧箍咒外部干预。'", category: "方法论" },
            { buzzword: "敏捷开发", chinese_meaning: "快速迭代", xiyou_usage: "悟空：'先打探虚实·再搬救兵·这是敏捷开发的精髓。'", category: "执行用语" },
            { buzzword: "MVP", chinese_meaning: "最小可行产品", xiyou_usage: "观音：'先收一个徒弟试试水·这是MVP·可行再扩团队。'", category: "项目用语" },
            { buzzword: "OKR", chinese_meaning: "目标与关键结果", xiyou_usage: "如来定OKR：O=取经成功，KR1=九九八十一难，KR2=14年完成，KR3=5人晋升。", category: "项目用语" },
            { buzzword: "向上管理", chinese_meaning: "管理上级", xiyou_usage: "悟空：'师父你别老赶我走·这叫向上管理。'", category: "职场用语" },
            { buzzword: "打透", chinese_meaning: "彻底解决", xiyou_usage: "悟空：'这次要把狮驼岭打透·不留后患。'", category: "执行用语" },
            { buzzword: "复用", chinese_meaning: "重复使用", xiyou_usage: "悟空：'紧箍咒这工具复用率太高·每次都被念。'", category: "方法论" }
        ]
    };

    // ===== 配色映射 =====
    const ALERT_COLORS = {
        "黄": "#e9b885",
        "橙": "#d97706",
        "红": "#c8463a",
        "红·极端高温": "#c8463a",
        "红·洪水": "#c8463a",
        "红·伪佛": "#c8463a",
        "SSS·全城紧急": "#1a1410"
    };
    const ALERT_RANK = {
        "黄": 1, "橙": 2, "红": 3, "红·极端高温": 3,
        "红·洪水": 3, "红·伪佛": 3, "SSS·全城紧急": 4
    };
    const SKILL_LEVEL_VALUE = { "初级": 2, "中级": 4, "高级": 6, "专家": 8, "大师": 10 };
    const PHASE_COLORS = ["#3a6b8c", "#c8463a", "#C9A063", "#6B8E5A"];
    const CAT_COLORS = {
        "会议用语": "#3a6b8c", "资源支持": "#6B8E5A", "方法论": "#C9A063",
        "汇报用语": "#c8463a", "执行用语": "#d97706", "项目用语": "#1a1410", "职场用语": "#C9A063"
    };

    // ===== 渲染：项目复盘卡片 =====
    function renderProjectMeta(p) {
        const meta = d3.select("#project-meta");
        meta.selectAll("*").remove();
        const items = [
            { k: "PROJECT · 项目名", v: p.project_name },
            { k: "CODE · 代号", v: p.project_code },
            { k: "DURATION · 时长", v: p.duration_years + " 年" },
            { k: "SPONSOR · 发起人", v: p.sponsor },
            { k: "PM · 项目经理", v: p.pm },
            { k: "TECH LEAD · 技术负责人", v: p.tech_lead },
            { k: "TEAM · 团队", v: p.team_size + " 人" },
            { k: "DELIVERY · 交付", v: p.deliverables },
            { k: "RATING · 评级", v: p.final_review.rating + " · " + p.final_review.comment }
        ];
        items.forEach(it => {
            const div = meta.append("div").attr("class", "meta-item");
            div.append("div").attr("class", "k").text(it.k);
            div.append("div").attr("class", "v").text(it.v);
        });
    }

    function renderMilestone(milestones) {
        const svg = d3.select("#milestone-svg");
        svg.selectAll("*").remove();
        const el = document.getElementById("milestone-svg");
        const w = Math.max(200, el.clientWidth || 1100);
        const h = 200;
        svg.attr("viewBox", `0 0 ${w} ${h}`);

        const margin = { top: 50, right: 40, bottom: 50, left: 40 };
        const innerW = w - margin.left - margin.right;
        const cy = h / 2;

        // 主轴
        svg.append("line")
            .attr("x1", margin.left).attr("x2", w - margin.right)
            .attr("y1", cy).attr("y2", cy)
            .attr("stroke", "var(--line)").attr("stroke-width", 2);

        const xStep = innerW / (milestones.length - 1);
        const tip = d3.select("#milestone-tip");

        milestones.forEach((m, i) => {
            const x = margin.left + xStep * i;
            const g = svg.append("g").attr("transform", `translate(${x},${cy})`);

            // 节点圆
            g.append("circle")
                .attr("r", 8)
                .attr("fill", "var(--accent)")
                .attr("stroke", "#fff").attr("stroke-width", 2)
                .style("cursor", "pointer")
                .on("mouseover", function(e) {
                    d3.select(this).transition().duration(150).attr("r", 11);
                    tip.style("opacity", 1)
                        .html(`<strong style="color:var(--accent-soft);">${m.phase}</strong><br/>` +
                              `<span style="font-size:0.78rem;color:#e9b885;">${m.year}</span><br/>` +
                              `${m.event}<br/>` +
                              `<span style="color:var(--accent-soft);">KPI: ${m.kpi}</span>`);
                })
                .on("mousemove", function(e) {
                    const rect = el.parentElement.getBoundingClientRect();
                    tip.style("left", (e.clientX - rect.left + 14) + "px")
                       .style("top", (e.clientY - rect.top - 10) + "px");
                })
                .on("mouseout", function() {
                    d3.select(this).transition().duration(150).attr("r", 8);
                    tip.style("opacity", 0);
                });

            // 阶段名（上方）
            g.append("text")
                .attr("y", -22)
                .attr("text-anchor", "middle")
                .style("font-size", "0.82rem")
                .style("font-weight", "600")
                .style("fill", "var(--accent-2)")
                .text(m.phase);

            // 年份（下方）
            g.append("text")
                .attr("y", 28)
                .attr("text-anchor", "middle")
                .style("font-size", "0.75rem")
                .style("fill", "var(--accent-3)")
                .style("font-family", "JetBrains Mono, monospace")
                .text(m.year);

            // 事件（更下方）
            const lines = m.event.split("·");
            lines.forEach((ln, j) => {
                g.append("text")
                    .attr("y", 44 + j * 14)
                    .attr("text-anchor", "middle")
                    .style("font-size", "0.75rem")
                    .style("fill", "var(--ink-soft)")
                    .text(ln);
            });
        });
    }

    // ===== 渲染：团队效能曲线 =====
    function renderEffectiveness(data) {
        const svg = d3.select("#effectiveness-svg");
        svg.selectAll("*").remove();
        const el = document.getElementById("effectiveness-svg");
        const w = Math.max(200, el.clientWidth || 1100);
        const h = 420;
        svg.attr("viewBox", `0 0 ${w} ${h}`);

        const margin = { top: 40, right: 40, bottom: 60, left: 50 };
        const innerW = w - margin.left - margin.right;
        const innerH = h - margin.top - margin.bottom;

        const phases = data.phases;
        const spikes = data.spike_points;

        // 解析章节范围中点
        phases.forEach(p => {
            const [a, b] = p.chapter_range.split("-").map(Number);
            p._mid = (a + b) / 2;
            p._start = a;
            p._end = b;
        });

        const xMin = 12, xMax = 100;
        const x = d3.scaleLinear().domain([xMin, xMax]).range([0, innerW]);
        const y = d3.scaleLinear().domain([0, 11]).range([innerH, 0]);

        const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

        // 阶段背景带
        phases.forEach((p, i) => {
            g.append("rect")
                .attr("x", x(p._start))
                .attr("y", 0)
                .attr("width",Math.max(0, x(p._end) - x(p._start)))
                .attr("height", innerH)
                .attr("fill", PHASE_COLORS[i])
                .attr("opacity", 0.06);
        });

        // 阶段标签
        phases.forEach((p, i) => {
            g.append("text")
                .attr("x", x(p._mid))
                .attr("y", -16)
                .attr("text-anchor", "middle")
                .style("font-size", "0.82rem")
                .style("font-weight", "600")
                .style("fill", PHASE_COLORS[i])
                .text(p.phase);
            g.append("text")
                .attr("x", x(p._mid))
                .attr("y", -2)
                .attr("text-anchor", "middle")
                .style("font-size", "0.7rem")
                .style("fill", "var(--ink-soft)")
                .style("font-family", "JetBrains Mono, monospace")
                .text("第" + p.chapter_range + "回");
        });

        // X 轴
        g.append("g")
            .attr("transform", `translate(0,${innerH})`)
            .call(d3.axisBottom(x).ticks(10).tickFormat(d => "第" + d + "回"))
            .selectAll("text").style("font-size", "0.72rem").style("fill", "var(--ink-soft)");

        // Y 轴
        g.append("g")
            .call(d3.axisLeft(y).ticks(10).tickFormat(d => d))
            .selectAll("text").style("font-size", "0.75rem").style("fill", "var(--ink-soft)");

        // 轴标签
        g.append("text")
            .attr("transform", "rotate(-90)")
            .attr("x", -innerH / 2)
            .attr("y", -38)
            .attr("text-anchor", "middle")
            .style("font-size", "0.78rem")
            .style("fill", "var(--accent-3)")
            .text("Effectiveness 效能值");

        g.append("text")
            .attr("x", innerW / 2)
            .attr("y", innerH + 44)
            .attr("text-anchor", "middle")
            .style("font-size", "0.78rem")
            .style("fill", "var(--accent-3)")
            .text("章节回目（项目时间线）");

        // 网格线
        g.append("g")
            .selectAll("line")
            .data([2, 4, 6, 8, 10])
            .enter()
            .append("line")
            .attr("x1", 0).attr("x2", innerW)
            .attr("y1", d => y(d)).attr("y2", d => y(d))
            .attr("stroke", "var(--line)")
            .attr("stroke-dasharray", "3,3")
            .attr("opacity", 0.5);

        // 主效能曲线（阶段点）
        const line = d3.line()
            .x(d => x(d._mid))
            .y(d => y(d.effectiveness))
            .curve(d3.curveMonotoneX);

        const path = g.append("path")
            .datum(phases)
            .attr("fill", "none")
            .attr("stroke", "var(--accent)")
            .attr("stroke-width", 3)
            .attr("d", line);

        // 路径动画
        const totalLen = path.node().getTotalLength();
        path.attr("stroke-dasharray", totalLen)
            .attr("stroke-dashoffset", totalLen)
            .transition()
            .duration(1500)
            .ease(d3.easeCubicOut)
            .attr("stroke-dashoffset", 0);

        // 阶段点
        g.selectAll(".phase-dot")
            .data(phases)
            .enter()
            .append("circle")
            .attr("class", "phase-dot")
            .attr("cx", d => x(d._mid))
            .attr("cy", d => y(d.effectiveness))
            .attr("r", 7)
            .attr("fill", "var(--accent-2)")
            .attr("stroke", "#fff").attr("stroke-width", 2)
            .style("opacity", 0)
            .transition().delay(800).duration(400)
            .style("opacity", 1);

        // 阶段点标注（效能值）
        g.selectAll(".eff-label")
            .data(phases)
            .enter()
            .append("text")
            .attr("class", "eff-label")
            .attr("x", d => x(d._mid))
            .attr("y", d => y(d.effectiveness) - 14)
            .attr("text-anchor", "middle")
            .style("font-size", "0.85rem")
            .style("font-weight", "600")
            .style("fill", "var(--accent)")
            .style("opacity", 0)
            .text(d => d.effectiveness)
            .transition().delay(1000).duration(400)
            .style("opacity", 1);

        // Spike 点
        const tip = d3.select("#eff-tip");
        g.selectAll(".spike-dot")
            .data(spikes)
            .enter()
            .append("circle")
            .attr("class", "spike-dot")
            .attr("cx", d => x(d.chapter))
            .attr("cy", d => y(d.spike))
            .attr("r", 9)
            .attr("fill", "var(--accent-4)")
            .attr("stroke", "var(--accent)").attr("stroke-width", 2.5)
            .style("cursor", "pointer")
            .style("opacity", 0)
            .transition().delay(1400).duration(500)
            .style("opacity", 1);

        // 重新绑定事件（动画后）
        g.selectAll(".spike-dot")
            .on("mouseover", function(e, d) {
                d3.select(this).transition().duration(150).attr("r", 12);
                tip.style("opacity", 1)
                    .html(`<div class="tip-title">第${d.chapter}回 · ${d.event}</div>` +
                          `<div>飙升值：<strong style="color:var(--accent-soft);">+${d.spike}</strong></div>` +
                          `<div style="margin-top:4px;font-size:0.78rem;color:#e9b885;">${d.note}</div>`);
            })
            .on("mousemove", function(e) {
                const rect = el.parentElement.getBoundingClientRect();
                tip.style("left", (e.clientX - rect.left + 14) + "px")
                   .style("top", (e.clientY - rect.top - 10) + "px");
            })
            .on("mouseout", function() {
                d3.select(this).transition().duration(150).attr("r", 9);
                tip.style("opacity", 0);
            });

        // Spike 点标注（飙升值）
        g.selectAll(".spike-label")
            .data(spikes)
            .enter()
            .append("text")
            .attr("class", "spike-label")
            .attr("x", d => x(d.chapter))
            .attr("y", d => y(d.spike) + 22)
            .attr("text-anchor", "middle")
            .style("font-size", "0.78rem")
            .style("font-weight", "600")
            .style("fill", "var(--accent-4)")
            .style("opacity", 0)
            .text(d => "+" + d.spike)
            .transition().delay(1600).duration(400)
            .style("opacity", 1);
    }

    // ===== 渲染：差旅行程表 =====
    function renderTripTable(trips) {
        const sorted = trips.slice().sort((a, b) => {
            const ra = ALERT_RANK[a.alert_level] || 0;
            const rb = ALERT_RANK[b.alert_level] || 0;
            if (ra !== rb) return ra - rb;
            return (a.n || 0) - (b.n || 0);
        });

        const tbody = d3.select("#trip-tbody");
        tbody.selectAll("*").remove();
        sorted.forEach(t => {
            const tr = tbody.append("tr");
            tr.append("td").attr("class", "num").text("第" + t.n + "难");
            tr.append("td").text(t.hardship);
            tr.append("td").text(t.location);
            tr.append("td").html(`<span class="alert-badge" style="background:${ALERT_COLORS[t.alert_level] || '#999'}">${t.alert_level}</span>`);
            tr.append("td").text(t.weather);
            tr.append("td").text(t.remark);
            tr.append("td").attr("class", "delay").text("+" + t.delay_days);
        });
    }

    // ===== 渲染：悟空简历 =====
    function renderResumeBasic(info) {
        const sel = d3.select("#resume-basic");
        sel.selectAll("*").remove();
        sel.append("h3").text("基本信息 · " + info.basic_info.name);
        const grid = sel.append("div").attr("class", "resume-basic-grid");
        const fields = [
            { k: "曾用名", v: info.basic_info.alias },
            { k: "籍贯", v: info.basic_info.birthplace },
            { k: "学历", v: info.basic_info.education },
            { k: "专业", v: info.basic_info.major },
            { k: "联系方式", v: info.basic_info.phone }
        ];
        fields.forEach(f => {
            const d = grid.append("div").attr("class", "field");
            d.html(`<span style="color:var(--accent-3);font-size:0.78rem;">${f.k}</span><br/><strong>${f.v}</strong>`);
        });
    }

    function renderWorkExperience(exp) {
        const sel = d3.select("#work-grid");
        sel.selectAll("*").remove();
        exp.forEach(w => {
            const card = sel.append("div").attr("class", "work-card");
            card.append("div").attr("class", "wc-company").text(w.company);
            card.append("div").attr("class", "wc-position").text(w.position);
            card.append("div").attr("class", "wc-duration").text("⏱ " + w.duration);
            card.append("div").attr("class", "wc-ach").text("成果：" + w.achievements);
            card.append("div").attr("class", "wc-reason").text("离职：" + w.reason_for_leave);
        });
    }

    function renderSkills(skills) {
        const svg = d3.select("#skill-svg");
        svg.selectAll("*").remove();
        const el = document.getElementById("skill-svg");
        const w = Math.max(200, el.clientWidth || 1100);
        const h = 260;
        svg.attr("viewBox", `0 0 ${w} ${h}`);

        const margin = { top: 20, right: 80, bottom: 20, left: 130 };
        const innerW = w - margin.left - margin.right;
        const barH = 28;
        const gap = 14;
        const totalH = skills.length * (barH + gap) - gap;
        svg.attr("viewBox", `0 0 ${w} ${Math.max(h, totalH + margin.top + margin.bottom)}`);

        const maxY = 10;
        const x = d3.scaleLinear().domain([0, maxY]).range([0, innerW]);

        const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

        skills.forEach((s, i) => {
            const yPos = i * (barH + gap);
            const val = SKILL_LEVEL_VALUE[s.level] || 5;
            const color = val >= 9 ? "var(--accent)" : val >= 7 ? "var(--accent-3)" : "var(--accent-2)";

            // 技能名
            g.append("text")
                .attr("x", -12)
                .attr("y", yPos + barH / 2 + 4)
                .attr("text-anchor", "end")
                .style("font-size", "0.86rem")
                .style("font-weight", "600")
                .style("fill", "var(--ink)")
                .text(s.skill);

            // 背景轨道
            g.append("rect")
                .attr("x", 0).attr("y", yPos)
                .attr("width",Math.max(0, innerW)).attr("height", barH)
                .attr("fill", "#faf7f2")
                .attr("stroke", "var(--line)")
                .attr("rx", 4);

            // 数值条
            g.append("rect")
                .attr("x", 0).attr("y", yPos)
                .attr("width",0).attr("height", barH)
                .attr("fill", color)
                .attr("rx", 4)
                .transition()
                .delay(i * 120).duration(800)
                .ease(d3.easeCubicOut)
                .attr("width",Math.max(0, x(val)));

            // 等级标签
            g.append("text")
                .attr("x", x(val) + 8)
                .attr("y", yPos + barH / 2 + 4)
                .style("font-size", "0.82rem")
                .style("font-weight", "600")
                .style("fill", color)
                .text(s.level);

            // 注释（小字）
            g.append("text")
                .attr("x", innerW)
                .attr("y", yPos + barH / 2 + 4)
                .attr("text-anchor", "end")
                .style("font-size", "0.72rem")
                .style("fill", "var(--ink-soft)")
                .style("font-style", "italic")
                .text(s.note);
        });
    }

    function renderInterview(interviews) {
        const sel = d3.select("#interview-grid");
        sel.selectAll("*").remove();
        interviews.forEach((iv, i) => {
            const card = sel.append("div").attr("class", "interview-card");
            card.append("div").attr("class", "ic-emoji").text("😎");
            card.append("div").attr("class", "ic-q").text("Q" + (i + 1) + " · 压力面试");
            card.append("div").attr("class", "ic-question").text(iv.question);
            card.append("div").attr("class", "ic-a-label").text("A · 悟空回答：");
            card.append("div").attr("class", "ic-answer").text(iv.wukong_answer);
            card.append("div").attr("class", "ic-note").text("🎭 " + iv.emoji_note);
        });
    }

    // ===== 渲染：黑话词典 =====
    function renderBuzzwords(words) {
        const sel = d3.select("#buzzword-grid");
        sel.selectAll("*").remove();
        words.forEach(b => {
            const card = sel.append("div").attr("class", "buzzword-card");
            card.style("border-left-color", CAT_COLORS[b.category] || "var(--accent)");
            const head = card.append("div").attr("class", "bw-head");
            head.append("div").attr("class", "bw-word").text(b.buzzword);
            head.append("div").attr("class", "bw-cat").style("background", CAT_COLORS[b.category] || "var(--accent-soft)")
                .style("color", "#fff").text(b.category);
            card.append("div").attr("class", "bw-meaning").text("释义：" + b.chinese_meaning);
            card.append("div").attr("class", "bw-usage").text(b.xiyou_usage);
        });
    }

    // ===== 渲染：关键洞察 =====
    function renderInsights() {
        const insights = [
            `取经项目 <strong>14 年强制团建</strong>，团队经历 Forming → Storming → Norming → Performing 全过程，最终 A+ 评级交付。`,
            `三打白骨精（27回）后团队效能降至最低，<strong>真假美猴王（58回）后飙升 +3 进入规范期</strong>，验证"危机即转机"。`,
            `狮驼岭警报 <strong>SSS 级</strong>，需如来亲降；火焰山/红孩儿属极端高温，<strong>需发放高温补贴</strong>。`,
            `悟空简历亮点：<strong>策划天庭压力测试·推动安保与组织升级</strong>，搬救兵 30+ 次体现资源调度能力。`,
            `黑话词典揭示：<strong>"对齐/闭环/赋能/抓手"</strong>等 15 个互联网词汇，皆可在取经项目中找到对应场景。`
        ];
        const ul = d3.select("#insights");
        ul.selectAll("*").remove();
        insights.forEach(t => ul.append("li").html(t));
    }

    // ===== 数据加载 =====
    async function loadJson(path, fallback) {
        try {
            const res = await fetch(path);
            if (!res.ok) throw new Error("fetch failed: " + path);
            return await res.json();
        } catch (e) {
            console.warn("[INFO] 使用嵌入数据 for", path, ":", e.message);
            return fallback;
        }
    }

    async function loadAll() {
        const [pr, te, tr, wr, ib] = await Promise.all([
            loadJson("../../scripts/output/data/project_review.json", EMBEDDED.project_review),
            loadJson("../../scripts/output/data/team_effectiveness.json", EMBEDDED.team_effectiveness),
            loadJson("../../scripts/output/data/trip_report.json", EMBEDDED.trip_report),
            loadJson("../../scripts/output/data/wukong_resume.json", EMBEDDED.wukong_resume),
            loadJson("../../scripts/output/data/internet_buzzwords.json", EMBEDDED.internet_buzzwords)
        ]);
        return { project_review: pr, team_effectiveness: te, trip_report: tr, wukong_resume: wr, internet_buzzwords: ib };
    }

    // ===== 主流程 =====
    async function main() {
        const data = await loadAll();
        window.__data = data;

        // 如果 fetch 成功，更新数据源提示
        if (data.project_review === EMBEDDED.project_review) {
            // 仍是嵌入数据
        } else {
            document.getElementById("dataSource").innerHTML =
                "数据源：实时加载自 <code>scripts/output/data/</code>（运行于 http server 模式）";
        }

        renderProjectMeta(data.project_review);
        renderMilestone(data.project_review.milestones);
        renderEffectiveness(data.team_effectiveness);
        renderTripTable(data.trip_report);
        renderResumeBasic(data.wukong_resume);
        renderWorkExperience(data.wukong_resume.work_experience);
        renderSkills(data.wukong_resume.skills);
        renderInterview(data.wukong_resume.stress_interview);
        renderBuzzwords(data.internet_buzzwords);
        renderInsights();

        // 生成时间
        const genTimeEl = document.getElementById("gen-time");
        if (genTimeEl) genTimeEl.textContent =
            "数据生成时间：" + new Date().toISOString().slice(0, 19).replace("T", " ") + " (Asia/Shanghai)";
    }

    // 窗口缩放重绘
    let resizeTimer;
    window.addEventListener("resize", () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            if (window.__data) {
                renderMilestone(window.__data.project_review.milestones);
                renderEffectiveness(window.__data.team_effectiveness);
                renderSkills(window.__data.wukong_resume.skills);
            }
        }, 250);
    });

    // 性能：D3 改为 defer 加载，DOM 就绪后再启动渲染（不阻塞首屏）
    window.addEventListener('DOMContentLoaded', main);
    