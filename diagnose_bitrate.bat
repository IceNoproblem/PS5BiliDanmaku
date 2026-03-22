@echo off
chcp 65001 >nul
echo ==================== RTMP码率问题诊断工具 ====================
echo.

echo [步骤1] 检查Docker容器运行状态...
docker ps --filter "name=ps5-danmaku-monitor" --format "table {{.Names}}\t{{.Status}}"
docker ps --filter "name=ps5-playstation-server" --format "table {{.Names}}\t{{.Status}}"
echo.

echo [步骤2] 访问playstation-server状态页面...
echo 正在访问 http://localhost:8081 ...
curl -s http://localhost:8081 | findstr /i "live bitrate bandwidth kbps fps resolution"
echo.

echo [步骤3] 查看monitor容器日志(最近50行)...
echo ==================== monitor_rtmp日志 ====================
docker logs ps5-danmaku-monitor --tail 50 2>&1
echo.

echo [步骤4] 测试RTMP状态API...
echo 正在测试 http://localhost:5000/api/rtmp/status ...
curl -s http://localhost:5000/api/rtmp/status
echo.
echo.

echo [步骤5] 如果要启用调试模式...
echo 1. 编辑 docker-compose.yml
echo 2. 将 rtmp-monitor 的 command 改为: ["python", "monitor_rtmp_debug.py"]
echo 3. 将 DEBUG_MODE 改为: true
echo 4. 重启容器: docker-compose restart rtmp-monitor
echo 5. 查看调试HTML: docker exec ps5-danmaku-monitor cat /app/debug_playstation.html
echo.

pause
