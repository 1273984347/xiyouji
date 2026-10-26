"""W757 一次性：四页脚版本链前置 W757 条目（方案 D 后 bump_version 停用·按 _w702_edits 形态）。

形态：`<footer>... · W756 <描述> · W755 ...` → 在链首插入 `W757 <描述> · `。
每页先断言 W757 未存在、W756 存在恰一次（拒绝盲改·幂等）。
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    "site/dukou-engine.html",
    "site/index.html",
    "site/data/cross-time-danmaku.html",
    "site/data/tag-cloud.html",
]

ENTRY = ("W757 CI 门禁接线缺陷修复（第 43 门禁 CI 必红加安全单测接线加扫描扩面）"
         "（verify-delivery job 补 Playwright 安装与浏览器缓存·D1 第 43 门禁此前 CI 必红；"
         "agent-web-build job 补 test:server·D2 W752 安全单测此前未接线；"
         "security_scan 扩面 xiyouji-agent-web 与 TS 源文件并排除 tsc 产物·D3；"
         "新增 test_ci_wiring.py 接线回归 9 例加负样本 4/4 真防线）")


def main():
    for rel in PAGES:
        p = ROOT / rel
        s = p.read_text(encoding="utf-8")
        assert "W757" not in s, "%s: 已含 W757（重复执行？）" % rel
        anchor = "W756 "
        n = s.count(anchor)
        assert n == 1, "%s: 期望 1 处 %r，实得 %d" % (rel, anchor, n)
        s = s.replace(anchor, ENTRY + " · W756 ", 1)
        p.write_text(s, encoding="utf-8")
        print("OK  %s" % rel)


if __name__ == "__main__":
    main()
