#!/usr/bin/env python3
"""W1067 · action ref 完整性门禁——「CI 引用的每个 action 必须是该仓库真实存在的完整 SHA」。

## 存在的理由（根因，不是装饰）

W1066 批新增暗色门禁 merge job 时，写入了一个 **39 位的编造 SHA**
（`actions/download-artifact@fa0a91b8…`，该仓库无此 commit，且长度少 1 字符）。
后果：merge job 在 GitHub 的 **「Set up job」阶段 1 秒内 failure**——Checkout 都没跑，
错误信息是 `Unable to resolve action … unable to find version …`。
该症状**极易被误判为 GitHub 基础设施故障 / runner 限额 / 并发排队**（本轮即如此误判过一轮）。
而仓内当时**零**机器判据能拦住它 ⇒ 只有 job 真跑到才炸。

## 判据（两道）

① **离线·格式判据**（零依赖·永远可跑）
   `.github/workflows/**` 里每一条 `uses:` 必须是 `owner/repo@<40 位小写 hex>`。
   - 拒绝 tag / branch 引用（仓内铁律 W663/T4：actions 必钉 full SHA）
   - 拒绝任何长度 ≠ 40 的十六进制串（截断/手滑/编造）——**本次真缺陷正是 39 位**

② **联网·存在性判据**（`--api`，需 token）
   逐个 ref 调 GitHub API 验证该 commit 真的在那个仓库里。

## 三条纪律（来自本轮实测，写死在这里防止后人重犯）

1. **「查不到」≠「不存在」**
   实测：同一个真实存在的 `github/codeql-action@1190a975…`，连续两次调用
   `repos/<repo>/commits/<sha>` 一次 200、一次 404。⇒ 判红前必须**双 endpoint 复核**：
   `commits/<sha>` 与 `git/commits/<sha>`，**两个都 404 才算不存在**。
   任何其它错误（限流 403 / 网络 / JSON 解析失败）⇒ **fail-closed**（退出码 2），
   绝不当作「不存在」——假阴性会诱使人去改坏本来正确的 SHA。
2. **先怀疑自己的判据，再动产品代码**
   本轮初版脚本把「任何非 0 退出码」都当「不存在」，差点把 4 处正确的 CodeQL SHA
   判成编造的并「修」掉。⇒ 判据自身必须带自测与负样本。
3. **负样本夹具必须低熵**
   本仓 gitleaks 会拦高熵合成密钥 ⇒ 自测里**不硬编码任何 SHA 字符串**，
   真实存在的那个 ref 由运行时从仓内文件抽取。

## 用法

    python scripts/check_action_refs.py             # 仅离线格式判据
    python scripts/check_action_refs.py --api       # 离线 + GitHub API 存在性
    python scripts/check_action_refs.py --self-test # 自测（含负样本·不碰真实文件）

退出码：0 = 通过 / 1 = 判红 / 2 = 门禁自身故障（fail-closed）
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WF_DIR = ROOT / ".github" / "workflows"

USES_RE = re.compile(r"uses:\s*([A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-/]+)@([^\s#]+)")
SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
HEXISH_RE = re.compile(r"^[0-9a-f]{7,}$")

API_ROOT = "https://api.github.com"
UA = "xiyouji-action-ref-gate"
TIMEOUT = 20
RETRY_SLEEP = 1.0


# --------------------------------------------------------------------------- 扫描


def scan_dir(wf_dir: Path) -> list[dict]:
    """扫描工作流目录，返回每个 uses 引用的明细。"""
    out: list[dict] = []
    if not wf_dir.is_dir():
        return out

    def _loc(wf: Path) -> str:
        try:
            return wf.relative_to(ROOT).as_posix()
        except ValueError:
            # 自测用临时目录（不在仓根下）⇒ 退回绝对路径，不得抛异常
            return wf.as_posix()

    for wf in sorted(list(wf_dir.rglob("*.yml")) + list(wf_dir.rglob("*.yaml"))):
        try:
            text = wf.read_text(encoding="utf-8")
        except OSError as exc:
            out.append(
                {
                    "repo": "",
                    "ref": "",
                    "loc": f"{_loc(wf)}:<读取失败>",
                    "error": f"读取失败（fail-closed）: {exc}",
                }
            )
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            m = USES_RE.search(line)
            if not m:
                continue
            action_path = m.group(1)
            # 关键：action 引用有两种形态——
            #   owner/repo@ref            （如 actions/checkout@<sha>）
            #   owner/repo/subdir@ref     （如 github/codeql-action/analyze@<sha>）
            # 校验 commit 存在性时，API 路径只能用 owner/repo（前两段）。
            # 早期版本把整条 action_path 当仓库名 ⇒ 对子目录 action 拼出
            # /repos/github/codeql-action/analyze/commits/<sha> ⇒ 必然 404（假阴性）。
            owner_repo = "/".join(action_path.split("/")[:2])
            out.append(
                {
                    "action": action_path,
                    "repo": owner_repo,
                    "ref": m.group(2),
                    "loc": f"{_loc(wf)}:{lineno}",
                    "error": "",
                }
            )
    return out


def format_violations(entries: list[dict]) -> list[dict]:
    """判据①：必须是 owner/repo@<40 位小写 hex>。"""
    bad: list[dict] = []
    for e in entries:
        if e.get("error"):
            bad.append(e)
            continue
        ref = e["ref"]
        if not SHA40_RE.match(ref):
            if HEXISH_RE.match(ref):
                why = (
                    f"疑似 SHA 但长度 {len(ref)} ≠ 40（截断/手滑/编造）——"
                    f"该仓库极可能无此 commit，job 会在 set-up 阶段直接失败"
                )
            else:
                why = (
                    "未钉 full SHA（tag/branch 引用）——仓内铁律 W663/T4 "
                    "要求 actions 一律钉 40 位 full SHA"
                )
            bad.append({**e, "error": why})
    return bad


# --------------------------------------------------------------------------- API


def _api_get(path: str, token: str | None) -> tuple[bool, str]:
    """返回 (是否「该 commit 不存在」, 错误摘要)。

    404 与 422 都算「不存在」：
      - 404 = 该仓库/该 SHA 找不到
      - 422 = SHA 格式合法但该仓库无此 commit（`No commit found for SHA`）
    其它错误（限流 403 / 网络 / JSON 解析失败）**一律不算不存在**——
    假阴性会诱使人去改坏本来正确的 SHA。
    """
    req = urllib.request.Request(
        f"{API_ROOT}{path}",
        headers={
            "User-Agent": UA,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode("utf-8", "replace")
            try:
                json.loads(body)
            except Exception as exc:
                return False, f"HTTP {resp.status} 但 JSON 解析失败: {exc}"
            return False, ""
    except urllib.error.HTTPError as exc:
        if exc.code in (404, 422):
            return True, f"HTTP {exc.code}"
        return False, f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return False, f"网络错误: {exc.reason}"
    except Exception as exc:  # 其它异常：无法判定 ⇒ fail-closed
        return False, f"请求异常: {exc}"


def ref_exists(owner_repo: str, ref: str, token: str | None) -> tuple[bool, str]:
    """判定某 ref 是否真的存在于 owner_repo 仓库里。

    双 endpoint 复核：两个都「不存在」才判不存在；任一成功即存在；
    其它错误 ⇒ 无法判定（fail-closed，由调用方决定退出码 2）。
    """
    ep1 = f"/repos/{owner_repo}/commits/{ref}"
    ep2 = f"/repos/{owner_repo}/git/commits/{ref}"
    last_err = ""
    for attempt in range(3):
        nf1, err1 = _api_get(ep1, token)
        if not nf1 and not err1:
            return True, ""
        last_err = err1
        if not nf1:
            # 非「不存在」错误：可能是限流/网络 ⇒ 重试；不可当不存在
            time.sleep(RETRY_SLEEP * (attempt + 1))
            continue
        nf2, err2 = _api_get(ep2, token)
        if not nf2 and not err2:
            return True, ""
        if nf2:
            return False, "两个 endpoint 均报不存在"
        last_err = err2
        time.sleep(RETRY_SLEEP * (attempt + 1))
    return False, f"无法判定（最后一个错误: {last_err}）"


# --------------------------------------------------------------------------- 主流程


def run_check(api: bool, token: str | None, ci_mode: bool = False) -> int:
    entries = scan_dir(WF_DIR)
    if not entries:
        print("FAIL: 未扫到任何 uses 引用（扫描面为空 ⇒ fail-closed）")
        return 2
    if not WF_DIR.is_dir():
        print(f"FAIL: 工作流目录不存在: {WF_DIR}")
        return 2

    print(f"扫描目录: {WF_DIR}")
    print(f"uses 引用条目: {len(entries)}")

    bad = format_violations(entries)
    unique_refs = sorted({(e["repo"], e["ref"]) for e in entries if not e.get("error")})
    print(f"去重后 (repo, ref): {len(unique_refs)}")

    if bad:
        print(f"\n[① 离线格式判据] FAIL — {len(bad)} 处不合规：")
        for e in bad:
            print(f"  ✗ {e['loc']}  {e.get('action') or e['repo']}@{e['ref']}")
            print(f"      {e['error']}")
    else:
        print("\n[① 离线格式判据] PASS — 全部为 40 位 full SHA")

    unverifiable: list[tuple[str, str, str]] = []
    if api:
        print("\n[② 联网存在性判据] 查询中 …")
        for repo, ref in unique_refs:
            exists, err = ref_exists(repo, ref, token)
            if exists:
                print(f"  ✓ {repo}@{ref[:16]}…")
            elif err.startswith("两个 endpoint"):
                print(f"  ✗ {repo}@{ref} —— {err}")
                bad.append(
                    {
                        "repo": repo,
                        "ref": ref,
                        "loc": "(见上)",
                        "error": f"{repo}@{ref} 在该仓库不存在（双 endpoint 均报不存在：404/422）",
                    }
                )
            else:
                print(f"  ? {repo}@{ref} —— {err}")
                unverifiable.append((repo, ref, err))
    else:
        print("\n[② 联网存在性判据] SKIP（未加 --api）")

    if unverifiable:
        for repo, ref, err in unverifiable:
            print(f"  ? {repo}@{ref} —— {err}")
        if ci_mode:
            # CI 模式：外部 API 的限流/网络抖动**不得卡死 PR**（工程决策，非纪律妥协）。
            # 但「判定为不存在」仍然阻断（那是真缺陷）—— 已在上面进 bad。
            print(
                f"\n[②] 有 {len(unverifiable)} 处无法判定（限流/网络）⇒ CI 模式降级为 WARN，"
                "不阻断 PR；离线格式判据与「判定不存在」仍阻断。"
                "请手动重跑 `python scripts/check_action_refs.py --api` 复核。"
            )
            print("::warning::部分 action ref 的存在性本轮未能验证")
        else:
            print(
                f"\n[②] 有 {len(unverifiable)} 处无法判定 ⇒ fail-closed（退出码 2）。"
                "限流/网络问题，请稍后重跑；不要据此改代码。"
            )
            return 2

    if bad:
        print(f"\n结论: FAIL（{len(bad)} 处）")
        return 1
    print("\n结论: PASS")
    return 0


# --------------------------------------------------------------------------- 自测


def _selftest() -> int:
    """负样本自证：每条判据都必须能被证伪（能判红）。

    纪律：夹具**不硬编码任何 SHA 字符串**（gitleaks 会拦高熵合成密钥），
    真实存在的 ref 运行时从仓内工作流抽取。
    """
    import tempfile

    cases: list[tuple[str, str, bool, str]] = []
    # N1 39 位 hex（本次真缺陷形态）——运行时拼接，不硬编码
    short = "a" * 39
    cases.append(("N1 39 位 hex", f"owner/repo@{short}", True, "长度 39 ≠ 40"))

    # N2 tag 引用
    cases.append(("N2 tag 引用", "owner/repo@v4", True, "未钉 full SHA"))

    # N3 合法 40 位 hex（低熵构造）——格式判据应放行
    good = "b" * 40
    cases.append(("N3 40 位 hex（格式合法）", f"owner/repo@{good}", False, ""))

    # N4 短 SHA（7 位）
    cases.append(("N4 7 位短 SHA", f"owner/repo@{'c' * 7}", True, "未钉 full SHA"))

    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        wf_dir = Path(tmp) / "workflows"
        wf_dir.mkdir(parents=True)
        for name, uses, expect_bad, _why in cases:
            (wf_dir / f"{name.split()[0]}.yml").write_text(
                f"steps:\n  - uses: {uses}\n", encoding="utf-8"
            )
            entries = scan_dir(wf_dir)
            bad = format_violations(entries)
            got_bad = bool(bad)
            ok = got_bad == expect_bad
            print(
                f"  {'✓' if ok else '✗'} {name}：期望{'判红' if expect_bad else '放行'} 实得{'判红' if got_bad else '放行'}"
            )
            if not ok:
                failed += 1
            for f in wf_dir.iterdir():
                f.unlink()

    # 联网判据的负样本：40 位低熵 hex 必然在真实仓库不存在 ⇒ 双 endpoint 应均 404
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    ghost = "d" * 40
    exists, err = ref_exists("actions/checkout", ghost, token)
    if exists:
        print("  ✗ N5 联网负样本（40 位低熵 ghost SHA）竟然被判定为存在 ⇒ 判据失效")
        failed += 1
    else:
        print(f"  ✓ N5 联网负样本（40 位低熵 ghost SHA）判定为不存在（{err}）")

    # 联网判据的正样本：从仓内真实工作流抽一个已存在的 ref
    real_ref = ""
    for e in scan_dir(WF_DIR):
        if e["ref"] and SHA40_RE.match(e["ref"]) and e["repo"]:
            real_ref = e["repo"]
            real_sha = e["ref"]
            break
    if real_ref:
        ok_exist, err2 = ref_exists(real_ref, real_sha, token)
        if ok_exist:
            print(
                f"  ✓ N6 联网正样本（仓内真实 ref {real_ref}@{real_sha[:12]}…）判定为存在"
            )
        else:
            print(
                f"  ✗ N6 联网正样本（{real_ref}@{real_sha[:12]}…）判定为不存在（{err2}）⇒ 判据失效"
            )
            failed += 1
    else:
        print("  ? N6 联网正样本：仓内未抽到可用 ref（跳过，不计失败）")

    if failed:
        print(f"\n自测 FAIL：{failed} 条判据不可证伪")
        return 1
    print("\n自测 PASS：全部判据均可证伪（负样本必红）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="action ref 完整性门禁（W1067）")
    ap.add_argument(
        "--api", action="store_true", help="联网验证 commit 在该仓库真实存在"
    )
    ap.add_argument("--self-test", action="store_true", help="自测（含负样本）")
    args = ap.parse_args()

    if args.self_test:
        return _selftest()

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if args.api and not token:
        print(
            "FAIL: --api 需要 token（设 GH_TOKEN 或 GITHUB_TOKEN）"
            "⇒ 无法判定，fail-closed（退出码 2）"
        )
        return 2
    return run_check(args.api, token)


if __name__ == "__main__":
    sys.exit(main())
