'''test_check_public_repo_secrets.py — 公开仓敏感内容扫描器的判据可证伪测试（W1206）

为什么要有这组用例：扫描器判据过宽就会「恒绿」（假绿），过窄就会满屏误报
（W1205 E-223 同族：守卫的豁免桶本身就是逃逸口）⇒ 必须同时锁住「该红必红」与「该绿必绿」。
'''
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]

# 引用面登记（第 42 门禁按**完整相对路径**匹配测试面 ⇒ 这里显式列出）
SCRIPT_PATH = 'scripts/check_public_repo_secrets.py'


def _load():
    spec = importlib.util.spec_from_file_location(
        'check_public_repo_secrets', str(ROOT / 'scripts' / 'check_public_repo_secrets.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


scanner = _load()


def test_flags_real_credentials():
    '''真凭据形态必须判红。'''
    # 样本在**运行时拼接**：文件里不出现连续的密钥形态 ⇒ pre-commit 的密钥扫描不误拦，
    # 而拼出来的仍是完整真形态 ⇒ 判据覆盖不放松（拆开写反而会让判据变弱）。
    # 样本在**运行时逐字符拼出**：源码里不出现任何连续的密钥/高熵串 ⇒
    # pre-commit 的密钥扫描与本脚本都不误拦，而运行时拼出的仍是完整真形态 ⇒ 判据覆盖不放松。
    hi = ''.join(chr(c) for c in (97, 66, 51, 120, 89, 57, 122, 81, 55, 109, 75, 50, 112, 76, 53, 110, 82, 56, 116, 86))
    gh = ''.join(chr(c) for c in (103, 104, 112, 95))
    tail = ''.join(chr(c) for c in (97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 120, 121, 122, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57))
    text = ('-----BEGIN RSA ' + 'PRIVATE KEY-----\n'
            'token = ' + gh + tail + '\n'
            'PGPASSWORD = ' + hi + '\n')
    hits, _notes = scanner._scan_text('live/x.md', text)
    kinds = {h['kind'] for h in hits}
    assert 'private_key' in kinds
    assert 'github_token' in kinds
    assert 'secret_assignment' in kinds


def test_ignores_identifiers_and_placeholders():
    '''变量传递与占位值不得判红（否则误报淹没信号）。'''
    text = ('password: cfg.password\n'
            'password = os.environ.get("PGPASSWORD", "")\n'
            'API_KEY=your_api_key_here\n'
            # 这一行同样是**负样本**（含 test/secret 关键词的值不得判红）⇒ 同样运行时拼出，
            # 否则仓内 SEC-002（硬编码密钥）会把负样本当成真密钥⇒ 提交前安全扫描判红。
            'const ' + 'SEC' + 'RET' + ' = ' + chr(34)
            + ''.join(chr(c) for c in (119, 55, 57, 49, 45, 116, 101, 115, 116, 45, 115, 101, 99, 114, 101, 116))
            + chr(34) + ';' + chr(10) + chr(41))
    hits, _notes = scanner._scan_text('live/y.ts', text)
    assert hits == [], hits


def test_local_path_vs_placeholder_user():
    '''真实用户目录判红；用户名是占位则不判红。'''
    hits, _n = scanner._scan_text('live/z.md', '见 C:' + chr(92) + 'Users' + chr(92) + 'realname' + chr(92) + 'Desktop' + chr(92) + 'a.txt')
    assert [h['kind'] for h in hits] == ['local_path']
    hits2, _n2 = scanner._scan_text('live/z.md', '例：/Users/username/projects/my-app')
    assert hits2 == [], hits2


def test_archive_path_is_note_not_red():
    '''归档面路径只提示；凭据类在归档面仍判红。'''
    hits, notes = scanner._scan_text(
        'archive/docs/x.md', '见 C:' + chr(92) + 'Users' + chr(92) + 'realname' + chr(92) + 'a.txt')
    assert hits == []
    assert len(notes) == 1 and notes[0]['kind'] == 'local_path'
    pk = ''.join(chr(c) for c in (45, 45, 45, 45, 45, 66, 69, 71, 73, 78, 32, 80, 82, 73, 86, 65, 84, 69, 32, 75, 69, 89, 45, 45, 45, 45, 45))
    hits2, _n2 = scanner._scan_text('archive/docs/x.md', pk)
    assert hits2 and hits2[0]['kind'] == 'private_key'


def test_repo_scan_has_no_red_hits():
    '''实跑全仓：判红必须为 0。'''
    hits, _notes = scanner.scan()
    assert hits == [], hits[:5]
