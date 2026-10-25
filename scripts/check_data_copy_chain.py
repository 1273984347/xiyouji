#!/usr/bin/env python3
"""check_data_copy_chain.py — 数据副本链值级对账门禁（W920 建置·B-W855-04 清偿）。

背景（W855/T-09 实证）：json 副本链三层（生成器→scripts/output/data（gitignored 本地
产物）→site/data/json（入库·页面消费的生效真源）），47 个入库副本中 24 个与生成器产物
**值级漂移**且无任何防线三年。方向未定（入库副本被手工改 vs 生成器产物 stale）——
翻旧账需逐个比对页面消费方（另批定性），本门禁先防增量：

判据：
  C1 源目录在（本地态）：同名文件值级对账（JSON 解析后深度相等·非逐字节）——
     漂移集 == 基线冻结集 → OK；出现基线外新漂移 → FAIL；基线内恢复一致 → NOTE（可除名）
  C2 源目录缺（CI/干净检出态）：gitignored 产物不在 → NOTE「本地-only 面·不可判定」
     （fail-closed 例外登记：判据依赖未入库产物·与 W716 json_count 键移除同因）
  crash/解析失败按 FAIL（禁静默跳过）。

基线：scripts/output/data-copy-chain-baseline.json（首跑 --record 生成·存量漂移=登记态）。

用法：
    python scripts/check_data_copy_chain.py --gate
    python scripts/check_data_copy_chain.py --record   # 重建基线（存量漂移入册）
    python scripts/check_data_copy_chain.py --self-test
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "output" / "data"
DST = ROOT / "site" / "data" / "json"
BASELINE = ROOT / "scripts" / "output" / "data-copy-chain-baseline.json"


def _drift_set() -> tuple[set[str] | None, list[str]]:
    """返回 (漂移集|None=源缺, 错误清单)。"""
    if not SRC.is_dir():
        return None, []
    errs: list[str] = []
    drift: set[str] = set()
    for d in sorted(DST.glob("*.json")):
        s = SRC / d.name
        if not s.exists():
            continue
        try:
            a = json.loads(s.read_text(encoding="utf-8"))
            b = json.loads(d.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            errs.append("%s 解析失败（fail-closed）：%s" % (d.name, e))
            continue
        if a != b:
            drift.add(d.name)
    return drift, errs


def check(verbose: bool = True) -> int:
    fails: list[str] = []
    notes: list[str] = []
    drift, errs = _drift_set()
    fails.extend(errs)
    if drift is None:
        notes.append("C2: scripts/output/data 不在（CI 态·gitignored 本地产物）——本地-only 面·不可判定（W716 同因登记）")
    else:
        base: set[str] = set()
        if BASELINE.exists():
            try:
                base = set(json.loads(BASELINE.read_text(encoding="utf-8")).get("drift", []))
            except (OSError, json.JSONDecodeError):
                fails.append("基线文件损坏（fail-closed）——重跑 --record 重建")
        new = drift - base
        healed = base - drift
        if new:
            fails.append("C1: 基线外新漂移 %d 件：%s（分发副本或重建基线并登记原因）" % (len(new), "、".join(sorted(new)[:8])))
        if healed:
            notes.append("C1: 基线内 %d 件已恢复一致（可 --record 除名）：%s" % (len(healed), "、".join(sorted(healed)[:5])))
    if verbose:
        for f in fails:
            print("FAIL ", f)
        for n in notes:
            print("NOTE ", n)
        print("---- 数据副本链值级对账：%d FAIL / %d NOTE ----" % (len(fails), len(notes)))
    return 1 if fails else 0


def record() -> int:
    drift, errs = _drift_set()
    if drift is None:
        print("[ERROR] 源目录不在，无法建基线")
        return 1
    if errs:
        for e in errs:
            print("FAIL ", e)
        return 1
    BASELINE.write_text(json.dumps({"drift": sorted(drift), "recorded_by": "W920",
                                    "note": "存量漂移登记态（方向定性另批）·新漂移判红"}, ensure_ascii=False, indent=1),
                       encoding="utf-8")
    print("[OK] 基线重建：登记存量漂移 %d 件" % len(drift))
    return 0


def self_test() -> int:
    import tempfile
    cases = []
    with tempfile.TemporaryDirectory() as td:
        global SRC, DST, BASELINE
        old = (SRC, DST, BASELINE)
        try:
            SRC = Path(td) / "src"
            DST = Path(td) / "dst"
            SRC.mkdir()
            DST.mkdir()
            (SRC / "a.json").write_text('{"v": 1}', encoding="utf-8")
            (DST / "a.json").write_text('{"v": 1}', encoding="utf-8")
            (SRC / "b.json").write_text('{"v": 1}', encoding="utf-8")
            (DST / "b.json").write_text('{"v": 2}', encoding="utf-8")
            BASELINE = Path(td) / "base.json"
            cases.append(("T1 无基线时有漂移必红", check(verbose=False) == 1))
            record()
            cases.append(("T2 漂移入基线后放行", check(verbose=False) == 0))
            (DST / "c.json").write_text('{"v": 9}', encoding="utf-8")
            (SRC / "c.json").write_text('{"v": 1}', encoding="utf-8")
            cases.append(("T3 基线外新漂移必红", check(verbose=False) == 1))
            (DST / "b.json").write_text('{"v": 1}', encoding="utf-8")
            record()  # T3 的 c 漂移入基线后再测恢复
            cases.append(("T4 恢复一致不红（NOTE）", check(verbose=False) == 0))
            SRC = Path(td) / "nothere"
            cases.append(("T5 源缺 CI 态 NOTE 放行", check(verbose=False) == 0))
        finally:
            SRC, DST, BASELINE = old
    bad = [n for n, ok in cases if not ok]
    for n, ok in cases:
        print("%s  %s" % ("PASS" if ok else "FAIL", n))
    print("---- 数据副本链门禁 self-test：%d/%d ----" % (len(cases) - len(bad), len(cases)))
    return 1 if bad else 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    if "--record" in sys.argv:
        return record()
    return check()


if __name__ == "__main__":
    sys.exit(main())
