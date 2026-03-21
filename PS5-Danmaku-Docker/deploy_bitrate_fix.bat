@echo off
chcp 65001 >nul
echo ==================== 码率格式修复部署脚本 ====================
echo.
echo 正在更新monitor_rtmp.py以支持 6.36 Mb/s 格式...
echo.

cd /d D:\PS5-Danmaku-Docker

echo [步骤1] 检查Docker容器状态...
docker ps --filter "name=ps5-danmaku-monitor" --format "table {{.Names}}\t{{.Status}}"
echo.

echo [步骤2] 重启monitor容器以应用新代码...
docker-compose restart rtmp-monitor
echo.

echo [步骤3] 等待容器启动(10秒)...
timeout /t 10 /nobreak >nul
echo.

echo [步骤4] 查看容器日志(最近30行)...
echo ==================== monitor_rtmp日志 ====================
docker logs ps5-danmaku-monitor --tail 30 2>&1
echo.

echo [步骤5] 测试RTMP状态API...
echo 正在测试 http://localhost:5000/api/rtmp/status ...
curl -s http://localhost:5000/api/rtmp/status
echo.
echo.

echo ==================== 部署完成 ====================
echo.
echo 验证步骤:
echo 1. 确认日志中显示: [INFO] 检测到码率: XXXX kbps
echo 2. 访问 http://localhost:5000
echo 3. 确认Web界面码率显示正确(不再是 -)
echo.
echo 如果仍然显示 -,请运行:
echo   python test_rtmp_server.py
echo.
pause
