r"""W1330 专项测试：看板交互二期（搜索深链 / 最近浏览 / 回到顶部 / 键盘聚焦）

## 为什么测

四项功能的共同失效形态是「页面看起来正常，但记忆/深链某天静默断掉」：
- recent.js 若从 90 个内容页漏注入 ⇒ 看板永远空条，无报错；
- 看板若误加载 recent.js ⇒ 看板自己会被写进最近浏览；
- #q= / syncHash 若被后续改造覆盖 ⇒ 搜索分享/回退失效；
- 回到顶部按钮若被删 ⇒ 长页无回顶入口。
本文件把「引用面守恒 + 交互 token 在位 + 注入幂等」钉成可回归判据。

## 覆盖判据

  G1 90 个 site/data 内容页各引用 recent.js 恰一次，看板不引用
  G2 recent.js 契约（键名 / 上限 5 / localStorage 读写）
  G3 看板交互 token（recent/back-top/#q= 解析/键盘 /）
  G4 注入器幂等：insert 后重放零变化；缺 </body> 时 fail-closed
  G5 CLI --check 在真实仓库 PASS
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import w1330_recent_inject  # noqa: E402
from w1330_recent_inject import MARK, TAG, process  # noqa: E402

SCRIPT = SCRIPTS / "w1330_recent_inject.py"


def test_all_data_pages_reference_once():
    for f in w1330_recent_inject._pages():
        txt = f.read_text(encoding="utf-8")
        assert txt.count("recent.js") == 1, f.name


def test_dashboard_does_not_load_recent_js():
    dash = w1330_recent_inject.DASH.read_text(encoding="utf-8")
    assert "recent.js" not in dash


def test_dashboard_interaction_tokens():
    dash = w1330_recent_inject.DASH.read_text(encoding="utf-8")
    for token in (
        "xy-recent-pages", "initRecent", "initBackTop", "backTop",
        "readHashState", "applyHashState", "syncHash(activeCategory",
        "e.key !== '/'",
    ):
        assert token in dash, token


def test_recent_js_contract():
    js = w1330_recent_inject.JS.read_text(encoding="utf-8")
    assert "xy-recent-pages" in js
    assert "MAX = 5" in js
    assert "localStorage" in js


HTML = "<html><body><p>x</p></body></html>"


def test_process_insert_and_idempotent():
    new, action = process(HTML)
    assert action == "insert"
    assert MARK in new and TAG in new
    again, action2 = process(new)
    assert action2 == "update"
    assert again == new
    assert action2 == "update" and again == new


def test_process_fail_closed_without_body():
    out, action = process("<html><p>x</p></html>")
    assert action == "no-body" and out == "<html><p>x</p></html>"


def test_cli_check_pass():
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    assert r.returncode == 0, (r.stdout or "")[-1200:]
    assert "CHECK PASS" in r.stdout
