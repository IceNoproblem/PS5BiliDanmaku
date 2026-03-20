@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ============================================================
echo   停止Docker服务
echo ============================================================
echo.

echo 正在停止所有Docker容器...
docker-compose down

echo.
echo 所有服务已停止。
echo.
pause
