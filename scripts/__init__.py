"""《详解西游记》分析脚本包（W424 S1 打包：regular package）。

脚本仍可直接 `python scripts/xxx.py` 运行；本文件使 scripts/ 可作为
常规包被 import（`import scripts.utils` 等），并配合各脚本顶部的
`sys.path.insert(0, str(Path(__file__).parent.parent))` 引导，消除 cwd 依赖。
"""
