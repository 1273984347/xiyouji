r"""W1327 专项测试：scripts/w1327_related_links.py（页脚同类关联链接生成器）

## 为什么测这个脚本

页脚关联链接是「看板卡片 → 45 个内容页」的**单向派生**：推荐口径、自页排除、类别一致
全部由本脚本的解析与匹配决定。脚本若静默漂移（正则漏卡 / 循环错位 / 幂等破坏），
页面上的链接会变成死链、自页链或错类链，而页面本身仍「看起来正常」——本文件把
派生规则与注入/重放行为钉成可回归的判据。

## 覆盖判据

  G1 同类循环取后 3 页且自页排除（4 页类别 → a 得到 b/c/d）
  G2 类别成员不足 4 时取 n-1（Q+ 两页互链 1 条）
  G3 注入形态固定（MARK + nav.footer-related + 类别标签 + 相对链接）
  G4 重放幂等：同一块再跑 process 输出逐字不变（update 且零变化）
  G5 损坏/缺锚点 fail-closed：mark-broken / no-footer 不被静默吞掉
  G6 CLI --check 在真实仓库为 PASS（覆盖/MARK/死链/自页/分类/杂散/看板解析完备）
  G7 NO_FOOTER 5 页在磁盘上真实存在且确无 site-footer
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import w1327_related_links as rl  # noqa: E402

SCRIPT = SCRIPTS / "w1327_related_links.py"


def _cache(items):
    rl.parse_cache = {"a-l": items}


def test_cyclic_next_three_excludes_self():
    _cache([("a.html", "甲"), ("b.html", "乙"), ("c.html", "丙"), ("d.html", "丁")])
    assert rl.related_for("a-l", "a.html") == ["b.html", "c.html", "d.html"]
    assert rl.related_for("a-l", "d.html") == ["a.html", "b.html", "c.html"]


def test_small_category_takes_n_minus_1():
    rl.parse_cache = {"q-plus": [("x.html", "批评史长卷"), ("y.html", "观念装置")]}
    assert rl.related_for("q-plus", "x.html") == ["y.html"]
    block = rl.build_block("q-plus", "x.html")
    assert block.count("<a href=") == 1
    assert "同类 · Q+ 批评史" in block
    assert "观念装置" in block


def test_block_shape():
    _cache([("a.html", "甲"), ("b.html", "乙")])
    block = rl.build_block("a-l", "a.html")
    assert block.startswith("        " + rl.MARK)
    assert 'class="footer-related"' in block
    assert 'aria-label="同类可视化推荐"' in block
    assert 'href="b.html"' in block


HTML = (
    "<body>\n"
    '<footer class="site-footer">\n'
    '    <nav aria-label="页脚导航"><a href="../index.html">首页</a></nav>\n'
    "</footer>\n"
    "</body>\n"
)
BLOCK = (
    "        " + rl.MARK + "\n"
    '        <nav class="footer-related" aria-label="同类可视化推荐">\n'
    '            <span class="footer-meta">同类 · A-L 基础</span>\n'
    '            <a href="b.html">乙</a>\n'
    "        </nav>"
)


def test_insert_then_idempotent_update():
    new, action = rl.process(HTML, BLOCK)
    assert action == "insert"
    assert BLOCK in new
    assert new.endswith("</footer>\n</body>\n")
    again, action2 = rl.process(new, BLOCK)
    assert action2 == "update"
    assert again == new


def test_mark_broken_and_no_footer():
    broken = '<footer class="site-footer">' + rl.MARK + " 缺闭合</footer>"
    out, action = rl.process(broken, BLOCK)
    assert action == "mark-broken" and out == broken
    out2, action2 = rl.process("<body></body>", BLOCK)
    assert action2 == "no-footer" and out2 == "<body></body>"


def test_no_footer_set_matches_disk():
    for page in rl.NO_FOOTER:
        f = rl.DATA / page
        assert f.is_file(), page
        assert not rl.FOOTER.search(f.read_text(encoding="utf-8")), page


def test_cli_check_pass():
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    assert r.returncode == 0, (r.stdout or "")[-1200:]
    assert "CHECK PASS" in r.stdout
