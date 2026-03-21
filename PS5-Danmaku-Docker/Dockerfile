FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（包含编译工具）
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY danmaku_forward.py .
COPY monitor_rtmp.py .
COPY config.json .

# 创建日志目录
RUN mkdir -p /app/logs

# 暴露端口
EXPOSE 5000
EXPOSE 6667

# 启动命令（默认启动弹幕转发系统）
CMD ["python", "danmaku_forward.py"]
