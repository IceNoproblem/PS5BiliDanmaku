# 阿冰没问题（Icenoproblem）PS5 哔哩哔哩 直播系统 - Docker版本

## 🚀 一键部署

### Windows用户

1. 安装 [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
2. 双击运行 `docker启动.bat`
3. 等待启动完成，自动打开Web管理界面

### Linux用户

1. 安装 [Docker](https://docs.docker.com/engine/install/) 和 [Docker Compose](https://docs.docker.com/compose/install/)
2. 运行启动脚本：
   ```bash
   chmod +x docker-start.sh
   ./docker-start.sh
   ```
3. 访问 http://127.0.0.1:5000

### macOS用户

1. 安装 [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
2. 使用Linux启动脚本或手动命令：
   ```bash
   docker-compose up -d
   ```
3. 访问 http://127.0.0.1:5000

## 📦 服务架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  nginx-rtmp  │  │ danmaku-     │  │ rtmp-        │      │
│  │  (1935,8080) │←→│ system       │←→│ monitor      │      │
│  │              │  │ (5000,6667)  │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↑                  ↑                  ↑            │
│         │                  │                  │            │
│    PS5推流            Web界面            监控服务            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 配置说明

### 快速配置

首次使用需要配置B站登录：

1. 访问 http://127.0.0.1:5000
2. 点击"登录B站"
3. 扫描二维码登录
4. 配置PS5推流和IRC参数

### 端口说明

| 端口 | 用途 | 说明 |
|------|------|------|
| 1935 | RTMP推流 | PS5推流到此端口 |
| 5000 | Web管理 | 系统管理界面 |
| 6667 | IRC服务 | PS5 IRC连接 |
| 8080 | RTMP统计 | 推流状态监控 |
| 80 | HTTP | 可选的HTTP服务 |

## 📝 常用命令

### 启动/停止

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 重启服务
docker-compose restart

# 重启特定服务
docker-compose restart danmaku-system
```

### 查看日志

```bash
# 查看所有日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f danmaku-system
docker-compose logs -f nginx-rtmp
docker-compose logs -f rtmp-monitor

# 查看最近日志
docker-compose logs --tail=100
```

### 容器管理

```bash
# 查看运行状态
docker-compose ps

# 进入容器调试
docker-compose exec danmaku-system bash

# 查看资源占用
docker stats
```

## 🎯 PS5配置

### 推流设置

在PS5的推流设置中：
- **服务器**: `rtmp://你的电脑IP:1935/live`
- **密钥**: 任意（如：`ps5_stream`）

### IRC设置

在PS5的Twitch IRC设置中：
- **服务器**: 你的电脑IP
- **端口**: 6667
- **频道名**: `#你的Twitch频道名`

## 🔍 故障排查

### 服务无法启动

```bash
# 查看详细日志
docker-compose logs

# 检查Docker服务
docker ps -a
```

### 无法访问Web界面

```bash
# 检查服务状态
docker-compose ps

# 重启弹幕系统
docker-compose restart danmaku-system

# 查看日志
docker-compose logs danmaku-system
```

### RTMP推流失败

```bash
# 检查nginx-rtmp服务
docker-compose logs nginx-rtmp

# 测试RTMP端口
curl http://127.0.0.1:8080/stat

# 检查防火墙
# Windows: 控制面板 -> Windows Defender 防火墙
# Linux: sudo ufw status
```

## 📚 详细文档

完整的部署和使用说明请查看 [DOCKER_DEPLOY.md](DOCKER_DEPLOY.md)

## 🌟 优势

相比Windows版本，Docker版本具有以下优势：

- ✅ **环境隔离**：不依赖本地Python环境
- ✅ **一键部署**：自动处理所有依赖
- ✅ **跨平台**：Windows/Linux/macOS通用
- ✅ **易于维护**：统一的管理和升级
- ✅ **资源隔离**：不会影响系统其他服务

## 💡 提示

- 确保Docker Desktop正在运行
- 首次构建镜像需要几分钟
- 配置文件修改后需要重启服务
- 建议定期备份数据目录

## 📞 技术支持

- GitHub: https://github.com/IceNoproblem/PS5BiliDanmaku
- B站空间: https://space.bilibili.com/31517300

## 📄 许可证

MIT License
