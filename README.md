# PS5BiliDanmaku - Docker 版本

<div align="center">

**把 Bilibili 直播弹幕转发到 PS5 的轻量工具**

![Version](https://img.shields.io/badge/version-v1.0.0-blue)
![Docker](https://img.shields.io/badge/docker-supported-brightgreen)
![License](https://img.shields.io/badge/license-GPL--3.0-green)

**容器化一键部署 | 跨平台支持 | 环境隔离**

[快速开始](#快速开始) • [详细部署](#详细部署指南) • [常见问题](#常见问题) • [更新日志](#版本更新日志)

</div>

---

## 📖 项目简介

PS5BiliDanmaku 是一款轻量级工具，通过 IRC 协议将 B 站直播弹幕转发到 PS5。Docker 版本提供容器化部署，一键启动所有服务，完美支持 Linux、Windows 和 macOS 系统。

### ✨ 核心功能

- ✅ **实时弹幕抓取与转发**：支持去重，延迟极低
- ✅ **全 Web 可视化配置**：http://localhost:5000，无需命令行
- ✅ **Docker 容器化部署**：环境隔离，一键启动
- ✅ **内置 RTMP 推流服务器**：支持 PS5 不使用采集卡进行直播
- ✅ **跨平台支持**：Windows、Linux、macOS 统一部署
- ✅ **自动重启机制**：服务异常自动恢复
- ✅ **数据持久化**：配置和日志自动保存

---

## 🎯 系统要求

### 硬件要求

- **CPU**：双核及以上
- **内存**：2GB 及以上
- **磁盘**：5GB 可用空间

### 软件要求

- **操作系统**：Windows 10/11、Ubuntu 18.04+、CentOS 7+、macOS 10.14+
- **Docker**：20.0 及以上
- **Docker Compose**：2.0 及以上
- **网络**：PS5 与部署设备在同一局域网

### 端口要求

请确保以下端口未被占用：

| 端口 | 用途 | 说明 |
|------|------|------|
| 1935 | RTMP 推流 | PS5 推流端口 |
| 5000 | Web 管理界面 | 配置和监控 |
| 6667 | IRC 服务 | PS5 IRC 连接 |
| 8080 | RTMP 统计页面 | 推流状态监控 |
| 80 | HTTP 服务（可选） | 访问统计页面 |

---

## 🚀 快速开始

### Windows 用户

#### 前置步骤

1. **安装 Docker Desktop**

   下载地址：https://www.docker.com/products/docker-desktop/

2. **启动 Docker Desktop**

   安装完成后，启动 Docker Desktop 并等待状态变为 "Docker Desktop is running"

#### 一键启动

```bash
# 双击运行
docker启动.bat
```

脚本会自动完成：
- ✅ 检查 Docker 是否安装
- ✅ 检查 Docker 服务状态
- ✅ 停止旧容器
- ✅ 构建新镜像
- ✅ 启动所有服务
- ✅ 自动打开 Web 管理界面

#### 验证部署

1. 访问 http://localhost:5000
2. 看到 Web 界面表示部署成功
3. 查看 Docker 容器状态：
   ```bash
   docker-compose ps
   ```

---

### Linux/macOS 用户

#### 前置步骤

**Ubuntu/Debian：**
```bash
# 更新软件包
sudo apt update

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo apt install docker-compose-plugin

# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER
newgrp docker
```

**CentOS/RHEL：**
```bash
# 安装 Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker

# 安装 Docker Compose
sudo yum install docker-compose-plugin
```

**macOS：**

下载 Docker Desktop：https://www.docker.com/products/docker-desktop/

#### 一键启动

```bash
# 赋予执行权限
chmod +x docker-start.sh

# 运行启动脚本
./docker-start.sh
```

#### 验证部署

1. 访问 http://localhost:5000
2. 查看 Docker 容器状态：
   ```bash
   docker-compose ps
   ```

---

## 📚 详细部署指南

### 架构说明

```
┌─────────────────────────────────────────────────┐
│              Docker Compose                       │
├─────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐            │
│  │  nginx-rtmp  │←→│ danmaku-     │            │
│  │  (1935,8080, │  │ system      │            │
│  │   80)        │  │ (5000,6667)  │            │
│  └──────────────┘  └──────────────┘            │
│        ↑                     ↑                 │
│        └─────────────────────┘                 │
│              ↓                                  │
│       ┌─────────────┐                          │
│       │ rtmp-monitor│                          │
│       └─────────────┘                          │
└─────────────────────────────────────────────────┘
```

### 服务说明

#### 1. nginx-rtmp（RTMP 服务器）

- **作用**：接收 PS5 的 RTMP 推流
- **端口**：1935（推流）、8080（统计）、80（HTTP）
- **镜像**：tiangolo/nginx-rtmp
- **配置**：nginx-rtmp/nginx.conf

#### 2. danmaku-system（弹幕转发系统）

- **作用**：抓取 B 站弹幕并通过 IRC 转发到 PS5
- **端口**：5000（Web）、6667（IRC）
- **镜像**：自定义 Python 镜像
- **核心文件**：danmaku_forward.py

#### 3. rtmp-monitor（推流监控）

- **作用**：监控 RTMP 推流状态并更新到 Web 界面
- **端口**：无（内部通信）
- **镜像**：同 danmaku-system
- **核心文件**：monitor_rtmp.py

### 手动部署步骤

如果不想使用自动脚本，可以手动执行：

#### 步骤 1：克隆或下载项目

```bash
# 如果有 Git
git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
cd PS5BiliDanmaku

# 或者直接下载解压
unzip PS5BiliDanmaku-docker.zip
cd PS5BiliDanmaku-docker
```

#### 步骤 2：构建镜像

```bash
# 构建所有服务的镜像
docker-compose build

# 或者只构建特定服务
docker-compose build danmaku-system
```

首次构建可能需要 5-10 分钟，取决于网络速度。

#### 步骤 3：启动服务

```bash
# 启动所有服务（后台运行）
docker-compose up -d

# 启动所有服务（前台运行，可查看日志）
docker-compose up

# 启动特定服务
docker-compose up -d danmaku-system
```

#### 步骤 4：查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f danmaku-system

# 查看最近 100 行日志
docker-compose logs --tail=100
```

#### 步骤 5：验证服务状态

```bash
# 查看容器状态
docker-compose ps

# 检查端口占用
netstat -tlnp | grep -E "1935|5000|6667|8080"

# 测试 Web 界面
curl http://localhost:5000

# 测试 RTMP 统计页面
curl http://localhost:8080/stat
```

---

## ⚙️ 配置说明

### 首次配置

1. **访问 Web 管理界面**

   打开浏览器访问：http://localhost:5000

2. **配置 B站直播间**

   - 输入 B站直播间 ID（例如：31517300）
   - 点击"保存配置"

3. **配置 PS5 IRC 连接**

   - 服务器地址：部署设备的局域网 IP（例如：192.168.1.100）
   - 端口：6667
   - 频道名：#PS5频道名（必须加 # 号）

4. **其他配置（可选）**

   - IRC 超时时间：默认 5 小时（18000 秒）
   - 保留弹幕数量：默认 100 条
   - 保留礼物数量：默认 20 个
   - 保留日志数量：默认 50 条
   - 重连延迟：默认 10 秒

### 配置文件位置

配置文件保存在宿主机（容器外部），删除容器不会丢失：

```bash
# Windows
D:\PS5-Danmaku-Docker\logs\config.json

# Linux/macOS
./logs/config.json
```

### 修改配置

**方法一：通过 Web 界面修改**

1. 访问 http://localhost:5000
2. 修改配置参数
3. 点击"保存配置"

**方法二：直接编辑配置文件**

1. 停止服务：
   ```bash
   docker-compose down
   ```

2. 编辑配置文件：
   ```bash
   # Windows
   notepad logs\config.json

   # Linux/macOS
   vim logs/config.json
   ```

3. 重启服务：
   ```bash
   docker-compose up -d
   ```

---

## 🎮 PS5 推流配置

### 步骤 1：配置 DNS 重定向

PS5 推流使用 Twitch 的 RTMP 服务器，需要通过 DNS 劫持将 Twitch 的推流地址重定向到本地。

#### 方法一：路由器 DNS 劫持（推荐）

1. **登录路由器管理界面**

   通常是 192.168.1.1 或 192.168.0.1

2. **添加 DNS 重定向规则**

   | 域名 | 类型 | 值 |
  ------|------|-----|
   | live.twitch.tv | A | 你的服务器 IP |
   | video-weaver.twitch.tv | A | 你的服务器 IP |

3. **保存并重启路由器**

#### 方法二：本地 hosts 文件（仅限本地测试）

修改 hosts 文件添加：

```
# Windows
C:\Windows\System32\drivers\etc\hosts

# Linux/macOS
/etc/hosts
```

添加内容：
```
服务器IP    live.twitch.tv
服务器IP    video-weaver.twitch.tv
```

### 步骤 2：PS5 开启直播

1. **安装 Twitch 应用**（PS5 应用商店）

2. **登录 Twitch 账号**

3. **选择要直播的游戏或应用**

4. **点击开始直播**

   PS5 会推流到本地服务器（通过 DNS 重定向）

### 步骤 3：OBS/直播姬拉流

#### OBS Studio

1. **添加媒体源**

   来源 → + → 媒体源

2. **输入 RTMP 地址**

   ```
   rtmp://服务器IP/live/PS5推流码
   ```

3. **开始推流**

#### 直播姬

1. **添加直播源**

   直播设置 → 直播源

2. **输入 RTMP 地址**

   ```
   服务器：rtmp://服务器IP/live
   串流密钥：PS5推流码
   ```

3. **开始直播**

---

## 🔧 常用命令

### Docker Compose 命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f

# 查看容器状态
docker-compose ps

# 构建镜像
docker-compose build

# 重新构建并启动
docker-compose up -d --build

# 删除所有容器和镜像
docker-compose down --rmi all

# 查看资源占用
docker-compose top
```

### Docker 原生命令

```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括已停止）
docker ps -a

# 查看容器日志
docker logs <容器ID>

# 进入容器
docker exec -it <容器ID> /bin/bash

# 查看容器资源占用
docker stats

# 删除容器
docker rm <容器ID>

# 删除镜像
docker rmi <镜像ID>
```

---

## 🔍 故障排查

### 问题 1：容器无法启动

**症状**：`docker-compose up` 失败

**解决方案**：

1. 检查端口是否被占用：
   ```bash
   netstat -tlnp | grep -E "1935|5000|6667|8080"
   ```

2. 查看容器日志：
   ```bash
   docker-compose logs
   ```

3. 检查 Docker 是否正常运行：
   ```bash
   docker info
   ```

### 问题 2：Web 界面无法访问

**症状**：http://localhost:5000 无法打开

**解决方案**：

1. 检查 danmaku-system 容器是否运行：
   ```bash
   docker-compose ps
   ```

2. 检查容器日志：
   ```bash
   docker-compose logs danmaku-system
   ```

3. 检查防火墙：
   ```bash
   # Linux
   sudo ufw allow 5000

   # Windows
   # 控制面板 → 系统和安全 → Windows Defender 防火墙 → 允许应用通过防火墙
   ```

4. 尝试重启容器：
   ```bash
   docker-compose restart danmaku-system
   ```

### 问题 3：弹幕不显示

**症状**：PS5 上看不到弹幕

**解决方案**：

1. 检查 B站直播间 ID 是否正确

2. 检查 PS5 IRC 连接配置：
   - 服务器地址是否正确
   - 端口是否为 6667
   - 频道名是否包含 # 号

3. 检查弹幕转发系统日志：
   ```bash
   docker-compose logs danmaku-system
   ```

4. 检查网络连接：
   ```bash
   ping live.bilibili.com
   ```

5. 查看浏览器控制台（F12）是否有错误

### 问题 4：RTMP 推流失败

**症状**：PS5 推流后 OBS 无法拉流

**解决方案**：

1. 检查 RTMP 服务器是否运行：
   ```bash
   docker-compose ps nginx-rtmp
   ```

2. 检查 RTMP 统计页面：
   访问 http://localhost:8080/stat

3. 检查 DNS 配置是否正确

4. 检查 PS5 是否开启加速器（Twitch 访问限制）

5. 检查端口 1935 是否开放：
   ```bash
   telnet localhost 1935
   ```

### 问题 5：服务频繁重启

**症状**：容器反复重启

**解决方案**：

1. 查看重启日志：
   ```bash
   docker-compose logs --tail=50
   ```

2. 检查资源占用：
   ```bash
   docker stats
   ```

3. 增加资源限制（修改 docker-compose.yml）：
   ```yaml
   deploy:
     resources:
       limits:
         memory: 1G
   ```

4. 检查配置文件是否损坏

### 问题 6：配置修改不生效

**症状**：修改 Web 界面配置后没有效果

**解决方案**：

1. 检查配置文件是否保存：
   ```bash
   cat logs/config.json
   ```

2. 重启服务：
   ```bash
   docker-compose restart
   ```

3. 清除浏览器缓存后刷新页面

---

## 📝 版本更新日志

### v1.0.0 (2026-03-21)

**新增功能**：
- ✅ 完整的 Docker 容器化部署
- ✅ Docker Compose 多服务编排
- ✅ 一键启动脚本（Windows 和 Linux/macOS）
- ✅ 自动重启机制
- ✅ 数据持久化支持
- ✅ Web 可视化配置界面
- ✅ RTMP 推流监控
- ✅ 详细的部署文档

**已知限制**：
- ⚠️ 需要预先安装 Docker 和 Docker Compose
- ⚠️ 首次构建镜像需要较长时间
- ⚠️ 需要配置 DNS 重定向

**待优化**：
- [ ] 添加健康检查
- [ ] 优化镜像大小（多阶段构建）
- [ ] 添加监控面板（Grafana）
- [ ] 支持多实例部署
- [ ] 添加自动备份
- [ ] 支持 HTTPS
- [ ] 添加 Redis 缓存

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 GPL-3.0 许可证。

详见 [LICENSE](LICENSE) 文件。

---

## 📞 联系方式

- **作者**：IceNoproblem
- **B站空间**：https://space.bilibili.com/2250922
- **GitHub**：https://github.com/IceNoproblem
- **问题反馈**：https://github.com/IceNoproblem/PS5BiliDanmaku/issues

---

## 🙏 致谢

感谢以下开源项目：

- [tiangolo/nginx-rtmp](https://github.com/tiangolo/nginx-rtmp) - Nginx RTMP 模块
- [Flask](https://flask.palletsprojects.com/) - Python Web 框架
- [Docker](https://www.docker.com/) - 容器化平台

---

## 🔗 相关链接

- [Windows 版本](https://github.com/IceNoproblem/PS5BiliDanmaku/tree/windows)
- [详细部署文档](DOCKER_DEPLOY.md)
- [快速开始指南](README_DOCKER.md)
- [版本更新日志](DOCKER_CHANGELOG.md)

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**

Made with ❤️ by IceNoproblem

</div>
