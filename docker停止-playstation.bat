@echo off
chcp 65001 >nul
title PS5 弹幕系统 - 停止 (bao3/playstation)
cd /d "%~dp0"

echo ============================================================
echo   PS5 弹幕系统 Docker 版本
echo   停止所有服务
echo ============================================================
echo.

echo [1/3] 停止 Docker 容器...
docker-compose -f docker-compose-playstation.yml down
if %ERRORLEVEL% EQU 0 (
    echo [OK] 容器已停止
) else (
    echo [警告] 容器停止失败，可能已停止
)
echo.

echo [2/3] 清理镜像 (可选)...
echo 如需清理 bao3/playstation 镜像，请手动运行:
echo   docker rmi bao3/playstation:latest
echo.

echo [3/3] 检查容器状态...
docker ps -a --filter "name=ps5-"
echo.

echo ============================================================
echo   停止完成
echo ============================================================
echo.
pause
