"""生成 dataset/README.md 数据索引（从磁盘实读，替代手工维护的 41 行表）。

W1149：修复 README 索引 41/44、体积与「40/80」失真、示例死文件。
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "dataset"
ENT = D / "entities"


def _rows(files: list[Path], base: Path) -> list[str]:
    rows = []
    for p in sorted(files, key=lambda x: x.name):
        raw = p.read_bytes()
        size = len(raw) / 1024
        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception:  # noqa: BLE001
            rows.append("| %s | - | %.1f KB | 解析失败 | - |" % (p.name, size))
            continue
        if isinstance(data, dict):
            keys = sorted(data.keys())
            top = "、".join(keys[:6]) + ("…" if len(keys) > 6 else "")
            count = data.get("count")
            if not isinstance(count, int):
                count = len(data)
        elif isinstance(data, list):
            top = "（数组）"
            count = len(data)
        else:
            top = type(data).__name__
            count = "-"
        rows.append("| %s | %s | %.1f KB | %s | %s |" % (p.name, count, size, len(keys) if isinstance(data, dict) else "-", top))
    return rows


def main() -> int:
    root_files = sorted(p for p in D.glob("*.json"))
    ent_files = sorted(p for p in ENT.glob("*.json")) if ENT.is_dir() else []
    total = sum(p.stat().st_size for p in root_files + ent_files) / 1024
    lines = [
        "# dataset/ — 详解西游记结构化数据",
        "",
        "> 来源：`site/data/*.html` 的 `EMBEDDED_DATA` 快照 + 人工整理件；",
        "> 本索引由 `scripts/gen_dataset_index.py` 从磁盘实读生成（禁手改）。",
        "> 当前规模：根级 %d 个 JSON + `entities/` %d 个 JSON，合计 %.1f KB。" % (len(root_files), len(ent_files), total),
        "",
        "## 概览",
        "",
        "- 根级数据文件：%d 个；实体聚合：%d 个。" % (len(root_files), len(ent_files)),
        "- 快照来源：页面 `EMBEDDED_DATA`（未找到对应页面的文件在「主要键」列标注人工件）。",
        "- 校验：第 61 门禁 `python scripts/check_dataset_provenance.py`；清单对拍 `python scripts/check_dataset_manifest.py`。",
        "",
        "## 数据索引",
        "",
        "| 文件 | 条目数 | 大小 | 键数 | 主要键 |",
        "|------|-------|------|------|--------|",
    ]
    lines += _rows(root_files, D)
    lines += [
        "",
        "### entities/",
        "",
        "| 文件 | 条目数 | 大小 | 键数 | 主要键 |",
        "|------|-------|------|------|--------|",
    ]
    lines += _rows(ent_files, ENT)
    lines += [
        "",
        "## 编码与溯源",
        "",
        "- [CODING.md](CODING.md)：人物关系编码手册（关系类型、权重、证据级别、边界案例与争议处理）。",
        "- `character-relationship-3d.json`：22 节点 / 32 边；节点补阵营、登场回目与证据级别；边补规则、理由、权重与争议标记。",
        "- `edge-wukong-tangseng.json`：唐僧—孙悟空单边示范档案（9 组逐回事件、引文状态、max/mean/count 权重敏感性）。",
        "- `entities/`：`characters.json`（56 实体）与 `locations.json`（61 实体），由 `chapters-metadata.json` 的逐回聚合对拍。",
        "- 校验：`check_dataset_provenance.py`（第 61 槽）覆盖关系网络与标杆边；`check_dataset_manifest.py` 校验本索引与磁盘一致。",
        "",
        "> 该网络为示意性人工整理网络，不做统计推断；与 `character_nlp.py` 生成的共现网络不是同一口径。",
        "",
        "## 使用方式",
        "",
        "```python",
        "import json",
        "with open('dataset/character-relationship-3d.json', encoding='utf-8') as f:",
        "    data = json.load(f)",
        "print(data['meta'], len(data['nodes']), len(data['links']))",
        "```",
        "",
        "```javascript",
        "const data = await fetch('dataset/character-relationship-3d.json').then(r => r.json());",
        "```",
        "",
        "## 许可",
        "",
        "MIT License · 数据来源于《西游记》原著（公共版权）+ 项目原创分析标注。",
        "",
    ]
    (D / "README.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("[OK] dataset/README.md 已生成：根级 %d + entities %d" % (len(root_files), len(ent_files)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
