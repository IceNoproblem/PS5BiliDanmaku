#!/bin/bash
# PS5-Danmaku-Docker 一键部署脚本 (NAS / 软路由 / Linux)
# 使用: bash deploy.sh
# 支持: 群晖 DSM、iStoreOS、OpenWRT (with Docker)、Ubuntu Server 等

set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

info()  { echo -e "${GREEN}[✓] $*${NC}"; }
warn()  { echo -e "${YELLOW}[!] $*${NC}"; }
error() { echo -e "${RED}[✗] $*${NC}"; }
step()  { echo -e "${BLUE}[→] $*${NC}"; }

echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  PS5-Danmaku-Docker 一键部署          ║${NC}"
echo -e "${BLUE}║  适用于 NAS / 软路由 / Linux           ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"
echo

# ── 切换到脚本所在目录 ──────────────────────────────────────────
cd "$(dirname "$(readlink -f "$0")")"

# ── 检查 Docker ──────────────────────────────────────────────────
step "检查 Docker..."
if ! command -v docker &>/dev/null; then
    error "未检测到 Docker，请先安装 Docker"
    echo "  群晖: 套件中心安装 Container Manager"
    echo "  iStoreOS: 软件包中心安装 docker"
    echo "  Ubuntu: curl -fsSL https://get.docker.com | sh"
    exit 1
fi
info "Docker 已安装: $(docker --version | head -1)"

# ── 检查 docker compose (v2 优先, 兼容 v1) ─────────────────────
step "检查 Docker Compose..."
if docker compose version &>/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
    info "Docker Compose v2 就绪"
elif command -v docker-compose &>/dev/null; then
    COMPOSE_CMD="docker-compose"
    warn "使用旧版 docker-compose，建议升级到 Docker Compose v2"
else
    error "未检测到 docker compose，请升级 Docker 或安装 docker-compose"
    exit 1
fi

# ── 创建必要目录 ─────────────────────────────────────────────────
step "创建必要目录..."
mkdir -p config/playstation data/playstation logs debug_output
info "目录已就绪"

# ── 初始化配置文件 ───────────────────────────────────────────────
step "检查配置文件..."

if [ ! -f "bili_cookies.json" ]; then
    warn "bili_cookies.json 不存在，创建空模板..."
    if [ -f "bili_cookies.example.json" ]; then
        cp bili_cookies.example.json bili_cookies.json
    else
        echo '{"SESSDATA":"","bili_jct":"","uid":0,"uname":"","saved_at":""}' > bili_cookies.json
    fi
    info "bili_cookies.json 已创建（首次部署，进入 Web 界面后扫码登录）"
fi

if [ ! -f ".env" ]; then
    warn ".env 不存在，创建默认配置..."
    # 自动检测本机 IP（NAS 环境优先用实际网卡 IP）
    HOST_IP=$(ip route get 1.1.1.1 2>/dev/null | awk '/src/{print $NF; exit}' || \
              hostname -I 2>/dev/null | awk '{print $1}' || \
              echo "auto")
    echo "EXTERNAL_IP=${HOST_IP}" > .env
    info ".env 已创建，EXTERNAL_IP=${HOST_IP}"
else
    info ".env 已存在"
fi

# ── 停止旧容器 ───────────────────────────────────────────────────
step "停止旧容器（如有）..."
$COMPOSE_CMD down --remove-orphans 2>/dev/null || true

# ── 构建并启动 ───────────────────────────────────────────────────
step "构建镜像并启动容器..."
echo "  (首次构建需要下载依赖，约 2-5 分钟，请耐心等待)"
echo
$COMPOSE_CMD up -d --build

# ── 等待服务就绪 ─────────────────────────────────────────────────
step "等待服务启动..."
echo "  (healthcheck 最长等待 ~60 秒)"
for i in $(seq 1 30); do
    sleep 2
    STATUS=$($COMPOSE_CMD ps --format json 2>/dev/null || $COMPOSE_CMD ps)
    # 检查是否有容器在 starting 状态
    if echo "$STATUS" | grep -q '"Health":"starting"' 2>/dev/null; then
        printf "  等待 healthcheck... (%ds)\r" $((i*2))
    else
        break
    fi
done
echo

# ── 输出状态 ─────────────────────────────────────────────────────
step "容器状态:"
$COMPOSE_CMD ps

# ── 获取本机 IP ───────────────────────────────────────────────────
HOST_IP=$(ip route get 1.1.1.1 2>/dev/null | awk '/src/{print $NF; exit}' || \
          hostname -I 2>/dev/null | awk '{print $1}' || \
          echo "127.0.0.1")

echo
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ 部署完成！                        ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo
echo -e "  📊 Web 控制台:  ${BLUE}http://${HOST_IP}:5000${NC}"
echo -e "  🎮 RTMP 推流地址: ${BLUE}rtmp://${HOST_IP}:1935/live${NC}"
echo -e "  📡 IRC 端口:     ${BLUE}${HOST_IP}:6667${NC}"
echo -e "  🔍 RTMP 状态页:  ${BLUE}http://${HOST_IP}:8081${NC}"
echo
echo -e "  常用命令:"
echo -e "  ${YELLOW}$COMPOSE_CMD logs -f danmaku-system${NC}   # 查看弹幕系统日志"
echo -e "  ${YELLOW}$COMPOSE_CMD logs -f rtmp-monitor${NC}     # 查看 RTMP 监控日志"
echo -e "  ${YELLOW}$COMPOSE_CMD restart rtmp-monitor${NC}     # 重启 RTMP 监控"
echo -e "  ${YELLOW}$COMPOSE_CMD down && $COMPOSE_CMD up -d${NC}  # 完全重启"
echo
warn "首次使用请访问 Web 控制台扫码登录 B站账号"
