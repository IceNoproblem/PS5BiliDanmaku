@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ============================================================
echo   阿冰没问题（Icenoproblem）PS5 哔哩哔哩 直播系统 V3.0
echo   Docker快速启动脚本
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

echo [1/3] 停止旧容器（如果存在）...
docker-compose down

echo [2/3] 构建Docker镜像...
docker-compose build

echo [3/3] 启动所有服务...
docker-compose up -d

echo.
echo ============================================================
echo   Docker服务启动完成！
echo ============================================================
echo.
echo 服务地址：
echo   - Web管理界面: http://127.0.0.1:5000
echo   - RTMP统计页面: http://127.0.0.1:8080/stat
echo   - 健康检查: http://127.0.0.1:8080/health
echo.
echo 常用命令：
echo   - 查看服务状态: docker-compose ps
echo   - 查看日志: docker-compose logs -f
echo   - 停止服务: docker-compose down
echo.
echo 按任意键打开Web管理界面...
pause > nul

start http://127.0.0.1:5000

echo.
echo Web界面已打开。
echo 详细使用说明请查看：DOCKER_DEPLOY.md
echo.
