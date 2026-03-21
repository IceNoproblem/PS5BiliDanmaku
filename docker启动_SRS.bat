@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ============================================================
echo   阿冰没问题（Icenoproblem）PS5 哔哩哔哩 直播系统 V3.0
echo   Docker快速启动脚本 (使用 SRS)
echo ============================================================
echo.

REM 检查Docker是否安装
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Docker，请先安装Docker Desktop
    echo 下载地址: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)

REM 检查Docker服务是否运行
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Docker服务未运行，请启动Docker Desktop
    pause
    exit /b 1
)

echo [1/4] 停止旧容器（如果存在）...
docker-compose down

echo [2/4] 启动 SRS 服务（使用官方镜像）...
docker run -d ^
  --name ps5-danmaku-srs ^
  --network ps5-danmaku-network ^
  -p 1935:1935 ^
  -p 1985:1985 ^
  -p 8080:8080 ^
  -v %cd%\srs.conf:/usr/local/srs/conf/srs.conf:ro ^
  --restart unless-stopped ^
  ossrs/srs:5

timeout /t 3 >nul
echo [OK] SRS 服务已启动

echo [3/4] 构建弹幕转发系统镜像...
docker-compose build danmaku-system

echo [4/4] 启动所有服务...
docker-compose -f docker-compose_srs.yml up -d

echo.
echo ============================================================
echo   Docker服务启动完成！
echo ============================================================
echo.
echo 服务地址：
echo   - Web管理界面: http://127.0.0.1:5000
echo   - SRS HTTP API: http://127.0.0.1:1985
echo   - HTTP-FLV/HLS: http://127.0.0.1:8080
echo   - RTMP推流: rtmp://127.0.0.1:1935/app
echo.
echo 常用命令：
echo   - 查看服务状态: docker-compose -f docker-compose_srs.yml ps
echo   - 查看日志: docker-compose -f docker-compose_srs.yml logs -f
echo   - 停止服务: docker-compose -f docker-compose_srs.yml down
echo   - 重启服务: docker-compose -f docker-compose_srs.yml restart
echo.
echo 按任意键打开 Web 管理界面...
pause >nul
start http://127.0.0.1:5000
