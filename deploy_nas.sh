#!/bin/bash
# NAS 部署自动配置脚本
# 用于在 NAS 上一键部署和修复 PS5 Bilibili Danmaku

set -e  # 遇到错误立即退出

echo "========================================="
echo "PS5 Bilibili Danmaku - NAS 部署脚本"
echo "========================================="
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

echo "✅ Docker 环境检查通过"
echo ""

# 进入项目目录
cd "$(dirname "$0")"

echo "📂 当前目录: $(pwd)"
echo ""

# 停止现有容器
echo "🛑 停止现有容器..."
docker compose down 2>/dev/null || true
echo ""

# 重新构建镜像（包含 brotli）
echo "🔨 重新构建镜像（安装 brotli）..."
docker compose build --no-cache
echo ""

# 启动容器
echo "🚀 启动容器..."
docker compose up -d
echo ""

# 等待容器启动
echo "⏳ 等待容器启动..."
sleep 5

# 检查容器状态
echo "📊 容器状态:"
docker compose ps
echo ""

# 显示访问地址
echo "========================================="
echo "✅ 部署完成！"
echo "========================================="
echo ""
echo "📋 访问地址:"
echo ""
echo "🌐 Web 管理界面:  http://$(hostname -I | awk '{print $1}'):5000"
echo "📡 IRC 服务器:     $(hostname -I | awk '{print $1}'):6667"
echo "🎬 RTMP 推流:     rtmp://$(hostname -I | awk '{print $1}'):1935/live"
echo "📊 RTMP 统计:     http://$(hostname -I | awk '{print $1}'):8080/stat"
echo ""
echo "========================================="
echo "📝 下一步:"
echo "========================================="
echo "1. 访问 Web 界面进行配置"
echo "2. 配置 DNS 劫持（将 Twitch 域名解析到 NAS IP）"
echo "3. PS5 开启直播测试"
echo "4. 使用 OBS 或直播姬拉流到 B站"
echo ""
echo "💡 提示: 查看日志使用命令: docker compose logs -f"
echo ""
