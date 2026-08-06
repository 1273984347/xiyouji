
    // ============= EMBEDDED_DATA =============
    const EMBEDDED_DATA = {
        meta: {title: "人物关系 3D 网络图", version: "v2.2.42", w_id: "W236-V", direction: "V4"},
        kpi: [
            {label: "NODES · 节点数", value: "22", desc: "人物节点"},
            {label: "EDGES · 边数", value: "32", desc: "关系边"},
            {label: "CLUSTERS · 聚类", value: "5", desc: "阵营聚类"},
            {label: "CENTRALITY · 最高中心性", value: "悟空", desc: "度中心性 0.78"},
            {label: "DEGREE · 最高度数", value: "唐僧", desc: "度数 9"}
        ],
        // 22 个角色节点：id, name, group (0=取经团,1=天庭,2=佛门,3=妖界,4=龙族), importance (1-10), desc
        nodes: [
            {id: 1, name: "唐僧", group: 0, importance: 9, desc: "金蝉子转世，取经团队核心，意志坚定但常陷险境。"},
            {id: 2, name: "孙悟空", group: 0, importance: 10, desc: "齐天大圣，神通广大，降妖除魔的主力。"},
            {id: 3, name: "猪八戒", group: 0, importance: 7, desc: "天蓬元帅转世，贪吃好色但忠心耿耿。"},
            {id: 4, name: "沙悟净", group: 0, importance: 6, desc: "卷帘大将转世，沉稳老实，挑担随行。"},
            {id: 5, name: "白龙马", group: 0, importance: 5, desc: "西海龙王三太子，化身为马驮唐僧。"},
            {id: 6, name: "观音菩萨", group: 2, importance: 9, desc: "南海普陀落伽山，取经事业的策划者与守护者。"},
            {id: 7, name: "如来佛祖", group: 2, importance: 10, desc: "西天灵山释迦牟尼，最终授经者。"},
            {id: 8, name: "文殊菩萨", group: 2, importance: 6, desc: "五台山文殊，智慧象征。"},
            {id: 9, name: "普贤菩萨", group: 2, importance: 6, desc: "峨眉山普贤，行愿象征。"},
            {id: 10, name: "玉皇大帝", group: 1, importance: 9, desc: "天庭最高统治者，三界之主。"},
            {id: 11, name: "太白金星", group: 1, importance: 7, desc: "天庭外交官，多次招安悟空。"},
            {id: 12, name: "二郎神", group: 1, importance: 8, desc: "杨戬，玉帝外甥，擒获悟空。"},
            {id: 13, name: "托塔天王", group: 1, importance: 7, desc: "李靖，天兵统帅，多次征讨。"},
            {id: 14, name: "哪吒", group: 1, importance: 7, desc: "三太子，先锋官，与悟空交战。"},
            {id: 15, name: "牛魔王", group: 3, importance: 8, desc: "平天大圣，悟空结拜大哥，最终归顺。"},
            {id: 16, name: "铁扇公主", group: 3, importance: 6, desc: "罗刹女，芭蕉扇主人，牛魔王之妻。"},
            {id: 17, name: "红孩儿", group: 3, importance: 7, desc: "圣婴大王，牛魔王之子，三昧真火。"},
            {id: 18, name: "白骨精", group: 3, importance: 6, desc: "白骨夫人，三变戏悟空，致师徒离心。"},
            {id: 19, name: "黄袍怪", group: 3, importance: 6, desc: "奎木狼下凡，与百花羞宿缘。"},
            {id: 20, name: "六耳猕猴", group: 3, importance: 8, desc: "假悟空，乱真难辨，全书最大悬案。"},
            {id: 21, name: "东海龙王", group: 4, importance: 6, desc: "敖广，悟空借取定海神针。"},
            {id: 22, name: "西海龙王", group: 4, importance: 5, desc: "敖闰，白龙马之父。"}
        ],
        // 32 条关系边：source, target, type (师徒/结拜/父子/敌对/盟友/亲属/从属)
        links: [
            {source: 1, target: 2, type: "师徒"},
            {source: 1, target: 3, type: "师徒"},
            {source: 1, target: 4, type: "师徒"},
            {source: 1, target: 5, type: "师徒"},
            {source: 1, target: 6, type: "庇护"},
            {source: 6, target: 7, type: "从属"},
            {source: 6, target: 1, type: "指派"},
            {source: 6, target: 8, type: "同僚"},
            {source: 6, target: 9, type: "同僚"},
            {source: 7, target: 1, type: "授经"},
            {source: 2, target: 10, type: "反叛"},
            {source: 2, target: 12, type: "敌对"},
            {source: 2, target: 13, type: "敌对"},
            {source: 2, target: 14, type: "敌对"},
            {source: 2, target: 21, type: "索取"},
            {source: 2, target: 15, type: "结拜"},
            {source: 2, target: 20, type: "宿敌"},
            {source: 10, target: 11, type: "从属"},
            {source: 10, target: 12, type: "从属"},
            {source: 10, target: 13, type: "从属"},
            {source: 10, target: 14, type: "从属"},
            {source: 13, target: 14, type: "父子"},
            {source: 12, target: 14, type: "兄弟"},
            {source: 15, target: 16, type: "夫妻"},
            {source: 15, target: 17, type: "父子"},
            {source: 16, target: 17, type: "母子"},
            {source: 2, target: 16, type: "敌对"},
            {source: 2, target: 17, type: "敌对"},
            {source: 2, target: 18, type: "击杀"},
            {source: 2, target: 19, type: "交战"},
            {source: 5, target: 22, type: "父子"},
            {source: 21, target: 22, type: "兄弟"}
        ]
    };

    const GROUP_COLORS = [0xe67e22, 0x3a6b8c, 0x8c2a2a, 0x5a7a3a, 0x7a5230];
    const GROUP_NAMES = ["取经团", "天庭", "佛门", "妖界", "龙族"];

    // 渲染 KPI
    function renderKPI(data) {
        const kpiRow = document.getElementById("kpiRow");
        data.kpi.forEach(k => {
            const card = document.createElement("div");
            card.className = "kpi-card";
            card.innerHTML = `<div class="label">${k.label}</div><div class="value">${k.value}</div><div class="desc">${k.desc}</div>`;
            kpiRow.appendChild(card);
        });
    }

    // ============= Three.js 3D 力导向图 =============
    let scene, camera, renderer, controls;
    let nodeMeshes = [];
    let linkLines = [];
    let raycaster, mouse;
    let nodePositions = [];
    let velocity = [];
    let selectedNode = null;

    function init3D() {
        const container = document.getElementById("three-container");
        const w = container.clientWidth;
        const h = container.clientHeight;

        // 场景
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1a2530);
        scene.fog = new THREE.Fog(0x1a2530, 200, 600);

        // 相机
        camera = new THREE.PerspectiveCamera(60, w / h, 0.1, 2000);
        camera.position.set(0, 0, 280);

        // 渲染器
        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(w, h);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); // 性能：限制 DPR，避免视网膜屏 2-3x 过度绘制
        container.appendChild(renderer.domElement);

        // 光照
        const ambient = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambient);
        const pointLight = new THREE.PointLight(0xffffff, 1.0, 500);
        pointLight.position.set(100, 100, 100);
        scene.add(pointLight);
        const pointLight2 = new THREE.PointLight(0xe67e22, 0.5, 500);
        pointLight2.position.set(-100, -100, 100);
        scene.add(pointLight2);

        // OrbitControls（手动实现，避免外部依赖）
        setupOrbitControls(container);

        // 初始化节点位置（按聚类分组建圈）
        const groupNodes = [[], [], [], [], []];
        EMBEDDED_DATA.nodes.forEach(n => groupNodes[n.group].push(n));

        nodePositions = [];
        velocity = [];
        EMBEDDED_DATA.nodes.forEach((node, i) => {
            const groupIdx = node.group;
            const groupSize = groupNodes[groupIdx].length;
            const idxInGroup = groupNodes[groupIdx].indexOf(node);
            // 每个聚类成一个环
            const clusterRadius = 40 + groupIdx * 15;
            const angleStep = (Math.PI * 2) / groupSize;
            const angle = idxInGroup * angleStep + groupIdx * 0.5;
            const clusterOffset = groupIdx * 60 - 120;
            const axis = groupIdx % 2 === 0 ? "x" : "y";
            let x, y, z;
            if (axis === "x") {
                x = clusterRadius * Math.cos(angle);
                y = clusterOffset;
                z = clusterRadius * Math.sin(angle);
            } else {
                x = clusterOffset;
                y = clusterRadius * Math.cos(angle);
                z = clusterRadius * Math.sin(angle);
            }
            nodePositions.push(new THREE.Vector3(x, y, z));
            velocity.push(new THREE.Vector3(0, 0, 0));
        });

        // 创建节点
        EMBEDDED_DATA.nodes.forEach((node, i) => {
            const radius = 4 + node.importance * 0.8;
            const geo = new THREE.SphereGeometry(radius, 32, 32);
            const mat = new THREE.MeshPhongMaterial({
                color: GROUP_COLORS[node.group],
                shininess: 80,
                specular: 0x444444
            });
            const mesh = new THREE.Mesh(geo, mat);
            mesh.position.copy(nodePositions[i]);
            mesh.userData = { nodeIndex: i, node: node };
            scene.add(mesh);
            nodeMeshes.push(mesh);

            // 节点光环（外圈）
            const ringGeo = new THREE.RingGeometry(radius * 1.4, radius * 1.6, 32);
            const ringMat = new THREE.MeshBasicMaterial({
                color: GROUP_COLORS[node.group],
                transparent: true,
                opacity: 0.4,
                side: THREE.DoubleSide
            });
            const ring = new THREE.Mesh(ringGeo, ringMat);
            ring.position.copy(nodePositions[i]);
            ring.lookAt(camera.position);
            mesh.userData.ring = ring;
            scene.add(ring);

            // 文字标签（精灵）
            const sprite = createTextSprite(node.name);
            sprite.position.copy(nodePositions[i]);
            sprite.position.y += radius + 8;
            mesh.userData.label = sprite;
            scene.add(sprite);
        });

        // 创建边
        const lineMat = new THREE.LineBasicMaterial({
            color: 0xaab8c8,
            transparent: true,
            opacity: 0.4
        });
        EMBEDDED_DATA.links.forEach(link => {
            const geo = new THREE.BufferGeometry();
            const positions = new Float32Array(6);
            geo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
            const line = new THREE.Line(geo, lineMat);
            scene.add(line);
            linkLines.push({ line: line, source: link.source, target: link.target, type: link.type });
        });

        // Raycaster
        raycaster = new THREE.Raycaster();
        mouse = new THREE.Vector2();

        // 鼠标事件
        container.addEventListener("click", onNodeClick);
        container.addEventListener("mousemove", onNodeHover);

        // 窗口调整
        window.addEventListener("resize", onWindowResize);

        // 关闭按钮
        document.getElementById("infoClose").addEventListener("click", function() {
            document.getElementById("infoPanel").style.display = "none";
            if (selectedNode) {
                selectedNode.material.emissive.setHex(0x000000);
                selectedNode = null;
            }
        });

        animate();
    }

    // 文字精灵
    function createTextSprite(text) {
        const canvas = document.createElement("canvas");
        canvas.width = 256;
        canvas.height = 64;
        const ctx = canvas.getContext("2d");
        ctx.fillStyle = "rgba(0, 0, 0, 0)";
        ctx.fillRect(0, 0, 256, 64);
        ctx.font = "bold 32px 'Noto Serif SC', serif";
        ctx.fillStyle = "#f5e9d4";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(text, 128, 32);
        const texture = new THREE.CanvasTexture(canvas);
        const mat = new THREE.SpriteMaterial({ map: texture, transparent: true });
        const sprite = new THREE.Sprite(mat);
        sprite.scale.set(30, 8, 1);
        return sprite;
    }

    // OrbitControls 手动实现
    let isDragging = false;
    let prevMouse = { x: 0, y: 0 };
    let cameraTheta = 0;
    let cameraPhi = Math.PI / 2;
    let cameraRadius = 280;

    function setupOrbitControls(container) {
        container.addEventListener("mousedown", function(e) {
            isDragging = true;
            prevMouse.x = e.clientX;
            prevMouse.y = e.clientY;
        });
        document.addEventListener("mouseup", function() { isDragging = false; });
        document.addEventListener("mousemove", function(e) {
            if (!isDragging) return;
            const dx = e.clientX - prevMouse.x;
            const dy = e.clientY - prevMouse.y;
            cameraTheta -= dx * 0.005;
            cameraPhi -= dy * 0.005;
            cameraPhi = Math.max(0.1, Math.min(Math.PI - 0.1, cameraPhi));
            prevMouse.x = e.clientX;
            prevMouse.y = e.clientY;
            updateCameraPosition();
        });
        container.addEventListener("wheel", function(e) {
            e.preventDefault();
            cameraRadius += e.deltaY * 0.3;
            cameraRadius = Math.max(80, Math.min(600, cameraRadius));
            updateCameraPosition();
        });
    }

    function updateCameraPosition() {
        camera.position.x = cameraRadius * Math.sin(cameraPhi) * Math.cos(cameraTheta);
        camera.position.y = cameraRadius * Math.cos(cameraPhi);
        camera.position.z = cameraRadius * Math.sin(cameraPhi) * Math.sin(cameraTheta);
        camera.lookAt(0, 0, 0);
    }

    function onWindowResize() {
        const container = document.getElementById("three-container");
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
    }

    function onNodeClick(event) {
        const container = document.getElementById("three-container");
        const rect = container.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(nodeMeshes);

        if (intersects.length > 0) {
            const mesh = intersects[0].object;
            const node = mesh.userData.node;

            if (selectedNode) {
                selectedNode.material.emissive.setHex(0x000000);
            }
            selectedNode = mesh;
            mesh.material.emissive.setHex(0x442200);

            // 显示信息面板
            const panel = document.getElementById("infoPanel");
            document.getElementById("infoName").textContent = node.name;
            const groupIdx = node.group;
            document.getElementById("infoDesc").innerHTML = node.desc;
            // 计算度数
            const degree = EMBEDDED_DATA.links.filter(l => l.source === node.id || l.target === node.id).length;
            document.getElementById("infoMeta").innerHTML =
                `阵营：${GROUP_NAMES[groupIdx]}<br>` +
                `重要性：${node.importance}/10<br>` +
                `度数：${degree}<br>` +
                `ID：#${node.id}`;
            panel.style.display = "block";
        }
    }

    function onNodeHover(event) {
        const container = document.getElementById("three-container");
        const rect = container.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(nodeMeshes);
        container.style.cursor = intersects.length > 0 ? "pointer" : "grab";
    }

    // 力导向模拟
    function applyForces() {
        const repulsion = 800;
        const attraction = 0.005;
        const damping = 0.85;
        const idealLength = 50;

        // 节点间斥力
        for (let i = 0; i < nodePositions.length; i++) {
            for (let j = i + 1; j < nodePositions.length; j++) {
                const diff = new THREE.Vector3().subVectors(nodePositions[i], nodePositions[j]);
                const dist = Math.max(0.1, diff.length());
                const force = repulsion / (dist * dist);
                diff.normalize().multiplyScalar(force);
                velocity[i].add(diff);
                velocity[j].sub(diff);
            }
        }

        // 边的引力
        linkLines.forEach(link => {
            const i = link.source - 1;
            const j = link.target - 1;
            const diff = new THREE.Vector3().subVectors(nodePositions[j], nodePositions[i]);
            const dist = Math.max(0.1, diff.length());
            const force = (dist - idealLength) * attraction;
            diff.normalize().multiplyScalar(force);
            velocity[i].add(diff);
            velocity[j].sub(diff);
        });

        // 更新位置
        for (let i = 0; i < nodePositions.length; i++) {
            velocity[i].multiplyScalar(damping);
            // 限制速度
            const maxSpeed = 2;
            if (velocity[i].length() > maxSpeed) {
                velocity[i].normalize().multiplyScalar(maxSpeed);
            }
            nodePositions[i].add(velocity[i]);
            // 轻微回归中心
            nodePositions[i].multiplyScalar(0.999);
            // 更新 mesh 位置
            nodeMeshes[i].position.copy(nodePositions[i]);
            if (nodeMeshes[i].userData.ring) {
                nodeMeshes[i].userData.ring.position.copy(nodePositions[i]);
                nodeMeshes[i].userData.ring.lookAt(camera.position);
            }
            if (nodeMeshes[i].userData.label) {
                const r = 4 + EMBEDDED_DATA.nodes[i].importance * 0.8;
                nodeMeshes[i].userData.label.position.copy(nodePositions[i]);
                nodeMeshes[i].userData.label.position.y += r + 8;
            }
        }

        // 更新边
        linkLines.forEach(link => {
            const i = link.source - 1;
            const j = link.target - 1;
            const positions = link.line.geometry.attributes.position.array;
            positions[0] = nodePositions[i].x;
            positions[1] = nodePositions[i].y;
            positions[2] = nodePositions[i].z;
            positions[3] = nodePositions[j].x;
            positions[4] = nodePositions[j].y;
            positions[5] = nodePositions[j].z;
            link.line.geometry.attributes.position.needsUpdate = true;
        });
    }

    function animate() {
        requestAnimationFrame(animate);
        if (document.hidden) return;  // 性能：标签页隐藏时跳过物理与渲染
        applyForces();
        // 节点缓慢自转
        nodeMeshes.forEach(mesh => {
            mesh.rotation.y += 0.005;
        });
        renderer.render(scene, camera);
    }

    // ============= 主流程 =============
    function main() {
        renderKPI(EMBEDDED_DATA);
        if (typeof THREE !== "undefined") {
            init3D();
            updateCameraPosition();
        } else {
            document.getElementById("three-container").innerHTML =
                '<div style="color:#f5e9d4; padding:40px; text-align:center;">Three.js 加载失败，请检查网络。</div>';
        }
    }

    main();
    