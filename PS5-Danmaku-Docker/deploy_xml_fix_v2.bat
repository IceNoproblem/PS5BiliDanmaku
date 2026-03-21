@echo off
chcp 65001 >nul
echo ==================== XML 解析修复部署脚本 v2 ====================
echo.
echo 正在部署 XML 格式解析修复...
echo.

cd /d D:\PS5-Danmaku-Docker

echo [步骤1] 检查 Docker 容器状态...
docker ps --filter "name=ps5" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.

echo [步骤2] 停止并删除 rtmp-monitor 容器...
docker stop ps5-danmaku-monitor 2>nul
docker rm ps5-danmaku-monitor 2>nul
echo.

echo [步骤3] 重新启动服务...
docker-compose up -d rtmp-monitor
echo.

echo [步骤4] 等待容器启动(20秒)...
timeout /t 20 /nobreak >nul
echo.

echo [步骤5] 查看容器日志(最近50行)...
echo ==================== monitor_rtmp日志 ====================
docker logs ps5-danmaku-monitor --tail 50 2>&1
echo.

echo [步骤6] 检查容器内部网络连接...
echo 正在测试容器间连接...
docker exec ps5-danmaku-monitor ping -c 2 playstation-server 2>nul
if errorlevel 1 (
    echo [警告] 容器间网络连接失败
) else (
    echo [成功] 容器间网络连接正常
)
echo.

echo [步骤7] 测试 RTMP 统计页面访问...
echo 正在从容器内部访问 playstation-server:8081...
docker exec ps5-danmaku-monitor curl -s http://playstation-server:8081/ 2>&1 | findstr /C:"bw_video" /C:"bw_audio" /C:"bw_in"
echo.

echo [步骤8] 测试弹幕系统 API...
echo 正在测试 http://localhost:5000/api/rtmp/status ...
curl -s http://localhost:5000/api/rtmp/status
echo.
echo.

echo ==================== 部署完成 ====================
echo.
echo 修改内容:
echo ✓ monitor_rtmp.py - 使用 XML 解析替代 HTML 表格解析
echo ✓ docker-compose.yml - 修正端口从 80 改为 8081
echo ✓ 添加 re 模块导入
echo.
echo 验证步骤:
echo 1. 检查日志中是否显示: [INFO] 检测到视频码率: X.XX Mb/s (XXXX kbps)
echo 2. 访问 http://localhost:5000
echo 3. 确认Web界面 RTMP 部分正常显示
echo 4. 确认码率显示正确(不再是 -)
echo.
echo 预期显示格式:
echo   6.71 Mb/s (6705 kbps) | 1920x1080 | 59fps | H264
echo.
echo 如果 RTMP 部分完全不显示,请检查:
echo 1. PS5 是否正在推流
echo 2. playstation-server 容器是否正常运行
echo 3. 端口 8081 是否正确映射
echo.
echo 故障排查命令:
echo   docker logs ps5-danmaku-monitor -f
echo   docker exec ps5-danmaku-monitor curl http://playstation-server:8081/
echo   docker exec ps5-danmaku-monitor ping playstation-server
echo   python test_local_xml.py
echo.
pause
