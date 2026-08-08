# cleanup.ps1
# 清理 xiyouji-agent-web 迁移过程中产生的残留文件。
# 这些残留由沙箱文件监控持锁、且沙箱无回收站而无法在沙箱内删除；
# 在本机（有回收站、无此锁）运行即可正常移除。
# 用法：右键 -> 用 PowerShell 运行，或执行：
#   powershell -ExecutionPolicy Bypass -File cleanup.ps1

$ErrorActionPreference = 'SilentlyContinue'

# 1) 项目内冗余的残缺 node_modules（无害，npm 不会读取）
Remove-Item -Recurse -Force "D:\1\xiyouji\xiyouji-agent-web\_nm_partial"

# 2) 调试日志
Remove-Item -Force "D:\1\xiyouji\xiyouji-agent-web\build.log"
Remove-Item -Force "D:\1\xiyouji\xiyouji-agent-web\install.log"
Remove-Item -Force "D:\1\xiyouji\xiyouji-agent-web\npm-install.log"
Remove-Item -Force "D:\1\xiyouji\xiyouji-agent-web\rebuild.log"
Remove-Item -Force "D:\1\xiyouji\xiyouji-agent-web\server.log"
Remove-Item -Force "D:\1\xiyouji\xiyouji-agent-web\vite_build.log"

# 3) 根目录下的零散残留
Remove-Item -Recurse -Force "D:\1\xiyouji-agent-web"
Remove-Item -Recurse -Force "D:\1\_trash_src"
Remove-Item -Recurse -Force "D:\1\_trash_xiyouji_move"
Remove-Item -Recurse -Force "D:\1\_DEBRIS_xiyouji_move"

Write-Output "cleanup done."
