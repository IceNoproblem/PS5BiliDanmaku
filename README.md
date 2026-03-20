# PS5BiliDanmaku - Docker 版本

<div align="center">

**把 Bilibili 直播弹幕转发到 PS5 的轻量工具**

![Version](https://img.shields.io/badge/version-v1.0.0-blue)
![Docker](https://img.shields.io/badge/docker-supported-brightgreen)
![NAS](https://img.shields.io/badge/NAS-ready-green)
![License](https://img.shields.io/badge/license-GPL--3.0-green)

**专为 NAS 和软路由设计 | 一键部署 | 低资源占用**

[快速开始](#快速开始) • [NAS 部署](#nas-部署) • [软路由部署](#软路由部署) • [常见问题](#常见问题)

</div>

---

没有软路由、nas的windows电脑用户 直接看https://github.com/IceNoproblem/PS5BiliDanmaku/tree/windows


## 📖 项目简介

PS5BiliDanmaku 是一款专为 NAS 和软路由设计的轻量级工具，通过 IRC 协议将 B 站直播弹幕转发到 PS5。采用 Docker 容器化部署，完美适配 OpenWrt、群晖 Synology、威联通 QNAP、Unraid 等主流 NAS 系统。


### 推荐部署环境

| 环境 | 系统示例 | 推荐度 |
|------|----------|--------|
| 软路由 | OpenWrt、iKuai、Padavan | ⭐⭐⭐⭐⭐ |
| NAS | 群晖 Synology、威联通 QNAP、海康威视 | ⭐⭐⭐⭐⭐ |
| 服务器 | Ubuntu、Debian、CentOS | ⭐⭐⭐⭐ |
| 玩客云 | OpenWrt 固件 | ⭐⭐⭐ |
| 树莓派 | Raspberry Pi OS | ⭐⭐⭐ |
| 其他 | 支持 Docker 的设备 | ⭐⭐⭐ |

### 硬件要求

**最低配置：**
- CPU：单核 1.5GHz+（x86）
- 内存：512MB
- 存储：500MB 可用空间
- 网络：千兆局域网

**推荐配置：**
- CPU：双核 2.0GHz+
- 内存：1GB+
- 存储：1GB+ SSD

### 软件要求

- **Docker**：20.10 及以上
- **Docker Compose**：2.0 及以上（或 docker-compose v1.27+）
- **开放端口**：1935、5000、6667、8081

---

## 🚀 快速开始

### 一键部署（适用于有 Docker Compose 的系统）

```bash
# 1. 下载项目
git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
cd PS5BiliDanmaku

# 2. 一键启动
docker compose up -d

# 3. 访问 Web 管理界面
# 浏览器打开 http://你的NAS IP:5000
```

---

## 🏠 NAS 部署

### 群晖 Synology

#### 方法一：通过 Synology Docker 部署（推荐）

1. **安装 Docker 套件**

   打开套件中心，搜索并安装 "Container Manager" 或 "Docker"

2. **下载项目文件**

   - 下载项目 ZIP：https://github.com/IceNoproblem/PS5BiliDanmaku/archive/refs/heads/docker.zip
   - 解压到群晖共享文件夹（如 `docker/PS5BiliDanmaku`）

3. **导入镜像**

   - 打开 Container Manager → 注册表
   - 搜索 `tiangolo/nginx-rtmp`
   - 下载 `latest` 标签

4. **创建项目**

   - Container Manager → 项目
   - 点击"新建" → "从 docker-compose.yml 创建"
   - 选择 `docker/PS5BiliDanmaku/docker-compose.yml`
   - 点击"下一步"
   - 等待容器启动

5. **访问 Web 界面**

   浏览器访问：http://群晖IP:5000

#### 方法二：通过 SSH 部署

1. **启用 SSH**

   - 控制面板 → 终端机和 SNMP → 启用 SSH 服务

2. **SSH 连接到群晖**

   ```bash
   ssh your_username@your_nas_ip
   ```

3. **部署 Docker**

   ```bash
   # 进入共享文件夹
   cd /volume1/docker

   # 下载项目
   git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
   cd PS5BiliDanmaku

   # 启动服务
   docker compose up -d

   # 查看状态
   docker compose ps
   ```

---

### 威联通 QNAP

#### 通过 Container Station 部署

1. **安装 Container Station**

   打开 App Center，搜索并安装 "Container Station"

2. **下载项目**

   - 通过 File Station 上传项目文件到 NAS
   - 或通过 SSH 下载（见下方）

3. **SSH 连接到 QNAP**

   ```bash
   ssh admin@your_nas_ip
   ```

4. **部署**

   ```bash
   # 进入共享目录
   cd /share/CACHEDEV1_DATA

   # 下载项目
   git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
   cd PS5BiliDanmaku

   # 启动服务
   docker compose up -d
   ```

---

### Unraid

1. **安装 Docker 插件**

   - Settings → Docker → 启用 Docker
   - 安装完成后进入 "Docker" 标签

2. **添加容器**

   - 点击 "Add Container"
   - 在 Template 选择 "Community Applications"
   - 搜索 "PS5BiliDanmaku"
   - 或手动配置（见下方手动配置）

3. **手动配置**

   **Nginx-RTMP：**
   - Name: `ps5-nginx-rtmp`
   - Repository: `tiangolo/nginx-rtmp`
   - Ports: `1935:1935`, `8080:8080`, `80:80`

   **Danmaku-System：**
   - Name: `ps5-danmaku-system`
   - Repository: `icecynoproblem/ps5-bili-danmaku`（或本地构建）
   - Ports: `5000:5000`, `6667:6667`
   - Volumes: `/path/to/config:/app/logs`

---

### 真实 NAS

1. **安装 Docker**

   打开 App Center，搜索并安装 "Docker"

2. **SSH 连接**

   ```bash
   ssh admin@your_nas_ip
   ```

3. **部署**

   ```bash
   cd /home/admin
   git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
   cd PS5BiliDanmaku
   docker compose up -d
   ```

---

## 🌐 软路由部署

### OpenWrt

#### 前置准备

1. **安装 Docker 插件**

   - OpenWrt 21.02+：系统 → 软件包 → 安装 `dockerd`、`docker-compose`
   - 或通过 LuCI → System → Docker 安装

2. **启用 Docker**

   - LuCI → System → Docker → 启用
   - 确保 Docker 状态为"运行中"

#### 部署步骤

1. **SSH 连接到 OpenWrt**

   ```bash
   ssh root@192.168.1.1
   ```

2. **创建工作目录**

   ```bash
   cd /tmp
   git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
   cd PS5BiliDanmaku
   ```

3. **启动服务**

   ```bash
   docker compose up -d
   ```

4. **验证部署**

   ```bash
   # 查看容器状态
   docker ps

   # 访问 Web 界面
   # 浏览器打开 http://192.168.1.1:5000
   ```

5. **持久化配置（可选）**

   OpenWrt 重启后 /tmp 目录会被清空，建议移动到持久化目录：

   ```bash
   # 移动到 /opt 或 overlay
   mv /tmp/PS5BiliDanmaku /opt/ps5-danmaku
   cd /opt/ps5-danmaku
   docker compose up -d
   ```

---

### iKuai（爱快）

#### 方法一：通过 Docker 插件（推荐）

1. **安装 Docker 插件**

   - 控制台 → 插件管理 → 应用商店
   - 搜索 "Docker" → 安装

2. **部署容器**

   - 控制台 → Docker → 容器
   - 点击"添加容器"
   - 填写配置（见下方配置说明）

#### 方法二：通过 SSH 部署

1. **启用 SSH**

   - 系统设置 → SSH 服务 → 启用

2. **SSH 连接**

   ```bash
   ssh admin@192.168.1.1
   ```

3. **部署**

   ```bash
   cd /tmp
   git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
   cd PS5BiliDanmaku
   docker compose up -d
   ```

---

### Padavan

1. **启用 Docker**

   - 高级设置 → USB 应用 → Docker → 启用

2. **SSH 连接**

   ```bash
   ssh admin@192.168.1.1
   ```

3. **部署**

   ```bash
   cd /tmp/mnt/sda1
   git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
   cd PS5BiliDanmaku
   docker compose up -d
   ```

---


## ⚙️ 配置说明

### 首次配置

1. **访问 Web 管理界面**

   浏览器打开：http://你的NAS IP:5000

2. **配置 B站直播间**

   - 输入 B站直播间 ID（例如：31517300）
   - 点击"保存配置" 并重启容器


### 配置文件位置

配置文件存储在宿主机（NAS/软路由），删除容器不会丢失：

```bash
# 项目目录下的 logs 文件夹
./logs/config.json        # 主配置文件
./logs/bili_cookies.json  # B站登录凭证
./logs/danmaku.log       # 弹幕日志
./logs/rtmp.log          # RTMP 日志
```

### 修改配置

**方法一：通过 Web 界面修改**

1. 访问 http://你的NAS IP:5000
2. 修改配置参数
3. 点击"保存配置"

**方法二：直接编辑配置文件**

1. **SSH 连接到 NAS**

   ```bash
   ssh user@your_nas_ip
   cd /path/to/PS5BiliDanmaku
   ```

2. **编辑配置文件**

   ```bash
   vi logs/config.json
   ```

3. **重启服务**

   ```bash
   docker compose restart danmaku-system
   ```

---

## 🎮 PS5 推流配置

### 步骤 1：配置 DNS 劫持（软路由上配置）

由于 PS5 推流使用 Twitch 的 RTMP 服务器，需要在软路由上配置 DNS 劫持。

#### OpenWrt 配置

1. **登录 OpenWrt 后台**

   - 默认地址：192.168.1.1

2. **添加 DNS 劫持规则**

   - 网络 DHCP/DNS → DNS 转发
   - 添加以下规则：

   | 域名 | 类型 | 值 |
   |------|------|-----|
   | live.twitch.tv | A | 你的 NAS IP |
   | video-weaver.twitch.tv | A | 你的 NAS IP |

3. **保存并应用**

   - 点击"保存并应用"

#### 群晖配置

群晖本身不具备 DNS 功能，需要在路由器上配置。

#### 其他路由器

1. **登录路由器后台**

   - 通常是 192.168.1.1 或 192.168.0.1

2. **添加 DNS 重定向规则**

   - 找到"DNS 重定向"或"Hosts"功能
   - 添加规则：

   ```
   你的NAS IP    live.twitch.tv
   你的NAS IP    video-weaver.twitch.tv
   ```

3. **保存并重启路由器**




**打开要直播的游戏或应用**

 **点击开始直播**

   PS5 会通过 DNS 劫持推流到本地 NAS


   

### 步骤 3：OBS/直播姬拉流

#### OBS Studio

1. **添加媒体源**

   来源 → + → 媒体源

2. **输入 RTMP 地址**

   ```
     服务器：rtmp://NAS-IP/app/live/PS5推流码
   ```

3. **开始推流**

#### 直播姬

1. **添加直播源**

   直播设置 → 直播源

2. **输入 RTMP 地址**

   ```
   服务器：rtmp://NAS-IP/app/live/PS5推流码
   ```

3. **开始直播**

---

## 🔧 常用命令

### Docker Compose 命令

```bash
# 启动服务
docker compose up -d

# 停止服务
docker compose down

# 重启服务
docker compose restart

# 查看日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f danmaku-system

# 查看容器状态
docker compose ps

# 重新构建并启动
docker compose up -d --build

# 删除所有容器和镜像
docker compose down --rmi all

# 查看资源占用
docker compose top
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

# 停止容器
docker stop <容器ID>

# 启动容器
docker start <容器ID>

# 重启容器
docker restart <容器ID>
```

---

## 🔍 故障排查

### 问题 1：容器无法启动

**症状**：`docker compose up` 失败

**解决方案**：

1. **检查 Docker 是否正常运行**

   ```bash
   docker info
   ```

2. **检查端口是否被占用**

   ```bash
   netstat -tlnp | grep -E "1935|5000|6667|8080"
   ```

   如果端口被占用，修改 `docker-compose.yml` 中的端口映射

3. **查看详细错误日志**

   ```bash
   docker compose logs
   ```

4. **检查镜像是否成功拉取**

   ```bash
   docker images
   ```

### 问题 2：Web 界面无法访问

**症状**：http://NAS-IP:5000 无法打开

**解决方案**：

1. **检查容器是否运行**

   ```bash
   docker compose ps
   ```

2. **检查 danmaku-system 日志**

   ```bash
   docker compose logs danmaku-system
   ```

3. **检查防火墙设置**

   - OpenWrt：网络 → 防火墙 → 允许 5000 端口
   - 群晖：控制面板 → 安全性 → 防火墙 → 允许 5000 端口

4. **尝试使用本地 IP**

   ```bash
   # 在 NAS 上执行
   curl http://localhost:5000
   ```

5. **检查网络连接**

   ```bash
   # 从其他设备 ping NAS
   ping your_nas_ip
   ```

### 问题 3：弹幕不显示

**症状**：PS5 上看不到弹幕

**解决方案**：

1. **检查 B站直播间 ID 是否正确**

2. **检查 PS5 IRC 连接**

3. **查看弹幕系统日志**

   ```bash
   docker compose logs danmaku-system
   ```

4. **检查网络连接**

   ```bash
   ping live.bilibili.com
   ```

5. **测试 IRC 连接**

   ```bash
   telnet NAS-IP 6667
   ```

### 问题 4：RTMP 推流失败

**症状**：PS5 推流后 OBS 无法拉流

**解决方案**：

1. **检查 RTMP 服务器是否运行**

   ```bash
   docker compose ps nginx-rtmp
   ```

2. **访问 RTMP 统计页面**

   http://NAS-IP:8080/stat

3. **检查 DNS 劫持配置**

   ```bash
   # 在 PC 上测试
   nslookup live.twitch.tv
   # 应该返回 NAS 的 IP
   ```

4. **检查端口 1935 是否开放**

   ```bash
   telnet NAS-IP 1935
   ```

5. **检查 PS5 是否开启加速器**

   Twitch 可能需要加速器才能访问

### 问题 5：NAS 重启后容器不自动启动

**症状**：NAS 重启后需要手动启动容器

**解决方案**：

编辑 `docker-compose.yml`，添加 `restart: always`：

```yaml
services:
  nginx-rtmp:
    restart: always

  danmaku-system:
    restart: always

  rtmp-monitor:
    restart: always
```

然后重新启动：

```bash
docker compose up -d
```

### 问题 6：OpenWrt 重启后配置丢失

**症状**：OpenWrt 重启后 /tmp 目录被清空

**解决方案**：

将项目移动到持久化目录（如 /opt）：

```bash
# 移动到 /opt
mv /tmp/PS5BiliDanmaku /opt/ps5-danmaku
cd /opt/ps5-danmaku
docker compose up -d

# 添加到启动脚本（可选）
echo "cd /opt/ps5-danmaku && docker compose up -d" >> /etc/rc.local
chmod +x /etc/rc.local
```

---


## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### NAS 特定的贡献

如果你在特定 NAS 系统上成功部署，欢迎贡献部署教程：

- 群晖不同版本的部署方法
- 威联通不同型号的配置
- Unraid 模板优化
- OpenWrt 不同版本的兼容性

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

## 🔗 相关链接

- [Windows 版本](https://github.com/IceNoproblem/PS5BiliDanmaku/tree/windows)
- [详细部署文档](DOCKER_DEPLOY.md)
- [快速开始指南](README_DOCKER.md)
- [版本更新日志](DOCKER_CHANGELOG.md)

---

## 🙏 致谢

感谢以下开源项目和社区：

- [tiangolo/nginx-rtmp](https://github.com/tiangolo/nginx-rtmp) - Nginx RTMP 模块
- [Flask](https://flask.palletsprojects.com/) - Python Web 框架
- [Docker](https://www.docker.com/) - 容器化平台
- [OpenWrt](https://openwrt.org/) - 嵌入式 Linux 发行版
- 所有贡献者和用户

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**

专为 NAS 和软路由用户设计

Made with ❤️ by IceNoproblem

</div>
