# Memory Hub 安装指南

> 从零开始部署 Memory Hub，5 分钟完成

---

## 📋 前置条件

### 必需

- ✅ **Docker** (20.10+) 和 **Docker Compose** (2.0+)
- ✅ **Git**（克隆项目）
- ✅ 8GB+ 内存
- ✅ 20GB 可用磁盘空间

### 可选

- Python 3.10+（本地开发）
- PostgreSQL 客户端工具（如 psql、DBeaver）

---

## 🚀 快速安装（推荐）

### 步骤 1：克隆项目

```bash
git clone https://github.com/wen41/memory-hub.git
cd memory-hub
```

### 步骤 2：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置
nano .env
```

**必须修改的配置**：
```ini
# 数据库密码（生产环境请使用强密码）
DB_PASSWORD=your_secure_password_here

# pgAdmin 密码
ADMIN_PASSWORD=your_admin_password_here

# CORS 允许的来源（多个用逗号分隔）
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 步骤 3：启动服务

```bash
# 一键启动所有服务
docker-compose up -d
```

### 步骤 4：验证安装

```bash
# 检查容器状态
docker-compose ps

# 应该看到：
# NAME                  STATUS          PORTS
# memory-hub-api        Up              0.0.0.0:8000->8000/tcp
# memory-hub-db         Up              5432/tcp
# memory-hub-pgadmin    Up              0.0.0.0:5050->80/tcp
```

```bash
# 测试 API 健康检查
curl http://localhost:8000/api/v1/health
```

**成功响应**：
```json
{
  "status": "ok",
  "database": "connected",
  "version": "0.1.0"
}
```

---

## 🔧 访问服务

### API 文档（Swagger UI）

📖 **地址**: http://localhost:8000/docs

**功能**：
- 可视化 API 接口
- 在线测试所有接口
- 自动生成请求示例

### API 接口

🔌 **基础地址**: http://localhost:8000/api/v1

**示例**：
```bash
# 创建智能体
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "小笔", "description": "文案专家"}'

# 创建记忆
curl -X POST http://localhost:8000/api/v1/memories \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "...", "content": "用户喜欢简洁", "memory_type": "preference"}'

# 搜索记忆
curl -X POST http://localhost:8000/api/v1/memories/search/text \
  -H "Content-Type: application/json" \
  -d '{"query": "用户偏好", "match_count": 5}'
```

### pgAdmin（数据库管理）

🛠️ **地址**: http://localhost:5050

**登录凭据**：
- 邮箱：`admin@memory.hub`（来自 .env 的 `ADMIN_EMAIL`）
- 密码：您在 .env 中设置的 `ADMIN_PASSWORD`

**连接数据库**：
1. 登录 pgAdmin
2. 右键 "Servers" → "Create" → "Server"
3. 配置：
   - **Name**: memory-hub
   - **Host**: memory-hub-db（Docker 服务名）
   - **Port**: 5432
   - **Username**: memory_user（来自 .env 的 `DB_USER`）
   - **Password**: 您在 .env 中设置的 `DB_PASSWORD`

---

## 📚 使用教程

### 第一个智能体

1. 打开 http://localhost:8000/docs
2. 找到 `POST /api/v1/agents`
3. 点击 "Try it out"
4. 填写：
```json
{
  "name": "小笔",
  "description": "文案专家，擅长写文章",
  "capabilities": ["写作", "翻译", "润色"]
}
```
5. 点击 "Execute"
6. **保存返回的 agent_id**

### 第一条记忆

1. 找到 `POST /api/v1/memories`
2. 填写（替换为你的 agent_id）：
```json
{
  "agent_id": "你的 agent_id",
  "content": "用户喜欢简洁的回答，讨厌废话",
  "memory_type": "preference",
  "importance": 0.8,
  "tags": ["用户偏好", "沟通风格"]
}
```
3. 点击 "Execute"

### 第一次搜索

1. 找到 `POST /api/v1/memories/search/text`
2. 填写：
```json
{
  "query": "用户喜欢什么？",
  "match_count": 5
}
```
3. 点击 "Execute"
4. 查看返回的记忆（即使查询词不同也能搜到！）

---

## 🛠️ 运维命令

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f api
docker-compose logs -f db
```

### 停止服务

```bash
# 停止并保留数据
docker-compose stop

# 停止并删除容器（数据保留）
docker-compose down
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart api
```

### 完全重置

```bash
# ⚠️ 警告：删除所有数据！
docker-compose down -v
docker-compose up -d
```

### 数据库备份

```bash
# 导出数据库
docker-compose exec db pg_dump -U memory_user memory_hub > backup.sql

# 导入数据库
docker-compose exec -T db psql -U memory_user memory_hub < backup.sql
```

---

## 🐛 常见问题

### 问题 1：端口被占用

**错误**: `Address already in use`

**解决**:
```bash
# 查看占用端口的进程
lsof -i :8000
lsof -i :5050

# 杀死进程
kill -9 <PID>

# 或修改端口
nano .env  # 修改 API_PORT=8001, ADMIN_PORT=5051
```

### 问题 2：Docker 权限问题

**错误**: `permission denied`

**解决**:
```bash
# 使用 sudo
sudo docker-compose up -d

# 或将用户加入 docker 组
sudo usermod -aG docker $USER
# 重新登录生效
newgrp docker
```

### 问题 3：容器启动失败

**检查日志**:
```bash
docker-compose logs api
```

**常见原因**:
- 数据库还没启动完成 → 等待 30 秒后重试
- 环境变量配置错误 → 检查 .env 文件
- 端口冲突 → 修改 .env 中的端口

### 问题 4：找不到记忆

**可能原因**:
- agent_id 不正确
- 记忆还没创建成功

**检查**:
```bash
# 列出所有智能体
curl http://localhost:8000/api/v1/agents

# 列出智能体的记忆
curl http://localhost:8000/api/v1/agents/<agent_id>/memories
```

---

## 📖 下一步

安装完成后，建议阅读：

1. **[QUICKSTART.md](docs/QUICKSTART.md)** - 5 分钟快速上手
2. **[USER_GUIDE.md](docs/USER_GUIDE.md)** - 详细使用说明
3. **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - 系统架构详解
4. **[API.md](docs/API.md)** - 完整 API 参考

---

## 💡 技术支持

- 📧 Email: [您的邮箱]
- 💬 Issues: https://github.com/wen41/memory-hub/issues
- 📚 文档：https://github.com/wen41/memory-hub/tree/master/docs

---

*Memory Hub v0.1.0 - 2026.03.14*
