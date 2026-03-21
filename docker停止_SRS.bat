@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ============================================================
echo   阿冰没问题（Icenoproblem）PS5 哔哩哔哩 直播系统 V3.0
echo   停止 Docker 服务
echo ============================================================
echo.

echo 停止所有 Docker 容器...
docker-compose -f docker-compose_srs.yml down

echo.
echo ============================================================
echo   所有服务已停止
echo ============================================================
echo.
pause
