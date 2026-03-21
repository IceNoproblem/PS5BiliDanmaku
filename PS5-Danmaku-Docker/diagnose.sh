#!/bin/bash
# Docker 容器诊断脚本

echo "========================================="
echo "   PS5 Bilibili Danmaku - 诊断脚本"
echo "========================================="
echo ""

# 1. 检查所有容器状态
echo "1. 容器状态："
echo "-----------------------------------"
docker compose ps
echo ""

# 2. 检查 playstation-server 容器日志
echo "2. playstation-server 日志："
echo "-----------------------------------"
docker logs ps5-playstation-server --tail 20
echo ""

# 3. 检查容器网络连接
echo "3. 容器网络测试："
echo "-----------------------------------"
echo "从 ps5-danmaku-monitor 测试连接 playstation-server:80"
docker exec ps5-danmaku-monitor ping -c 2 playstation-server 2>/dev/null || echo "  ❌ 无法 ping 通 playstation-server"
docker exec ps5-danmaku-monitor wget -O- --timeout=2 http://playstation-server:80 2>&1 | head -5
echo ""

# 4. 检查 playstation-server 内部网络
echo "4. playstation-server 内部状态："
echo "-----------------------------------"
docker exec ps5-playstation-server ps aux | grep nginx || echo "  ❌ nginx 未运行"
docker exec ps5-playstation-server netstat -tlnp 2>/dev/null | grep -E ':(80|1935)' || echo "  ❌ 端口未监听"
echo ""

# 5. 检查配置文件
echo "5. 配置文件检查："
echo "-----------------------------------"
docker exec ps5-playstation-server cat /etc/nginx/nginx.conf | head -30
echo ""

# 6. 检查 Docker 网络
echo "6. Docker 网络信息："
echo "-----------------------------------"
docker network inspect ps5-bilibili-danmaku_ps5-danmaku-network --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{"\n"}}{{end}}'
echo ""

echo "========================================="
echo "   诊断完成"
echo "========================================="
