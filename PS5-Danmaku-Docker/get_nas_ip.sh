#!/bin/bash
# 获取 NAS 外部 IP 地址

echo "========================================="
echo "   获取 NAS IP 地址"
echo "========================================="
echo ""

echo "可用的网络接口 IP 地址："
echo ""

# 显示所有网络接口的 IP 地址
ip addr show | grep -E "inet [0-9]" | awk '{print "  " $2}'

echo ""
echo "========================================="
echo "推荐使用以下地址（非 Docker 内部网络）："
echo ""

# 查找非 Docker 网络的 IP 地址
ip addr show | grep -E "inet [0-9]" | grep -v "172\." | grep -v "10\." | awk '{print "  " $2}'

echo ""
echo "========================================="
echo "使用方法："
echo "========================================="
echo ""
echo "1. 复制上面推荐的 IP 地址"
echo "2. 编辑 .env 文件：nano .env"
echo "3. 修改 EXTERNAL_IP=auto 为：EXTERNAL_IP=你的IP地址"
echo "4. 重启容器：docker compose up -d"
echo ""
