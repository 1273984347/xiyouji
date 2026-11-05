#!/usr/bin/env python3
"""人物关系数据溯源校验器（W1138 建·W1141 挂第 61 槽）。

判据：`dataset/character-relationship-3d.json` 的节点与边必须带齐
阵营、回目、规则编号、判定理由、证据级别、权重与争议标记；
边引用必须闭合，回目必须在 1-100，权重必须在 0-1。

用法：
    py -3 scripts/check_dataset_provenance.py          # 门禁模式（供 verify_delivery 第 61 槽调用）
    py -3 scripts/check_dataset_provenance.py --self-test

退出码：0=通过；1=有违例；2=基础设施缺失（文件不可读）。
汇总行恒为 `---- 第 61 门禁 数据集溯源：N FAIL ----`。
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "dataset" / "character-relationship-3d.json"
PAGE = ROOT / "site" / "data" / "character-relationship-3d.html"

META_REQUIRED = (
    "coding_version",
    "provenance_batch",
    "coder",
    "updated",
    "text_source",
    "coding_doc",
    "evidence_policy",
    "weight_method",
    "note",
)
NODE_REQUIRED = (
    "id",
    "name",
    "group",
    "faction",
    "importance",
    "desc",
    "evidence",
    "chapter_range",
    "source_chapters",
    "note",
)
LINK_REQUIRED = (
    "source",
    "target",
    "type",
    "relation",
    "rule",
    "chapters",
    "summary",
    "rationale",
    "evidence",
    "weight",
    "weight_basis",
    "disputed",
    "source_note",
)
FACTIONS = {"取经团", "天庭", "佛门", "妖界", "龙族"}
EVIDENCE = {"文本事实", "解读假设"}
RULES = {"E-01", "E-02", "E-03", "E-04", "E-05", "E-06", "E-07"}
WEIGHTS = {"W-1", "W-2", "W-3", "W-4"}


def _is_int_list(value):
    return isinstance(value, list) and value and all(isinstance(x, int) and not isinstance(x, bool) for x in value)


def _validate_meta(meta):
    errors = []
    for key in META_REQUIRED:
        if not meta.get(key):
            errors.append("meta 缺字段或为空：%s" % key)
    return errors


def _validate_nodes(nodes):
    errors = []
    node_ids = {n.get("id") for n in nodes}
    for n in nodes:
        for key in NODE_REQUIRED:
            if key not in n or n.get(key) in (None, "", []):
                errors.append("节点 %s 缺字段或为空：%s" % (n.get("id"), key))
        if n.get("faction") not in FACTIONS:
            errors.append("节点 %s 阵营非法：%r" % (n.get("id"), n.get("faction")))
        if n.get("evidence") not in EVIDENCE:
            errors.append("节点 %s 证据级别非法：%r" % (n.get("id"), n.get("evidence")))
        if not _is_int_list(n.get("source_chapters")):
            errors.append("节点 %s source_chapters 非非空整数列表" % n.get("id"))
        elif any(ch < 1 or ch > 100 for ch in n["source_chapters"]):
            errors.append("节点 %s source_chapters 越界（须 1-100）" % n.get("id"))
    return errors, node_ids


def _validate_links(links, node_ids):
    errors = []
    seen = set()
    for link in links:
        label = "%s→%s" % (link.get("source"), link.get("target"))
        for key in LINK_REQUIRED:
            if key not in link or link.get(key) in (None, "", []):
                errors.append("边 %s 缺字段或为空：%s" % (label, key))
        if link.get("source") not in node_ids or link.get("target") not in node_ids:
            errors.append("边 %s 引用不存在的节点" % label)
        if link.get("rule") not in RULES:
            errors.append("边 %s 规则编号非法：%r" % (label, link.get("rule")))
        if link.get("evidence") not in EVIDENCE:
            errors.append("边 %s 证据级别非法：%r" % (label, link.get("evidence")))
        if link.get("weight_basis") not in WEIGHTS:
            errors.append("边 %s 权重档位非法：%r" % (label, link.get("weight_basis")))
        w = link.get("weight")
        if not isinstance(w, (int, float)) or isinstance(w, bool) or not 0 <= w <= 1:
            errors.append("边 %s 权重越界：%r" % (label, w))
        if not _is_int_list(link.get("chapters")):
            errors.append("边 %s chapters 非非空整数列表" % label)
        elif any(ch < 1 or ch > 100 for ch in link["chapters"]):
            errors.append("边 %s chapters 越界（须 1-100）" % label)
        if link.get("relation") != link.get("type"):
            errors.append("边 %s relation 与 type 不一致" % label)
        if link.get("disputed") is True and len(str(link.get("rationale") or "")) < 8:
            errors.append("边 %s 标为争议但 rationale 过短" % label)
        key = (link.get("source"), link.get("target"), link.get("type"))
        if key in seen:
            errors.append("边 %s 重复（同 source/target/type）" % label)
        seen.add(key)
    return errors


def validate(data):
    nodes = data.get("nodes") or []
    links = data.get("links") or []
    errors = _validate_meta(data.get("meta") or {})
    node_errors, node_ids = _validate_nodes(nodes)
    errors.extend(node_errors)
    errors.extend(_validate_links(links, node_ids))
    if len(nodes) != 22:
        errors.append("节点数应为 22，实际 %d" % len(nodes))
    if len(links) != 32:
        errors.append("边数应为 32，实际 %d" % len(links))
    return errors


def page_sync_errors():
    errors = []
    try:
        page = PAGE.read_text(encoding="utf-8")
    except OSError as exc:
        return ["页面不可读：%s" % exc]
    if 'coding_version: "v0.1.0"' not in page:
        errors.append("页面 EMBEDDED_DATA 未同步 coding_version")
    if 'provenance_batch: "W1138"' not in page:
        errors.append("页面 EMBEDDED_DATA 未同步 provenance_batch")
    return errors


def self_test(data):
    cases = []

    bad = copy.deepcopy(data)
    bad["links"][0]["rationale"] = ""
    cases.append(("missing-rationale", bad))

    bad = copy.deepcopy(data)
    bad["links"][0]["chapters"] = [101]
    cases.append(("bad-chapter", bad))

    bad = copy.deepcopy(data)
    bad["links"][0]["weight"] = 1.5
    cases.append(("bad-weight", bad))

    bad = copy.deepcopy(data)
    bad["links"][0]["target"] = 999
    cases.append(("dangling-node", bad))

    bad = copy.deepcopy(data)
    bad["links"][1] = copy.deepcopy(bad["links"][0])
    cases.append(("duplicate-edge", bad))

    failures = []
    for name, sample in cases:
        if not validate(sample):
            failures.append(name)
    return failures


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("FAIL 数据不可读：%s" % exc)
        print("---- 第 61 门禁 数据集溯源：1 FAIL ----")
        return 2

    if args.self_test:
        failures = self_test(data)
        if failures:
            print("FAIL 自测未拦：%s" % "、".join(failures))
            return 1
        print("OK 自测 5 例全部按预期拦截")
        return 0

    errors = validate(data) + page_sync_errors()
    if errors:
        for err in errors:
            print("FAIL " + err)
        print("---- 第 61 门禁 数据集溯源：%d FAIL ----" % len(errors))
        return 1
    print("OK 数据集溯源校验：22 节点 / 32 边字段完整 · 引用闭合 · 回目与权重合法")
    print("---- 第 61 门禁 数据集溯源：0 FAIL ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
