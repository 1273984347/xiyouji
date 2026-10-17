"""path_guard.py — W536 路径守卫公共模块（W761：14 处重复定义收敛为单实现）

背景（W536 安全加固）：根级工具脚本曾各自内联一份 `_w536_guard_open`——
open() 的路径受限包装，防止过程工具把仓库外路径当作读写目标。14 份拷贝在历史
演进中漂移出三种 root 表达式与两种根语义（仓库根 3 份 / scripts/ 目录 10 份，
其中 3 份无调用点=死定义；另 4 份 scripts/-scoped 根与其自身 site/ 写面相悖，
守卫生效即必炸、仅被调用点幂等跳过掩盖——登记为 P-01 待裁，本批只收敛重复、
不改写任何文件的既有语义）。

公共 API：
  PROJECT_ROOT   仓库根绝对路径（realpath）
  SCRIPTS_ROOT   scripts/ 目录绝对路径（realpath）
  make_guard(root)  生成 open() 的 root 受限版：realpath 解析后仅放行 root
                    自身及其子路径，逃逸 raise SystemExit；消息文本与历史
                    内联实现逐字一致（对账面·禁改写）。

迁移形态（二选一·零行为变化）：
  from utils.path_guard import make_guard, PROJECT_ROOT   # 原 root=仓库根
  _w536_guard_open = make_guard(PROJECT_ROOT)
  from utils.path_guard import make_guard, SCRIPTS_ROOT   # 原 root=scripts/
  _w536_guard_open = make_guard(SCRIPTS_ROOT)
scripts/rag/ 下文件需先 sys.path.insert(0, 上溯两级) 使 utils 包可见
（与 A-Z 分析脚本 `from utils.analyzer_base import ...` 同款形态）。
"""
import os

_UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.realpath(os.path.join(_UTILS_DIR, "..", ".."))
SCRIPTS_ROOT = os.path.realpath(os.path.join(_UTILS_DIR, ".."))


def make_guard(root):
    """生成 open() 的 root 受限包装（行为与 W536 历史内联实现一致）。

    root 传已 realpath 的绝对路径（推荐 PROJECT_ROOT / SCRIPTS_ROOT）。
    返回 guarded_open(path, *args, **kwargs)，调用形态与内置 open 兼容。
    """

    def guarded_open(path, *args, **kwargs):
        real = os.path.realpath(path)
        if not (real == root or real.startswith(root + os.sep)):
            raise SystemExit("W536 guard: path escapes project root: %s" % path)
        return open(real, *args, **kwargs)

    return guarded_open
