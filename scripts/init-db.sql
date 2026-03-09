-- ============================================================
-- 多智能体记忆中枢 - 数据库初始化脚本
-- ============================================================
-- 功能：创建向量扩展、数据表、索引
-- 作者：小码
-- 日期：2026-03-05
-- ============================================================

-- 启用 pgvector 扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================
-- 核心数据表
-- ============================================================

-- 智能体表：记录所有接入的智能体
CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    capabilities TEXT[],  -- 智能体能力标签数组
    metadata JSONB DEFAULT '{}',  -- 额外元数据
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 记忆条目表：存储智能体的记忆
CREATE TABLE IF NOT EXISTS memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    
    -- 记忆内容
    content TEXT NOT NULL,  -- 记忆文本内容
    
    -- 向量嵌入（用于语义搜索）
    -- dimension=1024 对应 text-embedding-v4 (DashScope)
    embedding vector(1024),
    
    -- 元数据
    memory_type VARCHAR(50) DEFAULT 'fact',  -- fact, preference, skill, experience
    importance FLOAT DEFAULT 0.5,  -- 重要性分数 0-1
    access_count INTEGER DEFAULT 0,  -- 访问次数（用于遗忘机制）
    
    -- 时间信息
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,  -- 过期时间（可选）
    
    -- 标签和分类
    tags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}'
);

-- 记忆关联表：记忆之间的关系
CREATE TABLE IF NOT EXISTS memory_relations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_memory_id UUID NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
    target_memory_id UUID NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
    relation_type VARCHAR(50) NOT NULL,  -- similar, contradicts, derives_from, etc.
    confidence FLOAT DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(source_memory_id, target_memory_id, relation_type)
);

-- 会话表：记录智能体的会话上下文
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    session_key VARCHAR(255) NOT NULL,  -- 会话标识
    context JSONB DEFAULT '{}',  -- 会话上下文
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(agent_id, session_key)
);

-- ============================================================
-- 索引优化
-- ============================================================

-- 智能体查询索引
CREATE INDEX IF NOT EXISTS idx_agents_name ON agents(name);
CREATE INDEX IF NOT EXISTS idx_agents_created_at ON agents(created_at DESC);

-- 记忆查询索引
CREATE INDEX IF NOT EXISTS idx_memories_agent_id ON memories(agent_id);
CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(memory_type);
CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance DESC);
CREATE INDEX IF NOT EXISTS idx_memories_created_at ON memories(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_memories_tags ON memories USING GIN(tags);

-- 向量索引（用于相似性搜索）
-- HNSW 索引：高性能近似最近邻搜索
CREATE INDEX IF NOT EXISTS idx_memories_embedding ON memories 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 会话索引
CREATE INDEX IF NOT EXISTS idx_sessions_agent_id ON sessions(agent_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);

-- ============================================================
-- 辅助函数
-- ============================================================

-- 向量相似性搜索函数
CREATE OR REPLACE FUNCTION search_similar_memories(
    query_embedding vector(1024),
    target_agent_id UUID DEFAULT NULL,
    match_threshold FLOAT DEFAULT 0.7,
    match_count INTEGER DEFAULT 10
)
RETURNS TABLE (
    id UUID,
    agent_id UUID,
    content TEXT,
    similarity FLOAT,
    memory_type VARCHAR(50),
    importance FLOAT,
    tags TEXT[]
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id,
        m.agent_id,
        m.content,
        1 - (m.embedding <=> query_embedding) AS similarity,
        m.memory_type,
        m.importance,
        m.tags
    FROM memories m
    WHERE 
        (target_agent_id IS NULL OR m.agent_id = target_agent_id)
        AND 1 - (m.embedding <=> query_embedding) > match_threshold
    ORDER BY m.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- 记忆遗忘函数：删除过期的低重要性记忆
CREATE OR REPLACE FUNCTION cleanup_old_memories(
    days_old INTEGER DEFAULT 30,
    min_importance FLOAT DEFAULT 0.3,
    max_access_count INTEGER DEFAULT 3
)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM memories
    WHERE 
        created_at < CURRENT_TIMESTAMP - (days_old || ' days')::interval
        AND importance < min_importance
        AND access_count < max_access_count;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$;

-- 更新时间戳触发器
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_agents_updated_at
    BEFORE UPDATE ON agents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- 初始化数据
-- ============================================================

-- 插入默认智能体（如果不存在）
INSERT INTO agents (name, description, capabilities)
VALUES ('system', '系统默认智能体', ARRAY['system', 'admin'])
ON CONFLICT DO NOTHING;

-- ============================================================
-- 注释
-- ============================================================

COMMENT ON TABLE agents IS '智能体注册表：记录所有接入记忆中枢的智能体';
COMMENT ON TABLE memories IS '记忆条目：存储智能体的各类记忆，支持向量搜索';
COMMENT ON TABLE memory_relations IS '记忆关联：记录记忆之间的语义关系';
COMMENT ON TABLE sessions IS '会话管理：存储智能体的会话上下文';

COMMENT ON COLUMN memories.embedding IS '记忆内容的向量嵌入，用于语义相似性搜索';
COMMENT ON COLUMN memories.importance IS '重要性分数，用于遗忘机制';
COMMENT ON COLUMN memories.access_count IS '访问次数，用于判断记忆活跃度';

-- 输出完成信息
DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE '数据库初始化完成！';
    RAISE NOTICE '已创建表：agents, memories, memory_relations, sessions';
    RAISE NOTICE '已创建向量索引：idx_memories_embedding';
    RAISE NOTICE '已创建搜索函数：search_similar_memories';
    RAISE NOTICE '========================================';
END $$;