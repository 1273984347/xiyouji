#!/usr/bin/env python3
"""
generate_csp.py — 全站 CSP（Content Security Policy）生成 / 注入 / 校验

为 site/**/*.html 逐页生成并注入 <meta http-equiv="Content-Security-Policy">：
  - script-src 'self' + 外部脚本白名单 EXTERNAL_SCRIPT_HOSTS（W695 曾清空——W456 禁外域 CDN
      后全站零外域脚本；W1167 G0-1 曾为 GA4 开具名例外，W1168 起 GA4 轨退役 ⇒ 当前为空集，
      即全站再次零外域**脚本**；统计改由自托管 goatcounter.js + stats.js 承载）
      + 该页全部内联 <script> 的 SHA-256 哈希（无 'unsafe-inline' / 'unsafe-eval'；
      全站 0 eval 已核；graph-explorer / mobile-index 的动态 onclick 与
      javascript: URL 已改事件绑定，脚本可严格哈希化）
  - script-src-attr 'none'（禁止内联事件处理器 / javascript: URL）
  - style-src 'self' 'unsafe-inline'（全站内联 CSS 与 style 属性，工程取舍：
      样式注入风险显著低于脚本，且全站 766 处 @font-face / 1636 处 style 属性
      哈希化不可维护）
  - img-src / font-src 'self'（全站资源本地化后无外部图片/字体）
  - connect-src 'self' + 统计回传域（W1168 起为 GoatCounter **单域**具名例外·W1167 的 GA4 两域
      已随双轨退役；dukou-engine 两页追加本地 RAG 引擎 127.0.0.1:8777）
  - object-src 'none' · base-uri 'self' · form-action 'self' · frame-src 'none'

用法：
  python scripts/generate_csp.py            # 注入 / 更新全部页面 meta（幂等）
  python scripts/generate_csp.py --check    # 只校验：任一页缺 meta 或哈希漂移即退出 1
                                            # （挂 verify_delivery 门禁，W425）

哈希口径（与浏览器 CSP 校验一致，2026-08-12 Chromium 实测确认）：
  取无 src 的 <script> 块原始文本 → UTF-8 → SHA-256 → base64。
  **不做任何清洗**：不去首尾空白、不解码 HTML 实体、不剥离 <!-- / --> 注释壳——
  实测 Chrome 对内联脚本哈希以解析后的原始文本为准（含首尾换行缩进与 &amp; 原样）。
  注意：任何内联脚本内容变更后必须重跑本脚本，否则该页脚本会被 CSP 拦截
  （这正是漂移门禁存在的意义）。
"""

import argparse
import base64
import hashlib
import os
import re
import sys

from utils.path_guard import PROJECT_ROOT, make_guard

_w536_guard_open = make_guard(PROJECT_ROOT)  # W761：W536 守卫单模块化（root=仓库根）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根
SITE = os.path.join(ROOT, "site")

# W1167 G0-1 用户拍板（2026-11-08·decision_log 见 spark-output/context/brief.json）：
# 零外域约束的**具名例外**——仅 GA4 统计（脚本下载域 + 数据回传域），file:// 场景由注入侧
# 异步+失败静默兜底（G0-3 口径）；例外清单之外任何外域资源仍为门禁违规。
# 注意：host 源必须**裸写不加单引号**——Chrome 实测拒绝带引号的 scheme-host
# （`''https://...''` invalid source 被忽略·第 43 门禁 console 回归当场抓出）；
# 引号形态仅 'self' 等关键字与 'sha256-' 源合法。
EXTERNAL_SCRIPT_HOSTS = []
# 统计回传域「具名例外」全集（W1168 起收敛为 GoatCounter **单域**）：
# W1167 曾按 G0-1 开 GA4 三域 + GoatCounter 一域共四域；W1168 用户决定 GA4 轨退出
# （账号未建 + 大陆可达性差 + web vitals/自定义事件改由自托管 GoatCounter 承载），
# 例外面随之收缩——收缩与扩张同样必须留痕（铁律 16⑦），见 CHANGELOG W1168 段。
# GoatCounter 端点须与 scripts/output/_w1167_analytics.json 的 goatcounter_endpoint 同源，
# 二者不一致由第 67 槽 C5 与第 56 槽 CSP 增量漂移同批拦下。
ANALYTICS_CONNECT_HOSTS = "https://1273984347.goatcounter.com"
RAG_ORIGIN = "http://127.0.0.1:8777"
# 口径沿革：W806 因 GoatCounter 账号实测 404 退役统计链，connect-src 归零外域；
# W1167 G0-1 拍板恢复为「具名例外」——仅 ANALYTICS_CONNECT_HOSTS 所列回传域
# （GoatCounter 端点本次复验 HTTP 400=缺参而非 404=死号，账号在活），其余外域仍为门禁违规。
# 开发模板（不入站、不入 sitemap）：不注入 CSP，避免模板占位内容干扰哈希门禁
TEMPLATE_EXCLUDE = {"_template.html"}

SCRIPT_RE = re.compile(
    r"<[sS][cC][rR][iI][pP][tT](?![^>]*\b[sS][rR][cC]\s*=)[^>]*>"
    r"(.*?)</[sS][cC][rR][iI][pP][tT](?:\s[^>]*)?\s*>",
    re.DOTALL,
)
# 本工具始终以双引号包裹 content；CSP 令牌用单引号（'self'/'sha256-…'），
# 因此 content 内不会出现双引号，用 [^"]* 即可完整捕获。
META_RE = re.compile(
    r'<meta\s+http-equiv=["\']Content-Security-Policy["\']\s+content="([^"]*)"\s*/?>',
    re.IGNORECASE,
)


def inline_script_hashes(html):
    """返回该页全部内联脚本的 CSP SHA-256 哈希列表（'sha256-…'）。"""
    hashes = []
    for m in SCRIPT_RE.finditer(html):
        body = m.group(1)
        # 纯空白脚本不执行，无需哈希；其余一律按原始文本哈希（Chrome 实测口径）
        if not body.strip(" \t\r\n"):
            continue
        digest = hashlib.sha256(body.encode("utf-8")).digest()
        hashes.append("'sha256-%s'" % base64.b64encode(digest).decode("ascii"))
    return hashes


def build_policy(html, needs_rag):
    parts = ["default-src 'self'"]
    script_src = ["script-src 'self'"] + EXTERNAL_SCRIPT_HOSTS + inline_script_hashes(html)
    parts.append(" ".join(script_src))
    parts.append("script-src-attr 'none'")
    parts.append("style-src 'self' 'unsafe-inline'")
    parts.append("img-src 'self'")
    parts.append("font-src 'self'")
    if needs_rag:
        parts.append("connect-src 'self' %s %s" % (RAG_ORIGIN, ANALYTICS_CONNECT_HOSTS))
    else:
        parts.append("connect-src 'self' %s" % ANALYTICS_CONNECT_HOSTS)
    parts.append("object-src 'none'")
    parts.append("base-uri 'self'")
    parts.append("form-action 'self'")
    parts.append("frame-src 'none'")
    return "; ".join(parts)


def meta_tag(policy):
    return '<meta http-equiv="Content-Security-Policy" content="%s">' % policy


def inject(html, policy):
    tag = meta_tag(policy)
    if META_RE.search(html):
        return META_RE.sub(lambda _m: tag, html, count=1)
    # 插到 <head> 后第一个 meta（charset）之后，保证早于任何资源加载
    m = re.search(r"(<head[^>]*>\s*)(<meta[^>]*charset[^>]*>)", html, re.IGNORECASE)
    if m:
        return html[: m.end(2)] + "\n" + tag + html[m.end(2):]
    m = re.search(r"<head[^>]*>", html, re.IGNORECASE)
    if m:
        return html[: m.end()] + "\n" + tag + html[m.end():]
    raise ValueError("页面缺少 <head>，无法注入 CSP meta")


def walk_html():
    for root, _dirs, files in os.walk(SITE):
        for fn in sorted(files):
            if fn.endswith(".html"):
                yield os.path.join(root, fn)


def main():
    ap = argparse.ArgumentParser(description="全站 CSP 生成 / 注入 / 校验")
    ap.add_argument("--check", action="store_true", help="只校验不写文件；漂移即退出 1")
    args = ap.parse_args()

    total = drift = injected = 0
    total_hashes = 0
    for path in walk_html():
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        if os.path.basename(path) in TEMPLATE_EXCLUDE:
            continue
        with open(path, encoding="utf-8") as f:
            html = f.read()
        # 本地 RAG 引擎放行：dukou-engine 直连 fetch，index/dashboard 经 rag-chat.js 探活
        needs_rag = "127.0.0.1:8777" in html or "rag-chat.js" in html
        policy = build_policy(html, needs_rag)
        hashes = inline_script_hashes(html)
        total += 1
        total_hashes += len(hashes)
        cur = META_RE.search(html)
        cur_content = cur.group(1) if cur else None
        if cur_content == policy:
            continue
        drift += 1
        if args.check:
            why = "缺 CSP meta" if cur_content is None else "CSP 哈希/策略漂移"
            print("DRIFT  %s — %s" % (rel, why))
            continue
        new_html = inject(html, policy)
        if new_html == html:
            print("SKIP   %s — 注入失败（内容未变化）" % rel)
            drift -= 1
            continue
        with _w536_guard_open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_html)
        injected += 1

    if args.check:
        print("CSP 校验：%d 页 · 内联脚本哈希 %d 个 · 漂移/缺失 %d 页"
              % (total, total_hashes, drift))
        return 1 if drift else 0
    print("CSP 注入：%d 页已更新 · 共 %d 页 · 内联脚本哈希 %d 个"
          % (injected, total, total_hashes))
    print("提示：请随后运行  python scripts/generate_csp.py --check  确认零漂移")
    return 0


if __name__ == "__main__":
    sys.exit(main())
