# PS5 哔哩哔哩 直播系统 - Docker 版本（SRS）

## 简介

Docker 版本使用 **SRS (Simple Realtime Server)** 作为 RTMP 流媒体服务器，性能更强、延迟更低、支持更高码率。

**主要特性：**
- ✅ 使用 SRS 5.x 官方镜像
- ✅ Docker Compose 一键部署
- ✅ 支持高码率推流（1080p 60fps + HDR）
- ✅ 低延迟（HTTP-FLV <1s）
- ✅ 多协议支持（RTMP、HTTP-FLV、HLS）
- ✅ 完整的 Web 管理界面
- ✅ 容器自动重启
- ✅ 数据持久化

## 目录结构

```
D:\PS5-Danmaku-Docker\
├── danmaku_forward.py    # 弹幕转发主程序
├── monitor_rtmp.py       # RTMP 推流监控（已适配 SRS）
├── Dockerfile           # 弹幕系统镜像定义
├── docker-compose_srs.yml # SRS 版本 Docker Compose 配置（新增）
├── srs.conf             # SRS 配置文件（新增）
├── config.json          # 主配置文件
├── bili_cookies.json    # B站登录凭证
├── requirements.txt      # Python 依赖
├── docker启动_SRS.bat    # Windows 快速启动（新增）
├── docker停止_SRS.bat    # Windows 快速停止（新增）
├── docker-start.sh      # Linux/macOS 启动脚本
└── README_SRS.md        # 本文档
```

## 快速开始

### 前置要求

- Docker Desktop（Windows）或 Docker + Docker Compose（Linux/macOS）
- 至少 2GB 可用内存
- 至少 5GB 可用磁盘空间

### Windows 一键部署

1. 双击运行 **`docker启动_SRS.bat`**
2. 等待镜像拉取和容器启动
3. 自动打开 Web 管理界面：http://127.0.0.1:5000

### Linux/macOS 部署

```bash
# 赋予执行权限
chmod +x docker-start.sh

# 启动所有服务
./docker-start.sh
```

### 手动部署

```bash
# 启动 SRS 和所有服务
docker-compose -f docker-compose_srs.yml up -d

# 查看服务状态
docker-compose -f docker-compose_srs.yml ps

# 查看日志
docker-compose -f docker-compose_srs.yml logs -f

# 停止服务
docker-compose -f docker-compose_srs.yml down
```

## 服务说明

### SRS 服务器 (srs-server)
- **镜像：** `ossrs/srs:5`
- **端口映射：**
  - 1935:1935（RTMP 推流）
  - 1985:1985（HTTP API）
  - 8080:8080（HTTP-FLV/HLS）
- **配置挂载：** `./srs.conf:/usr/local/srs/conf/srs.conf:ro`
- **重启策略：** unless-stopped

### 弹幕转发系统 (danmaku-system)
- **镜像：** 从 Dockerfile 构建
- **端口映射：**
  - 5000:5000（Web 管理界面）
  - 6667:6667（IRC 服务）
- **配置挂载：**
  - `./config.json:/app/config.json`
  - `./bili_cookies.json:/app/bili_cookies.json`
  - `./logs:/app/logs`
  - `./room_history.json:/app/room_history.json`
- **依赖：** srs-server
- **环境变量：**
  - `SRS_HOST=srs-server`
  - `SRS_PORT=1935`
- **重启策略：** unless-stopped

### RTMP 监控 (rtmp-monitor)
- **镜像：** 从 Dockerfile 构建
- **命令：** `python monitor_rtmp.py`
- **配置挂载：**
  - `./config.json:/app/config.json`
  - `./logs:/app/logs`
- **依赖：** srs-server、danmaku-system
- **环境变量：**
  - `RTMP_MONITOR_URL=http://srs-server:1985/api/v1/streams/`
  - `DANMAKU_API_URL=http://danmaku-system:5000/api/rtmp/status/update`
  - `DOCKER_ENV=true`
  - `RTMP_SERVER_TYPE=srs`
- **重启策略：** unless-stopped

## PS5 推流配置

### 1. DNS 劫持

在你的路由器上配置 DNS 劫持：

```
address=/live.twitch.tv/你的NAS/电脑IP
address=/.live-video.net/你的NAS/电脑IP
```

### 2. PS5 开启直播

1. PS5 设置 → 串流
2. 绑定 Twitch 账号
3. 开始直播
4. 流量自动推流到 SRS 服务器

### 3. 查看推流状态

访问 http://你的IP:1985 查看流状态和统计信息

## 配置说明

### SRS 配置文件 (srs.conf)

```nginx
listen              1935;
max_connections     1000;
daemon              off;
srs_log_tank        console;

http_api {
    listen         1985;
    enabled        on;
    stats {
        enabled        on;
    }
}

http_server {
    listen         8080;
    dir            ./objs/nginx/html;
}

vhost __defaultVhost__ {
    hls {
        enabled         on;
        hls_path       ./objs/nginx/html;
        hls_fragment    2;
        hls_window     30;
    }

    http_remux {
        enabled on;
        mount [vhost]/[app]/[stream].flv;
    }
}
```

### 关键参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| listen | 1935 | RTMP 监听端口 |
| max_connections | 1000 | 最大并发连接数 |
| hls_fragment | 2 | HLS 分片时长（秒） |
| hls_window | 30 | HLS 窗口时长（秒） |

## 常用命令

### 查看服务状态
```bash
docker-compose -f docker-compose_srs.yml ps
```

### 查看日志
```bash
# 查看所有服务日志
docker-compose -f docker-compose_srs.yml logs -f

# 查看特定服务日志
docker-compose -f docker-compose_srs.yml logs -f srs-server
docker-compose -f docker-compose_srs.yml logs -f danmaku-system
docker-compose -f docker-compose_srs.yml logs -f rtmp-monitor
```

### 重启服务
```bash
docker-compose -f docker-compose_srs.yml restart
```

### 停止服务
```bash
docker-compose -f docker-compose_srs.yml down
```

### 进入容器
```bash
docker exec -it ps5-danmaku-srs /bin/bash
docker exec -it ps5-danmaku-system /bin/bash
```

## 性能优势对比

| 指标 | bao3/playstation | nginx-rtmp | SRS 5.x |
|------|-----------------|-------------|----------|
| **并发连接数** | ~1000 | ~1000 | **10000+** |
| **延迟** | 2-3s | 2-5s | **<1s** |
| **内存占用** | ~100MB | ~150MB | **~80MB** |
| **CPU 占用** | 中等 | 中等 | **较低** |
| **码率支持** | 优秀 | 一般 | **超高码率** |
| **维护状态** | 停止（4年未更新） | 停止（2018） | **活跃维护（2026）** |

## 常见问题

### Q: 如何使用旧版 nginx-rtmp？
A: 使用原来的 `docker-compose.yml` 即可，不用 `docker-compose_srs.yml`。

### Q: 推流画面不清晰怎么办？
A: SRS 支持更高码率，请检查：
   1. PS5 推流设置中的码率是否已调至最高
   2. 网络带宽是否充足（建议 15+ Mbps 上传）
   3. 查看实际推流码率：http://127.0.0.1:1985

### Q: 容器无法启动怎么办？
A: 检查以下几点：
   1. 端口是否被占用（1935、1985、8080、5000、6667）
   2. 配置文件路径是否正确
   3. 查看容器日志：`docker-compose logs srs-server`

### Q: RTMP 监控不工作？
A: 检查：
   1. SRS 容器是否正常运行
   2. 环境变量 `RTMP_MONITOR_URL` 是否正确
   3. 检查 rtmp-monitor 容器日志

### Q: 如何升级 SRS 版本？
A:
```bash
# 停止服务
docker-compose -f docker-compose_srs.yml down

# 修改 docker-compose_srs.yml 中的镜像版本
# 例如：image: ossrs/srs:5

# 重新启动
docker-compose -f docker-compose_srs.yml up -d
```

## 版本历史

### V2.0 (2026-03-21)
- ✅ 替换 nginx-rtmp 为 SRS
- ✅ 使用官方 SRS 5.x 镜像
- ✅ 更新监控脚本适配 SRS API
- ✅ 优化高码率推流性能
- ✅ 添加新的 docker-compose_srs.yml
- ✅ 更新部署脚本

### V1.0
- 初始版本（使用 nginx-rtmp）

## 技术支持

- SRS 官方文档：https://ossrs.io/lts/zh-cn/
- SRS GitHub：https://github.com/ossrs/srs
- Docker Hub：https://hub.docker.com/r/ossrs/srs

---

**使用愉快！如有问题请查看 SRS 官方文档。**
