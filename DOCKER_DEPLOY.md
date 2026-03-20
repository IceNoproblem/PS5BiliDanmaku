# 阿冰没问题（Icenoproblem）PS5 哔哩哔哩 直播系统 - Docker部署指南

## 快速开始

### 前置要求

1. 安装Docker
   - Windows: https://docs.docker.com/desktop/install/windows-install/
   - Linux: https://docs.docker.com/engine/install/
   - macOS: https://docs.docker.com/desktop/install/mac-install/

2. 安装Docker Compose
   - Docker Desktop已包含Docker Compose

### 一键启动

```bash
# 1. 克隆或下载项目到本地
cd C:\PS5-Danmaku-System

# 2. 一键启动所有服务
docker-compose up -d

# 3. 查看服务状态
docker-compose ps

# 4. 查看日志
docker-compose logs -f
```

### 访问服务

启动成功后，可以访问以下地址：

- **Web管理界面**: http://127.0.0.1:5000
- **RTMP统计页面**: http://127.0.0.1:8080/stat
- **健康检查**: http://127.0.0.1:8080/health

## 服务说明

### 服务列表

| 服务名 | 端口 | 说明 |
|--------|------|------|
| nginx-rtmp | 1935, 8080, 80 | RTMP服务器和统计页面 |
| danmaku-system | 5000, 6667 | 弹幕转发系统和Web界面 |
| rtmp-monitor | - | RTMP监控服务 |

### 端口说明

- **1935**: RTMP推流端口（PS5推流到此端口）
- **5000**: Web管理界面
- **6667**: IRC服务端口（PS5连接到此端口）
- **8080**: RTMP统计页面
- **80**: HTTP访问（可选）

## 配置说明

### 修改配置

1. **主配置文件**: `config.json`
   ```bash
   # 修改后需要重启服务
   docker-compose restart danmaku-system
   ```

2. **B站登录凭证**: `bili_cookies.json`
   ```bash
   # 修改后需要重启服务
   docker-compose restart danmaku-system
   ```

3. **Nginx配置**: `nginx-rtmp/nginx.conf`
   ```bash
   # 修改后需要重启服务
   docker-compose restart nginx-rtmp
   ```

### 挂载目录

- `./config.json`: 主配置文件
- `./bili_cookies.json`: B站登录凭证
- `./logs`: 日志文件目录
- `./room_history.json`: 直播间历史记录

## 常用命令

### 启动/停止

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 重启某个服务
docker-compose restart danmaku-system

# 重启所有服务
docker-compose restart
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f danmaku-system
docker-compose logs -f nginx-rtmp
docker-compose logs -f rtmp-monitor

# 查看最近100行日志
docker-compose logs --tail=100
```

### 容器管理

```bash
# 查看运行状态
docker-compose ps

# 进入容器（调试用）
docker-compose exec danmaku-system bash

# 查看容器资源占用
docker stats
```

### 更新和重建

```bash
# 停止并删除容器
docker-compose down

# 重新构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

## PS5推流配置

### DNS劫持（推荐）

1. 修改PS5的DNS设置为你的电脑IP
2. 在hosts文件添加：
   ```
   live-prod-ap-northeast-1.twitch.tv 你的电脑IP
   ```
3. 启动Docker服务
4. PS5推流设置：
   - 服务器: rtmp://你的电脑IP:1935/live
   - 密钥: 任意（如：ps5_stream）

### 直接推流

1. 确保Docker服务已启动
2. PS5推流设置：
   - 服务器: rtmp://你的电脑IP:1935/live
   - 密钥: 任意（如：ps5_stream）

### IRC连接配置

1. 在PS5的Twitch设置中配置IRC：
   - 服务器: 你的电脑IP
   - 端口: 6667
   - 频道名: #你的Twitch频道名

## 故障排查

### 服务无法启动

```bash
# 查看详细日志
docker-compose logs

# 检查端口占用
netstat -ano | findstr "1935 5000 6667 8080"
```

### 无法访问Web界面

```bash
# 检查服务状态
docker-compose ps

# 查看弹幕系统日志
docker-compose logs danmaku-system

# 尝试重启
docker-compose restart danmaku-system
```

### RTMP推流失败

```bash
# 检查nginx-rtmp服务
docker-compose logs nginx-rtmp

# 检查RTMP端口
curl http://127.0.0.1:8080/stat

# 检查防火墙
# Windows: 控制面板 -> Windows Defender 防火墙 -> 高级设置
# 允许端口 1935, 5000, 6667, 8080
```

### 弹幕不显示

```bash
# 检查B站登录凭证
cat bili_cookies.json

# 查看弹幕系统日志
docker-compose logs danmaku-system | grep ERROR

# 重新配置B站登录
# 1. 访问 http://127.0.0.1:5000
# 2. 点击"登录B站"
# 3. 扫码登录
```

## 生产环境部署

### 修改端口（避免冲突）

编辑 `docker-compose.yml`:

```yaml
ports:
  - "5001:5000"    # 将5000改为5001
  - "6668:6667"    # 将6667改为6668
```

### 使用域名

1. 购买域名并配置DNS
2. 配置Nginx反向代理
3. 使用SSL证书（Let's Encrypt）

### 限制推流IP

编辑 `nginx-rtmp/nginx.conf`:

```nginx
allow publish 你的电脑IP;
allow publish PS5的IP;
deny publish all;
```

### 日志管理

编辑 `docker-compose.yml`:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## 性能优化

### 资源限制

编辑 `docker-compose.yml`:

```yaml
services:
  danmaku-system:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

### 数据库优化（可选）

对于高并发场景，可以添加Redis：
```yaml
  redis:
    image: redis:alpine
    container_name: ps5-danmaku-redis
    restart: unless-stopped
    networks:
      - ps5-danmaku-network
```

## 技术支持

- GitHub Issues: https://github.com/IceNoproblem/PS5BiliDanmaku/issues
- B站空间: https://space.bilibili.com/31517300

## 许可证

MIT License
