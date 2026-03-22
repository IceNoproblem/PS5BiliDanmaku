#!/bin/bash
# 阿冰没问题（Icenoproblem）PS5 哔哩哔哩 直播系统 - Docker快速启动脚本

echo "============================================================"
echo "  阿冰没问题（Icenoproblem）PS5 哔哩哔哩 直播系统 V3.0"
echo "  Docker快速启动脚本"
echo "============================================================"
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "[错误] 未检测到Docker，请先安装Docker"
    echo "安装地址: https://docs.docker.com/engine/install/"
    exit 1
fi

# 检查Docker服务是否运行
if ! docker info &> /dev/null; then
    echo "[错误] Docker服务未运行，请启动Docker"
    exit 1
fi

echo "[1/3] 停止旧容器（如果存在）..."
docker-compose down

echo "[2/3] 构建Docker镜像..."
docker-compose build

echo "[3/3] 启动所有服务..."
docker-compose up -d

echo ""
echo "============================================================"
echo "  Docker服务启动完成！"
echo "============================================================"
echo ""
echo "服务地址："
echo "  - Web管理界面: http://127.0.0.1:5000"
echo "  - RTMP统计页面: http://127.0.0.1:8080/stat"
echo "  - 健康检查: http://127.0.0.1:8080/health"
echo ""
echo "常用命令："
echo "  - 查看服务状态: docker-compose ps"
echo "  - 查看日志: docker-compose logs -f"
echo "  - 停止服务: docker-compose down"
echo ""
