FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 更换国内 Debian 镜像源（清华源），加速 apt 下载
RUN sed -i 's|http://deb.debian.org/debian|https://mirrors.tuna.tsinghua.edu.cn/debian|g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's|http://security.debian.org|https://mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list.d/debian.sources

# 安装系统依赖（包含编译工具）
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖（使用清华 PyPI 镜像加速）
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制项目文件
COPY danmaku_forward.py .
COPY monitor_rtmp.py .
COPY monitor_rtmp_debug.py .
COPY config.json .

# 创建必要目录（避免 volume 挂载时因目录不存在报错）
RUN mkdir -p /app/logs /app/debug_output

# 暴露端口
EXPOSE 5000
EXPOSE 6667

# 启动命令（默认启动弹幕转发系统）
CMD ["python", "danmaku_forward.py"]

