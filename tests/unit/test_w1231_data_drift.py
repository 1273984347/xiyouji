r"""W1231 单元测试·数据漂移门禁 v4（面板配对）+ embed_json 行锚定根修回归锁。

## 背景（W1231 批·审计专批「单侧键 1702 条 schema 分歧清理」）

  - check_data_drift.js v4：根级配对前置（零重叠包壳找键集全等面板 / 数组↔对象找同形
    数组成员）+ 设计性单侧键族豁免（_schema/link_endpoint_schema/*_status）——
    配对形态差不再误计为分歧（1702→69·余量为 dataset 手维护摘录的设计性分歧）；
    配对暴露的真实值漂移 476 处同批以 V8 执行式替换修复（EMBEDDED 快照回归生成权威）。
  - embed_json.py：W102 系逐字符括号计数（含字符串感知中途版）在「洞察文案含引号/
    括号混排」页面上边界失步 ⇒ 17 页 replace 后脚本语法损坏（实测）。根修 = 行锚定
    成员定位（embed_json insert 的既定行格式）；本文件用含「字符串内括号 + 注释 +
    数组值面板」的刁钻夹具钉住行为。

运行：py -m pytest tests/unit/test_w1231_data_drift.py -v
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"

# ———————— check_data_drift.js v4 自测（8 例·含负样本）————————


def test_data_drift_self_test():
    r = subprocess.run(["node", str(SCRIPTS / "check_data_drift.js"), "--self-test"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=120, cwd=str(ROOT))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "8/8 通过" in r.stdout, r.stdout[-300:]


# ———————— embed_json 行锚定根修回归锁 ————————


PAGE_TMPL = """<!doctype html><meta charset="utf-8">
<script>
const EMBEDDED = {
    summary: {total: 3, note: "文案含 } 与 { 的字符串"},
    // 注释里也含 }{ 括号
    @KEY@: @INIT@
};
</script>
"""


def _write_page(tmp_path, key, init):
    p = tmp_path / "page.html"
    p.write_text(PAGE_TMPL.replace("@KEY@", key).replace("@INIT@", init), encoding="utf-8")
    return p


def _write_json(tmp_path, obj):
    p = tmp_path / "data.json"
    p.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    return p


def _run_embed(page, data, key, mode):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "embed_json.py"), "--html", str(page),
         "--json", str(data), "--key", key, "--mode", mode, "--no-backup"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)


def _page_valid_js(page):
    """页面内联脚本必须仍是合法 JS（node new Function 编译校验）。"""
    html = Path(page).read_text(encoding="utf-8")
    script = html.split("<script>")[1].split("</script>")[0]
    r = subprocess.run(["node", "-e", "new Function(process.argv[1]); console.log('OK')",
                        script], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=60)
    return r.returncode == 0 and "OK" in r.stdout, r.stdout + r.stderr


def test_embed_json_replace_object_with_braces_in_strings(tmp_path):
    """字符串值含 {} 的页面上 replace 对象面板：值正确 + 页面脚本语法仍合法。"""
    page = _write_page(tmp_path, "panel", '{"a": 1, "note": "含 }{ 的旧文案"}')
    data = _write_json(tmp_path, {"a": 2, "note": "含 }{ 的新文案"})
    r = _run_embed(page, data, "panel", "replace")
    assert r.returncode == 0, r.stdout + r.stderr
    html = Path(page).read_text(encoding="utf-8")
    assert "含 }{ 的新文案" in html
    ok, msg = _page_valid_js(page)
    assert ok, msg


def test_embed_json_replace_array_valued_panel(tmp_path):
    """数组值面板 replace（W1231 前报「未找到」·行锚定后可替换）。"""
    page = _write_page(tmp_path, "colors", '[{"name": "旧"}]')
    data = _write_json(tmp_path, [{"name": "新1"}, {"name": "新2"}])
    r = _run_embed(page, data, "colors", "replace")
    assert r.returncode == 0, r.stdout + r.stderr
    html = Path(page).read_text(encoding="utf-8")
    assert "新2" in html and "旧" not in html.split("colors:")[1].split("}")[0]
    ok, msg = _page_valid_js(page)
    assert ok, msg


def test_embed_json_insert_then_replace_roundtrip(tmp_path):
    """insert→replace 全链：插入的键可被再次替换（幂等重灌路径）。"""
    page = _write_page(tmp_path, "timeline", "[]")
    d1 = _write_json(tmp_path, [{"n": 1}])
    r1 = _run_embed(page, d1, "timeline", "replace")
    assert r1.returncode == 0, r1.stdout + r1.stderr
    d2 = _write_json(tmp_path, [{"n": 1}, {"n": 2}])
    r2 = _run_embed(page, d2, "timeline", "replace")
    assert r2.returncode == 0, r2.stdout + r2.stderr
    html = Path(page).read_text(encoding="utf-8")
    assert '"n": 2' in html.replace("{", "{").replace(" ", " ") or '"n":2' in html
    ok, msg = _page_valid_js(page)
    assert ok, msg


def test_embed_json_double_wrapped_value_form(tmp_path):
    """值形态 JSON（不带键包裹）replace：W1231 双包裹教训的回归锁。"""
    page = _write_page(tmp_path, "detail", '{"detail": {"x": 0}}')
    data = _write_json(tmp_path, {"x": 1})
    r = _run_embed(page, data, "detail", "replace")
    assert r.returncode == 0, r.stdout + r.stderr
    html = Path(page).read_text(encoding="utf-8")
    assert '"detail": {"detail"' not in html, "不得残留双包裹"
    ok, msg = _page_valid_js(page)
    assert ok, msg
