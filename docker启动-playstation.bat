@echo off
chcp 65001 >nul
title PS5 弹幕系统 - 启动 (bao3/playstation)
cd /d "%~dp0"

echo ============================================================
echo   PS5 弹幕系统 Docker 版本
echo   使用 bao3/playstation RTMP 服务器
echo ============================================================
echo.

echo [1/4] 检查 Docker 环境...
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到 Docker，请先安装 Docker Desktop
    pause
    exit /b 1
)
echo [OK] Docker 已安装
echo.

echo [2/4] 拉取最新镜像...
echo 正在拉取 bao3/playstation 镜像...
docker pull bao3/playstation:latest
echo [OK] 镜像拉取完成
echo.

echo [3/4] 启动 Docker 容器...
docker-compose -f docker-compose-playstation.yml up -d
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 容器启动失败
    pause
    exit /b 1
)
echo [OK] 容器已启动
echo.

echo [4/4] 等待服务就绪...
timeout /t 5 >nul
echo [OK] 服务启动完成
echo.

echo ============================================================
echo   访问地址：
echo     Web 管理界面: http://127.0.0.1:5000
echo     PlayStation 管理界面: http://127.0.0.1:8888
echo ============================================================
echo.
echo 推流地址示例：
echo   rtmp://localhost:1935/app/live_xxxxxxxxxxxxxxx
echo   (具体串流密钥请访问 PlayStation 管理界面查看)
echo.
echo 按任意键打开 Web 界面...
pause >nul
start http://127.0.0.1:5000

echo.
echo 系统正在后台运行。
echo 如需停止服务，请运行 "docker停止-playstation.bat"
echo.
pause
