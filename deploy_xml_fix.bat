@echo off
chcp 65001 >nul
echo ==================== XML 解析修复部署脚本 ====================
echo.
echo 正在部署 XML 格式解析修复...
echo.

cd /d D:\PS5-Danmaku-Docker

echo [步骤1] 检查Docker容器状态...
docker ps --filter "name=ps5-danmaku-monitor" --format "table {{.Names}}\t{{.Status}}"
echo.

echo [步骤2] 重启monitor容器以应用新代码...
docker-compose restart rtmp-monitor
if errorlevel 1 (
    echo [错误] docker-compose 命令失败,尝试使用 docker compose...
    docker compose restart rtmp-monitor
)
echo.

echo [步骤3] 等待容器启动(15秒)...
timeout /t 15 /nobreak >nul
echo.

echo [步骤4] 查看容器日志(最近50行)...
echo ==================== monitor_rtmp日志 ====================
docker logs ps5-danmaku-monitor --tail 50 2>&1
echo.

echo [步骤5] 测试RTMP统计页面访问...
echo 正在测试容器内部访问...
docker exec ps5-danmaku-monitor curl -s http://playstation-server:8081/ 2>&1 | findstr "bw_video bw_audio bw_in"
echo.

echo ==================== 部署完成 ====================
echo.
echo 修改内容:
echo ✓ monitor_rtmp.py - 使用 XML 解析替代 HTML 表格解析
echo ✓ docker-compose.yml - 修正端口从 80 改为 8081
echo.
echo 验证步骤:
echo 1. 检查日志中是否显示: [INFO] 检测到视频码率: X.XX Mb/s (XXXX kbps)
echo 2. 访问 http://localhost:5000
echo 3. 确认Web界面码率显示正确(不再是 -)
echo.
echo 预期显示格式:
echo   6.71 Mb/s (6705 kbps) | 1920x1080 | 59fps | H264
echo.
echo 故障排查:
echo   docker logs ps5-danmaku-monitor -f
echo   docker exec ps5-danmaku-monitor curl http://playstation-server:8081/
echo.
echo 测试XML解析:
echo   python test_xml_integration.py
echo.
pause
