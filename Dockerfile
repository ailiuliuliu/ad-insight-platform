FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装git（用于推送代码）
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY webhook/requirements.txt /app/webhook/requirements.txt

# 安装Python依赖
RUN pip install --no-cache-dir -r /app/webhook/requirements.txt

# 复制项目文件
COPY . /app/

# 配置Git（使用环境变量）
RUN git config --global user.name "KIM Bot" && \
    git config --global user.email "bot@kuaishou.com"

# 设置SSH密钥（容器启动时通过环境变量或挂载）
# 在容器云中配置SSH_PRIVATE_KEY环境变量

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "--chdir", "/app/webhook", "app:app"]
