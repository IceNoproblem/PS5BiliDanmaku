
# PS5BiliDanmaku
# 阿冰没问题（Icenoproblem）PS5 哔哩哔哩 直播系统


> PS5 B站直播 把 Bilibili 直播弹幕转发到 PS5 的轻量工具
> 
### 为什么需要DNS重定向？

PS5直播系统之所以能工作，**核心技术是DNS重定向**。这里解释为什么它如此重要：
如果您无法搞定此项配置，请关闭本页面，购买采集卡

####  **突破官方限制**
- PS5直播只能推送到官方支持的平台（如YouTube、Twitch）
- 通过DNS重定向，将PS5的直播请求劫持到本地服务器
- 无需修改PS5系统文件，完全通过网络层面实现


## 📋 项目简介

PS5BiliDanmaku 是一个专为主播设计的工具，它能够在您使用 PlayStation 5 进行游戏直播，不依赖采集卡，并将来自 Bilibili 直播间的实时弹幕、礼物消息、用户进入通知等互动信息，实时转发并显示在您的 PS5 屏幕上。

**这意味着您无需再分心查看手机或电脑上的弹幕助手，可以在沉浸游戏的同时，直接在游戏画面中与观众即时互动，显著提升直播体验和观众参与感。**

## ✨ 核心特性

*   **实时同步**：稳定、低延迟地将 B 站直播间的各类互动消息推送至 PS5。
*   **全 Web 配置**：提供友好的浏览器管理界面，所有设置均可通过网页完成，无需记忆复杂命令。
*   **容器化部署**：采用 Docker 封装，实现环境隔离、依赖统一，部署与迁移极其简单。
*   **轻量高效**：使用 Python 等高效技术栈开发，资源占用低，适合在树莓派、NAS、软路由或家庭服务器上 7x24 小时后台运行。
*   **一键启动**：提供 `docker-compose.yml` 配置文件，一行命令即可完成所有环境搭建与服务启动。

## 🖥️ 运行效果预览

<img width="1882" height="1260" alt="image" src="https://github.com/user-attachments/assets/5fbe1890-05d6-453e-a3ee-5badca9d7ef7" />


## 🚀 快速开始

### 前提条件
1.  **一台 PS5**，并与部署本工具的服务器处于**同一局域网 (LAN)** 下。
2.  **一台可安装 Docker 的服务器/软路由/NAS**，例如：群晖、飞牛、威联通、openwrt等 如果您没有，请移步 分支项目：https://github.com/IceNoproblem/PS5BiliDanmaku/tree/windows 这是专为windows电脑开发的程序，同样的功能。
3.  **已安装 Docker 及 Docker Compose**。请根据您的操作系统参考 https://docs.docker.com/engine/install/ 和 https://docs.docker.com/compose/install/。
4.  **您的路由器可以进行流量劫持或DNS重定向（类似名字，不同设备品牌名字不一样）可自行百度用法。
5.  **端口未被占用，如被占用请释放相应端口：5000、6667、8081、1935。
6.  **有NAS、软路由等相应基础操作能力和命令行操作能力。

### 部署步骤

1.  **获取项目代码**
    通过 Git 克隆本项目到您的服务器上：
    ```bash
    #克隆项目文件到本地
    git clone https://github.com/IceNoproblem/PS5BiliDanmaku.git
    #进入项目文件夹
    cd PS5-Danmaku-Docker
    ```

2.  **一键启动服务**
    执行以下命令：
    ```bash
    # 停止所有容器
    docker compose down
    # 重新构建镜像
    docker compose build --no-cache
    # 启动所有容器
    docker compose up -d
    ```
    首次运行会自动从 `Dockerfile` 构建镜像并启动容器。

3.  **访问管理界面**
    服务启动后，在浏览器中打开：
    ```
    http://<你的服务器IP地址>:5000
    ```
    例如：`http://192.168.1.100:8000`

4.  **基础配置**
    首次访问 Web 界面，您需要配置以下核心信息：
    *   **Bilibili 直播间 ID**：在 B 站直播间页面的网址中找到，通常是 `https://live.bilibili.com/123456` 中的数字部分。
    *   **扫码登陆**：如果需要读取需要登录才能查看的弹幕（如高能榜、舰长消息等），可能需要在此处配置登录后的 Cookie 信息。**请注意保护个人账户安全，勿泄露此信息。**
    *   **点击保存后根据提示重启容器**：
    *   **对PS5进行相应的流量劫持**：根据Web界面提示，对ps5流量进行dns劫持。

5.  **在 PS5 上验证**
    确保您的 PS5 已开机并处于加速器加速状态下，按截屏键选择播放或直播（信号塔图标），首次开播需要注册关联twitch账号。在 B 站直播间发送一条测试弹幕，观察是否能在 PS5 游戏画面上正确显示。**请注意，此工具的原理是在 PS5 的网络中注入一个虚拟的“信息层”，具体呈现方式（如叠加层、侧边栏等）需遵循项目本身的实现逻辑。**

如有需要可以设置容器开机自启动

## ⚙️ 高级配置与管理

### 环境变量
您可以通过修改 `docker-compose.yml` 文件中的 `environment` 部分，或 Docker 运行命令的 `-e` 参数来设置环境变量，例如调整日志级别等。

### 数据持久化
在 `docker-compose.yml` 中，我们已将容器内的 `/app/config` 目录映射到宿主机的 `./config` 目录。所有配置文件、用户数据均保存在此，**请定期备份此目录**。即使删除并重建容器，您的配置也不会丢失。

### 查看日志
```bash
# 查看实时日志
docker-compose logs -f

# 查看最近100行日志
docker-compose logs --tail=100
```

### 服务管理
```bash
# 停止服务
docker-compose down

# 停止并删除容器、镜像、匿名卷（配置文件会被保留）
docker-compose down -v --rmi all

# 重启服务
docker-compose restart

# 更新服务（重新拉取代码后，重新构建并启动）
docker-compose up -d --build
```

## ❓ 常见问题 (FAQ)

**Q: 无法访问 Web 管理界面 (`http://服务器IP:8000`)**
- **A1**: 检查防火墙是否放行了服务器的 `5000` 端口。
- **A2**: 确认容器是否正常运行：`docker-compose ps`。查看日志排查错误：`docker-compose logs`。
- **A3**: 确认 `docker-compose.yml` 中端口映射配置是否正确，查看容器日志。

**Q: PS5 上收不到任何弹幕**
- **A1**: 确认 PS5开播成功，将dns正确劫持。
- **A2**: 确认 Bilibili 直播间 ID 填写无误，且直播间正在开播。保存后需要重启容器。
- **A3**: 查看容器日志，确认是否成功连接到 B 站弹幕服务器以及是否在向 PS5 发送数据。

**Q: 如何更新到最新版本？**
```bash
# 进入项目目录
cd /path/to/PS5BiliDanmaku
# 拉取最新的代码
git pull
# 重新构建并启动服务
docker-compose up -d --build
```

**Q: 这个工具安全吗？会封号吗？**
- 本项目为开源工具，代码透明，仅通过 B 站公开的直播流接口获取弹幕数据。但任何第三方工具都存在理论风险，**请勿用于发送垃圾信息、刷屏等违反 B 站社区规则的行为**，并自行承担使用风险。关于 Cookie 的使用，请务必谨慎。

## 🤝 贡献指南
我们欢迎并感谢所有的贡献！
1.  **Fork** 本仓库。
2.  创建您的功能分支 (`git checkout -b feature/AmazingFeature`)。
3.  提交您的更改 (`git commit -m 'Add some AmazingFeature'`)。
4.  推送到分支 (`git push origin feature/AmazingFeature`)。
5.  开启一个 **Pull Request**。

在提交 PR 前，请确保代码风格一致并通过基本的测试。

## 📄 许可证
本项目采用 LICENSE 开源。

## 🙏 致谢
bao3/playstation https://hub.docker.com/r/bao3/playstation
xfgryujk/blivechat https://github.com/xfgryujk/blivechat
---
**如果这个项目对您有帮助，请点个 Star ⭐ 支持一下！**

> *注意：本项目为开源社区作品，与 Sony PlayStation 或 Bilibili 官方无关。使用本工具产生的任何问题，开发者不承担责任。*
