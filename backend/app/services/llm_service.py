# ============================================================
# 多智能体记忆中枢 - LLM 调用服务
# ============================================================
# 功能：调用 LLM API 生成文本（用于对话增强）
# 作者：小码
# 日期：2026-03-06
# 更新：2026-03-09 - 改用 HTTP API 支持 Coding API Key
# ============================================================

import logging
from typing import List, Dict, Any, Optional
import httpx

from ..config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """LLM 调用服务：使用 HTTP API 生成文本"""
    
    def __init__(self):
        self.model_name = settings.LLM_MODEL
        # 使用专门的 LLM API Key（对话增强）
        self.api_key = settings.DASHSCOPE_LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL
        
        if not self.api_key:
            logger.warning("DASHSCOPE_LLM_API_KEY 未配置，LLM 服务可能不可用")
        else:
            logger.info(f"LLMService 初始化完成，模型: {self.model_name}, URL: {self.base_url}")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        调用 LLM 进行对话补全
        
        Args:
            messages: 消息列表，格式为 [{"role": "user/assistant", "content": "..."}]
            temperature: 温度参数，控制随机性（0-1）
            max_tokens: 最大生成 token 数
            system_prompt: 系统提示词（可选）
        
        Returns:
            生成的文本
        
        Raises:
            ValueError: API 调用失败
        """
        if not self.api_key:
            raise ValueError("DASHSCOPE_LLM_API_KEY 未配置")
        
        # 构建消息列表
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        try:
            logger.info(f"开始 LLM 调用，消息数: {len(full_messages)}")
            
            # 使用 HTTP API 调用
            url = f"{self.base_url}/chat/completions"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model_name,
                "messages": full_messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    error_msg = f"LLM API 调用失败: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                logger.info(f"✅ LLM 生成成功，内容长度: {len(content)}")
                return content
        
        except Exception as e:
            logger.error(f"❌ LLM 调用失败: {e}", exc_info=True)
            raise ValueError(f"LLM 调用失败: {str(e)}")
    
    async def generate_enhanced_reply(
        self,
        user_message: str,
        memories: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        基于记忆生成增强回复
        
        Args:
            user_message: 用户消息
            memories: 相关记忆列表
            conversation_history: 对话历史（可选）
        
        Returns:
            增强后的 AI 回复
        """
        # 构建系统提示词
        system_prompt = """你是一个有记忆的 AI 助手。你会基于记忆库中的相关信息来回复用户。

重要规则：
1. 优先使用记忆中的信息来个性化回复
2. 如果记忆中有用户的偏好、习惯或重要信息，要在回复中体现出来
3. 保持自然、友好的对话风格
4. 不要在回复中明确提及"根据我的记忆"或"记忆库中显示"，而是自然地融入对话"""

        # 构建记忆上下文
        memory_context = ""
        if memories:
            memory_context = "\n\n【相关记忆】\n"
            for i, mem in enumerate(memories[:5], 1):  # 最多使用 5 条相关记忆
                content = mem.get("content", "")
                mem_type = mem.get("memory_type", "unknown")
                memory_context += f"{i}. [{mem_type}] {content}\n"
        
        # 构建对话历史上下文
        history_context = ""
        if conversation_history:
            history_context = "\n\n【对话历史】\n"
            for msg in conversation_history[-6:]:  # 最近 3 轮对话
                role = "用户" if msg.get("role") == "user" else "AI"
                history_context += f"{role}: {msg.get('content', '')}\n"
        
        # 构建完整消息
        full_prompt = f"""{memory_context}{history_context}

【当前用户消息】
{user_message}

请基于以上信息，给出个性化的回复。"""
        
        messages = [{"role": "user", "content": full_prompt}]
        
        return await self.chat_completion(
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=1000
        )


# 全局服务实例
llm_service = LLMService()