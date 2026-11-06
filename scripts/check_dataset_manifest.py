"""第 63 门禁：dataset 清单与 schema 对拍（README ↔ 磁盘 / 量纲 / 端点 / 空值 / 废弃标记）。

README 由 `scripts/gen_dataset_index.py` 从磁盘生成；本门禁校验其与磁盘一致。


W1149 B2：README 41/44 与体积失真、权重两套量纲无语义、sankey 数字索引无声明、
chapter=0 哨兵、17 空数组 + 1 null 无「无/待补」语义。
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "dataset"
ENT = D / "entities"
MARKER = "---- 第 63 门禁 数据集清单："
ROW_RE = re.compile(r"^\| ([A-Za-z0-9._-]+\.json) \| ([^|]*) \| ([0-9.]+) KB \|")
WEIGHT_KEYS = {"weight", "edge_weight", "event_weight", "score"}
CHAPTER_KEYS = {"chapter", "回目", "chapter_start", "chapter_end"}


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def _count(data):
    if isinstance(data, dict):
        c = data.get("count")
        return c if isinstance(c, int) else len(data)
    if isinstance(data, list):
        return len(data)
    return "-"


def c1_readme(files: list[Path], readme: Path, base: Path) -> list[str]:
    if not readme.exists():
        return ["README.md 缺失"]
    rows = {}
    for ln in readme.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(ln)
        if m:
            rows[m.group(1)] = (m.group(2).strip(), float(m.group(3)))
    fails = []
    for p in files:
        if p.name not in rows:
            fails.append("README 缺文件行：%s" % os.path.relpath(p, base).replace(os.sep, "/"))
            continue
        actual_kb = p.stat().st_size / 1024
        claimed_kb = rows[p.name][1]
        if abs(actual_kb - claimed_kb) > max(0.2, actual_kb * 0.05):
            fails.append("README 大小失真：%s 标 %.1f KB 实 %.1f KB" % (p.name, claimed_kb, actual_kb))
        try:
            data = _load(p)
        except Exception as exc:  # noqa: BLE001
            fails.append("%s 解析失败：%s" % (p.name, exc))
            continue
        claimed = rows[p.name][0]
        actual = str(_count(data))
        if claimed not in ("-", actual):
            fails.append("README 条目数失真：%s 标 %s 实 %s" % (p.name, claimed, actual))
    extra = sorted(set(rows) - {p.name for p in files})
    if extra:
        fails.append("README 多出磁盘不存在的行：%s" % "、".join(extra))
    return fails


def _walk(obj, path, acc):
    if isinstance(obj, dict):
        acc.append((path, obj))
        for k, v in obj.items():
            _walk(v, path + "/" + str(k), acc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _walk(v, path + "[%d]" % i, acc)
    return acc


def _weights(obj):
    out = []
    for _p, d in _walk(obj, "", []):
        for k, v in d.items():
            if str(k).lower() in WEIGHT_KEYS and isinstance(v, (int, float)) and not isinstance(v, bool):
                out.append(float(v))
    return out


def c2_schema(files: list[Path], base: Path) -> list[str]:
    fails = []
    for p in files:
        try:
            data = _load(p)
        except Exception:
            continue
        rel = os.path.relpath(p, base).replace(os.sep, "/")
        weights = _weights(data)
        if weights:
            declared = (data.get("_schema") or {}).get("weight_scale") if isinstance(data, dict) else None
            mx = max(weights)
            expect = "0-1" if mx <= 1 else ("0-10" if mx <= 10 else ("0-100" if mx <= 100 else "超界"))
            if declared != expect:
                fails.append("%s weight_scale=%r 与实测上限 %s 不符（应 %s）" % (rel, declared, mx, expect))
        if isinstance(data, dict) and isinstance(data.get("sankey"), dict):
            sk = data["sankey"]
            nodes = sk.get("nodes") or []
            links = sk.get("links") or sk.get("edges") or []
            srcs = [e.get("source") for e in links if isinstance(e, dict)]
            if all(isinstance(x, int) for x in srcs) and srcs:
                if sk.get("link_endpoint_schema") != "index":
                    fails.append("%s sankey 数字端点未声明 link_endpoint_schema=index" % rel)
                if any(not (0 <= x < len(nodes)) for x in srcs):
                    fails.append("%s sankey 端点索引越界（nodes=%d）" % (rel, len(nodes)))
    return fails


def _chapter_errors(rel, path, d):
    fails = []
    for k, v in d.items():
        if str(k).lower() not in CHAPTER_KEYS:
            continue
        if v is None and not str(d.get("chapter_scope") or "").strip():
            fails.append("%s%s/%s=null 但缺 chapter_scope" % (rel, path, k))
        elif isinstance(v, int) and not isinstance(v, bool) and not 1 <= v <= 100:
            fails.append("%s%s/%s=%r 越界（须 1-100 或 null+scope）" % (rel, path, k, v))
    return fails


def c3_chapters(files: list[Path], base: Path) -> list[str]:
    fails = []
    for p in files:
        try:
            data = _load(p)
        except Exception:
            continue
        rel = os.path.relpath(p, base).replace(os.sep, "/")
        for path, d in _walk(data, "", []):
            fails += _chapter_errors(rel, path, d)
    return fails


def _empty_status(parent: dict, key: str, value) -> bool:
    if not (value == [] or (value is None and str(key).lower() not in CHAPTER_KEYS)):
        return True
    if str(parent.get(key + "_status") or "").strip():
        return True
    fs = parent.get("field_status")
    if isinstance(fs, dict) and str(fs.get(key) or "").strip():
        return True
    if str(key).lower() == "quotes" and str(parent.get("quote_status") or "").strip():
        return True
    return False


def c4_empty(files: list[Path], base: Path) -> list[str]:
    fails = []
    for p in files:
        try:
            data = _load(p)
        except Exception:
            continue
        rel = os.path.relpath(p, base).replace(os.sep, "/")
        for path, d in _walk(data, "", []):
            for k, v in d.items():
                if not _empty_status(d, str(k), v):
                    fails.append("%s%s/%s 为空/null 且无状态声明" % (rel, path, k))
    return fails


def c5_deprecated(files: list[Path], base: Path) -> list[str]:
    fails = []
    for p in files:
        try:
            data = _load(p)
        except Exception:
            continue
        if isinstance(data, dict) and data.get("deprecated") is True:
            if not str(data.get("deprecation_note") or "").strip():
                fails.append("%s deprecated=true 但缺 deprecation_note" % p.name)
            repl = data.get("replacement_page")
            if repl and not os.path.exists(os.path.join(base, repl)):
                fails.append("%s replacement_page 不存在：%s" % (p.name, repl))
    return fails


def scan(base: Path = ROOT) -> tuple[list[str], int]:
    data_dir = base / "dataset"
    if not data_dir.is_dir():
        return [], 0
    files = sorted(p for p in data_dir.glob("*.json"))
    ent = sorted((data_dir / "entities").glob("*.json")) if (data_dir / "entities").is_dir() else []
    all_files = files + ent
    if not all_files:
        return [], 0
    fails = []
    fails += c1_readme(all_files, data_dir / "README.md", base)
    fails += c2_schema(all_files, base)
    fails += c3_chapters(all_files, base)
    fails += c4_empty(all_files, base)
    fails += c5_deprecated(all_files, base)
    return fails, len(all_files)


def _self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        d = base / "dataset"
        d.mkdir(parents=True)
        good = {"_schema": {"weight_scale": "0-1"}, "items": [{"chapter": 1, "weight": 0.5}]}
        bad_ch = {"chapter": 0}
        bad_null = {"chapter": None}
        bad_w = {"_schema": {"weight_scale": "0-1"}, "items": [{"weight": 5}]}
        bad_empty = {"items": []}
        files = {
            "good.json": good, "bad_chapter.json": bad_ch, "bad_null.json": bad_null,
            "bad_weight.json": bad_w, "bad_empty.json": bad_empty,
        }
        for name, obj in files.items():
            (d / name).write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        rows = ["| 文件 | 条目数 | 大小 | 键数 | 主要键 |", "|------|-------|------|------|--------|"]
        (d / "unlisted.json").write_text("{}", encoding="utf-8")
        for name in files:
            p = d / name
            rows.append("| %s | %d | %.1f KB | 1 | x |" % (name, _count(_load(p)), p.stat().st_size / 1024))
        (d / "README.md").write_text("\n".join(rows), encoding="utf-8")
        # unlisted.json 故意不写 README 行
        fails, _n = scan(base)
        checks = [
            ("README 缺行", any("unlisted.json" in f for f in fails)),
            ("chapter=0", any("bad_chapter.json" in f and "越界" in f for f in fails)),
            ("null 缺 scope", any("bad_null.json" in f and "chapter_scope" in f for f in fails)),
            ("weight_scale", any("bad_weight.json" in f and "weight_scale" in f for f in fails)),
            ("空值无状态", any("bad_empty.json" in f for f in fails)),
            ("正向不误报", not any("good.json" in f for f in fails)),
        ]
        bad = 0
        for name, ok in checks:
            print(("OK  " if ok else "FAIL") + " " + name)
            bad += 0 if ok else 1
        print("self-test", "PASS" if bad == 0 else "FAIL")
        return 0 if bad == 0 else 1


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()
    fails, n = scan()
    if n == 0:
        print("FAIL 基础设施缺失：dataset 无 JSON（fail-closed）")
        print(MARKER + " 不可执行 ----")
        return 2
    for f in fails:
        print("FAIL " + f)
    print(MARKER + " %d FAIL（扫描 %d 文件） ----" % (len(fails), n))
    if "--report" in sys.argv:
        return 0
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
