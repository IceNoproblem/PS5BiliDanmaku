@echo off
chcp 65001 >nul
echo ==================== 实时码率监控部署脚本 ====================
echo.
echo 更新内容:
echo   - 支持 6.36 Mb/s 等带小数点的格式
echo   - 监控间隔改为2秒(更频繁采集)
echo   - 同时显示 Mb/s 和 kbps
echo   - 日志显示实时变化
echo.

cd /d D:\PS5-Danmaku-Docker

echo [步骤1] 检查Docker容器状态...
docker ps --filter "name=ps5-danmaku-monitor" --format "table {{.Names}}\t{{.Status}}"
docker ps --filter "name=ps5-danmaku-system" --format "table {{.Names}}\t{{.Status}}"
echo.

echo [步骤2] 重新构建并启动容器(应用新代码)...
docker-compose up -d --build rtmp-monitor
echo.

echo [步骤3] 等待容器启动(10秒)...
timeout /t 10 /nobreak >nul
echo.

echo [步骤4] 查看实时日志(Ctrl+C退出)...
echo ==================== 实时码率监控日志 ====================
echo.
echo 日志格式: [实时] stream_key | 分辨率 | fps | Mb/s (kbps)
echo 码率会根据实际推流情况实时变化(如 6.36, 6.42, 5.98...)
echo.
docker logs -f ps5-danmaku-monitor 2>&1
