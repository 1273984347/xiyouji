### W1198（2026-11-10）：Dependabot 41 条 Pillow 告警归零批（删除后重建依赖清单触发依赖图重算）

**本批要点**（41 条 Pillow 告警的根因在依赖图条目生命周期·读数来自 Graph Update run 日志与 SBOM API 实查）：

> - **T1 根因（与前两批的判断相反）**：W1193 把这 41 条判为「未随清单变更重算的 stale 投影」。本批实证证伪该判断：**依赖图里确实存在 pillow@12.3.0 的活条目**（SBOM API 返回三个 pillow SPDXID：13.0.0×2 与 12.3.0×1，其中 12.3.0 被 main 以 DEPENDS_ON 直接引用）⇒ 告警引擎按依赖图当前状态评估 ⇒ 41 条告警永远 open、updated_at 停在 2026-10-22 与 2026-10-24。
> - **T2 对拍证据（读它的运行日志，不从告警文案推测）**：抓 GitHub 自身的 Graph Update run 日志（run 42753213397 与 42633604982），其 manifests → resolved 段显示**每次解析结果都只有 pkg:pypi/pillow@13.0.0**，从未出现 12.3.0 ⇒ 12.3.0 不是任何一次解析的产物 ⇒ 只能来自历史 blob 留下的条目（依赖图按 manifest 路径累积·版本变更只新增不清理）。
> - **T3 前两批修法为何无效**：W1191（纯注释变更）与 W1193（依赖名大小写归一）都只让依赖图**新增**条目、从不删除 ⇒ 两条路都不可能关闭告警；这解释了「清单已钉 13.0.0 而告警仍在」的现象。
> - **T4 修法（让该路径消失一次）**：删除 scripts/requirements.txt（CI 的安装源本就是哈希化清单，删除不改变 CI 行为）⇒ GitHub 依赖图移除该 manifest 贡献的全部条目（含 12.3.0 残留）⇒ 第二步逐字重建该文件 ⇒ 依赖图写入干净的 pillow@13.0.0、Dependabot 恢复对 /scripts 的监控。两次提交在同一个 PR 内相邻落地（删除在前、重建在后），使 main 上依次出现「该路径不存在」与「该路径重建」两个状态。
> - **T5 CI 判据同源修正**：cache-dependency-path（4 处）与 pip-audit 扫描源（2 处）改指 scripts/requirements-hashed.txt —— CI 自 W1195 起已用该清单安装，而缓存键与审计源仍指向另一份文件；本批统一到真实安装源，pip-audit 审计覆盖面由 9 项直接依赖扩到 51 项闭包（实测 rc 0 · No known vulnerabilities found）。
> - **T6 J3 判据漂移修正**：test_ci_wiring.py 的 PyYAML 登记断言自 W813 起绑定 scripts/requirements.txt，而 CI 的真实安装源自 W1195 起已是哈希化清单 ⇒ 判据与安装源脱节；本批改绑真实安装源，并加回「Dependabot 监控面亦须声明 PyYAML」的第二段断言。
> - **T7 坑表 E-219 入表**：依赖图条目按 manifest 路径累积历史 blob 的规律（改内容不触发清理·改版本不关闭告警·须让路径消失一次·Dependency submission API 是追加语义不能清残留）与计数链同步。
> - **状态**：已落地。
> - **文件**：见 file-index。

### W1197（2026-11-10）：守卫扫描面扩到全仓 shell 批（两守卫扩面 + 接入 CI 阻断）

**本批要点**（守卫扫描面扩到全仓 shell·读数来自 Scorecard 源码实读与变异自证）：

> - **T1 根因（上批登记的已知缺口）**：Scorecard 的依赖扫描面是 `Pattern: "*"`（**全仓 shell 脚本**）、`"*Dockerfile*"`、`".github/workflows/*"`；而本仓守卫 `check_install_pins.py` / `check_action_refs.py` 是 workflow-only。上批变异自证已确认该缺口真实。
> - **T2 识别规则抽共享模块**：新建 `scripts/external_rule_scope.py`，实现 Scorecard `isMatchingShellScriptFile` 的识别规则（扩展名属 shell 家族 或 首行 shebang 匹配 shell 家族）——两个守卫共用同一份实现，避免「口径分裂」。
> - **T3 check_install_pins.py 扩面（安装命令面）**：扫描面从 workflow 扩到全仓 shell，判据与 Scorecard shell 面同源（pip 需 `--require-hashes`·npm 需 `npm ci`）；自证用例由 14 例升为 **20 例**（新增 shell 面 6 例：包含注释行与 echo 参数位不算命令的反例）。
> - **T4 check_action_refs.py 扩面（不可变引用面）**：Scorecard 的 uses 面只扫 workflow（从 YAML AST 解析 `uses:` 键），它的 shell 面只判安装命令——但 shell 里同样可能出现「静默替换」的外部下载（归档/tag clone/管道执行），属同类安全面，故一并管理；自证用例新增 N9-N14 六例（三个形态的正样本 + 三个反样本）。
> - **T5 CI 接入与阻断**：`security.yml` 的 dependency-pin job 新增 `check_action_refs.py` 步骤（该 workflow 无 paths 过滤·PR/push 全触发）；`workflow-lint.yml` 的 paths 扩到 `**/*.sh`（否则 shell 改动不会触发它）。两处均为无 `continue-on-error` 的 `run:` → 失败即阻断。
> - **T6 变异自证（判据真会红、非恒绿）**：在仓内临时放一个 `.sh` → `check_install_pins.py` rc=1（报出其中的 `npm install`）、`check_action_refs.py` rc=1（报出其中的归档下载）→ 两守卫在 shell 面均真会阻断。
> - **T7 覆盖缺口已闭合**：`check_external_rule_coverage.py` 的第③ 项由「已知缺口·WARN」变为「PASS 无覆盖缺口」。
> - **T8 自查口径必须与门禁实际口径一致**：自查时用 `ruff check --select C901,PLR`（ruff 默认阈值 C901=10/branches=12/statements=50）判定「超限」，而门禁实际用的是 `scripts/guardrails/ruff-structure.toml`（宽档 C901=15/branches=16/statements=80）⇒ **误报为阻断项**，差点为不存在的缺陷去改代码。⇒ 判「某门禁会不会拦我」必须跑该门禁的**真实入口**（`pwsh -File scripts/guardrails/check_changed.ps1`），不能拿等价规则名 + 默认阈值代替。
> - **状态**：已落地。
> - **文件**：见 file-index。

### W1196（2026-11-10）：外部规则覆盖面审计批（守卫扫描面宽于规则面 + 盲区监控守卫）

**本批要点**（外部规则覆盖面审计·读数来自 Scorecard 源码实读与沙箱变异自证）：

> - **T1 第三类复发面（本批根因）**：W1194→W1195 两批解决了「判定口径错误」与「新依赖树带漏洞」两类问题，但都依赖「人工发现规则要求」——第三类是「规则的覆盖面本身可能超出本仓守卫的扫描面」。
> - **T2 读 Scorecard 扫描 Pattern（不只读判定函数）**：`checks/raw/pinned_dependencies.go` 的三个扫描面为 `collectShellScriptInsecureDownloads` → `Pattern: "*"`（**全仓所有 shell 脚本**）、`collectDockerfile…` → `"*Dockerfile*"`、`collectGitHubWorkflow…` → `".github/workflows/*"`。即 shell 面不只是 workflow。
> - **T3 覆盖缺口实测（变异自证）**：本仓守卫为 workflow-only（`check_install_pins.py` / `check_action_refs.py`）。在 `scripts/` 下放一个含 `npm install somepkg@1.0.0` 与 `pip install somepkg==1.0.0` 的 `.sh` → 两个守卫均 **rc=0、无任何输出** ⇒ 确认是覆盖盲区。
> - **T4 实测暴露面内容**：Scorecard shell 扫描面内本仓共 5 个文件（`scripts/guardrails/check_changed.sh`、`scripts/install_hooks.sh`、`xiyouji-agent-web/deploy/pg/bin/{backup,initdb-bootstrap,restore-drill}.sh`）——实测均无安装类命令（唯一命中是 `echo` 字符串内的提示文本·非真实命令），即目前无真实漏洞；但面窄本身就是未来的盲区。
> - **T5 新增监控守卫**：`scripts/check_external_rule_coverage.py`（守卫「规则面 × 守卫面」差集：① shell 面内的安装命令、② 各生态清单的非官方 `resolved` 源、③ 守卫覆盖缺口），自证 8/8 通过，变异自证：放 shell 里未钉版安装命令 → rc=1报错；把 lock 的 `resolved` 改回第三方镜像 → rc=1报错；已接入 `security.yml` 的安装命令面守卫 job。覆盖缺口项目前以 **WARN 不阻断**（实测无真实漏洞），修法是扩守卫扫描面（另批）。
> - **T6 新生态面核对**：全仓依赖清单仅 4 个 npm lock 与 1 个 pip 清单；无 NuGet / Go / Ruby / PHP 生态文件（Scorecard 的 NuGet / Go 面在本仓不适用）；无多阶段 Dockerfile（1 条 FROM·已钉 digest）；无其他 CI 配置文件。
> - **状态**：已落地。
> - **文件**：见 file-index。

### W1195（2026-11-09）：Scorecard Pinned-Dependencies 真修批（pip 哈希化清单 + npm ci 化）

**本批要点**（Scorecard Pinned-Dependencies 真修·读数来自 Scorecard 源码与实测）：

> - **T1 前批方向性错误的实证（本批根因）**：W1194 把 Scorecard 的安装命令面判定为「未钉精确版本」并钉了 7 处；合并 PR #151 后重跑 Scorecard（run `42736414215`）实测：**该面 13 条 `PinnedDependenciesID` 告警一条未消**（总数 20 → 16，消的是 Dockerfile digest 与 TokenPermissions 那几条）。读 Scorecard 源码（`checks/raw/shell_download_validate.go`）后确认：**它要的是「钉 hash」而非「钉版本」**——pip 面命令含 `--require-hashes` → pinned（直接 `return false`），含其他参数 → unpinned（其中 `--hash=` 是 flag、被 `isFlag` 跳过 ⇒ 不作用）；npm 面只有命令含 `ci`（走 lockfile·ci 会校验 lock 内的 integrity hash）→ pinned。
> - **T2 pip 面真修（新建哈希化清单）**：新建 `scripts/requirements-hashed.txt`（51 项闭包：直接依赖 9 + 测试传递 8 + CI 工具包与传递 34），每包列出其「全部发布文件」的 sha256（含各平台 wheel + sdist）。闭包完整性实测：`pip install --require-hashes` 会拒绝未钉 hash 的**任何依赖包括传递依赖**，故用 pip resolver 验证合并后闭包可解（resolved 51 · 额外依赖 0）；传递依赖版本与直接依赖的冲突（packaging 26.0 vs 26.3）已按仓内现行版本取低者。
> - **T3 npm 面真修（全部改 npm ci）**：3 处 `npm install playwright@1.63.0 @playwright/test@1.63.0` 改为 `npm ci --prefix scripts`（scripts/package-lock.json 已钉 playwright 1.63.0 含 integrity），同时删除 `@playwright/test`（全仓仅 `tests/e2e/test_w266_e2e_extended.js` 引用它，而该文件按 `.github/workflows/README.md` 的 D-02 裁决明确排除出 CI 首波）；lhci 单独建 `scripts/lighthouse/{package.json,package-lock.json}`（348 包·resolved 全为 registry.npmjs.org），`npm ci` 实测 added 347 packages · lhci bin 可用。
> - **T4 删除 black 遗留安装（W400 起从未被执行）**：ci.yml 的 code-quality job 原本安装 black 仅为「遗留安装」（自 W400 起 `black --check` 步骤已移除，black 从未被执行）——本批删除该安装，同时把 ruff 的安装改为从哈希化清单统一安装（ruff 已在清单里·与 requirements.txt 版本一致）。
> - **T5 守卫升级为与 Scorecard 源码同源**：`scripts/check_install_pins.py` 的判据从「钉精确版本」改为「按 Scorecard 源码判定」（pip 需 `--require-hashes`·npm 需 `npm ci`），自证用例升级为 14 例（含「钉了版本但无 --require-hashes → 判红」与「钉了版本的 npm install 仍→ 判红」两个反例），自证 14/14 通过。
> - **T6 实测证据（不假收敛）**：干净 venv 实测 `pip install --require-hashes -r <小包哈希清单>` → rc 0（真实安装成功）；改掉一个 hash 后重跑 → pip 报 `THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE` → 伪 hash 被拒（判据真会红、非恒绿）。
> - **T7 首轮 CI 的 Dependency review 失败的漏洞处置（新建依赖树带来的 high 级漏洞）**：PR #152 首轮 CI 报 `basic-ftp@5.3.1` 漏洞（GHSA-c475-qrg2-pj4r·high·`Client.list()` 二次时间 DoS）——来自 lhci 子项目引入的 `express@4` 依赖链（`get-uri` → `basic-ftp@^5.0.2`）；advisory 的 vulnerable range 为 `<= 6.2.0`、`first_patched_version` 为 `6.2.1` ⇒ 用 npm `overrides` 把 `basic-ftp` 锁到 `6.2.6`（已超过修复版）；重生成 lock 后实测：`basic-ftp -> 6.2.6`、348 包不变、`resolved` 全为 `registry.npmjs.org`、无缺 `integrity`、`npm ci` rc 0（added 347 packages）且 `lhci` bin 可用。
> - **T8 坑表 E-216（新建依赖树带来新漏洞）**：新建依赖树后必须跑一次依赖审查；新漏洞的 advisory 可能还未入库（OSV 与 GitHub Advisory API 均查不到，仅 CI 审查实测输出报出）。
> - **T9 二轮·extract-zip 无修复版的漏洞通过升 lhci 解决**：二轮 CI 报出 `小 scripts/lighthouse/package-lock.json » extract-zip@2.0.1` 两条 high 级漏洞（GHSA-7pqw-9j4j-h8q3 与 GHSA-jmr9-qjv8-65gv，均为 `first_patched_version: None` ⇒ **最新版 2.0.1 仍落在漏洞区间**）。来源链：`lighthouse@11.4.0` → `puppeteer-core@21.x` → `@puppeteer/browsers@1.x/2.x` → `extract-zip@2.0.1`；而 `@puppeteer/browsers@3.x`（依赖改为 `modern-tar`）**不再拉 extract-zip**。解法：将 `@lhci/cli` 升到 `0.16.0`（其 `lighthouse 13.6.0` → `puppeteer-core 25.16.0` → `@puppeteer/browsers 3.2.6`），实测：新 lock 356 包、**extract-zip 已不再存在**、`basic-ftp` 仍锁 6.2.6、`resolved` 全为官方源、`npm ci` rc 0（added 337 packages）且 `lhci` bin 可用；配合需求：`@lhci/cli 0.16.0` 的 `engines` 要求 `node >= 22.19.0` ⇒ `perf.yml` 该 job 的 Node 由 20 升到 22（仓内 Node 22 已为主流，6 处）。
> - **T10 收官（面板复查最终读数）**：PR #152 三轮 CI 全绿 31/31（`mergeStateStatus=CLEAN`）→ 合并 `d44c1f4b` → 重跑 Scorecard（run `42753322885`）：**Code scanning open 16 → 3**（安装命令面 13 条 `PinnedDependenciesID` 全部消解）；**Dependabot open 43 → 41**（2 条 minimatch 真告警自动关闭·fixed 计数 26），剩余 41 条 Pillow 为未随清单变更重算的 stale 投影（告警内 `version_requirement` 仍为 `= 12.3.0`·而现行清单已钉 13.0.0）。剩余 3 条 Code scanning 为无文件关联的整体评级项（CII / CodeReview / Fuzzing）——其判定依据已逐条核实，属平台侧配置与外部登记项（非代码面缺陷）。
> - **状态**：已落地。
> - **文件**：见 file-index。

### W1194（2026-11-09）：Scorecard 告警真项收口批（安装命令钉版 + 权限最小化 + 镜像 digest 守卫）

**本批要点**（Scorecard 告警真项收口·读数来自 GitHub REST API 实查与本地实跑）：

> - **T1 告警逐条定位（Code scanning 20 条全部为 Scorecard 投影）**：`PinnedDependenciesID` 14 条 + `TokenPermissionsID` 2 条 + `CIIBestPracticesID`/`CodeReviewID`/`FuzzingID`/`VulnerabilitiesID` 各 1 条（后四条无文件关联·属组织级整体评级项）。前批只核了 `uses:` 面（90 个引用全钉 40-hex SHA）就判「陈旧投影」⇒ 核对面窄于 Scorecard 的告据面，漏判两类真实对象。
> - **T2 告警定位行逐条回读当前内容（行号漂移须人工对账）**：SARIF 行号是告警产生时的快照，多条已漂移至空行；回读后确认真实对象——`xiyouji-agent-web/Dockerfile:6` 的 `FROM node:22-alpine`（未钉 digest）、`screenshot-review.yml` 两处 `npm install playwright @playwright/test`、`ci-sim.yml` 的 `python -m pip install --upgrade pip`、`ci.yml` 两处 `pip install pip-audit` 与 `pip install … black mypy`、`perf.yml` 的 `npm install -g @lhci/cli@0.13.x`。
> - **T3 七处安装命令钉精确版本**：pip-audit==2.10.1（ci.yml + security.yml）、black==26.10.1 + mypy==2.4.1（ci.yml）、@lhci/cli@0.13.0（perf.yml·registry 实查 0.13.x 区间仅此一版⇒钉版语义等价）、playwright@1.63.0 + @playwright/test@1.63.0（screenshot-review.yml 两处·对齐 scripts/package-lock.json 的 W913 口径）、pip==26.3（ci-sim.yml·CI 全量固定 Python 3.12）。改后三面扫描：`uses:` 91 个 0 未钉、安装命令 13 条全部带版本。
> - **T4 钉版不改变 CI 判定行为（实查使用面后决策）**：`black` 在 CI 仅安装不执行（自 W400 起移除 `--check`）、`mypy` 为 `|| true` 的 report-only、`pip-audit` 为审计工具、`@lhci/cli` 的 0.13.x 区间唯一解 ⇒ 钉版零行为漂移，故不走上游升级路径。
> - **T5 两处写权限最小化**：release.yml 顶层 `contents: write` 收窄为顶层 `contents: read` + 仅 `release` job 持 `contents: write`（原先覆盖 preflight 与 build 两个不需要写权限的 job）；stale.yml 的 job 级 `contents: write` 为多余项（`actions/stale` 只需 `issues: write` + `pull-requests: write`）⇒ 直接删除。
> - **T6 镜像 digest 落成机器判据**：新增 `scripts/check_docker_pin.py`（仓内每条 `FROM` 必须写成 `image@sha256:<64 位十六进制>`，5 例负样本自证通过）；`security.yml` 新增 `docker-pin` job——首步用 `docker buildx imagetools inspect` 打印当前 tag 的期望 digest 供回填，步二跑严格判据。本机对 registry 全域不可达（registry/auth/mirror/index 均连接失败或 503·本机无 docker 可执行程序）⇒ 取值动作交由具出网能力的 CI runner 承担，判据不降级（回填前该 job 判红）。
> - **T7 Scorecard 四条整体评级项**：CII / CodeReview / Fuzzing / Vulnerabilities 属组织级指标，仓内基础件已具备（SECURITY.md、CODEOWNERS、CONTRIBUTING.md、fuzz.yml、dependency-review 与 codeql 双轨）；外部登记动作（CII 徽章与项目网站登记、OSS-Fuzz 集成、PR review 强制要求）登记在案，不在本仓代码面内。

> - **T8 二轮·digest 取值并回填（PR #151 首轮 CI 后）**：`docker buildx imagetools inspect` 在 PR 首轮 CI（run `42645364116`·job `129257068185`）上 **exit 255**、连 `EXPECTED_DIGEST` 都未打印 ⇒ 取值改走纯 HTTP registry API（curl 读 `Docker-Content-Digest` 响应头 + 三源回退 + 失败只警告不阻断）。最终取值 `sha256:0e1754758c2df4cfa3e68d59e2e1b7374bb7fd9ea6328eaaacf15cc934af8202`，**双证确认**：`dockerproxy.net` 与 `docker.1panel.live` 两个互相独立的代理各自返回的 manifest 响应体 SHA256 **逐字节一致**且与响应头相同，按该 digest 直取 manifest 200，官方镜像清单仓库 `docker-library/official-images` 确认 `22-alpine` 标签存在。回填 `xiyouji-agent-web/Dockerfile` 后 `check_docker_pin.py` 输出 `0 FAIL / 1 文件 / 1 条 FROM`。
> - **T9 二轮·npm audit job 500 根因真修（供应链面）**：同 run 的 job `129257068115` 报 `npm error 500 Internal Server Error - GET https://registry.npmmirror.com/omi/-/omi-7.7.13.tgz - [ER_NO_SUCH_TABLE]` ⇒ 表层是第三方镜像站数据库故障（外部故障），根因在本仓依赖解析层——`xiyouji-agent-web/package-lock.json` 里 26 条 `resolved` 指向该镜像站 ⇒ 安装取值被绑到别人站点。归一前逐条核对 26 个包的 lock `integrity` 与 npmjs 官方 `dist.integrity` **26/26 一致、0 mismatch**（同一 tarball·行为零变化），随后 26 条 `resolved` 全部归一为 `registry.npmjs.org`（host 分布 570+26 → 596）；`npm ci --dry-run` 通过、两侧 `npm audit --omit=dev` 均 `found 0 vulnerabilities`。同步把该口径落成机器判据：`scripts/check_install_pins.py` 扩供应链面（lock 的 `resolved` 只允许官方注册表，新增 4 例负样本自证 ⇒ 13/13 通过；沙箱内变异自证：改回镜像站即判红、原件不红）。
> - **状态**：已落地。
> - **文件**：见 file-index。

### W1193（2026-11-09）：Security and quality 面板残余收口批（minimatch 真修 + Pillow stale 源头 + Scorecard 投影复查）

**本批要点**（Security and quality 面板残余收口·读数来自 GitHub REST API 实查与本地实跑）：

> - **T1 面板基线（PR #150 合并后平台重算）**：Dependabot open 47 → 43（electron 1 条 + fast-uri 4 条 + qs 1 条随合并重算消除）；Code scanning open 20 条全部为 Scorecard 投影（PinnedDependenciesID 14 / TokenPermissionsID 2 / CIIBestPracticesID / CodeReviewID / VulnerabilitiesID / FuzzingID 各 1）——本地逐行核对 90 个 workflow `uses:` 引用**全部钉 40-hex SHA**、0 未钉 ⇒ 属新 SARIF 上传前的陈旧投影。
> - **T2 minimatch 2 条真告警真修（GHSA-g3hv-75wg-m249·moderate·vulnerable 7.0.0-11.0.0）**：依赖链实查 —— scripts 侧 eslint@10.11.0 → minimatch@10.2.6（eslint 最新 10.14.0 仍声明 `minimatch: ^10.2.6` ⇒ 升级 eslint 不解决）；desktop 侧 electron-builder@26.15.3 → app-builder-lib → minimatch@10.2.6，且 @electron/universal@2.0.3 → minimatch@9.0.9（electron-builder 26.18.0 仍带 @electron/universal@2.x ⇒ 升级 electron-builder 亦不解决）。修法：两处 package.json 各加**精确版本选择器** override `minimatch@>=9.0.0 <11.0.1` → `^11.0.5`——只覆盖落在 vulnerable 范围内的实例，glob@7 的 minimatch@3.1.5 与 filelist 的 5.1.9 保持原版本 ⇒ 不引入 glob 7 与 minimatch 11 的兼容风险。
> - **T3 实测（判据不降）**：两处 `npm ls minimatch` 显示受影响实例升到 11.0.5 且非受影响实例版本不变；两处 `npm audit` 均 0 vulnerabilities；scripts 侧 eslint 全量跑，override 前后诊断数**逐项相同**（20 problems = 10 errors + 10 warnings，全部为既有 no-undef 浏览器全局存量，CI 不跑 eslint）；desktop 侧 electron-builder 打包链路由 CI `Desktop Build` job 复验。
> - **T4 Pillow 41 条 stale 告警的源头处置**：告警 vulnerable_version_range 全为「< 13.0.0」及其子集，清单已钉 13.0.0（= advisory 的 first_patched_version），且告警 updated_at 停在 2026-10-24 ⇒ 未重算的 stale 投影。W1191 的纯注释变更未触发重算，本批改用**依赖名大小写归一**（PyPI 名大小写不敏感·安装与导入行为零变化）制造依赖行实质变更以触发重新解析；钉版与依赖面不变。
> - **T5 平台侧限制（沿用 W1191 登记）**：`secret_scanning_validity_checks` 在 public + 个人账户仓由平台判定为不可用（需 GitHub Advanced Security 订阅）；Scorecard 四项（CII / CodeReview / Vulnerabilities / Fuzzing）需新一轮 SARIF 上传后由平台消。
> - **状态**：已落地。
> - **文件**：见 file-index。

### W1192（2026-11-09）：CI 五处红灯清偿批（PR #150 存量缺陷全修）

**本批要点**（PR #150 五个失败 job 的根因全修·全部读数来自本地实跑 + GitHub REST API 实查）：

> - **T1 摸底（五处红灯全部定位到根）**：PR #150 的 required checks 已双绿（`Delivery Gate (verify_delivery.py)` 与 `Unit Tests (pytest)` 均 success），但 CI 仍暴露 5 处红灯：`CI-side simulation`（链接门禁 4 条 broken）、`Agent Web Build`（evals 校验 2 项 FAIL）、`CodeQL`（新增 1 条 high）、`Dark-state gate (merge shards)`（625 项 FAIL）、`E2E Interaction`（A1 失败）。五处均为本地 65 个未推送提交从未跑过 Actions 而暴露的**潜伏存量缺陷**，非平台侧故障。
> - **T2 暗色门禁 625 项恒红（断言域与采集面错配）**：基线 `scripts/output/render-state-audit-baseline.jsonl` 784 行混装两个采集面——charts 面 160 行（W579 建门禁时采）+ reader 面 621 行（W662 事后并入）+ 3 个已下线页；CI 只采 charts 面（当前磁盘 168 页），而 W1155 深度审计新增的「基线页缺失 / 采集面萎缩」断言遍历**全部**基线行 ⇒ reader 面 621 行与 3 个已下线页被恒判缺失。W662 段原文已定口径「gate compare 只遍历 charts scope 当前输出侧，reader 行不参与比对」，W1155 的新增断言未按该口径限定 ⇒ 属实现偏离设计意图。修法四项：① 新建 `scripts/_render_scope.js`（`listPages` / `chartsPages`）作采集面口径**单点来源**，采集端 `_audit_render_states.js` 与比对端 `check_dark_state_gate.js` 共用；② 缺失/萎缩断言只在「基线 ∩ 当前 charts 面」内成立（分片丢页与 upload 缺 `always()` 仍被拦）；③ **新增**「基线页磁盘已无且未登记 `RETIRED_PAGES` ⇒ FAIL」（防悄悄删页被 scope 限定放过）；④ reader 面遗留 621 行不参与比对但计数输出可见。基线不刷新（`--update-baseline` 会把 784 行砍到 168 行并抹掉 reader 面 ⇒ 属降判据·本批禁用）。本地实证：charts 面 168 页全采、基线同面 160 页 0 缺失、8 个新页 0 缺陷 ⇒ 门禁 OK；自测 9/9（原 5 例 + 新增同面缺页 / 采集面萎缩 / 已下线页未登记 / 已下线页已登记）。
> - **T3 CodeQL #120 真修（`py/incomplete-url-substring-sanitization`·high）**：`scripts/stat_event_probe.py:286` 的 `"goatcounter.com" in u` 是 URL 子串匹配——既会误判 `https://evil.example/?u=goatcounter.com`，也被 CodeQL 判为不完整 URL 净化。改为解析 URL 取 hostname 后按 DNS 标签**精确**比对（末两段标签等于 goatcounter 与 com），口径与 `scripts/fetch_gate_stats.py:117` 同款（同族单一实现）；`file:` 等非 http(s) 协议由 scheme 判定排除，原「file:// 下零远端上报」断言强度不减。7 例自测（真实域 / 子域 / file: / 查询串含词 / 伪后缀域 / 域后缀攻击）全通过，`--self-test` 输出 `SELF_TEST_OK`。
> - **T4 CHANGELOG 4 条断链**：W1181 段把正文（位于 `docs/` 下）的相对链接原样抄进仓库根的 CHANGELOG ⇒ `../03-主题与情节专题/…` 与 `../../source/…` 解析到仓库外。4 条改为根相对（`docs/03-主题与情节专题/…`、`source/引用与网络解读/…`）；`lint_links.py --dir .` 实跑 29321 链接 0 broken。
> - **T5 E2E 与 evals 两处**：① 页面自 W1169（`0582f327`）起监听 `pointerenter`，E2E 仍派发 `mouseenter` ⇒ A1 失败；改测试派发 `PointerEvent`（坐标来源与断言不变；A7 的 mouse 族派发因对应页面仍用 mouse 族而保持原样）；② evals dataset-039/041 指向 `dataset/dashboard.json`，该文件已于 W1157 删除 ⇒ 改指现存等价数据集（`dataset/century-dialogue.json` 顶层恰 2 组、`dataset/yuanqi-graph.json` 含 `meta`），`must_mention` 与真实结构相符、判据强度不减；`validate.mjs` 实跑 50/50 通过。
> - **T6 连带清偿（本批新增的体积窗红灯 + 归档工具根修）**：本批 CHANGELOG 段落盘后体积达 264907 B > 上限 262144 B（pytest `test_real_tree_within_size_budget` 判红），file-index 面同步超限（263023 B）⇒ 走 `archive_segments.py` 体积模式迁出 W1108-W1116 共 9 段（正本回落 236837 B / 244634 B·上限 262144 B·余量 25307 B / 17510 B）；迁移时暴露工具自身缺陷——`archive_segments.py` 的 `_a3_ok` 末尾块分支写作「正本**不**以末尾块结尾」，而 W1130 引入的 `split_tail_block` 明确把末尾文件级块留在正本末尾 ⇒ 该分支恒假、CHANGELOG 体积迁移必红。已根修为「以末尾块结尾」并补 3 条回归锁（末尾块留在正本末尾 / 前缀被改拦截 / 末尾块被搬走拦截），相关 29 条测试全通过。
> - **状态**：已落地。
> - **文件**：见 file-index。

### W1191（2026-11-09）：GitHub「Security and quality」全清批

**本批要点**（用户「把 GitHub 上面的 Security and quality 里面的所有问题一并解决」·全部读数来自 GitHub REST API 实查）：

> - **T1 摸底（三张面板）**：Dependabot 65 条（open 47 / fixed 18）、Code scanning 95 条（open 26 / fixed 17 / dismissed 52）、仓库安全配置 3 项缺口（Dependabot alerts 关、private vulnerability reporting 关、secret scanning validity checks 关）。
> - **T2 判定（多数告警实为「已修未推送」）**：open 26 条里 15 条 Scorecard `PinnedDependenciesID` + 2 条 `TokenPermissionsID` 在本地早已修复（全部 action 钉 40-hex SHA、release/stale 已加 `permissions`），症结是**本地 main 领先 origin/main 64 个提交、全部未推送** ⇒ 推送即消；Dependabot 37 条 Pillow/pillow 的 vulnerable range 全为 `< 13.0.0` 而清单已钉 13.0.0 ⇒ stale 告警，requirements.txt 留复核痕以触发重算。
> - **T3 真待办与处置**：① 6 条 `py/bad-tag-filter` 全在 `archive/scripts/batches/` 归档脚本，四条实证判为假阳性（该正则是「选取 `<script>` 块」而非剥标签；输入为本仓自产 HTML 且 861 页大小写敏感扫描 `<SCRIPT` 命中 0；输出非 HTML；归档位已被 ruff 与 CI 排除）⇒ 按仓内既有 28 条同族口径以 `won't fix` 关闭，open 26→20；② 仓库安全配置：Dependabot alerts 开启、private vulnerability reporting 开启（`PATCH` 返 404·改 `PUT` 成功）、secret scanning validity checks 平台侧对本 public + 个人账户仓不可用（记为已知限制）；③ Scorecard 4 项治理（CII / CodeReview / Fuzzing / Vulnerabilities：CODEOWNERS + README 徽章 + SECURITY.md 披露流程 + Jazzer/fast-check 双层 fuzz 与 CI）；④ 依赖版本对齐（electron 44.9.1、fast-uri 3.1.9、qs 6.17.1，npm audit 0 vulnerabilities）。
> - **T4 连带清偿存量 CI 红灯 7 条**（推 main 前必须全绿，否则 Unit Tests 必红）：AGENTS 正本体积 51273 B > 48KB 预算 ⇒ §4.2 五条槽摘要下放至 gates.md（51273→46702 B）；台账 61 数据行 > 窗口 60 ⇒ 归档 3 行至 58 行；glossary 新页未入可视化基线与朱砂实底面；`scripts/verify_delivery.py:1604` 的跨行高危正则；统计事件 `--check` 断言；三处口径数字漂移（速查 A5 35→42、文档规范 71→75 段、启动 Prompt 616/88/89→623/89/90）。
> - **T5 附带**：CodeQL action v3 → v4（GitHub 公告 2026-12 弃用·钉 `33d7b85da1a04171e211befe2c739303b9a4c066`·存在性实测通过）。
> - **状态**：已落地。
> - **文件**：见 file-index。


### W1190（2026-11-09）：CI 周级联网扫描根修批（Workflow Lint 每周 schedule 必红的两层根因）

**本批要点**（用户「检查一下 Workflow Lint 失败」·GitHub run #42605193188 实证·`unrecognized arguments: --ci`·退出码 2）：

> - **T1 失败本体**：schedule 触发的「Workflow YAML parseable」job 里，「Action refs 存在性扫描（联网·周级/手动）」一步失败；其前的 YAML 全量解析与 40-hex 形态判据均通过。**不阻塞 PR**（main 分支 required checks 仅 `Delivery Gate (verify_delivery.py)` 与 `Unit Tests (pytest)`），但周级门禁面每次必红并掩盖真实信号。
> - **T2 根因一（远端缺参）**：远端 `scripts/check_action_refs.py` 无 `--ci` 参数，而远端 workflow 已传 `--api --ci` ⇒ argparse 直接退出码 2。修复其实早在 W1155（本地 commit `5ebb587d`），但**本地 main 领先 origin/main 64 个提交、全部未推送** ⇒ 远端每周一 03:00 UTC 必然复现同一失败。
> - **T3 根因二（脚本与 workflow 矛盾·此前无人修）**：脚本入口对 `--api` **强制要求 token**，无 token 即退出码 2；而 workflow 注释明写「刻意不带 token：目标仓库均为 public，匿名读即可」⇒ **即便把 64 个提交全部推送，周级扫描仍是红的**（实测 `py -3 scripts/check_action_refs.py --api --ci` → 退出码 2）。这是典型「补丁加补丁」：只补参数缺失、没碰能力矛盾。
> - **T4 两侧同修**：① 脚本新增 `api_auth_decision()`——无 token 不再立即失败，改走匿名（实测匿名读 public 仓库 commit 返回 HTTP 200）；匿名限流归入「无法判定」，`--ci` 模式降级 WARN 不阻断，不带 `--ci` 仍 fail-closed。② workflow 联网步注入 `GH_TOKEN: ${{ github.token }}`（实测匿名配额 60 次/小时 < 本步最坏 84 次请求 ＝ 14 ref × 2 endpoint × 3 次重试；认证后 5000 次/小时）。
> - **T5 验证与负样本锁**：脚本自测 8/8 通过（新增 N7「无 token 判为可继续」+ N8「入口不早退」）；**变异自证 2/2**——mutant A「入口早退」被 N8 专属咬红、mutant B「认证判定拒绝」被 N7 专属咬红，证明两把锁都不是假锁；`check_changed.ps1` 四档全绿；全量 workflow YAML 12/12 可解析。
> - **状态**：已落地。
> - **文件**：见 file-index。


### W1189（2026-11-09）：集成连通：A5 文化背景系列 ↔ 角色/器物文档 双向补链

**本批要点**（用户「继续」· A2 人物深度分析经核查已饱和：216 篇且含女性主义理论子簇 W173/W224/W237/W240/W242，「A3 人物深化」作为新内容方向属假缺口；遂转做真实缺口「集成连通」· 用户的头号优先级）：

> - **T1 缺口定位**：刚收官的 A5 文化背景系列（W1180–W1187 七篇）全站 0 篇链向 216 篇角色文档，仅 3 篇角色文档反向链 A5；系列与角色库断联。
> - **T2 前向补链（A5→角色/器物）**：金公木母 / 八十一难与正果 / 天罡地煞 / 四大部洲 / 法器与兵器 五篇各加「关联角色 / 关联器物」块，指向实际论述到的角色与器物文档（孙悟空 · 猪八戒 · 沙僧 · 白龙马 · 唐僧 · 观音 · 菩提祖师 · 如来 · 铁扇公主 · 太上老君 · 金箍棒 · 芭蕉扇 · 紧箍）。
> - **T3 反向补链（角色/器物→A5）**：孙悟空 / 猪八戒 / 沙僧 / 白龙马 / 唐僧 / 观音 / 菩提祖师 / 铁扇公主 / 太上老君 九篇各加「关联文化背景」行，指回相关 A5 系列专题。
> - **T4 路径与纪律**：相对路径 A5→角色用 `../../02-人物深度分析/`、角色→A5 用 `../04-文化与历史背景/`；全部目标文件实存校验 0 broken；不新增篇数（A5 42 / A1-A6 623 不变），计数链与 dashboard KPI 不动；撞车核查规避 E-212 假缺口。
> - **状态**：已落地（本地提交·不推送）。
> - **文件**：见 file-index。

### W1188（2026-11-09）：读者路径验收与导航修复

**本批要点**（用户「继续」·真实读者路径验收·W1181–W1187 七批成果走查）：

> - **T1 验收动线**：按首页 → 看板 → 术语速查 → 深度解读 → 文档 → 返回 走查最近七批成果，发现四类断链。
> - **T2 断链一（入口缺失）**：术语速查页 `site/data/glossary.html` 全站仅被自身 / data 索引 / 搜索页 / sitemap 引用，首页与看板均不链它；而看板本身链了 52 个 data 页却独漏 glossary。修复：首页工具网格新增「术语速查」卡（与标签云 / 全文检索同簇），看板标签云横幅旁新增「术语速查」横幅。
> - **T3 断链二（返回路径）**：W1186 金公木母 / W1187 八十一难 两篇缺标准页脚（`> 双索引` / `> 导航`），读者落到这两篇无返回导读 / 首页 / 板块索引入口；其余五篇均有。修复：为两篇补标准页脚，与系列一致。
> - **T4 断链三（陈旧口径）**：glossary 深度解读区小标题仍写「W1180–W1182 系列」，实际已列七篇。修复：改为「W1180–W1187 系列，共七篇」。
> - **T5 口径漂移**：首页工具网格注记「两件常用工具」随新增卡失准，改为「常用工具」（去数词，规避硬计数漂移）。
> - **T6 验证**：新增链接目标均存在（data/glossary.html · site/index.html · docs/00-导读/阅读指南.md · 板块 README）；docs 全量链接校验 0 broken；本批不改篇数（A5 42 / A1-A6 623 不变），故计数链与 dashboard KPI 不动。
> - **状态**：已落地（本地提交·不推送）。
> - **文件**：见 file-index。

### W1187（2026-11-09）：A5 佛教术语专题（八十一难与正果）

**本批要点**（用户「继续」·按既定模式推进，术语表六组仅剩佛教术语组）：

> - **T1 选题锚定（避免重复）**：术语表第二组佛教术语 10 条参差（教义/目的论条目 + 袈裟/钵器物 + 心猿意马）。查 docs/04-文化与历史背景/ 无专题覆盖八十一难/正果/劫难（佛道思想.md / 西游与禅宗公案专题.md 仅零星提及 4/8 处，未系统化）；且「三三行满/九九数完」在 A5 零命中。据此取最可清点的**劫难—正果轴**（取经须历难方能成正果），并明确分层：袈裟/钵交 W1182、心猿意马交 W1186、四大部洲宇宙观交 W1184，本文不重做。
> - **T2 核心证据（难簿与九九归真）**：第 99 回难簿「蒙差揭谛皈依旨，谨记唐僧难数清：金蝉遭贬第一难，出胎几杀第二难，满月抛江第三难……」是**逐条编号、可勾销的灾难清单**；菩萨复核「佛门中九九归真，圣僧受过八十难，还少一难，不得完成此数」→ 补 1 难成 81。回目「九九数完魔刬尽三三行满道归根」同点九九/三三数術。本文取文本自陈的「八十难 + 补一难 = 八一」，不自行重数难簿长串（易错，以文本为准）。
> - **T3 正果授职（五圣成真）**：第 100 回如来授职，逐字引五封号——唐僧→旃檀功德佛、悟空→斗战胜佛、八戒→净坛使者、沙僧→金身罗汉、白龙马→八部天龙马；授职理由与沿途功过一一对应，使苦难可折算为功绩。
> - **T4 目的论框架**：劫难是机制（灾难被登记—勾销）、正果是目标（终点钉死且理由挂钩功过）、九九归真是数術外壳（佛圆满套道内炼数字，佛道混用又一例，呼应 W1186 诗赞「般若波罗到彼家」）、因果是底色（金蝉遭贬源于前世轻慢）。因果/轮回/五蕴/涅槃/禅定条目留白，不强行塞进一篇滑向教义概论。
> - **T5 引文与术语门禁**：8 条引文逐字核验（命中 100%）；其中回目句初稿误加逗号致子串不匹配，修正为无逗号连续串「九九数完魔刬尽三三行满道归根」；第 99 回难簿句初稿误加句号（原文此处为逗号接「寻亲报冤第四难」），去句号后通过。glossary 中「唐僧」为变体、规范词「玄奘」，首段介绍唐僧处自然补「（本名玄奘）」满足 C2；全量新违规 0。lint_links docs 5535 / site 23242 链接均 0 broken。
> - **T6 索引同步（不让系列断链）**：A5 README 系列段扩为 W1180–W1187（按行插入、实读复核，规避 W1184 表格断裂）；术语速查页深度解读区加「二、佛教术语」反向入口。改既有文件按 E-03 原子替换。
> - **T7 计数链**：A5 41→42、A1-A6 622→623；统计口径说明表格、dashboard 三处、docs_index 重建 INDEX（868 篇）、stats 标记面跟随 11 处一次同步到位。清单连续第八批零返工。**至此术语表六组全部覆盖**。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1186（2026-11-09）：A5 人物称谓专题（金公木母与心猿意马）

**本批要点**（用户「继续」·按既定模式推进，撞车核查后锚定术语表第一组）：

> - **T1 选题锚定（避免重复）**：术语表六组已覆盖三/四/五/六（道教术语/回目结构/地理名词/法宝兵器），剩一（人物称谓）、二（佛教术语）。查 docs/04-文化与历史背景/ 发现 明代隐喻.md 已存在，但其讲明代社会政治隐喻（弼马温与御马监、天庭九品、妖怪官僚），grep 金公/木母/黄婆/心猿/意马 全空——它只在「弼马温与御马监」把弼马温当官职讽刺，不碰丹经五行人物编码。故选定术语表第一组「人物称谓」的丹经隐喻层（心猿/意马/金公/木母/黄婆），与明代隐喻.md 同名不同层。
> - **T2 核心证据（四词同框）**：第 30 回「意马心猿都失散，金公木母尽凋零。黄婆伤损通分别，道义消疏怎得成！」把四个隐喻称谓并置同一诗赞，紧接叙事「却说那猪八戒，从离了沙……」——隐喻层与实写人物同场景互为注脚，证明这是绑定取经团队的稳定隐喻命名系统，非零散比喻。第 23/57 回另有木母+金公+黄婆同框佐证。
> - **T3 五词归属（文本同场景指代为据）**：心猿/金公→孙悟空（心性之猿 vs 金/铅之象，同一人物两层维度）、木母→猪八戒、黄婆→沙僧、意马→白龙马；以六条逐字引文（第 19/22/23/30/40/57 回）锚定，不使用外部注本的强行指派。
> - **T4 百回分布（可复算）**：text-search.json 逐回字面 count——心猿 12 回、木母 9 回、黄婆 6 回、金公 3 回、意马 3 回；读出三趋势：心猿最常用（收心主线）、金公意马密集前四十回后期隐退、木母黄婆长尾到六十五回。
> - **T5 学术衔接（引用存在·不作断言）**：学术论文索引收录 V04 西游证道书 / V05 西游真诠 / C03 刘一明西游原旨 / P04 张伯端悟真篇 / P01 王阳明传习录「心猿」，证明「人物=金公木母黄婆心猿意马」是明清内丹派读法；本文实证对象为百回正文如何用这套称谓，内丹精确对应仅引用其存在、不越界做教义引申。第 23 回诗赞末句「般若波罗到彼家」提示佛道术语混用，反对任一系统绝对化。
> - **T6 术语门禁新违规修复**：glossary 中「唐僧」为变体、规范词「玄奘」，门禁 C2 要求用变体须同现规范词；本文首段介绍唐僧处自然补「（本名玄奘，法号三藏）」——既是真信息也满足一致性，非堵判据。单文件 PASS、全量新违规 0。
> - **T7 引文与索引同步**：_cite_probe 实提并逐字校验 6 条（命中 100%）；lint_links docs 5519 / site 23241 链接均 0 broken。A5 README 系列段扩为 W1180–W1186（按行插入、实读复核，规避 W1184 表格断裂）；术语速查页深度解读区加「一、人物称谓」反向入口。
> - **T8 计数链**：A5 40→41、A1-A6 621→622；统计口径说明表格、dashboard 三处、docs_index 重建 INDEX（867 篇）、stats 标记面跟随 11 处一次同步到位。清单连续第七批零返工。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1185（2026-11-09）：A5 章回套语专题（且听下回分解）

**本批要点**（用户「继续」·按既定模式推进，但撞车核查推翻了上一轮推荐依据）：

> - **T1 选题收窄（避免重复）**：上一轮推荐写「回目对仗」，本批动笔前核查发现 [明代文学体裁与西游对照专题](docs/04-文化与历史背景/明代文学体裁与西游对照专题.md) 已有 3.3 节「回目对仗（骈文传统 vs 西游回目）」，全库「回目对仗」命中 27 次；3.2 节对照表也已列出「诗曰」「有诗为证」。**只看词形零命中、没看已有章节**是 E-212 的同型问题。据此把题目收窄为《且听下回分解：〈西游记〉章回套语的百回分布与程式》——那篇做体裁理论对照，本文做**可复算的频次与强制性**，层次不重叠。
> - **T2 数据实算**：以 `dataset/text-search.json` 的百回 `chapters[].text` 逐回做字面 `count`（不含 title / fullTitle），得六个套语分布：话说 59 次 / 44 回（首见第 11 回）、诗曰 82 / 47、有诗为证 55 / 38、且听下回分解 99 / 99、欲知后事如何 0 / 0、毕竟不知 83 / 83（术语表未登记）。
> - **T3 三个发现**：① 「且听下回分解」99 回各一次、唯一缺席第 100 回，与「毕竟不知…」构成两拍收束 ⇒ **分回首先是收束动作而非内容切分**；② 「话说」仅 44 回、第 1 回以「诗曰」开卷 ⇒ **起是可选项、收是强制项**；③ 术语表登记「欲知后事如何」而语料零命中，实际承担悬念功能的是「毕竟不知」+「且听下回分解」⇒ 继四大部洲专题「原文四洲 / 术语表三洲」之后第二处口径差异，如实标注、不代改写、不臆测来源。
> - **T4 方法论边界**：明确「话说」59 次里混有非程式对白（如第 11 回「看他有甚话说」），因此 44 回是**字面命中的上界**，不等于回首程式次数；零命中只针对本项目语料；学术索引未收章回套语专门研究 ⇒ 不作说书传统源流断言；与 3.1/3.2/3.3 的理论对照分层。
> - **T5 引文实提**：`_cite_probe.py` 从第 1 / 2 / 9 / 17 回实提并逐字校验 6 条引文（含第 1 回语料字面「毕竟不之」，逐字保留不代为改写），`check_citations.py --file` 命中率 100%；`lint_links.py --dir docs` 5506 链接 0 broken、`--dir site` 23240 链接 0 broken；元信息块 v2 与术语一致性一次通过。
> - **T6 索引同步（不让系列断链）**：A5 README 系列段扩为 W1180–W1185 并新增一行；术语速查页「深度解读」区加「四、回目结构」反向入口。**按行插入表格行并实读复核**，规避上一批「字符串替换导致 Markdown 表格断裂」的问题；改既有文件按坑表 E-03 用临时文件 + `os.replace` 原子替换。
> - **T7 计数链**：A5 39→40、A1-A6 620→621；`docs/00-导读/统计口径说明.md` 表格、`site/dashboard.html` 三处、`docs_index.py` 重建 INDEX（866 篇）、stats 标记面跟随 11 处一次同步到位。清单连续第六批零返工。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1184（2026-11-09）：A5 空间框架专题（四大部洲与三界）

**本批要点**（用户明确「继续在这个项目、不想换线」·按既定模式定题写作）：

> - **T1 选题与分工**：定题《四大部洲与三界：〈西游记〉空间框架的文本内证》。项目已有六张地理可视化页（journey-geo-semiotics / journey-geo-3d / journey-map-interactive / journey-route / journey-spacetime / customs-pass-route），处理的都是**水平路线**；A5 里具体地名散见各篇（女儿国 34 次、通天河 18 次、火焰山 10 次、取经路线 9 次），而「东土大唐」「地理考据」零命中 ⇒ 本专题补**垂直宇宙框架**。术语表「五、地理名词」组为入口，是 W1180–W1182 之后的系列续篇。
> - **T2 核心主张（文本内证）**：① 第 1 回「世界之间，遂分为四大部洲」把空间划分放在人物与情节之前，**空间框架先于叙事**；② 第 8 回如来评四洲「但那南赡部洲者，贪淫乐祸，多杀多争」把空间**伦理化**——取经的必要性来自洲的道德属性，而非路途远近；③ 前七回孙悟空逐一走遍地表、跨洲、海底龙宫、地下地府、天上天庭，构成一次**空间框架遍历仪式**，第八回才把叙事收回水平路线；④ 「器物管能做什么，空间管能在哪里做」——与 W1182 的器物克制链形成对照；⑤ 第 4 回「三十三座天宫」「七十二重宝殿」延续 W1180 归纳的数目趣味。
> - **T3 证据边界**：学术论文索引未收佛教宇宙观 / 四大部洲教义溯源专门条目 ⇒ 本文**只作文本内证、不作教义断言**；术语表只登记三洲而原文列四洲（含北俱芦洲），**口径差异如实标注、不代为补写、不臆测省略原因**。第七章明列四条方法论边界。
> - **T4 引文实提**：`_cite_probe.py` 从第 1 / 3 / 4 / 8 回实提并逐字校验 9 条引文（全部为 `text-search.json` 对应回目子串），`check_citations.py --file` 命中率 100%；`lint_links.py --dir docs` 5481 链接 0 broken、`--dir site` 23239 链接 0 broken；元信息块 v2 与术语一致性一次通过。
> - **T5 索引同步（不让系列断在续篇）**：A5 README 系列段扩为 W1180–W1184 并增 W1184 行；术语速查页「深度解读」区增另一条反向入口。改既有文件按坑表 E-03 原子替换；**替换后复核发现新表格行落在空行之后导致 Markdown 表格断裂**，按行重排修复（W1184 紧接 W1182 表格行、段前留空行）——又一处「字符串替换后必须实读结果」的实证。
> - **T6 计数链**：A5 38→39、A1-A6 619→620；`docs/00-导读/统计口径说明.md` 表格、`site/dashboard.html` 三处、`docs_index.py` 重建 INDEX（865 篇）、stats 标记面跟随 11 处一次同步到位。清单连续第四批零返工。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1183（2026-11-09）：A5 系列收口批（三篇登记板块索引 + 双向链接 + 图标路径根修）

**本批要点**（用户引用「推荐做一次系列收口」·不新增文档、不改篇数）：

> - **T1 板块索引登记**：`docs/04-文化与历史背景/README.md` 新增「近期专题系列（W1180–W1182）」段，按「术语 → 传播 → 器物」递进列表，逐篇标注对应术语表组别 / 主题与站点入口。此前 README 只有命名规范与双索引格式，三篇虽已入库却无板块级入口。
> - **T2 三篇互链补齐**：核查发现 W1182 已链 W1180/W1181，但 W1180 缺 W1181/W1182、W1181 缺 W1182 ⇒ 两篇各补一段「系列关联」并回指板块 README，三篇双向可达。
> - **T3 站点反向入口**：`site/data/glossary.html` 在引用格式块前新增「深度解读」区，按术语组别给出三条专题链接 + 板块索引链接；`site/data/cultural-misreading.html` 与 `site/data/deconstruction.html` 在 `</main>` 前各加一行「关联解读」指向译介专题。可视化页原本没有关联文档区，故采用最小侵入的单行补法，不新增结构块。
> - **T4 顺带发现并根修图标路径缺陷**：站点链接校验报 3 broken，全部为 `glossary.html` 的 `href="static/icons/..."`。根因是模板位于 `site/` 根、写裸 `"static/"`，而 `new_page.py` 固定输出到 `site/data/` 却不做路径重写 ⇒ 每个新页图标链接都会错。修法：`render_template` 增加 `text.replace('"static/', '"../static/')`（只匹配引号后紧跟 static，不误伤已有的 `../` 路径），并修正 glossary 存量三处；函数级验证生成页图标路径全部为 `../static/icons/...`、裸路径 0，站点 23238 链接 0 broken。这是 W1177 补模板四要素之后发现的同类脚手架缺陷。
> - **T5 两条纪律实证**：① 改既有文件全程按坑表 E-03 用「临时文件 + `os.replace`」原子替换，`git diff --numstat` 核对各文件均为纯插入（N 0）；② 幂等检查曾因用通用前缀 `<section class="sect…` 判「已存在」而误跳过 glossary 插入 ⇒ 改用独特锚点「按术语表组别延伸的 A5 背景专题」——**又一次检索假阳性**，与第 69 槽 / E-212 同族，说明判据必须用独特串而非类名前缀。
> - **T6 验证**：`lint_links --dir docs` 5445 链接 0 broken、`--dir site` 23238 链接 0 broken；Playwright 实测术语页 59 卡片 / 深度解读区存在 / 4 条 A5 链接 / JS 无报错；ruff 0 error；清单自测 7/7。计数链未变（A5 38 篇、A1-A6 619 篇）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1182（2026-11-09）：A5 文化专题第二篇（法器与兵器器物体系）

**本批要点**（用户再次指定「文化专题」·按既定模式直接定题写作，未做缺口检索）：

> - **T1 最小撞车核查后收窄题目**：A5 [明代服饰舆服制度对照专题](docs/04-文化与历史背景/明代服饰舆服制度对照专题.md) 3.3 节已系统处理「僧道服饰（袈裟法衣 vs 西游佛衣）」，锦襕袈裟在该篇命中 6 次 ⇒ 把题目从「取经三宝」收窄为**《法器与兵器：〈西游记〉的器物体系及其明代知识背景》**——那篇讲「穿什么」，本专题讲「拿什么、用什么」。术语表「六、法宝兵器」组 10 条为入口（W1180 补第三组、W1181 译介史之后的系列第三篇）。
> - **T2 核心主张（文本内证）**：按功能把 10 条器物分为随身兵器 / 禁制法器 / 容纳型法宝 / 功能型法宝四类；第 8 回「虽是一样三个，但只是用各不同」与第 88 回「一个使金箍铁棒…把我三个的兵器，比的通没有分毫」⇒ **器物是角色结构的物化**，不是装备清单；金刚琢「套取一切兵器法宝」是一件**让别的器物失效的反器物**，法宝之间存在克制链（金刚琢 > 兵器、芭蕉扇 > 火焰），体系是关系网而非清单。
> - **T3 形制纪律与数目边界**：借用坑表 E-07 / E-18（只写器物名会被图像误读成邻近形）——原著「两头金箍、中间乌铁」「九齿」「或粗或细能生灭」说明**描述器物必须给形制**；「一万三千五百斤」只作文本层的「可清点」处理，**索引未提供度量衡或术数专门条目，不推演其丹道/星象对应**，与 W1180 的数目趣味只作同族对照、不强行打通。
> - **T4 学界依据与引用纪律**：[学术论文索引·N06](source/引用与网络解读/学术论文索引.md) 阳达、肖慧《〈西游记〉的器物叙事与民俗文化》（明清小说研究 2025(1): 83-95）为同主题真实研究，索引只载书目与「器物叙事的民俗文化解读」关键观点 ⇒ 本文不转述其论证、不代替该论文；[·T06](source/引用与网络解读/学术论文索引.md) 何谷理插图本物质文化研究与 V01「出像」全名合读，支撑第六章的图文层。N06 条目注明系替换幻觉条目后经检索核验 ⇒ 第七章把「引用前确认条目已核验」写为纪律（与 E-212 同源）。
> - **T5 三层分置**：文本内证（形制/重量/功能/克制链）、学界已有方向（N06 民俗、T06 图文）、索引未载处留白（明代军器形制、度量衡、道教法器制度）——不以读者侧系统化解读取代作者本意，与 W1180/W1181 同一纪律。
> - **T6 引文实提**：`_cite_probe.py` 从第 8 / 19 / 22 / 35 / 59 / 60 / 88 回实提并逐字校验 9 条引文（全部为 `text-search.json` 对应回目子串），`check_citations.py --file` 命中率 100%；`lint_links.py --internal --dir docs` 5429 链接 0 broken；元信息块 v2 与术语一致性一次通过。
> - **T7 清单连续第二批零返工**：按 `new-doc` 清单顺序执行，计数链 A5 37→38、A1-A6 618→619 与三处无标记数字一次同步到位；`docs_index.py` 重建 INDEX（864 篇）；stats 标记面跟随 11 处。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1181（2026-11-09）：A5 文化专题（《西游记》的东传与译介）

**本批要点**（用户指定「文化专题」方向·按上一批建议不再做缺口检索）：

> - **T1 选题与分工**：定题《〈西游记〉的东传与译介：从江户和刻本到英文全译本》，属 A5 文化史。与 A4 三篇划清层次——[翻译学专题](docs/03-主题与情节专题/翻译学专题.md)（四理论家 + 四译本对比）、[接受美学专题](docs/03-主题与情节专题/接受美学专题.md)（四阶段接受史）、[取经传播学专题](docs/03-主题与情节专题/取经传播学专题.md)（理论框架 + 古今对位）均回答「意义如何被读」；本专题回答「**文本以什么物质形态、经由哪些书目、在什么年代到达**」——接受史讲意义，传播史讲载体。
> - **T2 证据纪律（全文硬约束）**：所有译本、年代、出版社、奖项、藏地、研究观点一律出自 [学术论文索引](source/引用与网络解读/学术论文索引.md) 的 T01–T11 / V01 / T05 / T06 / N02，**不补录索引外书目、不凭记忆补写译者生平或发行数据**；索引未载的流入年代、江户翻案细目、印数流通一律留白。第八章明列四条方法论边界，线索与结论分层标注。
> - **T3 核心主张（可复核）**：① V01 显示现存最早完整百回本分藏台北故宫与日本日光轮王寺、天理图书馆 ⇒ 「东传」在刻本实物层面早于近代译介；② 英译三形态（T03 节译 / T01 学术全译 / T02 全译）的差别不是译笔优劣，而是**译本形态本身是对「这本书是什么」的一次回答**；③ 法德俄全译本年代 1959 / 1991 / 2016 偏晚、T08 明载历时 17 年 ⇒ 经典地位不等于可译性，篇幅、宗教典故、文化专名构成三重门槛；④ T05「四大奇书」与国内「四大名著」是两套分类框架，海外汉学与国内大众并不共享同一预期；⑤ N02 以文体计量比较重译 ⇒ 译本已成为有独立文体特征的研究对象。
> - **T4 引文实提**：`_cite_probe.py` 从第 8 / 98 / 100 回实提并逐字校验 4 条引文（「我待要送上东土…」「永传东土」「五千零四十八卷，乃一藏之数」等），`check_citations.py --file` 命中率 100%；`lint_links.py --internal --dir docs` 5403 链接 0 broken；元信息块 v2 与术语一致性一次通过。
> - **T5 清单首次「零返工」**：按 W1179/W1180 两次实战修正后的 `new-doc` 清单顺序执行（`git add` 先于 `stats.py`、含 `check_frontmatter` / `docs_index` / dashboard KPI 同步），本批计数链 A5 36→37、A1-A6 617→618 与三处无标记数字一次同步到位，首轮提交无需第二轮修复。
> - **T6 计数链**：`docs/00-导读/统计口径说明.md` 分板块表格 A5 36→37（合计 618）；`site/dashboard.html` 的 A5 卡片与「A1-A6 共 N 篇」段落同步；`docs_index.py` 重建 docs/INDEX.md（863 篇）；stats 标记面跟随 11 处。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1180（2026-11-09）：A5 内容深化首批（天罡地煞与变化之术专题）

**本批要点**（用户「按现有文档缺口挑选一个」指令）：

> - **T1 缺口复算，排除六个假缺口**：先按篇幅判定《成书背景》（3476 字符）偏薄，读全文后发现七节结构完整、引文与学术索引齐备，属概览式分工而非缺口；再逐一核查内丹五行配属（A5 有 43954 字符《西游与道教全真派专题》）、域外译介（A4 有翻译学/接受美学/取经传播学三篇）、地理考据（A5 制度篇承接）、明代刻书业（34 次命中）、回目体制（3.1 专节）——**均已覆盖**。此轮避免重犯 E-212（检索给个数就下结论）。
> - **T2 唯一零覆盖主题**：`docs/00-导读/术语表.md` 第 51–52 行登记「天罡三十六变 / 地煞七十二变」，以 `docs/02`+`03`+`04` 共 462 篇内容文档为扫描面，**两个词形只出现在术语表本身，无任何解读**；W1176 上线的术语速查页展示该组却无背景文档可跳。据此新建 `docs/04-文化与历史背景/天罡地煞与变化之术专题.md`（14469 字符，A5 中位数 6835）。
> - **T3 引文实提（坑表 L219 硬约束）**：`_cite_probe.py` 从第 2 回实提「有一般天罡数，该三十六般变化，有一般地煞数，该七十二般变化」并获 16 条跨回目候选；再逐条校验为 `text-search.json` 对应回目 `text` 的**逐字子串**（10 条全部命中）。文档落 8 条规范引文，`check_citations.py --file` 命中率 100%，`lint_links.py --internal --dir docs` 5376 链接 0 broken。
> - **T4 术语一致性修正**：文档表格用变体称谓「唐僧」却未给 canonical，`check_glossary.py` 报新违规「玄奘」；按坑表 L219 补「唐僧即玄奘」的称谓口径说明后新违规归零。
> - **T5 内容主张（可复核）**：第 2 回「弟子愿多里捞摸」表明数目首先是性格描写而非术数设定；第 67 / 75 回由角色自陈能力边界（八戒不能变轻巧之物、孙悟空变人物只变头脸）⇒ **数目不是能力上限，而是身体类型的编码**；第 41 / 46 回「七十二条性命 / 七十二个头」属章回体数目趣味，**与清代内丹派评本的系统化解读分属文本层与接受层**，文中明确标注界限，不以评本反推作者本意。
> - **T6 清单实战检验并补第五类**：W1179 交付的四类清单在本批 `--task` 中未命中——「新增内容文档」不在覆盖面内。就地补 `new-doc` 类（引文实提 / 引文硬验证 / 链接 / 术语 / 计数链 / 目录 / 索引 / 双索引，每条带依据锚），自测 7/7；AGENTS §7 第 0 步同步改「五类」。
> - **T7 清单顺序修正（实证）**：`stats.py --w W1180` 首次报「无变更」、A5 仍 35 篇，根因是**统计按 Git 索引收集**；先 `git add` 后重跑才生效（A5 35→36、A1-A6 616→617、标记面跟随 11 处）。已把 `git add` 提前到 `stats.py` 之前（new-doc 与 stats-scope 两类），并写入「顺序硬约束」依据。
> - **T8 计数链**：`docs/00-导读/统计口径说明.md` 分板块表格 A5 由 34 订正为 36（100+44+215+209+36+13=617，与标题已自动跟随的 617 一致）；`stats.py` 已刷新 CHANGELOG 口径块与 11 处标记面。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1179（2026-11-09）：变更类型→必跑清单批（agent_start --task / --checklist）

**本批要点**（用户引用「把变更类型 → 必跑清单写进 agent_start.py」·W1176-W1178 三次同类缺口的收口）：

> - **T1 立项依据**：W1176 新增页返工四轮、W1177 把新增页清单化、W1178 新增槽又漏改 `EXPECTED_SECTION_NAMES`——三者是同一缺口的三种形态：**清单只存在于上一轮的记忆里，且随变更类型改变就失效**。
> - **T2 四类清单入 `agent_start.py`**：新增页 / 新增门禁槽 / 改共享 CSS / 改口径块。`--task` 按 `git status` 状态码与路径自动分类（`changed_entries()` 保留原 `changed_paths()` 接口）；每类列出可直接粘贴的命令与需人工判断的动作，多类命中时命令去重保序。
> - **T3 动手前可用**：新增 `--checklist <类型|all>`——工作树干净时也能在开工前查该跑什么；`--checklist-selftest` 断言四类命中、命令无省略号/占位符、批号口径分离。**清单最有用的时刻恰是动手前**，原 `--task` 依赖已有改动，覆盖不到这个时刻。
> - **T4 命令完整性**：批号取台账最新认领行、页名取改动路径，输出即可粘贴，无 `...` 或待填占位符。初版误把「台账下一自由号」当「本批号」，`stats.py --w` 会指向尚未开工的下一批（实跑抓出 W1180 vs W1179）⇒ 拆出 `current_batch_w()` 与 `next_batch_w()`，并把「清单不得出现下一自由号」写成自测守卫。
> - **T5 依据锚防漂移**：每条清单带坑表 E-NN / 门禁槽号 / W 批次依据（如新增槽引 E-98 五处接线并注明「恒跑段登记 `_SCOPE_CORE`、读页面非恒跑登记 `SCOPE_SITE_SECTIONS`，二选一」），可用 Grep 检索核对。
> - **T6 顺带核实与订正**：复核 E-98 第 3 处接线——第 69 槽登记在 `_SCOPE_CORE`（恒跑），与 `SCOPE_SITE_SECTIONS` 互斥，**不构成漏项**；但 `_SCOPE_CORE` 注释里的恒跑段计数仍为 19，已随批同步为 20。
> - **T7 文档链**：AGENTS §7 第 0 步补「W1179 必跑清单」用法；agent_start docstring 补 `--checklist` / `--checklist-selftest` 说明；`gather()` 与清单共用 `next_batch_w()` / `current_batch_w()` 单一实现，防两套批号口径漂移。
> - **验证**：自测 6/6（四类命中 + 干净工作树不误报 + 批号口径分离）· ruff 0 error · 三个入口实跑正常 · `--task` 对本批改动的分类命中 new-gate 与 stats-scope。按本批清单自身跑完收尾（第 31/41/42/45/46/51 槽与索引/CSP 重生成）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1178（2026-11-08）：检索假阳性判据化批（第 69 槽 · 模板结构契约）

**本批要点**（用户「先把检索假阳性变成机器判据」指令）：

> - **T1 两次同类实证**：W1177 `grep -c cite-block site/_template.html` 返回 7 就判「模板已有引用块」，实际 7 处全是 CSS 选择器、HTML 结构为 0 ⇒ 新页 citability C3 判红；W1175 只 grep `site/` 就断「`STATUS_TEXT` 无定义」，实为正本在 `scripts/w1167_badge_inject.py`，差点把错误结论写进方案。共同点：**检索给了个数就下结论，且结论不可复算**。
> - **T2 新增第 69 槽 `check_template_contract.py`**：C1 模板（及 `--target` 新页）必须含四项**完整标签串**——`<div class="cite-block">` / `<div id="dataSource">` / `<meta name="description"` / `<!-- chart-degrade:`，**类名 / CSS 选择器命中一律不算证据**；C2 `--evidence KEYWORD [--scope all]` 输出命中行号、行文本与形态（结构 / CSS / 注释 / 其他），命中全是非结构时显式告警。默认只约束模板（历史页有各自合规形态，全量套新契约会误伤存量），新页由 `--post --target` 单验。
> - **T3 机器化接入三处**：挂 `verify_delivery.py` 第 69 槽（`_StrictGate`·恒跑·毫秒级）；`new_page.py --post` 追加第 8 步「模板契约自检」；`--post` 的 `run_post` 现接收 `name` 以便 `--target`。
> - **T4 反例自测与实证**：自测 4/4（含「只有 CSS 类无结构」反例）；实测 `--evidence cite-block` 把 727 处命中拆为 637 CSS + 90 结构并给出行号；构造「只有 `.cite-block` CSS 类」的假页 → 判红（违规 4 · 退出码 1）。E-167 自指防护：扫描面不含 `scripts/`，自测样本在内存构造不落盘；另修跨盘符 `--target` 的 `os.path.relpath` 异常回退。
> - **T5 文档链**：`AGENTS.md` §4.2 第 69 条 + 槽数三处 68→69；`docs/agent/gates.md` 第 69 条（有序列表条目 + 文末详细定义）；`pitfalls.md` 新增 **E-212**（305→306 条·流程段 172→173）并同步 HANDOVER / puti-shouye skill 计数；`stats.py --w 1178` 刷新；第 41 槽三方编号 69/69/69、第 31 槽 0 FAIL。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1177（2026-11-08）：新增页上线自动化批（--post 一键全链路 + 模板补齐四要素）

**本批要点**（用户「做」指令·W1176 四轮返工的机制化沉淀）：

> - **T1 问题根因**：新增一个页面会牵连十余项门禁（徽标 / 导航 / SEO head / sitemap / 搜索索引 / CSP 哈希 / 统计口径 / 色盲基线 / citability 四字段 / 降级声明），逐个手跑必然漏——W1176 因此返工四轮。根因不是疏忽，是「新增页的连带面没有被清单化」。
> - **T2 `new_page.py --post`**：生成页面后按依赖序一键跑完七步（`--batch` 给出时追加统计刷新为第八步）：<br>改 HTML：数据源徽标 → 主导航 → SEO head；<br>读 HTML：sitemap → 搜索索引 → CSP 哈希（必须最后，哈希依赖上面全部改动）；<br>读全站：统计刷新（需批号）→ 色盲基线。<br>任一步非 0 即停（fail-fast）——继续跑只会叠加更难定位的错误；每步打印末行摘要便于定位。
> - **T3 模板补齐四要素**（新页从此天生齐全）：`<meta name="description">`（第 26 槽 R1）、`<!-- chart-degrade: n/a -->`（第 30 槽）、`<div id="dataSource">` 锚点（第 28 槽 C1/C2/C4 的扫描区，内部禁嵌套 div）、`<div class="cite-block">` **HTML 结构**（第 28 槽 C3）——此前模板只有 `.cite-block` 的 CSS 类而无对应结构，`grep -c cite-block` 会返回 7（全是样式选择器），是最容易误判「模板已经有了」的陷阱。
> - **T4 端到端实证**：生成临时探针页 `w1177-probe` 跑 `--post`，七步全过；随后门禁复核 **citability C1-C4 各 90/90**、SEO head 通过、数据徽标 90 页零违规、降级声明 90 页零违规、导航一致性 861 页零违规。清理探针页后重跑各派生物，sitemap 回 855 URLs、色盲基线回 18292 对、citability 回 89/89，工作树无残留。
> - **T5 使用方式**：`py -3 scripts/new_page.py --name foo --title "标题" --category "分类" --desc "描述" --post [--batch W1178]`。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1176（2026-11-08）：术语表可视化页（V2 首批·数据管道根修 + 新页落地）

**本批要点**（用户「开工」指令·V2 首批）：

> - **T1 数据管道根修（先修管道再建页）**：`scripts/check_glossary.py` 的 `parse_md` 原实现只取前 1-2 列——`variant` 类取「异名/指代」丢「出处说明」、`term` 类只取术语名丢「含义/书中用法」两列。源表 `docs/00-导读/术语表.md` 是三列结构，**近半信息在生成管道里蒸发**，直接拿 JSON 建页会得到一个只有词名的空壳。改为保留完整列（缺列给空串保持结构稳定），重新生成 `dataset/glossary.json`（6 组 59 条，C1 与源表逐条对拍零差异）。
> - **T2 新页 `site/data/glossary.html`**：KPI 四卡（6 组 / 59 条 / 10 异名映射 / 49 术语）+ 6 组筛选 tab + 防抖搜索 + 59 张术语卡片（人物称谓组展示「异名 → 正名」的内丹配属关系，其余组保留含义与书中用法）+ 完整对照表（与源表同构）。渲染实测：59 卡 / 59 行 / 7 tab / 计数正确、JS 无报错。
> - **T3 模板缺陷根修（影响所有未来新页）**：`site/_template.html` 的说明注释里写了 `<script>` 字面量，被 HTML 解析器当成真的脚本块开始标签 ⇒ 注释文字被当脚本执行、报语法错误（`Unexpected identifier 'EMBEDDED_DATA'`）。浏览器容错使其不致命，但第 8 槽内联脚本语法门禁必红。改为「script 标签」文字表述，模板与新页同修；修后全站 859 文件语法通过。
> - **T4 新增页的全链路要素补齐**：`w1167_badge_inject.py` 注入数据源徽标（snapshot/内嵌快照）、`w1167_nav_inject.py` 注入主导航（MARK 恰一次）、`<div id="dataSource">` 锚点满足第 28 槽 C1/C2/C4（citability 89/89）、`<!-- chart-degrade: n/a -->` 声明（第 30 槽）、`gen_sitemap.py` 补 sitemap、搜索索引重生成、CSP 全站重哈希（860 页 915 哈希零漂移）。
> - **T5 色盲基线**：新页内联 CSS 继承模板的深色适配映射规则（两处近色 `#d87c6e`/`#e17670` ΔE=0.3），按官方路径 `--generate-baseline` 重冻结：17448 → 18295 行（+847 = 新页配对，其余页零变化，符合「单调不增」语义），基线外违规归零。
> - **T6 V2 定位说明**：V2 原列的「西游地理 3D / 人物关系动态网络 / 八十一难难度热力图」三项**已全部存在**（2069 / 3156·2422 / 2276 行）。全站 89 个 data 页与 43 个数据集配对后，真正「有数据、无页面」的孤儿只有 `glossary` 一项——本批即把它落地，V2 的可视化侧至此清空。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1175（2026-11-08）：方案 §7 核验订正批（v5 批后清偿逐条复算）

**本批要点**（用户「先订正方案」指令）：

> - **T1 逐条按仓内证据复算 §7 批后清偿登记**：四个悬置条目逐个给出可复算命令与命中位置，不再留「待评估」。
> - **qa-1（失效）**：`site/data/night-sky.html` 不存在——`find site/ -iname "*night*" -o -iname "*star*" -o -iname "*sky*"` 只命中国标 svg 与一张背景图，无页面。设计链路的假设未落到实现，条目划掉并注明失效原因。
> - **qa-5（仍有效·真实缺口）**：`STATUS_TEXT["sample"]` 文案已定义于正本 `scripts/w1167_badge_inject.py`（「示例数据 · 仅演示」），但 `DEMO_SET = set()` 为空集、`classify()` 永不返回 `sample` ⇒ **徽标三态里的「演示」态从未在页面上出现过**。这不是失效条目而是功能缺口，已在方案里写明闭合路径（`DEMO_SET` 加一项 + 页内数据标 `sample`）。
> - **qa-6（形态不符·影响可忽略）**：全站（`site/` + `scripts/`）无任何自定义双击处理器；`d3.zoom` 仅 `journey-geo-semiotics` 中英两版使用，其双击缩放是 **d3 内置行为**；因无 document 级双击监听，`stopPropagation` 缺失无实际副作用。若不要双击缩放，正解是 `.on("dblclick.zoom", null)`。
> - **T2 核验纪律（本批自身教训）**：首版核验只 grep 了 `site/` 就判定 qa-5「`STATUS_TEXT` 无定义」，实为正本在 `scripts/w1167_badge_inject.py`——**核验范围必须覆盖 `scripts/` 与 `site/` 全域，grep 须排除 `.min.js`；结论写进方案前必须给出可复算命令与命中位置，不写「无任何定义」这类绝对表述除非全仓可验证**。该纪律已写入方案 §7 表下。
> - **T3 数据源条目结转**：§7 的「旧『数据源：』行话多种口径」标注为 **W1174 已清偿**（四种说法统一、括号内信息原样保留）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1174（2026-11-08）：移动端全量确认 + 数据源表述统一批（V1 收尾）

**本批要点**（用户「先跑全量，再继续 V1」指令）：

> - **T1 双视口全量普查（reader 不再抽样）**：`--scope all --reader-sample 1` 覆盖 859 页（根页 + data 89 + en 138 + reader 623 全量）。结果：**375px 859 页 FAIL 0 / 溢出 0**、**320px 859 页 FAIL 0 / 溢出 0**（各约 12 分钟）。这是 W1165 以来第一次真正意义上的全站移动端验证——此前 268 页口径中 reader 只抽样了 42 页（7%）。
> - **T2 数据源表述统一**：`site/data` 的 dataSource 容器里，「数据在页面内嵌」这一概念原有四种说法（页面内嵌 EMBEDDED 数据 53 / 嵌入版本 26 / 嵌入式数据 1 / 嵌入式版本 1）。统一为「页面内嵌 EMBEDDED 数据」共 **30 页 32 处**；**括号内容原样保留**——B 类括号是「如何加载最新数据」的操作指引、A 类括号是「生成脚本 + 快照日期」的溯源信息，两者信息不同，合并会丢信息。最终分布：102 处统一表述 + 38 处「实时加载自」（不同语义，保留）+ 5 处页面专属表述（保留）。
> - **T3 逐层收敛的实证**：首轮替换后抽查发现 `visual-art` 仍有「嵌入式版本」——映射表只写了「嵌入式数据」，漏了同族的「嵌入式版本」变体（分类时用 `'嵌入式数据' in text` 判断，把两者混为一谈）。补映射后单页重跑，残留归零。
> - **T4 报告升级**：两份探针报告由抽样版（268 页）替换为全量版（859 页），第 64 槽 B1/B3 采信口径同步受益。
> - **T5 连带**：改页面文案触发 CSP 3 页重哈希（文案在内联脚本模板里）+ 搜索索引重生成，均零漂移/零差异。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1173（2026-11-08）：移动端覆盖面与视口补齐批（探针扩面 data→all + 320px 采信）

**本批要点**（W1172 期间暴露的双盲区补齐·用户「继续 V1」指令）：

> - **T1 双盲区**：① **覆盖面**——探针原只扫 `site/data`，`site/en`（138 页）与 `site/reader`（623 页）从未被移动端检查；② **视口**——原只测 375px，320px（最窄主流宽度）未覆盖。W1165 起的所有「FAIL 归零」结论仅对 data 目录 + 375px 成立。
> - **T2 探针扩面**：`list_pages` 加 `scope`（data/en/reader/all）+ `reader_sample` 抽样，且修正递归遗漏——`site/reader` 下有 people/themes/essays/culture 四个子目录，只取直接子文件会漏掉八成页面。扩面后：data 98 → all 268 页（en 148 含根页、reader 抽样 42）。
> - **T3 button 触摸线**：W1165 那条移动端规则覆盖了 `select/input/label[for]` 却**漏了 button**——`en/relationships` 的「Redraw」实测 73×23px，差 1px 到 WCAG 2.5.8 的 24px 线。补 `button{min-height:24px}`：已够高的按钮（40/44px）原值保留，23px 这类仅 +1px 视觉无感。
> - **T4 第 64 槽加 B3**：采信 320px 报告（`mobile_viewport_report_320.json`）的 FAIL=0；缺失仅 NOTE（探针约 4 分钟不进 pre-commit）。连同既有 B1（375px）构成双视口判据。
> - **T5 验证**：双视口三目录普查——**375px 268 页 FAIL 0 / 溢出 0**、**320px 268 页 FAIL 0 / 溢出 0**；第 64 槽契约 7 项实跑 0 违规、自测 7/7。
> - **T6 说明**：本轮为抽样口径（reader 每 20 页取一），非全量；全量 623 页需约 20 分钟，留作批收尾可选动作。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1172（2026-11-08）：表格窄屏溢出根修批（V4 视口延伸·851 页传播）

**本批要点**（V4 视口延伸·用户「继续 V1」指令期间的实测发现）：

> - **T1 发现（探针覆盖面盲区暴露）**：既有移动端探针只扫 `site/data`（99 页），**从未覆盖 `site/en`（138 页）与 `site/reader`（623 页）**。本次扩展到三目录后实测：`reader/ch006` 在 **375px 下就溢出 274px**、320px 下 329px；`ch004` 94px；`en/monster-sociology` 54px。即 W1165「99 页 FAIL 84→0」的结论只对 data 目录成立，全站视角下 reader/en 的表格从未被检查过。
> - **T2 根因（统一且单一）**：reader 模板虽定义了 `.table-wrap`（带 `overflow:auto`），但正文表格是**裸 `<table>`**，未用该容器包裹；表格按内容撑开（实测 633px），直接把文档宽度顶破。en/data 多页同类。
> - **T3 修法（共享层一条规则）**：`system.css` 移动端块加 `table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}` —— 让表格自身成为横向滚动容器。三档实测：**375px 溢出 274→0**（表高 441 不变 ⇒ 内容未被压缩）、**768px/1280px 零变化**（断点 640 不触发）。
> - **T4 传播**：`inline_css --force` 重同步 851 页（reader 623 + en 138 + data 89 + 根页 3），单一事实源改动一次即全站生效。
> - **T5 验证**：375px 六页抽查（reader ch006/ch004 + en monster-sociology + data 三页）溢出**全部归零**；320px 下 reader 两页归零。
> - **T6 遗留（已开 W1173 追踪）**：320px 极窄屏另有 4 类**个别页硬编码宽度**残留（`en/monster-sociology` 表格内部 2599px、`data/character-dynamic-network` 的 `.stage-display`、`data/global-pattern` 的 `.pilgrim-card` 170px×2 列、`data/hardship-heatmap` 的 SVG 760px）——与 table 规则不同类，需逐页诊断，已后台跑 320px 全量拿完整清单。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

### W1171（2026-11-08）：坑表补强批（行尾形态补全 + 元教训 E-211）

**本批要点**（用户「先记坑」指令·W1170 三次提交失败的教训沉淀）：

> - **T1 先去重再入册**：按「入册前先 Grep 去重」纪律核验，W1170 三次失败对应的三条坑**全部已在表内**——目录刷新必须先 `git add` 再 `--refresh`（E-107）、git 中文路径必须取 `-z`（E-37）、写盘行尾漂移（E-11 的近亲）。因此**不新增三条重复条目**（会污染坑表、稀释检索），改为补强与提炼。
> - **T2 补强 E-11（第三种形态）**：原条目只覆盖「脚本显式把 `\n` 替换成 `\r\n`」；W1170 遇到的是**不显式替换也会污染**——Windows 下 Python `open(p,'w')` 文本模式默认产 CRLF（连续两批实证：W1169 的 CHANGELOG 968 处、W1170 的 23 个文件）。此形态更隐蔽：`git status` 干净、`git diff` 为空（`.gitattributes` 的 `eol=lf` 在入库层转换），但工作树字节与索引不一致，`batch_cascade` 读工作树直接 fail-closed「混合行尾」。补入三条修法：写文本永不省略 `newline='\n'` / 提交前 `git ls-files --eol | grep w/crlf` 自检为 0 / 归一用字节级写回而非文本模式重写。
> - **T3 新增 E-211（元教训）**：同批三次提交失败**全部命中已入册的坑**，且第 45 槽的 FAIL 消息里就明写着「先 git add 本批新件再重跑 refresh」。这不是知识缺口而是执行纪律缺口，故记为方法论条目：① 开批前按本次触碰面 grep 坑表（文件类型/目录/工具名）；② 门禁 FAIL 消息里的「修法=…」是已沉淀经验，先照做再想根因，不要先怀疑工具；③ 重复踩已入册的坑时补强原条目或记元教训，**不新增重复条目**。
> - **T4 计数链**：坑表 304→305 条、流程段 171→172，同步 AGENTS / HANDOVER / puti-shouye skill 四处。
> - **验证**：第 31 门禁 C5e 分项对拍 0 FAIL；坑表编号唯一性 0 FAIL；本批纯 md 治理面，走 `batch_cascade --light` 轻量通道（准入判据=触碰面 ⊆ md）。
> - **状态**：已落地（本地提交·不推送·Actions 额度归零用户令）。
> - **文件**：见 file-index。

# 更新日志


> **📖 阅读契约（W707）**：查表型——判断「当前版本/最近批次」时只读**顶段 1 个版本段**；查历史段用 grep（`grep -A 30 "### vX"`）；完整通读非预期用法（历史细节在 archive/docs/CHANGELOG-ARCHIVE*.md·grep 单段查勿打开通读）。
本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W1198），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **v/W 双键口径（W706）**：时间点查询以 W 号为准（单调键）；v 号在 W659-W667 合并段/并行批次区间不单调（v2.3.262〔W661〕列于 v2.3.261〔W666〕后）；v 号形态演化（阶段标签化·方案 D）经盘点 docs/superpowers/plans/2026-10-11-version-space-inventory.md 后另批实施。
>
> **方案 D 形态切换（W711 生效）**：自 W711 段起，CHANGELOG 段标题去 v 号（新形态 `### W###（日期）：标题`）；W001-W1000 段保留 `### vX.Y.Z（日期）：W###` 历史形态不改写；v 号降格为阶段标签（v2.3·无 patch）；CITATION.cff version 改批次号形态（"W###"·CFF free string）；file-index 历史条目保留 v 引用、新增条目 W only。
>
> **历史版本归档**：v0.1 - v2.3.17（W001-W1000）已迁移至 [archive/docs/CHANGELOG-ARCHIVE-tier2.md](archive/docs/CHANGELOG-ARCHIVE-tier2.md)（W513 二级归档）；W422 再归档 v2.3.18-v2.3.31（W400-W416）段；W511 归档 v2.3.32-v2.3.82（W417-W464）段 + v2.3.83（W484）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W681 归档 v2.3.84-v2.3.249（W485-W649）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W736 再归档 v2.3.250-v2.3.293（W650-W699）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)（源文件超 50KB/500 行阈值）。本文件正本按 110 段窗滚动（W960 窗口制·正本最老段随批推进·早期形态：W650-W710 段用历史 vX.Y.Z 形态·W711+ 段用批次键 W### 形态）。
>
> **全站页数口径**（W459 建·W702 实跑刷新·W1149 随批刷新，各门禁分母不同）：HTML 共 861<!--stats:html_total--> 页（site/data 90<!--stats:site_data_html--> + site/en 138<!--stats:site_en_html--> + site 根 10<!--stats:site_root_html--> + site/reader 623<!--stats:site_reader_html-->）；CSP 覆盖 860<!--stats:csp_covered--> 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 859<!--stats:scan_files--> 文件（再排除 `_shell.html`）；check_seo_head 扫 859<!--stats:seo_scanned--> 页（site 全树减两个模板壳）；inline_css 同步 852<!--stats:inline_css_pages--> 页（site 全树含 INLINED 标记页）；「可视化页 89<!--stats:visualization_pages-->」= site/data 90 减 `_shell.html`。
>
> **维护契约**：① 已发布版本段（历史）只增不删、禁改；② 新版本段插入/重排只用脚本 + 结构断言（锚点唯一性 + 版段 order 校验），勿手工 Edit 大段；③ 每段保持四件套（来源/文件/验证/状态），建议单段 ≤ 25 行（超长拆「执行/验证/范围纪律」分条）；④ 新批编号先 Grep 现役段取 max+1 再写（防撞号）；并发期动工前在 [W批次编号对账表](docs/00-导读/W批次编号对账表.md) 登记认领（W663 起·版段递延时以对账表为准）。
> - **T9 体积门禁脚注切片根修（CI 首红暴露·铁律 15）**：check_doc_size_budget._agents_face 的行切片在「脚注=文件末行且无换行尾」（AGENTS.md 恒为该形态）时 find(nl)=-1 使 t[fs:-1] 吞收尾家具星号 ⇒ 剥家具失败条目恒 +19 字误判（往批短 note 潜伏未触顶·W1137 note=119 首踩本地绿 CI 红）⇒ 末行无换行时取到文件尾 + batch_cascade agents_note 预检与门禁同源计量（口径对齐）· 单测 12 例全过。
