# 更新日志 (CHANGELOG)

所有重要的项目变更都会记录在这个文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [0.1.0] - 2026-03-14

### ✨ 新增
- 多智能体记忆管理系统核心功能
- 双表隔离架构（私人记忆 + 共同记忆）
- RESTful API（创建智能体、记忆、搜索等）
- Docker 一键部署
- 完整的 API 文档（Swagger UI）
- 语义搜索功能
- 智能记忆提取（异步后台任务）

### 🏗️ 架构
- PostgreSQL + pgvector 向量数据库
- FastAPI 后端服务
- 多租户支持
- 记忆分类逻辑

### 📚 文档
- README.md / README.zh.md（中英文文档）
- docs/INSTALL.md（安装指南）
- docs/QUICKSTART.md（快速开始）
- docs/API.md（API 参考）
- docs/ARCHITECTURE.md（架构设计）
- docs/USER_GUIDE.md（用户指南）

### 🔧 技术栈
- 后端：Python 3.10+, FastAPI
- 数据库：PostgreSQL 15, pgvector
- 部署：Docker, Docker Compose
- 嵌入模型：bge-small-zh-v1.5 (1024 维)

### 🐛 修复
- 修复对话记忆提取失败问题
- 增加 LLM API 超时时间并优化错误日志
- 更新向量维度为 1024 (text-embedding-v4)

---

## [Unreleased]

### 待添加
- 更多文档和示例
- 性能优化
- 单元测试和集成测试

---

## 版本说明

- **[0.1.0]** - 首个开源版本，包含核心功能和完整文档