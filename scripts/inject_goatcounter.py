#!/usr/bin/env python3
"""
W403 · GoatCounter 访问统计注入脚本

遍历 site/ 下所有 *.html，幂等地注入 GoatCounter tracking script 到 </head> 前。

GoatCounter 是开源免费网站分析（AGPL·提供免费托管版 goatcounter.com，
零自管服务器）。脚本格式：
  <script data-goatcounter="https://{SITE}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>

配置优先级：
  1. 命令行参数 --site
  2. .env / 环境变量：GOATCOUNTER_SITE
缺失时以 --check 运行不报错（仅检查覆盖率），注入模式报错退出。

幂等：若页面已含 "goatcounter" 则跳过，可重复运行不重复注入。

用法:
  python scripts/inject_goatcounter.py --site xiyouji       # 注入
  python scripts/inject_goatcounter.py --check               # 仅报告覆盖率，不写入
"""

import os
import sys

SITE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
MARKER = "goatcounter"


def load_env():
    """极简 .env 读取（项目根 .env + scripts/.env），不覆盖已有环境变量。"""
    root = os.path.dirname(SITE_DIR)
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(root, ".env"), os.path.join(here, ".env")):
        if not os.path.exists(p):
            continue
        try:
            with open(p, encoding="utf-8") as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln or ln.startswith("#") or "=" not in ln:
                        continue
                    k, _, v = ln.partition("=")
                    k, v = k.strip(), v.strip().strip('"').strip("'")
                    if k and k not in os.environ:
                        os.environ[k] = v
        except Exception:
            pass


def build_tag(site):
    site = site.strip().rstrip("/")
    if not site:
        return None
    if site.startswith("http"):
        site = site.split("//")[-1]  # 容忍完整 URL
    site = site.split(".")[0]  # 容忍 xxx.goatcounter.com 形式
    return ('  <script data-goatcounter="https://%s.goatcounter.com/count"'
            ' async src="//gc.zgo.at/count.js"></script>\n' % site)


def inject(html_path, tag, check_only=False):
    with open(html_path, encoding="utf-8") as f:
        content = f.read()
    # 本地自托管 count.js：按页面深度计算相对路径（file:// 与 GitHub Pages 均可用）
    if tag and '__GCJS__' in tag:
        rel = os.path.relpath(os.path.join(SITE_DIR, 'static', 'js', 'goatcounter.js'),
                              os.path.dirname(html_path)).replace('\\', '/')
        tag = tag.replace('__GCJS__', rel)
    if MARKER in content:
        return "skip"  # 已注入，幂等跳过
    if "</head>" in content or "</HEAD>" in content:
        anchor = "</head>" if "</head>" in content else "</HEAD>"
        new_content = content.replace(anchor, tag + anchor, 1)
    elif "</body>" in content or "</BODY>" in content:
        anchor = "</body>" if "</body>" in content else "</BODY>"
        new_content = content.replace(anchor, tag + anchor, 1)
    else:
        return "no-anchor"
    if check_only:
        return "would-inject"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return "injected"


def main():
    load_env()
    check_only = "--check" in sys.argv

    site = ""
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--site" and i + 1 < len(args):
            site = args[i + 1]
    site = site or os.environ.get("GOATCOUNTER_SITE", "").strip()

    tag = build_tag(site) if site else None
    if tag is None and not check_only:
        print("错误：缺少 GoatCounter site 配置。需 --site xxx 或 .env 中 GOATCOUNTER_SITE=xxx。",
              file=sys.stderr)
        sys.exit(1)

    html_files = []
    for root, _dirs, files in os.walk(SITE_DIR):
        for fn in files:
            if fn.endswith(".html"):
                html_files.append(os.path.join(root, fn))
    html_files.sort()

    stats = {"injected": 0, "skip": 0, "no-anchor": 0, "would-inject": 0}
    for hp in html_files:
        rel = os.path.relpath(hp, SITE_DIR)
        result = inject(hp, tag, check_only=check_only) if tag else "no-anchor"
        stats[result] = stats.get(result, 0) + 1
        if result in ("injected", "would-inject", "no-anchor"):
            print("[%s] %s" % (result, rel))

    print("\n=== 统计 ===")
    print("  扫描文件数: %d" % len(html_files))
    print("  注入/待注入: %d" % (stats["injected"] + stats["would-inject"]))
    print("  已跳过(幂等): %d" % stats["skip"])
    print("  无锚点(跳过): %d" % stats["no-anchor"])
    if check_only:
        print("(check-only 模式，未写入任何文件)")


if __name__ == "__main__":
    main()
