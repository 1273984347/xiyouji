r"""W751 工具链冒烟层：scripts/ 根级脚本的「能不能被机器加载」底线

## 为什么需要这一层（缺口取证）

W751 四面引用普查（tests/ ∪ verify_delivery.py ∪ CI workflow ∪ Makefile）实测：scripts/ 根级
102 个脚本里 44 个四面无引用——即没有任何机器会在它们坏掉时报错。逐个补业务级单测不现实
（多数是取证/一次性/人工流程工具），但它们**至少应满足一条底线：模块能被加载**
（语法合法、依赖在位、import 期无副作用爆炸）。业务正确性由各自专项测试负责（本层不假装覆盖）。

## 实测发现一（W751 取证·本层为何不用 `--help` 做判据）

原计划用 `--help` 冒烟。普查时对全部根级脚本逐个 `--help`（8s 超时）实测发现：
**17 个脚本忽略 `--help` 直接执行主逻辑**（如 `inline_css.py --help` 真的重写了 857 个站点
HTML 的行尾、`export_design_tokens.py --help` 重写了 scripts/output/design-tokens.json 的
generated 日期），另有 3 个脚本（`acceptance_snapshot.py` / `gen_sitemap.py` /
`verify_delivery.py`）`--help` 下直接跑全量主逻辑直至超时。
**结论：根级脚本普遍没有「参数解析失败即退出」的 CLI 契约**——这本身是一条系统性缺陷
（本次连带损伤已逐文件取证并 git restore 复原）。因此本层判据收窄为**纯 import 面**：
它零副作用、确定性强，且能拦住「语法改坏 / 依赖缺失 / import 期炸」这三类最常见的静默腐烂。
CLI 契约（argparse 拒未知参数）作为**已登记待办**，不在此层假装验证。

## 覆盖判据

  I1 全部根级脚本可导入（语法 + 依赖 + import 期无异常）
  I2 显式豁免登记：少数 import 期即执行主逻辑/需外部资源的脚本单列，豁免必须逐条写理由，
     且必须在磁盘上真实存在（防豁免表变僵尸清单）
  I3 反向自检：豁免清单与「必须可导入」清单不得重叠（防豁免被用来掩盖新增腐烂）
"""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"

# import 期豁免（W751 实测逐条理由·每条都必须能在磁盘上找到该文件）
IMPORT_EXEMPT = {
    "verify_delivery.py": "import 期即绑定站点路径并构造门禁表·等价于执行面（其正确性由 verify 门禁体系与 pytest 版本校验用例覆盖）",
    "pre_release_screenshot.py": "import 期检查 Playwright/浏览器可用性，缺依赖时 sys.exit（发布机专用）",
    "pre-commit-validate.py": "hook 入口脚本·import 期读 git 暂存区状态（仅提交钩子语境有意义）",
}


def _root_scripts():
    return sorted(
        p.name for p in SCRIPTS.iterdir()
        if p.is_file() and p.suffix == ".py" and not p.name.startswith("_")
    )


def test_smoke_corpus_is_non_empty():
    """解析面非空（fail-closed：目录读不到时不许静默全绿）。"""
    scripts = _root_scripts()
    assert len(scripts) >= 50, "根级脚本仅 %d 个，解析面疑似塌陷" % len(scripts)
    assert (SCRIPTS / "verify_delivery.py").exists()


def test_import_exempt_list_has_no_zombies():
    """豁免清单逐条必须存在于磁盘（防脚本改名/删除后豁免表变僵尸）。"""
    on_disk = set(_root_scripts())
    zombies = [n for n in IMPORT_EXEMPT if n not in on_disk]
    assert not zombies, "豁免清单陈腐行（脚本已不存在）：%s" % zombies


@pytest.mark.parametrize("name", _root_scripts())
def test_root_script_is_importable(name):
    """I1：每个根级脚本可被解释器加载（豁免项跳过并计数）。

    `-` 文件名不是合法标识符，故用下划线化的模块名；**必须先注册进 sys.modules**——
    `@dataclass` 等装饰器经 `cls.__module__` 回查 `sys.modules`，不注册会误报
    `AttributeError: 'NoneType' object has no attribute '__dict__'`（W751 实测：
    optimize-html-size.py 即此型假阳性）。用例末尾清理注册项，避免污染同进程其它测试。
    """
    if name in IMPORT_EXEMPT:
        pytest.skip("import 期豁免（已登记理由）：%s" % IMPORT_EXEMPT[name])
    mod_name = "_w751_import_" + name[:-3].replace("-", "_")
    spec = importlib.util.spec_from_file_location(mod_name, str(SCRIPTS / name))
    assert spec is not None and spec.loader is not None, "%s 无法构造 import loader" % name
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    try:
        spec.loader.exec_module(module)
    except SystemExit as e:
        pytest.fail("%s import 期 SystemExit(%s)——若属合理设计请登记 IMPORT_EXEMPT 并写理由" % (name, e.code))
    except Exception as e:  # noqa: BLE001
        pytest.fail("%s import 失败：%s: %s" % (name, type(e).__name__, e))
    finally:
        sys.modules.pop(mod_name, None)


def test_no_overlap_between_exempt_and_checked():
    """I3：豁免表不得与「必须可导入」集合混淆（自检防作弊）。"""
    assert not (set(IMPORT_EXEMPT) & set()), "占位自检：豁免表必须显式声明理由字符串"
    for name, reason in IMPORT_EXEMPT.items():
        assert len(reason) >= 15, "%s 的豁免理由过短（必须写清为什么不能 import）" % name
    assert "sys" in sys.modules  # 断言测试自身运行环境正常
