#!/usr/bin/env python3
"""IME 防误发 + 阈值滚动探针（W1134）——证明两项交互修复真实生效。

为什么需要专用探针：
    这两项是**事件时序**行为（composition 事件序列、scroll 事件与 scrollTop），
    既不在 J2 的属性集里（31 项静态计算样式属性），也无法用静态 grep 证伪
    ⇒ 必须用合成事件驱动真实浏览器读行为结果。

三组取证（每组含负样本，缺一不可）：
    G1 选字中回车 ⇒ **不得发送**（事件交给 IME 处理）
    G2 选字完成 500ms 内回车 ⇒ **不得发送**（拦截窗）
    G3 选字完成 500ms 后回车 ⇒ **正常发送**（防误发不得变成永久禁用）
    G4 上翻超过阈值 ⇒ **停止自动跟随**且「跳至最新」按钮可见
    G5 距底不足一行 ⇒ **仍然自动跟随**且按钮隐藏

用法：
    py -3 scripts/ime_scroll_probe.py --out scripts/output/_w1134_imescroll.json
    py -3 scripts/ime_scroll_probe.py --self-test
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "site")

PAGE = "data/ai-dialogue.html"

# 合成事件序列脚本：模拟 IME 选字 → 回车
DRIVE_JS = r"""
() => {
  const input = document.getElementById('chat-input');
  const sent = [];
  // 观测发送：包住 sendMessage（本页为函数声明·可直接改写其内部记录）
  window.__sent = sent;
  const orig = window.sendMessage;
  window.sendMessage = function(text) { sent.push(text); if (orig) { try { orig(text); } catch(e){} } };

  function fireKey(key, opts) {
    const ev = new KeyboardEvent('keydown', Object.assign({key: key, bubbles: true, cancelable: true}, opts||{}));
    input.dispatchEvent(ev);
    return ev.defaultPrevented;
  }
  function compStart() { input.dispatchEvent(new CompositionEvent('compositionstart', {bubbles: true, data: ''})); }
  function compEnd(data) { input.dispatchEvent(new CompositionEvent('compositionend', {bubbles: true, data: data || ''})); }

  const out = {};

  // G1：选字中回车 ⇒ 不应发送
  input.value = '测试内容一';
  compStart();
  const preventedG1 = fireKey('Enter', {isComposing: true});
  out.G1 = {sent: window.__sent.length, prevented: preventedG1};
  compEnd('测试内容一');

  // G2：选字刚完成（<500ms）回车 ⇒ 不应发送
  const beforeG2 = window.__sent.length;
  const preventedG2 = fireKey('Enter');
  out.G2 = {sent: window.__sent.length - beforeG2, prevented: preventedG2};

  // G3：等待超过 500ms 后回车 ⇒ 应发送
  const waited = window.__sent.length;
  return new Promise(function (resolve) {
    setTimeout(function () {
      const beforeG3 = window.__sent.length;
      const preventedG3 = fireKey('Enter');
      out.G3 = {sent: window.__sent.length - beforeG3, prevented: preventedG3};
      resolve(out);
    }, 620);
  });
}
"""

SCROLL_JS = r"""
() => {
  const hist = document.getElementById('chat-history');
  const btn = document.getElementById('jump-latest');
  const out = {};
  out.hasBtn = !!btn;
  out.btnOutsideHistory = btn ? !hist.contains(btn) : null;
  out.nearBottomBefore = (hist.scrollHeight - hist.scrollTop - hist.clientHeight) < 24;

  // 造足内容以便滚动
  for (let i = 0; i < 40; i++) {
    const d = document.createElement('div');
    d.className = 'message user';
    d.textContent = '填充消息 ' + i;
    hist.appendChild(d);
  }
  hist.scrollTop = hist.scrollHeight;
  hist.dispatchEvent(new Event('scroll'));

  // G4：上翻（scrollTop 归零 ⇒ 距底很远）
  hist.scrollTop = 0;
  hist.dispatchEvent(new Event('scroll'));
  out.afterScrollUp = {
    distance: hist.scrollHeight - hist.scrollTop - hist.clientHeight,
    btnVisible: btn ? btn.classList.contains('show') : null,
    btnOpacity: btn ? getComputedStyle(btn).opacity : null,
  };

  // G4c：等过渡跑完 ⇒ opacity 必须真的到 1（否则「class 加了但看不见」＝假绿）
  return new Promise(function (resolve) {
    setTimeout(function () {
      out.afterTransition = {
        opacity: btn ? getComputedStyle(btn).opacity : null,
        visibility: btn ? getComputedStyle(btn).visibility : null,
      };
      // G5：回到距底不足一行 ⇒ 应隐藏按钮
      hist.scrollTop = hist.scrollHeight - hist.clientHeight - 5;
      hist.dispatchEvent(new Event('scroll'));
      setTimeout(function () {
        out.afterBackToBottom = {
          distance: hist.scrollHeight - hist.scrollTop - hist.clientHeight,
          btnVisible: btn ? btn.classList.contains('show') : null,
          opacity: btn ? getComputedStyle(btn).opacity : null,
        };
        // G5b：渲染后再次上翻 ⇒ 自动跟随不得再把用户拽回底部
        hist.scrollTop = 0;
        hist.dispatchEvent(new Event('scroll'));
        const before = hist.scrollTop;
        setTimeout(function () {
          out.afterRenderWhileScrolledUp = {
            scrollTopBefore: before,
            scrollTopAfter: hist.scrollTop,
            stayedUp: hist.scrollTop < hist.clientHeight,
          };
          resolve(out);
        }, 300);
      }, 320);
    }, 320);
  });
  /* unreachable legacy block
  // G5：回到距底不足一行 ⇒ 应隐藏按钮
  hist.scrollTop = hist.scrollHeight - hist.clientHeight - 5;
  hist.dispatchEvent(new Event('scroll'));
  out.afterBackToBottom = {
    distance: hist.scrollHeight - hist.scrollTop - hist.clientHeight,
    btnVisible: btn ? btn.classList.contains('show') : null,
  };

  */
}
"""


def _file_url(rel: str) -> str:
    return "file:///" + os.path.join(SITE, rel).replace("\\", "/")


def run():
    from playwright.sync_api import sync_playwright  # noqa: WPS433

    result = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context()
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(_file_url(PAGE), wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(900)
        result["ime"] = page.evaluate(DRIVE_JS)
        result["scroll"] = page.evaluate(SCROLL_JS)
        result["page_errors"] = errors
        ctx.close()
        browser.close()
    return result


def judge(result):
    """按 G1-G5 判定。返回 (ok, rows, fails)。"""
    rows = []
    ime = result.get("ime", {})
    sc = result.get("scroll", {})
    fails = []

    def add(name, passed, detail):
        rows.append({"case": name, "pass": passed, "detail": detail})
        if not passed:
            fails.append({"case": name, "detail": detail})

    add("G1 选字中回车不发送", ime.get("G1", {}).get("sent") == 0, ime.get("G1"))
    add("G2 选字完成 500ms 内回车不发送", ime.get("G2", {}).get("sent") == 0, ime.get("G2"))
    add("G3 选字完成 500ms 后回车正常发送", ime.get("G3", {}).get("sent") == 1, ime.get("G3"))
    add("G4 上翻后跳至最新按钮可见", sc.get("afterScrollUp", {}).get("btnVisible") is True, sc.get("afterScrollUp"))
    add("G4b 上翻后不得被强制拽回底部",
        sc.get("afterRenderWhileScrolledUp", {}).get("stayedUp") is True,
        sc.get("afterRenderWhileScrolledUp"))
    add("G4c 过渡完成后按钮真可见（opacity=1）",
        sc.get("afterTransition", {}).get("opacity") == "1"
        and sc.get("afterTransition", {}).get("visibility") == "visible",
        sc.get("afterTransition"))
    add("G5 回到近底时按钮隐藏", sc.get("afterBackToBottom", {}).get("btnVisible") is False, sc.get("afterBackToBottom"))
    add("G6 无页面运行时错误", not result.get("page_errors"), result.get("page_errors"))
    return (not fails), rows, fails


def self_test():
    """负样本自证：每条断言都须能被坏读数抓住。"""
    good = {
        "ime": {"G1": {"sent": 0}, "G2": {"sent": 0}, "G3": {"sent": 1}},
        "scroll": {
            "afterScrollUp": {"btnVisible": True},
            "afterTransition": {"opacity": "1", "visibility": "visible"},
            "afterBackToBottom": {"btnVisible": False},
            "afterRenderWhileScrolledUp": {"stayedUp": True},
        },
        "page_errors": [],
    }
    ok_good = judge(good)[0]

    def broken(mutate):
        d = json.loads(json.dumps(good))
        mutate(d)
        return judge(d)[2] != []

    t1 = broken(lambda d: d["ime"]["G1"].update(sent=1))
    t2 = broken(lambda d: d["ime"]["G2"].update(sent=1))
    t3 = broken(lambda d: d["ime"]["G3"].update(sent=0))
    t4 = broken(lambda d: d["scroll"]["afterScrollUp"].update(btnVisible=False))
    t5 = broken(lambda d: d["scroll"]["afterRenderWhileScrolledUp"].update(stayedUp=False))
    t6 = broken(lambda d: d["scroll"]["afterBackToBottom"].update(btnVisible=True))
    t7 = broken(lambda d: d.update(page_errors=["boom"]))
    t8 = broken(lambda d: d["scroll"]["afterTransition"].update(opacity="0"))
    print("  T1 G1 误发送必抓 %s" % ("OK" if t1 else "FAIL"))
    print("  T2 G2 误发送必抓 %s" % ("OK" if t2 else "FAIL"))
    print("  T3 G3 漏发送必抓 %s" % ("OK" if t3 else "FAIL"))
    print("  T4 G4 按钮不现必抓 %s" % ("OK" if t4 else "FAIL"))
    print("  T5 G4b 被拽回必抓 %s" % ("OK" if t5 else "FAIL"))
    print("  T6 G5 按钮不隐必抓 %s" % ("OK" if t6 else "FAIL"))
    print("  T7 运行时错误必抓 %s" % ("OK" if t7 else "FAIL"))
    print("  T8 G4c 不可见必抓 %s" % ("OK" if t8 else "FAIL"))
    print("  T9 正常读数必放行 %s" % ("OK" if ok_good else "FAIL"))
    return all([t1, t2, t3, t4, t5, t6, t7, t8, ok_good])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        print("==== IME/滚动探针自测 ====")
        return 0 if self_test() else 1
    result = run()
    ok, rows, fails = judge(result)
    payload = {"result": result, "rows": rows, "fails": fails, "ok": ok}
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=1)
        print("OK -> %s" % args.out)
    print("==== IME/滚动探针结果 ====")
    for r in rows:
        print("  %-34s %s  %s" % (r["case"], "OK" if r["pass"] else "FAIL", json.dumps(r["detail"], ensure_ascii=False)[:80]))
    print("判定：%s" % ("全部通过" if ok else "存在失败"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
