# 使用官方 Python 3.13 slim 镜像作为基础
FROM python:3.13-slim

# 从 uv 官方镜像复制 uv 二进制文件
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 设置工作目录
WORKDIR /app

# 设置环境变量
# 确保 uv 不会尝试连接互联网去更新自己
ENV UV_LINK_MODE=copy \
    # 编译字节码以加快启动速度
    UV_COMPILE_BYTECODE=1 \
    # 将 .venv/bin 加入 PATH
    PATH="/app/.venv/bin:$PATH"

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装依赖
# --frozen: 严格按照 uv.lock 安装
# --no-install-project: 仅安装依赖，暂不安装项目本身
RUN uv sync --frozen --no-install-project

# 复制项目代码
COPY . .

# 暴露端口 8001
EXPOSE 8001

# 启动命令
CMD ["python", "app/main.py"]
