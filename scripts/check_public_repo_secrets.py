#!/usr/bin/env python3
r'''check_public_repo_secrets.py — 公开仓敏感内容扫描（可复跑防线）

为什么需要它（W1206 实证）：公开仓的敏感面不止凭据——**本机绝对路径**同样暴露个人
文件布局（桌面文件、用户目录、工具链目录）。2026-11-11 的公开面审计在 25 个现役文档里
发现 33 处本机用户目录路径并已脱敏；本脚本把该判据固化为可复跑防线，避免下一批文档
又把机器指纹写回仓库。

扫描范围与分档（**关键**：不可改的历史与必须清的现在分开判）：
  - 凭据类（私钥 / token / 带值口令赋值）：**全仓判红**（含 archive/）——安全项，历史也要清。
  - 本机路径类（用户目录绝对路径）：**现役面判红，archive/ 只提示**——历史段按「归档只追加
    不改」铁律不可回溯改写，故记为提示并登记，不阻塞。

误报口径（已按实证收紧，避免把「代码里的变量传递」当凭据）：
  - 值是标识符/属性访问形态（password: cfg.password）⇒ 不算凭据
  - 值不是纯字面量形态（os.environ.get(...) 等）⇒ 不算凭据
  - 值含 test/secret/mock/example/your 等占位关键词 ⇒ 不算凭据
  - 路径里的用户名段是 username/user/example 一类占位 ⇒ 不算机器指纹

退出码：0 = 干净；1 = 有判红命中；2 = 用法/环境错误。
用法：py -3 scripts/check_public_repo_secrets.py [--json <证据路径>]
'''
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUOTE = chr(34) + chr(39)

# 私钥头**分片拼接**：文件里不得出现连续形态——否则提交前的密钥扫描会把本守卫自己当泄漏拦下
# （判据自身被自己的门禁拦 ⇒ 守卫反而无法入库·W1206 实测）。
PRIVATE_KEY_RE = re.compile(
    r'-----BEGIN ' + r'(?:RSA |OPENSSH |EC |DSA |PGP )?' + r'PRIVATE KEY-----')
GITHUB_TOKEN_RE = re.compile(r'\b(?:ghp|gho|ghs|ghu)_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}')
VENDOR_KEY_RE = re.compile(r'\bsk-(?:ant-)?[A-Za-z0-9_-]{24,}')
AWS_KEY_RE = re.compile(r'\bAKIA[0-9A-Z]{16}\b')
SLACK_RE = re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{12,}')
SECRET_ASSIGN_RE = re.compile(
    r'(?im)^[^\n#]{0,40}?\b(PGPASSWORD|PGPASS_FILE|DB_PASSWORD|DATABASE_PASSWORD|PASSWORD|SECRET|API_KEY|ACCESS_TOKEN|PRIVATE_KEY)\b\s*[:=]\s*(\S{8,})'
)
PLACEHOLDER_VALUES = {
    'your_api_key', 'your_password', 'your_password_here', 'your_api_key_here',
    'placeholder', 'changeme', 'example', 'mock-key', 'mock', 'none', 'null',
    'undefined', 'todo', 'xxx', 'unit-test-secret-should-never-leak',
    'unit-test-key-should-not-leak', 'w808-e2e-key',
}
PLACEHOLDER_PAT = re.compile(r'(your[_-]|example|placeholder|mock|fake|dummy|test|secret|fixture|changeme)', re.I)
LOCAL_USER_PLACEHOLDERS = {'username', 'user', 'your', 'example', 'someone', 'john', 'test'}
LOCAL_PATH_RE = re.compile(r'(?:[A-Za-z]:[\\/]Users[\\/]|/[a-z]?/Users/)[A-Za-z0-9._-]+')
IDENT_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z0-9_]+)*$')
LITERAL_RE = re.compile(r'^[A-Za-z0-9+/=_-]{12,}$')

TEXT_EXTS = {'.md', '.txt', '.json', '.jsonl', '.yml', '.yaml', '.py', '.js', '.mjs',
             '.ts', '.tsx', '.html', '.css', '.sh', '.ps1', '.sql', '.toml',
             '.ini', '.cfg', '.xml', '.env'}
SKIP_DIRS = {'.git', 'node_modules', 'dist', '__pycache__', '.venv', 'venv',
            'out', 'build', '.tsbuild'}


def _is_placeholder_value(value: str) -> bool:
    v = (value or '').strip().strip(QUOTE)
    if not v:
        return True
    if v.lower() in PLACEHOLDER_VALUES:
        return True
    if PLACEHOLDER_PAT.search(v):
        return True
    if IDENT_RE.match(v) and len(v) < 16:
        return True
    if not LITERAL_RE.match(v):
        return True
    return False


def _tracked_files():
    out = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True,
                       encoding='utf-8', errors='replace').stdout
    return [ln for ln in out.split(chr(10)) if ln.strip()]


def _read(rel: str):
    p = os.path.join(ROOT, rel.replace('/', os.sep))
    try:
        if os.path.getsize(p) > 4 * 1024 * 1024:
            return None
        with open(p, encoding='utf-8', errors='replace') as fh:
            return fh.read()
    except OSError:
        return None


def _redact_path(line: str) -> str:
    """证据落盘前的摘要：**只留定位信息与前 8 字符，绝不落原文**。

    为什么只留 8 字符：证据文件若落原文 ⇒ (a) 证据本身成了新的泄漏面；
    (b) 扫描器会把自己的证据判红（自指循环）；(c) 提交前的密钥扫描会拦下提交。
    文件 + 行号 + 类别已足够定位复核，原文不必入库。
    """
    head = line.strip()[:8]
    return re.sub(r'(?i)(users)([/\\])[^/\\"\s]+', r'\1\2<user>', head)


def _scan_text(rel: str, text: str):
    hits = []
    notes = []
    archived = rel.replace(chr(92), '/').startswith('archive/')
    for lineno, line in enumerate(text.split(chr(10)), 1):
        for kind, rx in (('private_key', PRIVATE_KEY_RE), ('github_token', GITHUB_TOKEN_RE),
                         ('vendor_key', VENDOR_KEY_RE), ('aws_key', AWS_KEY_RE),
                         ('slack_token', SLACK_RE)):
            if rx.search(line):
                hits.append({'file': rel, 'line': lineno, 'kind': kind,
                             'snippet': line.strip()[:120]})
        for m in SECRET_ASSIGN_RE.finditer(line):
            if _is_placeholder_value(m.group(2)):
                continue
            hits.append({'file': rel, 'line': lineno, 'kind': 'secret_assignment',
                         'snippet': line.strip()[:120]})
        for m in LOCAL_PATH_RE.finditer(line):
            seg = m.group(0).replace(chr(92), '/').split('/')
            uname = ''
            for _i, _s in enumerate(seg):
                if _s.lower() == 'users' and _i + 1 < len(seg):
                    uname = seg[_i + 1]
                    break
            if uname.lower() in LOCAL_USER_PLACEHOLDERS:
                continue
            rec = {'file': rel, 'line': lineno, 'kind': 'local_path',
                   'snippet': _redact_path(line.strip())[:120]}
            (notes if archived else hits).append(rec)
    return hits, notes


def scan():
    hits = []
    notes = []
    for rel in _tracked_files():
        parts = rel.replace(chr(92), '/').split('/')
        if parts[0] in SKIP_DIRS or os.path.basename(rel) in SKIP_DIRS:
            continue
        if os.path.splitext(rel)[1].lower() not in TEXT_EXTS:
            continue
        text = _read(rel)
        if text is None:
            continue
        h, n = _scan_text(rel, text)
        hits.extend(h)
        notes.extend(n)
    return hits, notes


def main() -> int:
    ap = argparse.ArgumentParser(description='公开仓敏感内容扫描')
    ap.add_argument('--json', help='证据输出路径')
    args = ap.parse_args()
    hits, notes = scan()
    report = {'scanned_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'scope': 'git 跟踪面（凭据类全仓判红·本机路径类 archive 只提示）',
              'red_count': len(hits), 'note_count': len(notes),
              'red_hits': hits, 'notes': notes}
    if args.json:
        d = os.path.dirname(os.path.abspath(args.json))
        if d:
            os.makedirs(d, exist_ok=True)
        with open(args.json, 'w', encoding='utf-8') as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
    print('扫描完成：判红 %d 处 · 提示 %d 处' % (len(hits), len(notes)))
    for h in hits[:40]:
        print('  [红] %s:%d  %s  %s' % (h['file'], h['line'], h['kind'], h['snippet'][:90]))
    if notes:
        print('  提示（archive 历史·不可回溯改写）：%d 处' % len(notes))
    return 1 if hits else 0


if __name__ == '__main__':
    sys.exit(main())
