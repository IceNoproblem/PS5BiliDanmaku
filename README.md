# 请注意 windows版请移步https://github.com/IceNoproblem/PS5BiliDanmaku/tree/windows


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

## 📖 项目简介

PS5BiliDanmaku 是一款专为 NAS 和软路由设计的轻量级工具，通过 IRC 协议将 B 站直播弹幕转发到 PS5。采用 Docker 容器化部署，完美适配 OpenWrt、群晖 Synology、威联通 QNAP、Unraid 等主流 NAS 系统。

### ✨ 核心特性

- ✅ **超低资源占用**：CPU 使用率 < 5%，内存 < 200MB
- ✅ **NAS/软路由完美适配**：支持 OpenWrt、群晖、威联通、Unraid
- ✅ **Docker Compose 一键部署**：无需手动配置，3 分钟完成
- ✅ **Web 可视化管理**：http://NAS-IP:5000，界面友好
- ✅ **断电自动恢复**：容器自动重启，无需人工干预
- ✅ **数据持久化**：配置和日志存储在本地，删除容器不丢失
- ✅ **跨架构支持**：AMD64、ARM64、ARMv7 全覆盖

---

## 🎯 适用场景

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
- CPU：单核 1.5GHz+（ARM 或 x86）
- 内存：512MB
- 存储：500MB 可用空间
- 网络：千兆以太网

**推荐配置：**
- CPU：双核 2.0GHz+
- 内存：1GB+
- 存储：1GB+ SSD

### 软件要求

- **Docker**：20.10 及以上
- **Docker Compose**：2.0 及以上（或 docker-compose v1.27+）
- **开放端口**：1935、5000、6667、8080

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
   - 解压到群晖的 Docker 目录（如 `/volume1/docker/PS5BiliDanmaku`）

3. **使用 Container Manager 部署**

   - 打开 Container Manager
   - 点击 "项目" → "新建"
   - 路径选择解压后的目录
   - 点击 "运行"

4. **访问 Web 界面**

   浏览器打开：`http://群晖IP:5000`

#### 方法二：通过 SSH 部署（高级用户）

```bash
# 1. 启用 SSH
# 群晖控制面板 → 终端机和 SNMP → 启用 SSH 功能

# 2. SSH 连接到群晖
ssh 群晖用户名@群晖IP

# 3. 进入 Docker 目录
cd /volume1/docker

# 4. 克隆项目
git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
cd PS5BiliDanmaku

# 5. 启动容器
docker compose up -d
```

### 威联通 QNAP

1. **安装 Container Station**

   打开 App Center，搜索并安装 "Container Station"

2. **下载项目**

   - 通过 File Station 上传项目文件到 NAS
   - 或使用 SSH：`git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git`

3. **创建容器**

   - 打开 Container Station
   - 点击 "创建" → "应用程序"
   - 粘贴 docker-compose.yml 内容
   - 点击 "创建"

### Unraid

1. **安装 CA User Scripts 插件**（可选）

2. **添加 Community Applications 搜索**

3. **搜索并安装**

   - 在 Community Applications 中搜索 "PS5BiliDanmaku"
   - 或手动添加：点击 "Add" → "Docker Compose"

4. **配置参数**

   - 设置端口映射
   - 设置存储路径
   - 点击 "Apply"

### 真实 NAS（海康威视、大华等）

1. **安装 Docker 套件**

   检查 NAS 是否支持 Docker，通常在应用市场或套件中心

2. **通过 SSH 部署**

   ```bash
   # 启用 SSH（通常在系统设置中）
   ssh admin@NAS_IP

   # 进入 Docker 目录
   cd /volume1/docker 或 /volume2/docker

   # 克隆项目
   git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
   cd PS5BiliDanmaku

   # 启动
   docker compose up -d
   ```

---

## 🌉 软路由部署

### OpenWrt

#### 前置准备

1. **安装 Docker 插件**

   ```bash
   opkg update
   opkg install docker dockerd docker-compose
   ```

2. **启动 Docker 服务**

   ```bash
   /etc/init.d/dockerd start
   /etc/init.d/dockerd enable
   ```

#### 部署步骤

```bash
# 1. 进入 Docker 工作目录
cd /root 或 cd /opt/docker

# 2. 克隆项目
git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
cd PS5BiliDanmaku

# 3. 启动容器
docker compose up -d

# 4. 查看状态
docker compose ps
```

#### 持久化配置（重要）

**OpenWrt 的 `/tmp` 目录在重启后会清空，建议将项目放在 `/opt` 或 `/overlay`：**

```bash
# 挂载 /opt 到持久化存储（如果没有）
# 确保有足够空间，建议挂载到 U 盘或硬盘
mkdir -p /opt/docker
cd /opt/docker
git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
cd PS5BiliDanmaku
docker compose up -d
```

#### 性能优化

- **资源限制**：在 docker-compose.yml 中添加 `mem_limit: 512m` 限制内存使用
- **存储驱动**：使用 overlay2 驱动提升性能
- **日志管理**：禁用不必要的日志以减少存储占用

### iKuai（爱快）

#### 方法一：Docker 插件图形界面

1. **安装 Docker 插件**

   - 进入爱快路由器管理界面
   - "高级应用" → "Docker"
   - 点击"安装"（需要联网）

2. **创建容器**

   - 点击"创建容器"
   - 选择"Compose 模式"
   - 粘贴 docker-compose.yml 内容
   - 设置端口和存储路径
   - 点击"创建"

3. **访问管理界面**

   浏览器打开：`http://爱快IP:5000`

#### 方法二：SSH 部署

```bash
# 1. 启用 SSH
# 系统设置 → SSH 设置 → 开启 SSH

# 2. SSH 连接
ssh admin@爱快IP

# 3. 进入 Docker 目录
cd /opt/docker

# 4. 克隆项目
git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
cd PS5BiliDanmaku

# 5. 启动
docker compose up -d
```

### Padavan

Padavan 需要启用 USB 应用 Docker：

1. **准备 USB 设备**

   - 格式化为 ext4 或 NTFS
   - 插入路由器 USB 端口

2. **启用 Docker**

   - 进入 Padavan 管理界面
   - "USB 应用" → "Docker"
   - 勾选"启用 Docker"

3. **通过 SSH 部署**

   ```bash
   ssh admin@路由器IP
   cd /mnt/sda1/docker  # 根据实际 USB 挂载点调整
   git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
   cd PS5BiliDanmaku
   docker compose up -d
   ```

---

## ⚙️ 配置说明

### 首次配置

1. **访问 Web 管理界面**

   浏览器打开：`http://NAS-IP:5000`

2. **配置 B站直播间**

   - 输入 B站直播间 ID（如：31517300）
   - 点击"保存配置"

3. **配置 IRC 连接**

   - IRC 服务器地址：填入 NAS IP（如 192.168.1.100）
   - IRC 服务器端口：6667（默认）
   - PS5 频道：#你的PS5账号

### 配置文件位置

- `config.json`：主配置文件
- `bili_cookies.json`：B站登录凭证
- `logs/`：日志目录
- `room_history.json`：直播间历史记录

### 修改配置

#### 方法一：Web 界面修改（推荐）

访问 `http://NAS-IP:5000`，在界面中修改配置并保存

#### 方法二：编辑配置文件

```bash
# 进入项目目录
cd /vol3/1000/system/docker/ps5-bilibili-danmaku/PS5BiliDanmaku

# 编辑配置
nano config.json

# 重启容器应用配置
docker compose restart
```

---

## 🎮 PS5 推流配置

### DNS 劫持配置

将 PS5 访问的 Twitch 域名解析到 NAS IP，实现推流劫持。

#### OpenWrt 配置

1. **登录 OpenWrt 管理界面**

2. **网络 → DHCP/DNS**

3. **添加静态域名解析**

   | 域名 | IP 地址 |
   |-------|---------|
   | live.twitch.tv | 192.168.110.99（你的 NAS IP） |
   | twitch.tv | 192.168.110.99 |
   |usher.ttvnw.net | 192.168.110.99 |

4. **保存并应用**

#### 群晖 DNS 配置

群晖默认作为 DNS 服务器的情况较少，建议在路由器上配置 DNS 劫持。

#### 软路由通用配置

在路由器的 DNS 设置中添加：

```
live.twitch.tv → NAS_IP
twitch.tv → NAS_IP
usher.ttvnw.net → NAS_IP
```

### PS5 开启直播

1. **在 PS5 上开启直播**

   - 设置 → 广播与分享 → 开始直播
   - 选择 Twitch 平台
   - 输入推流密钥（任意即可）

2. **PS5 连接到 IRC**

   - 系统会自动连接到 IRC 服务器
   - 查看日志确认连接成功

### 拉流到 B站

使用 OBS 或直播姬从 NAS 拉流到 B站：

1. **获取 RTMP 推流地址**

   - 访问 RTMP 统计页面：`http://NAS-IP:8080/stat`
   - 查看推流密钥（stream key）

2. **配置 OBS**

   - 推流服务：Bilibili Live
   - 服务器：`rtmp://NAS-IP:1935/live`
   - 串流密钥：从统计页面获取的推流码

3. **开始推流**

   - 在 OBS 中点击"开始推流"
   - 查看弹幕是否正常显示

---

## 📊 常用命令

### Docker Compose 命令

```bash
# 启动所有容器
docker compose up -d

# 停止所有容器
docker compose down

# 重启所有容器
docker compose restart

# 查看容器状态
docker compose ps

# 查看日志
docker compose logs -f

# 查看特定容器日志
docker compose logs -f ps5-danmaku-system

# 重新构建镜像
docker compose build --no-cache

# 更新项目
git pull
docker compose up -d --build
```

### Docker 原生命令

```bash
# 查看所有容器
docker ps -a

# 查看容器资源占用
docker stats

# 进入容器
docker exec -it ps5-danmaku-system /bin/bash

# 查看容器日志
docker logs -f ps5-danmaku-system

# 停止单个容器
docker stop ps5-danmaku-system

# 启动单个容器
docker start ps5-danmaku-system

# 删除容器
docker rm ps5-danmaku-system
```

---

## ❓ 常见问题

### 问题 1：容器无法启动

**症状**：`docker compose up -d` 后容器立即退出

**解决方法**：
1. 查看日志：`docker compose logs`
2. 检查端口是否被占用：`netstat -tunlp | grep 5000`
3. 检查配置文件格式是否正确
4. 确认 Docker 版本是否符合要求

### 问题 2：Web 界面无法访问

**症状**：浏览器无法打开 `http://NAS-IP:5000`

**解决方法**：
1. 确认容器是否运行：`docker compose ps`
2. 检查防火墙是否阻止 5000 端口
3. 确认 NAS IP 是否正确
4. 查看 danmaku-system 容器日志：`docker compose logs ps5-danmaku-system`

### 问题 3：弹幕不显示

**症状**：PS5 上看不到弹幕

**解决方法**：
1. 检查 IRC 连接状态：查看日志是否有"PS5 连接建立"
2. 确认 PS5 频道配置正确
3. 检查 B站直播间 ID 是否正确
4. 确认 DNS 劫持配置成功

### 问题 4：RTMP 推流失败

**症状**：无法从 NAS 拉流到 B站

**解决方法**：
1. 访问 RTMP 统计页面：`http://NAS-IP:8080/stat`
2. 确认 PS5 正在推流（页面应显示推流信息）
3. 检查 OBS 推流配置
4. 查看容器日志确认 RTMP 服务器状态

### 问题 5：NAS 重启后容器不自动启动

**症状**：NAS 重启后需要手动启动容器

**解决方法**：
1. 确认 docker-compose.yml 中有 `restart: unless-stopped`
2. 检查 Docker 服务是否开机自启
3. 群晖：确保 Docker 套件开机自启
4. OpenWrt：确保 dockerd 服务开机自启

### 问题 6：OpenWrt 重启后配置丢失

**症状**：OpenWrt 重启后项目文件或容器配置丢失

**解决方法**：
1. **重要**：将项目放在 `/opt` 目录，不要放在 `/tmp`
2. 确保 `/opt` 挂载到持久化存储（U 盘或硬盘）
3. 重新部署到持久化目录：
   ```bash
   cd /opt/docker
   git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
   cd PS5BiliDanmaku
   docker compose up -d
   ```

---

## 🚀 性能优化

### OpenWrt 优化

- **资源限制**：在 docker-compose.yml 中添加：
  ```yaml
  deploy:
    resources:
      limits:
        memory: 512M
  ```
- **存储优化**：使用外部存储挂载 /opt
- **日志管理**：定期清理日志文件

### 群晖优化

- **SSD 缓存**：启用 SSD 缓存提升 I/O 性能
- **存储设置**：将 Docker 目录放在 SSD 上
- **内存优化**：限制容器内存使用

---

## 📝 版本更新日志

### v1.0.0 (2026-03-21)

- ✅ Docker Compose 一键部署
- ✅ Web 可视化管理界面
- ✅ RTMP 推流监控
- ✅ NAS/软路由完美适配
- ✅ 自动重启和持久化
- ✅ 跨架构支持

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### NAS 特定贡献

如果你在特定的 NAS 系统上成功部署，欢迎分享部署经验：

- 部署步骤截图
- 遇到的问题和解决方案
- 性能优化建议
- 配置文件模板

---

## 📄 许可证

本项目采用 GPL-3.0 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- [PS5BiliDanmaku](https://github.com/IceNoproblem/PS5BiliDanmaku) 原项目
- [B站直播](https://live.bilibili.com/) 提供直播平台
- [nginx-rtmp](https://github.com/arut/nginx-rtmp-module) RTMP 流媒体服务器

---

## 📧 联系方式

- **GitHub Issues**：https://github.com/IceNoproblem/PS5BiliDanmaku/issues
- **项目主页**：https://github.com/IceNoproblem/PS5BiliDanmaku

---

## 🔗 相关链接

- [PS5BiliDanmaku Windows 版本](https://github.com/IceNoproblem/PS5BiliDanmaku/tree/windows)
- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [B站直播推流文档](https://help.bilibili.com/hc/zh-cn/articles/1155122960203172096)

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
