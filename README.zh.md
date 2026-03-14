# 多智能体记忆中枢 (Multi-Agent Memory Hub)

> 专为多智能体协作设计的记忆管理系统

<p align="center">
  <img src="docs/images/hero-banner.png" alt="Memory Hub" width="100%">
</p>

<p align="center">
  <img src="logo/memory-hub-logo.png" alt="Logo" width="128" height="128">
</p>

<p align="center">
  <strong>让智能体拥有长期记忆，对话更懂你</strong>
</p>

<p align="center">
  <a href="https://github.com/hanhao/memory-hub">
    <img src="https://img.shields.io/badge/version-0.1.0-blue.svg" alt="Version">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </a>
  <a href="docker-compose.yml">
    <img src="https://img.shields.io/badge/docker-ready-brightgreen.svg" alt="Docker">
  </a>
</p>

---

## 📖 项目介绍

**多智能体记忆中枢 (Multi-Agent Memory Hub)** 是一个创新的记忆管理系统，专门为多智能体协作环境设计。它解决了传统 AI 智能体面临的"健忘症"问题，实现了跨智能体的知识共享和协同工作。

### 核心理念

在多智能体系统中，每个智能体都有自己的专业领域和技能，但它们往往缺乏有效的记忆共享机制。Memory Hub 作为中央记忆库，让所有智能体能够：

- 存储和检索重要信息
- 共享经验和知识
- 协同完成复杂任务
- 保持上下文一致性

### 为什么需要 Memory Hub？

传统的单智能体系统存在诸多局限：

- 🔴 **记忆孤立** - 每个智能体都独立记忆，信息无法共享
- 🔴 **上下文丢失** - 每次对话都从零开始，无法累积经验
- 🔴 **重复学习** - 相同的信息需要多次输入给不同智能体
- 🔴 **效率低下** - 缺乏长期记忆导致重复工作

Memory Hub 通过统一的记忆管理解决了这些问题。

---

## ✨ 核心特性

### 1. 双表隔离架构（私人记忆 + 共同记忆）

```
┌─────────────────────────────────────────────────────────┐
│                    记忆架构                              │
│                                                         │
│  ┌─────────────────┐    ┌─────────────────┐            │
│  │   私人记忆表     │    │   共同记忆表     │            │
│  │ (Private Table) │    │ (Shared Table)  │            │
│  │                 │    │                 │            │
│  │ • 小搜专属记忆  │    │ • 共享事实      │            │
│  │ • 小码代码经验  │    │ • 用户偏好      │            │
│  │ • 小笔文案技巧  │    │ • 项目信息      │            │
│  │ • 小析分析模型  │    │ • 通用知识      │            │
│  └─────────────────┘    └─────────────────┘            │
│                                                         │
│  智能体只能访问自己的私人记忆，但可以读写共同记忆        │
└─────────────────────────────────────────────────────────┘
```

- **私人记忆表**：每个智能体独有的记忆空间，存储个人经验和专有知识
- **共同记忆表**：所有智能体共享的记忆空间，存储通用信息和协作知识
- **数据隔离**：确保敏感信息不被其他智能体访问
- **协作机制**：通过共同记忆实现智能体间的信息同步

### 2. Hook 机制解决智能体失忆问题

Memory Hub 实现了独特的 Hook 机制，确保智能体在对话过程中不会"忘记"重要信息：

```
┌─────────────────────────────────────────────────────────┐
│                    Hook 机制                             │
│                                                         │
│  用户输入 → Hook 拦截 → 智能体处理 → Hook 记录 → 存储  │
│     ↓                                                 ↑
│   重要信息提取 ←───────────────────────────────────────┘
│     ↓
│   记忆关联 → 上下文注入 → 更智能的回复
│
│  工作流程：
│  1. 每次交互都会触发 Hook
│  2. 自动提取关键信息
│  3. 保存到相应记忆表
│  4. 后续对话自动关联相关记忆
└─────────────────────────────────────────────────────────┘
```

- **自动捕获**：无需手动操作，自动记录重要对话
- **智能分类**：根据内容类型自动归类到不同记忆类别
- **上下文关联**：后续对话能自动唤起相关记忆
- **防遗忘**：确保重要信息不会丢失

### 3. Orchestrator-Worker 模式

采用经典的 Orchestrator-Worker 架构，实现高效的智能体协作：

```
┌─────────────────────────────────────────────────────────┐
│                  Orchestrator-Worker                    │
│                                                         │
│  ┌─────────────┐                                        │
│  │ Orchestrator│                                        │
│  │  (调度器)   │                                        │
│  └──────┬──────┘                                        │
│         │                                               │
│    ┌────▼────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│    │ Worker  │  │ Worker  │  │ Worker  │  │ Worker  │  │
│    │  (小搜) │  │ (小码)  │  │ (小笔)  │  │ (小析)  │  │
│    └─────────┘  └─────────┘  └─────────┘  └─────────┘  │
│                                                         │
│  调度器负责：                                           │
│  - 任务分发                                            │
│  - 资源协调                                            │
│  - 记忆同步                                            │
│  - 错误处理                                            │
│                                                         │
│  工作者负责：                                           │
│  - 专业领域任务                                        │
│  - 个人记忆管理                                        │
│  - 与其他工作者协作                                    │
└─────────────────────────────────────────────────────────┘
```

### 4. 语义搜索能力

基于向量数据库的语义搜索，理解而非匹配：

- **向量化存储**：将文本转换为高维向量进行存储
- **相似度匹配**：找到语义相近而非关键词相同的内容
- **多语言支持**：支持中文、英文等多种语言
- **上下文感知**：考虑查询的上下文环境

### 5. 智能遗忘机制

模拟人类大脑的记忆规律：

- **重要性评分**：根据访问频率和内容重要性评分
- **自动清理**：定期清理低重要性记忆
- **保留策略**：重要记忆自动延长保存期限
- **版本管理**：保留记忆的演化历史

### 6. 8 个智能体手下

专门设计的 8 个专业智能体：

| 智能体 | 专长 | 记忆特点 |
|--------|------|----------|
| 小搜 🟢 | 信息采集 | 搜索技巧、知识库索引 |
| 小写 🟢 | 文案撰写 | 写作风格、语言技巧 |
| 小码 🟡 | 代码开发 | 编程技能、框架知识 |
| 小审 🔴 | 质量审核 | 检查标准、错误模式 |
| 小析 🟡 | 数据分析 | 统计方法、模型知识 |
| 小览 🟡 | 浏览器操作 | 页面解析、DOM 操作 |
| 小图 🎨 | 视觉设计 | 设计原理、美学标准 |
| 小排 📐 | 内容排版 | 排版规则、格式标准 |

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/wen41/memory-hub.git
cd memory-hub
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置（修改密码等）
nano .env
```

**必须修改的配置**：
- `DB_PASSWORD` - 数据库密码
- `ADMIN_PASSWORD` - pgAdmin 密码
- `ALLOWED_ORIGINS` - 允许的 CORS 来源

### 3. 启动服务

### 前置条件

- ✅ Docker & Docker Compose v2.0+
- ✅ Python 3.10+（仅本地开发需要）
- ✅ 8GB+ 内存（推荐 16GB）
- ✅ 2GB+ 空闲磁盘空间

### 安装步骤

#### 1️⃣ 克隆项目

```bash
git clone https://github.com/hanhao/memory-hub.git
cd memory-hub
```

#### 2️⃣ 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置（可选，默认配置即可用）
vim .env
```

#### 3️⃣ 一键启动

##### 方式一：傻瓜式启动（新手推荐）✨

专为新手设计，自动处理 Docker 权限和环境问题：

```bash
# 进入交互式菜单
./scripts/quick-start.sh

# 或直接启动
./scripts/quick-start.sh start
```

**特色功能：**
- ✅ 自动检查 Docker 安装和权限
- ✅ 自动处理权限问题
- ✅ 自动检查端口占用
- ✅ 自动创建 .env 文件
- ✅ 友好的交互式菜单

##### 方式二：标准启动

```bash
# 一键启动所有服务（数据库 + API + pgAdmin）
./scripts/start.sh start
```

**服务地址：**
- 📚 API 文档：http://localhost:8000/docs
- 🔌 API 接口：http://localhost:8000/api/v1
- 🗄️ 数据库：localhost:5432
- 🛠️ pgAdmin：http://localhost:5050

#### 4️⃣ 验证安装

```bash
# 检查服务状态
./scripts/start.sh status

# 测试 API
curl http://localhost:8000/health
```

### 配置

#### 环境变量详解

| 变量 | 默认值 | 说明 |
|------|--------|------|
| DB_HOST | localhost | 数据库主机 |
| DB_PORT | 5432 | 数据库端口 |
| DB_USER | memory_user | 数据库用户 |
| DB_PASSWORD | memory_pass_2026 | 数据库密码 |
| DB_NAME | memory_hub | 数据库名称 |
| API_HOST | 0.0.0.0 | API 监听地址 |
| API_PORT | 8000 | API 端口 |
| API_DEBUG | false | 调试模式 |
| EMBEDDING_MODEL | text-embedding-v4 | 嵌入模型 |
| EMBEDDING_DIMENSION | 1024 | 向量维度 |
| DASHSCOPE_API_KEY | - | 阿里云 DashScope API Key |
| MEMORY_PRIVATE_TABLE | private_memories | 私人记忆表名 |
| MEMORY_SHARED_TABLE | shared_memories | 共同记忆表名 |
| HOOK_ENABLED | true | 启用 Hook 机制 |
| HOOK_TIMEOUT | 30 | Hook 超时时间（秒） |

### 运行

启动后，Memory Hub 会自动运行以下服务：

- **API 服务**：提供 RESTful 接口
- **数据库服务**：PostgreSQL + pgvector
- **向量引擎**：处理语义搜索
- **Hook 服务**：监听智能体交互
- **调度服务**：Orchestrator-Worker 管理

---

## 📁 项目结构

```
memory-hub/
├── docker-compose.yml          # Docker 编排配置
├── .env.example               # 环境变量模板
├── .gitignore                 # Git 忽略配置
├── LICENSE                    # 许可证文件
├── README.md                  # 英文文档
├── README.zh.md               # 中文文档
│
├── backend/                   # 后端代码
│   ├── Dockerfile             # API 服务镜像
│   ├── requirements.txt       # Python 依赖
│   └── app/
│       ├── main.py            # FastAPI 应用入口
│       ├── config.py          # 配置管理
│       ├── database.py        # 数据库连接
│       ├── models/            # 数据模型
│       │   ├── agent.py       # 智能体模型
│       │   ├── memory.py      # 记忆模型
│       │   └── hook.py        # Hook 模型
│       ├── api/               # API 路由
│       │   ├── agents.py      # 智能体接口
│       │   ├── memories.py    # 记忆接口
│       │   ├── hooks.py       # Hook 接口
│       │   └── orchestrator.py # 调度接口
│       └── services/          # 业务服务
│           ├── memory_service.py # 记忆服务
│           ├── agent_service.py  # 智能体服务
│           └── hook_service.py   # Hook 服务
│
├── scripts/                   # 脚本
│   ├── start.sh               # 一键启动脚本
│   ├── quick-start.sh         # 傻瓜式启动脚本
│   ├── backup.sh              # 数据库备份脚本
│   ├── health-check.sh        # 健康检查脚本
│   └── init-db.sql            # 数据库初始化
│
├── docs/                      # 文档目录
│   ├── QUICKSTART.md          # 5 分钟上手指南
│   ├── USER_GUIDE.md          # 用户使用手册
│   ├── ARCHITECTURE.md        # 架构设计文档
│   ├── API.md                 # API 参考手册
│   └── HOOK_MECHANISM.md      # Hook 机制详解
│
├── logo/                      # Logo 图片
│   └── memory-hub-logo.png
│
├── tests/                     # 测试文件
│   ├── unit/                  # 单元测试
│   ├── integration/           # 集成测试
│   └── conftest.py            # 测试配置
│
└── docker/                    # Docker 相关
    ├── db.Dockerfile          # 数据库镜像
    ├── api.Dockerfile         # API 服务镜像
    └── docker-compose.yml     # 服务编排
```

### 关键目录说明

- **backend/app/models/** - 数据模型定义，包括智能体、记忆、Hook 等核心实体
- **backend/app/api/** - RESTful API 接口，提供对外服务
- **backend/app/services/** - 业务逻辑层，处理复杂的业务流程
- **scripts/** - 自动化脚本，简化日常操作
- **docs/** - 详细文档，包含使用指南和开发说明

---

## 🧠 架构设计

### 系统架构图

<p align="center">
  <img src="docs/images/architecture-diagram.png" alt="Architecture" width="100%">
</p>

### 整体架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        智能体层 (Agents Layer)                           │
│                                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │ 小搜    │  │ 小码    │  │ 小笔    │  │ 小析    │  │ 小审    │      │
│  │ (搜索)  │  │ (代码)  │  │ (文案)  │  │ (分析)  │  │ (审核)  │      │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘      │
│       │            │            │            │            │            │
└───────┼────────────┼────────────┼────────────┼────────────┼────────────┘
        │            │            │            │            │
        └────────────┴─────┬──────┴────────────┴────────────┘
                           │ HTTP API + Hook
                  ┌────────▼────────┐
                  │   Memory Hub    │
                  │   (Orchestrator)│
                  │   FastAPI +     │
                  │   PostgreSQL    │
                  └────────┬────────┘
                           │
              ┌────────────┴────────────┐
              │    数据库层 (Database)    │
              │                         │
              │  ┌─────────────────────┐ │
              │  │   Private Table     │ │
              │  │  (私人记忆表)       │ │
              │  │                     │ │
              │  │ • Agent-specific    │ │
              │  │ • Isolated storage  │ │
              │  │ • Security ensured  │ │
              │  └─────────────────────┘ │
              │                         │
              │  ┌─────────────────────┐ │
              │  │   Shared Table      │ │
              │  │  (共同记忆表)       │ │
              │  │                     │ │
              │  │ • Cross-agent       │ │
              │  │ • Knowledge sharing │ │
              │  │ • Collaboration     │ │
              │  └─────────────────────┘ │
              └───────────────────────────┘
```

### 核心组件

#### 1. Orchestrator（调度器）

- **智能体管理**：注册、注销、状态监控
- **任务分发**：根据能力分配任务给合适的智能体
- **记忆协调**：管理智能体间的数据交换
- **错误处理**：异常恢复和容错机制

#### 2. Hook 机制

- **事件监听**：捕获智能体的所有交互
- **信息提取**：自动识别重要信息
- **记忆存储**：将信息分类存储到相应表
- **上下文注入**：为后续交互提供上下文

#### 3. 双表存储系统

- **私人表**：每个智能体独享，存储专有知识
- **共同表**：所有智能体共享，存储通用信息
- **权限控制**：严格的访问权限管理
- **性能优化**：针对不同类型查询优化

#### 4. 语义搜索引擎

- **向量嵌入**：使用先进模型生成向量表示
- **相似度计算**：高效的相关性匹配算法
- **多语言支持**：支持中文、英文等语言
- **实时索引**：动态更新搜索索引

### 记忆类型

Memory Hub 支持四种记忆类型：

| 类型 | 英文 | 示例 | 存储位置 |
|------|------|------|----------|
| 📌 事实 | fact | "用户叫憨货，住在上海" | 共同表 |
| ❤️ 偏好 | preference | "喜欢简洁的回答，讨厌废话" | 共同表 |
| 🛠️ 技能 | skill | "会写 Python 代码，擅长数据分析" | 私人表 |
| 📖 经验 | experience | "上次用户遇到问题，用方案 A 解决了" | 共同表 |

### 数据流向

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        数据流向图                                       │
│                                                                         │
│  用户输入 → Hook 拦截 → 智能体处理 → 记忆提取 → 上下文注入 → 智能回复   │
│     │          │          │          │          │          │           │
│     │          │          │          │          │          │           │
│     ▼          ▼          ▼          ▼          ▼          ▼           │
│  输入验证   信息提取    任务执行   语义搜索   记忆关联   输出生成        │
│     │          │          │          │          │          │           │
│     └──────────┴──────────┴──────────┴──────────┴──────────┘           │
│                                                                         │
│  存储流程：                                                              │
│  1. Hook 识别重要信息 → 分类 → 存储到对应表                              │
│  2. 智能体查询记忆 → 语义搜索 → 返回相关结果                             │
│  3. 上下文组装 → 注入到当前对话 → 生成个性化回复                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 使用示例

### 示例 1：创建智能体

```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "小笔",
    "description": "文案专家，擅长写文章",
    "capabilities": ["写作", "翻译", "润色"],
    "metadata": {"team_id": "003"}
  }'
```

**响应：**
```json
{
  "message": "智能体创建成功，ID: 550e8400-e29b-41d4-a716-446655440000",
  "agent_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 示例 2：创建私人记忆

```bash
curl -X POST http://localhost:8000/api/v1/memories/private \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "550e8400-e29b-41d4-a716-446655440000",
    "content": "我在写一篇关于AI的文章，标题是《智能未来》",
    "memory_type": "experience",
    "importance": 0.9,
    "tags": ["写作", "AI", "文章"]
  }'
```

### 示例 3：创建共同记忆

```bash
curl -X POST http://localhost:8000/api/v1/memories/shared \
  -H "Content-Type: application/json" \
  -d '{
    "content": "用户喜欢简洁的回答，讨厌废话",
    "memory_type": "preference",
    "importance": 0.8,
    "tags": ["用户偏好", "沟通风格"]
  }'
```

### 示例 4：语义搜索记忆

```bash
curl -X POST http://localhost:8000/api/v1/memories/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "用户喜欢什么样的回答？",
    "limit": 5,
    "memory_types": ["preference"],
    "access_level": "shared"
  }'
```

**响应：**
```json
[
  {
    "id": "记忆 ID",
    "content": "用户喜欢简洁的回答，讨厌废话",
    "similarity": 0.92,
    "memory_type": "preference",
    "importance": 0.8,
    "access_count": 15,
    "created_at": "2026-03-14T10:00:00Z"
  }
]
```

### 示例 5：增强对话（核心功能）🚀

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "550e8400-e29b-41d4-a716-446655440000",
    "session_id": "session_123",
    "user_message": "你好，帮我写个关于 AI 的文案",
    "use_memory": true,
    "use_history": true,
    "auto_extract": true,
    "memory_context": {
      "private_only": false,
      "shared_only": false,
      "include_tags": ["AI", "写作"],
      "min_importance": 0.5
    }
  }'
```

**工作流程：**
1. Hook 拦截用户输入
2. 检索相关私人记忆（小笔的写作经验）
3. 检索相关共同记忆（用户偏好、历史交互）
4. 用 LLM 生成个性化回复
5. Hook 自动记录对话和提取新记忆

### 示例 6：智能体协作

```bash
curl -X POST http://localhost:8000/api/v1/orchestration \
  -H "Content-Type: application/json" \
  -d '{
    "task": "帮我分析一下市场趋势，然后写一份报告",
    "preferred_agents": ["小析", "小笔"],
    "requirements": {
      "analysis_depth": "deep",
      "report_style": "professional"
    },
    "collaboration_enabled": true
  }'
```

**协作流程：**
1. 调度器分析任务需求
2. 分配给小析进行数据分析
3. 小析查询共同记忆获取历史数据
4. 小析完成分析并存储结果到共同表
5. 调度器分配给小笔写报告
6. 小笔查询共同表获取分析结果
7. 小笔生成最终报告

### 示例 7：Hook 机制演示

当智能体与用户交互时，Hook 会自动执行：

```bash
# Hook 拦截到的事件
{
  "event_type": "conversation",
  "agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_input": "我想要一个简洁的回答",
  "response": "好的，我会提供简洁的回复",
  "timestamp": "2026-03-14T10:30:00Z",
  "extracted_info": [
    {
      "type": "preference",
      "content": "用户喜欢简洁的回答",
      "confidence": 0.95
    }
  ]
}
```

---

## 🔧 配置说明

### 环境变量配置

#### 基础配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| DB_HOST | localhost | 数据库主机地址 |
| DB_PORT | 5432 | 数据库端口 |
| DB_USER | memory_user | 数据库用户名 |
| DB_PASSWORD | memory_pass_2026 | 数据库密码 |
| DB_NAME | memory_hub | 数据库名称 |
| API_HOST | 0.0.0.0 | API 服务监听地址 |
| API_PORT | 8000 | API 服务端口 |

#### 记忆系统配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| EMBEDDING_MODEL | text-embedding-v4 | 向量嵌入模型 |
| EMBEDDING_DIMENSION | 1024 | 向量维度 |
| MEMORY_PRIVATE_TABLE | private_memories | 私人记忆表名 |
| MEMORY_SHARED_TABLE | shared_memories | 共同记忆表名 |
| MEMORY_MAX_SIZE | 100000 | 单表最大记录数 |
| MEMORY_RETENTION_DAYS | 365 | 记忆保留天数 |

#### Hook 机制配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| HOOK_ENABLED | true | 是否启用 Hook |
| HOOK_TIMEOUT | 30 | Hook 超时时间（秒） |
| HOOK_BATCH_SIZE | 10 | 批量处理大小 |
| HOOK_RETRY_ATTEMPTS | 3 | 重试次数 |

#### 智能体配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| AGENT_MAX_CONCURRENT | 10 | 最大并发智能体数 |
| AGENT_IDLE_TIMEOUT | 300 | 智能体空闲超时（秒） |
| AGENT_HEARTBEAT_INTERVAL | 60 | 心跳间隔（秒） |

### 数据库配置

#### PostgreSQL + pgvector

Memory Hub 使用 PostgreSQL 作为主数据库，并集成 pgvector 扩展以支持向量搜索：

```sql
-- 启用 pgvector 扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- 私人记忆表结构
CREATE TABLE private_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1024),
    memory_type VARCHAR(50),
    importance FLOAT DEFAULT 0.5,
    access_count INTEGER DEFAULT 0,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    INDEX idx_agent_id (agent_id),
    INDEX idx_memory_type (memory_type),
    INDEX idx_embedding USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)
);

-- 共同记忆表结构
CREATE TABLE shared_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding vector(1024),
    memory_type VARCHAR(50),
    importance FLOAT DEFAULT 0.5,
    access_count INTEGER DEFAULT 0,
    tags TEXT[],
    created_by UUID,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    INDEX idx_memory_type (memory_type),
    INDEX idx_embedding USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)
);
```

#### 性能优化建议

1. **向量索引优化**：
   - 根据数据量调整 `lists` 参数
   - 定期 `REINDEX` 向量索引

2. **内存配置**：
   - 增加 `shared_buffers` 到内存的 25%
   - 调整 `work_mem` 以优化查询性能

3. **连接池**：
   - 使用连接池减少连接开销
   - 合理设置最大连接数

### 生产环境部署配置

#### 安全配置

```bash
# .env.production
API_DEBUG=false
API_LOG_LEVEL=WARNING
DB_SSL_MODE=require
CORS_ORIGINS=https://yourdomain.com
SECRET_KEY=your-very-long-secret-key-here
ADMIN_PASSWORD=strong-admin-password
```

#### 性能配置

```bash
# .env.production
WORKER_COUNT=4
MAX_WORKERS=8
THREAD_COUNT=100
CONNECTION_POOL_SIZE=20
QUERY_TIMEOUT=30
MAX_REQUEST_SIZE=10MB
```

#### 监控配置

```bash
# .env.production
METRICS_ENABLED=true
LOG_LEVEL=INFO
HEALTH_CHECK_INTERVAL=30
ALERT_THRESHOLD_ERROR_RATE=0.05
ALERT_THRESHOLD_LATENCY_MS=1000
```

---

## 🤝 贡献指南

我们欢迎各种形式的贡献！以下是参与项目的几种方式：

### 1. 代码贡献

#### 开发环境搭建

```bash
# 1. 克隆项目
git clone https://github.com/hanhao/memory-hub.git
cd memory-hub

# 2. 创建开发分支
git checkout -b feature/your-feature-name

# 3. 启动开发环境
./scripts/start.sh dev
```

#### 代码规范

- **Python**: 遵循 PEP 8 规范
- **Git 提交**: 使用约定式提交 (Conventional Commits)
- **文档**: 保持文档与代码同步更新
- **测试**: 确保 100% 代码覆盖率

#### 提交信息格式

```
feat: 添加新的智能体协作功能
^--^  ^-----------------------^
|     |
|     +-> 简短描述变更内容
|
+-------> 类型: feat|fix|docs|style|refactor|test|chore
```

### 2. 文档改进

- 修复错别字和语法错误
- 补充缺失的使用示例
- 更新过时的配置说明
- 添加最佳实践指南

### 3. 问题反馈

- 提交 Bug 报告
- 提出功能建议
- 分享使用心得
- 参与技术讨论

### 4. 社区建设

- 帮助解答用户问题
- 编写教程和案例
- 推广项目使用
- 组织线下活动

### 开发流程

```bash
# 1. Fork 仓库
# 2. 克隆代码
git clone https://github.com/your-username/memory-hub.git

# 3. 创建特性分支
git checkout -b feature/amazing-feature

# 4. 编写代码和测试
# 5. 运行测试
cd backend && pytest tests/

# 6. 提交更改
git add .
git commit -m "feat: 添加 amazing feature"

# 7. 推送分支
git push origin feature/amazing-feature

# 8. 提交 PR
# 在 GitHub 界面创建 Pull Request
```

### 代码审查标准

- **功能完整性**: 代码是否实现了预期功能
- **代码质量**: 是否遵循编码规范
- **性能影响**: 是否有性能问题
- **安全性**: 是否存在安全漏洞
- **可维护性**: 代码是否易于理解和维护
- **测试覆盖**: 是否有足够的测试用例

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

### MIT 许可证条款

MIT License

Copyright (c) 2026 Han Hao

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### 许可证说明

- ✅ **商业使用**: 允许用于商业项目
- ✅ **修改**: 可以修改源代码
- ✅ **分发**: 可以重新分发
- ✅ **私用**: 可以用于私有项目
- ❗ **保留版权**: 必须保留原始版权声明
- ❗ **无担保**: 软件按"原样"提供，不提供任何担保

---

## 🙏 致谢

感谢以下开源项目和社区的支持：

### 核心依赖

- [FastAPI](https://fastapi.tiangolo.com/) - 现代高性能 Web 框架
- [pgvector](https://github.com/pgvector/pgvector) - PostgreSQL 向量扩展
- [Pydantic](https://pydantic-docs.helpmanual.io/) - 数据验证库
- [DashScope](https://dashscope.aliyun.com/) - 阿里云通义千问 API
- [Docker](https://www.docker.com/) - 容器化解决方案
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL 工具包

### 工具链

- [pytest](https://docs.pytest.org/) - 测试框架
- [black](https://github.com/psf/black) - 代码格式化工具
- [flake8](https://flake8.pycqa.org/) - 代码风格检查
- [mypy](https://mypy.readthedocs.io/) - 静态类型检查
- [uvicorn](https://www.uvicorn.org/) - ASGI 服务器

### 特别感谢

- **Han Hao (憨货)** - 项目发起人和主要贡献者
- **傻妞团队** - 项目管理和整体架构设计
- **小码团队** - 核心开发和文档编写
- **所有贡献者** - 代码、文档、测试和反馈

---

> 💡 **提示**：如需技术支持，请联系憨货或傻妞团队，我们致力于为用户提供最优质的体验！

---

*多智能体记忆中枢 v0.1.0 - 2026.03.14*
