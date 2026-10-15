"""W751 专项测试：scripts/new_page.py（可视化页面脚手架）

## 为什么测这个脚本（缺口取证）

W751 四面引用普查（tests/ ∪ verify_delivery ∪ CI ∪ Makefile）实测：new_page.py 属于
「46/101 无任何引用」清单——它是新增可视化页的**唯一脚手架入口**，生成物直接落
site/data/、并改写 site/index.html 导航，却没有任何自动化兜底：脚手架自身坏了（占位符
替换失效、模板锚点漂移、name 校验放行危险字符）只会被人工在很久以后发现。

## 覆盖判据（每条对应一个真实失效模式）

  P1 占位符全替换     → 模板改版后残留「页面标题」等占位符会产出半成品页
  P2 模板缺失快速失败  → 静默产空白页比报错更贵
  P3 name 白名单       → 放行 `../x`、`x/y`、大写会写出越界路径/坏文件名
  P4 索引锚点插入位置  → 插错 </ul> 会污染无关列表（user-visible）
  P5 锚点缺失不误写    → 找不到锚点必须只警告、绝不改 index.html
  P6 dry-run 零写入    → 预览命令写盘是最容易踩的「意外落盘」
  P7 --no-index 不碰导航 → 只建页不改索引的契约
  P8 幂等/可重复产出一致 → 同参数两次产出字节一致（防时间戳/随机串混入模板）

## 手法

`monkeypatch.setattr(np, "TEMPLATE"|"OUTPUT_DIR"|"INDEX", tmp_path/...)` 把三个模块级路径
全部改道到临时目录——**本测试进程内调用 main()，不启子进程**（Windows 无 fork 成本更低），
且真实仓库的 site/ 与 index.html 永不被触碰（用例逐条断言这一点）。
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import new_page as np  # noqa: E402

# 与 site/_template.html 的占位符契约同源（W751 抄录自脚手架 docstring）
TEMPLATE_BODY = """<!doctype html>
<html lang="zh-CN"><head>
<title>页面标题 · 详解西游记</title>
</head><body>
<h1>页面主标题</h1>
<div class="subtitle">副标题 / SECTION NAME</div>
<div class="tagline">一句话点题，斜体浅色</div>
<nav><span class="current">当前页面</span></nav>
<script>const EMBEDDED_DATA = {};</script>
</body></html>
"""

INDEX_BODY = """<!doctype html>
<html><body>
<!-- A-AH 数据可视化 -->
<ul>
  <li><a href="data/existing.html">已有页</a></li>
</ul>
<!-- 其他区块 -->
<ul><li>无关列表项</li></ul>
</body></html>
"""


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    """把脚手架的三个模块级路径改道到临时目录，返回路径集合。"""
    template = tmp_path / "site" / "_template.html"
    out_dir = tmp_path / "site" / "data"
    index = tmp_path / "site" / "index.html"
    template.parent.mkdir(parents=True, exist_ok=True)
    template.write_text(TEMPLATE_BODY, encoding="utf-8")
    index.write_text(INDEX_BODY, encoding="utf-8")
    monkeypatch.setattr(np, "TEMPLATE", template)
    monkeypatch.setattr(np, "OUTPUT_DIR", out_dir)
    monkeypatch.setattr(np, "INDEX", index)
    return {"template": template, "out_dir": out_dir, "index": index, "tmp": tmp_path}


def run_main(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["new_page.py", *argv])
    np.main()


# ---------------------------------------------------------------- P1 占位符全替换
def test_p1_all_placeholders_replaced(sandbox):
    content = np.render_template("power-resources", "三界权力资源", "J_权力与资源", "权力结构 + 长生资源链")
    for placeholder in ["页面标题", "页面主标题", "副标题 / SECTION NAME", "一句话点题，斜体浅色", "当前页面"]:
        assert placeholder not in content, "占位符残留：%s" % placeholder
    assert "<title>三界权力资源 · 详解西游记</title>" in content
    assert "<h1>三界权力资源</h1>" in content
    assert '<div class="subtitle">J_权力与资源</div>' in content
    assert '<div class="tagline">权力结构 + 长生资源链</div>' in content
    assert '<span class="current">三界权力资源</span>' in content
    assert "EMBEDDED_DATA" in content, "模板的 file:// 回退框架必须原样保留（铁律 5）"


# ------------------------------------------------------------ P2 模板缺失快速失败
def test_p2_missing_template_exits_with_error(sandbox, capsys):
    sandbox["template"].unlink()
    with pytest.raises(SystemExit) as ei:
        np.render_template("x", "X", "Z_图表", "d")
    assert "[ERROR]" in str(ei.value)
    assert "模板文件不存在" in str(ei.value)


# ------------------------------------------------------------------ P3 name 白名单
@pytest.mark.parametrize("bad", ["../evil", "a/b", "Upper", "with space", "中文名", "a.b", ""])
def test_p3_rejects_illegal_name(sandbox, monkeypatch, bad):
    with pytest.raises(SystemExit) as ei:
        run_main(monkeypatch, "--name", bad, "--title", "T", "--category", "Z_图表")
    assert "只能包含小写字母/数字/连字符" in str(ei.value)
    assert not sandbox["out_dir"].exists() or list(sandbox["out_dir"].iterdir()) == []


# ------------------------------------------------------------ P4 索引条目插入位置
def test_p4_index_entry_inserted_before_first_ul_close(sandbox, monkeypatch):
    run_main(monkeypatch, "--name", "power-resources", "--title", "三界权力资源",
             "--category", "J_权力与资源", "--desc", "d")
    text = sandbox["index"].read_text(encoding="utf-8")
    assert '<li><a href="data/power-resources.html">三界权力资源（J_权力与资源）</a></li>' in text
    a_ah = text.index("<!-- A-AH 数据可视化")
    first_close = text.index("</ul>", a_ah)
    second_close = text.index("</ul>", first_close + 1)
    assert text.index("power-resources.html") < first_close, "必须插进 A-AH 区块的第一个 </ul> 内"
    assert text.index("power-resources.html") < second_close
    assert "无关列表项" in text, "无关区块不得被动"


# -------------------------------------------------------- P5 锚点缺失只警告不误写
def test_p5_missing_anchor_warns_and_leaves_index_untouched(sandbox, monkeypatch, capsys):
    sandbox["index"].write_text(INDEX_BODY.replace("<!-- A-AH 数据可视化 -->", "<!-- 无锚点 -->"), encoding="utf-8")
    before = sandbox["index"].read_text(encoding="utf-8")
    added = np.append_to_index("foo", "Foo", "Z_图表")
    assert added == []
    assert "[WARN]" in capsys.readouterr().out
    assert sandbox["index"].read_text(encoding="utf-8") == before


def test_p5b_missing_index_file_warns(sandbox, monkeypatch, capsys):
    sandbox["index"].unlink()
    assert np.append_to_index("foo", "Foo", "Z_图表") == []
    assert "index.html 不存在" in capsys.readouterr().out


# ------------------------------------------------------------ P6/P7 dry-run 与 no-index
def test_p6_dry_run_writes_nothing(sandbox, monkeypatch, capsys):
    run_main(monkeypatch, "--name", "foo", "--title", "Foo", "--category", "Z_图表", "--dry-run")
    out = capsys.readouterr().out
    assert "[DRY-RUN]" in out
    assert not (sandbox["out_dir"] / "foo.html").exists()
    assert sandbox["index"].read_text(encoding="utf-8") == INDEX_BODY


def test_p7_no_index_flag_leaves_nav_untouched(sandbox, monkeypatch):
    before = sandbox["index"].read_text(encoding="utf-8")
    run_main(monkeypatch, "--name", "foo", "--title", "Foo", "--category", "Z_图表",
             "--desc", "d", "--no-index")
    out_file = sandbox["out_dir"] / "foo.html"
    assert out_file.exists(), "页面本体必须仍然生成"
    assert sandbox["index"].read_text(encoding="utf-8") == before, "--no-index 禁改导航"


# ------------------------------------------------------------- P8 产出幂等且自包含
def test_p8_repeat_run_is_byte_identical(sandbox, monkeypatch):
    argv = ("--name", "foo", "--title", "Foo", "--category", "Z_图表", "--desc", "d", "--no-index")
    run_main(monkeypatch, *argv)
    first = (sandbox["out_dir"] / "foo.html").read_bytes()
    run_main(monkeypatch, *argv)
    assert (sandbox["out_dir"] / "foo.html").read_bytes() == first
    text = first.decode("utf-8")
    assert "http://" not in text and "https://" not in text.replace("https://1273984347.github.io", ""), \
        "新页禁外域依赖（铁律 5：D3/Three 本地引用）"


# ------------------------------------------------- 真实仓库零触碰（安全断言）
def test_real_repo_untouched():
    """本测试文件的所有用例都必须走临时目录——真实 site/index.html 不得被测试改写。"""
    index = ROOT / "site" / "index.html"
    assert index.exists()
    assert "data/power-resources.html" not in index.read_text(encoding="utf-8"), \
        "测试产物泄漏进真实仓库导航（用例未改道 TEMPLATE/OUTPUT_DIR/INDEX 的信号）"
    assert not (ROOT / "site" / "data" / "foo.html").exists()
