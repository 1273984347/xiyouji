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
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "dataset" / "character-relationship-3d.json"
PAGE = ROOT / "site" / "data" / "character-relationship-3d.html"
EDGE_DATA = ROOT / "dataset" / "edge-wukong-tangseng.json"
EDGE_PAGE = ROOT / "site" / "data" / "wukong-tangseng-benchmark.html"
TEXT_SEARCH = ROOT / "dataset" / "text-search.json"

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
EDGE_META_REQUIRED = (
    "title",
    "coding_version",
    "provenance_batch",
    "coder",
    "updated",
    "text_source",
    "coding_doc",
    "quote_probe",
    "evidence_policy",
    "weight_method",
    "note",
)
EDGE_REQUIRED = (
    "source",
    "target",
    "source_name",
    "target_name",
    "relation",
    "rule",
    "weight",
    "weight_basis",
    "evidence",
    "disputed",
    "chapters",
    "source_note",
)
EVENT_REQUIRED = (
    "id",
    "chapter_start",
    "chapter_end",
    "chapters",
    "title",
    "type",
    "rule",
    "event_weight",
    "weight_basis",
    "summary",
    "rationale",
    "evidence",
    "disputed",
    "disputed_note",
)


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


def _validate_edge_meta(meta):
    return ["meta 缺字段或为空：%s" % key for key in EDGE_META_REQUIRED if not meta.get(key)]


def _validate_edge_core(edge, events):
    errors = []
    for key in EDGE_REQUIRED:
        if key not in edge or edge.get(key) in (None, "", []):
            errors.append("edge 缺字段或为空：%s" % key)
    if edge.get("rule") not in RULES:
        errors.append("edge 规则编号非法：%r" % edge.get("rule"))
    if edge.get("weight_basis") not in WEIGHTS:
        errors.append("edge 权重档位非法：%r" % edge.get("weight_basis"))
    if edge.get("evidence") not in EVIDENCE:
        errors.append("edge 证据级别非法：%r" % edge.get("evidence"))
    w = edge.get("weight")
    if not isinstance(w, (int, float)) or isinstance(w, bool) or not 0 <= w <= 1:
        errors.append("edge 权重越界：%r" % w)
    if not _is_int_list(edge.get("chapters")) or any(ch < 1 or ch > 100 for ch in edge["chapters"]):
        errors.append("edge chapters 非 1-100 整数列表")
    else:
        union = sorted({ch for event in events for ch in event.get("chapters", [])})
        if sorted(set(edge["chapters"])) != union:
            errors.append("edge chapters 与事件回目并集不一致")
    return errors


def _validate_quote_status(event, label):
    errors = []
    status = event.get("quote_status")
    if status not in ("verified", "not_probed"):
        errors.append("事件 %s quote_status 非 verified/not_probed：%r" % (label, status))
    elif status == "verified" and not (event.get("quotes") or []):
        errors.append("事件 %s quote_status=verified 但无引文" % label)
    elif status == "not_probed" and not str(event.get("quote_note") or "").strip():
        errors.append("事件 %s quote_status=not_probed 但缺 quote_note" % label)
    return errors


def _validate_edge_events(events):
    errors = []
    seen = set()
    for event in events:
        label = event.get("id")
        for key in EVENT_REQUIRED:
            if key not in event:
                errors.append("事件 %s 缺字段：%s" % (label, key))
        if label in seen:
            errors.append("事件 id 重复：%s" % label)
        seen.add(label)
        if not isinstance(event.get("event_weight"), (int, float)) or isinstance(event.get("event_weight"), bool) or not 0 <= event["event_weight"] <= 1:
            errors.append("事件 %s 权重越界" % label)
        if event.get("rule") not in RULES:
            errors.append("事件 %s 规则编号非法：%r" % (label, event.get("rule")))
        if event.get("weight_basis") not in WEIGHTS:
            errors.append("事件 %s 权重档位非法：%r" % (label, event.get("weight_basis")))
        if event.get("evidence") not in EVIDENCE:
            errors.append("事件 %s 证据级别非法：%r" % (label, event.get("evidence")))
        if event.get("disputed") is True and not str(event.get("disputed_note") or "").strip():
            errors.append("事件 %s 标为争议但缺 disputed_note" % label)
        errors.extend(_validate_quote_status(event, label))
        if not _is_int_list(event.get("chapters")) or any(not event["chapter_start"] <= ch <= event["chapter_end"] for ch in event["chapters"]):
            errors.append("事件 %s chapters 越界或不在区间内" % label)
        if not (isinstance(event.get("chapter_start"), int) and isinstance(event.get("chapter_end"), int) and 1 <= event["chapter_start"] <= event["chapter_end"] <= 100):
            errors.append("事件 %s 回目区间非法" % label)
        for quote in event.get("quotes", []):
            if not quote.get("text") or not quote.get("chapter"):
                errors.append("事件 %s 引文缺 text/chapter" % label)
            elif not event["chapter_start"] <= quote["chapter"] <= event["chapter_end"]:
                errors.append("事件 %s 引文回目不在事件区间内" % label)
    return errors


def _validate_edge_aggregate(aggregate, edge, events):
    errors = []
    weights = [event.get("event_weight") for event in events]
    if not weights:
        return ["events 为空，无法计算权重"]
    expected_max = max(weights)
    expected_mean = sum(weights) / len(weights)
    if aggregate.get("formula") != "max(event_weight)":
        errors.append("aggregate formula 非 max(event_weight)")
    if aggregate.get("edge_weight") != expected_max or edge.get("weight") != expected_max:
        errors.append("aggregate/edge weight 与 max(event_weight) 不一致")
    if aggregate.get("event_count") != len(events):
        errors.append("aggregate event_count 与 events 数不一致")
    if abs(float(aggregate.get("event_weight_sum", -1)) - sum(weights)) > 1e-9:
        errors.append("aggregate event_weight_sum 不一致")
    if abs(float(aggregate.get("event_weight_mean", -1)) - expected_mean) > 1e-9:
        errors.append("aggregate event_weight_mean 不一致")
    methods = {item.get("method") for item in aggregate.get("sensitivity", []) if isinstance(item, dict)}
    if not {"max", "mean", "count"}.issubset(methods):
        errors.append("aggregate sensitivity 缺 max/mean/count 对照")
    return errors


def validate_edge(data):
    edge = data.get("edge") or {}
    events = data.get("events") or []
    errors = _validate_edge_meta(data.get("meta") or {})
    errors.extend(_validate_edge_core(edge, events))
    errors.extend(_validate_edge_events(events))
    errors.extend(_validate_edge_aggregate(data.get("aggregate") or {}, edge, events))
    if len(events) != 9:
        errors.append("事件数应为 9，实际 %d" % len(events))
    if len(data.get("disputed_points") or []) < 3:
        errors.append("disputed_points 应至少 3 条")
    return errors


def quote_exactness_errors(data, search):
    """每一条直接引文去空白后，必须是对应回目原文的精确子串。"""
    errors = []
    chapters = search.get("chapters") or []
    if len(chapters) < 100:
        return ["原文索引章节数不足 100（实际 %d）" % len(chapters)]

    def norm(value):
        return re.sub(r"\s+", "", str(value or ""))

    for event in data.get("events") or []:
        for quote in event.get("quotes") or []:
            chapter = quote.get("chapter")
            text = norm(quote.get("text"))
            if not isinstance(chapter, int) or not 1 <= chapter <= 100:
                errors.append("事件 %s 引文回目非法：%r" % (event.get("id"), chapter))
                continue
            body = norm(chapters[chapter - 1].get("text"))
            if not text or text not in body:
                errors.append("事件 %s 第 %d 回引文非原文精确子串：%s" % (event.get("id"), chapter, quote.get("text")))
    return errors


def page_sync_errors():
    errors = []
    targets = (
        (PAGE, "3D 页面", "v0.1.0", "W1138"),
        (EDGE_PAGE, "标杆页面", "v0.1.0", "W1143"),
    )
    for path, label, coding, batch in targets:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append("%s 不可读：%s" % (label, exc))
            continue
        if ('coding_version: "%s"' % coding) not in text and ('"coding_version": "%s"' % coding) not in text:
            errors.append("%s EMBEDDED_DATA 未同步 coding_version" % label)
        if ('provenance_batch: "%s"' % batch) not in text and ('"provenance_batch": "%s"' % batch) not in text:
            errors.append("%s EMBEDDED_DATA 未同步 provenance_batch" % label)
    return errors


def self_test(data, edge=None, search=None):
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

    if edge is not None:
        edge_cases = []
        bad = copy.deepcopy(edge)
        bad["aggregate"]["edge_weight"] = 0.8
        edge_cases.append(("edge-bad-max", bad))

        bad = copy.deepcopy(edge)
        bad["events"][0]["quotes"][0]["chapter"] = 100
        edge_cases.append(("edge-quote-outside-range", bad))

        bad = copy.deepcopy(edge)
        bad["events"][1]["disputed_note"] = ""
        edge_cases.append(("edge-disputed-without-note", bad))

        bad = copy.deepcopy(edge)
        bad["events"][5]["quote_status"] = "verified"
        edge_cases.append(("edge-verified-without-quotes", bad))

        for name, sample in edge_cases:
            if not validate_edge(sample):
                failures.append(name)

    if edge is not None and search is not None:
        bad = copy.deepcopy(edge)
        bad["events"][0]["quotes"][0]["text"] = "这是伪造的引文"
        if not quote_exactness_errors(bad, search):
            failures.append("quote-not-exact")
    return failures


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
        edge = json.loads(EDGE_DATA.read_text(encoding="utf-8"))
        search = json.loads(TEXT_SEARCH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("FAIL 数据不可读：%s" % exc)
        print("---- 第 61 门禁 数据集溯源：1 FAIL ----")
        return 2

    if args.self_test:
        failures = self_test(data, edge, search)
        if failures:
            print("FAIL 自测未拦：%s" % "、".join(failures))
            return 1
        print("OK 自测 9 例全部按预期拦截")
        return 0

    errors = (
        ["关系网络：" + err for err in validate(data)]
        + ["标杆档案：" + err for err in validate_edge(edge)]
        + ["标杆档案引文：" + err for err in quote_exactness_errors(edge, search)]
        + page_sync_errors()
    )
    # W1155（深度审计 #15）：汇总句带引文状态分布——读者可直接区分「已核引文」与
    # 「not_probed 无引文事件」（原句仅报引文总数·状态分布只在 per-event 字段里）。
    _ev = edge.get("events") or []
    _verified = sum(1 for e in _ev if e.get("quote_status") == "verified")
    _notprobed = sum(1 for e in _ev if e.get("quote_status") == "not_probed")
    if errors:
        for err in errors:
            print("FAIL " + err)
        print("---- 第 61 门禁 数据集溯源：%d FAIL ----" % len(errors))
        return 1
    print("OK 数据集溯源校验：22 节点 / 32 边 + 9 组标杆事件 + 9 条引文精确"
          "（verified %d / not_probed %d 事件）· 引用闭合 · 回目与权重合法"
          % (_verified, _notprobed))
    print("---- 第 61 门禁 数据集溯源：0 FAIL ----")
    return 0


if __name__ == "__main__":
    sys.exit(main())
