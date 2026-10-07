import io

edits = [
  (r'D:\xiyouji\xiyouji-agent-web\server\engine\agent-loop.ts',
   '// engine/agent-loop.ts — 工具循环（W680：替代 CodeBuddy SDK 的 sdkQuery agent 循环）。',
   '// engine/agent-loop.ts — 工具循环（W680：替代旧厂商 SDK agent 循环的自主实现）。'),
  (r'D:\xiyouji\xiyouji-agent-web\server\engine\tools.ts',
   '// engine/tools.ts — 服务端工具集（W680：替代 CodeBuddy SDK 内建运行时）。',
   '// engine/tools.ts — 服务端工具集（W680：替代旧厂商 SDK 内建运行时的自主实现）。'),
  (r'D:\xiyouji\xiyouji-agent-web\server\engine\types.ts',
   '// engine/types.ts — 引擎类型契约（W680 引擎去 CodeBuddy 化）',
   '// engine/types.ts — 引擎类型契约（W680 引擎更换）'),
  (r'D:\xiyouji\xiyouji-agent-web\server\index.ts',
   '// 引擎配置状态（W680：原 CodeBuddy CLI 登录检查退役——路径保留以免前端 404）',
   '// 引擎配置状态（W680：原厂商 CLI 登录检查退役——路径保留以免前端 404）'),
  (r'D:\xiyouji\xiyouji-agent-web\server\feedback.test.mjs',
   '// 无需 CODEBUDDY_API_KEY（不触发 LLM）。测试行用完即删，不污染真实数据。',
   '// 无需 LLM 凭证（不触发 LLM）。测试行用完即删，不污染真实数据。'),
]

for path, old, new in edits:
    s = io.open(path, encoding='utf-8', newline='').read()
    assert s.count(old) == 1, 'anchor not found in ' + path
    io.open(path, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
    print('edited', path)
